#!/usr/bin/env python3
"""Copy budget checker for eyal-visualization-v2 dashboards.

Usage
  python3 scripts/copy-check.py dashboard.html [more.html ...]
  python3 scripts/copy-check.py --kind action-reason --text "193 sessions, 92% agreement."
  render_strings.sh | python3 scripts/copy-check.py --kind insight-bullet

File mode parses the static HTML and prints one PASS / FAIL line per capped
surface. Exits 1 if anything is over budget, so the agent must cut before
showing the artifact.

Limitation: copy built in JS (`insightBox.textContent = ...`, KPI details,
action cards rendered from DATA) is not in the static HTML, so file mode cannot
see it. Check those with --kind, passing the rendered strings.

Budgets (SKILL.md "Copy budget"):
  hero subtitle    .subtitle                    35 words, max 2 sentences
  hero eyebrow     .hero-badge                   4 words
  hero chip        .badge in hero                4 words each, max 3 chips

Chips are also checked on content: a tool or pipeline name, a commit hash, a
service / table slug, or three `·`-joined segments fails regardless of length.
That is Methodology content, not hero content.
  card body        .action-reason               20 words, max 1 sentence
  scored row body  .row-reason                  20 words, max 1 sentence
  insight bullet   li inside .insight           18 words
  insight block    .insight with no li          54 words (3 bullets' worth)
  KPI caption      .kpi-caption / .kpi-detail    8 words
"""

import re
import sys
from html.parser import HTMLParser

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
SKIP_TEXT_IN = {"script", "style", "template"}

# class name -> budget key
CLASS_KIND = {
    "subtitle": "subtitle",
    "hero-badge": "hero-badge",
    "badge": "badge",
    "action-reason": "action-reason",
    "row-reason": "row-reason",
    "kpi-caption": "kpi-caption",
    "kpi-detail": "kpi-caption",
}

WORD_BUDGET = {
    "subtitle": 35,
    "hero-badge": 4,
    "badge": 4,
    "action-reason": 20,
    "row-reason": 20,
    "kpi-caption": 8,
    "insight-bullet": 18,
    "insight-block": 54,
}
SENTENCE_BUDGET = {
    "subtitle": 2,
    "action-reason": 1,
    "row-reason": 1,
}
MAX_HERO_CHIPS = 3

# Chips and captions are label fragments, not prose.
LABELS = {"hero-badge", "badge", "kpi-caption"}

# A chip carries scope / window / n / freshness. Method never gets promoted to
# the hero, so these are rejected on content and not just on length.
CHIP_KINDS = {"hero-badge", "badge"}
STACK_WORDS = {
    "trino", "xmla", "dax", "presto", "airflow", "dbt", "snowflake",
    "bigquery", "spark", "quix", "petri", "kafka", "athena", "redshift",
    "tableau", "powerbi", "looker", "sql", "etl", "dag", "ctas", "mdx",
}
# Hex letters AND digits, so a plain numeric ID (Experiment 5073656) is fine
# but a commit sha (a7bbfca8) is not.
HASH_RE = re.compile(r"^(?=.*[a-f])(?=.*\d)[0-9a-f]{7,40}$", re.I)
SLUG_RE = re.compile(r"^[a-z]+(?:[-_][a-z]+){1,}$")


def chip_content_problem(text):
    """Return a reason string when a chip carries method instead of scope."""
    if text.count("\u00b7") >= 2:
        return "3+ segments in one chip"
    for raw in re.split(r"[\s\u00b7,]+", text):
        token = raw.strip(".,:;()[]").lower()
        if not token:
            continue
        if token in STACK_WORDS:
            return "tool / pipeline name %r" % token
        if HASH_RE.match(token):
            return "looks like a hash %r" % token
        if SLUG_RE.match(token) and token not in ("logged-in", "multi-site", "self-service", "opted-in"):
            return "looks like a service / table slug %r" % token
    return None


def count_words(text):
    return len([t for t in text.split() if re.search(r"[0-9A-Za-z]", t)])


def count_sentences(text):
    text = text.strip()
    if not text:
        return 0
    return max(1, len(re.findall(r"[.!?](?:\s|$)", text)))


def shorten(text, width=52):
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 1] + "\u2026"


def report(kind, label, text):
    """Print one PASS / FAIL line. Returns 1 when over budget."""
    words = count_words(text)
    budget = WORD_BUDGET[kind]
    ok = words <= budget
    note = ""

    if kind not in LABELS and kind in SENTENCE_BUDGET:
        sentences = count_sentences(text)
        if sentences > SENTENCE_BUDGET[kind]:
            ok = False
            note = "%d sentences / %d" % (sentences, SENTENCE_BUDGET[kind])

    if kind in CHIP_KINDS:
        problem = chip_content_problem(text)
        if problem:
            ok = False
            note = problem

    print("%-4s %-22s %3dw / %-4s %-20s %s" % (
        "PASS" if ok else "FAIL", label, words, budget, note, shorten(text)))
    return 0 if ok else 1


class CopyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.found = []
        self.open_targets = []

    def _classes(self, attrs):
        for name, value in attrs:
            if name == "class" and value:
                return value.split()
        return []

    def _inside_class(self, needle):
        return any(needle in classes for _, classes in self.stack)

    def handle_starttag(self, tag, attrs):
        classes = self._classes(attrs)
        self.stack.append((tag, classes))
        if tag in VOID:
            self.stack.pop()
            return

        kind = None
        for cls in classes:
            if cls in CLASS_KIND:
                kind = CLASS_KIND[cls]
                break
            if cls == "insight":
                kind = "insight-block"
                break
        if kind is None and tag == "li" and self._inside_class("insight"):
            kind = "insight-bullet"

        if kind:
            self.open_targets.append({
                "kind": kind,
                "depth": len(self.stack),
                "text": [],
                "in_hero": self._inside_class("hero-geometric"),
                "has_li": False,
            })

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        self._close_deeper_than(len(self.stack))
        if self.stack:
            self.stack.pop()
        self._close_deeper_than(len(self.stack))

    def _close_deeper_than(self, depth):
        while self.open_targets and self.open_targets[-1]["depth"] > depth:
            self.found.append(self.open_targets.pop())

    def handle_data(self, data):
        if any(tag in SKIP_TEXT_IN for tag, _ in self.stack):
            return
        if self.open_targets and self.stack and self.stack[-1][0] == "li":
            for target in self.open_targets:
                if target["kind"] == "insight-block":
                    target["has_li"] = True
        for target in self.open_targets:
            target["text"].append(data)

    def close(self):
        super().close()
        while self.open_targets:
            self.found.append(self.open_targets.pop())


def check_file(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
    except OSError as err:
        print("cannot read %s: %s" % (path, err))
        return 1

    parser = CopyParser()
    parser.feed(source)
    parser.close()

    print("\n" + path)
    print("-" * len(path))

    failures = 0
    seen = {}
    hero_chips = 0

    for item in parser.found:
        kind = item["kind"]
        text = " ".join(item["text"]).strip()
        if not text:
            continue
        # A bulleted insight is judged bullet by bullet, not as a block.
        if kind == "insight-block" and item["has_li"]:
            continue
        if kind == "badge" and item["in_hero"]:
            hero_chips += 1

        seen[kind] = seen.get(kind, 0) + 1
        failures += report(kind, "%s[%d]" % (kind, seen[kind]), text)

    if hero_chips > MAX_HERO_CHIPS:
        failures += 1
        print("%-4s %-22s %3d  / %-4s %-20s %s" % (
            "FAIL", "hero chip count", hero_chips, MAX_HERO_CHIPS, "",
            "keep the 3 that change how the page is read"))

    if not parser.found:
        print("no capped copy surfaces found - check the class names")

    js_copy = re.search(r"(textContent|innerHTML)\s*=", source)
    if js_copy:
        print("note: copy is built in JS here - also check rendered strings "
              "with --kind (see --help)")

    return failures


def check_strings(kind, texts):
    if kind not in WORD_BUDGET:
        print("unknown kind %r. Known: %s" % (kind, ", ".join(sorted(WORD_BUDGET))))
        return 1
    failures = 0
    print("\n--kind %s" % kind)
    print("-" * (8 + len(kind)))
    for i, text in enumerate(texts, 1):
        text = text.strip()
        if text:
            failures += report(kind, "%s[%d]" % (kind, i), text)
    return failures


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args else 2

    if "--kind" in args:
        at = args.index("--kind")
        if at + 1 >= len(args):
            print("--kind needs a value")
            return 2
        kind = args[at + 1]
        rest = args[:at] + args[at + 2:]
        texts = []
        while "--text" in rest:
            at = rest.index("--text")
            if at + 1 >= len(rest):
                print("--text needs a value")
                return 2
            texts.append(rest[at + 1])
            rest = rest[:at] + rest[at + 2:]
        if not texts:
            texts = sys.stdin.read().splitlines()
        total = check_strings(kind, texts)
    else:
        total = sum(check_file(path) for path in args)

    print("\n%s" % ("copy budget: PASS" if total == 0
                    else "copy budget: %d over budget - cut before showing" % total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

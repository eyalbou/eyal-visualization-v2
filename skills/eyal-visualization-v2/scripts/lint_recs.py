#!/usr/bin/env python3
"""De-slop gate for the Recommendations tab of a v2 dashboard.

    python3 scripts/lint_recs.py dashboard.html
    python3 scripts/lint_recs.py dashboard.html --id view-overview
    python3 scripts/lint_recs.py dashboard.html --allow-proof --allow-three

Extracts one panel by id (default `view-recommendations`), drops `<script>`,
`<style>`, and `.action-rank` badges, and scores the rest with the vendored
SlopMonster linter (`deslop.py`, do not edit). Em and en dashes always fail.

Fails, instead of passing, when the panel is missing or holds no static
`.action-card`: cards rendered from JS are invisible to every gate, and an
empty panel scoring 5/5 is how slop ships.

Flags:
    --allow-proof   every flagged number traces to the analysis
    --allow-three   every flagged three-item list names three real things
"""
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deslop  # noqa: E402

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
SKIP_TAGS = {"script", "style", "template"}
SKIP_CLASSES = {"action-rank"}
DASHES = re.compile(r"[\u2013\u2014]")


class Panel(HTMLParser):
    def __init__(self, target):
        super().__init__(convert_charrefs=True)
        self.target = target
        self.depth = 0
        self.found = False
        self.skip_depth = 0
        self.text = []
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if self.depth == 0:
            if a.get("id") == self.target:
                self.found = True
                self.depth = 1
            return
        if tag in VOID:
            return
        self.depth += 1
        if "action-card" in classes:
            self.cards += 1
        if self.skip_depth == 0 and (tag in SKIP_TAGS or SKIP_CLASSES & set(classes)):
            self.skip_depth = self.depth
        if tag in ("p", "div", "h1", "h2", "h3", "li", "article", "br"):
            self.text.append(" . ")

    def handle_endtag(self, tag):
        if self.depth == 0 or tag in VOID:
            return
        if self.skip_depth == self.depth:
            self.skip_depth = 0
        self.depth -= 1

    def handle_data(self, data):
        if self.depth and not self.skip_depth:
            self.text.append(data)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)
    allow_proof = "--allow-proof" in args
    allow_three = "--allow-three" in args
    target = "view-recommendations"
    if "--id" in args:
        target = args[args.index("--id") + 1]
    path = args[0]

    try:
        html = deslop.read_utf8(path)
    except OSError as e:
        sys.exit(f"lint_recs: cannot read {path}: {e.strerror}")

    p = Panel(target)
    p.feed(html)
    p.close()
    if not p.found:
        sys.exit(f'lint_recs: FAIL no element with id="{target}"')
    if p.cards == 0:
        sys.exit(f'lint_recs: FAIL #{target} has no static .action-card -- '
                 'write the cards as HTML, not from JS, so the gates can read them')

    raw = " ".join(p.text)
    dashes = DASHES.findall(raw)
    text = deslop.normalise(re.sub(r"(\s*\.\s*)+", " . ", raw)).strip(" .")
    hits = deslop.audit(text)
    advisory = []
    if allow_three and hits["rhythm"]:
        advisory, hits["rhythm"] = hits["rhythm"], []

    print(f"#{target}: {p.cards} cards, {len(text.split())} words\n")
    score = deslop.report(hits, allow_proof=allow_proof)
    for label, snippet in advisory:
        print(f"    advisory (--allow-three): {label}: {snippet}")
    if dashes:
        print(f"\n  FAIL: {len(dashes)} em/en dash(es) -- use --")
    sys.exit(0 if score == 5 and not dashes else 1)


if __name__ == "__main__":
    main()

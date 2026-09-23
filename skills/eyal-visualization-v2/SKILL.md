---
name: eyal-visualization-v2
description: Use when the user asks to "eyal visualize v2", "/eyal-visualize-v2", "soft UI dashboard", "build dashboard v2", "app shell dashboard", or wants the Soft UI system (full-page geometric hero, rounded cards, pill nav, trend chips). Self-contained -- do not read eyal-visualization v1. No decorative images. Defer to studio-data-visualization only for Wix branding.
version: 0.14.1
---

# Eyal Visualization v2 (Soft UI)

**Skill version 0.14.1** -- same value as [VERSION](VERSION) and the YAML `version` above. To check you are current, compare your `VERSION` file against `VERSION` on `main` in `eyalbou/eyal-visualization-v2`. Older copy: pull the repo, or in Willow resync From GitHub.

Standalone skill. Geometric hero, ice canvas, white cards, pills, trend chips, optional app shell. Do **not** open `eyal-visualization` v1 files. Defer to `studio-data-visualization` only when the user asks for Wix branding.

If they already asked for v2 / Soft UI, do **not** re-ask which visual system.

This file plus `references/` and `assets/` is the full pack.

---

## Visual system (this skill)

| Topic | Rule |
|-------|------|
| Fonts | `--font` everywhere; `--font-mono` only on `code` / `pre` |
| Images | No decorative images; Phosphor icons |
| Funnel | CSS columns ([funnel-graph.md](references/funnel-graph.md)), not Chart.js funnel |
| Hero KPI color | Valence token; bad-when-up is never trust-blue |
| Null sentinel | `-` |
| Tab arc | Overview → drill-down(s) → **Recommendations** → Sampling → Methodology |
| Sampling IDs | Session sampler: uuid cell = UM link; conversation id cell = conversation URL. Never a second URL column. [Sampling table](#sampling-table-ids-are-the-links) |
| Type | Two families; four DM Sans weights; no Axiforma `<link>` |
| Doughnut | **2-4** slices; 5+ or one slice >80% → horizontal bar |
| Copy length | Hard word caps, checked by script. [Copy budget](#copy-budget-hard-caps) |
| Accent | `#2563EB` default; never ask. [Hard constraint 4](#hard-constraints) |
| Recs type | Recommendations type palette: blue primary, purple add, mint go, yellow wait/look, red severe-only. Use 2-3 colors when enough. [Recommendations](#recommendations-tab-action-grid) |
| Motion no-op | If a click does not change the screen, skip animation and skip re-render. [No motion on no-ops](#no-motion-on-no-ops) |

Maps only if the question is geo.

---

## Craft (built in -- no other skill)

- 4-point spacing; 16px tight groups; 32px section gaps; 12-col desktop
- Hierarchy from size/position/color, not a spreadsheet
- One aesthetic, executed tightly. Atmosphere supports data
- Grasp the core idea in 5 seconds
- Every control has default / hover / active / disabled / loading
- Progressive disclosure: hide complexity until asked
- Motion ~300ms enter, ~100ms hover; honor `prefers-reduced-motion`. No animation when the click did not change the screen
- Numbers via `fmtNum` / `fmtInt` / `fmtPct` only

---

## Read map (do not load the whole pack)

**Must (every call):** this file (constraints + [Copy budget](#copy-budget-hard-caps) + checklist) + [color-valence.md](references/color-valence.md) + [soft-ui-tokens.md](references/soft-ui-tokens.md). Before delivery, run [`scripts/copy-check.py`](scripts/copy-check.py).

**Scaffold:** copy `assets/analytics-starter.html` or `assets/app-shell-starter.html` **from disk**. Do **not** Read the full HTML into context.

**If-needed:** [analytics-storytelling.md](references/analytics-storytelling.md) (analytics), [funnel-graph.md](references/funnel-graph.md) (3-stage conversion), [app-shell-patterns.md](references/app-shell-patterns.md) (shell), [chartjs-configs.md](references/chartjs-configs.md) (drawing Chart.js -- **read Chart hover** when any Chart.js tooltip exists), [overflow-rules.md](references/overflow-rules.md) (a chart exists), [hero-geometric.md](references/hero-geometric.md) (not copying the starter), [component-recipes.md](references/component-recipes.md) (KPI / finding cards / Recommendations grid).

Recipes stay in references. Copy CSS from assets on disk.

---

## Hard constraints

1. **No decorative images.** Icons: **Phosphor** default. Lucide only if the user asks.
2. **Two font families, never more** -- `--font` + `--font-mono` on `<code>` / `<pre>` only. [Fonts](#fonts).
3. **Light mode default** -- `body.dark` toggle (sibling of `:root`, not nested in it). Re-render Chart.js on theme change with animation off (checklist section 7).
4. **Accent** -- if the user names a color, use it. If they do not, **use the default silently and build**: `--accent: #2563EB`, `--accent-2: #6366F1`. **Never ask which color.** Chart series, mesh, shapes, glow, and washes all derive from the tokens already in [soft-ui-tokens.md](references/soft-ui-tokens.md) -- do not invent a new palette. Valence and the 5-stop severity scale still win over accent ([constraint 9](#hard-constraints)). The [optional brand palette](#optional-brand-palette) is used only if the user asks for it by name.
5. **Self-contained HTML** -- CDN only.
6. **No fake sparklines** on histogram / cross-section snaps. Sparklines only for dated series.
7. **Every displayed count goes through `fmtNum`**. Tables/tooltips: `fmtInt`. Rates: `fmtPct`. Never `toLocaleString()`.
8. **Artifact UI punctuation** -- in the HTML, `-` only (no em/en/`--`). This rule is **artifact UI only**. Chat / Slack drafts still use `--`. Keep `--` in CSS vars, JS, and SQL in `<pre>`.
9. **Color valence** -- up-is-bad is never trust-blue. [color-valence.md](references/color-valence.md).
10. **Skill self-update** -- if you change this skill, write **local and git in the same turn**: bump the three version stamps, run `scripts/ship.sh`, tell Eyal to resync in Willow. [MAINTAINING.md](MAINTAINING.md).
11. **Copy budget** -- visible copy obeys the word caps in [Copy budget](#copy-budget-hard-caps); `python3 scripts/copy-check.py <file>` must exit 0 before the artifact is shown. Detail goes to info hover, not on screen.

---

## Invocation checklist

Run **when the skill is called**, before showing the file. Analytics vs shell is the first gate.

### 0. Confirm

- [ ] Archetype: analytics report vs sidebar/top-nav shell (ask only if unclear)
- [ ] Soft UI / v2 already requested → do not re-ask visual system
- [ ] `--accent`: user's color if they named one, else `#2563EB` / `#6366F1` silently. Never ask about color

### 1. Scaffold

- [ ] Copy `assets/analytics-starter.html` or `assets/app-shell-starter.html` (not a blank file)
- [ ] Full-page `.page-canvas` + `.shell` z-index 1; theme toggle in `.page-chrome`
- [ ] Four DM Sans weights; no Axiforma `<link>`; `html, body` use `--font`; `code, pre` use `--font-mono`; form controls `font-family: inherit`; `Chart.defaults.font.family` matches `--font`

### 2. Story and copy (analytics only)

- [ ] Overview **is** the hero tab. Title + subtitle (same on every tab) cover: what this is, why read it, what you get, what we aim to achieve. No extra briefing card
- [ ] **Every capped surface is inside [Copy budget](#copy-budget-hard-caps).** Subtitle ≤35 words / ≤2 sentences; hero chips ≤3 × ≤4 words; card + row body ≤20 words / 1 sentence; insight bullet ≤18 words; KPI caption ≤8 words
- [ ] Hero chips carry **population / window / n / freshness in plain words**. No pipeline, tool, connector, table, commit hash, run ID, or second-level timestamp
- [ ] After the stake chart: ranked **finding cards** in a carousel (stake / what to look at next). Finding in stakeholder English, **not** a verb-first action. [Overview finding cards](#overview-finding-cards-carousel)
- [ ] **Recommendations** tab before Sampling: action items only, 1-6 cards, **2×3 CSS grid**, no carousel. Skip the tab if there is no recommended move -- do not show it empty. Type color: blue / purple / mint / yellow / red-severe-only; 2-3 colors when enough; title keyword + labeled footer. [Recommendations](#recommendations-tab-action-grid)
- [ ] **When a Recommendations tab exists, `python3 scripts/lint_recs.py <file>` exits 0** -- cards are static HTML in `#view-recommendations`, every number traces to the analysis. [De-slop the rec copy](#de-slop-the-rec-copy-required-when-this-tab-exists)
- [ ] Every tab panel is `<section class="view" id="view-<tab>">` (starter pattern), so each tab can be linted on its own
- [ ] Tabs: Overview → drill-down(s) → Recommendations → Sampling → Methodology. Do not put actions on Overview. Sampling may be a **filter recap** (inclusion / exclusion / n remaining) -- still its own tab. Not a required session sampler. If a **session sampler table** exists: uuid is the User Manager link; conversation id is the conversation URL; no extra URL columns. [Sampling table](#sampling-table-ids-are-the-links)
- [ ] One primary visual per question; chart type from the [chooser](#chart-chooser); title = finding in stakeholder English
- [ ] At most 3 insight bullets under the chart (outcome, not method). One short under-chart caveat only if skipping it would misread the number
- [ ] Extra method / definitions / grain live in **hover info**, `*`, collapse, or Methodology. Every domain term, internal name, or metric definition on screen has an info hover
- [ ] UI strings use `-` only; chat drafts may still use `--`

### 3. Data and numbers

- [ ] Baked `DATA`; buttons use `data-pop`; visible names from `.label`
- [ ] Canonical `fmtNum` / `fmtInt` / `fmtPct`; null → `-` (never `--`)
- [ ] KPIs/axes/prose → `fmtNum`; tables/tooltips → `fmtInt`; rates → `fmtPct`; movements → `pp`
- [ ] SQL pointer on Methodology; footer shows `generated_at`

### 4. Color and charts

- [ ] For each KPI/fill: up is better / worse / magnitude-only → valence tokens. TOR/DSAT hero starts as `.kpi.hero.is-bad`
- [ ] Ordered scales (mild → rage, TOR bands): rank order + `--sev-*`; driver bars: volume order + end labels
- [ ] Nested subset: arrow + caption between parent and child
- [ ] 3-stage conversion: CSS funnel (hue family **per population**; Cara table is an **example**)
- [ ] Chart ticks and datalabels **14px / 600**. Hide collisions; do not shrink to 11px. Funnel conversion chip stays the loudest number
- [ ] Series colors **locked** across population toggles (same hex for SSA / SR / NS, or Cara vs Chatbot)
- [ ] Click a bar → filter the sibling chart that shares the grain. Two metrics with different baselines (TOR vs resolution) = **toggle**, never dual-axis. Hover follows the **active pill** (TOR hover = TOR; Res hover = Res; Score / mixed = both, each with its own gap). `label` returns a string array -- never one `TOR · Res · gap` line.
- [ ] Chart hover sits **on top**: HTML `external` `#chart-tip` on `body` (`z-index: 9999`). Overlay plugins use `afterDatasetsDraw` with HTML tooltips, or `beforeTooltipDraw` if the tooltip stays on canvas. Never `afterDraw` + `fillRect` over a canvas tooltip. [chartjs-configs.md](references/chartjs-configs.md#chart-hover--tooltip-must-sit-on-top)
- [ ] Horizontal driver / mix / gap bars: y-axis is `Name (n)` two-tone -- name in `--ink`, `()` in `--ink-soft`, count in the **subject color** (Cara `--cara` / `--cara-label` on dark) via `fmtNum`. Never the bar / winner fill. Not a single-color Chart.js tick string. Gutter plugin = `beforeTooltipDraw`.
- [ ] No histogram sparklines; Chart.js re-renders on theme toggle. Keep CSS `rise` ~300ms, canvas enter on first load, hover ~100ms, `prefers-reduced-motion`

### 5. Chrome and motion

- [ ] Hero KPI / active snap: top bar + wash in the **valence** color
- [ ] Pills synced; long tables in `collapse-card` closed
- [ ] Phosphor icons (unless user asked Lucide); no photos
- [ ] Action-card pointer glow **default ON**; off under `prefers-reduced-motion`; static only if the user kills glow

### 6. Auto-review (silent)

- [ ] Grep list below
- [ ] **Run `python3 scripts/copy-check.py <file>`** -- every `FAIL` fixed, exit code 0, before the file is shown
- [ ] KPI row: any count ≥ 1000 still raw digits → missed `fmtNum`
- [ ] Hero: bad-when-up in `--accent` blue → valence miss
- [ ] Chart hover: overlay `afterDraw` + `fillRect` with no tooltip `external:` → fail. Metric-toggle hover ignores the pill, or Score omits one metric → fail
- [ ] **Copy scan** (required): [Copy-scan pass](#copy-scan-pass)
- [ ] Note fixes in the delivery message

### 7. Chart.js toggles

- [ ] `Chart.defaults.animation = false` (set next to the font defaults). Population / theme / tab / filter updates must not tween: `chart.update('none')` or destroy + recreate under that default. Do **not** leave Chart.js duration on for toggles
- [ ] CSS page enter stays (`rise` ~300ms, canvas on first load, hover ~100ms). Do not kill page-enter motion to satisfy this rule
- [ ] **No motion on no-ops.** Re-clicking the already-selected pill / tab / chip returns immediately -- no `renderAll()`, no chart rebuild, no `rise` replay. Same for same-state theme, same metric, same sort. [No motion on no-ops](#no-motion-on-no-ops)

### 8. Stash (unless already covered)

- [ ] If the user did **not** already forbid sharing, say local-only, or give a Stash URL: publish the HTML with Stash MCP `stash__publish_artifact` (`slug` kebab-case, `files` with `index.html` UTF-8). Return `https://bo.wix.com/stash/<slug>/`. Do not set `anonymous`. Do not set `overwrite` unless they confirmed replace
- [ ] Skip this step if they already said not to upload / keep it local / already published

**Shell-only skip:** section 2 except hyphen/fonts; no forced Sampling / Recommendations tabs; no forced funnel; no finding carousel or action grid.

---

## Copy budget (hard caps)

The reader is a stakeholder, not a domain owner. Visible copy is the **short version**; the detail lives one hover away. These are counted numbers, not vibes -- [`scripts/copy-check.py`](scripts/copy-check.py) fails the build when a surface goes over.

| Surface | Class | Cap |
|---------|-------|-----|
| Hero subtitle | `.subtitle` | **35 words**, max 2 sentences |
| Hero eyebrow | `.hero-badge` | **4 words** |
| Hero chip | `.badge` in the hero | **4 words** each, **max 3 chips**, content-checked |
| Action card body | `.action-reason` | **20 words**, 1 sentence |
| Scored / comparison row body | `.row-reason` | **20 words**, 1 sentence |
| Insight bullet | `li` inside `.insight` | **18 words** |
| KPI caption | `.kpi-caption` | **8 words** |

Run it before delivery:

```bash
python3 scripts/copy-check.py dashboard.html
```

Chips are checked on **content**, not only length -- a tool or pipeline name, a commit hash, a `snake_case` / `kebab-case` service or table slug, or three `·`-joined segments fails even at 4 words. A plain numeric ID (`Experiment 5073656`) is fine.

**What moves to hover.** Anything that is evidence rather than the point: commit counts, connector and tool names, table names, why this threshold, sample mechanics, "held to 4 because…". Also every domain term, internal name, and metric definition -- if a stakeholder outside the domain would need to look it up, it needs an info hover, `*`, collapse, or a Methodology row. Hover has no word cap; the visible layer does.

**How to cut** (in this order): drop the second clause of evidence; drop the qualifier; move the number's provenance to hover; keep one number, not three. Never shrink type to fit more words.

---

## Overview hero copy

The first tab **is** the hero. Do **not** add a briefing card, extra snaps, or a second title. Title + subtitle stay tab-agnostic (they still show on drill-down / Sampling / Methodology).

- **Title (h1):** research name. No slogan, grain, event IDs, pipeline (`What to fix first`, `session by session`, `4:1148`).
- **Subtitle: ≤35 words, max 2 sentences** ([Copy budget](#copy-budget-hard-caps)). Stakeholder English, covering **why read / what you get**. The aim can be implied -- do not spend a third sentence on it. "How we will answer it" is at most **one clause**, not SQL, row counts, or funnel mechanics.
- Ban caveats, scoring mechanics, `COUNT(DISTINCT msid)`, and `engaged → view → submit` as the whole subtitle.
- If copy is ambiguous, draft 3 subtitle options and wait.
- Overview **body** still sets the stake (KPIs + one chart). It does not repeat the hero beats.

Good (24 words): `How many accounts carry 100+ sites, and does that concentration change who we should treat as the unit of analysis?`

Bad (95 words, 3 sentences -- passes an old sentence count, fails the budget): `Customer Care runs 27 dashboards on Vizion and one semantic model on Power BI, and nothing written down says which platform new work should go to. This page scores both across 25 rows, keeping what each product can do apart from what CC actually has working today, and names the three rows where Power BI is the only right answer. The aim is a routing rule for new dashboards plus four ownership decisions, not a winner.`

Same page, inside budget (28 words): `CC has no written rule for which platform a new dashboard belongs on. This page scores both and names the three cases where Power BI wins.`

Bad (slogan): `Finding the sub-text of our users.`

### Hero chips (the `.badge` row under the subtitle)

Max **3 chips**, **≤4 words each**. A chip earns its place only if it changes how the reader reads the page.

| Allowed | Example |
|---------|---------|
| Population / scope | `Logged-in users` |
| Window | `Jun 11 - Aug 20` |
| Size | `6.4M accounts` |
| Freshness | `Data through Aug 27` |
| Status | `Test running` |

**Never in a chip:** pipeline or job names, tool and connector names, table names, commit hashes, run IDs, model names, second-level timestamps, or a `·`-joined stack of them. `XMLA · vizion-platform a7bbfca8 · Trino` and `Verified live 2026-08-26 and 2026-08-27` are both failures -- that is Methodology content. Method **never** gets promoted to the hero to make room elsewhere.

---

## Overview finding cards (carousel)

Required on Overview **after** the stake chart. Not for app-shell. These set the ground and point at the drill-downs. They are **not** action items.

**Title:** finding in stakeholder English (`Premium is 41% of TOR`). Not a verb (`Stop routing Premium`). Not a theme label (`UI grounding`).

**Reason:** one sentence, **≤20 words** ([Copy budget](#copy-budget-hard-caps)), 1-2 numbers. What to look at next, not what to build.

Layout: existing `.action-strip` carousel -- swipe + arrows, `scroll-snap`. 3-5 cards. Rank optional. Same card chrome and pointer glow as action cards. Recipe: [component-recipes.md](references/component-recipes.md#overview-finding-cards).

Do **not** put verb-first actions here. Actions live only on [Recommendations](#recommendations-tab-action-grid).

---

## Recommendations tab (action grid)

Label: **Recommendations**. Last analysis beat: after drill-downs, **before** Sampling and Methodology. Not for app-shell. Skip the whole tab if there is no recommended move -- do not invent cards, do not show an empty tab.

**Title:** verb-first operative action (`Stop repeating a failed step`). Not a theme label (`UI grounding`). Not a finding (`Premium is 41% of TOR`).

**Reason:** why the research points here. **≤20 words, 1 sentence** ([Copy budget](#copy-budget-hard-caps)). One number, two only if the pair is the point. Stakeholder English. Not SQL, not classifier names, not the evidence chain -- `held to 4 because 54 fix commits sit against 55 feat commits across 118 merged PRs` is hover content.

Layout: **2 rows × 3 columns**, CSS grid, **no carousel**. 1-6 cards, recommended build order. 4 cards = 3+1, 5 = 3+2. **Do not pad** empty slots. Rank `01`…, title `--text-h3`, reason `--text-sm` / `--ink-soft`. Optional Phosphor icon, owner / effort chips, one highlighted stat. **Pointer-follow glow default ON**; `prefers-reduced-motion` disables it. Below ~768px: 1 column, no horizontal scroll.

**Type color (this section only).** Blue primary, purple add, mint go, yellow wait/look (type, never a fill), red severe-only. Color the title keyword, footer, rank, and icon; `.action-reason` stays `--ink-soft`. Use 2 or 3 colors when that covers the grid. Palette table and rules: [color-valence.md section 9](references/color-valence.md#9-recommendations-type-palette-section-lock).

**Footer** is a labeled line, not a bare number. `Cara 39% vs chatbot 56%`, not `39% / 56%`. `9.6% resolved`, not `9.6%`. `Offer 7.55K, route 3.24K`, not `7.55K vs 3.24K`.

Show **once** -- actions on this tab only. Do not duplicate on Overview.

**Static HTML, fixed id.** The panel is `<section class="view" id="view-recommendations">`, and every card is written as HTML inside it, not rendered from `DATA`. Rec copy does not change with the population toggle, and cards built in JS are invisible to both gates. Format each number with the `fmtNum` / `fmtPct` rules as you write it. Same for the Overview finding cards in `#view-overview`. The starter shows the pattern. Recipe: [component-recipes.md](references/component-recipes.md#recommendations-action-grid).

### De-slop the rec copy (required when this tab exists)

`copy-check.py` counts words; it does not hear tone. Rec titles and reasons are the most persuasive prose in the artifact, so they are where AI phrasing shows up. Lint this tab only -- not the whole file, which would score chart labels and KPI values.

```bash
python3 scripts/lint_recs.py dashboard.html
```

It extracts `#view-recommendations`, skips rank badges, and scores the cards with the vendored SlopMonster linter (`deslop.py`, do not edit). It **fails** when the panel is missing or has no static `.action-card`. Em and en dashes fail too. Exit 0 = pass. Fix every hit and re-run.

- **Verb-first is not the same as slop-free.** `Unlock faster routing` and `Elevate the Premium journey` are verb-first and still fail. Use the plain verb the team says out loud: stop, offer, route, hold, add, drop.
- **The reason line is where the rule-of-three creeps in.** Three clauses for rhythm inside a ≤20-word sentence is padding. Cut to the real count. If the three items are real named things, `--allow-three` makes the hit advisory.
- **Invented proof is a fail, not a style note.** Every number in a title, reason, or footer must trace to the analysis. If it does not exist, the card does not ship with it -- there is no `[needs number]` state on a delivered artifact.

When a flagged number is real and evidenced, `--allow-proof` clears that group. Only use it after checking each figure against the data, and say so in the delivery message.

---

## Sampling table: IDs are the links

Applies only when Sampling is a **session sampler table**. The id **is** the link: uuid cell links to User Manager, conversation id cell links to the conversation. A second URL column is a fail. URLs, CSV, and row-click rules: [analytics-storytelling.md](references/analytics-storytelling.md#sampling-table-ids-are-the-links).

---

## Copy-scan pass

Required after the dashboard renders, before showing it. Silent. Fix, then ship.

Visible layer is **load-bearing only**. If a sentence can go without changing what the reader should believe or do, it goes to hover or it gets deleted.

1. **Sense.** Each insight follows from the chart or KPI above it. No leftover claims from an older cut. Numbers in prose match `DATA`.
2. **Minimal.** One idea per sentence. No restating the bars (`Premium is the largest bar`). No method in the insight (`we joined on msid`).
3. **Inside budget.** Run `python3 scripts/copy-check.py <file>` and fix every `FAIL`. Counted caps, not judgement: [Copy budget](#copy-budget-hard-caps). At most 3 bullets under a chart. One short under-chart caveat only when it changes how to read the number. No second paragraph of "also note".
4. **Relevant only.** Delete captions that repeat the title. Delete chips that repeat the KPI. Delete taxonomy labels the reader cannot act on. Delete chips carrying pipeline or tool names.
5. **Hover for extra.** Definitions, grain, why this filter, "what is SSA", the evidence behind a score -- hover info (or `*` / collapse). Not body copy. A domain term with no hover is a fail.
6. **Stakeholder-readable.** Read the page as someone outside the domain: every visible sentence lands without a glossary, or it has a hover.

**Fail** if the page looks like a report dump: stacked caveats, insight that retells the chart, walls of evidence in card bodies, info-i as the only place for a caveat that changes the read.

---

## Fonts

Exactly two families: `--font` (Axiforma stack, DM Sans ships) and `--font-mono` on `code` / `pre` only. A third on screen is a bug -- almost always an unstyled `<code>`. Axiforma has **no public CDN**; never `<link>` / `@import` it. Load all four DM Sans weights. `Chart.defaults.font.family` = the same string as `--font`. Phosphor is an icon font and does not count. `--text-hero-display` only on the page hero h1. Loading tags and base CSS: [soft-ui-tokens.md](references/soft-ui-tokens.md#font-loading-required-in-head).

Expressive display type (slides, posters, marketing heroes) is the only exception: `eyal-fonts` supplies one loud face and the house font stays the quiet face. Never on dashboards, KPIs, charts or tables.

---

## No motion on no-ops

Motion exists to show a **change**. If a click does not change the screen, the setter returns first: no `renderAll()`, no chart `update`, no `rise` replay. Applies to pills, tabs, chips, metric toggles, sort, filters, and theme; `:active:not(.active)` for press-scale. Still animate a real change. Setter code and the full no-op table: [state-patterns.md](references/state-patterns.md#no-motion-on-no-ops).

---

## Number formatting

Implement verbatim. Do not improvise.

| Value | Rendering | Example |
|-------|-----------|---------|
| `< 1,000` | all digits, no separator | `42`, `543` |
| `1,000` to `< 1,000,000` | `K` at one decimal, two only when the second is significant | `1.0K`, `17.1K`, `25.16K`, `999.99K` |
| `>= 1,000,000` | `M`, always two decimals | `1.25M`, `12.40M` |

The `K` band never drops to zero decimals -- `26.0K`, not `26K`.

```javascript
function fmtNum(val) {
  if (val == null || isNaN(val)) return "-";
  const n = Number(val);
  const sign = n < 0 ? "-" : "";
  const abs = Math.abs(n);
  if (Math.round(abs) < 1000) return sign + String(Math.round(abs));
  const k = abs / 1e3;
  const two = k.toFixed(2);
  if (parseFloat(two) < 1000) return sign + (two.endsWith("0") ? k.toFixed(1) : two) + "K";
  return sign + (abs / 1e6).toFixed(2) + "M";
}

function fmtInt(val) {
  if (val == null || isNaN(val)) return "-";
  const s = String(Math.round(Math.abs(val)));
  let out = "";
  for (let i = 0; i < s.length; i++) {
    if (i > 0 && (s.length - i) % 3 === 0) out += ",";
    out += s[i];
  }
  return (val < 0 ? "-" : "") + out;
}

function fmtPct(val, decimals) {
  if (val == null || isNaN(val)) return "-";
  const d = decimals == null ? 1 : decimals;
  return Number(val).toFixed(d) + "%";
}
```

| Surface | Formatter |
|---------|-----------|
| KPI values, snap cards, hero numbers, axis ticks, bar end labels, insight prose | `fmtNum` |
| Data tables, tooltips | `fmtInt` |
| Rates | `fmtPct` |
| Movements | `pp` |

Numeric table columns: `font-variant-numeric: tabular-nums`. Null → `-`, never `--`.

---

## Color valence (MUST)

Before a fill: **if this number goes up, is that better or worse?** Up is bad → `--warning` → `--sev-hi` / `--danger`. Up is good → `--success` or `--accent`. Magnitude only → `--accent` / `--ink`. TOR / DSAT / rage are never trust-blue; their hero starts as `.kpi.hero.is-bad`. Ordered negative states go left-to-right by **rank**. Series hexes stay locked across population toggles. Full rules (loaded every call): [color-valence.md](references/color-valence.md).

---

## Optional brand palette

Use **only when the user asks** for it by name; never offer it. It does not replace valence. Tokens and roles: [soft-ui-tokens.md](references/soft-ui-tokens.md#optional-brand-palette).

---

## Chart chooser

Pick by the **question**, not by habit. **Never:** pie, radar, Chart.js funnel / Sankey for a 3-stage survey drop, gauges, word clouds unless asked. Doughnut only at 2-4 slices. TOR vs resolution is a toggle, never dual-axis. Not every dashboard needs a funnel. Full question-to-chart table: [chartjs-configs.md](references/chartjs-configs.md#chart-chooser).

---

## Required v2 chrome

- Full-page `.page-canvas` (mesh, 5 pills, vignette). First-load `canvasEaseIn` + `meshEaseIn`. Toggle in `.page-chrome`. [hero-geometric.md](references/hero-geometric.md)
- Pill toggles: solid `--accent` when active; sync duplicates. [state-patterns.md](references/state-patterns.md)
- Trend chips: `+X.XXpp vs {baseline.label}`
- Long secondary content: `<details class="collapse-card">` **closed**. Headline + primary chart stay visible
- Linked charts: clicking a bar filters the sibling that shares the grain. TOR vs resolution = metric **toggle**, never one dual-axis. [state-patterns.md](references/state-patterns.md)
- Insight: borderless + shadow (not a left-accent border)

### DATA pattern (analytics)

```javascript
const DATA = {
  generated_at: "2026-06-17T10:00:00Z",
  populations: {
    segment_a: { label: "Display Name", subtitle: "SQL definition",
      total: { count: 1200, rate: 4.5 }, series: [] },
  },
};
```

Pre-aggregate before embedding. `data-pop="segment_a"`; visible text uses `.label`. `renderAll()` updates KPIs, chart, and snaps together; finding and rec cards are static HTML. SQL pointer lives on the Methodology tab; footer: `Generated {fmtDate(DATA.generated_at)}`.

In-skill proofs: `assets/analytics-starter.html` (full tab arc), `assets/funnel-graph.html`.

---

## Dark mode

Put overrides in a **`body.dark { }` rule that is a sibling of `:root`**. Nested `body.dark` inside `:root` is invalid.

| Token | Light | Dark |
|-------|-------|------|
| `--page-bg` | soft gradient | `#030303` |
| `--surface` | `#FFFFFF` | `#1C1F28` |
| `--canvas` | `#F5F5F7` | `#0F1117` |
| `--sev-hi` / `--sev-max` | `#da0808` / `#950404` | `#f04444` / `#da0808` |

Call `renderAll()` inside `setTheme()`.

---

## Anti-patterns (never)

- Hero background trapped in a card; `--text-h1` for Kokonut hero
- `box-shadow` ring on active snaps; histogram sparklines on snaps
- `toLocaleString()`; ad-hoc `toFixed(1)+"K"`; null `"--"`; raw digits ≥1000 on a KPI
- Third font; Axiforma `<link>`; mono outside `code`/`pre`; photos
- Slogan / pipeline as h1; funnel/SQL/caveat as the whole subtitle; subtitle true only on Tab 1
- Hero subtitle over 35 words or 2 sentences; a third sentence restating the aim
- Chips carrying pipeline, tool, connector, table, commit hash, run ID, or a second-level timestamp; more than 3 hero chips
- Card body / scored row over 20 words; the evidence chain (`held to 4 because 54 fix commits…`) on screen instead of in hover
- A domain term or internal name on screen with no info hover; shipping without running `copy-check.py`
- Asking the user which accent color to use
- Analyst-process in the insight (`we joined on msid`, `batch 4:1148`)
- Three charts of the same mix; insight after secondary charts; hardcoded fractions
- Horizontal bars without end labels; ordered scale sorted by volume
- Sampler buried in Methodology; Methodology not last; Sampling skipped on analytics; Recommendations after Sampling
- Verb-first actions on the Overview carousel; finding cards on Recommendations
- Recommendations as a carousel; empty Recommendations tab; padding dummy cards to fill a 2×3
- Yellow fill / row mark on Recommendations; bare-number footers (`39% / 56%`); red on Hold or a non-severe investigate; `#60d394` green as recs go (use mint); forcing 4-5 type colors when 2-3 cover it
- `Reccomendations` (misspelling) as the tab label
- Session sampler: uuid or conversation id as plain text with a separate URL column; Listen/Open replacing the cid
- Em/en/`--` punctuation in **artifact UI**
- Chart.js / Sankey for 3-stage survey funnel; one `--accent` for every funnel population
- Neon chatbot orange next to Cara blues; ice-300 funnel fills; two-tone funnel bars
- Bad-when-up hero in `--accent` blue; two blues for mild vs frustrated; green for mild-bad
- White type on `--sev-ok` / `--sev-lo` / `--sev-mid`; black type on `--sev-hi` / `--sev-max`
- Shrinking chart labels to 11px; reminting series colors per population toggle
- Chart.js grow / tween on population, theme, tab, or filter toggle (`animation` left on; `update()` without `'none'`)
- Re-clicking an already-selected pill / tab / chip / filter retriggers `renderAll()`, chart destroy, or `rise`; `:active` scale on a control that is already `.active`
- Dual-axis for TOR vs resolution; action list duplicated on Overview and Recommendations
- Canvas Chart.js tooltip under `afterDraw` overlays (hover "behind" y-labels); one-string tooltip mixing TOR + Res + gap; metric-toggle hover that ignores the active pill
- Reading or depending on `eyal-visualization` v1 files

---

## Auto-review (before delivery)

1. Phase 0 -- numbers match source; labels match `DATA.*.label`
2. Phase 1 -- charts render; toggles sync; no console errors; overflow rules
3. Phase 2 -- **this file's visual-system table + gated checklist** (two fonts, CSS funnel, `-` sentinel, valence colors)
4. Grep and fix:

| Grep | Expect |
|------|--------|
| `toLocaleString` | zero hits |
| `font-family` | only `--font`, `--font-mono`, and `inherit` |
| `<code` / `<pre` | matching `code, pre` CSS rule |
| `axiforma` in a `<link>` / `@import` | zero hits |
| `text-h1` on hero | zero hits -- hero uses `--text-hero-display` |
| `Chart.defaults.font.family` | present, equal to `--font` |
| `Chart.defaults.animation` | present, `false` |
| `setPopulation` / `setTab` / `setMetric` / `setTheme` | early `return` when the value is already current; no `renderAll()` on that path |
| `toFixed(1) + "K"` | zero hits |
| `fmtNum` / `fmtInt` / `fmtPct` bodies | present; null sentinel `"-"` not `"--"` |
| `—` `–` | zero hits |
| ` -- ` in visible copy | zero hits (ignore `var(--token)` and SQL `--` in `<pre>`) |
| `afterDraw` + `fillRect` | fail if tooltip has no `external:` -- overlays use `afterDatasetsDraw` (HTML tip) or `beforeTooltipDraw` (canvas tip). [chartjs-configs.md](references/chartjs-configs.md#chart-hover--tooltip-must-sit-on-top) |
| `TOR Cara` and `Res Cara` in one `label` return string | fail unless Score / mixed and `label` returns an **array** of lines |
| metric-toggle chart (`data-metric` / TOR \| Resolution pills) | hover body follows the active pill; Score shows both metrics |
| `.subtitle` word count | ≤35 words, ≤2 sentences |
| `.badge` in hero | ≤3 chips, ≤4 words each, no pipeline / tool / hash / table slug / `·` stack |
| `.action-reason` / `.row-reason` | ≤20 words, 1 sentence each |
| `li` inside `.insight` | ≤18 words each |
| `.kpi-caption` | ≤8 words |
| domain term / internal name in visible copy | has an info hover, `*`, collapse, or Methodology row |
| session sampler `uuid` / conversation id | cell text is the id; `href` is UM / conversation URL; zero extra URL columns |
| Recommendations tab | after drill-downs, before Sampling; `.action-grid` not `.action-strip`; 1-6 cards; skip if no move |
| Recommendations type | `--type-blue` `--type-purple` `--type-mint` `--type-yellow` `#ff9500` `--type-red` severe-only; title + labeled footer; body ink; yellow is type not fill |
| Overview carousel titles | findings, not verb-first actions |

5. **Run the copy budget script.** `python3 scripts/copy-check.py <file>` must exit 0:

```bash
python3 scripts/copy-check.py dashboard.html
```

6. Read the KPI row, hero color, mild → rage order, then run the [copy-scan](#copy-scan-pass).

Fix before showing. Note what was fixed.

---

## Additional resources

| File | When |
|------|------|
| [v2-delta.md](references/v2-delta.md) | Soft UI surface, motion, chrome |
| [layout-archetypes.md](references/layout-archetypes.md) | Analytics vs shell |
| [component-recipes.md](references/component-recipes.md) | KPI, snaps, finding carousel, Recommendations grid |
| [funnel-graph.md](references/funnel-graph.md) | CSS survey funnel |
| [analytics-storytelling.md](references/analytics-storytelling.md) | Tab arc, overlap, copy-scan |
| [dashboard-patterns.md](references/dashboard-patterns.md) | Analytics layout |
| [state-patterns.md](references/state-patterns.md) | Pills, hover info, linked charts |
| [chartjs-configs.md](references/chartjs-configs.md) | Chart.js extensions; 14px ticks; **Chart hover** (z-order + metric-toggle body) |
| [overflow-rules.md](references/overflow-rules.md) | Clip / collision rules |
| [scripts/copy-check.py](scripts/copy-check.py) | **Required before delivery** -- counts words per copy surface |
| [scripts/lint_recs.py](scripts/lint_recs.py) | **Required when a Recommendations tab exists** -- lints `#view-recommendations` for AI tells and invented proof |
| [scripts/deslop.py](scripts/deslop.py) | Vendored SlopMonster linter used by `lint_recs.py`. Do not edit |
| [assets/analytics-starter.html](assets/analytics-starter.html) | Analytics scaffold with the full tab arc, finding carousel, and static Recommendations grid (copy from disk) |
| [MAINTAINING.md](MAINTAINING.md) | Editing and shipping this skill only |
| [assets/app-shell-starter.html](assets/app-shell-starter.html) | Shell scaffold |
| [assets/funnel-graph.html](assets/funnel-graph.html) | Funnel graph dummy bake |

This skill is **standalone**. Do not Read `../eyal-visualization/` or any v1 path.

---

## Shipping an update (required)

Only when editing this skill: bump `VERSION` + YAML `version` + the stamp together, then run `bash scripts/ship.sh`. Full steps and the "am I on the latest" check: [MAINTAINING.md](MAINTAINING.md).

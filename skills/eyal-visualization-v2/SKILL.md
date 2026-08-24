---
name: eyal-visualization-v2
description: Use when the user asks to "eyal visualize v2", "/eyal-visualize-v2", "soft UI dashboard", "build dashboard v2", "app shell dashboard", or wants the Soft UI system (full-page geometric hero, rounded cards, pill nav, trend chips) instead of v1. Typography sizes from v1. No decorative images. Defer to studio-data-visualization for Wix branding; defer to eyal-visualization v1 for editorial grain.
version: 0.4.0
---

# Eyal Visualization v2 (Soft UI)

Opt-in fork. **v1 stays default** for editorial / grain / terracotta. v2 is geometric hero, ice canvas, white cards, pills, trend chips, optional app shell.

If the user already asked for v2, do **not** re-ask v1 vs v2.

---

## When v1 fights v2, v2 wins

Workflow still inherits v1 Phase 0-2 **data and function checks**. Do **not** apply v1 visual laws that contradict this table. A correct v2 file that "fails" v1 Phase 2 on these rows is still correct.

| Topic | v1 | v2 |
|-------|----|----|
| Fonts | One family; never mix display + mono | `--font` everywhere; `--font-mono` only on `code` / `pre` |
| Images | Add whenever possible | No decorative images; Phosphor icons |
| Funnel | Chart.js funnel | CSS columns ([funnel-graph.md](references/funnel-graph.md)) |
| Hero KPI color | `--accent` | Valence token; bad-when-up is never trust-blue |
| Null sentinel | `--` | `-` |
| Tab arc | overview → deep-dive → who/where → growth → explore | Overview → drill-down(s) → Sampling → Methodology |
| Phase 2 type | one font, header hack | Two families; four DM Sans weights; no Axiforma `<link>` |
| Doughnut | 2-4 slices | **2-4** slices; 5+ or one slice >80% → horizontal bar |

v1 "Funnel = Funnel Chart" and v1 maps: ignore unless the question is geo. Do not paste v1 SKILL.md into v2 files.

---

## Read map (do not load the whole pack)

**Must (every call):** this file (constraints + checklist) + [color-valence.md](references/color-valence.md) + [soft-ui-tokens.md](references/soft-ui-tokens.md).

**Scaffold:** copy `examples/analytics-starter.html` or `examples/app-shell-starter.html` **from disk**. Do **not** Read the full HTML into context.

**If-needed:** [analytics-storytelling.md](references/analytics-storytelling.md) (analytics), [funnel-graph.md](references/funnel-graph.md) (3-stage conversion), [app-shell-patterns.md](references/app-shell-patterns.md) (shell), [chartjs-configs.md](references/chartjs-configs.md) (drawing Chart.js), [overflow-rules.md](references/overflow-rules.md) (a chart exists), [hero-geometric.md](references/hero-geometric.md) (not copying the starter), [component-recipes.md](references/component-recipes.md) (KPI / action cards).

Recipes stay in references. Copy CSS from examples on disk.

---

## Hard constraints

1. **No decorative images.** Icons: **Phosphor** default. Lucide only if the user asks.
2. **Two font families, never more** -- `--font` + `--font-mono` on `<code>` / `<pre>` only. [Fonts](#fonts).
3. **Light mode default** -- `body.dark` toggle (sibling of `:root`, not nested in it). Re-render Chart.js on theme change.
4. **Anti-Vibe-Code** -- `--accent` from the user. If none, **ask once**. Do not silently use `#2563EB` unless they said CC-family / keep last dashboard.
5. **Self-contained HTML** -- CDN only.
6. **No fake sparklines** on histogram / cross-section snaps. Sparklines only for dated series.
7. **Every displayed count goes through `fmtNum`**. Tables/tooltips: `fmtInt`. Rates: `fmtPct`. Never `toLocaleString()`.
8. **Artifact UI punctuation** -- in the HTML, `-` only (no em/en/`--`). This rule is **artifact UI only**. Chat / Slack drafts still use `--`. Keep `--` in CSS vars, JS, and SQL in `<pre>`.
9. **Color valence** -- up-is-bad is never trust-blue. [color-valence.md](references/color-valence.md).

---

## Invocation checklist

Run **when the skill is called**, before showing the file. Analytics vs shell is the first gate.

### 0. Confirm

- [ ] Archetype: analytics report vs sidebar/top-nav shell (ask only if unclear)
- [ ] v2 already requested → do not re-ask v1 vs v2
- [ ] `--accent` from the user; if none, ask once

### 1. Scaffold

- [ ] Copy `examples/analytics-starter.html` or `examples/app-shell-starter.html` (not a blank file, not v1)
- [ ] Full-page `.page-canvas` + `.shell` z-index 1; theme toggle in `.page-chrome`
- [ ] Four DM Sans weights; no Axiforma `<link>`; `html, body` use `--font`; `code, pre` use `--font-mono`; form controls `font-family: inherit`; `Chart.defaults.font.family` matches `--font`

### 2. Story and copy (analytics only)

- [ ] Overview **is** the hero tab. Title + subtitle (same on every tab) cover: what this is, why read it, what you get, what we aim to achieve. No extra briefing card
- [ ] After the stake chart: ranked **action-item cards** (operative title + research reason with 1-2 numbers). Skip only if there is no recommended move
- [ ] Tabs: Overview → drill-down(s) → Sampling → Methodology. Sampling may be a **filter recap** (inclusion / exclusion / n remaining) -- still its own tab. Not a required session sampler
- [ ] One primary visual per question; chart type from the [chooser](#chart-chooser); title = finding in stakeholder English
- [ ] At most 3 insight bullets under the chart (outcome, not method). One short under-chart caveat only if skipping it would misread the number
- [ ] Extra method / definitions / grain live in **hover info**, `*`, collapse, or Methodology
- [ ] UI strings use `-` only; chat drafts may still use `--`

### 3. Data and numbers

- [ ] Baked `DATA`; buttons use `data-pop`; visible names from `.label`
- [ ] Canonical `fmtNum` / `fmtInt` / `fmtPct`; null → `-` (never `--`)
- [ ] KPIs/axes/prose → `fmtNum`; tables/tooltips → `fmtInt`; rates → `fmtPct`; movements → `pp`
- [ ] Footer: SQL pointer + `generated_at`

### 4. Color and charts

- [ ] For each KPI/fill: up is better / worse / magnitude-only → valence tokens. TOR/DSAT hero starts as `.kpi.hero.is-bad`
- [ ] Ordered scales (mild → rage, TOR bands): rank order + `--sev-*`; driver bars: volume order + end labels
- [ ] Nested subset: arrow + caption between parent and child
- [ ] 3-stage conversion: CSS funnel (hue family **per population**; Cara table is an **example**)
- [ ] Chart ticks and datalabels **14px / 600**. Hide collisions; do not shrink to 11px. Funnel conversion chip stays the loudest number
- [ ] Series colors **locked** across population toggles (same hex for SSA / SR / NS, or Cara vs Chatbot)
- [ ] Click a bar → filter the sibling chart that shares the grain. Two metrics with different baselines (TOR vs resolution) = **toggle**, never dual-axis
- [ ] No histogram sparklines; Chart.js re-renders on theme toggle. Keep `rise` ~300ms, canvas enter on first load, hover ~100ms, `prefers-reduced-motion`. Do **not** default Chart.js animation off

### 5. Chrome and motion

- [ ] Hero KPI / active snap: top bar + wash in the **valence** color
- [ ] Pills synced; long tables in `collapse-card` closed
- [ ] Phosphor icons (unless user asked Lucide); no photos
- [ ] Action-card pointer glow **default ON**; off under `prefers-reduced-motion`; static only if the user kills glow

### 6. Auto-review (silent)

- [ ] Grep list below
- [ ] KPI row: any count ≥ 1000 still raw digits → missed `fmtNum`
- [ ] Hero: bad-when-up in `--accent` blue → valence miss
- [ ] **Copy scan** (required): [Copy-scan pass](#copy-scan-pass)
- [ ] Note fixes in the delivery message

**Shell-only skip:** section 2 except hyphen/fonts; no forced Sampling tab; no forced funnel; no action-item strip.

---

## Overview hero copy

The first tab **is** the hero. Do **not** add a briefing card, extra snaps, or a second title. Title + subtitle stay tab-agnostic (they still show on drill-down / Sampling / Methodology).

- **Title (h1):** research name. No slogan, grain, event IDs, pipeline (`What to fix first`, `session by session`, `4:1148`).
- **Subtitle: 2-3 sentences**, stakeholder English, covering **why read / what you get / what we aim to achieve**. "How we will answer it" is **one clause**, not SQL or funnel mechanics.
- Ban caveats, `COUNT(DISTINCT msid)`, and `engaged → view → submit` as the whole subtitle.
- If copy is ambiguous, draft 3 subtitle options and wait.
- Overview **body** still sets the stake (KPIs + one chart). It does not repeat the four hero beats.

Good shape (adapt, do not paste): `Cara never files most complaints as tickets. This page sizes how often that happens, names the top drivers, and points at what to fix first so we can cut repeat contacts.`

Bad: `Finding the sub-text of our users.` (slogan)

---

## Action-item cards (analytics)

Required on Overview **after** the stake chart when there is a recommended move. Not for app-shell. Do not invent cards if there is no move. Show the strip **once** -- do not duplicate as "Recommended next actions".

**Title:** verb-first operative action (`Stop repeating a failed step`). Not a theme label (`UI grounding`).

**Reason:** why the research points here. 1-2 numbers from `DATA` via formatters. Stakeholder English. Not SQL, not classifier names.

Layout: horizontal ranked strip, swipe + arrows, `scroll-snap`, rank `01`…, title `--text-h3`, reason `--text-sm` / `--ink-soft`. Optional Phosphor icon, owner / effort chips, one highlighted stat. **Pointer-follow glow default ON**; `prefers-reduced-motion` disables it. 3-7 cards. Sort = recommended build order, not theme volume.

```javascript
actions: [
  { rank: 1, title: "Stop repeating a failed step",
    n: 193, agree: 0.92,
    reason: (a) => fmtInt(a.n) + " sessions, " + fmtPct(a.agree * 100, 0) + " agreement - cheapest P0." }
]
```

Bake counts as numbers; format in render. Recipe: [component-recipes.md](references/component-recipes.md#action-item-cards).

---

## Copy-scan pass

Required after the dashboard renders, before showing it. Silent. Fix, then ship.

Visible layer is **load-bearing only**. If a sentence can go without changing what the reader should believe or do, it goes to hover or it gets deleted.

1. **Sense.** Each insight follows from the chart or KPI above it. No leftover claims from an older cut. Numbers in prose match `DATA`.
2. **Minimal.** One idea per sentence. No restating the bars (`Premium is the largest bar`). No method in the insight (`we joined on msid`).
3. **Not a wall.** Hero subtitle 2-3 sentences. At most 3 bullets under a chart. One short under-chart caveat only when it changes how to read the number. No second paragraph of "also note".
4. **Relevant only.** Delete captions that repeat the title. Delete chips that repeat the KPI. Delete taxonomy labels the reader cannot act on.
5. **Hover for extra.** Definitions, grain, why this filter, "what is SSA" -- hover info (or `*` / collapse). Not body copy.

**Fail** if the page looks like a report dump: stacked caveats, insight that retells the chart, info-i as the only place for a caveat that changes the read.

---

## Fonts

Exactly two families. A third on screen is a bug -- almost always an unstyled `<code>`.

```css
--font: "Axiforma", "DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
code, pre { font-family: var(--font-mono); }
code {
  font-size: 0.92em;
  padding: 1px 6px;
  border-radius: 5px;
  background: var(--canvas-deep);
  color: var(--ink);
}
```

```html
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/400.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/500.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/600.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/700.css" rel="stylesheet" />
```

Axiforma has **no public CDN**. Never `<link>` / `@import` it. Load all four DM Sans weights.

- Set family on `html, body`. `button, input, select, textarea { font-family: inherit; }`
- `Chart.defaults.font.family` = the same string as `--font`
- Phosphor is an icon font; it does not count toward the two

`--text-hero-display` only on the page hero h1. Sections stay `--text-h2`.

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

Before a fill: **if this number goes up, is that better or worse?** Full rules: [color-valence.md](references/color-valence.md).

| Direction | Color |
|-----------|--------|
| Up is bad | `--warning` `#ff9323` → `--sev-hi` / `--danger` `#da0808` |
| Up is good | `--success` / `--sev-ok` `#69c440`, or `--accent` |
| Magnitude only | `--accent` / `--ink` |

Never paint TOR / DSAT / dissatisfaction / rage share in trust-blue. Ordered negative states: `--sev-lo` `#f1dc32` → `--sev-mid` `#ff9323` → `--sev-hi` `#da0808` left-to-right by **rank**, never volume, never the accent ramp. Dark ink `#1D1D1F` on ok / lo / mid; white on hi / max. "Has the bad signal vs remainder" uses `--sev-flag`, not `--accent`. In-bar type `--text-h3` / `--text-sm`. Series hexes stay **locked** when a population toggle flips.

Hero / active snap: top bar + wash in the **valence** color. `.kpi.hero` accent chrome is for good-when-up / magnitude only. TOR/DSAT start as `.kpi.hero.is-bad`.

---

## Chart chooser

Pick by the **question**. Implementations live in [chartjs-configs.md](references/chartjs-configs.md), [overflow-rules.md](references/overflow-rules.md), [funnel-graph.md](references/funnel-graph.md).

| Question | Chart |
|----------|--------|
| Rank / compare categories / drivers | Horizontal bar, volume sort, end labels. Long names → horizontal, not vertical |
| Few discrete periods (quarters, 4-8 weeks) | Vertical bar |
| Trend over continuous time | Smooth line `tension: 0.4`. Two series → dual-line + crosshair. 5+ series → small multiples |
| Widget footer trend | Sparkline **only if dated**. Never under a histogram bucket |
| Distribution / buckets / histogram | Vertical bar, `borderRadius: 12` |
| Part-to-whole, 2-4 slices | Doughnut, total in center. **5+ slices or one slice >80%** → horizontal bar |
| Mix + a second metric (mean, rate) | Stacked / 100% stacked bar with overlay tick. Not a fourth KPI. Not three charts of the same mix |
| Ordered negative scale (mild → rage, TOR bands) | Stacked HTML bar, **rank** order, `--sev-*` |
| Sequential conversion (eligible → viewed → submitted) | CSS column funnel. Not Chart.js, not Sankey |
| Cross-population compare | KPI + trend chips + snap grid (not a grouped bar of 12 pops) |
| Density over calendar time | CSS heatmap. Accent ramp if magnitude-only; `--sev-*` if the cell is a bad-when-up rate |
| Exact values / audit / many columns | Table (`fmtInt`). Collapse if long |
| Volume + rate together over few categories | Combo (bars + line), dual axis. Disable datalabels on one series |
| Relationship / correlation | Scatter (rare). Do not connect unordered categories with a line |
| Single status number | KPI card. Not a one-bar chart. Not a gauge |

**Never:** pie (use doughnut or bar); Chart.js funnel / Sankey for 3-stage survey drop; radar; word cloud unless asked; photos as charts.

3-4 sequential conversion stages → funnel recipe. Mix/share → bar/doughnut. **Not every dashboard needs a funnel.**

CSS funnel rule: one hue family per population, 400/500/600, 4-8% sheen, no neon orange. Cara All / sky / violet / apricot is a **worked example**, not global law. Do not paint Chatbot apricot onto an unrelated dashboard.

---

## Required v2 chrome

- Full-page `.page-canvas` (mesh, 5 pills, vignette). First-load `canvasEaseIn` + `meshEaseIn`. Toggle in `.page-chrome`. [hero-geometric.md](references/hero-geometric.md)
- Pill toggles: solid `--accent` when active; sync duplicates. [state-patterns.md](references/state-patterns.md)
- Trend chips: `+X.XXpp vs {baseline.label}`
- Long secondary content: `<details class="collapse-card">` **closed**. Headline + primary chart stay visible
- Linked charts: clicking a bar filters the sibling that shares the grain. TOR vs resolution = metric **toggle**, never one dual-axis. [state-patterns.md](references/state-patterns.md)
- Insight: borderless + shadow (not v1 left border)

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

Pre-aggregate before embedding. `data-pop="segment_a"`; visible text uses `.label`. `renderAll()` updates KPIs, chart, snaps, insight together. Footer: `SQL: ... · Generated {fmtDate(DATA.generated_at)}`.

Optional live dashboard (may not exist in this workspace): `ab-tests/priority-general-agent/dashboards/multi-site-accounts-v2.html`. In-skill proofs: `examples/analytics-starter.html`, `examples/funnel-graph.html`.

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
- Analyst-process in the insight (`we joined on msid`, `batch 4:1148`)
- Three charts of the same mix; insight after secondary charts; hardcoded fractions
- Horizontal bars without end labels; ordered scale sorted by volume
- Sampler buried in Methodology; Methodology not last; Sampling skipped on analytics
- Em/en/`--` punctuation in **artifact UI**
- Chart.js / Sankey for 3-stage survey funnel; one `--accent` for every funnel population
- Neon chatbot orange next to Cara blues; ice-300 funnel fills; two-tone funnel bars
- Bad-when-up hero in `--accent` blue; two blues for mild vs frustrated; green for mild-bad
- White type on `--sev-ok` / `--sev-lo` / `--sev-mid`; black type on `--sev-hi` / `--sev-max`
- Shrinking chart labels to 11px; reminting series colors per population toggle
- Dual-axis for TOR vs resolution; action-item strip duplicated as a second list
- Duplicating full v1 SKILL.md into v2 files

---

## Auto-review (before delivery)

1. Phase 0 -- numbers match source; labels match `DATA.*.label`
2. Phase 1 -- charts render; toggles sync; no console errors; overflow rules
3. Phase 2 -- **this file's inherit table + gated checklist**, not v1 "one font / Chart.js funnel / `--` sentinel"
4. Grep and fix:

| Grep | Expect |
|------|--------|
| `toLocaleString` | zero hits |
| `font-family` | only `--font`, `--font-mono`, and `inherit` |
| `<code` / `<pre` | matching `code, pre` CSS rule |
| `axiforma` in a `<link>` / `@import` | zero hits |
| `text-h1` on hero | zero hits -- hero uses `--text-hero-display` |
| `Chart.defaults.font.family` | present, equal to `--font` |
| `toFixed(1) + "K"` | zero hits |
| `fmtNum` / `fmtInt` / `fmtPct` bodies | present; null sentinel `"-"` not `"--"` |
| `—` `–` | zero hits |
| ` -- ` in visible copy | zero hits (ignore `var(--token)` and SQL `--` in `<pre>`) |

5. Read the KPI row, hero color, mild → rage order, then run the [copy-scan](#copy-scan-pass).

Fix before showing. Note what was fixed.

---

## Additional resources

| File | When |
|------|------|
| [v2-delta.md](references/v2-delta.md) | What differs from v1 |
| [layout-archetypes.md](references/layout-archetypes.md) | Analytics vs shell |
| [component-recipes.md](references/component-recipes.md) | KPI, snaps, action cards |
| [funnel-graph.md](references/funnel-graph.md) | CSS survey funnel |
| [analytics-storytelling.md](references/analytics-storytelling.md) | Tab arc, overlap, copy-scan |
| [dashboard-patterns.md](references/dashboard-patterns.md) | Analytics layout |
| [state-patterns.md](references/state-patterns.md) | Pills, hover info, linked charts |
| [chartjs-configs.md](references/chartjs-configs.md) | Chart.js extensions; 14px ticks |
| [overflow-rules.md](references/overflow-rules.md) | Clip / collision rules |
| [examples/analytics-starter.html](examples/analytics-starter.html) | Analytics scaffold (copy from disk) |
| [examples/app-shell-starter.html](examples/app-shell-starter.html) | Shell scaffold |
| [examples/funnel-graph.html](examples/funnel-graph.html) | Funnel graph dummy bake |

**v1 inherited (do not duplicate):** [eyal-visualization/SKILL.md](../eyal-visualization/SKILL.md) -- 16 principles, Phase 0-1, delivery standards. Phase 2 visual laws: use the inherit table above.

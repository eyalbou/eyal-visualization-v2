# Analytics Storytelling (v2)

Patterns for investigation and presentation dashboards: RCA, prevalence studies, taxonomy, funnel + score + reasons.

Hero copy (title = research name; subtitle = why / get / aim in 2-3 sentences) lives in [hero-geometric.md](hero-geometric.md). This file is the tab arc, overlap rules, driver charts, action cards, and copy-scan.

---

## North-star questions

Before building, list the 3-5 questions the viewer must answer without opening a spreadsheet:

| Pattern | Example questions |
|---------|-------------------|
| Prevalence | How common is X in the sampled population? |
| Drivers | What are the main root causes / reasons? |
| Initiators | What triggers each driver? (intent, channel, product area) |
| Proof | What do top drivers look like in real examples? |
| Share | What fraction does each reason represent? |

Every **section and chart** must map to one question. Delete sections that do not.

Put **why read / what you get / what we aim to achieve** in the **hero subtitle** (2-3 sentences). "How we will answer it" is one clause, not SQL. If the line is ambiguous, draft 3 options and wait. The Overview tab **is** the hero -- no extra briefing card.

---

## Single population rule

- One headline rate for the **whole analyzed sample**
- Never show batch names, CTAS labels, or dedup rules in hero KPIs or narrative tabs
- Pipeline metadata belongs in **Methodology** only (collapsed `<details>` or last tab)

---

## KPI selection

**Hero row (max 3 cards)** -- `1fr 1fr 1.35fr`. A fourth metric overlays the primary chart (avg tick on a mix bar) instead of a fourth card.

1. Primary metric (prevalence / rate / count)
2-3. Supporting rate or n (not a second view of the same mix)

Each KPI subtitle: count + share. Definitions go in **click elaboration panel** (info icon), not inline jargon.

---

## Investigation tab arc (default)

Tabs are a **story sequence**, not a gallery of leftover charts. Walk the reader from the overview to the finding, then hand them proof and the recipe.

| Order | Story beat | What to show | What not to show |
|-------|------------|--------------|------------------|
| **1 Overview** | Introduce the story. How big is this, or what are we trying to find? Often **volume / funnel**. Pick graphs that set the stake. After the stake chart: ranked **action-item cards** (skip only if there is no recommended move). | 3 KPIs, one primary chart, 3-bullet read, action strip | Driver taxonomy, SQL, sampler, a second briefing card |
| **2-n Drill-down** | Each tab answers one question the previous tab set up. Build toward the interesting finding -- do not dump it first. | One primary visual + insight; collapse tables | Repeating Tab 1 KPIs; three views of the same mix |
| **Sampling** | Always last-but-one. Full filter recap (inclusion / exclusion / n remaining). A session sampler is optional -- the recap is enough. | Filter recap and/or working tool + conversation links | Analysis charts |
| **Methodology** | Always last. How we know + **project documentation** (scope, grain, joins, caveats, SQL, definitions). | Collapsed SQL, scope vs stage-2 split | Repeated driver charts |

Hero + tab chrome persist. Title and subtitle stay the same on every tab. Optional deep link: `?tab=`.

Analyst names are allowed on the middle tabs (`Volume`, `Satisfaction`, `What was wrong`) when that is clearer than Summary / Why / Where. Do not force RCA names on an exploration dashboard. Do not skip Sampling or put it inside Methodology. Sampling may be a filter recap with no session tool -- still its own tab.

### How to pick Overview graphs

Ask: if the reader left after Tab 1, would they know the stake? Volume of who saw the survey, overall conversion, Cara vs Cara CF -- yes. Chip taxonomy -- no, that is a later beat.

### How to chain drill-downs

Each tab should make the next one inevitable. Example: Overview (who submits) → Satisfaction (how they score, where Cara wins) → What was wrong (why low scores) → Sampling (read the sessions) → Methodology (how the numbers were built).

If you found something surprising, do not open with it. Build the path so the finding is the payoff of the previous chart.

---

## Overlap (one visual per question)

- Mix **or** mean **or** histogram -- not all three. Overlay the second metric (avg tick + number on the mix chart).
- One home for a caveat (insight or Methodology `i`). Delete repeats in guide-blocks and snap chips.
- Put the **read** (at most 3 bullets, outcome not method) directly under the primary chart, not after two more charts.
- One short under-chart caveat only if skipping it would misread the number. Definitions, grain, extra why: hover info (or `*` / collapse / Methodology).
- Thin-n charts (intent titles with n 5-16) go in `collapse-card` or drop; keep the grain that actually has sample.

---

## Driver + initiator + examples pattern

For taxonomy / RCA dashboards, each **top driver** gets a block:

```
Headline: driver name + share
Plain-English definition (hover)
Top initiators table (what triggered this driver)
N example rows (links + snippet)
```

Do not rely on intent-only samplers when the story is about **drivers** -- invert the cross-tab.

---

## Bar end labels + sort (mandatory)

Use `chartjs-plugin-datalabels` on horizontal bar charts:

- Count + rate: `{count} ({pct})`
- `anchor: 'end'`, `align: 'end'`, `clip: false`
- Font must match `Chart.defaults.font.family`

**Default sort = volume** (highest share on top). Optional pill: **Volume** | **Survey order** (catalog / appearance order). Filter chips may stay in survey order so they match the form. Ties keep catalog order.

**Exception -- ordered scales.** Severity (mild → frustrated → rage), TOR bands, and any ordinal heat sort **by rank**, left-to-right or top-to-bottom, not by volume. Volume stays in the labels. Legend matches the bar. See [color-valence.md](color-valence.md).

---

## Nested distribution

When chart B is how a **segment of chart A** breaks (Dissatisfied → heat among the dissatisfied), put a connector between the cards: Phosphor `ph-arrow-down` + one line naming the subset. Derive n from `DATA` (`fmtInt`). Do not rely on titles alone. Full recipe: [color-valence.md](color-valence.md#7-nested-distribution-drill-down-arrow).

---

## Hover elaboration panels

Use info-icon popovers (`.elab-panel`) for:

- Wilson CI / go-no-go methodology
- Multi-label taxonomy note (shares sum >100%)
- Intent coverage vs population benchmark
- Driver definitions and fix hints

Chart.js tooltips for bar hover detail. Never use `title=` alone for critical methodology.

---

## Number formatting

Canonical scale and implementations (including `fmtPct`): [SKILL.md](../SKILL.md#number-formatting).

- `fmtNum(n)` for counts on display surfaces -- KPIs, axes, bar labels, narrative prose
- `fmtInt(n)` for counts in tables and tooltips -- those are the audit trail, keep exact digits
- `fmtPct(x, d)` for all rates -- never raw decimals in UI; movements in `pp`
- Never `toLocaleString()`
- Tables: `font-variant-numeric: tabular-nums` on numeric columns

Prose reads as speech, so it takes the compact form: "25.16K events, 67.96% of the total" -- not "25,161".

---

## Anti-patterns

- Duplicating prevalence in KPI + corpus section + bounds table
- Three charts of the same mix (overlay instead)
- The same caveat in a guide-block + insight + snap chips
- Insight after secondary charts instead of under the primary chart
- Intent coverage / backfill counts in hero KPIs
- Rules/classifier layer in main story (appendix only)
- Hardcoded fractions in insights (`47/118`) -- always derive from `DATA`
- Funnel copy, caveats, or SQL as the hero subtitle
- Driver bars frozen in survey order with no volume default
- Severity / TOR-band stacked bars sorted by volume (frustrated left of mild)
- Subset chart stacked under a parent split with no drill-down arrow
- Sampler inside Methodology; Methodology not last
- Single 10-section scroll for executive presentation (use tabs)
- Insight that retells the bars; method in the insight (`we joined on msid`)
- A second "recommended actions" list that duplicates the Overview strip

---

## Action-item cards (Overview)

After the stake chart. Verb-first title + research reason with 1-2 formatted numbers. Glow default on. Recipe: [component-recipes.md](component-recipes.md#action-item-cards). Skip only if there is no recommended move. Show once.

---

## Copy-scan pass

Required before showing the file. Visible text is load-bearing only. Extra explanation in hover. Full scan: [SKILL.md](../SKILL.md#copy-scan-pass).

Fail if the page is a report dump, the insight retells the chart, or a caveat that changes the read lives only in the info-i.

---

## QA checklist

Master gated list: [SKILL.md](../SKILL.md#invocation-checklist). Analytics extras:

- [ ] Tab 1 (Overview) readable in <60s -- stake is clear if the reader stopped here
- [ ] Action-item cards after the stake chart (or skipped with a reason)
- [ ] Each later analysis tab is a drill-down of the previous, not a parallel dump
- [ ] Sampling is last-but-one (filter recap is enough); Methodology is last
- [ ] Hero subtitle is 2-3 sentences: why / get / aim; identical on every tab
- [ ] One visual per question; at most 3 insight bullets; one under-chart caveat max
- [ ] Copy-scan passed -- insights follow the chart; no bar restatement; extra in hover
- [ ] Every horizontal bar has end labels; default sort is volume **except ordered scales (severity, TOR bands) which sort by rank**
- [ ] No batch jargon above Methodology tab
- [ ] Playwright: each tab activates without console errors

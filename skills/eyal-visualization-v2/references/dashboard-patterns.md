# Dashboard Patterns (v2)

DATA shape, population toggles, hover strip, snaps, insight, footer: this file + [SKILL.md](../SKILL.md). Chrome overrides: [v2-delta.md](v2-delta.md). Do not read v1 paths.

---

## v2-specific overrides

| Avoid | Use instead |
|-------|-------------|
| Grain + radial mesh on `body` | Full-page `.page-canvas` geometric layer |
| Masthead eyebrow line | Kokonut badge pill with dot |
| Left-aligned `--text-h1` title | Centered `--text-hero-display` two-line gradient |
| Inset pill toggles | Solid accent active pills |
| Left-border insight | Borderless card + shadow |
| `.active-pop` border ring | Top accent bar + `--accent-glow` wash |
| Optional grain atmosphere | `canvasEaseIn` + `meshEaseIn` on first load |
| Long tables / examples always visible | `<details class="collapse-card">` default **closed** |

---

## Collapsible sections (page length)

On multi-section or multi-tab dashboards:

1. **Charts + KPIs stay open** -- the 5-second scan path.
2. **Tables, example lists, heatmaps, explorer results, appendices** -- `collapse-card`, no `open` attribute.
3. **Per-category drill-down** -- card headline visible; initiators + examples in nested `collapse-nested`.
4. **Summary line on the right** -- `.collapse-meta` with row counts (`96 loops · 5 examples`).

Recipe: [state-patterns.md](state-patterns.md) collapsible section.

Validated: `investigations/chatbot-loops/analysis/loop-rca-v440.html` (Tab 2 product-failure drill-downs).

## Analytics layout (validated)

```
page-canvas (fixed)
page-chrome (theme)
shell
  hero-geometric__content
  pop-card + synced toggles
  kpi-grid (1fr 1fr 1.35fr)
  card (chart + hover strip + caption)
  insight
  snap-grid
  footer
```

Volume / survey conversion uses the CSS funnel in [funnel-graph.md](funnel-graph.md), not a Chart.js card. Standalone: `assets/funnel-graph.html`.

In-skill proofs: `assets/analytics-starter.html`, `assets/funnel-graph.html`. Optional live (may not exist here): `ab-tests/priority-general-agent/dashboards/multi-site-accounts-v2.html`.

Starter template: `assets/analytics-starter.html`. Copy from disk; do not Read the full HTML into context.

---

## Presentation tab layout

Default investigation arc -- see [analytics-storytelling.md](analytics-storytelling.md):

```
hero + tab-bar (persistent -- same title + subtitle on every tab)
  Tab 1 Overview     -- stake: often volume / funnel; 3 KPIs + one chart + read
  Tabs 2-n Drill-down -- one question each, chained toward the finding
  Sampling           -- last-but-one; filter recap (session tool optional).
                       Session table: uuid = UM link; conversation id = conversation URL;
                       never a second URL column (see SKILL.md Sampling table)
  Methodology        -- last; scope, grain, SQL, project documentation
```

Analyst tab labels (`Volume`, `Satisfaction`, `What was wrong`) are fine. RCA names (Summary / Why / Where) are optional on the middle tabs only. Never skip Sampling (a filter recap is enough). Never put the sampler inside Methodology.

Footer: `generated_at` on every tab. SQL details stay in Methodology.

---

## Checklist (v2 dashboard-specific)

Master gated list: [SKILL.md](../SKILL.md#invocation-checklist). Visual laws: [SKILL.md](../SKILL.md#visual-system-this-skill).

- [ ] Hero title is the research name; subtitle is why / get in **≤35 words / ≤2 sentences**, on every tab
- [ ] Tabs: Overview → drill-down(s) → Sampling → Methodology (Sampling may be a filter recap)
- [ ] Session sampler (if present): uuid and conversation id are the hyperlinks, not extra URL columns
- [ ] Overview action-item cards after the stake chart (or skipped because there is no move)
- [ ] Full-page `.page-canvas` -- not hero-card background
- [ ] `--text-hero-display` for page hero only; sections use `--text-h2`
- [ ] Theme toggle in `.page-chrome`; charts re-render on `setTheme`
- [ ] Pill toggles synced across duplicate controls
- [ ] Hero KPI + active snap: top bar + glow wash in the **valence** color
- [ ] Trend chips for cross-pop comparison; no histogram sparklines
- [ ] Copy-scan passed; extra explanation in hover; `copy-check.py` exits 0
- [ ] Hero chips ≤3 × ≤4 words -- scope / window / n / freshness, no pipeline or tool names
- [ ] Light default; dark mode token overrides in `body.dark { }` sibling of `:root`
- [ ] `generated_at` in footer; canonical `fmtNum` / `fmtInt` / `fmtPct`; null → `-`
- [ ] No em dash, en dash, or `--` in UI copy; use `-`
- [ ] `prefers-reduced-motion` respected; action-card glow off under it
- [ ] No decorative images; Phosphor icons (Lucide only if asked)

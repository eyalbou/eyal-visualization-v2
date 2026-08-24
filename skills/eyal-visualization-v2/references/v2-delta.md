# v2 Delta (Soft UI Layer)

Rules that differ from v1 `eyal-visualization`. Everything else inherits from v1 unchanged.

When v1 Phase 2 visual laws fight this file, **v2 wins**. Inherit table: [SKILL.md](../SKILL.md#when-v1-fights-v2-v2-wins).

Icons: **Phosphor** default. Lucide only if the user asks.

**Typography:** Link only -- do not copy. [v1 design-system section 4](../../eyal-visualization/references/design-system.md) + dashboard CSS variables block.

---

## Surface & layout

| Token / pattern | v2 value |
|-----------------|----------|
| `--canvas` | `#F5F5F7` light |
| `--page-bg` | Full-page gradient (light) / `#030303` (dark) |
| `--surface` | `#FFFFFF` cards on canvas |
| `--radius` | 20px cards |
| `--radius-lg` | 24px hero-adjacent cards |
| `--radius-pill` | 9999px toggles, badges, chips |
| `--shadow-md` | `0 4px 24px rgba(0,0,0,0.06)` |

Cards: white, no border (or hairline), soft shadow -- not v1 editorial borders + grain.

---

## Full-page geometric canvas

Not a hero card. See [hero-geometric.md](hero-geometric.md).

- `.page-canvas` fixed `inset: 0`, z-index 0
- Mesh + 5 pill shapes + vignette
- `--page-bg` on `::before` (theme crossfade without replaying enter animation)
- First-load: `canvasEaseIn`, `meshEaseIn`, `vignetteEaseIn`
- Content in `.shell` at z-index 1

---

## Hero typography exception

| Token | Use |
|-------|-----|
| `--text-hero-display` | Page hero h1 only (`clamp(2.5rem, 6vw + 1rem, 4.75rem)`) |
| `--text-h2` | Section titles (20px) -- unchanged |
| `--text-h1` | Do not use for Kokonut hero |

Centered two-line gradient title + badge pill. Theme toggle in `.page-chrome` fixed top-right.

**Copy:** h1 = research name (`Cara Feedback Modal`), not a slogan or method. Subtitle = why read / what you get / what we aim to achieve (2-3 sentences). "How we will answer it" is one clause. Tab-agnostic. Full rules: [hero-geometric.md](hero-geometric.md#hero-copy-required).

---

## Interactive controls

- **Pill toggles:** track `--canvas-deep`; active = solid `--accent` + white text
- Sync duplicate toggles (e.g. `.pop-btn` + `.hist-pop-btn`) via one `setPopulation()`
- **Trend chips:** cross-section comparison (`+X.XXpp vs baseline`) -- not time series
- **Collapse drill-downs:** `<details class="collapse-card">` default closed for tables, examples, lists, appendices; KPIs + primary charts stay open. See [state-patterns.md](state-patterns.md)
- **Survey funnel:** CSS columns, not Chart.js. One hue family per population, 400/500/600, 4-8% sheen. The Cara All / sky / violet / apricot ramps in [funnel-graph.md](funnel-graph.md) are a **worked example**, not global law.
- **Action-item cards** on Overview after the stake chart. Glow default on. See [component-recipes.md](component-recipes.md#action-item-cards).
- Chart ticks and datalabels **14px / 600**. Hide collisions; do not shrink to 11px.

---

## Metric surfaces

- **Hero KPI:** top bar + wash + `--text-kpi-hero` value in the **valence** token. `--accent` only when good-when-up or magnitude-only (analysed n). Bad-when-up rates use `--sev-flag` / `--danger` / `--warning`. See [color-valence.md](color-valence.md).
- **Active snap card:** same top bar + wash -- no `box-shadow` ring (selection chrome stays `--accent`)
- **No histogram sparklines** on population snap cards
- **Severity / heat:** 5-stop palette `--sev-ok` `#69c440` → `--sev-lo` `#f1dc32` → `--sev-mid` `#ff9323` → `--sev-hi` `#da0808` → `--sev-max` `#950404`. Default 3-stop heat skips ok and max. Never the accent ramp. Sort by rank, not volume. Dark ink on ok / lo / mid; white on hi / max. Nested subset charts get a drill-down arrow.

---

## Insight & chart chrome

- Insight: borderless card + `--shadow-md` (not v1 left-accent border)
- Chart hover strip: `--canvas-deep` well, no left border (v2)
- Bar `borderRadius: 12` for soft look

---

## Motion

| Element | Timing |
|---------|--------|
| Content `rise` | 300ms stagger |
| Hovers | 100-125ms |
| Page canvas enter | 1.8-2.2s Kokonut ease (first load only) |
| Shape enter | 2.4s stagger 0.3-0.7s |
| Shape float | 12s infinite |

`prefers-reduced-motion`: snap canvas to final state; disable float.

---

## Dark mode

- `--page-bg: #030303`
- Brighter shape opacities (12-22%)
- White / indigo / rose title gradients
- Cards: `#1C1F28` surface, elevated shadows

---

## Anti-Vibe-Code

Start from user `--accent`. Do not default every dashboard to `#2563EB` unless requested.

In-skill proofs: `examples/analytics-starter.html`, `examples/funnel-graph.html`. Optional live (may not exist here): `ab-tests/priority-general-agent/dashboards/multi-site-accounts-v2.html`.

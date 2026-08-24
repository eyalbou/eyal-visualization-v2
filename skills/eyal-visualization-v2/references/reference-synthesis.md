# Reference Synthesis (5 dashboard refs)

Design notes extracted from reference images. **Output must never include photos, avatars, 3D art, or logo images.**

Use these to pick components per archetype -- see [layout-archetypes.md](layout-archetypes.md).

---

## SocialSync (analytics SaaS)

**Archetype:** Sidebar shell + analytics widgets

| Pattern | v2 encoding |
|---------|-------------|
| Soft shadow white cards | `--shadow-md`, `--radius-lg` |
| Metric + trend chip | [component-recipes.md](component-recipes.md) trend chip |
| Sparkline footer | **Only** for dated time-series metrics |
| Pill time-range | `.pop-btn` / filter chip pattern |
| Heatmap grid | [chartjs-configs.md](chartjs-configs.md) heatmap section |

---

## Light financial dashboard

**Archetype:** Sidebar shell

| Pattern | v2 encoding |
|---------|-------------|
| Canvas `#F5F5F7` | `--canvas` default |
| Black/accent pill CTAs | Map to user `--accent` |
| Transaction list rows | [app-shell-patterns.md](app-shell-patterns.md) list row |
| Category pills on rows | `.category-pill` |
| Filter chip row above chart | Solid accent active chip |
| Dual-line + crosshair | [chartjs-configs.md](chartjs-configs.md) |
| Date badge squares | Month/day pill in schedule lists |

---

## Dark fintech dashboard

**Archetype:** Sidebar shell

| Pattern | v2 encoding |
|---------|-------------|
| Card grid in rounded container | `.widget-grid` + outer padding |
| Search + bell + numeric badge | Header actions, no avatar |
| Toggle switches | [state-patterns.md](state-patterns.md) |
| Smooth minimal line chart | `tension: 0.4`, light grid |
| Floating bold value on hover | Chart.js tooltip emphasis |
| "Digit of the day" contrast pill | Light pill on dark card |

---

## Crextio (HR / warm UI)

**Archetype:** Top-nav shell

| Pattern | v2 encoding |
|---------|-------------|
| Top horizontal nav, dark active pill | [app-shell-patterns.md](app-shell-patterns.md) topnav |
| Warm off-white gradient canvas | `--page-bg` warm variant |
| Gold/yellow progress | Map to user `--accent` |
| Segmented progress bars | CSS multi-stop `linear-gradient` on track |
| Circular progress ring | SVG `stroke-dasharray` -- no photos |
| Weekly calendar event pills | Horizontal rounded pills in strip |
| Dark contrast task card | `--surface` on darker `--canvas` |
| Accordion rows | `details/summary` or JS toggle |

---

## skillalley (education / schedule)

**Archetype:** 3-column shell

| Pattern | v2 encoding |
|---------|-------------|
| Sidebar + main + right detail | `.app-layout--3col` |
| Pill active nav + notification badge | `.side-nav__item` + `.nav-badge` |
| Vertical timeline | Left time axis + variable-height cards |
| Pastel category card tints | `--accent-2-soft` per category |
| Circular progress on cards | SVG ring |
| Hero CTA primary pill | Solid `--accent` button |

---

## Explicit skips (all references)

Do not implement:

- Profile photos or avatar stacks
- Brand logo images in headers
- 3D illustrations or decorative hero photography
- Overlapping user avatar groups
- Stock imagery of any kind

Use: **Phosphor** icons (Lucide only if asked), icon circles, initials in typographic badges if identity is required.

---

## v2 validated synthesis

The approved analytics artifact combines:

- Kokonut full-page geometric hero ([hero-geometric.md](hero-geometric.md))
- SocialSync-style soft cards + trend chips
- Financial-style pill population toggles
- Soft UI DATA keys (`label`, `generated_at`)

This is the **default analytics archetype** for v2.

In-skill proofs: `assets/analytics-starter.html`, `assets/funnel-graph.html`. Optional live: `ab-tests/priority-general-agent/dashboards/multi-site-accounts-v2.html`.

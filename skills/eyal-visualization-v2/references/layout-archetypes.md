# Layout Archetypes

Pick **one archetype before building**. Each maps to an example starter and reference set.

---

## Decision tree

```
What are you building?
|
|-- Internal SQL-backed report, AB sizing, single narrative
|   -> ANALYTICS (hero geometric + KPI + chart + insight)
|
|-- Multi-section product dashboard, many nav items
|   -> SIDEBAR SHELL (228px nav + card grid)
|   -> Optional: 3-COLUMN (+ sticky detail panel)
|
|-- Fewer nav items, warmer product/marketing feel
    -> TOP-NAV SHELL (horizontal pill nav + card grid)
```

---

## 1. Analytics report

**When:** AB tests, population sizing, one-off investigations, SQL baked into HTML.

**Layout:**
```
[page-canvas full viewport]
[page-chrome: theme toggle]
[hero geometric: badge + gradient title + subtitle + meta badges]
[population card: pill toggles]
[kpi grid: 2 + hero column]
[chart card + synced toggles + hover strip]
[insight box]
[snap grid: all segments]
[footer: SQL + generated_at]
```

**References:** [hero-geometric.md](hero-geometric.md), [component-recipes.md](component-recipes.md), [soft-ui-tokens.md](soft-ui-tokens.md)

**Example (copy from disk):** `examples/analytics-starter.html`

**In-skill proof:** `examples/analytics-starter.html`. Optional live (may not exist here): `ab-tests/priority-general-agent/dashboards/multi-site-accounts-v2.html`

---

## 2. Sidebar app shell

**When:** Ongoing product dashboard (SocialSync, financial SaaS style).

**Layout:**
```
[sidebar 228px fixed] | [header: search + icon actions]
                      | [card grid: mixed widget sizes]
                      | [optional: metric + trend + sparkline IF time series]
```

**References:** [app-shell-patterns.md](app-shell-patterns.md), [component-recipes.md](component-recipes.md)

**Example:** `examples/app-shell-starter.html`

**No images:** profile = icon circle only, never photos.

---

## 3. Top-nav app shell

**When:** Fewer sections, Crextio-style warm UI, horizontal navigation.

**Layout:**
```
[top bar: logo text + pill nav items + actions]
[warm gradient canvas]
[card grid below]
```

**References:** [app-shell-patterns.md](app-shell-patterns.md), [soft-ui-tokens.md](soft-ui-tokens.md)

---

## 4. Three-column variant (sidebar + detail)

**When:** Selecting a list item needs persistent context panel (schedule, education).

**Layout:** Sidebar | main content | right detail panel (sticky).

**References:** [app-shell-patterns.md](app-shell-patterns.md) section 3, [reference-synthesis.md](reference-synthesis.md) skillalley notes.

---

## Archetype vs v1

| Need | Use |
|------|-----|
| Editorial grain, warm terracotta, internal briefing | v1 `eyal-visualization` |
| Soft product UI, geometric hero, pill controls | v2 (this skill) |
| Wix branding | `studio-data-visualization` |

# State Patterns (v2)

**Inherit v1:** [eyal-visualization/references/state-patterns.md](../../eyal-visualization/references/state-patterns.md) -- toasts, empty states, loading, validation, success.

**v2 additions below:** pill toggles, filter chips, toggle switches, notification badges.

Tokens: [soft-ui-tokens.md](soft-ui-tokens.md)

---

## Pill population toggle (synced)

```html
<div class="pop-toggle" role="tablist" aria-label="Population selector">
  <button class="pop-btn active" data-pop="exposed" role="tab" type="button" aria-selected="true">Exposed</button>
  <button class="pop-btn" data-pop="baseline" role="tab" type="button" aria-selected="false">Baseline</button>
</div>
```

```css
.pop-toggle {
  display: flex;
  flex-wrap: nowrap;
  gap: 4px;
  padding: 4px;
  background: var(--canvas-deep);
  border-radius: var(--radius-pill);
  overflow-x: auto;
}
.pop-btn {
  flex-shrink: 0;
  white-space: nowrap;
  padding: 8px 16px;
  border: none;
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--ink-soft);
  background: transparent;
  cursor: pointer;
  transition: background 100ms ease, color 100ms ease, box-shadow 100ms ease;
}
.pop-btn:hover:not(.active) { color: var(--ink); background: rgba(0,0,0,0.04); }
.pop-btn.active {
  background: var(--accent);
  color: #fff;
  box-shadow: var(--shadow-sm);
}
.pop-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.pop-btn:active:not(.active) { transform: scale(0.98); }
```

Sync duplicates:

```javascript
function setPopulation(key) {
  currentPop = key;
  document.querySelectorAll(".pop-btn, .hist-pop-btn").forEach((btn) => {
    const active = btn.dataset.pop === key;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-selected", String(active));
  });
  renderAll();
}
```

---

## Filter chips (above chart)

```html
<div class="filter-chips" role="group" aria-label="Filters">
  <button class="filter-chip active" type="button">All</button>
  <button class="filter-chip" type="button">Last 7 days</button>
  <button class="filter-chip" type="button">Last 30 days</button>
</div>
```

```css
.filter-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.filter-chip {
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  font-size: var(--text-sm);
  font-weight: 500;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--ink-soft);
  cursor: pointer;
  transition: background 100ms ease, border-color 100ms ease, color 100ms ease;
}
.filter-chip.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}
```

Always include an **All** reset option for SQL-sourced filters.

---

## Toggle switch

```html
<label class="toggle">
  <input type="checkbox" class="toggle__input" />
  <span class="toggle__track" aria-hidden="true"></span>
  <span class="toggle__label">Show benchmarks</span>
</label>
```

```css
.toggle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: var(--text-sm);
  color: var(--ink);
}
.toggle__input { position: absolute; opacity: 0; width: 0; height: 0; }
.toggle__track {
  width: 44px;
  height: 24px;
  border-radius: var(--radius-pill);
  background: var(--canvas-deep);
  position: relative;
  transition: background 150ms ease;
}
.toggle__track::after {
  content: "";
  position: absolute;
  top: 3px;
  left: 3px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  transition: transform 150ms ease;
}
.toggle__input:checked + .toggle__track { background: var(--accent); }
.toggle__input:checked + .toggle__track::after { transform: translateX(20px); }
.toggle__input:focus-visible + .toggle__track { outline: 2px solid var(--accent); outline-offset: 2px; }
```

---

## Notification badge

```css
.nav-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: 600;
  border-radius: var(--radius-pill);
  background: var(--accent);
  color: #fff;
}
```

On icon buttons, position absolute top-right:

```css
.btn-icon { position: relative; }
.btn-icon .nav-badge {
  position: absolute;
  top: -4px;
  right: -4px;
}
```

---

## Trend chip (metric context)

See [component-recipes.md](component-recipes.md). States: `.up` (green), `.down` (red), `.neutral` (gray).

Inverted metrics (error rate): flip color logic -- lower is better.

---

## Theme toggle button

```html
<button class="btn-icon" id="themeBtn" type="button" aria-label="Toggle theme">
  <i class="ph ph-moon" id="themeIcon"></i>
  <span id="themeLabel">Dark mode</span>
</button>
```

```javascript
function setTheme(dark) {
  document.body.classList.toggle("dark", dark);
  document.getElementById("themeLabel").textContent = dark ? "Light mode" : "Dark mode";
  document.getElementById("themeIcon").className = dark ? "ph ph-sun" : "ph ph-moon";
  renderAll(); // re-read CSS vars for Chart.js
}
```

Place in `.page-chrome` for analytics archetype.

---

## Collapsible drill-down sections (default closed)

**Rule:** Keep headline metrics and primary charts visible. Collapse long secondary content -- breakdown tables, example lists, heatmaps, explorer results, appendices -- **closed by default**. Aligns with v1 progressive disclosure; critical on multi-tab analytics dashboards.

### When to collapse

| Keep visible | Collapse (default closed) |
|--------------|---------------------------|
| Hero KPIs, section titles, primary chart | Intent / dimension breakdown tables |
| Card headline + share % + one-line desc | Per-category initiator tables + conversation examples |
| Filter controls + match count | Paginated / long result lists |
| Workflow tree / summary narrative | Methodology appendix, decision-rule reference blocks |

Do **not** nest collapse inside collapse more than one level deep.

### Markup

```html
<details class="card collapse-card">
  <summary class="collapse-summary">
    Intent breakdown table
    <span class="collapse-meta">12 intents</span>
  </summary>
  <div class="collapse-body">
    <!-- table, examples, heatmap, etc. -->
  </div>
</details>
```

Inside an open card (nested drill-down):

```html
<div class="card rc-block">
  <div class="rc-head">…headline always visible…</div>
  <p class="layer-desc">…</p>
  <details class="collapse-card collapse-nested">
    <summary class="collapse-summary">
      Drill-down: initiators &amp; examples
      <span class="collapse-meta">96 loops · 5 examples</span>
    </summary>
    <div class="collapse-body">…</div>
  </details>
</div>
```

Omit the `open` attribute unless the user explicitly asks for one section expanded by default.

### CSS

```css
details.collapse-card { margin-bottom: 20px; }
details.collapse-card > summary.collapse-summary {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--ink);
  padding: 2px 0;
  cursor: pointer;
  user-select: none;
}
details.collapse-card > summary.collapse-summary::-webkit-details-marker { display: none; }
details.collapse-card > summary.collapse-summary::before {
  content: "";
  display: inline-block;
  width: 0;
  height: 0;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 7px solid var(--accent);
  transition: transform 150ms ease;
  flex-shrink: 0;
}
details.collapse-card[open] > summary.collapse-summary::before {
  transform: rotate(90deg);
}
details.collapse-card > summary .collapse-meta {
  font-weight: 400;
  font-size: var(--text-xs);
  color: var(--ink-soft);
  margin-left: auto;
}
details.collapse-body {
  padding-top: 14px;
  margin-top: 4px;
  border-top: 1px solid var(--border);
}
details.collapse-nested {
  margin-top: 12px;
  margin-bottom: 0;
  box-shadow: none;
}
details.collapse-nested > summary.collapse-summary {
  font-size: var(--text-sm);
}
```

Respect `prefers-reduced-motion`: chevron rotation may use `transition: none`.

### JS helper

```javascript
function collapseSection(summaryHtml, bodyHtml, extraClass = "card collapse-card") {
  return `<details class="${extraClass}">
    <summary class="collapse-summary">${summaryHtml}</summary>
    <div class="collapse-body">${bodyHtml}</div>
  </details>`;
}
```

Update `.collapse-meta` when filters change (e.g. explorer: `${filtered.length} matching`).

### Accessibility

- Use semantic `<details>` / `<summary>` (keyboard + screen reader native).
- `summary` must describe what expands (`Drill-down: initiators & examples`, not `Click here`).
- Counts in `.collapse-meta` supplement the label; do not rely on color alone for state.

### Anti-patterns

- Entire tab body inside one collapse -- user loses scan path.
- Default-open long lists on analytics tabs -- page height explodes.
- Custom accordion JS when native `<details>` suffices.
- Hiding the only chart for a section inside a closed panel.

---

## On-page note vs hover info

**On the page (one short line under the chart):** a caveat that changes how to read the number (`n = 41`, `Chatbot is a guideline`). Skipping it would mislead.

**Hover / info-i / `*` / collapse:** definitions, grain, extra why, "what is SSA". Not a wall of body copy. Do not hide a load-bearing caveat only in the info-i.

```html
<p class="chart-note">n = 41 in this slice - treat ranks as directional.</p>
<button class="info-btn" type="button" aria-label="What is SSA"></button>
```

`.chart-note` is `--text-sm` / `--ink-soft`. At most one per chart.

---

## Linked charts + metric toggle

Clicking a bar filters the sibling chart that shares the grain (reason → comments, driver → examples). Highlight the selected bar. Provide a clear reset.

Two metrics with different baselines (TOR vs resolution) are a **pill toggle**, never one dual-axis.

```javascript
function onBarClick(key) {
  selectedKey = selectedKey === key ? null : key;
  renderSibling(selectedKey); // filter, do not remint series colors
}
```

Keep `SERIES_COLOR[pop]` stable across the toggle. See [color-valence.md](color-valence.md).

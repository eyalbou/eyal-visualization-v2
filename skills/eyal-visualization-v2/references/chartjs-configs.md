# Chart.js Configuration (v2)

Bar datalabels, combo, threshold colors, plus v2 defaults: `tension: 0.4`, `borderRadius: 12` on bars, grid `rgba(0,0,0,0.06)`, colors from `--accent`.

**Survey / conversion funnel:** do not use Chart.js. CSS column recipe: [funnel-graph.md](funnel-graph.md).

---

## Font + number setup (do this first)

Chart.js does **not** inherit font from CSS. Declare the stack once and reuse the constant in every axis, tooltip and datalabel config:

```javascript
const FONT_FAMILY = "'Axiforma', 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
Chart.defaults.font.family = FONT_FAMILY;
Chart.defaults.font.size = 14;
Chart.defaults.animation = false;
```

The string must match `--font` in CSS exactly. Never introduce a mono stack into a chart.

**Toggles:** Chart.js animation stays **off**. Population / theme / tab / filter must not tween bars. If the chart is kept alive, call `chart.update('none')`. Destroy + recreate is fine under `Chart.defaults.animation = false`. CSS page `rise` and canvas enter on first load are separate -- do not turn those off.

Axis ticks and bar end labels use the canonical `fmtNum` from [SKILL.md](../SKILL.md#number-formatting) -- all digits below 1K, trimmed `K` up to 1M, `M` at two decimals:

```javascript
ticks: { callback: (v) => fmtNum(v), font: { family: FONT_FAMILY, size: 14, weight: "600" } }
```

Tooltips are the drill-down surface, so they use `fmtInt` (exact grouped digits).

---

## Soft UI bar chart (analytics)

```javascript
datasets: [{
  borderRadius: 12,
  borderSkipped: false,
  backgroundColor: barColors(labels),
}],
options: {
  scales: {
    x: { grid: { display: false }, ticks: { font: { family: FONT_FAMILY, size: 12 } } },
    y: { grid: { color: isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.06)" }, beginAtZero: true },
  },
}
```

Re-render on `setTheme()` so `getComputedStyle` picks up dark tokens.

---

## Horizontal bar end labels (required for driver charts)

Load `chartjs-plugin-datalabels@2` and `Chart.register(ChartDataLabels)`.

```javascript
plugins: {
  datalabels: {
    anchor: 'end',
    align: 'end',
    clip: false,
    offset: 4,
    color: () => getComputedStyle(document.body).getPropertyValue('--ink').trim(),
    font: { family: FONT_FAMILY, size: 14, weight: '600' },
    display: (ctx) => {
      /* Hide collisions. Never shrink below 14px. */
      return true;
    },
    formatter: (value, ctx) => {
      const row = rows[ctx.dataIndex];
      return `${row.count} (${fmtPct(row.share_of_loops, 0)})`;
    },
  },
},
```

For intent loop charts: `${loops} (${fmtPct(loop_rate, 0)})`.

**Sort:** default highest volume / share on top. Optional **Volume** | **Survey order** toggle. Ties keep catalog order. Filter pills may stay in survey/form order.

**Exception -- ordered scales.** Severity (mild → frustrated → rage), TOR bands, and any ordinal heat sort **by rank**, left-to-right or top-to-bottom, not by volume. Volume stays in the labels. Legend matches the bar. See [color-valence.md](color-valence.md).

---

## Horizontal bar category labels (name + n)

Ranked, mix, and gap horizontal bars put **volume on the y-axis**, not only in the tooltip.

Pattern: `PREMIUM (1.4K)`

| Part | Color | Formatter |
|------|--------|-----------|
| Category name | `--ink` (must read on `--surface`) | truncated if long; full name in tooltip |
| `(` `)` | `--ink-soft` | |
| Count | the **subject volume color** -- Cara n is `--cara` ( `--cara-label` on `body.dark` ). Never the bar / winner / Chatbot fill | `fmtNum` (`117`, `1.4K`, `26.0K`, `1.25M`) |

Do **not** dump `Name (n)` as one Chart.js tick string. That paints name and count the same color. Do **not** paint the name in `--ink-soft` -- that fails contrast on white cards (`EMAIL_MARKETING` washes out). Draw with a plugin hooked on **`afterDatasetsDraw`** (HTML tooltip default) or **`beforeTooltipDraw`** (canvas tooltip only). Never `afterDraw` -- see [Chart hover](#chart-hover--tooltip-must-sit-on-top):

1. Mask the y-gutter with `--surface`.
2. Left-align the name at ~16px in `--ink`. Right-align `(`, `fmtNum(n)`, `)` at `chartArea.left - 10`. Truncate the name if it would collide with n.
3. Hide native ticks (`ticks.color = "transparent"`).
4. Reserve width with `y.afterFit` (~272px for product codes, ~312px for truncated intent titles).

n is the **subject population** (Cara sessions on a Cara-vs-Chatbot page). Paint it in the subject color. Share % and the comparison n stay in the tooltip. Tooltips still use `fmtInt` for the audit count.

Diverging / mix / gap bars: the **bar** encodes who won (teal vs indigo vs gray). The **n** does not. n is how many subject sessions sit on that row -- same Cara teal on every row. Do not recolor n to match the bar fill.

---

## Chart hover / tooltip (must sit on top)

Learned from Product gap (Chatbot ↔ Cara): the hover looked missing or "behind" the left labels, and TOR-mode hover looked like the wrong metric.

### 1. Z-order -- canvas tooltip is not the top layer

Chart.js paints its default tooltip **on the canvas**. Plugins that `afterDraw` (y-gutter `fillRect` masks, zero-lines, custom labels) run **after** the tooltip, so the hover is covered by the axis paint. HTML siblings (`position` / `z-index` / `overflow: hidden` on `.card` / `.chart-wrap`) can also clip or bury it.

**Required:** do not use the canvas tooltip next to overlay plugins.

- **Default:** HTML tooltip via `plugins.tooltip.external`, `enabled: false`. Append `#chart-tip` to `document.body` (`position: fixed; z-index: 9999; pointer-events: none`). Clamp to the viewport. Hide when `tooltip.opacity === 0`. Overlay plugins (gutter mask, name+n, zero line) hook **`afterDatasetsDraw`** so they still paint when the canvas tooltip is off.
- **If you must stay on canvas:** every overlay plugin hooks **`beforeTooltipDraw`**, never `afterDraw`. Crosshair that *reads* `tooltip.caretX` may still `afterDraw`.

```javascript
function ensureChartTip() {
  let el = document.getElementById("chart-tip");
  if (!el) {
    el = document.createElement("div");
    el.id = "chart-tip";
    document.body.appendChild(el);
  }
  return el;
}
function htmlChartTooltip(ctx) {
  const tip = ensureChartTip();
  const t = ctx.tooltip;
  if (!t || t.opacity === 0) { tip.classList.remove("open"); return; }
  const title = (t.title || []).join(" ");
  const lines = (t.body || []).flatMap((b) => b.lines || []);
  const after = t.afterBody || [];
  tip.innerHTML = (title ? "<strong>" + escHtml(title) + "</strong>" : "")
    + lines.concat(after).map((l) => "<div>" + escHtml(l) + "</div>").join("");
  tip.classList.add("open");
  const rect = ctx.chart.canvas.getBoundingClientRect();
  const tw = tip.offsetWidth, th = tip.offsetHeight;
  let left = rect.left + t.caretX - tw / 2;
  let top = rect.top + t.caretY - th - 12;
  left = Math.min(Math.max(8, left), window.innerWidth - tw - 8);
  if (top < 8) top = rect.top + t.caretY + 16;
  tip.style.left = left + "px";
  tip.style.top = top + "px";
}
```

```css
#chart-tip {
  display: none; position: fixed; z-index: 9999; pointer-events: none;
  padding: 12px 14px; background: var(--ink); color: #fff;
  border-radius: 12px; box-shadow: var(--shadow-md);
  font-family: var(--font); font-size: var(--text-sm); font-weight: 500;
  line-height: 1.45; max-width: 360px; white-space: nowrap;
}
#chart-tip.open { display: block; }
#chart-tip strong { display: block; margin-bottom: 6px; font-weight: 600; }
```

### 2. Metric toggle -- hover follows the pill

A TOR | Resolution | Score (or any metric) toggle is the **question**. The hover answers **that** question.

| Active pill | Hover body |
|-------------|------------|
| TOR | TOR rates + TOR gap, then n |
| Resolution | Res rates + Res gap, then n |
| Score / mixed | Score line, then **both** TOR and Res, each with **its own** gap, then n |

`label` returns a **string array** (one line per metric). Never one concatenated string (`TOR … · Res … · gap …`). Chart.js wraps mid-token; the active gap sits next to the other metric and the hover looks wrong even when the numbers are right.

```javascript
label: (c) => {
  const p = rows[c.dataIndex].p;
  const tor = `TOR  Cara ${fmtPct(p.cara_tor_pct)} vs Chatbot ${fmtPct(p.cb_tor_pct)}  (${fmtPp(p.tor_gap_pp)})`;
  const res = `Res  Cara ${fmtPct(p.cara_res_pct)} vs Chatbot ${fmtPct(p.cb_res_pct)}  (${p.res_gap_pp == null ? "-" : fmtPp(p.res_gap_pp)})`;
  const n = `Cara n ${fmtInt(p.cara_n)}  ·  Chatbot n ${fmtInt(p.cb_n)}`;
  if (metric === "tor") return [tor, n];
  if (metric === "res") return [res, n];
  return [`Score ${fmtScore(scoreCara(p))}  (0.7 TOR + 0.3 Res)`, tor, res, n];
}
```

Counts in tooltips use `fmtInt`. Rates `fmtPct`. Gaps `pp`. Null → `-`.

### 3. Fail if

- Overlay plugin uses `afterDraw` + `fillRect` and tooltip has no `external`
- `label` returns one template that joins two metrics with ` · `
- Metric-toggle chart whose hover ignores the active pill, or Score hover that omits one of the two metrics
- Hover title is `Name · Cara n …` when n is already a body line (duplicate)

---

## Smooth line chart (minimal axes)

```javascript
datasets: [{
  tension: 0.4,
  borderWidth: 2,
  pointRadius: 0,
  pointHoverRadius: 5,
  pointHoverBackgroundColor: accent,
  fill: false,
}],
plugins: {
  legend: { display: false },
  datalabels: { display: false },
},
interaction: { intersect: false, mode: "index" },
```

Tooltip: bold value, accent border -- fintech dashboard style.

---

## Sparklines (time series ONLY)

**Do not** use on histogram buckets or cross-section snap cards. Only when X axis is dates/hours.

```javascript
function createSparkline(canvas, series, accent) {
  return new Chart(canvas.getContext("2d"), {
    type: "line",
    data: {
      labels: series.map((_, i) => i),
      datasets: [{
        data: series,
        borderColor: accent,
        backgroundColor: accent + "22",
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { enabled: false }, datalabels: { display: false } },
      scales: { x: { display: false }, y: { display: false, beginAtZero: true } },
    },
  });
}
```

Container: `height: 36px` below metric value in widget cards.

---

## Dual-line chart + crosshair

For comparing two series (financial dashboard ref):

```javascript
options: {
  interaction: { mode: "index", intersect: false },
  plugins: {
    tooltip: {
      enabled: true,
      callbacks: {
        label: (ctx) => ctx.dataset.label + ": " + fmtInt(ctx.raw),
      },
    },
    crosshair: false, // use plugin or custom onHover vertical line
  },
}
```

Custom crosshair via `afterDraw` plugin:

```javascript
const crosshairPlugin = {
  id: "crosshair",
  afterDraw(chart) {
    const { ctx, chartArea, tooltip } = chart;
    if (!tooltip || tooltip.opacity === 0) return;
    const x = tooltip.caretX;
    ctx.save();
    ctx.strokeStyle = "rgba(0,0,0,0.15)";
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(x, chartArea.top);
    ctx.lineTo(x, chartArea.bottom);
    ctx.stroke();
    ctx.restore();
  },
};
Chart.register(crosshairPlugin);
```

---

## Heatmap grid (GitHub-style)

For density-over-time when cell count is manageable (< 53 weeks x 7 days). Accent ramp = volume / activity (no moral). Ordered negative heat (mild → rage, TOR bands) uses `--sev-lo` / `--sev-mid` / `--sev-hi` (add `--sev-ok` / `--sev-max` when the scale has a healthy or critical stop) instead -- see [color-valence.md](color-valence.md).

```html
<div class="heatmap" role="img" aria-label="Activity heatmap"></div>
```

```css
.heatmap {
  display: grid;
  grid-template-columns: repeat(53, 12px);
  gap: 3px;
}
.heatmap-cell {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  background: var(--canvas-deep);
}
.heatmap-cell[data-level="1"] { background: color-mix(in srgb, var(--accent) 25%, var(--canvas-deep)); }
.heatmap-cell[data-level="2"] { background: color-mix(in srgb, var(--accent) 50%, var(--canvas-deep)); }
.heatmap-cell[data-level="3"] { background: color-mix(in srgb, var(--accent) 75%, var(--canvas-deep)); }
.heatmap-cell[data-level="4"] { background: var(--accent); }
```

Populate levels from data in JS. Prefer table alongside for accessibility.

---

## Overflow

See [overflow-rules.md](overflow-rules.md) -- apply on every chart.

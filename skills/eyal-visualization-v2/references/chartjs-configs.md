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
```

The string must match `--font` in CSS exactly. Never introduce a mono stack into a chart.

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

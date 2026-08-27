# Text Overflow Prevention Rules (by chart type)

> **Principle**: No text in any chart or HTML element should ever be clipped, truncated invisibly, or overflow its container. Every chart type has specific overflow risks -- check each one.

## Vertical bar charts
- [ ] **Top datalabels clipped**: Every chart with `align: 'top'` MUST have `layout: { padding: { top: 20-25 } }`
- [ ] **X-axis labels overlapping**: If labels are long (>8 chars) or numerous (>12 bars), set `ticks: { maxRotation: 45 }` and add `layout: { padding: { bottom: 10 } }` to accommodate rotated text
- [ ] **X-axis labels cut at bottom**: If `maxRotation > 0`, ensure the chart container (`chart-container`) has enough height (min 300px) or the canvas is not cropped by CSS `overflow: hidden`
- [ ] **Dense bars with datalabels colliding**: If >15 bars, consider hiding datalabels (`display: false`) and relying on tooltips, or use `display: (ctx) => ctx.raw > threshold` to only show labels for significant values

## Horizontal bar charts
- [ ] **Right datalabels clipped**: Every chart with `anchor: 'end', align: 'end'` MUST have `layout: { padding: { right: 60-80 } }` -- the value depends on label length (percentages ~60px, counts with K format ~80px)
- [ ] **Y-axis labels truncated (long category names)**: Chart.js does NOT word-wrap axis labels. If categories exceed ~25 chars (e.g. `ui_triggered_action/suggest_section`), truncate the **name** only: `callback` / `shortLabel` to ~26-34 chars -- and show the full label in the tooltip. Do not truncate the `fmtNum` count.
- [ ] **Y-axis `Name (n)` two-tone**: Native ticks cannot split colors. Use an `afterDraw` plugin (see [chartjs-configs.md](chartjs-configs.md#horizontal-bar-category-labels-name--n)). Hide ticks (`color: "transparent"`). `afterFit` width ~236px (product codes) / ~300px (intent titles) so `PREMIUM (1.4K)` is not clipped on the left.
- [ ] **Y-axis labels cut at left**: If labels are long, add `layout: { padding: { left: 10 } }` or increase the chart container width

## Line / area charts
- [ ] **Peak data points clipped at top**: Add `layout: { padding: { top: 10-15 } }` OR set `y: { suggestedMax }` with ~5-10% headroom above the max value
- [ ] **X-axis date labels too dense**: Use `ticks: { autoSkip: true, maxTicksLimit: 10-15 }` to prevent overlapping date strings
- [ ] **Datalabels disabled**: Line/area charts should NOT use per-point datalabels (Phase 3.5 rule). If they do exist, ensure `layout: { padding: { top: 20 } }`

## Doughnut / pie charts
- [ ] **Legend clipped on right**: When `legend: { position: 'right' }`, add `layout: { padding: { right: 20 } }` to prevent legend text from being cut by the canvas edge
- [ ] **Legend labels too long**: Use legend `labels.generateLabels` callback or keep labels under ~30 chars. If a label includes a percentage (e.g. `"English (94.2%)"`), ensure the container is wide enough (~400px min) or move legend to `'bottom'`
- [ ] **Inner datalabels overflow small slices**: When a slice is <5% of total, its datalabel can overlap adjacent slices. Use conditional display: `display: (ctx) => { const pct = ctx.dataset.data[ctx.dataIndex] / ctx.dataset.data.reduce((a,b)=>a+b,0); return pct > 0.05; }` -- hide labels for tiny slices and let the tooltip handle them
- [ ] **Many-slice charts (6+ slices) with dominant value**: If one slice >80%, a doughnut becomes unreadable for other slices. Convert to horizontal bar chart instead (Phase 3.3 rule)

## Stacked bar charts
- [ ] **Segment datalabels inside thin segments**: Hide labels for segments too small to contain text: `display: (ctx) => ctx.raw > minThreshold` (HTML stacks: hide under ~8% width, use a tick callout on the worst end)
- [ ] **In-bar type too small**: On 56-72px HTML stacked bars, percentage is `--text-h3`, category is `--text-sm` / `--text-base`. Do not use `--text-xs` as the only in-bar size. Legend `--text-sm`.
- [ ] **Ordered scale vs volume**: mild → rage (or TOR bands) left-to-right by rank, not by n. See [color-valence.md](color-valence.md).
- [ ] **Legend with many items**: If >6 series, the legend can wrap or overflow. Set `legend: { labels: { boxWidth: 12, padding: 8, font: { size: 11 } } }` to keep it compact, or move `position: 'bottom'`
- [ ] **Top segment datalabels clipped**: Same as vertical bar -- add `layout: { padding: { top: 20 } }` if datalabels sit above the top-most segment

## Grouped bar charts
- [ ] **Datalabels collide between groups**: Keep ticks and datalabels at **14px / 600**. Hide the colliding label (`display: false` / `display: (ctx) => ...`) or show only the larger series. Never shrink to 11px. Funnel conversion chip stays the loudest number. Chart type from the SKILL chooser.
- [ ] **Legend overlapping chart area**: Ensure `layout: { padding: { top: 30 } }` when legend is at `'top'`, to separate legend from bars

## Dual-axis / combo charts (bar + line)
- [ ] **Right y-axis labels clipped**: Add `layout: { padding: { right: 40-60 } }` to give the secondary axis ticks room
- [ ] **Datalabels overlap between datasets**: Disable datalabels on the line dataset (`datalabels: { display: false }`) and only show them on bars, or vice versa. Never show both

## Word clouds
- [ ] **Words clipped at canvas edges**: Use `shrinkToFit: true` in WordCloud options and ensure the canvas is sized to its container via `requestAnimationFrame` dimension checks before rendering
- [ ] **Tooltip overflows viewport**: Word cloud custom tooltips should use CSS `max-width: 300px; word-wrap: break-word` and JS position clamping: `Math.min(x, window.innerWidth - tooltipWidth - 20)`

## HTML elements (non-chart)
- [ ] **Stat box numbers overflow**: Large numbers must use K/M format. CSS: `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` as fallback
- [ ] **Tab bar wrapping to multiple lines**: Use `flex-wrap: nowrap; overflow-x: auto` on the tab container. Tab buttons: `white-space: nowrap; flex-shrink: 0`
- [ ] **Info icon tooltips overflow viewport**: CSS `max-width: 320px; word-wrap: break-word`. Position with JS or CSS so tip never extends past `right: 0` or `bottom: 0` of the viewport
- [ ] **Insight box bullets overflow**: Use `word-wrap: break-word; overflow-wrap: break-word` on `<li>` elements
- [ ] **Sample table long text**: Cells with user messages should have `max-width: 500px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap` or use a scrollable container
- [ ] **Card titles with info icons overflow**: Ensure card `<h2>` has `overflow: hidden; text-overflow: ellipsis` or the card has enough width

## Verification checklist (run after all fixes)
- [ ] **Grep for `align: 'top'`** -- confirm every hit has `padding: { top:`
- [ ] **Grep for `align: 'end'`** on horizontal bars -- confirm every hit has `padding: { right:`
- [ ] **Grep for `position: 'right'`** on legends -- confirm the chart has `padding: { right:` or container is wide enough
- [ ] **Grep for `maxRotation`** -- if any axis rotates labels, confirm the container has enough height
- [ ] **Visually check each tab** at both full-width and ~900px to catch responsive overflow

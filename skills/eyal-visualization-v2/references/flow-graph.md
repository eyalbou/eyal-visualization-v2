# Flow graph (v2)

SVG tree flow (Sankey-style) for **where units go**: one whole splits into destinations, and some destinations split again. Hand-drawn SVG, **not Chart.js**, no plugin. Validated Oct 2026 on the jev-classify "Where rows go" view.

**Durable copies (do not depend on Stash):**

| File | Role |
|------|------|
| This recipe | When to use, anatomy, data shape, tokens, writing rules, review |
| [assets/flow-graph.html](../assets/flow-graph.html) | Self-contained graph: generic engine + worked example (copy from disk) |

Stash (`https://bo.wix.com/stash/jev-classify-graph-options/`, tab C) is a preview only.

---

## When to use

| Question | Chart |
|----------|-------|
| One population splits into 2+ destinations, then some split again (sets, routes, outcomes) | **This flow graph** |
| How many remain across 3-4 sequential stages (eligible → viewed → submitted) | CSS funnel ([funnel-graph.md](funnel-graph.md)). Not this graph |
| Share of one mix, no second split | Horizontal bar or doughnut (2-4 slices) |
| Units merge from several sources, loop back, or move between states over time | Not this graph -- table, stacked bar, or transition matrix |
| The same split over time | Line or stacked bar per period |

**Fit test -- all three must be yes:**

1. Every unit lands in exactly one node per column (a tree, no merges).
2. Each node's children add up to the node. A remainder gets its own `Other` node.
3. The reader's question is "where did they go", not "how many are left".

If only the first split matters (one parent, 2-4 children, no second level), a bar is simpler. The flow graph earns its space at **two levels of split or more**.

---

## Anatomy (do not invent a new layout)

```
.card
  .card-header-row
    left:  h2 (finding or "Where X go") + .card-sub (one line)
    right: .flow-legend  [Example split chip]  swatch + meaning, one per tone
  .flow-scroll                       overflow-x: auto
    .flow-host (min-width 900px)
      svg.flow-svg (viewBox 1240 x auto)
        column heads (uppercase, top row)
        g ribbons   -> parent slot to child node, child tone, 0.24 opacity
        g nodes     -> 14px bars, node tone
        g labels    -> "Label value" + note, right of each node
  ul.insight (max 3 bullets)
```

Columns run left → right in process order. Column 0 is the whole (one root). Each later column holds the children of the column before it.

---

## Data shape

```javascript
const FLOW = {
  generated_at: "2026-10-08T08:00:00Z",
  title: "Where rows go",
  subtitle: "Which rows prove quality, and which ones get labeled.",
  example: true,                     // true = numbers are illustrative -> shows the chip
  columns: ["All rows", "Disjoint sets", "Scale routing", "Fallback result"],
  legend: [{ tone: "teal", label: "Proof rows" }],
  nodes: [
    { key: "all", col: 0, label: "All rows", tone: "neutral" },   // root: value = sum of children
    { key: "scale", col: 1, parent: "all", label: "Scale", note: "Scored by Jev after your yes", value: 10000, tone: "accent" },
    { key: "keep", col: 2, parent: "scale", label: "Jev keeps its label", shareNote: "coverage at the threshold", value: 7800, tone: "accent" },
  ],
};
```

| Field | Rule |
|-------|------|
| `col` | Child is always `parent.col + 1` |
| `value` | Raw count. Root may omit it -- the engine sums the children |
| `note` | Static line under the label, **≤8 words** |
| `shareNote` | Engine prefixes `fmtPct(share of parent)`: `78.0% coverage at the threshold`. Use it instead of hand-typing a percent |
| `tone` | One of the tones below. Picked by **meaning**, not position |
| Node order | Array order = top-to-bottom order inside the column |

The engine (`buildFlow`) warns in the console when: more or fewer than one root; a child is not one column right of its parent; children do not sum to the parent (±0.5); more than 4 columns or 6 nodes in a column; a label over 4 words or a note over 8. **Zero warnings before delivery.**

---

## Layout tokens (locked)

| Token | Value | Why |
|-------|-------|-----|
| viewBox width | `1240` | Scales to the card; fonts stay legible at 1100-1440 |
| `top` | `44` | Room for the column heads |
| `nodeW` | `14` | Reads as a node, not a bar chart |
| `gap` | `34` | Two-line labels (title + note) never collide |
| `minH` | `4` | A 5-row set stays visible next to 10K; the label keeps the exact value |
| `heightBudget` | `496` | Scale unit = (budget - gaps) / largest column total |
| `lastColRoom` | `280` | Label room right of the last column |
| Height | Auto: tallest node or label + 28 | Never a fixed height -- a fixed height clips the last split |
| `.flow-host` min-width | `900px` inside `.flow-scroll` | Phone scrolls the graph, never the page |
| Ribbon opacity | `0.24`, hover `0.45` (100ms) | Ribbons recede; nodes and labels carry the read |
| Column head | 12px / 700 / uppercase / `--ink-soft` | |
| Label | 14px / 600, value tspan 700 | Same 14/600 floor as chart labels. Never shrink to fit |
| Note | 12px / 500 / `--ink-soft` | |

Column x positions are spaced evenly by the engine. Children start level with their slot in the parent, then stack down with `gap`, so the main branch stays straight.

---

## Tones (color by meaning)

| Tone | Token | Use for |
|------|-------|---------|
| `neutral` | `--flow-neutral` | The whole (root), plumbing sets with no story (smoke, holdout) |
| `accent` | `--accent` | The primary path the reader cares about |
| `accent-2` | `--accent-2` | A second actor or source (another model, another team) |
| `teal` | `--flow-teal` | Proof / control / validation sets |
| `violet` | `--flow-violet` | A fallback or secondary handler |
| `good` | `--success` | A good outcome when up is better (resolved, approved) |
| `warning` | `--warning` | A leftover that is bad when it grows (unresolved, dropped) |
| `danger` | `--danger` | A severe bad outcome only (failed, lost) |

Rules:

- **Same meaning, same tone.** Work and validation are both proof → both teal. Scale and "Jev keeps" are both the Jev path → both accent.
- **Ribbon takes the child's tone.** The destination is the story, so the band entering a node is that node's color.
- **Valence wins over accent.** A bad leftover is `warning` / `danger`, never blue, even if it sits on the primary path. [color-valence.md](color-valence.md).
- At most **5 tones + neutral** on one graph. More means the graph has more than one story -- split it.
- Legend lists tones by meaning (`Proof rows`), not by node name.

---

## Writing guidelines (how to make it read best)

1. **Title is the finding** when the numbers are real (`78% of scale rows keep Jev's label`). Use `Where X go` only for a teaching or example view.
2. **Put the node that splits again last in its column.** Its children can then sit level with it and the ribbons never cross. Terminal nodes go above it.
3. **Put the bad leftover last** in its column (`Unresolved` under `2 of 3 agree`). The eye ends on the problem.
4. **Label = name + value.** Name ≤4 words in stakeholder English (`Fallback vote`, not `vote.py --ids-file`). Value via `fmtNum`.
5. **Note says why the node exists or its share.** Purpose for sets (`Accuracy and threshold, never tuned on`), share for outcomes (`shareNote`). ≤8 words. No method, no tool names.
6. **Column heads name the step**, not the data type (`Scale routing`, not `Rows`).
7. **Do not hide tiny nodes.** `minH` keeps them on screen; do not inflate their value or drop them. If a node is plumbing nobody acts on, it may be cut -- then its parent's total must still add up via `Other`.
8. **Illustrative numbers carry the chip.** `example: true` shows `Example split` in the legend, and one insight bullet says which numbers are examples. A delivered analysis never ships invented splits without it.
9. **Hover is the exact layer.** Each ribbon `<title>` is `Label: fmtInt(value) (fmtPct(share) of Parent)`. Exact counts and shares live there, not in more on-screen text.
10. **Max 3 insight bullets** under the card (≤18 words, outcome not method). Do not retell the bands (`Scale is the biggest`).
11. **Domain terms get a hover** like anywhere else -- an info icon in `.card-sub` or a Methodology row.

---

## State and motion

- Draw with `renderFlow(FLOW, host)`. It replaces the SVG; no tween, no Chart.js.
- **Theme toggle does not redraw.** Tones are CSS classes on `var(--flow-*)`, so `body.dark` recolors in place.
- **Resize does not redraw.** The viewBox scales.
- Hidden tabs are fine: the layout is computed from data, not from DOM measurement.
- Population toggle: swap `FLOW` and call `renderFlow` once. The setter returns early when the population is already current ([No motion on no-ops](../SKILL.md#no-motion-on-no-ops)).
- Card `rise` ~300ms on first load; ribbon hover 100ms; `prefers-reduced-motion` turns both off.

---

## Review checklist

- [ ] Fit test passes (tree, sums add up, "where did they go")
- [ ] Console shows **zero** `[flow]` warnings
- [ ] Labels ≤4 words, notes ≤8 words, all counts via `fmtNum`, shares via `fmtPct`, hover via `fmtInt`
- [ ] Same meaning → same tone; bad leftover is `warning` / `danger`; ≤5 tones + neutral
- [ ] Splitting node and bad leftover are last in their columns; no crossing ribbons
- [ ] Height is auto -- the last split and its labels are fully visible
- [ ] `.flow-scroll` wraps the host; page `scrollWidth` equals viewport at 390px
- [ ] Illustrative numbers → `example: true` chip + one bullet saying so
- [ ] Light and dark both read; no redraw on theme toggle

---

## Anti-patterns (never)

- A flow graph for a 3-stage survey drop (use the CSS funnel)
- Merges, loops, or a unit counted in two nodes of one column
- Children that do not add up to the parent, with no `Other` node
- One tone per node (rainbow), or a bad leftover in trust-blue
- Fixed SVG height that clips the last column
- Labels shrunk below 14px to fit, or notes carrying tool, table, or script names
- Inflating a tiny node's value to make it visible (`minH` exists for that)
- Invented split shown without the `Example split` chip
- Chart.js / d3-sankey plugin for this (the asset engine is the implementation)
- Redrawing on theme toggle or replaying `rise` on a same-population click

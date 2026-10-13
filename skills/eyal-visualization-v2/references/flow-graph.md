# Flow graph (v2)

SVG tree flow (Sankey-style) for **where units go**: one whole splits into destinations, and some destinations split again. Hand-drawn SVG, **not Chart.js**, no plugin. Validated Oct 2026 on the jev-classify "Where rows go" view. Focus mode and rate labels approved Oct 2026 on the agent-first-turn SR dashboard.

**Two defaults ship with the engine:** [focus mode](#focus-mode-default) (click any stage to see only the units through it, at any depth) and [rate labels](#labels-rates-by-default) (labels are shares, counts live in hover).

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
    left:  h2 (finding or "Where X go") + .card-sub (one line + info-i: label base)
    right: .flow-legend  [Example split chip]  swatch + meaning, one per tone
  .flow-focus (hidden unless focused)  "Showing A > B. Esc goes back a step ..." + Back + Show all
  .flow-scroll                       overflow-x: auto
    .flow-host (min-width 900px)
      svg.flow-svg (viewBox 1240 x auto, user-select: none)
        column heads (uppercase, top row)
        g ribbons   -> parent slot to child node, child tone, 0.24 opacity
        g nodes     -> one g.flow-node-g per node, ABOVE ribbons:
                       [focusable nodes: .flow-hit rects] 14px bar + "Label rate" + note
  .flow-status (aria-live)           click hint / focus path / pinned node
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
  unit: "rows",                      // plural noun for the status line ("10,000 rows")
  // base: "parent",                 // opt-in: label = share of parent (default: share of the whole)
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
| `shareNote` | Engine prefixes `fmtPct(share of parent)`: `78.0% coverage at the threshold`. Use it instead of hand-typing a percent. The prefix is dropped when the label already shows the share of that parent (focused on it, or level 1 of the root) |
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
4. **Label = name + rate.** Name ≤4 words in stakeholder English (`Fallback vote`, not `vote.py --ids-file`). Rate via `fmtPct` ([Labels: rates by default](#labels-rates-by-default)); the root keeps its total via `fmtNum`.
5. **Note says why the node exists or its share.** Purpose for sets (`Accuracy and threshold, never tuned on`), share for outcomes (`shareNote`). ≤8 words. No method, no tool names.
6. **Column heads name the step**, not the data type (`Scale routing`, not `Rows`).
7. **Do not hide tiny nodes.** `minH` keeps them on screen; do not inflate their value or drop them. If a node is plumbing nobody acts on, it may be cut -- then its parent's total must still add up via `Other`.
8. **Illustrative numbers carry the chip.** `example: true` shows `Example split` in the legend, and one insight bullet says which numbers are examples. A delivered analysis never ships invented splits without it.
9. **Hover is the exact layer.** Each node and ribbon `<title>` is `Label: fmtInt(value) (fmtPct(rate) of Base, fmtPct(share) of Parent)`. Exact counts and shares live there, not in more on-screen text.
10. **Max 3 insight bullets** under the card (≤18 words, outcome not method). Do not retell the bands (`Scale is the biggest`).
11. **Domain terms get a hover** like anywhere else -- an info icon in `.card-sub` or a Methodology row.

---

## Labels: rates by default

The reader asks "what share went where". A wall of raw totals makes them do the division.

| Node | On-screen value | Base |
|------|-----------------|------|
| Root, unfocused | Total via `fmtNum` (the one count that stays visible: the size of 100%) | -- |
| Any other node, unfocused | `fmtPct` | Share of the root (level 2 `Jev keeps 62.9%` = of all rows) |
| Root, focused | `fmtPct` of the whole, note `in <Node>` | Focused node's share of the root |
| Any other node, focused | `fmtPct` | Share of the focused node (ancestors read 100%, the next stage sums to 100%) |

- `base: "parent"` switches every label to share of its parent. Use it only when "of the parent" is the question for every column.
- A non-zero share under 0.1% renders `<0.1%`, never `0.0%` (`fmtRate`).
- Counts go in hover via `fmtInt`, on both the node and the ribbon `<title>`. If a count must stay visible, use `fmtNum`.
- **Name the base in the info hover** next to `.card-sub`: `Labels show the share of all rows. Hover a node or band for counts.` Update it when focused (`share of Scale; the first column shows its share of all rows`).

---

## Focus mode (default)

Focus works at **every level**. Click any non-root node that has children (its bar, its label, or the band into it) and the graph shows only the units that pass through it. The root and every ancestor re-sum to that node, so it fills the full height and the stage after it reads as a full-size distribution: focus a level-2 node and level 3 is 100% of it. Clicks drill down a **focus path**: focus `Scale`, then click `Fallback vote`, and the view narrows to `Scale > Fallback vote`. Clicking an ancestor on the path steps back up to it. Leaves have nothing to expand: their click pins.

| Rule | Behavior |
|------|----------|
| Labels | Shares of the focused node; ancestors read 100%; root shows the focused node's share of the whole |
| Hover on an ancestor | `Scale: 2,200 in focus, of 10,000`, so the reader never mistakes the re-summed bar for the full node |
| Title / chip / status | Prefixed with the path `Scale > Fallback vote: `; chip `Showing Scale > Fallback vote. Esc goes back a step, double-click shows all.`; status `Showing Scale > Fallback vote: 2,200 rows. Click a later stage to narrow further.` |
| Back a step | Esc, or the `Back` button in `.flow-focus` (shown only when the path is 2+ deep). From level 1 it shows all |
| Show all | Double-click anywhere on the chart, or the `Show all` button. Clears the whole path |
| Esc order | First Esc clears a pin, then each Esc goes up one level |
| While focused | Click a later focusable node narrows; click a leaf pins its path (ancestors + descendants); click empty chart clears the pin |
| No-op | Re-clicking the focused node returns early: no redraw ([No motion on no-ops](../SKILL.md#no-motion-on-no-ops)) |
| Data swap | Focus and pin survive a filter / population swap while their keys still exist and stay focusable |
| Keyboard | Every node is `tabindex=0 role=button`; Enter / Space acts like click; keyboard focus returns to the node you left on Back / restore |
| Columns | x positions come from the full flow, so focusing never slides columns sideways |
| Other controls | A control that has no meaning while focused is `disabled` with a `title`, not hidden |
| Opt out | `renderFlow(FLOW, host, { focus: false })` -- clicks pin instead |

**Hit-testing (the part that breaks):**

- Node groups are drawn **after** ribbons, so a node or label is never under a band.
- Every focusable node (and the focused one) gets two invisible `.flow-hit` rects (`fill: transparent; pointer-events: all`): the bar plus 4px each side, and the label block sized from `getComputedTextLength()` after insert. A 4px node stays clickable and a band under the label never eats the click. Do not use one big rect across the label width: it covers the band and blocks pins.
- `click` ignores `ev.detail > 1`, and `dblclick` ignores anything within 500ms of focusing, so a double-click on a node focuses once and does not flicker back.
- `svg.flow-svg { user-select: none }` so a double-click never selects text.

```javascript
// State per host; the engine owns it. S.focus is the deepest node on the focus path.
const S = { focus: null, pin: null, focusAt: 0 };

// buildFlow marks every non-root node with children: n.focusable = !!n.parent && n.children.length > 0.

// Focused copy: ancestor chain + the node's subtree. Ancestors (and the root) drop their value,
// so buildFlow re-sums them to the focused node and it gets the full height.
function focusFlow(flow, full, key) {
  const keep = new Set(), chain = new Set();
  const walk = (n) => { keep.add(n.key); n.children.forEach(walk); };
  walk(full.byKey[key]);
  for (let p = full.byKey[full.byKey[key].parent]; p; p = full.byKey[p.parent]) chain.add(p.key);
  return { ...flow, nodes: flow.nodes.filter((n) => keep.has(n.key) || chain.has(n.key))
    .map((n) => (chain.has(n.key) ? { ...n, value: undefined } : n)) };
}

function setFocus(host, key, fromKey) {
  if (S.focus === key) return;                       // no-op: no redraw
  const prev = S.focus;
  S.focus = key; S.pin = null; S.focusAt = performance.now();
  renderFlow(S.flow, host);
  if (fromKey) host.querySelector(`.flow-node-g[data-key="${CSS.escape(key || prev)}"]`)?.focus();
}
function focusBack(host, fromKey) {                  // one level up; from level 1, show all
  if (!S.focus) return;
  const up = full.byKey[full.byKey[S.focus].parent];
  setFocus(host, up && up.focusable ? up.key : null, fromKey);
}

svg.addEventListener("click", (ev) => {
  if (ev.detail > 1) return;
  const key = ev.target.closest("[data-key]")?.getAttribute("data-key");
  if (!key) return S.pin && setPin(host, null);
  if (key === S.focus) return;
  if (full.byKey[key].focusable) return setFocus(host, key, false);
  setPin(host, S.pin === key ? null : key);
});
svg.addEventListener("dblclick", (ev) => {
  if (!S.focus || performance.now() - S.focusAt < 500) return;
  ev.preventDefault();
  setFocus(host, null, false);
});
document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  if (S.pin) setPin(host, null);
  else if (S.focus) focusBack(host, host.contains(document.activeElement));
});
backBtn.addEventListener("click", (ev) => focusBack(host, ev.detail === 0));
showAllBtn.addEventListener("click", (ev) => setFocus(host, null, ev.detail === 0));
```

The asset wires title, chip, Back, status, and info text through `renderFlow(FLOW, host, { onChange })`, which fires after every draw and pin change with `{ focus, path, pin, base, enabled }` (`path` = level-1 down to the focused node).

### Same rule on a layered path chart

When nodes are shared across paths (every unit passes one node per layer, and paths merge, as in a d3-sankey of chat stages), the tree copy above does not apply, but the behavior is the same. Keep the focus path as a list of `{ layer, key, label }` conditions, at most one per layer:

- Click a node: replace the condition on its layer with that node.
- Click a band: add both of its endpoints (and its color dimension, such as the turn, when the band carries one), so the view is exactly that band.
- Filter the source rows to those matching **every** condition, then re-aggregate and re-layout, so each layer below the deepest condition splits 100% of it.
- Labels are shares of the filtered total; the root shows its share of the unfiltered whole.
- Esc pops the last condition, double-click / `Show all` clears all. Approved Oct 2026 on the agent-first-turn SR dashboard.

---

## State and motion

- Draw with `renderFlow(FLOW, host, { focus: true, onChange })`. It replaces the SVG; no tween, no Chart.js. Focus and pin redraw the same way.
- **Theme toggle does not redraw.** Tones are CSS classes on `var(--flow-*)`, so `body.dark` recolors in place.
- **Resize does not redraw.** The viewBox scales.
- Hidden tabs are fine: the layout is computed from data, not from DOM measurement.
- Population toggle: swap `FLOW` and call `renderFlow` once. The setter returns early when the population is already current ([No motion on no-ops](../SKILL.md#no-motion-on-no-ops)).
- Card `rise` ~300ms on first load; ribbon hover and pin dim 100ms; `prefers-reduced-motion` turns them off. Focus and restore are an instant redraw, never a tween.

---

## Review checklist

- [ ] Fit test passes (tree, sums add up, "where did they go")
- [ ] Console shows **zero** `[flow]` warnings
- [ ] Labels ≤4 words, notes ≤8 words; label values are shares via `fmtPct` (root total via `fmtNum`), counts in hover via `fmtInt`
- [ ] Info hover names the label base, and changes when focused
- [ ] Real click on a node at level 1 **and** at level 2+ (bar, label, and its band) each focuses; the focused node fills the full height and the next stage sums to 100%
- [ ] A second click on a later stage narrows the path; title and chip show `A > B`; `Back` appears at depth 2+
- [ ] Esc and `Back` each go up one level; double-click and `Show all` clear the path; Esc clears a pin first; a double-click on a node does not flicker back
- [ ] Re-clicking the focused node does not redraw; no text selected on double-click
- [ ] Enter on a node focuses; keyboard focus returns to the node you left on Back / restore
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
- A flow graph without focus mode, focus limited to the first level, or focus that keeps the other branches at their old size
- Flow labels as raw totals (`Scale 10.0K`) with the share only in hover
- Nodes drawn under ribbons, or a branch hit area that a band can swallow

# v2 Component Recipes

Typography tokens: [soft-ui-tokens.md](soft-ui-tokens.md) type scale.

## Hero KPI (3-up grid, third column wider)

```css
.kpi-grid { grid-template-columns: 1fr 1fr 1.35fr; gap: 16px; }

.kpi { position: relative; overflow: hidden; }
.kpi::after {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--border);
}
.kpi.hero::after {
  height: 4px;
  background: var(--accent);
}
.kpi.hero {
  background: linear-gradient(135deg, var(--accent-glow) 0%, transparent 58%), var(--surface);
}
.kpi.hero .kpi-value {
  font-size: var(--text-kpi-hero);
  color: var(--accent);
}
.kpi.hero.is-bad::after { background: var(--danger); }
.kpi.hero.is-bad {
  background: linear-gradient(135deg, var(--danger-soft) 0%, transparent 58%), var(--surface);
}
.kpi.hero.is-bad .kpi-value { color: var(--danger); }
```

Top line and value color **must** use the same token. That token is `--accent` only when the hero is good-when-up or magnitude-only (analysed n, CSAT). **TOR / DSAT / dissatisfaction / rage share start as `.kpi.hero.is-bad`** -- do not copy `.kpi.hero` accent chrome and forget the class. Optional: `DATA` rows carry `direction: "worse" | "better" | "magnitude"` and `renderAll()` maps that onto `.is-bad`. Wash uses the matching `*-soft` at 8-12% opacity. Full rules: [color-valence.md](color-valence.md).

## Severity fills (heat / TOR / mild → rage)

Use tokens, never one-off hex. Color in-bar type with the matching `--sev-*-ink`.

```css
.heat-ok  { background: var(--sev-ok);  color: var(--sev-ok-ink); }
.heat-lo  { background: var(--sev-lo);  color: var(--sev-lo-ink); }
.heat-mid { background: var(--sev-mid); color: var(--sev-mid-ink); }
.heat-hi  { background: var(--sev-hi);  color: var(--sev-hi-ink); }
.heat-max { background: var(--sev-max); color: var(--sev-max-ink); }
```

3-stop default: lo → mid → hi. Add `.heat-ok` only when the scale has a healthy band; `.heat-max` when it has critical. White on yellow/orange/green fails. See [color-valence.md](color-valence.md).

## Active Snap Card

```css
.snap-card { position: relative; overflow: hidden; }
.snap-card::after {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: transparent;
}
.snap-card.active-pop {
  background: linear-gradient(135deg, var(--accent-glow) 0%, transparent 55%), var(--surface);
}
.snap-card.active-pop::after {
  background: var(--accent);
}
```

Do **not** use `box-shadow: 0 0 0 2px var(--accent)` ring -- use top bar + wash instead.

## KPI grid: prevalence + top drivers (RCA)

Four equal columns when showing **1 prevalence + 3 top root causes**:

```css
.kpi-grid { grid-template-columns: repeat(4, 1fr); gap: 14px; }
.kpi.hero .val { font-size: var(--text-kpi-hero); color: var(--accent); }
/* .kpi.hero.is-bad .val { color: var(--danger); } when prevalence is bad-when-up */
```

Each non-hero card: driver label (truncated), `fmtPct(share)`, subtitle `{count} loops`.

## Elaboration panel (info icon hover)

For methodology, Wilson CI, multi-label notes, driver definitions:

```html
<span style="position:relative;display:inline-flex">
  <button type="button" class="info-btn" aria-label="More info">i</button>
  <div class="elab-panel">…HTML explanation…</div>
</span>
```

```css
.info-btn { width:22px;height:22px;border-radius:50%;background:var(--canvas);cursor:pointer; }
.elab-panel { display:none; position:absolute; z-index:20; top:100%; padding:14px;
  background:var(--surface); border:1px solid var(--border); border-radius:12px;
  box-shadow:var(--shadow-md); font-size:var(--text-xs); min-width:220px; }
.elab-panel.open { display:block; }
```

Toggle `.open` on click; close on outside click. Use on KPI labels and section headers -- not for data that belongs in the main narrative.

## Driver deep-dive block (RCA)

Per top driver: headline + share, initiators table, 5 `example-conv` rows with Chatbot links + reasoning snippet.

---

## Trend Chip (cross-population, not time series)

```html
<span class="trend-chip up">
  <i class="ph ph-trend-up"></i>
  +7.44pp vs Priority + Studio
</span>
```

```css
.trend-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: 600;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
}
.trend-chip.up { color: var(--success); background: var(--success-soft); }
.trend-chip.neutral { color: var(--ink-soft); background: var(--canvas-deep); }
.trend-chip.better { color: var(--success); background: var(--success-soft); }
.trend-chip.worse { color: var(--danger); background: var(--danger-soft); }
```

Chip color follows **valence**, not geometry. TOR / DSAT / dissatisfaction **up** is `.worse`, not `.up` in green. Prefer `.better` / `.worse`. See [color-valence.md](color-valence.md).

## Anti-pattern: histogram sparklines on snap cards

Histogram bucket percentages are **not** a time series. Mini area charts at the bottom of population cards imply temporal change and mislead. Remove them. Reserve sparklines for dated metrics only.

## Survey funnel (CSS columns)

3-stage conversion (eligible → view → submit): not Chart.js. Conversion chip is the hero number. Population pills + `% from` sit on the **right** of the card header. Nearly-solid bars (4-8% sheen). **Rule:** one hue family per population, 400 / 500 / 600, 4-8% sheen, no neon orange. Cara All / sky / violet / apricot in [funnel-graph.md](funnel-graph.md) is a **worked example**, not a global palette. Do not paint Chatbot apricot onto an unrelated dashboard.

Full layout, tokens, copy, CSS, and JS: [funnel-graph.md](funnel-graph.md). Self-contained graph: [assets/funnel-graph.html](../assets/funnel-graph.html).

---

## Action-item cards

Required on Overview **after** the stake chart when there is a recommended move. Not for app-shell. Skip if there is no move. Show the strip **once**.

**Title:** verb-first action (`Stop repeating a failed step`). Not a theme (`UI grounding`).

**Reason:** why the research points here. 1-2 numbers via `fmtNum` / `fmtInt` / `fmtPct`. Not SQL.

Layout: horizontal ranked strip, swipe + arrow buttons, `scroll-snap`. Rank `01`. Title `--text-h3`, reason `--text-sm` / `--ink-soft`. Optional Phosphor icon, owner / effort chips, one highlighted stat. **Pointer-follow glow default ON.** Off under `prefers-reduced-motion`. Static only if the user kills glow. 3-7 cards. Sort = recommended build order.

```javascript
actions: [
  { rank: 1, title: "Stop repeating a failed step", n: 193, agree: 0.92,
    reason: (a) => fmtInt(a.n) + " sessions, " + fmtPct(a.agree * 100, 0) + " agreement - cheapest P0." }
]
```

```css
.action-strip {
  display: flex; gap: 16px; overflow-x: auto;
  scroll-snap-type: x mandatory; scrollbar-width: none;
  padding: 8px 4px 20px;
}
.action-card {
  --glow-x: 50%; --glow-y: 50%;
  flex: 0 0 min(360px, 82vw); min-height: 280px;
  scroll-snap-align: start;
  position: relative; display: flex; flex-direction: column; gap: 12px;
  padding: 20px; border-radius: 16px;
  background: var(--surface);
  box-shadow: var(--shadow-md);
}
.action-card::after {
  content: ""; pointer-events: none; position: absolute; inset: -2px;
  border-radius: inherit; border: 2px solid transparent;
  background: radial-gradient(180px 180px at var(--glow-x) var(--glow-y),
    color-mix(in srgb, var(--accent) 55%, transparent), transparent 70%) border-box;
  mask: linear-gradient(#000 0 0) padding-box, linear-gradient(#000 0 0);
  mask-composite: exclude;
}
.action-rank {
  width: 36px; height: 36px; border-radius: 50%;
  display: grid; place-items: center;
  font-weight: 700; font-size: var(--text-sm);
  background: var(--accent-glow); color: var(--accent);
}
.action-card h3 { margin: 0; font-size: var(--text-h3); letter-spacing: -0.03em; }
.action-reason { margin: 0; font-size: var(--text-sm); color: var(--ink-soft); line-height: 1.55; flex: 1; }
@media (prefers-reduced-motion: reduce) {
  .action-card::after { display: none; }
}
```

```javascript
strip.querySelectorAll(".action-card").forEach((card) => {
  card.addEventListener("pointermove", (e) => {
    const r = card.getBoundingClientRect();
    card.style.setProperty("--glow-x", (e.clientX - r.left) + "px");
    card.style.setProperty("--glow-y", (e.clientY - r.top) + "px");
  });
});
```

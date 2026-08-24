# Survey funnel graph (v2)

CSS column funnel for 3 (or 4) sequential stages. **Not Chart.js.** Conversion between stages is the hero number. Validated Aug 2026 on Cara Satisfaction Volume tab.

**Durable copies (do not depend on Stash):**

| File | Role |
|------|------|
| This recipe | Layout, copy, tokens, color families, JS skeleton |
| [assets/funnel-graph.html](../assets/funnel-graph.html) | Self-contained graph with dummy bake numbers + 4 color families |
| `investigations/cara-dissatisfaction/dashboard/cara-survey-channel-v2.html` | Live product (optional; may move) |

Stash (`https://bo.wix.com/stash/cara-satisfaction/`) is a preview only. If it is deleted, copy from this file + the example.

---

## When to use

| Question | Chart |
|----------|--------|
| Eligible → viewed → submitted (or any 3-stage drop) | This CSS funnel |
| Share of a mix (sat scores, reasons) | Stacked bar / doughnut |
| Distribution of a continuous metric | Vertical bar |

Never use Chart.js bars, a Sankey, or a full-width stretched funnel for this story. The read is **how many remain**, with **% conversion** between columns.

---

## Anatomy (do not invent a new layout)

```
.card
  .card-header-row
    left:  h2 "Survey funnel" + .card-sub (stage sentence + eligible definition)
    right: .card-header-actions
             pop-toggle (population / channel)
             .funnel-basis  |  "% from:" + pop-toggle (step vs first)
  #funnelHost
    .funnel[data-funnel-scale="{popKey}"]
      .funnel-col     .funnel-arrow     .funnel-col     .funnel-arrow     .funnel-col
        count           icon              count           icon              count
        bar track       .funnel-conv      bar track       .funnel-conv      bar track
        stage label                       stage label                       stage label
    .funnel-foot
      Overall conversion | Total drop-off | Biggest drop
```

Header: title stays left. Channel pills and `% from` sit on the **right**. `% from` has a left hairline so it does not merge into the channel track.

---

## Layout tokens (locked)

These numbers keep bar **bottoms level** even when a stage label wraps to two lines. Changing the track height without changing the matching grid row breaks alignment.

| Token | Value | Why |
|-------|--------|-----|
| Column width | `flex: 0 0 128px` | Bars stay a cluster in the center, not stretched across the card |
| Bar width | `100px` | Reads as a column, not a slab |
| Track / grid row 2 | `220px` (`maxH` in JS must match) | Shared row so arrow chips sit mid-bar, not mid-label |
| Count row | `32px` | Counts sit on one baseline above every bar |
| Arrow column | `72px` | Room for the conversion chip without crowding bars |
| Gap | `8px` | Tight cluster |
| Bar radius | `16px` | Softer than Chart.js `12px` bars |
| Min bar height | `12px` | Zero-ish stages still visible |
| Conversion chip | `--text-h2` / 700 / `8px 12px` pill | **Most important number on the chart** |
| Stage count | `--text-h2` / 700 / `--ink` | Second; `fmtNum` |
| Stage label | `--text-sm` / 500 / `--ink-soft` / center | Wraps inside 128px |
| Foot metrics | 3 equal columns, top border | Overall %, drop count, biggest drop name |

Grid on **both** `.funnel-col` and `.funnel-arrow`:

```css
grid-template-rows: 32px 220px auto;
justify-items: center;
```

Arrow icon + chip live in `.funnel-arrow-body` on **row 2** (`align-self: center`). Do not put the chip in the label row.

Mobile (`max-width: 640px`): wrap arrows to a full-width row; drop track to `160px` and set the same on `grid-template-rows`.

---

## Copy

| Surface | Pattern | Ban |
|---------|---------|-----|
| Card title | `Survey funnel` | Product slogan, event IDs |
| Card sub | Stages in speech (`Eligible to viewed modal to submitted`) plus **who is eligible per population** | Funnel arrows in the page hero subtitle; SQL |
| Stage 1 label | Population-specific (`Engaged sessions` vs `Contact flow conversations`) | Same label when the denominator is different |
| Stage 2 / 3 | `Viewed modal` / `Submitted` (or the real stage names) | Internal action names (`4:1148`) |
| `% from:` | Pill pair: `previous step` vs `first stage` | Raw `step` / `base` keys in the UI |
| Conversion chip | `fmtPct(rate, 1)` only | Count on the chip; the count is on the column |
| Foot: biggest drop | `{label} · {fmtNum(n)}` | Two competing "biggest" stories |
| Ranges | `Aug 6 - Aug 18` | Em dash, en dash, `--` |

Counts: `fmtNum`. Table / tooltip audits: `fmtInt`. Rates: `fmtPct`. Missing: `-`.

---

## Color families (canvas-aware)

v2 canvas is a **cool ice wash**: `--page-bg` `#F8FAFF` / `#F0F4FF` / `#F5F5F7` / `#FAF8FF`, mesh in `--accent` (`#2563EB`) and `--accent-2` (`#6366F1`), cards `#FFFFFF`. Funnel fills must **sit on the white card** and **not melt into the ice canvas**.

| Rule | Do | Do not |
|------|----|--------|
| Intra-bar | Nearly solid. Sheen only: mix **4-8%** white at the top, **4-8%** ink at the bottom (`color-mix`) | Two far hexes on one bar (pastel top, navy bottom) |
| Across stages | Eligible a step lighter than submit, **same hue**, 400 / 500 / 600 | 300 ice tint → 800 navy |
| Vs canvas | Mid chroma so the bar reads on white and on `#F0F4FF` | `#93C5FD` / `#C4B5FD` / `#F4CFA8` (they match the page wash) |
| Other product | Warm complement, same chroma band as Cara 400-600 | Neon `#F97316` / `#FF6B00` |

Each **population** gets a hue family. Set `data-funnel-scale` on `.funnel`. Conversion chips **reuse the destination bar fill**: first chip = `--funnel-2`, second chip = `--funnel-3`. Wash = `color-mix(14%, var(--surface))`. No extra chip hex.

**Worked example, not law.** The four Cara / Chatbot ramps below are from one satisfaction dashboard. The rule is: one hue family per population, 400 / 500 / 600, 4-8% sheen, no neon orange. Do not paint Chatbot apricot onto an unrelated dashboard.

**Why these four (Cara example):**

- **Cara All** - `--accent` royal blue. Already on the mesh. Stage 3 = `#2563EB`.
- **Cara no CF** - sky / cyan shift of the same cool family. Distinct from royal, still at home on the ice wash.
- **Cara CF** - violet, sibling of `--accent-2` indigo (the lavender end of `--page-bg`). Not pale 300-violet.
- **Chatbot CF** - dusty apricot. Warm complement to the cool canvas so it reads as a **different product**, chroma matched so it does not shout.

### Light mode (one solid per stage)

| Scale | Key | Stage 1 | Stage 2 | Stage 3 |
|-------|-----|---------|---------|---------|
| Cara All - royal blue | `cara_all` | `#60A5FA` | `#3B82F6` | `#2563EB` |
| Cara no CF - sky | `cara_lower` | `#38BDF8` | `#0EA5E9` | `#0284C7` |
| Cara CF - violet | `cara_cf` | `#A78BFA` | `#8B5CF6` | `#7C3AED` |
| Chatbot CF - dusty apricot | `chatbot_cf` | `#D4A574` | `#C4925A` | `#B07D48` |

### Dark mode

Same solids (they already sit on `#1C1F28`). Chatbot stage 1 only: `#DDB089` so clay does not mud on dark cards. Chips still track `--funnel-2` / `--funnel-3`.

| Scale | Stage 1 | Stage 2 | Stage 3 |
|-------|---------|---------|---------|
| `cara_all` | `#60A5FA` | `#3B82F6` | `#2563EB` |
| `cara_lower` | `#38BDF8` | `#0EA5E9` | `#0284C7` |
| `cara_cf` | `#A78BFA` | `#8B5CF6` | `#7C3AED` |
| `chatbot_cf` | `#DDB089` | `#C4925A` | `#B07D48` |

### Intra-bar sheen (required)

One `--funnel-N` solid. The bar is **not** a second color:

```css
.funnel-bar {
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--funnel-fill) 96%, #FFFFFF) 0%,
    color-mix(in srgb, var(--funnel-fill) 94%, #1D1D1F) 100%
  );
}
.funnel-bar--engaged { --funnel-fill: var(--funnel-1); }
.funnel-bar--view { --funnel-fill: var(--funnel-2); }
.funnel-bar--submit { --funnel-fill: var(--funnel-3); }
body.dark .funnel-bar {
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--funnel-fill) 94%, #FFFFFF) 0%,
    color-mix(in srgb, var(--funnel-fill) 96%, #030303) 100%
  );
}
```

If the top of a bar reads as a different color from the bottom, the mix is too strong. Cap at 8% white / 8% ink.

### New products

Pick a **hue that already lives on the canvas** (accent, accent-2, or a warm complement), then three close stops:

1. Stage 1 ≈ 400 of the hue (not 300: ice tints vanish on `--page-bg`).
2. Stage 2 ≈ 500.
3. Stage 3 ≈ 600 (not 800: navy fights the white card).
4. No separate chip color. First conversion = `--funnel-2`. Second = `--funnel-3`.
5. Comparison product: complementary hue, **same chroma band**. Never `#FF6B00` / `#F97316`.

---

## CSS (copy)

Requires v2 tokens (`--text-h2`, `--ink`, `--radius-pill`, `--border`, `--canvas-deep`) and Phosphor `ph-arrow-right`. Header actions use the same `.card-header-row` / `.pop-toggle` as the rest of the dashboard.

```css
.card-header-row {
  display: flex; align-items: flex-start; justify-content: space-between;
  gap: 16px; flex-wrap: wrap; margin-bottom: 18px;
}
.card-header-actions {
  display: flex; align-items: center; gap: 12px; margin-left: auto; flex-shrink: 0;
  flex-wrap: wrap; justify-content: flex-end;
}
.funnel-basis { display: flex; align-items: center; gap: 8px; margin: 0; }
.card-header-actions .funnel-basis {
  padding-left: 12px;
  border-left: 1px solid var(--border);
}
.funnel-basis-label {
  font-size: var(--text-sm); font-weight: 500; color: var(--ink-soft);
  white-space: nowrap;
}

.funnel {
  display: flex; align-items: stretch; justify-content: center;
  gap: 8px; padding: 24px 8px 8px;
  --funnel-1: #60A5FA;
  --funnel-2: #3B82F6;
  --funnel-3: #2563EB;
}
.funnel[data-funnel-scale="cara_all"] {
  --funnel-1: #60A5FA;
  --funnel-2: #3B82F6;
  --funnel-3: #2563EB;
}
.funnel[data-funnel-scale="cara_lower"] {
  --funnel-1: #38BDF8;
  --funnel-2: #0EA5E9;
  --funnel-3: #0284C7;
}
.funnel[data-funnel-scale="cara_cf"] {
  --funnel-1: #A78BFA;
  --funnel-2: #8B5CF6;
  --funnel-3: #7C3AED;
}
.funnel[data-funnel-scale="chatbot_cf"] {
  --funnel-1: #D4A574;
  --funnel-2: #C4925A;
  --funnel-3: #B07D48;
}
body.dark .funnel[data-funnel-scale="chatbot_cf"] {
  --funnel-1: #DDB089;
  --funnel-2: #C4925A;
  --funnel-3: #B07D48;
}

.funnel-col {
  flex: 0 0 128px; width: 128px;
  display: grid;
  grid-template-rows: 32px 220px auto;
  justify-items: center;
}
.funnel-count {
  grid-row: 1; align-self: end;
  font-size: var(--text-h2); font-weight: 700; letter-spacing: -0.03em;
  line-height: 1.1; color: var(--ink); margin: 0;
  font-variant-numeric: tabular-nums;
}
.funnel-bar-track {
  grid-row: 2;
  width: 100px; height: 100%;
  display: flex; align-items: flex-end;
}
.funnel-bar {
  width: 100%; border-radius: 16px;
  min-height: 12px;
  transition: height 300ms cubic-bezier(0.22, 1, 0.36, 1);
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--funnel-fill) 96%, #FFFFFF) 0%,
    color-mix(in srgb, var(--funnel-fill) 94%, #1D1D1F) 100%
  );
}
.funnel-bar--engaged { --funnel-fill: var(--funnel-1); }
.funnel-bar--view { --funnel-fill: var(--funnel-2); }
.funnel-bar--submit { --funnel-fill: var(--funnel-3); }
body.dark .funnel-bar {
  background: linear-gradient(
    180deg,
    color-mix(in srgb, var(--funnel-fill) 94%, #FFFFFF) 0%,
    color-mix(in srgb, var(--funnel-fill) 96%, #030303) 100%
  );
}
.funnel-label {
  grid-row: 3; align-self: start;
  margin-top: 12px; font-size: var(--text-sm); font-weight: 500;
  color: var(--ink-soft); text-align: center; line-height: 1.3;
  max-width: 128px;
}
.funnel-arrow {
  flex: 0 0 72px; width: 72px;
  display: grid;
  grid-template-rows: 32px 220px auto;
  justify-items: center;
  color: var(--ink-soft);
}
.funnel-arrow-body {
  grid-row: 2; align-self: center;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.funnel-arrow i { font-size: 18px; line-height: 1; }
.funnel-arrow--to-2 { --funnel-chip: var(--funnel-2); }
.funnel-arrow--to-3 { --funnel-chip: var(--funnel-3); }
.funnel-arrow--to-2 i,
.funnel-arrow--to-3 i { color: var(--funnel-chip); opacity: 0.72; }
.funnel-conv {
  font-size: var(--text-h2); font-weight: 700; letter-spacing: -0.03em;
  line-height: 1.1; color: var(--funnel-chip);
  background: color-mix(in srgb, var(--funnel-chip) 14%, var(--surface));
  border-radius: var(--radius-pill);
  padding: 8px 12px;
  font-variant-numeric: tabular-nums;
}
.funnel-foot {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 16px; margin-top: 24px; padding-top: 20px;
  border-top: 1px solid var(--border);
  text-align: center;
}
.funnel-foot-label {
  font-size: var(--text-xs); font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.06em; color: var(--ink-soft);
}
.funnel-foot-value {
  font-size: var(--text-h3); font-weight: 700; letter-spacing: -0.02em;
  color: var(--ink); margin-top: 6px; font-variant-numeric: tabular-nums;
}
@media (max-width: 640px) {
  .funnel { flex-wrap: wrap; }
  .funnel-arrow { width: 100%; flex: 1 0 100%; grid-template-rows: auto; }
  .funnel-arrow-body { flex-direction: row; gap: 8px; }
  .funnel-bar-track { height: 160px; }
  .funnel-col { grid-template-rows: 32px 160px auto; }
}
```

Bar class names `--engaged` / `--view` / `--submit` are stage slots (1 / 2 / 3). Relabel the copy; keep the class hooks.

---

## HTML header (copy)

```html
<div class="card">
  <div class="card-header-row">
    <div>
      <h2 class="card-title">Survey funnel</h2>
      <p class="card-sub">Eligible to viewed modal to submitted. Cara All, Cara no CF, and Cara CF eligible = engaged. Chatbot CF eligible = reached contact flow.</p>
    </div>
    <div class="card-header-actions">
      <div class="pop-toggle" id="chToggleVol" role="tablist" aria-label="Channel"></div>
      <div class="funnel-basis">
        <span class="funnel-basis-label">% from:</span>
        <div class="pop-toggle" id="rateBaseToggle" role="tablist" aria-label="Rate basis"></div>
      </div>
    </div>
  </div>
  <div id="surveyFunnel"></div>
</div>
```

---

## JS skeleton

`maxH` **must** equal the CSS track row (`220`). Bar height is `n / firstStage * maxH`, floored at `12`.

`% from` previous step: `to / from * 100`. `% from` first stage: `to / first * 100`.

```javascript
function renderSurveyFunnel() {
  const ch = DATA.channels[currentCh];
  const first = ch.engaged;
  const view = ch.funnel.view;
  const submit = ch.funnel.submit;
  const firstLabel = currentCh === "chatbot_cf"
    ? "Contact flow conversations"
    : "Engaged sessions";
  const steps = [
    { label: firstLabel, n: first, bar: "funnel-bar--engaged" },
    { label: "Viewed modal", n: view, bar: "funnel-bar--view" },
    { label: "Submitted", n: submit, bar: "funnel-bar--submit" },
  ];
  const maxH = 220;
  const rates = [
    funnelRate(view, first, first),
    funnelRate(submit, view, first),
  ];

  function col(step) {
    const h = first ? Math.max(12, (step.n / first) * maxH) : 12;
    return (
      '<div class="funnel-col">' +
        '<div class="funnel-count">' + fmtNum(step.n) + "</div>" +
        '<div class="funnel-bar-track"><div class="funnel-bar ' + step.bar + '" style="height:' + h + 'px"></div></div>' +
        '<div class="funnel-label">' + step.label + "</div>" +
      "</div>"
    );
  }
  function arrow(pct, toStage) {
    return (
      '<div class="funnel-arrow funnel-arrow--to-' + toStage + '">' +
        '<div class="funnel-arrow-body">' +
          '<i class="ph ph-arrow-right" aria-hidden="true"></i>' +
          '<span class="funnel-conv">' + fmtPct(pct, 1) + "</span>" +
        "</div>" +
      "</div>"
    );
  }

  host.innerHTML =
    '<div class="funnel" data-funnel-scale="' + currentCh + '">' +
      col(steps[0]) + arrow(rates[0], 2) + col(steps[1]) + arrow(rates[1], 3) + col(steps[2]) +
    "</div>" +
    '<div class="funnel-foot">…</div>';
}
```

Re-render when the population pill or `% from` pill changes so `data-funnel-scale` and chip percents stay in sync.

---

## Reference bake (Cara, Aug 6 - Aug 18 2026)

Use only as **visual dummy data** in the example file, not as a live source of truth.

| Key | Label | Eligible | Viewed | Submitted |
|-----|-------|----------|--------|-----------|
| `cara_all` | Cara All | 1943 | 1190 | 624 |
| `cara_lower` | Cara no CF | 1327 | 694 | 318 |
| `cara_cf` | Cara CF | 616 | 496 | 306 |
| `chatbot_cf` | Chatbot CF | 36261 | 29905 | 13038 |

---

## Anti-patterns

- Stretching columns with `flex: 1` so bars fill the card
- Putting `% from` under the title or left of the channel pills
- Conversion chip at `--text-sm` (it is the hero of this chart)
- One `--accent` / `--accent-2` pair for every population
- Neon chatbot orange (`#F97316`, `#FF6B00`)
- Mixing royal blue and sky blue in the **same** funnel (those are two Cara breaks)
- Ice-300 fills (`#93C5FD`, `#7DD3FC`, `#C4B5FD`, `#F4CFA8`) that melt into `--page-bg`
- A two-tone bar (pastel top, navy bottom). Sheen is 4-8% `color-mix`, not a second hex
- A third chip hex. Conversion color is the destination bar (`--funnel-2` / `--funnel-3`)
- Stage 3 at 800-navy (`#1E3A8A`, `#0C4A6E`) on a white card
- Chart.js funnel, pyramid, or Sankey for this 3-stage survey story
- Bar height from `%` when `% from` is "first stage" (height is always share of eligible)
- `maxH` out of sync with `grid-template-rows`
- `toLocaleString` on counts; `--` as the empty sentinel

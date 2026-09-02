# Color valence (v2)

Color encodes **whether the metric going up is better or worse**, not the chart's category. Ask before every fill: **if this number goes up, is that better or worse for the reader?**

Validated against Cara Dissatisfaction: two blues for mild vs frustrated understated heat; volume-sorting the heat bar put frustrated left of mild so the scale read backwards; `--text-xs` on 72px segments was too small to scan.

`--accent` is the user's color when they name one, otherwise the **default** `#2563EB` with `--accent-2` `#6366F1`. Never ask which color -- use the default and build. Accent is not a severity color.

**Locked series colors.** A population key keeps the same hex when a toggle flips (SSA, SR, NS; Cara vs Chatbot). Do not remint the palette per view. Map `DATA.populations[k].color` (or a `SERIES_COLOR` table) once; every chart reads from that map.

Canonical severity fills are the 5-stop palette below. Do not invent a sixth heat color.

---

## 1. Direction of the metric

| If the number goes up | Color family | Examples |
|-----------------------|--------------|----------|
| **Worse** | `--warning` → `--sev-mid` → `--danger` / `--sev-hi` as magnitude / severity rises | TOR, DSAT, dissatisfaction rate, rage share, wait time, error rate, churn, handover failure, occupancy-too-high when that is the story |
| **Better** | `--success` / `--sev-ok`, or `--accent` if it is the healthy primary KPI | CSAT, resolution, intended deflection, coverage |
| **No moral** (magnitude only) | `--accent` / `--ink` | analysed n, session volume, sample size |

Never paint a bad-when-high KPI in trust-blue. A 72.7% dissatisfaction split in big blue reads as a healthy score. Use `--sev-flag` (`--sev-hi` red, white ink) for "has the bad signal"; gray for remainder. Heat among that group still uses `--sev-lo` / `--sev-mid` / `--sev-hi` (add `--sev-max` when there is a critical stop). Connect the two with a drill-down arrow (section 7). `--accent` stays on analysed n, selected pills, and primary actions.

Hero KPI chrome follows the same rule. Top bar, wash, and value color use the valence token, not `--accent`, when the hero is a standalone bad-when-up number. See [component-recipes.md](component-recipes.md).

Trend chips follow valence, not geometry. TOR **up** is `--danger` / `--warning`, not `--success`. Prefer classes `.better` / `.worse` over `.up` / `.down`.

---

## 2. Intensity / severity scales

Canonical 5-stop palette (light mode). Ink is locked per fill from WCAG 2.1 AA (body 4.5:1). Do not put white on green / yellow / orange, or black on red / maroon.

| Rank | Token | Fill | Ink on fill | Reads as |
|------|-------|------|-------------|----------|
| Healthy / lowest | `--sev-ok` | `#69c440` | `#1D1D1F` (9.57:1) | Good, ok, CSAT-high, TOR-zero. **Not** mild-bad. |
| Lowest-bad | `--sev-lo` | `#f1dc32` | `#1D1D1F` (15.02:1) | Mild / caution. Still a problem. Never blue. Never `--sev-ok` green. |
| Mid-bad | `--sev-mid` | `#ff9323` | `#1D1D1F` (9.45:1) | Elevated / frustrated. Must not look like `--accent`. |
| High | `--sev-hi` | `#da0808` | `#FFFFFF` (5.22:1) | Rage / fail / high TOR. White ink only. |
| Worst | `--sev-max` | `#950404` | `#FFFFFF` (9.14:1) | Critical. Darker than `--sev-hi`. |
| No signal | `--sev-none` | `--paper-deep` gray | `--ink-soft` | Not in group / not a problem color. |

Which stops to use:

| Scale | Tokens left → right |
|-------|---------------------|
| 3-stop (mild → frustrated → rage) | `--sev-lo` → `--sev-mid` → `--sev-hi` |
| 4-stop (add critical) | `--sev-lo` → `--sev-mid` → `--sev-hi` → `--sev-max` |
| 5-stop (includes a healthy band) | `--sev-ok` → `--sev-lo` → `--sev-mid` → `--sev-hi` → `--sev-max` |
| Bad-vs-remainder split | `--sev-flag` (`#da0808`, white ink) vs `--sev-none` |

`--success` is `#69c440` (same as `--sev-ok`). `--warning` is `#ff9323` (same as `--sev-mid`) for chips and copy. `--danger` is `#da0808` (same as `--sev-hi`). `--sev-flag` aliases `--sev-hi`.

Green vs orange is 1.01:1. Yellow vs green is 1.57:1. Never stack those fills as the only difference between adjacent segments. Order + label + legend are required.

Do **not** use the primary accent ramp for a heat / severity scale. Accent stays for analysed counts, primary actions, selected pills, and volume. Density calendars of volume may still use the accent ramp (magnitude, no moral).

---

## 3. Order is the scale, not volume

Left-to-right (or top-to-bottom) on an **ordered state** chart is the rank: ok → mild → mid → high → worst. Volume lives in the **label and legend counts**.

Driver / reason bars still default to **volume sort** (highest share first). That rule does not apply to severity, TOR bands, or any ordinal heat. Volume-sorting those puts the fattest band first, so frustrated sits left of mild and the scale reads backwards.

Legend order **matches the bar** (the scale), not a separate volume ranking.

A sliver below ~8% cannot hold an in-bar label. Keep a tick-and-label callout; park it on the **worst** end so the callout does not sit in the middle of mild.

---

## 4. Tokens

Canonical copy also in [soft-ui-tokens.md](soft-ui-tokens.md). Ink tokens stay dark on the three light fills even under `body.dark` (those fills do not invert).

```css
:root {
  --accent: #2563EB;              /* primary / volume / trust. Not heat. */

  --success: #69c440;             /* = --sev-ok. Good-when-up. Dark ink on fill. */
  --success-soft: rgba(105, 196, 64, 0.16);
  --warning: #ff9323;             /* = --sev-mid. Caution chips. Dark ink on fill. */
  --warning-soft: rgba(255, 147, 35, 0.16);
  --danger: #da0808;              /* = --sev-hi. Fail / rage. White ink on fill. */
  --danger-soft: rgba(218, 8, 8, 0.14);

  --sev-ok: #69c440;              /* healthy. Ink #1D1D1F. */
  --sev-lo: #f1dc32;              /* mild-bad. Ink #1D1D1F. */
  --sev-mid: #ff9323;             /* elevated. Ink #1D1D1F. */
  --sev-hi: #da0808;              /* high / rage. Ink #fff. */
  --sev-max: #950404;             /* worst. Ink #fff. */
  --sev-flag: var(--sev-hi);      /* bad-when-up rate split. White ink. */
  --sev-none: var(--paper-deep);

  --sev-ok-ink: #1D1D1F;
  --sev-lo-ink: #1D1D1F;
  --sev-mid-ink: #1D1D1F;
  --sev-hi-ink: #FFFFFF;
  --sev-max-ink: #FFFFFF;
  --sev-flag-ink: #FFFFFF;

  --sev-ok-soft: rgba(105, 196, 64, 0.16);
  --sev-lo-soft: rgba(241, 220, 50, 0.16);
  --sev-mid-soft: rgba(255, 147, 35, 0.16);
  --sev-hi-soft: rgba(218, 8, 8, 0.14);
  --sev-max-soft: rgba(149, 4, 4, 0.16);
}

body.dark {
  --warning: #ff9323;             /* still a fill; as text on dark it clears AA */
  --danger: #F87171;              /* text-on-dark. Fill charts still use --sev-hi */
  --sev-ok: #69c440;
  --sev-lo: #f1dc32;
  --sev-mid: #ff9323;
  --sev-hi: #f04444;              /* slight lift so it separates from max on #1C1F28 */
  --sev-max: #da0808;             /* #950404 is 1.80:1 on dark surface - unreadable */
  --sev-flag: var(--sev-hi);
  --sev-none: var(--paper-deep);
  /* ink tokens do not flip: light fills still need #1D1D1F */
}
```

Retune `--sev-hi` / `--sev-max` under `body.dark` so rank still reads high < worst and both bars clear the dark surface. Do not invert the green / yellow / orange stops.

---

## 5. Accessibility

- Text **on** colored segments must use the ink column in section 2. White on `--sev-ok` / `--sev-lo` / `--sev-mid` fails (2.19 / 1.40 / 2.22). Black on `--sev-hi` / `--sev-max` fails body AA (4.02 / 2.30). If a pairing fails, **darken the fill** - do not keep pale-on-pale.
- `--sev-ok-ink`, `--sev-lo-ink`, `--sev-mid-ink` stay `#1D1D1F` in dark mode. Do not use `var(--ink)` on those fills (dark-mode `--ink` is light).
- Color is never the only encoder. Pair with labels, counts, **order**, and a legend.
- `--sev-ok` vs `--sev-mid` collapse by luminance (1.01:1). Do not rely on red / green alone for good / bad.

---

## 6. In-bar type (stacked HTML bars)

`--text-xs` (12px) on a 56-72px segment is too small to scan. Use the existing scale, do not invent a seventh size:

| Surface | Size |
|---------|------|
| In-bar percentage (`b`) | `--text-h3` (18) |
| In-bar category (`i`) | `--text-sm` (13) or `--text-base` (14) |
| Legend + counts | `--text-sm`; counts tabular |
| Thin-slice callout | `--text-sm`, not xs |
| Card KPI (n analysed) | `--text-kpi` |

Hide in-bar type under ~8% width; callout instead. Color in-bar type with the matching `--sev-*-ink`. See [overflow-rules.md](overflow-rules.md).

---

## 7. Nested distribution (drill-down arrow)

When chart B is how a **segment of chart A** breaks (Dissatisfied → heat; TOR failures → reason), do not stack two sibling cards and hope the titles explain it.

- Put a connector **between** the cards: elbow from the **midpoint of the parent segment** down, then into the **midpoint of the child chart**, with a Phosphor caret and one line that names the subset (`How those 2,561 break by heat`). Derive the count from `DATA` via `fmtInt`. Do not center the arrow on the page if the parent slice is not centered.
- Optional: a tick under the parent segment that B expands.
- Static. No bounce. `prefers-reduced-motion` already forbids extra motion.
- Caption uses `-`, never em/en/`--`.

---

## 8. Anti-patterns

- Two blues for mild vs frustrated
- Hero dissatisfaction % (or TOR, DSAT, rage share) in `--accent` blue
- Painting the "has signal" rate segment `--accent` so 72.7% dissatisfied looks healthy
- TOR bar in the same blue as "sessions analysed" when TOR is the hero
- Rage as a tiny orange sliver that looks like a highlight, not `--sev-hi`
- Green (`--sev-ok`) for "mild dissatisfaction" (mild is `--sev-lo` yellow)
- White text on `--sev-ok`, `--sev-lo`, or `--sev-mid`
- Black text on `--sev-hi` or `--sev-max` for body copy
- Accent ramp as a dissatisfaction / TOR heat scale
- `.trend-chip.up` in `--success` when up is worse
- Volume-sorting a mild → rage (or TOR-band) stacked bar
- Legend in volume order while the bar is in severity order
- Two stacked distribution cards with no arrow when the second is a subset of the first
- `--text-xs` as the only type on in-bar labels
- Adjacent `--sev-ok` and `--sev-mid` segments with no label (1.01:1)

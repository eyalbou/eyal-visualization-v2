# Soft UI Tokens (v2)

`#2563EB` / `#6366F1` is the **default accent pair**. Keep it whenever the user has not named a color -- never ask. If they do name one, swap `--accent`, `--accent-2`, `--accent-glow`, and the derived mesh / shape / shadow rgba values to that hue.

Default chart colors come from this file, not from a new palette: `--accent` and `--accent-2` for magnitude and category series, `--sev-*` for severity and bad-when-up rates, `--success` / `--danger` for trend chips. See [color-valence.md](color-valence.md).

Full validated set from `multi-site-accounts-v2.html`:

```css
:root {
  /* Two families only -- see SKILL.md "Fonts". Axiforma has no public CDN;
     DM Sans is what actually ships. Never <link> Axiforma. */
  --font: "Axiforma", "DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;

  /* Dashboard type scale; hero exception below */
  --text-xs: 12px;
  --text-sm: 13px;
  --text-base: 14px;
  --text-body: 16px;
  --text-h3: 18px;
  --text-h2: 20px;
  --text-h1: 24px;
  --text-kpi: 28px;
  --text-kpi-hero: 32px;
  --text-hero-display: clamp(2.5rem, 6vw + 1rem, 4.75rem);

  --canvas: #F5F5F7;
  --canvas-deep: #EBEBEF;
  --ink: #1D1D1F;
  --ink-soft: #6E6E73;
  --surface: #FFFFFF;
  --surface-raised: #FFFFFF;
  --paper-deep: #F0F1F5;

  --accent: #2563EB;
  --accent-glow: rgba(37, 99, 235, 0.1);
  --accent-2: #6366F1;
  --accent-2-soft: rgba(99, 102, 241, 0.1);

  --success: #69c440;
  --success-soft: rgba(105, 196, 64, 0.16);
  --warning: #ff9323;
  --warning-soft: rgba(255, 147, 35, 0.16);
  --danger: #da0808;
  --danger-soft: rgba(218, 8, 8, 0.14);

  /* 5-stop severity palette. Not the accent ramp. Rank left-to-right.
     Ink is locked per fill. Full rules: color-valence.md */
  --sev-ok: #69c440;
  --sev-lo: #f1dc32;
  --sev-mid: #ff9323;
  --sev-hi: #da0808;
  --sev-max: #950404;
  --sev-flag: var(--sev-hi);
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

  --border: rgba(0, 0, 0, 0.06);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 24px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.08);

  --radius-sm: 12px;
  --radius: 20px;
  --radius-lg: 24px;
  --radius-pill: 9999px;

  /* Full-page canvas */
  --page-bg: linear-gradient(160deg, #F8FAFF 0%, #F0F4FF 35%, #F5F5F7 70%, #FAF8FF 100%);
  --hero-surface-base: #F5F5F7;
  --hero-mesh: radial-gradient(ellipse 80% 60% at 20% 20%, rgba(37, 99, 235, 0.08), transparent 55%),
    radial-gradient(ellipse 70% 50% at 85% 75%, rgba(99, 102, 241, 0.07), transparent 50%);
  --shape-border: rgba(37, 99, 235, 0.12);
  --shape-shadow: 0 8px 32px rgba(37, 99, 235, 0.08);
  --shape-1: linear-gradient(90deg, rgba(37, 99, 235, 0.16), transparent);
  --shape-2: linear-gradient(90deg, rgba(99, 102, 241, 0.14), transparent);
  --shape-3: linear-gradient(90deg, rgba(79, 70, 229, 0.12), transparent);
  --shape-4: linear-gradient(90deg, rgba(37, 99, 235, 0.1), transparent);
  --shape-5: linear-gradient(90deg, rgba(99, 102, 241, 0.1), transparent);
  --hero-badge-bg: rgba(255, 255, 255, 0.65);
  --hero-badge-border: rgba(0, 0, 0, 0.06);
  --hero-title-grad-1: linear-gradient(180deg, var(--ink) 0%, color-mix(in srgb, var(--ink) 75%, transparent) 100%);
  --hero-title-grad-2: linear-gradient(90deg, var(--accent) 0%, color-mix(in srgb, var(--accent-2) 80%, var(--accent)) 55%, color-mix(in srgb, var(--accent) 70%, #fda4af) 100%);
  --hero-subtitle: var(--ink-soft);
}

body.dark {
  --page-bg: #030303;
  --hero-surface-base: #030303;
  --canvas: #0F1117;
  --canvas-deep: #161922;
  --ink: #F5F5F7;
  --ink-soft: #98989D;
  --surface: #1C1F28;
  --paper-deep: #12151C;
  --accent: #3B82F6;
  --accent-glow: rgba(59, 130, 246, 0.15);
  --warning: #ff9323;
  --danger: #F87171;
  --sev-ok: #69c440;
  --sev-lo: #f1dc32;
  --sev-mid: #ff9323;
  --sev-hi: #f04444;
  --sev-max: #da0808;
  --sev-flag: var(--sev-hi);
  --sev-none: var(--paper-deep);
  --hero-title-grad-1: linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0.78) 100%);
  --hero-title-grad-2: linear-gradient(90deg, #A5B4FC 0%, rgba(255, 255, 255, 0.92) 50%, #FDA4AF 100%);
  --hero-subtitle: rgba(255, 255, 255, 0.45);
  /* boost shape-* opacities -- see hero-geometric.md */
}
```

## Font loading (required in `<head>`)

```html
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/400.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/500.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/600.css" rel="stylesheet" />
<link href="https://cdn.jsdelivr.net/npm/@fontsource/dm-sans/700.css" rel="stylesheet" />
```

All four weights, or the browser synthesises fake bold and it reads as a second typeface.

## Base type rules (required)

```css
html, body { font-family: var(--font); }
body { font-size: var(--text-body); }
button, input, select, textarea { font-family: inherit; }
code, pre { font-family: var(--font-mono); }
code {
  font-size: 0.92em;
  padding: 1px 6px;
  border-radius: 5px;
  background: var(--canvas-deep);
  color: var(--ink);
}
```

Skipping the `code` rule is the usual cause of a stray third font -- the UA default is Courier at an unscaled size.

Cards: white `--surface`, no border, `--shadow-md`, `--radius-lg`.

Pill toggles: track `--canvas-deep`; active = solid `--accent` + white text.

**Valence:** `--accent` is volume / trust / selected, not "how hot." Bad-when-up KPIs and mild → rage scales use `--warning` / `--sev-*` / `--danger`. 3-stop heat is `--sev-lo` `#f1dc32` → `--sev-mid` `#ff9323` → `--sev-hi` `#da0808`. Add `--sev-ok` `#69c440` only when the scale includes a healthy band, `--sev-max` `#950404` when it includes critical. Ink: dark `#1D1D1F` on ok / lo / mid; white on hi / max. See [color-valence.md](color-valence.md).

See [hero-geometric.md](hero-geometric.md) for canvas structure and first-load animations.

## Optional brand palette

When the user picks this palette (see SKILL.md). Dropped `#FF9100` (dup orange) and `#00B7CD` (dup teal).

```css
:root.palette-ocean-sun {
  --palette-cream: #FFF1D1;
  --palette-ice: #8ECAE6;
  --palette-teal: #219EBC;
  --palette-navy: #023047;
  --palette-gold: #FFB703;
  --palette-orange: #FB8500;
  --palette-red: #DF301C;
  --accent: var(--palette-teal);
  --accent-2: var(--palette-ice);
  --accent-glow: rgba(33, 158, 188, 0.12);
  --ink: var(--palette-navy);
  --canvas: var(--palette-cream);
  --highlight: var(--palette-gold);
  --warm: var(--palette-orange);
}
```

`--palette-gold` / `--palette-orange` are highlights, not TOR/DSAT fills. `--palette-red` may alias `--danger` if they want brand-aligned errors.


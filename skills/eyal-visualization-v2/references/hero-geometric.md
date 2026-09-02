# Hero Geometric Masthead

Kokonut UI "Shape Landing Hero" adapted for **self-contained HTML dashboards** (no React, no Framer Motion). Reference: [21st.dev shape-landing-hero](https://21st.dev/community/components/kokonutd/shape-landing-hero/default).

## Full-page canvas (required)

Geometric background covers the **entire document**, not a hero card:

```html
<body>
  <div class="page-canvas" aria-hidden="true">
    <div class="page-canvas__mesh"></div>
    <div class="hero-shape hero-shape--1"></div>
    <!-- ... 5 shapes, viewport-positioned -->
    <div class="page-canvas__vignette"></div>
  </div>
  <div class="page-chrome"><!-- fixed theme toggle --></div>
  <div class="shell">
    <header class="hero-geometric">...</header>
    <!-- dashboard content scrolls on top -->
  </div>
</body>
```

```css
.page-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: var(--page-bg);
}
.shell { position: relative; z-index: 1; }
```

Shapes use **viewport** placement (Kokonut sizes: 600x140, 500x120, etc.) at `left: -10%`, `top: 12%`, etc.

## Hero typography (Kokonut-style)

Center-aligned. **Exception** to dashboard `--text-h1` (24px) -- page hero only:

```css
--text-hero-display: clamp(2.5rem, 6vw + 1rem, 4.75rem); /* ~40-76px */

.hero-geometric__content { text-align: center; max-width: 52rem; margin: 0 auto; }

.hero-geometric h1 {
  font-size: var(--text-hero-display);
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1.05;
}
```

- **Line 1**: vertical gradient (`--hero-title-grad-1`) -- ink fade light / white fade dark
- **Line 2**: horizontal gradient (`--hero-title-grad-2`) -- accent indigo-white-rose mapping
- **Subtitle**: `font-weight: 300`, `letter-spacing: 0.04em`, centered, muted (`--hero-subtitle`)
- **Badge**: pill above title, accent dot with glow

Section titles below hero still use `--text-h2` (20px).

## Hero copy (required)

Visual rules above are not enough. The h1 and subtitle carry the story.

Caps are counted, not judged: [SKILL.md Copy budget](../SKILL.md#copy-budget-hard-caps), enforced by `scripts/copy-check.py`.

**Title -- research name.** Line 1 + line 2 together are the study name a teammate would search for (`Cara Feedback Modal`, `Cara Dissatisfaction`, `Multi-site accounts`). Not a slogan (`What to fix first`) and not method (`session by session`, `4:1148`, `session grain`). Method goes to **Methodology** -- never to the badge pill or a hero chip.

**Subtitle -- ≤35 words, max 2 sentences, covering why read / what you get.** Stakeholder English. The aim can stay implied; do not spend a sentence on it. "How we will answer it" is at most **one clause**, not SQL, scoring mechanics, or funnel mechanics. Ban caveats, `COUNT(DISTINCT msid)`, and `engaged → view → submit` as the whole subtitle. If the line is ambiguous, draft 3 options and wait.

The page hero **is** the briefing. Do not add a second briefing card. Title + subtitle stay tab-agnostic.

Good (24 words): `How many accounts carry 100+ sites, and does that concentration change who we should treat as the unit of analysis?`

Bad (95 words -- three sentences that each add a clause of method): `Customer Care runs 27 dashboards on Vizion and one semantic model on Power BI, and nothing written down says which platform new work should go to. This page scores both across 25 rows, keeping what each product can do apart from what CC actually has working today, and names the three rows where Power BI is the only right answer. The aim is a routing rule for new dashboards plus four ownership decisions, not a winner.`

Same page inside budget (28 words): `CC has no written rule for which platform a new dashboard belongs on. This page scores both and names the three cases where Power BI wins.`

Bad (slogan): `Finding the sub-text of our users.`

### Chips under the subtitle (`.badge` row)

Max **3 chips**, **≤4 words each**. Allowed: population / scope (`Logged-in users`), window (`Jun 11 - Aug 20`), size (`6.4M accounts`), freshness (`Data through Aug 27`), status (`Test running`).

**Never:** pipeline or job names, tool and connector names, table names, commit hashes, run IDs, model names, second-level timestamps, or a `·`-joined stack of them. `XMLA · vizion-platform a7bbfca8 · Trino` and `Verified live 2026-08-26 and 2026-08-27` are failures. The eyebrow `.hero-badge` follows the same 4-word cap.

**Tab-agnostic.** Title and subtitle do not change per tab and must not describe only Tab 1. Sampling and Methodology still sit under the same question.

North-star table and tab arc: [analytics-storytelling.md](analytics-storytelling.md).

## Theme-aware tokens

| Token | Light | Dark |
|-------|-------|------|
| `--page-bg` | soft accent-tinted gradient | `#030303` |
| `--hero-surface-base` | `#F5F5F7` | `#030303` |
| `--hero-mesh` | radial accents 6-8% | radial accents 10-12% |
| `--shape-1` … `--shape-5` | accent gradients 10-16% | same at 12-22% |
| `--hero-title-grad-1` | ink vertical | white vertical |
| `--hero-title-grad-2` | accent horizontal | indigo-white-rose |

Derive from user `--accent` / `--accent-2`.

## Motion (CSS only)

**First page load only** -- CSS `animation` runs once on mount; theme toggle updates `--page-bg` on `::before` with `transition` (no replay).

| Layer | Animation | Timing |
|-------|-----------|--------|
| `.page-canvas` | `canvasEaseIn` opacity 0→1 | 1.8s, ease Kokonut |
| `.page-canvas__mesh` | `meshEaseIn` opacity + scale + blur | 2.2s, delay 0.2s |
| `.page-canvas__vignette` | `vignetteEaseIn` opacity 0→0.75 | 2s, delay 0.35s |
| `.hero-shape` | `shapeEnter` + `shapeFloat` | 2.4s enter, 12s float |

```css
@keyframes canvasEaseIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes meshEaseIn {
  from { opacity: 0; transform: scale(1.06); filter: blur(64px); }
  to   { opacity: 1; transform: scale(1); filter: blur(48px); }
}
```

Base gradient lives on `.page-canvas::before` so dark-mode `background` crossfades without re-running enter animations.

- `prefers-reduced-motion`: snap canvas/mesh/vignette to final state; disable float

## Validation artifact

In-skill: `assets/analytics-starter.html`. Optional live (may not exist here): `ab-tests/priority-general-agent/dashboards/multi-site-accounts-v2.html`.

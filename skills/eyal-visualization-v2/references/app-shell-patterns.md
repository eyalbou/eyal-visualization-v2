# App Shell Patterns (v2)

Sidebar and top-nav layouts for product dashboards. **No photos or avatars.** Icons: **Phosphor** default; Lucide only if the user asks.

Tokens: [soft-ui-tokens.md](soft-ui-tokens.md). Type: same file, font-loading block.

---

## Sidebar shell (default product layout)

```css
.app-layout {
  display: grid;
  grid-template-columns: 228px 1fr;
  min-height: 100vh;
  background: var(--canvas);
}

.app-sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: 228px;
  padding: 24px 16px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.app-main {
  margin-left: 228px;
  padding: 24px 32px 48px;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 32px;
}
```

### Sidebar nav pills

```html
<nav class="side-nav">
  <a class="side-nav__item active" href="#">Overview</a>
  <a class="side-nav__item" href="#">Analytics</a>
  <a class="side-nav__item" href="#">
    Alerts <span class="nav-badge">3</span>
  </a>
</nav>
```

```css
.side-nav__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: var(--radius-pill);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--ink-soft);
  text-decoration: none;
  transition: background 100ms ease, color 100ms ease;
}
.side-nav__item:hover { background: var(--canvas-deep); color: var(--ink); }
.side-nav__item.active {
  background: var(--accent);
  color: #fff;
}
.nav-badge {
  font-size: var(--text-xs);
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  background: rgba(255,255,255,0.2);
}
.side-nav__item:not(.active) .nav-badge {
  background: var(--accent-2-soft);
  color: var(--accent);
}
```

### Card grid

```css
.widget-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}
.widget-span-4 { grid-column: span 4; }
.widget-span-6 { grid-column: span 6; }
.widget-span-8 { grid-column: span 8; }
.widget-span-12 { grid-column: span 12; }

@media (max-width: 900px) {
  .app-layout { grid-template-columns: 1fr; }
  .app-sidebar { display: none; } /* or drawer */
  .app-main { margin-left: 0; }
}
```

---

## Top-nav shell (Crextio-style)

```css
.topnav-shell {
  min-height: 100vh;
  background: linear-gradient(160deg, var(--canvas) 0%, color-mix(in srgb, var(--accent-glow) 40%, var(--canvas)) 100%);
}

.topnav-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

.topnav-pill {
  padding: 8px 18px;
  border-radius: var(--radius-pill);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--ink-soft);
  background: transparent;
  border: none;
  cursor: pointer;
}
.topnav-pill.active {
  background: var(--ink);
  color: var(--surface);
}
body.dark .topnav-pill.active {
  background: var(--surface-raised);
  color: var(--ink);
}
```

---

## Three-column detail panel

```css
.app-layout--3col {
  grid-template-columns: 228px 1fr 320px;
}
.app-detail {
  position: sticky;
  top: 24px;
  height: fit-content;
  padding: 24px;
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
```

Use for: selected row context, schedule detail, preview pane. Panel content = text, metrics, pills only.

---

## Header actions (no avatars)

```html
<div class="header-actions">
  <input class="search-input" type="search" placeholder="Search..." />
  <button class="btn-icon" aria-label="Notifications">
    <i class="ph ph-bell"></i>
    <span class="nav-badge">5</span>
  </button>
  <button class="btn-icon" aria-label="Settings">
    <i class="ph ph-gear"></i>
  </button>
</div>
```

---

## List row (financial dashboard pattern)

```html
<div class="list-row">
  <div class="list-row__icon"><i class="ph ph-arrow-down-left"></i></div>
  <div class="list-row__body">
    <div class="list-row__title">Payment received</div>
    <div class="list-row__meta">Today · 14:32</div>
  </div>
  <span class="category-pill">Income</span>
  <span class="list-row__amount positive">+$1.2K</span>
</div>
```

Icon circle = solid `--canvas-deep` background, Phosphor icon -- never brand logos or photos.

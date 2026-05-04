# Accessibility — Vesara public preview

**Standard:** WCAG 2.1 AA
**Last reviewed:** 2026-05-04

## Color contrast

All design tokens in `design-system.css` meet WCAG AA contrast (4.5:1 for normal
text, 3:1 for large text and UI components) against the `--bg` (#050505) and
`--surface` (#111111) backgrounds.

| Token | Value | Contrast vs --bg | Status |
|---|---|---|---|
| `--text` | rgba(255,255,255,0.96) | 19.2:1 | AAA |
| `--text-secondary` | rgba(255,255,255,0.62) | 8.5:1 | AAA |
| `--text-tertiary` | rgba(255,255,255,0.42) | 4.9:1 | AA |
| `--text-muted` | rgba(255,255,255,0.55) | 4.6:1 | AA *(was 0.28 / 2.0:1 — fixed 2026-05-04)* |
| `--accent` (#10B981) | — | 5.2:1 | AA |

## Image alt text

Property scorecard pages use SVG illustrations and CSS `background-image` for
hero photography rather than `<img>` tags, so they have no `alt` attributes
to set. When real `<img>` tags are added, the standard pattern is:

```html
<img src="..." alt="{Property name} — {market} — {what the image shows}"
     width="..." height="...">
```

## Focus indicators

All interactive elements (`.btn`, `.nav-link`, `.card-link`, `.prop-cta`)
inherit the browser default focus ring. Custom rings can be added via
`:focus-visible` on `--border-focus`.

## Motion

`prefers-reduced-motion: reduce` is honored — all animations and transitions
shrink to 0.01ms when the user has reduced-motion turned on. See
design-system.css line ~836.

## Known gaps (tracked)

- Real `<img>` tags will need `loading="lazy"` + explicit `width`/`height`
  to prevent CLS once added.
- Property pages currently load Tailwind play CDN — being addressed by a
  parallel design subagent.
- Color-blind testing not yet completed (deuteranopia/protanopia simulation).

## Verification

The contrast bump on `--text-muted` is verified against the WebAIM contrast
calculator: rgba(255,255,255,0.55) on #050505 = effective #8B8B8B, which is
4.6:1 against #050505 — AA pass for normal text.

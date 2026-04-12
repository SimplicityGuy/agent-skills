---
name: brand-asset-audit
description: Use when creating a new project's visual identity, auditing brand asset completeness, generating missing design deliverables, or when a project needs logos, favicons, OG images, or a design system document. Triggers on "brand assets", "design system", "favicon", "og image", "logo variants", "apple-touch-icon", "webmanifest".
---

# Brand Asset Audit

## Overview

Audit and generate the complete set of brand assets every project needs. Ensures consistent coverage across logo variants, favicon sizes, social sharing images, PWA manifests, and HTML integration. Source SVGs are the single source of truth — all raster assets derive from them.

## When to Use

- Starting a new project that needs visual identity
- Auditing an existing project for missing brand assets
- After creating initial SVG logos/favicons and needing the full derivative set
- Before shipping a web project (favicon, OG image, manifest gaps)

## Asset Inventory Checklist

### 1. Design System Document

```
design/DESIGN_SYSTEM.md
```

Must define:
- [ ] Project name and tagline
- [ ] Voice and tone guidelines
- [ ] Color system with CSS custom properties (dark + light mode)
  - Brand colors (primary, dim, bright)
  - Status colors (active, running, disabled, error) with background tints
  - Surface/background colors (primary, surface, raised, sunken, hover)
  - Border colors (default, subtle, strong, focus)
  - Text colors (primary, secondary, muted, inverse, accent)
- [ ] Typography: font family, weights (regular/medium/bold), size scale, letter spacing
- [ ] Spacing scale (base unit, token table)
- [ ] Border radius tokens
- [ ] Component patterns (badges, buttons, cards, inputs, tables, code blocks)
- [ ] Dark/light mode CSS custom properties block (copy-pasteable)
- [ ] Quick reference card (one-screen summary of key values)
- [ ] File manifest listing all assets

### 2. Logo Variants

```
design/logos/
  {project}-square-dark.svg    # Square logo, dark background
  {project}-square-light.svg   # Square logo, light background
  icon_dark.svg                # Icon mark only (no text), dark bg
  icon_light.svg               # Icon mark only (no text), light bg
  square_dark.png              # PNG export of square dark
  square_light.png             # PNG export of square light
  icon_dark.png                # PNG export of icon dark
  icon_light.png               # PNG export of icon light
```

**Icon derivation rule:** Remove all `<text>` elements from the square logo SVG. Re-center and scale up the graphic mark to fill the canvas with appropriate padding.

**Dark variant:** Dark background, light/colored graphic.
**Light variant:** Light background, dark/colored graphic. Use the light-mode brand color (not the dark-mode color).

### 3. Banners

```
design/banners/
  {project}-banner-static.svg  # Static banner (GitHub, print)
  {project}-banner-animated.svg # Animated banner (README hero) [optional]
  banner_dark.png              # PNG export of static banner
  banner_light.png             # PNG export of static banner (or light variant if exists)
```

### 4. Favicon SVGs (source)

```
design/favicons/
  favicon-16.svg
  favicon-32.svg
  favicon-48.svg
  favicon-64.svg
  favicon-128.svg
  favicon-192.svg
  favicon-256.svg
  favicon-512.svg
```

All favicon SVGs use dark background with the brand mark. Smaller sizes (16, 32, 48) should simplify the mark for legibility — reduce stroke widths, drop fine details.

### 5. Deployable Favicon Assets

```
assets/static/favicons/        # (or project's static asset directory)
  favicon-{16,32,48,64,128,192,256,512}.svg   # Copy of source SVGs
  favicon-{16,32,48,64,128,192,256,512}.png   # PNG renders at native size
  favicon.ico                  # Multi-size ICO (16 + 32 + 48)
  apple-touch-icon.png         # 180x180, no transparency, dark bg
  site.webmanifest             # PWA manifest
```

### 6. Social / OG Image

```
design/og_image.png            # 1200x630, dark bg, centered logo + name + tagline
assets/static/og_image.png     # Deployed copy
```

### 7. Design Showcase

```
design/showcase.html           # Interactive HTML showing all design tokens
design/design_showcase.png     # Full-page screenshot of showcase.html
```

### 8. HTML Integration

The project's base HTML template must include:

```html
<link rel="icon" type="image/x-icon" href="/static/favicons/favicon.ico">
<link rel="icon" type="image/svg+xml" sizes="32x32" href="/static/favicons/favicon-32.svg">
<link rel="icon" type="image/svg+xml" sizes="16x16" href="/static/favicons/favicon-16.svg">
<link rel="icon" type="image/svg+xml" sizes="192x192" href="/static/favicons/favicon-192.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/static/favicons/apple-touch-icon.png">
<link rel="manifest" href="/static/favicons/site.webmanifest">
<meta property="og:image" content="/static/og_image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
```

## Generation Process

### Prerequisites

Check available tools before starting:

| Tool | Purpose | Fallback |
|------|---------|----------|
| `rsvg-convert` | SVG to PNG | `inkscape --export-type=png` or `resvg` |
| Pillow (`pip3 install Pillow`) | ICO generation, image composition | `icotool` from `icoutils` |
| Playwright (MCP or CLI) | HTML to PNG (OG image, showcase) | `wkhtmltoimage` or manual screenshot |
| Local HTTP server | Serve HTML for Playwright | `python3 -m http.server` |

### Step-by-step

1. **Read DESIGN_SYSTEM.md** — extract tagline, brand colors, dark bg color, font family
2. **Inventory existing SVGs** — glob `design/**/*.svg` to see what exists
3. **Generate missing SVGs** — create icon variants (strip text from square logos), missing favicon sizes
4. **Render all PNGs** — use `rsvg-convert -w {size} -h {size} input.svg -o output.png`
5. **Create favicon.ico** — Pillow: open 16/32/48 PNGs, save with `format='ICO'`, `append_images`
6. **Create apple-touch-icon** — render 192px favicon SVG at 180x180
7. **Create OG image** — build a minimal HTML file (1200x630 viewport, dark bg, centered logo SVG inline, project name + tagline below), serve locally, screenshot with Playwright
8. **Create design showcase PNG** — serve `showcase.html` locally, full-page screenshot with Playwright
9. **Write site.webmanifest** — JSON with name, short_name, description (tagline), 192+512 PNG icons, theme_color and background_color from dark bg
10. **Copy deployable assets** — SVGs, PNGs, ICO, manifest to `assets/static/favicons/`; OG image to `assets/static/`
11. **Update base template** — add favicon, apple-touch-icon, manifest, and OG meta tags
12. **Clean up** — remove temp HTML files used for rendering

### site.webmanifest Template

```json
{
  "name": "{Project Name}",
  "short_name": "{Project Name}",
  "description": "{tagline from DESIGN_SYSTEM.md}",
  "icons": [
    { "src": "/static/favicons/favicon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/static/favicons/favicon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "{--bg-primary dark value}",
  "background_color": "{--bg-primary dark value}",
  "display": "standalone"
}
```

### OG Image HTML Template

Minimal self-contained HTML. Key properties:
- Viewport: exactly 1200x630
- Background: project's `--bg-primary` dark value
- Logo mark SVG inlined (not referenced) — no external deps
- Project name: largest text, `font-weight: 700`
- Tagline below: muted color, smaller
- Subtle background texture (grid lines, radial glow) optional but recommended
- Import the project font via Google Fonts `@import`

### Pillow ICO Generation

```python
from PIL import Image
img16 = Image.open('favicon-16.png')
img32 = Image.open('favicon-32.png')
img48 = Image.open('favicon-48.png')
img48.save('favicon.ico', format='ICO',
           append_images=[img32, img16],
           sizes=[(16, 16), (32, 32), (48, 48)])
```

## Audit Mode

When auditing an existing project, check each item in the inventory. Report as:

```
[OK]   design/logos/icon_dark.svg
[MISS] design/logos/icon_light.svg
[OK]   assets/static/favicons/favicon.ico
[MISS] assets/static/favicons/apple-touch-icon.png
...
```

Then generate only the missing items. Never modify existing SVG source files.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| favicon.ico with only one size | Must include 16+32+48 via `append_images` |
| apple-touch-icon with transparency | Use opaque dark background; iOS fills transparency with white |
| OG image referencing external files | Inline the SVG logo; external refs break in Playwright |
| Light icon using dark-mode brand color | Light variant must use the light-mode color value |
| Favicon SVGs not simplified at small sizes | 16px favicon needs thicker strokes, fewer details than 512px |
| Pillow installed for wrong Python version | Check `python3 -c "from PIL import Image"` before using |
| Missing PNG copies in deploy directory | Both `design/` (source) and `assets/static/` (deploy) need copies |

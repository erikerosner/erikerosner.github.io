# ErikRosner.com

A one-page personal site: plain static HTML, CSS and JavaScript. There is no framework, no npm, and nothing to compile. GitHub Pages can serve it as-is.

## Files

| File | What it is |
|---|---|
| `index.html` | The page: markup, component CSS and the theme/clue script |
| `tokens.css` | **Every adjustable measurement** (type sizes, line heights, tracking, column width, gaps, padding, hint icon, hover line, phone overrides) |
| `themes.csv` | **Source of truth for themes:** one row per palette with its two colors, name font, and the clue + icon for each side. Mirrors the Figma variables and theme frames |
| `assets/phosphor-icons.svg` | Icon sprite generated from `themes.csv` (don't edit by hand) |
| `scripts/update_icons.py` | Rebuilds the icon sprite and the PenNib favicon (`assets/favicon.svg`) |
| `scripts/type_scale.py` | Regenerates the fluid type/space scale in `tokens.css` |
| `scripts/check.py` | Validates everything (run before publishing) |
| `scripts/build.py` | Runs the checks, then copies the public files into `_site/` |
| `DEPLOY.md` | Click-by-click guide for the first launch (GitHub Pages + GoDaddy DNS) and later updates |
| `.github/workflows/deploy.yml` | Publishes `_site/` to GitHub Pages on every push to `main` |

## Preview locally

The page loads `themes.csv` with `fetch`, so it needs a local web server; opening the file directly from Finder won't work.

```bash
python3 -m http.server 4791
```

Then open http://localhost:4791

## Themes (`themes.csv`)

One row per palette, in the same order as the Figma file *Portfolio homepage → 🌐 website* (frames 01–26). Each palette is a variable group in Figma's **Themes** collection with the same values: `color_a`, `color_b`, `hover_a`, `hover_b`, `hint_a` / `hint_b` (= `clue_a` / `clue_b` here), `icon_a`, `icon_b`, `name_font` and `name_weight`. The `_a` values are the palette's first appearance (frames 01–13), and the `_b` values its second (frames 14–26). Each palette's name matches its Figma variable group, and `color_a` / `color_b` match the Figma variables `<palette>/color_a` and `<palette>/color_b`.

| Column | What it does |
|---|---|
| `palette` | The palette's name, as in Figma (e.g. `UCSC Slugs`) |
| `live` | `1` = on the site, `0` = kept in the file but not shown (e.g. a palette still being written) |
| `color_a`, `color_b` | The two colors. **color_a is always the background the first time the palette appears** (round 1, Figma frames 01–13), with `color_b` text; the second time (round 2, frames 14–26) they swap: background `color_b`, text `color_a` |
| `hover_a`, `hover_b` | The hover color on side a (background `color_a`) and side b (background `color_b`), so each can be tuned for contrast against its own background. Used for the body links' underline, the name's drawn underline, the clue icon while hovered, and the clue text. Blank = that side's text color. Match the Figma variables `<palette>/hover_a` and `hover_b` |
| `name_font`, `name_weight`, `name_size` | The font for "Erik Rosner" on both sides (see below) |
| `clue_a`, `icon_a` | Clue and icon for side a (round 1, background `color_a`) |
| `clue_b`, `icon_b` | Clue and icon for side b (round 2, background `color_b`) |

Click order: round 1 goes down the live rows playing side a, then round 2 goes down them again playing side b. With all 13 palettes live that's 26 steps, the same as Figma frames 01–26. Row order = click order. Add, remove or reorder rows freely; the cycle length follows.

- Icons use the Phosphor React name (e.g. `PawPrintIcon`, see https://phosphoricons.com). After changing any icon, run `python3 scripts/update_icons.py`. That adds the icon to `assets/phosphor-icons.svg` and stamps a new version into `index.html` (`ICON_SPRITE = '…svg?v=…'`), so browsers load the new file instead of a cached old one. Until you run it, the new icon shows up blank, and `python3 scripts/check.py` names the row that's missing.
- The words of links and the name stay the text color; only the lines, the clue icon (on hover) and the clue text use the hover color. The custom cursor uses the text color for now.
- The icon always shows the current theme's icon. The clue text only appears while the icon is hovered (or focused with the keyboard).
- Older clue options (five per side) are kept in `_archive/before-themes-csv-2026-11-09/hints.csv`.

## Contrast: recommended color changes (not applied)

Recorded Nov 10, 2026. The launch keeps the colors as they are in Figma; these are the suggested fixes for later. Each one keeps the original hue and changes only lightness, by the smallest amount that meets the guideline: **4.5:1** for text (the clue text and the body copy), **3:1** for lines and icons. Contrast is against that side's background.

**Hover colors below 3:1** (clue text, link underlines, name underline, icon on hover):

| Step | Variable | Now | For text (4.5:1) | Lines only (3:1) |
|---|---|---|---|---|
| 3 | Wave FC `hover_a` | #2ECFE5 · 2.63 | #E3F9FC (only lighter works on this magenta) | #60DBEB |
| 5 | Torrey Pines HS `hover_a` | #E0000F · 2.63 | #9D000B | #CF000E |
| 8 | Hornets `hover_a` | #7B5CE5 · 2.61 | #4E24DC | #704FE3 |
| 13 | Seattle `hover_a` | #FFFFFF · 2.12 | #105025 deep green, or #004D4D teal | #5F5F5F |
| 16 | Wave FC `hover_b` | #0092A6 · 1.93 | #00545F | #007080 |
| 17 | State of North Carolina `hover_b` | #EB1793 · 2.60 | #A80E68 | #D81386 |
| 20 | Liverpool FC `hover_b` | #FFA200 · 2.92 | #FFDDA1 | #FFA60A |
| 25 | LCAD `hover_b` | #E517C3 · 1.84 | #7D0D6A | #AA1191 |

Also between 3:1 and 4.5:1 (fine for lines and icons, light for clue text): UCSC `hover_a` (step 1), NC `hover_a` (4), Liverpool `hover_a` (7), Padres `hover_a` (11), San Diego FC `hover_b` (15).

**Body text below 4.5:1** (the two colors swap between sides, so one change fixes both):

| Palette | Now | Recommended | Result | Knock-on change |
|---|---|---|---|---|
| Panthers | #E0E0E0 / #008BD1 · 2.83 | `color_b` → #00699F | 4.52 | `hover_b` black would drop to 3.52 on the new blue, so also set `hover_b` → #FFFFFF (5.96) |
| Wolfpack + Aztecs | #D90000 / #000000 · 3.95 | `color_a` → #EB0000 | 4.53 | none (`hover_a` white stays 4.63) |

With all of these applied, every side passes for both body text and clue text. To apply: change the values in Figma, then sync `themes.csv` (or edit it directly) and run `python3 scripts/build.py`.

## Name fonts and weights

Each row sets the font for "Erik Rosner" on both color versions of that palette:

| Column | What to type |
|---|---|
| `name_font` | The family name exactly as fonts.google.com spells it, e.g. `MuseoModerno`. Don't put the weight here. |
| `name_weight` | A weight the font actually has (see **Styles** on its Google Fonts page): 100 thin, 200 extra-light, 300 light, 400 regular, 500 medium, 600 semibold, 700 bold, 800 extra-bold, 900 black. Blank = 400. |
| `name_size` | Size multiplier to even out how big fonts look (1 = normal, 0.85 = 15% smaller). |

Example: bold Redaction 50 on Torrey Pines HS → `Torrey Pines HS,…,Redaction 50,700,1.1,…`.

`python3 scripts/check.py` asks Google Fonts whether every font and weight exists and fails if one doesn't, so a typo can't be published. On the live page, a broken font only affects its own theme; the others still load.

Body text weights are in `tokens.css`: `--font-weight-body` (columns, links, clue) and `--font-weight-intro`. Google Sans Flex supports any weight from 100 to 1000, and only the weights you set are downloaded.

## Layout and interactions

Built from the Figma frame *Portfolio homepage → website → desktop* (node 2306:416).

- **Intro:** one sentence, left-aligned, with the name inline at the start. The intro is the page's `<h1>`.
- **Body:** two columns that sit at the right edge on desktop. Each column's width comes from characters per line (`--body-cpl`), so the line length stays readable at every size. When two columns no longer fit side by side, they stack into one column automatically; on phones (≤768px) that column sits flush left.
- **Links:** every link opens in a new tab: merch (Ridgeway Goods), lessons (Koalendar), Rally, design work (Dribbble), "Let’s talk" (the Typeform) and Instagram. "a short email" is plain text until the newsletter signup is ready; the comment above the columns in `index.html` shows how to link it.
- **Contact:** inline in the right column. The email stays plain text.
- **Two theme buttons:** clicking **the name** or **the clue icon** moves to the next theme. Both update together: colors, the name font and the icon. The name gets the hand-drawn underline on hover and keyboard focus; the icon gets the magnetic pull (below).
- **Body links:** Osmo Supply's "Underline Link Animation" (the alt version), pure CSS. Links are underlined at rest. On hover, the line slides away to the right, then a fresh one draws in from the left 340ms later; on leave it plays back. Keyboard focus plays the same animation. Every link carries `data-underline-link="alt"`, and the checker fails if one is missing. Osmo draws the two lines with `::before`/`::after`, which only underline the first row of a link that wraps. Here they are two background layers instead (animated with `@property`), so wrapped links are underlined on every row. The curve and thickness are Osmo's; the timing is rounded to the site's Fibonacci ladder (890ms, 340ms delay; Osmo uses 735ms and 300ms). All in the `--link-underline-*` tokens. With reduced motion, the lines swap instantly. Browsers without `@property` (very old ones) still show the underline; it just doesn't animate.
- **Name hover:** Osmo Supply's "Draw Random Underline". On hover or keyboard focus, one of six hand-drawn lines draws in under the name, then draws out when the pointer leaves. Each hover uses the next of the six, starting at a random one. It uses GSAP 3.15.0 and its DrawSVG plugin from jsDelivr, pinned to that exact version. The line sits in an overlay so the text never moves. With reduced motion, the lines appear without animating. If GSAP can't load, the name falls back to a plain underline. To add your own lines, draw them left to right with Figma's Pencil tool and add the SVG to `svgVariants` in `index.html`.
- **Clue icon:** sits in a padded button (`--hint-hit-area`, 0.5em on each side) for a bigger hover/click/tap area. An equal negative margin keeps the icon exactly where it was. The button has Osmo Supply's "Magnetic Hover Effect": it drifts toward the pointer, and the icon inside drifts a little further, then springs back when the pointer leaves. The strength is set by `data-magnetic-strength="50"` and `data-magnetic-strength-inner="25"` (Osmo's defaults) on the button in `index.html`. For a gentler pull, try 20 and 10. The clue sits in its own container (`data-magnetic-follow="hint-button"`) that gets the button's exact movement, so the clue travels and springs back with the icon. The pull is still measured on the icon button alone, so it aims where your pointer is. Osmo's original turns the effect off on windows 991px wide or narrower to skip phones and tablets, but that also turned it off in narrow desktop windows. Here, each pointer move checks what is pointing instead: a mouse or a pen (such as a Wacom) gets the effect at any window size, and touch never does. It's off with reduced motion. The icon has no underline: it changes to the hover color, and keyboard focus shows a thin ring around it.
- **Custom cursor:** Osmo Supply's "Velocity Based Custom Cursor" (no libraries). A pixel arrow replaces the browser's cursor and becomes a pointing hand over any link or button (or any element with `data-cursor`). It tilts up to 70° in the direction you move the mouse sideways, then settles. Its outline is the theme's text color (for now; switching it to the hover color is one line in `index.html`) and its fill is the background color, and both fade with the theme. It only takes over once the mouse moves, so without JavaScript you keep the normal cursor. It's off on touch screens and doesn't tilt with reduced motion. Sizes: `--cursor-size` (1.74rem arrow) and `--cursor-size-pointer` (2.175rem hand), 13% smaller than Osmo's.
- **Clue:** sits to the right of the icon, its first line level with the icon (Figma comps); longer clues wrap below. Hidden by default. While the icon is hovered or focused, the clue fades and slides in (ease-out), and fades and slides back out (ease-in) when the pointer leaves. With the system's reduced-motion setting, it fades without moving. Its space is always reserved, so showing it never moves anything. On touch screens, a tap changes the theme; most phones then keep the clue showing until you tap elsewhere. Nothing essential depends on hover.
- **Page:** the content is aligned to the top, so when a theme changes the name font or the clue length, the content only grows or shrinks downward and the name stays under your pointer. To still look centered like the mockup, the script measures every theme at the current window size and sets the top offset so the tallest one sits centered (recalculated on resize and when fonts finish loading). Phones simply start at the top. There is no separate footer.

## Design tokens (`tokens.css`)

**One fluid modular scale drives every text size and vertical space**, modeled on lifeofpai.com. `--step-N` = body size × ratio^N. Each step grows with the window **width** (720 → 1760px, matching the reference) and with the window **height** (480 → 1130px), and uses whichever is smaller. Wide-but-short windows (laptops) therefore shrink everything in proportion, and the page fits without scrolling on desktop windows from 1280×640 up.

| | small window | 1440×789 | 1920×963 | large screen |
|---|---|---|---|---|
| `--step-0` body, links, clue | 16px | ≈19.7px | ≈21.9px | 24px |
| `--step-3` intro | 32px | ≈49px | ≈59px | 68px |

The name is the intro size × `--name-to-intro` (1.15) × the theme's `name_size` from `themes.csv`.

The steps are generated. To change them, edit the numbers at the top of `scripts/type_scale.py` (width range, height range, body size and ratio at each end), then run `python3 scripts/type_scale.py`. It rewrites the block between `scale:start` and `scale:end`. Each step mixes rem with vw/vh, so browser zoom and the reader's text-size setting still work. Phones in portrait still scroll, because the intro wraps to several lines.

| What | Tokens |
|---|---|
| Scale | `--step-minus-1` … `--step-5` (generated) |
| Font weights | `--font-weight-body` (400), `--font-weight-intro` (400); name weights are `name_weight` in `themes.csv` |
| Text sizes | `--font-size-intro` (step 3), `--name-to-intro` (1.15), `--font-size-name` (intro × that), `--font-size-body` (step 0), `--font-size-hint` (step 0) |
| Line heights | `--line-height-name` (= 1 × the intro size, shorter than the intro's row, so name fonts never move the baseline or the row height), `--line-height-intro` (1.3), `--line-height-body` (1.33), `--line-height-hint` (1.33) |
| Tracking | `--letter-spacing-name`, `--letter-spacing-intro`, `--letter-spacing-body`, `--letter-spacing-hint` |
| Line lengths | `--intro-max-width` (82%); columns: `--body-cpl` (36 = lines average ≈34.5 characters, longest 38), `--char-width` (0.475em, Google Sans Flex's average character), `--body-measure` (the two multiplied) |
| Page padding | `--page-padding-top` and `--page-padding-bottom` (10vh), `--page-padding-x` (9.5vw) |
| Placement | `--visual-center` (1 = top-aligned at the spot where the tallest theme is centered; 0 = plain top), `--columns-align` (`end` = right edge; `start` = left) |
| Spacing | `--space-intro-body` (step 3, intro → columns), `--space-column-gap` (step 2), `--space-paragraph` (step 0), `--space-icon-hint` (0.45em, icon → clue, side by side) |
| Hint | `--hint-icon-size` (1.5em), `--hint-hit-area` (0.5em of padding around the icon), `--hint-shift` (0.5em slide), `--font-style-hint`. Icon weight: `python3 scripts/update_icons.py --weight light` |
| Body-link underline | `--link-underline-thickness` (0.0625em), `--link-underline-duration` (890ms), `--link-underline-delay` (340ms), `--link-underline-ease` (Osmo's cubic-bezier) |
| Name hover underline | `--underline-height` (0.42em; the stroke is a quarter of it), `--underline-offset` (0.32em: the deepest the name's line sits below the baseline), `--underline-ink-gap` (0.18 × size below the lowest ink of the name), `--underline-duration` (550ms), `--underline-ease` (`power2.inOut`) |
| Cursor | `--cursor-size` (1.74rem arrow), `--cursor-size-pointer` (2.175rem hand) |
| Motion | All timings are whole milliseconds on a Fibonacci ladder (×10: 130, 210, 340, 550, 890, 1440). `--theme-duration` (340ms) and `--theme-ease` (ease-in-out) for the color change on click, combined in `--theme-transition`; `--hint-reveal-duration` (340ms); `--page-reveal-duration` (340ms, first-load fade-in) |
| Safe areas | `--safe-top`, `--safe-right`, `--safe-bottom`, `--safe-left` |
| Phones (≤768px) | page padding 10vh / 7vw / 4vh, content starts at the top, intro full width, single column flush left |

Why not `ch` for the columns? CSS's `ch` is the width of a zero, which in Google Sans Flex is much wider than an average letter (`34ch` came out at about 46 real characters per line). If you change the body font, re-measure `--char-width`.

## Before publishing

```bash
python3 scripts/build.py
```

This runs `scripts/check.py`, which validates:

- `themes.csv`: its columns, hex colors (including `hover_a` / `hover_b`), `live` values, that every live palette has a clue and icon for both sides (warns over 12 words or on a repeated clue), and that every icon exists in the sprite
- that the intro and the four body paragraphs match exactly, “Let’s talk” goes to the Typeform, “Instagram” goes to the Instagram profile, and the email is plain text
- that both theme buttons exist, the page has a single `<main>`, every link opens safely in a new tab, and no sizes are hard-coded outside `tokens.css`

Any `#` placeholder link shows up as a warning until it has a real URL.

## Deployment

**First launch:** follow [DEPLOY.md](DEPLOY.md), a click-by-click guide (GitHub Desktop, GitHub Pages and GoDaddy DNS). The GitHub Actions workflow in `.github/workflows/deploy.yml` does the publishing. It needs no Node or `package-lock.json`.

In short:

1. Run `python3 scripts/build.py`, then turn the folder into a Git repository with GitHub Desktop (the `.gitignore` keeps reference images, briefs, `_archive/` and `_site/` out).
2. Publish it as the public repository `erikrosner.github.io`.
3. Repo → Settings → Pages → **Source: GitHub Actions**, re-run **Deploy ErikRosner.com**, and test `https://erikrosner.github.io/`.
4. Verify the domain (account Settings → Pages), then set the repo's custom domain to `erikrosner.com`.
5. GoDaddy DNS: four GitHub A records on `@`, `www` CNAME → `erikrosner.github.io`. Keep the MX/TXT email records. Then enforce HTTPS, and retire Webflow last.

**Later updates:** edit, run `python3 scripts/build.py`, then commit and push in GitHub Desktop. The site redeploys in about a minute.

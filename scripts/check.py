#!/usr/bin/env python3
"""Validate the site before publishing:  python3 scripts/check.py

Checks themes.csv, the icon sprite, index.html and tokens.css against the
brief's rules and the Figma mockup's copy. Exits non-zero (and the GitHub deploy stops) if anything is wrong.
"""
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

from sitedata import ROOT, SIDES, SPRITE, THEMES, icon_file_name, read_csv, sprite_ref

errors, warnings = [], []
HEX = re.compile(r"^#?([0-9a-f]{3}|[0-9a-f]{6})$", re.I)

TYPEFORM = "https://form.typeform.com/to/eKoB51ql"
INSTAGRAM = "https://www.instagram.com/erikrosner/"
EMAIL = "hi@erikrosner.com"
INTRO = "Erik Rosner is a designer and pickleball pro who makes thoughtful things where craft meets play."
PARAGRAPHS = [   # the body copy, in order (left column, then right column)
    "I make tees, hats and merch worth wearing for a handful of my own brands. Every week, I send out "
    "a short email with pickleball mindset, tactics and strategy you can use in your next match.",
    "I also design products, brand systems and identities for teams that care about the details.",
    "Ready to level up? I teach private and group pickleball lessons. Occasionally spotted in the wild at Rally in Charlotte.",
    f"Got a project or partnership in mind? Let’s talk. If you prefer to email, reach me at {EMAIL}.",
    "Behind-the-scenes lives on Instagram.",
]
REQUIRED_TOKENS = [
    "--step-0", "--step-2", "--step-3", "--font-weight-body", "--font-weight-intro",
    "--font-size-intro", "--font-size-name", "--name-to-intro", "--font-size-body", "--font-size-hint",
    "--line-height-name", "--line-height-intro", "--line-height-body", "--line-height-hint",
    "--letter-spacing-name", "--letter-spacing-intro", "--letter-spacing-body", "--letter-spacing-hint",
    "--intro-max-width", "--body-cpl", "--char-width", "--body-measure",
    "--page-padding-top", "--page-padding-x", "--page-padding-bottom",
    "--visual-center", "--columns-align", "--space-intro-body", "--space-column-gap", "--space-paragraph",
    "--space-icon-hint", "--hint-icon-size", "--hint-hit-area", "--hint-shift", "--hint-reveal-duration",
    "--underline-height", "--underline-offset", "--underline-ink-gap", "--underline-duration",
    "--underline-ease", "--link-underline-thickness", "--link-underline-duration",
    "--link-underline-delay", "--link-underline-ease",
    "--cursor-size", "--cursor-size-pointer",
]


# ---------- themes.csv ----------
# One row per palette (a Figma variable group). Side a (round 1, Figma frames 01–13) = background color_a;
# side b (round 2, frames 14–26) = background color_b. hover_a / hover_b = the hover color on each side.
COLUMNS = ["palette", "live", "color_a", "color_b", "hover_a", "hover_b", "name_font", "name_weight", "name_size",
           "clue_a", "icon_a", "clue_b", "icon_b"]
MAX_CLUE_WORDS = 12
themes = read_csv(THEMES)
with open(THEMES, encoding="utf-8-sig") as f:
    header = [h.strip().lower() for h in f.readline().split(",")]
for col in COLUMNS:
    if col not in header:
        errors.append(f"themes.csv: missing the {col!r} column")
sprite = SPRITE.read_text(encoding="utf-8") if SPRITE.exists() else ""
if not sprite:
    errors.append("assets/phosphor-icons.svg is missing — run: python3 scripts/update_icons.py")
names, shown = set(), {}
name_fonts = {}   # family -> set of weights used (live rows only)
live_count = 0
for i, row in enumerate(themes, start=2):
    name = row.get("palette", "")
    where = f"themes.csv row {i} ({name or 'no palette name'})"
    if not name:
        errors.append(f"{where}: palette is blank")
    if name.lower() in names:
        errors.append(f"{where}: duplicate palette name")
    names.add(name.lower())
    live = row.get("live", "1") or "1"
    if live not in ("0", "1"):
        errors.append(f"{where}: live must be 1 (on the site) or 0 (off), got {live!r}")
    for col in ("color_a", "color_b"):
        if not HEX.match(row.get(col, "")):
            errors.append(f"{where}: {col} must be a hex color, got {row.get(col)!r}")
    for col in ("hover_a", "hover_b"):    # blank = that side's text color
        if row.get(col) and not HEX.match(row[col]):
            errors.append(f"{where}: {col} must be a hex color or blank, got {row[col]!r}")
    for side in SIDES:
        icon = row.get(f"icon_{side}", "")
        if icon and sprite and f'id="ph-{icon_file_name(icon)}"' not in sprite:
            errors.append(f"{where}: icon_{side} {icon} is not in the sprite — run: python3 scripts/update_icons.py")
    if live == "0":
        warnings.append(f"{where}: live = 0, so it is not on the site")
        continue
    live_count += 1
    for side in SIDES:
        clue, icon = row.get(f"clue_{side}", ""), row.get(f"icon_{side}", "")
        words = len(clue.split())
        if not clue:
            errors.append(f"{where}: clue_{side} is empty")
        elif words > MAX_CLUE_WORDS:
            warnings.append(f"{where}: clue_{side} has {words} words (over {MAX_CLUE_WORDS}): {clue!r}")
        if not icon:
            errors.append(f"{where}: icon_{side} is empty")
        if clue in shown:
            warnings.append(f"{where}: clue_{side} is the same as {shown[clue]} ({clue!r})")
        shown.setdefault(clue, f"{where} clue_{side}")
    size = row.get("name_size", "")
    try:
        if size and not 0 < float(size) < 5:
            raise ValueError
    except ValueError:
        errors.append(f"{where}: name_size must be a number between 0 and 5, got {size!r}")
    if not row.get("name_font"):
        warnings.append(f"{where}: name_font is blank (falls back to Ballet)")
    weight = row.get("name_weight", "") or "400"
    if not (weight.isdigit() and 1 <= int(weight) <= 1000):
        errors.append(f"{where}: name_weight must be a number like 300, 400 or 700, got {weight!r}")
    else:
        name_fonts.setdefault(row.get("name_font") or "Ballet", set()).add(int(weight))
if not live_count:
    errors.append("themes.csv: no live rows")


# ---------- Google Fonts: does each name_font exist with the requested weights? ----------
def google_has(family, weights):
    """True/False from Google Fonts, or None if Google can't be reached (e.g. offline)."""
    q = urllib.parse.quote_plus(family)
    w = sorted(weights)
    url = f"https://fonts.googleapis.com/css2?family={q}" + ("" if w == [400] else ":wght@" + ";".join(map(str, w)))
    try:
        urllib.request.urlopen(url, timeout=15).close()
        return True
    except urllib.error.HTTPError:
        return False
    except Exception:
        return None


for family, weights in sorted(name_fonts.items()):
    found = google_has(family, weights)
    if found is None:
        warnings.append("could not reach Google Fonts — name_font / name_weight not verified")
        break
    if not found:
        if google_has(family, {400}):
            errors.append(f"themes.csv: {family!r} does not come in weight(s) "
                          f"{', '.join(map(str, sorted(weights)))} — see 'Styles' on fonts.google.com")
        else:
            errors.append(f"themes.csv: name_font {family!r} is not on Google Fonts — check the spelling")


# ---------- index.html ----------
class Page(HTMLParser):
    """Collects the body's top-level sections, every link (with its text), the intro (h1)
    text, every paragraph's text, and the ids of the two theme buttons."""
    VOID = ("meta", "link", "br", "img", "input", "use")

    def __init__(self):
        super().__init__()
        self.stack, self.body_children, self.links, self.buttons = [], [], [], []
        self.paragraphs, self.intro, self.open = [], "", []   # open = text buffers being filled

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.stack and self.stack[-1] == "body" and tag not in ("script", "noscript") and a.get("class") != "cursor":
            self.body_children.append(tag)
        if tag == "a":
            self.links.append([a, ""])
            self.open.append(("a", self.links[-1]))
        if tag == "button":
            self.buttons.append(a.get("id", ""))
        if tag == "h1":
            self.open.append(("h1", None))
        if tag == "p" and a.get("class") != "hint-text":
            self.paragraphs.append([""])
            self.open.append(("p", self.paragraphs[-1]))
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        while self.stack:
            if self.stack.pop() == tag:
                break
        for i in range(len(self.open) - 1, -1, -1):
            if self.open[i][0] == tag:
                del self.open[i]
                break

    def handle_data(self, data):
        for kind, buf in self.open:
            if kind == "h1":
                self.intro += data
            elif kind == "a":
                buf[1] += data
            else:
                buf[0] += data


html = (ROOT / "index.html").read_text(encoding="utf-8")
page = Page()
page.feed(html)
squash = lambda s: re.sub(r"\s+", " ", s).strip()

if page.body_children != ["main"]:
    errors.append(f"index.html: body must hold exactly one <main> (plus the custom cursor), found {page.body_children}")
if squash(page.intro) != INTRO:
    errors.append(f"index.html: intro (h1) does not match the mockup: {squash(page.intro)!r}")
found = [squash(p[0]) for p in page.paragraphs]
if found != PARAGRAPHS:
    errors.append("index.html: body copy does not match the mockup:\n    " + "\n    ".join(found))
for needed in ("wordmark", "hint-button"):
    if needed not in page.buttons:
        errors.append(f"index.html: theme button #{needed} is missing (the name and the clue icon both change the theme)")
for label, url in (("Let’s talk", TYPEFORM), ("Instagram", INSTAGRAM)):
    found_link = [a for a, text in page.links if squash(text) == label]
    if not found_link or found_link[0].get("href") != url:
        errors.append(f"index.html: “{label}” must link to {url}")
if EMAIL not in html:
    errors.append(f"index.html: the email {EMAIL} is missing")
if "linkedin" in html.lower():
    errors.append("index.html: LinkedIn should be removed")
if "mailto:" in html.lower():
    errors.append("index.html: the email must be plain text (no mailto:)")
for a, text in page.links:
    href = a.get("href", "")
    if a.get("data-underline-link") != "alt":
        errors.append(f'index.html: link {squash(text)!r} needs data-underline-link="alt" (the body-link underline)')
    if href.startswith("#"):
        warnings.append(f"index.html: placeholder link {squash(text)!r} → {href!r} — replace before launch")
        continue
    # Every link opens in a new tab, safely.
    rel = set((a.get("rel") or "").split())
    if a.get("target") != "_blank" or not {"noopener", "noreferrer"} <= rel:
        errors.append(f'index.html: link {href} needs target="_blank" rel="noopener noreferrer"')
# Third-party scripts must name an exact version (e.g. gsap@3.15.0), so the site never changes on its own.
for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
    if "cdn.jsdelivr.net" in src and not re.search(r"@\d+\.\d+\.\d+/", src):
        errors.append(f"index.html: script {src} must pin an exact version like @3.15.0")
if not re.search(r'id="hint-button"[^>]*data-magnetic-strength="\d+(\.\d+)?"', html, re.S) or "data-magnetic-inner-target" not in html:
    errors.append("index.html: the clue icon needs data-magnetic-strength (button) and data-magnetic-inner-target (icon wrapper)")
if 'class="cursor"' not in html or 'cursor-inner regular' not in html or 'cursor-inner pointer' not in html:
    errors.append('index.html: the custom cursor (<div class="cursor"> with the regular and pointer SVGs) is missing')
if 'data-magnetic-follow="hint-button"' not in html:
    errors.append('index.html: the clue container needs data-magnetic-follow="hint-button" (it moves with the icon)')
if "gsap.min.js" not in html or "DrawSVGPlugin.min.js" not in html:
    errors.append("index.html: GSAP and DrawSVGPlugin are needed for the hover underline")
if sprite and sprite_ref() not in html:
    errors.append("index.html: the icon sprite changed but its version in ICON_SPRITE is out of date "
                  "(browsers would keep showing old icons) — run: python3 scripts/update_icons.py")
if 'href="tokens.css"' not in html:
    errors.append("index.html: tokens.css is not linked")

# Component CSS should read sizes from tokens, not hard-code them.
style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
for prop in ("font-size", "line-height", "letter-spacing", "gap", "column-gap", "row-gap"):
    for m in re.finditer(rf"(?<![-\w]){prop}\s*:\s*([^;]+);", style):
        val = m.group(1).strip()
        if "var(" not in val and val not in ("inherit", "0", "normal"):
            errors.append(f"index.html <style>: {prop}: {val} is hard-coded — move it to tokens.css")

# ---------- tokens.css ----------
tokens = (ROOT / "tokens.css").read_text(encoding="utf-8")
for t in REQUIRED_TOKENS:
    if not re.search(rf"{re.escape(t)}\s*:", tokens):
        errors.append(f"tokens.css: missing {t}")

# ---------- report ----------
for w in warnings:
    print("warning:", w)
for e in errors:
    print("ERROR:", e)
print(f"\n{live_count} live palettes ({live_count * 2} theme steps) of {len(themes)} in themes.csv, "
      f"{sprite.count('<symbol')} icons — {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)

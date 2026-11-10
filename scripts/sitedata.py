"""Shared helpers for the site scripts (no third-party packages needed)."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes.csv"      # one row per palette: colors, name font, side a + side b clue and icon
SPRITE = ROOT / "assets" / "phosphor-icons.svg"
SIDES = ("a", "b")
FALLBACK_ICON = "sparkle"          # shown if a theme has no icon

# The page asks for the sprite as "assets/phosphor-icons.svg?v=<first 8 characters of its SHA-1>",
# so browsers fetch a fresh copy whenever the icons change instead of reusing a cached old one.
SPRITE_REF = re.compile(r"const ICON_SPRITE = 'assets/phosphor-icons\.svg(?:\?v=[0-9a-f]*)?';")


def sprite_version():
    import hashlib
    return hashlib.sha1(SPRITE.read_bytes()).hexdigest()[:8]


def sprite_ref():
    return f"const ICON_SPRITE = 'assets/phosphor-icons.svg?v={sprite_version()}';"


# Phosphor icons come from the official @phosphor-icons/core package, pinned.
PHOSPHOR_VERSION = "2.1.1"


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in rows
            if any((v or "").strip() for v in r.values())]


def icon_file_name(react_name):
    """'UsersThreeIcon' -> 'users-three' (the file name inside @phosphor-icons/core)."""
    name = re.sub(r"Icon$", "", react_name.strip())
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def theme_rows():
    return read_csv(THEMES)


def used_icons():
    """Every icon named in themes.csv (live or not, so switching a row on needs no rebuild) + the fallback."""
    icons = {FALLBACK_ICON}
    for row in theme_rows():
        for side in SIDES:
            if row.get(f"icon_{side}"):
                icons.add(icon_file_name(row[f"icon_{side}"]))
    return sorted(icons)

#!/usr/bin/env python3
"""Stage the publishable site into _site/:  python3 scripts/build.py

The site is plain static HTML/CSS/JS — nothing is compiled. This only copies the files
visitors need (and nothing else: no reference images, briefs or scripts) after running
the checks. GitHub Actions runs the same command and publishes _site/ to GitHub Pages.
"""
import shutil
import subprocess
import sys

from sitedata import ROOT

PUBLISH = ["index.html", "tokens.css", "themes.csv", "assets", "CNAME"]
OUT = ROOT / "_site"

if subprocess.call([sys.executable, str(ROOT / "scripts" / "check.py")]) != 0:
    sys.exit("Checks failed — nothing was built.")

shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()
for name in PUBLISH:
    src = ROOT / name
    if not src.exists():
        continue
    if src.is_dir():
        shutil.copytree(src, OUT / name)
    else:
        shutil.copy2(src, OUT / name)
(OUT / ".nojekyll").touch()

files = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file())
print(f"\nBuilt _site/ with {len(files)} files: {', '.join(files)}")

#!/usr/bin/env python3
"""
Add term name at the start of each <dd> in all glossary cluster files.

Before:
  <dt id="metalldach"><span itemprop="name">Metalldach</span></dt>
  <dd itemprop="description">
    Oberbegriff für alle ...

After:
  <dt id="metalldach"><span itemprop="name">Metalldach</span></dt>
  <dd itemprop="description">
    <strong class="dcr-gl-term-name">Metalldach</strong> — Oberbegriff für alle ...
"""

import pathlib, re

BASE = pathlib.Path(__file__).parent

FILES = [f for f in BASE.glob("glossary-*.html") if "parent" not in f.name]

# Regex: capture the term name from <dt>, then match opening of <dd>
# We process pairs: dt→dd
DT_PATTERN = re.compile(
    r'(<dt\b[^>]*>.*?<span itemprop="name">([^<]+)</span>.*?</dt>\s*)'
    r'(<dd itemprop="description">\s*)',
    re.DOTALL
)

def replacer(m):
    dt_block = m.group(1)          # full <dt>...</dt>
    term_name = m.group(2).strip() # the term text
    dd_open   = m.group(3)         # <dd itemprop="description">\n
    name_tag  = f'<strong class="dcr-gl-term-name">{term_name}</strong> — '
    return dt_block + dd_open + name_tag

# Also inject CSS for the term-name strong once, in the <style> block
CSS_INJECT = '.dcr-gl-term-name{font-weight:700;color:#1A1A1A}'
CSS_ANCHOR = '.dcr-gl-page__dl dd{'  # anchor point to insert before

changed = 0
for p in sorted(FILES):
    html = p.read_text(encoding='utf-8')

    # Skip if already patched
    if 'dcr-gl-term-name' in html:
        print(f'SKIP (already patched): {p.name}')
        continue

    # Inject CSS
    html = html.replace(CSS_ANCHOR, CSS_INJECT + '\n' + CSS_ANCHOR)

    # Insert term name into every dd
    new_html, n = DT_PATTERN.subn(replacer, html)
    p.write_text(new_html, encoding='utf-8')
    print(f'OK  {p.name}  ({n} terms)')
    changed += 1

print(f'\nPatched {changed} files.')

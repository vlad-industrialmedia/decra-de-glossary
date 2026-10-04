#!/usr/bin/env python3
"""
Fix <dd> format for files 07-12 which use plain <dt id="...">Term</dt> (no span/itemprop).

Before:
  <dt id="windlast">Windlast</dt>
  <dd>
    Die <strong>Windlast</strong> bezeichnet ...

After:
  <dt id="windlast">Windlast</dt>
  <dd>
    <strong class="dcr-gl-term-name">Windlast</strong> — Die <strong>Windlast</strong> bezeichnet ...
"""

import pathlib, re

BASE = pathlib.Path(__file__).parent

FILES = [
    BASE / "glossary-07-witterungsbestaendigkeit.html",
    BASE / "glossary-08-dachsanierung-lexikon.html",
    BASE / "glossary-09-dachdurchdringungen.html",
    BASE / "glossary-10-nachhaltigkeit.html",
    BASE / "glossary-11-garantie-und-normen.html",
    BASE / "glossary-12-dachdeckerterminologie.html",
]

# Match plain <dt id="...">Term</dt> followed by <dd>
DT_PLAIN = re.compile(
    r'(<dt\s+id="[^"]+">([^<]+)</dt>\s*)'
    r'(<dd>(\s*))',
    re.DOTALL
)

def replacer(m):
    dt_block  = m.group(1)        # full <dt ...>Term</dt>
    term_name = m.group(2).strip()
    dd_open   = m.group(3)        # <dd>
    whitespace = m.group(4)       # leading whitespace after <dd>
    name_tag  = f'<strong class="dcr-gl-term-name">{term_name}</strong> — '
    return dt_block + dd_open + whitespace + name_tag

# CSS to inject (same as the other script)
CSS_INJECT = '.dcr-gl-term-name{font-weight:700;color:#1A1A1A}'
CSS_ANCHOR = '.dcr-gl-page__dl dd{'

changed = 0
for p in FILES:
    if not p.exists():
        print(f'MISSING: {p.name}')
        continue

    html = p.read_text(encoding='utf-8')

    if 'class="dcr-gl-term-name"' in html:
        print(f'SKIP (already patched): {p.name}')
        continue

    # Inject CSS
    if CSS_ANCHOR in html:
        html = html.replace(CSS_ANCHOR, CSS_INJECT + '\n' + CSS_ANCHOR)

    new_html, n = DT_PLAIN.subn(replacer, html)
    p.write_text(new_html, encoding='utf-8')
    print(f'OK  {p.name}  ({n} terms)')
    changed += 1

print(f'\nPatched {changed} files.')

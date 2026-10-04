#!/usr/bin/env python3
"""
Fix wrapped glossary files:
1. Remove <base href="https://www.decra.de/">
2. Rewrite preview-nav links from filename.html → /de/glossar/... URLs
   (Vercel will rewrite these; same URLs work natively on decra.de)
"""
import pathlib, re

BASE = pathlib.Path(__file__).parent

# Map: filename → /de/glossar/ URL used in nav + canonical link
SLUG_MAP = [
    ("glossary-00-parent.html",               "/de/glossar/",                      "00 Übersicht"),
    ("glossary-01-dacheindeckungsarten.html",  "/de/glossar/dacheindeckungsarten/", "01 Dacheindeckung"),
    ("glossary-02-dachprofile.html",           "/de/glossar/dachprofile/",          "02 Profile"),
    ("glossary-03-material-und-legierungen.html", "/de/glossar/material-und-legierungen/", "03 Material"),
    ("glossary-04-steinschlag-und-farben.html","/de/glossar/steinschlag-und-farben/","04 Farben"),
    ("glossary-05-dachkonstruktion.html",      "/de/glossar/dachkonstruktion/",     "05 Konstruktion"),
    ("glossary-06-montage-und-installation.html","/de/glossar/montage-und-installation/","06 Montage"),
    ("glossary-07-witterungsbestaendigkeit.html","/de/glossar/witterungsbestaendigkeit/","07 Wetter"),
    ("glossary-08-dachsanierung-lexikon.html", "/de/glossar/dachsanierung-lexikon/","08 Sanierung"),
    ("glossary-09-dachdurchdringungen.html",   "/de/glossar/dachdurchdringungen/",  "09 Durchdringungen"),
    ("glossary-10-nachhaltigkeit.html",        "/de/glossar/nachhaltigkeit/",       "10 Nachhaltigkeit"),
    ("glossary-11-garantie-und-normen.html",   "/de/glossar/garantie-und-normen/",  "11 Garantie"),
    ("glossary-12-dachdeckerterminologie.html","/de/glossar/dachdeckerterminologie/","12 Terminologie"),
]

def build_nav(current_file):
    links = []
    for fname, url, label in SLUG_MAP:
        active = ' class="active"' if fname == current_file else ''
        links.append(f'<a href="{url}"{active}>{label}</a>')
    return (
        '<nav id="dcr-preview-nav">'
        '<span class="pnav-brand">▸ DECRA® Glossar Preview</span>'
        + "".join(links)
        + "</nav>"
    )

for fname, _url, _label in SLUG_MAP:
    p = BASE / fname
    if not p.exists():
        print(f"SKIP {fname}")
        continue

    html = p.read_text(encoding="utf-8")

    # 1. Remove <base href=...>
    html = re.sub(r'\n?<base href="[^"]*">\n?', '\n', html)

    # 2. Replace the entire preview nav block
    nav_html = build_nav(fname)
    html = re.sub(
        r'<nav id="dcr-preview-nav">.*?</nav>',
        nav_html,
        html,
        flags=re.DOTALL
    )

    p.write_text(html, encoding="utf-8")
    print(f"OK  {fname}")

print("Done.")

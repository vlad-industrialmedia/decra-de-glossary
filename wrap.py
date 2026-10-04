#!/usr/bin/env python3
"""
Wrap CMS fragment HTML files into standalone full-page HTML.
- Adds DOCTYPE, head (charset, viewport, base href, title)
- Inserts a floating preview nav bar for local browsing
- base href="https://www.decra.de/" makes all content links go to decra.de
"""

import os, re, pathlib

BASE = pathlib.Path(__file__).parent

CHAPTERS = [
    ("glossary-00-parent.html",              "Dachlexikon DECRA® – Übersicht"),
    ("glossary-01-dacheindeckungsarten.html", "Arten der Dacheindeckung – Dachlexikon DECRA®"),
    ("glossary-02-dachprofile.html",          "Dachprofile und -formen – Dachlexikon DECRA®"),
    ("glossary-03-material-und-legierungen.html", "Material und Stahllegierungen – Dachlexikon DECRA®"),
    ("glossary-04-steinschlag-und-farben.html",   "Steinschlag und Farben – Dachlexikon DECRA®"),
    ("glossary-05-dachkonstruktion.html",     "Dachkonstruktion – Dachlexikon DECRA®"),
    ("glossary-06-montage-und-installation.html", "Montage und Installation – Dachlexikon DECRA®"),
    ("glossary-07-witterungsbestaendigkeit.html", "Witterungsbeständigkeit – Dachlexikon DECRA®"),
    ("glossary-08-dachsanierung-lexikon.html","Dachsanierung – Dachlexikon DECRA®"),
    ("glossary-09-dachdurchdringungen.html",  "Dachdurchdringungen – Dachlexikon DECRA®"),
    ("glossary-10-nachhaltigkeit.html",       "Nachhaltigkeit – Dachlexikon DECRA®"),
    ("glossary-11-garantie-und-normen.html",  "Garantie und Normen – Dachlexikon DECRA®"),
    ("glossary-12-dachdeckerterminologie.html","Dachdeckerterminologie – Dachlexikon DECRA®"),
]

NAV_LABELS = [
    "00 Übersicht","01 Dacheindeckung","02 Profile","03 Material",
    "04 Farben","05 Konstruktion","06 Montage","07 Wetter",
    "08 Sanierung","09 Durchdringungen","10 Nachhaltigkeit",
    "11 Garantie","12 Terminologie",
]

PREVIEW_NAV_CSS = """
<style id="preview-nav-css">
#dcr-preview-nav{position:fixed;top:0;left:0;right:0;z-index:9999;
  background:#1A1A1A;border-bottom:2px solid #C8102E;
  padding:0 1rem;display:flex;align-items:center;gap:0;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:.7rem;overflow-x:auto;white-space:nowrap}
#dcr-preview-nav a{display:inline-block;color:rgba(255,255,255,.7);
  text-decoration:none;padding:.45rem .55rem;border-right:1px solid #333;
  transition:color .15s,background .15s}
#dcr-preview-nav a:hover,#dcr-preview-nav a.active{color:#fff;background:#C8102E}
#dcr-preview-nav .pnav-brand{color:#fff;font-weight:700;padding:.45rem .7rem .45rem 0;
  border-right:1px solid #333;margin-right:.25rem;white-space:nowrap;font-size:.72rem}
body{padding-top:34px}
</style>
"""

def build_preview_nav(current_file):
    links = []
    for i, (fname, _title) in enumerate(CHAPTERS):
        label = NAV_LABELS[i]
        active = ' class="active"' if fname == current_file else ''
        links.append(f'<a href="{fname}"{active}>{label}</a>')
    return (
        '<nav id="dcr-preview-nav">'
        '<span class="pnav-brand">▸ DECRA® Glossar Preview</span>'
        + "".join(links)
        + "</nav>"
    )

def wrap_file(src_file, title):
    content = src_file.read_text(encoding="utf-8")
    preview_nav = build_preview_nav(src_file.name)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<base href="https://www.decra.de/">
{PREVIEW_NAV_CSS}
</head>
<body>
{preview_nav}
{content}
</body>
</html>"""
    return html

for fname, title in CHAPTERS:
    src = BASE / fname
    if not src.exists():
        print(f"SKIP (not found): {fname}")
        continue
    wrapped = wrap_file(src, title)
    src.write_text(wrapped, encoding="utf-8")
    print(f"OK  {fname}")

# Create index.html that redirects to hub
index = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=glossary-00-parent.html">
<title>DECRA® Dachlexikon – Preview</title>
</head>
<body>
<p><a href="glossary-00-parent.html">→ Zum Dachlexikon</a></p>
</body>
</html>"""
(BASE / "index.html").write_text(index, encoding="utf-8")
print("OK  index.html")
print("Done.")

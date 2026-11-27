"""Builds the legal and support pages of the Helio site from one template.
Usage: python3 tools/build_legal.py .   (edit legal_en.py / legal_es.py, then run)"""
import sys, os, html

SITE = sys.argv[1]
SPRITE_SRC = open(os.path.join(SITE, "es/index.html")).read()
s0 = SPRITE_SRC.index("<!-- Icon sprite -->")
SPRITE = SPRITE_SRC[s0:SPRITE_SRC.index("</svg>\n\n<header", s0) + len("</svg>")]

UI = {
    "en": dict(skip="Skip to content", nav=[("Features", "#features"), ("Pricing", "#pricing"), ("FAQ", "#faq")],
               cta="Try free", other="Español", other_lang="es", home="", main="Main", foot="Footer",
               links=[("privacy", "Privacy"), ("terms", "Terms"), ("support", "Support")],
               updated="Effective", toc="On this page"),
    "es": dict(skip="Saltar al contenido", nav=[("Funciones", "#funciones"), ("Planes", "#planes"), ("Preguntas", "#preguntas")],
               cta="Prueba gratis", other="English", other_lang="en", home="es/", main="Principal", foot="Pie de página",
               links=[("privacy", "Privacidad"), ("terms", "Términos"), ("support", "Soporte")],
               updated="Vigente desde", toc="En esta página"),
}

TEMPLATE = """<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Helio</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://helio.harcode.com/{path}">
<link rel="alternate" hreflang="{lang}" href="https://helio.harcode.com/{path}">
<link rel="alternate" hreflang="{other_lang}" href="https://helio.harcode.com/{other_path}">
<meta name="theme-color" content="#F7F5F0">
<link rel="icon" href="{root}assets/icon.png">
<link rel="apple-touch-icon" href="{root}assets/icon.png">
<link rel="stylesheet" href="{root}assets/landing.css">
<link rel="stylesheet" href="{root}assets/legal.css">
</head>
<body>
<a class="skip" href="#main">{skip}</a>

{sprite}

<header class="top">
  <div class="wrap">
    <a class="brand" href="{root}{home}"><img src="{root}assets/icon.png" alt="" width="36" height="36">Helio</a>
    <nav aria-label="{main_label}">
{nav}
    </nav>
    <a class="lang" href="{root}{other_path}" hreflang="{other_lang}" lang="{other_lang}">{other}</a>
    <a class="btn btn-primary" href="{root}{home}#{dl}">{cta}</a>
  </div>
</header>

<main id="main" class="doc-wrap">
  <article class="doc">
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    {meta}
{body}
  </article>
</main>

<footer class="foot">
  <div class="wrap">
    <span>© 2026 Harcode · Helio</span>
    <nav aria-label="{foot_label}">
{foot}
      <a href="{root}{other_path}" hreflang="{other_lang}" lang="{other_lang}">{other}</a>
    </nav>
  </div>
</footer>
<script src="{root}assets/landing.js"></script>
</body>
</html>
"""

def build(lang, slug, title, kicker, desc, effective, body):
    ui = UI[lang]
    root = "../" if lang == "en" else "../../"
    path = f"{slug}/" if lang == "en" else f"es/{slug}/"
    other_path = f"es/{slug}/" if lang == "en" else f"{slug}/"
    nav = "\n".join(f'      <a href="{root}{ui["home"]}{h}">{t}</a>' for t, h in ui["nav"])
    foot = "\n".join(
        f'      <a href="{root}{ui["home"]}{s}/"' + (' aria-current="page"' if s == slug else "") + f">{t}</a>"
        for s, t in ui["links"])
    meta = f'<p class="meta">{ui["updated"]} {effective}</p>' if effective else ""
    out = TEMPLATE.format(lang=lang, title=title, desc=html.escape(desc), path=path, other_lang=ui["other_lang"],
                          other_path=other_path, root=root, skip=ui["skip"], sprite=SPRITE, home=ui["home"],
                          main_label=ui["main"], nav=nav, other=ui["other"], dl="download" if lang == "en" else "descargar",
                          cta=ui["cta"], kicker=kicker, meta=meta, body=body, foot_label=ui["foot"], foot=foot)
    dest = os.path.join(SITE, path, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w").write(out)
    print("wrote", dest)

sys.path.insert(0, os.path.dirname(__file__))
import legal_en, legal_es
for mod, lang in ((legal_en, "en"), (legal_es, "es")):
    for page in mod.PAGES:
        build(lang, **page)

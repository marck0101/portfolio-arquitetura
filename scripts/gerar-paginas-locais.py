"""
Gera as páginas de SEO local e os arquivos de SEO/GEO a partir de scripts/cidades.json.

Rodar da raiz do projeto:  python scripts/gerar-paginas-locais.py
Depois:                    npm run build:css   (se mudou classes Tailwind)

O que este script escreve:
  arquiteta-<slug>.html     uma página por cidade (texto e FAQ próprios)
  atendimento-regiao.html   cidades atendidas (todas até ~50 km de São Martinho)
  index.html                só o bloco JSON-LD entre <!-- JSONLD:inicio --> e <!-- JSONLD:fim -->
  *.html                    o <footer> de todas as páginas (mesmo rodapé em todo o site)
  sitemap.xml, robots.txt, llms.txt

Não edite à mão o que este script gera: a próxima execução sobrescreve.
"""

import html
import io
import json
import os
import re
import sys
from datetime import date
from urllib.parse import quote

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = json.load(io.open(os.path.join(RAIZ, "scripts", "cidades.json"), encoding="utf-8"))
SITE = DADOS["site"]
ESC = DADOS["escritorio"]
HOJE = date.today().isoformat()
ID_NEGOCIO = f"{SITE}/#business"
ID_PESSOA = f"{SITE}/#person"
COR = "#74424e"

e = html.escape  # texto -> HTML seguro


def escrever(nome, conteudo):
    with io.open(os.path.join(RAIZ, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)


def ler(nome):
    return io.open(os.path.join(RAIZ, nome), encoding="utf-8").read()


def jsonld(obj):
    texto = json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{texto}\n</script>'


def wa(msg):
    return f"https://wa.me/{ESC['whatsapp']}?text={quote(msg)}"


# ---------------------------------------------------------------------------
# Peças comuns (iguais às páginas feitas à mão)
# ---------------------------------------------------------------------------

def head(titulo, descricao, caminho, blocos_jsonld):
    url = f"{SITE}/{caminho}" if caminho else f"{SITE}/"
    ld = "\n  ".join(jsonld(b) for b in blocos_jsonld)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(descricao)}">
  <meta name="author" content="{e(ESC['arquiteta'])}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="{COR}">
  <meta name="geo.region" content="BR-RS">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="{e(ESC['nome'])}">
  <meta property="og:title" content="{e(titulo)}">
  <meta property="og:description" content="{e(descricao)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/img/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" media="print" onload="this.media='all'"
    href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@500;600;700&display=swap">
  <noscript><link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@500;600;700&display=swap"></noscript>
  <link rel="stylesheet" href="assets/css/tailwind.css">
  <link rel="stylesheet" href="assets/css/style.css">
  {ld}
  <!-- Google Tag Manager — só carrega com consentimento do visitante (LGPD).
       O banner de cookies fica em assets/js/script.js e chama window.loadAnalytics(). -->
  <script>
    (function (w, d, id) {{
      w.dataLayer = w.dataLayer || [];
      function gtag() {{ w.dataLayer.push(arguments); }}
      gtag("consent", "default", {{
        analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied"
      }});
      var loaded = false;
      function load() {{
        if (loaded) return; loaded = true;
        gtag("consent", "update", {{ analytics_storage: "granted" }});
        w.dataLayer.push({{ "gtm.start": new Date().getTime(), event: "gtm.js" }});
        var j = d.createElement("script"); j.async = true;
        j.src = "https://www.googletagmanager.com/gtm.js?id=" + id;
        d.head.appendChild(j);
      }}
      w.loadAnalytics = load;
      var consent = null;
      try {{ consent = localStorage.getItem("cookieConsent"); }} catch (e) {{}}
      if (consent === "granted") {{
        var idle = function () {{ (w.requestIdleCallback || function (cb) {{ setTimeout(cb, 1); }})(load, {{ timeout: 2000 }}); }};
        if (d.readyState === "complete") idle(); else w.addEventListener("load", idle);
      }}
    }})(window, document, "GTM-N4J8VN6Z");
  </script>
  <!-- End Google Tag Manager -->
</head>
"""


HEADER = f"""<body class="font-sans">

  <header class="sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-neutral-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <a href="index.html" class="font-display font-semibold text-lg tracking-tight">Taís Regina Müller</a>
      <nav class="hidden md:flex items-center gap-6 text-sm">
        <a href="index.html" class="hover:text-brand-500">Home</a>
        <a href="projetos.html" class="hover:text-brand-500">Projetos</a>
        <a href="servicos.html" class="hover:text-brand-500">Serviços</a>
        <a href="sobre.html" class="hover:text-brand-500">Sobre</a>
        <a href="contato.html" class="hover:text-brand-500">Contato</a>
      </nav>
      <div class="flex items-center gap-3">
        <a href="projetos.html"
          class="hidden sm:inline-flex px-4 py-2 rounded-lg border border-neutral-300 hover:bg-neutral-50">
          Ver portfólio</a>
        <a href="contato.html" class="px-4 py-2 rounded-lg text-white hover:opacity-90 transition"
          style="background-color: {COR};">
          Fale conosco
        </a>
        <button id="menuBtn" class="md:hidden text-2xl ml-2" aria-label="Abrir menu" aria-controls="mobileMenu"
          aria-expanded="false">☰</button>
      </div>
    </div>
    <div id="mobileMenu" class="md:hidden hidden border-t border-neutral-200">
      <div class="px-4 py-3 space-y-2">
        <a href="index.html" class="block">Home</a>
        <a href="projetos.html" class="block">Projetos</a>
        <a href="servicos.html" class="block">Serviços</a>
        <a href="sobre.html" class="block">Sobre</a>
        <a href="contato.html" class="block">Contato</a>
      </div>
    </div>
  </header>
"""


def footer():
    links = "\n".join(
        f'            <li><a href="arquiteta-{c["slug"]}.html" class="hover:text-brand-500">Arquiteta em {e(c["nome"])}</a></li>'
        for c in DADOS["cidades"]
    )
    cau = f'<div>Arquiteta e urbanista · {e(ESC["cau"])}</div>' if ESC["cau"] else ""
    return f"""<footer class="border-t border-neutral-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <nav aria-label="Cidades atendidas" class="text-sm text-neutral-600">
        <p class="font-semibold text-neutral-800">Arquitetura no noroeste do RS</p>
        <p class="mt-1">Escritório em {e(ESC['localidade'])}, {e(ESC['cidade'])} - {ESC['uf']} · atendimento online e visitas na região.</p>
        <ul class="mt-3 flex flex-wrap gap-x-5 gap-y-2">
{links}
            <li><a href="atendimento-regiao.html" class="hover:text-brand-500">Todas as cidades atendidas</a></li>
        </ul>
      </nav>
      <div class="flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-neutral-600">
        <div>© <span data-year>{date.today().year}</span> {e(ESC['arquiteta'])}. Todos os direitos reservados.{cau}</div>
        <div class="flex items-center gap-4">
          <a href="{ESC['instagram']}" class="hover:text-brand-500" target="_blank"
            rel="noopener noreferrer">Instagram</a>
          <a href="privacidade.html" class="hover:text-brand-500">Privacidade</a>
          <button type="button" data-cookie-prefs class="hover:text-brand-500">Cookies</button>
          <a href="sitemap.xml" class="hover:text-brand-500">Sitemap</a>
        </div>
      </div>
    </div>
  </footer>"""


FIM = """
  <script src="assets/js/script.js"></script>

</body>

</html>
"""

# Projetos reais do portfólio (projetos.html) usados nas páginas locais
PROJETOS = [
    ("img/cozinha01.webp", 1536, 1024, "Ateliê Viver", "Residencial • Interiores", "Ateliê Viver: cozinha integrada com marcenaria clara"),
    ("img/new_render.webp", 1536, 1024, "Casa Horizonte", "Residencial • Interiores", "Casa Horizonte: ambiente residencial contemporâneo"),
    ("img/house_external.webp", 1536, 1024, "Casa Forte", "Residencial • Fachada", "Casa Forte: fachada residencial"),
    ("img/sala_de_visita.webp", 1536, 1024, "Casa Serena", "Residencial • Interiores", "Casa Serena: sala de estar"),
    ("img/projeto-09_II.webp", 1536, 1024, "Projeto Acolher", "Design inclusivo", "Projeto Acolher: ambiente com design inclusivo"),
    ("img/clinica.webp", 1536, 1024, "Clínica Essenza", "Comercial • Interiores", "Clínica Essenza: interior de clínica"),
]

ETAPAS = [
    ("Briefing", "Levantamento de necessidades e referências."),
    ("Conceito", "Diretrizes espaciais e materiais."),
    ("Projeto", "Desenvolvimento e compatibilização."),
    ("Executivo", "Detalhamento técnico para obra."),
    ("Obra", "Acompanhamento e assistência técnica."),
]


def lugar_cidade(c):
    return {
        "@type": "City",
        "name": c["nome"],
        "containedInPlace": {"@type": "State", "name": "Rio Grande do Sul"},
        "geo": {"@type": "GeoCoordinates", "latitude": c["lat"], "longitude": c["lng"]},
        "identifier": f"IBGE {c['ibge']}",
    }


# ---------------------------------------------------------------------------
# Página de cada cidade
# ---------------------------------------------------------------------------

def pagina_cidade(i, c):
    nome = c["nome"]
    caminho = f"arquiteta-{c['slug']}.html"
    url = f"{SITE}/{caminho}"
    titulo = f"Arquiteta em {nome} - RS | {ESC['arquiteta']}"
    vizinhas = ", ".join(c["vizinhas"][:-1]) + " e " + c["vizinhas"][-1]
    distancia = (
        f"Escritório em {ESC['localidade']}, {ESC['cidade']}"
        if c["km"] == 0
        else f"Cerca de {c['km']} km de {ESC['cidade']}"
    )
    faq = c["faq"] + [
        [f"Atende também cidades perto de {nome}?", f"Sim: {vizinhas}, entre outras cidades do noroeste do RS, com reuniões online e visitas presenciais conforme o projeto."],
        ["E se eu for de fora da região?", "Atendo online em todo o Brasil: briefing, apresentações e acompanhamento por videochamada. As visitas presenciais ficam para quem está na região."],
    ]
    capa = PROJETOS[i % len(PROJETOS)]
    outros = [PROJETOS[(i + k) % len(PROJETOS)] for k in (1, 2, 3)]
    msg = f"Olá, Taís! Sou de {nome} e gostaria de conversar sobre um projeto."

    ld = [
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebPage",
                    "@id": f"{url}#pagina",
                    "url": url,
                    "name": titulo,
                    "description": c["descricao"],
                    "inLanguage": "pt-BR",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@id": ID_NEGOCIO},
                },
                {
                    "@type": "Service",
                    "@id": f"{url}#servico",
                    "name": f"Projetos de arquitetura e interiores em {nome}",
                    "serviceType": "Arquitetura e design de interiores",
                    "description": c["descricao"],
                    "provider": {"@id": ID_NEGOCIO},
                    "areaServed": lugar_cidade(c),
                    "availableChannel": {
                        "@type": "ServiceChannel",
                        "serviceUrl": f"{SITE}/contato.html",
                        "servicePhone": ESC["telefone"],
                        "availableLanguage": "Portuguese",
                    },
                    "hasOfferCatalog": {
                        "@type": "OfferCatalog",
                        "name": "Serviços",
                        "itemListElement": [
                            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s, "description": d}}
                            for s, d in DADOS["servicos"]
                        ],
                    },
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                        {"@type": "ListItem", "position": 2, "name": "Cidades atendidas", "item": f"{SITE}/atendimento-regiao.html"},
                        {"@type": "ListItem", "position": 3, "name": f"Arquiteta em {nome}", "item": url},
                    ],
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq
                    ],
                },
            ],
        }
    ]

    servicos = "\n".join(
        f"""          <div class="bg-white rounded-2xl border border-neutral-200 p-5">
            <h3 class="font-semibold">{e(s)}</h3>
            <p class="text-sm text-neutral-700 mt-1">{e(d)}</p>
          </div>"""
        for s, d in DADOS["servicos"]
    )
    etapas = "\n".join(
        f"""          <li class="bg-white rounded-2xl border border-neutral-200 p-4">
            <div class="text-xs uppercase tracking-wide text-neutral-500">Etapa {n}</div>
            <div class="font-semibold">{e(t)}</div>
            <p class="text-sm text-neutral-600 mt-1">{e(d)}</p>
          </li>"""
        for n, (t, d) in enumerate(ETAPAS, 1)
    )
    projetos = "\n".join(
        f"""          <a href="projetos.html" class="bg-white rounded-2xl border border-neutral-200 overflow-hidden hover:shadow-lg transition block">
            <img src="{src}" class="h-56 w-full object-cover" width="{w}" height="{h}" loading="lazy" alt="{e(alt)}">
            <div class="p-5">
              <div class="font-semibold">{e(n)}</div>
              <div class="text-sm text-neutral-600">{e(cat)}</div>
            </div>
          </a>"""
        for src, w, h, n, cat, alt in outros
    )
    perguntas = "\n".join(
        f"""          <details class="bg-white rounded-2xl border border-neutral-200 p-4">
            <summary class="font-semibold cursor-pointer">{e(p)}</summary>
            <p class="text-neutral-700 mt-2">{e(r)}</p>
          </details>"""
        for p, r in faq
    )
    outras_cidades = "\n".join(
        f'          <li><a href="arquiteta-{o["slug"]}.html" class="inline-flex px-4 py-2 rounded-full border border-neutral-300 bg-white hover:bg-neutral-50">{e(o["nome"])}</a></li>'
        for o in DADOS["cidades"]
        if o["slug"] != c["slug"]
    )
    intro = "\n".join(f'        <p class="mt-4 text-lg text-neutral-700 max-w-xl">{e(p)}</p>' for p in c["intro"])

    corpo = f"""
  <main>
    <section>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16 grid lg:grid-cols-2 gap-10 items-center">
        <div>
          <nav aria-label="Você está em" class="text-sm text-neutral-500">
            <a href="index.html" class="hover:text-brand-500">Home</a> /
            <a href="atendimento-regiao.html" class="hover:text-brand-500">Cidades atendidas</a> /
            <span aria-current="page">{e(nome)}</span>
          </nav>
          <span class="mt-4 inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm bg-brand-50 ring-1 ring-brand-200">Atendimento online e visitas presenciais</span>
          <h1 class="mt-4 font-display text-4xl md:text-5xl leading-[1.08] tracking-tight text-neutral-900">Arquiteta em {e(nome)} <span style="color: {COR};">- RS</span></h1>
{intro}
          <div class="mt-6 flex flex-wrap gap-3">
            <a href="contato.html" class="px-5 py-3 rounded-xl text-white hover:opacity-90 transition" style="background-color: {COR};">Solicitar orçamento</a>
            <a href="{wa(msg)}" target="_blank" rel="noopener noreferrer" class="px-5 py-3 rounded-xl border border-neutral-300 bg-white hover:bg-neutral-50">Conversar no WhatsApp</a>
          </div>
        </div>
        <figure>
          <img src="{capa[0]}" alt="{e(capa[5])}" width="{capa[1]}" height="{capa[2]}" fetchpriority="high"
            class="rounded-3xl shadow-soft w-full h-[380px] object-cover">
          <figcaption class="mt-3 text-sm text-neutral-500">{e(capa[3])} · {e(capa[4])}</figcaption>
        </figure>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="bg-white border border-neutral-200 rounded-3xl p-6 md:p-10 grid md:grid-cols-3 gap-8 shadow-soft">
          <div class="md:col-span-2">
            <h2 class="font-display text-2xl md:text-3xl">{e(c['destaque'][0])}</h2>
            <p class="text-neutral-700 mt-3">{e(c['destaque'][1])}</p>
          </div>
          <ul class="space-y-3 text-sm">
            <li class="rounded-xl bg-brand-50 p-3"><span class="block text-xs uppercase tracking-wide text-neutral-500">Distância</span>{e(distancia)}</li>
            <li class="rounded-xl bg-brand-50 p-3"><span class="block text-xs uppercase tracking-wide text-neutral-500">Reuniões</span>Online ou presenciais</li>
            <li class="rounded-xl bg-brand-50 p-3"><span class="block text-xs uppercase tracking-wide text-neutral-500">Visitas</span>Terreno, imóvel e obra em {e(nome)}</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h2 class="font-display text-2xl md:text-3xl">Serviços para {e(nome)}</h2>
        <div class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{servicos}
        </div>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h2 class="font-display text-2xl md:text-3xl">Como funciona</h2>
        <ol class="grid md:grid-cols-5 gap-4 mt-6">
{etapas}
        </ol>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div class="flex items-end justify-between">
          <h2 class="font-display text-2xl md:text-3xl">Alguns projetos</h2>
          <a href="projetos.html" class="text-sm hover:text-brand-500">Ver todos</a>
        </div>
        <div class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{projetos}
        </div>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h2 class="font-display text-2xl md:text-3xl">Perguntas de quem é de {e(nome)}</h2>
        <div class="mt-4 space-y-3">
{perguntas}
        </div>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h2 class="font-display text-xl md:text-2xl">Também atendo</h2>
        <ul class="mt-4 flex flex-wrap gap-3 text-sm">
{outras_cidades}
          <li><a href="atendimento-regiao.html" class="inline-flex px-4 py-2 rounded-full border border-neutral-300 bg-white hover:bg-neutral-50">Todas as cidades da região</a></li>
        </ul>
      </div>
    </section>

    <section class="reveal">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="bg-white border border-neutral-200 rounded-3xl p-8 md:p-12 text-center shadow-soft">
          <h2 class="font-display text-2xl md:text-3xl">Vamos conversar sobre o seu projeto em {e(nome)}?</h2>
          <p class="text-neutral-700 mt-2">Conte sobre o terreno, a reforma ou o ambiente. Respondo rápido.</p>
          <div class="mt-5 flex flex-wrap justify-center gap-3">
            <a href="contato.html" class="px-5 py-3 rounded-xl text-white hover:opacity-90 transition" style="background-color: {COR};">Falar com a arquiteta</a>
            <a href="{wa(msg)}" target="_blank" rel="noopener noreferrer" class="px-5 py-3 rounded-xl border border-neutral-300 bg-white hover:bg-neutral-50">WhatsApp {e(ESC['telefoneExibicao'])}</a>
          </div>
        </div>
      </div>
    </section>
  </main>
  """
    escrever(caminho, head(titulo, c["descricao"], caminho, ld) + HEADER + corpo + footer() + FIM)
    return caminho


# ---------------------------------------------------------------------------
# Página da região
# ---------------------------------------------------------------------------

def pagina_regiao():
    caminho = "atendimento-regiao.html"
    url = f"{SITE}/{caminho}"
    titulo = f"Arquiteta no noroeste do RS: cidades atendidas | {ESC['arquiteta']}"
    descricao = (
        "Arquitetura e interiores em São Martinho, Três de Maio, Boa Vista do Buricá, Independência, Horizontina, "
        "Santa Rosa e cidades do noroeste do RS. Reuniões online e visitas presenciais."
    )
    cartoes = "\n".join(
        f"""          <a href="arquiteta-{c['slug']}.html" class="bg-white rounded-2xl border border-neutral-200 p-5 hover:shadow-lg transition block">
            <div class="font-semibold">Arquiteta em {e(c['nome'])}</div>
            <div class="text-sm text-neutral-600 mt-1">{'Escritório na cidade' if c['km'] == 0 else f"Cerca de {c['km']} km de São Martinho"}</div>
          </a>"""
        for c in DADOS["cidades"]
    )
    com_pagina = {c["nome"]: c["slug"] for c in DADOS["cidades"]}
    lista = "\n".join(
        (
            f'          <li><a href="arquiteta-{com_pagina[n]}.html" class="hover:text-brand-500 underline">{e(n)}</a> <span class="text-neutral-500">· {"sede" if km == 0 else f"{km} km"}</span></li>'
            if n in com_pagina
            else f'          <li>{e(n)} <span class="text-neutral-500">· {km} km</span></li>'
        )
        for n, km in DADOS["regiao"]
    )
    ld = [
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebPage",
                    "@id": f"{url}#pagina",
                    "url": url,
                    "name": titulo,
                    "description": descricao,
                    "inLanguage": "pt-BR",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@id": ID_NEGOCIO},
                },
                {
                    "@type": "ItemList",
                    "name": "Cidades atendidas",
                    "itemListElement": [
                        {"@type": "ListItem", "position": n, "name": f"Arquiteta em {c['nome']}", "url": f"{SITE}/arquiteta-{c['slug']}.html"}
                        for n, c in enumerate(DADOS["cidades"], 1)
                    ],
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                        {"@type": "ListItem", "position": 2, "name": "Cidades atendidas", "item": url},
                    ],
                },
            ],
        }
    ]
    corpo = f"""
  <main>
    <section>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <nav aria-label="Você está em" class="text-sm text-neutral-500">
          <a href="index.html" class="hover:text-brand-500">Home</a> / <span aria-current="page">Cidades atendidas</span>
        </nav>
        <h1 class="mt-4 font-display text-3xl md:text-5xl tracking-tight">Arquitetura no noroeste do RS</h1>
        <p class="text-neutral-700 mt-3 max-w-2xl">Meu escritório fica em {e(ESC['localidade'])}, {e(ESC['cidade'])} - RS. Atendo a região com reuniões online e visitas presenciais ao terreno, ao imóvel e à obra. Para quem é de fora, o atendimento é online, em todo o Brasil.</p>

        <h2 class="mt-10 font-display text-2xl md:text-3xl">Principais cidades</h2>
        <div class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
{cartoes}
        </div>

        <h2 class="mt-12 font-display text-2xl md:text-3xl">Cidades até cerca de 50 km de São Martinho</h2>
        <p class="text-neutral-700 mt-2 max-w-2xl">Distâncias aproximadas, em linha reta, a partir do centro de cada município (IBGE). A sua cidade não está na lista? Fale comigo: provavelmente atendo também.</p>
        <ul class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2 text-neutral-800">
{lista}
        </ul>

        <div class="mt-12 bg-white border border-neutral-200 rounded-3xl p-8 md:p-12 text-center shadow-soft">
          <h2 class="font-display text-2xl md:text-3xl">Vamos projetar algo incrível?</h2>
          <p class="text-neutral-700 mt-2">Conte sobre seu terreno, reforma ou interior. Respondo rápido.</p>
          <div class="mt-5 flex flex-wrap justify-center gap-3">
            <a href="contato.html" class="px-5 py-3 rounded-xl text-white hover:opacity-90 transition" style="background-color: {COR};">Falar com a arquiteta</a>
            <a href="{wa('Olá, Taís! Gostaria de conversar sobre um projeto.')}" target="_blank" rel="noopener noreferrer" class="px-5 py-3 rounded-xl border border-neutral-300 bg-white hover:bg-neutral-50">WhatsApp {e(ESC['telefoneExibicao'])}</a>
          </div>
        </div>
      </div>
    </section>
  </main>
  """
    escrever(caminho, head(titulo, descricao, caminho, ld) + HEADER + corpo + footer() + FIM)
    return caminho


# ---------------------------------------------------------------------------
# JSON-LD do escritório (home), rodapé de todas as páginas, sitemap, robots, llms
# ---------------------------------------------------------------------------

def jsonld_escritorio():
    negocio = {
        "@type": "ProfessionalService",
        "@id": ID_NEGOCIO,
        "additionalType": "https://www.wikidata.org/wiki/Q42973",
        "name": ESC["nome"],
        "description": "Escritório de arquitetura com foco em neuroarquitetura: projetos residenciais, comerciais e de interiores. Sede em São Martinho - RS, visitas no noroeste do RS e atendimento online em todo o Brasil.",
        "url": f"{SITE}/",
        "image": f"{SITE}/img/og-image.jpg",
        "logo": f"{SITE}/favicon.svg",
        "email": ESC["email"],
        "telephone": ESC["telefone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ESC["localidade"],
            "addressLocality": ESC["cidade"],
            "addressRegion": ESC["uf"],
            "addressCountry": "BR",
        },
        "areaServed": [lugar_cidade(c) for c in DADOS["cidades"]]
        + [
            {"@type": "AdministrativeArea", "name": "Noroeste do Rio Grande do Sul"},
            {"@type": "Country", "name": "Brasil"},
        ],
        "knowsAbout": ["Neuroarquitetura", "Arquitetura residencial", "Arquitetura de interiores", "Projetos comerciais", "BIM"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Serviços de arquitetura",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s, "description": d}}
                for s, d in DADOS["servicos"]
            ],
        },
        "founder": {"@id": ID_PESSOA},
        "sameAs": [ESC["instagram"]],
    }
    if ESC["cau"]:
        negocio["identifier"] = {"@type": "PropertyValue", "propertyID": "CAU", "value": ESC["cau"]}
    pessoa = {
        "@type": "Person",
        "@id": ID_PESSOA,
        "name": ESC["arquiteta"],
        "alternateName": ["Taís Müller", "Tais Regina Muller", "Arquiteta Taís Müller"],
        "jobTitle": "Arquiteta",
        "knowsAbout": ["Neuroarquitetura", "Arquitetura residencial", "Arquitetura de interiores", "Projetos comerciais"],
        "url": f"{SITE}/sobre.html",
        "workLocation": {"@type": "Place", "name": f"{ESC['cidade']} - {ESC['uf']}"},
        "worksFor": {"@id": ID_NEGOCIO},
        "sameAs": [ESC["instagram"]],
    }
    if ESC["cau"]:
        pessoa["hasCredential"] = {"@type": "EducationalOccupationalCredential", "credentialCategory": "Registro profissional", "name": ESC["cau"]}
    site = {
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": ESC["nome"],
        "inLanguage": "pt-BR",
        "publisher": {"@id": ID_NEGOCIO},
    }
    return jsonld({"@context": "https://schema.org", "@graph": [negocio, pessoa, site]})


def atualizar_index():
    s = ler("index.html")
    bloco = f"<!-- JSONLD:inicio (gerado por scripts/gerar-paginas-locais.py) -->\n  {jsonld_escritorio()}\n  <!-- JSONLD:fim -->"
    if "<!-- JSONLD:inicio" in s:
        s = re.sub(r"<!-- JSONLD:inicio.*?<!-- JSONLD:fim -->", lambda _: bloco, s, flags=re.S)
    else:
        s, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda _: bloco, s, count=1, flags=re.S)
        if n != 1:
            sys.exit("index.html: bloco JSON-LD não encontrado")
    escrever("index.html", s)


def atualizar_rodapes():
    rodape = footer()
    alterados = []
    for nome in sorted(os.listdir(RAIZ)):
        if not nome.endswith(".html"):
            continue
        s = ler(nome)
        novo, n = re.subn(r"<footer\b.*?</footer>", lambda _: rodape, s, count=1, flags=re.S)
        if n and novo != s:
            escrever(nome, novo)
            alterados.append(nome)
    return alterados


FIXAS = [
    ("", "1.0"),
    ("projetos.html", "0.9"),
    ("servicos.html", "0.8"),
    ("sobre.html", "0.7"),
    ("contato.html", "0.7"),
    ("atendimento-regiao.html", "0.8"),
    ("privacidade.html", "0.2"),
]


def sitemap():
    urls = FIXAS[:-1] + [(f"arquiteta-{c['slug']}.html", "0.8") for c in DADOS["cidades"]] + FIXAS[-1:]
    itens = "\n".join(
        f"""  <url>
    <loc>{SITE}/{u}</loc>
    <lastmod>{HOJE}</lastmod>
    <priority>{p}</priority>
  </url>"""
        for u, p in urls
    )
    escrever("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{itens}\n</urlset>\n')


def robots():
    escrever(
        "robots.txt",
        f"""# Buscadores e assistentes de IA liberados: aparecer em respostas do
# ChatGPT, Claude, Perplexity e Gemini ajuda a ser encontrada (GEO).
User-agent: *
Allow: /
Disallow: /404.html

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""",
    )


def llms():
    cidades = "\n".join(
        f"- [Arquiteta em {c['nome']} - RS]({SITE}/arquiteta-{c['slug']}.html): {c['descricao']}" for c in DADOS["cidades"]
    )
    regiao = ", ".join(n for n, _ in DADOS["regiao"])
    servicos = "\n".join(f"- {s}: {d}" for s, d in DADOS["servicos"])
    cau = f"\n- Registro: {ESC['cau']}" if ESC["cau"] else ""
    escrever(
        "llms.txt",
        f"""# {ESC['nome']}

> {ESC['arquiteta']} é arquiteta com foco em neuroarquitetura. Faz projetos residenciais, comerciais e de interiores. Escritório em {ESC['localidade']}, {ESC['cidade']} - {ESC['uf']}, no noroeste do Rio Grande do Sul, com visitas presenciais na região e atendimento online em todo o Brasil.

- Arquiteta: {ESC['arquiteta']}{cau}
- Escritório: {ESC['localidade']}, {ESC['cidade']} - {ESC['uf']}, Brasil
- Atendimento presencial (visita técnica, levantamento, acompanhamento de obra): São Martinho, Três de Maio, Boa Vista do Buricá, Independência, Horizontina, Santa Rosa e cidades do noroeste do RS
- Atendimento online: todo o Brasil
- WhatsApp: {ESC['telefoneExibicao']} (https://wa.me/{ESC['whatsapp']})
- E-mail: {ESC['email']}
- Instagram: {ESC['instagram']}

## Serviços

{servicos}

## Como funciona

1. Briefing: levantamento de necessidades e referências.
2. Conceito: diretrizes espaciais e materiais.
3. Projeto: desenvolvimento e compatibilização.
4. Executivo: detalhamento técnico para obra.
5. Obra: acompanhamento e assistência técnica.

## Páginas por cidade

{cidades}
- [Todas as cidades atendidas]({SITE}/atendimento-regiao.html)

Região atendida (até cerca de 50 km de São Martinho): {regiao}.

## Outras páginas

- [Projetos]({SITE}/projetos.html): portfólio com projetos residenciais, comerciais e de interiores.
- [Serviços]({SITE}/servicos.html)
- [Sobre a arquiteta]({SITE}/sobre.html)
- [Contato]({SITE}/contato.html)
""",
    )


if __name__ == "__main__":
    geradas = [pagina_cidade(i, c) for i, c in enumerate(DADOS["cidades"])] + [pagina_regiao()]
    atualizar_index()
    rodapes = atualizar_rodapes()
    sitemap()
    robots()
    llms()
    print("páginas geradas:", ", ".join(geradas))
    print("rodapé atualizado em:", ", ".join(rodapes) or "nenhuma")
    print("também: index.html (JSON-LD), sitemap.xml, robots.txt, llms.txt")

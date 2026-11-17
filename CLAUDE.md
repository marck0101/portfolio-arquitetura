# CLAUDE.md — site da arquiteta Taís Regina Müller

Site estático (HTML + Tailwind compilado) publicado no Netlify a partir da raiz do repositório:
https://taismuller-arquiteta.netlify.app

## Rodar e publicar

- Abrir os `.html` direto no navegador ou servir a pasta com qualquer servidor estático.
- Depois de mudar classes Tailwind em qualquer `.html`: `npm run build:css` (gera `assets/css/tailwind.css`, que vai no commit).
- O Netlify não roda build: publica os arquivos como estão.

## SEO local (objetivo: aparecer em buscas por arquiteta em São Martinho, Três de Maio, Boa Vista do Buricá e região)

A arquiteta tem escritório em Flor da Serra, São Martinho - RS. Atende **online em todo o Brasil** e faz **visitas presenciais** (terreno, levantamento, acompanhamento de obra) no noroeste do RS.

Tudo o que é local sai de **`scripts/cidades.json`** pelo gerador:

```bash
python scripts/gerar-paginas-locais.py   # depois: npm run build:css
```

| Gera / atualiza | O quê |
|---|---|
| `arquiteta-<cidade>.html` | uma página por cidade: texto, destaque e perguntas próprios, distância real, cidades vizinhas, JSON-LD `Service` + `FAQPage` + `BreadcrumbList` com coordenadas da cidade |
| `atendimento-regiao.html` | cidades principais + todos os municípios até ~50 km de São Martinho |
| `index.html` | só o bloco JSON-LD do escritório (`ProfessionalService` + `Person` + `WebSite`), entre `<!-- JSONLD:inicio -->` e `<!-- JSONLD:fim -->` |
| `<footer>` de todos os `.html` | rodapé único com links para as cidades |
| `sitemap.xml`, `robots.txt`, `llms.txt` | sempre em sincronia com as páginas |

**Não editar à mão** o que o gerador escreve: a próxima execução sobrescreve. Editar o JSON e rodar de novo.

Regras para o conteúdo das cidades:
- Texto **diferente de verdade** em cada página (intro, destaque, 2 perguntas próprias). Página que só troca o nome da cidade é tratada como spam pelo Google.
- Só afirmar o que a arquiteta faz. Distâncias e vizinhas vêm dos centroides oficiais do IBGE (API de malhas), em linha reta, calculados em 17/11/2026.
- Para incluir uma cidade: adicionar o objeto em `cidades`, com texto próprio, e rodar o gerador. A home tem a seção "Onde atendo" com os links escritos à mão: incluir a cidade lá também.

## Pendências

| Item | Onde | Efeito |
|---|---|---|
| Número do **CAU** | `escritorio.cau` em `scripts/cidades.json` | aparece no rodapé e no JSON-LD (`identifier`/`hasCredential`) |
| **Perfil no Google (Google Business Profile)** | fora do site | é o que mais pesa para aparecer no mapa e em "arquiteta perto de mim". Cadastrar como empresa de área de serviço, com as cidades atendidas, e linkar o site |
| Domínio próprio | trocar `site` no JSON e o canonical das páginas feitas à mão | `*.netlify.app` funciona, mas domínio próprio passa mais confiança |
| Search Console | fora do site | enviar o `sitemap.xml` e pedir indexação das páginas novas |

## Histórico

| Data | Mudança |
|---|---|
| 2026-10 | Nome correto, SEO básico, performance, LGPD (banner e política) |
| 2026-11-17 | SEO local: 6 páginas por cidade, página de região, JSON-LD com `areaServed` por cidade, `llms.txt`, `robots.txt` com bots de IA, sitemap atualizado, rodapé com cidades, gerador `scripts/gerar-paginas-locais.py` |

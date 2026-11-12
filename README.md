# Elahs Beauty: site

Landing page estática da Elahs Beauty (mega hair invisível em São Vicente, SP).

- `site/`: o que vai para o ar. A Netlify publica esta pasta (veja `netlify.toml`), sem comando de build.
- `fonte/`: arquivos que geram `site/index.html`. Os dados da marca (nome, telefone, endereço, serviços, avaliações, dúvidas) ficam no bloco DADOS do `build.py`.

Cada push na branch `main` gera um deploy novo na Netlify.

## Antes de ir para o domínio final

- Trocar `SITE` no `fonte/build.py` pelo domínio real e gerar de novo (afeta canonical, sitemap, robots e dados estruturados).
- Colar o snippet do Google Tag Manager no lugar marcado no `<head>`.
- Enviar `sitemap.xml` no Google Search Console.

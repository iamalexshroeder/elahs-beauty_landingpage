#!/usr/bin/env python3
"""Gera o site da Elahs Beauty (estático) a partir de base.css/base.js (projeto Alma) + camada da marca.
Saída: ../site (produção) e ../preview/index.html (prévia para o artifact).
Tudo que a cliente pode querer trocar está no bloco DADOS abaixo."""
import json, pathlib, re, datetime, urllib.parse as up, html

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'site'
PREV = HERE.parent / 'preview'
PREV.mkdir(exist_ok=True)

# ============================== DADOS (edite aqui) ==============================
SITE = 'https://elahsbeauty.com.br'          # domínio final (trocar quando estiver definido)
NOME = 'Elahs Beauty'
SLOGAN = 'Expert em resultados impecáveis'
TEL = '5513998066656'; TEL_TXT = '(13) 99806-6656'; TEL_LD = '+55-13-99806-6656'
IG_USER = 'elahsbeauty_'; IG = f'https://www.instagram.com/{IG_USER}/'
END1 = 'R. Maurício Moura, 231a'; BAIRRO = 'Cidade Náutica'; CIDADE = 'São Vicente'; UF = 'SP'; CEP = '11355-410'
MAPS = 'https://www.google.com/maps/search/?api=1&query=' + up.quote_plus(f'Elahs Beauty, {END1} - {BAIRRO}, {CIDADE} - {UF}, {CEP}')
NOTA = '5,0'; NOTA_NUM = '5.0'; AVALIACOES = 84
CEO = 'Esther Heloize'

SERVICOS = [  # nome, descrição, imagem, clipe
    ('Mega hair invisível', 'Comprimento e volume com acabamento natural, sem marcas aparentes.', 'servico-mega-hair'),
    ('Cores personalizadas', 'Cor pensada para o seu tom de pele e o seu estilo, com brilho duradouro.', 'servico-cores-personalizadas'),
    ('Mechas e loiros', 'Loiros iluminados e platinados com cuidado com a saúde do fio.', 'servico-mechas-loiras'),
    ('Morena iluminada', 'Luzes suaves que valorizam o castanho e dão movimento.', 'servico-morena-iluminada'),
    ('Cachos', 'Definição e cuidado para cachos com forma, brilho e leveza.', 'servico-cachos'),
    ('Extensão de cílios', 'Olhar marcante sem rímel, no formato dos seus olhos.', 'servico-cilios'),
    ('Design de sobrancelhas', 'Sobrancelhas alinhadas que respeitam o desenho do seu rosto.', 'servico-sobrancelhas'),
    ('Unhas', 'Esmaltação caprichada, do nude ao vinho, com acabamento impecável.', 'servico-unhas'),
    ('Pés', 'Cuidado completo para pés macios e unhas bem feitas.', 'servico-pes'),
]
AVALS = [
    ('Fernanda C.', '4 meses atrás', 'Eu adoro este salão, sempre sou muito bem recebida pelas meninas. Faço manutenção de mega hair e luzes. Podem confiar sem medo, a cabeleireira é super profissional e tem muito conhecimento.'),
    ('Anna M.', '5 meses atrás', 'Todas as meninas que trabalham no Elahs são perfeitas, todos os serviços que eu fiz foram impecáveis. Fora que o salão em si é muito organizado. É tudo pensado com todos os detalhes. Recomendo muitão.'),
    ('Hevilly R.', '5 meses atrás', 'Fiz as unhas e o cabelo, e fiquei apaixonada pelo resultado. O espaço é lindo, confortável e muito acolhedor. Toda a equipe é extremamente atenciosa, talentosa e faz um trabalho excelente em cada detalhe.'),
]
FAQ = [
    ('Como faço para agendar?', f'Pelo WhatsApp {TEL_TXT}. A gente confirma o serviço, o valor e o melhor horário para você.'),
    ('Quanto custa?', 'Depende do serviço e, no cabelo, do comprimento e da técnica. Mande uma foto pelo WhatsApp que a gente passa o orçamento.'),
    ('O mega hair invisível fica natural?', 'A técnica é escolhida para o seu tipo de fio, com acabamento sem marcas aparentes. Na avaliação a Esther explica cada etapa.'),
    ('De quanto em quanto tempo faço manutenção?', 'Depende da técnica e do seu cabelo. No atendimento a gente indica o intervalo ideal para você.'),
    ('Posso remarcar?', 'Pode. Avise com antecedência pelo WhatsApp para liberarmos o horário para outra cliente.'),
]
EQUIPE_P = [
    f'A {NOME} é comandada por {CEO}, expert em mega hair invisível e em cores personalizadas. Cada alongamento e cada cor são planejados para o seu fio e o seu rosto, com acabamento natural.',
    'No mega hair, Esther divide a cadeira com Thaíssa Marques. Nas unhas e no banho de gel, Nailvi Marques. Na depilação e na podologia, Emilly Silva. Cada uma é especialista no que faz.',
]
TITLE = f'{NOME} | Mega hair invisível em São Vicente, SP'
DESC = f'Mega hair invisível, cores personalizadas, cílios e unhas na Cidade Náutica, São Vicente. Nota {NOTA} no Google com {AVALIACOES} avaliações. Agende pelo WhatsApp.'
# ================================================================================

def wa(msg): return 'https://api.whatsapp.com/send/?phone=' + TEL + '&amp;text=' + up.quote(msg)
W_AGENDAR = wa('Olá! Vim pelo site e gostaria de agendar um horário.')
W_IND = wa('Olá! Vim pelo site e queria uma indicação de serviço.')
W_ESTHER = wa('Olá! Vim pelo site e gostaria de agendar com a Esther.')
W_TRANSF = wa('Olá! Vim pelo site e quero uma avaliação para a minha transformação.')
W_DUV = wa('Olá! Vim pelo site e tenho uma dúvida.')
MAPS_H = MAPS.replace('&', '&amp;')
EXT = 'target="_blank" rel="noopener"'
WA = '<svg aria-hidden="true"><use href="#wa"/></svg>'
STARS = '<span class="stars" aria-hidden="true">' + '<svg><use href="#star"/></svg>' * 5 + '</span>'

LOGO_PATH = re.search(r' d="([^"]+)"', (HERE / 'logo.svg').read_text()).group(1)

# ---------- CSS e JS: base do projeto + troca de paleta + camada da marca ----------
css = (HERE / 'base.css').read_text()
for a, b in {'#231F1B':'#3D2822','#38271a':'#3D2822','#3d4336':'#47302A','#4A3628':'#3D2822','#4C5343':'#553830','#6B6259':'#7A6159',
             '#79573E':'#6E4637','#BB9979':'#C79A8B','#D9C3A8':'#E6CBC1','#E7DCCB':'#EBD5CC','#F3EBD9':'#F4E6E0','#F8F5EF':'#FBF7F5',
             'rgba(248,245,239':'rgba(251,247,245','rgba(35,31,27':'rgba(61,40,34','rgba(56,39,26':'rgba(61,40,34','rgba(101,57,27':'rgba(85,56,48',
             'rgba(121,87,62':'rgba(110,70,55'}.items():
    css = css.replace(a, b)
css += (HERE / 'elahs.css').read_text()
js = (HERE / 'base.js').read_text()
js = js.replace("setTimeout(function(){ type(tags[1]); },1650);", "if(tags[1]) setTimeout(function(){ type(tags[1]); },1650);")
js = js.replace("setTimeout(function(){ type(tags[0]); },1250);", "if(tags[0]) setTimeout(function(){ type(tags[0]); },1250);")
js += (HERE / 'elahs.js').read_text()
# minificação leve (sem dependências)
css = re.sub(r'/\*.*?\*/', '', css, flags=re.S); css = re.sub(r'\s*\n\s*', '\n', css); css = re.sub(r'\s*([{};:,>])\s*', r'\1', css).replace(';}', '}')
js = '\n'.join(l.strip() for l in js.split('\n') if l.strip() and not l.strip().startswith('//'))

# ---------- blocos ----------
def slug(s): return re.sub(r'[^a-z]+', '-', s.lower().translate(str.maketrans('áãâéêíóôõúç', 'aaaeeiooouc'))).strip('-')
def card(s, dup):
    nome, desc, base = s
    return (f'<li><a class="svc-card" href="{wa("Olá! Vim pelo site e gostaria de agendar: " + nome + ".")}" {EXT} data-video="media/{base}.mp4"{" tabindex=\"-1\"" if dup else ""}>'
            f'<img src="img/{base}.webp" width="554" height="776" alt="{"" if dup else html.escape(nome + " na " + NOME)}" loading="lazy" decoding="async">'
            f'<span class="svc-info"><span class="svc-name">{nome}</span><span class="svc-desc">{desc}</span>'
            f'<span class="svc-go" aria-hidden="true">Agendar <span>→</span></span></span></a></li>')
cards = ''.join(card(s, False) for s in SERVICOS)
cards_dup = ''.join(card(s, True) for s in SERVICOS)

VID_POS = {}   # quadros que viram vídeo curto (posição na grade: número do clipe)
def res_item(i):
    if i in VID_POS:
        k = VID_POS[i]
        return (f'<li class="res-vid"><img src="img/resultado-video-{k}.webp" width="608" height="760" alt="Vídeo de resultado de cabelo na {NOME}" loading="lazy" decoding="async">'
                f'<video muted loop playsinline preload="none" aria-hidden="true" data-src="media/resultado-video-{k}.mp4"></video></li>')
    return f'<li><img src="img/resultado-{i}.webp" srcset="img/resultado-{i}-400.webp 400w, img/resultado-{i}.webp 608w" sizes="(max-width: 900px) 46vw, 304px" width="608" height="760" alt="Resultado de cabelo de cliente da {NOME}" loading="lazy" decoding="async"></li>'
res = ''.join(res_item(i) for i in range(1, 9))

KNOB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l-6 6 6 6M15 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ba = ''.join(f'''<li class="ba-item">
  <img src="img/depois-{i}.webp" width="480" height="624" alt="Depois: transformação {i} feita na {NOME}" loading="lazy" decoding="async">
  <div class="ba-before"><img src="img/antes-{i}.webp" width="480" height="624" alt="Antes: transformação {i}" loading="lazy" decoding="async"></div>
  <span class="ba-line"></span><span class="ba-knob">{KNOB}</span><span class="ba-grab" aria-hidden="true"></span><span class="ba-tag a" aria-hidden="true">Antes</span><span class="ba-tag d" aria-hidden="true">Depois</span>
  <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Comparar antes e depois da transformação {i}">
</li>''' for i in range(1, 6))

rev = ''.join(f'<li><figure class="rev"><figcaption><b>{n}</b><span>{d} · Google</span></figcaption><blockquote>“{q}”</blockquote>'
              f'<span class="rev-stars" role="img" aria-label="5 de 5 estrelas">{STARS}</span></figure></li>' for n, d, q in AVALS)
faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))

# mapa ilustrativo (cores do Google Maps), traçado real da Rua Maurício Moura
streets = ['M-10 112 L610 44','M-10 332 L560 270','M40 -10 L70 460','M210 -10 L252 460','M311 -10 L351 372','M405 -10 L441 362','M509 -10 L542 300']
canal = 'M-30 470 L0 442 C 60 425 110 405 165 397 C 250 386 330 382 390 375 C 420 371 445 365 465 356 C 520 330 565 280 600 232 L640 190'
MAP_SVG = f'''<svg class="map-art" viewBox="0 0 600 450" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
<rect width="600" height="450" fill="#E8EAED"/><g fill="none">
{''.join(f'<path d="{d}" stroke="#DADCE0" stroke-width="14"/>' for d in streets)}{''.join(f'<path d="{d}" stroke="#fff" stroke-width="11"/>' for d in streets)}
<path d="M-10 222 L610 154" stroke="#DADCE0" stroke-width="17"/><path d="M-10 222 L610 154" stroke="#fff" stroke-width="14"/>
<path d="{canal}" stroke="#AADAFF" stroke-width="26"/>
<path d="M146 -10 L188 460" stroke="#F2C94C" stroke-width="56"/><path d="M146 -10 L188 460" stroke="#FDE293" stroke-width="52"/><path d="M146 -10 L188 460" stroke="#AADAFF" stroke-width="18"/></g>
<g font-family="Inter,system-ui,sans-serif" font-size="13"><text x="330" y="176" transform="rotate(-6.3 330 176)" fill="#3C4043" font-weight="600">R. Maurício Moura</text>
<text x="350" y="272" transform="rotate(-6.3 350 272)" fill="#5F6368" font-size="11" letter-spacing="1.5">CIDADE NÁUTICA</text>
<text x="226" y="262" transform="rotate(84.8 226 262)" fill="#5F6368">R. Walt Disney</text>
<text x="214" y="404" transform="rotate(-4.5 214 404)" fill="#4A8BC2">Av. Eduardo Souto</text></g></svg>'''
PIN = f'<svg class="map-pin" viewBox="0 0 56 70" aria-hidden="true"><path d="M28 70S4 44 4 28a24 24 0 1 1 48 0c0 16-24 42-24 42Z" fill="#6E4637"/><svg x="9" y="9" width="38" height="38" viewBox="0 0 268 268"><path d="{LOGO_PATH}" fill="#FBF7F5"/></svg></svg>'

H1 = ('<span class="w" style="--i:0">Do</span> <span class="w" style="--i:1">mega&nbsp;hair</span><br class="bm"> '
      '<span class="w" style="--i:2">invisível</span><br class="bd"> <span class="w" style="--i:3">à</span> <span class="w" style="--i:4">cor</span><br class="bm"> '
      '<span class="w" style="--i:5">perfeita</span> <span class="w" style="--i:6">para</span> <span class="w" style="--i:7">você</span>')

BODY = f'''
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="star" viewBox="0 0 24 24"><path fill="currentColor" d="m12 2.6 2.9 6.1 6.6.8-4.9 4.6 1.3 6.5L12 17.4l-5.9 3.2 1.3-6.5L2.5 9.5l6.6-.8z"/></symbol>
  <symbol id="wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.7 11.7 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3Z"/></symbol>
  <symbol id="eh" viewBox="0 0 268 268"><path fill="currentColor" d="{LOGO_PATH}"/></symbol>
</svg>

<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="nav" id="nav">
  <nav class="wrap nav-in" aria-label="Principal">
    <ul><li><a class="link" href="#sobre">Sobre</a></li><li><a class="link" href="#servicos">Serviços</a></li></ul>
    <a class="logo" href="#conteudo" aria-label="{NOME}, início"><svg class="logo-mark" role="img" aria-label="{NOME}"><use href="#eh"/></svg></a>
    <ul><li><a class="link" href="#resultados">Resultados</a></li><li><a class="link" href="#contato">Contato</a></li></ul>
  </nav>
</header>

<main id="conteudo" tabindex="-1">
  <section class="hero" aria-labelledby="hero-t">
    <video class="hero-bg" id="heroVideo" muted loop playsinline autoplay preload="none" poster="media/hero-m.webp" aria-hidden="true"
      data-src-m="media/hero-m.mp4" data-src-d="media/hero-d.mp4" data-poster-m="media/hero-m.webp" data-poster-d="media/hero-d.webp"></video>
    <div class="wrap hero-copy">
      <h1 id="hero-t">{H1}</h1>
      <p class="hero-sub">Mega hair invisível, cores personalizadas, cílios e unhas em um só lugar. Agende pelo WhatsApp.</p>
      <div class="hero-act">
        <a class="btn btn-rosa" href="{W_AGENDAR}" {EXT}>Agendar meu horário</a>
        <a class="btn btn-photo-line" href="#antes-depois">Ver resultados</a>
        <a class="hero-rating" href="#avaliacoes">{STARS}<span><b>{NOTA}</b> no Google · {AVALIACOES} avaliações</span></a>
      </div>
    </div>
  </section>

  <section class="svc" id="servicos" aria-labelledby="svc-t">
    <div class="wrap sec-head" data-stagger>
      <div class="head"><h2 id="svc-t">Do mega hair às unhas, tudo em um só lugar</h2><p class="lead">Escolha o serviço e agende pelo WhatsApp. Não sabe qual? A gente indica.</p></div>
      <a class="btn btn-wa-line" href="{W_IND}" {EXT}>{WA}Pedir indicação no WhatsApp</a>
    </div>
    <div class="car" id="car" data-reveal data-slide>
      <div class="car-track">
        <ul class="car-set" aria-label="Serviços">{cards}</ul>
        <ul class="car-set" aria-hidden="true" inert>{cards_dup}</ul>
      </div>
    </div>
    <div class="wrap car-hint" aria-hidden="true"><span class="car-prog"><i></i></span><span class="car-hint-t">Deslize para ver os {len(SERVICOS)} serviços</span></div>
    <div class="wrap svc-cta-m"><a class="btn btn-wa-line" href="{W_IND}" {EXT}>{WA}Pedir indicação no WhatsApp</a></div>
    <div class="wrap car-ctl">
      <button class="car-btn" id="carBtn" type="button" aria-controls="car">
        <span class="car-ic" aria-hidden="true"><svg class="i-pause" viewBox="0 0 16 16"><path fill="currentColor" d="M4 3h3v10H4zM9 3h3v10H9z"/></svg><svg class="i-play" viewBox="0 0 16 16"><path fill="currentColor" d="M5 3l8 5-8 5z"/></svg></span>
        <span class="car-lbl">Pausar o carrossel</span>
      </button>
    </div>
  </section>

  <section class="team" id="sobre" aria-labelledby="team-t">
    <div class="team-txt" data-stagger>
      <svg class="team-logo" aria-hidden="true"><use href="#eh"/></svg>
      <h2 id="team-t">Quem cuida de você</h2>
      {''.join(f'<p class="lead">{p}</p>' for p in EQUIPE_P)}
      <a class="btn btn-primary team-cta" href="{W_ESTHER}" {EXT}>Agendar com a Esther</a>
    </div>
    <figure class="team-ph" data-reveal data-mask><img srcset="img/esther-600.webp 600w, img/esther-1000.webp 1000w" sizes="(max-width: 900px) 100vw, 50vw" src="img/esther-1000.webp" width="1000" height="1388" alt="{CEO}, CEO e expert em mega hair invisível da {NOME}" loading="lazy" decoding="async"></figure>
  </section>


  <section class="ba" id="antes-depois" aria-labelledby="ba-t">
    <div class="wrap sec-head" data-stagger>
      <div class="head"><h2 id="ba-t">Antes e depois</h2><p class="lead">Arraste para comparar. Transformações de mega hair e cor feitas aqui no estúdio.</p></div>
      <div class="ba-nav"><button type="button" id="baPrev" aria-label="Transformação anterior"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button><button type="button" id="baNext" aria-label="Próxima transformação"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>
    </div>
    <ul class="ba-row" id="baRow" aria-label="Comparações de antes e depois" data-reveal data-slide>{ba}</ul>
    <div class="wrap"><p class="ba-hint" aria-hidden="true">Arraste a alça para comparar. Deslize a foto para ver as 5.</p>
      <a class="btn btn-primary ba-cta" href="{W_TRANSF}" {EXT}>Quero minha transformação</a></div>
  </section>

  <section class="res" id="resultados" aria-labelledby="res-t">
    <div class="wrap">
      <div class="sec-head" data-stagger>
        <div class="head"><h2 id="res-t">Resultados</h2><p class="lead">Clientes atendidas aqui no estúdio. Tem muito mais no nosso Instagram.</p></div>
        <a class="btn btn-rosa-claro" href="{IG}" {EXT}>Ver mais no Instagram</a>
      </div>
      <ul class="res-grid" data-stagger>{res}</ul>
      <div class="sec-cta-m"><a class="btn btn-rosa-claro" href="{IG}" {EXT}>Ver mais no Instagram</a></div>
    </div>
  </section>

  <section class="reviews" id="avaliacoes" aria-labelledby="rev-t">
    <div class="wrap">
      <div class="sec-head" data-stagger>
        <div class="head"><h2 id="rev-t">Avaliações</h2><p class="lead"><span class="count" data-to="{NOTA_NUM}" data-dec="1">{NOTA}</span> de média em <b class="b-m count" data-to="{AVALIACOES}">{AVALIACOES}</b> avaliações no Google</p></div>
        <a class="cta-link rev-link" href="{MAPS_H}" {EXT}>Ver avaliações <span aria-hidden="true">→</span></a>
      </div>
      <ul class="rev-grid" data-stagger>{rev}</ul>
      <a class="btn btn-outline rev-more" href="{MAPS_H}" {EXT}>Ver mais avaliações <span aria-hidden="true">→</span></a>
    </div>
  </section>

  <section class="faq-s" id="duvidas" aria-labelledby="faq-t">
    <div class="wrap faq">
      <div class="intro" data-stagger>
        <h2 id="faq-t">Dúvidas frequentes</h2>
        <p class="lead">Não encontrou sua dúvida?<br>A gente responde no WhatsApp.</p>
        <a class="btn btn-wa-line" href="{W_DUV}" {EXT}>{WA}Falar no WhatsApp</a>
      </div>
      <div class="faq-list" data-stagger>{faq}</div>
    </div>
  </section>

  <section class="visit-s" id="contato" aria-labelledby="visit-t">
    <div class="wrap visit">
      <div class="txt" data-stagger>
        <h2 id="visit-t">Como chegar</h2>
        <dl>
          <div><dt>Endereço</dt><dd>{END1}<br>{BAIRRO}, {CIDADE}, {UF} · <span class="nw">CEP {CEP}</span></dd></div>
          <div><dt>WhatsApp</dt><dd><a href="{W_AGENDAR}" {EXT}>{TEL_TXT}</a></dd></div>
          <div><dt>Agendamento</dt><dd>Pelo WhatsApp, com hora marcada</dd></div>
          <div><dt>Instagram</dt><dd><a href="{IG}" {EXT}>@{IG_USER}</a></dd></div>
        </dl>
        <a class="btn btn-primary" href="{MAPS_H}" {EXT}>Abrir no Google Maps</a>
      </div>
      <a class="map" href="{MAPS_H}" {EXT} aria-label="Ver {NOME} no Google Maps: {END1}, {BAIRRO}, {CIDADE}" data-reveal data-mask>
        {MAP_SVG}
        <span class="map-ring" aria-hidden="true"></span>{PIN}
        <span class="map-card" aria-hidden="true"><b>{NOME}</b><span>{END1}<span class="mc-b"> · {BAIRRO}</span></span></span>
        <span class="map-go" aria-hidden="true">Abrir no Maps ↗</span>
      </a>
    </div>
  </section>
</main>

<footer>
  <svg class="foot-mark" aria-hidden="true" focusable="false"><use href="#eh"/></svg>
  <div class="wrap">
    <div class="foot">
      <div><a class="logo" href="#conteudo" aria-label="{NOME}, voltar ao início"><svg class="logo-mark" aria-hidden="true"><use href="#eh"/></svg></a><p>{SLOGAN}. {BAIRRO}, {CIDADE}.</p></div>
      <details class="fcol" open><summary><h2 class="fh">Navegue</h2></summary><ul><li><a href="#servicos">Serviços</a></li><li><a href="#antes-depois">Antes e depois</a></li><li><a href="#duvidas">Dúvidas</a></li></ul></details>
      <details class="fcol" open><summary><h2 class="fh">Contato</h2></summary><ul><li><a href="{W_AGENDAR}" {EXT}>WhatsApp {TEL_TXT}</a></li><li><a href="{IG}" {EXT}>@{IG_USER}</a></li></ul></details>
      <details class="fcol" open><summary><h2 class="fh">Endereço</h2></summary><ul><li>{END1}</li><li>{BAIRRO}</li><li>{CIDADE}, {UF}</li></ul></details>
    </div>
    <div class="base"><span>© {datetime.date.today().year} {NOME}</span><a class="btn btn-foot" href="{W_AGENDAR}" {EXT}>{WA}Chamar no WhatsApp</a></div>
  </div>
</footer>

<nav class="mbar" id="mbar" aria-label="Agendamento rápido">
  <a class="btn btn-primary" href="{W_AGENDAR}" {EXT}>Agendar meu horário</a>
  <a class="btn btn-wa" href="{W_ESTHER}" {EXT} aria-label="Falar no WhatsApp">{WA}</a>
</nav>
'''

# ---------- SEO ----------
LD_BIZ = {
  '@context': 'https://schema.org', '@type': 'HairSalon', '@id': SITE + '/#salao', 'name': NOME, 'url': SITE + '/',
  'description': DESC, 'image': SITE + '/img/og-1200x630.jpg', 'logo': SITE + '/img/icon-512.png', 'telephone': TEL_LD,
  'priceRange': 'R$ 100 a 200', 'currenciesAccepted': 'BRL',
  'address': {'@type': 'PostalAddress', 'streetAddress': END1, 'addressLocality': CIDADE, 'addressRegion': UF, 'postalCode': CEP, 'addressCountry': 'BR'},
  'areaServed': [{'@type': 'City', 'name': c} for c in ['São Vicente', 'Santos', 'Praia Grande', 'Guarujá', 'Cubatão']],
  'hasMap': MAPS, 'sameAs': [IG, 'https://www.instagram.com/estherheloizee/'],
  'founder': {'@type': 'Person', 'name': CEO, 'jobTitle': 'CEO e expert em mega hair invisível'},
  'potentialAction': {'@type': 'ReserveAction', 'name': 'Agendar pelo WhatsApp', 'target': 'https://wa.me/' + TEL},
  'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Serviços', 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'description': d}} for n, d, _ in SERVICOS]},
}
LD_FAQ = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
LD_WEB = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NOME, 'url': SITE + '/', 'inLanguage': 'pt-BR'}
ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (LD_BIZ, LD_FAQ, LD_WEB))

FONTFACE = "@font-face{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;src:url(fonts/inter-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}\n"
HEAD = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{SITE}/">
<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<meta name="theme-color" content="#FBF7F5">
<meta name="geo.region" content="BR-SP"><meta name="geo.placename" content="{CIDADE}">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="{NOME}">
<meta property="og:title" content="{TITLE}"><meta property="og:description" content="{DESC}"><meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/img/og-1200x630.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{NOME}, mega hair invisível em {CIDADE}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{TITLE}"><meta name="twitter:description" content="{DESC}"><meta name="twitter:image" content="{SITE}/img/og-1200x630.jpg">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="32x32"><link rel="apple-touch-icon" href="img/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="media/hero-m.webp" media="(max-width: 640px)" fetchpriority="high"><link rel="preload" as="image" href="media/hero-d.webp" media="(min-width: 641px)" fetchpriority="high">
{ld}<!-- Google Tag Manager: cole aqui o snippet do GTM (GA4 + Meta Pixel). Os cliques já vão para o dataLayer: whatsapp_click, como_chegar. -->
'''
prod = f'{HEAD}<style>\n{FONTFACE}{css}\n</style>\n</head>\n<body>\n{BODY}\n<script>\n{js}\n</script>\n</body>\n</html>\n'
OUT.mkdir(exist_ok=True)
(OUT / 'index.html').write_text(prod)

# prévia (artifact): sem <html>/<head>, fonte do Google Fonts e caminhos iguais
prev = f'''<title>{NOME}</title>
<meta name="description" content="{DESC}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
<script>document.documentElement.lang="pt-BR"</script>
<style>
{css}
</style>
{BODY}
<script>
{js}
</script>
'''
(PREV / 'index.html').write_text(prev)

# ---------- arquivos de rastreio ----------
hoje = datetime.date.today().isoformat()
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>{SITE}/</loc>
    <lastmod>{hoje}</lastmod>
    <image:image><image:loc>{SITE}/img/og-1200x630.jpg</image:loc></image:image>
    <image:image><image:loc>{SITE}/img/esther-1000.webp</image:loc></image:image>
  </url>
</urlset>
''')
servs = '\n'.join(f'- **{n}**: {d}' for n, d, _ in SERVICOS)
faqs = '\n'.join(f'- **{q}** {a}' for q, a in FAQ)
(OUT / 'llms.txt').write_text(f'''# {NOME}

> Salão de beleza na {BAIRRO}, {CIDADE}, {UF}, comandado por {CEO}, expert em mega hair invisível e cores personalizadas. Nota {NOTA} no Google com {AVALIACOES} avaliações. Agendamento pelo WhatsApp.

## Contato e localização
- Endereço: {END1}, {BAIRRO}, {CIDADE}, {UF}, CEP {CEP}
- WhatsApp: {TEL_TXT} (https://wa.me/{TEL})
- Instagram: https://www.instagram.com/{IG_USER}/
- Mapa: {MAPS}
- Atendimento com hora marcada, agendado pelo WhatsApp.

## Serviços
{servs}

## Equipe
- {CEO}: CEO, mega hair invisível e cores personalizadas.
- Thaíssa Marques: mega hair.
- Nailvi Marques: unhas e banho de gel.
- Emilly Silva: depilação e podologia.

## Perguntas frequentes
{faqs}

## Páginas
- [Página inicial]({SITE}/): serviços, antes e depois, avaliações, dúvidas e como chegar.
''')
(OUT / 'site.webmanifest').write_text(json.dumps({'name': NOME, 'short_name': 'Elahs', 'start_url': '/', 'display': 'standalone', 'background_color': '#FBF7F5', 'theme_color': '#FBF7F5',
  'icons': [{'src': '/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, ensure_ascii=False, indent=1))
(OUT / 'favicon.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 268 268"><circle cx="134" cy="134" r="134" fill="#FBF7F5"/><path fill="#6E4637" d="{LOGO_PATH}"/></svg>')
print('ok', len(prod)//1024, 'KB html')

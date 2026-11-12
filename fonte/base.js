(function(){
  // eventos de conversão: prontos para GTM / GA4 / Meta Pixel
  window.dataLayer=window.dataLayer||[];
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href]'); if(!a) return;
    var h=a.getAttribute('href');
    var ev=h.indexOf('trinks.com')>-1?'agendar_trinks':h.indexOf('whatsapp')>-1?'whatsapp_click':h.indexOf('google.com/maps')>-1?'como_chegar':null;
    if(!ev) return;
    var sec=a.closest('section,header,footer,nav');
    window.dataLayer.push({event:ev,cta_texto:(a.textContent||a.getAttribute('aria-label')||'').trim().replace(/\s+/g,' '),secao:sec?(sec.id||sec.className.split(' ')[0]):''});
  });

  // carrossel: botão pausar / retomar (WCAG 2.2.2)
  var car=document.getElementById('car'), btn=document.getElementById('carBtn');
  if(car&&btn){
    var lbl=btn.querySelector('.car-lbl');
    btn.addEventListener('click',function(){
      var p=car.classList.toggle('paused');
      lbl.textContent=p?'Retomar o carrossel':'Pausar o carrossel';
    });
  }
})();
(function(){
  var root=document.documentElement, nav=document.getElementById('nav'), mbar=document.getElementById('mbar'), mark=document.querySelector('.how-mark');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ticking=false;
  function frame(){
    ticking=false;
    var y=window.scrollY||0, vh=window.innerHeight;
    nav.classList.toggle('scrolled',y>24);
    mbar.classList.toggle('show',y>vh*0.6);
    if(mark&&!reduce){
      var r=mark.parentNode.getBoundingClientRect();
      if(r.bottom>0&&r.top<vh){ var p=(r.top+r.height/2-vh/2)/vh; mark.style.setProperty('--py',(p*-80).toFixed(1)+'px'); }
    }
  }
  window.addEventListener('scroll',function(){ if(!ticking){ ticking=true; requestAnimationFrame(frame); } },{passive:true});
  frame();

  if(reduce||!('IntersectionObserver' in window)) return;
  root.classList.add('js');
  var targets=[];
  document.querySelectorAll('[data-reveal]').forEach(function(el){ targets.push({el:el,d:0}); });
  document.querySelectorAll('[data-stagger]').forEach(function(g){ Array.prototype.forEach.call(g.children,function(c,i){ targets.push({el:c,d:Math.min(i,7)*90}); }); });
  var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); },{rootMargin:'0px 0px -8% 0px',threshold:0.06});
  targets.forEach(function(t){
    if(t.el.getBoundingClientRect().top<window.innerHeight*0.92) return; // já na tela: não esconde
    t.el.classList.add('pre');
    t.el.style.setProperty('--d',t.d+'ms');
    io.observe(t.el);
  });
  var ft=document.querySelector('footer');
  if(ft.getBoundingClientRect().top>window.innerHeight){
    var fo=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ ft.classList.add('seen'); fo.disconnect(); } },{threshold:.2}); fo.observe(ft);
  } else ft.classList.add('seen');
})();

(function(){
  // rodapé: no celular os grupos começam fechados; no computador ficam sempre abertos
  var mq=window.matchMedia('(max-width: 640px)'), cols=document.querySelectorAll('.fcol');
  function apply(){ cols.forEach(function(d){ var s=d.querySelector('summary'); if(mq.matches){ d.open=false; s.removeAttribute('tabindex'); } else { d.open=true; s.setAttribute('tabindex','-1'); } }); }
  cols.forEach(function(d){ d.querySelector('summary').addEventListener('click',function(e){ if(!mq.matches) e.preventDefault(); }); });
  apply(); if(mq.addEventListener) mq.addEventListener('change',apply);
})();

(function(){
  // carrossel no celular: barra de progresso conforme desliza + um empurrãozinho único ao aparecer
  var car=document.getElementById('car'), bar=document.querySelector('.car-prog i'), hint=document.querySelector('.car-hint-t');
  if(!car||!bar) return;
  var mq=window.matchMedia('(max-width: 760px), (prefers-reduced-motion: reduce)');
  function upd(){ var max=car.scrollWidth-car.clientWidth; if(max<=0) return; var p=car.scrollLeft/max; var vis=car.clientWidth/car.scrollWidth; bar.style.setProperty('--p', Math.min(100,(vis+(1-vis)*p)*100).toFixed(1)+'%'); if(p>0.92 && hint) hint.textContent='Você viu os 9 serviços'; }
  car.addEventListener('scroll',function(){ requestAnimationFrame(upd); },{passive:true});
  window.addEventListener('resize',upd); upd();
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce||!('IntersectionObserver' in window)) return;
  var done=false;
  var io=new IntersectionObserver(function(es){ if(done||!es[0].isIntersecting||!mq.matches||car.scrollLeft>0) return; done=true; io.disconnect();
    setTimeout(function(){ car.style.scrollSnapType='none'; car.scrollTo({left:56,behavior:'smooth'}); setTimeout(function(){ car.scrollTo({left:0,behavior:'smooth'}); setTimeout(function(){ car.style.scrollSnapType=''; },700); },650); },900); },{threshold:.6});
  io.observe(car);
})();

(function(){
  // EQUIPE: etiquetas acompanham o cursor (paralaxe) no desktop; toque destaca no celular
  var ph=document.querySelector('.team-ph'); if(!ph) return;
  var tags=ph.querySelectorAll('.tag'); var depth=[14,-9];
  // depois da entrada, tira o atraso para o hover e a paralaxe responderem na hora
  if('IntersectionObserver' in window){ var so=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ so.disconnect(); setTimeout(function(){ ph.classList.add('settled'); },2600); } },{threshold:.2}); so.observe(ph); } else ph.classList.add('settled');
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var fine=window.matchMedia('(hover: hover) and (pointer: fine)').matches, raf=0, t;
  if(!fine){ /* no celular, toque destaca as etiquetas; no desktop fica só o hover (CSS) */
    ph.addEventListener('click',function(){ ph.classList.add('tapped'); clearTimeout(t); t=setTimeout(function(){ ph.classList.remove('tapped'); },900); });
  }
})();

(function(){
  // HERO: a foto sobe mais devagar que o texto ao rolar (paralaxe), depois da animação de entrada
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var hero=document.querySelector('.hero'), bg=document.querySelector('.hero-bg'); if(!hero||!bg) return;
  var on=false, tk=false;
  setTimeout(function(){ on=true; bg.style.animation='none'; upd(); },2100);
  function upd(){ tk=false; if(!on) return; var h=hero.offsetHeight, y=Math.min(Math.max(window.scrollY,0),h); bg.style.transform='translate3d(0,'+(y*0.2).toFixed(1)+'px,0) scale('+(1+y/h*0.03).toFixed(3)+')'; }
  window.addEventListener('scroll',function(){ if(!tk){ tk=true; requestAnimationFrame(upd); } },{passive:true});
})();

(function(){
  // COMO CHEGAR: troca a foto pelo mapa só quando a pessoa pede (o mapa não pesa no carregamento)
  var box=document.getElementById('visitMedia'), btn=document.getElementById('mapToggle'), slot=document.getElementById('mapSlot');
  if(!box||!btn||!slot) return;
  var lbl=btn.querySelector('.map-lbl'), loaded=false;
  // onde o mapa não pode ser embutido (prévia), o botão abre o Google Maps numa nova aba
  if(box.getAttribute('data-embed')==='0'){ lbl.textContent='Ver no mapa ↗'; btn.removeAttribute('aria-pressed'); btn.addEventListener('click',function(){ window.open('https://www.google.com/maps/search/?api=1&query=R.+Benjamin+Constant,+61,+Centro,+S%C3%A3o+Vicente+-+SP','_blank','noopener'); if(window.dataLayer) window.dataLayer.push({event:'como_chegar',cta_texto:'Ver no mapa'}); }); return; }
  btn.addEventListener('click',function(){
    var on=!box.classList.contains('show-map');
    if(on && !loaded){
      var f=document.createElement('iframe');
      f.src='https://www.google.com/maps?q=R.+Benjamin+Constant,+61,+Centro,+S%C3%A3o+Vicente+-+SP,+11310-500&z=17&output=embed';
      f.title='Mapa: Studio Alma Beauty, R. Benjamin Constant, 61, Centro, São Vicente';
      f.loading='lazy'; f.referrerPolicy='no-referrer-when-downgrade'; f.setAttribute('allowfullscreen','');
      slot.appendChild(f); loaded=true;
    }
    slot.hidden=false;
    requestAnimationFrame(function(){ box.classList.toggle('show-map',on); });
    btn.setAttribute('aria-pressed',on);
    lbl.textContent=on?'Ver foto do salão':'Ver no mapa';
    if(window.dataLayer && on) window.dataLayer.push({event:'ver_mapa'});
  });
})();



(function(){
  // AVALIAÇÕES: conta 0 → 4,9 e 0 → 81 quando a frase entra na tela (uma vez)
  var els=document.querySelectorAll('.count'); if(!els.length) return;
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)) return;
  var fmt=function(v,d){ return d? v.toFixed(d).replace('.',',') : String(Math.round(v)); };
  var lead=els[0].closest('p'); if(lead.getBoundingClientRect().top<innerHeight*0.9) return; // já visível: mantém o valor
  els.forEach(function(e){ e.textContent=fmt(0,+e.dataset.dec||0); });
  var io=new IntersectionObserver(function(es){ if(!es[0].isIntersecting) return; io.disconnect();
    var t0=performance.now(), dur=1500;
    (function step(t){ var k=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-k,3);
      els.forEach(function(el){ el.textContent=fmt(+el.dataset.to*e, +el.dataset.dec||0); });
      if(k<1) requestAnimationFrame(step); })(t0);
  },{threshold:.6});
  io.observe(lead);
})();

(function(){
  // EQUIPE: nomes aparecem digitando, logo depois de cada etiqueta surgir
  if(window.matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window)) return;
  var ph=document.querySelector('.team-ph'); if(!ph) return;
  if(ph.getBoundingClientRect().top<innerHeight*0.92) return; // já na tela ao abrir: mostra completo
  var tags=[].slice.call(ph.querySelectorAll('.tag'));
  tags.forEach(function(t){ var n=t.querySelector('.tn'); n.dataset.full=n.textContent; n.textContent=''; });
  function type(t){ var n=t.querySelector('.tn'), full=n.dataset.full, i=0; t.classList.add('typing');
    (function next(){ n.textContent=full.slice(0,++i); if(i<full.length) setTimeout(next, 55+Math.random()*45); else setTimeout(function(){ t.classList.remove('typing'); },600); })(); }
  var io=new IntersectionObserver(function(es){ if(!es[0].isIntersecting) return; io.disconnect();
    setTimeout(function(){ type(tags[0]); },1250); setTimeout(function(){ type(tags[1]); },1650); },{threshold:.2});
  io.observe(ph);
})();

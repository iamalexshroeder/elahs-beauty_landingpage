
(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var save=navigator.connection&&navigator.connection.saveData;

  // HERO: vídeo certo para cada tela; com movimento reduzido ou economia de dados fica só a capa
  var hv=document.getElementById('heroVideo');
  if(hv){
    var m=window.matchMedia('(max-width: 640px)').matches;
    hv.poster=m?hv.dataset.posterM:hv.dataset.posterD;
    if(!reduce&&!save){ hv.src=m?hv.dataset.srcM:hv.dataset.srcD; var p=hv.play(); if(p&&p.catch) p.catch(function(){}); }
  }

  // SERVIÇOS: clipe curto toca no card em foco (mouse) ou no centro da fileira (celular)
  if(!reduce&&!save){
    var cards=[].slice.call(document.querySelectorAll('.svc-card[data-video]'));
    var load=function(c){ var v=c.querySelector('video'); if(!v){ v=document.createElement('video'); v.muted=true; v.loop=true; v.playsInline=true; v.setAttribute('playsinline',''); v.setAttribute('aria-hidden','true'); v.preload='none'; v.src=c.dataset.video; c.insertBefore(v,c.querySelector('.svc-info')); } return v; };
    var play=function(c){ var v=load(c); var p=v.play(); if(p&&p.then) p.then(function(){ c.classList.add('playing'); }).catch(function(){}); };
    var stop=function(c){ var v=c.querySelector('video'); if(v){ v.pause(); } c.classList.remove('playing'); };
    if('IntersectionObserver' in window){
      // cada card toca o seu clipe enquanto está visível na tela e pausa ao sair
      var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.intersectionRatio>=.6) play(e.target); else stop(e.target); }); },{threshold:[0,.6]});
      cards.forEach(function(c){ io.observe(c); });
    }
  }

  // ANTES E DEPOIS: alça arrastável (mouse em qualquer ponto; no toque, pela alça ou com um toque na imagem)
  [].slice.call(document.querySelectorAll('.ba-item')).forEach(function(it){
    var r=it.querySelector('.ba-range');
    var set=function(v){ v=Math.max(0,Math.min(100,v)); it.style.setProperty('--p',v+'%'); r.value=Math.round(v); };
    r.addEventListener('input',function(){ set(+r.value); });
    var drag=false, startX=0, startY=0, moved=false, touch=false;
    var pos=function(e){ var b=it.getBoundingClientRect(); return (e.clientX-b.left)/b.width*100; };
    it.addEventListener('pointerdown',function(e){
      touch=e.pointerType!=='mouse'; startX=e.clientX; startY=e.clientY; moved=false;
      var b=it.getBoundingClientRect(), hx=b.left+b.width*(+r.value)/100;
      if(!touch || Math.abs(e.clientX-hx)<36){ drag=true; it.classList.add('dragging'); it.setPointerCapture(e.pointerId); if(!touch) set(pos(e)); e.preventDefault(); }
    });
    it.addEventListener('pointermove',function(e){ if(Math.abs(e.clientX-startX)>6||Math.abs(e.clientY-startY)>6) moved=true; if(drag) set(pos(e)); });
    var end=function(e){ if(drag){ drag=false; it.classList.remove('dragging'); } else if(touch&&!moved){ set(pos(e)); } };
    it.addEventListener('pointerup',end); it.addEventListener('pointercancel',function(){ drag=false; it.classList.remove('dragging'); });
  });
  var row=document.getElementById('baRow'), prev=document.getElementById('baPrev'), next=document.getElementById('baNext');
  if(row&&prev&&next){
    var step=function(){ var it=row.querySelector('.ba-item'); return it?it.getBoundingClientRect().width+24:420; };
    var upd=function(){ prev.disabled=row.scrollLeft<8; next.disabled=row.scrollLeft+row.clientWidth>=row.scrollWidth-8; };
    prev.addEventListener('click',function(){ row.scrollBy({left:-step(),behavior:reduce?'auto':'smooth'}); });
    next.addEventListener('click',function(){ row.scrollBy({left:step(),behavior:reduce?'auto':'smooth'}); });
    row.addEventListener('scroll',function(){ requestAnimationFrame(upd); },{passive:true}); window.addEventListener('resize',upd); upd();
  }

  // MAPA: pulso do alfinete quando aparece (uma vez)
  var map=document.querySelector('.map');
  if(map&&!reduce&&'IntersectionObserver' in window){ var mo=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ map.classList.add('in'); mo.disconnect(); } },{threshold:.5}); mo.observe(map); }
})();
(function(){
  // RESULTADOS: vídeos tocam só quando aparecem e pausam ao sair
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches, save=navigator.connection&&navigator.connection.saveData;
  if(reduce||save||!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){ es.forEach(function(e){ var li=e.target, v=li.querySelector('video');
    if(e.isIntersecting){ if(!v.src) v.src=v.dataset.src; var p=v.play(); if(p&&p.then) p.then(function(){ li.classList.add('playing'); }).catch(function(){}); }
    else { v.pause(); li.classList.remove('playing'); } }); },{threshold:.5});
  document.querySelectorAll('.res-vid').forEach(function(li){ io.observe(li); });
})();

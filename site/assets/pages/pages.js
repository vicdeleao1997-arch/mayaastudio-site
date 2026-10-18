/* MAYAA STUDIO · páginas internas. Reveals leves com GSAP/ScrollTrigger, header, menu, vídeo e embed sob demanda. */
(function(){
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header: fundo ao rolar e cor conforme a seção por baixo */
  var hdr = document.querySelector('.hdr');
  function onScroll(){
    if(!hdr) return;
    hdr.classList.toggle('compact', window.scrollY > 40);
    var x = Math.min(window.innerWidth-2, 60), y = Math.round(hdr.offsetHeight/2), sec = null;
    var els = document.elementsFromPoint ? document.elementsFromPoint(x, y) : [];
    for(var i=0;i<els.length;i++){ if(els[i].closest && !els[i].closest('.hdr') && !els[i].closest('#menu')){ sec = els[i].closest('.sec,.ftr'); if(sec) break; } }
    hdr.classList.toggle('on-light', !!(sec && sec.classList.contains('sec--light')));
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  onScroll();

  /* Menu mobile */
  var burger = document.querySelector('.burger'), menu = document.getElementById('menu');
  if(burger && menu){
    var toggle = function(open){
      menu.classList.toggle('open', open); burger.classList.toggle('on', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.style.overflow = open ? 'hidden' : '';
      if(hdr) hdr.classList.toggle('on-light', false);
    };
    burger.addEventListener('click', function(){ toggle(!menu.classList.contains('open')); });
    menu.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ toggle(false); }); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && menu.classList.contains('open')) toggle(false); });
  }

  /* Reveals */
  if(window.gsap && window.ScrollTrigger){
    gsap.registerPlugin(ScrollTrigger);
    root.classList.add('anim'); if(reduce) root.classList.add('rm');
    gsap.utils.toArray('.reveal').forEach(function(el){
      gsap.to(el, reduce ? {opacity:1, duration:.35, ease:'none', scrollTrigger:{trigger:el, start:'top 92%', once:true}}
                         : {opacity:1, y:0, duration:1, ease:'expo.out', scrollTrigger:{trigger:el, start:'top 90%', once:true}});
    });
    gsap.utils.toArray('.reveal-line > span').forEach(function(el, i){
      gsap.to(el, reduce ? {opacity:1, duration:.35, ease:'none', scrollTrigger:{trigger:el.parentNode, start:'top 95%', once:true}}
                         : {y:0, yPercent:0, duration:1.1, ease:'expo.out', delay:(i%3)*.06, scrollTrigger:{trigger:el.parentNode, start:'top 95%', once:true}});
    });
    window.addEventListener('load', function(){ ScrollTrigger.refresh(); });
  } else {
    root.classList.remove('anim','rm');
  }

  /* Vídeos: tocam mudos só quando visíveis; com movimento reduzido, só no clique */
  var vids = document.querySelectorAll('video[data-inview]');
  if(vids.length && 'IntersectionObserver' in window && !reduce){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        var v = en.target;
        if(en.isIntersecting){ if(v.preload === 'none') v.preload = 'metadata'; var p = v.play(); if(p && p.catch) p.catch(function(){}); }
        else if(!v.paused){ v.pause(); }
      });
    }, {threshold:.35});
    vids.forEach(function(v){ io.observe(v); });
  }

  /* Instagram: o embed oficial só carrega se a pessoa pedir (cookies de terceiros) */
  var igLoaded = false;
  document.querySelectorAll('[data-ig-load]').forEach(function(btn){
    btn.addEventListener('click', function(){
      var slot = document.getElementById(btn.getAttribute('data-ig-load'));
      if(!slot || slot.dataset.done) return;
      var url = slot.getAttribute('data-permalink');
      slot.innerHTML = '<blockquote class="instagram-media" data-instgrm-permalink="' + url + '" data-instgrm-version="14" style="background:#141414;border:0;margin:0;padding:0;width:100%"><a href="' + url + '" target="_blank" rel="noopener">Ver no Instagram</a></blockquote>';
      slot.dataset.done = '1'; btn.setAttribute('disabled', ''); btn.setAttribute('aria-disabled', 'true');
      if(window.instgrm && window.instgrm.Embeds){ window.instgrm.Embeds.process(); return; }
      if(!igLoaded){
        igLoaded = true;
        var s = document.createElement('script'); s.async = true; s.src = 'https://www.instagram.com/embed.js';
        s.onload = function(){ if(window.instgrm && window.instgrm.Embeds) window.instgrm.Embeds.process(); };
        document.body.appendChild(s);
      }
    });
  });

  /* Ano do rodapé */
  document.querySelectorAll('[data-year]').forEach(function(n){ n.textContent = new Date().getFullYear(); });
})();

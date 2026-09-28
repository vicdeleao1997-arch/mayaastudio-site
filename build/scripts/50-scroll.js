/* Rolagem: Lenis (só modo completo em desktop), parallax das faixas por ScrollTrigger scrub (sem pin), zoom da capa
   do próximo case, janela da prova (home), trilha e pilha do processo, e âncoras com desconto do cabeçalho
   (§4.2 regras 4 e 6). Nada em loop: tudo é rolagem (scrub) ou toca uma vez. */
(function () {
  var M = window.MAYAA;
  var LENIS = 'https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js';

  function loadLenis() {
    var g = M.gsap, ST = M.ST;
    var s = document.createElement('script');
    s.src = LENIS; s.async = true;
    s.onload = function () {
      try {
        if (!window.Lenis) return;
        var L = new window.Lenis({ duration: 1.1, smoothWheel: true });
        M.lenis = L;
        document.documentElement.classList.add('lenis');
        L.on('scroll', ST.update);
        g.ticker.add(function (t) { L.raf(t * 1000); });
        g.ticker.lagSmoothing(0);
        if (document.body.classList.contains('is-locked')) L.stop();
      } catch (e) { M.lenis = null; }
    };
    document.head.appendChild(s);
  }

  /* Prova (só home): a seção de tinta chega como janela que se abre (recorte lateral menor que o gutter, o texto nunca
     sai dela). Janela aberta → .4 s parado → o 12,55 conta (45 e 12 logo atrás, .12 entre eles). */
  function proof(g) {
    var pf = document.querySelector('.home .proof.sec--tinta');
    if (!pf) return;
    var held = pf.querySelectorAll('[data-hold]'), fired = 0, w = pf.querySelector('.wrap');
    var fire = function () {
      if (fired++) return;
      [].forEach.call(held, function (el, i) { M.play(el, M.T.hold + i * .12); });
    };
    var gp = function () { return Math.max(0, w.offsetLeft + parseFloat(getComputedStyle(w).paddingLeft) - 4); };
    var at = function (s) { if (s.progress === 1) fire(); };
    g.fromTo(pf, { clipPath: function () { return 'inset(0px ' + gp() + 'px 0px ' + gp() + 'px round 16px)'; } },
      { clipPath: 'inset(0px 0px 0px 0px round 0px)', ease: 'none',
        scrollTrigger: { trigger: pf, start: 'top bottom', end: 'top 40%', scrub: true, invalidateOnRefresh: true,
          onLeave: fire, onRefresh: at } });
  }

  /* Processo. >= 1024: a trilha (fio de 2 px no topo) anda com a rolagem e cada passo acende quando ela chega (o kanji
     sai da tinta nessa hora; título e texto nunca apagam). Celular: cartões presos (sticky, CSS) e o coberto encolhe
     para .94 e cai para .6 só enquanto o próximo passa por cima dele. */
  function proc(g) {
    var ol = document.querySelector('[data-proc]');
    if (!ol) return;
    var lis = [].slice.call(ol.children), n = lis.length;
    if (M.wide) {
      var ks = lis.map(function (li) { var k = li.querySelector('[data-reveal=ink]'); if (k && M.hold) M.hold(k); return k; });
      ol.classList.add('is-trail');
      g.fromTo(ol, { '--p': 0 }, { '--p': 1, ease: 'none', scrollTrigger: { trigger: ol, start: 'top 80%', end: 'bottom 60%', scrub: true,
        onUpdate: function (s) {
          lis.forEach(function (li, i) {
            var on = s.progress > i / n;
            if (on === li.classList.contains('is-lit')) return;
            li.classList.toggle('is-lit', on);
            if (on && ks[i] && M.play) M.play(ks[i]);
          });
        } } });
    } else if (matchMedia('(max-width:639px)').matches) {
      /* gatilho = a lista (não é sticky); posição natural do passo k = soma das alturas antes dele */
      var T = M.T, top = function (i) { return M.headerOffset() - 16 + i * T.stackStep; },   /* = top do sticky (10-base.css) */
        nat = function (k) { for (var y = 0, j = 0; j < k; j++) y += lis[j].offsetHeight; return y; };
      lis.slice(0, -1).forEach(function (li, i) {
        g.to(li.firstElementChild, { scale: T.stack, opacity: .6, ease: 'none', scrollTrigger: { trigger: ol,
          scrub: true, invalidateOnRefresh: true,
          start: function () { return 'top+=' + nat(i + 1) + ' ' + (top(i) + li.offsetHeight) + 'px'; },
          end: function () { return 'top+=' + nat(i + 1) + ' ' + top(i + 1) + 'px'; } } });
      });
    }
  }

  M.register('scroll', function () {
    var g = M.gsap, ST = M.ST, T = M.T;

    if (!M.reduced && g && ST) {
      document.querySelectorAll('[data-parallax]').forEach(function (el) {
        var cine = el.closest('.band--cine');   /* faixa cine: sem zoom, só 3% (cabe na sobra de 5% do CSS) */
        var y = cine ? 3 : 6, sc = cine ? 1 : 1.12;
        g.fromTo(el, { yPercent: -y, scale: sc }, {
          yPercent: y, scale: sc, ease: 'none',
          scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
        });
      });
      /* capa do próximo case: 1.12 → 1 até o bloco chegar ao centro (na <picture>: a img fica livre para o hover) */
      document.querySelectorAll('[data-zoom] picture').forEach(function (pic) {
        pic.style.display = 'block';
        g.fromTo(pic, { scale: T.img }, { scale: 1, ease: 'none',
          scrollTrigger: { trigger: pic.parentElement, start: 'top bottom', end: 'center center', scrub: true } });
      });
      proof(g);
      proc(g);
      if (M.fine) loadLenis();
    }

    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      var t = id && document.getElementById(id);
      if (!t) return;
      if (M.closeMenu) M.closeMenu(true);
      if (!M.lenis) { setTimeout(M.sweep || function () {}, 1200); return; }   /* nativo: scroll-margin-top */
      e.preventDefault();
      M.lenis.scrollTo(t, { offset: -M.headerOffset(), onComplete: function () { if (M.sweep) M.sweep(); } });
      if (history.pushState) history.pushState(null, '', '#' + id);
      if (!t.matches('a,button,input,select,textarea,[tabindex]')) t.setAttribute('tabindex', '-1');
      t.focus({ preventScroll: true });
    });

    if (ST) {
      var refresh = function () { try { ST.refresh(); } catch (e) {} };
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
      if (document.readyState === 'complete') refresh(); else window.addEventListener('load', refresh);
    }
  });
})();

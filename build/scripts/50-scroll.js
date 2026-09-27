/* Rolagem: Lenis (só modo completo em desktop), parallax das faixas por ScrollTrigger scrub (sem pin),
   "respira" só enquanto visível e âncoras com desconto do cabeçalho (§4.2 regras 4 e 6). */
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

  M.register('scroll', function () {
    var g = M.gsap, ST = M.ST;

    if ('IntersectionObserver' in window) {
      var bio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { e.target.classList.toggle('is-in', e.isIntersecting); });
      });
      document.querySelectorAll('[data-band]').forEach(function (b) { bio.observe(b); });
    }

    if (!M.reduced && g && ST) {
      document.querySelectorAll('[data-parallax]').forEach(function (el) {
        g.fromTo(el, { yPercent: -6, scale: 1.12 }, {
          yPercent: 6, scale: 1.12, ease: 'none',
          scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
        });
      });
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

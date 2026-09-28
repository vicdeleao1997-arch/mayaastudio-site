/* Motor de movimento. Só acrescenta: sem JS/GSAP ou no reduzido tudo já está no estado final.
   HTML: data-depth="-12" (yPercent com scrub; -from, -m = valor < 1024 e "0" desliga, -o = fade nos 1.os X,
   -group = 1 ScrollTrigger, -start/-end/-id, trigger [data-depth-trigger]|section) · NUNCA junto de data-reveal.
   data-focus: .is-focus no item da linha central (só toque).
   JS: M.tick(fn) · M.onScroll(fn(y,dy,dt)) · M.observe(el,fn,margem) · M.split(el,'char') · M.countPrep · M.count */
(function () {
  var M = window.MAYAA, T = M.T;

  /* um rAF (teto ~60 fps, para sozinho) e um listener de rolagem para o site; fn() === false sai do laço */
  var jobs = [], subs = [], dirty = 0, rid = 0, last = 0, sy = scrollY, st = 0;
  function kick() { if (!rid) rid = requestAnimationFrame(frame); }
  function frame(t) {
    rid = 0;
    if (last && t - last < 10) return kick();
    var dt = last ? Math.min(t - last, 100) : 16.7, i;
    last = t;
    if (dirty) {
      var y = scrollY, dy = y - sy, ds = st ? Math.min(t - st, 100) : 16.7;
      dirty = 0; sy = y; st = t;
      for (i = 0; i < subs.length; i++) subs[i](y, dy, ds);
    }
    for (i = jobs.length - 1; i >= 0; i--) if (jobs[i](t, dt) === false) jobs.splice(i, 1);
    if (jobs.length) kick(); else last = 0;
  }
  M.tick = function (fn) { if (jobs.indexOf(fn) < 0) jobs.push(fn); kick(); };
  M.onScroll = function (fn) { subs.push(fn); };
  addEventListener('scroll', function () { dirty = 1; kick(); }, { passive: true });

  /* um IntersectionObserver por margem; fn(entry) === false para de observar */
  var ios = {};
  M.observe = function (el, fn, mg) {
    if (!window.IntersectionObserver) return fn({ isIntersecting: true, target: el });
    var o = ios[mg = mg || '0px'];
    if (!o) {
      var map = new Map();
      o = ios[mg] = { map: map, io: new IntersectionObserver(function (es) {
        es.forEach(function (e) { var f = map.get(e.target); if (f && f(e) === false) { o.io.unobserve(e.target); map.delete(e.target); } });
      }, { rootMargin: mg }) };
    }
    o.map.set(el, fn); o.io.observe(el);
  };

  /* split: texto original em .sr (leitor de tela), peças .sp > .sp__in em aria-hidden. Pula quem tem link/botão.
     Só antes do 1.º paint ou fora da dobra. */
  M.split = function (el, by) {
    if (el.hasAttribute('data-split')) return el.querySelectorAll('.sp__in');
    if (el.querySelector('a,button,input')) return [];
    var sr = document.createElement('span'), vis = document.createElement('span');
    sr.className = 'sr'; sr.textContent = el.textContent.replace(/\s+/g, ' ').trim();
    vis.setAttribute('aria-hidden', 'true');
    while (el.firstChild) vis.appendChild(el.firstChild);
    (function walk(n) {
      [].slice.call(n.childNodes).forEach(function (c) {
        if (c.nodeType === 1) return walk(c);
        if (c.nodeType !== 3 || !c.nodeValue.trim()) return;
        var f = document.createDocumentFragment();
        c.nodeValue.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (!w.trim()) return f.appendChild(document.createTextNode(w));
          var sp = document.createElement('span');
          sp.className = 'sp';
          (by === 'char' ? w.split('') : [w]).forEach(function (p) {
            var s = document.createElement('span'); s.className = 'sp__in'; s.textContent = p; sp.appendChild(s);
          });
          f.appendChild(sp);
        });
        n.replaceChild(f, c);
      });
    })(vis);
    el.append(sr, vis);
    el.setAttribute('data-split', by || 'word');
    return vis.querySelectorAll('.sp__in');
  };

  /* contador: largura final presa (minWidth) → trocar dígitos não desloca nada (CLS 0).
     onUpdate(p) com p = valor/alvo, para um fio andar junto com o número. */
  function num(el, n, d) { var v = parseFloat(el.getAttribute(n)); return isNaN(v) ? d : v; }
  M.fmt = function (v, dec) { return v.toFixed(dec).replace('.', ','); };
  M.countPrep = function (el) {
    var cur = el.textContent, s = el.style;
    if (!el.hasAttribute('data-final')) el.setAttribute('data-final', cur);
    s.minWidth = ''; el.textContent = el.getAttribute('data-final');
    s.minWidth = Math.ceil(el.getBoundingClientRect().width) + 'px'; s.textAlign = 'end';
    el.textContent = cur;
  };
  M.count = function (el, o) {
    o = o || {};
    var to = num(el, 'data-to', 0), dec = num(el, 'data-dec', 0), v = { v: 0 }, up = o.onUpdate || function () {};
    var fin = el.getAttribute('data-final') || M.fmt(to, dec);
    var end = function () { el.textContent = fin; el.style.minWidth = el.style.textAlign = ''; up(1); if (o.onComplete) o.onComplete(); };
    if (M.reduced || !M.gsap) return end();
    if (!el.style.minWidth) M.countPrep(el);
    el.textContent = M.fmt(0, dec);
    return M.gsap.to(v, { v: to, duration: o.dur || T.count, ease: 'power2.out', delay: o.delay || 0, onComplete: end,
      onUpdate: function () { el.textContent = M.fmt(v.v, dec); up(to ? v.v / to : 1); } });
  };

  M.register('motor', function () {
    var g = M.gsap;
    if (!M.reduced && g && M.ST) {
      var G = {}, n = 0;
      document.querySelectorAll('[data-depth]').forEach(function (el) {
        if (el.hasAttribute('data-reveal')) return console.warn('[MAYAA] data-depth + data-reveal', el);
        var m = el.getAttribute('data-depth-m'), v = parseFloat(!M.wide && m != null ? m : el.getAttribute('data-depth')) || 0,
          op = num(el, 'data-depth-o', 0), k = el.getAttribute('data-depth-group') || n++;
        if (v || op) (G[k] = G[k] || []).push({ el: el, to: v, from: num(el, 'data-depth-from', 0), o: op });
      });
      Object.keys(G).forEach(function (k) {
        var el = G[k][0].el, a = function (x, d) { return el.getAttribute('data-depth-' + x) || d; };
        var tl = g.timeline({ defaults: { ease: 'none' }, scrollTrigger: { id: a('id', undefined), scrub: true,
          trigger: el.closest('[data-depth-trigger],section') || el.parentElement, start: a('start', 'top bottom'), end: a('end', 'bottom top') } });
        tl.to({}, { duration: 1 }, 0);
        G[k].forEach(function (d) {
          if (d.to !== d.from) tl.fromTo(d.el, { yPercent: d.from }, { yPercent: d.to, duration: 1 }, 0);
          if (d.o) tl.fromTo(d.el, { opacity: 1 }, { opacity: 0, duration: d.o }, 0);
        });
      });
    }
    /* foco por toque: linha de altura zero no centro → no máximo 1 .is-focus */
    if (M.touch && !M.reduced) document.querySelectorAll('[data-focus]').forEach(function (el) {
      M.observe(el, function (e) { el.classList.toggle('is-focus', e.isIntersecting); }, '-50% 0px -50% 0px');
    });
  });
})();

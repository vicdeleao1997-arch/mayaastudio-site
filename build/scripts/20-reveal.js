/* Revelações por IntersectionObserver (§4.1, §4.2 regras 1 a 3).
   Nada começa invisível no CSS: o estado escondido é aplicado aqui, só em quem ainda está abaixo da dobra
   (ou na dobra, se o init chegou cedo). Rede de segurança: load + 4 s, hashchange e erro → revealAll(). */
(function () {
  var M = window.MAYAA;
  var state = {                   /* el → 'wait' | 'run' | 'done' (espelhado em data-rv, útil para testes) */
    get: function (el) { return el.getAttribute('data-rv'); },
    set: function (el, v) { el.setAttribute('data-rv', v); }
  };
  var all = [];
  var io = null;
  var arm = null;   /* contadores: o número real fica no DOM e só vira 0 pouco antes de entrar na tela */

  function num(el, name, dflt) { var v = parseFloat(el.getAttribute(name)); return isNaN(v) ? dflt : v; }
  function fmt(v, dec) { return v.toFixed(dec).replace('.', ','); }
  function kids(el) { return Array.prototype.slice.call(el.children); }
  function maskParts(el) {
    var media = el.querySelector('.fig__media, .vid__frame') || el;
    return { media: media, img: media.querySelector('img, video'), cap: el.querySelector('figcaption') };
  }
  function targets(el) {
    var t = el.getAttribute('data-reveal');
    if (t === 'lines') return el.querySelectorAll('.line__in');
    if (t === 'stagger') return kids(el);
    if (t === 'mask') { var p = maskParts(el); return [el, p.media, p.img, p.cap].filter(Boolean); }
    return [el];
  }

  function hide(el) {
    var g = M.gsap, t = el.getAttribute('data-reveal'), soft = M.reduced;
    state.set(el, 'wait');
    if (t === 'lines') g.set(el.querySelectorAll('.line__in'), soft ? { yPercent: 30, opacity: 0 } : { yPercent: 150 });   /* 150: passa do respiro de .24em da .line */
    else if (t === 'fade') g.set(el, { y: soft ? 8 : num(el, 'data-y', 24), opacity: 0 });
    else if (t === 'stagger') g.set(kids(el), { y: soft ? 8 : 24, opacity: 0 });
    else if (t === 'mask') {
      if (soft) g.set(el, { opacity: 0 });
      else {
        var p = maskParts(el);
        g.set(p.media, { clipPath: 'inset(100% 0% 0% 0%)' });
        if (p.img) g.set(p.img, { scale: 1.12 });
        if (p.cap) g.set(p.cap, { opacity: 0, y: 12 });
      }
    } else if (t === 'count') {
      /* R1-03: não troca o texto por 0 aqui. Buscador, prévia de link e leitor sem CSS leem o número real;
         o 0 entra só quando o contador está a 35% da tela de aparecer (arm) ou no início da contagem (play). */
      if (!el.hasAttribute('data-final')) el.setAttribute('data-final', el.textContent);
      if (arm) arm.observe(el);
    }
  }

  function done(el) { state.set(el, 'done'); }

  function play(el) {
    var g = M.gsap, t = el.getAttribute('data-reveal'), soft = M.reduced;
    if (state.get(el) !== 'wait') return;
    state.set(el, 'run');
    var d = num(el, 'data-delay', 0);
    var fin = function () { done(el); };
    if (t === 'lines') {
      g.to(el.querySelectorAll('.line__in'), soft
        ? { yPercent: 0, opacity: 1, duration: 0.5, ease: 'power2.out', stagger: 0.06, delay: d, clearProps: 'transform,opacity', onComplete: fin }
        : { yPercent: 0, duration: 0.9, ease: 'expo.out', stagger: 0.08, delay: d, clearProps: 'transform', onComplete: fin });
    } else if (t === 'fade') {
      g.to(el, { y: 0, opacity: 1, duration: soft ? 0.45 : num(el, 'data-dur', 0.8), ease: soft ? 'power2.out' : 'expo.out',
        delay: d, clearProps: 'transform,opacity', onComplete: fin });
    } else if (t === 'stagger') {
      g.to(kids(el), { y: 0, opacity: 1, duration: soft ? 0.45 : 0.8, ease: soft ? 'power2.out' : 'expo.out',
        stagger: 0.06, delay: d, clearProps: 'transform,opacity', onComplete: fin });
    } else if (t === 'mask') {
      if (soft) { g.to(el, { opacity: 1, duration: 0.5, ease: 'power1.out', delay: d, clearProps: 'opacity', onComplete: fin }); return; }
      var p = maskParts(el);
      g.to(p.media, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power2.inOut', delay: d, clearProps: 'clipPath', onComplete: fin });
      if (p.img) g.to(p.img, { scale: 1, duration: 1.4, ease: 'expo.out', delay: d, clearProps: 'transform' });
      if (p.cap) g.to(p.cap, { opacity: 1, y: 0, duration: 0.8, ease: 'expo.out', delay: d + 0.35, clearProps: 'transform,opacity' });
    } else if (t === 'count') {
      var to = num(el, 'data-to', 0), dec = num(el, 'data-dec', 0), o = { v: 0 };
      var final = el.getAttribute('data-final') || fmt(to, dec);
      if (arm) { try { arm.unobserve(el); } catch (e) {} }
      el.textContent = fmt(0, dec);
      g.to(o, { v: to, duration: soft ? 1.0 : 1.6, ease: 'power2.out', delay: d,
        onUpdate: function () { el.textContent = fmt(o.v, dec); },
        onComplete: function () { el.textContent = final; fin(); } });
    } else fin();
  }

  function finish(el) {
    var g = M.gsap;
    if (state.get(el) === 'done') return;
    if (g) {
      var t = targets(el);
      g.killTweensOf(t);
      g.set(t, { clearProps: 'transform,opacity,clipPath' });
    }
    if (el.getAttribute('data-reveal') === 'count') {
      if (arm) { try { arm.unobserve(el); } catch (e) {} }
      if (el.hasAttribute('data-final')) el.textContent = el.getAttribute('data-final');
    }
    done(el);
  }

  function sweep() {
    var vh = window.innerHeight;
    all.forEach(function (el) {
      var s = state.get(el);
      if (s !== 'wait') return;
      if (el.getBoundingClientRect().top < vh) { if (io) io.unobserve(el); finish(el); }
    });
  }
  M.sweep = sweep;
  M.revealAll = function () {
    all.forEach(function (el) { if (io) { try { io.unobserve(el); } catch (e) {} } finish(el); });
  };

  M.register('reveal', function () {
    all = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
    if (!M.gsap || !('IntersectionObserver' in window)) { all.forEach(done); return; }
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { io.unobserve(en.target); play(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    arm = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var el = en.target;
        if (!en.isIntersecting) return;
        arm.unobserve(el);
        if (state.get(el) === 'wait') el.textContent = fmt(0, num(el, 'data-dec', 0));
      });
    }, { rootMargin: '0px 0px 35% 0px' });
    var vh = window.innerHeight;
    var late = M.LATE || M.painted();          /* reavaliado aqui: o boot pode vir depois do 1.º paint */
    all.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom <= 0 && r.top <= 0 && (r.width || r.height)) { done(el); return; }   /* já passou: fica visível */
      if (!r.width && !r.height) { done(el); return; }                                /* escondido por CSS */
      if (r.top < vh) {                                                                /* na dobra */
        if (late) { done(el); return; }
        hide(el); play(el); return;
      }
      hide(el); io.observe(el);
    });
    var later = function () { setTimeout(sweep, 4000); };
    if (document.readyState === 'complete') later(); else window.addEventListener('load', later);
    window.addEventListener('hashchange', function () { sweep(); setTimeout(sweep, 1200); });
  });
})();

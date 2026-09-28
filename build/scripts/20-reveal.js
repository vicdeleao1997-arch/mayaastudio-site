/* Revelações por IntersectionObserver (§4.1, §4.2 regras 1 a 3).
   Nada começa invisível no CSS: o estado escondido é aplicado aqui, só em quem ainda está abaixo da dobra
   (ou na dobra, se o init chegou cedo). Rede de segurança: load + 4 s, hashchange e erro → revealAll().
   Movimento reduzido: nada se esconde (estado final desde o 1.º paint). Botão e link do direct nunca se escondem nem
   entram em cascata. Tokens de duração e curva: M.T (00-env.js).
   Tipos: lines · fade (data-y, data-yp = yPercent) · stagger (data-y, data-st, data-rule, data-arr) · mask
   (data-mask="box" = cinema, data-noscale) · ink (tinta de cima; data-from="bottom") · count (data-rule, data-land,
   data-hold = espera M.play) · rule (fio de rótulo sem título depois). */
(function () {
  var M = window.MAYAA;
  var state = {                   /* el → 'wait' | 'run' | 'done' (espelhado em data-rv, útil para testes) */
    get: function (el) { return el.getAttribute('data-rv'); },
    set: function (el, v) { el.setAttribute('data-rv', v); }
  };
  var all = [];
  var io = null;
  var arm = null;   /* contadores: o número real fica no DOM e só vira 0 pouco antes de entrar na tela */
  var DM = '[data-magnet],a[href^="https://ig.me/"]';   /* direct: sempre visível */
  var INK = { top: 'inset(0% 0% 100% 0%)', bottom: 'inset(100% 0% 0% 0%)' }, OPEN = 'inset(0% 0% 0% 0%)';

  function num(el, name, dflt) { var v = parseFloat(el.getAttribute(name)); return isNaN(v) ? dflt : v; }
  function has(el, a) { return el.hasAttribute(a); }
  function mag(el) { return el.matches(DM) || !!el.querySelector(DM); }
  function kids(el) { return Array.prototype.slice.call(el.children).filter(function (k) { return !mag(k); }); }
  function maskParts(el) {
    var media = el.querySelector('.fig__media, .vid__frame') || el;
    return { media: media, img: has(el, 'data-noscale') ? null : media.querySelector('img, video'), cap: el.querySelector('figcaption') };
  }
  /* extras do contador: fio (.proof__rule) e o × que pousa no fim */
  function cx(el) {
    var p = el.parentElement;
    return { rule: has(el, 'data-rule') ? p.querySelector('.proof__rule') : null, x: has(el, 'data-land') ? p.querySelector('.proof__x') : null };
  }
  function targets(el) {
    var t = el.getAttribute('data-reveal');
    if (t === 'lines') return [].slice.call(el.querySelectorAll('.line__in')).concat(el._rule || []);
    if (t === 'stagger') return kids(el);
    if (t === 'mask') { var p = maskParts(el); return [el, p.media, p.img, p.cap].filter(Boolean); }
    if (t === 'count') { var c = cx(el); return [el, c.rule, c.x].filter(Boolean); }
    return [el];
  }
  /* props de entrada da cascata: fio (--r) e seta do caminho (--ax, só onde as setas são horizontais) */
  function kidFrom(el) {
    var o = { y: num(el, 'data-y', M.T.y), opacity: 0 };
    if (has(el, 'data-rule')) o['--r'] = 0;
    if (has(el, 'data-arr') && M.wide) o['--ax'] = '-8px';
    return o;
  }

  function hide(el) {
    var g = M.gsap, t = el.getAttribute('data-reveal'), T = M.T;
    state.set(el, 'wait');
    if (t === 'lines') {
      g.set(el.querySelectorAll('.line__in'), { yPercent: T.lines });   /* 150: passa do respiro de .24em da .line */
      if (el._rule) g.set(el._rule, { '--r': 0 });
    } else if (t === 'fade') g.set(el, { y: num(el, 'data-y', T.y), yPercent: num(el, 'data-yp', 0), opacity: 0 });
    else if (t === 'stagger') g.set(kids(el), kidFrom(el));
    else if (t === 'mask') {
      var p = maskParts(el);
      g.set(p.media, { clipPath: el.getAttribute('data-mask') === 'box' ? 'inset(14% 0% 14% 0%)' : INK.bottom });
      if (p.img) g.set(p.img, { scale: T.img });
      if (p.cap) g.set(p.cap, { opacity: 0, y: 12 });
    } else if (t === 'ink') g.set(el, { clipPath: INK[el.getAttribute('data-from')] || INK.top });
    else if (t === 'rule') g.set(el, { '--r': 0 });
    else if (t === 'count') {
      /* R1-03: não troca o texto por 0 aqui. Buscador, prévia de link e leitor sem CSS leem o número real;
         o 0 entra só quando o contador está a 35% da tela de aparecer (arm) ou no início da contagem (play).
         countPrep prende a largura final (minWidth): a troca de dígitos não desloca nada (CLS 0). */
      var c = cx(el);
      M.countPrep(el);
      if (c.rule) c.rule.style.transform = 'scaleX(0)';
      if (c.x) g.set(c.x, { yPercent: 40, opacity: 0 });
      if (arm) arm.observe(el);
    }
  }

  function done(el) { state.set(el, 'done'); }

  function play(el, dl) {
    var g = M.gsap, t = el.getAttribute('data-reveal'), T = M.T;
    if (state.get(el) !== 'wait') return;
    state.set(el, 'run');
    var d = dl == null ? num(el, 'data-delay', 0) : dl;
    var fin = function () { done(el); };
    if (t === 'lines') {
      /* o fio do rótulo "puxa" o título: começa no mesmo frame da 1.ª linha */
      var ls = el.querySelectorAll('.line__in');
      if (el._rule) g.to(el._rule, { '--r': 1, duration: T.d4, ease: T.out, delay: d, clearProps: '--r' });
      g.to(ls, { yPercent: 0, duration: T.d5, ease: T.out, stagger: M.stagger(ls.length, T.sLine), delay: d, clearProps: 'transform', onComplete: fin });
    } else if (t === 'fade') {
      g.to(el, { y: 0, yPercent: 0, opacity: 1, duration: num(el, 'data-dur', T.d4), ease: T.out, delay: d, clearProps: 'transform,opacity', onComplete: fin });
    } else if (t === 'stagger') {
      var ks = kids(el), to = { y: 0, opacity: 1, duration: T.d4, ease: T.out, delay: d, onComplete: fin,
        stagger: M.stagger(ks.length, num(el, 'data-st', T.sList)), clearProps: 'transform,opacity,--r,--ax' };
      if (has(el, 'data-rule')) to['--r'] = 1;
      if (has(el, 'data-arr') && M.wide) to['--ax'] = '0px';
      g.to(ks, to);
    } else if (t === 'mask') {
      /* mídia e imagem dividem uma só intenção: .9 s expo.out nas duas */
      var p = maskParts(el);
      g.to(p.media, { clipPath: OPEN, duration: T.d5, ease: T.out, delay: d, clearProps: 'clipPath', onComplete: fin });
      if (p.img) g.to(p.img, { scale: 1, duration: T.d5, ease: T.out, delay: d, clearProps: 'transform' });
      if (p.cap) g.to(p.cap, { opacity: 1, y: 0, duration: T.d4, ease: T.out, delay: d + 0.35, clearProps: 'transform,opacity' });
    } else if (t === 'ink') {
      g.to(el, { clipPath: OPEN, duration: T.d4, ease: T.out, delay: d, clearProps: 'clipPath', onComplete: fin });
    } else if (t === 'rule') {
      g.to(el, { '--r': 1, duration: T.d4, ease: T.out, delay: d, clearProps: '--r', onComplete: fin });
    } else if (t === 'count') {
      if (arm) { try { arm.unobserve(el); } catch (e) {} }
      var c = cx(el);
      /* o fio anda no MESMO tween do número; no frame em que a contagem acaba, o × pousa (back.out só aqui) */
      M.count(el, { delay: d, onUpdate: function (k) { if (c.rule) c.rule.style.transform = k < 1 ? 'scaleX(' + k + ')' : ''; },
        onComplete: function () {
          if (c.x) g.to(c.x, { yPercent: 0, opacity: 1, duration: T.d3, ease: T.land, clearProps: 'transform,opacity' });
          fin();
        } });
    } else fin();
  }

  function finish(el) {
    var g = M.gsap;
    if (state.get(el) === 'done') return;
    if (g) {
      var t = targets(el);
      g.killTweensOf(t);
      g.set(t, { clearProps: 'transform,opacity,clipPath,--r,--ax' });
    }
    if (el.getAttribute('data-reveal') === 'count') {
      if (arm) { try { arm.unobserve(el); } catch (e) {} }
      if (has(el, 'data-final')) el.textContent = el.getAttribute('data-final');
      el.style.minWidth = el.style.textAlign = '';
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
  /* para quem comanda a própria entrada (janela da prova, trilha do processo): tira do IO e toca na hora certa */
  M.hold = function (el) { if (io) { try { io.unobserve(el); } catch (e) {} } };
  M.play = function (el, d) { M.hold(el); play(el, d); };

  /* fio do rótulo: pareado com o título que vem logo depois (mesmo frame); sem título, entra sozinho ('rule') */
  function pair(lab) {
    for (var s = lab.nextElementSibling, i = 0; s && i < 3; s = s.nextElementSibling, i++) {
      var t = s.matches('[data-reveal=lines]') ? s : s.querySelector('[data-reveal=lines]');
      if (t) return t;
    }
    return null;
  }

  M.register('reveal', function () {
    if (M.reduced || !M.gsap || !('IntersectionObserver' in window)) {
      [].forEach.call(document.querySelectorAll('[data-reveal]'), done); return;
    }
    [].forEach.call(document.querySelectorAll('.label--rule:not([data-reveal])'), function (lab) {
      var t = pair(lab);
      if (t && !t._rule) t._rule = lab; else lab.setAttribute('data-reveal', 'rule');
    });
    all = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
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
        if (state.get(el) === 'wait') el.textContent = M.fmt(0, num(el, 'data-dec', 0));
      });
    }, { rootMargin: '0px 0px 35% 0px' });
    var vh = window.innerHeight;
    var late = M.LATE || M.painted();          /* reavaliado aqui: o boot pode vir depois do 1.º paint */
    all.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom <= 0 && r.top <= 0 && (r.width || r.height)) { done(el); return; }   /* já passou: fica visível */
      if (!r.width && !r.height) { done(el); return; }                                /* escondido por CSS */
      if (mag(el) && el.getAttribute('data-reveal') !== 'stagger') { done(el); return; }   /* direct: nunca escondido */
      if (M.vtIn && (el.closest('[data-vt-open]') || el.querySelector('[data-vt-open]'))) { done(el); return; }   /* recebe o morph 'obra' */
      if (!M.wide && el.closest('.mq--logos')) { done(el); return; }                 /* parede só >= 1024; abaixo é a esteira */
      if (r.top < vh) {                                                                /* na dobra */
        if (late) { done(el); return; }
        hide(el); play(el); return;
      }
      hide(el);
      if (!has(el, 'data-hold') || !M.ST) io.observe(el);   /* data-hold: quem toca é a janela da prova (50-scroll.js) */
    });
    var later = function () { setTimeout(sweep, 4000); };
    if (document.readyState === 'complete') later(); else window.addEventListener('load', later);
    window.addEventListener('hashchange', function () { sweep(); setTimeout(sweep, 1200); });
  });
})();

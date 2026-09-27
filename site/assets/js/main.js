/* 00-env.js */
/* Ambiente e modos (§4.1): completo × suave (prefers-reduced-motion) × sem GSAP. */
(function () {
  var M = window.MAYAA = window.MAYAA || {};
  var html = document.documentElement;
  var mq = function (q) { try { return window.matchMedia(q).matches; } catch (e) { return false; } };

  M.t0 = performance.now();
  /* A página já foi pintada (1.º paint com conteúdo)? Então o que está na dobra fica como está: esconder para
     animar de novo faria o conteúdo piscar (aparece, some ~250 ms, volta) em rede média e no modo suave. */
  M.painted = function () {
    try { return performance.getEntriesByName('first-contentful-paint').length > 0; } catch (e) { return false; }
  };
  M.LATE = M.t0 > 900 || M.painted();         /* init tardio: o que já está na tela não anima */
  M.reduced = mq('(prefers-reduced-motion: reduce)');
  M.fine = mq('(hover: hover) and (pointer: fine)');
  M.wide = mq('(min-width: 1024px)');
  var conn = navigator.connection || {};
  M.saveData = !!conn.saveData;
  M.gsap = window.gsap || null;
  M.ST = window.ScrollTrigger || null;
  if (M.gsap && M.ST) { try { M.gsap.registerPlugin(M.ST); } catch (e) {} }
  M.mode = M.reduced ? 'suave' : 'completo';

  M.webglOK = function () {
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
    } catch (e) { return false; }
  };
  M.fxOK = !M.reduced && M.fine && M.wide && !M.saveData && M.webglOK();

  html.classList.add('js', 'mode-' + M.mode);
  if (M.fxOK) html.classList.add('fx-on');
  if (!M.gsap) html.classList.add('no-gsap');

  M.headerOffset = function () {
    var cs = getComputedStyle(html);
    var px = function (v) { var d = document.createElement('div'); d.style.height = v; d.style.position = 'absolute';
      d.style.visibility = 'hidden'; document.body.appendChild(d); var h = d.getBoundingClientRect().height; d.remove(); return h; };
    return px(cs.getPropertyValue('--header-h')) + px(cs.getPropertyValue('--frame')) + 16;
  };

  M.mods = [];
  M.register = function (name, fn) { M.mods.push([name, fn]); };
})();

/* 10-header.js */
/* Cabeçalho (some ao descer, volta ao subir) e menu em tela cheia com foco preso (§2.7.1). */
(function () {
  var M = window.MAYAA;
  M.register('header', function () {
    var hd = document.querySelector('[data-header]');
    if (!hd) return;
    var menu = document.getElementById('menu');
    var openBtn = hd.querySelector('.hd__menu');
    var closeBtn = menu && menu.querySelector('.menu__close');
    var lastY = window.scrollY, ticking = false, isOpen = false;
    if (M.reduced) hd.style.transitionDuration = 'var(--dur-1)';

    function update() {
      ticking = false;
      var y = window.scrollY;
      hd.classList.toggle('is-scrolled', y > 24);
      var focusInside = hd.contains(document.activeElement);
      if (!isOpen && !focusInside && y > 400 && y > lastY + 2) hd.classList.add('is-hidden');
      else if (y < lastY - 2 || y <= 400 || isOpen || focusInside) hd.classList.remove('is-hidden');
      lastY = y;
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    hd.addEventListener('focusin', function () { hd.classList.remove('is-hidden'); });
    update();

    if (!menu || !openBtn) return;
    var focusables = function () {
      return Array.prototype.slice.call(menu.querySelectorAll('a[href], button:not([disabled])'))
        .filter(function (el) { return el.offsetParent !== null || el === closeBtn; });
    };
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables(); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    function open() {
      if (isOpen) return;
      isOpen = true;
      menu.hidden = false;
      openBtn.setAttribute('aria-expanded', 'true');
      document.body.classList.add('is-locked');
      if (M.lenis) M.lenis.stop();
      document.addEventListener('keydown', onKey);
      var g = M.gsap;
      if (g) {
        var links = menu.querySelectorAll('.menu__list li');
        if (M.reduced) g.fromTo(menu, { opacity: 0 }, { opacity: 1, duration: 0.2, clearProps: 'opacity' });
        else {
          g.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 0.6, ease: 'expo.out', clearProps: 'clipPath' });
          g.fromTo(links, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out', stagger: 0.04, delay: 0.1, clearProps: 'transform,opacity' });
        }
      }
      (closeBtn || focusables()[0]).focus();
    }
    function close(noFocus) {
      if (!isOpen) return;
      isOpen = false;
      menu.hidden = true;
      openBtn.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-locked');
      if (M.lenis) M.lenis.start();
      document.removeEventListener('keydown', onKey);
      if (!noFocus) openBtn.focus();
    }
    M.closeMenu = close;
    openBtn.addEventListener('click', function () { isOpen ? close() : open(); });
    if (closeBtn) closeBtn.addEventListener('click', function () { close(); });
    menu.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (a) close(true);
    });
    window.addEventListener('resize', function () { if (isOpen && window.innerWidth >= 900) close(true); });
  });
})();

/* 20-reveal.js */
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

/* 30-media.js */
/* Vídeo só visível, "Copiar e-mail", Instagram por clique e FAQ animado (§2.7.4, §2.7.21, §2.7.24, §2.7.25). */
(function () {
  var M = window.MAYAA;

  function vbtn(cls, txt) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'vid__btn label ' + cls; b.textContent = txt;
    return b;
  }
  function tocar(v, falhou) { var p = v.play(); if (p && p.catch) p.catch(falhou || function () {}); }

  /* Sem JS: controles nativos. Modo suave, economia de dados ou sem IntersectionObserver: nada toca sozinho; pôster
     limpo + botão da marca ("Ver filme" + triângulo em SVG) e os controles do navegador só depois do clique.
     Modo completo: toca mudo só quando ≥50% visível, com Pausar/Continuar (WCAG 2.2.2) e Ativar som; clicar no
     vídeo também pausa e continua. Pausa pedida pela pessoa não é desfeita pela rolagem. */
  M.register('video', function () {
    var vids = Array.prototype.slice.call(document.querySelectorAll('video[data-autoplay]'));
    if (!vids.length) return;
    var auto = !M.reduced && !M.saveData && ('IntersectionObserver' in window);
    vids.forEach(function (v) {
      var frame = v.parentElement;
      v.muted = true; v.defaultMuted = true;
      v.removeAttribute('controls');

      if (!auto) {
        var go = vbtn('vid__play', '');
        go.appendChild(document.createTextNode((v.getAttribute('data-play') || 'Ver filme') + ' '));
        var tri = document.createElement('span'); tri.setAttribute('aria-hidden', 'true'); tri.className = 'vid__tri';
        /* U+25B6 (play) não existe na Archivo nem na Shippori (caía na Segoe UI): triângulo em traço, SVG (R1-04) */
        tri.innerHTML = '<svg class="ico ico--play" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false"><path d="M2.2 1.2v7.6L8.8 5z"/></svg>';
        go.appendChild(tri);
        go.addEventListener('click', function () {
          v.setAttribute('controls', ''); v.preload = 'auto';
          go.remove(); v.focus(); tocar(v);
        });
        frame.appendChild(go);
        return;
      }

      var bar = document.createElement('div');
      bar.className = 'vid__bar';
      var bp = vbtn('vid__pause', 'Pausar'); bp.setAttribute('aria-pressed', 'false');
      var bs = vbtn('vid__sound', 'Ativar som');
      bar.appendChild(bp); bar.appendChild(bs);
      frame.appendChild(bar);
      frame.classList.add('is-auto');
      var held = false;                                   /* pausado pela pessoa */
      var restore = function () { v.setAttribute('controls', ''); frame.classList.remove('is-auto'); if (bar.parentNode) bar.remove(); };
      var sync = function () {
        var p = v.paused;
        bp.textContent = p ? 'Continuar' : 'Pausar';
        bp.setAttribute('aria-pressed', String(p));
      };
      v.addEventListener('play', sync);
      v.addEventListener('pause', sync);
      var toggle = function () {
        if (v.paused) { held = false; tocar(v, restore); } else { held = true; v.pause(); }
      };
      bp.addEventListener('click', toggle);
      v.addEventListener('click', toggle);
      bs.addEventListener('click', function () {
        v.muted = !v.muted;
        bs.textContent = v.muted ? 'Ativar som' : 'Desligar som';
      });
      var pre = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { v.preload = 'auto'; pre.disconnect(); } });
      }, { rootMargin: '100% 0px 100% 0px' });
      pre.observe(v);
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && e.intersectionRatio >= 0.5) { if (!held) tocar(v, restore); }
          else if (!v.paused) v.pause();
        });
      }, { threshold: [0, 0.5, 0.75] });
      io.observe(v);
      v.addEventListener('error', restore, true);
    });
  });

  M.register('mail', function () {
    if (!(navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext)) return;
    document.querySelectorAll('[data-copy]').forEach(function (b) {
      b.hidden = false;
      var st = b.parentElement.querySelector('[data-copy-status]');
      var timer = null;
      b.addEventListener('click', function () {
        navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {
          b.textContent = 'Copiado';
          if (st) st.textContent = 'E-mail copiado';
          clearTimeout(timer);
          timer = setTimeout(function () { b.textContent = 'Copiar e-mail'; if (st) st.textContent = ''; }, 2000);
        }).catch(function () {});
      });
    });
  });

  M.register('ig', function () {
    document.querySelectorAll('[data-ig-load]').forEach(function (b) {
      b.addEventListener('click', function () {
        var box = b.closest('[data-ig-src]');
        if (!box) return;
        var kind = box.getAttribute('data-ig-kind');
        var f = document.createElement('iframe');
        f.src = box.getAttribute('data-ig-src');
        f.title = 'Instagram: ' + (box.getAttribute('data-ig-what') || 'conteúdo');
        f.width = '100%'; f.height = kind === 'post' ? '620' : '740';
        f.loading = 'lazy'; f.className = 'ig__frame';
        f.setAttribute('allow', 'encrypted-media; picture-in-picture');
        f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
        var link = box.querySelector('.link-arrow');
        var wrap = document.createElement('div');
        wrap.className = 'ig-loaded';
        wrap.appendChild(f);
        if (link) { var p = document.createElement('p'); p.className = 'ig__after'; p.appendChild(link); wrap.appendChild(p); }
        box.replaceWith(wrap);
        f.focus();
        if (M.ST) setTimeout(function () { M.ST.refresh(); }, 300);
      });
    });
  });

  M.register('faq', function () {
    var items = document.querySelectorAll('.faq__item');
    if (!items.length) return;
    items.forEach(function (d) {
      d.addEventListener('toggle', function () { if (M.ST) M.ST.refresh(); });
    });
    var g = M.gsap;
    if (!g || M.reduced) return;
    items.forEach(function (d) {
      var s = d.querySelector('summary'), a = d.querySelector('.faq__a');
      if (!s || !a) return;
      s.addEventListener('click', function (e) {
        e.preventDefault();
        g.killTweensOf(a);
        if (d.open) {
          g.to(a, { height: 0, duration: 0.4, ease: 'power2.inOut',
            onComplete: function () { d.open = false; g.set(a, { clearProps: 'height' }); } });
        } else {
          d.open = true;
          g.fromTo(a, { height: 0 }, { height: 'auto', duration: 0.4, ease: 'power2.out', clearProps: 'height' });
        }
      });
    });
  });
})();

/* 40-marquee.js */
/* Marquee de logos e de texto: só CSS; aqui o botão Pausar/Continuar e a pausa fora da tela (§2.7.7). */
(function () {
  var M = window.MAYAA;
  M.register('marquee', function () {
    document.querySelectorAll('[data-marquee]').forEach(function (m) {
      var b = m.querySelector('.mq__toggle');
      if (b) b.addEventListener('click', function () {
        var p = m.classList.toggle('is-paused');
        b.setAttribute('aria-pressed', String(p));
        b.textContent = p ? 'Continuar' : 'Pausar';
      });
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (e) { m.classList.toggle('is-off', !e.isIntersecting); });
        }).observe(m);
      }
    });
  });
})();

/* 50-scroll.js */
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

/* 60-fx.js */
/* Distorção WebGL leve no hover das imagens [data-fx="distort"] (§4.2 regra 7).
   Só modo completo, desktop com mouse, ≥1024 px, sem save-data. OGL carrega no 1.º pointerenter.
   Um canvas fixo reaproveitado sobre a imagem sob o ponteiro; deslocamento radial pela velocidade do ponteiro,
   força máxima 0,035 em UV, sem separação de cor. Falhou: tira `fx-on` e o hover CSS volta. */
(function () {
  var M = window.MAYAA;
  var OGL = 'https://cdn.jsdelivr.net/npm/ogl@1.0.11/+esm';
  var VERT = 'attribute vec2 uv;attribute vec2 position;varying vec2 vUv;' +
    'void main(){vUv=uv;gl_Position=vec4(position,0.,1.);}';
  var FRAG = 'precision highp float;uniform sampler2D tMap;uniform vec2 uMouse;uniform vec2 uVel;uniform float uStrength;' +
    'uniform vec2 uScale;uniform vec2 uOffset;uniform float uAspect;varying vec2 vUv;' +
    'void main(){vec2 d=vUv-uMouse;d.x*=uAspect;float f=smoothstep(.5,0.,length(d));' +
    'vec2 uv=vUv-uVel*f*uStrength*.035;uv=clamp(uv,0.,1.)*uScale+uOffset;gl_FragColor=texture2D(tMap,uv);}';

  M.register('fx', function () {
    if (!M.fxOK) return;
    var els = document.querySelectorAll('[data-fx="distort"]');
    if (!els.length) return;
    var fx = null, loading = null, failed = false;

    function fail() {
      failed = true;
      document.documentElement.classList.remove('fx-on');
      if (fx && fx.canvas && fx.canvas.parentNode) fx.canvas.remove();
      fx = null;
    }
    function load() {
      if (!loading) loading = import(OGL).then(function (ogl) { try { fx = build(ogl); } catch (e) { fail(); } }).catch(fail);
      return loading;
    }

    function build(ogl) {
      var renderer = new ogl.Renderer({ dpr: Math.min(window.devicePixelRatio || 1, 2), alpha: true, antialias: false });
      var gl = renderer.gl;
      if (!gl) throw new Error('sem WebGL');
      var canvas = gl.canvas;
      canvas.className = 'fx-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      document.body.appendChild(canvas);
      var tex = new ogl.Texture(gl, { generateMipmaps: false, minFilter: gl.LINEAR });
      var U = {
        tMap: { value: tex }, uMouse: { value: [0.5, 0.5] }, uVel: { value: [0, 0] }, uStrength: { value: 0 },
        uScale: { value: [1, 1] }, uOffset: { value: [0, 0] }, uAspect: { value: 1 }
      };
      var prog = new ogl.Program(gl, { vertex: VERT, fragment: FRAG, uniforms: U, transparent: true });
      var mesh = new ogl.Mesh(gl, { geometry: new ogl.Triangle(gl), program: prog });
      var cur = null, img = null, raf = 0, w = 0, h = 0;
      var mouse = { x: 0.5, y: 0.5, px: null, py: null }, vel = [0, 0], target = [0, 0];
      var strength = 0, goal = 0;

      function cover() {
        var nw = img.naturalWidth, nh = img.naturalHeight, r = img.getBoundingClientRect();
        var fit = getComputedStyle(img).objectFit;
        if (fit === 'cover' && nw && nh) {
          var s = Math.max(r.width / nw, r.height / nh);
          var fx_ = r.width / (nw * s), fy = r.height / (nh * s);
          U.uScale.value = [fx_, fy]; U.uOffset.value = [(1 - fx_) / 2, (1 - fy) / 2];
        } else { U.uScale.value = [1, 1]; U.uOffset.value = [0, 0]; }
      }
      function frame() {
        raf = 0;
        if (!img) return;
        var r = img.getBoundingClientRect();
        if (Math.round(r.width) !== w || Math.round(r.height) !== h) {
          w = Math.round(r.width); h = Math.round(r.height);
          renderer.setSize(w, h);
          cover();
        }
        canvas.style.transform = 'translate(' + r.left + 'px,' + r.top + 'px)';
        target[0] *= 0.9; target[1] *= 0.9;
        vel[0] += (target[0] - vel[0]) * 0.15; vel[1] += (target[1] - vel[1]) * 0.15;
        strength += (goal - strength) * (goal > strength ? 0.12 : 0.09);
        U.uVel.value = vel; U.uStrength.value = strength;
        U.uMouse.value = [mouse.x, mouse.y]; U.uAspect.value = w / Math.max(h, 1);
        renderer.render({ scene: mesh });
        if (goal === 0 && strength < 0.01) { canvas.style.visibility = 'hidden'; img = null; cur = null; return; }
        raf = requestAnimationFrame(frame);
      }
      function kick() { if (!raf) raf = requestAnimationFrame(frame); }

      return {
        canvas: canvas,
        enter: function (el, e) {
          var i = el.querySelector('img');
          if (!i || !i.complete || !i.naturalWidth) return;
          if (img !== i) { img = i; tex.image = i; w = h = 0; }
          cur = el; goal = 1; mouse.px = null;
          this.move(e);
          canvas.style.visibility = 'visible';
          kick();
        },
        move: function (e) {
          if (!img || !e) return;
          var r = img.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width, y = 1 - (e.clientY - r.top) / r.height;
          if (mouse.px !== null) {
            target[0] = Math.max(-1, Math.min(1, (x - mouse.px) * 14));
            target[1] = Math.max(-1, Math.min(1, (y - mouse.py) * 14));
          }
          mouse.px = x; mouse.py = y; mouse.x = x; mouse.y = y;
          kick();
        },
        leave: function (el) { if (el === cur) { goal = 0; kick(); } }
      };
    }

    els.forEach(function (el) {
      el.addEventListener('pointerenter', function (e) {
        if (failed || e.pointerType !== 'mouse') return;
        load().then(function () { if (fx) fx.enter(el, e); });
      });
      el.addEventListener('pointermove', function (e) { if (fx) fx.move(e); });
      el.addEventListener('pointerleave', function () { if (fx) fx.leave(el); });
    });
  });
})();

/* 70-legal.js */
/* Política de privacidade (grupo legal-seo): marca no índice lateral o tópico que está sendo lido
   (o último cujo topo já passou de 35% da altura da janela). Só marcação (aria-current="location");
   nada se move, vale igual nos modos completo e suave. */
(function () {
  var M = window.MAYAA;
  if (!M || !M.register) return;
  M.register('legal-toc', function () {
    var nav = document.querySelector('[data-priv-toc]');
    if (!nav) return;
    var items = [];
    Array.prototype.forEach.call(nav.querySelectorAll('a[href^="#"]'), function (a) {
      var el = document.getElementById(a.getAttribute('href').slice(1));
      if (el) items.push({ a: a, el: el });
    });
    if (!items.length) return;
    var atual = null, pendente = false;
    function mark() {
      pendente = false;
      var linha = window.innerHeight * 0.35, alvo = null;
      for (var i = 0; i < items.length; i++) {
        if (items[i].el.getBoundingClientRect().top <= linha) alvo = items[i]; else break;
      }
      if (alvo === atual) return;
      if (atual) atual.a.removeAttribute('aria-current');
      if (alvo) alvo.a.setAttribute('aria-current', 'location');
      atual = alvo;
    }
    function onScroll() { if (!pendente) { pendente = true; window.requestAnimationFrame(mark); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    mark();
  });
})();

/* 90-boot.js */
/* Boot: roda os módulos em ordem. Erro em qualquer um → aviso no console + revealAll() (nada fica escondido). */
(function () {
  var M = window.MAYAA;
  function boot() {
    M.mods.forEach(function (m) {
      try { m[1](); }
      catch (e) {
        if (window.console) console.warn('[MAYAA] módulo ' + m[0] + ' falhou:', e);
        try { if (M.revealAll) M.revealAll(); } catch (e2) {}
      }
    });
    M.booted = true;
  }
  try {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  } catch (e) { try { M.revealAll(); } catch (e2) {} }
})();

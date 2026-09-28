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

  /* tokens de movimento = 00-tokens.css (d1/d3/d5 = --dur-1/2/3). Sem bounce nem elastic. */
  var T = M.T = { d0: .12, d1: .2, d2: .24, d3: .45, d4: .8, d5: .9, count: 1.6, hold: .4,
    out: 'expo.out', 'in': 'power4.in', io: 'power2.inOut', snap: 'power3.out', land: 'back.out(1.4)',
    y: 24, y16: 16, lines: 150, img: 1.12, zoom: 1.035, mag: .3, magMax: 10, magPad: 24, stack: .94, stackStep: 8,
    sLogo: .04, sList: .06, sLine: .08, cap: .5 };
  /* atraso por item, cascata total <= .5 s */
  M.stagger = function (n, b) { return n > 1 ? Math.min(b == null ? T.sList : b, T.cap / (n - 1)) : 0; };
  M.touch = !M.fine;
  /* chegou por View Transition: a mídia do morph não se esconde */
  try {
    M.vtIn = !M.reduced && CSS.supports('view-transition-name:a') && !!((window.navigation && navigation.activation &&
      navigation.activation.from) || document.referrer.indexOf(location.origin) === 0);
  } catch (e) {}

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

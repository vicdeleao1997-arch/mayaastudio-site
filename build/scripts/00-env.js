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

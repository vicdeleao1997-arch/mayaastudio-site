/* Ímã do botão do direct ([data-magnet]): só mouse + desktop + movimento liberado. Área = botão + 24 px; força .3,
   teto 10 px; texto a metade; volta .45 s power3.out. Nunca mexe em opacity. Toque .97 é CSS (`scale`). */
(function () {
  var M = window.MAYAA;
  M.register('magnet', function () {
    var g = M.gsap, T = M.T;
    if (!g || !g.quickTo || M.reduced || !M.fine || !M.wide) return;
    var q = function (el, p) { return el && g.quickTo(el, p, { duration: T.d3, ease: T.snap }); };
    var its = [].map.call(document.querySelectorAll('[data-magnet]'), function (el) {
      var t = el.querySelector('.btn__txt');
      return { el: el, x: q(el, 'x'), y: q(el, 'y'), tx: q(t, 'x'), ty: q(t, 'y') };
    });
    if (!its.length) return;
    var px = -1e4, py = -1e4, R = T.magPad, lim = function (v) { return Math.max(-T.magMax, Math.min(T.magMax, v * T.mag)); };
    function run() {
      its.forEach(function (o) {
        var r = o.el.getBoundingClientRect(), l = r.left - g.getProperty(o.el, 'x'), t = r.top - g.getProperty(o.el, 'y');
        var on = px > l - R && px < l + r.width + R && py > t - R && py < t + r.height + R;
        if (!on && !o.on) return;
        o.on = on;
        var dx = on ? lim(px - l - r.width / 2) : 0, dy = on ? lim(py - t - r.height / 2) : 0;
        o.x(dx); o.y(dy);
        if (o.tx) { o.tx(dx / 2); o.ty(dy / 2); }
      });
      return false;
    }
    addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') { px = e.clientX; py = e.clientY; M.tick(run); } }, { passive: true });
    document.addEventListener('pointerout', function (e) { if (!e.relatedTarget) { px = py = -1e4; M.tick(run); } });
    M.onScroll(function () { M.tick(run); });
  });
})();

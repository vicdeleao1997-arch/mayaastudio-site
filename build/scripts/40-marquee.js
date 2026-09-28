/* Marquee de logos e de texto: só CSS; aqui o botão Pausar/Continuar, a pausa fora da tela (§2.7.7) e a reação à
   rolagem: a velocidade do polegar acelera a esteira (até 3×, lerp .1) e ela volta sozinha a 1×. Nunca inverte, nunca
   para; o rAF (M.tick) sai do laço quando assenta.
   Logos (.mq--logos): só anima abaixo de 1024 px e sem prefers-reduced-motion; fora disso fica parado
   (.is-static: a parede de logos, sem "Pausar"). */
(function () {
  var M = window.MAYAA;
  function speed(m) {
    if (M.reduced || !M.tick) return;
    var anims = function () {
      return [].concat.apply([], [].map.call(m.querySelectorAll('.mq__track'), function (t) { return t.getAnimations ? t.getAnimations() : []; }));
    };
    var rate = 1, tgt = 1, on = 0;
    var set = function (r) { anims().forEach(function (a) { a.playbackRate = r; }); };
    function step() {
      tgt += (1 - tgt) * .06;
      rate += (tgt - rate) * .1;
      if (Math.abs(rate - 1) < .02 && Math.abs(tgt - 1) < .02) { rate = tgt = 1; set(1); on = 0; return false; }
      set(rate);
    }
    M.onScroll(function (y, dy, dt) {
      if (m.matches('.is-static,.is-paused,.is-off')) return;
      tgt = Math.max(tgt, 1 + Math.min(Math.abs(dy) / (dt || 16.7) * .8, 2));
      if (!on) { on = 1; M.tick(step); }
    });
  }

  M.register('marquee', function () {
    var mm = window.matchMedia;
    var estreita = mm ? mm('(max-width:1023px)') : { matches: true };
    var calma = mm ? mm('(prefers-reduced-motion: reduce)') : { matches: false };
    document.querySelectorAll('[data-marquee]').forEach(function (m) {
      if (m.classList.contains('mq--logos')) {
        var sync = function () { m.classList.toggle('is-static', !(estreita.matches && !calma.matches)); };
        sync();
        [estreita, calma].forEach(function (q) {
          if (q.addEventListener) q.addEventListener('change', sync);
          else if (q.addListener) q.addListener(sync);
        });
      }
      var b = m.querySelector('.mq__toggle');
      if (b) b.addEventListener('click', function () {
        var p = m.classList.toggle('is-paused');
        b.setAttribute('aria-pressed', String(p));
        b.textContent = p ? 'Continuar' : 'Pausar';
      });
      speed(m);
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (es) {
          es.forEach(function (e) { m.classList.toggle('is-off', !e.isIntersecting); });
        }).observe(m);
      }
    });
  });
})();

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

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

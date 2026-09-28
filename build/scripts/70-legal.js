/* Política de privacidade (grupo legal-seo): marca no índice lateral o tópico que está sendo lido
   (o último cujo topo já passou de 35% da altura da janela): aria-current="location" e um marcador que desliza até
   ele (no reduzido, pula sem transição). */
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
      move();
    }
    /* marcador de 2 px que desliza até o tópico ativo (só transform; posições lidas no início e no resize) */
    var ind = nav.querySelector('.toc__ind'), box = [];
    if (ind && !M.reduced) ind.style.transition = 'transform var(--d2) var(--ease-snap)';
    function read() { box = items.map(function (it) { return [it.a.offsetLeft, it.a.offsetTop, it.a.offsetHeight]; }); move(); }
    function move() {
      if (!ind || !box.length) return;
      var i = items.indexOf(atual), b = box[i];
      ind.style.transform = b ? 'translate(' + b[0] + 'px,' + b[1] + 'px) scaleY(' + b[2] + ')' : 'scaleY(0)';
    }
    function onScroll() { if (!pendente) { pendente = true; window.requestAnimationFrame(mark); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { read(); onScroll(); }, { passive: true });
    mark();
    read();
  });
})();

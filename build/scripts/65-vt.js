/* Morph 'obra' da View Transition (root e hd são só CSS): a mídia do card clicado (a[data-vt]) vira a abertura do
   case ([data-vt-open], nome estático no CSS). No pageswap (página antiga, sem corrida) a abertura local perde o
   nome (duplicado aborta a transição) e, se o destino é /cases/, a mídia do card ganha. Sem suporte: nada. */
(function () {
  var M = window.MAYAA;
  M.register('vt', function () {
    if (M.reduced || !('onpageswap' in window)) return;
    var last = null, MED = '[data-vt-media],.case-card__media,.nc__media';
    document.addEventListener('click', function (e) { last = e.target.closest && e.target.closest('a[data-vt]'); }, true);
    addEventListener('pageswap', function (e) {
      if (!e.viewTransition) return;
      var op = document.querySelector('[data-vt-open]'), a = last, to = e.activation && e.activation.entry && e.activation.entry.url;
      last = null;
      if (op) op.style.viewTransitionName = 'none';
      if (!a || !to || a.href.split('#')[0] !== to.split('#')[0] || new URL(to).pathname.indexOf('/cases/')) return;
      var m = a.querySelector(MED) || (a.closest('.case-card,.nc') || a).querySelector(MED);
      if (m) m.style.viewTransitionName = 'obra';
    });
    addEventListener('pageshow', function (e) {   /* volta pelo bfcache: limpa os nomes */
      if (e.persisted) document.querySelectorAll('[style*=view-transition-name]').forEach(function (el) { el.style.viewTransitionName = ''; });
    });
  });
})();

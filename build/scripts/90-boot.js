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

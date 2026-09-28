/* Boot: roda os módulos em ordem. Erro em qualquer um → aviso no console + revealAll() (nada fica escondido). */
(function () {
  var M = window.MAYAA;
  function boot() {
    var t0 = performance.now();
    M.modMs = {};   /* ms por módulo; soma (M.bootMs) <= 30 ms no celular 4x */
    M.mods.forEach(function (m) {
      var t = performance.now();
      try { m[1](); M.modMs[m[0]] = +(performance.now() - t).toFixed(1); }
      catch (e) {
        if (window.console) console.warn('[MAYAA] módulo ' + m[0] + ' falhou:', e);
        try { if (M.revealAll) M.revealAll(); } catch (e2) {}
      }
    });
    M.bootMs = +(performance.now() - t0).toFixed(1);
    M.booted = true;
  }
  try {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  } catch (e) { try { M.revealAll(); } catch (e2) {} }
})();

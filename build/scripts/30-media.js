/* Vídeo só visível, "Copiar e-mail", Instagram por clique e FAQ animado (§2.7.4, §2.7.21, §2.7.24, §2.7.25). */
(function () {
  var M = window.MAYAA;

  function vbtn(cls, txt) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'vid__btn label ' + cls; b.textContent = txt;
    return b;
  }
  function tocar(v, falhou) { var p = v.play(); if (p && p.catch) p.catch(falhou || function () {}); }

  /* Sem JS: controles nativos. Modo suave, economia de dados ou sem IntersectionObserver: nada toca sozinho; pôster
     limpo + botão da marca ("Ver filme" + triângulo em SVG) e os controles do navegador só depois do clique.
     Modo completo: toca mudo só quando ≥50% visível, com Pausar/Continuar (WCAG 2.2.2) e Ativar som; clicar no
     vídeo também pausa e continua. Pausa pedida pela pessoa não é desfeita pela rolagem. */
  M.register('video', function () {
    var vids = Array.prototype.slice.call(document.querySelectorAll('video[data-autoplay]'));
    if (!vids.length) return;
    var auto = !M.reduced && !M.saveData && ('IntersectionObserver' in window);
    vids.forEach(function (v) {
      var frame = v.parentElement;
      v.muted = true; v.defaultMuted = true;
      v.removeAttribute('controls');

      if (!auto) {
        var go = vbtn('vid__play', '');
        go.appendChild(document.createTextNode((v.getAttribute('data-play') || 'Ver filme') + ' '));
        var tri = document.createElement('span'); tri.setAttribute('aria-hidden', 'true'); tri.className = 'vid__tri';
        /* U+25B6 (play) não existe na Archivo nem na Shippori (caía na Segoe UI): triângulo em traço, SVG (R1-04) */
        tri.innerHTML = '<svg class="ico ico--play" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" focusable="false"><path d="M2.2 1.2v7.6L8.8 5z"/></svg>';
        go.appendChild(tri);
        go.addEventListener('click', function () {
          v.setAttribute('controls', ''); v.preload = 'auto';
          go.remove(); v.focus(); tocar(v);
        });
        frame.appendChild(go);
        return;
      }

      var bar = document.createElement('div');
      bar.className = 'vid__bar';
      var bp = vbtn('vid__pause', 'Pausar'); bp.setAttribute('aria-pressed', 'false');
      var bs = vbtn('vid__sound', 'Ativar som');
      bar.appendChild(bp); bar.appendChild(bs);
      frame.appendChild(bar);
      frame.classList.add('is-auto');
      var held = false;                                   /* pausado pela pessoa */
      var restore = function () { v.setAttribute('controls', ''); frame.classList.remove('is-auto'); if (bar.parentNode) bar.remove(); };
      var sync = function () {
        var p = v.paused;
        bp.textContent = p ? 'Continuar' : 'Pausar';
        bp.setAttribute('aria-pressed', String(p));
      };
      v.addEventListener('play', sync);
      v.addEventListener('pause', sync);
      var toggle = function () {
        if (v.paused) { held = false; tocar(v, restore); } else { held = true; v.pause(); }
      };
      bp.addEventListener('click', toggle);
      v.addEventListener('click', toggle);
      bs.addEventListener('click', function () {
        v.muted = !v.muted;
        bs.textContent = v.muted ? 'Ativar som' : 'Desligar som';
      });
      var pre = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { v.preload = 'auto'; pre.disconnect(); } });
      }, { rootMargin: '100% 0px 100% 0px' });
      pre.observe(v);
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting && e.intersectionRatio >= 0.5) { if (!held) tocar(v, restore); }
          else if (!v.paused) v.pause();
        });
      }, { threshold: [0, 0.5, 0.75] });
      io.observe(v);
      v.addEventListener('error', restore, true);
    });
  });

  M.register('mail', function () {
    if (!(navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext)) return;
    document.querySelectorAll('[data-copy]').forEach(function (b) {
      b.hidden = false;
      var st = b.parentElement.querySelector('[data-copy-status]');
      var timer = null;
      b.addEventListener('click', function () {
        navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {
          b.textContent = 'Copiado';
          if (st) st.textContent = 'E-mail copiado';
          clearTimeout(timer);
          timer = setTimeout(function () { b.textContent = 'Copiar e-mail'; if (st) st.textContent = ''; }, 2000);
        }).catch(function () {});
      });
    });
  });

  M.register('ig', function () {
    document.querySelectorAll('[data-ig-load]').forEach(function (b) {
      b.addEventListener('click', function () {
        var box = b.closest('[data-ig-src]');
        if (!box) return;
        var kind = box.getAttribute('data-ig-kind');
        var f = document.createElement('iframe');
        f.src = box.getAttribute('data-ig-src');
        f.title = 'Instagram: ' + (box.getAttribute('data-ig-what') || 'conteúdo');
        f.width = '100%'; f.height = kind === 'post' ? '620' : '740';
        f.loading = 'lazy'; f.className = 'ig__frame';
        f.setAttribute('allow', 'encrypted-media; picture-in-picture');
        f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
        var link = box.querySelector('.link-arrow');
        var wrap = document.createElement('div');
        wrap.className = 'ig-loaded';
        wrap.appendChild(f);
        if (link) { var p = document.createElement('p'); p.className = 'ig__after'; p.appendChild(link); wrap.appendChild(p); }
        box.replaceWith(wrap);
        f.focus();
        if (M.ST) setTimeout(function () { M.ST.refresh(); }, 300);
      });
    });
  });

  M.register('faq', function () {
    var items = document.querySelectorAll('.faq__item');
    if (!items.length) return;
    items.forEach(function (d) {
      d.addEventListener('toggle', function () { if (M.ST) M.ST.refresh(); });
    });
    var g = M.gsap;
    if (!g || M.reduced) return;
    items.forEach(function (d) {
      var s = d.querySelector('summary'), a = d.querySelector('.faq__a');
      if (!s || !a) return;
      s.addEventListener('click', function (e) {
        e.preventDefault();
        g.killTweensOf(a);
        if (d.open) {
          g.to(a, { height: 0, duration: 0.4, ease: 'power2.inOut',
            onComplete: function () { d.open = false; g.set(a, { clearProps: 'height' }); } });
        } else {
          d.open = true;
          g.fromTo(a, { height: 0 }, { height: 'auto', duration: 0.4, ease: 'power2.out', clearProps: 'height' });
        }
      });
    });
  });
})();

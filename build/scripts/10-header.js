/* Cabeçalho (some ao descer, volta ao subir) e menu em tela cheia com foco preso (§2.7.1). */
(function () {
  var M = window.MAYAA;
  M.register('header', function () {
    var hd = document.querySelector('[data-header]');
    if (!hd) return;
    var menu = document.getElementById('menu');
    var openBtn = hd.querySelector('.hd__menu');
    var closeBtn = menu && menu.querySelector('.menu__close');
    var lastY = window.scrollY, ticking = false, isOpen = false;
    if (M.reduced) hd.style.transitionDuration = 'var(--dur-1)';

    function update() {
      ticking = false;
      var y = window.scrollY;
      hd.classList.toggle('is-scrolled', y > 24);
      var focusInside = hd.contains(document.activeElement);
      if (!isOpen && !focusInside && y > 400 && y > lastY + 2) hd.classList.add('is-hidden');
      else if (y < lastY - 2 || y <= 400 || isOpen || focusInside) hd.classList.remove('is-hidden');
      lastY = y;
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    hd.addEventListener('focusin', function () { hd.classList.remove('is-hidden'); });
    update();

    if (!menu || !openBtn) return;
    var focusables = function () {
      return Array.prototype.slice.call(menu.querySelectorAll('a[href], button:not([disabled])'))
        .filter(function (el) { return el.offsetParent !== null || el === closeBtn; });
    };
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables(); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
    function open() {
      if (isOpen) return;
      isOpen = true;
      menu.hidden = false;
      openBtn.setAttribute('aria-expanded', 'true');
      document.body.classList.add('is-locked');
      if (M.lenis) M.lenis.stop();
      document.addEventListener('keydown', onKey);
      var g = M.gsap;
      if (g) {
        var links = menu.querySelectorAll('.menu__list li');
        if (M.reduced) g.fromTo(menu, { opacity: 0 }, { opacity: 1, duration: 0.2, clearProps: 'opacity' });
        else {
          g.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 0.6, ease: 'expo.out', clearProps: 'clipPath' });
          g.fromTo(links, { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out', stagger: 0.04, delay: 0.1, clearProps: 'transform,opacity' });
        }
      }
      (closeBtn || focusables()[0]).focus();
    }
    function close(noFocus) {
      if (!isOpen) return;
      isOpen = false;
      menu.hidden = true;
      openBtn.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('is-locked');
      if (M.lenis) M.lenis.start();
      document.removeEventListener('keydown', onKey);
      if (!noFocus) openBtn.focus();
    }
    M.closeMenu = close;
    openBtn.addEventListener('click', function () { isOpen ? close() : open(); });
    if (closeBtn) closeBtn.addEventListener('click', function () { close(); });
    menu.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (a) close(true);
    });
    window.addEventListener('resize', function () { if (isOpen && window.innerWidth >= 900) close(true); });
  });
})();

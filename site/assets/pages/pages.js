/* Victor Mey · navegação acessível e Instagram somente por solicitação. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  var closeButton = menu && menu.querySelector('.menu-close');
  var background = Array.from(document.querySelectorAll('header.hdr, main, footer.ftr'));
  var previousInert = [];
  function closeMenu(restoreFocus) {
    if (!menu || menu.hidden) return;
    menu.hidden = true;
    burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-open');
    background.forEach(function (el, i) { el.inert = previousInert[i]; });
    if (restoreFocus) burger.focus();
  }
  function openMenu() {
    menu.hidden = false;
    burger.setAttribute('aria-expanded', 'true');
    document.body.classList.add('menu-open');
    previousInert = background.map(function (el) { return el.inert; });
    background.forEach(function (el) { el.inert = true; });
    closeButton.focus();
  }
  if (burger && menu && closeButton) {
    burger.addEventListener('click', openMenu);
    closeButton.addEventListener('click', function () { closeMenu(true); });
    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { closeMenu(true); });
    });
    document.addEventListener('keydown', function (event) {
      if (menu.hidden) return;
      if (event.key === 'Escape') { event.preventDefault(); closeMenu(true); return; }
      if (event.key !== 'Tab') return;
      var items = Array.from(menu.querySelectorAll('a[href],button:not([disabled])'));
      var first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth >= 900) closeMenu(false); });
  }
  document.querySelectorAll('.nav a').forEach(function (link) {
    if (new URL(link.href).pathname === location.pathname && !link.hash) link.setAttribute('aria-current', 'page');
  });
  /* O vídeo local mantém controles nativos; não há reprodução automática. */
  document.querySelectorAll('video').forEach(function (video) { video.controls = true; });
  var instagramPromise;
  function loadInstagram() {
    if (window.instgrm && window.instgrm.Embeds) return Promise.resolve();
    if (instagramPromise) return instagramPromise;
    instagramPromise = new Promise(function (resolve, reject) {
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.instagram.com/embed.js';
      script.onload = resolve;
      script.onerror = function () { script.remove(); instagramPromise = null; reject(new Error('Instagram indisponível')); };
      document.body.appendChild(script);
    });
    return instagramPromise;
  }
  document.querySelectorAll('[data-ig-load]').forEach(function (button) {
    button.addEventListener('click', function () {
      var slot = document.getElementById(button.getAttribute('data-ig-load'));
      if (!slot || slot.dataset.done) return;
      var permalink;
      try { permalink = new URL(slot.dataset.permalink); } catch (_) { return; }
      if (permalink.protocol !== 'https:' || permalink.hostname !== 'www.instagram.com') return;
      var block = document.createElement('blockquote');
      block.className = 'instagram-media';
      block.setAttribute('data-instgrm-permalink', permalink.href);
      block.setAttribute('data-instgrm-version', '14');
      var link = document.createElement('a');
      link.href = permalink.href; link.target = '_blank'; link.rel = 'noopener'; link.textContent = 'Abrir publicação no Instagram';
      block.appendChild(link); slot.replaceChildren(block);
      slot.dataset.done = '1'; button.disabled = true;
      loadInstagram().then(function () {
        if (window.instgrm && window.instgrm.Embeds) window.instgrm.Embeds.process();
      }).catch(function () {
        delete slot.dataset.done; button.disabled = false;
        var message = document.createElement('p'); message.setAttribute('role', 'status');
        message.textContent = 'Não foi possível carregar. Use o link para abrir no Instagram ou tente novamente.';
        slot.prepend(message);
      });
    });
  });
  document.querySelectorAll('[data-year]').forEach(function (node) { node.textContent = new Date().getFullYear(); });
})();

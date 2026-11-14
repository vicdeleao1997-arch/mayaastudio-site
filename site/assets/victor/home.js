(() => {
  document.documentElement.classList.add('js');
  const menu = document.querySelector('#mobile-nav');
  const toggle = document.querySelector('.menu-button');
  function setMenu(open, restore = false) {
    menu.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', document.documentElement.lang === 'en' ? (open ? 'Close menu' : 'Open menu') : (open ? 'Fechar menu' : 'Abrir menu'));
    toggle.textContent = open ? '×' : '☰';
    if (restore) toggle.focus();
  }
  toggle.addEventListener('click', () => setMenu(menu.hidden));
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) setMenu(false, true); });
  document.addEventListener('click', e => { if (!menu.hidden && !e.target.closest('.site-header')) setMenu(false); });
  window.matchMedia('(min-width:861px)').addEventListener('change', e => { if (e.matches) setMenu(false); });
  const language = document.querySelector('.language');
  const translations = [...document.querySelectorAll('[data-en]')].map(el => ({el, pt:el.innerHTML, en:el.dataset.en}));
  language.addEventListener('click', () => {
    const en = document.documentElement.lang !== 'en';
    document.documentElement.lang = en ? 'en' : 'pt-BR';
    translations.forEach(({el,pt,en:english}) => { el.innerHTML = en ? english : pt; });
    language.textContent = en ? 'PT' : 'EN';
    language.setAttribute('aria-label', en ? 'Ler em português' : 'Read in English');
    document.title = en ? 'Performance & AI for businesses | MAYAA by Victor Mey' : 'Performance & IA para empresas | MAYAA por Victor Mey';
    setMenu(false);
  });
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if(entry.isIntersecting){entry.target.classList.remove('is-pending');observer.unobserve(entry.target);}
    }), {threshold:.08});
    document.querySelectorAll('.reveal').forEach(el => {el.classList.add('is-pending');observer.observe(el);});
  }
  document.querySelector('[data-year]').textContent = new Date().getFullYear();
})();

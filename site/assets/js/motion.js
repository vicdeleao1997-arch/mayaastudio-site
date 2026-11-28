/* Motion do site: rolagem suave, títulos por linha, revelações, pilhas, contadores, ímã.
   Sem JS ou com movimento reduzido, tudo fica visível e estático. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasGsap = window.gsap && window.ScrollTrigger;
  window.MAYAA = { reduce, progress: 0, scene: 'hero' };

  // navegação: pílula de vidro ao rolar, tom escuro sobre seções escuras
  const nav = document.querySelector('[data-nav]');
  const darks = [...document.querySelectorAll('.dark')];
  const onScroll = () => {
    const y = scrollY;
    nav.classList.toggle('is-scrolled', y > 40);
    const mid = 40;
    nav.classList.toggle('on-dark-bg', darks.some(s => { const r = s.getBoundingClientRect(); return r.top < mid && r.bottom > mid; }));
    const max = document.documentElement.scrollHeight - innerHeight;
    window.MAYAA.progress = max > 0 ? y / max : 0;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // cena ativa para o 3D (a seção que cruza o meio da tela)
  const scenes = [...document.querySelectorAll('[data-scene]')];
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) window.MAYAA.scene = e.target.dataset.scene; }), { rootMargin: '-50% 0px -50% 0px' });
  scenes.forEach(s => io.observe(s));

  waveCanvas();
  const show = () => document.querySelectorAll('[data-reveal],[data-split]').forEach(el => el.style.visibility = 'visible');
  if (reduce || !hasGsap) { show(); return; }

  const { gsap, ScrollTrigger } = window;
  gsap.registerPlugin(ScrollTrigger);

  // rolagem suave ligada ao ScrollTrigger
  if (window.Lenis) {
    const lenis = new Lenis({ duration: 1.15, easing: t => 1 - Math.pow(1 - t, 4), smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -20 }); t.focus({ preventScroll: true }); }
    }));
  }

  // títulos: cada linha sobe de dentro de uma máscara
  document.querySelectorAll('[data-split]').forEach(el => {
    const parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map(p => `<span class="split-line"><span>${p.trim()}</span></span>`).join('');
    const lines = el.querySelectorAll('.split-line > span');
    const isHero = el.classList.contains('hero__title');
    gsap.from(lines, {
      yPercent: 110, rotate: 3, duration: 1.2, ease: 'expo.out', stagger: .09, delay: isHero ? .25 : 0,
      scrollTrigger: isHero ? null : { trigger: el, start: 'top 85%' }
    });
  });

  // revelações simples
  gsap.utils.toArray('[data-reveal]').forEach(el => gsap.from(el, {
    y: 28, autoAlpha: 0, duration: 1, ease: 'power3.out',
    scrollTrigger: el.closest('.hero') ? null : { trigger: el, start: 'top 88%' }, delay: el.closest('.hero') ? .7 : 0
  }));
  show(); // estados iniciais do gsap.from já aplicados, sem piscar
  gsap.utils.toArray('[data-stagger]').forEach(g => gsap.from(g.children, {
    y: 40, autoAlpha: 0, duration: .9, ease: 'power3.out', stagger: .06,
    scrollTrigger: { trigger: g, start: 'top 85%' }
  }));

  // painel de vidro sobe e endireita sobre a cena 3D
  const lift = document.querySelector('[data-lift]');
  if (lift) {
    gsap.fromTo(lift, { yPercent: 18, scale: .92, rotateX: 10, transformPerspective: 1400 },
      { yPercent: 0, scale: 1, rotateX: 0, ease: 'none', scrollTrigger: { trigger: lift, start: 'top bottom', end: 'top 25%', scrub: 1 } });
    gsap.from('.dash__line', { strokeDasharray: 900, strokeDashoffset: 900, duration: 2.2, ease: 'power2.inOut', scrollTrigger: { trigger: '.dash', start: 'top 75%' } });
    gsap.from('.dash__area', { opacity: 0, duration: 1.6, delay: .6, scrollTrigger: { trigger: '.dash', start: 'top 75%' } });
    gsap.utils.toArray('.bar').forEach(b => gsap.fromTo(b, { '--p': 0 }, { '--p': 1, duration: 1.6, ease: 'expo.out', scrollTrigger: { trigger: b, start: 'top 85%' } }));
  }

  // linhas alternadas entram de lado; arte com paralaxe
  gsap.utils.toArray('[data-row]').forEach((r, i) => gsap.from(r, {
    y: 80, autoAlpha: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: r, start: 'top 85%' }
  }));
  gsap.utils.toArray('[data-parallax]').forEach(el => gsap.fromTo(el.children.length ? el.children : el, { yPercent: 12 }, {
    yPercent: -12, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }
  }));

  // pilhas presas: o cartão de baixo encolhe e escurece quando o próximo chega
  ScrollTrigger.matchMedia({ 'all': () => {
    ['.stack__card', '.stat'].forEach(sel => {
      const cards = gsap.utils.toArray(sel);
      cards.forEach((c, i) => {
        const next = cards[i + 1]; if (!next) return;
        gsap.to(c, { scale: .93, opacity: .55, filter: 'blur(2px)', ease: 'none',
          scrollTrigger: { trigger: next, start: 'top 85%', end: 'top 25%', scrub: true } });
      });
    });
  } });

  // contadores
  gsap.utils.toArray('[data-count]').forEach(el => {
    const to = +el.dataset.count, o = { v: 0 };
    gsap.to(o, { v: to, duration: 1.6, ease: 'power2.out', onUpdate: () => el.textContent = (el.dataset.pre || '') + Math.round(o.v) + (el.dataset.suf || ''),
      scrollTrigger: { trigger: el, start: 'top 90%' } });
  });

  // botões com ímã
  if (matchMedia('(pointer:fine)').matches) document.querySelectorAll('[data-magnetic]').forEach(b => {
    const xTo = gsap.quickTo(b, 'x', { duration: .5, ease: 'power3' }), yTo = gsap.quickTo(b, 'y', { duration: .5, ease: 'power3' });
    b.addEventListener('mousemove', e => { const r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .25); yTo((e.clientY - r.top - r.height / 2) * .35); });
    b.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
  });

  // brilho laranja do fundo acompanha o cursor
  const glow = document.querySelector('.stage__glow');
  if (glow) addEventListener('pointermove', e => gsap.to(glow, { x: (e.clientX / innerWidth - .5) * 80, y: (e.clientY / innerHeight - .5) * 60, duration: 1.8, ease: 'power2.out' }));

  // canvas 2D: onda de partículas laranja (cartão de tráfego pago)
  function waveCanvas() {
    document.querySelectorAll('[data-wave]').forEach(cv => {
      const ctx = cv.getContext('2d'); let w, h, t = 0, vis = false;
      const fit = () => { const d = Math.min(devicePixelRatio, 2); w = cv.width = cv.clientWidth * d; h = cv.height = cv.clientHeight * d; };
      fit(); addEventListener('resize', fit);
      new IntersectionObserver(([e]) => vis = e.isIntersecting).observe(cv);
      const draw = () => {
        if (vis) {
          ctx.clearRect(0, 0, w, h);
          const rows = 18, cols = 70;
          for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
            const x = (c / (cols - 1)) * w;
            const ph = c * .16 + t + r * .25;
            const y = h * .62 + Math.sin(ph) * h * .1 * (1 - r / rows) - r * h * .018 + Math.cos(c * .05 + t * .7) * h * .04;
            const a = (1 - r / rows) * .85;
            ctx.fillStyle = `rgba(255,${110 + r * 6},${40 + r * 4},${a})`;
            ctx.beginPath(); ctx.arc(x, y, (1.4 - r * .05) * (w / 400), 0, 6.283); ctx.fill();
          }
          if (!reduce) t += .02;
        }
        if (!reduce) requestAnimationFrame(draw); else if (vis) {}
      };
      reduce ? (vis = true, draw()) : draw();
    });
  }
})();

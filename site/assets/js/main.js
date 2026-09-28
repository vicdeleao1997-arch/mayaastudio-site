/* 00-env.js */
(function () {
var M = window.MAYAA = window.MAYAA || {};
var html = document.documentElement;
var mq = function (q) { try { return window.matchMedia(q).matches; } catch (e) { return false; } };
M.t0 = performance.now();
M.painted = function () {
try { return performance.getEntriesByName('first-contentful-paint').length > 0; } catch (e) { return false; }
};
M.LATE = M.t0 > 900 || M.painted();
M.reduced = mq('(prefers-reduced-motion: reduce)');
M.fine = mq('(hover: hover) and (pointer: fine)');
M.wide = mq('(min-width: 1024px)');
var conn = navigator.connection || {};
M.saveData = !!conn.saveData;
M.gsap = window.gsap || null;
M.ST = window.ScrollTrigger || null;
if (M.gsap && M.ST) { try { M.gsap.registerPlugin(M.ST); } catch (e) {} }
M.mode = M.reduced ? 'suave' : 'completo';
var T = M.T = { d0: .12, d1: .2, d2: .24, d3: .45, d4: .8, d5: .9, count: 1.6, hold: .4,
out: 'expo.out', 'in': 'power4.in', io: 'power2.inOut', snap: 'power3.out', land: 'back.out(1.4)',
y: 24, y16: 16, lines: 150, img: 1.12, zoom: 1.035, mag: .3, magMax: 10, magPad: 24, stack: .94, stackStep: 8,
sLogo: .04, sList: .06, sLine: .08, cap: .5 };
M.stagger = function (n, b) { return n > 1 ? Math.min(b == null ? T.sList : b, T.cap / (n - 1)) : 0; };
M.touch = !M.fine;
try {
M.vtIn = !M.reduced && CSS.supports('view-transition-name:a') && !!((window.navigation && navigation.activation &&
navigation.activation.from) || document.referrer.indexOf(location.origin) === 0);
} catch (e) {}
M.webglOK = function () {
try {
var c = document.createElement('canvas');
return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
} catch (e) { return false; }
};
M.fxOK = !M.reduced && M.fine && M.wide && !M.saveData && M.webglOK();
html.classList.add('js', 'mode-' + M.mode);
if (M.fxOK) html.classList.add('fx-on');
if (!M.gsap) html.classList.add('no-gsap');
M.headerOffset = function () {
var cs = getComputedStyle(html);
var px = function (v) { var d = document.createElement('div'); d.style.height = v; d.style.position = 'absolute';
d.style.visibility = 'hidden'; document.body.appendChild(d); var h = d.getBoundingClientRect().height; d.remove(); return h; };
return px(cs.getPropertyValue('--header-h')) + px(cs.getPropertyValue('--frame')) + 16;
};
M.mods = [];
M.register = function (name, fn) { M.mods.push([name, fn]); };
})();

/* 05-motor.js */
(function () {
var M = window.MAYAA, T = M.T;
var jobs = [], subs = [], dirty = 0, rid = 0, last = 0, sy = scrollY, st = 0;
function kick() { if (!rid) rid = requestAnimationFrame(frame); }
function frame(t) {
rid = 0;
if (last && t - last < 10) return kick();
var dt = last ? Math.min(t - last, 100) : 16.7, i;
last = t;
if (dirty) {
var y = scrollY, dy = y - sy, ds = st ? Math.min(t - st, 100) : 16.7;
dirty = 0; sy = y; st = t;
for (i = 0; i < subs.length; i++) subs[i](y, dy, ds);
}
for (i = jobs.length - 1; i >= 0; i--) if (jobs[i](t, dt) === false) jobs.splice(i, 1);
if (jobs.length) kick(); else last = 0;
}
M.tick = function (fn) { if (jobs.indexOf(fn) < 0) jobs.push(fn); kick(); };
M.onScroll = function (fn) { subs.push(fn); };
addEventListener('scroll', function () { dirty = 1; kick(); }, { passive: true });
var ios = {};
M.observe = function (el, fn, mg) {
if (!window.IntersectionObserver) return fn({ isIntersecting: true, target: el });
var o = ios[mg = mg || '0px'];
if (!o) {
var map = new Map();
o = ios[mg] = { map: map, io: new IntersectionObserver(function (es) {
es.forEach(function (e) { var f = map.get(e.target); if (f && f(e) === false) { o.io.unobserve(e.target); map.delete(e.target); } });
}, { rootMargin: mg }) };
}
o.map.set(el, fn); o.io.observe(el);
};
M.split = function (el, by) {
if (el.hasAttribute('data-split')) return el.querySelectorAll('.sp__in');
if (el.querySelector('a,button,input')) return [];
var sr = document.createElement('span'), vis = document.createElement('span');
sr.className = 'sr'; sr.textContent = el.textContent.replace(/\s+/g, ' ').trim();
vis.setAttribute('aria-hidden', 'true');
while (el.firstChild) vis.appendChild(el.firstChild);
(function walk(n) {
[].slice.call(n.childNodes).forEach(function (c) {
if (c.nodeType === 1) return walk(c);
if (c.nodeType !== 3 || !c.nodeValue.trim()) return;
var f = document.createDocumentFragment();
c.nodeValue.split(/(\s+)/).forEach(function (w) {
if (!w) return;
if (!w.trim()) return f.appendChild(document.createTextNode(w));
var sp = document.createElement('span');
sp.className = 'sp';
(by === 'char' ? w.split('') : [w]).forEach(function (p) {
var s = document.createElement('span'); s.className = 'sp__in'; s.textContent = p; sp.appendChild(s);
});
f.appendChild(sp);
});
n.replaceChild(f, c);
});
})(vis);
el.append(sr, vis);
el.setAttribute('data-split', by || 'word');
return vis.querySelectorAll('.sp__in');
};
function num(el, n, d) { var v = parseFloat(el.getAttribute(n)); return isNaN(v) ? d : v; }
M.fmt = function (v, dec) { return v.toFixed(dec).replace('.', ','); };
M.countPrep = function (el) {
var cur = el.textContent, s = el.style;
if (!el.hasAttribute('data-final')) el.setAttribute('data-final', cur);
s.minWidth = ''; el.textContent = el.getAttribute('data-final');
s.minWidth = Math.ceil(el.getBoundingClientRect().width) + 'px'; s.textAlign = 'end';
el.textContent = cur;
};
M.count = function (el, o) {
o = o || {};
var to = num(el, 'data-to', 0), dec = num(el, 'data-dec', 0), v = { v: 0 }, up = o.onUpdate || function () {};
var fin = el.getAttribute('data-final') || M.fmt(to, dec);
var end = function () { el.textContent = fin; el.style.minWidth = el.style.textAlign = ''; up(1); if (o.onComplete) o.onComplete(); };
if (M.reduced || !M.gsap) return end();
if (!el.style.minWidth) M.countPrep(el);
el.textContent = M.fmt(0, dec);
return M.gsap.to(v, { v: to, duration: o.dur || T.count, ease: 'power2.out', delay: o.delay || 0, onComplete: end,
onUpdate: function () { el.textContent = M.fmt(v.v, dec); up(to ? v.v / to : 1); } });
};
M.register('motor', function () {
var g = M.gsap;
if (!M.reduced && g && M.ST) {
var G = {}, n = 0;
document.querySelectorAll('[data-depth]').forEach(function (el) {
if (el.hasAttribute('data-reveal')) return console.warn('[MAYAA] data-depth + data-reveal', el);
var m = el.getAttribute('data-depth-m'), v = parseFloat(!M.wide && m != null ? m : el.getAttribute('data-depth')) || 0,
op = num(el, 'data-depth-o', 0), k = el.getAttribute('data-depth-group') || n++;
if (v || op) (G[k] = G[k] || []).push({ el: el, to: v, from: num(el, 'data-depth-from', 0), o: op });
});
Object.keys(G).forEach(function (k) {
var el = G[k][0].el, a = function (x, d) { return el.getAttribute('data-depth-' + x) || d; };
var tl = g.timeline({ defaults: { ease: 'none' }, scrollTrigger: { id: a('id', undefined), scrub: true,
trigger: el.closest('[data-depth-trigger],section') || el.parentElement, start: a('start', 'top bottom'), end: a('end', 'bottom top') } });
tl.to({}, { duration: 1 }, 0);
G[k].forEach(function (d) {
if (d.to !== d.from) tl.fromTo(d.el, { yPercent: d.from }, { yPercent: d.to, duration: 1 }, 0);
if (d.o) tl.fromTo(d.el, { opacity: 1 }, { opacity: 0, duration: d.o }, 0);
});
});
}
if (M.touch && !M.reduced) document.querySelectorAll('[data-focus]').forEach(function (el) {
M.observe(el, function (e) { el.classList.toggle('is-focus', e.isIntersecting); }, '-50% 0px -50% 0px');
});
});
})();

/* 10-header.js */
(function () {
var M = window.MAYAA;
M.register('header', function () {
var hd = document.querySelector('[data-header]');
if (!hd) return;
var menu = document.getElementById('menu');
var openBtn = hd.querySelector('.hd__menu');
var closeBtn = menu && menu.querySelector('.menu__close');
var lastY = window.scrollY, isOpen = false;
if (M.reduced) hd.style.transitionDuration = 'var(--dur-1)';
var fixo = window.matchMedia ? window.matchMedia('(max-width:899px)') : { matches: false };
function update() {
var y = window.scrollY;
hd.classList.toggle('is-scrolled', y > 24);
var focusInside = hd.contains(document.activeElement);
if (fixo.matches) hd.classList.remove('is-hidden');
else if (!isOpen && !focusInside && y > 400 && y > lastY + 2) hd.classList.add('is-hidden');
else if (y < lastY - 2 || y <= 400 || isOpen || focusInside) hd.classList.remove('is-hidden');
lastY = y;
}
M.onScroll(update);
var prog = hd.querySelector('.hd__prog');
if (prog) {
var span = 1, measure = function () { span = Math.max(1, document.documentElement.scrollHeight - innerHeight); bar(scrollY); };
var bar = function (y) { prog.style.transform = 'scaleX(' + Math.min(1, Math.max(0, y / span)).toFixed(4) + ')'; };
prog.hidden = false;
M.onScroll(bar);
addEventListener('resize', measure, { passive: true });
addEventListener('load', measure);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
measure();
}
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

/* 20-reveal.js */
(function () {
var M = window.MAYAA;
var state = {
get: function (el) { return el.getAttribute('data-rv'); },
set: function (el, v) { el.setAttribute('data-rv', v); }
};
var all = [];
var io = null;
var arm = null;
var DM = '[data-magnet],a[href^="https://ig.me/"]';
var INK = { top: 'inset(0% 0% 100% 0%)', bottom: 'inset(100% 0% 0% 0%)' }, OPEN = 'inset(0% 0% 0% 0%)';
function num(el, name, dflt) { var v = parseFloat(el.getAttribute(name)); return isNaN(v) ? dflt : v; }
function has(el, a) { return el.hasAttribute(a); }
function mag(el) { return el.matches(DM) || !!el.querySelector(DM); }
function kids(el) { return Array.prototype.slice.call(el.children).filter(function (k) { return !mag(k); }); }
function maskParts(el) {
var media = el.querySelector('.fig__media, .vid__frame') || el;
return { media: media, img: has(el, 'data-noscale') ? null : media.querySelector('img, video'), cap: el.querySelector('figcaption') };
}
function cx(el) {
var p = el.parentElement;
return { rule: has(el, 'data-rule') ? p.querySelector('.proof__rule') : null, x: has(el, 'data-land') ? p.querySelector('.proof__x') : null };
}
function targets(el) {
var t = el.getAttribute('data-reveal');
if (t === 'lines') return [].slice.call(el.querySelectorAll('.line__in')).concat(el._rule || []);
if (t === 'stagger') return kids(el);
if (t === 'mask') { var p = maskParts(el); return [el, p.media, p.img, p.cap].filter(Boolean); }
if (t === 'count') { var c = cx(el); return [el, c.rule, c.x].filter(Boolean); }
return [el];
}
function kidFrom(el) {
var o = { y: num(el, 'data-y', M.T.y), opacity: 0 };
if (has(el, 'data-rule')) o['--r'] = 0;
if (has(el, 'data-arr') && M.wide) o['--ax'] = '-8px';
return o;
}
function hide(el) {
var g = M.gsap, t = el.getAttribute('data-reveal'), T = M.T;
state.set(el, 'wait');
if (t === 'lines') {
g.set(el.querySelectorAll('.line__in'), { yPercent: T.lines });
if (el._rule) g.set(el._rule, { '--r': 0 });
} else if (t === 'fade') g.set(el, { y: num(el, 'data-y', T.y), yPercent: num(el, 'data-yp', 0), opacity: 0 });
else if (t === 'stagger') g.set(kids(el), kidFrom(el));
else if (t === 'mask') {
var p = maskParts(el);
g.set(p.media, { clipPath: el.getAttribute('data-mask') === 'box' ? 'inset(14% 0% 14% 0%)' : INK.bottom });
if (p.img) g.set(p.img, { scale: T.img });
if (p.cap) g.set(p.cap, { opacity: 0, y: 12 });
} else if (t === 'ink') g.set(el, { clipPath: INK[el.getAttribute('data-from')] || INK.top });
else if (t === 'rule') g.set(el, { '--r': 0 });
else if (t === 'count') {
var c = cx(el);
M.countPrep(el);
if (c.rule) c.rule.style.transform = 'scaleX(0)';
if (c.x) g.set(c.x, { yPercent: 40, opacity: 0 });
if (arm) arm.observe(el);
}
}
function done(el) { state.set(el, 'done'); }
function play(el, dl) {
var g = M.gsap, t = el.getAttribute('data-reveal'), T = M.T;
if (state.get(el) !== 'wait') return;
state.set(el, 'run');
var d = dl == null ? num(el, 'data-delay', 0) : dl;
var fin = function () { done(el); };
if (t === 'lines') {
var ls = el.querySelectorAll('.line__in');
if (el._rule) g.to(el._rule, { '--r': 1, duration: T.d4, ease: T.out, delay: d, clearProps: '--r' });
g.to(ls, { yPercent: 0, duration: T.d5, ease: T.out, stagger: M.stagger(ls.length, T.sLine), delay: d, clearProps: 'transform', onComplete: fin });
} else if (t === 'fade') {
g.to(el, { y: 0, yPercent: 0, opacity: 1, duration: num(el, 'data-dur', T.d4), ease: T.out, delay: d, clearProps: 'transform,opacity', onComplete: fin });
} else if (t === 'stagger') {
var ks = kids(el), to = { y: 0, opacity: 1, duration: T.d4, ease: T.out, delay: d, onComplete: fin,
stagger: M.stagger(ks.length, num(el, 'data-st', T.sList)), clearProps: 'transform,opacity,--r,--ax' };
if (has(el, 'data-rule')) to['--r'] = 1;
if (has(el, 'data-arr') && M.wide) to['--ax'] = '0px';
g.to(ks, to);
} else if (t === 'mask') {
var p = maskParts(el);
g.to(p.media, { clipPath: OPEN, duration: T.d5, ease: T.out, delay: d, clearProps: 'clipPath', onComplete: fin });
if (p.img) g.to(p.img, { scale: 1, duration: T.d5, ease: T.out, delay: d, clearProps: 'transform' });
if (p.cap) g.to(p.cap, { opacity: 1, y: 0, duration: T.d4, ease: T.out, delay: d + 0.35, clearProps: 'transform,opacity' });
} else if (t === 'ink') {
g.to(el, { clipPath: OPEN, duration: T.d4, ease: T.out, delay: d, clearProps: 'clipPath', onComplete: fin });
} else if (t === 'rule') {
g.to(el, { '--r': 1, duration: T.d4, ease: T.out, delay: d, clearProps: '--r', onComplete: fin });
} else if (t === 'count') {
if (arm) { try { arm.unobserve(el); } catch (e) {} }
var c = cx(el);
M.count(el, { delay: d, onUpdate: function (k) { if (c.rule) c.rule.style.transform = k < 1 ? 'scaleX(' + k + ')' : ''; },
onComplete: function () {
if (c.x) g.to(c.x, { yPercent: 0, opacity: 1, duration: T.d3, ease: T.land, clearProps: 'transform,opacity' });
fin();
} });
} else fin();
}
function finish(el) {
var g = M.gsap;
if (state.get(el) === 'done') return;
if (g) {
var t = targets(el);
g.killTweensOf(t);
g.set(t, { clearProps: 'transform,opacity,clipPath,--r,--ax' });
}
if (el.getAttribute('data-reveal') === 'count') {
if (arm) { try { arm.unobserve(el); } catch (e) {} }
if (has(el, 'data-final')) el.textContent = el.getAttribute('data-final');
el.style.minWidth = el.style.textAlign = '';
}
done(el);
}
function sweep() {
var vh = window.innerHeight;
all.forEach(function (el) {
var s = state.get(el);
if (s !== 'wait') return;
if (el.getBoundingClientRect().top < vh) { if (io) io.unobserve(el); finish(el); }
});
}
M.sweep = sweep;
M.revealAll = function () {
all.forEach(function (el) { if (io) { try { io.unobserve(el); } catch (e) {} } finish(el); });
};
M.hold = function (el) { if (io) { try { io.unobserve(el); } catch (e) {} } };
M.play = function (el, d) { M.hold(el); play(el, d); };
function pair(lab) {
for (var s = lab.nextElementSibling, i = 0; s && i < 3; s = s.nextElementSibling, i++) {
var t = s.matches('[data-reveal=lines]') ? s : s.querySelector('[data-reveal=lines]');
if (t) return t;
}
return null;
}
M.register('reveal', function () {
if (M.reduced || !M.gsap || !('IntersectionObserver' in window)) {
[].forEach.call(document.querySelectorAll('[data-reveal]'), done); return;
}
[].forEach.call(document.querySelectorAll('.label--rule:not([data-reveal])'), function (lab) {
var t = pair(lab);
if (t && !t._rule) t._rule = lab; else lab.setAttribute('data-reveal', 'rule');
});
all = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
io = new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
if (en.isIntersecting) { io.unobserve(en.target); play(en.target); }
});
}, { rootMargin: '0px 0px -8% 0px' });
arm = new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
var el = en.target;
if (!en.isIntersecting) return;
arm.unobserve(el);
if (state.get(el) === 'wait') el.textContent = M.fmt(0, num(el, 'data-dec', 0));
});
}, { rootMargin: '0px 0px 35% 0px' });
var vh = window.innerHeight;
var late = M.LATE || M.painted();
all.forEach(function (el) {
var r = el.getBoundingClientRect();
if (r.bottom <= 0 && r.top <= 0 && (r.width || r.height)) { done(el); return; }
if (!r.width && !r.height) { done(el); return; }
if (mag(el) && el.getAttribute('data-reveal') !== 'stagger') { done(el); return; }
if (M.vtIn && (el.closest('[data-vt-open]') || el.querySelector('[data-vt-open]'))) { done(el); return; }
if (!M.wide && el.closest('.mq--logos')) { done(el); return; }
if (r.top < vh) {
if (late) { done(el); return; }
hide(el); play(el); return;
}
hide(el);
if (!has(el, 'data-hold') || !M.ST) io.observe(el);
});
var later = function () { setTimeout(sweep, 4000); };
if (document.readyState === 'complete') later(); else window.addEventListener('load', later);
window.addEventListener('hashchange', function () { sweep(); setTimeout(sweep, 1200); });
});
})();

/* 30-media.js */
(function () {
var M = window.MAYAA;
function vbtn(cls, txt) {
var b = document.createElement('button');
b.type = 'button'; b.className = 'vid__btn label ' + cls; b.textContent = txt;
return b;
}
function tocar(v, falhou) { var p = v.play(); if (p && p.catch) p.catch(falhou || function () {}); }
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
var held = false;
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

/* 40-marquee.js */
(function () {
var M = window.MAYAA;
function speed(m) {
if (M.reduced || !M.tick) return;
var anims = function () {
return [].concat.apply([], [].map.call(m.querySelectorAll('.mq__track'), function (t) { return t.getAnimations ? t.getAnimations() : []; }));
};
var rate = 1, tgt = 1, on = 0;
var set = function (r) { anims().forEach(function (a) { a.playbackRate = r; }); };
function step() {
tgt += (1 - tgt) * .06;
rate += (tgt - rate) * .1;
if (Math.abs(rate - 1) < .02 && Math.abs(tgt - 1) < .02) { rate = tgt = 1; set(1); on = 0; return false; }
set(rate);
}
M.onScroll(function (y, dy, dt) {
if (m.matches('.is-static,.is-paused,.is-off')) return;
tgt = Math.max(tgt, 1 + Math.min(Math.abs(dy) / (dt || 16.7) * .8, 2));
if (!on) { on = 1; M.tick(step); }
});
}
M.register('marquee', function () {
var mm = window.matchMedia;
var estreita = mm ? mm('(max-width:1023px)') : { matches: true };
var calma = mm ? mm('(prefers-reduced-motion: reduce)') : { matches: false };
document.querySelectorAll('[data-marquee]').forEach(function (m) {
if (m.classList.contains('mq--logos')) {
var sync = function () { m.classList.toggle('is-static', !(estreita.matches && !calma.matches)); };
sync();
[estreita, calma].forEach(function (q) {
if (q.addEventListener) q.addEventListener('change', sync);
else if (q.addListener) q.addListener(sync);
});
}
var b = m.querySelector('.mq__toggle');
if (b) b.addEventListener('click', function () {
var p = m.classList.toggle('is-paused');
b.setAttribute('aria-pressed', String(p));
b.textContent = p ? 'Continuar' : 'Pausar';
});
speed(m);
if ('IntersectionObserver' in window) {
new IntersectionObserver(function (es) {
es.forEach(function (e) { m.classList.toggle('is-off', !e.isIntersecting); });
}).observe(m);
}
});
});
})();

/* 50-scroll.js */
(function () {
var M = window.MAYAA;
var LENIS = 'https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js';
function loadLenis() {
var g = M.gsap, ST = M.ST;
var s = document.createElement('script');
s.src = LENIS; s.async = true;
s.onload = function () {
try {
if (!window.Lenis) return;
var L = new window.Lenis({ duration: 1.1, smoothWheel: true });
M.lenis = L;
document.documentElement.classList.add('lenis');
L.on('scroll', ST.update);
g.ticker.add(function (t) { L.raf(t * 1000); });
g.ticker.lagSmoothing(0);
if (document.body.classList.contains('is-locked')) L.stop();
} catch (e) { M.lenis = null; }
};
document.head.appendChild(s);
}
function proof(g) {
var pf = document.querySelector('.home .proof.sec--tinta');
if (!pf) return;
var held = pf.querySelectorAll('[data-hold]'), fired = 0, w = pf.querySelector('.wrap');
var fire = function () {
if (fired++) return;
[].forEach.call(held, function (el, i) { M.play(el, M.T.hold + i * .12); });
};
var gp = function () { return Math.max(0, w.offsetLeft + parseFloat(getComputedStyle(w).paddingLeft) - 4); };
var at = function (s) { if (s.progress === 1) fire(); };
g.fromTo(pf, { clipPath: function () { return 'inset(0px ' + gp() + 'px 0px ' + gp() + 'px round 16px)'; } },
{ clipPath: 'inset(0px 0px 0px 0px round 0px)', ease: 'none',
scrollTrigger: { trigger: pf, start: 'top bottom', end: 'top 40%', scrub: true, invalidateOnRefresh: true,
onLeave: fire, onRefresh: at } });
}
function proc(g) {
var ol = document.querySelector('[data-proc]');
if (!ol) return;
var lis = [].slice.call(ol.children), n = lis.length;
if (M.wide) {
var ks = lis.map(function (li) { var k = li.querySelector('[data-reveal=ink]'); if (k && M.hold) M.hold(k); return k; });
ol.classList.add('is-trail');
g.fromTo(ol, { '--p': 0 }, { '--p': 1, ease: 'none', scrollTrigger: { trigger: ol, start: 'top 80%', end: 'bottom 60%', scrub: true,
onUpdate: function (s) {
lis.forEach(function (li, i) {
var on = s.progress > i / n;
if (on === li.classList.contains('is-lit')) return;
li.classList.toggle('is-lit', on);
if (on && ks[i] && M.play) M.play(ks[i]);
});
} } });
} else if (matchMedia('(max-width:639px)').matches) {
var T = M.T, top = function (i) { return M.headerOffset() - 16 + i * T.stackStep; },
nat = function (k) { for (var y = 0, j = 0; j < k; j++) y += lis[j].offsetHeight; return y; };
lis.slice(0, -1).forEach(function (li, i) {
g.to(li.firstElementChild, { scale: T.stack, opacity: .6, ease: 'none', scrollTrigger: { trigger: ol,
scrub: true, invalidateOnRefresh: true,
start: function () { return 'top+=' + nat(i + 1) + ' ' + (top(i) + li.offsetHeight) + 'px'; },
end: function () { return 'top+=' + nat(i + 1) + ' ' + top(i + 1) + 'px'; } } });
});
}
}
M.register('scroll', function () {
var g = M.gsap, ST = M.ST, T = M.T;
if (!M.reduced && g && ST) {
document.querySelectorAll('[data-parallax]').forEach(function (el) {
var cine = el.closest('.band--cine');
var y = cine ? 3 : 6, sc = cine ? 1 : 1.12;
g.fromTo(el, { yPercent: -y, scale: sc }, {
yPercent: y, scale: sc, ease: 'none',
scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
});
});
document.querySelectorAll('[data-zoom] picture').forEach(function (pic) {
pic.style.display = 'block';
g.fromTo(pic, { scale: T.img }, { scale: 1, ease: 'none',
scrollTrigger: { trigger: pic.parentElement, start: 'top bottom', end: 'center center', scrub: true } });
});
proof(g);
proc(g);
if (M.fine) loadLenis();
}
document.addEventListener('click', function (e) {
var a = e.target.closest && e.target.closest('a[href^="#"]');
if (!a) return;
var id = decodeURIComponent(a.getAttribute('href').slice(1));
var t = id && document.getElementById(id);
if (!t) return;
if (M.closeMenu) M.closeMenu(true);
if (!M.lenis) { setTimeout(M.sweep || function () {}, 1200); return; }
e.preventDefault();
M.lenis.scrollTo(t, { offset: -M.headerOffset(), onComplete: function () { if (M.sweep) M.sweep(); } });
if (history.pushState) history.pushState(null, '', '#' + id);
if (!t.matches('a,button,input,select,textarea,[tabindex]')) t.setAttribute('tabindex', '-1');
t.focus({ preventScroll: true });
});
if (ST) {
var refresh = function () { try { ST.refresh(); } catch (e) {} };
if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
if (document.readyState === 'complete') refresh(); else window.addEventListener('load', refresh);
}
});
})();

/* 55-magnet.js */
(function () {
var M = window.MAYAA;
M.register('magnet', function () {
var g = M.gsap, T = M.T;
if (!g || !g.quickTo || M.reduced || !M.fine || !M.wide) return;
var q = function (el, p) { return el && g.quickTo(el, p, { duration: T.d3, ease: T.snap }); };
var its = [].map.call(document.querySelectorAll('[data-magnet]'), function (el) {
var t = el.querySelector('.btn__txt');
return { el: el, x: q(el, 'x'), y: q(el, 'y'), tx: q(t, 'x'), ty: q(t, 'y') };
});
if (!its.length) return;
var px = -1e4, py = -1e4, R = T.magPad, lim = function (v) { return Math.max(-T.magMax, Math.min(T.magMax, v * T.mag)); };
function run() {
its.forEach(function (o) {
var r = o.el.getBoundingClientRect(), l = r.left - g.getProperty(o.el, 'x'), t = r.top - g.getProperty(o.el, 'y');
var on = px > l - R && px < l + r.width + R && py > t - R && py < t + r.height + R;
if (!on && !o.on) return;
o.on = on;
var dx = on ? lim(px - l - r.width / 2) : 0, dy = on ? lim(py - t - r.height / 2) : 0;
o.x(dx); o.y(dy);
if (o.tx) { o.tx(dx / 2); o.ty(dy / 2); }
});
return false;
}
addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') { px = e.clientX; py = e.clientY; M.tick(run); } }, { passive: true });
document.addEventListener('pointerout', function (e) { if (!e.relatedTarget) { px = py = -1e4; M.tick(run); } });
M.onScroll(function () { M.tick(run); });
});
})();

/* 60-fx.js */
(function () {
var M = window.MAYAA;
var OGL = 'https://cdn.jsdelivr.net/npm/ogl@1.0.11/+esm';
var VERT = 'attribute vec2 uv;attribute vec2 position;varying vec2 vUv;' +
'void main(){vUv=uv;gl_Position=vec4(position,0.,1.);}';
var FRAG = 'precision highp float;uniform sampler2D tMap;uniform vec2 uMouse;uniform vec2 uVel;uniform float uStrength;' +
'uniform vec2 uScale;uniform vec2 uOffset;uniform float uAspect;varying vec2 vUv;' +
'void main(){vec2 d=vUv-uMouse;d.x*=uAspect;float f=smoothstep(.5,0.,length(d));' +
'vec2 uv=vUv-uVel*f*uStrength*.035;uv=clamp(uv,0.,1.)*uScale+uOffset;gl_FragColor=texture2D(tMap,uv);}';
M.register('fx', function () {
if (!M.fxOK) return;
var els = document.querySelectorAll('[data-fx="distort"]');
if (!els.length) return;
var fx = null, loading = null, failed = false;
function fail() {
failed = true;
document.documentElement.classList.remove('fx-on');
if (fx && fx.canvas && fx.canvas.parentNode) fx.canvas.remove();
fx = null;
}
function load() {
if (!loading) loading = import(OGL).then(function (ogl) { try { fx = build(ogl); } catch (e) { fail(); } }).catch(fail);
return loading;
}
function build(ogl) {
var renderer = new ogl.Renderer({ dpr: Math.min(window.devicePixelRatio || 1, 2), alpha: true, antialias: false });
var gl = renderer.gl;
if (!gl) throw new Error('sem WebGL');
var canvas = gl.canvas;
canvas.className = 'fx-canvas';
canvas.setAttribute('aria-hidden', 'true');
document.body.appendChild(canvas);
var tex = new ogl.Texture(gl, { generateMipmaps: false, minFilter: gl.LINEAR });
var U = {
tMap: { value: tex }, uMouse: { value: [0.5, 0.5] }, uVel: { value: [0, 0] }, uStrength: { value: 0 },
uScale: { value: [1, 1] }, uOffset: { value: [0, 0] }, uAspect: { value: 1 }
};
var prog = new ogl.Program(gl, { vertex: VERT, fragment: FRAG, uniforms: U, transparent: true });
var mesh = new ogl.Mesh(gl, { geometry: new ogl.Triangle(gl), program: prog });
var cur = null, img = null, raf = 0, w = 0, h = 0;
var mouse = { x: 0.5, y: 0.5, px: null, py: null }, vel = [0, 0], target = [0, 0];
var strength = 0, goal = 0;
function cover() {
var nw = img.naturalWidth, nh = img.naturalHeight, r = img.getBoundingClientRect();
var fit = getComputedStyle(img).objectFit;
if (fit === 'cover' && nw && nh) {
var s = Math.max(r.width / nw, r.height / nh);
var fx_ = r.width / (nw * s), fy = r.height / (nh * s);
U.uScale.value = [fx_, fy]; U.uOffset.value = [(1 - fx_) / 2, (1 - fy) / 2];
} else { U.uScale.value = [1, 1]; U.uOffset.value = [0, 0]; }
}
function frame() {
raf = 0;
if (!img) return;
var r = img.getBoundingClientRect();
if (Math.round(r.width) !== w || Math.round(r.height) !== h) {
w = Math.round(r.width); h = Math.round(r.height);
renderer.setSize(w, h);
cover();
}
canvas.style.transform = 'translate(' + r.left + 'px,' + r.top + 'px)';
target[0] *= 0.9; target[1] *= 0.9;
vel[0] += (target[0] - vel[0]) * 0.15; vel[1] += (target[1] - vel[1]) * 0.15;
strength += (goal - strength) * (goal > strength ? 0.12 : 0.09);
U.uVel.value = vel; U.uStrength.value = strength;
U.uMouse.value = [mouse.x, mouse.y]; U.uAspect.value = w / Math.max(h, 1);
renderer.render({ scene: mesh });
if (goal === 0 && strength < 0.01) { canvas.style.visibility = 'hidden'; img = null; cur = null; return; }
raf = requestAnimationFrame(frame);
}
function kick() { if (!raf) raf = requestAnimationFrame(frame); }
return {
canvas: canvas,
enter: function (el, e) {
var i = el.querySelector('img');
if (!i || !i.complete || !i.naturalWidth) return;
if (img !== i) { img = i; tex.image = i; w = h = 0; }
cur = el; goal = 1; mouse.px = null;
this.move(e);
canvas.style.visibility = 'visible';
kick();
},
move: function (e) {
if (!img || !e) return;
var r = img.getBoundingClientRect();
var x = (e.clientX - r.left) / r.width, y = 1 - (e.clientY - r.top) / r.height;
if (mouse.px !== null) {
target[0] = Math.max(-1, Math.min(1, (x - mouse.px) * 14));
target[1] = Math.max(-1, Math.min(1, (y - mouse.py) * 14));
}
mouse.px = x; mouse.py = y; mouse.x = x; mouse.y = y;
kick();
},
leave: function (el) { if (el === cur) { goal = 0; kick(); } }
};
}
els.forEach(function (el) {
el.addEventListener('pointerenter', function (e) {
if (failed || e.pointerType !== 'mouse') return;
load().then(function () { if (fx) fx.enter(el, e); });
});
el.addEventListener('pointermove', function (e) { if (fx) fx.move(e); });
el.addEventListener('pointerleave', function () { if (fx) fx.leave(el); });
});
});
})();

/* 65-vt.js */
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
addEventListener('pageshow', function (e) {
if (e.persisted) document.querySelectorAll('[style*=view-transition-name]').forEach(function (el) { el.style.viewTransitionName = ''; });
});
});
})();

/* 70-legal.js */
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

/* 90-boot.js */
(function () {
var M = window.MAYAA;
function boot() {
var t0 = performance.now();
M.modMs = {};
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

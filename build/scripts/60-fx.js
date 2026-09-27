/* Distorção WebGL leve no hover das imagens [data-fx="distort"] (§4.2 regra 7).
   Só modo completo, desktop com mouse, ≥1024 px, sem save-data. OGL carrega no 1.º pointerenter.
   Um canvas fixo reaproveitado sobre a imagem sob o ponteiro; deslocamento radial pela velocidade do ponteiro,
   força máxima 0,035 em UV, sem separação de cor. Falhou: tira `fx-on` e o hover CSS volta. */
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

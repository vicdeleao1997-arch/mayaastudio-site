// Palco 3D: quadrados de vidro laranja (o quadrado do monograma MAYAA) que acompanham a rolagem.
// Sem colisão por construção: cada peça ocupa uma esfera própria que nunca cruza a de outra.
// Peças só giram em torno do próprio centro; o grupo inteiro se move como um corpo rígido.
// Se o WebGL falhar, fica o fundo em CSS.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const M = window.MAYAA || { reduce: false, progress: 0, scene: 'hero' };
const canvas = document.getElementById('gl');
const small = matchMedia('(max-width: 720px)').matches;

// aparelho fraco ou economia de dados: fica só o fundo em CSS
if (navigator.connection?.saveData || (navigator.hardwareConcurrency || 8) <= 4) { canvas.remove(); throw new Error('MAYAA: 3D desligado neste aparelho'); }
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: !small, powerPreference: 'high-performance' });
} catch (e) { canvas.remove(); throw e; }
renderer.setPixelRatio(Math.min(devicePixelRatio, small ? 1.25 : 1.6));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, 1, .1, 100);
camera.position.set(0, 0, 11);

// fundo pintado: cinzas do brandbook, brilho laranja suave e uma sombra grafite (o vidro refrata isso)
function backdrop() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
  const g = c.getContext('2d');
  const lin = g.createLinearGradient(0, 0, 0, 1024);
  lin.addColorStop(0, '#F6F6F8'); lin.addColorStop(.55, '#E9E9ED'); lin.addColorStop(1, '#DCDDE2');
  g.fillStyle = lin; g.fillRect(0, 0, 1024, 1024);
  const rad = g.createRadialGradient(820, 880, 10, 820, 880, 640);
  rad.addColorStop(0, 'rgba(255,106,26,.75)'); rad.addColorStop(.4, 'rgba(255,150,90,.3)'); rad.addColorStop(1, 'rgba(255,106,26,0)');
  g.fillStyle = rad; g.fillRect(0, 0, 1024, 1024);
  const ink = g.createRadialGradient(960, 140, 10, 960, 140, 460);
  ink.addColorStop(0, 'rgba(38,38,43,.6)'); ink.addColorStop(1, 'rgba(38,38,43,0)');
  g.fillStyle = ink; g.fillRect(0, 0, 1024, 1024);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
scene.background = backdrop();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), .04).texture;

const key = new THREE.DirectionalLight(0xffffff, 2); key.position.set(-4, 6, 6); scene.add(key);
const rim = new THREE.PointLight(0xffb48a, 90, 30); rim.position.set(5, -3, 4); scene.add(rim);
const back = new THREE.PointLight(0xffffff, 50, 25); back.position.set(-5, 3, -4); scene.add(back);

// a peça: quadrado de cantos arredondados, proporção do quadrado laranja do monograma (raio 1/8 do lado)
const SIDE = 2, DEPTH = .34;
const geo = new RoundedBoxGeometry(SIDE, SIDE, DEPTH, small ? 4 : 6, .25);
const glass = new THREE.MeshPhysicalMaterial({
  color: new THREE.Color('#FF7A2E'), metalness: 0, roughness: .07,
  transmission: 1, thickness: 1.1, ior: 1.5,
  attenuationColor: new THREE.Color('#FF6A1A'), attenuationDistance: 1.4,
  clearcoat: 1, clearcoatRoughness: .04, iridescence: .2, iridescenceIOR: 1.3,
  envMapIntensity: 2, specularIntensity: 1
});
// raio da esfera que envolve a peça em qualquer rotação
const HALF_DIAG = Math.hypot(SIDE / 2, SIDE / 2, DEPTH / 2);
const BOB = .1;          // flutuação vertical máxima de cada peça
const GAP = .18;         // folga extra entre esferas

// sorteio determinístico (sempre o mesmo arranjo)
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function layout(count, seed) {
  const R = rng(seed), out = [];
  let tries = 0;
  while (out.length < count && tries < 20000) {
    tries++;
    const s = .8 + R() * .55;
    const p = new THREE.Vector3((R() - .5) * 5.2, (R() - .5) * 8.5, (R() - .5) * 4.5);
    const r = HALF_DIAG * s;
    const ok = out.every(o => o.p.distanceTo(p) > o.r + r + 2 * BOB + GAP);
    if (ok) out.push({ p, s, r });
  }
  return out;
}
const slots = layout(small ? 5 : 8, 20261115);

// conferência: nenhuma esfera cruza outra (aparece no console se algo mudar no arranjo)
let minGap = Infinity;
for (let i = 0; i < slots.length; i++) for (let j = i + 1; j < slots.length; j++)
  minGap = Math.min(minGap, slots[i].p.distanceTo(slots[j].p) - slots[i].r - slots[j].r - 2 * BOB);
console.assert(minGap > 0, 'MAYAA: peças com risco de colisão', minGap);
M.minGap = +minGap.toFixed(3); M.pieces = slots.length;

const group = new THREE.Group(); scene.add(group);
const pieces = slots.map((o, i) => {
  const m = new THREE.Mesh(geo, glass);
  m.scale.setScalar(o.s);
  m.position.copy(o.p);
  group.add(m);
  // face voltada para a câmera: oscila no máximo ~35°, gira livre só no próprio plano
  return { m, home: o.p.clone(), base: new THREE.Vector3((i % 3 - 1) * .25, (i % 4 - 1.5) * .2, i * .7), spinZ: (i % 2 ? 1 : -1) * (.08 + (i % 3) * .04), phase: i * 1.3 };
});

// pose do grupo por seção (corpo rígido: só posição, giro e escala uniforme)
const POSES = {
  hero:    { x: small ? .6 : 2.7,  y: 0,   z: 0,    s: 1,    rx: -.12, ry: .1,  focus: 12 },
  lift:    { x: 0,                 y: .6,  z: -1.5, s: 1.1,  rx: .1,   ry: -.3, focus: 13 },
  clients: { x: small ? 0 : -3.2,  y: 0,   z: -2,   s: .85,  rx: -.2,  ry: .35,  focus: 14 },
  dark:    { x: 0,                 y: 0,   z: -3,   s: .8,   rx: 0,    ry: .2, focus: 14 },
  stack:   { x: small ? 0 : 2.6,   y: -.3, z: 0,    s: 1.05, rx: .15,  ry: -.25, focus: 11.5 },
  stats:   { x: small ? 0 : 2.4,   y: .3,  z: .5,   s: 1.15, rx: -.1,  ry: .3, focus: 11 },
  finale:  { x: small ? 0 : 1.2,   y: 0,   z: .8,   s: 1.3,  rx: .05,  ry: -.1,   focus: 12 },
};
const cur = { ...POSES.hero };

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bokeh = new BokehPass(scene, camera, { focus: 12, aperture: small ? .0015 : .003, maxblur: small ? .006 : .011 });
if (!small) composer.addPass(bokeh); // no celular, sem desfoque (renderiza a cena de novo)
composer.addPass(new OutputPass());

function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false); composer.setSize(w, h);
  camera.aspect = w / h; camera.updateProjectionMatrix();
}
addEventListener('resize', resize); resize();

const mouse = new THREE.Vector2();
addEventListener('pointermove', e => mouse.set(e.clientX / innerWidth - .5, e.clientY / innerHeight - .5), { passive: true });
let visible = true;
document.addEventListener('visibilitychange', () => { visible = !document.hidden; });

const clock = new THREE.Clock();
const lerp = (a, b, k) => a + (b - a) * k;
function frame() {
  const dt = Math.min(clock.getDelta(), .05), t = clock.elapsedTime;
  const target = POSES[M.scene] || POSES.hero;
  const k = M.reduce ? 1 : 1 - Math.pow(.03, dt);
  for (const key in cur) cur[key] = lerp(cur[key], target[key], k);

  const p = M.reduce ? 0 : M.progress;
  // grupo rígido: a rolagem gira e desce o conjunto inteiro, nunca peça contra peça
  group.position.set(cur.x, cur.y - p * 1.2, cur.z);
  group.scale.setScalar(cur.s);
  group.rotation.set(cur.rx + mouse.y * .1, cur.ry + p * .9, mouse.x * -.06);

  for (const c of pieces) {
    c.m.position.set(c.home.x, c.home.y + (M.reduce ? 0 : Math.sin(t * .6 + c.phase) * BOB), c.home.z);
    const w = M.reduce ? 0 : 1;
    c.m.rotation.x = c.base.x + w * Math.sin(t * .35 + c.phase) * .45;
    c.m.rotation.y = c.base.y + w * Math.sin(t * .28 + c.phase * 1.7) * .55 - group.rotation.y * .85;
    c.m.rotation.z = c.base.z + w * t * c.spinZ;
  }
  camera.position.x = lerp(camera.position.x, mouse.x * .6, .05);
  camera.position.y = lerp(camera.position.y, -mouse.y * .4, .05);
  camera.lookAt(0, 0, 0);
  bokeh.uniforms.focus.value = cur.focus;

  if (visible && M.scene !== 'dark') composer.render(dt);
  if (!M.reduce) requestAnimationFrame(frame); else setTimeout(() => requestAnimationFrame(frame), 250);
}
frame();

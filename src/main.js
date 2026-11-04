import './styles.css';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { HainanEnvironment } from './environment.js';
import { plans, PLAN_KEY } from './plan.js';
import { I18N, LANGUAGES, getLang } from './i18n.js';
import { renderPanel } from './panel.js';
import { createRoamController } from './roam.js';

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

const langCodes = LANGUAGES.map((l) => l.code);
let lang = 'zh';
try { lang = localStorage.getItem('lanai-house-lang') || 'zh'; } catch (e) { lang = 'zh'; }
if (!langCodes.includes(lang)) lang = 'zh';
let t = getLang(lang);

// ------------------------------------------------------------------ renderer
const host = $('#scene');
const renderer = new THREE.WebGLRenderer({
  antialias: true, alpha: false, powerPreference: 'high-performance',
  stencil: false,
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.02;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
host.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 500);
camera.position.set(23, 16.5, 27);

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.inset = '0';
labelRenderer.domElement.style.pointerEvents = 'none';
$('#labels').appendChild(labelRenderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2.7, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.055;
controls.minDistance = 7;
controls.maxDistance = 74;
controls.maxPolarAngle = Math.PI / 2 - 0.025;
controls.minPolarAngle = 0.12;
controls.autoRotateSpeed = 0.42;
controls.update();

const env = new HainanEnvironment(renderer, scene);

// Ground beyond the walled site, built as four strips so the pool basin is
// never covered by a giant plane.
const outerGroundMat = new THREE.MeshStandardMaterial({ color: 0x4e5f42, roughness: 1, metalness: 0 });
function addGroundStrip(x0, x1, z0, z1) {
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, z1 - z0), outerGroundMat);
  mesh.rotation.x = -Math.PI / 2;
  mesh.position.set((x0 + x1) / 2, -0.03, (z0 + z1) / 2);
  mesh.receiveShadow = true;
  scene.add(mesh);
}
addGroundStrip(-110, 110, -110, -16);
addGroundStrip(-110, 110, 16, 110);
addGroundStrip(-110, -13, -16, 16);
addGroundStrip(13, 110, -16, 16);

// A loose ring of neighbouring trees hides the edge of the site and gives the
// garden a believable tropical horizon. Instanced for a single draw call.
function addTreeLine() {
  const count = 30;
  const trunkGeo = new THREE.CylinderGeometry(0.13, 0.24, 1, 6);
  const canopyGeo = new THREE.SphereGeometry(1, 10, 7);
  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x4a3a29, roughness: 1 });
  const canopyMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.98, flatShading: false });
  const trunks = new THREE.InstancedMesh(trunkGeo, trunkMat, count);
  const canopies = new THREE.InstancedMesh(canopyGeo, canopyMat, count * 3);
  const dummy = new THREE.Object3D();
  const rng = mulberry32(1907);
  const palette = [0x2d4631, 0x365138, 0x2a4230, 0x405b3d, 0x253d2b, 0x4b6240];
  let n = 0, c = 0;
  const used = [];
  for (let i = 0; i < count * 8 && n < count; i++) {
    const a = rng() * Math.PI * 2;
    const r = 26 + rng() * 17;
    const x = Math.cos(a) * r;
    const z = Math.sin(a) * r;
    if (Math.abs(x) < 18 && Math.abs(z) < 21) continue;
    if (used.some(u => (u.x - x) ** 2 + (u.z - z) ** 2 < 9)) continue;
    used.push({ x, z });
    const h = 4.2 + rng() * 4.4;
    dummy.position.set(x, h / 2, z);
    dummy.rotation.set(0, rng() * Math.PI, 0);
    dummy.scale.set(1 + rng() * 0.4, h, 1 + rng() * 0.4);
    dummy.updateMatrix();
    trunks.setMatrixAt(n, dummy.matrix);
    trunks.setColorAt(n, new THREE.Color(0x4a3a29));
    for (let j = 0; j < 3; j++) {
      const ca = rng() * Math.PI * 2;
      const cr = rng() * 1.4;
      const s = 1.15 + rng() * 1.15;
      dummy.position.set(x + Math.cos(ca) * cr, h * (0.78 + rng() * 0.22), z + Math.sin(ca) * cr);
      dummy.rotation.set(rng() * 0.4, rng() * Math.PI, rng() * 0.4);
      dummy.scale.set(s * (0.85 + rng() * 0.3), s * (0.7 + rng() * 0.4), s * (0.85 + rng() * 0.3));
      dummy.updateMatrix();
      canopies.setMatrixAt(c, dummy.matrix);
      canopies.setColorAt(c, new THREE.Color(palette[Math.floor(rng() * palette.length)]));
      c++;
    }
    n++;
  }
  trunks.count = n;
  canopies.count = c;
  trunks.castShadow = false;
  trunks.receiveShadow = true;
  canopies.castShadow = false;
  canopies.receiveShadow = true;
  scene.add(trunks, canopies);
}
function mulberry32(a) {
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
addTreeLine();

// post processing
const composer = new EffectComposer(renderer);
composer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
const renderPass = new RenderPass(scene, camera);
const bloom = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 0.14, 0.75, 0.92);
const outputPass = new OutputPass();
const gradePass = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uSat: { value: 1.12 }, uContrast: { value: 1.045 } },
  vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
  fragmentShader: `
    varying vec2 vUv; uniform sampler2D tDiffuse; uniform float uSat; uniform float uContrast;
    void main(){
      vec4 tex = texture2D(tDiffuse, vUv);
      vec3 c = tex.rgb;
      c = (c - 0.5) * uContrast + 0.5;
      float l = dot(c, vec3(0.2126, 0.7152, 0.0722));
      c = mix(vec3(l), c, uSat);
      c.r += 0.004; c.g += 0.002; c.b -= 0.002;
      gl_FragColor = vec4(clamp(c, 0.0, 1.0), tex.a);
    }
  `,
});
composer.addPass(renderPass);
composer.addPass(bloom);
composer.addPass(outputPass);
composer.addPass(gradePass);

// ------------------------------------------------------------------- model
const groups = {};
const emissiveMats = [];
const glassMats = [];
const windMats = [];
const materialSeen = new Set();
let water = null;
let waterNormal = null;
let model = null;
let loaded = false;
let ceilingGroup = null;

const ROOM_LABEL_POINTS = [
  ['ldk', 'LDK', -0.4, 2.5, 1.7],
  ['engawa', 'ENGawa', 0.8, 1.35, -4.55],
  ['master', 'MASTER', -2.9, 6.4, 1.6],
  ['kids', 'KIDS', -2.9, 6.4, -2.0],
  ['study', 'STUDY', 1.9, 6.4, 2.3],
  ['guest', 'GUEST', -6.7, 2.4, 0.2],
  ['pool', 'POOL', -4.6, 0.65, -8.8],
  ['pavilion', 'PAVILION', 4.6, 2.8, -9.1],
  ['carport', 'CARPORT', 9.2, 2.6, 1.2],
  ['shiro', 'SHIRO', -3.65, 1.35, 8.95],
];

const ROOM_VIEWS = {
  living: { pos: [8.8, 6.2, 10.5], target: [-0.4, 2.0, 1.0], fov: 42 },
  engawa: { pos: [4.2, 3.5, -8.2], target: [0.8, 1.6, -3.0], fov: 46 },
  master: { pos: [-9.8, 7.5, 8.0], target: [-3.0, 4.8, 1.0], fov: 42 },
  kids: { pos: [-8.8, 7.0, -4.6], target: [-2.9, 4.9, -2.0], fov: 44 },
  study: { pos: [7.7, 6.5, 8.2], target: [1.8, 4.8, 1.5], fov: 43 },
  pool: { pos: [-11.8, 4.6, -7.8], target: [-2.4, 0.9, -8.6], fov: 48 },
};

// -------------------------------------------------------------------- water
function setupWater(mesh) {
  waterNormal = new THREE.TextureLoader().load('/textures/water_normal.png');
  waterNormal.wrapS = waterNormal.wrapT = THREE.RepeatWrapping;
  waterNormal.repeat.set(4.5, 3.0);
  waterNormal.colorSpace = THREE.NoColorSpace;
  const mat = new THREE.MeshPhysicalMaterial({
    color: 0x178b92,
    roughness: 0.035,
    metalness: 0.08,
    transparent: true,
    opacity: 0.9,
    transmission: 0.08,
    thickness: 0.35,
    ior: 1.33,
    envMapIntensity: 1.8,
    normalMap: waterNormal,
    normalScale: new THREE.Vector2(0.42, 0.42),
    clearcoat: 1,
    emissive: 0x073f48,
    emissiveIntensity: 0.65,
    clearcoatRoughness: 0.08,
    side: THREE.DoubleSide,
  });
  mesh.material = mat;
  mesh.receiveShadow = false;
  mesh.castShadow = false;
  mesh.renderOrder = 3;
  // An animated caustic veil sits a few millimetres above the physical water.
  const causticMat = new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    uniforms: {
      uTime: { value: 0 },
      uOpacity: { value: 0.06 },
      uColor: { value: new THREE.Color(0xb8fff4) },
    },
    vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader: `
      varying vec2 vUv;
      uniform float uTime, uOpacity;
      uniform vec3 uColor;
      void main(){
        vec2 p = vUv * 10.0;
        float a = sin(p.x * 3.0 + uTime * 0.65 + sin(p.y * 2.4 + uTime * 0.22));
        float b = sin(p.y * 2.6 - uTime * 0.48 + sin(p.x * 1.9 - uTime * 0.31));
        float v = pow(abs(a * b), 2.4);
        float line = smoothstep(0.55, 1.0, v);
        float edge = smoothstep(0.0, 0.10, vUv.x) * (1.0 - smoothstep(0.90, 1.0, vUv.x))
                   * smoothstep(0.0, 0.10, vUv.y) * (1.0 - smoothstep(0.90, 1.0, vUv.y));
        gl_FragColor = vec4(uColor * line * 0.85, line * edge * uOpacity);
      }
    `,
  });
  const caustic = new THREE.Mesh(mesh.geometry, causticMat);
  caustic.position.copy(mesh.position);
  caustic.rotation.copy(mesh.rotation);
  caustic.scale.copy(mesh.scale);
  caustic.position.y += 0.012;
  caustic.renderOrder = 4;
  (mesh.parent || scene).add(caustic);
  // a small coral float gives the water a human scale
  const floatMat = new THREE.MeshStandardMaterial({ color: 0xe46b4d, roughness: 0.55, metalness: 0.05 });
  const floatRing = new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.075, 8, 20), floatMat);
  floatRing.rotation.x = -Math.PI / 2;
  floatRing.position.set(-4.9, 0.04, -8.4);
  floatRing.castShadow = true;
  scene.add(floatRing);
  water = { mesh, mat, caustic, causticMat };
}

function setupWind(material) {
  if (!material || !material.name) return;
  if (!/frond|leaf|foliage|banana/i.test(material.name)) return;
  if (material.userData.wind) return;
  material.userData.wind = true;
  material.side = THREE.DoubleSide;
  material.onBeforeCompile = (shader) => {
    shader.uniforms.uTime = { value: 0 };
    shader.vertexShader = 'uniform float uTime;\n' + shader.vertexShader;
    shader.vertexShader = shader.vertexShader.replace(
      '#include <begin_vertex>',
      `#include <begin_vertex>
       float h = smoothstep(0.15, 1.5, position.y);
       float sway = sin(uTime * 0.85 + position.x * 0.38 + position.z * 0.24) * 0.018 * h;
       transformed.x += sway;
       transformed.z += sway * 0.64;
       transformed.y += sin(uTime * 1.1 + position.x * 0.7) * 0.006 * h;`
    );
    material.userData.shader = shader;
  };
  material.needsUpdate = true;
  windMats.push(material);
}

function enhanceMaterial(mat) {
  if (!mat || materialSeen.has(mat.uuid)) return;
  materialSeen.add(mat.uuid);
  mat.envMapIntensity = 0.75;
  const name = mat.name || '';
  if (/glass/i.test(name)) {
    mat.transparent = true;
    mat.opacity = Math.min(mat.opacity ?? 0.32, 0.32);
    mat.depthWrite = false;
    mat.roughness = 0.05;
    mat.metalness = 0.22;
    mat.envMapIntensity = 2.0;
    mat.side = THREE.DoubleSide;
    glassMats.push(mat);
    return;
  }
  if (/lamp|paper lamp|warm lamp|led/i.test(name)) {
    mat.emissiveIntensity = name.match(/led/i) ? 1.2 : 1.8;
    emissiveMats.push(mat);
    return;
  }
  if (/pool mosaic|water/i.test(name)) {
    mat.envMapIntensity = 0.9;
  }
  if (/grass|lawn/i.test(name)) {
    mat.color.setHex(0x7d9367);
    mat.roughness = 1.0;
    mat.envMapIntensity = 0.3;
    return;
  }
  if (/tile|stone|plaster|teak|roof/i.test(name)) {
    mat.envMapIntensity = 0.45;
  }
  if (/foliage|frond|leaf|banana/i.test(name)) {
    mat.side = THREE.DoubleSide;
    mat.color.multiplyScalar(0.62);
    mat.roughness = Math.max(0.7, mat.roughness ?? 0.7);
    mat.envMapIntensity = 0.35;
    setupWind(mat);
  }
}

// Soft ceiling planes keep first-person interiors from showing the roof
// underside. They are hidden with the upper floor in the cutaway view.
function addCeilings() {
  if (ceilingGroup) return;
  ceilingGroup = new THREE.Group();
  ceilingGroup.name = 'CEILINGS';
  const mat = new THREE.MeshStandardMaterial({
    color: 0xffffff, roughness: 0.9, metalness: 0,
    emissive: 0xffefd6, emissiveIntensity: 0.92, side: THREE.DoubleSide,
  });
  const add = (x0, x1, z0, z1, y) => {
    const geo = new THREE.PlaneGeometry(x1 - x0, z1 - z0);
    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.set((x0 + x1) / 2, y, (z0 + z1) / 2);
    mesh.receiveShadow = true;
    ceilingGroup.add(mesh);
  };
  add(-8.4, -5.0, -3.4, 2.6, 3.28);
  add(-5.0, 3.45, -3.8, 4.2, 3.28);
  add(3.45, 5.4, -3.8, -2.8, 3.28);
  add(3.45, 5.4, 1.8, 4.2, 3.28);
  add(-5.0, 3.45, -3.8, 4.2, 6.86);
  add(3.45, 5.4, -3.8, -2.8, 6.86);
  add(3.45, 5.4, 1.8, 4.2, 6.86);
  scene.add(ceilingGroup);
}

// ------------------------------------------------------------------- labels
const labelObjects = [];
const labelEls = {};
function createLabels() {
  for (const [key, en, x, y, z] of ROOM_LABEL_POINTS) {
    const el = document.createElement('div');
    el.className = 'room-label';
    el.innerHTML = `<span class="label-dot"></span><b>${t.labels[key]}</b><small>${en}</small>`;
    const obj = new CSS2DObject(el);
    obj.position.set(x, y, z);
    scene.add(obj);
    labelObjects.push(obj);
    labelEls[key] = el;
  }
}
function refreshLabels() {
  for (const [key, en] of ROOM_LABEL_POINTS) {
    if (labelEls[key]) labelEls[key].innerHTML = `<span class="label-dot"></span><b>${t.labels[key]}</b><small>${en}</small>`;
  }
}

function setLabels(on) {
  $('#labels').classList.toggle('is-on', on);
  $('#labelToggle').classList.toggle('is-on', on);
  $('#labelToggle').setAttribute('aria-pressed', String(on));
}

// ------------------------------------------------------------------ loading
const loader = new GLTFLoader();
let loadStart = performance.now();
loader.load('/models/lanai_house.glb', (gltf) => {
  model = gltf.scene;
  model.name = 'LANAI_HOUSE';
  model.traverse((o) => {
    if (!o.isMesh) return;
    o.castShadow = true;
    o.receiveShadow = true;
    const mats = Array.isArray(o.material) ? o.material : [o.material];
    for (const m of mats) enhanceMaterial(m);
    if (o.name === 'POOL_Water') setupWater(o);
  });
  // group toggles
  for (const name of ['ROOF_All', 'F2_House', 'F2_Interior', 'GF_House', 'GF_Interior', 'GF_Trim', 'SITE_All', 'POOL_All', 'LANDSCAPE_All']) {
    const obj = model.getObjectByName(name);
    if (obj) groups[name] = obj;
  }
  scene.add(model);
  createLabels();
  addCeilings();
  setLabels(false);
  loaded = true;
  $('#loadingBar').style.width = '100%';
  $('#loadingPct').textContent = '100%';
  setTimeout(() => {
    $('#loading').classList.add('is-hidden');
    document.body.classList.add('is-ready');
  }, 450);
  // intro camera glide
  setView('overview', true);
}, (xhr) => {
  if (xhr.total) {
    const pct = clamp(Math.round(xhr.loaded / xhr.total * 100), 0, 99);
    $('#loadingBar').style.width = pct + '%';
    $('#loadingPct').textContent = pct + '%';
  } else {
    const pct = clamp(Math.round((xhr.loaded / (17.5 * 1024 * 1024)) * 100), 0, 99);
    $('#loadingBar').style.width = pct + '%';
    $('#loadingPct').textContent = pct + '%';
  }
}, (err) => {
  console.error(err);
  $('#loading').classList.add('is-hidden');
  $('#error').classList.add('is-on');
  $('#errorText').textContent = '模型文件没有加载成功。请确认 public/models/lanai_house.glb 存在，并通过本地开发服务器打开页面。';
});

// --------------------------------------------------------------- interior lights
const warmLights = [];
const nightSprites = [];
function addInteriorLight(x, y, z, intensity = 10, distance = 6.5, color = 0xffc58d) {
  const light = new THREE.PointLight(color, 0, distance, 1.7);
  light.position.set(x, y, z);
  scene.add(light);
  warmLights.push({ light, day: 0, dusk: intensity * 0.28, night: intensity });
}
addInteriorLight(-0.4, 2.9, 1.8, 30, 8.0);
addInteriorLight(-0.3, 2.9, -0.5, 24, 6.5);
addInteriorLight(-1.4, 2.7, -2.6, 18, 5.5);
addInteriorLight(1.8, 2.5, 3.8, 16, 5.0);
addInteriorLight(-2.9, 5.7, 1.6, 24, 6.0);
addInteriorLight(-2.9, 5.7, -2.0, 20, 5.5);
addInteriorLight(1.8, 5.7, 2.3, 20, 5.5);
addInteriorLight(-6.7, 2.5, 0.4, 17, 5.0);
addInteriorLight(4.6, 2.3, -9.0, 13, 4.5);
// path and garden lights
for (const [x, z] of [[1.4, 13.2], [1.4, 9.9], [1.4, 6.7], [-7.8, -6.8], [6.5, -6.3], [11.8, 3.8]]) {
  addInteriorLight(x, 0.6, -z, 5.5, 4.0, 0xffb86b);
}
// cyan pool light
const poolLight = new THREE.PointLight(0x65e0d5, 0, 4.5, 1.8);
poolLight.position.set(-4.6, -0.3, -8.8);
scene.add(poolLight);

// fireflies
const fireflyCount = 48;
const ffGeo = new THREE.BufferGeometry();
const ffPos = new Float32Array(fireflyCount * 3);
const ffSeeds = [];
for (let i = 0; i < fireflyCount; i++) {
  const x = -9 + Math.random() * 18;
  const z = -14 + Math.random() * 11;
  ffPos[i*3] = x; ffPos[i*3+1] = 0.4 + Math.random() * 1.8; ffPos[i*3+2] = z;
  ffSeeds.push({ phase: Math.random() * Math.PI * 2, speed: 0.3 + Math.random() * 0.5, r: 0.35 + Math.random() * 0.6, x, z });
}
ffGeo.setAttribute('position', new THREE.BufferAttribute(ffPos, 3));
const ffMat = new THREE.PointsMaterial({ color: 0xffd27a, size: 0.055, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
const fireflies = new THREE.Points(ffGeo, ffMat);
scene.add(fireflies);

// warm festival bulbs on the pavilion and veranda
const stringBulbs = new THREE.Group();
const bulbGeo = new THREE.SphereGeometry(0.035, 6, 4);
const bulbMat = new THREE.MeshBasicMaterial({ color: 0xffcc7a, transparent: true, opacity: 0.35 });
const bulbPositions = [];
for (let i = 0; i < 11; i++) bulbPositions.push([2.75 + i * 0.37, 2.86, -6.92]);
for (let i = 0; i < 9; i++) bulbPositions.push([2.75, 2.86, -7.05 - i * 0.43]);
for (let i = 0; i < 9; i++) bulbPositions.push([6.62, 2.86, -7.05 - i * 0.43]);
for (let i = 0; i < 7; i++) bulbPositions.push([-3.25 + i * 0.55, 3.16, -5.12]);
for (const [x, y, z] of bulbPositions) {
  const b = new THREE.Mesh(bulbGeo, bulbMat);
  b.position.set(x, y, z);
  stringBulbs.add(b);
}
scene.add(stringBulbs);

// ------------------------------------------------------------------- camera
const VIEWS = {
  overview: { pos: [24, 12.8, 27], target: [0, 4.1, 0], fov: 37 },
  entry: { pos: [9.2, 4.4, 17.2], target: [1.7, 2.5, 4.2], fov: 40 },
  garden: { pos: [-16.5, 7.8, -18.2], target: [0.2, 2.6, -6.0], fov: 42 },
  pool: { pos: [-11.8, 4.6, -7.8], target: [-2.4, 0.9, -8.6], fov: 48 },
  cutaway: { pos: [15.5, 18.5, 19.5], target: [0, 2.0, 0], fov: 40 },
};

let viewTween = null;
function tweenView(view, duration = 1.5) {
  const from = {
    pos: camera.position.clone(),
    target: controls.target.clone(),
    fov: camera.fov,
  };
  const to = {
    pos: new THREE.Vector3(...view.pos),
    target: new THREE.Vector3(...view.target),
    fov: view.fov ?? camera.fov,
  };
  viewTween = { from, to, t: 0, duration, started: performance.now() };
  controls.enabled = false;
}
function setView(name, immediate = false) {
  const view = VIEWS[name];
  if (!view) return;
  if (name === 'cutaway') {
    setRoof(false);
    setFloor(false);
  } else {
    setRoof(true);
    setFloor(true);
  }
  if (immediate) {
    camera.position.set(...view.pos);
    controls.target.set(...view.target);
    camera.fov = view.fov;
    camera.updateProjectionMatrix();
    controls.update();
    return;
  }
  tweenView(view);
  $$('.dock-btn').forEach(b => b.classList.toggle('is-active', b.dataset.view === name));
}

function updateTween(now) {
  if (!viewTween) return;
  const p = clamp((now - viewTween.started) / (viewTween.duration * 1000), 0, 1);
  const e = 1 - Math.pow(1 - p, 3);
  camera.position.lerpVectors(viewTween.from.pos, viewTween.to.pos, e);
  controls.target.lerpVectors(viewTween.from.target, viewTween.to.target, e);
  camera.fov = THREE.MathUtils.lerp(viewTween.from.fov, viewTween.to.fov, e);
  camera.updateProjectionMatrix();
  controls.update();
  if (p >= 1) {
    viewTween = null;
    controls.enabled = true;
  }
}

// --------------------------------------------------------------- film mode
let cinema = null;
const cinemaTitle = $('#cinemaTitle');

function defaultCinemaKeyframes() {
  const k = [
    { t: 0.0, pos: [24, 12, 27], target: [0, 4.2, 0], fov: 38 },
    { t: 3.6, pos: [24, 12, 26], target: [0, 4.2, 0], fov: 38 },
  ];
  for (let i = 0; i <= 18; i++) {
    const a = 0.9 + (Math.PI * 2 * i) / 18;
    k.push({
      t: 4.2 + i * 0.65,
      pos: [Math.cos(a) * 25, 10.6 + Math.sin(i * 0.6) * 1.4, Math.sin(a) * 25],
      target: [0, 4.2, 0], fov: 38,
    });
  }
  k.push(
    { t: 17.5, pos: [14.0, 8.5, 20.0], target: [0, 4.0, 2.0], fov: 42 },
    { t: 19.0, pos: [2.6, 2.00, 3.7], target: [0.8, 1.8, 1.0], fov: 62 },
    { t: 21.5, pos: [2.8, 2.20, 0.9], target: [-1.0, 1.7, -2.3], fov: 60 },
    { t: 24.0, pos: [2.9, 2.20, 2.6], target: [-1.4, 1.5, 1.0], fov: 58 },
    { t: 26.5, pos: [2.3, 2.10, 2.5], target: [4.2, 1.5, -1.8], fov: 58 },
    { t: 29.0, pos: [-10.8, 2.8, -6.5], target: [-2.6, 1.4, -8.3], fov: 54 },
    { t: 32.5, pos: [-9.4, 3.6, -11.0], target: [-2.6, 1.2, -7.6], fov: 50 },
    { t: 35.0, pos: [-1.7, 5.2, 0.35], target: [-2.6, 4.6, 2.8], fov: 62 },
    { t: 37.5, pos: [1.0, 5.2, 1.8], target: [1.5, 4.7, -1.0], fov: 60 },
    { t: 39.5, pos: [18, 12, 24], target: [0, 4.2, 0], fov: 40 },
    { t: 42.5, pos: [24, 13, 18], target: [0, 4.2, 0], fov: 40 },
    { t: 46.0, pos: [24, 12, 27], target: [0, 4.2, 0], fov: 38 },
  );
  return k;
}

function showCinemaTitle(on) {
  if (!cinemaTitle) return;
  cinemaTitle.classList.toggle('is-on', Boolean(on));
}

function startCinema(keyframes, duration = 46) {
  if (!loaded) return false;
  const frames = (keyframes && keyframes.length ? keyframes : defaultCinemaKeyframes())
    .slice().sort((a, b) => a.t - b.t);
  if (!frames.length) return false;
  closePanel?.();
  closeRoom?.();
  closePlan?.();
  setRoof(true);
  setFloor(true);
  setLabels(false);
  controls.enabled = false;
  controls.autoRotate = false;
  viewTween = null;
  document.body.classList.add('cinema');
  showCinemaTitle(true);
  const fade = setTimeout(() => showCinemaTitle(false), 2800);
  cinema = { frames, duration, elapsed: 0, fade, saved: {
    pos: camera.position.clone(), quat: camera.quaternion.clone(), fov: camera.fov,
    target: controls.target.clone(),
  }};
  const f = frames[0];
  camera.position.set(...f.pos);
  camera.lookAt(new THREE.Vector3(...f.target));
  camera.fov = f.fov ?? camera.fov;
  camera.updateProjectionMatrix();
  return true;
}

function stopCinema() {
  if (!cinema) return;
  clearTimeout(cinema.fade);
  document.body.classList.remove('cinema');
  showCinemaTitle(false);
  const saved = cinema.saved;
  cinema = null;
  if (saved) {
    camera.position.copy(saved.pos);
    camera.quaternion.copy(saved.quat);
    camera.fov = saved.fov;
    camera.updateProjectionMatrix();
    controls.target.copy(saved.target);
    controls.enabled = true;
  }
}

function updateCinema(dt) {
  if (!cinema) return;
  cinema.elapsed = Math.min(cinema.elapsed + dt, cinema.duration);
  const t = cinema.elapsed;
  const frames = cinema.frames;
  let i = 0;
  while (i < frames.length - 2 && t > frames[i + 1].t) i++;
  const a = frames[i];
  const b = frames[Math.min(i + 1, frames.length - 1)];
  const span = Math.max(0.001, b.t - a.t);
  const raw = clamp((t - a.t) / span, 0, 1);
  const u = raw * raw * (3 - 2 * raw);
  camera.position.set(
    THREE.MathUtils.lerp(a.pos[0], b.pos[0], u),
    THREE.MathUtils.lerp(a.pos[1], b.pos[1], u),
    THREE.MathUtils.lerp(a.pos[2], b.pos[2], u),
  );
  camera.lookAt(new THREE.Vector3(
    THREE.MathUtils.lerp(a.target[0], b.target[0], u),
    THREE.MathUtils.lerp(a.target[1], b.target[1], u),
    THREE.MathUtils.lerp(a.target[2], b.target[2], u),
  ));
  const fov = THREE.MathUtils.lerp(a.fov ?? camera.fov, b.fov ?? camera.fov, u);
  if (Math.abs(camera.fov - fov) > 0.01) {
    camera.fov = fov;
    camera.updateProjectionMatrix();
  }
}

// visibility toggles
let roofVisible = true;
let floorVisible = true;
function applyVisibility() {
  if (groups.ROOF_All) groups.ROOF_All.visible = roofVisible;
  if (groups.F2_House) groups.F2_House.visible = floorVisible;
  if (groups.F2_Interior) groups.F2_Interior.visible = floorVisible;
  if (ceilingGroup) ceilingGroup.visible = floorVisible;
  $('#roofToggle').classList.toggle('is-on', roofVisible);
  $('#roofToggle').classList.toggle('is-off', !roofVisible);
  $('#floorToggle').classList.toggle('is-on', floorVisible);
  $('#floorToggle').classList.toggle('is-off', !floorVisible);
}
function setRoof(v) { roofVisible = v; applyVisibility(); }
function setFloor(v) { floorVisible = v; applyVisibility(); }

// UI bindings
$$('.dock-btn').forEach(btn => {
  btn.addEventListener('click', () => setView(btn.dataset.view));
});
$('#roofToggle').addEventListener('click', () => setRoof(!roofVisible));
$('#floorToggle').addEventListener('click', () => setFloor(!floorVisible));

const panelEl = $('#panel');
function isMobileLayout() { return window.innerWidth <= 920; }
function openPanel() {
  if (isMobileLayout()) {
    panelEl.classList.add('is-open');
    document.body.classList.add('panel-open');
    document.body.classList.remove('panel-collapsed');
  } else {
    panelEl.classList.remove('is-closed');
    document.body.classList.remove('panel-collapsed');
  }
  $('#panelToggle').setAttribute('aria-expanded', 'true');
}
function closePanel() {
  if (isMobileLayout()) {
    panelEl.classList.remove('is-open');
    document.body.classList.remove('panel-open');
  } else {
    panelEl.classList.add('is-closed');
    document.body.classList.add('panel-collapsed');
  }
  $('#panelToggle').setAttribute('aria-expanded', 'false');
}
function togglePanel() {
  const open = isMobileLayout()
    ? panelEl.classList.contains('is-open')
    : !panelEl.classList.contains('is-closed');
  if (open) closePanel(); else openPanel();
}
$('#panelToggle').addEventListener('click', togglePanel);
$('#panelReopen').addEventListener('click', openPanel);
panelEl.addEventListener('click', (e) => {
  if (e.target.closest('[data-action="close-panel"]')) { closePanel(); return; }
  const row = e.target.closest('.room-row');
  if (row) openRoom(row.dataset.room);
});
$$('.topnav button[data-scroll]').forEach(btn => {
  btn.addEventListener('click', () => {
    openPanel();
    const target = document.getElementById(btn.dataset.scroll);
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// time
$$('.time-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('.time-btn').forEach(b => b.classList.toggle('is-active', b === btn));
    env.setMode(btn.dataset.time);
    document.body.dataset.time = btn.dataset.time;
  });
});

// auto rotate
$('#autoRotate').addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  $('#autoRotate').classList.toggle('is-on', controls.autoRotate);
});

// ------------------------------------------------------------------- i18n
let roamController = null;

function renderPanelContent() {
  const previous = panelEl.querySelector('.panel-inner');
  const scrollTop = previous ? previous.scrollTop : 0;
  panelEl.innerHTML = renderPanel(t);
  const next = panelEl.querySelector('.panel-inner');
  if (next) next.scrollTop = scrollTop;
}

function setLanguage(code, save = true) {
  const nextCode = I18N[code] ? code : 'zh';
  lang = nextCode;
  t = getLang(lang);
  const language = LANGUAGES.find((l) => l.code === lang) || LANGUAGES[0];
  document.documentElement.lang = language.htmlLang;
  document.title = t.meta.title;
  const desc = document.querySelector('meta[name="description"]');
  if (desc) desc.setAttribute('content', t.meta.description);

  $$('.topnav button[data-scroll]').forEach((b, i) => { b.textContent = t.nav[i]; });
  $('#planOpenTop').textContent = t.nav[4];
  $$('.dock-btn').forEach((b, i) => {
    const item = t.ui.dock[i];
    if (!item) return;
    b.querySelector('span').textContent = item[0];
    b.querySelector('small').textContent = item[1];
  });
  $('#roamToggle span').textContent = t.ui.tools.roam;
  $('#roofToggle span').textContent = t.ui.tools.roof;
  $('#floorToggle span').textContent = t.ui.tools.floor;
  $('#labelToggle span').textContent = t.ui.tools.labels;
  $('#planOpen span').textContent = t.ui.tools.plan;
  $('.time-label').textContent = t.ui.time.label;
  $$('.time-btn').forEach((b) => { b.textContent = t.ui.time[b.dataset.time]; });
  $('.hint').innerHTML = `<span class="dot"></span>${t.ui.hint}`;
  $('#autoRotate').title = t.ui.autoRotate;
  $('#autoRotate').setAttribute('aria-label', t.ui.autoRotate);
  $('#panelToggle').title = t.ui.panelToggle;
  $('#panelToggle').setAttribute('aria-label', t.ui.panelToggle);
  $('#panelReopen').setAttribute('aria-label', t.ui.panelReopen);
  $('#roomCardFocus').innerHTML = `${t.ui.roomCardFocus} <span>↗</span>`;
  $('#loading .loading-title').textContent = t.ui.loading.title;
  $('#loading .loading-sub').textContent = t.ui.loading.sub;
  $('#error h2').textContent = t.ui.error.title;
  $('#error p').textContent = t.ui.error.text;

  $('.plan-modal-head .eyebrow').textContent = t.ui.plan.eyebrow;
  $('.plan-modal-head h2').innerHTML = `${t.ui.plan.title} <span>${t.ui.plan.titleEn}</span>`;
  $('.plan-note').textContent = t.ui.plan.note;
  const legendClasses = ['lg-wall', 'lg-wet', 'lg-deck', 'lg-pool'];
  $('.plan-legend').innerHTML = t.ui.plan.legend.map((label, i) =>
    `<span><i class="${legendClasses[i]}"></i>${label}</span>`).join('') +
    '<span class="plan-scale">0&nbsp;&nbsp;1&nbsp;&nbsp;2&nbsp;&nbsp;3 m</span>';
  $$('.plan-tab').forEach((b, i) => { b.textContent = t.ui.plan.tabs[i]; });

  $('#roamBadgeSub').textContent = t.ui.roam.sub;
  $('#roamBadge').textContent = t.ui.roam.badge;
  $('#roamExit span').textContent = t.ui.roam.exit;
  $('#roamHelp').textContent = t.ui.roam.hint;
  $('#roamCurrentLabel').textContent = t.ui.roam.current;
  $('#roamLockHint').textContent = t.ui.roam.click;
  $$('.roam-floor-btn').forEach((b) => {
    b.setAttribute('aria-label', b.dataset.floor === '1' ? t.ui.roam.f1 : t.ui.roam.f2);
  });

  renderPanelContent();
  refreshLabels();
  if (currentRoomKey) updateRoomCard();
  if (planModal.classList.contains('is-open')) renderPlan();
  if (roamController) roamController.setLanguage(t);
  const select = $('#langSelect');
  if (select) select.value = lang;
  if (save) {
    try { localStorage.setItem('lanai-house-lang', lang); } catch (e) {}
  }
}

const langSelect = $('#langSelect');
for (const language of LANGUAGES) {
  const option = document.createElement('option');
  option.value = language.code;
  option.textContent = language.label;
  langSelect.appendChild(option);
}
langSelect.value = lang;
langSelect.addEventListener('change', (e) => setLanguage(e.target.value));

// room panel interactions
const roomCard = $('#roomCard');
let currentRoomKey = null;
function updateRoomCard() {
  if (!currentRoomKey) return;
  const room = t.rooms[currentRoomKey];
  if (!room) return;
  $('#roomCardKicker').textContent = room.kicker;
  $('#roomCardTitle').textContent = room.title;
  $('#roomCardText').textContent = room.text;
  $('#roomCardMeta').innerHTML = room.meta.map(m => `<span>${m}</span>`).join('');
  $('#roomCardFocus').innerHTML = `${t.ui.roomCardFocus} <span>↗</span>`;
}
function openRoom(key) {
  if (window.innerWidth <= 920) {
    document.body.classList.remove('panel-open');
    $('#panel').classList.remove('is-open');
  }
  const room = t.rooms[key];
  const view = ROOM_VIEWS[key];
  if (!room) return;
  currentRoomKey = key;
  updateRoomCard();
  roomCard.classList.add('is-open');
  if (view) {
    viewTween = null;
    controls.enabled = true;
    tweenView(view, 1.4);
    $$('.dock-btn').forEach(b => b.classList.remove('is-active'));
  }
}
function closeRoom() {
  roomCard.classList.remove('is-open');
  currentRoomKey = null;
}
$('#roomCardClose').addEventListener('click', closeRoom);
$('#roomCardFocus').addEventListener('click', () => {
  const view = currentRoomKey ? ROOM_VIEWS[currentRoomKey] : null;
  if (view) {
    tweenView(view, 1.4);
    if (window.innerWidth <= 920) roomCard.classList.remove('is-open');
  }
});

// plan modal
const planModal = $('#planModal');
let currentPlan = 'gf';
function localizePlanLabels() {
  $$('#planStage .plan-label').forEach((el) => {
    const key = PLAN_KEY[el.textContent.trim()];
    if (key && t.plan.labels[key]) el.textContent = t.plan.labels[key];
  });
}
function renderPlan() {
  $('#planStage').innerHTML = plans[currentPlan]();
  localizePlanLabels();
  $$('.plan-tab').forEach((b, i) => {
    b.textContent = t.ui.plan.tabs[i];
    b.classList.toggle('is-active', b.dataset.plan === currentPlan);
  });
}
function openPlan() {
  if (isMobileLayout()) closePanel();
  renderPlan();
  planModal.classList.add('is-open');
  planModal.setAttribute('aria-hidden', 'false');
  closeRoom();
}
function closePlan() {
  planModal.classList.remove('is-open');
  planModal.setAttribute('aria-hidden', 'true');
}
$('#planOpen').addEventListener('click', openPlan);
$('#planOpenTop').addEventListener('click', openPlan);
$('#planClose').addEventListener('click', closePlan);
$$('.plan-tab').forEach(btn => btn.addEventListener('click', () => {
  currentPlan = btn.dataset.plan;
  renderPlan();
}));
$('#labelToggle').addEventListener('click', () => {
  const on = !$('#labels').classList.contains('is-on');
  setLabels(on);
});
document.addEventListener('keydown', (e) => {
  if (roamController?.active && e.code === 'KeyL') {
    const next = langCodes[(langCodes.indexOf(lang) + 1) % langCodes.length];
    setLanguage(next);
    e.preventDefault();
    return;
  }
  if (e.key.toLowerCase() === 'h') document.body.classList.toggle('is-present');
  if (e.key === 'Escape') {
    if (planModal.classList.contains('is-open')) closePlan();
    else closeRoom();
  }
});

// ------------------------------------------------------------------- resize
function onResize() {
  const w = window.innerWidth, h = window.innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  composer.setSize(w, h);
  labelRenderer.setSize(w, h);
  bloom.resolution.set(w * Math.min(window.devicePixelRatio || 1, 2), h * Math.min(window.devicePixelRatio || 1, 2));
}
window.addEventListener('resize', onResize);

// ------------------------------------------------------------------- animate
const clock = new THREE.Clock();
let elapsed = 0;

function updateLights(mode) {
  const lit = mode === 'night' ? 1 : mode === 'dusk' ? 0.32 : 0;
  for (const w of warmLights) w.light.intensity = w.night * lit;
  poolLight.intensity = mode === 'night' ? 18 : mode === 'dusk' ? 5 : 1.5;
  for (const m of emissiveMats) {
    if (/led/i.test(m.name || '')) m.emissiveIntensity = mode === 'night' ? 2.2 : 0.8;
    else m.emissiveIntensity = mode === 'night' ? 2.8 : mode === 'dusk' ? 1.2 : 0.5;
  }
  for (const g of glassMats) {
    g.opacity = mode === 'night' ? 0.34 : 0.27;
    g.envMapIntensity = mode === 'night' ? 0.9 : 2.0;
  }
  ffMat.opacity = mode === 'night' ? 0.9 : 0;
  bulbMat.opacity = mode === 'night' ? 1 : mode === 'dusk' ? 0.55 : 0.28;
  if (water) {
    water.mat.color.set(mode === 'night' ? 0x146d78 : mode === 'dusk' ? 0x18747e : 0x178b92);
    water.mat.emissiveIntensity = mode === 'night' ? 0.9 : 0.45;
    water.mat.envMapIntensity = mode === 'night' ? 1.4 : 1.8;
  }
}
document.body.dataset.time = 'day';
updateLights('day');

function animate() {
  requestAnimationFrame(animate);
  const rawDt = clock.getDelta();
  const dt = Math.min(rawDt, 0.05);
  elapsed += dt;
  env.update(dt, elapsed);
  if (cinema) {
    updateCinema(rawDt);
  } else if (roamController?.active) {
    roamController.update(dt);
  } else {
    updateTween(performance.now());
  }
  updateLights(env.mode === 'night' ? 'night' : env.mode === 'dusk' ? 'dusk' : 'day');
  bloom.strength = THREE.MathUtils.lerp(bloom.strength, env.target.bloom, 0.04);
  if (waterNormal) {
    waterNormal.offset.x += dt * 0.012;
    waterNormal.offset.y += dt * 0.007;
  }
  if (water?.causticMat) {
    water.causticMat.uniforms.uTime.value = elapsed;
    water.causticMat.uniforms.uOpacity.value = env.mode === 'night' ? 0.13 : env.mode === 'dusk' ? 0.09 : 0.06;
  }
  for (const m of windMats) {
    if (m.userData.shader) m.userData.shader.uniforms.uTime.value = elapsed;
  }
  // slow fireflies
  const arr = ffGeo.attributes.position.array;
  for (let i = 0; i < fireflyCount; i++) {
    const s = ffSeeds[i];
    arr[i*3] = s.x + Math.sin(elapsed * s.speed + s.phase) * s.r;
    arr[i*3+1] = 0.45 + Math.sin(elapsed * s.speed * 1.4 + s.phase) * 0.7 + 0.7;
    arr[i*3+2] = s.z + Math.cos(elapsed * s.speed * 1.2 + s.phase) * s.r;
  }
  ffGeo.attributes.position.needsUpdate = true;
  if (water) water.mat.normalMap.offset.x = waterNormal.offset.x;
  if (!roamController?.active && !cinema) controls.update();
  composer.render();
  labelRenderer.render(scene, camera);
}
animate();

// ------------------------------------------------------------------- roam
roamController = createRoamController({
  camera,
  controls,
  domElement: renderer.domElement,
  closePanel,
  closeRoom,
  closePlan,
  setRoof,
  setFloor,
  setLabels,
  isLabelsOn: () => $('#labels').classList.contains('is-on'),
});
$('#roamToggle').addEventListener('click', () => {
  if (roamController.active) roamController.stop();
  else roamController.start();
});

setLanguage(lang, false);

// expose for local inspection / screenshots
window.__VILLA__ = {
  scene, camera, renderer, controls, env, setView, setRoof, setFloor, openPlan, closePlan,
  setLanguage, openPanel, closePanel, startCinema, stopCinema, showCinemaTitle,
  get roam() { return roamController; }, get cinema() { return cinema; },
  get loaded() { return loaded; },
};

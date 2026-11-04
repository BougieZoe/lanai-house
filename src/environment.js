import * as THREE from 'three';

const MODES = {
  morning: {
    top: 0x3d7397, horizon: 0xf3d6b8, bottom: 0x8b8066,
    sun: 0xffd59c, sunIntensity: 3.0, hemiSky: 0xe8d5c0, hemiGround: 0x5d624e,
    hemi: 0.82, ambient: 0.10, fog: 0xd8bda2, fogDensity: 0.0040,
    exposure: 1.04, stars: 0, clouds: 0.50, env: 0.72, bloom: 0.16,
    sunDir: new THREE.Vector3(-0.55, 0.30, 0.62).normalize(),
  },
  day: {
    top: 0x245f92, horizon: 0xc8d9dc, bottom: 0x6c7c66,
    sun: 0xffefd2, sunIntensity: 4.1, hemiSky: 0xbfd8e9, hemiGround: 0x5b654c,
    hemi: 0.68, ambient: 0.05, fog: 0x91aaa5, fogDensity: 0.0018,
    exposure: 1.0, stars: 0, clouds: 0.55, env: 0.9, bloom: 0.12,
    sunDir: new THREE.Vector3(0.45, 0.78, 0.38).normalize(),
  },
  dusk: {
    top: 0x4f5e89, horizon: 0xf2b681, bottom: 0x6f5e50,
    sun: 0xffb36c, sunIntensity: 2.35, hemiSky: 0xe4b58e, hemiGround: 0x4e4d3d,
    hemi: 0.92, ambient: 0.15, fog: 0xc49d85, fogDensity: 0.007,
    exposure: 1.08, stars: 0.08, clouds: 0.78, env: 0.6, bloom: 0.25,
    sunDir: new THREE.Vector3(-0.72, 0.20, 0.24).normalize(),
  },
  night: {
    top: 0x071321, horizon: 0x142b38, bottom: 0x0a1412,
    sun: 0x9fc6e8, sunIntensity: 0.38, hemiSky: 0x36536f, hemiGround: 0x17251e,
    hemi: 0.62, ambient: 0.13, fog: 0x1a2b31, fogDensity: 0.0035, exposure: 1.10, moon: 0.65,
    stars: 0.85, clouds: 0.14, env: 0.3, bloom: 0.5,
    sunDir: new THREE.Vector3(0.38, 0.70, -0.42).normalize(),
  },
};

function cloudTexture() {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 256;
  const g = c.getContext('2d');
  g.clearRect(0, 0, 512, 256);
  const blobs = [
    [120, 150, 80, 40], [180, 120, 110, 54], [260, 145, 128, 58],
    [340, 120, 95, 46], [400, 155, 72, 34], [250, 175, 170, 45],
    [90, 170, 55, 26], [440, 170, 50, 22],
  ];
  for (const [x, y, rx, ry] of blobs) {
    const grd = g.createRadialGradient(x, y, 0, x, y, rx);
    grd.addColorStop(0, 'rgba(255,255,255,.72)');
    grd.addColorStop(0.55, 'rgba(255,255,255,.35)');
    grd.addColorStop(1, 'rgba(255,255,255,0)');
    g.save(); g.translate(x, y); g.scale(1, ry / rx); g.translate(-x, -y);
    g.fillStyle = grd;
    g.beginPath(); g.arc(x, y, rx, 0, Math.PI * 2); g.fill();
    g.restore();
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.minFilter = THREE.LinearFilter;
  return tex;
}

function glowTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, 'rgba(255,255,255,1)');
  grd.addColorStop(0.08, 'rgba(255,246,222,.95)');
  grd.addColorStop(0.22, 'rgba(255,220,160,.34)');
  grd.addColorStop(0.55, 'rgba(255,190,120,.07)');
  grd.addColorStop(1, 'rgba(255,180,110,0)');
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

export class HainanEnvironment {
  constructor(renderer, scene) {
    this.renderer = renderer;
    this.scene = scene;

    // sky dome ------------------------------------------------------------
    this.uniforms = {
      uTop: { value: new THREE.Color(MODES.day.top) },
      uHorizon: { value: new THREE.Color(MODES.day.horizon) },
      uBottom: { value: new THREE.Color(MODES.day.bottom) },
      uSunColor: { value: new THREE.Color(MODES.day.sun) },
      uSunDir: { value: MODES.day.sunDir.clone() },
      uSunGlow: { value: 1.0 },
    };
    const skyGeo = new THREE.SphereGeometry(260, 48, 32);
    const skyMat = new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      fog: false,
      uniforms: this.uniforms,
      vertexShader: `
        varying vec3 vDir;
        void main() {
          vec4 wp = modelMatrix * vec4(position, 1.0);
          vDir = normalize(wp.xyz);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        varying vec3 vDir;
        uniform vec3 uTop, uHorizon, uBottom, uSunColor, uSunDir;
        uniform float uSunGlow;
        void main() {
          vec3 d = normalize(vDir);
          float h = d.y;
          vec3 col = mix(uHorizon, uTop, pow(clamp(h, 0.0, 1.0), 0.55));
          col = mix(uBottom, col, smoothstep(-0.16, 0.02, h));
          float sd = max(dot(d, normalize(uSunDir)), 0.0);
          col += uSunColor * pow(sd, 420.0) * 1.8 * uSunGlow;
          col += uSunColor * pow(sd, 9.0) * 0.16 * uSunGlow;
          float haze = smoothstep(0.22, -0.04, h) * smoothstep(-0.2, 0.0, h);
          col = mix(col, uHorizon, haze * 0.20);
          gl_FragColor = vec4(col, 1.0);
        }
      `,
    });
    this.sky = new THREE.Mesh(skyGeo, skyMat);
    this.sky.frustumCulled = false;
    this.sky.renderOrder = -10;
    scene.add(this.sky);

    // sun / moon ----------------------------------------------------------
    this.sunSprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTexture(), color: 0xfff1cf, transparent: true, opacity: 0.95,
      depthWrite: false, blending: THREE.AdditiveBlending, fog: false,
    }));
    this.sunSprite.scale.setScalar(38);
    scene.add(this.sunSprite);
    this.moonSprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTexture(), color: 0xcfe4ff, transparent: true, opacity: 0,
      depthWrite: false, blending: THREE.AdditiveBlending, fog: false,
    }));
    this.moonSprite.scale.setScalar(22);
    scene.add(this.moonSprite);

    // stars ---------------------------------------------------------------
    const starCount = 720;
    const pos = new Float32Array(starCount * 3);
    const rng = mulberry32(8);
    for (let i = 0; i < starCount; i++) {
      const a = rng() * Math.PI * 2;
      const y = Math.pow(rng(), 0.6) * 0.92 + 0.04;
      const r = Math.sqrt(1 - y * y);
      pos[i*3] = Math.cos(a) * r * 240;
      pos[i*3+1] = y * 240;
      pos[i*3+2] = Math.sin(a) * r * 240;
    }
    const starGeo = new THREE.BufferGeometry();
    starGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    this.starMat = new THREE.PointsMaterial({
      color: 0xdfe9ff, size: 2.6, sizeAttenuation: true, transparent: true,
      opacity: 0, depthWrite: false, fog: false,
    });
    this.stars = new THREE.Points(starGeo, this.starMat);
    this.stars.renderOrder = -8;
    scene.add(this.stars);

    // clouds --------------------------------------------------------------
    this.clouds = [];
    const cmap = cloudTexture();
    for (let i = 0; i < 8; i++) {
      const mat = new THREE.SpriteMaterial({
        map: cmap, transparent: true, opacity: 0.55, depthWrite: false,
        color: 0xfff5e8, fog: false,
      });
      const sp = new THREE.Sprite(mat);
      const a = (i / 8) * Math.PI * 2 + rng() * 0.5;
      const rad = 180 + rng() * 70;
      sp.position.set(Math.cos(a) * rad, 42 + rng() * 30, Math.sin(a) * rad);
      sp.scale.set(75 + rng() * 55, 22 + rng() * 15, 1);
      sp.userData = { angle: a, radius: rad, speed: 0.002 + rng() * 0.0025, y: sp.position.y };
      this.clouds.push(sp);
      scene.add(sp);
    }

    // distant ridge -------------------------------------------------------
    const ridgeGeo = new THREE.BufferGeometry();
    const ridgeVerts = [];
    const ridgeFaces = [];
    const N = 160;
    for (let i = 0; i <= N; i++) {
      const a = (i / N) * Math.PI * 2;
      const r = 176 + Math.sin(a * 3.2) * 10 + Math.sin(a * 8.7 + 1.2) * 5;
      const h = 4.5 + Math.sin(a * 2.1 + 0.8) * 3.2 + Math.sin(a * 6.3) * 1.5 + Math.max(0, Math.sin(a * 1.3)) * 3.0;
      ridgeVerts.push([Math.cos(a) * r, -1.5, Math.sin(a) * r]);
      ridgeVerts.push([Math.cos(a) * (r + 3), h, Math.sin(a) * (r + 3)]);
    }
    for (let i = 0; i < N; i++) {
      const a = i * 2, b = a + 1, c = a + 2, d = a + 3;
      ridgeFaces.push(a, b, d, a, d, c);
    }
    ridgeGeo.setAttribute('position', new THREE.Float32BufferAttribute(ridgeVerts.flat(), 3));
    ridgeGeo.setIndex(ridgeFaces);
    ridgeGeo.computeVertexNormals();
    this.ridgeMat = new THREE.MeshStandardMaterial({
      color: 0x73866e, roughness: 1, metalness: 0, side: THREE.DoubleSide, fog: true,
    });
    this.ridge = new THREE.Mesh(ridgeGeo, this.ridgeMat);
    scene.add(this.ridge);

    // lights --------------------------------------------------------------
    this.sun = new THREE.DirectionalLight(0xfff2d8, 3.1);
    this.sun.position.copy(MODES.day.sunDir).multiplyScalar(70);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(2048, 2048);
    this.sun.shadow.camera.left = -25;
    this.sun.shadow.camera.right = 25;
    this.sun.shadow.camera.top = 25;
    this.sun.shadow.camera.bottom = -25;
    this.sun.shadow.camera.near = 1;
    this.sun.shadow.camera.far = 150;
    this.sun.shadow.bias = -0.00035;
    this.sun.shadow.normalBias = 0.035;
    this.sun.target.position.set(0, 0, 0);
    scene.add(this.sun, this.sun.target);

    this.hemi = new THREE.HemisphereLight(0xbfd8e9, 0x5b654c, 1.35);
    scene.add(this.hemi);
    this.ambient = new THREE.AmbientLight(0xffffff, 0.18);
    scene.add(this.ambient);
    this.moon = new THREE.DirectionalLight(0x9fc6e8, 0.0);
    this.moon.position.set(-50, 55, -35);
    this.moon.target.position.set(0, 0, 0);
    scene.add(this.moon, this.moon.target);

    this.scene.fog = new THREE.FogExp2(0x91aaa5, 0.0018);
    this.mode = 'day';
    this.target = MODES.day;
    this.mix = 1;
    this.prev = { ...MODES.day,
      top: new THREE.Color(MODES.day.top), horizon: new THREE.Color(MODES.day.horizon),
      bottom: new THREE.Color(MODES.day.bottom), sun: new THREE.Color(MODES.day.sun),
      fog: new THREE.Color(MODES.day.fog),
    };
    // a soft environment for glass and water
    this.buildEnvironment(renderer);
  }

  buildEnvironment(renderer) {
    const c = document.createElement('canvas');
    c.width = 1024; c.height = 512;
    const g = c.getContext('2d');
    const grd = g.createLinearGradient(0, 0, 0, 512);
    grd.addColorStop(0, '#77a6ce');
    grd.addColorStop(0.48, '#d9e5dd');
    grd.addColorStop(0.56, '#8e9c83');
    grd.addColorStop(1, '#4e5b43');
    g.fillStyle = grd; g.fillRect(0, 0, 1024, 512);
    const sun = g.createRadialGradient(710, 150, 0, 710, 150, 80);
    sun.addColorStop(0, 'rgba(255,249,227,1)');
    sun.addColorStop(0.15, 'rgba(255,236,192,.55)');
    sun.addColorStop(1, 'rgba(255,220,160,0)');
    g.fillStyle = sun; g.fillRect(0, 0, 1024, 512);
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    tex.colorSpace = THREE.SRGBColorSpace;
    const pmrem = new THREE.PMREMGenerator(renderer);
    this.envMap = pmrem.fromEquirectangular(tex).texture;
    this.scene.environment = this.envMap;
    this.scene.environmentIntensity = 0.9;
    tex.dispose();
    pmrem.dispose();
  }

  setMode(mode) {
    if (!MODES[mode] || mode === this.mode) return;
    this.prev = {
      top: this.uniforms.uTop.value.clone(),
      horizon: this.uniforms.uHorizon.value.clone(),
      bottom: this.uniforms.uBottom.value.clone(),
      sun: new THREE.Color(this.sun.color),
      fog: this.scene.fog.color.clone(),
      sunIntensity: this.sun.intensity,
      hemi: this.hemi.intensity,
      ambient: this.ambient.intensity,
      exposure: this.renderer.toneMappingExposure,
      env: this.scene.environmentIntensity,
      stars: this.starMat.opacity,
      clouds: this.clouds[0] ? this.clouds[0].material.opacity : 0,
      fogDensity: this.scene.fog.density,
    };
    this.mode = mode;
    this.target = MODES[mode];
    this.mix = 0;
  }

  update(dt, elapsed) {
    if (this.mix < 1) {
      this.mix = Math.min(1, this.mix + dt / 1.8);
      const t = this.mix * this.mix * (3 - 2 * this.mix);
      const T = this.target;
      this.uniforms.uTop.value.lerpColors(this.prev.top, new THREE.Color(T.top), t);
      this.uniforms.uHorizon.value.lerpColors(this.prev.horizon, new THREE.Color(T.horizon), t);
      this.uniforms.uBottom.value.lerpColors(this.prev.bottom, new THREE.Color(T.bottom), t);
      this.uniforms.uSunColor.value.lerpColors(this.prev.sun, new THREE.Color(T.sun), t);
      this.sun.color.lerpColors(this.prev.sun, new THREE.Color(T.sun), t);
      this.sun.intensity = THREE.MathUtils.lerp(this.prev.sunIntensity, T.sunIntensity, t);
      this.hemi.intensity = THREE.MathUtils.lerp(this.prev.hemi, T.hemi, t);
      this.ambient.intensity = THREE.MathUtils.lerp(this.prev.ambient, T.ambient, t);
      this.renderer.toneMappingExposure = THREE.MathUtils.lerp(this.prev.exposure, T.exposure, t);
      this.scene.environmentIntensity = THREE.MathUtils.lerp(this.prev.env, T.env, t);
      this.scene.fog.density = THREE.MathUtils.lerp(this.prev.fogDensity, T.fogDensity, t);
      this.scene.fog.color.lerpColors(this.prev.fog, new THREE.Color(T.fog), t);
      this.starMat.opacity = THREE.MathUtils.lerp(this.prev.stars, T.stars, t);
      for (const c of this.clouds) c.material.opacity = THREE.MathUtils.lerp(this.prev.clouds, T.clouds, t);
    }
    const T = this.target;
    const dir = T.sunDir;
    this.uniforms.uSunDir.value.copy(dir);
    this.uniforms.uSunColor.value.set(T.sun);
    this.sun.position.copy(dir).multiplyScalar(70);
    this.sunSprite.position.copy(dir).multiplyScalar(320);
    this.sunSprite.material.color.set(T.sun);
    this.sunSprite.material.opacity = this.mode === 'night' ? 0.0 : (this.mode === 'dusk' ? 0.9 : (this.mode === 'morning' ? 0.72 : 0.55));
    this.moonSprite.material.opacity = this.mode === 'night' ? 0.55 : 0.0;
    this.moonSprite.position.copy(dir).multiplyScalar(320);
    this.celestialScale(elapsed);
    this.stars.rotation.y += dt * 0.002;
    for (const c of this.clouds) {
      const u = c.userData;
      u.angle += dt * u.speed * 0.08;
      c.position.x = Math.cos(u.angle) * u.radius;
      c.position.z = Math.sin(u.angle) * u.radius;
      c.position.y = u.y + Math.sin(elapsed * 0.08 + u.radius) * 0.6;
    }
    this.ridgeMat.color.set(this.mode === 'night' ? 0x1c2b28 : (this.mode === 'dusk' ? 0x6d6f5e : (this.mode === 'morning' ? 0x7a8a74 : 0x73866e)));
    this.moon.intensity = this.mode === 'night' ? (MODES.night.moon || 0) : 0;
  }

  celestialScale(elapsed) {
    const pulse = 1 + Math.sin(elapsed * 1.3) * 0.012;
    this.sunSprite.scale.setScalar((this.mode === 'dusk' ? 54 : (this.mode === 'morning' ? 50 : 46)) * pulse);
  }
}

function mulberry32(a) {
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

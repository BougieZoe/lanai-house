import * as THREE from 'three';

const GF = 0.35;
const F2 = 3.55;
const EYE = 1.62;
const RADIUS = 0.24;

// Walkable rectangles are in three.js coordinates (x, z), derived from the
// Blender plan. Rooms stop short of wall centrelines; narrow connector rectangles
// bridge the actual door openings.
const GF_ROOMS = [
  { x0: -12.6, x1: 12.6, z0: 4.15, z1: 15.2, room: 'front' },
  { x0: -12.6, x1: 12.6, z0: -14.8, z1: -3.95, room: 'garden' },
  { x0: 5.35, x1: 12.6, z0: -3.95, z1: 4.15, room: 'east' },
  { x0: -12.6, x1: -8.35, z0: -3.95, z1: 4.15, room: 'west' },
  { x0: -3.3, x1: 4.9, z0: -5.25, z1: -3.55, room: 'engawa' },
  { x0: 0.35, x1: 2.9, z0: 4.1, z1: 5.65, room: 'porch' },
  { x0: -2.82, x1: 3.42, z0: -3.68, z1: 3.52, room: 'living' },
  { x0: 0.98, x1: 3.42, z0: 2.45, z1: 4.08, room: 'entry' },
  { x0: -4.8, x1: -3.05, z0: 0.32, z1: 4.05, room: 'tea' },
  { x0: -4.8, x1: -3.78, z0: -1.3, z1: -0.05, room: 'powder' },
  { x0: -4.8, x1: -3.05, z0: -3.48, z1: -1.62, room: 'laundry' },
  { x0: -8.22, x1: -5.2, z0: -0.9, z1: 2.4, room: 'guest' },
  { x0: -6.48, x1: -5.2, z0: -2.62, z1: -1.05, room: 'guestBath' },
  { x0: -8.1, x1: -6.62, z0: -3.2, z1: -1.0, room: 'gardenHall' },
  { x0: 3.52, x1: 4.88, z0: -3.48, z1: -1.95, room: 'wc' },
  { x0: 3.6, x1: 4.88, z0: -1.55, z1: 2.65, room: 'stair' },
  // door / threshold connectors
  { x0: 0.98, x1: 2.22, z0: 3.9, z1: 4.3 },
  { x0: -2.72, x1: 3.18, z0: -3.86, z1: -3.54 },
  { x0: -5.3, x1: -4.7, z0: 0.9, z1: 1.82 },
  { x0: -7.96, x1: -5.84, z0: -4.05, z1: -3.18 },
  { x0: -6.72, x1: -6.32, z0: -2.3, z1: -1.65 },
  { x0: -3.2, x1: -2.7, z0: -3.12, z1: -2.3 },
  { x0: -3.88, x1: -2.72, z0: -1.12, z1: -0.24 },
  { x0: 3.36, x1: 3.62, z0: -2.86, z1: -2.2 },
  { x0: 3.35, x1: 3.7, z0: 2.4, z1: 2.7 },
  { x0: 3.5, x1: 4.9, z0: -2.05, z1: -1.5 },
  { x0: -3.15, x1: -2.75, z0: 1.75, z1: 2.8 },
  { x0: -6.42, x1: -5.25, z0: -1.15, z1: -0.82 },
  { x0: -7.95, x1: -6.55, z0: -1.15, z1: -0.78 },
];

const F2_ROOMS = [
  { x0: -4.8, x1: -1.05, z0: -0.05, z1: 4.05, room: 'master' },
  { x0: -4.8, x1: -1.05, z0: -3.65, z1: -0.15, room: 'kids' },
  { x0: 0.05, x1: 3.4, z0: 0.65, z1: 4.05, room: 'study' },
  { x0: 0.15, x1: 2.32, z0: -3.45, z1: -1.45, room: 'bath' },
  { x0: -0.85, x1: 3.4, z0: -1.3, z1: 0.5, room: 'hall' },
  { x0: 2.5, x1: 3.4, z0: -3.4, z1: -2.2, room: 'storage' },
  { x0: -4.4, x1: -1.6, z0: 4.2, z1: 5.65, room: 'balcony' },
  { x0: -0.6, x1: 3.4, z0: -4.9, z1: -3.85, room: 'rearDeck' },
  // door / threshold connectors
  { x0: -1.2, x1: 0.2, z0: 2.35, z1: 3.3 },
  { x0: -1.2, x1: -0.7, z0: -1.9, z1: -0.9 },
  { x0: 1.6, x1: 2.45, z0: 0.45, z1: 0.75 },
  { x0: 0.0, x1: 0.3, z0: -2.2, z1: -1.2 },
  { x0: 2.25, x1: 2.6, z0: -3.2, z1: -2.5 },
  { x0: 2.5, x1: 3.4, z0: -3.92, z1: -3.35 },
  { x0: -4.4, x1: -1.6, z0: 4.0, z1: 4.32 },
];

const BLOCKERS = [
  { x0: -7.58, x1: -1.62, z0: -10.78, z1: -6.82, floor: 1 },
  { x0: 8.1, x1: 10.1, z0: -0.4, z1: 2.95, floor: 1 },
  { x0: 0.05, x1: 1.02, z0: 0.9, z1: 3.2, floor: 1 },
  { x0: -1.45, x1: 1.05, z0: -1.35, z1: 0.35, floor: 1 },
  { x0: -1.68, x1: -0.08, z0: -2.85, z1: -1.95, floor: 1 },
  { x0: -4.38, x1: -3.35, z0: 1.62, z1: 2.4, floor: 1 },
  { x0: -8.2, x1: -6.15, z0: 0.0, z1: 1.98, floor: 1 },
  { x0: -4.7, x1: -2.45, z0: 0.65, z1: 2.62, floor: 2 },
  { x0: 2.58, x1: 3.27, z0: 2.75, z1: 3.95, floor: 1 },
  { x0: 2.35, x1: 2.92, z0: 2.30, z1: 2.62, floor: 1 },
];

const POINTS = {
  gfStart: { x: 2.05, z: 3.45, yaw: 0 },
  f2Start: { x: -1.7, z: 0.35, yaw: Math.PI },
  stairGf: { x: 4.2, z: 2.35, yaw: Math.PI },
  stairF2: { x: 2.8, z: 0.1, yaw: 0 },
};

function inRect(r, x, z) {
  return x >= r.x0 && x <= r.x1 && z >= r.z0 && z <= r.z1;
}

export function createRoamController({
  camera, controls, domElement, closePanel, closeRoom, closePlan, setRoof, setFloor, setLabels, isLabelsOn,
}) {
  const hud = document.querySelector('#roamHud');
  const roomEl = document.querySelector('#roamRoomName');
  const floorEl = document.querySelector('#roamFloorName');
  const currentEl = document.querySelector('#roamCurrentLabel');
  const promptEl = document.querySelector('#roamPrompt');
  const helpEl = document.querySelector('#roamHelp');
  const lockHint = document.querySelector('#roamLockHint');
  const exitBtn = document.querySelector('#roamExit');
  const floorButtons = [...document.querySelectorAll('.roam-floor-btn')];
  const joystick = document.querySelector('#roamJoystick');
  const joystickKnob = joystick?.querySelector('i');

  let active = false;
  let t = null;
  let floor = 1;
  let yaw = 0;
  let pitch = 0;
  let px = POINTS.gfStart.x;
  let pz = POINTS.gfStart.z;
  let keys = new Set();
  let pointerLocked = false;
  let dragging = false;
  let lastMouse = null;
  let touchLook = null;
  let joy = { x: 0, y: 0 };
  let joyPointer = null;
  let saved = null;
  let lastRoom = '';
  let nearStair = false;

  function floorY() { return floor === 1 ? GF : F2; }

  function walkable(x, z) {
    if (x < -12.55 || x > 12.55 || z < -14.75 || z > 15.15) return false;
    for (const b of BLOCKERS) {
      if (b.floor !== floor) continue;
      if (inRect(b, x, z)) return false;
    }
    const rects = floor === 1 ? GF_ROOMS : F2_ROOMS;
    return rects.some((r) => inRect(r, x, z));
  }

  function roomAt(x, z) {
    const rects = floor === 1 ? GF_ROOMS : F2_ROOMS;
    let found = null;
    for (const r of rects) {
      if (r.room && inRect(r, x, z)) found = r.room;
    }
    return found || (floor === 1 ? 'front' : 'hall');
  }

  function isNearStair() {
    const p = floor === 1 ? POINTS.stairGf : POINTS.stairF2;
    return Math.hypot(px - p.x, pz - p.z) < 1.3;
  }

  function setFloorLevel(next) {
    floor = next;
    if (floor === 2) {
      px = POINTS.f2Start.x; pz = POINTS.f2Start.z; yaw = POINTS.f2Start.yaw;
    } else {
      px = POINTS.stairGf.x; pz = POINTS.stairGf.z; yaw = POINTS.stairGf.yaw;
    }
    pitch = 0;
    floorButtons.forEach((b) => b.classList.toggle('is-active', Number(b.dataset.floor) === floor));
    renderHud();
  }

  function setPosition(p) {
    px = p.x; pz = p.z; yaw = p.yaw;
    floorButtons.forEach((b) => b.classList.toggle('is-active', Number(b.dataset.floor) === floor));
  }

  function renderHud() {
    if (!t) return;
    const room = roomAt(px, pz);
    const name = t.roam.rooms[room] || room;
    if (roomEl) roomEl.textContent = name;
    if (floorEl) floorEl.textContent = `${floor}F · ${floor === 1 ? t.ui.roam.f1 : t.ui.roam.f2}`;
    if (currentEl) currentEl.textContent = t.ui.roam.current;
    floorButtons.forEach((b) => {
      const f = Number(b.dataset.floor);
      b.classList.toggle('is-active', f === floor);
      b.setAttribute('aria-pressed', String(f === floor));
      b.setAttribute('aria-label', f === 1 ? t.ui.roam.f1 : t.ui.roam.f2);
    });
    nearStair = isNearStair();
    if (promptEl) {
      promptEl.textContent = nearStair ? (floor === 1 ? t.ui.roam.up : t.ui.roam.down) : '';
      promptEl.classList.toggle('is-on', nearStair);
    }
    if (helpEl) helpEl.textContent = t.ui.roam.hint;
  }

  function switchFloor(next = floor === 1 ? 2 : 1) {
    setFloorLevel(next);
  }

  function update(dt) {
    if (!active) return;
    const forward = (keys.has('KeyW') || keys.has('ArrowUp') ? 1 : 0) - (keys.has('KeyS') || keys.has('ArrowDown') ? 1 : 0);
    const strafe = (keys.has('KeyD') || keys.has('ArrowRight') ? 1 : 0) - (keys.has('KeyA') || keys.has('ArrowLeft') ? 1 : 0);
    let mx = forward * -Math.sin(yaw) + strafe * Math.cos(yaw);
    let mz = forward * -Math.cos(yaw) - strafe * Math.sin(yaw);
    mx += joy.x;
    mz += joy.y;
    const len = Math.hypot(mx, mz);
    if (len > 1) { mx /= len; mz /= len; }
    const speed = (keys.has('ShiftLeft') || keys.has('ShiftRight') ? 4.4 : 2.15) * dt;
    if (len > 0.001) {
      const nx = px + mx * speed;
      if (walkable(nx, pz)) px = nx;
      const nz = pz + mz * speed;
      if (walkable(px, nz)) pz = nz;
    }
    camera.position.set(px, floorY() + EYE, pz);
    camera.rotation.order = 'YXZ';
    camera.rotation.y = yaw;
    camera.rotation.x = pitch;
    const room = roomAt(px, pz);
    if (room !== lastRoom || isNearStair() !== nearStair) {
      lastRoom = room;
      renderHud();
    }
  }

  function start() {
    if (active) return;
    active = true;
    saved = {
      position: camera.position.clone(),
      quaternion: camera.quaternion.clone(),
      fov: camera.fov,
      near: camera.near,
      target: controls.target.clone(),
      enabled: controls.enabled,
      autoRotate: controls.autoRotate,
      labels: isLabelsOn ? isLabelsOn() : false,
    };
    if (window.innerWidth <= 920) closePanel?.();
    closeRoom?.();
    closePlan?.();
    controls.enabled = false;
    controls.autoRotate = false;
    setRoof?.(true);
    setFloor?.(true);
    setLabels?.(false);
    floor = 1;
    setPosition(POINTS.gfStart);
    pitch = -0.02;
    lastRoom = '';
    camera.near = 0.04;
    camera.fov = 72;
    camera.updateProjectionMatrix();
    camera.position.set(px, floorY() + EYE, pz);
    camera.rotation.order = 'YXZ';
    camera.rotation.set(pitch, yaw, 0);
    document.body.classList.add('roaming');
    document.body.classList.remove('panel-open', 'panel-collapsed');
    hud?.classList.add('is-active');
    hud?.setAttribute('aria-hidden', 'false');
    renderHud();
    if (domElement?.requestPointerLock) {
      const promise = domElement.requestPointerLock();
      if (promise?.catch) promise.catch(() => {});
    }
  }

  function stop() {
    if (!active) return;
    active = false;
    document.body.classList.remove('roaming', 'pointer-locked');
    hud?.classList.remove('is-active');
    hud?.setAttribute('aria-hidden', 'true');
    if (document.pointerLockElement === domElement) document.exitPointerLock?.();
    keys.clear();
    joy = { x: 0, y: 0 };
    joystickKnob?.style.setProperty('transform', 'translate(0px, 0px)');
    if (saved) {
      camera.position.copy(saved.position);
      camera.quaternion.copy(saved.quaternion);
      camera.fov = saved.fov;
      camera.near = saved.near;
      camera.updateProjectionMatrix();
      controls.target.copy(saved.target);
      controls.enabled = saved.enabled;
      controls.autoRotate = saved.autoRotate;
      controls.update();
      if (saved.labels) setLabels?.(true);
    }
    saved = null;
  }

  function onKeyDown(e) {
    if (!active) return;
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code)) e.preventDefault();
    if (e.code === 'Escape') { stop(); return; }
    if (e.code === 'KeyE' && isNearStair()) { switchFloor(); return; }
    if (e.code === 'Digit1') { setFloorLevel(1); return; }
    if (e.code === 'Digit2') { setFloorLevel(2); return; }
    keys.add(e.code);
  }
  function onKeyUp(e) { keys.delete(e.code); }

  function onPointerLockChange() {
    pointerLocked = document.pointerLockElement === domElement;
    document.body.classList.toggle('pointer-locked', pointerLocked);
    if (lockHint) lockHint.style.opacity = pointerLocked ? '0' : '1';
  }

  function onMouseMove(e) {
    if (!active) return;
    if (pointerLocked) {
      yaw -= e.movementX * 0.0022;
      pitch = Math.max(-1.15, Math.min(1.15, pitch - e.movementY * 0.0020));
      return;
    }
    if (dragging && lastMouse) {
      yaw -= (e.clientX - lastMouse.x) * 0.0035;
      pitch = Math.max(-1.15, Math.min(1.15, pitch - (e.clientY - lastMouse.y) * 0.0032));
      lastMouse = { x: e.clientX, y: e.clientY };
    }
  }

  function onPointerDown(e) {
    if (!active) return;
    if (e.pointerType === 'touch') {
      touchLook = { x: e.clientX, y: e.clientY };
      return;
    }
    if (!pointerLocked && domElement?.requestPointerLock) {
      domElement.requestPointerLock();
    }
    dragging = true;
    lastMouse = { x: e.clientX, y: e.clientY };
  }
  function onPointerUp(e) {
    if (e.pointerType === 'touch') touchLook = null;
    dragging = false;
    lastMouse = null;
  }
  function onTouchMove(e) {
    if (!active || e.pointerType !== 'touch' || !touchLook) return;
    yaw -= (e.clientX - touchLook.x) * 0.0045;
    pitch = Math.max(-1.15, Math.min(1.15, pitch - (e.clientY - touchLook.y) * 0.0040));
    touchLook = { x: e.clientX, y: e.clientY };
  }

  function onJoyDown(e) {
    e.stopPropagation();
    joyPointer = e.pointerId;
    joystick.setPointerCapture?.(e.pointerId);
    updateJoy(e);
  }
  function onJoyMove(e) {
    if (joyPointer !== e.pointerId) return;
    e.stopPropagation();
    updateJoy(e);
  }
  function onJoyUp(e) {
    if (joyPointer !== e.pointerId) return;
    joyPointer = null;
    joy = { x: 0, y: 0 };
    joystickKnob?.style.setProperty('transform', 'translate(0px, 0px)');
  }
  function updateJoy(e) {
    const r = joystick.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    let dx = (e.clientX - cx) / (r.width * 0.34);
    let dy = (e.clientY - cy) / (r.height * 0.34);
    const l = Math.hypot(dx, dy);
    if (l > 1) { dx /= l; dy /= l; }
    joy = { x: dx, y: dy };
    joystickKnob?.style.setProperty('transform', `translate(${dx * 27}px, ${dy * 27}px)`);
  }

  function bind() {
    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('pointerlockchange', onPointerLockChange);
    domElement?.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointerup', onPointerUp);
    window.addEventListener('pointermove', onTouchMove);
    joystick?.addEventListener('pointerdown', onJoyDown);
    joystick?.addEventListener('pointermove', onJoyMove);
    joystick?.addEventListener('pointerup', onJoyUp);
    joystick?.addEventListener('pointercancel', onJoyUp);
    exitBtn?.addEventListener('click', stop);
    floorButtons.forEach((b) => b.addEventListener('click', () => setFloorLevel(Number(b.dataset.floor))));
  }
  bind();

  function setLanguage(next) {
    t = next;
    renderHud();
    if (lockHint) lockHint.textContent = t.ui.roam.click;
    if (exitBtn) exitBtn.querySelector('span').textContent = t.ui.roam.exit;
  }

  return {
    start, stop, update, setLanguage, switchFloor,
    get active() { return active; },
    get floor() { return floor; },
    get position() { return { x: px, z: pz, floor, yaw, pitch }; },
    set position(p) { px = p.x; pz = p.z; },
    teleportTo(p) { setPosition(p); renderHud(); },
  };
}

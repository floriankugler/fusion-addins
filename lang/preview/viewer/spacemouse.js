// 3Dconnexion SpaceMouse support through the 3DxWare navigation server.
//
// The driver's "Navigation Library Server" (3DxNLServer) exposes a WAMP v1
// WebSocket on a fixed loopback address. The page does not receive axis
// data: it acts as a property server. The driver reads the camera and the
// model extents, computes a new camera pose and writes it back, which is
// what makes the device feel the same in every application.
//
// Protocol reference: the handshake and property catalogue documented by
// github.com/kchellappan/spacemouse_linux_ws (docs 01-03), observed from
// 3Dconnexion's own client library. Matrices are column-major, translation
// at indices 12, 13, 14, as every client since library version 0.5.

const HOST = '127.51.68.120';
const DISCOVERY = `https://${HOST}:8181/3dconnexion/nlproxy`;
const CLIENT_VERSION = '0.8.1';

const WELCOME = 0, PREFIX = 1, CALL = 2, CALLRESULT = 3, CALLERROR = 4, SUBSCRIBE = 5, EVENT = 8;

export class SpaceMouse {
  /**
   * @param {object} props  property server: an object with get/set handlers,
   *   keyed by navlib property name, e.g. { 'view.affine': { get() {...}, set(v) {...} } }
   * @param {object} opts   { name, onStatus(text, ok), onLog(dir, text) }
   */
  constructor(props, opts = {}) {
    this.props = props;
    this.name = opts.name || document.title || 'web app';
    this.onStatus = opts.onStatus || (() => {});
    this.onLog = opts.onLog || (() => {});
    this.ws = null;
    this.pending = new Map();
    this.controller = null;
    this.connexion = null;
    this.focused = false;
    this.retryMs = 3000;
  }

  async connect() {
    let port;
    try {
      const res = await fetch(DISCOVERY, { headers: { Accept: 'application/json; charset=utf-8' } });
      if (!res.ok) throw new Error(`discovery ${res.status}`);
      const info = await res.json();
      port = info.port || 8181;
      this.onStatus(`driver ${info.version}, connecting…`, false);
    } catch (e) {
      this.onStatus('no 3DxWare navigation server', false);
      return false;
    }
    try {
      this.ws = new WebSocket(`wss://${HOST}:${port}/`, 'wamp');
    } catch (e) {
      this.onStatus('websocket refused: ' + e.message, false);
      return false;
    }
    this.ws.onmessage = (m) => this._onMessage(JSON.parse(m.data));
    this.ws.onclose = () => { this.onStatus('disconnected', false); this.controller = null; };
    this.ws.onerror = () => this.onStatus('connection error', false);
    return true;
  }

  _send(msg) {
    this.onLog('send', msg);
    this.ws.send(JSON.stringify(msg));
  }

  _call(proc, ...args) {
    const id = Math.random().toString(36).slice(2, 12);
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this._send([CALL, id, proc, ...args]);
    });
  }

  async _handshake(sessionId, serverIdent) {
    this.onLog('info', `session ${sessionId}: ${serverIdent}`);
    this._send([PREFIX, '3dx_rpc', `wss://${HOST}/3dconnexion#`]);
    this._send([PREFIX, '3dconnexion', `wss://${HOST}/3dconnexion`]);
    this._send([PREFIX, 'self', location.href]);
    const mouse = await this._call('3dx_rpc:create', '3dconnexion:3dmouse', CLIENT_VERSION);
    this.connexion = mouse.connexion;
    const ctl = await this._call('3dx_rpc:create', '3dconnexion:3dcontroller', this.connexion,
      { version: 0.8, name: this.name, rowMajorOrder: false });
    this.controller = `3dconnexion:3dcontroller/${ctl.instance}`;
    this._send([SUBSCRIBE, this.controller]);
    await this.update({ focus: this.focused });
    this.onStatus('connected', true);
  }

  /** Pushes properties to the driver, e.g. { focus: true } or { 'view.affine': m }. */
  update(values) {
    if (!this.controller) return Promise.resolve();
    return this._call('3dx_rpc:update', this.controller, values);
  }

  setFocus(focused) {
    this.focused = focused;
    this.update({ focus: focused }).catch(() => {});
  }

  _onMessage(msg) {
    this.onLog('recv', msg);
    switch (msg[0]) {
      case WELCOME:
        this._handshake(msg[1], msg[3]).catch((e) => this.onStatus('handshake failed: ' + e, false));
        break;
      case CALLRESULT: {
        const p = this.pending.get(msg[1]);
        if (p) { this.pending.delete(msg[1]); p.resolve(msg[2]); }
        break;
      }
      case CALLERROR: {
        const p = this.pending.get(msg[1]);
        if (p) { this.pending.delete(msg[1]); p.reject(new Error(`${msg[2]}: ${msg[3]}`)); }
        break;
      }
      case EVENT:
        // The driver's requests arrive as CALL messages wrapped in an event.
        if (Array.isArray(msg[2]) && msg[2][0] === CALL) this._serve(msg[2]);
        break;
    }
  }

  _serve(call) {
    const [, id, proc, , prop, value] = call;
    const handler = this.props[prop];
    try {
      if (proc === 'self:read') {
        if (!handler?.get) throw new Error('unknown property');
        const result = handler.get();
        this.onLog('read', `${prop} -> ${JSON.stringify(result)}`);
        this._send([CALLRESULT, id, result]);
      } else if (proc === 'self:update') {
        if (!handler?.set) throw new Error('unknown property');
        this.onLog('write', `${prop} <- ${JSON.stringify(value)}`);
        handler.set(value);
        this._send([CALLRESULT, id, {}]);
      } else {
        throw new Error('unknown procedure ' + proc);
      }
    } catch (e) {
      this._send([CALLERROR, id, `${proc}#generic`, `${prop} ${e.message}`]);
    }
  }
}

/**
 * Wires a three.js camera to the driver. `world` provides the model bounds
 * (THREE.Box3 or null), `applied()` is called after the driver moved the
 * camera. Returns the SpaceMouse instance.
 */
export function attachSpaceMouse(THREE, camera, controls, canvas, world, opts = {}) {
  const identity = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
  // Our world is z-up with y across; the driver's canonical frame is y-up.
  // This matrix maps our axes into that frame: x stays, z becomes up (y),
  // y becomes -z (toward the viewer of a front view).
  const zUpToYUp = [1, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 1];
  const targetDistance = () => camera.position.distanceTo(controls.target);
  const hit = { from: null, direction: null, aperture: 0, selectionOnly: false };
  // The driver's rotation pivot. It is not the orbit target: the driver writes
  // it after a motion (model centre or a hit point), and the orbit controls
  // must keep looking straight ahead or the next mouse drag turns the camera.
  const pivot = { position: null, visible: false };

  const props = {
    'coordinateSystem': { get: () => zUpToYUp },
    'view.affine': {
      get: () => { camera.updateMatrixWorld(true); return camera.matrixWorld.toArray(); },
      set: (m) => {
        // The driver owns the pose while it moves; the orbit controls adopt it
        // when the motion ends (see the page's motion handler).
        new THREE.Matrix4().fromArray(m).decompose(camera.position, camera.quaternion, camera.scale);
        camera.updateMatrixWorld(true);
        opts.applied?.();
      },
    },
    'view.perspective': { get: () => camera.isPerspectiveCamera === true },
    'view.rotatable': { get: () => true },
    'view.fov': {
      get: () => THREE.MathUtils.degToRad(camera.fov),
      set: (v) => { camera.fov = THREE.MathUtils.radToDeg(v); camera.updateProjectionMatrix(); },
    },
    'view.frustum': {
      get: () => {
        const t = camera.near * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
        return [-t * camera.aspect, t * camera.aspect, -t, t, camera.near, camera.far];
      },
    },
    'view.target': {
      get: () => controls.target.toArray(),
      set: (p) => { controls.target.fromArray(p); },
    },
    'view.extents': { get: () => { const b = world(); return b ? [...b.min.toArray(), ...b.max.toArray()] : [-1, -1, -1, 1, 1, 1]; } },
    'model.extents': {
      get: () => { const b = world(); return b ? [...b.min.toArray(), ...b.max.toArray()] : [-1, -1, -1, 1, 1, 1]; },
    },
    'model.unitsToMeters': { get: () => 0.001 },
    'model.floorPlane': { get: () => [0, 0, 1, 0] },
    'view.constructionPlane': { get: () => [0, 0, 1, 0] },
    'pivot.position': {
      get: () => (pivot.position || controls.target.toArray()),
      set: (p) => { pivot.position = p; opts.pivot?.(pivot.position, pivot.visible); },
    },
    'pivot.visible': { set: (v) => { pivot.visible = v; opts.pivot?.(pivot.position, pivot.visible); } },
    // Hit test: the driver sets up a ray, then reads the hit point.
    'hit.lookfrom': { set: (p) => { hit.from = p; } },
    'hit.direction': { set: (d) => { hit.direction = d; } },
    'hit.aperture': { set: (a) => { hit.aperture = a; } },
    'hit.selectionOnly': { set: (v) => { hit.selectionOnly = v; } },
    'hit.lookat': {
      get: () => {
        const point = opts.pick && hit.from && hit.direction ? opts.pick(hit.from, hit.direction) : null;
        if (!point) throw new Error('no hit');
        return point;
      },
    },
    'pivot.user': { get: () => false },
    'views.front': {
      get: () => {
        // front view: looking along +x (toward the rear of the van), z up
        const b = world();
        const c = b ? b.getCenter(new THREE.Vector3()) : new THREE.Vector3();
        const dist = b ? b.getSize(new THREE.Vector3()).length() : 1000;
        const m = new THREE.Matrix4().makeBasis(
          new THREE.Vector3(0, -1, 0), new THREE.Vector3(0, 0, 1), new THREE.Vector3(-1, 0, 0));
        m.setPosition(c.x - dist, c.y, c.z);
        return m.toArray();
      },
    },
    'selection.empty': { get: () => true },
    'motion': { set: (v) => opts.motion?.(v) },
    'transaction': { set: () => {} },
    'settings.changed': { set: () => {} },
    'commands.activeCommand': { set: (id) => opts.command?.(id) },
    'events.keyPress': { set: () => {} },
    'events.keyRelease': { set: () => {} },
  };

  const mouse = new SpaceMouse(props, { name: opts.name, onStatus: opts.onStatus, onLog: opts.onLog });
  // Focus gating: the driver only drives the client that has focus. The
  // page claims it while the pointer is anywhere over it (side pane
  // included) or the window is focused, and releases it when the pointer
  // leaves the page or the window loses focus, so another application
  // under the pointer can take over.
  canvas.setAttribute('tabindex', '0');
  const focus = () => mouse.setFocus(true);
  const blur = () => mouse.setFocus(false);
  const page = document.documentElement;
  page.addEventListener('pointerenter', focus);
  page.addEventListener('pointerdown', focus);
  page.addEventListener('pointerleave', blur);
  window.addEventListener('focus', focus);
  window.addEventListener('blur', blur);
  mouse.connect();
  return mouse;
}

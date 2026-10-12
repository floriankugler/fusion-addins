// The SpaceMouse client (spacemouse.js) without a driver: calls failing
// when the socket closes, unreadable messages, reconnecting, stopping, and
// the front view from the page's front direction.
import { test, mock, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { SpaceMouse, frontView } from '../spacemouse.js';

const settle = () => new Promise((resolve) => setImmediate(resolve));

// A socket that records what is sent; the test opens and closes it.
class FakeSocket {
  static made = [];
  constructor(url, protocol) {
    this.url = url;
    this.protocol = protocol;
    this.sent = [];
    this.closed = false;
    FakeSocket.made.push(this);
  }
  send(text) { this.sent.push(JSON.parse(text)); }
  close() { this.closed = true; }
}

let saved;
let discovery;     // whether the driver's discovery answers
beforeEach(() => {
  saved = { fetch: globalThis.fetch, WebSocket: globalThis.WebSocket, location: globalThis.location };
  FakeSocket.made = [];
  discovery = true;
  globalThis.fetch = async () => {
    if (!discovery) throw new TypeError('fetch failed');
    return { ok: true, json: async () => ({ port: 8181, version: '1.2.3' }) };
  };
  globalThis.WebSocket = FakeSocket;
  Object.defineProperty(globalThis, 'location', { value: { href: 'http://127.0.0.1:8765/' }, configurable: true, writable: true });
});
afterEach(() => {
  globalThis.fetch = saved.fetch;
  globalThis.WebSocket = saved.WebSocket;
  Object.defineProperty(globalThis, 'location', { value: saved.location, configurable: true, writable: true });
  mock.timers.reset();
});

function client() {
  const status = [], log = [];
  const mouse = new SpaceMouse({}, {
    name: 'test', onStatus: (text) => status.push(text), onLog: (kind, msg) => log.push([kind, msg]),
  });
  return { mouse, status, log };
}

test('a closed socket fails the calls waiting for an answer, so the handshake does not hang', async () => {
  const { mouse, status } = client();
  assert.equal(await mouse.connect(), true);
  const ws = FakeSocket.made[0];
  ws.onmessage({ data: JSON.stringify([0, 'session', 1, 'server']) });     // WELCOME starts the handshake
  assert.equal(mouse.pending.size, 1);
  assert.equal(ws.sent.at(-1)[2], '3dx_rpc:create');
  ws.onclose();                                     // never opened: no reconnect
  await settle();
  assert.equal(mouse.pending.size, 0);
  assert.equal(mouse.ws, null);
  assert.equal(status.at(-1), 'handshake failed: connection closed');
  assert.equal(mouse.timer, null);
});

test('the handshake completes on the driver\'s answers', async () => {
  const { mouse, status } = client();
  await mouse.connect();
  const ws = FakeSocket.made[0];
  ws.onopen();
  ws.onmessage({ data: JSON.stringify([0, 'session', 1, 'server']) });
  ws.onmessage({ data: JSON.stringify([3, ws.sent.at(-1)[1], { connexion: 7 }]) });
  await settle();
  const create = ws.sent.at(-1);
  assert.equal(create[3], '3dconnexion:3dcontroller');
  assert.equal(create[4], 7);
  ws.onmessage({ data: JSON.stringify([3, create[1], { instance: 'c1' }]) });
  await settle();
  const focus = ws.sent.at(-1);
  assert.deepEqual(focus.slice(2), ['3dx_rpc:update', '3dconnexion:3dcontroller/c1', { focus: false }]);
  ws.onmessage({ data: JSON.stringify([3, focus[1], {}]) });
  await settle();
  assert.equal(status.at(-1), 'connected');
  assert.equal(mouse.controller, '3dconnexion:3dcontroller/c1');
});

test('an unreadable message is logged and dropped', async () => {
  const { mouse, log } = client();
  await mouse.connect();
  const ws = FakeSocket.made[0];
  assert.doesNotThrow(() => ws.onmessage({ data: '{not json' }));
  assert.doesNotThrow(() => ws.onmessage({ data: '{"an": "object"}' }));
  assert.deepEqual(log.map(([kind]) => kind), ['error', 'error']);
  assert.match(log[0][1], /unreadable message: \{not json/);
});

test('a call without a socket fails at once', async () => {
  const { mouse } = client();
  await assert.rejects(mouse._call('3dx_rpc:update'), /not connected/);
});

test('a connection that was up reconnects, the wait doubling, until stopped', async () => {
  mock.timers.enable({ apis: ['setTimeout'] });
  const { mouse, status } = client();
  await mouse.connect();
  const first = FakeSocket.made[0];
  first.onopen();
  first.onclose();
  assert.equal(status.at(-1), 'disconnected, trying again in 3 s');
  discovery = false;                    // the driver is still away
  mock.timers.tick(3000);
  await settle();
  assert.equal(FakeSocket.made.length, 1);
  assert.equal(status.at(-1), 'disconnected, trying again in 6 s');
  discovery = true;
  mock.timers.tick(6000);
  await settle();
  assert.equal(FakeSocket.made.length, 2);
  const second = FakeSocket.made[1];
  second.onclose();                     // closed before it opened: still trying
  assert.equal(status.at(-1), 'disconnected, trying again in 12 s');
  mock.timers.tick(12000);
  await settle();
  const third = FakeSocket.made[2];
  third.onopen();                       // up again: the wait starts over
  assert.equal(mouse.delay, 3000);
  third.onclose();
  assert.equal(status.at(-1), 'disconnected, trying again in 3 s');
  mouse.stop();
  mock.timers.tick(60000);
  await settle();
  assert.equal(FakeSocket.made.length, 3);
  assert.equal(status.at(-1), 'off');
});

test('without a driver at the start it stays off', async () => {
  mock.timers.enable({ apis: ['setTimeout'] });
  discovery = false;
  const { mouse, status } = client();
  assert.equal(await mouse.connect(), false);
  assert.equal(status.at(-1), 'no 3DxWare navigation server');
  mock.timers.tick(120000);
  await settle();
  assert.equal(FakeSocket.made.length, 0);
});

test('stopped during the handshake, it says off', async () => {
  const { mouse, status } = client();
  await mouse.connect();
  const ws = FakeSocket.made[0];
  ws.onopen();
  ws.onmessage({ data: JSON.stringify([0, 'session', 1, 'server']) });
  mouse.stop();
  ws.onclose();
  await settle();
  assert.equal(mouse.pending.size, 0);
  assert.equal(status.at(-1), 'off');
  assert.equal(mouse.timer, null);
});

test('stop gives the device back and closes the socket', async () => {
  const { mouse } = client();
  await mouse.connect();
  const ws = FakeSocket.made[0];
  ws.onopen();
  mouse.controller = '3dconnexion:3dcontroller/c1';
  mouse.stop();
  assert.deepEqual(ws.sent.at(-1).slice(2), ['3dx_rpc:update', '3dconnexion:3dcontroller/c1', { focus: false }]);
  assert.equal(ws.closed, true);
  ws.onclose();
  await settle();
  assert.equal(mouse.pending.size, 0);
  assert.equal(mouse.timer, null);
  assert.equal(await mouse.connect(), false);
});

// Just enough of three.js for frontView().
class Vector3 {
  constructor(x = 0, y = 0, z = 0) { this.x = x; this.y = y; this.z = z; }
  clone() { return new Vector3(this.x, this.y, this.z); }
  length() { return Math.hypot(this.x, this.y, this.z); }
  normalize() { const l = this.length() || 1; this.x /= l; this.y /= l; this.z /= l; return this; }
  addScaledVector(v, s) { this.x += v.x * s; this.y += v.y * s; this.z += v.z * s; return this; }
  crossVectors(a, b) {
    return this.set(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
  }
  cross(v) { return this.crossVectors(this.clone(), v); }
  set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
  copy(v) { return this.set(v.x, v.y, v.z); }
}
class Matrix4 {
  constructor() { this.columns = [new Vector3(1, 0, 0), new Vector3(0, 1, 0), new Vector3(0, 0, 1), new Vector3()]; }
  makeBasis(x, y, z) { this.columns = [x.clone(), y.clone(), z.clone(), this.columns[3]]; return this; }
  setPosition(v) { this.columns[3] = v.clone(); return this; }
  toArray() { return this.columns.flatMap((c, i) => [c.x, c.y, c.z, i === 3 ? 1 : 0]); }
}
const THREE = { Vector3, Matrix4 };
const round = (m) => m.map((x) => Math.round(x * 1e9) / 1e9 + 0);
const box = {      // centre (100, 0, 50), size (300, 400, 0): diagonal 500
  getCenter: (v) => v.copy(new Vector3(100, 0, 50)),
  getSize: (v) => v.copy(new Vector3(300, 400, 0)),
};

test('the front view looks from the front the page gives', () => {
  // The van's front is -x: the eye on -x, looking along +x, -y to the right (the driver's old fixed view).
  assert.deepEqual(round(frontView(THREE, box, [-1, 0, 0])),
    [0, -1, 0, 0,  0, 0, 1, 0,  -1, 0, 0, 0,  -400, 0, 50, 1]);
  assert.deepEqual(frontView(THREE, box, null), frontView(THREE, box, [-1, 0, 0]));
  // A cabinet's front is -y: the eye on -y, looking along +y, x to the right.
  assert.deepEqual(round(frontView(THREE, box, [0, -1, 0])),
    [1, 0, 0, 0,  0, 0, 1, 0,  0, -1, 0, 0,  100, -500, 50, 1]);
  // Without bounds: a metre away from the origin.
  assert.deepEqual(round(frontView(THREE, null, [0, 2, 0])).slice(12), [0, 1000, 0, 1]);
});

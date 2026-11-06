#!/usr/bin/env node
'use strict';

// Regression tests for the footer motion controller.
// Native Space/Enter activation and visual focus need browser QA; this harness
// verifies the actual extracted footer controller and its asynchronous states.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const site = path.resolve(process.argv[2] || path.join(__dirname, '..'));
const source = fs.readFileSync(path.join(site, 'dist/app.js'), 'utf8');
const start = source.indexOf('/* ── Footer video:');
const end = source.indexOf('/* ── Custom circle cursor:', start);
assert(start >= 0 && end > start, 'The actual footer block must be identifiable');
const footerCode = source.slice(start, end);
const html = fs.readFileSync(path.join(site, 'dist/index.html'), 'utf8');
const css = fs.readFileSync(path.join(site, 'dist/style.css'), 'utf8');

function events(target = {}) {
  const listeners = new Map();
  target.addEventListener = (name, fn) => {
    if (!listeners.has(name)) listeners.set(name, []);
    listeners.get(name).push(fn);
  };
  target.emit = (name, event = {}) => {
    for (const fn of listeners.get(name) || []) fn(event);
  };
  return target;
}

function mediaError(name) {
  return Object.assign(new Error(`Simulated ${name}`), { name });
}

function makeHarness({ reduced = false, hidden = false, missing = null, deferred = false, abortOnPause = false } = {}) {
  const attributes = new Map();
  const control = events({ disabled: false, title: '', setAttribute: (key, value) => attributes.set(key, String(value)) });
  const preference = events({ matches: reduced });
  const pending = [];
  const video = {
    paused: true,
    currentTime: 4.125,
    playCalls: 0,
    pauseCalls: 0,
    nextFailure: null,
    play() {
      this.playCalls++;
      this.paused = false;
      if (this.nextFailure) {
        const error = this.nextFailure;
        this.nextFailure = null;
        return Promise.reject(error);
      }
      if (!deferred) return Promise.resolve();
      return new Promise((resolve, reject) => pending.push({ resolve, reject }));
    },
    pause() {
      this.pauseCalls++;
      this.paused = true;
      if (abortOnPause) {
        for (const request of pending.splice(0)) request.reject(mediaError('AbortError'));
      }
    },
    removeAttribute() {},
  };
  const document = events({
    hidden,
    querySelector(selector) {
      if (selector === '.footer-metal video') return missing === 'video' ? null : video;
      if (selector === 'button.footer-metal') return missing === 'control' ? null : control;
      return null;
    },
  });
  let observer = null;
  const context = {
    document,
    window: { matchMedia: () => preference },
    IntersectionObserver: class {
      constructor(callback) { observer = callback; }
      observe(element) { assert.equal(element, video); }
    },
  };
  vm.runInNewContext(footerCode, context, { filename: 'actual-footer-block.js' });
  return {
    video, control, preference, document, pending,
    label: () => attributes.get('aria-label'),
    setVisible(value) { assert(observer, 'Observer exists'); observer([{ isIntersecting: value }]); },
    setHidden(value) { document.hidden = value; document.emit('visibilitychange'); },
    setReduced(value) { preference.matches = value; preference.emit('change', { matches: value }); },
    click() { if (!control.disabled) control.emit('click'); },
    rejectPending(name) { const request = pending.shift(); assert(request, 'Pending play exists'); request.reject(mediaError(name)); },
    resolvePending() { for (const request of pending.splice(0)) request.resolve(); },
  };
}

const flush = async () => { for (let i = 0; i < 6; i++) await Promise.resolve(); };
const tests = [];
function test(name, fn) { tests.push({ name, fn }); }
function running(h) { assert.equal(h.video.paused, false); assert.equal(h.label(), 'Pause logo animation'); }
function userPaused(h) { assert.equal(h.video.paused, true); assert.equal(h.label(), 'Resume logo animation'); }

test('markup supplies one native button, action label and wrapper focus indicator', () => {
  assert.match(html, /<button\b[^>]*type="button"[^>]*class="footer-metal"[^>]*aria-label="Pause logo animation"/);
  assert.doesNotMatch(html, /class="footer-motion-toggle"/);
  assert.doesNotMatch(html.match(/<button\b[^>]*class="footer-metal"[^>]*>/)[0], /aria-pressed/);
  assert.match(css, /\.footer-mark-wrap:has\(\.footer-metal:focus-visible\)\{outline:3px solid/);
});

test('offscreen starts paused; intersection starts playback', async () => {
  const h = makeHarness();
  assert.equal(h.video.paused, true); assert.equal(h.video.playCalls, 0);
  h.setVisible(true); await flush(); running(h);
  assert.equal(h.control.title, h.label());
});

test('click pauses/resumes without resetting animation phase', async () => {
  const h = makeHarness(); h.setVisible(true); await flush();
  h.click(); userPaused(h);
  h.click(); await flush(); running(h);
  assert.equal(h.video.currentTime, 4.125);
});

test('explicit pause survives viewport and tab changes', async () => {
  const h = makeHarness(); h.setVisible(true); await flush(); h.click();
  const calls = h.video.playCalls;
  h.setVisible(false); h.setVisible(true); h.setHidden(true); h.setHidden(false);
  await flush(); userPaused(h); assert.equal(h.video.playCalls, calls);
});

test('initial reduced motion is static and disables control', () => {
  const h = makeHarness({ reduced: true }); h.setVisible(true); h.click();
  assert.equal(h.video.paused, true); assert.equal(h.video.playCalls, 0);
  assert.equal(h.control.disabled, true); assert.match(h.label(), /reduced motion/);
});

test('runtime reduced motion pauses, then normal motion resumes', async () => {
  const h = makeHarness(); h.setVisible(true); await flush();
  h.setReduced(true); assert.equal(h.video.paused, true); assert.equal(h.control.disabled, true);
  h.setReduced(false); await flush(); running(h); assert.equal(h.control.disabled, false);
});

test('explicit pause survives reduced-motion preference changes', async () => {
  const h = makeHarness(); h.setVisible(true); await flush(); h.click();
  h.setReduced(true); h.setReduced(false); await flush(); userPaused(h);
});

test('hidden page cannot start video and resumes when visible', async () => {
  const h = makeHarness({ hidden: true }); h.setVisible(true);
  assert.equal(h.video.playCalls, 0); assert.equal(h.video.paused, true);
  h.setHidden(false); await flush(); running(h);
});

test('genuine rejected playback exposes Resume and supports retry', async () => {
  const h = makeHarness(); h.video.nextFailure = mediaError('NotAllowedError');
  h.setVisible(true); await flush(); userPaused(h);
  h.click(); await flush(); running(h);
});

test('missing footer video or control is safe', () => {
  for (const missing of ['video', 'control']) assert.doesNotThrow(() => makeHarness({ missing }));
});

test('offscreen cancellation is not mistaken for explicit user pause', async () => {
  const h = makeHarness({ deferred: true, abortOnPause: true });
  h.setVisible(true); h.setVisible(false); await flush();
  h.setVisible(true); await flush(); running(h); assert.equal(h.video.playCalls, 2);
  h.resolvePending(); await flush();
});

test('page-hide cancellation is not mistaken for explicit user pause', async () => {
  const h = makeHarness({ deferred: true, abortOnPause: true });
  h.setVisible(true); h.setHidden(true); await flush();
  h.setHidden(false); await flush(); running(h);
  h.resolvePending(); await flush();
});

test('reduced-motion cancellation resumes when preference is removed', async () => {
  const h = makeHarness({ deferred: true, abortOnPause: true });
  h.setVisible(true); h.setReduced(true); await flush();
  h.setReduced(false); await flush(); running(h);
  h.resolvePending(); await flush();
});

test('stale rejected request cannot pause a newer playback request', async () => {
  const h = makeHarness({ deferred: true });
  h.setVisible(true); h.setVisible(false); h.setVisible(true);
  h.rejectPending('NotAllowedError'); await flush(); running(h);
  h.resolvePending(); await flush();
});

test('quick user pause/resume ignores cancellation from the old play', async () => {
  const h = makeHarness({ deferred: true, abortOnPause: true });
  h.setVisible(true); h.click(); h.click(); await flush(); running(h);
  h.resolvePending(); await flush();
});

(async () => {
  let failed = 0;
  for (const { name, fn } of tests) {
    try { await fn(); console.log(`PASS ${name}`); }
    catch (error) { failed++; console.error(`FAIL ${name}\n  ${error.message}`); }
  }
  console.log(`\n${tests.length - failed}/${tests.length} footer checks passed (${site}).`);
  if (failed) process.exitCode = 1;
})();

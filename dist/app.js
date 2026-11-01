const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const root = document.documentElement;
root.classList.add('js-enabled');
if (!reduceMotion) root.classList.add('js-motion');

/* ── Logo preloader (once per visit) ───────────────────────────────── */
(() => {
  const pre = document.querySelector('.preloader');
  if (!pre || root.classList.contains('skip-preloader') || reduceMotion) { pre && pre.remove(); return; }
  document.body.classList.add('is-preloading');
  const started = performance.now();
  let finished = false;
  const finish = () => {
    if (finished) return;
    finished = true;
    pre.classList.add('is-done');
    document.body.classList.remove('is-preloading');
    try { sessionStorage.setItem('cor-preloaded', '1'); } catch (e) {}
    setTimeout(() => pre.remove(), 900);
  };
  const whenReady = () => setTimeout(finish, Math.max(0, 1900 - (performance.now() - started)));
  if (document.readyState === 'complete') whenReady(); else window.addEventListener('load', whenReady, { once: true });
  setTimeout(finish, 3500); // never hold the page longer than this
})();

/* ── Reveal on scroll ──────────────────────────────────────────────── */
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      if (entry.target.matches('.reveal')) observer.unobserve(entry.target);
    }
  });
}, { threshold: .12 });
document.querySelectorAll('.reveal, .meal-section, .results-section').forEach(el => observer.observe(el));

/* ── Mobile menu ───────────────────────────────────────────────────── */
const menuButton = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  mobileMenu.hidden = true;
  menuButton.setAttribute('aria-label', 'Open navigation menu');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  menuButton.setAttribute('aria-label', open ? 'Open navigation menu' : 'Close navigation menu');
  mobileMenu.hidden = open;
});
mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
document.addEventListener('click', e => { if (!e.target.closest('.nav-bar')) closeMenu(); });

/* ── Focus Lens nav: nearest link sharpens, brackets glide to it ───── */
(() => {
  const bar = document.querySelector('.lens-bar');
  if (!bar) return;
  const links = [...bar.querySelectorAll('.lens-link')];
  const lens = bar.querySelector('.lens');
  let current = null;
  function focusLink(link) {
    if (current === link) return;
    current = link;
    links.forEach(l => l.classList.toggle('is-focus', l === link));
    const b = bar.getBoundingClientRect(), r = link.getBoundingClientRect(), pad = 2;
    lens.style.setProperty('--lx', `${r.left - b.left - pad}px`);
    lens.style.setProperty('--ly', `${r.top - b.top - pad}px`);
    lens.style.setProperty('--lw', `${r.width + pad * 2}px`);
    lens.style.setProperty('--lh', `${r.height + pad * 2}px`);
    bar.classList.add('is-focusing');
  }
  function clear() { current = null; bar.classList.remove('is-focusing'); links.forEach(l => l.classList.remove('is-focus')); }
  bar.addEventListener('pointermove', e => {
    if (e.pointerType === 'touch') return;
    let best = null, bestD = Infinity;
    links.forEach(l => { const r = l.getBoundingClientRect(); const d = Math.abs(e.clientX - (r.left + r.width / 2)); if (d < bestD) { bestD = d; best = l; } });
    if (best) focusLink(best);
  });
  bar.addEventListener('pointerleave', clear);
  links.forEach(l => { l.addEventListener('focus', () => focusLink(l)); l.addEventListener('blur', clear); });
})();

/* ── Food suggestions ──────────────────────────────────────────────── */
const foods = [...document.querySelectorAll('.food-orbit')];
foods.forEach(button => button.addEventListener('click', () => {
  const was = button.getAttribute('aria-pressed') === 'true';
  foods.forEach(o => o.setAttribute('aria-pressed', 'false'));
  button.setAttribute('aria-pressed', String(!was));
}));
const guide = document.querySelector('#food-guide');
document.querySelector('.food-help').addEventListener('click', () => guide.showModal());
document.querySelector('.dialog-close').addEventListener('click', () => guide.close());
guide.addEventListener('click', e => { if (e.target === guide) guide.close(); });

/* ── How it works ──────────────────────────────────────────────────── */
const how = document.querySelector('.how-section');
const howPhone = document.querySelector('.how-phone');
const titles = [...document.querySelectorAll('.how-title')];
const descs = [...document.querySelectorAll('.how-desc')];
const dots = [...document.querySelectorAll('.how-dot')];
let currentStep = -1, manualUntil = 0;
function setStep(i) {
  if (i === currentStep) return;
  currentStep = i;
  [titles, descs, dots].forEach(list => list.forEach((el, n) => el.classList.toggle('active', n === i)));
  [...titles, ...descs].forEach((el, n) => el.setAttribute('aria-hidden', String(n % 3 !== i)));
  dots.forEach((el, n) => el.setAttribute('aria-pressed', String(n === i)));
  howPhone.classList.toggle('is-scanned', i > 0);
  howPhone.classList.toggle('is-action', i === 2);
}
dots.forEach((d, i) => d.addEventListener('click', () => { manualUntil = performance.now() + 12000; setStep(i); }));
setStep(0);
// On phones the section isn't sticky, so cycle the steps while it's on screen.
let howTimer = null;
new IntersectionObserver(([e]) => {
  clearInterval(howTimer);
  if (e.isIntersecting && innerWidth < 810 && !reduceMotion) {
    howTimer = setInterval(() => { if (performance.now() > manualUntil) setStep((currentStep + 1) % 3); }, 3200);
  }
}, { threshold: .4 }).observe(how);

/* ── Scroll-driven scenes ──────────────────────────────────────────── */
const hero = document.querySelector('.hero');
const heroScene = document.querySelector('.hero-scene');
const heroPhone = document.querySelector('.hero-phone');
const burger = document.querySelector('.burger-stage');
const foodStage = document.querySelector('.food-stage');
let pending = false;
function onScroll() {
  if (pending) return;
  pending = true;
  requestAnimationFrame(() => {
    pending = false;
    const h = heroScene.getBoundingClientRect();
    hero.classList.toggle('hero-revealed', h.top < -80 || reduceMotion);
    if (h.top < -120) heroPhone.classList.add('is-scanned');
    else if (h.top > 60) heroPhone.classList.remove('is-scanned');
    if (reduceMotion) return;
    const b = burger.getBoundingClientRect();
    const p = Math.max(0, Math.min(1, (innerHeight * .9 - b.top) / (innerHeight * .8)));
    const eased = 1 - Math.pow(1 - p, 3);
    burger.style.setProperty('--spread', `${eased * (innerWidth < 810 ? 70 : 150)}px`);
    const f = foodStage.getBoundingClientRect();
    const fp = (innerHeight / 2 - (f.top + f.height / 2)) / innerHeight; // about -1..1 around centre
    foods.forEach((el, i) => el.style.setProperty('--py', `${fp * (i % 2 ? -70 : 50) * (1 + (i % 3) * .3)}px`));
    if (innerWidth >= 810 && performance.now() > manualUntil) {
      const r = how.getBoundingClientRect();
      const prog = Math.max(0, Math.min(.999, -r.top / Math.max(1, r.height - innerHeight)));
      setStep(Math.floor(prog * 3));
    }
  });
}
addEventListener('scroll', onScroll, { passive: true });
addEventListener('resize', onScroll, { passive: true });
onScroll();

/* ── AI meal demo ──────────────────────────────────────────────────── */
let mealTimers = [];
const status = document.querySelector('.meal-status');
const statusText = status.querySelector('span');
function replayMeal() {
  mealTimers.forEach(clearTimeout);
  mealTimers = [];
  document.querySelectorAll('.plate-layer').forEach((el, i) => el.classList.toggle('active', i === 0));
  document.querySelectorAll('.ingredient').forEach(el => el.classList.remove('active'));
  document.querySelector('.meal-total').classList.remove('active');
  status.classList.remove('done');
  statusText.textContent = 'Estimating nutrition';
  ['Omelet', 'Cheese', 'Chicken'].forEach((name, i) => {
    mealTimers.push(setTimeout(() => {
      document.querySelectorAll('.plate-layer').forEach((el, n) => el.classList.toggle('active', n === i + 1));
      document.querySelector(`.ingredient-${i}`).classList.add('active');
      statusText.textContent = `Reading ${name}`;
    }, reduceMotion ? 0 : 1300 + i * 1400));
  });
  mealTimers.push(setTimeout(() => {
    status.classList.add('done');
    statusText.textContent = 'Done ✓';
    document.querySelector('.meal-total').classList.add('active');
  }, reduceMotion ? 0 : 5600));
}
let mealSeen = false;
new IntersectionObserver(entries => {
  const vis = entries.some(e => e.isIntersecting);
  if (vis && !mealSeen) replayMeal();
  mealSeen = vis;
}, { threshold: .35 }).observe(document.querySelector('.meal-demo'));
document.querySelector('.prompt-demo').addEventListener('click', replayMeal);

/* ── FAQ: Smooth FAQ Flow (one open at a time) ─────────────────────── */
const flowItems = [...document.querySelectorAll('.flow-item')];
flowItems.forEach(item => item.querySelector('.flow-a').setAttribute('aria-hidden', String(!item.classList.contains('open'))));
flowItems.forEach(item => item.querySelector('.flow-q').addEventListener('click', () => {
  const opening = !item.classList.contains('open');
  flowItems.forEach(o => { o.classList.remove('open'); o.querySelector('.flow-q').setAttribute('aria-expanded', 'false'); o.querySelector('.flow-a').setAttribute('aria-hidden', 'true'); });
  if (opening) { item.classList.add('open'); item.querySelector('.flow-q').setAttribute('aria-expanded', 'true'); item.querySelector('.flow-a').setAttribute('aria-hidden', 'false'); }
}));

/* Real app screenshots: full-size viewing with native dialog focus handling. */
const screenViewer = document.querySelector('#screen-viewer');
document.querySelectorAll('.screen-shot').forEach(button => button.addEventListener('click', () => {
  const image = screenViewer.querySelector('img');
  image.src = button.dataset.screen;
  image.alt = `${button.dataset.title} — real COR screen with sample data`;
  screenViewer.querySelector('h2').textContent = button.dataset.title;
  screenViewer.showModal();
}));
screenViewer.querySelector('.screen-close').addEventListener('click', () => screenViewer.close());
screenViewer.addEventListener('click', e => { if (e.target === screenViewer) screenViewer.close(); });

/* ── Footer video: only play while visible ─────────────────────────── */
const metal = document.querySelector('.footer-metal video');
if (metal) {
  if (reduceMotion) { metal.removeAttribute('autoplay'); metal.pause(); }
  else new IntersectionObserver(([e]) => { e.isIntersecting ? metal.play().catch(() => {}) : metal.pause(); }).observe(metal);
}

/* ── Custom circle cursor: desktop fine pointers only ──────────────── */
(() => {
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  const cursor = document.querySelector('.custom-cursor');
  if (!cursor || !finePointer.matches) return;

  const ring = cursor.querySelector('.cursor-ring');
  const dot = cursor.querySelector('.cursor-dot');
  let targetX = -100, targetY = -100, ringX = targetX, ringY = targetY;
  let frame = 0;
  const moveRing = () => {
    frame = 0;
    ringX += (targetX - ringX) * 0.22;
    ringY += (targetY - ringY) * 0.22;
    ring.style.transform = `translate3d(${ringX}px,${ringY}px,0) translate(-50%,-50%)`;
    if (Math.abs(targetX - ringX) > 0.15 || Math.abs(targetY - ringY) > 0.15) frame = requestAnimationFrame(moveRing);
    else { ringX = targetX; ringY = targetY; }
  };
  const isEditable = target => target instanceof Element && target.closest('input, textarea, select, [contenteditable="true"]');
  const isInteractive = target => target instanceof Element && target.closest('a, button, [role="button"], summary, label');

  document.documentElement.classList.add('has-custom-cursor');
  document.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse') return;
    targetX = event.clientX;
    targetY = event.clientY;
    dot.style.transform = `translate3d(${targetX}px,${targetY}px,0) translate(-50%,-50%)`;
    const editing = Boolean(isEditable(event.target));
    cursor.classList.toggle('is-editing', editing);
    document.documentElement.classList.toggle('cursor-native', editing);
    cursor.classList.toggle('is-hovering', Boolean(isInteractive(event.target)));
    cursor.classList.add('is-visible');
    if (reduceMotion) {
      ringX = targetX; ringY = targetY;
      ring.style.transform = `translate3d(${ringX}px,${ringY}px,0) translate(-50%,-50%)`;
    } else if (!frame) frame = requestAnimationFrame(moveRing);
  }, { passive: true });
  document.addEventListener('pointerdown', event => { if (event.pointerType === 'mouse') cursor.classList.add('is-pressed'); });
  window.addEventListener('pointerup', () => cursor.classList.remove('is-pressed'));
  window.addEventListener('blur', () => cursor.classList.remove('is-visible', 'is-hovering', 'is-pressed'));
  document.addEventListener('pointerout', event => {
    if (event.pointerType === 'mouse' && !event.relatedTarget) cursor.classList.remove('is-visible', 'is-hovering', 'is-pressed');
  });
  finePointer.addEventListener?.('change', event => {
    if (!event.matches) document.documentElement.classList.remove('has-custom-cursor');
  });
})();

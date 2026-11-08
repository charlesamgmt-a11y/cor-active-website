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
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
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
  image.alt = `${button.dataset.title} — CŌR app screen with illustrative records`;
  screenViewer.querySelector('h2').textContent = button.dataset.title;
  screenViewer.showModal();
}));
screenViewer.querySelector('.screen-close').addEventListener('click', () => screenViewer.close());
screenViewer.addEventListener('click', e => { if (e.target === screenViewer) screenViewer.close(); });

/* Feature showcase: tabs keep the product story orderly and one screen in focus. */
const showcaseTabs = [...document.querySelectorAll('.showcase-tab')];
const showcaseCapture = document.querySelector('.showcase-capture');
const showcaseCount = document.querySelector('.capture-count');
const showcaseStage = document.querySelector('.showcase-stage');
const showcasePanel = document.querySelector('#showcase-panel');
function selectShowcase(index, moveFocus = false) {
  if (!showcaseTabs.length || !showcaseCapture) return;
  const safeIndex = (index + showcaseTabs.length) % showcaseTabs.length;
  showcaseTabs.forEach((tab, i) => {
    const active = i === safeIndex;
    tab.classList.toggle('active', active);
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
  });
  const current = showcaseTabs[safeIndex];
  if (showcasePanel) showcasePanel.setAttribute('aria-labelledby', current.id);
  if (showcaseStage) showcaseStage.style.setProperty('--showcase-background', current.dataset.background ? `url("${current.dataset.background}")` : 'none');
  showcaseCapture.dataset.screen = current.dataset.screen;
  showcaseCapture.dataset.title = current.dataset.title;
  showcaseCapture.setAttribute('aria-label', `Enlarge ${current.dataset.title} app screen`);
  const image = showcaseCapture.querySelector('img');
  image.src = current.dataset.screen;
  image.alt = `${current.dataset.title} — CŌR app screen with illustrative records`;
  if (showcaseCount) showcaseCount.textContent = `${String(safeIndex + 1).padStart(2, '0')} — ${String(showcaseTabs.length).padStart(2, '0')}`;
  if (moveFocus) current.focus();
}
showcaseTabs.forEach((tab, index) => {
  tab.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse' || event.pointerType === 'pen') selectShowcase(index);
  });
  tab.addEventListener('focus', () => selectShowcase(index));
  tab.addEventListener('click', () => selectShowcase(index));
  tab.addEventListener('keydown', event => {
    const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1, Home: -index, End: showcaseTabs.length - 1 - index };
    if (!(event.key in keys)) return;
    event.preventDefault();
    selectShowcase(index + keys[event.key], true);
  });
});

/* ── Footer video: only play while visible ─────────────────────────── */
const metal = document.querySelector('.footer-metal video');
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (metal) {
  let footerVisible = false;
  const syncFooterMotion = () => {
    if (motionPreference.matches) {
      metal.removeAttribute('autoplay');
      metal.pause();
      return;
    }
    if (footerVisible) metal.play().catch(() => {});
    else metal.pause();
  };
  new IntersectionObserver(([entry]) => {
    footerVisible = entry.isIntersecting;
    syncFooterMotion();
  }).observe(metal);
  motionPreference.addEventListener('change', syncFooterMotion);
  syncFooterMotion();
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

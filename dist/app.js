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
// Mobile steps stay under the reader’s control; desktop retains scroll progression.

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

/* ── FAQ: Smooth FAQ Flow (one open at a time) ─────────────────────── */
/* Real app screenshots: full-size viewing with native dialog focus handling. */
const screenViewer = document.querySelector('#screen-viewer');
document.querySelectorAll('.screen-shot, .strength-screen-button').forEach(button => button.addEventListener('click', () => {
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
let selectedShowcase = -1;
let showcaseManualY = null;
function selectShowcase(index, moveFocus = false, fromScroll = false) {
  if (!showcaseTabs.length || !showcaseCapture) return;
  const safeIndex = (index + showcaseTabs.length) % showcaseTabs.length;
  if (!fromScroll) showcaseManualY = scrollY;
  const changed = selectedShowcase !== safeIndex;
  selectedShowcase = safeIndex;
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
  if (changed && !matchMedia('(prefers-reduced-motion: reduce)').matches) image.animate([{opacity:.15},{opacity:1}], {duration:320,easing:'ease-out'});
  image.alt = `${current.dataset.title} — CŌR app screen with illustrative records`;
  if (showcaseCount) showcaseCount.textContent = `${String(safeIndex + 1).padStart(2, '0')} — ${String(showcaseTabs.length).padStart(2, '0')}`;
  if (moveFocus) current.focus();
}
showcaseTabs.forEach((tab, index) => {
  tab.addEventListener('focus', () => selectShowcase(index));
  tab.addEventListener('click', () => selectShowcase(index));
  tab.addEventListener('keydown', event => {
    const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1, Home: -index, End: showcaseTabs.length - 1 - index };
    if (!(event.key in keys)) return;
    event.preventDefault();
    selectShowcase(index + keys[event.key], true);
  });
});

/* Scroll selects only on movement, so manual/keyboard exploration stays usable. */
(() => {
 const section=document.querySelector('.features-section'),layout=document.querySelector('.showcase-layout');
 if(!section||!layout||!showcaseTabs.length)return;
 const preference=matchMedia('(prefers-reduced-motion: reduce)');let queued=false;
 showcaseTabs.forEach(tab=>{const image=new Image();image.src=tab.dataset.screen;});
 function update(){
  queued=false;
  if(preference.matches||innerHeight<=620)return;
  if(showcaseManualY!==null&&Math.abs(scrollY-showcaseManualY)<120)return;
  const rect=section.getBoundingClientRect();
  if(rect.top>innerHeight||rect.bottom<0)return;
  const pinTop=parseFloat(getComputedStyle(layout).top)||100;
  const marker=section.querySelector('.showcase-scroll-start');
  const start=scrollY+marker.getBoundingClientRect().top+(parseFloat(getComputedStyle(layout).marginTop)||0)-pinTop;
  const end=section.offsetTop+section.offsetHeight-layout.offsetHeight-pinTop;
  const progress=Math.max(0,Math.min(1,(scrollY-start)/Math.max(1,end-start)));
  const next=progress<.5?0:1;
  if(next!==selectedShowcase)selectShowcase(next,false,true);
 }
 function request(){if(!queued){queued=true;requestAnimationFrame(update);}}
 addEventListener('scroll',request,{passive:true});addEventListener('resize',request,{passive:true});preference.addEventListener('change',request);request();
})();

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


/* Assemble physical plate layers; match the burger's ease-out scroll pacing. */
(() => {
 const section=document.querySelector('.barbell-section'),stage=document.querySelector('.barbell-stage');
 if(!section||!stage)return;
 const preference=matchMedia('(prefers-reduced-motion: reduce)');let queued=false;
 function update(){queued=false;const r=section.getBoundingClientRect();const p=preference.matches?1:Math.max(0,Math.min(1,(innerHeight*.35-r.top)/(innerHeight*.75)));stage.style.setProperty('--assembly',String(1-Math.pow(1-p,3)));}
 function request(){if(!queued){queued=true;requestAnimationFrame(update);}}
 addEventListener('scroll',request,{passive:true});addEventListener('resize',request,{passive:true});preference.addEventListener('change',request);update();
})();

/* COR preview: deliberate, accessible interactions. Native captures remain unchanged. */
const menuButton = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');
function closeMenu() {
  if (!menuButton || !mobileMenu) return;
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation menu');
  mobileMenu.hidden = true;
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  menuButton.setAttribute('aria-label', open ? 'Open navigation menu' : 'Close navigation menu');
  mobileMenu.hidden = open;
});
mobileMenu?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
    closeMenu(); menuButton.focus();
  }
});
document.addEventListener('click', e => { if (!e.target.closest('.nav-bar')) closeMenu(); });
window.matchMedia('(min-width: 851px)').addEventListener('change', closeMenu);

const viewer = document.querySelector('#screen-viewer');
let screenOpener;
document.querySelectorAll('.screen-shot').forEach(button => button.addEventListener('click', () => {
  screenOpener = button;
  const image = viewer.querySelector('img');
  image.src = button.dataset.screen;
  image.alt = `${button.dataset.title} — COR app screen with illustrative records`;
  viewer.querySelector('h2').textContent = button.dataset.title;
  viewer.showModal();
}));
viewer?.querySelector('.screen-close').addEventListener('click', () => viewer.close());
viewer?.addEventListener('click', e => { if (e.target === viewer) viewer.close(); });
viewer?.addEventListener('close', () => screenOpener?.focus());

const tabs = [...document.querySelectorAll('.showcase-tab')];
const panel = document.querySelector('#showcase-panel');
function selectScreen(index, focus = false) {
  const activeIndex = (index + tabs.length) % tabs.length;
  const current = tabs[activeIndex];
  if (!current || !panel) return;
  tabs.forEach((tab, i) => {
    tab.classList.toggle('active', i === activeIndex);
    tab.setAttribute('aria-selected', String(i === activeIndex));
    tab.tabIndex = i === activeIndex ? 0 : -1;
  });
  panel.setAttribute('aria-labelledby', current.id);
  const button = panel.querySelector('.screen-shot');
  button.dataset.screen = current.dataset.screen;
  button.dataset.title = current.dataset.title;
  button.setAttribute('aria-label', `Enlarge ${current.dataset.title} app screen`);
  const image = button.querySelector('img');
  image.src = current.dataset.screen;
  image.alt = `${current.dataset.title} — COR app screen with illustrative records`;
  panel.querySelector('.capture-count').textContent = `${String(activeIndex + 1).padStart(2, '0')} / ${String(tabs.length).padStart(2, '0')}`;
  panel.querySelector('.capture-title').textContent = current.dataset.title;
  if (focus) current.focus();
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectScreen(index));
  tab.addEventListener('keydown', event => {
    const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1, Home: -index, End: tabs.length - 1 - index };
    if (!(event.key in keys)) return;
    event.preventDefault(); selectScreen(index + keys[event.key], true);
  });
});

/* Footer motion is optional and only runs while visible. */
const metal = document.querySelector('.footer-metal video');
const metalToggle = document.querySelector('.footer-motion-toggle');
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (metal && metalToggle) {
  let userPaused = false, footerVisible = false;
  function syncFooterMotion() {
    const paused = userPaused || motionPreference.matches;
    metalToggle.disabled = motionPreference.matches;
    metalToggle.textContent = motionPreference.matches ? 'Animation paused (reduced motion)' : userPaused ? 'Resume animation' : 'Pause animation';
    metalToggle.setAttribute('aria-pressed', String(paused));
    if (footerVisible && !paused) metal.play().catch(() => {}); else metal.pause();
  }
  metalToggle.addEventListener('click', () => { userPaused = !userPaused; syncFooterMotion(); });
  new IntersectionObserver(([entry]) => { footerVisible = entry.isIntersecting; syncFooterMotion(); }).observe(metal);
  motionPreference.addEventListener('change', syncFooterMotion);
  syncFooterMotion();
}

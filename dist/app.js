'use strict';
const menuToggle = document.querySelector('.menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
function closeMenu() {
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open navigation menu');
  mobileMenu.hidden = true;
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
  mobileMenu.hidden = !open;
});
mobileMenu.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
document.addEventListener('click', e => { if (!e.target.closest('.nav-bar')) closeMenu(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });

const viewer = document.getElementById('screen-viewer');
const viewerImage = document.getElementById('viewer-image');
document.addEventListener('click', e => {
  const shot = e.target.closest('button[data-shot]');
  if (!shot) return;
  viewerImage.src = `/assets/product/${shot.dataset.shot}.png`;
  viewerImage.alt = `${shot.dataset.title} — actual COR app screen with sample data`;
  document.getElementById('viewer-title').textContent = shot.dataset.title;
  viewer.showModal();
});
viewer.querySelector('.viewer-close').addEventListener('click', () => viewer.close());
viewer.addEventListener('click', e => {
  const bounds = viewer.getBoundingClientRect();
  if (e.target === viewer && (e.clientX < bounds.left || e.clientX > bounds.right || e.clientY < bounds.top || e.clientY > bounds.bottom)) viewer.close();
});

const tabs = [...document.querySelectorAll('[role="tab"][data-screen]')];
const panel = document.getElementById('nutrition-screen');
function selectScreen(tab) {
  tabs.forEach(item => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
  });
  const device = panel.querySelector('button[data-shot]');
  device.dataset.shot = tab.dataset.screen;
  device.dataset.title = tab.dataset.label;
  device.setAttribute('aria-label', `Enlarge ${tab.dataset.label}`);
  const img = device.querySelector('img');
  img.src = `/assets/product/${tab.dataset.screen}.png`;
  img.alt = `${tab.dataset.label} — actual COR app screen with sample data`;
  panel.setAttribute('aria-label', tab.dataset.heading);
  panel.querySelector('figcaption').firstChild.textContent = `${tab.dataset.heading} `;
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectScreen(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index + tabs.length - 1) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); tabs[next].focus(); selectScreen(tabs[next]); }
  });
});
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.documentElement.classList.add('js-motion');
  const revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('in-view'); revealObserver.unobserve(entry.target); }
  }), { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(element => revealObserver.observe(element));
}

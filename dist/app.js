const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduceMotion) document.documentElement.classList.add('js-motion');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      if (entry.target.matches('.reveal')) observer.unobserve(entry.target);
    }
  });
}, { threshold: .12 });
document.querySelectorAll('.reveal, .meal-section').forEach(el => observer.observe(el));

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
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
document.addEventListener('click', event => { if (!event.target.closest('.nav-bar')) closeMenu(); });

document.querySelectorAll('.food-orbit').forEach(button => {
  button.addEventListener('click', () => {
    const wasPressed = button.getAttribute('aria-pressed') === 'true';
    document.querySelectorAll('.food-orbit').forEach(other => other.setAttribute('aria-pressed', 'false'));
    button.setAttribute('aria-pressed', String(!wasPressed));
  });
});
const guide = document.querySelector('#food-guide');
document.querySelector('.food-help').addEventListener('click', () => guide.showModal());
document.querySelector('.dialog-close').addEventListener('click', () => guide.close());
guide.addEventListener('click', event => {
  if (event.target === guide) {
    const rect = guide.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) guide.close();
  }
});

document.querySelectorAll('.shutter').forEach(button => button.addEventListener('click', () => {
  button.closest('.phone').classList.toggle('is-scanned');
}));
document.querySelectorAll('.phone-log').forEach(button => button.addEventListener('click', () => {
  button.textContent = 'Added to demo log ✓';
  button.disabled = true;
}));

const hero = document.querySelector('.hero');
const heroScene = document.querySelector('.hero-scene');
const heroPhone = document.querySelector('.hero-phone');
const burger = document.querySelector('.burger-stage');
const how = document.querySelector('.how-section');
const howPhone = document.querySelector('.how-phone');
const steps = [...document.querySelectorAll('.step')];
let currentStep = -1;
let manualStepUntil = 0;
function setStep(index) {
  if (index === currentStep) return;
  currentStep = index;
  steps.forEach((button, i) => {
    button.classList.toggle('active', i === index);
    button.setAttribute('aria-pressed', String(i === index));
  });
  document.querySelectorAll('.step-description').forEach((el, i) => el.classList.toggle('active', i === index));
  document.querySelectorAll('.step-progress i').forEach((el, i) => el.classList.toggle('active', i === index));
  howPhone.classList.toggle('is-scanned', index > 0);
  howPhone.classList.toggle('is-action', index === 2);
}
steps.forEach((button, index) => button.addEventListener('click', () => {
  manualStepUntil = performance.now() + 15000;
  setStep(index);
}));
setStep(0);
let framePending = false;
function onScroll() {
  if (framePending) return;
  framePending = true;
  requestAnimationFrame(() => {
    framePending = false;
    const h = heroScene.getBoundingClientRect();
    const revealed = h.top < -80 || reduceMotion;
    hero.classList.toggle('hero-revealed', revealed);
    if (h.top < -160 && !reduceMotion) heroPhone.classList.add('is-scanned');
    else if (h.top > 100 && !reduceMotion) heroPhone.classList.remove('is-scanned');
    if (!reduceMotion) {
      const b = burger.getBoundingClientRect();
      const progress = Math.max(0, Math.min(1, (innerHeight - b.top) / (innerHeight * .85)));
      burger.style.setProperty('--spread', `${progress * (innerWidth < 810 ? 60 : 100)}px`);
    }
    if (innerWidth >= 810 && !reduceMotion && performance.now() > manualStepUntil) {
      const rect = how.getBoundingClientRect();
      const progress = Math.max(0, Math.min(.999, -rect.top / Math.max(1, rect.height - innerHeight)));
      setStep(Math.floor(progress * 3));
    }
  });
}
window.addEventListener('scroll', onScroll, {passive:true});
window.addEventListener('resize', onScroll, {passive:true});
onScroll();

let mealTimers = [];
function replayMeal() {
  mealTimers.forEach(clearTimeout);
  mealTimers = [];
  document.querySelectorAll('.plate-layer').forEach((el,i) => el.classList.toggle('active', i === 0));
  document.querySelectorAll('.ingredient').forEach(el => el.classList.remove('active'));
  document.querySelector('.meal-total').classList.remove('active');
  const status = document.querySelector('.meal-status');
  status.textContent = 'Working it out…';
  ['Omelet', 'Cheese', 'Chicken'].forEach((name,index) => {
    mealTimers.push(setTimeout(() => {
      document.querySelectorAll('.plate-layer').forEach((el,i) => el.classList.toggle('active', i === index + 1));
      document.querySelector(`.ingredient-${index}`).classList.add('active');
      status.textContent = `Adding ${name.toLowerCase()}`;
    }, reduceMotion ? 0 : 1000 + index * 1400));
  });
  mealTimers.push(setTimeout(() => {
    status.textContent = 'Done ✓';
    document.querySelector('.meal-total').classList.add('active');
  }, reduceMotion ? 0 : 5400));
}
const mealObserver = new IntersectionObserver(entries => {
  if (entries.some(entry => entry.isIntersecting)) {
    replayMeal();
    mealObserver.disconnect();
  }
}, {threshold:.25});
mealObserver.observe(document.querySelector('.meal-demo'));
document.querySelector('.prompt-demo').addEventListener('click', replayMeal);

document.querySelectorAll('.faq-item').forEach(details => details.addEventListener('toggle', () => {
  if (details.open) document.querySelectorAll('.faq-item').forEach(other => { if (other !== details) other.open = false; });
}));

"""Build the COR Active homepage.

Layout, typography and motion follow the owner's Framer project
(Calories copy, published at goodness-zebra-710061.framer.app).
Copy comes from reference-data.json (text from that Framer project).

Run:      python3 build.py
Preview:  python3 -m http.server 4317 --bind 127.0.0.1 --directory dist
"""
from pathlib import Path
import json
from html import escape

# ── Links: paste the real ones here before launch, then rebuild ─────────
APP_STORE_URL = ''          # e.g. https://apps.apple.com/app/id0000000000
PRIVACY_URL = ''            # public privacy policy page
TERMS_URL = ''              # public terms page
SUPPORT_EMAIL = ''          # e.g. support@coractive.app
PRO_PRICE = ''              # e.g. '9.99'  (leave empty to show "In app")
# ────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'reference-data.json').read_text())
BRAND = 'COR'
DOWNLOAD = APP_STORE_URL or '#download'
ARROW = '<span aria-hidden="true">›</span>'
APPSTORE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#1d8cf8"/><path d="M8.1 16.6h7.8M9.6 16.6l3.9-8.9M14.4 16.6l-1.6-3.6M10.3 7.7l.8 1.8" stroke="#fff" stroke-width="1.6" stroke-linecap="round" fill="none"/></svg>'
NAV = [('Features', '#features'), ('How it works', '#how-it-works'), ('Pricing', '#pricing'), ('FAQ', '#faq'), ('Legal', '#legal')]


def img(name, alt='', cls='', eager=False):
    return (f'<img src="/assets/{escape(name)}" alt="{escape(alt)}" class="{cls}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')


def icon(name, cls='deco'):
    return img(data['icons'][name], '', cls)


def button(label='Download for iPhone', href=DOWNLOAD, cls='solid-button'):
    return f'<a class="{cls}" href="{href}">{escape(label)}{ARROW}</a>'


def section_header(index):
    t = data['sections'][index]['texts']
    return (f'<header class="section-header reveal"><h2>{escape(t[0])}</h2>'
            f'<p>{escape(t[1].replace("CŌR", BRAND))}</p></header>')


# ── Phone (shared by hero + how-it-works) ───────────────────────────────
NUTRIENT_ROWS = [('◎', '5g', 'Protein', 'n-protein'), ('⟋', '25g', 'Carbs', 'n-carbs'),
                 ('◈', '36g', 'Sugar', 'n-sugar'), ('◐', '12g', 'Fats', 'n-fat')]
nutrient_rows = ''.join(
    f'<li class="{c}"><i>{g}</i><span><b>{v}</b>{n}</span></li>' for g, v, n, c in NUTRIENT_ROWS)


def phone(cls=''):
    return f'''<div class="phone {cls}">
  <div class="phone-screen">
    {img('JAkAjO3nzzlBXQIicczRvbDEEng.png', 'A packet of biscuits framed in the scanner', 'camera-photo', True)}
    <div class="phone-top"><span>‹</span><strong>Scan food</strong><span>···</span></div>
    <div class="scan-frame"><i></i><i></i><i></i><i></i><div class="scan-line"></div></div>
    <div class="phone-camera"><span class="cam-thumb"></span><button class="shutter" tabindex="-1" aria-label="Preview food scan"></button><span>↻</span></div>
    <div class="analysis-sheet">
      <span class="sheet-grabber"></span>
      <div class="sheet-head">{img('JAkAjO3nzzlBXQIicczRvbDEEng.png', '', 'sheet-thumb')}<div><b>515 Calories</b><small>Nutella Biscuits</small></div></div>
      <div class="sheet-actions"><span class="phone-log">Add to log</span><span>Edit</span></div>
      <p class="sheet-label">Nutritional data</p>
      <ul class="sheet-nutrients">{nutrient_rows}</ul>
      <div class="scan-goal"><p><b>Goal</b><span>1,415 / 2000 kcal</span></p><i><em></em></i><small>Adding it leaves you with 585 calories for the day</small></div>
      <div class="sheet-ai"><p>✧ AI Suggestion</p><div>You’re low on protein today — swap one serving for Greek yogurt with berries to stay under goal and add 15g protein.</div><span>Ask {BRAND} AI ✧</span></div>
    </div>
  </div>
  {img('EYwE63Pj2EhNh6QWM26TBWhXD8Q.png', '', 'phone-hardware', True)}
</div>'''


# ── Food suggestions ───────────────────────────────────────────────────
FOOD = [  # name, good pick?, hint shown on hover
    ('Salad', True, 'Good pick · high fibre'), ('Meat', True, 'Good pick · 26g protein'),
    ('Ramen', False, 'Heavy on sodium'), ('Chocolate', False, 'High in sugar'),
    ('Pizza', False, 'Over your fat target'), ('Sandwhich', True, 'Fits your macros'),
    ('Salmon', True, 'Good pick · omega-3'),
]
food_orbit = ''.join(
    f'<button class="food-orbit food-{i}" data-recommendation="{"yes" if ok else "no"}" '
    f'aria-pressed="false" aria-label="{escape(n if n != "Sandwhich" else "Sandwich")}: {escape(hint)}">'
    f'<span class="food-bob">{icon(n)}</span><span class="food-hint"><em>{"✓" if ok else "×"}</em>{escape(hint)}</span></button>'
    for i, (n, ok, hint) in enumerate(FOOD))

# ── Burger ─────────────────────────────────────────────────────────────
burger_layers = [('HvjQmDxRBTKIbqDxNzJ0cUAK4fU.png', 'Top bun', 'Butter'),
                 ('H8sG3UXknbtlYDaq7sAodIzbnI.png', 'Grilled onion and tomato', 'Sauce'),
                 ('7eX4TRQB9ImxpRvIjFUsm5MYYI.png', 'Patty and cheese', 'Cooked in oil'),
                 ('tMaKfYWjAnAWOIq0SI15iAwub4.png', 'Lettuce', 'Dressing'),
                 ('O4R9JTspTUUYe3YUs6qsV3HZ09k.png', 'Bottom bun', 'Large portion')]
(ROOT / 'burger-layers.json').write_text(json.dumps(burger_layers))
burger = ''.join(
    f'<div class="burger-layer layer-{i}">{img(asset, alt)}'
    f'<span class="ingredient-tag"><span class="tag-thumb" style="background-image:url(/assets/{asset})"></span>{label}<i></i></span></div>'
    for i, (asset, alt, label) in enumerate(burger_layers))

# ── Feature cards ──────────────────────────────────────────────────────
graphics = [
    '<div class="calorie-widget"><div><span>Calorie Intake</span><small>388 Kcal 🥑</small></div><p><b>1,612</b> <em>/ 2000</em></p></div><div class="week">'
    + ''.join(f'<span class="{"selected" if day == "Sat" else ""}"><small>{day}</small>{i + 11}</span>' for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])) + '</div>',
    '<div class="food-plan"><div><b>Monday<br><span>6 Items</span></b><small>1,526 Kcal</small></div><div class="mini-foods">'
    + ''.join(icon(n) for n in ['Salad', 'Meat', 'Sandwhich', 'Meat']) + '<span>+2</span></div></div><div class="food-plan plan-ghost"><b>Tuesday<br><span>5 Items</span></b><small>1,544 Kcal</small></div>',
    '<div class="search-widget"><b>Search food items</b><div class="search-box"><span class="typed">Green Salads</span><span>⌕</span></div><p class="searching">Searching <i></i></p><div class="search-results"><p>' + icon('Salad') + '<span>Lettuce Tomato Salad<br><small>100 Kcal</small></span><i>›</i></p></div></div>',
    '<div class="barcode-widget"><div class="barcode"></div><i></i><i></i><i></i><i></i><div class="barcode-light"></div></div>',
]
features = ''.join(
    f'<article class="feature-card reveal" style="--d:{i % 2 * 90}ms"><div class="feature-graphic graphic-{i}">{graphics[i]}</div>'
    f'<div class="feature-copy"><h3>{escape(f["title"])}</h3><p>{escape(f["description"])}</p></div></article>'
    for i, f in enumerate(data['features']))

# ── Pricing (real tiers only: Free + COR Pro) ──────────────────────────
free = ['Personalized plan and targets', 'Manual food logging and food search', 'Known barcode lookup',
        'Workout tracking and rest timers', 'Strength history and progress', 'Apple Health integration']
pro = ['Everything in Free', 'Meal-photo and text estimates', 'Restaurant menu scanning',
       'Nutrition-label photos and new-product lookup', 'AI coach and weekly coaching', 'AI workouts and workout-photo import']
pro_price = f'<b>${escape(PRO_PRICE)}</b> <span>/month</span>' if PRO_PRICE else '<b class="price-tba">In app</b> <span>at launch</span>'
plans_data = [('Free', '<b>$0</b> <span>/month</span>', 'Anyone who’s getting started', free, 'Get started'),
              (f'{BRAND} Pro', pro_price, 'Users who want automation', pro, 'Try Pro')]
plans = ''.join(
    f'<article class="pricing-card plan-{i} reveal" style="--d:{i * 90}ms"><div class="price-heading"><h3>{escape(name)}</h3>'
    f'<p class="price">{price}</p><p>{escape(tag)}</p></div>{button(cta, DOWNLOAD, "solid-button plan-cta")}'
    f'<div class="includes">Includes<ul>' + ''.join(f'<li>{escape(x)}</li>' for x in feats) + '</ul></div></article>'
    for i, (name, price, tag, feats, cta) in enumerate(plans_data))

# ── FAQ (Smooth FAQ Flow style) ────────────────────────────────────────
faq = ''.join(
    f'<div class="flow-item reveal{" open" if i == 0 else ""}" style="--d:{i * 60}ms"><h3><button class="flow-q" aria-expanded="{"true" if i == 0 else "false"}" '
    f'aria-controls="faq-a{i}" id="faq-q{i}"><span>{escape(f["q"].replace("CŌR", BRAND))}</span><span class="flow-icon" aria-hidden="true"><i></i><i></i></span></button></h3>'
    f'<div class="flow-a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}"><div><p>{escape(f["a"].replace("CŌR", BRAND))}</p></div></div></div>'
    for i, f in enumerate(data['faq']))

# ── How it works ───────────────────────────────────────────────────────
steps = [('Scan your <br>food', 'Point your camera or scan a barcode the app instantly recognizes your meal with AI-powered accuracy.'),
         ('Get <br>Nutritional <br>Insights', 'See exactly what’s on your plate, calories, macros, and key nutrients, all broken down in seconds.'),
         ('Make Your <br>Action', 'Log it, tweak your plan, or ask AI for smarter alternatives all in one tap.')]
how_titles = ''.join(f'<h3 class="how-title{" active" if i == 0 else ""}">{t}</h3>' for i, (t, _) in enumerate(steps))
how_descs = ''.join(f'<p class="how-desc{" active" if i == 0 else ""}">{escape(d)}</p>' for i, (_, d) in enumerate(steps))
how_dots = ''.join(f'<button class="how-dot{" active" if i == 0 else ""}" data-step="{i}" aria-label="Step {i + 1}: {escape(t.replace("<br>", " "))}"></button>' for i, (t, _) in enumerate(steps))

# ── Real app screens (in place of the template's stock "results" photos) ──
screens = [('weight', 'Weight trend'), ('home', 'Daily food log'), ('strength', 'Strength history')]
screen_cards = ''.join(
    f'<figure class="result-card result-{i}">{img("product/" + n + ".png", label + " — real COR screen with sample data")}</figure>'
    for i, (n, label) in enumerate(screens))

nav_links = ''.join(f'<a class="lens-link" href="{h}">{t}</a>' for t, h in NAV)
hero_copy = data['sections'][0]['texts'][1].replace('CŌR', BRAND)
meal = data['sections'][2]['texts']
ai = data['sections'][5]['texts']
plates = [('CgUIeltv0Dq9CmMfit3NI4VHzY.png', 'Empty plate'), ('0S91gIGvUFBixLMM13HRQUucNwc.png', 'Omelet on plate'),
          ('gm6Geusoczh1lGedoY46WeMIBZs.png', 'Omelet and cheese'), ('RMrVeVtxfeVSJDV0ASPBXMU9U.png', 'Omelet, cheese and grilled chicken')]
plate_html = ''.join(img(a, alt, f'plate-layer plate-{i}') for i, (a, alt) in enumerate(plates))
ingredients = ''.join(f'<span class="ingredient ingredient-{i}">{icon(n)}</span>' for i, n in enumerate(['Omelet', 'Cheese', 'Chicken']))
contact = f'mailto:{SUPPORT_EMAIL}' if SUPPORT_EMAIL else '#faq'

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>COR Active</title>
<meta name="description" content="COR Active — the nutrition and training app that shows its work. Scan food, see what’s in it, log your lifts, and get one score with the arithmetic printed underneath.">
<meta name="theme-color" content="#030505">
<meta property="og:title" content="COR Active"><meta property="og:description" content="The nutrition and training app that shows its work on every number."><meta property="og:image" content="/icon-512.png">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="/favicon-64.png" sizes="64x64" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/brand/cor-metal-wordmark.webp" as="image">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/style.css">
<script>try{{if(sessionStorage.getItem('cor-preloaded'))document.documentElement.classList.add('skip-preloader')}}catch(e){{}}</script>
<script src="/app.js" defer></script></head>
<body>
<div class="preloader" aria-hidden="true"><div class="preloader-mark"><img src="/assets/brand/cor-metal-wordmark.webp" alt=""><span class="preloader-shine"></span></div></div>
<a class="skip-link" href="#main">Skip to content</a><div class="ambient" aria-hidden="true"></div>
<nav class="nav-bar" aria-label="Main navigation"><a class="brand" href="#top" aria-label="{BRAND} Active home"><span class="brand-star">✱</span><span>{BRAND}</span></a><div class="nav-links lens-bar">{nav_links}<span class="lens" aria-hidden="true"><i></i><i></i><i></i><i></i></span></div>{button(cls='solid-button nav-download')}<button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button><div id="mobile-menu" hidden>{''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}</div></nav>
<main id="main">
<section class="hero" id="top"><header class="hero-header"><span class="iphone-badge">{APPSTORE} Built for iPhone</span><h1>The app that<br><mark>shows its work</mark><br>on every number.</h1><p>{escape(hero_copy)}</p>{button(cls='solid-button hero-cta')}</header>
<div class="hero-scene"><div class="hero-sticky"><div class="hero-phone-group">{phone('hero-phone')}
<div class="float-food float-salad">{icon('Salad')}</div><div class="float-food float-ramen">{icon('Ramen')}</div><div class="float-food float-pizza">{icon('Pizza')}</div><div class="float-food float-chocolate">{icon('Chocolate')}</div>
<div class="nutrition-toast toast-carbs"><i>⟋</i><span><b>25g</b>Carbs</span></div><div class="nutrition-toast toast-protein"><i>◎</i><span><b>5g</b>Protein</span></div><div class="nutrition-toast toast-sugar"><i>◈</i><span><b>36g</b>Sugar</span></div><div class="nutrition-toast toast-fat"><i>◐</i><span><b>12g</b>Fats</span></div>
<h2 class="know-heading">Know what<br>you’re eating</h2></div></div></div></section>
<section class="food-suggestions section" id="food-suggestions"><div class="food-stage"><h2 class="reveal">Helps you find<br>what you should<br>eat.</h2>{food_orbit}<button class="food-help"><span aria-hidden="true">ⓘ</span> Hover over these icons</button></div><dialog id="food-guide"><button class="dialog-close" aria-label="Close guide">×</button>{icon('Salad')}<h3>Hover over the elements</h3><p>The 3D food icons are interactable — hovering over them shows which food you should probably eat. That’s what the app does for you.</p><p class="touch-help">On a touch screen, tap an icon to explore it.</p></dialog></section>
<section class="meal-section section" id="meal-deconstruct"><header class="section-header reveal"><h2>{escape(meal[0])}</h2><p>{escape(meal[1].replace("CŌR", BRAND))}</p></header><div class="burger-stage">{burger}</div></section>
<section class="how-section section" id="how-it-works"><div class="how-sticky"><div class="how-left">{how_titles}</div>{phone('how-phone')}<div class="how-right">{how_descs}<div class="how-dots">{how_dots}</div></div></div></section>
<section class="features-section section" id="features">{section_header(4)}<div class="feature-grid">{features}</div></section>
<section class="ai-section section" id="ai-meals"><header class="section-header reveal">{img('product/cor-app-icon.png', f'{BRAND} app icon', 'ai-icon')}<h2>{escape(ai[0])}</h2><p>{escape(ai[1])}</p></header><div class="meal-demo"><div class="plate-scene">{plate_html}</div><div class="meal-ingredients">{ingredients}</div><p class="meal-status" role="status"><i class="spinner" aria-hidden="true"></i><span>{BRAND} AI is thinking</span></p><div class="meal-total"><span>258 Calories</span><span>32g Protein</span></div><button class="prompt-demo" aria-label="Replay the meal demo"><span class="prompt-text">Make me a 30g protein dish under 300Kcal</span><span class="prompt-tools"><i>+</i><i>⚙ Tools</i><i class="mic">◖</i><i class="send">↑</i></span></button></div></section>
<section class="results-section section" id="screens"><header class="section-header reveal"><h2>Real screens. Real numbers.</h2><p>Everything here comes from the app itself — shown with sample data, so you can see exactly what you’ll get.</p></header><div class="result-cards">{screen_cards}</div><a class="pill-link" href="#how-it-works">See it in action {ARROW}</a></section>
<section class="pricing-section section" id="pricing">{section_header(7)}<div class="pricing-grid">{plans}</div><p class="pricing-footnote">Subscriptions, prices and any eligible trial are shown in the app before you buy.</p></section>
<section class="faq-section section" id="faq">{section_header(8)}<div class="flow-list">{faq}</div></section>
<section class="cta-section section" id="download"><div class="cta-icon reveal">{img('product/cor-app-icon.png', f'{BRAND} app icon', 'app-icon')}{img('vfwd58TDMrxP0cuErxsVbpt2Qs.png', '', 'crown')}</div><span class="iphone-badge">{APPSTORE} Built for iPhone</span><h2>See your plan before you make an account.</h2><p>Answer the setup questions and get your calorie and macro targets, your goal timeline with dated milestones, and the goal that actually fits your body composition. Sign in only if you want to keep it.</p>{button()}</section>
</main>
<footer class="footer" id="legal"><div class="footer-top"><div class="footer-about"><a class="footer-brand" href="#top">{BRAND}</a><p>The nutrition and training app that shows its work.</p></div><div><h3>Product</h3><a href="#top">Home</a><a href="#pricing">Pricing</a><a href="{DOWNLOAD}">Download</a><a href="{contact}">Contact</a></div><div><h3>Legal</h3><a href="{PRIVACY_URL or '#legal'}">Privacy Policy</a><a href="{TERMS_URL or '#legal'}">Terms &amp; Conditions</a></div></div>
<div class="copyright">© 2026 COR Active. All rights reserved.</div>
<a class="footer-metal" href="#top" aria-label="Back to top"><video autoplay muted loop playsinline preload="metadata" poster="/assets/brand/cor-liquid-metal-poster.jpg"><source src="/assets/brand/cor-liquid-metal.mp4" type="video/mp4"></video></a></footer>
</body></html>'''
(ROOT / 'dist/index.html').write_text(html)
print('Built COR Active homepage')

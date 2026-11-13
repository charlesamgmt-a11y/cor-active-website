"""Build the COR Active homepage.

Layout, typography and motion follow the owner's Framer project
(Calories copy, published at goodness-zebra-710061.framer.app).
Product copy comes from reference-data.json, reviewed against the COR app.

Run:      python3 build.py
Preview:  python3 -m http.server 4317 --bind 127.0.0.1 --directory dist
"""
from pathlib import Path
import json
import hashlib
from html import escape

# ── Links: paste the real ones here before launch, then rebuild ─────────
APP_STORE_URL = ''          # e.g. https://apps.apple.com/app/id0000000000
PRIVACY_URL = ''            # public privacy policy page
TERMS_URL = ''              # public terms page
SUPPORT_EMAIL = 'support@coractive.co'
PRO_PRICE = ''              # e.g. '9.99'  (leave empty to show "In app")
# ────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'reference-data.json').read_text())
BRAND = 'CŌR'
DOWNLOAD = APP_STORE_URL or '#download'
DOWNLOAD_LABEL = 'Download for iPhone' if APP_STORE_URL else 'Coming soon'
AVAILABILITY = 'Built for iPhone' if APP_STORE_URL else 'Coming soon for iPhone'
ARROW = '<span aria-hidden="true">›</span>'
APPSTORE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#1d8cf8"/><path d="M8.1 16.6h7.8M9.6 16.6l3.9-8.9M14.4 16.6l-1.6-3.6M10.3 7.7l.8 1.8" stroke="#fff" stroke-width="1.6" stroke-linecap="round" fill="none"/></svg>'
NAV = [('Features', '#features'), ('How it works', '#how-it-works'), ('App screens', '#screens')]

def versioned_asset(name):
    digest = hashlib.sha256((ROOT / 'dist' / name).read_bytes()).hexdigest()[:12]
    return f'/{name}?v={digest}'


def img(name, alt='', cls='', eager=False):
    src = versioned_asset(f'assets/{name}') if name.startswith('brand/cor-') else f'/assets/{name}'
    return (f'<img src="{escape(src, quote=True)}" alt="{escape(alt)}" class="{cls}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')


def icon(name, cls='deco'):
    return img(data['icons'][name], '', cls)


def button(label=DOWNLOAD_LABEL, href=DOWNLOAD, cls='solid-button'):
    return f'<a class="{cls} dot-button" href="{escape(href, quote=True)}"><span class="dot-label">{escape(label)}</span></a>'


def section_header(index):
    t = data['sections'][index]['texts']
    return (f'<header class="section-header reveal"><h2>{escape(t[0])}</h2>'
            f'<p>{escape(t[1].replace("CŌR", BRAND))}</p></header>')


# ── Phone (shared by hero + how-it-works) ───────────────────────────────
NUTRIENT_ROWS = [('◎', '5g', 'Protein', 'n-protein'), ('⟋', '25g', 'Carbs', 'n-carbs'),
                 ('◈', '12g', 'Sugar', 'n-sugar'), ('◐', '12g', 'Fats', 'n-fat')]
nutrient_rows = ''.join(
    f'<li class="{c}"><i>{g}</i><span><b>{v}</b>{n}</span></li>' for g, v, n, c in NUTRIENT_ROWS)


def phone(cls=''):
    return f'''<div class="phone {cls}">
  <div class="phone-screen">
    {img('JAkAjO3nzzlBXQIicczRvbDEEng.png', 'A packet of biscuits framed in the scanner', 'camera-photo', True)}
    <div class="phone-top"><span>‹</span><strong>Scan food</strong><span>···</span></div>
    <div class="scan-frame"><i></i><i></i><i></i><i></i><div class="scan-line"></div></div>
    <div class="phone-camera"><span class="cam-thumb"></span><span class="shutter" aria-hidden="true"></span><span>↻</span></div>
    <div class="analysis-sheet">
      <span class="sheet-grabber"></span>
      <div class="sheet-head">{img('JAkAjO3nzzlBXQIicczRvbDEEng.png', '', 'sheet-thumb')}<div><b>228 Calories</b><small>Illustrative serving</small></div></div>
      <div class="sheet-actions"><span class="phone-log">Add to log</span><span>Edit</span></div>
      <p class="sheet-label">Nutritional data</p>
      <ul class="sheet-nutrients">{nutrient_rows}</ul>
      <div class="scan-goal"><p><b>Goal</b><span>1,415 / 2000 kcal</span></p><i><em></em></i><small>Adding it leaves you with 585 calories for the day</small></div>
      <div class="sheet-ai"><p>✧ AI Suggestion</p><div>You’re low on protein today — swap one serving for Greek yogurt with berries to stay under goal and add 15g protein.</div><span>Ask {BRAND} AI ✧</span></div>
    </div>
  </div>
  {img('EYwE63Pj2EhNh6QWM26TBWhXD8Q.png', '', 'phone-hardware', True)}
</div>'''


def iphone_hero():
    return f'''<div class="hero-phone hero-iphone" role="img" aria-label="COR nutrition screen in the blue iPhone bezel, with illustrative records">
  <div class="iphone-screen-bed" aria-hidden="true"><img src="/assets/product/nutrition.png" alt="" fetchpriority="high"></div>
  {img('brand/iphone-18-pro-max-glacier-portrait.png', '', 'iphone-bezel', True)}
</div>'''


# ── Food suggestions ───────────────────────────────────────────────────
FOOD = [  # name, good pick?, hint shown on hover
    ('Salad', True, 'Include the dressing'), ('Meat', True, 'Check the portion'),
    ('Ramen', True, 'Review the ingredients'), ('Chocolate', True, 'Choose your serving'),
    ('Pizza', True, 'Log by the slice'), ('Sandwhich', True, 'Add sauces and extras'),
    ('Salmon', True, 'Include cooking oil'),
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


# ── How it works ───────────────────────────────────────────────────────
steps = [('Log your <br>food', 'Search for a food, scan a recognized barcode, or use Pro to estimate a meal from a photo or description.'),
         ('Review the <br>details', 'For photo estimates, add hidden ingredients and portion details. Review and edit the nutrition before saving.'),
         ('Keep your <br>day in view', 'Save your meal to the daily log and see how it contributes to your calorie and macro targets.')]
how_titles = ''.join(f'<h3 class="how-title{" active" if i == 0 else ""}">{t}</h3>' for i, (t, _) in enumerate(steps))
how_descs = ''.join(f'<p class="how-desc{" active" if i == 0 else ""}">{escape(d)}</p>' for i, (_, d) in enumerate(steps))
how_dots = ''.join(f'<button class="how-dot{" active" if i == 0 else ""}" data-step="{i}" aria-label="Step {i + 1}: {escape(t.replace("<br>", " "))}"></button>' for i, (t, _) in enumerate(steps))

barbell_assembly = '''<svg class="assembly-barbell" viewBox="0 0 1000 570" role="img" aria-label="Brushed silver weight plates float apart and stack together as you scroll"><defs>
<linearGradient id="plate-edge" x2="0" y2="1"><stop stop-color="#d0d2d4"/><stop offset=".35" stop-color="#565b60"/><stop offset=".8" stop-color="#15191d"/><stop offset="1" stop-color="#989da2"/></linearGradient>
<radialGradient id="plate-silver" cx="32%" cy="25%" r="80%"><stop stop-color="#fff"/><stop offset=".28" stop-color="#bcc2c7"/><stop offset=".52" stop-color="#f2f3f4"/><stop offset=".76" stop-color="#767f87"/><stop offset="1" stop-color="#c4c9ce"/></radialGradient>
<linearGradient id="hub-silver"><stop stop-color="#596169"/><stop offset=".45" stop-color="#f6f7f8"/><stop offset="1" stop-color="#747c84"/></linearGradient>
<g id="silver-plate"><ellipse cy="22" rx="218" ry="90" fill="#090b0d"/><path d="M-218 0v22a218 90 0 0 0 436 0V0" fill="url(#plate-edge)"/><ellipse rx="218" ry="90" fill="#252a2e" stroke="#a1a7ac"/><ellipse rx="205" ry="83" fill="url(#plate-silver)"/><ellipse rx="104" ry="42.016000000000005" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="102" ry="41.208000000000006" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="110" ry="44.440000000000005" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="108" ry="43.632000000000005" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="116" ry="46.864000000000004" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="114" ry="46.056000000000004" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="122" ry="49.288000000000004" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="120" ry="48.480000000000004" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="128" ry="51.712" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="126" ry="50.904" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="134" ry="54.136" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="132" ry="53.328" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="140" ry="56.56" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="138" ry="55.752" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="146" ry="58.984" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="144" ry="58.176" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="152" ry="61.408" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="150" ry="60.6" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="158" ry="63.832" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="156" ry="63.024" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="164" ry="66.256" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="162" ry="65.44800000000001" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="170" ry="68.68" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="168" ry="67.872" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="176" ry="71.104" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="174" ry="70.296" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="182" ry="73.528" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="180" ry="72.72" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="188" ry="75.952" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="186" ry="75.144" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="194" ry="78.376" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="192" ry="77.56800000000001" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="200" ry="80.80000000000001" fill="none" stroke="#454f58" stroke-opacity=".2" stroke-width=".7"/><ellipse rx="198" ry="79.992" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width=".7"/><ellipse rx="98" ry="40" fill="#2a3035" stroke="#d2d6d9" stroke-width="2"/><ellipse rx="39" ry="16" fill="url(#hub-silver)"/><ellipse rx="25" ry="10" fill="#07090b"/><path d="M-23 1Q0 11 23 1" fill="none" stroke="#899198" stroke-width="2"/></g></defs><ellipse class="plate-ground" cx="500" cy="455" rx="210" ry="20" fill="#a8b3bc" opacity=".08"/>
<g transform="translate(500 382)"><g class="floating-plate" style="--spread:78px"><use href="#silver-plate"/></g></g>
<g transform="translate(500 354)"><g class="floating-plate" style="--spread:-36px"><use href="#silver-plate"/></g></g>
<g transform="translate(500 326)"><g class="floating-plate" style="--spread:-150px"><use href="#silver-plate"/></g></g></svg>'''

# ── Product showcase: one current app capture at a time ────────────────
showcase_items = [
    ('food', 'Hidden ingredients', 'questions', 'Add the details a photo can miss.',
     'Add oil, butter, sauces or other extras a photo may miss before reviewing your meal estimate.'),
    ('ingredients', 'Understand the grade', 'ingredients', 'See the reasons behind the grade.',
     'Review ingredient flags, positive findings and the explanation behind a product’s CŌR grade.')
]

showcase_tabs = ''.join(
    f'<button type="button" class="showcase-tab{" active" if i == 0 else ""}" role="tab" id="showcase-tab-{key}" '
    f'aria-controls="showcase-panel" aria-selected="{"true" if i == 0 else "false"}" tabindex="{"0" if i == 0 else "-1"}" '
    f'data-showcase="{key}" data-screen="/assets/product/{image_name}.png" data-title="{escape(label)}" data-background="">'
    f'<span class="showcase-tab-number">0{i + 1}</span><span class="showcase-tab-title">{escape(label)}</span><span class="showcase-tab-arrow" aria-hidden="true">↗</span>'
    f'<span class="showcase-tab-description">{escape(description)}</span></button>'
    for i, (key, label, image_name, _, description) in enumerate(showcase_items))
showcase_image = img('product/questions.png', 'CŌR food details screen, shown with illustrative records', 'showcase-screen', True)

nav_links = ''.join(f'<a class="lens-link" href="{h}">{t}</a>' for t, h in NAV)
hero_copy = data['sections'][0]['texts'][1].replace('CŌR', BRAND)
meal = data['sections'][2]['texts']
ai = data['sections'][5]['texts']
plates = [('CgUIeltv0Dq9CmMfit3NI4VHzY.png', 'Empty plate'), ('0S91gIGvUFBixLMM13HRQUucNwc.png', 'Omelet on plate'),
          ('gm6Geusoczh1lGedoY46WeMIBZs.png', 'Omelet and cheese'), ('RMrVeVtxfeVSJDV0ASPBXMU9U.png', 'Omelet, cheese and grilled chicken')]
plate_html = ''.join(img(a, alt, f'plate-layer plate-{i}') for i, (a, alt) in enumerate(plates))
ingredients = ''.join(f'<span class="ingredient ingredient-{i}">{icon(n)}</span>' for i, n in enumerate(['Omelet', 'Cheese', 'Chicken']))
contact_link = f'<a href="mailto:{escape(SUPPORT_EMAIL, quote=True)}">{escape(SUPPORT_EMAIL)}</a>' if SUPPORT_EMAIL else ''
legal_links = '<a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a>'
final_cta = button('Join the waitlist', '#waitlist')

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>COR Active – Track the work. See the payoff.</title>
<meta name="description" content="Meals, weight, sets, reps and body fat—plus calories, ingredients and a score that shows the math. Join the CŌR Active launch waitlist.">
<link rel="canonical" href="https://coractive.co/">
<meta property="og:url" content="https://coractive.co/">
<meta name="theme-color" content="#030505">
<meta property="og:type" content="website"><meta property="og:title" content="COR Active – Track the work. See the payoff."><meta property="og:description" content="Meals, weight, sets, reps and body fat—plus calories, ingredients and a score that shows the math. Join the CŌR Active launch waitlist."><meta property="og:image" content="https://coractive.co/assets/brand/cor-og-preview.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="CŌR nutrition and training app screen with the message Track the work. See the payoff.">
<link rel="icon" href="{versioned_asset('favicon-32.png')}" sizes="32x32" type="image/png"><link rel="icon" href="{versioned_asset('favicon-64.png')}" sizes="64x64" type="image/png"><link rel="apple-touch-icon" href="{versioned_asset('apple-touch-icon.png')}">
<link rel="preload" href="{versioned_asset('assets/brand/cor-metal-wordmark.webp')}" as="image">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="{versioned_asset('style.css')}">
<script>try{{if(sessionStorage.getItem('cor-preloaded'))document.documentElement.classList.add('skip-preloader')}}catch(e){{}}</script>
<script src="{versioned_asset('app.js')}" defer></script><script type="module" src="{versioned_asset('original-components.js')}"></script><script type="module" src="{versioned_asset('sticky-original.js')}"></script></head>
<body>
<div class="preloader" aria-hidden="true"><div class="preloader-mark"><img src="{versioned_asset('assets/brand/cor-metal-wordmark.webp')}" alt=""><span class="preloader-shine"></span></div></div>
<div class="custom-cursor" aria-hidden="true"><span class="cursor-ring"></span><span class="cursor-dot"></span></div>
<a class="skip-link" href="#main">Skip to content</a><div class="ambient" aria-hidden="true"></div>
<nav class="nav-bar" aria-label="Main navigation"><a class="brand" href="#top" aria-label="{BRAND} home">{img('brand/cor-nav-wordmark.svg', BRAND, 'nav-wordmark', True)}</a><div class="nav-links lens-bar">{nav_links}<span class="lens" aria-hidden="true"><i></i><i></i><i></i><i></i></span></div>{button('Join the waitlist', '#waitlist', 'solid-button nav-download')}<button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button><div id="mobile-menu" hidden>{''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}</div></nav>
<main id="main" tabindex="-1">
<section class="hero" id="top"><header class="hero-header"><span class="iphone-badge">{APPSTORE} Coming soon for iPhone</span><h1>Track the work.<br><mark>See the payoff.</mark></h1><p>{escape(hero_copy)}</p>{button('Join the waitlist', '#waitlist', 'solid-button hero-cta')}</header>
<div class="hero-scene"><div class="hero-sticky"><div class="hero-phone-group">{iphone_hero()}
<div class="float-food float-salad">{icon('Salad')}</div><div class="float-food float-ramen">{icon('Ramen')}</div><div class="float-food float-pizza">{icon('Pizza')}</div><div class="float-food float-chocolate">{icon('Chocolate')}</div>
<div class="nutrition-toast toast-carbs"><i>⟋</i><span><b>25g</b>Carbs</span></div><div class="nutrition-toast toast-protein"><i>◎</i><span><b>5g</b>Protein</span></div><div class="nutrition-toast toast-sugar"><i>◈</i><span><b>12g</b>Sugar</span></div><div class="nutrition-toast toast-fat"><i>◐</i><span><b>12g</b>Fats</span></div>
<h2 class="know-heading">Know what<br>you’re eating</h2></div></div></div><p class="demo-note">Captured CŌR nutrition screen with illustrative records. <a href="#screens">Explore the iPhone screens</a>.</p></section>
<section class="food-suggestions section" id="food-suggestions"><div class="food-stage"><h2 class="reveal">Make room for<br>the details<br>in every meal.</h2>{food_orbit}<button class="food-help"><span aria-hidden="true">ⓘ</span> Tap or hover to explore</button></div><dialog id="food-guide"><button class="dialog-close" aria-label="Close guide">×</button>{icon('Salad')}<h3>Details make a difference</h3><p>Explore examples of portion and ingredient details you can include when logging a meal. These illustrations are prompts, not personalized food recommendations.</p><p class="touch-help">On a touch screen, tap an icon to explore it.</p></dialog></section>
<section class="how-section section" id="how-it-works"><div class="how-sticky"><div class="how-left">{how_titles}</div>{phone('how-phone')}<div class="how-right">{how_descs}<div class="how-dots">{how_dots}</div><p class="demo-note">Illustrated flow · sample values</p></div></div></section>
<section class="meal-section section" id="meal-deconstruct"><header class="section-header reveal"><h2>{escape(meal[0])}</h2><p>{escape(meal[1].replace("CŌR", BRAND))}</p></header><div class="burger-stage">{burger}</div></section>
<section class="features-section section" id="features"><span id="screens" class="anchor-alias" aria-hidden="true"></span>{section_header(4)}<div class="showcase-scroll-start" aria-hidden="true"></div><div class="showcase-layout"><div class="showcase-content"><div class="showcase-tabs" role="tablist" aria-label="Explore CŌR ingredient features">{showcase_tabs}</div><p class="showcase-note">App screen details shown with illustrative records. <span>Scroll to explore. Tap a step or use arrow keys.</span></p></div><div class="showcase-stage"><!-- BACKGROUND PHOTO SLOT: set --showcase-background to the supplied image when ready. --><div class="showcase-photo-slot" aria-hidden="true"></div><figure class="showcase-device" id="showcase-panel" role="tabpanel" aria-labelledby="showcase-tab-food"><div class="showcase-phone"><button type="button" class="screen-shot showcase-capture" data-screen="/assets/product/questions.png" data-title="Hidden ingredients" aria-label="Enlarge Hidden ingredients app screen">{showcase_image}<span class="capture-zoom" aria-hidden="true">↗</span></button><img class="showcase-bezel" src="/assets/brand/iphone-duo-star-white-outer-closed-portrait.png" alt="" aria-hidden="true"></div><figcaption><span class="capture-count">01 — 02</span><span>CŌR for iPhone</span></figcaption></figure></div></div></section>
<section class="barbell-section" id="training-intro"><div class="barbell-pin"><header class="section-header"><p class="assembly-eyebrow">FUEL. TRAIN. BUILD.</p><h2>Built one set at a time.</h2><p>Know what fuels you. See what your training adds up to.</p></header><div class="barbell-stage">{barbell_assembly}</div><a class="assembly-next" href="#strength">See your training in CŌR <span aria-hidden="true">↓</span></a></div></section>
<section class="training-story section" id="strength"><header class="section-header"><h2>Log the work. See what adds up.</h2><p>Your sets, personal records and training history, together.</p></header><div id="original-sticky"><p>Training volume, recent sessions, personal records and weight trends in CŌR.</p></div><div class="strength-screen-links" aria-label="Enlarge training app screens"><button type="button" class="strength-screen-button dot-button dot-button-dark" data-screen="/assets/product/workout-history.png" data-title="Workout history"><span class="dot-label">Workout history</span></button><button type="button" class="strength-screen-button dot-button dot-button-dark" data-screen="/assets/product/strength.png" data-title="Strength overview"><span class="dot-label">Strength overview</span></button><button type="button" class="strength-screen-button dot-button dot-button-dark" data-screen="/assets/product/muscle-balance.png" data-title="Muscle groups"><span class="dot-label">Muscle groups</span></button></div><p class="capture-caption">Real app captures · illustrative records</p></section>
<section class="cta-section section" id="download"><div class="cta-icon reveal"><div class="app-icon">{img('brand/cor-mirror-transparent.png', f'{BRAND} app logo', 'app-icon-wordmark')}</div></div><span class="iphone-badge">{APPSTORE} Coming soon for iPhone</span><h2>See your plan before you make an account.</h2><p>Answer the setup questions and get your calorie and macro targets, your goal timeline with dated milestones, and a suggested goal based on your setup answers. Sign in when you are ready to keep your plan.</p>{final_cta}</section>
<section class="waitlist-section section" id="waitlist"><header class="section-header"><span class="eyebrow">CŌR is coming soon</span><h2>Get launch updates.</h2><p>Join for early access news and the launch announcement. You can unsubscribe at any time.</p></header><form class="waitlist-preview" aria-label="CŌR launch waitlist preview"><label for="waitlist-email">Email address</label><div class="waitlist-row"><input id="waitlist-email" type="email" name="email" autocomplete="email" placeholder="you@example.com" disabled><button class="solid-button dot-button" type="button" disabled><span class="dot-label">Join the waitlist</span></button></div><p class="waitlist-status" role="status">Waitlist signup is not available yet. Please check back soon.</p><!-- BREVO EMBED GOES HERE: replace this preview form with the Brevo embed in build.py, in the #waitlist section. --></form></section>
<section class="contact-section section" id="contact"><h2>Questions? Get in touch.</h2><p>For support or launch questions, email <a href="mailto:{escape(SUPPORT_EMAIL)}">{escape(SUPPORT_EMAIL)}</a>.</p></section>
</main>
<dialog id="screen-viewer" aria-labelledby="screen-viewer-title"><button class="screen-close" aria-label="Close app screenshot">×</button><h2 id="screen-viewer-title">CŌR app screen</h2><p>CŌR interface · illustrative records</p><img alt=""></dialog>
<footer class="footer" id="legal"><div class="footer-top"><div class="footer-about"><p>The nutrition and training app that shows its work.</p></div><div><h3>Product</h3><a href="#top">Home</a><a href="#waitlist">Join the waitlist</a><a href="#contact">Contact</a>{contact_link}</div><div><h3>Legal &amp; Privacy</h3>{legal_links}</div></div>
<div class="copyright">© 2026 CŌR Active. All rights reserved.</div>
<div class="footer-mark-wrap"><a class="footer-metal" href="#top" aria-label="Back to top"><video autoplay muted loop playsinline preload="metadata" aria-hidden="true" poster="{versioned_asset('assets/brand/cor-liquid-metal-poster.jpg')}"><source src="{versioned_asset('assets/brand/cor-liquid-metal.mp4')}" type="video/mp4"></video></a></div></footer>
</body></html>'''
(ROOT / 'dist/index.html').write_text(html)

def legal_page(title, slug, description, body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | COR Active</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="https://coractive.co/{slug}/">
<meta name="theme-color" content="#000000"><link rel="icon" href="{versioned_asset('favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/style.css"></head>
<body><a class="skip-link" href="#legal-main">Skip to content</a><main id="legal-main" class="legal-document" tabindex="-1">
<header><a href="/" class="legal-top-link">← Back to {BRAND} Active</a><p><span class="draft-banner">DRAFT — FOR REVIEW</span></p><h1>{escape(title)}</h1><p class="last-updated">Last updated: November 1, 2026</p></header>
<article>{body}<p class="legal-top-link"><a href="mailto:{escape(SUPPORT_EMAIL, quote=True)}">Questions? Contact {escape(SUPPORT_EMAIL)}</a></p><a class="legal-top-link" href="/">Return to {BRAND} Active</a></article>
</main></body></html>'''

privacy_body = '''
<p><strong>Draft for review:</strong> This page describes the intended practices supplied for CŌR. Confirm the bracketed operational details and have the final policy reviewed before making it public.</p>
<h2>Who this policy covers</h2><p>This policy covers the CŌR iPhone and Apple Watch apps, the CŌR Active website, and the launch waitlist. “CŌR,” “we,” and “our” refer to CŌR Active. For privacy questions, contact <a href="mailto:support@coractive.co">support@coractive.co</a>.</p>
<h2>Information you provide</h2><ul><li>Account details supplied through Sign in with Apple or Google, such as an account identifier, name, or email address, handled through Supabase.</li><li>Profile and app information you choose to enter, including goals, meals, nutrition, workouts, weight, measurements, and feedback.</li><li>Health information you choose to connect through Apple Health, subject to the permissions you grant. Supported information may include steps, workouts, heart rate, sleep, weight, body fat, and meal calories or macros. You can manage access in Apple Health and iOS settings.</li><li>Photos, descriptions, and other content you submit when you choose an AI feature. A feature may send the content needed for that request to its AI service provider.</li><li>If you join the launch waitlist, your email address and subscription or confirmation status, handled through Brevo.</li></ul>
<h2>How information is used</h2><p>We use information to operate and personalize CŌR, sync your account, show the health and fitness features you request, answer support messages, process an AI request you choose to make, and send waitlist or launch updates you signed up to receive.</p>
<h2>Apple Health information</h2><p>HealthKit access is permission-based. You can grant or deny supported read and write permissions separately. We use health information to provide CŌR health and fitness functionality. We do not sell health data and do not use it for advertising. Health data is not used to target ads. Information already written to Apple Health may remain there after you delete your CŌR account; manage or remove those records in Apple Health.</p>
<h2>Optional AI features</h2><p>AI features are optional. When you choose one, CŌR may send the text, image, or other information shown in that feature to an AI provider so it can return an estimate or response. Review the in-app notice before sending. <strong>[Before publication, list the active AI providers, the types of inputs each receives, and their retention or model-training terms.]</strong></p>
<h2>Service providers and sharing</h2><p>We use service providers to operate the product: Supabase for authentication and app services, Apple and Google for sign-in, Apple HealthKit when you connect it, Brevo for waitlist email, and AI providers only when you choose an AI feature. We do not sell personal or health information and do not use health data for advertising. We may disclose information if required by law or to protect the service and its users.</p>
<h2>How long we keep information</h2><p>We keep account information while your account is active and for the time needed to provide the service, meet legal obligations, resolve disputes, and protect the service. Waitlist information is kept until you unsubscribe or ask us to remove it. <strong>[Confirm the actual retention period for backups, support messages, and provider logs before publication.]</strong></p>
<h2>Your choices and deletion</h2><ul><li>Change Apple Health permissions in Apple Health or iOS Settings.</li><li>Delete your CŌR account in the app’s Settings under “Delete Account.” Account deletion removes the account and associated CŌR data from active systems; <strong>[confirm backup deletion timing and any records that must be retained]</strong>.</li><li>Use the unsubscribe link in a Brevo email to stop waitlist messages, or email <a href="mailto:support@coractive.co">support@coractive.co</a> to request removal.</li><li>Contact us to ask about access, correction, or deletion of information.</li></ul>
<h2>Security and children</h2><p>We use technical and organizational safeguards designed to protect information. No online service can guarantee absolute security. CŌR is not designed for children under 13, and we do not knowingly ask children under 13 to create an account.</p>
<h2>Changes to this policy</h2><p>We may update this policy as CŌR changes. We will update the date above and provide additional notice when required.</p>
'''

terms_body = '''
<p><strong>Draft for review:</strong> This draft describes the intended CŌR service. Confirm the bracketed company and jurisdiction details and review the final terms before publication.</p>
<h2>About CŌR</h2><p>CŌR is a nutrition and fitness app from CŌR Active. It offers food logging, nutrition information, workout tracking, progress tools, Apple Health connections, and optional AI-assisted features. The app is coming soon.</p>
<h2>Accounts</h2><p>You may create an account using Sign in with Apple or Google. Keep your sign-in details secure and provide accurate information. You can delete your account through Settings in the app. Account deletion removes your CŌR account and associated data from active systems, subject to the retention details in the Privacy Policy.</p>
<h2>Health and fitness information</h2><p>CŌR is for general wellness and fitness information. Calorie, nutrition, body-fat, workout, and AI-generated values may be estimates and can be incomplete or inaccurate. They are not medical advice, diagnosis, or treatment, and should not replace advice from a qualified health professional. Use your judgment and stop any activity that feels unsafe.</p>
<h2>Apple Health and connected services</h2><p>Apple Health access is optional and controlled by permissions on your device. You are responsible for reviewing those permissions and any third-party service terms that apply to services you choose to connect.</p>
<h2>Optional AI features</h2><p>AI-assisted features are optional and may produce inaccurate or incomplete results. You are responsible for reviewing an estimate or response before relying on it or saving it. When you choose an AI feature, the information shown in that feature may be sent to a service provider to generate a result.</p>
<h2>Subscriptions and payments</h2><p>CŌR is free to start, with CŌR Pro available in the app. Any price, trial, renewal period, and cancellation terms will be shown before you confirm a purchase. App Store subscriptions are managed through your Apple account. <strong>[Confirm subscription terms and any trial details before launch.]</strong></p>
<h2>Acceptable use</h2><p>Do not misuse CŌR, interfere with its operation, attempt unauthorized access, or use it unlawfully. Do not submit content you do not have the right to use or that violates another person’s rights.</p>
<h2>Service availability and changes</h2><p>We may update, suspend, or discontinue features to maintain or improve the service, comply with law, or address safety or security concerns. We will provide notice where required.</p>
<h2>Intellectual property</h2><p>CŌR Active owns or licenses CŌR, its software, branding, and content. These terms give you a personal, limited, non-transferable right to use the app for its intended purpose. You keep ownership of content you submit, and authorize us to process it only as needed to provide the features you choose.</p>
<h2>Disclaimers and liability</h2><p>To the extent permitted by law, CŌR is provided as available and without guarantees that every result will be accurate, uninterrupted, or suitable for your needs. Nothing in these terms removes rights that cannot legally be limited. <strong>[Have counsel complete jurisdiction-specific warranty and liability language.]</strong></p>
<h2>Governing law and contact</h2><p><strong>[Confirm the contracting legal entity and governing-law jurisdiction before publication.]</strong> For questions, contact <a href="mailto:support@coractive.co">support@coractive.co</a>.</p>
'''

for slug, title, description, body in [
    ('privacy', 'Privacy Policy', 'Draft privacy policy for CŌR Active, the COR Active health and fitness app.', privacy_body),
    ('terms', 'Terms of Use', 'Draft terms for using the CŌR Active health and fitness app.', terms_body)
]:
    target = ROOT / 'dist' / slug
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(legal_page(title, slug, description, body))

not_found = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | COR Active</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/style.css"></head><body><main class="not-found"><h1>Page not found.</h1><p>That address doesn’t lead to a CŌR page. Head back to the site and keep going.</p><a class="solid-button dot-button" href="/"><span class="dot-label">Back to CŌR Active</span></a></main></body></html>'''
(ROOT / 'dist' / '404.html').write_text(not_found)
(ROOT / 'dist' / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://coractive.co/sitemap.xml\n')
(ROOT / 'dist' / 'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://coractive.co/</loc></url>
  <url><loc>https://coractive.co/privacy/</loc></url>
  <url><loc>https://coractive.co/terms/</loc></url>
</urlset>
''')
# Brevo redirects to these pages after submission and after email verification.
# The pages themselves never add or confirm a contact; Brevo owns that state.
def waitlist_status_page(title, heading, message, detail, confirmed=False):
    symbol = ('<path d="m8 17 6 6 12-13"/>' if confirmed else
              '<rect x="5" y="8" width="26" height="20" rx="3"/><path d="m6 10 12 9 12-9"/>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | COR Active</title><meta name="robots" content="noindex,follow">
<meta name="theme-color" content="#000000"><link rel="icon" href="{versioned_asset('favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="stylesheet" href="{versioned_asset('fonts.css')}"><link rel="stylesheet" href="{versioned_asset('style.css')}"></head>
<body class="waitlist-result"><a class="skip-link" href="#main">Skip to content</a>
<header class="waitlist-result-header"><a href="/" aria-label="COR Active home">{img('brand/cor-nav-wordmark.svg', 'COR Active')}</a></header>
<main id="main" class="waitlist-result-main" tabindex="-1">
<svg class="waitlist-result-icon" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{symbol}</svg>
<p class="waitlist-result-eyebrow">COR Active · Launch waitlist</p><h1>{escape(heading)}</h1>
<p class="waitlist-result-message">{escape(message)}</p><p class="waitlist-result-detail">{detail}</p>
<a class="solid-button dot-button" href="/#features"><span class="dot-label">Explore CŌR</span></a>
<p class="waitlist-result-help">Need a hand? <a href="mailto:{escape(SUPPORT_EMAIL, quote=True)}">{escape(SUPPORT_EMAIL)}</a></p>
</main><footer class="waitlist-result-footer"><a href="/privacy/">Privacy policy</a><span>© 2026 COR Active</span></footer>
</body></html>'''

for slug, title, heading, message, detail, confirmed in [
    ('check-email', 'Confirm your email', 'One more step.',
     'Check your inbox for an email from COR Active. Follow the confirmation link to join the waitlist.',
     'No email yet? Check your spam folder. If you entered the wrong address, <a href="/#waitlist">try again</a>.', False),
    ('confirmed', 'Welcome to the waitlist', 'You’re on the list.',
     'Thanks for confirming your email. We’ll send you early access news and let you know when CŌR launches.',
     'You can unsubscribe at any time using the link in our emails.', True)
]:
    target = ROOT / 'dist' / 'waitlist' / slug
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(waitlist_status_page(title, heading, message, detail, confirmed))

print('Built COR Active homepage, draft legal pages, waitlist confirmation pages, and SEO files')

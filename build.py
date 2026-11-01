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
SUPPORT_EMAIL = ''          # e.g. support@coractive.app
PRO_PRICE = ''              # e.g. '9.99'  (leave empty to show "In app")
# ────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'reference-data.json').read_text())
BRAND = 'COR'
DOWNLOAD = APP_STORE_URL or '#download'
DOWNLOAD_LABEL = 'Download for iPhone' if APP_STORE_URL else 'Coming soon'
AVAILABILITY = 'Built for iPhone' if APP_STORE_URL else 'Coming soon for iPhone'
ARROW = '<span aria-hidden="true">›</span>'
APPSTORE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#1d8cf8"/><path d="M8.1 16.6h7.8M9.6 16.6l3.9-8.9M14.4 16.6l-1.6-3.6M10.3 7.7l.8 1.8" stroke="#fff" stroke-width="1.6" stroke-linecap="round" fill="none"/></svg>'
NAV = [('Features', '#features'), ('How it works', '#how-it-works'), ('Plans', '#pricing'), ('FAQ', '#faq'), ('App screens', '#screens')]

def versioned_asset(name):
    digest = hashlib.sha256((ROOT / 'dist' / name).read_bytes()).hexdigest()[:12]
    return f'/{name}?v={digest}'


def img(name, alt='', cls='', eager=False):
    return (f'<img src="/assets/{escape(name)}" alt="{escape(alt)}" class="{cls}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')


def icon(name, cls='deco'):
    return img(data['icons'][name], '', cls)


def button(label=DOWNLOAD_LABEL, href=DOWNLOAD, cls='solid-button'):
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{escape(label)}{ARROW}</a>'


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

# ── Pricing (real tiers only: Free + COR Pro) ──────────────────────────
free = ['Plan and daily targets', 'Food search, manual logging and recognized barcode lookup',
        'Daily calories, macros and hydration', 'Workout tracking and rest timers',
        'Weight and strength progress', 'Apple Health connection with permission']
pro = ['Everything in Free', 'Meal-photo and text estimates', 'Restaurant menu scanning',
       'Nutrition-label photos and new-product lookup', 'AI coach and weekly coaching', 'AI workouts and workout-photo import']
pro_price = f'<b>${escape(PRO_PRICE)}</b> <span>/month</span>' if PRO_PRICE else '<b class="price-tba">In app</b> <span>at launch</span>'
plans_data = [('Free', '<b>$0</b> <span>/month</span>', 'Your everyday tracking', free, 'Get started' if APP_STORE_URL else 'Coming soon'),
              (f'{BRAND} Pro', pro_price, 'Optional AI tools', pro, 'Explore Pro' if APP_STORE_URL else 'Coming soon')]
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
steps = [('Log your <br>food', 'Search for a food, scan a recognized barcode, or use Pro to estimate a meal from a photo or description.'),
         ('Review the <br>details', 'For photo estimates, add hidden ingredients and portion details. Review and edit the nutrition before saving.'),
         ('Keep your <br>day in view', 'Save your meal to the daily log and see how it contributes to your calorie and macro targets.')]
how_titles = ''.join(f'<h3 class="how-title{" active" if i == 0 else ""}">{t}</h3>' for i, (t, _) in enumerate(steps))
how_descs = ''.join(f'<p class="how-desc{" active" if i == 0 else ""}">{escape(d)}</p>' for i, (_, d) in enumerate(steps))
how_dots = ''.join(f'<button class="how-dot{" active" if i == 0 else ""}" data-step="{i}" aria-label="Step {i + 1}: {escape(t.replace("<br>", " "))}"></button>' for i, (t, _) in enumerate(steps))

# ── Real app screens (in place of template stock-result photography) ──
screens = [
    ('home', 'Daily dashboard', 'Food log, calorie and macro progress, hydration, and your next action.'),
    ('questions', 'Meal photo context', 'Add ingredients the camera may miss, choose a portion, and leave a note.'),
    ('nutrition', 'Review a meal estimate', 'Inspect calories and macros, adjust the entry, then choose whether to log it.'),
    ('ingredients', 'Product ingredients', 'Read the ingredient breakdown and the reasons behind a product grade.'),
    ('strength', 'Strength and training load', 'See recent volume, training sessions, personal records, and trends.'),
    ('weight', 'Weight trend', 'Follow the rolling average, goal range, and longer-term progress.')
]
screen_cards = ''.join(
    f'<article class="result-card"><button class="screen-shot" data-screen="/assets/product/{name}.png" data-title="{title}" aria-label="Enlarge {title.lower()}">{img("product/" + name + ".png", title + " — COR app screen with sample data")}</button><div class="screen-caption"><h3>{escape(title)}</h3><p>{escape(description)}</p></div></article>'
    for name, title, description in screens)

nav_links = ''.join(f'<a class="lens-link" href="{h}">{t}</a>' for t, h in NAV)
hero_copy = data['sections'][0]['texts'][1].replace('CŌR', BRAND)
meal = data['sections'][2]['texts']
ai = data['sections'][5]['texts']
plates = [('CgUIeltv0Dq9CmMfit3NI4VHzY.png', 'Empty plate'), ('0S91gIGvUFBixLMM13HRQUucNwc.png', 'Omelet on plate'),
          ('gm6Geusoczh1lGedoY46WeMIBZs.png', 'Omelet and cheese'), ('RMrVeVtxfeVSJDV0ASPBXMU9U.png', 'Omelet, cheese and grilled chicken')]
plate_html = ''.join(img(a, alt, f'plate-layer plate-{i}') for i, (a, alt) in enumerate(plates))
ingredients = ''.join(f'<span class="ingredient ingredient-{i}">{icon(n)}</span>' for i, n in enumerate(['Omelet', 'Cheese', 'Chicken']))
contact_link = f'<a href="mailto:{escape(SUPPORT_EMAIL, quote=True)}">Contact</a>' if SUPPORT_EMAIL else ''
legal_links = ''.join(f'<a href="{escape(url, quote=True)}">{label}</a>' for label, url in [('Privacy Policy', PRIVACY_URL), ('Terms &amp; Conditions', TERMS_URL)] if url)
footer_info = f'<h3>Legal</h3>{legal_links}' if legal_links else '<h3>Explore</h3><a href="#screens">App screens</a><a href="#faq">Questions</a>'
final_cta = button() if APP_STORE_URL else button('Explore the app', '#features')

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>COR Active</title>
<meta name="description" content="COR Active — coming soon for iPhone and Apple Watch. Explore food logging, nutrition estimates, workout tracking and real screens from COR.">
<link rel="canonical" href="https://coractive.co/">
<meta property="og:url" content="https://coractive.co/">
<meta name="theme-color" content="#030505">
<meta property="og:title" content="COR Active"><meta property="og:description" content="The nutrition and training app that shows its work on every number."><meta property="og:image" content="https://coractive.co/icon-512.png">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="/favicon-64.png" sizes="64x64" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/brand/cor-metal-wordmark.webp" as="image">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="{versioned_asset('style.css')}">
<script>try{{if(sessionStorage.getItem('cor-preloaded'))document.documentElement.classList.add('skip-preloader')}}catch(e){{}}</script>
<script src="{versioned_asset('app.js')}" defer></script></head>
<body>
<div class="preloader" aria-hidden="true"><div class="preloader-mark"><img src="/assets/brand/cor-metal-wordmark.webp" alt=""><span class="preloader-shine"></span></div></div>
<div class="custom-cursor" aria-hidden="true"><span class="cursor-ring"></span><span class="cursor-dot"></span></div>
<a class="skip-link" href="#main">Skip to content</a><div class="ambient" aria-hidden="true"></div>
<nav class="nav-bar" aria-label="Main navigation"><a class="brand" href="#top" aria-label="{BRAND} Active home">{img('brand/cor-nav-wordmark.svg', 'COR', 'nav-wordmark', True)}</a><div class="nav-links lens-bar">{nav_links}<span class="lens" aria-hidden="true"><i></i><i></i><i></i><i></i></span></div>{button(cls='solid-button nav-download')}<button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button><div id="mobile-menu" hidden>{''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}</div></nav>
<main id="main" tabindex="-1">
<section class="hero" id="top"><header class="hero-header"><span class="iphone-badge">{APPSTORE} {AVAILABILITY}</span><h1>The app that<br><mark>shows its work</mark><br>on every number.</h1><p>{escape(hero_copy)}</p>{button(cls='solid-button hero-cta')}</header>
<div class="hero-scene"><div class="hero-sticky"><div class="hero-phone-group">{phone('hero-phone')}
<div class="float-food float-salad">{icon('Salad')}</div><div class="float-food float-ramen">{icon('Ramen')}</div><div class="float-food float-pizza">{icon('Pizza')}</div><div class="float-food float-chocolate">{icon('Chocolate')}</div>
<div class="nutrition-toast toast-carbs"><i>⟋</i><span><b>25g</b>Carbs</span></div><div class="nutrition-toast toast-protein"><i>◎</i><span><b>5g</b>Protein</span></div><div class="nutrition-toast toast-sugar"><i>◈</i><span><b>12g</b>Sugar</span></div><div class="nutrition-toast toast-fat"><i>◐</i><span><b>12g</b>Fats</span></div>
<h2 class="know-heading">Know what<br>you’re eating</h2></div></div></div><p class="demo-note">Animated illustration with sample values. <a href="#screens">See real COR screens</a>.</p></section>
<section class="food-suggestions section" id="food-suggestions"><div class="food-stage"><h2 class="reveal">Make room for<br>the details<br>in every meal.</h2>{food_orbit}<button class="food-help"><span aria-hidden="true">ⓘ</span> Tap or hover to explore</button></div><dialog id="food-guide"><button class="dialog-close" aria-label="Close guide">×</button>{icon('Salad')}<h3>Details make a difference</h3><p>Explore examples of portion and ingredient details you can include when logging a meal. These illustrations are prompts, not personalized food recommendations.</p><p class="touch-help">On a touch screen, tap an icon to explore it.</p></dialog></section>
<section class="meal-section section" id="meal-deconstruct"><header class="section-header reveal"><h2>{escape(meal[0])}</h2><p>{escape(meal[1].replace("CŌR", BRAND))}</p></header><div class="burger-stage">{burger}</div></section>
<section class="how-section section" id="how-it-works"><div class="how-sticky"><div class="how-left">{how_titles}</div>{phone('how-phone')}<div class="how-right">{how_descs}<div class="how-dots">{how_dots}</div><p class="demo-note">Illustrated flow · sample values</p></div></div></section>
<section class="features-section section" id="features">{section_header(4)}<div class="feature-grid">{features}</div><p class="demo-note">Illustrated feature previews. <a href="#screens">Explore the real app screens</a>.</p></section>
<section class="ai-section section" id="ai-meals"><header class="section-header reveal">{img('product/cor-app-icon.png', f'{BRAND} app icon', 'ai-icon')}<h2>{escape(ai[0])}</h2><p>{escape(ai[1])}</p></header><div class="meal-demo"><div class="plate-scene">{plate_html}</div><div class="meal-ingredients">{ingredients}</div><p class="meal-status" role="status"><i class="spinner" aria-hidden="true"></i><span>Estimating nutrition</span></p><div class="meal-total"><span>258 Calories</span><span>32g Protein</span></div><button class="prompt-demo" aria-label="Replay the meal demo"><span class="prompt-text">Estimate this meal: omelet, cheese and chicken</span><span class="prompt-tools"><i>+</i><i>⚙ Tools</i><i class="mic">◖</i><i class="send">↑</i></span></button><p class="demo-note">Illustrated meal estimate · sample values</p></div></section>
<section class="results-section section" id="screens"><header class="section-header reveal"><h2>Real app screens. Sample data.</h2><p>These are native COR captures, not AI-redrawn mockups. Explore food logging, estimate review, product details, strength and weight trends.</p></header><div class="result-cards" role="region" aria-label="COR app screen gallery" tabindex="0">{screen_cards}</div><div class="gallery-controls" role="group" aria-label="App screenshot gallery controls"><button type="button" class="gallery-control" data-gallery-direction="-1" aria-label="Show previous app screenshots">‹</button><button type="button" class="gallery-control" data-gallery-direction="1" aria-label="Show next app screenshots">›</button></div><p class="demo-note">Use the arrow buttons, scroll, or swipe to explore all six screens. Select a screen to open it at full size.</p></section>
<section class="pricing-section section" id="pricing">{section_header(7)}<div class="pricing-grid">{plans}</div><p class="pricing-footnote">COR is coming soon. The app will show the final price and any eligible trial before purchase. AI usage limits may apply.</p></section>
<section class="faq-section section" id="faq">{section_header(8)}<div class="flow-list">{faq}</div></section>
<section class="cta-section section" id="download"><div class="cta-icon reveal">{img('product/cor-app-icon.png', f'{BRAND} app icon', 'app-icon')}{img('vfwd58TDMrxP0cuErxsVbpt2Qs.png', '', 'crown')}</div><span class="iphone-badge">{APPSTORE} {AVAILABILITY}</span><h2>See your plan before you make an account.</h2><p>Answer the setup questions and get your calorie and macro targets, your goal timeline with dated milestones, and a suggested goal based on your setup answers. Sign in when you are ready to keep your plan.</p>{final_cta}</section>
</main>
<dialog id="screen-viewer" aria-labelledby="screen-viewer-title"><button class="screen-close" aria-label="Close app screenshot">×</button><h2 id="screen-viewer-title">COR app screen</h2><p>Real app screen · sample data</p><img alt=""></dialog>
<footer class="footer" id="legal"><div class="footer-top"><div class="footer-about"><p>The nutrition and training app that shows its work.</p></div><div><h3>Product</h3><a href="#top">Home</a><a href="#pricing">Plans</a><a href="{DOWNLOAD}">{DOWNLOAD_LABEL}</a>{contact_link}</div><div><h3>Legal &amp; Privacy</h3><a href="#privacy">Privacy policy</a><a href="#terms">Terms of use</a></div><div>{footer_info}</div></div>
<div class="legal-details"><section id="privacy"><h3>Privacy policy</h3><p>Privacy details for COR are being prepared and will be posted here.</p></section><section id="terms"><h3>Terms of use</h3><p>Terms for using COR are being prepared and will be posted here.</p></section></div>
<div class="copyright">© 2026 COR Active. All rights reserved.</div>
<a class="footer-metal" href="#top" aria-label="Back to top"><video autoplay muted loop playsinline preload="metadata" poster="/assets/brand/cor-liquid-metal-poster.jpg"><source src="/assets/brand/cor-liquid-metal.mp4" type="video/mp4"></video></a></footer>
</body></html>'''
(ROOT / 'dist/index.html').write_text(html)
print('Built COR Active homepage')

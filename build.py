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
BRAND = 'COR'
DEVICE_FRAME = 'brand/iphone-18-pro-max-glacier-apple.png'
IMAGE_VARIANTS = json.loads((ROOT / 'image-variants.json').read_text())
DOWNLOAD = APP_STORE_URL or '#download'
DOWNLOAD_LABEL = 'Download for iPhone' if APP_STORE_URL else 'Coming soon'
AVAILABILITY = 'Built for iPhone' if APP_STORE_URL else 'Coming soon for iPhone'
ARROW = '<span aria-hidden="true">›</span>'
NAV = [('Features', '#features'), ('How it works', '#how-it-works'), ('Plans', '#pricing'), ('FAQ', '#faq'), ('App screens', '#screens')]

def versioned_asset(name):
    digest = hashlib.sha256((ROOT / 'dist' / name).read_bytes()).hexdigest()[:12]
    return f'/{name}?v={digest}'


def asset_url(name):
    return '/assets/' + IMAGE_VARIANTS.get(name, name)


def img(name, alt='', cls='', eager=False):
    return (f'<img src="{escape(asset_url(name))}" alt="{escape(alt)}" class="{cls}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')


def icon(name, cls='deco'):
    return img(data['icons'][name], '', cls)


def button(label=DOWNLOAD_LABEL, href=DOWNLOAD, cls='solid-button'):
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{escape(label)}{ARROW}</a>'


def section_header(index):
    t = data['sections'][index]['texts']
    return (f'<header class="section-header reveal"><h2>{escape(t[0])}</h2>'
            f'<p>{escape(t[1].replace("COR", BRAND))}</p></header>')


# ── Native app captures, using illustrative records ────────────────────
def device_frame(cls='device-bezel', eager=False):
    # Exact, unmodified PNG supplied in Apple's iPhone 18 bezel package.
    return (f'<img src="{asset_url(DEVICE_FRAME)}" class="{cls}" width="1470" height="3000" '
            f'alt="" aria-hidden="true" loading="{"eager" if eager else "lazy"}" decoding="async">')


def phone(cls=''):
    return f'''<div class="phone {cls}"><button type="button" class="screen-shot device-screen-bed how-screen-button" data-screen="{asset_url('product/home.png')}" data-title="Keep your targets in view" aria-label="Enlarge Keep your targets in view app screen">{img('product/home.png', 'COR daily targets screen with illustrative records', 'how-capture')}</button>{device_frame()}</div>'''


def pro_max_hero():
    # Preserve native app content beneath Apple's unmodified device artwork.
    # The composition is illustrative, not a device compatibility test.
    return f'''<div class="hero-phone hero-pro-max" role="img" aria-label="iPhone 18 Pro Max in Glacier showing a captured COR nutrition screen">
  <div class="device-screen-bed" aria-hidden="true">
    <img src="{asset_url("product/nutrition.png")}" width="1000" height="2175" alt="" fetchpriority="high">
  </div>
  {device_frame(eager=True)}
</div>'''


# ── Burger ─────────────────────────────────────────────────────────────
burger_layers = [('HvjQmDxRBTKIbqDxNzJ0cUAK4fU.png', 'Top bun', 'Butter'),
                 ('H8sG3UXknbtlYDaq7sAodIzbnI.png', 'Grilled onion and tomato', 'Sauce'),
                 ('7eX4TRQB9ImxpRvIjFUsm5MYYI.png', 'Patty and cheese', 'Cooked in oil'),
                 ('tMaKfYWjAnAWOIq0SI15iAwub4.png', 'Lettuce', 'Dressing'),
                 ('O4R9JTspTUUYe3YUs6qsV3HZ09k.png', 'Bottom bun', 'Large portion')]
(ROOT / 'burger-layers.json').write_text(json.dumps(burger_layers))
burger = ''.join(
    f'<div class="burger-layer layer-{i}">{img(asset, alt)}'
    f'<span class="ingredient-tag"><span class="tag-thumb" style="background-image:url({asset_url(asset)})"></span>{label}<i></i></span></div>'
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
plans_data = [('Free', '<b>Free to start</b>', 'Your everyday tracking', free, 'See launch status'),
              (f'{BRAND} Pro', '<b>Available in the app</b>', 'Optional AI tools', pro, 'See launch status')]
plans = ''.join(
    f'<article class="pricing-card plan-{i} reveal" style="--d:{i * 90}ms"><div class="price-heading"><h3>{escape(name)}</h3>'
    f'<p class="price">{price}</p><p>{escape(tag)}</p></div>{button(cta, "#waitlist", "solid-button plan-cta")}'
    f'<div class="includes">Includes<ul>' + ''.join(f'<li>{escape(x)}</li>' for x in feats) + '</ul></div></article>'
    for i, (name, price, tag, feats, cta) in enumerate(plans_data))

# ── FAQ (Smooth FAQ Flow style) ────────────────────────────────────────
faq = ''.join(
    f'<div class="flow-item reveal{" open" if i == 0 else ""}" style="--d:{i * 60}ms"><h3><button class="flow-q" aria-expanded="{"true" if i == 0 else "false"}" '
    f'aria-controls="faq-a{i}" id="faq-q{i}"><span>{escape(f["q"].replace("COR", BRAND))}</span><span class="flow-icon" aria-hidden="true"><i></i><i></i></span></button></h3>'
    f'<div class="flow-a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}"><div><p>{escape(f["a"].replace("COR", BRAND))}</p></div></div></div>'
    for i, f in enumerate(data['faq']))

# ── How it works ───────────────────────────────────────────────────────
steps = [('Keep your <br>targets in view', 'See your daily calorie and macro targets alongside the meals you log.'),
         ('Follow your <br>strength', 'Review training volume, session history and personal records as you build your routine.'),
         ('Look at the <br>trend', 'Follow your weight trend and seven-day rolling average, beyond a single day.')]
how_titles = ''.join(f'<h3 class="how-title{" active" if i == 0 else ""}">{t}</h3>' for i, (t, _) in enumerate(steps))
how_descs = ''.join(f'<p class="how-desc{" active" if i == 0 else ""}">{escape(d)}</p>' for i, (_, d) in enumerate(steps))
how_screens = ['home', 'strength', 'weight']
how_dots = ''.join(f'<button class="how-dot{" active" if i == 0 else ""}" data-step="{i}" data-screen="{asset_url("product/" + how_screens[i] + ".png")}" aria-label="Step {i + 1}: {escape(t.replace("<br>", " "))}"></button>' for i, (t, _) in enumerate(steps))

# ── Product showcase: one current app capture at a time ────────────────
showcase_items = [
    ('food', 'Food & meals', 'questions', 'Add the details a photo can miss.',
     'Choose hidden ingredients and a portion size, then review the estimate before saving.'),
    ('training', 'Training', 'strength', 'Train with a clearer picture.',
     'See recent training load, session history, and personal records together.'),
    ('progress', 'Progress', 'weight', 'See change over time.',
     'Follow your rolling average and recent weight trend.')
]
showcase_tabs = ''.join(
    f'<button type="button" class="showcase-tab{" active" if i == 0 else ""}" role="tab" id="showcase-tab-{key}" '
    f'aria-controls="showcase-panel" aria-selected="{"true" if i == 0 else "false"}" tabindex="{"0" if i == 0 else "-1"}" '
    f'data-showcase="{key}" data-screen="{asset_url("product/" + image_name + ".png")}" data-title="{escape(label)}" data-background="">'
    f'<span class="showcase-tab-number">0{i + 1}</span><span class="showcase-tab-title">{escape(label)}</span><span class="showcase-tab-arrow" aria-hidden="true">↗</span>'
    f'<span class="showcase-tab-description">{escape(description)}</span></button>'
    for i, (key, label, image_name, _, description) in enumerate(showcase_items))
showcase_image = img('product/questions.png', 'COR food details screen, shown with illustrative records', 'showcase-screen')

nav_links = ''.join(f'<a class="lens-link" href="{h}">{t}</a>' for t, h in NAV)
hero_copy = data['sections'][0]['texts'][1].replace('COR', BRAND)
meal = data['sections'][2]['texts']
ai = data['sections'][5]['texts']
plates = [('CgUIeltv0Dq9CmMfit3NI4VHzY.png', 'Empty plate'), ('0S91gIGvUFBixLMM13HRQUucNwc.png', 'Omelet on plate'),
          ('gm6Geusoczh1lGedoY46WeMIBZs.png', 'Omelet and cheese'), ('RMrVeVtxfeVSJDV0ASPBXMU9U.png', 'Omelet, cheese and grilled chicken')]
plate_html = ''.join(img(a, alt, f'plate-layer plate-{i}') for i, (a, alt) in enumerate(plates))
ingredients = ''.join(f'<span class="ingredient ingredient-{i}">{icon(n)}</span>' for i, n in enumerate(['Omelet', 'Cheese', 'Chicken']))
legal_links = '<a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a>'
final_cta = button('See launch status', '#waitlist')

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>COR Active – Track the work. See the payoff.</title>
<meta name="description" content="Nutrition and strength, together. Plan your targets, log meals and workouts, and follow your progress. COR Active is coming soon for iPhone.">
<link rel="canonical" href="https://coractive.co/">
<meta property="og:url" content="https://coractive.co/">
<meta name="theme-color" content="#030505">
<meta property="og:type" content="website"><meta property="og:title" content="COR Active – Track the work. See the payoff."><meta property="og:description" content="Nutrition and strength, together. Plan your targets, log meals and workouts, and follow your progress. COR Active is coming soon for iPhone."><meta property="og:image" content="https://coractive.co/assets/brand/cor-og-preview.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="COR nutrition and training app screen with the message Track the work. See the payoff.">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="/favicon-64.png" sizes="64x64" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/brand/cor-metal-wordmark.webp" as="image">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="{versioned_asset('style.css')}">
<script>try{{if(sessionStorage.getItem('cor-preloaded'))document.documentElement.classList.add('skip-preloader')}}catch(e){{}}</script>
<script src="{versioned_asset('app.js')}" defer></script></head>
<body>
<div class="preloader" aria-hidden="true"><div class="preloader-mark"><img src="/assets/brand/cor-metal-wordmark.webp" alt=""><span class="preloader-shine"></span></div></div>
<div class="custom-cursor" aria-hidden="true"><span class="cursor-ring"></span><span class="cursor-dot"></span></div>
<a class="skip-link" href="#main">Skip to content</a><div class="ambient" aria-hidden="true"></div>
<nav class="nav-bar" aria-label="Main navigation"><a class="brand" href="#top" aria-label="{BRAND} home">{img('brand/cor-nav-wordmark.svg', BRAND, 'nav-wordmark', True)}</a><div class="nav-links lens-bar">{nav_links}<span class="lens" aria-hidden="true"><i></i><i></i><i></i><i></i></span></div>{button('Explore the app', '#features', 'solid-button nav-download')}<button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button><div id="mobile-menu" hidden>{''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}</div></nav>
<main id="main" tabindex="-1">
<section class="hero" id="top"><header class="hero-header"><span class="iphone-badge">Coming soon for iPhone</span><h1>Track the work.<br><mark>See the payoff.</mark></h1><p>{escape(hero_copy)}</p>{button('Explore the app', '#features', 'solid-button hero-cta')}</header>
<div class="hero-scene"><div class="hero-sticky"><div class="hero-phone-group">{pro_max_hero()}
</div></div></div><p class="demo-note">iPhone 18 Pro Max in Glacier · captured COR nutrition screen with illustrative records. <a href="#screens">Explore the iPhone screens</a>.</p></section>
<section class="meal-section section" id="meal-deconstruct"><header class="section-header reveal"><h2>{escape(meal[0])}</h2><p>{escape(meal[1].replace("COR", BRAND))}</p></header><div class="burger-stage">{burger}</div></section>
<section class="how-section section" id="how-it-works"><div class="how-sticky"><div class="how-left">{how_titles}</div>{phone('how-phone')}<div class="how-right">{how_descs}<div class="how-dots">{how_dots}</div><p class="demo-note">Captured in COR · illustrative records</p></div></div></section>
<section class="features-section section" id="features"><span id="screens" class="anchor-alias" aria-hidden="true"></span>{section_header(4)}<div class="showcase-layout"><div class="showcase-content"><div class="showcase-tabs" role="tablist" aria-label="Explore COR app screens">{showcase_tabs}</div><p class="showcase-note">App screen details shown with illustrative records. <span>Hover, tap, or use arrow keys to explore.</span></p></div><div class="showcase-stage"><!-- BACKGROUND PHOTO SLOT: set --showcase-background to the supplied image when ready. --><div class="showcase-photo-slot" aria-hidden="true"></div><figure class="showcase-device" id="showcase-panel" role="tabpanel" aria-labelledby="showcase-tab-food"><div class="showcase-phone"><button type="button" class="screen-shot device-screen-bed showcase-capture" data-screen="{asset_url("product/questions.png")}" data-title="Food & meals" aria-label="Enlarge Food and meals app screen">{showcase_image}</button>{device_frame('showcase-bezel')}</div><figcaption><span class="capture-count">01 — 03</span><span>COR for iPhone</span></figcaption></figure></div></div></section>
<section class="ai-section section" id="ai-meals"><header class="section-header reveal">{img('product/cor-app-icon.png', f'{BRAND} app icon', 'ai-icon')}<h2>{escape(ai[0])}</h2><p>{escape(ai[1])}</p></header><div class="meal-demo"><div class="plate-scene">{plate_html}</div><div class="meal-ingredients">{ingredients}</div><p class="meal-status" role="status"><i class="spinner" aria-hidden="true"></i><span>Estimating nutrition</span></p><div class="meal-total"><span>258 Calories</span><span>32g Protein</span></div><button class="prompt-demo" aria-label="Estimate this meal: omelet, cheese and chicken — replay example"><span class="prompt-text">Estimate this meal: omelet, cheese and chicken</span><span class="prompt-tools" aria-hidden="true"><i>+</i><i>⚙ Tools</i><i class="mic">◖</i><i class="send">↑</i></span></button><p class="demo-note">Illustrated meal estimate · sample values</p></div></section>
<section class="pricing-section section" id="pricing">{section_header(7)}<div class="pricing-statement">Free to start. {BRAND} Pro available in the app.</div><div class="pricing-grid">{plans}</div><p class="pricing-footnote">The app will show any subscription details before purchase.</p></section>
<section class="faq-section section" id="faq">{section_header(8)}<div class="flow-list">{faq}</div></section>
<section class="cta-section section" id="download"><div class="cta-icon reveal">{img('product/cor-app-icon.png', f'{BRAND} app icon', 'app-icon')}</div><span class="iphone-badge">Coming soon for iPhone</span><h2>See your plan before you make an account.</h2><p>Answer the setup questions and get your calorie and macro targets, your goal timeline with dated milestones, and a suggested goal based on your setup answers. Sign in when you are ready to keep your plan.</p>{final_cta}</section>
<section class="waitlist-section section" id="waitlist"><header class="section-header"><span class="eyebrow">Launch status</span><h2>Coming soon for iPhone.</h2><p>We’re getting COR ready for launch. Download and signup details will appear here when they’re available.</p></header><!-- BREVO EMBED GOES HERE: replace this launch-status section with the verified Brevo form when signup is ready. No addresses are collected by this page. --></section>
<section class="contact-section section" id="contact"><h2>Questions? Get in touch.</h2><p>For support or launch questions, email <a href="mailto:{escape(SUPPORT_EMAIL)}">{escape(SUPPORT_EMAIL)}</a>.</p></section>
</main>
<dialog id="screen-viewer" aria-labelledby="screen-viewer-title"><button class="screen-close" aria-label="Close app screenshot">×</button><h2 id="screen-viewer-title">COR app screen</h2><p>COR interface · illustrative records</p><img alt=""></dialog>
<footer class="footer" id="legal"><div class="footer-top"><div class="footer-about"><p>The nutrition and training app that shows its work.</p></div><div><h3>Product</h3><a href="#top">Home</a><a href="#pricing">Plans</a><a href="#waitlist">Launch status</a><a href="#contact">Contact</a></div><div><h3>Legal &amp; Privacy</h3>{legal_links}</div></div>
<div class="copyright">© 2026 COR Active. All rights reserved.<br>Apple and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries.</div>
<div class="footer-mark-wrap"><a class="footer-metal" href="#top" aria-label="Back to top"><video muted loop playsinline preload="none" aria-hidden="true" poster="/assets/brand/cor-liquid-metal-poster.jpg"><source src="/assets/brand/cor-liquid-metal.mp4" type="video/mp4"></video></a><button type="button" class="footer-motion-toggle" aria-pressed="false">Pause animation</button></div></footer>
</body></html>'''
(ROOT / 'dist/index.html').write_text(html)

def legal_page(title, slug, description, body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | COR Active</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="https://coractive.co/{slug}/">
<meta name="theme-color" content="#000000"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/style.css"></head>
<body><a class="skip-link" href="#legal-main">Skip to content</a><main id="legal-main" class="legal-document" tabindex="-1">
<header><a href="/" class="legal-top-link">← Back to COR Active</a><p><span class="draft-banner">DRAFT — FOR REVIEW</span></p><h1>{escape(title)}</h1><p class="last-updated">Last updated: November 1, 2026</p></header>
<article>{body}<p class="legal-top-link"><a href="mailto:{escape(SUPPORT_EMAIL, quote=True)}">Questions? Contact {escape(SUPPORT_EMAIL)}</a></p><a class="legal-top-link" href="/">Return to COR Active</a></article>
</main></body></html>'''

privacy_body = '''
<p><strong>Draft for review:</strong> This page describes the intended practices supplied for COR. Confirm the bracketed operational details and have the final policy reviewed before making it public.</p>
<h2>Who this policy covers</h2><p>This policy covers the COR iPhone and Apple Watch apps, the COR Active website, and the launch waitlist. “COR,” “we,” and “our” refer to COR Active. For privacy questions, contact <a href="mailto:support@coractive.co">support@coractive.co</a>.</p>
<h2>Information you provide</h2><ul><li>Account details supplied through Sign in with Apple or Google, such as an account identifier, name, or email address, handled through Supabase.</li><li>Profile and app information you choose to enter, including goals, meals, nutrition, workouts, weight, measurements, and feedback.</li><li>Health information you choose to connect through Apple Health, subject to the permissions you grant. Supported information may include steps, workouts, heart rate, sleep, weight, body fat, and meal calories or macros. You can manage access in Apple Health and iOS settings.</li><li>Photos, descriptions, and other content you submit when you choose an AI feature. A feature may send the content needed for that request to its AI service provider.</li><li>If you join the launch waitlist, your email address and subscription or confirmation status, handled through Brevo.</li></ul>
<h2>How information is used</h2><p>We use information to operate and personalize COR, sync your account, show the health and fitness features you request, answer support messages, process an AI request you choose to make, and send waitlist or launch updates you signed up to receive.</p>
<h2>Apple Health information</h2><p>HealthKit access is permission-based. You can grant or deny supported read and write permissions separately. We use health information to provide COR health and fitness functionality. We do not sell health data and do not use it for advertising. Health data is not used to target ads. Information already written to Apple Health may remain there after you delete your COR account; manage or remove those records in Apple Health.</p>
<h2>Optional AI features</h2><p>AI features are optional. When you choose one, COR may send the text, image, or other information shown in that feature to an AI provider so it can return an estimate or response. Review the in-app notice before sending. <strong>[Before publication, list the active AI providers, the types of inputs each receives, and their retention or model-training terms.]</strong></p>
<h2>Service providers and sharing</h2><p>We use service providers to operate the product: Supabase for authentication and app services, Apple and Google for sign-in, Apple HealthKit when you connect it, Brevo for waitlist email, and AI providers only when you choose an AI feature. We do not sell personal or health information and do not use health data for advertising. We may disclose information if required by law or to protect the service and its users.</p>
<h2>How long we keep information</h2><p>We keep account information while your account is active and for the time needed to provide the service, meet legal obligations, resolve disputes, and protect the service. Waitlist information is kept until you unsubscribe or ask us to remove it. <strong>[Confirm the actual retention period for backups, support messages, and provider logs before publication.]</strong></p>
<h2>Your choices and deletion</h2><ul><li>Change Apple Health permissions in Apple Health or iOS Settings.</li><li>Delete your COR account in the app’s Settings under “Delete Account.” Account deletion removes the account and associated COR data from active systems; <strong>[confirm backup deletion timing and any records that must be retained]</strong>.</li><li>Use the unsubscribe link in a Brevo email to stop waitlist messages, or email <a href="mailto:support@coractive.co">support@coractive.co</a> to request removal.</li><li>Contact us to ask about access, correction, or deletion of information.</li></ul>
<h2>Security and children</h2><p>We use technical and organizational safeguards designed to protect information. No online service can guarantee absolute security. COR is not designed for children under 13, and we do not knowingly ask children under 13 to create an account.</p>
<h2>Changes to this policy</h2><p>We may update this policy as COR changes. We will update the date above and provide additional notice when required.</p>
'''

terms_body = '''
<p><strong>Draft for review:</strong> This draft describes the intended COR service. Confirm the bracketed company and jurisdiction details and review the final terms before publication.</p>
<h2>About COR</h2><p>COR is a nutrition and fitness app from COR Active. It offers food logging, nutrition information, workout tracking, progress tools, Apple Health connections, and optional AI-assisted features. The app is coming soon.</p>
<h2>Accounts</h2><p>You may create an account using Sign in with Apple or Google. Keep your sign-in details secure and provide accurate information. You can delete your account through Settings in the app. Account deletion removes your COR account and associated data from active systems, subject to the retention details in the Privacy Policy.</p>
<h2>Health and fitness information</h2><p>COR is for general wellness and fitness information. Calorie, nutrition, body-fat, workout, and AI-generated values may be estimates and can be incomplete or inaccurate. They are not medical advice, diagnosis, or treatment, and should not replace advice from a qualified health professional. Use your judgment and stop any activity that feels unsafe.</p>
<h2>Apple Health and connected services</h2><p>Apple Health access is optional and controlled by permissions on your device. You are responsible for reviewing those permissions and any third-party service terms that apply to services you choose to connect.</p>
<h2>Optional AI features</h2><p>AI-assisted features are optional and may produce inaccurate or incomplete results. You are responsible for reviewing an estimate or response before relying on it or saving it. When you choose an AI feature, the information shown in that feature may be sent to a service provider to generate a result.</p>
<h2>Subscriptions and payments</h2><p>COR is free to start, with COR Pro available in the app. Any price, trial, renewal period, and cancellation terms will be shown before you confirm a purchase. App Store subscriptions are managed through your Apple account. <strong>[Confirm subscription terms and any trial details before launch.]</strong></p>
<h2>Acceptable use</h2><p>Do not misuse COR, interfere with its operation, attempt unauthorized access, or use it unlawfully. Do not submit content you do not have the right to use or that violates another person’s rights.</p>
<h2>Service availability and changes</h2><p>We may update, suspend, or discontinue features to maintain or improve the service, comply with law, or address safety or security concerns. We will provide notice where required.</p>
<h2>Intellectual property</h2><p>COR Active owns or licenses COR, its software, branding, and content. These terms give you a personal, limited, non-transferable right to use the app for its intended purpose. You keep ownership of content you submit, and authorize us to process it only as needed to provide the features you choose.</p>
<h2>Disclaimers and liability</h2><p>To the extent permitted by law, COR is provided as available and without guarantees that every result will be accurate, uninterrupted, or suitable for your needs. Nothing in these terms removes rights that cannot legally be limited. <strong>[Have counsel complete jurisdiction-specific warranty and liability language.]</strong></p>
<h2>Governing law and contact</h2><p><strong>[Confirm the contracting legal entity and governing-law jurisdiction before publication.]</strong> For questions, contact <a href="mailto:support@coractive.co">support@coractive.co</a>.</p>
'''

for slug, title, description, body in [
    ('privacy', 'Privacy Policy', 'Draft privacy policy for COR Active, the COR Active health and fitness app.', privacy_body),
    ('terms', 'Terms of Use', 'Draft terms for using the COR Active health and fitness app.', terms_body)
]:
    target = ROOT / 'dist' / slug
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(legal_page(title, slug, description, body))

not_found = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | COR Active</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/style.css"></head><body><main class="not-found"><h1>Page not found.</h1><p>That address doesn’t lead to a COR page. Head back to the site and keep going.</p><a class="solid-button" href="/">Back to COR Active</a></main></body></html>'''
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
<meta name="theme-color" content="#000000"><link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="stylesheet" href="{versioned_asset('fonts.css')}"><link rel="stylesheet" href="{versioned_asset('style.css')}"></head>
<body class="waitlist-result"><a class="skip-link" href="#main">Skip to content</a>
<header class="waitlist-result-header"><a href="/" aria-label="COR Active home">{img('brand/cor-nav-wordmark.svg', 'COR Active')}</a></header>
<main id="main" class="waitlist-result-main" tabindex="-1">
<svg class="waitlist-result-icon" viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{symbol}</svg>
<p class="waitlist-result-eyebrow">COR Active · Launch waitlist</p><h1>{escape(heading)}</h1>
<p class="waitlist-result-message">{escape(message)}</p><p class="waitlist-result-detail">{detail}</p>
<a class="solid-button" href="/#features">Explore COR {ARROW}</a>
<p class="waitlist-result-help">Need a hand? <a href="mailto:{escape(SUPPORT_EMAIL, quote=True)}">{escape(SUPPORT_EMAIL)}</a></p>
</main><footer class="waitlist-result-footer"><a href="/privacy/">Privacy policy</a><span>© 2026 COR Active</span></footer>
</body></html>'''

for slug, title, heading, message, detail, confirmed in [
    ('check-email', 'Confirm your email', 'One more step.',
     'Check your inbox for an email from COR Active. Follow the confirmation link to join the waitlist.',
     'No email yet? Check your spam folder. If you entered the wrong address, <a href="/#waitlist">try again</a>.', False),
    ('confirmed', 'Welcome to the waitlist', 'You’re on the list.',
     'Thanks for confirming your email. We’ll send you early access news and let you know when COR launches.',
     'You can unsubscribe at any time using the link in our emails.', True)
]:
    target = ROOT / 'dist' / 'waitlist' / slug
    target.mkdir(parents=True, exist_ok=True)
    (target / 'index.html').write_text(waitlist_status_page(title, heading, message, detail, confirmed))

print('Built COR Active homepage, draft legal pages, waitlist confirmation pages, and SEO files')

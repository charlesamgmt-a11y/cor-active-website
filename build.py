"""Build the COR preview from verified copy and unchanged native app captures."""
from pathlib import Path
import json
import hashlib
from html import escape

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'reference-data.json').read_text())
site = data['website']
BRAND = 'COR'
SUPPORT_EMAIL = 'support@coractive.co'
DEVICE_FRAME = 'brand/iphone-18-pro-max-glacier-apple.png'
IMAGE_VARIANTS = json.loads((ROOT / 'image-variants.json').read_text())
ARROW = '<span aria-hidden="true">↗</span>'
NAV = [('Nutrition', '#nutrition'), ('Strength', '#strength'), ('The week', '#weekly-review'), ('App screens', '#screens')]

def versioned_asset(name):
    digest = hashlib.sha256((ROOT / 'dist' / name).read_bytes()).hexdigest()[:12]
    return f'/{name}?v={digest}'

def asset_url(name):
    return '/assets/' + IMAGE_VARIANTS.get(name, name)

def img(name, alt='', cls='', eager=False):
    return (f'<img src="{escape(asset_url(name))}" alt="{escape(alt)}" class="{cls}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async">')

def button(label='See launch status', href='#waitlist', cls='solid-button'):
    return f'<a class="{cls}" href="{escape(href, quote=True)}">{escape(label)}{ARROW}</a>'

def device(screen, label, cls='', eager=False):
    source = asset_url('product/' + screen + '.png')
    return f'''<div class="device {cls}"><button type="button" class="screen-shot device-screen-bed" data-screen="{source}" data-title="{escape(label)}" aria-label="Enlarge {escape(label)} app screen"><img src="{source}" alt="COR {escape(label)} screen with illustrative records" loading="{'eager' if eager else 'lazy'}" decoding="async" {'fetchpriority="high"' if eager else ''}></button><img class="device-bezel" src="{asset_url(DEVICE_FRAME)}" width="1470" height="3000" alt="" aria-hidden="true" loading="{'eager' if eager else 'lazy'}" decoding="async"></div>'''

hero = site['hero']
nav_links = ''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)
pillars = ''.join(f'''<article class="pillar" id="{p['id']}"><p class="eyebrow">{escape(p['label'])}</p><h3>{escape(p['title'])}</h3><p class="pillar-copy">{escape(p['copy'])}</p><div class="pillar-device-wrap">{device(p['screen'],p['screen_label'],'pillar-device')}</div><ul>{''.join(f'<li>{escape(x)}</li>' for x in p['points'])}</ul><a class="text-link" href="#screens">Explore {p['id']} in COR <span aria-hidden="true">↗</span></a></article>''' for p in site['pillars'])
journey = ''.join(f'<li><span class="step-number">0{i+1}</span><h3>{escape(j["title"])}</h3><p>{escape(j["copy"])}</p></li>' for i,j in enumerate(site['journey']))
tabs = ''.join(f'''<button class="showcase-tab{' active' if i==0 else ''}" type="button" role="tab" id="screen-tab-{s['key']}" aria-controls="showcase-panel" aria-selected="{'true' if i==0 else 'false'}" tabindex="{'0' if i==0 else '-1'}" data-screen="{asset_url('product/'+s['image']+'.png')}" data-title="{escape(s['title'])}"><span class="tab-number">0{i+1}</span><span><span class="tab-title">{escape(s['title'])}</span><span class="tab-description">{escape(s['copy'])}</span></span><span aria-hidden="true">↗</span></button>''' for i,s in enumerate(site['screens']))
ecosystem = ''.join(f'<article><span class="ecosystem-index" aria-hidden="true">0{i+1}</span><h3>{escape(e["title"])}</h3><p>{escape(e["copy"])}</p></article>' for i,e in enumerate(site['ecosystem']))
plans = ''.join(f'''<article class="pricing-card"><span class="eyebrow">{'Everyday essentials' if i==0 else 'Optional AI tools'}</span><h3>{escape(p['name'])}</h3><p class="price">{'Free to start' if i==0 else 'In app at launch'}</p><ul>{''.join(f'<li>{escape(x)}</li>' for x in p['features'])}</ul>{button()}</article>''' for i,p in enumerate(data['plans']))
faq = ''.join(f'<details class="faq-item"><summary>{escape(f["q"])}</summary><p>{escape(f["a"])}</p></details>' for f in data['faq'] if f['q'] in ['When can I download COR?','Do I need an account to see my plan?','What can I use without COR Pro?','Are meal-photo calories exact?','Does COR work with Apple Health and Apple Watch?','What happens when I use an AI feature?'])
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(site['title'])}</title><meta name="description" content="{escape(site['description'])}">
<link rel="canonical" href="https://coractive.co/"><meta name="theme-color" content="#050706">
<meta property="og:url" content="https://coractive.co/"><meta property="og:type" content="website"><meta property="og:title" content="{escape(site['title'])}"><meta property="og:description" content="{escape(site['description'])}"><meta property="og:image" content="https://coractive.co/assets/brand/cor-og-preview.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="COR nutrition and training app with an authentic daily view capture">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="/favicon-64.png" sizes="64x64" type="image/png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="{versioned_asset('style.css')}"><script src="{versioned_asset('app.js')}" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<nav class="nav-bar" aria-label="Main navigation"><a class="brand" href="#top" aria-label="COR home">{img('brand/cor-nav-wordmark.svg','COR','nav-wordmark',True)}</a><div class="nav-links">{nav_links}</div>{button('Coming soon','#waitlist','solid-button nav-cta')}<button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button><div id="mobile-menu" hidden>{nav_links}<a href="#pricing">Free &amp; Pro</a><a href="#waitlist">Launch status</a></div></nav>
<main id="main" tabindex="-1">
<section class="hero section" id="top"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span>{escape(hero['eyebrow'])}</p><h1>{escape(hero['title'])}<br><em>{escape(hero['emphasis'])}</em></h1><p class="hero-description">{escape(hero['copy'])}</p><div class="hero-actions">{button('Explore COR','#features')}<a class="text-link" href="#waitlist">Coming soon for iPhone</a></div><div class="hero-footnote"><span>Plan.</span><span>Fuel.</span><span>Train.</span><span>Review.</span></div></div><div class="hero-product"><div class="hero-device-pair"><figure>{device('home','daily view','hero-device',True)}<figcaption>Daily nutrition</figcaption></figure><figure>{device('strength','strength progression','hero-device',True)}<figcaption>Strength progression</figcaption></figure></div><p class="capture-note">Real COR screens · illustrative records</p></div></section>
<section class="pillars-section section" id="features"><div class="section-heading"><p class="eyebrow">The same commitment. Both sides.</p><h2>What you eat.<br>What you lift.</h2><p>Nutrition and strength deserve the same attention. Your progress connects the two.</p></div><div class="pillars-grid">{pillars}</div></section>
<section class="journey-section section" id="how-it-works"><div class="section-heading horizontal"><div><p class="eyebrow">A rhythm you can return to</p><h2>From a plan<br>to a pattern.</h2></div><p>Start with a direction. Build the record one day and one session at a time.</p></div><ol class="journey-grid">{journey}</ol></section>
<section class="screens-section section" id="screens"><div class="showcase-layout"><div class="showcase-content"><p class="eyebrow">Inside COR</p><h2>Your work,<br>in the picture.</h2><p class="section-intro">Actual screens from the iPhone app. Explore the details, then tap a screen to take a closer look.</p><div class="showcase-tabs" role="tablist" aria-label="Explore COR app screens" aria-orientation="vertical">{tabs}</div><p class="capture-note">Screens use illustrative records, not customer results.</p></div><figure class="showcase-stage" id="showcase-panel" role="tabpanel" aria-labelledby="screen-tab-daily">{device('home','Your daily view','showcase-device')}<figcaption><span class="capture-count">01 / 04</span><span class="capture-title">Your daily view</span></figcaption></figure></div></section>
<section class="weekly-section section" id="weekly-review"><div class="weekly-copy"><p class="eyebrow">The connected week</p><h2>{escape(site['weekly']['title']).replace(chr(10),'<br>')}</h2><p>{escape(site['weekly']['copy'])}</p><p class="weekly-caveat">Coaching is guidance, not a diagnosis or a guarantee of results.</p><a class="text-link" href="#pricing">Explore COR Pro <span aria-hidden="true">↗</span></a></div><div class="weekly-story" aria-label="How nutrition, training and progress connect"><p class="eyebrow">Look back. Keep the context.</p><ol><li><span>01</span><div><h3>Nutrition</h3><p>The meals and targets behind your days.</p></div></li><li><span>02</span><div><h3>Training</h3><p>The sessions behind your strength.</p></div></li><li><span>03</span><div><h3>Progress</h3><p>The trends that take more than a day.</p></div></li></ol><div class="weekly-summary"><span aria-hidden="true">↳</span><p>A fuller picture<br><strong>for your next week.</strong></p></div><p class="capture-note">A guide to the COR workflow, not an app screen.</p></div></section>
<section class="ecosystem-section section" id="apple"><div class="section-heading horizontal"><div><p class="eyebrow">On the devices you use</p><h2>Part of your<br>Apple routine.</h2></div><p>Keep the context close, with supported health connections and a companion for your wrist.</p></div><div class="ecosystem-grid">{ecosystem}</div><p class="capture-note">Apple Health access is optional. Available data depends on your permissions and supported devices.</p></section>
<section class="pricing-section section" id="pricing"><div class="section-heading"><p class="eyebrow">Free &amp; COR Pro</p><h2>A strong foundation.<br>Extra help, when you want it.</h2><p>Everyday tracking comes first. COR Pro adds selected AI-assisted tools you choose to use.</p></div><div class="pricing-grid">{plans}</div><p class="capture-note">Final pricing, subscription terms and any eligible trial will be shown in the app before purchase.</p></section>
<section class="faq-section section" id="faq"><div class="section-heading"><p class="eyebrow">Before you begin</p><h2>A little more clarity.</h2></div><div class="faq-list">{faq}</div></section>
<section class="launch-section section" id="waitlist"><span id="download" class="anchor-alias"></span><p class="eyebrow"><span class="status-dot"></span>Launch status</p><h2>Your next chapter.<br><em>Coming soon.</em></h2><p>COR is getting ready for iPhone, with a companion Apple Watch app. Download and signup details will appear here when they’re available.</p><p class="launch-note">No signup is open on this preview.</p><a class="text-link" href="mailto:{SUPPORT_EMAIL}">Questions? {SUPPORT_EMAIL} <span aria-hidden="true">↗</span></a><!-- Replace only with the verified Brevo form when signup is ready. --></section>
</main>
<dialog id="screen-viewer" aria-labelledby="screen-viewer-title"><button class="screen-close" aria-label="Close app screenshot">×</button><h2 id="screen-viewer-title">COR app screen</h2><p>Original app capture · illustrative records</p><img alt=""></dialog>
<footer class="footer" id="legal"><div class="footer-top"><p>Nutrition and strength.<br><span>One direction.</span></p><div><a href="#screens">The app</a><a href="#pricing">Free &amp; Pro</a><a href="#faq">FAQ</a><a href="mailto:{SUPPORT_EMAIL}">Contact</a></div><div><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a></div></div><div class="footer-mark-wrap"><a class="footer-metal" href="#top" aria-label="Back to top"><video muted loop playsinline preload="none" aria-hidden="true" poster="/assets/brand/cor-liquid-metal-poster.jpg"><source src="/assets/brand/cor-liquid-metal.mp4" type="video/mp4"></video></a><button type="button" class="footer-motion-toggle" aria-pressed="false">Pause animation</button></div><div class="copyright"><span>© 2026 COR Active. All rights reserved.</span><span>Apple and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries.</span></div></footer>
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

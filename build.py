"""Build the standalone homepage from content inspected in the user's Framer project."""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).parent
data = json.loads((ROOT / 'reference-data.json').read_text())
SOURCE = 'https://goodness-zebra-710061.framer.app'
ARROW = '<span aria-hidden="true">›</span>'
APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.1 12.3c0-2.4 2-3.6 2.1-3.7-1.2-1.7-3-1.9-3.6-1.9-1.5-.2-3 .9-3.8.9-.8 0-2-1-3.3-.9-1.7 0-3.2 1-4.1 2.5-1.8 3.1-.5 7.7 1.2 10.2.8 1.2 1.8 2.5 3.1 2.4 1.2 0 1.7-.8 3.3-.8s2 .8 3.3.8c1.4 0 2.2-1.2 3-2.4 1-1.4 1.4-2.8 1.4-2.8-.1 0-2.6-1-2.6-4.3M14.7 5.1c.7-.9 1.2-2.1 1.1-3.3-1 .1-2.3.7-3.1 1.6-.7.8-1.3 2-1.2 3.2 1.2.1 2.4-.6 3.2-1.5"/></svg>'
def img(name, alt='', cls='', eager=False):
    return f'<img src="/assets/{escape(name)}" alt="{escape(alt)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'
def icon(name, cls=''):
    return img(data['icons'][name],name,cls)
def button(label='Download for iPhone', href=SOURCE+'/download', cls=''):
    return f'<a class="glass-button {cls}" href="{href}">{escape(label)}{ARROW}</a>'
def section_header(index):
    t=data['sections'][index]['texts']
    return f'<header class="section-header reveal"><h2>{escape(t[0])}</h2><p>{escape(t[1])}</p></header>'
def phone(cls='', result=False):
    return f'''<div class="phone {cls}">
      <div class="phone-screen">
        {img('JAkAjO3nzzlBXQIicczRvbDEEng.png','Nutella biscuits being scanned','camera-photo',True)}
        <div class="phone-top"><span>‹</span><strong>Scan food</strong><span>···</span></div>
        <div class="scan-frame"><i></i><i></i><i></i><i></i><div class="scan-line"></div></div>
        <div class="phone-camera"><span>◧</span><button class="shutter" aria-label="Preview food scan"></button><span>↻</span></div>
        <div class="analysis-sheet"><small>515 Calories</small><h3>Nutella Biscuits</h3><div class="nutrients"><div><b>5g</b><span>Protein</span></div><div><b>25g</b><span>Carbs</span></div><div><b>12g</b><span>Fats</span></div></div><div class="scan-goal"><b>Goal</b><span>1,415 / 2000 kcal</span><i></i><p>Adding it leaves you with 585 calories for the day</p></div><button class="phone-log">Add to log <span>＋</span></button></div>
      </div>
      {img('EYwE63Pj2EhNh6QWM26TBWhXD8Q.png','Orange iPhone frame','phone-hardware',True)}
    </div>'''

food_names=['Salad','Meat','Ramen','Chocolate','Pizza','Sandwhich','Salmon']
food_orbit=''.join(f'<button class="food-orbit food-{i}" aria-label="Explore {escape(name)}" aria-pressed="false" data-recommendation="{"yes" if name in ["Salad","Meat","Sandwhich","Salmon"] else "no"}">{icon(name)}<span class="food-verdict">{"✓" if name in ["Salad","Meat","Sandwhich","Salmon"] else "×"}</span></button>' for i,name in enumerate(food_names))
burger_layers=[('HvjQmDxRBTKIbqDxNzJ0cUAK4fU.png','Top bun','Butter'),('H8sG3UXknbtlYDaq7sAodIzbnI.png','Tomato and onion','Sauce'),('7eX4TRQB9ImxpRvIjFUsm5MYYI.png','Patty and cheese','Cheese'),('tMaKfYWjAnAWOIq0SI15iAwub4.png','Lettuce','Dressing'),('O4R9JTspTUUYe3YUs6qsV3HZ09k.png','Bottom bun','Large portion')]
(ROOT/'burger-layers.json').write_text(json.dumps(burger_layers))
burger=''.join(f'<div class="burger-layer layer-{i}">{img(asset,alt)}<span class="ingredient-tag">{label}<i></i></span></div>' for i,(asset,alt,label) in enumerate(burger_layers))

graphics=[
 '<div class="calorie-widget"><div><span>Calorie Intake</span><small>585 Kcal 🥑</small></div><p><b>1,415</b> <em>/ 2000</em></p></div><div class="week">'+''.join(f'<span class="{"selected" if day=="Wed" else ""}"><small>{day}</small>{i+11}</span>' for i,day in enumerate(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']))+'</div>',
 '<div class="food-plan"><div><b>Monday<br><span>6 Items</span></b><small>1,756 Kcal</small></div><div class="mini-foods">'+''.join(icon(n) for n in ['Salad','Meat','Sandwhich','Salmon'])+'<span>+2</span></div></div><div class="food-plan plan-ghost"><b>Tuesday</b><span>1,544 Kcal</span></div>',
 '<div class="search-widget"><b>Search food items</b><div>Search foods <span>⌕</span></div><b>Recent searches</b><p>'+icon('Salad')+'<span>Lettuce Tomato Salad<br><small>200 Kcal</small></span><i>＋</i></p><p>'+icon('Meat')+'<span>Grilled steak<br><small>280 Kcal</small></span></p></div>',
 '<div class="barcode-widget"><div class="barcode"></div><i></i><i></i><i></i><i></i><div class="barcode-light"></div></div>'
]
features=''.join(f'<article class="feature-card reveal"><div class="feature-graphic graphic-{i}">{graphics[i]}</div><div class="feature-copy"><h3>{escape(f["title"])}</h3><p>{escape(f["description"])}</p></div></article>' for i,f in enumerate(data['features']))
plans=''.join(f'<article class="pricing-card plan-{i} reveal"><div class="price-heading"><h3>{escape(p["name"])}</h3><p class="price"><b>${p["price"]}</b> <span>/month</span></p><p>{escape(p["tagline"])}</p></div>{button("Try now")}<div class="includes">Includes<ul>'+''.join(f'<li>{escape(f)}</li>' for f in p['features'])+'</ul></div></article>' for i,p in enumerate(data['plans']))
faq=''.join(f'<details class="faq-item"><summary>{escape(f["q"])}<span aria-hidden="true">+</span></summary><p>{escape(f["a"])}</p></details>' for f in data['faq'])
steps=['Scan your food','Get Nutritional Insights','Make Your Action']
step_descriptions=['Point your camera or scan a barcode the app instantly recognizes your meal with AI-powered accuracy.','See exactly what’s on your plate, calories, macros, and key nutrients, all broken down in seconds.','Log it, tweak your plan, or ask AI for smarter alternatives all in one tap.']

html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CŌR — The app that shows its work</title><meta name="description" content="A recreation of the CŌR nutrition and training homepage. Explore food tracking, nutritional insights, and the numbers behind your progress."><meta name="theme-color" content="#030505"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><div class="ambient" aria-hidden="true"></div>
<nav class="nav-bar" aria-label="Main navigation"><a class="brand" href="#top" aria-label="CŌR home"><span class="brand-star">✱</span><span>CŌR</span></a><div class="nav-links"><a href="#pricing">Pricing</a><a href="{SOURCE}/legal">Legal</a></div>{button(cls='nav-download')}<button class="menu-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button><div id="mobile-menu" hidden><a href="#pricing">Pricing</a><a href="{SOURCE}/legal">Legal</a><a href="{SOURCE}/download">Download for iPhone</a></div></nav>
<main id="main">
<section class="hero" id="top"><header class="hero-header"><span class="iphone-badge">{APPLE} Built for iPhone</span><h1>The app that<br><mark>shows its work</mark><br>on every number.</h1>{button('Get started', '#how-it-works','hero-start')}<p>{escape(data['sections'][0]['texts'][1])}</p>{button()}</header>
<div class="hero-scene"><div class="hero-sticky"><div class="hero-phone-group">{phone('hero-phone')}
<div class="float-food float-salad">{icon('Salad')}</div><div class="float-food float-ramen">{icon('Ramen')}</div><div class="float-food float-pizza">{icon('Pizza')}</div><div class="float-food float-chocolate">{icon('Chocolate')}</div>
<div class="nutrition-toast toast-protein"><i>◉</i><span><b>5g</b>Protein</span></div><div class="nutrition-toast toast-carbs"><i>◒</i><span><b>25g</b>Carbs</span></div><div class="nutrition-toast toast-sugar"><i>◈</i><span><b>36g</b>Sugar</span></div><div class="nutrition-toast toast-fat"><i>◐</i><span><b>12g</b>Fats</span></div>
<h2 class="know-heading">Know what<br>you’re eating</h2></div></div></div></section>
<section class="food-suggestions section" id="food-suggestions"><div class="food-stage"><h2>Helps you find<br>what you should<br>eat.</h2>{food_orbit}<button class="food-help">Hover over these icons <span>ⓘ</span></button></div><dialog id="food-guide"><button class="dialog-close" aria-label="Close guide">×</button>{icon('Salad')}<h3>Hover over the elements</h3><p>The 3D food icons are interactable and hovering over them shows which food you should probably eat. That’s what the app will do for you.</p><p class="touch-help">On a touch screen, tap an icon to explore it.</p></dialog></section>
<section class="meal-section section" id="meal-deconstruct">{section_header(2)}<div class="burger-stage">{burger}</div></section>
<section class="how-section section" id="how-it-works"><div class="how-sticky"><div class="steps" aria-label="Explore how CŌR works">{''.join(f'<button class="step {"active" if i==0 else ""}" data-step="{i}" aria-pressed="{"true" if i==0 else "false"}"><span class="step-number">0{i+1}</span><span>{label}</span></button>' for i,label in enumerate(steps))}</div>{phone('how-phone')}<div class="step-descriptions">{''.join(f'<p class="step-description {"active" if i==0 else ""}" data-description="{i}">{escape(t)}</p>' for i,t in enumerate(step_descriptions))}<span class="step-progress"><i></i><i></i><i></i></span></div></div></section>
<section class="features-section section" id="features">{section_header(4)}<div class="feature-grid">{features}</div></section>
<section class="ai-section section" id="ai-meals">{section_header(5)}<div class="meal-demo"><div class="plate-scene">{''.join(img(asset,alt,f'plate-layer plate-{i}') for i,(asset,alt) in enumerate([('CgUIeltv0Dq9CmMfit3NI4VHzY.png','Empty plate'),('0S91gIGvUFBixLMM13HRQUucNwc.png','Omelet on plate'),('gm6Geusoczh1lGedoY46WeMIBZs.png','Omelet and cheese'),('RMrVeVtxfeVSJDV0ASPBXMU9U.png','Omelet, cheese, and grilled chicken')]))}</div><div class="meal-ingredients">{''.join(f'<span class="ingredient ingredient-{i}">{icon(n)}</span>' for i,n in enumerate(['Omelet','Cheese','Chicken']))}</div><p class="meal-status" role="status">Working it out<span class="thinking-dots">...</span></p><div class="meal-total"><span>258 Calories</span><span>32g Protein</span></div><button class="prompt-demo" aria-label="Replay the meal preparation demo"><span>✧</span><span>Make me a 30g protein dish under 300Kcal</span><span>↑</span></button></div></section>
<section class="results-section section" id="results">{section_header(6)}<div class="result-cards">{''.join(f'<figure class="result-card result-{i}">{img(asset,"Transformation story image from the reference")}</figure>' for i,asset in enumerate(['dth8hQXMbZ5riHrgo1mlMevouY.png','8GHJgMhqFeSkg6T8hKLQeW9ojg.png','fzzIg5LTVKzW5Tjl6HmSiZhO2LE.png']))}</div><a class="text-link" href="{SOURCE}/stories">See stories {ARROW}</a></section>
<section class="pricing-section section" id="pricing">{section_header(7)}<div class="pricing-grid">{plans}</div></section>
<section class="faq-section section" id="faq">{section_header(8)}<div class="faq-list">{faq}</div></section>
<section class="cta-section section" id="download">{img('vfwd58TDMrxP0cuErxsVbpt2Qs.png','CŌR app icon','app-icon')}<span class="iphone-badge">{APPLE} Built for iPhone</span><h2>See your plan before<br>you make an account.</h2><p>Answer the setup questions and get your calorie and macro targets, your goal timeline with dated milestones, and the goal that actually fits your body composition. Sign in only if you want to keep it.</p>{button()}</section>
</main><footer class="footer"><div class="footer-top"><a class="brand footer-brand" href="#top"><span class="brand-star">✱</span>CŌR</a><p>The nutrition and training app<br>that shows its work.</p><div><h3>Product</h3><a href="#top">Home</a><a href="#pricing">Pricing</a><a href="{SOURCE}/download">Download</a><a href="{SOURCE}/contact">Contact</a></div><div><h3>Legal</h3><a href="{SOURCE}/legal">Legal</a><a href="{SOURCE}/privacy-policy">Privacy Policy</a><a href="{SOURCE}/terms-and-conditions">Terms &amp; Conditions</a></div></div><a class="footer-wordmark" href="#top" aria-label="Back to top">CŌR</a><div class="copyright">© 2026 CŌR. All rights reserved.</div></footer>
</body></html>'''
(ROOT/'dist/index.html').write_text(html)
print('Built homepage with 10 sections, 4 feature cards, 3 plans, and 5 FAQs.')

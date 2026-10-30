# COR product website

The original site's dark blue, ivory, Boska and Satoshi visual direction, now curated around the COR iOS app. Availability is **Coming soon**, confirmed by the owner. No download URL, product price, trial duration, customer testimonial or separate Gold tier is asserted.

## Content and source

`build.py` generates `dist/index.html` and `curated-content.json`. The latter maps feature claims to app source at commit `ba0c183` from `/Applications/COR`. `dist/product.css` adds the product presentation to the retained theme. `dist/app.js` implements mobile navigation, nutrition tabs and a keyboard-accessible screenshot viewer.

Run `python3 build.py`, then `python3 -m http.server 4317 --bind 127.0.0.1 --directory dist` to preview. This is a static site with no analytics, signup collection or purchase flow.

## Real product images

`dist/assets/product/` contains native 1206 × 2622 simulator screenshots of COR's production SwiftUI views. Screen pixels are not AI-generated or redrawn. The phone borders, rotation, glow and detail crop are CSS presentation. Captures use synthetic local records, existing app preview fixtures, and the app's own burger artwork. These are illustrative app states, not customer results or measured nutrition for a real meal.

The isolated screenshot host is retained in `product-shots/CORWebsiteCapture.swift` for reproducibility. The original app checkout was not changed. No account, health records or secrets were copied to the site.

Screens: Home, hidden-ingredient questions, editable nutrition, ingredient grade, strength history and weight trend. The website identifies the images as sample data and allows visitors to enlarge them.

## Publishing

Keep `.openai/hosting.json` and the existing Site identity. Publish the static `dist` using the Sites source helper. Preserve the existing owner-private audience.

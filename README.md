# COR Active website

The static marketing website for https://coractive.co.
Shared repository: https://github.com/charlesamgmt-a11y/cor-active-website

Read [AGENTS.md](AGENTS.md) for shared editing conventions and
[DEPLOYMENT.md](DEPLOYMENT.md) for the verified hosting state and release process.
Cloudflare Pages is connected to GitHub: branches receive previews and `main`
deploys production at https://coractive.co. HTTPS and the www redirect are active.
The generated `/deployment.json` reports the hosted Git commit for release checks.

## Build and preview

Requires Python 3 and Node.js. No packages need installing.

```sh
bash scripts/build-site.sh
python3 -m http.server 4317 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4317/. The build validates JavaScript, local links/assets,
unique IDs and hosting file limits.

## Where to edit

- `build.py`: homepage, legal/confirmation pages, metadata and SEO files.
- `reference-data.json`: product copy and FAQs.
- `dist/style.css`, `dist/fonts.css`: source styles.
- `dist/app.js`: source interactions and animation.
- `dist/assets/`: logos, videos, product screens, bezels and fonts.

Do not delete `dist`: it contains source styles, scripts and original assets,
as well as generated HTML. Edit the generator instead of generated HTML and
commit rebuilt pages with source changes. `dist/product.css`, `dist/favicon.svg`
and `curated-content.json` are older unused assets.

## Current launch state

The app is coming soon. Business/tab name: COR Active; in-page app name: COR.
Pricing stays “Free to start. COR Pro available in the app.” Real app captures use
illustrative records; the iPhone 18 Pro Max Glacier frame is an illustrative mockup. Updated captures and
Charles's background photos are pending.

`/privacy/` and `/terms/` are public DRAFT review pages with placeholders, not
approved final policies. `support@coractive.co` is displayed, but delivery has
not been verified. Signup is hidden; the launch-status section collects no addresses.

## Waitlist integration

Replace the `BREVO EMBED GOES HERE` launch-status section in `build.py`, inside `#waitlist`,
with the configured Brevo form. Complete the account, sender-domain and double
confirmation setup first. Keep API keys out of frontend code.

Published redirect pages:

- After submission: https://coractive.co/waitlist/check-email/
- After confirmation: https://coractive.co/waitlist/confirmed/

Both are noindex and excluded from the sitemap. Opening them does not subscribe
or verify anyone: Brevo owns storage and confirmation. Waitlist membership is
separate from Supabase app accounts.

## Image delivery

The original PNG captures stay in `dist/assets/product/`. The page uses committed
WebP variants selected by `image-variants.json`, including for enlarged views.
Run `python3 scripts/optimize-images.py` locally with `cwebp` installed to regenerate
them after replacing an original. Then run the normal site build. Cloudflare
does not need the codec. Keep screenshots readable when tuning compression.

[Release notes and remaining work in Notion](https://app.notion.com/p/3dec8d97165e8182923acd936d5737d3).

## Social preview artwork

The committed Open Graph image uses COR without a macron and states Coming soon.
`product-shots/cor-og-preview.svg` is its editable vector layout, referencing the
unchanged native home screenshot. Render at 1200 × 630 with Inkscape, then encode
as JPEG. The Swift generator is retained as the macOS alternative.

The hero and app-screen showcase use Hoverify’s iPhone 18 Pro Max Glacier frame.
Glacier is Apple’s light-blue finish. See `product-shots/device-frame-provenance.md`
for the asset source, measurements, license and unchanged capture provenance.

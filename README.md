# COR Active website

A static homepage that follows the owner's Framer project ("Calories copy", published at goodness-zebra-710061.framer.app): the same sections, Boska + Satoshi type, dark blue/ivory palette and scroll animations, rebranded as **COR Active**.

## Build and preview

```
python3 build.py
python3 -m http.server 4317 --bind 127.0.0.1 --directory dist
```

`build.py` writes `dist/index.html`. Text comes from `reference-data.json` (copied from the Framer project). Styles are in `dist/fonts.css` + `dist/style.css`; all motion and interaction is in `dist/app.js` (no libraries).

## Before launch

Fill in the block at the top of `build.py`, then rebuild:

- `APP_STORE_URL`: every "Download for iPhone" button points here (until it is set they scroll to the download section)
- `PRIVACY_URL`, `TERMS_URL`: footer legal links (App Store Connect needs public URLs for these)
- `SUPPORT_EMAIL`: footer Contact link
- `PRO_PRICE`: shown on the COR Pro card (until it is set the card says "In app")

## What's on the page

- **Logo preloader**: the liquid-metal COR wordmark rises in, holds, then fades. It shows once per browser session.
- **Focus Lens nav**: the link nearest the cursor sharpens, the others blur, and corner brackets glide to it.
- **Hero**: the phone scans, the nutrition sheet slides up, and macro cards fly in ("Know what you're eating").
- **Food suggestions**: blurred 3D foods come into focus on hover or tap, with a good-pick or avoid hint.
- **Exploded burger**: the layers spread apart on scroll, with labels for hidden calories.
- **How it works**: a sticky phone with three steps (scan, insights, action) driven by scroll.
- **Feature cards, AI meal demo, a fan of real app screens, Free/Pro pricing.**
- **FAQ**: Smooth-FAQ-Flow-style glass cards. One is open at a time, with an animated height change and a +/− icon.
- **Footer**: the liquid-metal wordmark video (`dist/assets/brand/`).

The favicon is the "C" from the liquid-metal logo (`dist/favicon-*.png`, `apple-touch-icon.png`). The real app screenshots in `dist/assets/product/` are simulator captures with sample data.

`dist/product.css`, `dist/favicon.svg` and `curated-content.json` belong to the previous version and are no longer used.

## Publishing

Keep `.openai/hosting.json` and publish the static `dist` folder.

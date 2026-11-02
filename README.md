# COR Active website

A static homepage that follows the owner's Framer project ("Calories copy", published at goodness-zebra-710061.framer.app): the same sections, Boska + Satoshi type, dark blue/ivory palette and scroll animations, rebranded as **COR Active**.

## Build and preview

```
python3 build.py
python3 -m http.server 4317 --bind 127.0.0.1 --directory dist
```

`build.py` writes `dist/index.html`. Product copy comes from `reference-data.json`, reviewed against the COR app. Styles are in `dist/fonts.css` + `dist/style.css`; all motion and interaction is in `dist/app.js` (no libraries).

## Before launch

Fill in the block at the top of `build.py`, then rebuild:

- `APP_STORE_URL`: enables real download links; until set, the site says Coming soon
- `PRIVACY_URL`, `TERMS_URL`: footer legal links; omitted until real public URLs are configured
- `SUPPORT_EMAIL`: footer Contact link; omitted until configured
- `PRO_PRICE`: shown on the COR Pro card (until it is set the card says "In app")

## What's on the page

- **Logo preloader**: the liquid-metal COR wordmark rises in, holds, then fades. It shows once per browser session.
- **Focus Lens nav**: the link nearest the cursor sharpens, the others blur, and corner brackets glide to it.
- **Hero**: the phone scans, the nutrition sheet slides up, and macro cards fly in ("Know what you're eating").
- **Food suggestions**: blurred 3D foods come into focus on hover or tap, with a portion or ingredient detail to consider.
- **Exploded burger**: the layers spread apart on scroll, with labels for hidden calories.
- **How it works**: a sticky phone with three steps (scan, insights, action) driven by scroll.
- **Feature cards, AI meal demo, a fan of expandable real app screens, Free/Pro pricing.**
- **FAQ**: Smooth-FAQ-Flow-style glass cards. One is open at a time, with an animated height change and a +/− icon.
- **Footer**: the liquid-metal wordmark video (`dist/assets/brand/`).

The favicon is the "C" from the liquid-metal logo (`dist/favicon-*.png`, `apple-touch-icon.png`). The real app screenshots in `dist/assets/product/` are simulator captures with sample data.

`dist/product.css`, `dist/favicon.svg` and `curated-content.json` belong to the previous version and are no longer used.

## Publishing

Keep `.openai/hosting.json` and publish the static `dist` folder.

## Waitlist connection

The signup form is still a disabled preview. The `BREVO EMBED GOES HERE` marker in
`build.py` identifies where the generated Brevo form must replace it. Brevo account
access and sender-domain authentication are still pending; no contacts are collected.

Two branded redirect pages are generated for Brevo's double-confirmation flow:

- After form submission: `https://coractive.co/waitlist/check-email/`
- After the visitor clicks the confirmation email: `https://coractive.co/waitlist/confirmed/`

These pages currently exist only in the local review build. Publish them before
using their public URLs in Brevo. They are `noindex` and excluded from the sitemap.
Opening either page does not subscribe or verify anyone; Brevo must perform the
confirmation and list insertion. Use the local equivalents on port 4317 for design review.

## Review and release notes

The animated phone, feature widgets and meal scenes are labeled illustrations with sample values. The app gallery uses six native COR captures in a swipeable strip: daily dashboard, meal photo context, estimate review, product ingredients, strength and weight. A light progressive blur softens only the lower image edge; tapping a screen opens the unblurred capture. Coming-soon labels remain until an App Store URL is supplied. The loader cannot block the page when JavaScript is disabled, FAQ answers have accessible expanded states, and narrow mobile layouts are checked before publication.

The public custom domain is `https://coractive.co`. Brevo waitlist integration and public legal/support pages are still separate unfinished tasks; this redesign does not collect emails.

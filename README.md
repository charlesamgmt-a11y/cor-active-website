# CŌR homepage recreation

Standalone HTML, CSS, and JavaScript recreation of the homepage in the supplied Framer project. Original copy, Boska and Satoshi fonts, phone frame, food graphics, and photos are retained. Scroll effects, glass surfaces, scan previews, mobile navigation, and FAQ interactions are implemented in browser code.

Run `python3 build.py` to regenerate `dist/index.html` from `reference-data.json`, then `python3 -m http.server 4317 --bind 127.0.0.1 --directory dist` for a local preview. The files in `dist/` are ready for static hosting.

The food scan, log action, and meal preparation are presentation demos. Download, stories, contact, and legal links lead to the original Framer site's corresponding pages. Prices and testimonials reproduce the supplied reference; they have not been independently verified.

Validation: JavaScript syntax check; local asset existence; desktop and 390-pixel-wide browser inspection; food selection and guide dialog; interactive scan steps; FAQ expansion; mobile menu and pricing navigation; meal animation replay; no observed console errors or broken images.

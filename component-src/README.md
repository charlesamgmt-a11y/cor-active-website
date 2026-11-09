# Original Framer components in COR (preview only)

Retrieved 2026-11-08. Creator ownership retained; not COR-authored components.
Free component Limited Commercial License: https://www.framer.com/legal/community-terms (7.3.1).
Used only as part of COR's website, not offered as standalone assets.

- Reveal Text On Scroll, Ali Themes: https://www.framer.com/m/ScrollRevealText-vXBxyx.js@ymLCSaN7wX7cJKeayNed
- Spring FAQ Accordion, Zeeshan: https://www.framer.com/m/SpringFaqaccordion-JPXpfw.js@DzDAqhQK0oAqbErQpHNK

The two originals are byte-for-byte copies of their published modules. The build aliases only their editor controls and static-canvas detection to framer-bridge.js. Original animation implementation remains intact. COR supplies content, typography, colors and the FAQ's default spring (220 stiffness,24 damping,1 mass). Reduced-motion users get plain headings and zero-duration FAQ transitions at page load. Browser changes to reduced motion require reload in this preview.

Sticky Scroll now runs from the original native component and its original ShowcaseProgress module:
https://framer.com/m/Feature-Showcase-Native-id9zAN.js@gpvo5v6vZyB9jj7KIYuf
https://framerusercontent.com/modules/1SxRVjhFgB5Qf1i6uBW3/SCqe089z8jvO6PhJMxpT/ShowcaseProgress.js

The original modules remain byte-for-byte intact under originals/. The build applies explicit content substitutions from sticky-content.mjs (copy, local image URLs, and the mobile anchor setting). sticky-runtime.js uses Framer's MIT-licensed public 2.4.1 runtime for real variant state, RichText, Image, CSS, and callbacks. Compatibility wrappers provide the newer editor scope/viewport APIs; none implement crossfades or scroll transitions. The original .55-second tween and .16-second progress smoothing are unchanged. CSS only adapts typography, phone framing and responsive dimensions; unused template buttons are hidden.

The recreation's training markup and controller were removed. The section has a static text fallback while its original component loads. All assets are bundled locally; this does not embed or publish another Framer page.

Verified in Chrome desktop and 390px viewport: steps 1/2/3, exclusive visible image after settling, forward/backward scroll, ArrowLeft and End navigation, no horizontal overflow, no runtime console errors. Nav and footer code are unchanged by this integration. Public framer runtime declares an older Motion peer version; this project pins Motion 12 (required by the original motion.create call), and uses legacy-peer-deps for reproducible installation. Broader browser testing and performance tuning are still advisable before release.

Build: npm ci, then bash scripts/build-site.sh. Generated bundle is checked in so existing static hosting still receives a complete site. Do not publish without approval.

## Assembling barbell preview
The burger and ingredient details now sit together; the existing logging demo precedes them. A new code-native SVG barbell uses six independent metal plate layers and the burger's cubic ease-out scroll pacing. Reduced-motion users see a static assembled barbell. This new decorative sequence is custom COR artwork, not a Framer marketplace component. The original Sticky Scroll component below it is unchanged.

Fitness captures: workout-history.png is copied from output/strength-glass-refinement-2026-11-07/screenshots/Refined exercise session history.png; muscle-balance.png from output/activity-final-audit-2026-11-07/Strength common-baseline muscle balance.png. Both are actual app test captures with illustrative records, not generated interfaces. The first frame shows saved session history and PRs, not an active workout logger. Nutrition and weight images were removed from this fitness sequence.

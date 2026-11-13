# Website polish, local review only

Base: c6f2b06. No publish, push or main merge performed.

## Changes
- Replaced barbell assembly with original code-native brushed silver plates, dark hubs, concentric machining lines; plates condense as the visitor scrolls. Reduced-motion users see the completed stack.
- Removed CTA crown and replaced old icon artwork with user-supplied transparent mirror COR wordmark, maintaining proportions within black icon tile. iOS app assets unchanged.
- Removed duplicate footer legal group and corrected responsive columns.
- Kept Framer Motion spring transitions in accessible FAQ: native button, expanded state and separate labelled answer region, collapsed answers excluded from accessibility tree.
- Added full-size viewer buttons for all three training captures with native dialog/Escape/focus return.
- Mobile how-it-works no longer changes under a reader; steps are manually selectable. Desktop scroll progression remains.
- Replaced developer-facing Brevo placeholder with truthful visitor-facing unavailable notice. Signup remains disabled.

## Verification
- bash scripts/build-site.sh passes: 6 HTML pages, 109 local references, unique IDs, 80 deployable files.
- git diff --check passes.
- Chrome desktop and 390px/320px viewport visual checks, no horizontal document overflow.
- Strength overview enlargement opens; Escape closes and returns focus.
- FAQ Enter expands with a separate accessible answer, other collapsed answers not exposed.
- Plate scroll progress changed from .663 to .999 on narrow viewport, with transform offsets reducing toward zero.
- No Chrome console errors in local preview.
- Crown absent and new logo path/image verified.
- Real iPhone Safari, full assistive-technology audit, Lighthouse and real-user performance were not tested. Reduced-motion behavior reviewed in CSS, not OS-emulated.

## Inspiration
Observed Robinhood Platinum live page: spacious monochrome product presentation, oversized restrained headings, metallic close-ups and single-benefit sections. Applied restrained silver product staging to plates, not its financial claims, assets or unrelated page redesign.

## Still open
Waitlist integration and complete legal documents remain launch blockers. Do not activate/remove draft labels without actual configuration and approved policy details. Existing heavy captures and JS merit separate performance optimization. Live coractive.co unchanged pending review/publication authorization.

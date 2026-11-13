import React from 'react';
import {createRoot} from 'react-dom/client';
import Reveal from './originals/reveal.js';
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
if (!reduced.matches) document.querySelectorAll('.section-header h2').forEach(heading => {
 const text = heading.textContent.trim();
 const style = getComputedStyle(heading);
 const font={fontFamily:style.fontFamily,fontSize:'inherit',fontWeight:style.fontWeight,lineHeight:'inherit',letterSpacing:'inherit'};
 heading.dataset.originalComponent='Reveal Text On Scroll';
 heading.setAttribute('aria-label',text);
 const visual = document.createElement("span"); visual.setAttribute("aria-hidden","true"); heading.replaceChildren(visual);
 createRoot(visual).render(<Reveal {...Reveal.defaultProps} text={text} htmlTag="span" preset="Soft Words" font={font} colorHidden="#70746e" colorRevealed="#f5f3eb" trigger="Scroll" offsetStart={90} offsetEnd={35} style={{width:'100%'}}/>);
});

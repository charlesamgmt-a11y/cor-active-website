import React from 'react';
import {createRoot} from 'react-dom/client';
import FAQ from './accessible-faq.jsx';
import Reveal from './originals/reveal.js';
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const faq = document.querySelector('.flow-list');
const rows = [...document.querySelectorAll('.flow-item')];
if (faq && rows.length) {
 const items = rows.map(row => ({question: row.querySelector('.flow-q').textContent.replace(/OpenClose/g,'').replace(/^\d{2}/,'').trim(), answer:row.querySelector('.flow-a').textContent.trim()}));
 const host = document.createElement('div'); host.dataset.originalComponent='Spring FAQ Accordion';
 faq.replaceWith(host);
 const font = size => ({fontFamily:'inherit',fontSize:size,fontWeight:400,lineHeight:'1.6em'});
 createRoot(host).render(<FAQ items={items} showTitle={false} title="Questions" titleSpacing={12} defaultOpenIndex={-1} layout="auto" breakpoint={600} colors={{background:'transparent',border:'rgba(255,255,255,.18)',hoverColor:'#f5f3eb',number:'#b9bcb8',questionActive:'#f5f3eb',questionInactive:'#c5c8c3',answer:'#b9bcb8',label:'#f5f3eb'}} transition={reduced.matches?{duration:0}:{type:'spring',stiffness:220,damping:24,mass:1}} spacing={{desktop:{stackGap:12,rowPadding:'26px 0'},mobile:{stackGap:12,rowPadding:'22px 0'}}} titleFont={font(24)} numberFont={font(13)} questionFont={font(18)} answerFont={font(16)} labelFont={font(13)} uppercase={false} qaMaxWidth={720} containerPadding="0px" containerRadius="0px" containerBorder={{borderWidth:0}} containerBlurEnabled={false} containerBlurAmount={0} style={{height:'auto',overflow:'visible'}}/>);
}
if (!reduced.matches) document.querySelectorAll('.section-header h2').forEach(heading => {
 const text = heading.textContent.trim();
 const style = getComputedStyle(heading);
 const font={fontFamily:style.fontFamily,fontSize:'inherit',fontWeight:style.fontWeight,lineHeight:'inherit',letterSpacing:'inherit'};
 heading.dataset.originalComponent='Reveal Text On Scroll';
 heading.setAttribute('aria-label',text);
 const visual = document.createElement("span"); visual.setAttribute("aria-hidden","true"); heading.replaceChildren(visual);
 createRoot(visual).render(<Reveal {...Reveal.defaultProps} text={text} htmlTag="span" preset="Soft Words" font={font} colorHidden="#70746e" colorRevealed="#f5f3eb" trigger="Scroll" offsetStart={90} offsetEnd={35} style={{width:'100%'}}/>);
});

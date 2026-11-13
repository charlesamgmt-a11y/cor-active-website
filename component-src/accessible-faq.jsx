import React, {useState} from 'react';
import {motion} from 'framer-motion';
// Keep the original motion timing while separating controls from answer content.
export default function FAQ({items,transition}) {
 const [open,setOpen]=useState(-1);
 return <div className="accessible-faq">{items.map((item,i)=><div className="faq-row" key={i}>
  <h3><button type="button" id={`faq-question-${i}`} aria-expanded={open===i} aria-controls={`faq-answer-${i}`} onClick={()=>setOpen(open===i?-1:i)}>
   <span className="faq-number" aria-hidden="true">{String(i+1).padStart(2,'0')}</span><span>{item.question}</span><span className="faq-label" aria-hidden="true">{open===i?'Close':'Open'}</span>
  </button></h3>
  <motion.div id={`faq-answer-${i}`} role="region" aria-labelledby={`faq-question-${i}`} aria-hidden={open!==i} initial={false} animate={{height:open===i?'auto':0,opacity:open===i?1:0}} transition={transition} style={{overflow:'hidden'}}><p>{item.answer}</p></motion.div>
 </div>)}</div>;
}

import React, {useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import Sticky from './originals/sticky.js';
const host = document.querySelector('#original-sticky');
function ResponsiveSticky() {
 const [mobile,setMobile]=useState(matchMedia('(max-width:700px)').matches);
 useEffect(()=>{const m=matchMedia('(max-width:700px)');const update=()=>setMobile(m.matches);m.addEventListener('change',update);return()=>m.removeEventListener('change',update);},[]);
 return <Sticky key={String(mobile)} style={{width:'100%',height:'auto'}} />;
}
if (host) createRoot(host).render(<ResponsiveSticky />);

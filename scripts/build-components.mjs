import {readFile} from 'node:fs/promises';
import {customizeSticky} from '../component-src/sticky-content.mjs';
import {build} from 'esbuild';
await build({entryPoints:['component-src/index.jsx'],bundle:true,minify:true,outfile:'dist/original-components.js',format:'esm',alias:{framer:'./component-src/framer-bridge.js'},legalComments:'eof'});

await build({entryPoints:['component-src/sticky-entry.jsx'],plugins:[{name:'original-dependency',setup(b){b.onLoad({filter:/originals\/sticky\.js$/},async args=>({contents:customizeSticky(await readFile(args.path,'utf8')),loader:'js'}));b.onResolve({filter:/^https:.*ShowcaseProgress/},()=>({path:process.cwd()+'/component-src/originals/ShowcaseProgress.js'}));}}],bundle:true,minify:true,outfile:'dist/sticky-original.js',format:'esm',alias:{framer:'./component-src/sticky-runtime.js'},legalComments:'eof'});

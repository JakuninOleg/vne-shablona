import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {setTimeout as delay} from 'node:timers/promises';
const origin='https://vneshablona.ru';
const before=process.env.BEFORE_SHA;
const changed=before && !/^0+$/.test(before)
 ? execFileSync('git',['diff','--name-only','--diff-filter=ACM',before,'HEAD'],{encoding:'utf8'}).trim().split('\n')
 : ['index.html','legal/index.html','analytics.js'];
const files=changed.filter(f=>/^(?:assets\/|legal\/|uslugi\/|index\.html$|404\.html$|[^/]+\.(?:css|js|txt|xml)$)/.test(f));
if(!files.length){console.log('No public files changed.');process.exit(0);}
const publicPath=f=>'/'+f.replace(/(?:^|\/)index\.html$/,m=>m.startsWith('/')?'/':'');
const hash=b=>createHash('sha256').update(b).digest('hex');
const pending=new Map(await Promise.all(files.map(async f=>[f,hash(await readFile(f))])));
const end=Date.now()+15*60*1000;
while(pending.size && Date.now()<end){
 for(const [file,digest] of pending){
  try{
   const response=await fetch(origin+publicPath(file),{redirect:'manual',headers:{'Cache-Control':'no-cache'},signal:AbortSignal.timeout(15000)});
   if(response.status===200 && hash(Buffer.from(await response.arrayBuffer()))===digest)pending.delete(file);
  }catch{}
 }
 if(pending.size){console.log('Waiting for deployment:',[...pending.keys()].join(', '));await delay(30000);}
}
if(pending.size)throw Error('Deployment not verified; no notification sent.');
const sitemap=await readFile('sitemap.xml','utf8');
const allowed=[...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>m[1]);
const changedHtml=new Set(files.filter(f=>f.endsWith('.html')).map(f=>origin+publicPath(f)));
const shared=files.some(f=>/^(?:assets\/|[^/]+\.(?:css|js|xml)$)/.test(f));
const urls=allowed.filter(url=>shared||changedHtml.has(url));
if(urls.length)execFileSync('node',['scripts/submit-indexnow.mjs',...urls],{stdio:'inherit'});

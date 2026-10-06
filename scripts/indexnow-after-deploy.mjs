import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {setTimeout as delay} from 'node:timers/promises';
const origin='https://vneshablona.ru';
const before=process.env.BEFORE_SHA;
const changed=before && !/^0+$/.test(before)
 ? execFileSync('git',['diff','--name-only','--diff-filter=ACM',before,'HEAD'],{encoding:'utf8'}).trim().split('\n')
 : ['index.html','legal/index.html','analytics.js'];
const files=changed.filter(f=>/^(assets\/|legal\/|index\.html$|404\.html$|.*\.(css|js|txt|xml)$)/.test(f) && !f.startsWith('scripts/'));
if(!files.length){console.log('No public files changed.');process.exit(0);}
const hash=b=>createHash('sha256').update(b).digest('hex');
const pending=new Map(await Promise.all(files.map(async f=>[f,hash(await readFile(f))])));
const end=Date.now()+15*60*1000;
while(pending.size && Date.now()<end){
 for(const [file,digest] of pending){
  try{
   const path=file==='index.html' ? '/' : file==='legal/index.html' ? '/legal/' : '/'+file;
   const response=await fetch(origin+path,{redirect:'manual',headers:{'Cache-Control':'no-cache'},signal:AbortSignal.timeout(15000)});
   if(response.status===200 && hash(Buffer.from(await response.arrayBuffer()))===digest) pending.delete(file);
  }catch{}
 }
 if(pending.size){console.log('Waiting for deployment:',[...pending.keys()].join(', '));await delay(30000);}
}
if(pending.size)throw Error('Deployment not verified; no notification sent.');
const urls=['/'];
if(files.some(f=>f.startsWith('legal/')||f==='analytics.js'||f==='analytics.css'))urls.push('/legal/');
execFileSync('node',['scripts/submit-indexnow.mjs',...urls],{stdio:'inherit'});

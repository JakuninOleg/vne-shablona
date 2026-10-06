import {readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root = new URL('../',import.meta.url);
const origin = 'https://vneshablona.ru';
const {file} = JSON.parse(await readFile(new URL('scripts/indexnow-key.json',root),'utf8'));
const key = (await readFile(new URL(file,root),'utf8')).trim();
if (!/^[a-zA-Z0-9-]{8,128}$/.test(key) || file !== key+'.txt') throw Error('Invalid key');
const input = process.argv.slice(2).filter(s=>s!=='--dry-run');
if (!input.length) throw Error('Usage: node scripts/submit-indexnow.mjs / [/legal/] [--dry-run]');
const sitemap = await readFile(new URL('sitemap.xml',root),'utf8');
const allowed = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>m[1]);
const urls = [...new Set(input.map(s=>new URL(s,origin).href))];
if (urls.some(s=>!allowed.includes(s))) throw Error('Only canonical sitemap URLs allowed');
console.log('URLs:',urls.join(', '));
if (process.argv.includes('--dry-run')) process.exit(0);
const keyLocation = origin+'/'+file;
const request = (url) => fetch(url,{signal:AbortSignal.timeout(20000),redirect:'manual'});
const kr = await request(keyLocation);
if(kr.status!==200 || (await kr.text()).trim()!==key) throw Error('Deployed key unavailable');
for(const url of urls){
 const r = await request(url); const html = await r.text();
 if(r.status!==200 || /noindex/i.test(r.headers.get('x-robots-tag')||'') || /<meta[^>]+name=["']robots["'][^>]+content=["'][^"']*noindex/i.test(html)) throw Error('URL not publicly indexable: '+url);
 if(!html.includes('href="'+url+'"')) throw Error('Canonical missing: '+url);
}
const r=await fetch('https://api.indexnow.org/indexnow',{method:'POST',headers:{'Content-Type':'application/json; charset=utf-8'},body:JSON.stringify({host:new URL(origin).host,key,keyLocation,urlList:urls}),signal:AbortSignal.timeout(20000)});
if(![200,202].includes(r.status)) throw Error('IndexNow HTTP '+r.status+': '+(await r.text()).slice(0,200));
console.log('IndexNow received URLs: HTTP '+r.status+' (not a guarantee of indexing)');

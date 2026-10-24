"""Validate generated static routes, local links, assets and SEO metadata. Stdlib only."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://vneshablona.ru'

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set();self.links=[];self.assets=[];self.h1=0;self.canonical=[];self.description=[];self.title=[];self.json=[];self.active=None;self.buffer=[];self.errors=[];self.in_head=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='head':self.in_head=True
        if a.get('id'):
            if a['id'] in self.ids:self.errors.append('duplicate id '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='link':
            if a.get('rel')=='canonical':self.canonical.append(a.get('href'))
            elif a.get('href'):self.assets.append(a['href'])
        if tag=='meta' and a.get('name')=='description':self.description.append(a.get('content',''))
        if tag in ('img','script','source') and a.get('src'):self.assets.append(a['src'])
        if tag in ('img','source') and a.get('srcset'):self.assets.extend(v.strip().split()[0] for v in a['srcset'].split(','))
        if tag=='img' and any(k not in a for k in ('alt','width','height')):self.errors.append('image missing alt/width/height: '+a.get('src',''))
        if tag=='title' and self.in_head or tag=='script' and a.get('type')=='application/ld+json':self.active=tag;self.buffer=[]
    def handle_data(self,data):
        if self.active:self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=='head':self.in_head=False
        if self.active==tag:
            (self.title if tag=='title' else self.json).append(''.join(self.buffer));self.active=None

def local_path(url,base='/'):
    full=urlsplit(urljoin(ORIGIN+base,url))
    if full.scheme not in ('http','https') or full.netloc!=urlsplit(ORIGIN).netloc:return None,full.fragment
    path=ROOT/unquote(full.path).lstrip('/')
    if full.path.endswith('/'):path/='index.html'
    try:path.resolve().relative_to(ROOT.resolve())
    except ValueError:raise ValueError('Path escapes site root: '+url)
    return path,unquote(full.fragment)

def check():
    urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    errors=[];docs={};titles=set();descriptions=set();assets=set()
    for url in [*urls,ORIGIN+'/404.html']:
        path,_=local_path(url)
        if not path or not path.is_file():errors.append('Missing route '+url);continue
        doc=Document();doc.feed(path.read_text(encoding='utf-8'));docs[path]=doc
        errors.extend(str(path.relative_to(ROOT))+': '+error for error in doc.errors)
        if doc.h1!=1:errors.append(url+': expected one H1')
        if len(doc.title)!=1 or not doc.title[0].strip():errors.append(url+': missing title')
        elif doc.title[0] in titles:errors.append(url+': duplicate title')
        else:titles.add(doc.title[0])
        if len(doc.description)!=1 or not doc.description[0].strip():errors.append(url+': missing description')
        elif doc.description[0] in descriptions:errors.append(url+': duplicate description')
        else:descriptions.add(doc.description[0])
        if url in urls and doc.canonical!=[url]:errors.append(url+': incorrect canonical')
        for raw in doc.json:
            try:json.loads(raw)
            except ValueError:errors.append(url+': invalid JSON-LD')
        for ref in doc.assets:
            asset,_=local_path(ref,urlsplit(url).path)
            if asset:assets.add(asset)
    for path,doc in docs.items():
        base='/'+path.relative_to(ROOT).as_posix()
        for ref in doc.links:
            target,fragment=local_path(ref,base)
            if not target:continue
            if not target.is_file():errors.append(base+': broken link '+ref)
            elif fragment and target.suffix=='.html':
                target_doc=docs.get(target)
                if not target_doc:target_doc=Document();target_doc.feed(target.read_text(encoding='utf-8'))
                if fragment not in target_doc.ids:errors.append(base+': missing anchor '+ref)
    pending=list(assets)
    while pending:
        asset=pending.pop()
        if not asset.is_file():errors.append('Missing asset '+str(asset.relative_to(ROOT)));continue
        if asset.suffix=='.css':
            for value in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',asset.read_text(encoding='utf-8')):
                if value.startswith('data:'):continue
                child,_=local_path(value,'/'+asset.relative_to(ROOT).as_posix())
                if child and child not in assets:assets.add(child);pending.append(child)
    if len(urls)!=len(set(urls)):errors.append('Duplicate sitemap URLs')
    if errors:raise SystemExit('\n'.join(sorted(set(errors))))
    print(f'OK: {len(urls)} sitemap pages + 404, {len(assets)} local assets, canonical / H1 / metadata / JSON-LD / links / anchors')
    return urls,assets

if __name__=='__main__':check()

"""Build the migration pages in the incumbent paper/comic world. Run at site root."""
from pathlib import Path
from html import escape as e
import json
import re

ROOT = Path.cwd()
assert (ROOT / 'assets/logo-vne-shablona.svg').is_file(), 'Run in vne-shablona'
ORIGIN = 'https://vneshablona.ru'
home = (ROOT / 'index.html').read_text(encoding='utf-8')
SERVICES = json.loads((ROOT / 'scripts/service-content.json').read_text(encoding='utf-8'))
assert len({s['slug'] for s in SERVICES}) == len(SERVICES)

def arrow():
    return '<svg viewBox="0 0 32 24" width="32" height="24" aria-hidden="true"><path d="M2 12h26M19 3l9 9-9 9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def root_links(markup):
    return re.sub(r'href="#(?!contact)([^"]+)"', r'href="/#\1"', markup)

def header():
    return '<a class="skip-service" href="#main">К содержимому</a>' + root_links(re.search(r'<header class="site-header".*?</header>', home, re.S).group())

def footer():
    return root_links(re.search(r'<footer class="site-footer".*?</footer>', home, re.S).group())

def form(name):
    # Keep the complete homepage scene, writing tablet, validation and delivery handler.
    markup = re.search(r'<section class="contact" id="contact".*?</section>', home, re.S).group()
    markup = markup.replace('<form class="contact__form"', '<form class="contact__form"', 1)
    markup = markup.replace('<label>Ваше имя', f'<input type="hidden" name="Направление" value="{e(name)}" /><label>Ваше имя', 1)
    markup = markup.replace('placeholder="Что вы хотите сделать?"', 'placeholder="Ссылка на сайт и что хочется изменить"')
    markup = markup.replace('Готовы сделать сайт<br />под свой бизнес?', 'Дадим вашему сайту<br />новую жизнь?')
    markup = markup.replace('Опишите задачу в двух словах. Начнём с эскиза решения.', 'Пришлите ссылку и расскажите, что мешает. Начнём с эскиза решения.')
    return markup

def artwork(name, alt, *, eager=False, sizes='(max-width: 760px) 94vw, 52vw'):
    stem=Path(name).stem
    width,height=next(((s['width'],s['height']) for s in SERVICES if s['image']==name),(1870,841))
    loading='fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="/assets/{name}" srcset="/assets/{stem}-640.webp 640w, /assets/{stem}-1280.webp 1280w, /assets/{name} {width}w" sizes="{sizes}" width="{width}" height="{height}" alt="{e(alt)}" {loading} decoding="async" />'

def breadcrumbs(name=None):
    tail=f'<a href="/uslugi/">Перенос и переделка</a><span aria-hidden="true">/</span><span aria-current="page">{e(name)}</span>' if name else '<span aria-current="page">Перенос и переделка</span>'
    return '<nav class="service-breadcrumbs section-inner" aria-label="Хлебные крошки"><a href="/">Главная</a><span aria-hidden="true">/</span>'+tail+'</nav>'

def page(path, title, description, content, name, extra_graph, image):
    canonical=ORIGIN+path
    crumbs=[{'@type':'ListItem','position':1,'name':'Главная','item':ORIGIN+'/'}]
    if path!='/uslugi/': crumbs.append({'@type':'ListItem','position':2,'name':'Перенос и переделка','item':ORIGIN+'/uslugi/'})
    crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':name,'item':canonical})
    graph=[{'@type':'WebPage','@id':canonical+'#page','url':canonical,'name':title,'description':description,'inLanguage':'ru'},
           {'@type':'BreadcrumbList','itemListElement':crumbs},
           {'@type':'Person','@id':'https://jakuninoleg.dev/#person','name':'Олег Якунин','url':'https://jakuninoleg.dev/ru'},extra_graph]
    schema=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')
    html=f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{e(title)}</title><meta name="description" content="{e(description)}" /><link rel="canonical" href="{canonical}" />
<meta name="theme-color" content="#f6ecd9" /><meta property="og:type" content="website" /><meta property="og:locale" content="ru_RU" /><meta property="og:site_name" content="ВНЕ ШАБЛОНА" /><meta property="og:title" content="{e(title)}" /><meta property="og:description" content="{e(description)}" /><meta property="og:url" content="{canonical}" /><meta property="og:image" content="{ORIGIN}/assets/{image}" /><meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" /><link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Neucha-Regular.woff2" crossorigin />
<link rel="stylesheet" href="/site.css?v=mobile-perf-1" /><link rel="stylesheet" href="/services.css?v=comic-2" /><link rel="stylesheet" href="/analytics.css" />
<script type="application/ld+json">{schema}</script><script src="/script.js" defer></script><script src="/analytics.js" defer></script></head>
<body class="service-page">{header()}<main id="main">{content}{form(name)}</main>{footer()}</body></html>'''
    dest=ROOT/path.strip('/')/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html+'\n',encoding='utf-8')

def proof():
    return '''<section class="service-proof section-inner" aria-labelledby="proof-title"><div><h2 id="proof-title">За красивым сайтом —<br />удобное управление.</h2><p>На сайте КЭМЗ продукция, категории, новости и документы управляются через OJ CMS. Редактор работает с контентом, черновиками и публикацией в одной панели.</p><a class="service-text-link" href="https://jakuninoleg.dev/ru/work/aokemz">Посмотреть работу Олега Якунина '''+arrow()+'''</a></div><figure><img src="/assets/kemz-cms.webp" width="1265" height="723" loading="lazy" alt="Панель OJ CMS сайта КЭМЗ: продукция, категории, новости и последние изменения" /><figcaption>Настоящий проект: управление сайтом КЭМЗ</figcaption></figure></section>'''

def service_links(exclude=None):
    return ''.join(f'''<a class="migration-route" href="/uslugi/{s['slug']}/"><div class="migration-route__art">{artwork(s['image'],'',sizes='(max-width: 760px) 100vw, (max-width: 1500px) 48vw, 700px')}</div><div class="migration-route__copy"><h3>{e(s['short'])}</h3><p>{e(s['teaser'])}</p><span class="service-text-link">Что будем делать {arrow()}</span></div></a>''' for s in SERVICES if s['slug']!=exclude)

def migration_intro(catalog=False):
    heading='Перенос и переделка сайта.<br /><em>На ваших условиях.</em>' if catalog else 'Сайт вырос из шаблона?<br /><em>Пора переезжать.</em>'
    tag='h1' if catalog else 'h2'
    return f'''<div class="migration-intro"><div class="migration-intro__copy section-inner"><{tag} id="migration-title">{heading}</{tag}><p>Бизнесу стало тесно в старом сайте. Перенесём нужное, пересоберём неудобное и дадим место новым идеям.</p><a class="service-text-link" href="{'#routes' if catalog else '/uslugi/'}">Выбрать свой маршрут {arrow()}</a></div><figure class="service-panorama"><div class="service-panorama__frame">{artwork('service-migration.webp','Владелец бизнеса, разработчик и кот перевозят сайт из коробок конструктора в открытую мастерскую',eager=catalog,sizes='100vw')}</div></figure></div>'''

for s in SERVICES:
    path='/uslugi/'+s['slug']+'/'
    lines=s['headline'].splitlines()
    heading='<br />'.join(e(x) if i==0 else f'<em>{e(x)}</em>' for i,x in enumerate(lines))
    scopes=''.join(f'<article><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a,b in s['scope'])
    process=''.join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a,b in s['process'])
    faq=''.join(f'<details><summary>{e(a)}<span aria-hidden="true">{arrow()}</span></summary><div class="service-faq__answer"><p>{e(b)}</p></div></details>' for a,b in s['faq'])
    external=' target="_blank" rel="noopener noreferrer"' if s['feature_link'].startswith('https://') else ''
    content=breadcrumbs(s['name'])+f'''
<section class="service-hero" aria-labelledby="service-title"><div class="service-hero__copy section-inner"><h1 id="service-title">{heading}</h1><p>{e(s['lead'])}</p><div class="service-actions"><a class="pill-button" href="#contact">{e(s['cta'])} {arrow()}</a><a class="service-text-link" href="#scope">Что входит в работу {arrow()}</a></div></div><figure class="service-panorama"><div class="service-panorama__frame">{artwork(s['image'],s['alt'],eager=True,sizes='100vw')}</div><figcaption>{e(s['note'])}</figcaption></figure></section>
<section class="service-scope" id="scope" aria-labelledby="scope-title"><div class="section-inner"><div class="service-section-intro"><h2 id="scope-title">{e(s['intro']).replace(chr(10),'<br />')}</h2><p>{e(s['problem'])}</p></div><div class="service-scope__list">{scopes}</div></div></section>
<section class="service-feature section-inner"><h2>{e(s['feature_title']).replace(chr(10),'<br />')}</h2><div><p>{e(s['feature'])}</p><a class="service-text-link" href="{s['feature_link']}"{external}>{e(s['feature_label'])} {arrow()}</a></div></section>
<section class="service-process" aria-labelledby="move-title"><div class="section-inner"><h2 id="move-title">Сначала подготовка.<br /><em>Потом новая глава.</em></h2><ol>{process}</ol></div></section>
{proof()}
<section class="service-price section-inner"><h2>Сколько стоит<br />вернуть контроль?</h2><div><p>{e(s['pricing'])}</p><a class="service-text-link" href="#contact">Получить оценку {arrow()}</a></div></section>
<section class="service-faq section-inner" aria-labelledby="faq-title"><h2 id="faq-title">До того,<br />как начать</h2><div>{faq}</div></section>
<aside class="service-related section-inner" aria-labelledby="related-title"><h2 id="related-title">Есть и другие маршруты</h2><div class="migration-routes migration-routes--related">{service_links(s['slug'])}</div></aside>'''
    schema={'@type':'Service','name':s['name'],'serviceType':s['name'],'url':ORIGIN+path,'description':s['description'],'provider':{'@id':'https://jakuninoleg.dev/#person'}}
    page(path,s['title'],s['description'],content,s['name'],schema,s['image'])

catalog=breadcrumbs()+migration_intro(True)+'''<section class="migration-catalog section-inner" id="routes" aria-labelledby="routes-title"><h2 id="routes-title">Четыре маршрута.<br />Один — ваш.</h2><div class="migration-routes">'''+service_links()+'''</div></section>
<section class="service-feature section-inner"><h2>Не нашли<br />свою платформу?</h2><div><p>Joomla, OpenCart, Wix, uKit или старый самописный сайт — начать можно с любой основы. Разберём, как устроены контент, каталог и заявки. Предложим перенос на собственный код или переделку подходящей части сайта.</p><p>Перенос на другую CMS, редизайн и смена хостинга решают разные задачи. Расскажите, что именно мешает: ограничения дизайна, стоимость доработок, управление контентом или работа на телефоне.</p><a class="service-text-link" href="#contact">Показать свой сайт '''+arrow()+'''</a></div></section>'''+proof()+'''<aside class="service-related section-inner"><p>Нужен новый проект с нуля? <a class="service-text-link" href="https://jakuninoleg.dev/ru/services">Лендинги, каталоги, SaaS и другие услуги Олега Якунина '''+arrow()+'''</a></p></aside>'''
page('/uslugi/','Перенос и переделка сайтов: Tilda, WordPress, Битрикс — ВНЕ ШАБЛОНА','Перенос сайтов с Tilda, WordPress и Битрикса, переделка и редизайн: собственный код, CMS, каталог и работающие формы. Выберите задачу для вашего сайта.',catalog,'Перенос и переделка сайтов',{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':s['name'],'url':ORIGIN+'/uslugi/'+s['slug']+'/'} for i,s in enumerate(SERVICES)]},'service-migration.webp')

block='<!-- migration-start --><section class="migration-home" id="migration" aria-labelledby="migration-title">'+migration_intro()+'''<div class="section-inner"><div class="migration-routes">'''+service_links()+'''</div></div></section><!-- migration-end -->'''
home=re.sub(r'<!-- migration-start -->.*?<!-- migration-end -->','',home,flags=re.S)
home=home.replace('<section class="process section-paper',block+'\n      <section class="process section-paper',1)
home=re.sub(r'<link rel="stylesheet" href="/services\.css[^\"]*"\s*/>','<link rel="stylesheet" href="/services.css?v=comic-2" />',home)
proof_home='<!-- migration-proof-start -->'+proof()+'<!-- migration-proof-end -->'
home=re.sub(r'<!-- migration-proof-start -->.*?<!-- migration-proof-end -->',lambda _:proof_home,home,flags=re.S)
home='\n'.join(line.rstrip() for line in home.splitlines())+'\n'
home=re.sub(r'\n{3,}','\n\n',home)
(ROOT/'index.html').write_text(home,encoding='utf-8')
paths=['/','/legal/','/uslugi/']+['/uslugi/'+s['slug']+'/' for s in SERVICES]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+ORIGIN+p+'</loc></url>\n' for p in paths)+'</urlset>\n',encoding='utf-8')
print('Generated',len(SERVICES)+1,'service pages; homepage and sitemap updated')

"""Extend the existing static comic site. Run from the vne-shablona checkout."""
from pathlib import Path
from html import escape as e
import json
import re

ROOT = Path.cwd()
assert (ROOT / 'assets/logo-vne-shablona.svg').is_file(), 'Run in vne-shablona'
ORIGIN = 'https://vneshablona.ru'
home = (ROOT / 'index.html').read_text(encoding='utf-8')

SERVICES = [
    dict(slug='perenos-saita-s-tilda', name='Перенос сайта с Tilda',
        title='Перенос сайта с Tilda на свой код и хостинг — ВНЕ ШАБЛОНА',
        description='Перенесём сайт с Тильды на собственный код: дизайн, формы, CMS, адреса страниц и аналитика. Уберите ограничения конструктора и развивайте сайт по своим правилам.',
        headline='Ваш сайт вырос.\nТильда — нет.',
        lead='Перенесём сайт с Tilda на собственный код и хостинг. Сохраним то, что работает, уберём ограничения конструктора и подготовим место для роста.',
        image='process-planning-v2.webp', width=1620, height=971,
        alt='Иллюстрация мастерской: проектирование страниц и связей будущего сайта',
        intro='Сайт должен расти вместе с бизнесом',
        problem='Новая услуга не помещается в старую структуру. Каталог приходится собирать из обходных решений. Изменение формы требует ещё одного сервиса. Если каждый следующий шаг упирается в возможности платформы, пора менять основу сайта.',
        scope=[('Дизайн без рамок блоков', 'Перенесём узнаваемый образ бренда или создадим новый интерфейс. Отдельно проработаем телефон: меню, каталог, формы и путь до обращения.'),
               ('Контент под вашим управлением', 'Для услуг, товаров, кейсов и новостей настроим нужные поля в CMS. Для небольшого сайта без частых обновлений можно обойтись без отдельной админки.'),
               ('Заявки без привязки к конструктору', 'Пересоберём формы и доставку обращений, подключим согласованные CRM, почту или Telegram. Проверим не только кнопку, но и получение заявки.'),
               ('Основа для поиска', 'Составим карту старых и новых URL, перенесём заголовки и метаданные, проверим ссылки, sitemap и доступность страниц для поисковиков.')],
        feature_title='Экспорт ZIP ещё не означает независимый сайт',
        feature='У Тильды есть экспорт кода, но некоторые функции остаются связаны с платформой: приём форм, управление каталогом, потоки и личный кабинет. Поэтому сначала разбираемся, что именно использует ваш сайт. Затем выбираем: достаточно переноса страниц или нужна пересборка функций на своей стороне.',
        feature_link='https://help-ru.tilda.cc/export', feature_label='Ограничения экспорта в документации Tilda',
        process=[('Разобрать текущий сайт', 'Страницы, формы, каталог, внешние сервисы, посещаемые URL и доступы. Фиксируем, что сохраняем, что переделываем и от чего можно отказаться.'),
                 ('Собрать новую версию', 'Разрабатываем сайт отдельно от действующего. Переносим материалы, настраиваем управление и проверяем сценарии на компьютере и телефоне.'),
                 ('Переключить и проверить', 'Готовим резервную копию и план возврата. После переключения домена проверяем страницы, обращения, аналитику и перенаправления.')],
        pricing='На стоимость влияют количество типов страниц, каталог, CMS, формы и интеграции. Для оценки пришлите адрес сайта и расскажите, что сейчас мешает. Сравним разовую пересборку и регулярные расходы: тарифы, дополнительные сервисы и дальнейшие доработки.',
        faq=[('Можно сохранить дизайн сайта на Тильде?', 'Да. Сначала определим, какие элементы важно сохранить: композицию, типографику, иллюстрации и узнаваемые детали. Затем перенесём их в собственный интерфейс и отдельно проверим мобильную версию. При необходимости обновим структуру и дизайн в рамках того же проекта.'),
             ('Будут ли работать формы после переноса с Tilda?', 'Обработку заявок подключаем и проверяем отдельно. Экспорт страниц сам по себе не заменяет сервис приёма данных. До запуска согласуем получателя, состав полей и маршрут обращения, затем проверим доставку и обработку ошибок.'),
             ('Можно оставить домен и адреса страниц?', 'Домен можно сохранить, если у вас есть доступ к его управлению. Для полезных страниц стараемся сохранить URL. Если структура меняется, составляем карту адресов и настраиваем постоянные перенаправления со старых страниц на соответствующие новые.'),
             ('Как будет обновляться сайт без конструктора?', 'Зависит от частоты изменений. Небольшой сайт можно обновлять через разработчика. Если вы регулярно меняете услуги, товары или статьи, подключим CMS с полями под ваш контент и покажем, как ей пользоваться.'),
             ('Не пропадут ли позиции после переезда?', 'Переезд готовим по карте URL: переносим полезный контент, заголовки и метаданные, проверяем редиректы и внутренние ссылки. После запуска наблюдаем индексацию и доступные поисковые показатели. Смена платформы сама по себе не обещает роста позиций.')],
        cta='Обсудить перенос с Tilda'),
    dict(slug='pererabotka-saita-na-wordpress', name='Переработка сайта на WordPress',
        title='Перенос с WordPress на собственный сайт — ВНЕ ШАБЛОНА',
        description='Переработаем сайт на WordPress: уберём зависимость от темы и плагинов, перенесём контент, формы и каталог. Собственный код, понятная CMS и подготовленный переезд.',
        headline='Бизнес растёт.\nПлагины мешают?',
        lead='Пересоберём сайт на WordPress на собственном коде. Уберём цепочку лишних плагинов, ускорим страницы и вернём вам контроль над развитием сайта.',
        image='process-build-v2.webp', width=1583, height=994,
        alt='Иллюстрация мастерской: разработчик собирает собственный сайт за рабочим столом',
        intro='Хватит чинить сайт после каждого обновления',
        problem='Тема держит дизайн в своих рамках. Плагины конфликтуют, а отключить один страшно: неизвестно, что перестанет работать. Постоянные обновления и исправления съедают время. Разберём зависимости и соберём нужные функции в понятную систему.',
        scope=[('Контент и каталог', 'Перенесём страницы, записи, изображения и данные каталога. Разделим полезный контент, технические дубли и устаревшие материалы до запуска новой версии.'),
               ('Своя логика сайта', 'Формы, поиск, фильтры и внешние сервисы проектируем под ваши задачи. Каждая функция получает понятное назначение вместо очередного универсального плагина.'),
               ('Управление для вашей команды', 'Настроим CMS с нужными полями, черновиками и правами доступа. Редактор сможет менять контент без доступа к коду и серверным настройкам.'),
               ('Подготовленный переезд', 'Сопоставим URL, перенесём метаданные и настроим необходимые редиректы. Проверим карточки, документы, обращения и мобильные сценарии.')],
        feature_title='Меньше лишних зависимостей — меньше точек для атаки',
        feature='Устаревшие версии PHP, WordPress, тем и плагинов требуют внимания к безопасности. При пересборке можно убрать публичный PHP-движок и его расширения, отделить управление контентом от публичных страниц и ограничить доступ редакторов. Для новой системы определяем порядок обновлений, резервных копий и восстановления.',
        feature_link='https://developer.wordpress.org/advanced-administration/security/hardening/', feature_label='Рекомендации WordPress по защите сайта',
        process=[('Разобрать зависимости', 'Проверяем список функций и плагинов, типы контента, формы и внешние подключения. Составляем план замены и карту страниц.'),
                 ('Пересобрать нужное', 'Разрабатываем интерфейс и управление контентом. Переносим материалы, подключаем интеграции и проверяем права доступа.'),
                 ('Переехать под контролем', 'Делаем резервную копию, готовим переключение и возможность возврата. После публикации проверяем ключевые URL, формы и поисковую доступность.')],
        pricing='Цена зависит от функций, а не только от числа страниц: каталог и фильтры, личные кабинеты, формы, импорт данных и интеграции оцениваются отдельно. Пришлите ссылку и опишите, что ломается или ограничивает развитие. Подготовим состав работ и смету.',
        faq=[('Вы просто переносите WordPress на другой хостинг?', 'Эта услуга — пересборка сайта на собственном коде с переносом нужных материалов и функций. Смена хостинга сама по себе не убирает зависимость от WordPress, темы и плагинов. На старте согласуем, что должно остаться и какую архитектуру использовать.'),
             ('Почему старый PHP и плагины требуют внимания?', 'Версии PHP с завершённой поддержкой больше не получают исправления безопасности. Для WordPress нужно также поддерживать актуальность ядра, темы и расширений. Перед пересборкой определяем зависимости сайта и выбираем, какие компоненты заменить, изолировать или убрать.'),
             ('Сможет ли сотрудник сам редактировать сайт?', 'Да, если подключаем CMS. Настраиваем понятные типы контента: например, услуга, товар, новость и документ. Сотрудник редактирует записи и публикует изменения в пределах своей роли. Управление сервером и кодом ему для этого не требуется.'),
             ('Можно перенести каталог и сохранить ссылки на товары?', 'Сначала изучим структуру каталога: категории, характеристики, фотографии, документы и URL. Затем подготовим импорт и проверим записи. Значимые адреса сохраняем, а для изменённых составляем соответствия и настраиваем редиректы.'),
             ('Что входит в защиту новой версии?', 'Разделение публичной части и управления, минимально необходимые права, защита форм и API, обновление зависимостей и резервные копии. Конкретный набор зависит от данных и функций проекта. Для PHP отдельно проверяем срок поддержки используемой версии по документации разработчиков.')],
        cta='Обсудить уход с WordPress'),
]

def arrow():
    return '<svg viewBox="0 0 32 24" width="32" height="24" aria-hidden="true"><path d="M2 12h26M19 3l9 9-9 9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def header():
    return '''<a class="skip-service" href="#main">К содержимому</a><header class="site-header" id="top"><div class="site-header__inner"><a class="brand" href="/" aria-label="ВНЕ ШАБЛОНА — на главную"><img src="/assets/logo-vne-shablona.svg" width="920" height="200" alt="ВНЕ ШАБЛОНА" /></a><button class="menu-toggle" type="button" aria-label="Открыть меню" aria-controls="site-nav" aria-expanded="false"><span></span><span></span><span></span></button><nav class="site-nav" id="site-nav" aria-label="Основная навигация"><a href="/uslugi/">Перенос сайта</a><a href="/#benefits">Преимущества</a><a href="/#process">Процесс</a><a href="#contact">Связаться</a><a class="site-nav__cta" href="#contact">Обсудить переезд</a></nav><a class="site-header__cta" href="#contact">Обсудить переезд</a></div></header>'''

def footer():
    return '''<footer class="site-footer"><div class="section-inner site-footer__inner"><a class="brand brand--footer" href="/" aria-label="ВНЕ ШАБЛОНА — на главную"><img src="/assets/logo-vne-shablona.svg" width="920" height="200" alt="ВНЕ ШАБЛОНА" /></a><nav aria-label="Навигация внизу страницы"><a href="/uslugi/">Перенос сайта</a><a href="/#process">Как работаем</a><a href="#contact">Обсудить проект</a><a href="/legal/">Правовые документы</a></nav><div class="site-footer__end"><p>Ваш бизнес.<br />Ваш сайт. Ваши правила.</p><p class="site-footer__credit">Дизайн и разработка — <a href="https://jakuninoleg.dev/ru">Олег Якунин ↗</a></p></div></div></footer>'''

def form(name):
    # Same existing delivery handler and consent contract as the homepage.
    form = re.search(r'<form class="contact__form".*?</form>', home, re.S).group()
    form = form.replace('aria-label="Заявка на обсуждение проекта"', 'aria-label="Заявка на перенос сайта"')
    form = form.replace('<label>Ваше имя', f'<input type="hidden" name="Направление" value="{e(name)}" /><label>Ваше имя', 1)
    form = form.replace('placeholder="Что вы хотите сделать?"', 'placeholder="Ссылка на сайт и что хочется изменить"')
    return f'''<section class="service-contact section-inner" id="contact" aria-labelledby="contact-title"><div><h2 id="contact-title">Покажите, где<br />сайту тесно</h2><p>Пришлите ссылку и расскажите, что мешает. Разберём текущий сайт, предложим вариант переезда и состав работ.</p><p class="service-contact__note">Начинаем с вашей задачи.<br />Доступы и пароли в форму не нужны.</p></div><div class="service-form">{form}</div></section>'''

def page(path, title, description, content, name, extra_graph=None, image='process-planning-v2.webp'):
    canonical=ORIGIN+path
    crumbs=[{'@type':'ListItem','position':1,'name':'Главная','item':ORIGIN+'/'}]
    if path != '/uslugi/': crumbs.append({'@type':'ListItem','position':2,'name':'Перенос сайта','item':ORIGIN+'/uslugi/'})
    crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':name,'item':canonical})
    graph=[{'@type':'WebPage','@id':canonical+'#page','url':canonical,'name':title,'description':description,'inLanguage':'ru'},
           {'@type':'BreadcrumbList','itemListElement':crumbs},
           {'@type':'Person','@id':'https://jakuninoleg.dev/#person','name':'Олег Якунин','url':'https://jakuninoleg.dev/ru'}]
    if extra_graph:graph.append(extra_graph)
    schema = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\/')
    html=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>{e(title)}</title><meta name="description" content="{e(description)}" /><link rel="canonical" href="{canonical}" /><meta name="theme-color" content="#f6ecd9" /><meta property="og:type" content="website" /><meta property="og:locale" content="ru_RU" /><meta property="og:site_name" content="ВНЕ ШАБЛОНА" /><meta property="og:title" content="{e(title)}" /><meta property="og:description" content="{e(description)}" /><meta property="og:url" content="{canonical}" /><meta property="og:image" content="{ORIGIN}/assets/{image}" /><meta name="twitter:card" content="summary_large_image" /><link rel="icon" type="image/svg+xml" href="/favicon.svg" /><link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Neucha-Regular.woff2" crossorigin /><link rel="stylesheet" href="/site.css" /><link rel="stylesheet" href="/services.css" /><link rel="stylesheet" href="/analytics.css" /><script type="application/ld+json">{schema}</script><script src="/script.js" defer></script><script src="/analytics.js" defer></script></head><body class="service-page">{header()}<main id="main">{content}{form(name)}</main>{footer()}</body></html>'''
    dest=ROOT/path.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding='utf-8')

def breadcrumbs(name=None):
    last=f'<a href="/uslugi/">Перенос сайта</a><span aria-hidden="true">/</span><span aria-current="page">{e(name)}</span>' if name else '<span aria-current="page">Перенос сайта</span>'
    return '<nav class="service-breadcrumbs section-inner" aria-label="Хлебные крошки"><a href="/">Главная</a><span aria-hidden="true">/</span>'+last+'</nav>'

def proof():
    return '''<section class="service-proof section-inner" aria-labelledby="proof-title"><div><h2 id="proof-title">Своя CMS.<br />Настоящий каталог.</h2><p>На сайте КЭМЗ продукция, категории, новости и документы управляются через OJ CMS. Редактор работает с контентом, черновиками и публикацией в одной панели.</p><a class="service-text-link" href="https://jakuninoleg.dev/ru/work/aokemz">Посмотреть работу Олега Якунина '''+arrow()+'''</a></div><figure><img src="/assets/kemz-cms.webp" width="1265" height="723" loading="lazy" alt="Панель OJ CMS сайта КЭМЗ: продукция, категории, новости и последние изменения" /><figcaption>Интерфейс управления сайтом КЭМЗ</figcaption></figure></section>'''

for s in SERVICES:
    path='/uslugi/'+s['slug']+'/'
    heading='<br />'.join(map(e,s['headline'].splitlines()))
    scopes=''.join(f'<article><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a,b in s['scope'])
    process=''.join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a,b in s['process'])
    faq=''.join(f'<details><summary>{e(a)}<span aria-hidden="true">+</span></summary><p>{e(b)}</p></details>' for a,b in s['faq'])
    other=next(o for o in SERVICES if o!=s)
    content=breadcrumbs(s['name'])+f'''<section class="service-hero section-inner" aria-labelledby="service-title"><div><h1 id="service-title">{heading}</h1><p class="service-hero__lead">{e(s['lead'])}</p><a class="pill-button" href="#contact">{e(s['cta'])} {arrow()}</a><a class="service-hero__down" href="#scope">Что входит в перенос ↓</a></div><figure><img src="/assets/{s['image']}" width="{s['width']}" height="{s['height']}" fetchpriority="high" alt="{s['alt']}" /><figcaption>{e(s['name'])} → собственный сайт</figcaption></figure></section>
    <section class="service-scope section-paper section-paper--blue" id="scope" aria-labelledby="scope-title"><div class="section-inner"><div class="service-section-intro"><h2 id="scope-title">{e(s['intro'])}</h2><p>{e(s['problem'])}</p></div><div class="service-scope__list">{scopes}</div></div></section>
    <section class="service-feature section-inner" aria-labelledby="feature-title"><h2 id="feature-title">{e(s['feature_title'])}</h2><div><p>{e(s['feature'])}</p><a class="service-text-link" href="{s['feature_link']}" target="_blank" rel="noopener noreferrer">{e(s['feature_label'])} {arrow()}</a></div></section>
    <section class="service-process section-paper section-paper--sage" aria-labelledby="move-title"><div class="section-inner"><h2 id="move-title">Сначала подготовка.<br />Потом переезд.</h2><ol>{process}</ol></div></section>
    {proof()}
    <section class="service-price section-inner" aria-labelledby="price-title"><h2 id="price-title">Сколько стоит<br />вернуть контроль?</h2><div><p>{e(s['pricing'])}</p><a class="service-text-link" href="#contact">Получить оценку {arrow()}</a></div></section>
    <section class="service-faq section-paper section-paper--blue" aria-labelledby="faq-title"><div class="section-inner service-faq__layout"><h2 id="faq-title">До того,<br />как переезжать</h2><div>{faq}</div></div></section>
    <aside class="service-related section-inner"><a href="/uslugi/{other['slug']}/">{e(other['name'])} {arrow()}</a><p>Нужен SaaS, MVP или личный кабинет? <a href="https://jakuninoleg.dev/ru/services/web-applications">Разработка веб-приложений у Олега Якунина ↗</a></p></aside>'''
    page(path,s['title'],s['description'],content,s['name'],{'@type':'Service','name':s['name'],'serviceType':s['name'],'url':ORIGIN+path,'description':s['description'],'provider':{'@id':'https://jakuninoleg.dev/#person'}},s['image'])

def service_links():
    return ''.join(f'''<a class="migration-route" href="/uslugi/{s['slug']}/"><div><h3>{e(s['name'])}</h3><p>{'Сохранить нужное, пересобрать формы и CMS, выйти из ограничений конструктора.' if i==0 else 'Разобрать зависимости, убрать лишние плагины и перенести контент на свою основу.'}</p><span class="service-text-link">Посмотреть состав работ {arrow()}</span></div><img src="/assets/{s['image']}" width="{s['width']}" height="{s['height']}" alt="" loading="lazy" /></a>''' for i,s in enumerate(SERVICES))

catalog=breadcrumbs()+'''<section class="service-catalog-intro section-inner"><h1>Перенос сайта.<br />Без чужих рамок.</h1><p>Развиваете бизнес, а сайт упирается в конструктор, тему или плагины? Перенесём его на собственный код: с нужным дизайном, понятным управлением и работающими заявками.</p></section><section class="migration-routes section-inner" aria-labelledby="routes-title"><h2 id="routes-title">Откуда будем переезжать?</h2>'''+service_links()+'''</section><section class="service-feature section-inner"><h2>Сохраняем ценное.<br />Меняем основу.</h2><div><p>Сначала разбираем текущие страницы, контент и функции. Сохраняем сильные элементы бренда, полезные адреса и материалы. Затем пересобираем то, что ограничивает развитие: структуру, формы, каталог или управление.</p><p>Домен и доступы остаются у вас. Состав работ, размещение, платные внешние сервисы и дальнейшее сопровождение обсуждаем до старта.</p></div></section>'''+proof()+'''<aside class="service-related section-inner"><p>Начинаете новый продукт? <a href="https://jakuninoleg.dev/ru/services">Лендинги, каталоги, SaaS и другие услуги Олега Якунина ↗</a></p></aside>'''
page('/uslugi/','Перенос с Tilda и WordPress на собственный сайт — ВНЕ ШАБЛОНА','Перенос сайтов с Tilda и переработка WordPress: собственный код, CMS, формы, каталог и подготовка переезда. Верните контроль над развитием сайта.',catalog,'Перенос с Tilda и WordPress',{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':s['name'],'url':ORIGIN+'/uslugi/'+s['slug']+'/'} for i,s in enumerate(SERVICES)]})

# Keep incumbent hero, art direction and approved sales claims intact.
block='''<!-- migration-start --><section class="migration-home section-paper section-paper--blue" id="migration" aria-labelledby="migration-title"><div class="section-inner"><div class="section-heading"><h2 id="migration-title">Сайт вырос из шаблона?<br />Пора переезжать.</h2><p>Перенесём нужное на собственный код. Дизайн, контент, CMS и заявки будут работать на ваш бизнес.</p></div><div class="migration-routes">'''+service_links()+'''</div><p class="migration-home__more"><a class="service-text-link" href="/uslugi/">Как устроен перенос сайта '''+arrow()+'''</a></p></div></section><!-- migration-end -->'''
home=re.sub(r'<!-- migration-start -->.*?<!-- migration-end -->', '', home, flags=re.S)
home=home.replace('<section class="process section-paper',block+'\n      <section class="process section-paper',1)
if '/services.css' not in home:home=re.sub(r'(<link rel="stylesheet" href="/site\.css[^"]*"\s*/>)',r'\1\n    <link rel="stylesheet" href="/services.css" />',home,count=1)
home=home.replace('<a href="#story">История</a>','<a href="/uslugi/">Перенос сайта</a>')
home=home.replace('Индивидуальная разработка сайтов для бизнеса — ВНЕ ШАБЛОНА','Сайт без ограничений Tilda и WordPress — ВНЕ ШАБЛОНА')
home=home.replace('Индивидуальная разработка быстрых сайтов под задачи бизнеса: свой дизайн, нужные интеграции, удобное управление и пространство для роста.','Собственный сайт вместо ограничений Tilda и WordPress: перенос, индивидуальная разработка, удобная CMS и нужные интеграции. Быстрее, гибче и под вашим контролем.')
proof_home='<!-- migration-proof-start -->'+proof()+'<!-- migration-proof-end -->'
if '<!-- migration-proof-start -->' in home:home=re.sub(r'<!-- migration-proof-start -->.*?<!-- migration-proof-end -->',lambda _:proof_home,home,flags=re.S)
else:home=home.replace('<section class="contact" id="contact"',proof_home+'\n      <section class="contact" id="contact"',1)
home='\n'.join(line.rstrip() for line in home.splitlines())+'\n'
home=re.sub(r'\n{3,}', '\n\n', home)
(ROOT/'index.html').write_text(home,encoding='utf-8')
paths=['/','/legal/','/uslugi/']+['/uslugi/'+s['slug']+'/' for s in SERVICES]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+ORIGIN+p+'</loc></url>\n' for p in paths)+'</urlset>\n',encoding='utf-8')
print('Generated',len(SERVICES)+1,'pages; homepage and sitemap updated')

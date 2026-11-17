import os, re, json, shutil, datetime, html, zlib, yaml, markdown
from urllib.parse import quote
R = os.path.dirname(os.path.abspath(__file__))
S = yaml.safe_load(open(f'{R}/site.yml', encoding='utf8'))
NOW = datetime.date.today(); TODAY = NOW.isoformat()
BASE = S['url'].rstrip('/')
P = {
 'heart': '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
 'brief': '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 'card': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
 'home': '<path d="M3 11l9-8 9 8M5 10v10h14V10"/>',
 'set': '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
 'chat': '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8z"/>',
 'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
 'ext': '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/>',
 'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
 'back': '<path d="M5 12h14M12 5l7 7-7 7"/>',
 'x': '<path d="M18 6L6 18M6 6l12 12"/>',
 'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 7L2 7"/>',
 'send': '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
 'build': '<path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6M9 11h.01M15 11h.01"/>',
 'news': '<path d="M4 4h13a1 1 0 0 1 1 1v15a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2zM18 9h2a1 1 0 0 1 1 1v10a2 2 0 0 1-2 2M8 8h6M8 12h6M8 16h6"/>',
 'cap': '<path d="M22 10L12 5 2 10l10 5 10-5zM6 12v5c3 3 9 3 12 0v-5"/>',
 'copy': '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'alert': '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0zM12 9v4M12 17h.01"/>',
 'sim': '<path d="M15 2H8a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V6z"/><path d="M10 12h4v6h-4z"/>',
 'bot': '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9zM19 3v4M17 5h4"/>',
 'book': '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
 'trend': '<path d="M3 17l6-6 4 4 8-8M15 7h6v6"/>',
 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 'library': '<path d="M4 19V5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2zM4 19a2 2 0 0 0 2 2h12M8 7h6"/>',
 'landmark': '<path d="M3 21h18M5 21V10M9 21V10M15 21V10M19 21V10M12 3l9 5H3z"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
 'archive': '<rect x="2" y="3" width="20" height="5" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8M10 12h4"/>',
}
SEC = [
 ('news', 'آخر الأخبار', 'أحدث أخبار المساعدات والتسجيل والتنبيهات المهمة.', 'news', False),
 ('aid', 'المساعدات', 'روابط تسجيل المساعدات الغذائية والمالية والطبية وغيرها.', 'heart', True),
 ('jobs', 'الوظائف', 'وظائف شاغرة لدى المؤسسات في قطاع غزة.', 'brief', True),
 ('books', 'الكتب والروايات', 'كتب وروايات سهلة التحميل والتصفح.', 'library', False),
 ('grants', 'المنح الدراسية', 'منح لطلاب التوجيهي والجامعات في قطاع غزة، بروابط التقديم الرسمية.', 'cap', True),
 ('edu', 'الرزم التعليمية', 'رزم تعليمية لطلاب غزة من الصف الأول حتى التوجيهي، للتحميل المباشر.', 'book', False),
 ('unis', 'الجامعات', 'جامعات قطاع غزة: الروابط الرسمية وطرق الالتحاق والتسجيل.', 'landmark', False),
 ('orgs', 'المؤسسات', 'تعريف بالمؤسسات العاملة وكيف تتواصل معها.', 'build', False),
 ('wallets', 'المحافظ والبنوك', 'شرح فتح واستخدام المحافظ الإلكترونية والبنوك الفلسطينية، مع روابط التحميل والتحديث.', 'card', False),
]
SHOP = [
 ('sims', 'شرائح الإنترنت', 'شرائح إسرائيلية: إلكترونية (eSIM) أو بلاستيك، بأسعار واضحة وشراء مباشر عبر واتساب.', 'sim', False),
 ('topup', 'شحن الرصيد وحزم جوال وأوريدو', 'شحن رصيد جوال وتفعيل الحزم الشهرية والأسبوعية، وتسديد الفواتير.', 'phone', False),
 ('ai', 'اشتراكات الذكاء الاصطناعي', 'اشتراكات ChatGPT وGemini وClaude وNetflix وCanva وغيرها.', 'bot', False),
]
SHOPK = {s[0] for s in SHOP}
ALL = SEC + SHOP
GATE = {'sims': [('eSIM', 'شريحة إلكترونية (eSIM)', 'بدون شريحة فعلية'), ('بلاستيك', 'شريحة بلاستيك', 'شريحة فعلية')]}
SD = {s[0]: s for s in ALL}
TILESEC = {'aid', 'topup', 'sims', 'ai', 'books'}
NUM = re.sub(r'\D', '', str(S.get('whatsapp_number') or ''))
PAYLOGOS = [('bank-of-palestine', 'بنك فلسطين'), ('palpay', 'محفظتي PalPay'), ('jawwal-pay', 'جوال باي')]
LBL = {'open': 'مفتوح', 'soon': 'قريباً', 'closed': 'مغلق'}
e = lambda x: html.escape(str(x if x is not None else ''), quote=True)
ds = lambda v: str(v)[:10] if v else ''
def ic(n, s=22): return f'<svg class="ic" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[n]}</svg>'
def read(p):
    t = open(p, encoding='utf8').read()
    m = re.match(r'---\s*\n(.*?)\n---\s*\n?(.*)', t, re.S)
    if not m: return {}, t
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)
def status(p):
    st = p.get('status')
    if st == 'open' and ds(p.get('close_date')) and ds(p['close_date']) < TODAY: st = 'closed'
    return st
def badge(p):
    st = status(p)
    return f'<span class="badge {st}" data-status="{st}" data-close="{ds(p.get("close_date"))}">{LBL[st]}</span>' if st else ''
def md(b):
    h = markdown.markdown(b, extensions=['extra', 'sane_lists'])
    return re.sub(r'src="/?assets/', 'src="@@/assets/', h)
def fix(h, pre): return h.replace('@@/', pre)
AD = lambda: (f'<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="{S["adsense_client"]}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>' if S.get('adsense_client') else '')
URLS = []
def layout(title, desc, body, pre, path, cur='', ld=None, js=False):
    body = fix(body, pre)
    full = title if title == S['full_title'] else f'{title} | {S["title"]}'
    can = BASE + '/' + path; URLS.append(can)
    def li(k, t, i, href): return f'<a href="{href}" class="{"on" if cur == k else ""} c-{k}">{ic(i,22)}<span>{t}</span></a>'
    side = li('home', 'الرئيسية', 'home', pre) + li('search', 'بحث في الموقع', 'search', pre + 'search/') + ''.join(li(k, t, i, f'{pre}{k}/') for k, t, d, i, o in SEC[:1])
    side += '<p class="gl">الأقسام</p>' + ''.join(li(k, t, i, f'{pre}{k}/') for k, t, d, i, o in SEC[1:]) + li('archive', 'الأرشيف (المغلقة)', 'archive', pre + 'archive/')
    side += '<p class="gl">المتجر</p>' + ''.join(li(k, t, i, f'{pre}{k}/') for k, t, d, i, o in SHOP)
    side += '<p class="gl">المزيد</p>' + li('warning', 'احذر من الروابط المزيفة', 'alert', pre + 'warning/') + li('settings', 'الإعدادات', 'set', pre + 'settings/') + li('contact', 'طرق التواصل', 'chat', pre + 'contact/') + li('terms', 'سياسة الاستخدام', 'file', pre + 'terms/') + li('refund', 'الضمان والاسترجاع', 'shield', pre + 'refund/') + li('privacy', 'سياسة الخصوصية', 'shield', pre + 'privacy/') + li('about', 'من نحن', 'info', pre + 'about/')
    ads = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={S["adsense_client"]}" crossorigin="anonymous"></script>' if S.get('adsense_client') else ''
    schema = ''
    if ld: schema = '<script type="application/ld+json">' + json.dumps([dict({'@context': 'https://schema.org'}, **x) for x in ld], ensure_ascii=False).replace('</', '<\\/') + '</script>'
    guard = f'<script src="{pre}assets/guard.js"></script>' if S.get('protect', True) else ''
    sjs = f'<script src="{pre}assets/search.js"></script>' if js else ''
    backbtn = '' if cur == 'home' else f'<a id="back" class="ib" href="{pre}" aria-label="رجوع">{ic("back",22)}<span>رجوع</span></a>'
    return f'''<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try{{var d=document.documentElement,t=localStorage.getItem("theme"),f=localStorage.getItem("fs");if(t)d.dataset.theme=t;if(f)d.dataset.fs=f;if(localStorage.getItem("sb")==="off")d.dataset.sb="off"}}catch(e){{}}</script>
{guard}<title>{e(full)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{e(can)}">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:locale" content="ar_AR"><meta property="og:site_name" content="{e(S["title"])}"><meta property="og:url" content="{e(can)}"><meta name="theme-color" content="#0b7a75"><meta name="referrer" content="strict-origin-when-cross-origin"><meta http-equiv="Content-Security-Policy" content="object-src 'none'; base-uri 'self'; form-action 'self'"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{pre}assets/favicon.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="{pre}assets/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/style.css">{schema}{ads}</head><body data-root="{pre}">
<aside id="side" class="side"><div class="sh"><a class="logo" href="{pre}">{e(S["title"])}</a><button class="ib x" id="close" aria-label="إغلاق القائمة">{ic("x",22)}</button></div><nav aria-label="القائمة الرئيسية">{side}</nav></aside>
<div id="ov" class="ov"></div>
<div class="shell"><header class="top"><button class="ib" id="menu" aria-label="فتح أو إغلاق القائمة" aria-expanded="false">{ic("menu",24)}</button>{backbtn}<a class="tt" href="{pre}">{e(S["title"])}</a><a class="ib" href="{pre}search/" aria-label="بحث">{ic("search",22)}</a></header>
<main class="wrap">{body}</main>
<footer class="foot"><p>© {NOW.year} {e(S["full_title"])}. جميع الحقوق محفوظة. يمنع نسخ المحتوى أو إعادة نشره دون إذن.</p><p>موقع مستقل لا يمثل أي مؤسسة. الأسماء والشعارات لأصحابها وتُعرض للتعريف فقط. <a href="{pre}terms/">سياسة الاستخدام</a> · <a href="{pre}refund/">الضمان والاسترجاع</a> · <a href="{pre}privacy/">الخصوصية</a> · <a href="{pre}warning/">احذر من الروابط المزيفة</a></p></footer></div>
<script src="{pre}assets/app.js"></script>{sjs}</body></html>'''
def card(p):
    s = SD.get(p['section'], SEC[1]); cur = p.get('currency') or S.get('currency') or 'شيكل'
    txt = f'{p["title"]} {p.get("org","")} {p.get("category","")} {p.get("aid","")} {s[1]} {p["id"]}'
    if p['section'] in SHOPK:
        pr = ''.join(f'<span>{l}: <b>{e(p[k])} {e(cur)}</b>{(" <s>بدل " + e(p["old_price"]) + "</s>") if k == "price1" and p.get("old_price") else ""}</span>' for l, k in [('شهر' if p['section'] == 'sims' else 'السعر', 'price1'), ('3 شهور', 'price3')] if p.get(k))
        if not pr and p.get('price_text'): pr = f'<span><b>{e(p["price_text"])}</b></span>'
        return f'''<a class="card prod c-{s[0]}" href="@@/{p["path"]}/" data-cat="{e(p.get("category",""))}" data-text="{e(txt)}">
<div class="ph"><span class="av sm">{org_av(p)}</span><div><h3>{e(p["title"])}</h3><small>{e(p.get("org",""))}</small></div></div>{"<div class='prices'>"+pr+"</div>" if pr else "<div class='prices'><span>الأسعار والباقات قريباً</span></div>"}<div class="meta"><span>{e(p.get("category",""))}</span></div></a>'''
    return f'''<a class="card c-{s[0]}" href="@@/{p["path"]}/" data-cat="{e(p.get("category",""))}" data-text="{e(txt)}">
<h3><span class="mini">{ic(s[3],20)}</span>{e(p["title"])}</h3><p>{e(p.get("summary") or p.get("aid") or "")}</p>
<div class="meta">{badge(p)}{"<span class='badge tag'>"+e(p["tag"])+"</span>" if p.get("tag") else ""}<span>{e(p.get("org",""))}</span><span>{s[1]}</span></div></a>'''
def org_av(p):
    nm = p.get('org') or p['title']
    if p.get('logo'): return f'<img src="@@/{str(p["logo"]).lstrip("/")}" alt="{e(nm)}" loading="lazy">'
    return e(re.sub(r'^ال', '', nm.strip())[:1])
def org_cls(p): return 'c-' + list(SD)[zlib.crc32((p.get('org') or p['title']).encode()) % len(SD)]
def org_tile(p):
    nm = p.get('org') or p['title']
    return f'<a class="org {org_cls(p)}" href="@@/{p["path"]}/" data-text="{e(nm)} {p["id"]}"><span class="av">{org_av(p)}</span><b>{e(nm)}</b></a>'
def ptile(p):
    s = SD.get(p['section'], SEC[1]); cur = p.get('currency') or S.get('currency') or 'شيكل'
    o = org_of(p) if p['section'] != 'orgs' else None
    nm = p.get('short') or p['title']
    if p.get('logo'): av = org_av(p)
    elif o and o.get('logo'): av = org_av(o)
    else: av = ic(s[3], 26)
    price = ''
    if p.get('price1'): price = f'<span class="pr"><b>{e(p["price1"])} {e(cur)}</b>' + (f' <s>بدل {e(p["old_price"])}</s>' if p.get('old_price') else '') + '</span>'
    elif p.get('price_text'): price = f'<span class="pr">{e(p["price_text"])}</span>'
    tg = f'<span class="badge tag">{e(p["tag"])}</span>' if p.get('tag') else ''
    sub = ''
    if p['section'] in SHOPK and NUM:
        msg = 'مرحباً، أريد الاشتراك في: ' + p['title'] + chr(10) + BASE + '/' + p['path'] + '/'
        sub = f'<a class="sub" href="https://wa.me/{NUM}?text={quote(msg)}" target="_blank" rel="noopener">{ic("chat",16)}للاشتراك اضغط هنا</a>'
    txt = f'{p["title"]} {p.get("org","")} {p.get("category","")} {p.get("aid","")} {s[1]} {p["id"]}'
    return f'<div class="ptile c-{s[0]}" data-cat="{e(p.get("category",""))}" data-text="{e(txt)}"><a class="pt" href="@@/{p["path"]}/"><span class="av">{av}</span><b>{e(nm)}</b>{price}<span class="pm">{badge(p)}{tg}</span></a>{sub}</div>'
def payhtml():
    return '<div class="pay"><b>طرق الدفع المتوفرة</b><div class="paylogos">' + ''.join(f'<span class="pl"><img src="@@/assets/img/{f}.webp" alt="{n}" loading="lazy"><small>{n}</small></span>' for f, n in PAYLOGOS) + '</div><p>تُرسل لك تفاصيل الدفع عبر واتساب عند تأكيد الطلب.</p></div>'
def write(path, content):
    fp = os.path.join(R, path); os.makedirs(os.path.dirname(fp) or R, exist_ok=True)
    open(fp, 'w', encoding='utf8').write(content)
def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}

man = os.path.join(R, '.built.json')
if os.path.exists(man):
    for d in json.load(open(man)): shutil.rmtree(os.path.join(R, d), ignore_errors=True)
built = []; posts = []; used = set()
for f in sorted(os.listdir(f'{R}/content/posts')):
    if not f.endswith('.md'): continue
    d, b = read(f'{R}/content/posts/{f}')
    d['slug'] = f[:-3]; d['body'] = b; d['section'] = d.get('section') or 'aid'
    d['date'] = ds(d.get('date')) or '2000-01-01'
    n = int(d['id']) if d.get('id') else zlib.crc32(d['slug'].encode()) % 9000 + 1000
    while n in used: n += 1
    used.add(n); d['id'] = n; d['path'] = f'{d["slug"]}-{n}'
    posts.append(d)
posts.sort(key=lambda x: x['date'], reverse=True)
orgs = [p for p in posts if p['section'] == 'orgs']
by_slug = {p['slug']: p for p in orgs}; by_name = {p.get('org'): p for p in orgs if p.get('org')}
def org_of(p):
    if p['section'] == 'orgs': return None
    return by_slug.get(p.get('of')) or by_name.get(p.get('org'))
progs = {}
for p in posts:
    o = org_of(p)
    if o: progs.setdefault(o['slug'], []).append(p)
visible = [p for p in posts if status(p) != 'closed']
closed = sorted([p for p in posts if status(p) == 'closed'], key=lambda x: ds(x.get('close_date')) or x['date'], reverse=True)
search = '<input id="q" type="search" placeholder="ابحث بالاسم أو النوع أو رقم المنشور" aria-label="بحث">'
gsearch = '<div class="sbox"><input id="gq" data-gs="drop" type="search" placeholder="ابحث في كل الموقع: مؤسسة، وظيفة، مساعدة، رقم، رابط..." aria-label="بحث في الموقع" autocomplete="off"><div class="sdrop" id="gdrop" hidden></div></div>'
lsearch = search + f'<a class="gsl" id="gsl" href="@@/search/">{ic("search",16)}بحث في كل الموقع</a>'
note = f'<a class="note" href="@@/warning/">{ic("alert",20)}<span>احذر من الروابط المزيفة: ادخل فقط من الروابط الرسمية. تعرّف كيف تتحقق.</span></a>'
tiles = ''.join(f'<a class="tile c-{k}" href="@@/{k}/"><span class="ico">{ic(i,26)}</span><b>{t}</b></a>' for k, t, d, i, o in ALL)
tiles += (f'<a class="tile c-contact" href="{e(S["whatsapp"])}" target="_blank" rel="noopener"><span class="ico">{ic("chat",26)}</span><b>واتساب</b></a>' if S.get('whatsapp') else '') + (f'<a class="tile c-contact" href="{e(S["telegram"])}" target="_blank" rel="noopener"><span class="ico">{ic("send",26)}</span><b>تيليجرام</b></a>' if S.get('telegram') else '')
opn = [p for p in visible if status(p) == 'open' and p['section'] in ('aid', 'jobs', 'grants')][:6]
home = f'<section class="hero home"><h1>{S["full_title"]}</h1><p>{S["description"]}</p>{gsearch}</section>{note}<section class="tiles">{tiles}</section>'
if opn: home += '<h2 class="h">مفتوح للتسجيل الآن</h2><section class="grid">' + ''.join(card(p) for p in opn) + '</section>'
home += '<h2 class="h">آخر المنشورات</h2><section class="grid" id="list">' + (''.join(card(p) for p in [x for x in visible if x['section'] not in SHOPK][:12]) or '<p class="empty">لا يوجد منشورات بعد.</p>') + '</section>'
home_ld = [{'@type': 'WebSite', 'name': S['title'], 'alternateName': S['full_title'], 'url': BASE + '/', 'inLanguage': 'ar'},
           {'@type': 'Organization', 'name': S['title'], 'url': BASE + '/', 'sameAs': [x for x in [S.get('telegram'), S.get('facebook'), S.get('instagram')] if x]}]
write('index.html', layout(S['full_title'], S['description'], home, '', '', 'home', home_ld, True))
for k, t, d, i, o in ALL:
    items = sorted([p for p in visible if p['section'] == k], key=lambda p: p.get('order') or 9999)
    chips = ''
    if k == 'aid': chips += '<button class="chip on" data-cat="">الكل</button>' + ''.join(f'<button class="chip" data-cat="{c}">{c}</button>' for c in ['غذائية', 'مالية', 'طبية', 'تعليمية', 'إيواء', 'غاز'])
    if k in ('grants', 'edu', 'topup', 'books'):
        cs = []
        for p in items:
            if p.get('category') and p['category'] not in cs: cs.append(p['category'])
        chips += '<button class="chip on" data-cat="">الكل</button>' + ''.join(f'<button class="chip" data-cat="{c}">{c}</button>' for c in cs)
    if o: chips += '<button class="chip open-only" aria-pressed="false">مفتوح الآن فقط</button>'
    cards = ''.join(card(p) + (AD() if n == 3 else '') for n, p in enumerate(items)) or '<p class="empty">لا يوجد منشورات بهذا القسم حالياً.</p>'
    if k in TILESEC: cards = ''.join(ptile(p) for p in items) or '<p class="empty">لا يوجد منشورات بهذا القسم حالياً.</p>'
    strip = '<h2 class="h">المؤسسات</h2><section class="orgs">' + ''.join(org_tile(p) for p in orgs) + '</section>' if orgs and k in ('aid', 'orgs') else ''
    if k == 'orgs' and orgs: cards = ''
    wl = [p for p in visible if p['section'] == 'wallets']
    if k == 'wallets' and wl:
        strip = '<section class="orgs">' + ''.join(org_tile(p) for p in wl) + '</section>'; cards = ''
    ul = [p for p in visible if p['section'] == 'unis']
    if k == 'unis' and ul:
        strip = '<section class="orgs">' + ''.join(org_tile(p) for p in ul) + '</section>'; cards = ''
    gate = GATE.get(k)
    if gate: chips = '<div class="choices">' + ''.join(f'<button class="chip choice" data-cat="{c}"><b>{t_}</b><small>{s_}</small></button>' for c, t_, s_ in gate) + '</div>'
    gmsg = '<p class="gatemsg" id="gatemsg">اختر نوع الشريحة لعرض الباقات والأسعار.</p>' if gate else ''
    shopnote = f'<div class="note shopnote">{ic("info",20)}<span>قسم المتجر منفصل عن قسم المساعدات: الشراء بينك وبين الموقع مباشرة عبر واتساب، ولا علاقة له بأي مؤسسة إغاثية. نحن غير تابعين للشركات المذكورة، والأسماء والشعارات لأصحابها.</span></div>' if k in SHOPK else ''
    body = f'<section class="hero c-{k}"><h1><span class="ico">{ic(i,26)}</span>{t}</h1><p>{d}</p>{lsearch}<div class="chips">{chips}</div>{shopnote}</section>{payhtml() if k in SHOPK else ""}<div class="none" id="none" hidden>ما في نتائج.</div>{strip}{gmsg}<section class="{"ptiles" if k in TILESEC else "grid"}" id="list"{" data-gate=1" if gate else ""}>{cards}</section>'
    write(f'{k}/index.html', layout(t, d, body, '../', f'{k}/', k, [crumbs([('الرئيسية', BASE + '/'), (t, f'{BASE}/{k}/')])])); built.append(k)
# الأرشيف
acards = ''.join(card(p) for p in closed) or '<p class="empty">لا يوجد منشورات مغلقة حالياً.</p>'
body = f'<section class="hero c-archive"><h1><span class="ico">{ic("archive",26)}</span>الأرشيف (المغلقة)</h1><p>روابط انتهى تسجيلها. نحتفظ بها للرجوع إليها، قد يُعاد فتحها لاحقاً.</p>{lsearch}</section><div class="none" id="none" hidden>ما في نتائج.</div><section class="grid" id="list">{acards}</section>'
write('archive/index.html', layout('الأرشيف (المغلقة)', 'روابط المساعدات والوظائف والفرص التي انتهى تسجيلها في قطاع غزة.', body, '../', 'archive/', 'archive')); built.append('archive')
for p in posts:
    s = SD.get(p['section'], SEC[1]); can = f'{BASE}/{p["path"]}/'; st = status(p)
    o = org_of(p); facts = ''
    if p['section'] != 'orgs' and p.get('org'):
        facts += '<div><dt>' + ('الشركة' if p['section'] in SHOPK else ('المؤلف' if p['section'] == 'books' else 'المؤسسة')) + '</dt><dd>' + (f'<a href="@@/{o["path"]}/">{e(p["org"])}</a>' if o else e(p['org'])) + '</dd></div>'
    facts += ''.join(f'<div><dt>{a}</dt><dd>{e(p[b])}</dd></div>' for a, b in [('نوع المساعدة', 'aid'), ('المستفيدون', 'beneficiaries')] if p.get(b))
    if p.get('close_date'): facts += f'<div><dt>آخر موعد</dt><dd>{ds(p["close_date"])}</dd></div>'
    l2 = f'<a class="btn alt" href="{e(p["link2"])}" target="_blank" rel="noopener nofollow">{ic("ext",20)}{e(p.get("link2_label") or "تحديث البيانات")}</a>' if p.get('link2') else ''
    go = f'<div class="go"><a class="btn" href="{e(p["link"])}" target="_blank" rel="noopener nofollow">{ic("ext",20)}{e(p.get("link_label") or "اضغط هنا للانتقال للرابط الرسمي")}</a>{l2}<small>تأكد أن الرابط يطابق الموقع الرسمي للمؤسسة قبل إدخال بياناتك.</small></div>' if p.get('link') else ''
    bx = ''.join(f'<a class="btn alt" href="{e(b.get("url"))}" target="_blank" rel="noopener nofollow">{ic("ext",20)}{e(b.get("label") or "رابط")}</a>' for b in (p.get('buttons') or []) if isinstance(b, dict) and b.get('url'))
    if bx: go = go.replace('<small>', bx + '<small>', 1) if go else f'<div class="go">{bx}<small>تأكد أن الروابط تابعة للجهة الرسمية قبل إدخال بياناتك.</small></div>'
    shop = p['section'] in SHOPK; cur = p.get('currency') or S.get('currency') or 'شيكل'
    pbox = ''
    if shop and (p.get('price1') or p.get('price3')):
        pbox = '<div class="pbox">' + (f'<div><span>{"شهر واحد" if p["section"] == "sims" else "السعر"}</span><b>{e(p["price1"])} {e(cur)}{" <s>بدل " + e(p["old_price"]) + "</s>" if p.get("old_price") else ""}</b></div>' if p.get('price1') else '') + (f'<div><span>3 شهور</span><b>{e(p["price3"])} {e(cur)}</b></div>' if p.get('price3') else '') + '</div>'
    if shop and p.get('price_text') and not pbox: pbox = f'<div class="pbox"><div><span>السعر</span><b>{e(p["price_text"])}</b></div></div>'
    sp = p.get('specs')
    if isinstance(sp, str): sp = [x.strip() for x in sp.split('\n') if x.strip()]
    spl = '<h2 class="h">المواصفات</h2><ul class="specs">' + ''.join(f'<li>{e(x)}</li>' for x in sp) + '</ul>' if shop and sp else ''
    num = re.sub(r'\D', '', str(S.get('whatsapp_number') or ''))
    if shop and not num: print('تنبيه: whatsapp_number فارغ في site.yml، زر الشراء غير ظاهر')
    msg = f'مرحباً، أريد شراء: {p["title"]}' + (f'\nالسعر: شهر {p["price1"]} {cur}' if p.get('price1') else '') + (f' / 3 شهور {p["price3"]} {cur}' if p.get('price3') else '') + f'\nالرابط: {can}'
    buy = f'<div class="go"><a class="btn buy" href="https://wa.me/{num}?text={quote(msg)}" target="_blank" rel="noopener">{ic("chat",20)}شراء / تواصل للشراء عبر واتساب</a><small>سيتم تحويلك لمحادثة واتساب مباشرة معنا.</small></div>' if shop and num else ''
    if shop or p.get('pay'): buy = payhtml() + buy
    closed_note = f'<div class="note closed-note">{ic("alert",20)}<span>هذا التسجيل مغلق حالياً. تابع الموقع أو قناتنا لمعرفة أي موعد جديد.</span></div>' if st == 'closed' else ''
    pr = progs.get(p['slug'], []) if p['section'] == 'orgs' else []
    prl = '<section class="rel prog"><h2>برامج وروابط المؤسسة</h2><div class="grid">' + ''.join(card(x) for x in pr) + '</div></section>' if pr else ''
    rel = [x for x in visible if x['section'] == p['section'] and x['path'] != p['path']][:3]
    rl = '<section class="rel"><h2>اقرأ أيضاً</h2>' + ''.join(f'<a href="@@/{x["path"]}/">{e(x["title"])}</a>' for x in rel) + '</section>' if rel else ''
    sub = quote('بلاغ عن رابط: ' + p['title']); bd = quote(f'رابط الصفحة: {can}\nوصف المشكلة: ')
    wa = e('https://wa.me/?text=' + quote(p['title'] + ' ' + can)); tg = e('https://t.me/share/url?url=' + quote(can) + '&text=' + quote(p['title']))
    share = f'''<div class="share"><b>شارك المنشور مع من يحتاجه</b><div class="srow"><a class="sb" data-share="wa" href="{wa}" target="_blank" rel="noopener">{ic("chat",20)}واتساب</a><a class="sb" data-share="tg" href="{tg}" target="_blank" rel="noopener">{ic("send",20)}تيليجرام</a><button class="sb" data-copy type="button">{ic("copy",20)}<span>نسخ الرابط</span></button></div>
<p class="rep">الرابط مغلق أو مشبوه؟ <a href="mailto:{e(S["email"])}?subject={sub}&amp;body={bd}">أبلغ عنه</a> · <a href="@@/warning/">كيف تتحقق من الروابط</a></p></div>'''
    lg = f'<div class="olg {org_cls(p)}"><span class="av">{org_av(p)}</span></div>' if (p.get('logo') or p['section'] == 'orgs') else ''
    body = f'''<article class="article c-{s[0]}"><p class="crumb"><a href="@@/">الرئيسية</a> / <a href="@@/{s[0]}/">{s[1]}</a></p><h1>{e(p["title"])}</h1>{lg}
<div class="meta">{badge(p)}{"<span class='badge tag'>"+e(p["tag"])+"</span>" if p.get("tag") else ""}{"<span>تم التحقق: "+ds(p["verified"])+"</span>" if p.get("verified") else ""}<span>نُشر: {p["date"]}</span><span>رقم المنشور: {p["id"]}</span></div>
{closed_note}{pbox}{"<dl class='facts'>"+facts+"</dl>" if facts else ""}{spl}<div class="body">{md(p["body"])}</div>{buy}{AD()}{go}{share}{prl}{rl}</article>'''
    art = {'@type': 'Article', 'headline': p['title'], 'description': p.get('summary') or p['title'], 'inLanguage': 'ar', 'datePublished': p['date'], 'dateModified': ds(p.get('verified')) or p['date'],
           'mainEntityOfPage': can, 'author': {'@type': 'Organization', 'name': S['title']}, 'publisher': {'@type': 'Organization', 'name': S['title'], 'url': BASE + '/'}}
    if p.get('logo'): art['image'] = BASE + '/' + str(p['logo']).lstrip('/')
    ld = [art, crumbs([('الرئيسية', BASE + '/'), (s[1], f'{BASE}/{s[0]}/'), (p['title'], can)])]
    if shop and re.fullmatch(r'\d+(\.\d+)?', str(p.get('price1') or '')) and cur in ('شيكل', 'ILS'):
        ld.append({'@type': 'Product', 'name': p['title'], 'description': p.get('summary') or p['title'], 'brand': {'@type': 'Brand', 'name': p.get('org') or S['title']},
                   'offers': {'@type': 'Offer', 'price': str(p['price1']), 'priceCurrency': 'ILS', 'availability': 'https://schema.org/InStock', 'url': can}})
    if p['section'] == 'jobs' and p.get('org'):
        jp = {'@type': 'JobPosting', 'title': p['title'], 'description': p.get('summary') or p['title'], 'datePosted': p['date'], 'hiringOrganization': {'@type': 'Organization', 'name': p['org']},
              'jobLocation': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressRegion': 'Gaza Strip', 'addressCountry': 'PS'}}, 'url': can}
        if p.get('close_date'): jp['validThrough'] = ds(p['close_date'])
        ld.append(jp)
    write(f'{p["path"]}/index.html', layout(p['title'], p.get('summary') or p['title'], body, '../', f'{p["path"]}/', p['section'], ld)); built.append(p['path'])
for f in sorted(os.listdir(f'{R}/content/pages')):
    d, b = read(f'{R}/content/pages/{f}'); sl = f[:-3]; extra = ''
    if sl == 'warning':
        extra = f'<h2 id="report">أبلغ عن رابط مشبوه</h2><p>أرسل لنا الرابط ومن أين وصلك، وسنراجعه ونحذّر منه عند الحاجة.</p><div class="go"><a class="btn" href="mailto:{e(S["email"])}?subject={quote("بلاغ عن رابط مشبوه")}&amp;body={quote("الرابط المشبوه: ")}%0A{quote("من أين وصلك؟ ")}">{ic("mail",20)}أبلغ بالبريد</a><a class="btn alt" href="{e(S["telegram"])}" target="_blank" rel="noopener">{ic("send",20)}أبلغ عبر تيليجرام</a></div>'
    write(f'{sl}/index.html', layout(d.get('title', sl), S['description'], f'<article class="article"><h1>{e(d.get("title",""))}</h1><div class="body">{md(b)}{extra}</div></article>', '../', f'{sl}/', sl)); built.append(sl)
rows = ''
for key, lab, i, href in [('email', 'راسلنا بالبريد', 'mail', 'mailto:' + str(S.get('email', ''))), ('telegram', 'قناتنا على تيليجرام', 'send', S.get('telegram')), ('whatsapp', 'واتساب', 'chat', S.get('whatsapp')), ('facebook', 'فيسبوك', 'chat', S.get('facebook')), ('instagram', 'إنستغرام', 'chat', S.get('instagram'))]:
    if S.get(key): rows += f'<a class="row" href="{e(href)}" target="_blank" rel="noopener"><span class="ico">{ic(i,24)}</span><span><b>{lab}</b><small>اضغط هنا</small></span></a>'
write('contact/index.html', layout('طرق التواصل', 'تواصل معنا للإبلاغ عن رابط أو لاقتراح مؤسسة.', f'<article class="article"><h1>طرق التواصل</h1><p>للإبلاغ عن رابط مغلق أو مزيف أو لاقتراح مؤسسة جديدة:</p><div class="rows">{rows}</div></article>', '../', 'contact/', 'contact')); built.append('contact')
def opts(attr, items): return ''.join(f'<button class="chip" data-{attr}="{v}" aria-pressed="false">{l}</button>' for v, l in items)
st_ = f'''<article class="article"><h1>الإعدادات</h1><p>تُحفظ إعداداتك على جهازك فقط.</p>
<h2 class="h">المظهر</h2><div class="chips">{opts("theme", [("", "تلقائي"), ("light", "فاتح"), ("dark", "داكن")])}</div>
<h2 class="h">حجم الخط</h2><div class="chips">{opts("fs", [("s", "صغير"), ("", "متوسط"), ("l", "كبير")])}</div></article>'''
write('settings/index.html', layout('الإعدادات', 'إعدادات المظهر وحجم الخط.', st_, '../', 'settings/', 'settings')); built.append('settings')
SYN = [['وظائف','وظيفه','شغل','عمل','توظيف','jobs','job','vacancy','vacancies','career'],['مساعدات','مساعده','اغاثه','اغاثة','aid','relief','assistance','support'],['منح','منحه','منحة','scholarship','scholarships','grant'],['الاونروا','اونروا','وكاله الغوث','unrwa'],['الاغذيه العالمي','الغذاء العالمي','برنامج الاغذيه','wfp','world food programme'],['نقديه','نقدية','كاش','cash','شيكل','shekel','nis'],['ايتام','يتيم','كفاله ايتام','orphan','orphans'],['ارامل','ارمله','widow','widows'],['حوامل','مرضعات','حامل','pregnant','nursing'],['غاز','جره الغاز','gas','cooking gas'],['محفظه','محافظ','wallet','wallets','جوال باي','jawwal pay','palpay'],['كسوه','ملابس','clothes','clothing'],['طرد','طرود','كرتونه','كراتين','parcel','parcels','food parcel'],['تسجيل','سجل','register','registration','apply','تقديم'],['تحديث','تعديل بيانات','update'],['مؤسسه','جمعيه','منظمه','هيئه','organization','organisation','ngo','association'],['تدريب','دوره','training','course'],['طلاب','جامعات','توجيهي','student','students','university'],['خيام','شوادر','ايواء','shelter','tents'],['ذوي الاعاقه','اعاقه','disability','disabled']]
SYN += [['حزمه','حزم','باقه','باقات','bundle','bundles','package','plan'],['شحن','رصيد','تعبئه','topup','recharge','credit'],['فواتير','فاتوره','تسديد','سداد','bill','bills','payment'],['جوال','jawwal','paltel'],['اوريدو','ooredoo','وطنيه','wataniya'],['دقائق','دقيقه','رسائل','رساله','minutes','sms','messages']]
SYN += [['كتب','كتاب','روايات','رواية','book','books','novel','pdf'],['جامعه','جامعات','كليه','university','college','moodle','مودل','قبول']]
SYN += [g for g in (S.get('synonyms') or []) if isinstance(g, list)]
POP = S.get('popular') or ['مساعدات نقدية', 'وظائف', 'أيتام', 'الأونروا', 'WFP', 'محفظة إلكترونية']
TASH = re.compile('[\u064B-\u065F\u0670\u0640]')
clean = lambda s: TASH.sub('', s) if isinstance(s, str) else s
def plain(b): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', md(b)))).strip()[:4000]
docs = []
for p in posts:
    a = p.get('aliases'); a = ' '.join(a) if isinstance(a, list) else (a or '')
    dd = {'t': p['title'], 'u': p['path'] + '/', 'k': p['section'] if p['section'] in SD else 'aid', 'o': p.get('org'), 'c': p.get('category'), 'st': status(p), 'cd': ds(p.get('close_date')),
          'sm': p.get('summary'), 'b': plain(p['body']), 'a': a, 'l': ' '.join(str(x) for x in (p.get('link'), p.get('link2')) if x), 'id': p['id'], 'd': p['date']}
    docs.append({k: clean(v) for k, v in dd.items() if v})
for k, t_, d_, i_, o_ in ALL: docs.append({'t': t_, 'u': k + '/', 'k': 'page', 'sm': d_})
docs.append({'t': 'الأرشيف (المغلقة)', 'u': 'archive/', 'k': 'page', 'sm': 'روابط انتهى تسجيلها'})
for sl_, t_, d_ in [('contact', 'طرق التواصل', 'تواصل معنا للإبلاغ أو الاقتراح'), ('settings', 'الإعدادات', 'المظهر وحجم الخط')]: docs.append({'t': t_, 'u': sl_ + '/', 'k': 'page', 'sm': d_})
for f_ in sorted(os.listdir(f'{R}/content/pages')):
    d_, b_ = read(f'{R}/content/pages/{f_}'); docs.append({'t': clean(d_.get('title', f_[:-3])), 'u': f_[:-3] + '/', 'k': 'page', 'b': clean(plain(b_))})
META = {k: {'t': t_, 'i': ic(i_, 20), 'c': 'c-' + k, 'u': k + '/'} for k, t_, d_, i_, o_ in ALL}
META['page'] = {'t': 'الصفحات', 'i': ic('info', 20), 'c': 'c-page', 'u': ''}
write('assets/search-data.js', 'window.SEARCH_META=%s;window.SEARCH_SYN=%s;window.SEARCH_POP=%s;window.SEARCH_DATA=%s;' % tuple(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in (META, SYN, POP, docs)))
chips = '<button class="chip on" data-f="">الكل</button>' + ''.join(f'<button class="chip" data-f="{k}">{t_}</button>' for k, t_, d_, i_, o_ in ALL) + '<button class="chip" data-f="page">الصفحات</button><button class="chip" id="gopen" aria-pressed="false">مفتوح الآن فقط</button>'
sbody = f'''<section class="hero c-search"><h1><span class="ico">{ic("search",26)}</span>البحث في الموقع</h1><p>ابحث بالعربي أو الإنجليزي: اسم مؤسسة، وظيفة، نوع مساعدة، رقم منشور، أو الصق رابطاً للتحقق منه.</p>
<div class="sbox"><input id="gq" data-gs="page" type="search" placeholder="اكتب للبحث..." aria-label="بحث" autocomplete="off"></div><div class="chips" id="gchips">{chips}</div></section>
<div id="gnote"></div><p id="gcount" class="cnt" aria-live="polite"></p><div class="stack" id="gres"></div>'''
write('search/index.html', layout('البحث', 'ابحث في كل أقسام موقع الفاتحون: المساعدات والوظائف والمؤسسات والروابط.', sbody, '../', 'search/', 'search', None, True)); built.append('search')
write('404.html', layout('الصفحة غير موجودة', S['description'], '<article class="article"><h1>الصفحة غير موجودة</h1><p><a href="/">العودة للرئيسية</a></p></article>', '/', '404.html'))
write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{e(u)}</loc></url>' for u in URLS if '404' not in u) + '</urlset>')
write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
json.dump(built, open(man, 'w')); print('built', len(posts), 'posts,', len(closed), 'closed')

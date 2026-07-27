from pathlib import Path
import re, json, html
from PIL import Image

root=Path('/mnt/data/anko-global-stage5-seo-technical-2026-07-24-v9')
site=root/'site'

# CSS: remove external font dependency by using the system stack.
css=site/'css/style.css'
t=css.read_text('utf-8')
t=t.replace("--sans: 'Manrope', 'Segoe UI', Arial, sans-serif;", "--sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;")
css.write_text(t,'utf-8')

# Footer navigation labels are not content headings.
footer=site/'inc/footer.php'
t=footer.read_text('utf-8')
t=t.replace('<h4 class="footer__title">','<p class="footer__title">').replace('</h4>','</p>')
footer.write_text(t,'utf-8')

# Head: robust robots, OG image metadata and optional LCP preload.
head=site/'inc/head.php'
t=head.read_text('utf-8')
t=t.replace("$og_image     = $og_image     ?? 'img/og-image.jpg';\n$extra_head", "$og_image     = $og_image     ?? 'img/og-image.jpg';\n$og_type      = $og_type      ?? 'website';\n$og_image_alt = $og_image_alt ?? $page_title;\n$robots       = $robots       ?? 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1';\n$preload_image = $preload_image ?? '';\n$preload_srcset = $preload_srcset ?? '';\n$preload_sizes = $preload_sizes ?? '100vw';\n$extra_head")
insert="""
$og_width = 1200;
$og_height = 630;
$og_mime = 'image/jpeg';
$og_local = dirname(__DIR__) . '/' . ltrim($og_image, '/');
if (is_file($og_local)) {
    $og_info = @getimagesize($og_local);
    if (is_array($og_info)) {
        $og_width = (int) ($og_info[0] ?? $og_width);
        $og_height = (int) ($og_info[1] ?? $og_height);
        $og_mime = (string) ($og_info['mime'] ?? $og_mime);
    }
}
"""
t=t.replace("function nav_class($name, $active) {",insert+"\nfunction nav_class($name, $active) {")
t=t.replace('<meta name="description" content="<?= e($page_desc) ?>">','<meta name="description" content="<?= e($page_desc) ?>">\n<meta name="robots" content="<?= e($robots) ?>">')
t=t.replace('<meta property="og:type" content="website">','<meta property="og:type" content="<?= e($og_type) ?>">\n<meta property="og:locale" content="ru_BY">')
t=t.replace('<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">','<meta property="og:image:type" content="<?= e($og_mime) ?>">\n<meta property="og:image:width" content="<?= e((string) $og_width) ?>">\n<meta property="og:image:height" content="<?= e((string) $og_height) ?>">\n<meta property="og:image:alt" content="<?= e($og_image_alt) ?>">')
t=t.replace('<meta name="twitter:image" content="<?= e($SITE[\'domain\'] . \'/\' . ltrim($og_image, \'/\')) ?>">','<meta name="twitter:image" content="<?= e($SITE[\'domain\'] . \'/\' . ltrim($og_image, \'/\')) ?>">\n<meta name="twitter:image:alt" content="<?= e($og_image_alt) ?>">')
# Remove Google Fonts requests.
t=re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*<link href="https://fonts\.googleapis\.com/css2\?family=Manrope:[^\n]+\n','',t)
preload="""<?php if ($preload_image !== ''): ?>
<link rel="preload" as="image" href="<?= e($preload_image) ?>"<?php if ($preload_srcset !== ''): ?> imagesrcset="<?= e($preload_srcset) ?>" imagesizes="<?= e($preload_sizes) ?>"<?php endif; ?>>
<?php endif; ?>
"""
t=t.replace('<link rel="stylesheet" href="css/style.css?v=20260724">',preload+'<link rel="stylesheet" href="css/style.css?v=20260724-stage5">')
head.write_text(t,'utf-8')

# Noindex pages use the shared robots variable instead of duplicate tags.
for name in ['404.php','thanks.php','policy.php']:
    p=site/name; s=p.read_text('utf-8')
    s=re.sub(r"\$extra_head\s*=\s*<<<'HTML'\s*<meta name=\"robots\" content=\"noindex, ?follow\">\s*HTML;", "$robots = 'noindex,follow';", s, flags=re.S)
    s=s.replace("$extra_head = '<meta name=\"robots\" content=\"noindex,follow\">';", "$robots = 'noindex,follow';")
    p.write_text(s,'utf-8')

# send.php is never indexable.
send=site/'send.php'; s=send.read_text('utf-8')
s=s.replace("header('Cache-Control: no-store, max-age=0');", "header('Cache-Control: no-store, max-age=0');\nheader('X-Robots-Tag: noindex, nofollow', true);")
send.write_text(s,'utf-8')

# Map category social images.
cat_images={
'category-bentonit.php':'img/cat-bentonit.jpg','category-instrument.php':'img/cat-instrument.jpg',
'category-lokacia.php':'img/cat-lokacia.jpg','category-normet.php':'img/product-normet-geotek.jpg',
'category-polimer.php':'img/cat-polimery.jpg','category-smazki.php':'img/cat-smazki.jpg',
'category-trubi.php':'img/cat-pnd.jpg','category-ustanovki.php':'img/cat-ustanovki.jpg'}

# Helpers to insert page variables after canonical.
def insert_after_canonical(s, lines):
    if '$og_image' in s[:500]: return s
    m=re.search(r"(\$canonical\s*=\s*[^;]+;\n)",s)
    if not m: return s
    return s[:m.end()]+''.join(f"{x}\n" for x in lines)+s[m.end():]

# Product pages: product-specific social preview and LCP preload.
for p in sorted(site.glob('product-*.php')):
    s=p.read_text('utf-8')
    m=re.search(r'"@type":"Product".*?"image":"https://a-global\.by/(img/[^"]+\.jpg)"',s)
    if not m: continue
    jpg=m.group(1); webp=re.sub(r'\.jpg$','.webp',jpg)
    srcset=[]
    for w in (640,960):
        rp=re.sub(r'\.webp$',f'-{w}.webp',webp)
        if (site/rp).is_file(): srcset.append(f'{rp} {w}w')
    srcset.append(f'{webp} 1280w')
    lines=[f"$og_image = '{jpg}';", "$og_type = 'product';", f"$preload_image = '{webp}';", f"$preload_srcset = '{', '.join(srcset)}';", "$preload_sizes = '(max-width: 900px) 100vw, 50vw';"]
    s=insert_after_canonical(s,lines)
    p.write_text(s,'utf-8')

# Categories: individual social image and CollectionPage/ItemList schema.
for name,img in cat_images.items():
    p=site/name; s=p.read_text('utf-8')
    s=insert_after_canonical(s,[f"$og_image = '{img}';"])
    cards=re.findall(r'<h2 class="product__title"><a href="([^"]+)">([^<]+)</a></h2>',s)
    if not cards:
        cards=re.findall(r'<h3 class="product__title"><a href="([^"]+)">([^<]+)</a></h3>',s)
    titlem=re.search(r"\$page_title\s*=\s*'([^']+)'",s); title=titlem.group(1) if titlem else name
    items=[{'@type':'ListItem','position':i+1,'name':html.unescape(n.strip()),'url':'https://a-global.by/'+u} for i,(u,n) in enumerate(cards)]
    obj={'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':'https://a-global.by/'+name,'mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':items}}
    script='<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'</script>\n'
    if '"@type":"CollectionPage"' not in s:
        s=s.replace('\nHTML;\n$body_scripts', '\n'+script+'HTML;\n$body_scripts')
    p.write_text(s,'utf-8')

# Catalog CollectionPage with its eight categories.
p=site/'catalog.php'; s=p.read_text('utf-8')
cards=re.findall(r'<a class="category card" href="([^"]+)"[^>]*>.*?<h2 class="category__title">([^<]+)</h2>',s,re.S)
if not cards: cards=re.findall(r'<a class="category card" href="([^"]+)"[^>]*>.*?<h3 class="category__title">([^<]+)</h3>',s,re.S)
items=[{'@type':'ListItem','position':i+1,'name':html.unescape(n.strip()),'url':'https://a-global.by/'+u} for i,(u,n) in enumerate(cards)]
obj={'@context':'https://schema.org','@type':'CollectionPage','name':'Каталог продукции для ГНБ','url':'https://a-global.by/catalog.php','mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':items}}
script='<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'</script>\n'
if '"@type":"CollectionPage"' not in s: s=s.replace('\nHTML;\n$body_scripts','\n'+script+'HTML;\n$body_scripts')
p.write_text(s,'utf-8')

# Home LCP preload through shared variables; remove old manual preload.
p=site/'index.php'; s=p.read_text('utf-8')
s=insert_after_canonical(s,["$preload_image = 'img/generated/hero-generated-anko.webp';","$preload_srcset = 'img/generated/hero-generated-anko-640.webp 640w, img/generated/hero-generated-anko-960.webp 960w, img/generated/hero-generated-anko.webp 1200w';","$preload_sizes = '(max-width: 900px) 100vw, 50vw';"])
s=s.replace('<link rel="preload" as="image" href="img/generated/hero-generated-anko.webp" type="image/webp">\n','')
p.write_text(s,'utf-8')

# Responsive WebP srcsets, decoding hints and main-image priority.
picture_re=re.compile(r'(<picture>\s*)(<source\s+srcset="([^"]+\.webp)"\s+type="image/webp">)(\s*)(<img\s+[^>]*>)',re.S)
def picture_sub(m):
    prefix,source,webp,space,img=m.groups()
    cls=re.search(r'class="([^"]+)"',img); classes=cls.group(1) if cls else ''
    if 'product__img' in classes: sizes='(max-width: 620px) calc(100vw - 32px), (max-width: 1000px) 50vw, 33vw'
    elif 'gallery__img' in classes or 'hero__img' in classes: sizes='(max-width: 900px) 100vw, 50vw'
    else: sizes='100vw'
    paths=[]
    for w in (640,960):
        rp=re.sub(r'\.webp$',f'-{w}.webp',webp)
        if (site/rp).is_file(): paths.append(f'{rp} {w}w')
    fullw=1200 if 'hero__img' in classes else 1280
    paths.append(f'{webp} {fullw}w')
    newsource=f'<source srcset="{", ".join(paths)}" sizes="{sizes}" type="image/webp">'
    if 'decoding=' not in img: img=img[:-1]+' decoding="async">'
    if ('gallery__img' in classes or 'hero__img' in classes) and 'fetchpriority=' not in img: img=img[:-1]+' fetchpriority="high">'
    return prefix+newsource+space+img
for p in site.glob('*.php'):
    s=p.read_text('utf-8'); s=picture_re.sub(picture_sub,s)
    # Direct category JPGs get WebP wrappers.
    direct=re.compile(r'(?<!<picture>\s)(<img\s+class="category__img"\s+src="(img/cat-[^"]+\.jpg)"[^>]*>)')
    def direct_sub(mm):
        img,jpg=mm.groups(); wp=re.sub(r'\.jpg$','.webp',jpg)
        if not (site/wp).is_file(): return img
        if 'decoding=' not in img: img=img[:-1]+' decoding="async">'
        return f'<picture><source srcset="{wp}" type="image/webp">{img}</picture>'
    s=direct.sub(direct_sub,s)
    # All remaining lazy images decode asynchronously.
    s=re.sub(r'<img(?![^>]*decoding=)([^>]*loading="lazy"[^>]*)>',r'<img\1 decoding="async">',s)
    p.write_text(s,'utf-8')

# Canonical URL normalization and Brotli support.
ht=site/'.htaccess'; s=ht.read_text('utf-8')
rule='''# /index.php — только канонический корень\nRewriteCond %{THE_REQUEST} \\s/+index\\.php(?:[?\\s]) [NC]\nRewriteRule ^index\\.php$ https://a-global.by/ [R=301,L,NE]\n\n'''
if 'только канонический корень' not in s: s=s.replace('# ── Редиректы со старых .html',rule+'# ── Редиректы со старых .html')
if 'mod_brotli' not in s:
    s=s.replace('# ── Базовые заголовки безопасности', '<IfModule mod_brotli.c>\n  AddOutputFilterByType BROTLI_COMPRESS text/html text/css application/javascript text/plain application/json image/svg+xml application/xml\n</IfModule>\n\n# ── Базовые заголовки безопасности')
ht.write_text(s,'utf-8')

# robots: keep crawlers away from technical endpoints.
robots=site/'robots.txt'; s=robots.read_text('utf-8')
if 'Disallow: /send.php' not in s:
    s=s.replace('Allow: /\n','Allow: /\nDisallow: /send.php\nDisallow: /thanks.php\nDisallow: /inc/\n',1)
robots.write_text(s,'utf-8')

# Sitemap with lastmod and product/category image entries.
old=(site/'sitemap.xml').read_text('utf-8')
locs=re.findall(r'<url><loc>(.*?)</loc><changefreq>(.*?)</changefreq><priority>(.*?)</priority></url>',old)
product_meta={}
for p in site.glob('product-*.php'):
    ss=p.read_text('utf-8')
    m=re.search(r'"@type":"Product","name":"([^"]+)".*?"image":"([^"]+)"',ss)
    if m: product_meta['https://a-global.by/'+p.name]=(m.group(2),m.group(1))
cat_meta={'https://a-global.by/'+k:('https://a-global.by/'+v,k.replace('category-','').replace('.php','')) for k,v in cat_images.items()}
lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for loc,freq,prio in locs:
    lines.append('  <url>'); lines.append(f'    <loc>{loc}</loc>'); lines.append('    <lastmod>2026-07-24</lastmod>'); lines.append(f'    <changefreq>{freq}</changefreq>'); lines.append(f'    <priority>{prio}</priority>')
    meta=product_meta.get(loc) or cat_meta.get(loc)
    if meta:
        lines.append('    <image:image>'); lines.append(f'      <image:loc>{html.escape(meta[0])}</image:loc>'); lines.append(f'      <image:title>{html.escape(meta[1])}</image:title>'); lines.append('    </image:image>')
    lines.append('  </url>')
lines.append('</urlset>')
(site/'sitemap.xml').write_text('\n'.join(lines)+'\n','utf-8')

print('Stage-05 transformations applied')

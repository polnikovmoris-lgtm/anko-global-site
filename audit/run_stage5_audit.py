from pathlib import Path
import os,re,json,urllib.request,urllib.error,xml.etree.ElementTree as ET,gzip,hashlib
from collections import Counter
from bs4 import BeautifulSoup
from PIL import Image

root=Path(os.environ['ROOT']); base=os.environ['BASE']; out=Path(os.environ['OUT']); out.mkdir(parents=True,exist_ok=True)
pages=sorted(p.name for p in root.glob('*.php') if p.name!='send.php')
results=[]
for name in pages:
    try:
        with urllib.request.urlopen(base+name,timeout=15) as r: html=r.read().decode('utf-8','replace'); status=r.status
    except urllib.error.HTTPError as e:
        html=e.read().decode('utf-8','replace'); status=e.code
    soup=BeautifulSoup(html,'html.parser')
    def meta(key,prop=False):
        x=soup.find('meta',attrs={('property' if prop else 'name'):key}); return x.get('content','').strip() if x else ''
    title=soup.title.get_text(' ',strip=True) if soup.title else ''
    canonical=(soup.find('link',rel=lambda x:x and 'canonical' in x) or {}).get('href','') if soup.find('link',rel=lambda x:x and 'canonical' in x) else ''
    headings=[(int(h.name[1]),h.get_text(' ',strip=True)) for h in soup.find_all(re.compile('^h[1-6]$'))]
    skips=[]
    prev=0
    for lvl,text in headings:
        if prev and lvl>prev+1: skips.append({'from':prev,'to':lvl,'text':text})
        prev=lvl
    jsonobjs=[]; jsonerrs=[]
    for sc in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try: jsonobjs.append(json.loads(sc.string or sc.get_text()))
        except Exception as e: jsonerrs.append(str(e))
    ogimg=meta('og:image',True); ogw=meta('og:image:width',True); ogh=meta('og:image:height',True); ogtype=meta('og:type',True)
    ogdim_ok=None
    if ogimg.startswith('https://a-global.by/'):
        rel=ogimg.replace('https://a-global.by/','',1); p=root/rel
        if p.is_file():
            with Image.open(p) as im: ogdim_ok=(str(im.width)==ogw and str(im.height)==ogh)
    targets=[]
    for a in soup.find_all('a',target='_blank'):
        rels=set((a.get('rel') or []));
        if not {'noopener','noreferrer'}.issubset(rels): targets.append(a.get('href',''))
    results.append({'page':name,'status':status,'title':title,'description':meta('description'),'robots':meta('robots'),'canonical':canonical,'headings':headings,'heading_skips':skips,'jsonld_errors':jsonerrs,'jsonld_types':[x.get('@type') for x in jsonobjs if isinstance(x,dict)],'collection_items':[x.get('mainEntity',{}).get('numberOfItems') for x in jsonobjs if isinstance(x,dict) and x.get('@type')=='CollectionPage'],'og_image':ogimg,'og_type':ogtype,'og_dimension_ok':ogdim_ok,'preloads':len(soup.find_all('link',rel=lambda x:x and 'preload' in x)),'target_blank_unsafe':targets,'google_fonts':'fonts.googleapis.com' in html or 'fonts.gstatic.com' in html,'responsive_sources':sum(1 for x in soup.find_all('source',attrs={'type':'image/webp'}) if '640w' in x.get('srcset','') and '960w' in x.get('srcset',''))})

# Sitemap checks.
sm=root/'sitemap.xml'; tree=ET.parse(sm); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
urls=tree.getroot().findall('s:url',ns)
sm_lastmod=sum(1 for u in urls if u.find('s:lastmod',ns) is not None)
sm_images=sum(1 for u in urls if u.find('i:image',ns) is not None)

# Asset size comparison and delivery hints.
assets={}
for rel in ['css/style.css','js/main.js','js/search.js']:
    b=(root/rel).read_bytes(); assets[rel]={'raw':len(b),'gzip':len(gzip.compress(b,9))}
img_bytes=sum(p.stat().st_size for p in (root/'img').rglob('*') if p.is_file())
wide_base=[]
for p in (root/'img').rglob('*.jpg'):
    try:
        with Image.open(p) as im:
            if im.width>=900 and p.name != 'og-image.jpg' and not p.name.endswith(('-640.jpg','-960.jpg')): wide_base.append(p)
    except: pass
variant_missing=[]
for p in wide_base:
    stem=p.with_suffix('')
    for w in (640,960):
        q=Path(str(stem)+f'-{w}.webp')
        if not q.is_file(): variant_missing.append(q.relative_to(root).as_posix())

# Source checks.
head=(root/'inc/head.php').read_text('utf-8'); ht=(root/'.htaccess').read_text('utf-8'); robots=(root/'robots.txt').read_text('utf-8'); send=(root/'send.php').read_text('utf-8')
source_checks={
    'no_google_fonts_source':'fonts.googleapis.com' not in head and 'fonts.gstatic.com' not in head,
    'index_php_redirect':'только канонический корень' in ht and '^index\\.php$' in ht,
    'brotli_conditional':'mod_brotli.c' in ht,
    'robots_blocks_endpoints':all(x in robots for x in ['Disallow: /send.php','Disallow: /thanks.php','Disallow: /inc/']),
    'send_x_robots':'X-Robots-Tag: noindex, nofollow' in send,
    'dynamic_og_dimensions':'getimagesize' in head and 'og:image:alt' in head,
}

summary={
    'pages':len(results),
    'status_counts':dict(Counter(str(x['status']) for x in results)),
    'heading_skip_pages':[{'page':x['page'],'issues':x['heading_skips']} for x in results if x['heading_skips']],
    'jsonld_error_pages':[{'page':x['page'],'errors':x['jsonld_errors']} for x in results if x['jsonld_errors']],
    'unsafe_target_blank':[{'page':x['page'],'hrefs':x['target_blank_unsafe']} for x in results if x['target_blank_unsafe']],
    'google_fonts_pages':[x['page'] for x in results if x['google_fonts']],
    'product_og_specific':sum(1 for x in results if x['page'].startswith('product-') and not x['og_image'].endswith('/img/og-image.jpg')),
    'product_og_type_product':sum(1 for x in results if x['page'].startswith('product-') and x['og_type']=='product'),
    'unique_og_images':len(set(x['og_image'] for x in results)),
    'og_dimension_mismatches':[x['page'] for x in results if x['og_dimension_ok'] is False],
    'collection_pages':sum(1 for x in results if 'CollectionPage' in x['jsonld_types']),
    'collection_item_counts':{x['page']:x['collection_items'] for x in results if x['collection_items']},
    'lcp_preload_pages':sum(1 for x in results if x['preloads']>0),
    'responsive_source_total':sum(x['responsive_sources'] for x in results),
    'sitemap':{'urls':len(urls),'lastmod':sm_lastmod,'image_entries':sm_images},
    'assets':assets,'image_bytes':img_bytes,'responsive_variant_missing':variant_missing,
    'source_checks':source_checks,
    'noindex_pages':{x['page']:x['robots'] for x in results if x['robots'].startswith('noindex')},
}
(out/'stage5-final-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8')
(out/'stage5-pages.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))

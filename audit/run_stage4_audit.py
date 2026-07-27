from pathlib import Path
import os,re,json,hashlib,urllib.request,urllib.error,urllib.parse,http.cookiejar
from collections import Counter,defaultdict
from bs4 import BeautifulSoup
from PIL import Image
root=Path(os.environ['ROOT']); out=Path(os.environ['OUT']); base=os.environ['BASE']
php_files=sorted(p.name for p in root.glob('*.php'))
products=sorted(p.name for p in root.glob('product-*.php')); categories=sorted(p.name for p in root.glob('category-*.php'))
results=[]; rendered={}
for name in php_files:
    req=urllib.request.Request(base+name,headers={'User-Agent':'Stage4Audit/3.0'})
    try:
        with urllib.request.urlopen(req,timeout=10) as r:
            text=r.read().decode('utf-8','replace'); status=r.status
    except urllib.error.HTTPError as e:
        text=e.read().decode('utf-8','replace'); status=e.code
    rendered[name]=text; soup=BeautifulSoup(text,'html.parser')
    def meta(n):
        x=soup.find('meta',attrs={'name':n}); return x.get('content','').strip() if x else ''
    can=soup.find('link',rel=lambda x:x and 'canonical' in x)
    title=soup.title.get_text(' ',strip=True) if soup.title else ''
    desc=meta('description'); canon=can.get('href','').strip() if can else ''
    h1=[x.get_text(' ',strip=True) for x in soup.find_all('h1')]
    jsonerrs=[]; jsonobjs=[]
    for sc in soup.find_all('script',attrs={'type':'application/ld+json'}):
        try: jsonobjs.append(json.loads(sc.string or sc.get_text()))
        except Exception as e: jsonerrs.append(str(e))
    results.append({'page':name,'status':status,'title':title,'title_len':len(title),'description':desc,'description_len':len(desc),'canonical':canon,'h1':h1,'jsonld_errors':jsonerrs,'jsonld':jsonobjs,'robots':meta('robots')})

missing_assets=[]; broken_links=[]; dim=[]; missing_alt=[]; empty_alt=[]; referenced=set()
for page,text in rendered.items():
    soup=BeautifulSoup(text,'html.parser')
    for tag,attr in [('img','src'),('script','src'),('link','href'),('source','srcset')]:
        for el in soup.find_all(tag):
            val=el.get(attr)
            if not val: continue
            vals=[val] if attr!='srcset' else [x.strip().split()[0] for x in val.split(',') if x.strip()]
            for v in vals:
                if v.startswith(('http://','https://','//','data:','mailto:','tel:','#')): continue
                clean=v.split('?',1)[0].split('#',1)[0].lstrip('/')
                if clean:
                    referenced.add(clean)
                    if not (root/clean).is_file(): missing_assets.append({'page':page,'ref':v,'resolved':clean})
    for a in soup.find_all('a',href=True):
        v=a['href']
        if v.startswith(('http://','https://','//','mailto:','tel:','#','javascript:')): continue
        clean=v.split('?',1)[0].split('#',1)[0].lstrip('/')
        if clean and not (root/clean).exists(): broken_links.append({'page':page,'href':v,'resolved':clean})
    for i in soup.find_all('img'):
        src=i.get('src','')
        if i.get('alt') is None: missing_alt.append({'page':page,'src':src})
        elif not i.get('alt','').strip(): empty_alt.append({'page':page,'src':src})
        if src and not src.startswith(('http','//','data:')) and i.get('width') and i.get('height'):
            p=root/src.split('?',1)[0].lstrip('/')
            if p.is_file():
                try:
                    with Image.open(p) as im: actual=list(im.size)
                    declared=[int(i['width']),int(i['height'])]
                    if actual!=declared: dim.append({'page':page,'src':src,'declared':declared,'actual':actual})
                except: pass

img_files=[]; sha=defaultdict(list)
for p in sorted((root/'img').rglob('*')):
    if p.is_file():
        rel=p.relative_to(root).as_posix(); b=p.read_bytes(); h=hashlib.sha256(b).hexdigest(); sha[h].append(rel)
        item={'path':rel,'size':len(b),'sha256':h,'used':rel in referenced or rel=='img/og-image.jpg'}
        if p.suffix.lower() in {'.jpg','.jpeg','.png','.webp','.gif'}:
            try:
                with Image.open(p) as im:item['width'],item['height']=im.size; item['format']=im.format
            except Exception as e:item['image_error']=repr(e)
        img_files.append(item)
unused=[x for x in img_files if not x['used']]
dup=[v for v in sha.values() if len(v)>1]

sitemap=(root/'sitemap.xml').read_text('utf-8','replace'); locs=re.findall(r'<loc>(.*?)</loc>',sitemap); sm=[]
for loc in locs:
    x=re.sub(r'^https?://[^/]+/?','',loc).split('?',1)[0] or 'index.php'; sm.append(x)
missing_sm=[x for x in sm if not (root/x).is_file()]
php_not=[x for x in php_files if x not in sm and x not in {'send.php','thanks.php','404.php','policy.php'}]

search=(root/'js/search.js').read_text('utf-8','replace'); m=re.search(r'var INDEX_DATA = (\[.*?\]);\n',search,re.S); idx=json.loads(m.group(1)) if m else []
idx_urls=[x.get('u') for x in idx]

prod_issues=[]
for name in products:
    r=next(x for x in results if x['page']==name); h1=r['h1'][0] if len(r['h1'])==1 else ''
    objs=[x for x in r['jsonld'] if isinstance(x,dict) and x.get('@type')=='Product']
    if len(objs)!=1:
        prod_issues.append({'page':name,'issue':'product_jsonld_count','value':len(objs)})
    else:
        schema_name=(objs[0].get('name') or '').strip()
        h1_norm=' '.join(h1.lower().split())
        schema_norm=' '.join(schema_name.lower().split())
        if not schema_norm or not h1_norm or (schema_norm not in h1_norm and h1_norm not in schema_norm):
            prod_issues.append({'page':name,'issue':'schema_name_not_semantically_aligned','h1':h1,'schema':schema_name})

index=rendered['index.php']
claim_checks={
'reviews_anchor_present':'#reviews' in index,
'review_section_present':'id="reviews"' in index,
'placeholder_letters_present':'letter-1.jpg' in index,
'500_plus_present':'500<em>+</em>' in index or '500+' in index,
'30_minutes_anywhere':any('30 минут' in t for t in rendered.values()),
'external_normet_logo_present':'mb.cision.com' in index,
'baroid_brand_card_present':'brand-baroid' in index,
'local_normet_logo_present':'img/brand-normet.png' in index,
'catalog_59_present':'59' in index,
}

normet_checks={}
for name in ['category-normet.php']+[x for x in products if x.startswith('product-normet-')]:
    t=rendered[name]; normet_checks[name]=t.count('brand-normet.png')

rate_fixture=Path('/tmp/anko-lead-' + hashlib.sha256(b'127.0.0.1').hexdigest())
if rate_fixture.exists(): rate_fixture.unlink()
cj=http.cookiejar.CookieJar(); opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
page=opener.open(base+'index.php').read().decode('utf-8','replace'); soup=BeautifulSoup(page,'html.parser'); csrf=soup.find('input',attrs={'name':'csrf'}).get('value')
def post(data):
    req=urllib.request.Request(base+'send.php',data=urllib.parse.urlencode(data).encode(),method='POST',headers={'Content-Type':'application/x-www-form-urlencoded'})
    try:
        with opener.open(req) as r:return [r.status,json.loads(r.read().decode())]
    except urllib.error.HTTPError as e:return [e.code,json.loads(e.read().decode())]
form_tests={'bad_csrf':post({'phone':'+375296526709','csrf':'bad'}),'invalid_phone':post({'phone':'123','csrf':csrf}),'honeypot':post({'phone':'','csrf':'bad','company':'bot'}),'valid_but_mail_unconfigured':post({'phone':'+375296526709','csrf':csrf})}

allphp='\n'.join(p.read_text('utf-8','replace') for p in root.rglob('*.php')); config=(root/'inc/config.php').read_text('utf-8','replace'); ht=(root/'.htaccess').read_text('utf-8','replace')
source_checks={'php74_no_str_contains':'str_contains(' not in allphp,'telegram_primary_env':all(x in config for x in ['TELEGRAM_BOT_TOKEN','TELEGRAM_CHAT_ID']),'telegram_legacy_env':all(x in config for x in ['LEAD_TG_TOKEN','LEAD_TG_CHAT_ID']),'error_document':'ErrorDocument 404 /404.php' in ht,'canonical_redirect':'a-global\\.by' in ht,'protect_internal_extensions':'json|csv|sha256' in ht}

titles=Counter(r['title'] for r in results if r['title']); descs=Counter(r['description'] for r in results if r['description']); cans=Counter(r['canonical'] for r in results if r['canonical'])
summary={'file_counts':{'all':sum(1 for p in root.rglob('*') if p.is_file()),'php':len(list(root.rglob('*.php'))),'root_php':len(php_files),'products':len(products),'categories':len(categories),'images':len(img_files)},'http_status_counts':dict(Counter(str(r['status']) for r in results)),'pages_without_title':[r['page'] for r in results if r['page']!='send.php' and not r['title']],'pages_without_description':[r['page'] for r in results if r['page']!='send.php' and not r['description']],'pages_without_canonical':[r['page'] for r in results if r['page'] not in {'send.php','404.php'} and not r['canonical']],'bad_h1':[{'page':r['page'],'h1':r['h1']} for r in results if r['page']!='send.php' and len(r['h1'])!=1],'jsonld_errors':[{'page':r['page'],'errors':r['jsonld_errors']} for r in results if r['jsonld_errors']],'duplicate_titles':{k:v for k,v in titles.items() if v>1},'duplicate_descriptions':{k:v for k,v in descs.items() if v>1},'duplicate_canonicals':{k:v for k,v in cans.items() if v>1},'long_titles':[{'page':r['page'],'length':r['title_len']} for r in results if r['title_len']>70],'long_descriptions':[{'page':r['page'],'length':r['description_len']} for r in results if r['description_len']>180],'short_descriptions':[{'page':r['page'],'length':r['description_len']} for r in results if r['page']!='send.php' and r['description_len']<50],'missing_assets':missing_assets,'broken_internal_links':broken_links,'dimension_mismatches':dim,'missing_alt':missing_alt,'empty_alt':empty_alt,'unused_images':unused,'duplicate_image_groups':dup,'sitemap':{'urls':len(locs),'missing_files':missing_sm,'php_not_in_sitemap':php_not},'search_index':{'counts':dict(Counter(x.get('t') for x in idx)),'total':len(idx),'missing_urls':[u for u in idx_urls if not (root/u).is_file()],'duplicate_urls':[k for k,v in Counter(idx_urls).items() if v>1]},'product_issues':prod_issues,'claim_checks':claim_checks,'normet_logo_checks':normet_checks,'form_tests':form_tests,'source_checks':source_checks}
(out/'stage4-final-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8')
(out/'rendered-pages-v8.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),'utf-8')
(out/'image-inventory-v8.json').write_text(json.dumps(img_files,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps({'file_counts':summary['file_counts'],'status':summary['http_status_counts'],'missing_assets':len(missing_assets),'broken_links':len(broken_links),'dim':len(dim),'unused_images':len(unused),'duplicate_groups':len(dup),'bad_h1':len(summary['bad_h1']),'json_errors':len(summary['jsonld_errors']),'product_issues':len(prod_issues),'search':summary['search_index'],'form_tests':form_tests,'claim_checks':claim_checks,'pages_without_canonical':summary['pages_without_canonical'],'long_desc':summary['long_descriptions']},ensure_ascii=False,indent=2))

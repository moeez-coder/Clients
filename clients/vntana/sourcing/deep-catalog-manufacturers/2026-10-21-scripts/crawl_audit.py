import csv,json,re,sys,gzip,random,time,urllib.request,urllib.parse,urllib.robotparser,concurrent.futures as cf,hashlib
UA='Mozilla/5.0 (compatible; catalog-audit/1.0)'
SRC='/home/user/Clients/clients/vntana/sourcing/deep-catalog-manufacturers/2026-10-21-companies-qualified-2.csv'
rows=list(csv.DictReader(open(SRC,encoding='utf-8')))
PRODURL=re.compile(r'/(products?|p|item|items|catalog|catalogue|shop|part|parts|sku|detail|pd|prod)/[^/]+',re.I)
PLACE=re.compile(r'(coming[-_ ]?soon|no[-_ ]?image|image[-_ ]?(not[-_ ]?)?(available|unavailable|coming)|noimage|placeholder|no[-_ ]?photo|default[-_ ]?(product|image)|image[-_ ]?na\b|nopic|not[-_ ]?available)',re.I)
PLAT={'shopify':r'cdn\.shopify\.com|Shopify\.theme','magento':r'Magento|mage/cookies|/static/version\d+/frontend','bigcommerce':r'bigcommerce\.com|cdn11\.bigcommerce','woocommerce':r'woocommerce|wp-content/plugins/woocommerce','sap_commerce':r'/_ui/|hybris|sap-commerce|spartacus','salesforce_commerce':r'demandware|dwstatic|salesforce-commerce','optimizely':r'episerver|optimizely','wordpress':r'wp-content','sitecore':r'sitecore','salsify':r'salsify','akeneo':r'akeneo','traceparts':r'traceparts','cadenas':r'cadenas|partcommunity|partsolutions','3d_viewer':r'model-viewer|three\.js|sketchfab|3d[-_ ]viewer|vntana|threekit|cylindo'}
CAD=re.compile(r'(cad (model|download|file)s?|download cad|3d (model|cad)s?|step file|iges|\.stp\b|\.step\b|dwg)',re.I)
CONF=re.compile(r'(configurator|configure (your|a)|build your|part number builder|model selector)',re.I)
DRAW=re.compile(r'(drawing|dwg|diagram|schematic|line[-_]?art|dimension)',re.I)
def get(u,t=12,maxb=600000):
    req=urllib.request.Request(u,headers={'User-Agent':UA,'Accept':'*/*','Accept-Encoding':'gzip'})
    r=urllib.request.urlopen(req,timeout=t)
    b=r.read(maxb)
    if r.headers.get('Content-Encoding')=='gzip' or b[:2]==b'\x1f\x8b':
        try:b=gzip.decompress(b)
        except Exception:pass
    return r.status,b.decode('utf-8','ignore'),r.geturl()
def sitemap_urls(base,robots):
    cands=[]
    for line in robots.splitlines():
        if line.lower().startswith('sitemap:'):cands.append(line.split(':',1)[1].strip())
    for p in ('/sitemap.xml','/sitemap_index.xml'):
        if base+p not in cands:cands.append(base+p)
    seen=set();urls=[];total=0;files=0;q=cands[:3]
    while q and files<8:
        s=q.pop(0)
        if s in seen:continue
        seen.add(s)
        try:_,x,_=get(s,10,3000000)
        except Exception:continue
        files+=1
        locs=re.findall(r'<loc>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</loc>',x,re.S)
        if '<sitemapindex' in x:
            # prefer product-ish child sitemaps
            kids=[l.strip() for l in locs]
            kids.sort(key=lambda k:0 if re.search(r'product|item|part|catalog|sku',k,re.I) else 1)
            q=kids[:8]+q
        else:
            total+=len(locs);urls+=[l.strip() for l in locs[:50000]]
    return total,urls,files
def img_urls(html,base):
    imgs=[]
    m=re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',html,re.I) or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',html,re.I)
    og=urllib.parse.urljoin(base,m.group(1)) if m else '-'
    for t in re.findall(r'<img\b[^>]*>',html,re.I)[:60]:
        s=re.search(r'(?:data-src|data-lazy-src|src)=["\']([^"\']+)',t,re.I); a=re.search(r'alt=["\']([^"\']*)',t,re.I)
        if s: imgs.append((urllib.parse.urljoin(base,s.group(1)),a.group(1) if a else ''))
    return og,imgs
def audit(r):
    d=r['domain'].strip().lower().replace('www.','')
    out={'company_linkedin_url':r['company_linkedin_url'],'domain':d,'status':'ok','fail_reason':'-','robots_ok':'-','sitemap_url_count':'-','sitemap_product_like':'-','product_pages_fetched':0,'placeholder_pages':0,'placeholder_examples':'-','shared_image_pages':0,'og_image_pages':0,'line_drawing_hint_pages':0,'platform':'-','cad_3d_text':'no','configurator_text':'no','sample_urls':'-'}
    base=None
    for h in ('https://www.'+d,'https://'+d):
        try:
            st,home,final=get(h,12); base='{0.scheme}://{0.netloc}'.format(urllib.parse.urlparse(final)); break
        except urllib.error.HTTPError as e: out['fail_reason']=f'http_{e.code}'
        except Exception as e: out['fail_reason']='conn_error'
    if not base:
        out['status']='unreachable'; return out
    out['fail_reason']='-'
    plats=[k for k,p in PLAT.items() if re.search(p,home,re.I)]
    if CAD.search(home):out['cad_3d_text']='yes'
    if CONF.search(home):out['configurator_text']='yes'
    robots=''
    rp=urllib.robotparser.RobotFileParser()
    try:
        _,robots,_=get(base+'/robots.txt',8,200000); rp.parse(robots.splitlines()); out['robots_ok']='yes'
    except Exception: rp=None
    try: total,urls,files=sitemap_urls(base,robots)
    except Exception: total,urls,files=0,[],0
    pl=[u for u in urls if PRODURL.search(urllib.parse.urlparse(u).path)]
    out['sitemap_url_count']=total if total else 0; out['sitemap_product_like']=len(pl)
    pool=pl if len(pl)>=3 else urls
    if not pool:
        # fallback: product-like links from homepage
        pool=[urllib.parse.urljoin(base,l) for l in re.findall(r'href=["\']([^"\']+)',home) if PRODURL.search(l)][:200]
    random.seed(d); sample=random.sample(pool,min(6,len(pool))) if pool else []
    ogs=[];allimgs=[]
    for u in sample:
        if rp and not rp.can_fetch(UA,u): continue
        try: st,html,fin=get(u,12,500000)
        except Exception: continue
        out['product_pages_fetched']+=1
        plats+=[k for k,p in PLAT.items() if re.search(p,html,re.I)]
        if CAD.search(html):out['cad_3d_text']='yes'
        if CONF.search(html):out['configurator_text']='yes'
        og,imgs=img_urls(html,fin)
        if og!='-': out['og_image_pages']+=1; ogs.append(og)
        flag=False
        cand=[og]+[i for i,a in imgs[:12]]+[a for i,a in imgs[:12]]
        for c in cand:
            if c and c!='-' and PLACE.search(c): flag=True; ex=c; break
        if flag:
            out['placeholder_pages']+=1; out['placeholder_examples']=ex[:150]
        if any(DRAW.search(i) for i,a in imgs[:8]): out['line_drawing_hint_pages']+=1
    if ogs:
        c={}
        for o in ogs: c[o]=c.get(o,0)+1
        out['shared_image_pages']=sum(v for v in c.values() if v>1)
    out['platform']=','.join(sorted(set(plats))) or '-'
    out['sample_urls']=' | '.join(sample[:3]) or '-'
    if not total and not sample: out['status']='no_sitemap_no_product_links'
    elif out['product_pages_fetched']==0: out['status']='product_pages_unfetchable'
    return out
if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else len(rows)
    sel=rows[:n] if len(sys.argv)>1 else rows
    res=[]
    t=time.time()
    with cf.ThreadPoolExecutor(24) as ex:
        for i,o in enumerate(ex.map(lambda r:(lambda: audit(r))() if True else None,sel)):
            res.append(o)
            if i%100==0: print(i,round(time.time()-t),flush=True)
    json.dump(res,open('crawl/audit_out.json','w'))
    print('done',len(res))

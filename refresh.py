#!/usr/bin/env python3
"""Régénère le flux Google Merchant de mesbonbons.net et relève le stock.
Lit products.json (id ERP, adresse, EAN vérifié), relit chaque page produit publique
(prix TTC, disponibilité, stock, image, nom, description), écrit feed.tsv,
ajoute une ligne par produit à stock-history.csv et résume dans status.json.
Lecture seule sur le site ; aucune écriture ailleurs que dans ce dépôt."""
import concurrent.futures as cf, urllib.request, urllib.parse, re, json, time, html, csv, os, datetime, zoneinfo
SPLIT=re.compile(r'"\]\)</script><script>self\.__next_f\.push\(\[1,"')
def clean(t): return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',urllib.parse.unquote(t or '')))).strip()
def get(p):
    u='https://www.mesbonbons.net/fr/shop/'+p['slug']; s=None
    for t in range(3):
        try: s=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (flux Merchant Aives pour Fladis)'}),timeout=30).read().decode('utf-8','replace'); break
        except Exception as e: err=str(e); time.sleep(3)
    if s is None: return dict(p,err=err)
    r=dict(p,link=u)
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)
    if m:
        try:
            j=json.loads(m.group(1)); o=j.get('offers') or {}
            r.update(price=o.get('price'),availability=o.get('availability'),ld_desc=j.get('description'),ld_name=j.get('name'),
                     brand=(j.get('brand') or {}).get('name') if isinstance(j.get('brand'),dict) else j.get('brand'))
        except Exception: pass
    t=SPLIT.sub('',s).replace('\\"','"'); i=t.find('{"productId":'+str(p['id'])+',"productImages"')
    if i>=0:
        seg=t[i:i+20000]
        g=lambda k:(lambda m: m.group(1) if m else None)(re.search(r'"'+k+r'":"((?:[^"\\]|\\.)*)"',seg))
        n=re.search(r'"numberInStock":(-?[\d.]+)',seg)
        r.update(name=g('name'),cover=g('coverPath'),stock=n.group(1) if n else None,desc=clean(g('description')))
    h=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S); r['h1']=html.unescape(re.sub('<[^>]+>','',h.group(1))).strip() if h else None
    return r
def main():
    P=json.load(open('products.json')); now=datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Brussels')).strftime('%Y-%m-%d %H:%M')
    with cf.ThreadPoolExecutor(4) as ex: R=list(ex.map(get,P))
    feed=[];excl={};hist=[]
    for r in R:
        try: price=float(r.get('price'))
        except: price=0
        desc=clean(r.get('ld_desc')) or r.get('desc') or ''
        title=r.get('h1') or r.get('ld_name') or r.get('name')
        hist.append([now,r['id'],r['slug'],r.get('stock'),'in_stock' if 'InStock' in str(r.get('availability')) else ('out_of_stock' if r.get('availability') else ''),f'{price:.2f}' if price else '',r.get('err','')])
        why='page illisible' if r.get('err') else 'prix absent' if not price else 'image absente' if not r.get('cover') else 'description vide' if len(desc)<20 else 'titre absent' if not title else None
        if why: excl[why]=excl.get(why,0)+1; continue
        feed.append({'id':r['id'],'title':title[:150],'description':desc[:5000],'link':r['link'],'image_link':r['cover'],
            'availability':'in_stock' if 'InStock' in str(r.get('availability')) else 'out_of_stock','price':f'{price:.2f} EUR',
            'brand':(r.get('brand') or '').strip(),'gtin':r['gtin'],'identifier_exists':'yes','condition':'new'})
    if len(feed)<0.8*len(P): raise SystemExit(f'Flux anormalement court ({len(feed)}/{len(P)}) : feed.tsv non remplacé')
    with open('feed.tsv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,list(feed[0]),delimiter='\t'); w.writeheader(); w.writerows(feed)
    new=not os.path.exists('stock-history.csv')
    with open('stock-history.csv','a',newline='',encoding='utf-8') as f:
        w=csv.writer(f,delimiter=';')
        if new: w.writerow(['releve','id','adresse','stock','disponibilite','prix_TTC','erreur'])
        w.writerows(hist)
    st={'releve':now,'produits':len(P),'dans_flux':len(feed),'en_stock':sum(1 for x in feed if x['availability']=='in_stock'),'exclus':excl}
    json.dump(st,open('status.json','w'),ensure_ascii=False,indent=1); print(json.dumps(st,ensure_ascii=False))
if __name__=='__main__': main()

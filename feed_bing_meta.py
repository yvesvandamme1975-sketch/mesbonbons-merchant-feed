# Construit feed-bing-meta.tsv : produits de la liste validée, quel que soit le stock (décision Yves 09/10/2026 21:10),
# à partir de feed.tsv (prix, page, image relus sur le site) et du dernier relevé de stock-history.csv.
# Disponibilité : in_stock si stock > 0 au dernier relevé, sinon out_of_stock. Ancienne version (seuil 25) : feed_bing_meta-seuil25-2026-10-08.py.
import csv,json,sys
feed,hist,allow,out=sys.argv[1:5]
csv.field_size_limit(10**8)
A=set(json.load(open(allow)))
H=list(csv.DictReader(open(hist,encoding='utf-8'),delimiter=';'))
last=max(r['releve'] for r in H)
stock={r['id']:r['stock'] for r in H if r['releve']==last}
F=list(csv.DictReader(open(feed,encoding='utf-8'),delimiter='\t'))
def n(x):
    try: return int(float(x))
    except: return -1
K=[]
for p in F:
    if p['id'] in A and p['price'] and p['gtin'] and p['image_link']:
        q=dict(p); s=n(stock.get(p['id']))
        if s>=0: q['availability']='in_stock' if s>0 else 'out_of_stock'
        K.append(q)
w=csv.DictWriter(open(out,'w',encoding='utf-8',newline=''),fieldnames=list(F[0].keys()),delimiter='\t');w.writeheader();w.writerows(K)
print(f"feed-bing-meta: {len(K)}/{len(A)} produits (relevé {last}) ; en stock {sum(1 for k in K if k['availability']=='in_stock')}")

import json, subprocess, sys
sys.dont_write_bytecode = True
import os; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from data import *
src = open(os.path.join(HERE,'template.html')).read()
a = src.index('const D = {'); b = src.index('const MODELS = Object.keys(D);')
open('/tmp/_d.js','w').write(src[a:b].replace('const D =','module.exports =').rstrip().rstrip(';'))
old = json.loads(subprocess.check_output(['node','-e','process.stdout.write(JSON.stringify(require("/tmp/_d.js")))']))
colors = {s["n"]: s["c"] for m in old.values() for s in m["stores"]}; colors.update(EXTRA_COLORS)
slug = lambda n: n.lower().replace(" ","-")
D = {}
for name, m in M.items():
    prev = old.get(name)
    maxcap = max(m["stor"].values())
    cr, fa, np_ = m["c"]
    cond = dict(flawless=1.0, good=(prev["cond"]["good"] if prev else m["good"]),
                cracked=round(min(cr/maxcap,0.95),2), faulty=round(fa/maxcap,2), noPower=round(np_/maxcap,2))
    stores = []
    for disp, o in sorted(m["o"].items(), key=lambda kv: -kv[1]):
        n = N.get(disp, disp); d, r, rv, p, lk = META[n]
        stores.append(dict(n=n, o=round(o), d=d, r=r, rv=rv, p=p, lk=lk, c=colors[n]))
    D[name] = dict(
        bmc=(prev["bmc"] if prev else f"https://www.bankmycell.com/sell/{slug(name)}"),
        iwm=(prev["iwm"] if prev else f"https://www.itsworthmore.com/sell/iphone/{slug(name)}"),
        iwmTop=m["iwm"], stor={k: round(v) for k, v in m["stor"].items()}, cond=cond, stores=stores)
nstores = len({s["n"] for m in D.values() for s in m["stores"]}); nmodels = len(D)
out = src[:a] + "const D = " + json.dumps(D, indent=2) + ";\n" + src[b:]
rep = [
 ('Compare real iPhone buyback offers from 11 top US stores. Live prices August 2026.', f'Compare real iPhone buyback offers from {nstores} top US stores. Live prices {DATE_MONTH}.'),
 ('condition, August 2026. Under 55 words.', f'condition, {DATE_MONTH}. Under 55 words.'),
 ('● Live · Aug 14 2026', f'● Live · {DATE_SHORT}'),
 ('Real prices · 11 US stores · 18 iPhone models', f'Real prices · {nstores} US stores · {nmodels} iPhone models'),
 ('Real buyback quotes from 11 major US platforms. Not estimates — scraped prices updated August 14, 2026.', f'Real buyback quotes from {nstores} major US platforms. Not estimates — scraped prices updated {DATE_LONG}.'),
 ('"Top offers · Flawless"', '"Top offers by capacity"'),
 ('on August 14, 2026. Offers shown', f'on {DATE_LONG}. Offers shown'),
 ('18 models · 11 US stores · real scraped prices · Aug 14 2026', f'{nmodels} models · {nstores} US stores · real scraped prices · {DATE_SHORT}'),
 ('Prices updated August 14, 2026 · Data from', f'Prices updated {DATE_LONG} · Data from'),
]
for o_, n_ in rep:
    assert out.count(o_) == 1, o_
    out = out.replace(o_, n_)
open(os.path.join(HERE,'index.html'),'w').write(out)
print("models", nmodels, "stores", nstores)
for k, v in D.items(): print(f"{k:18s} stores={len(v['stores']):2d} top=${max(s['o'] for s in v['stores']):<4d} iwm=${v['iwmTop']:<5d} cond={v['cond']}")

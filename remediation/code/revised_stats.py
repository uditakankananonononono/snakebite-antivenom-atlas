#!/usr/bin/env python3
import pathlib,csv,json,collections,numpy as np
from scipy import stats
R=pathlib.Path(__file__).resolve().parents[2];D=R/'remediation';O=D/'results'
def read(p):return list(csv.DictReader(open(R/p)))
def write(name,rows):
 with open(O/name,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
resolution=read('remediation/all_unit_resolution.csv');gap=read('results/gap_table.csv');assign=read('remediation/results/toxin_assignments.csv');inv=read('results/toxin_inventory.csv')
units={}
for r,g in zip(resolution,gap):
 if not r['taxid']:continue
 u=units.setdefault(r['taxid'],dict(unit_id=r['taxid'],name=r['accepted_name'],source_rows=[],categories=set(),products=set(),regions=set(),toxins=set(),inherited=False))
 u['source_rows'].append(r['source_row']);u['categories'].add(g['category']);u['products'].update(x for x in g['antivenoms'].split('|') if x);u['regions'].update(x for x in g['regions'].split('|') if x);u['inherited']|=r['inherited_group_indications']=='yes'
for a in assign:
 if a['assigned_species_taxid'] in units:units[a['assigned_species_taxid']]['toxins'].add(a['accession'])
def flatten(us):
 out=[]
 for key,u in sorted(us.items()):
  cat='1' if '1' in u['categories'] else '2' if '2' in u['categories'] else 'unknown';nt=len(u['toxins']);np_=len(u['products']);cl='CRITICAL' if np_==0 and cat=='1' else 'HIGH' if np_==0 else 'DATA GAP' if nt==0 else 'covered'
  out.append(dict(unit_id=key,name=u['name'],source_rows='|'.join(u['source_rows']),category=cat,n_toxins=nt,n_products=np_,products='|'.join(sorted(u['products'])),regions='|'.join(sorted(u['regions'])),gap_class=cl,inherited_group_indications='yes' if u['inherited'] else 'no'))
 return out
primary=flatten(units);noinherit=[x for x in primary if x['inherited_group_indications']=='no']
groups={}
for g in gap:
 k=g['species'];u=groups.setdefault(k,dict(name=k,source_rows=[],categories=set(),products=set(),regions=set(),toxins=set(),inherited=False));u['source_rows'].append(str(len(u['source_rows'])+1));u['categories'].add(g['category']);u['products'].update(x for x in g['antivenoms'].split('|') if x);u['regions'].update(x for x in g['regions'].split('|') if x)
for x in inv:
 if x['matched_species'] in groups:groups[x['matched_species']]['toxins'].add(x['accession'])
group=flatten(groups)
write('primary_units.csv',primary);write('no_inherited_indication_units.csv',noinherit);write('source_group_units.csv',group)
REG=['Africa and the Middle East','Asia and Australasia','Europe','The Americas'];CL=['CRITICAL','HIGH','DATA GAP','covered']
def holm(p):
 order=np.argsort(p);out=np.empty(len(p));mx=0
 for i,k in enumerate(order):mx=max(mx,min(1,(len(p)-i)*p[k]));out[k]=mx
 return out.tolist()
def compute(rows):
 tab=np.zeros((4,4),int)
 for r in rows:
  for reg in r['regions'].split('|'):
   if reg in REG:tab[REG.index(reg),CL.index(r['gap_class'])]+=1
 active=tab[np.any(tab,axis=1)][:,np.any(tab,axis=0)];expected=np.outer(active.sum(1),active.sum(0))/active.sum();obs=((active-expected)**2/expected).sum()
 rng=np.random.default_rng(20261008);draw=stats.random_table.rvs(active.sum(1),active.sum(0),size=9999,random_state=rng);sim=((draw-expected)**2/expected).sum((1,2));p_region=(1+int((sim>=obs-1e-12).sum()))/10000
 nt=np.array([int(x['n_toxins']) for x in rows]);nav=np.array([int(x['n_products']) for x in rows]);mask=nav>0;rho,p_s=stats.spearmanr(nt,nav)
 u,p_m=stats.mannwhitneyu(nt[mask],nt[~mask],alternative='two-sided')
 cats=[x for x in rows if x['category'] in ['1','2']];a=sum(x['category']=='1' and int(x['n_toxins'])==0 for x in cats);b=sum(x['category']=='1' and int(x['n_toxins'])>0 for x in cats);c=sum(x['category']=='2' and int(x['n_toxins'])==0 for x in cats);d=sum(x['category']=='2' and int(x['n_toxins'])>0 for x in cats);odds,p_f=stats.fisher_exact([[a,b],[c,d]],alternative='two-sided')
 raw=[p_region,float(p_s),float(p_m),float(p_f)];return dict(n=len(rows),unique_toxins=sum(int(x['n_toxins']) for x in rows),gap_classes=dict(collections.Counter(x['gap_class'] for x in rows)),region_table=tab.tolist(),region_pearson=float(obs),region_mc_p=p_region,region_expected=expected.tolist(),expected_lt5=int((expected<5).sum()),region_min_expected=float(expected.min()),region_dof=int((active.shape[0]-1)*(active.shape[1]-1)),spearman_rho=float(rho),spearman_p=float(p_s),mannwhitney_u=float(u),mannwhitney_p=float(p_m),median_covered=float(np.median(nt[mask])),median_uncovered=float(np.median(nt[~mask])),covered_n=int(mask.sum()),uncovered_n=int((~mask).sum()),fisher_table=[[a,b],[c,d]],fisher_or=float(odds),fisher_p=float(p_f),holm_p=dict(zip(['region','spearman','mannwhitney','fisher'],holm(raw))),region_inference='descriptive only; multi-region dependence and source-group geographic inheritance')
allresults={name:compute(rows) for name,rows in [('primary_taxid',primary),('no_inherited_indications',noinherit),('source_groups',group)]}
(O/'revised_statistics.json').write_text(json.dumps(allresults,indent=2)+'\n');print(json.dumps(allresults,indent=2))

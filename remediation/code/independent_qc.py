#!/usr/bin/env python3
"""Independent re-computation from committed unit CSVs, not pipeline objects."""
import pathlib,csv,json,hashlib,subprocess,numpy as np
from scipy.stats import spearmanr,mannwhitneyu,fisher_exact,random_table
R=pathlib.Path(__file__).resolve().parents[2];D=R/'remediation';out=json.loads((D/'results/revised_statistics.json').read_text());checks=[]
for key,name in [('primary_taxid','primary_units.csv'),('no_inherited_indications','no_inherited_indication_units.csv'),('source_groups','source_group_units.csv')]:
 rows=list(csv.DictReader(open(D/'results'/name)));nt=[int(r['n_toxins']) for r in rows];np_=[int(r['n_products']) for r in rows];a=[nt[i] for i,n in enumerate(np_) if n>0];b=[nt[i] for i,n in enumerate(np_) if n==0];rho,p_s=spearmanr(nt,np_);u,p_m=mannwhitneyu(a,b,alternative='two-sided')
 ft=[[sum(r['category']==cat and (int(r['n_toxins'])==0)==zero for r in rows) for zero in [True,False]] for cat in ['1','2']];odds,p_f=fisher_exact(ft)
 regions=['Africa and the Middle East','Asia and Australasia','Europe','The Americas'];classes=['CRITICAL','HIGH','DATA GAP','covered'];tab=np.array([[sum(reg in r['regions'].split('|') and r['gap_class']==cl for r in rows) for cl in classes] for reg in regions]);exp=np.outer(tab.sum(1),tab.sum(0))/tab.sum();obs=sum(((tab-exp)**2/exp).ravel());sims=random_table.rvs(tab.sum(1),tab.sum(0),size=9999,random_state=np.random.default_rng(20261008));vals=((sims-exp)**2/exp).sum(axis=(1,2));p_r=(sum(vals>=obs-1e-12)+1)/10000
 raw=[float(p_r),float(p_s),float(p_m),float(p_f)];order=sorted(range(4),key=lambda i:raw[i]);adj=[0]*4;previous=0
 for j,i in enumerate(order):previous=max(previous,min(1,raw[i]*(4-j)));adj[i]=previous
 v=out[key]
 for field,actual in [('n',len(rows)),('region_mc_p',p_r),('spearman_rho',rho),('spearman_p',p_s),('mannwhitney_u',u),('mannwhitney_p',p_m),('fisher_or',odds),('fisher_p',p_f)]:assert np.isclose(actual,v[field],rtol=1e-12,atol=1e-15),(key,field,actual,v[field])
 assert ft==v['fisher_table'] and tab.tolist()==v['region_table']
 assert all(np.isclose(x,y,rtol=1e-12,atol=1e-15) for x,y in zip(adj,[v['holm_p'][x] for x in ['region','spearman','mannwhitney','fisher']]))
 checks.append(dict(unit=key,n=len(rows),tests='four effects/p-values, contingency, Holm independently recomputed',status='PASS'))
base='0d1fd38021dc6f5fcf66f222ac640d2ad755a073';modified=[]
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',base],cwd=R,text=True).splitlines():
 if not p.startswith('remediation/'):
  actual=(R/p).read_bytes();expected=subprocess.check_output(['git','show',base+':'+p],cwd=R)
  if actual!=expected:modified.append(p)
assert not modified,modified
for p in (D/'raw').glob('*.meta.json'):
 m=json.loads(p.read_text());stem=p.name.replace('.meta.json','');raw=D/'raw'/(stem+('.tsv' if stem=='live_organisms' else '.json'));assert hashlib.sha256(raw.read_bytes()).hexdigest()==m['sha256'];assert m['http_status']==200
report=dict(recomputations=checks,outside_tree_modified=modified,raw_sha_checks='PASS',baseline=base,gates_sha256=hashlib.sha256((D/'GATES_LOCKED.md').read_bytes()).hexdigest());(D/'results/independent_qc.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

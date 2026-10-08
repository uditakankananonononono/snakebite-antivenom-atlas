#!/usr/bin/env python3
"""Cache anonymous UniProt GET taxonomy/organism evidence; strict exact names."""
import pathlib,csv,re,requests,json,hashlib,datetime,time,collections
R=pathlib.Path(__file__).resolve().parents[2];D=R/'remediation';RAW=D/'raw';RAW.mkdir(exist_ok=True)
def read(p,sep=','):return list(csv.DictReader(open(R/p),delimiter=sep))
def write(p,rows):
 with open(D/p,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
sp=read('results/consolidated_species.csv');collision=read('results/closure/identity_collisions.csv');counts=collections.Counter(r['species'] for r in sp)
def binomial(s):return bool(re.fullmatch(r'[A-Z][a-z]+ [a-z][a-z-]+',s)) and s.split()[1] not in ['spp','sp']
def candidate(r):return r['split_spp'] if binomial(r['split_spp']) else r['species'] if binomial(r['species']) and counts[r['species']]==1 else ''
names=sorted({candidate(r) for r in sp if candidate(r)});ledger=[]
def fetch(url,params,stem):
 path=RAW/(stem+'.json');meta=RAW/(stem+'.meta.json')
 if path.exists() and meta.exists():content=path.read_bytes();m=json.loads(meta.read_text())
 else:
  resp=requests.get(url,params=params,timeout=60);content=resp.content;m=dict(url=resp.url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status=resp.status_code,sha256=hashlib.sha256(content).hexdigest());path.write_bytes(content);meta.write_text(json.dumps(m,indent=2)+'\n');time.sleep(.25)
 ledger.append(dict(file=str(path.relative_to(D)),**m))
 try:return json.loads(content) if m['http_status']==200 else {}
 except Exception:return {}
records=[]
for i in range(0,len(names),20):
 batch=names[i:i+20];q=' OR '.join('scientific:"'+n+'"' for n in batch)
 j=fetch('https://rest.uniprot.org/taxonomy/search',dict(query=q,format='json',size=500),'taxonomy_batch_'+str(i//20))
 records+=j.get('results',[]);print('taxonomy batch',i//20,'responses',len(j.get('results',[])),flush=True)
# Fetch accession-specific current organism evidence in a single public bulk response.
path=RAW/'live_organisms.tsv';mp=RAW/'live_organisms.meta.json'
if not path.exists():
 rr=requests.get('https://rest.uniprot.org/uniprotkb/stream',params=dict(query='(keyword:KW-0800) AND (taxonomy_id:8570)',format='tsv',fields='accession,organism_id,organism_name'),timeout=60);path.write_bytes(rr.content);mp.write_text(json.dumps(dict(url=rr.url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status=rr.status_code,sha256=hashlib.sha256(rr.content).hexdigest()),indent=2)+'\n')
ledger.append(dict(file=str(path.relative_to(D)),**json.loads(mp.read_text())))
resolved={}
for n in names:
 hits=[x for x in records if x.get('active') and x.get('rank')=='species' and (x.get('scientificName')==n or n in x.get('synonyms',[]))]
 ids={str(x['taxonId']) for x in hits}
 resolved[n]=hits[0] if len(ids)==1 else None
out=[]
for i,r in enumerate(sp):
 n=candidate(r);hit=resolved.get(n);out.append(dict(source_row=i+1,lb_id=r['lb_id'],species_label=r['species'],split_spp=r['split_spp'],candidate=n,taxid=hit['taxonId'] if hit else '',accepted_name=hit['scientificName'] if hit else '',status='exact_live_species' if hit else 'group_or_blank_unresolved' if not n else 'no_unique_exact_live_species',group_collision='yes' if counts[r['species']]>1 else 'no',inherited_group_indications='yes' if counts[r['species']]>1 else 'no'))
write('all_unit_resolution.csv',out);write('constituent_resolution.csv',[r for r in out if r['group_collision']=='yes']);write('results/source_response_ledger.csv',ledger)
inv=read('results/toxin_inventory.csv');live={r['Entry']:r for r in csv.DictReader(open(path),delimiter='\t')};byname={r['candidate']:r for r in out if r['taxid']};assigned=[]
for r in inv:
 original=' '.join(r['organism_raw'].split()[:2]);now=live.get(r['accession'],{});current=' '.join(now.get('Organism','').split()[:2]);hit=byname.get(original)
 valid=bool(hit and current==original)
 assigned.append(dict(accession=r['accession'],baseline_matched_label=r['matched_species'],original_binomial=original,current_binomial=current,current_organism_taxid=now.get('Organism (ID)',''),assigned_species_taxid=hit['taxid'] if valid else '',assigned_species_name=hit['accepted_name'] if valid else '',status='direct_original_and_live_match' if valid else 'group_level_or_name_unresolved',from_collision_group='yes' if counts[r['matched_species']]>1 else 'no'))
write('results/toxin_assignments.csv',assigned)
summary=dict(source_rows=len(out),collision_rows=sum(r['group_collision']=='yes' for r in out),resolved_rows=sum(bool(r['taxid']) for r in out),distinct_resolved_taxids=len({r['taxid'] for r in out if r['taxid']}),collision_resolved_rows=sum(bool(r['taxid']) and r['group_collision']=='yes' for r in out),toxins_assigned=sum(bool(r['assigned_species_taxid']) for r in assigned),collision_group_toxins=sum(r['from_collision_group']=='yes' for r in assigned),collision_group_toxins_assigned=sum(r['from_collision_group']=='yes' and bool(r['assigned_species_taxid']) for r in assigned))
(D/'results/resolution_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)

#!/usr/bin/env python3
"""Read-only baseline audit plus dated source-comparison ledgers. Run from repo root.
Does not alter baseline results. Current UniProt response must already be stored.
WHO catalogue rows are preserved separately; no guessed product identity merges.
"""
import csv, pathlib, collections, json, hashlib, platform
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'results/closure';OUT.mkdir(exist_ok=True)
def read(p,sep=','): return list(csv.DictReader(open(ROOT/p),delimiter=sep))
def write(name,rows):
    with open(OUT/name,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
base=read('data/uniprot/serpentes_toxins.tsv','\t');live=read('data/closure/uniprot_live_resolution.tsv','\t');liveby={r['Entry']:r for r in live}
record=json.loads((ROOT/'data/closure/live_retrieval.json').read_text());url=record['url'];ts=record['retrieved_at_utc']
rows=[]
for r in base:
    rows.append(dict(kind='UniProt',identifier=r['Entry'],status='present_in_live_query' if r['Entry'] in liveby else 'not_in_live_query_unresolved',source_url=url,retrieved_at_utc=ts,note='Current bulk query membership, not antibody or clinical validation'))
for p in sorted({p.strip() for r in base for p in r['PDB'].split(';') if p.strip()}):
    hits=[r['Entry'] for r in live if p in r['PDB'].split(';')]
    rows.append(dict(kind='PDB',identifier=p,status='current_uniprot_xref_only' if hits else 'baseline_xref_only_unresolved',source_url=url,retrieved_at_utc=ts,note='Not a direct PDB resolution check; live cross-reference accessions: '+'|'.join(hits)))
af=read('data/alphafold/uniprot_serpentes_toxins_with_afdb.tsv','\t')
for r in af:
    a=r['Entry'];l=liveby.get(a,{});rows.append(dict(kind='AlphaFoldDB',identifier=a,status='current_uniprot_xref_only' if l.get('AlphaFoldDB') else 'baseline_xref_only_unresolved',source_url=url,retrieved_at_utc=ts,note='Availability by UniProt cross-reference, not model downloaded or confidence checked'))
sp=read('results/consolidated_species.csv')
for r in sp:
    rows.append(dict(kind='species',identifier=r['species'],status='historical_source_name_not_full_live_taxonomy_validation',source_url='https://github.com/joshlongbottom/snakebite',retrieved_at_utc='2026-09-23 (day precision from baseline sources.md)',note='Canonical baseline label retained; spelling/alias evidence in synonym tables, not proof of current accepted taxonomy'))
products=sorted({r['product'] for r in read('results/antivenom_coverage_long.csv') if r['no_specific_antivenom']=='no'})
for p in products:
    rows.append(dict(kind='product',identifier=p,status='historical_label_live_identity_unresolved',source_url='https://github.com/joshlongbottom/snakebite',retrieved_at_utc='2026-09-23 (day precision from baseline sources.md)',note='No stable product ID/manufacturer in baseline; no guessed mapping to current WHO products'))
write('identifier_validation_ledger.csv',rows)
# Preserve every baseline product and independent catalogue entry without forced identity joins.
comparison=[dict(source='Longbottom historical matrix',name=p,manufacturer='',status='historical indication label',matched_baseline_label=p,evidence='data/longbottom/repo/antivenom.csv') for p in products]
for r in read('data/closure/who_catalogue.csv'):
    comparison.append(dict(source='WHO assessment outcomes 2026-10-08',name=r['name'],manufacturer=r['manufacturer'],status=r['status'],matched_baseline_label='',evidence=r['source_url']))
write('catalogue_union_unmerged.csv',comparison)
gap=read('results/gap_table.csv');inv=read('results/toxin_inventory.csv');xr=read('results/cross_reactivity_by_toxin.csv');long=read('results/antivenom_coverage_long.csv')
uncovered={r['species'] for r in gap if r['gap_class'].startswith(('HIGH','CRITICAL'))}
assert len(sp)==294
assert len({r['species'] for r in sp})==252
assert len(inv)==5131 and sum(bool(r['matched_species']) for r in inv)==3644
assert not [r for r in long if r['species'].startswith('UNKNOWN_ID')]
assert len(xr)==sum(r['matched_species'] in uncovered for r in inv)==290
metrics=dict(base_commit='6b94d537687eaf403b493934b90523bb332172e9',inventory_records=len(sp),distinct_species_labels=len({r['species'] for r in sp}),distinct_split_labels=len({r['split_spp'] for r in sp}),species_in_both=242,lb_only=52,who_artifact_only=25,toxins=len(inv),matched_toxins=3644,species_with_toxins=170,products=len(products),long_rows=len(long),actual_indication_rows=sum(r['no_specific_antivenom']=='no' for r in long),gap_classes=dict(collections.Counter(r['gap_class'] for r in gap)),live_uniprot=len(live),baseline_accessions_in_live_query=sum(r['Entry'] in liveby for r in base),pdb_ids=len({p.strip() for r in base for p in r['PDB'].split(';') if p.strip()}),afdb_accessions=len(af),who_catalogue_rows=len(read('data/closure/who_catalogue.csv')),ledger_rows=len(rows),ledger_status_counts=dict(collections.Counter((r['kind']+': '+r['status']) for r in rows)),python=platform.python_version())
(OUT/'closure_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics,indent=2))

c=collections.Counter(r['species'] for r in sp)
write('identity_collisions.csv',[dict(lb_id=r['lb_id'],species=r['species'],split_spp=r['split_spp'],category=r['category'],repeated_label_rows=c[r['species']]) for r in sp if c[r['species']]>1])

#!/usr/bin/env python3
"""SHA256 inventory of every data/results/code/paper/QC file; --check verifies."""
import pathlib,hashlib,sys,datetime
R=pathlib.Path(__file__).resolve().parent.parent;M=R/'manifests/slice-manifest.md'
files=sorted(p for directory in ['data','results','code','paper','qc'] for p in (R/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if '--check' in sys.argv:
 lines=[l.split(' | ') for l in M.read_text().splitlines() if l.startswith('`')]
 expected={a.strip('`'):b.strip('`') for a,b,*_ in lines};actual={str(p.relative_to(R)):digest(p) for p in files}
 assert expected==actual, 'Manifest mismatch, added/removed/changed files'
 print('PASS:',len(files),'artifact hashes verified');sys.exit()
intro='''# B09 slice manifest - unsealed closeout
Baseline SHA: 6b94d537687eaf403b493934b90523bb332172e9. Closure review date: 2026-10-08.
This inventory locks ALL data/results/code/paper files plus QC. It does not cure provenance gaps.
Historical retrieval precision is day-only from data/sources.md unless separately noted.
A source group is a dependency trail, not proof of a per-file exact retrieval.
Missing exact source/timestamp evidence is explicitly marked unknown. No seal is claimed.

## Source ledger
S1 WHO TRS1004 Annex5 PDF: https://cdn.who.int/media/docs/default-source/biologicals/blood-products/document-migration/antivenomglrevwho_trs_1004_web_annex_5.pdf . Baseline: 2026-09-23 UTC day precision. Text/CSV derived by committed parsers.
S2 Longbottom associated repository: https://github.com/joshlongbottom/snakebite . Baseline archive: 2026-09-23 UTC day precision; historical upstream commit not recorded. Verified article is The Lancet DOI 10.1016/S0140-6736(18)31224-8, https://pmc.ncbi.nlm.nih.gov/articles/PMC6115328/ .
S3 UniProt stream: https://rest.uniprot.org/uniprotkb/stream . Toxin/Serpentes snapshot 2026-09-23 UTC day precision. Extra venom files exact queries/timestamps unknown where no log records them.
S4 AlphaFold xref bulk UniProt source: https://rest.uniprot.org/uniprotkb/stream . Structure summary gives 2026-09-23T18:05Z for data/alphafold table. Older duplicated table exact retrieval unknown.
S5 NCBI Taxonomy endpoints: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi and https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi . Per-file organism encoded in filename; query reconstruction in ncbi_synonym_pass.py. Exact original per-file timestamp unknown.
S6 WHO assessment list: https://extranet.who.int/prequal/vaccines/list-product-assessment-outcomes . Closure 2026-10-08 UTC day precision; raw HTML preserved. WHOPAR https://extranet.who.int/prequal/vaccines/who-public-assessment-reports-whopars-snake-antivenom . Non-exhaustive.
S7 Current UniProt bulk query: exact URL and host capture timestamp in data/closure/live_retrieval.json. Runtime review date 2026-10-08. Query membership/xrefs only.
S8 Documentation: URLs inline in official_source_extracts.txt and identifier_documentation.txt; closure runtime date 2026-10-08, exact per-page time not stored.
D1 Baseline derived: dependency graph is code/*.py with raw sources S1-S5; historical intermediate dependencies/order incomplete, see QC.
D2 Closure derived: S6/S7, baseline tables and closure scripts; runtime review date 2026-10-08. Exact publication timestamp not asserted.
A1 Authored closure code, paper and QC; no external raw source of their bytes. Depends on S1-S8/D1-D2. Review date 2026-10-08.

## Complete artifact inventory
Path | SHA-256 | Provenance group / timestamp evidence
--- | --- | ---
'''
def provenance(p):
 s=str(p.relative_to(R))
 if s.startswith('data/who/'):return 'S1; baseline day precision, derivation for non-PDF'
 if s.startswith('data/longbottom/'):return 'S2; baseline day precision, exact upstream commit unknown'
 if s.startswith('data/ncbi/'):return 'S5; exact per-file retrieval unknown'
 if s.startswith('data/alphafold/'):return 'S4; summary timestamp 2026-09-23T18:05Z'
 if s.startswith('data/uniprot/'):return 'S3/S4; baseline day precision or explicit unknown'
 if s.startswith('data/closure/uniprot') or s.endswith('live_retrieval.json'):return 'S7; stored host timestamp, runtime date distinction'
 if s.startswith('data/closure/who'):return 'S6; closure day precision'
 if s.startswith('data/closure/'):return 'S8; closure day precision'
 if s=='data/sources.md':return 'S1-S3 historical source ledger; citation error preserved'
 if s.startswith('results/closure/'):return 'D2; derived closure'
 if s.startswith('results/'):return 'D1; historical derived; missing exact generation time'
 return 'A1; authored/archived code or closure paper/QC'
M.write_text(intro+'\n'.join('`'+str(p.relative_to(R))+'` | `'+digest(p)+'` | '+provenance(p) for p in files)+'\n')
print('Locked',len(files),'artifacts')

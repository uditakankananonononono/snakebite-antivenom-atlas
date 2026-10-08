# B09 independent closeout QC
Review date: 2026-10-08. Status: UNSEALED. No COMPLETE seal is warranted.
Baseline: 6b94d537687eaf403b493934b90523bb332172e9, freshly cloned and remote-read verified.

## Verified baseline facts
- 294 inventory rows, NOT 294 independent species: 252 canonical labels; 13 group labels recur across 55 rows, 42 excess occurrences; 292 split_spp strings including group/blank labels.
- Gap classes 16 CRITICAL, 116 HIGH, 38 DATA GAP, 124 covered, all baseline row counts.
- 5,131 unique toxin accessions, 3,644 joined; 290 uncovered-label toxins scored, 38 labels.
- T=80: 161/290 passing (55.5%), 24/38 labels meet half-inventory rule. T=90: 8/38 meet it, 30/38 do not. PROGRESS and dispatch reverse that last result.
- Nine baseline Python scripts, not ten. Closure adds four scripts.
- Longbottom is The Lancet 2018;392:673-684, DOI 10.1016/S0140-6736(18)31224-8, not Nature Communications 9:2178. sources.md historical bytes preserved.
- In-scope AFDB 3,331/3,644 = 91.4% to one decimal (baseline progress 91.5% is a rounding error); PDB 222, either 3,332, both 221, neither 312. Independently recomputed from inventory and AF accession list.
- 94 historical product labels; 451 long rows include 352 actual indication rows plus 99 no-product sentinel rows.
- Region chi-square p=.0852 retained, not significant. Seven expected cells <5; min .4718; repeated regional units. Richness/product rho=.560 p=1.25e-25, MW p=1.72e-18 and Fisher OR=.44 p=.00348 remain baseline row-level exploratory results, not independent-species causal findings.

## Reproduction
Partial baseline checksums passed. Separate copy reran build_synonym_map, build_audit_tables, build_gap_table, stats_analysis, cross_reactivity with PYTHONHASHSEED=0 and edlib installed. All substantive results were byte-identical. Only results/who_longbottom_disagreement_table.csv changed (five resolved entries dropped): the synonym builder consumes an unmatched-name file narrowed by the later audit build. This is a state-dependent rerun delta, not data falsification. The original 30-row table remains unchanged. Structure-summary generator is absent; some old negatives are historical intermediate outputs. Full G5 therefore does not pass.

## Bounded remediation
Independent WHO assessment catalogue captured as HTML and parsed into 30 regional rows /29 distinct name strings (3 positive outcome rows, 27 under assessment rows). Table headers excluded and section order inspected. No identities guessed between WHO and the 94 historical product labels. WHO says list is non-exhaustive and listing is not general national approval.
Current UniProt bulk response contains all 5,131 original accessions and references all 553 original PDB IDs and 4,644 AF-linked accessions. The 10,716-row ledger differentiates current query membership, cross-reference-only evidence and unresolved historical identities. No direct structure-object validation or full live species/product resolution is claimed.

## Locked gate assessment
G1 PARTIAL: all bytes locked, but missing baseline per-file source/timestamp records are explicitly unknown, not invented.
G2 BLOCKED: generic product identities, full taxonomy resolution and direct structure-object resolution incomplete.
G3 PARTIAL: dated genuine second catalogue added; historical catalogue identity reconciliation remains unresolved; WHO and Longbottom species sources share provenance.
G4 PARTIAL: seven historical negative files preserved and paper negatives reported; no full independent expired-lookup/product-without-indication ledgers.
G5 PARTIAL: substantive core reproduced, disagreement-table delta documented, some missing generators/intermediate histories.
G6 PASS: every file under data/results/code/paper SHA-256 locked, checker verifies bytes. QC also included as supplementary locks.
G7 paper arc delivered: problem/background/hypothesis/methods/stats/results/negatives/tool; addition over named prior art quantified as data resolution, not an invented performance benchmark.
G8 PASS: data access only, no spending or messages as user. No push performed by this closer.

## Visual inspection and format
20-page PDF rendered; all pages inspected in a contact sheet, pages 1-2 at full size, dense appendices inspected separately. Times PDF body, blue page borders, two source-derived charts, readable table hierarchy, no clipped text seen. DOCX was rendered using LibreOffice to a 20-page PDF, then inspected as an all-page contact sheet plus title and dense catalogue page at full size. Blue borders and Times-family text render cleanly without clipping. DOCX is editable and may paginate differently in other editors; the authored PDF remains authoritative fixed layout.
PDF dates reflect host clock metadata; report date is the runtime task date. Source capture dates are separately documented rather than promoted into historical retrieval proof.

## Completion boundary
The paper/manifest/review kit is delivered as an unsealed closeout. GATES_LOCKED.md, original data, original code and original results are preserved byte-for-byte. No new science is substituted to make a gate pass. Future work needs stable IDs, direct validation, genuine provenance records and a revised scientific unit before COMPLETE can be considered.

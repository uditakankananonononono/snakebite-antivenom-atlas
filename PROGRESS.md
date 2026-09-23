# PROGRESS - venom-toxin data audit slice
2026-09-23 (run 1, replacement builder). Gates locked standalone in commit 4c965fe BEFORE any results.

## Done
- GATES_LOCKED.md committed standalone and pushed.
- Sources pulled, checksummed (manifests/checksums-2026-09-23.partial.txt):
  WHO TRS1004 Annex5 PDF (official Cat1/Cat2 appendix), Longbottom2018 supp data
  (294 species + 99-antivenom matrix), UniProt Serpentes toxin pull (5131 entries, TSV+FASTA).
- WHO appendix species extraction: 256 species (code/extract_who_species.py,
  genus whitelist = Longbottom + UniProt genera; rejects dumped to results/negatives/).
- Methods decision (recorded negative): WHO PDF two-column layout makes automated
  country attribution unreliable -> species-level extraction only; country/category
  per species comes from Longbottom structured CSV. Old country-parser attempt kept
  at git history, superseded.

## Done (contd, run 1)
- results/consolidated_species.csv: 291 species; 232 both sources, 30 WHO-only, 59 LB-only.
- results/toxin_inventory.csv: 5131 toxins, 3516 matched to in-scope species, 18-family
  rule-based classification (mapping documented in code/build_audit_tables.py).
- results/antivenom_coverage_long.csv: 94 products, 451 species-product pairs.
- results/gap_table.csv: per-species gap class by WHO region:
  16 CRITICAL (Cat1 + no antivenom listed), 113 HIGH (no antivenom), 41 DATA GAP
  (covered but zero toxin records), 121 covered.

## Done (contd, run 1 end)
- NCBI taxonomy pass over all 114 orphan toxin organisms (raw esearch/esummary JSON
  cached in data/ncbi/): 5 are WHO-2017 appendix species MISSED by Longbottom
  (T. stejnegeri 68 toxins, T. albolabris 18, Gloydius blomhoffii 12,
  T. purpureomaculatus 5, Lachesis stenophrys 1) - reintegrated; 109 confirmed
  non-listed negatives; 0 direct synonyms (lebetinus/ikaheca are NCBI-accepted
  distinct spellings - taxonomy split, documented). Key paper finding:
  WHO-2017 vs Longbottom-2018 species-list drift.
- Tables re-run: 296 species, 3620/5131 toxins matched, 168 species with toxin data.

## Done (structure coverage)
- results/structure_coverage.txt: in-scope toxins 3620; PDB experimental structures
  221 (6.1%); AlphaFoldDB models 3307 (91.4%). Experimental-structure gap is a
  paper finding; AlphaFold used as predicted-structure layer (documented as such).

## Next (in order)
1. (synonym pass done - see above)
2. Clean who_species_not_in_longbottom negatives (bare genera / 'complex' phrases vs
   true taxonomy drift like Gloydius blomhoffii) -> disagreement table for paper.
3. Quiet region_validation.txt noise (277 flags are name-fragment false alarms,
   e.g. subsection ordering; verify section line ranges) - region map itself stands.
4. AlphaFold DB availability per toxin accession + RCSB PDB detail pull.
5. Cross-reactivity heuristic: cluster toxins by family (3FTx/PLA2/...), pairwise
   identity of uncovered-species toxins vs antivenom-covered species -> inferred coverage.
6. Stats (region x gap contingency, toxin-richness vs coverage correlation),
   coverage_atlas.py tool, paper (Times font, blue borders), full slice manifest, seal.

## Blockers/notes
- Deploy key rotated to this builder; push works (4c965fe on origin/main).

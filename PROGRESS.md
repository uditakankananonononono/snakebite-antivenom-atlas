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

## Next (in order)
1. Cross-check WHO-appendix species vs Longbottom species (synonym-aware via its
   previous/alternate/new name columns) -> consolidated species table + disagreement table.
2. Join UniProt toxins to consolidated species -> per-species toxin inventory,
   family classification, PDB xref + evidence flags; negatives = species with 0 toxins.
3. Parse antivenom.csv into long-form coverage (species x product).
4. AlphaFold DB availability per toxin accession (API), RCSB PDB mapping.
5. Coverage-gap scoring (direct coverage + toxin-similarity cross-reactivity heuristic),
   stats, tool, paper (Times font, blue borders), full slice manifest.

## Blockers/notes
- Deploy key rotated to this builder; push works (4c965fe on origin/main).

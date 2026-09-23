
## Done (run 2, replacement builder, 2026-09-23 ~23:30 IST)
- Step 2 DONE: code/build_synonym_map.py classifies all 30 who_species_not_in_longbottom
  entries -> results/who_longbottom_disagreement_table.csv: 8 column-split fragments,
  8 genus headers, 7 complex phrases, 2 prose/citation bleeds (parse artifacts);
  4 spelling variants + 1 genus transfer resolved to Longbottom rows (evidence per row).
  ZERO true WHO-only species among the 30. Paper finding strengthened.
- Root-caused two consolidated_species bugs: (a) comma-separated Longbottom synonym
  fields were never split -> false in_who=no (Eristocophis macmahoni 118);
  (b) NCBI reintegration added synonym duplicates -> Gloydius blomhoffii/blomhoffi and
  Lachesis stenophrys/stenophyrs double-counted (296 -> 294 unique species).
- results/synonym_map_applied.csv: 8 curated pairs w/ evidence; build_audit_tables.py
  patched to apply them (comma-split fix, WHO->LB bridge, dedupe, toxin joins).
- results/lb_synonym_resolution.csv: Gloydius brevicauda (18) + Eristicophis macmahoni (6)
  toxins join LB (rule 4_lb_listed); Echis multisquamatus + Tropidolaemus wagleri joins
  REJECTED (name only in a synonym field = taxonomy drift, kept as honest negative, rule 5).
- Step 3 DONE: region_validation noise root-caused - build_gap_table.py used splitlines();
  pdftotext form feeds split lines, shifting SECT ranges off by up to 191 lines.
  Fixed to split('\n'); region map itself was correct.

## Next (updated)
DONE (run 2 contd): deploy key rotated 23:17 IST; cloned; all manifest checksums verified OK.
   Pipeline rerun (synonyms -> audit tables -> gap table): 294 species (242 both sources /
   25 artifact-only WHO unmatched / 52 LB-only), 3644/5131 toxins matched (+24), 170 species
   with toxin data. Gap classes: 16 CRITICAL, 116 HIGH, 38 DATA GAP, 124 covered.
   region_validation flags 277 -> 25 (form-feed fix). One binding-order bug caught in review:
   curated WHO names now bind only to their synonym target row (acrochorda/stenophrys).
1. Update structure_coverage numbers for the +24 matched toxins (AFDB/PDB pull, next-step 4).
2. AlphaFold/PDB detail pull; 3. cross-reactivity heuristic; 4. stats + coverage_atlas.py
   + paper + full slice manifest + seal.
## Blockers
- SSH push pending: my ed25519 public key sent to parent 23:14 IST; clone+push blocked until
  deploy key rotates. UniProt TSV/FASTA (>1MB) not retrievable via GitHub file API - exact
  manifest-verified bytes need the clone. All run-2 code+outputs preserved in this commit.

## Done (run 2 contd, ~23:38 IST)
- Step 4 (part): AFDB availability per accession re-pulled via UniProt database:alphafolddb
  (one bulk query, 4644/5131, data/alphafold/...tsv, sha256 c321e055...). Structure coverage
  recomputed on corrected inventory: in-scope 3644, AFDB 3331 (91.5%), PDB 222 (6.1%).
- Step 5 DONE: code/cross_reactivity.py - uncovered-species toxins (CRITICAL+HIGH) vs
  covered-species toxins within family; 8-mer prefilter + edlib global identity; thresholds
  60/70/80/90 as sensitivity analysis. 290 toxins / 38 species scored. At T=80: 55.5% of
  toxins and 24/38 species have >=50% inventory inferred-covered. Honest negatives:
  8 species lack even a 90%-identity homolog for half their inventory; heuristic stated
  as upper bound, not clinical efficacy.

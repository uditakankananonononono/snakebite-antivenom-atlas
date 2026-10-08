# B09 remediation: constituent evidence and revised units
Date: 2026-10-08. No B09 re-seal judgment. B09/B10 baseline immutable.

## Answer
Direct species-name evidence resolves all 154 toxin accessions previously assigned
to repeated group labels, without transferring group toxin counts to every constituent.
Only 39 of 55 collision rows have exact accepted live-species matches. Sixteen remain
unresolved under the locked policy. Across all source rows, 251 validate and merge
into 248 distinct taxids. Primary direct assignment accounts for 3,603 accessions.
The remaining 1,528 snapshot accessions are not assigned to primary units; this is not
proof that toxins are absent, and includes out-of-scope or unresolved identities.

## What changed
Historical analysis treats 294 rows as species. Revised primary analysis uses 248
distinct validated taxids. The source-group sensitivity collapses the 294 rows to 252
labels, but those labels are not all species. The indication-inheritance sensitivity
excludes every unit sourced through a collision group, leaving 209 taxids.
No new products, species mining, WHO derivation or B10 changes were performed.

## Results side by side
Unit | n | Region p | Spearman rho | Spearman p | MW p | Fisher OR | Fisher p
--- | --- | --- | --- | --- | --- | --- | ---
Historical source rows | 294 | .0852 (asymptotic) | .560 | 1.25e-25 | 1.72e-18 | .44 | .00348
primary_taxid | 248 | 0.1862 (MC) | 0.555373 | 1.80623e-21 | 4.14536e-16 | 0.385281 | 0.00130994
no_inherited_indications | 209 | 0.3688 (MC) | 0.584857 | 1.42854e-20 | 2.44854e-14 | 0.491228 | 0.0253239
source_groups | 252 | 0.3858 (MC) | 0.539811 | 1.84777e-20 | 2.43048e-14 | 0.398762 | 0.00158856

### Holm-adjusted p-values
Unit | Region | Spearman | MW | Fisher
--- | --- | --- | --- | ---
primary_taxid | 0.1862 | 7.2249084e-21 | 1.2436079e-15 | 0.0026198816
no_inherited_indications | 0.3688 | 5.7141688e-20 | 7.345619e-14 | 0.050647881
source_groups | 0.3858 | 7.3910951e-20 | 7.2914416e-14 | 0.0031771211

## Which conclusions survive, weaken or die
- Richness/product association remains positive and significant after Holm in primary
  and both sensitivities. This is an association conditional on annotation and source
  labels, not causal or clinical evidence.
- The covered/uncovered toxin-count difference remains significant after Holm in all
  three revised analyses, with medians and group sizes stored in revised_statistics.json.
- Category-1 rows have fewer zero-toxin units than category-2 in primary and group
  sensitivity. The conclusion WEAKENS in the inheritance-exclusion sensitivity:
  OR=.49123, raw p=.02532, Holm p=.05065. It is not robust across locked sensitivities.
- Regional dependence was never established historically. All revised descriptive
  Monte Carlo p-values remain non-significant. Multi-region dependence prevents any
  confirmatory regional claim regardless of a p-value. No historical direction reverses.

## Policy and methods
Gates locked standalone before new response/results collection. Scientific-name
candidates were sent to live UniProt taxonomy search in 15 batches, with exact name,
active species rank and unique taxid required. No fuzzy matching or alternate spelling
search was added after failures. Parent/species synonym renames therefore often remain
unresolved. Original and current UniProt organism binomials must both match a validated
constituent; no toxin is assigned just because its baseline group has constituent rows.
Current organism taxid may be a subspecies, while assigned species taxid is separately
live validated. That distinction is explicit in the assignment ledger.

Primary category resolves 1 over 2, with unknown excluded from Fisher. Duplicate taxids
merge once with accession, product-label and region unions. Group product/country
context remains historical source evidence, not validated constituent indications or
geography. The exclusion sensitivity handles group-product inheritance conservatively.
For region counts a unit appears in each source region. Fixed-margin random contingency
simulation uses Pearson statistic, 9999 draws, seed 20261008 and add-one p correction.
This is descriptive, not a permutation preserving individual multi-region memberships.
Holm correction covers the four primary tests; sensitivity corrections are separate.

## Scope and limits
The exact-match policy does not recover all renamed species. Forty-three source rows
are unresolved overall. Three duplicate accepted taxids merge, leaving 248 units.
No full neutralization or current product identity validation exists. Outside-collision
historical product/geographic ambiguity also remains. Source-specific findings do not
become broader biological conclusions. B09 remains documented-unsealed; this slice
strengthens its identity and unit evidence only. No re-seal or B10 reevaluation is claimed.

## Evidence and reproducibility
- constituent_resolution.csv: all 55 collision rows with source labels, candidates,
  accepted names, taxids and resolution/indication-inheritance status.
- all_unit_resolution.csv: all 294 source rows.
- results/toxin_assignments.csv: all 5,131 snapshot accessions, direct evidence status.
- results/primary_units.csv and two sensitivity unit CSVs: inputs to statistical analysis.
- results/revised_statistics.json: exact values, tables, expected counts and Holm values.
- raw/: exact live response bytes and URL/time/status/SHA256 metadata.
- results/HONEST_NEGATIVES.md: unresolved, zero-toxin, missing-region and inherited-context records.
- LOCK_ORDER_PROOF.md and QC_RECORD.md: lock order and independent recomputation.
Source: https://rest.uniprot.org/taxonomy/search and
https://rest.uniprot.org/uniprotkb/stream . Exact query URLs are in raw metadata and
results/source_response_ledger.csv. Historical analysis remains in results/stats_summary.txt.

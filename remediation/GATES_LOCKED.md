# B09 remediation gates - locked before new outcomes
Date: 2026-10-08. Baseline 0d1fd38021dc6f5fcf66f222ac640d2ad755a073.
Purpose: resolve group-to-constituent evidence and audit changed scientific units.
This is not a B09 re-seal and not B10 modeling. All paths outside remediation/ immutable.

G1 LOCK ORDER. This document is the only file in its standalone first commit.
Record commit ancestry, SHA256 and baseline identity before any new results.
G2 PROVENANCE. Anonymous public GETs only; cache live taxonomy/UniProt response bytes
with exact URL, UTC capture time, status and SHA256. Empty/error/ambiguous returns
are retained; no guessed taxonomy identity. No money or external representation.
G3 RESOLUTION. All 55 collision rows must have a resolution record. Candidates are
binomial split_spp strings; group/blank strings cannot count as constituent species.
Use exact accepted scientific-name match from NCBI live taxonomy, or exact validated
scientific-name synonym if returned. No fuzzy spelling or most-common-constituent
substitution. Retain source label, constituent name, taxid and evidence status.
Assign toxin only when its ORIGINAL UniProt organism binomial directly matches a
constituent label or exact scientific synonym accepted by the live source. No
indication of inferred toxin transfer from group to every constituent. Ambiguous
candidate taxids/organisms remain unresolved. Live UniProt organism evidence must
support the accession, not merely a group annotation.
G4 UNIT. Primary unit = distinct live-taxonomy-validated constituent taxid.
For collision rows use split_spp; other rows use split_spp when binomial, otherwise
species when binomial. Exclude unresolved/group-only rows in primary analysis.
Combine duplicate taxids once: toxin accession union, product-label union, region
union. Category 1 wins over 2; unknown category remains excluded from category test.
Products are inherited SOURCE GROUP indication context, not independently verified
constituent efficacy. All such inheritance flagged and sensitivity-excluded.
Primary taxonomy-resolved analysis is conditional on existing source rows; no new
species/product mining. Recount toxins directly from raw live organism labels, not
by copying baseline group toxin counts into each constituent.
G5 SENSITIVITIES. (A) Distinct original source group label once, baseline accession
union and product/region union; no claim groups are species. (B) Primary resolved
units excluding inherited group-product contexts. Show both beside historical rows.
No unresolved group is added to primary species estimates.
G6 TEST FAMILY. Four tests: region x gap, Spearman richness/product count,
Mann-Whitney richness listed-covered/uncovered, Fisher category x zero-toxin.
Two-sided, alpha .05; Holm correction across the four PRIMARY tests. Historical
p-values preserved raw; sensitivities separately descriptive, Holm displayed each.
Region test uses primary source unit row occurrence in each of four regions as
historical descriptive comparison. Because multi-region units violate independent
contingency assumptions, use fixed-margin permutation p as a DESCRIPTIVE test only,
not confirmatory geographic inference. Sparse cells: ALWAYS use fixed-margin
Monte Carlo Pearson statistic, 9999 draws, seed 20261008, p=(exceedances+1)/10000;
show expected counts and number <5. Do not use asymptotic p as primary evidence.
Degenerate/empty tests yield null status and p=1 for multiplicity, not fake effects.
G7 CHANGE CRITERIA. Numerical change: report all count/effect/p deltas. A historical
significant conclusion survives only if its revised effect direction agrees and
Holm p<.05; otherwise weakens (same direction, non-significant) or reverses (opposite).
Region inference is ALWAYS limited by dependence; a significant descriptive p does
not rescue a regional biological claim. No discovery/clinical/causal language.
G8 HONEST NEGATIVES/QC. Keep every unresolved identity, zero assigned toxin unit,
missing region, source-group indication inheritance and failed live lookup.
Independent recompute headline test values from stored revised-unit CSV, not memory.
Hash every remediation artifact except MANIFEST.sha256 itself. Review outside-tree
byte equality against baseline before handoff. Failed gates explicit, no forced seal.

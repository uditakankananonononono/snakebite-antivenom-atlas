# GATES LOCKED — snakebite-antivenom-atlas / MODELING slice (B10)
Locked: 2026-10-08 by the B10 builder agent, baselined on repo main 6b94d537687eaf403b493934b90523bb332172e9.
This commit is STANDALONE: no modeling outcome artifacts (scores, metrics, calibration
outputs, figures, paper) exist at this commit. Gates below are frozen for this slice and
enforced by independent QC before seal. The stale 2026-09-24 closer-spec numbers
(19,760 scores, R=0.9998, 26x20 panel, India 4/3/240) exist in no durable record; they
are NOT used, targeted, or reported anywhere in this slice.

This slice inherits the eight B09 audit gates (root GATES_LOCKED.md, commit history)
and adds the modeling-specific gates M1-M10 below. "Outcome data" = antivenom-product
labels used for evaluation; nothing below the lock may be tuned after seeing them.

## Panel and labels
- GATE M1 PANEL FROM COMMITTED DATA ONLY: the panel derives exclusively from the
  committed B09 artifacts (results/toxin_inventory.csv, results/gap_table.csv,
  results/antivenom_coverage_long.csv, data/uniprot/serpentes_toxins.fasta,
  data/alphafold/uniprot_serpentes_toxins_with_afdb.tsv). TARGET set = toxins of
  CRITICAL/HIGH gap-class species with a sequence (290 toxins, 38 species, 11 families).
  REFERENCE set = toxins of covered / DATA-GAP-covered species with a sequence
  (3,354 toxins, 106 species). LABEL SOURCE = the committed species x product
  indication matrix (antivenom_coverage_long.csv; 141 species, 94 products), itself
  grounded in WHO TRS1004 Annex 5 + the Longbottom 2018 matrix. No refetch of labels.
- GATE M2 LEAKAGE-SAFE SPLIT: evaluation uses a SPECIES-LEVEL split of the covered
  species that have >=1 toxin with sequence AND >=1 listed product: 80% calibration /
  20% test, stratified by region, RNG seed fixed here at 20261008 (numpy
  default_rng). Test-species toxins are scored using ONLY references from
  calibration-split species; any toxin's own species is additionally excluded from
  its reference pool everywhere (calibration, test, and target scoring). No random
  toxin-pair or species-pair splitting. Per-family performance is reported.

## Comparators (named, frozen)
- GATE M3 NAIVE CONTROL: product-prior predictor. score_naive(t,p) = fraction of
  calibration-split species with toxins that are indicated for product p; identical
  for all toxins. This is the "no information about the toxin" floor.
- GATE M4 BASELINE: the committed B09 sequence-identity heuristic
  (code/cross_reactivity.py): best within-family edlib global identity to a
  covered-species toxin after the 8-mer prefilter; toxin inferred-covered at T=80;
  species majority rule. Re-implemented in modeling/code and verified against the
  committed results/cross_reactivity_by_toxin.csv and cross_reactivity_summary.txt
  before use (equivalence evidence committed).

## Model (frozen definition)
- GATE M5 CASCADE SCORE: for target toxin t and product p:
    S(t,p) = max over references r in R(t,p) of  0.4*I(t,r) + 0.4*TM(t,r) + 0.2*E(t,r)
  where R(t,p) = the top-K=10 covered-species references for t by sequence identity
  within family(t) (same 8-mer prefilter as baseline) whose species is indicated for
  p. I = global identity / 100. TM = TM-score over the edlib alignment-path CA
  correspondence between AFDB models (Kabsch superposition, d0 = 1.24*L^(1/3) - 1.8
  clamped >= 0.5, L = shorter aligned length). E = fraction of aligned positions that
  are solvent-exposed in BOTH models (CA neighbor count within 10 A <= 16) AND share
  the same physicochemical class ({AVLIM},{FWY},{STNQ},{KRH},{DE},{CGP}); E=0 and
  flagged if no both-exposed aligned positions exist. If a structure is missing for
  a shortlisted pair, that pair contributes the sequence-only fallback S = I and is
  flagged; all fallbacks are preserved as honest negatives, never silently dropped.
- GATE M6 CALIBRATED THRESHOLD: one global decision threshold tau on S is calibrated
  on the calibration split ONLY (pair-level labels, max Youden's J), then frozen and
  applied unchanged to the test split and the target set. Calibration curves and the
  tau search grid are committed.
- GATE M7 METRICS + WIN CRITERION: primary metric = pair-level AUPRC on the held-out
  test split for MODEL vs BASELINE vs NAIVE. Secondary = species-level
  majority-coverage sensitivity at frozen tau (test split) and target-set modeled
  coverage vs the heuristic's committed T=60/70/80/90 table. A win claim requires
  MODEL > BASELINE on the primary metric with a paired-bootstrap (1000 resamples,
  seed 20261008) 95% CI for the difference excluding zero; otherwise the result is
  reported as a negative. Per-family breakdowns are reported for all three predictors.

## Provenance, reproducibility, scope
- GATE M8 STRUCTURE PROVENANCE: AFDB models are fetched via the official AlphaFold DB
  API (api/prediction/{accession}, latest version 6 at lock time); each downloaded
  model records URL, retrieval timestamp (UTC), API-reported global pLDDT, and sha256
  in the slice manifest. Failed/absent models are preserved as negatives.
- GATE M9 CONDITIONAL INDIA ADDENDUM: an India-relevant addendum is computed ONLY if
  >=3 CRITICAL/HIGH species with toxin records occur in India per the committed
  gap_table countries field; otherwise the addendum is declared unsupported and that
  is reported as an honest negative. (Input-data check at lock time: 4 such species
  occur in IND but 0 have toxin records, so the addendum is expected to be reported
  unsupported.)
- GATE M10 ACCESS ONLY: free tools and public APIs only (AFDB, UniProt-derived
  committed tables; edlib, numpy/scipy/scikit-learn, matplotlib). No money, no
  accounts created, nothing sent as the user. All results regenerate from
  modeling/code/ against committed inputs; manifests sha256-lock every artifact under
  modeling/ before seal.

Status: LOCKED. Changes to this file after this commit invalidate the seal.

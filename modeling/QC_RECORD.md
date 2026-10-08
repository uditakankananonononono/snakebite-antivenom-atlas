# B10 modeling slice - QC RECORD (2026-10-08)

## 1. Lock order (gates before outcomes)
  fad3e96 B10 modeling slice: GATES_LOCKED (standalone, pre-outcome) - panel, leakage-safe species split, named comparators, frozen cascade score, calibrated-threshold + win criterion, provenance/reproducibility gates
  6223453 B10 modeling: panel + seeded split, baseline equivalence verified vs committed heuristic, AFDB v6 shortlist fetch (3331/3331 ok, sha256-locked, API metadata cached)
  69145e0 B10 modeling results: cascade scores (62,475 pairs), tau=0.5727 calibrated on calibration split, test AUPRC model 0.0910 vs baseline 0.0694 vs naive 0.0661 (paired-bootstrap 95% CI for delta [+0.0087,+0.0383] - WIN per GATE M7), target coverage 55.9% vs 55.5% heuristic, India addendum unsupported (honest negative), 5 figures
  gates commit fad3e96 touches ONLY modeling/GATES_LOCKED.md:
     modeling/GATES_LOCKED.md | 84 ++++++++++++++++++++++++++++++++++++++++++++++++
     1 file changed, 84 insertions(+)

## 2. Baseline equivalence (GATE M4)
  identity/best-hit mismatches: 0
  EQUIVALENT

## 3. Stale-spec numbers quarantine (19,760 / 0.9998 / 26x20 / India 4-3-240)
  modeling/QC_RECORD.md:15:## 3. Stale-spec numbers quarantine (19,760 / 0.9998 / 26x20 / India 4-3-240)
  modeling/GATES_LOCKED.md:6:(19,760 scores, R=0.9998, 26x20 panel, India 4/3/240) exist in no durable record; they
  modeling/paper/paper.tex:44:A secondary, equally important constraint shaped the work. A September 24 closer specification quoted precise modeling numbers for t
  (every occurrence above is an explicit DO-NOT-USE statement in GATES_LOCKED.md or the paper; none is a reported result)

## 4. Honest negatives present
  - structure fallbacks flagged in results/pair_features.csv + scores_eval.csv.gz
    fallback rows (incl header): 17913
  - India addendum (GATE M9):
    GATE M9 INDIA ADDENDUM: CRITICAL/HIGH species occurring in IND per committed gap_table: ['Bungarus magnimaculatus', 'Hypnale hypnale', 'Trimeresurus gramineus', 'Trimeresurus malabaricus']; of these, 

## 5. Independent recomputation spot checks
  recompute test AUPRC: model 0.0910 baseline 0.0694 naive 0.0661 (paper: 0.0910/0.0694/0.0661)
  recompute target coverage: model 162/290 baseline-T80 161/290 (paper: 162/161; committed 161)
  evaluation.txt consistent with recomputation: OK

## 6. Gate compliance checklist
  M1 panel from committed data only: PASS (code reads only results/, data/, panel CSVs)
  M2 species-level split, seed 20261008, own-species excluded: PASS (panel.py, shortlist.py)
  M3/M4 comparators named + baseline verified equivalent: PASS
  M5 frozen formula + declared fallbacks: PASS (score.py, flags column)
  M6 tau from calibration split only: PASS (calibration.txt, tau=0.5727)
  M7 win criterion: MET (delta AUPRC CI [+0.0087,+0.0383] excludes 0)
  M8 structure provenance (URL/ts/pLDDT/sha256): PASS (FETCH_MANIFEST.csv, 3331 rows)
  M9 India addendum: UNSUPPORTED, reported as honest negative: PASS
  M10 access only, free tools: PASS
  Paper arc (GATE 7 analog) + 17pp PDF, Times, blue borders, 7 figures, 5 tables: PASS

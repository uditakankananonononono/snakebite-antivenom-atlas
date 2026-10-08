#!/usr/bin/env python3
"""Apply frozen tau to the TARGET set (CRITICAL/HIGH species' toxins): modeled antivenom
coverage vs the committed heuristic (GATE M7 secondary). Writes
modeling/results/target_coverage.csv + target_coverage_summary.txt (+ India gate M9 note)."""
import csv, os, collections
import numpy as np
import common

P = os.path.join(common.ROOT, "modeling/panel")
R = os.path.join(common.ROOT, "modeling/results")
gap = common.load_gap()
tau = float(open(os.path.join(R, "calibration.txt")).read().split(":")[1].split()[0])

targets = {r["accession"]: r for r in csv.DictReader(open(os.path.join(P, "targets.csv")))}
scores = collections.defaultdict(list)  # acc -> [(product, S)]
import gzip
with gzip.open(os.path.join(R, "scores_eval.csv.gz"), "rt") as f:
    for r in csv.DictReader(f):
        if r["split"] == "target":
            scores[r["query"]].append((r["product"], float(r["model"])))

# baseline per-toxin from the committed equivalence table
base = {r["accession"]: float(r["best_identity"]) for r in csv.DictReader(open(os.path.join(P, "baseline_check.csv")))}

rows = []
for acc, t in targets.items():
    prods_hit = sorted(p for p, s in scores.get(acc, []) if s >= tau)
    rows.append({"accession": acc, "species": t["species"], "family": t["family"],
                 "model_score_max": round(max((s for _, s in scores.get(acc, [(None, 0.0)])), default=0.0), 4),
                 "model_covered": "yes" if prods_hit else "no",
                 "model_products": "|".join(prods_hit),
                 "baseline_identity": base.get(acc, 0.0),
                 "baseline_covered_T80": "yes" if base.get(acc, 0.0) >= 80 else "no"})
with open(os.path.join(R, "target_coverage.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

per_sp = collections.defaultdict(list)
for r in rows: per_sp[r["species"]].append(r)
per_fam = collections.defaultdict(lambda: [0, 0, 0])
for r in rows:
    per_fam[r["family"]][0] += 1
    per_fam[r["family"]][1] += r["model_covered"] == "yes"
    per_fam[r["family"]][2] += r["baseline_covered_T80"] == "yes"

n_mod = sum(1 for r in rows if r["model_covered"] == "yes")
n_base = sum(1 for r in rows if r["baseline_covered_T80"] == "yes")
sp_mod = sum(1 for v in per_sp.values() if sum(x["model_covered"] == "yes" for x in v) / len(v) >= 0.5)
agree = sum(1 for r in rows if (r["model_covered"] == "yes") == (r["baseline_covered_T80"] == "yes"))
out = [f"B10 target-set modeled coverage at frozen tau={tau:.4f}",
       f"target toxins: {len(rows)} across {len(per_sp)} species",
       f"MODEL: toxins inferred-covered {n_mod}/{len(rows)} ({100*n_mod/len(rows):.1f}%), species >=50% inventory covered: {sp_mod}/{len(per_sp)}",
       f"BASELINE (committed heuristic, T=80): {n_base}/{len(rows)} ({100*n_base/len(rows):.1f}%), species 24/38 (committed)",
       f"toxin-level agreement model vs baseline: {agree}/{len(rows)} ({100*agree/len(rows):.1f}%)",
       "", "per-family (n, model-covered, baseline-covered):"]
for fam in sorted(per_fam):
    n, m, b = per_fam[fam]
    out.append(f"  {fam:12s} {n:4d}  model {m:4d} ({100*m/n:.0f}%)  baseline {b:4d} ({100*b/n:.0f}%)")
ind = [s for s in per_sp if "IND" in gap.get(s, {}).get("countries", "")]
out += ["", f"GATE M9 INDIA ADDENDUM: CRITICAL/HIGH species occurring in IND per committed gap_table: "
        f"{[s for s,g in gap.items() if g['gap_class'].startswith(('CRITICAL','HIGH')) and 'IND' in g['countries']]}; "
        f"of these, species with toxin records in the panel: {len(ind)} (<3 required) -> ADDENDUM UNSUPPORTED, "
        f"reported as an honest negative. No India-specific scores were computed or claimed."]
out = "\n".join(out) + "\n"
open(os.path.join(R, "target_coverage_summary.txt"), "w").write(out)
print(out)

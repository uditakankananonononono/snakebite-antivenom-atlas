#!/usr/bin/env python3
"""GATE M5/M6/M7: assemble predictor scores, calibrate tau, evaluate.
Predictors per (query toxin, product) pair:
  MODEL    S = max over top10 of 0.4*I + 0.4*TM + 0.2*E (sequence-only fallback S=I, flagged)
  BASELINE S = best within-family identity to an indicated-species reference / 100
  NAIVE    S = calibration-split product prior (identical for all toxins)
Labels: product indicated for the query toxin's species (committed matrix).
tau calibrated on calibration pairs (max Youden J), frozen, applied to test + targets.
Outputs: modeling/results/{scores_eval.csv.gz, calibration.txt, evaluation.txt,
         target_coverage.csv, target_coverage_summary.txt, per_family.csv}
"""
import csv, os, collections, gzip
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score
import common

P = os.path.join(common.ROOT, "modeling/panel")
R = os.path.join(common.ROOT, "modeling/results")
rng = np.random.default_rng(common.SEED)

prods = common.load_products()
eval_sp = {r["species"]: r["split"] for r in csv.DictReader(open(os.path.join(P, "eval_species.csv")))}
products = [r["product"] for r in csv.DictReader(open(os.path.join(P, "products.csv")))]
cal_species = {s for s, v in eval_sp.items() if v == "calibration"}

# pair features lookup
pf = {}
for r in csv.DictReader(open(os.path.join(R, "pair_features.csv"))):
    pf[(r["query"], r["ref"])] = r

def pair_score(q, ref, ident):
    f = pf.get((q, ref))
    I = ident / 100.0
    if f is None or f["status"] in ("no_structure", "short_alignment") or f["tm"] == "":
        return I, "fallback_seq"
    e = 0.0 if f["epitope"] == "" else float(f["epitope"])
    return 0.4 * I + 0.4 * float(f["tm"]) + 0.2 * e, "structure" if f["status"] == "ok" else "structure_e0"

prior = {p: sum(1 for s in cal_species if p in prods.get(s, ())) / len(cal_species) for p in products}

rows, n_fallback = [], 0
with open(os.path.join(P, "shortlist.csv")) as f:
    for r in csv.DictReader(f):
        q, qsp, qsplit, qfam, p = r["query"], r["query_species"], r["query_split"], r["family"], r["product"]
        if qsplit == "test" and False: pass
        best, flags = 0.0, set()
        for item in r["top10"].split(";"):
            ref, ident = item.rsplit(":", 1)
            s, flag = pair_score(q, ref, float(ident))
            flags.add(flag)
            if s > best: best = s
        y = 1 if p in prods.get(qsp, ()) else 0
        rows.append({"query": q, "species": qsp, "split": qsplit, "family": qfam, "product": p,
                     "model": round(best, 4), "flags": "|".join(sorted(flags)), "y": y,
                     "naive": round(prior[p], 4)})
        if "fallback_seq" in flags: n_fallback += 1

base = {(r["query"], r["product"]): float(r["baseline_identity"]) / 100.0
        for r in csv.DictReader(open(os.path.join(P, "baseline_pairs.csv")))}
for r in rows:
    r["baseline"] = round(base.get((r["query"], r["product"]), 0.0), 4)

with gzip.open(os.path.join(R, "scores_eval.csv.gz"), "wt", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(f"eval rows: {len(rows)} (calibration {sum(1 for r in rows if r['split']=='calibration')}, "
      f"test {sum(1 for r in rows if r['split']=='test')}, target {sum(1 for r in rows if r['split']=='target')}), "
      f"rows w/ seq fallback: {n_fallback}")

cal = [r for r in rows if r["split"] == "calibration"]
test = [r for r in rows if r["split"] == "test"]

# --- tau calibration (max Youden J) on calibration pairs ---
scores = np.array([r["model"] for r in cal]); ys = np.array([r["y"] for r in cal])
cand = np.unique(np.concatenate(([0.0], np.quantile(scores, np.linspace(0, 1, 400)), [1.0])))
best_tau, best_j = 0.0, -1
for t in cand:
    pred = scores >= t
    tp = (pred & (ys == 1)).sum(); fp = (pred & (ys == 0)).sum()
    fn = (~pred & (ys == 1)).sum(); tn = (~pred & (ys == 0)).sum()
    j = tp / max(tp + fn, 1) + tn / max(tn + fp, 1) - 1
    if j > best_j: best_j, best_tau = j, float(t)
tau = best_tau
open(os.path.join(R, "calibration.txt"), "w").write(
    f"tau (max Youden J on calibration pairs, n={len(cal)}): {tau:.4f}  J={best_j:.4f}\n"
    f"calibration pair prevalence: {ys.mean():.4f}\n")

# --- evaluation on test split ---
def metrics(rs, key):
    s = np.array([r[key] for r in rs]); y = np.array([r["y"] for r in rs])
    return average_precision_score(y, s), roc_auc_score(y, s)
out = [f"tau frozen from calibration: {tau:.4f}", f"test pairs: {len(test)} (positives {sum(r['y'] for r in test)})"]
res = {}
for key in ("model", "baseline", "naive"):
    ap, auc = metrics(test, key)
    res[key] = ap
    out.append(f"{key:9s} test AUPRC={ap:.4f} AUROC={auc:.4f}")

# paired bootstrap over test pairs
n = len(test)
yarr = np.array([r["y"] for r in test])
marr = np.array([r["model"] for r in test]); barr = np.array([r["baseline"] for r in test])
diffs = []
for _ in range(1000):
    idx = rng.integers(0, n, n)
    if yarr[idx].sum() == 0: continue
    diffs.append(average_precision_score(yarr[idx], marr[idx]) - average_precision_score(yarr[idx], barr[idx]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
out.append(f"delta AUPRC (model - baseline): mean {np.mean(diffs):+.4f}, 95% CI [{lo:+.4f}, {hi:+.4f}] -> "
           + ("WIN (CI excludes 0)" if lo > 0 else "NO WIN CLAIM (CI includes 0 or negative) - reported as negative" ))
# per-family
fam_rows = collections.defaultdict(list)
for r in test: fam_rows[r["family"]].append(r)
with open(os.path.join(R, "per_family.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "n_pairs", "n_pos", "auprc_model", "auprc_baseline", "auprc_naive"])
    for fam in sorted(fam_rows):
        rs = fam_rows[fam]
        if sum(r["y"] for r in rs) == 0: continue
        w.writerow([fam, len(rs), sum(r["y"] for r in rs)] + [f"{metrics(rs, k)[0]:.4f}" for k in ("model", "baseline", "naive")])
# species-level: product recovery + inventory coverage on test species
sp_rows = collections.defaultdict(list)
for r in test: sp_rows[r["species"]].append(r)
rec, covfrac = [], []
for sp, rs in sp_rows.items():
    true_p = set(prods.get(sp, ()))
    hit_p = {r["product"] for r in rs if r["model"] >= tau}
    if true_p: rec.append(len(true_p & hit_p) / len(true_p))
    by_t = collections.defaultdict(float)
    for r in rs: by_t[r["query"]] = max(by_t[r["query"]], r["model"])
    covfrac.append(sum(1 for v in by_t.values() if v >= tau) / len(by_t))
out.append(f"test species: {len(sp_rows)}; mean per-species true-product recovery at tau: {np.mean(rec):.3f}; "
           f"mean fraction of toxin inventory model-covered at tau: {np.mean(covfrac):.3f}")
out = "\n".join(out) + "\n"
open(os.path.join(R, "evaluation.txt"), "w").write(out)
print(out)

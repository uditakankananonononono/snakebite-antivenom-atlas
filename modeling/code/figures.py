#!/usr/bin/env python3
"""Figures for the B10 paper (all from committed result artifacts)."""
import csv, os, gzip, collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score
import common

P, R = os.path.join(common.ROOT, "modeling/panel"), os.path.join(common.ROOT, "modeling/results")
F = os.path.join(common.ROOT, "modeling/paper/figures")
os.makedirs(F, exist_ok=True)
BLUE = "#1a4f8a"
rows = []
with gzip.open(os.path.join(R, "scores_eval.csv.gz"), "rt") as f:
    for r in csv.DictReader(f): rows.append(r)
tau = float(open(os.path.join(R, "calibration.txt")).read().split(":")[1].split()[0])
test = [r for r in rows if r["split"] == "test"]
cal = [r for r in rows if r["split"] == "calibration"]
tgt = [r for r in rows if r["split"] == "target"]

# 1. PR curves (test)
plt.figure(figsize=(6.2, 4.6))
for key, lab, c in [("model", "MODEL (cascade)", BLUE), ("baseline", "baseline (seq-id)", "#c0392b"), ("naive", "naive (product prior)", "#7f8c8d")]:
    y = np.array([int(r["y"]) for r in test]); s = np.array([float(r[key]) for r in test])
    pr, rc, _ = precision_recall_curve(y, s)
    plt.plot(rc, pr, color=c, lw=1.8, label=f"{lab}  AUPRC={average_precision_score(y, s):.3f}")
prev = np.mean([int(r["y"]) for r in test])
plt.axhline(prev, ls=":", color="k", lw=1, label=f"prevalence={prev:.3f}")
plt.xlabel("Recall"); plt.ylabel("Precision"); plt.title("Held-out test split (species-level holdout): toxin-product pair ranking")
plt.legend(fontsize=8, frameon=False); plt.tight_layout(); plt.savefig(f"{F}/fig_pr_curves.png", dpi=200); plt.close()

# 2. per-family AUPRC
pf_rows = list(csv.DictReader(open(os.path.join(R, "per_family.csv"))))
fams = [r["family"] for r in pf_rows]
x = np.arange(len(fams)); w = 0.27
plt.figure(figsize=(8.5, 4.2))
for i, k in enumerate(("auprc_model", "auprc_baseline", "auprc_naive")):
    plt.bar(x + (i-1)*w, [float(r[k]) for r in pf_rows], w, label=k.replace("auprc_", "").upper(), color=[BLUE, "#c0392b", "#7f8c8d"][i])
plt.xticks(x, fams, rotation=45, ha="right", fontsize=8); plt.ylabel("AUPRC (test split)")
plt.title("Per-family discrimination on held-out species")
plt.legend(fontsize=8, frameon=False); plt.tight_layout(); plt.savefig(f"{F}/fig_per_family.png", dpi=200); plt.close()

# 3. calibration curve
s = np.array([float(r["model"]) for r in cal]); y = np.array([int(r["y"]) for r in cal])
grid = np.linspace(0, 1, 201); J, TPR, FPR = [], [], []
for t in grid:
    pred = s >= t
    tp = (pred & (y == 1)).sum(); fp = (pred & (y == 0)).sum(); fn = (~pred & (y == 1)).sum(); tn = (~pred & (y == 0)).sum()
    TPR.append(tp / max(tp + fn, 1)); FPR.append(fp / max(fp + tn, 1)); J.append(TPR[-1] - FPR[-1])
plt.figure(figsize=(6.2, 4.2))
plt.plot(grid, TPR, label="sensitivity", color=BLUE); plt.plot(grid, FPR, label="1-specificity", color="#c0392b")
plt.plot(grid, J, label="Youden J", color="#27ae60", ls="--")
plt.axvline(tau, color="k", ls=":", lw=1); plt.text(tau+0.01, 0.05, f"tau={tau:.3f}", fontsize=8)
plt.xlabel("decision threshold on S"); plt.ylabel("rate"); plt.title("Threshold calibration (calibration split only)")
plt.legend(fontsize=8, frameon=False); plt.tight_layout(); plt.savefig(f"{F}/fig_calibration.png", dpi=200); plt.close()

# 4. model score vs baseline identity (test), colored by structure use
plt.figure(figsize=(6.2, 4.6))
sub = test[:: max(1, len(test)//4000)]
for flag, c, lab in [("structure", BLUE, "structure-scored pair"), ("fallback", "#e67e22", "sequence-only fallback")]:
    xs = [float(r["baseline"]) for r in sub if flag in r["flags"]]
    ys = [float(r["model"]) for r in sub if flag in r["flags"]]
    plt.scatter(xs, ys, s=4, alpha=0.35, color=c, label=lab)
plt.axhline(tau, color="k", ls=":", lw=1); plt.axvline(0.8, color="#c0392b", ls=":", lw=1)
plt.text(0.805, 0.02, "baseline T=80", fontsize=8, color="#c0392b")
plt.xlabel("baseline score (best identity / 100)"); plt.ylabel("MODEL score S")
plt.title("Test split: structure-augmented score vs sequence identity")
plt.legend(fontsize=8, frameon=False, markerscale=3); plt.tight_layout(); plt.savefig(f"{F}/fig_score_vs_identity.png", dpi=200); plt.close()

# 5. target coverage per family, model vs baseline
tc = list(csv.DictReader(open(os.path.join(R, "target_coverage.csv"))))
fam2 = collections.defaultdict(lambda: [0, 0, 0])
for r in tc:
    fam2[r["family"]][0] += 1
    fam2[r["family"]][1] += r["model_covered"] == "yes"
    fam2[r["family"]][2] += r["baseline_covered_T80"] == "yes"
fams = sorted(fam2); x = np.arange(len(fams))
plt.figure(figsize=(8.5, 4.2))
plt.bar(x - w/2, [100*fam2[f][1]/fam2[f][0] for f in fams], w, label="MODEL @ tau", color=BLUE)
plt.bar(x + w/2, [100*fam2[f][2]/fam2[f][0] for f in fams], w, label="baseline T=80", color="#c0392b")
plt.xticks(x, fams, rotation=45, ha="right", fontsize=8); plt.ylabel("% toxins inferred-covered")
plt.title("Target set (CRITICAL/HIGH species, n=290 toxins): modeled vs heuristic coverage")
plt.legend(fontsize=8, frameon=False); plt.tight_layout(); plt.savefig(f"{F}/fig_target_coverage.png", dpi=200); plt.close()
print("figures:", sorted(os.listdir(F)))

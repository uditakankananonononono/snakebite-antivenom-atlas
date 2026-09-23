#!/usr/bin/env python3
"""Statistical analysis for the paper (run 2).
1. Region x gap-class contingency (chi-square) - is antivenom-gap severity region-dependent?
2. Toxin richness vs antivenom coverage: Spearman correlation of n_toxins vs
   n_antivenom_products per species; Mann-Whitney U of toxin counts covered vs uncovered.
3. WHO-category vs toxin-record availability (the DATA GAP class) - Fisher exact:
   are Cat1 species more likely to have zero toxin records than Cat2?
Writes results/stats_summary.txt (statistics + plain-language reading)."""
import csv, collections
from scipy import stats
import numpy as np

rows = list(csv.DictReader(open("results/gap_table.csv")))
out = []

# 1. region x gap contingency (species may span regions: count once per region it occurs in)
REGIONS = ["Africa and the Middle East", "Asia and Australasia", "Europe", "The Americas"]
CLASSES = ["CRITICAL (Cat1, no antivenom listed)", "HIGH (no antivenom listed)",
           "DATA GAP (covered, but no toxin records)", "covered"]
tab = np.zeros((len(REGIONS), len(CLASSES)), dtype=int)
for r in rows:
    for reg in r["regions"].split("|"):
        if reg in REGIONS:
            tab[REGIONS.index(reg), CLASSES.index(r["gap_class"])] += 1
chi2, p, dof, _ = stats.chi2_contingency(tab)
out += ["== 1. region x gap-class contingency (species counted per region of occurrence) ==",
        "rows: " + ", ".join(REGIONS), "cols: " + ", ".join(CLASSES),
        str(tab.tolist()), f"chi2={chi2:.1f} dof={dof} p={p:.3g}", ""]

# 2. toxin richness vs coverage
nt = np.array([int(r["n_toxins"]) for r in rows])
nav = np.array([int(r["n_antivenom_products"]) for r in rows])
rho, p_rho = stats.spearmanr(nt, nav)
cov_mask = nav > 0
u, p_u = stats.mannwhitneyu(nt[cov_mask], nt[~cov_mask])
out += ["== 2. toxin richness vs antivenom coverage (per species) ==",
        f"Spearman rho(n_toxins, n_products)={rho:.3f} p={p_rho:.3g} n={len(rows)}",
        f"median toxins covered={np.median(nt[cov_mask]):.0f} (n={cov_mask.sum()}), uncovered={np.median(nt[~cov_mask]):.0f} (n={(~cov_mask).sum()})",
        f"Mann-Whitney U p={p_u:.3g}", ""]

# 3. Cat1/Cat2 vs zero toxin records (LB-sourced species with category 1 or 2)
cat_rows = [r for r in rows if r["category"] in ("1", "2")]
a = sum(1 for r in cat_rows if r["category"] == "1" and int(r["n_toxins"]) == 0)
b = sum(1 for r in cat_rows if r["category"] == "1" and int(r["n_toxins"]) > 0)
c = sum(1 for r in cat_rows if r["category"] == "2" and int(r["n_toxins"]) == 0)
d = sum(1 for r in cat_rows if r["category"] == "2" and int(r["n_toxins"]) > 0)
odds, p_f = stats.fisher_exact([[a, b], [c, d]])
out += ["== 3. WHO category vs absence of toxin records ==",
        f"Cat1: {a} zero-toxin / {a+b} species; Cat2: {c} zero-toxin / {c+d}",
        f"Fisher exact odds ratio={odds:.2f} p={p_f:.3g}", ""]
open("results/stats_summary.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))

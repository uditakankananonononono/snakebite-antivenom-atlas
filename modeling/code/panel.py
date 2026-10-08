#!/usr/bin/env python3
"""GATE M1/M2: build the modeling panel + seeded species-level split.
Outputs (design artifacts, deterministic from seed 20261008):
  modeling/panel/targets.csv          target toxins (CRITICAL/HIGH species)
  modeling/panel/references.csv       covered-species reference toxins
  modeling/panel/eval_species.csv     evaluable covered species + calibration/test split
  modeling/panel/products.csv         product list + indicated species counts
  modeling/panel/panel_summary.txt
"""
import csv, os, collections
import numpy as np
import common

rng = np.random.default_rng(common.SEED)
inv = common.load_inventory()
gap = common.load_gap()
prods = common.load_products()
seqs = common.load_fasta()
afdb = common.load_afdb()

unc_sp = {s for s, g in gap.items() if g["gap_class"].startswith(("CRITICAL", "HIGH"))}
cov_sp = {s for s, g in gap.items() if not g["gap_class"].startswith(("CRITICAL", "HIGH"))}

targets, references = [], []
for r in inv:
    acc, sp = r["accession"], r["matched_species"]
    if not sp or acc not in seqs:
        continue
    row = {"accession": acc, "species": sp, "family": r["family"],
           "length": len(seqs[acc]), "afdb": "yes" if acc in afdb else "no"}
    if sp in unc_sp:
        targets.append(row)
    elif sp in cov_sp:
        references.append(row)

# evaluable covered species: >=1 toxin w/ seq AND >=1 product
cov_with_tox = {r["species"] for r in references}
eval_species = sorted(s for s in cov_with_tox if prods.get(s))
by_region = collections.defaultdict(list)
for s in eval_species:
    by_region[gap[s]["regions"] or "unknown"].append(s)
split = {}
for region in sorted(by_region):
    sp_list = sorted(by_region[region])
    idx = rng.permutation(len(sp_list))
    n_test = max(1, round(0.2 * len(sp_list))) if len(sp_list) > 1 else 0
    for i, si in enumerate(idx):
        split[sp_list[si]] = "test" if i < n_test else "calibration"

os.makedirs(os.path.join(common.ROOT, "modeling/panel"), exist_ok=True)
def w(name, rows, fields):
    with open(os.path.join(common.ROOT, "modeling/panel", name), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields); wr.writeheader(); wr.writerows(rows)

w("targets.csv", targets, ["accession", "species", "family", "length", "afdb"])
w("references.csv", references, ["accession", "species", "family", "length", "afdb"])
w("eval_species.csv", [{"species": s, "region": gap[s]["regions"] or "unknown",
                        "n_products": len(prods[s]), "split": split[s]} for s in eval_species],
  ["species", "region", "n_products", "split"])
all_products = sorted({p for v in prods.values() for p in v})
w("products.csv", [{"product": p, "n_indicated_species": sum(1 for v in prods.values() if p in v)} for p in all_products],
  ["product", "n_indicated_species"])

n_cal = sum(1 for v in split.values() if v == "calibration")
n_test = sum(1 for v in split.values() if v == "test")
summary = f"""B10 modeling panel (seed {common.SEED})
targets (CRITICAL/HIGH toxins w/ seq): {len(targets)} across {len({r['species'] for r in targets})} species, families: {len({r['family'] for r in targets})}
references (covered toxins w/ seq): {len(references)} across {len({r['species'] for r in references})} species
evaluable covered species (toxins>0 AND products>0): {len(eval_species)}  ->  calibration {n_cal} / test {n_test}
products in scope: {len(all_products)}
AFDB availability: targets {sum(1 for r in targets if r['afdb']=='yes')}/{len(targets)}, references {sum(1 for r in references if r['afdb']=='yes')}/{len(references)}
regions of eval species: {dict(collections.Counter(gap[s]['regions'] or 'unknown' for s in eval_species))}
"""
open(os.path.join(common.ROOT, "modeling/panel/panel_summary.txt"), "w").write(summary)
print(summary)

#!/usr/bin/env python3
"""B10 query tool: modeled antivenom coverage for a species or toxin.
Usage: python3 modeling/code/coverage_model.py --species 'Hypnale hypnale'
       python3 modeling/code/coverage_model.py --toxin A0A0B4U9L8
Reads only committed artifacts (modeling/results/target_coverage.csv, scores_eval.csv.gz,
panel tables). Prints modeled coverage at frozen tau plus the baseline comparison."""
import argparse, csv, os, gzip, collections, sys
import common

P, R = os.path.join(common.ROOT, "modeling/panel"), os.path.join(common.ROOT, "modeling/results")
ap = argparse.ArgumentParser()
ap.add_argument("--species"); ap.add_argument("--toxin")
a = ap.parse_args()
tau = float(open(os.path.join(R, "calibration.txt")).read().split(":")[1].split()[0])
tc = list(csv.DictReader(open(os.path.join(R, "target_coverage.csv"))))
gap = common.load_gap()

def show_toxin(r):
    print(f"{r['accession']}  {r['species']}  [{r['family']}]")
    print(f"  model: max S={r['model_score_max']}  covered@tau={r['model_covered']}  products: {r['model_products'] or '-'}")
    print(f"  baseline: best identity={r['baseline_identity']}  covered@T80={r['baseline_covered_T80']}")

if a.toxin:
    hits = [r for r in tc if r["accession"] == a.toxin]
    if not hits: sys.exit("toxin not in the target panel (it may belong to a covered species)")
    show_toxin(hits[0])
elif a.species:
    hits = [r for r in tc if r["species"] == a.species]
    if hits:
        n = sum(h["model_covered"] == "yes" for h in hits)
        print(f"{a.species}: gap class = {gap.get(a.species, {}).get('gap_class', '?')}")
        print(f"  {len(hits)} toxins in panel; model-covered at tau={tau}: {n}/{len(hits)} ({100*n/len(hits):.0f}%)")
        for h in hits: show_toxin(h)
    else:
        g = gap.get(a.species)
        if not g: sys.exit("species not in the committed gap table")
        print(f"{a.species}: gap class = {g['gap_class']}; not a CRITICAL/HIGH modeling target.")
        print(f"  committed products: {g['antivenoms'] or '-'}")
else:
    ap.print_help()

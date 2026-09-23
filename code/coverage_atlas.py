#!/usr/bin/env python3
"""coverage_atlas.py - query tool built on the audit results.

USAGE:
  python3 code/coverage_atlas.py species "Naja naja"     # full audit card for one species
  python3 code/coverage_atlas.py region "The Americas"   # gap-class breakdown for a WHO region
  python3 code/coverage_atlas.py family PLA2             # toxins/products for a toxin family
  python3 code/coverage_atlas.py critical                # all CRITICAL species (Cat1, no antivenom)
  python3 code/coverage_atlas.py xref "Echis ocellatus"  # cross-reactivity inference for a species
  python3 code/coverage_atlas.py product "SAIMR polyvalent"  # species covered by a product
Reads only committed results/ tables; no network."""
import csv, sys, collections, os

os.chdir(os.path.join(os.path.dirname(__file__), ".."))
R = lambda p: list(csv.DictReader(open(os.path.join("results", p))))
gap, summ = R("gap_table.csv"), R("species_summary.csv")
inv, xr = R("toxin_inventory.csv"), R("cross_reactivity_by_toxin.csv")
avlong = R("antivenom_coverage_long.csv")
by_sp = {r["species"]: r for r in gap}
smap = {r["species"]: r for r in summ}

def card(sp):
    g, s = by_sp.get(sp), smap.get(sp)
    if not g: return f"'{sp}' not in the consolidated list (294 species)"
    lines = [f"{sp}  [WHO category {g['category'] or 'WHO2017-only'}]",
             f"  regions: {g['regions'] or '-'}   countries: {g['countries'] or '-'}",
             f"  gap class: {g['gap_class']}",
             f"  toxins: {s['n_toxins']} ({s['n_toxins_reviewed']} reviewed, {s['n_with_pdb']} with PDB)  families: {s['families'] or '-'}",
             f"  antivenom products ({s['n_antivenom_products']}): {s['antivenoms'] or 'NONE LISTED'}"]
    hits = [x for x in xr if x["species"] == sp]
    if hits:
        best = max(hits, key=lambda x: float(x["best_identity"]))
        lines.append(f"  cross-reactivity: {len(hits)} toxins scored; best covered-species homolog "
                     f"{best['best_identity']}% ({best['best_covered_species']})")
    return "\n".join(lines)

cmd = sys.argv[1] if len(sys.argv) > 1 else ""
arg = " ".join(sys.argv[2:])
if cmd == "species" and arg:
    hits = [s for s in by_sp if arg.lower() in s.lower()]
    print("\n\n".join(card(s) for s in hits) if hits else f"no species matching '{arg}'")
elif cmd == "region" and arg:
    sel = [r for r in gap if arg.lower() in r["regions"].lower()]
    c = collections.Counter(r["gap_class"] for r in sel)
    print(f"{arg}: {len(sel)} species occurrences")
    for k, v in c.most_common(): print(f"  {k}: {v}")
    crit = [r["species"] for r in sel if r["gap_class"].startswith("CRITICAL")]
    if crit: print("  CRITICAL:", "; ".join(sorted(crit)))
elif cmd == "family" and arg:
    sel = [r for r in inv if r["family"].lower() == arg.lower() and r["matched_species"]]
    sp = collections.Counter(r["matched_species"] for r in sel)
    print(f"{arg}: {len(sel)} in-scope toxins across {len(sp)} species")
    for s, n in sp.most_common(10): print(f"  {n:4d}  {s}")
elif cmd == "critical":
    for r in gap:
        if r["gap_class"].startswith("CRITICAL"):
            print(f"{r['species']:35s} {r['regions']:35s} toxins={r['n_toxins']}")
elif cmd == "xref" and arg:
    hits = [x for x in xr if arg.lower() in x["species"].lower()]
    for x in sorted(hits, key=lambda x: -float(x["best_identity"]))[:15]:
        print(f"{x['accession']:12s} {x['family']:12s} {x['best_identity']:>6s}%  vs {x['best_covered_species']} ({x['best_covered_accession']})")
    if not hits: print(f"no cross-reactivity scores for '{arg}' (species may be covered or have no toxins)")
elif cmd == "product" and arg:
    sel = [r for r in avlong if arg.lower() in r["product"].lower()]
    print(f"{len(sel)} coverage entries for products matching '{arg}':")
    for r in sel[:40]: print(f"  {r['product']:45s} -> {r['species']}")
else:
    print(__doc__)

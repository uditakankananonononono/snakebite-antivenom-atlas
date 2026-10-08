#!/usr/bin/env python3
"""GATE M4: re-implement the committed B09 cross-reactivity heuristic for the target set
and verify equivalence with committed results/cross_reactivity_by_toxin.csv before the
baseline is used as a comparator. Writes modeling/panel/baseline_check.csv and
modeling/panel/baseline_equivalence.txt."""
import csv, collections, os, sys
import common

targets = list(csv.DictReader(open(os.path.join(common.ROOT, "modeling/panel/targets.csv"))))
references = list(csv.DictReader(open(os.path.join(common.ROOT, "modeling/panel/references.csv"))))
seqs = common.load_fasta()

refs_by_fam = collections.defaultdict(list)
for r in references:
    refs_by_fam[r["family"]].append((r["accession"], r["species"], seqs[r["accession"]], common.kmers(seqs[r["accession"]])))

rows = []
for t in targets:
    fam, ua, usp = t["family"], t["accession"], t["species"]
    useq = seqs[ua]; uk = common.kmers(useq)
    best, best_sp, best_acc = 0.0, "", ""
    for ca, csp, cseq, ck in refs_by_fam.get(fam, []):
        if not common.prefilter_pass(uk, ck): continue
        ident = common.global_identity(useq, cseq)
        if ident > best: best, best_sp, best_acc = ident, csp, ca
    rows.append({"accession": ua, "species": usp, "family": fam,
                 "best_identity": round(best, 1), "best_covered_species": best_sp,
                 "best_covered_accession": best_acc})

with open(os.path.join(common.ROOT, "modeling/panel/baseline_check.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

committed = {r["accession"]: r for r in csv.DictReader(open(os.path.join(common.ROOT, "results/cross_reactivity_by_toxin.csv")))}
mine = {r["accession"]: r for r in rows}
report = []
report.append(f"committed rows: {len(committed)}, re-implemented rows: {len(mine)}")
same_keys = set(committed) == set(mine)
report.append(f"accession sets identical: {same_keys}")
mism = []
for acc in committed:
    c, m = committed[acc], mine.get(acc)
    if not m: continue
    if c["best_identity"] != str(m["best_identity"]) or c["best_covered_accession"] != m["best_covered_accession"]:
        mism.append((acc, c["best_identity"], m["best_identity"], c["best_covered_accession"], m["best_covered_accession"]))
report.append(f"identity/best-hit mismatches: {len(mism)}")
for x in mism[:10]: report.append("  MISMATCH " + " ".join(map(str, x)))
# threshold table comparison
per_sp = collections.defaultdict(list)
for r in rows: per_sp[r["species"]].append(r["best_identity"])
for T in (60, 70, 80, 90):
    n_t = sum(1 for r in rows if r["best_identity"] >= T)
    sp_full = sum(1 for s, v in per_sp.items() if v and sum(1 for x in v if x >= T)/len(v) >= 0.5)
    report.append(f"T={T}%: toxins inferred-covered {n_t}/{len(rows)} ({100*n_t/len(rows):.1f}%), species >=50% covered: {sp_full}/{len(per_sp)}")
report.append("committed reference: T=60 211/290 (72.8%) 29/38 | T=70 194/290 (66.9%) 27/38 | T=80 161/290 (55.5%) 24/38 | T=90 55/290 (19.0%) 8/38")
report.append("EQUIVALENT" if same_keys and not mism else "NOT EQUIVALENT - investigate before using baseline")
out = "\n".join(report) + "\n"
open(os.path.join(common.ROOT, "modeling/panel/baseline_equivalence.txt"), "w").write(out)
print(out)

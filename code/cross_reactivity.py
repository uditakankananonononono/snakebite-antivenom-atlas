#!/usr/bin/env python3
"""Cross-reactivity heuristic (run 2): infer potential antivenom coverage for species with
NO listed antivenom from sequence identity of their toxins to toxins of covered species.

Method (documented, parameters frozen here pre-results):
- In-scope toxins grouped by rule-based family (results/toxin_inventory.csv).
- Within each family: uncovered-species toxin vs every covered-species toxin.
  Prefilter: shared 8-mer count >= 15% of the shorter sequence's 8-mers (loose, keeps
  pairs plausibly >=50% identical), then global identity via edlib (NW, ends-free none).
- A toxin is INFERRED-COVERED at threshold T if its best covered-species hit >= T.
  Reported at T = 60/70/80/90% as a sensitivity analysis (no single cutoff claimed).
- Species-level: fraction of its toxin inventory inferred-covered at each T.
Rationale to cite in paper: same-family toxin epitopes are the antivenom target; high
sequence identity to a covered species' toxin implies plausible cross-neutralization
(heuristic upper bound, NOT evidence of clinical efficacy).
Outputs: results/cross_reactivity_by_toxin.csv, results/cross_reactivity_summary.txt
"""
import csv, collections, edlib, sys

THRESHOLDS = [60, 70, 80, 90]
K = 8
PREFILTER_FRAC = 0.15

def kmers(s, k=K): return {s[i:i+k] for i in range(len(s)-k+1)}

inv = list(csv.DictReader(open("results/toxin_inventory.csv")))
gap = {r["species"]: r["gap_class"] for r in csv.DictReader(open("results/gap_table.csv"))}
covered_sp = {s for s, g in gap.items() if g in ("covered", "DATA GAP (covered, but no toxin records)")}
uncovered_sp = {s for s, g in gap.items() if g.startswith("CRITICAL") or g.startswith("HIGH")}

seqs = {}
for h, s in [(l[1:], "") for l in open("data/uniprot/serpentes_toxins.fasta").read().split(">") if l.strip()]:
    pass
# parse fasta properly
seqs = {}
cur = None
for line in open("data/uniprot/serpentes_toxins.fasta"):
    line = line.strip()
    if line.startswith(">"):
        cur = line[1:].split("|")[1] if "|" in line else line[1:].split()[0]
        seqs[cur] = []
    elif cur:
        seqs[cur].append(line)
seqs = {k: "".join(v) for k, v in seqs.items()}

by_fam = collections.defaultdict(lambda: {"cov": [], "unc": []})
for r in inv:
    sp = r["matched_species"]
    if not sp or r["accession"] not in seqs: continue
    if sp in covered_sp: by_fam[r["family"]]["cov"].append((r["accession"], sp))
    elif sp in uncovered_sp: by_fam[r["family"]]["unc"].append((r["accession"], sp))

rows = []
for fam in sorted(by_fam):
    cov = by_fam[fam]["cov"]; unc = by_fam[fam]["unc"]
    if not cov or not unc: continue
    cov_k = [(a, sp, seqs[a], kmers(seqs[a])) for a, sp in cov]
    n_aln = 0
    for ua, usp in unc:
        useq = seqs[ua]; uk = kmers(useq)
        best, best_sp, best_acc = 0.0, "", ""
        for ca, csp, cseq, ck in cov_k:
            if len(uk & ck) < PREFILTER_FRAC * min(len(uk), len(ck) or 1): continue
            aln = edlib.align(useq, cseq, mode="NW", task="distance")
            if aln["editDistance"] < 0: continue
            n_aln += 1
            ident = 100.0 * (1 - aln["editDistance"] / max(len(useq), len(cseq)))
            if ident > best: best, best_sp, best_acc = ident, csp, ca
        rows.append({"accession": ua, "species": usp, "family": fam,
                     "best_identity": round(best, 1), "best_covered_species": best_sp,
                     "best_covered_accession": best_acc})
    print(f"{fam}: {len(unc)} uncovered x {len(cov)} covered, {n_aln} alignments", file=sys.stderr)

with open("results/cross_reactivity_by_toxin.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# species-level summary
per_sp = collections.defaultdict(list)
for r in rows: per_sp[r["species"]].append(r["best_identity"])
out = ["Cross-reactivity heuristic summary (uncovered species = CRITICAL+HIGH gap class)",
       f"uncovered-species toxins scored: {len(rows)} across {len(per_sp)} species", ""]
for T in THRESHOLDS:
    n_t = sum(1 for r in rows if r["best_identity"] >= T)
    sp_full = sum(1 for s, v in per_sp.items() if v and sum(1 for x in v if x >= T) / len(v) >= 0.5)
    out.append(f"T={T}%: toxins inferred-covered {n_t}/{len(rows)} ({100*n_t/len(rows):.1f}%), species with >=50% inventory inferred-covered: {sp_full}/{len(per_sp)}")
open("results/cross_reactivity_summary.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))

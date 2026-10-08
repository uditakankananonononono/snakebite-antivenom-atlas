#!/usr/bin/env python3
"""GATE M5: structural features for all unique shortlisted (query, ref) pairs.
Per model: CA coords, per-residue pLDDT (B-factor), exposed = CA-neighbor count within
10 A <= 16. Per pair: edlib alignment-path correspondence -> Kabsch superposition ->
TM-score (d0 = max(1.24*L^(1/3)-1.8, 0.5), L = aligned length) and E (exposed
physicochemical-class conservation). Output: modeling/results/pair_features.csv
"""
import csv, os, sys, pickle, time
import numpy as np
import common

P = os.path.join(common.ROOT, "modeling/panel")
D = os.path.join(common.ROOT, "modeling/data/alphafold/models")
R = os.path.join(common.ROOT, "modeling/results")
os.makedirs(R, exist_ok=True)
seqs = common.load_fasta()

CLASSES = [set("AVLIM"), set("FWY"), set("STNQ"), set("KRH"), set("DE"), set("CGP")]
def pclass(aa):
    for i, c in enumerate(CLASSES):
        if aa in c: return i
    return -1

def parse_model(acc):
    path = os.path.join(D, f"AF-{acc}-F1-model.pdb")
    if not os.path.exists(path): return None
    coords, bfac, resseq = [], [], []
    with open(path) as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                coords.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
                bfac.append(float(line[60:66]))
                resseq.append(line[22:26].strip())
    if not coords: return None
    c = np.array(coords, dtype=np.float32)
    # CA neighbor count within 10 A
    d2 = ((c[:, None, :] - c[None, :, :]) ** 2).sum(-1)
    nbr = (d2 <= 100.0).sum(1) - 1
    return {"coords": c, "plddt": np.array(bfac, dtype=np.float32), "exposed": nbr <= 16,
            "resseq": resseq}

def kabsch_tm(Pm, Qm):
    """Superpose Qm onto Pm (correspondence given), return per-pair distances and TM-score."""
    L = len(Pm)
    d0 = max(1.24 * L ** (1/3) - 1.8, 0.5)
    Pc, Qc = Pm - Pm.mean(0), Qm - Qm.mean(0)
    H = Qc.T @ Pc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    Rm = Vt.T @ np.diag([1, 1, d]) @ U.T
    Qr = Qc @ Rm
    dist = np.sqrt(((Pc - Qr) ** 2).sum(1))
    tm = float((1 / (1 + (dist / d0) ** 2)).mean())
    return tm, dist

# unique pairs from shortlist
pairs = {}  # (qacc, racc) -> max identity
with open(os.path.join(P, "shortlist.csv")) as f:
    for r in csv.DictReader(f):
        for item in r["top10"].split(";"):
            a, i = item.rsplit(":", 1)
            key = (r["query"], a)
            if key not in pairs: pairs[key] = float(i)
print(f"unique shortlisted pairs: {len(pairs)}", flush=True)

needed = {a for pr in pairs for a in pr}
models = {}
for i, acc in enumerate(sorted(needed)):
    m = parse_model(acc)
    if m is not None: models[acc] = m
    if (i+1) % 800 == 0: print(f"  parsed {i+1}/{len(needed)}", file=sys.stderr, flush=True)
print(f"models parsed: {len(models)}/{len(needed)}", flush=True)

rows, t0 = [], time.time()
for n, ((q, r), ident) in enumerate(pairs.items()):
    if n and n % 20000 == 0:
        print(f"  pair {n}/{len(pairs)} ({time.time()-t0:.0f}s)", file=sys.stderr, flush=True)
    mq, mr = models.get(q), models.get(r)
    if mq is None or mr is None:
        rows.append({"query": q, "ref": r, "identity": ident, "tm": "", "epitope": "", "status": "no_structure"})
        continue
    al = common.alignment_path(seqs[q], seqs[r])
    al = [(i, j) for i, j in al if i < len(mq["coords"]) and j < len(mr["coords"])]
    if len(al) < 8:
        rows.append({"query": q, "ref": r, "identity": ident, "tm": "", "epitope": "", "status": "short_alignment"})
        continue
    idx_q = np.array([i for i, j in al]); idx_r = np.array([j for i, j in al])
    tm, dist = kabsch_tm(mq["coords"][idx_q], mr["coords"][idx_r])
    both_exp = mq["exposed"][idx_q] & mr["exposed"][idx_r]
    if both_exp.sum() == 0:
        epi, status = 0.0, "no_both_exposed"
    else:
        same = sum(pclass(seqs[q][i]) == pclass(seqs[r][j]) and pclass(seqs[q][i]) >= 0
                   for (i, j), b in zip(al, both_exp) if b)
        epi, status = same / int(both_exp.sum()), "ok"
    rows.append({"query": q, "ref": r, "identity": round(ident, 2), "tm": round(tm, 4),
                 "epitope": round(epi, 4), "status": status})

with open(os.path.join(R, "pair_features.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
import collections
print(collections.Counter(r["status"] for r in rows))
print(f"elapsed {time.time()-t0:.0f}s")

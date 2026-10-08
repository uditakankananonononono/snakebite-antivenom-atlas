#!/usr/bin/env python3
"""GATE M2/M5: per-query sequence stage.
Queries = all in-scope toxins with sequences (targets + eval covered species' toxins).
Reference pools per GATE M2:
  calibration query -> covered refs, own species excluded
  test query        -> calibration-split refs only (own species is in test, auto-excluded)
  target query      -> all covered refs (own species uncovered, not in pool)
Outputs modeling/panel/shortlist.csv: one row per (query, product) with a non-empty
top-10 (accession:identity list, identity desc), plus baseline best-overall hit per query
in modeling/panel/baseline_pairs.csv (best identity among indicated refs per product).
Also writes modeling/panel/fetch_list.txt (unique AFDB accessions to download).
"""
import csv, collections, os, sys
import common

seqs = common.load_fasta()
gap = common.load_gap()
prods = common.load_products()
afdb = common.load_afdb()
P = os.path.join(common.ROOT, "modeling/panel")
targets = list(csv.DictReader(open(os.path.join(P, "targets.csv"))))
references = list(csv.DictReader(open(os.path.join(P, "references.csv"))))
eval_sp = {r["species"]: r["split"] for r in csv.DictReader(open(os.path.join(P, "eval_species.csv")))}
products = [r["product"] for r in csv.DictReader(open(os.path.join(P, "products.csv")))]

ref_by_acc = {r["accession"]: r for r in references}
fam_refs = collections.defaultdict(list)   # family -> [(acc, species, kmers)]
for r in references:
    fam_refs[r["family"]].append((r["accession"], r["species"], common.kmers(seqs[r["accession"]])))

# product -> set of indicated species (restricted to species that have references possible)
prod_species = collections.defaultdict(set)
for sp, plist in prods.items():
    for p in plist:
        prod_species[p].add(sp)

queries = [(t["accession"], t["species"], t["family"], "target") for t in targets]
for r in references:
    queries.append((r["accession"], r["species"], r["family"], eval_sp[r["species"]]))

cal_species = {s for s, v in eval_sp.items() if v == "calibration"}

short_rows, base_rows, fetch = [], [], set()
qi = 0
for qacc, qsp, qfam, qsplit in queries:
    qi += 1
    if qi % 500 == 0:
        print(f"  query {qi}/{len(queries)}", file=sys.stderr)
    qseq = seqs[qacc]; qk = common.kmers(qseq)
    scored = []  # (identity, ref_acc, ref_species)
    for racc, rsp, rk in fam_refs.get(qfam, []):
        if racc == qacc: continue
        if qsplit == "calibration" and rsp == qsp: continue
        if qsplit == "test" and rsp not in cal_species: continue
        if not common.prefilter_pass(qk, rk): continue
        ident = common.global_identity(qseq, seqs[racc])
        scored.append((ident, racc, rsp))
    scored.sort(key=lambda x: -x[0])
    # per-product top-10
    for p in products:
        top = [(i, a) for i, a, s in scored if s in prod_species[p]][:10]
        if not top: continue
        short_rows.append({"query": qacc, "query_species": qsp, "query_split": qsplit,
                           "family": qfam, "product": p,
                           "top10": ";".join(f"{a}:{i:.1f}" for i, a in top),
                           "n_indicated_refs_scored": sum(1 for i, a, s in scored if s in prod_species[p])})
        base_rows.append({"query": qacc, "product": p, "baseline_identity": round(top[0][0], 1),
                          "baseline_ref": top[0][1]})
        if qsplit in ("calibration", "target"):  # structures fetched once; test refs are calibration species
            for i, a in top:
                if a in afdb: fetch.add(a)
    if qacc in afdb: fetch.add(qacc)

with open(os.path.join(P, "shortlist.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(short_rows[0])); w.writeheader(); w.writerows(short_rows)
with open(os.path.join(P, "baseline_pairs.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(base_rows[0])); w.writeheader(); w.writerows(base_rows)
with open(os.path.join(P, "fetch_list.txt"), "w") as f:
    f.write("\n".join(sorted(fetch)) + "\n")
print(f"queries: {len(queries)}, (query,product) rows: {len(short_rows)}, unique AFDB models to fetch: {len(fetch)}")

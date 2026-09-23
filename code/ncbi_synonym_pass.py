#!/usr/bin/env python3
"""Resolve orphan toxin organism names against NCBI Taxonomy (eutils, access only).
Decision rules (documented):
 1. NCBI accepted binomial == a listed species            -> synonym map
 2. accepted binomial in WHO appendix species, not listed -> in-scope via WHO
 3. otherwise                                             -> congeneric non-listed (stays negative)
Raw JSON/XML cached under data/ncbi/ for reproducibility (GATE 5)."""
import json, time, urllib.parse, urllib.request, os, csv, re
os.makedirs("data/ncbi", exist_ok=True)
cands = []
for line in open("results/negatives/toxin_organisms_not_in_species_list.txt"):
    n, org = line.strip().split("\t"); cands.append((int(n), org))
listed = {r["species"] for r in csv.DictReader(open("results/consolidated_species.csv"))}
who = {l.strip() for l in open("data/who/who_appendix_species.txt") if l.strip()}
def get(url):
    for a in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return r.read()
        except Exception: time.sleep(2)
    return b""
out = []
for n, org in cands:
    safe = org.replace(" ", "_")
    spath = f"data/ncbi/esearch_{safe}.json"
    if os.path.exists(spath): raw = open(spath,"rb").read()
    else:
        raw = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&retmode=json&term=" + urllib.parse.quote(f'"{org}"[Scientific Name]'))
        open(spath,"wb").write(raw); time.sleep(0.4)
    ids = json.loads(raw or b"{}").get("esearchresult",{}).get("idlist",[])
    accepted = ""
    if ids:
        fpath = f"data/ncbi/esummary_{safe}.json"
        if os.path.exists(fpath): raw2 = open(fpath,"rb").read()
        else:
            raw2 = get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=taxonomy&retmode=json&id={ids[0]}")
            open(fpath,"wb").write(raw2); time.sleep(0.4)
        try: accepted = json.loads(raw2 or b"{}")["result"][ids[0]].get("scientificname","")
        except Exception: accepted = ""
    ab = " ".join(accepted.split()[:2])
    if ab in listed: rule, mapped = "1_synonym", ab
    elif ab in who: rule, mapped = "2_who_listed", ab
    else: rule, mapped = "3_non_listed", ""
    out.append({"toxin_count": n, "uniprot_name": org, "ncbi_taxid": ids[0] if ids else "",
                "ncbi_accepted": accepted, "rule": rule, "mapped_species": mapped})
    print(f"{n:4d} {org:35s} -> {accepted:35s} {rule}")
with open("results/ncbi_synonym_resolution.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
import collections; print(collections.Counter(o['rule'] for o in out))

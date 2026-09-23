#!/usr/bin/env python3
"""Build the consolidated audit tables:
  results/consolidated_species.csv      - Longbottom species x WHO-appendix cross-check
  results/toxin_inventory.csv           - every UniProt toxin joined to a consolidated species
  results/antivenom_coverage_long.csv   - product x covered-species long form
  results/species_summary.csv           - per-species audit row
Negatives are written to results/negatives/."""
import csv, re, os, collections

os.makedirs("results/negatives", exist_ok=True)
def norm(s): return (s or "").strip().replace("_", " ")

# ---- consolidated species (Longbottom primary) ----
who_species = {l.strip() for l in open("data/who/who_appendix_species.txt") if l.strip()}
species_rows, unmatched_who = [], set(who_species)
with open("data/longbottom/repo/snake_list.csv") as f:
    for r in csv.DictReader(f):
        names = [norm(r[c]) for c in ("species","split_spp","previous_sp_name","alternate_sp_name","new_sp_name") if norm(r[c])]
        hit = [n for n in names if n in who_species]
        for h in hit: unmatched_who.discard(h)
        species_rows.append({
            "lb_id": r["id"], "species": norm(r["species"]), "split_spp": norm(r["split_spp"]),
            "category": r["majority_cat"], "countries": r["countries_occ"].strip('"'),
            "in_who_appendix": "yes" if hit else "no",
            "who_match_name": "|".join(hit), "notes": (r["notes"] or "").strip()})
# reintegrate WHO-only species confirmed by NCBI pass as consolidated rows
if os.path.exists("results/ncbi_synonym_resolution.csv"):
    have = {r["species"] for r in species_rows}
    for r in csv.DictReader(open("results/ncbi_synonym_resolution.csv")):
        if r["rule"] == "2_who_listed" and r["mapped_species"] not in have:
            species_rows.append({"lb_id": "", "species": r["mapped_species"], "split_spp": "",
                "category": "WHO2017", "countries": "", "in_who_appendix": "yes",
                "who_match_name": r["mapped_species"], "notes": "WHO-2017 appendix species absent from Longbottom list; reintegrated via NCBI resolution"})
with open("results/consolidated_species.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(species_rows[0])); w.writeheader(); w.writerows(species_rows)
open("results/negatives/who_species_not_in_longbottom.txt","w").write("\n".join(sorted(unmatched_who))+"\n")

# ---- toxin inventory ----
FAMILY_RULES = [
    ("3FTx",       r"three[- ]finger|cardiotoxin|cytotoxin|cobrotoxin|bungarotoxin|fasciculin|muscarinic toxin|neurotoxin"),
    ("PLA2",       r"phospholipase a2"),
    ("SVMP",       r"metalloproteinase|metalloprotease"),
    ("SVSP",       r"serine protease"),
    ("CRISP",      r"cysteine-rich"),
    ("LAAO",       r"l-amino-acid oxidase"),
    ("Kunitz",     r"kunitz"),
    ("CNP",        r"natriuretic"),
    ("CTL",        r"c-type lectin|lectin-like"),
    ("Disintegrin",r"disintegrin"),
    ("Waprin",     r"waprin"),
    ("VEGF",       r"vascular endothelial growth factor"),
    ("NGF",        r"nerve growth factor"),
    ("HYAL",       r"hyaluronidase"),
    ("PDE",        r"phosphodiesterase"),
    ("NUC",        r"nucleotidase"),
    ("AChE",       r"acetylcholinesterase"),
    ("GPL",        r"glutaminyl"),
]
def fam_of(name, kw):
    t = f"{name} {kw}".lower()
    for fam, pat in FAMILY_RULES:
        if re.search(pat, t): return fam
    return "OTHER"

by_name = {}
for r in species_rows:
    for n in {r["species"], r["split_spp"]}:
        if n: by_name[n] = r["species"]
# NCBI-resolved WHO-listed organisms join to their accepted WHO name (match source: who_appendix)
import os
who2lb = {}
if os.path.exists("results/ncbi_synonym_resolution.csv"):
    for r in csv.DictReader(open("results/ncbi_synonym_resolution.csv")):
        if r["rule"] == "2_who_listed":
            by_name[r["uniprot_name"]] = r["mapped_species"]

inv, orphans = [], collections.Counter()
with open("data/uniprot/serpentes_toxins.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        org = (r["Organism"] or "").strip()
        binom = " ".join(org.split()[:2])
        sp = by_name.get(binom)
        if sp is None:
            orphans[binom] += 1
        inv.append({"accession": r["Entry"], "reviewed": r["Reviewed"],
                    "protein_name": r["Protein names"], "organism_raw": org,
                    "matched_species": sp or "", "family": fam_of(r["Protein names"], r.get("Keywords","")),
                    "length": r["Length"], "pdb": "yes" if (r["PDB"] or "").strip() else "no",
                    "existence": r["Protein existence"]})
with open("results/toxin_inventory.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(inv[0])); w.writeheader(); w.writerows(inv)
with open("results/negatives/toxin_organisms_not_in_species_list.txt","w") as f:
    for k,v in sorted(orphans.items(), key=lambda x:-x[1]): f.write(f"{v}\t{k}\n")

# ---- antivenom long-form ----
id2sp = {r["lb_id"]: r["species"] for r in species_rows}
long_rows = []
with open("data/longbottom/repo/antivenom.csv") as f:
    rd = csv.reader(f); header = next(rd)
    cols = list(zip(*[row for row in rd if any(c.strip() for c in row)]))
for product, col in zip(header, cols):
    for cell in col:
        cell = cell.strip()
        if not cell: continue
        long_rows.append({"product": product.replace("_"," "), "lb_id": cell,
                          "species": id2sp.get(cell, f"UNKNOWN_ID_{cell}"),
                          "no_specific_antivenom": "yes" if product=="No_specific_antivenom" else "no"})
with open("results/antivenom_coverage_long.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(long_rows[0])); w.writeheader(); w.writerows(long_rows)

# ---- per-species summary ----
cov = collections.defaultdict(set)
for r in long_rows:
    if r["no_specific_antivenom"]=="no": cov[r["species"]].add(r["product"])
tox = collections.defaultdict(list)
for r in inv:
    if r["matched_species"]: tox[r["matched_species"]].append(r)
summ = []
for r in species_rows:
    sp = r["species"]; T = tox.get(sp, [])
    fams = collections.Counter(t["family"] for t in T)
    summ.append({"species": sp, "category": r["category"], "countries": r["countries"],
                 "in_who_appendix": r["in_who_appendix"],
                 "n_toxins": len(T), "n_toxins_reviewed": sum(1 for t in T if t["reviewed"]=="reviewed"),
                 "n_toxin_families": len(fams), "families": "|".join(f"{k}:{v}" for k,v in fams.most_common()),
                 "n_with_pdb": sum(1 for t in T if t["pdb"]=="yes"),
                 "n_antivenom_products": len(cov.get(sp, [])),
                 "antivenoms": "|".join(sorted(cov.get(sp, [])))})
with open("results/species_summary.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summ[0])); w.writeheader(); w.writerows(summ)

n = len(species_rows)
print(f"species={n} who_both={sum(1 for r in species_rows if r['in_who_appendix']=='yes')} "
      f"who_only={len(unmatched_who)} lb_only={sum(1 for r in species_rows if r['in_who_appendix']=='no')}")
print(f"toxins={len(inv)} matched={sum(1 for t in inv if t['matched_species'])} orphan_orgs={len(orphans)}")
print(f"products={len(header)-1} coverage_pairs={len(long_rows)}")
print(f"species_with_toxins={sum(1 for s in summ if s['n_toxins']) } species_no_toxins={sum(1 for s in summ if not s['n_toxins'])}")
print(f"species_covered_by_av={sum(1 for s in summ if s['n_antivenom_products'])} species_no_av={sum(1 for s in summ if not s['n_antivenom_products'])}")

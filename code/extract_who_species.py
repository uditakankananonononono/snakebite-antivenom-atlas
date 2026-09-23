#!/usr/bin/env python3
"""Extract medically important snake SPECIES names from WHO TRS 1004 Annex 5
Appendix text (species-level only; country attribution comes from the structured
Longbottom/WHO-database table - see README methods note; PDF two-column layout
makes automated country attribution unreliable: recorded as methods negative).
Genus whitelist = Longbottom snake_list genera + genera observed in the UniProt
Serpentes toxin pull. Everything matched but rejected is dumped for QC."""
import re, csv

raw = open("data/who/who_trs1004_annex5.txt", encoding="utf-8").read()
start = raw.index("This Appendix lists venomous snake species")
end = raw.find("Acknowledg", start); end = end if end != -1 else len(raw)
body = raw[start:end]

genera = set()
with open("data/longbottom/repo/snake_list.csv") as f:
    for row in csv.DictReader(f):
        for col in ("species","split_spp","previous_sp_name","alternate_sp_name","new_sp_name"):
            v = (row.get(col) or "").strip()
            if v: genera.add(v.split("_")[0])
with open("data/uniprot/serpentes_toxins.tsv") as f:
    rd = csv.DictReader(f, delimiter="\t")
    for r in rd:
        org = (r.get("Organism") or "").strip()
        if org: genera.add(org.split()[0])
genera = {g for g in genera if re.fullmatch(r"[A-Z][a-z]+", g)}

FAMS = {"Elapidae","Viperidae","Colubridae","Atractaspididae","Lamprophiidae","Hydrophiidae","Homalopsidae","Dipsadidae","Natricidae"}
cand = re.findall(r"\b([A-Z][a-z]{2,}(?:\s+[a-z][a-z-]{1,}){1,2})\b", body)
species, rejected = set(), []
for c in cand:
    g = c.split()[0]
    if g not in genera: rejected.append(c); continue
    toks = c.split()
    if any(t in ("cf","sp","spp","ssp","et","al") for t in toks[1:]): rejected.append(c); continue
    if toks[0] in FAMS: rejected.append(c); continue
    # drop trinomial false tails like "Species name and"
    if toks[-1] in ("and","or","the","of","in","sensu"): c = " ".join(toks[:-1])
    if len(c.split()) >= 2: species.add(c)
    else: rejected.append(c)

open("data/who/who_appendix_species.txt","w").write("\n".join(sorted(species))+"\n")
open("results/negatives/who_extract_rejected.txt","w").write("\n".join(sorted(set(rejected)))+"\n")
print(f"genera_vocab={len(genera)} species={len(species)} rejected={len(set(rejected))}")

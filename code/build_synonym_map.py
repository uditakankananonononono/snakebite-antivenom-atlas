#!/usr/bin/env python3
"""Resolve WHO-2017 <-> Longbottom-2018 name disagreements (run 2, replacement builder).

Inputs : data/who/who_appendix_species.txt, data/longbottom/repo/snake_list.csv,
         results/negatives/who_species_not_in_longbottom.txt,
         results/ncbi_synonym_resolution.csv
Outputs: results/who_longbottom_disagreement_table.csv  - verdict per unmatched WHO entry
         results/synonym_map_applied.csv                - curated spelling/synonym pairs w/ evidence
         results/lb_synonym_resolution.csv              - toxin organisms resolved against Longbottom

Findings encoded here (each verified against the sources cited in 'evidence'):
* the WHO appendix two-column PDF splits some binomials across lines -> bare-epithet
  fragments, genus-only headers, 'complex' phrases and prose bleeds (parse artifacts);
* four spelling variants and one genus transfer caused false 'not in Longbottom' and
  false 'not in WHO' verdicts, and two species were double-counted (Gloydius blomhoffii/
  blomhoffi, Lachesis stenophrys/stenophyrs);
* the NCBI pass resolved orphan toxin organisms against the WHO list only - several
  are in Longbottom under a spelling variant (Eristicophis macmahoni, Gloydius brevicauda).
"""
import csv, re, collections

def norm(s): return (s or "").strip().replace("_", " ")
def split_names(field):
    return [norm(x) for x in re.split(r"[,;]", field or "") if norm(x)]

# ---- Longbottom name index (comma-split: fixes the original matching bug) ----
lb_rows = list(csv.DictReader(open("data/longbottom/repo/snake_list.csv")))
lb_index = {}   # any recorded name -> canonical LB species
for r in lb_rows:
    canon = norm(r["species"])
    names = [canon, norm(r["split_spp"])]
    for c in ("previous_sp_name", "alternate_sp_name", "new_sp_name"):
        names += split_names(r[c])
    for n in names:
        if n: lb_index.setdefault(n, canon)

who_species = {l.strip() for l in open("data/who/who_appendix_species.txt") if l.strip()}

# ---- curated pairs: variant/synonym name -> LB canonical (evidence = source trail) ----
CURATED = [
 ("Eristicophis macmahonii", "Eristocophis macmahoni",
  "WHO-2017 appendix spelling; Longbottom row 118 previous_sp_name lists 'Eristicophis_macmahonii'; NCBI txid 110227"),
 ("Gloydius blomhoffii", "Gloydius blomhoffi",
  "WHO-2017 + UniProt + NCBI txid 242054 spelling 'blomhoffii'; Longbottom row 119 uses orthographic variant 'blomhoffi' (prev. Agkistrodon blomhoffi)"),
 ("Lachesis stenophrys", "Lachesis stenophyrs",
  "WHO-2017 + UniProt + NCBI txid 88085 spelling 'stenophrys'; Longbottom row 135 misspells species as 'stenophyrs' (prev. Lachesis muta stenophrys)"),
 ("Naja senegelensis", "Naja senegalensis",
  "WHO-2017 appendix misspells 'senegelensis'; Longbottom row 175 'Naja senegalensis' (prev. Naja haje)"),
 ("Porthidium ophrymegas", "Porthidium ophryomegas",
  "WHO-2017 appendix spells 'ophrymegas'; Longbottom row 189 'Porthidium ophryomegas' (prev. Bothrops lansbergii annectans)"),
 ("Naja morgani", "Walterinnesia morgani",
  "WHO-2017 lists Naja morgani; genus transfer - Longbottom row 237 'Walterinnesia morgani' (prev. Walterinnesia aegyptia)"),
 ("Gloydius brevicauda", "Gloydius brevicaudus",
  "UniProt/NCBI txid 3148161 'brevicauda'; Longbottom row 120 orthographic variant 'brevicaudus' (prev. Agkistrodon blomhoffi brevicaudus)"),
 ("Eristicophis macmahoni", "Eristocophis macmahoni",
  "UniProt/NCBI txid 110227 genus 'Eristicophis'; Longbottom row 118 misspells genus 'Eristocophis'"),
]
syn = {a: b for a, b, _ in CURATED}

def lb_lookup(name):
    """Resolve a name to a Longbottom canonical species via index or curated map."""
    if name in lb_index: return lb_index[name]
    if name in syn and syn[name] in {norm(r["species"]) for r in lb_rows}: return syn[name]
    return None

# ---- classify every unmatched WHO entry ----
parent_binomial = {}  # bare epithet -> full binomial(s) present in WHO list
epithets = {w.split()[-1] for w in who_species if len(w.split()) >= 2}
rows = []
for entry in sorted(l.strip() for l in open("results/negatives/who_species_not_in_longbottom.txt") if l.strip()):
    toks = entry.split()
    if entry in syn:
        cls = "taxonomic_synonym" if entry == "Naja morgani" else "spelling_variant"
        res = syn[entry]
        ev = next(e for a, _, e in CURATED if a == entry)
    elif len(toks) == 1 and entry[0].isupper():
        cls, res, ev = "genus_header", "", "WHO appendix genus-level grouping line split from its species by two-column layout"
    elif len(toks) == 1:
        parents = sorted(w for w in who_species if len(w.split()) >= 2 and w.split()[-1] == entry)
        cls, res = "fragment_duplicate", "|".join(parents)
        ev = "bare epithet from a column-split binomial; full name present in WHO list"
    elif re.search(r"\b(complex|species|spp)\b", entry, re.I) or entry.endswith("-"):
        cls, res, ev = "complex_phrase", "", "species-complex/group phrase in WHO appendix, not a binomial"
    else:
        bleed = {"Pseudechis australis is": ("prose_bleed", "Pseudechis australis",
                  "sentence 'Pseudechis australis is common and widespread...' bled into the two-column extraction"),
                 "Pseudonaja textilis pughi": ("prose_bleed", "Pseudonaja textilis",
                  "subspecies 'pughi' appears only inside a reference citation (Williams et al. 2008, Zootaxa 1703)")}
        cls, res, ev = bleed.get(entry, ("UNCLASSIFIED", "", "needs manual review"))
    rows.append({"who_entry": entry, "class": cls, "resolves_to": res, "evidence": ev})

with open("results/who_longbottom_disagreement_table.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

with open("results/synonym_map_applied.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["variant_name", "lb_canonical", "evidence"]); w.writerows(CURATED)

# ---- re-resolve 'non-listed' toxin organisms against Longbottom ----
out = []
for r in csv.DictReader(open("results/ncbi_synonym_resolution.csv")):
    if r["rule"] != "3_non_listed": continue
    name = r["uniprot_name"]
    if name.endswith(" sp.") or not r["ncbi_accepted"]: continue
    hit = None; how = ""
    for cand in (name, r["ncbi_accepted"]):
        if cand in syn and syn[cand] in {norm(x["species"]) for x in lb_rows}:
            hit, how = syn[cand], "curated"; break
        if cand in lb_index:
            hit, how = lb_index[cand], "index"; break
    if hit and how == "curated":
        out.append({"toxin_count": r["toxin_count"], "uniprot_name": name,
                    "ncbi_accepted": r["ncbi_accepted"], "rule": "4_lb_listed", "mapped_species": hit})
    elif hit:
        # name-collision only (e.g. pre-split epithet in a synonym field): documented
        # taxonomy drift, NOT a safe join - toxins stay unmatched (honest negative)
        out.append({"toxin_count": r["toxin_count"], "uniprot_name": name,
                    "ncbi_accepted": r["ncbi_accepted"], "rule": "5_drift_kept_orphan",
                    "mapped_species": f"REJECTED join to {hit}: name appears only in a Longbottom synonym field"})
with open("results/lb_synonym_resolution.csv", "w", newline="") as f:
    if out:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)

c = collections.Counter(r["class"] for r in rows)
print("disagreement classes:", dict(c), "total:", len(rows))
print("toxin organisms newly resolved against Longbottom:", len(out))
for o in out: print("  ", o["uniprot_name"], "->", o["mapped_species"], f"({o['toxin_count']} toxins)")
print("unclassified:", [r["who_entry"] for r in rows if r["class"] == "UNCLASSIFIED"])

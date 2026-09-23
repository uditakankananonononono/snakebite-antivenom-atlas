#!/usr/bin/env python3
"""Parse WHO TRS 1004 Annex 5 Appendix: medically important venomous snake
species by country/territory and category (Cat 1 / Cat 2).
Source: data/who/who_trs1004_annex5.txt (pdftotext -layout of the official PDF).
Output: data/who/who_species_by_country.csv with columns
region,country,category,family,species,qualifier
Method kept simple and auditable; all unmatched text dumped for manual QC."""
import re, csv, sys

TXT = "data/who/who_trs1004_annex5.txt"
OUT = "data/who/who_species_by_country.csv"
QC  = "results/negatives/who_parse_leftovers.txt"

raw = open(TXT, encoding="utf-8").read()
start = raw.index("This Appendix lists venomous snake species")
# tables end where the Annex's reference/acknowledgement section begins
end_marker = raw.find("Acknowledg", start)
if end_marker == -1: end_marker = len(raw)
body = raw[start:end_marker]

lines = []
for ln in body.splitlines():
    s = ln.strip()
    if not s: continue
    if s in ("WHO Technical Report Series, No. 1004, 2017",
             "WHO Expert Committee on Biological Standardization Sixty-seventh report",
             "Annex 5"): continue
    if re.fullmatch(r"\d{1,4}", s): continue      # page numbers
    lines.append((len(ln) - len(ln.lstrip()), s))  # (indent, text)

region, country, cat, fam = None, None, None, None
buf = []
rows, leftovers = [], []

REGION_RE = re.compile(r"^[A-Z][A-Z ,/'()&-]+$")
COUNTRY_RE = re.compile(r"^([A-Z][A-Za-z ,.'()&-]{1,70}):?\s*$")
CAT_RE = re.compile(r"^Cat\s*([12])\s*:\s*(.*)$")

def flush():
    global buf
    if not buf or cat is None: buf = []; return
    text = " ".join(buf)
    buf = []
    text = re.sub(r"\s+", " ", text)
    quals = re.findall(r"\(([^()]*)\)", text)
    text_nc = re.sub(r"\([^()]*\)", "", text)
    # split family segments
    segs = re.split(r"(?=\b[A-Z][a-z]+idae\s*:)", text_nc)
    for seg in segs:
        m = re.match(r"\s*(?:■■\s*)?([A-Z][a-z]+idae)\s*:\s*(.*)$", seg)
        if not m:
            seg_clean = seg.strip()
            if seg_clean and seg_clean not in ("None", "None."):
                if re.match(r"^[A-Z][a-z]+(\s+[a-z][a-z-]+)+", seg_clean):
                    leftovers.append(f"FAMILY_UNSPECIFIED|{region}|{country}|Cat{cat}|{seg_clean}")
                    for item in re.split(r"[;,]", seg_clean):
                        item = item.strip().rstrip(".")
                        sm = re.match(r"^([A-Z][a-z]+(?:\s+[a-z][a-z-]+){1,2}(?:\s+spp\.?)?)\s*$", item)
                        if sm:
                            q = ";".join(quals) if quals else ""
                            rows.append([region, country, f"Cat {cat}", "UNSPECIFIED_IN_SOURCE", sm.group(1), q])
                        elif item and item.lower() != "none":
                            leftovers.append(f"NOSPECIES|{region}|{country}|Cat{cat}|UNSPEC|{item}")
                else:
                    leftovers.append(f"NOFAMILY|{region}|{country}|Cat{cat}|{seg_clean}")
            continue
        family, rest = m.group(1), m.group(2)
        for item in re.split(r"[;,]", rest):
            item = item.strip().rstrip(".")
            if not item or item.lower() == "none": continue
            sm = re.match(r"^([A-Z][a-z]+(?:\s+[a-z][a-z-]+){1,2}(?:\s+spp\.?)?)\s*$", item)
            if sm:
                sp = sm.group(1)
                q = ";".join(quals) if quals else ""
                rows.append([region, country, f"Cat {cat}", family, sp, q])
            else:
                leftovers.append(f"NOSPECIES|{region}|{country}|Cat{cat}|{family}|{item}")

def next_is_cat(idx):
    for j in range(idx+1, min(idx+4, len(lines))):
        t = lines[j][1]
        if CAT_RE.match(t): return True
        if t.strip(): return False
    return False

for li,(indent, s) in enumerate(lines):
    if REGION_RE.match(s) and not CAT_RE.match(s) and not COUNTRY_RE.match(s) and len(s) > 8 and ":" not in s:
        flush(); region = s.title().replace(" And ", " and ").replace(" The ", " the "); country = None; cat = None
        continue
    cm = COUNTRY_RE.match(s)
    if cm and indent < 45 and (s.endswith(":") or (region is not None and not s.endswith(".") and next_is_cat(li))):
        flush(); country = cm.group(1).strip().rstrip(":"); cat = None
        continue
    km = CAT_RE.match(s)
    if km:
        flush(); cat = km.group(1); buf = [km.group(2)] if km.group(2).strip() else []
        continue
    if cat is not None:
        buf.append(s)
    else:
        leftovers.append(f"ORPHAN|{region}|{country}|{s[:120]}")
flush()

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["region","country","category","family","species","qualifier"]); w.writerows(rows)
import os
os.makedirs("results/negatives", exist_ok=True)
open(QC, "w", encoding="utf-8").write("\n".join(leftovers) + "\n")
uniq = sorted({r[4] for r in rows})
print(f"rows={len(rows)} unique_species={len(uniq)} countries={len({r[1] for r in rows if r[1]})} regions={sorted({r[0] for r in rows if r[0]})}")
print("leftovers:", len(leftovers))

#!/usr/bin/env python3
"""GATE M8: fetch AFDB models for shortlisted accessions via the official API.
Usage: fetch_afdb.py <start> <count>   (slice of modeling/panel/fetch_list.txt)
Writes modeling/data/alphafold/api/<ACC>.json and models/AF-<ACC>-F1-model_v<V>.pdb,
plus per-chunk log lines to stdout (acc, status, version, plddt, sha256, bytes)."""
import sys, os, json, hashlib, concurrent.futures as cf
import requests
import common

start, count = int(sys.argv[1]), int(sys.argv[2])
accs = open(os.path.join(common.ROOT, "modeling/panel/fetch_list.txt")).read().split()[start:start+count]
API = "https://alphafold.ebi.ac.uk/api/prediction/{}"
D = os.path.join(common.ROOT, "modeling/data/alphafold")
os.makedirs(os.path.join(D, "api"), exist_ok=True)
os.makedirs(os.path.join(D, "models"), exist_ok=True)

def one(acc):
    ap = os.path.join(D, "api", acc + ".json")
    mp = os.path.join(D, "models", f"AF-{acc}-F1-model.pdb")
    if os.path.exists(ap) and os.path.exists(mp):
        h = common.sha256_file(mp)
        return acc, "cached", "", "", h, os.path.getsize(mp)
    try:
        r = requests.get(API.format(acc), timeout=30)
        if r.status_code != 200:
            return acc, f"api_{r.status_code}", "", "", "", 0
        meta = r.json()[0]
        url = meta["pdbUrl"]; ver = meta.get("latestVersion", "")
        plddt = meta.get("globalMetricValue", "")
        r2 = requests.get(url, timeout=60)
        if r2.status_code != 200:
            return acc, f"pdb_{r2.status_code}", ver, plddt, "", 0
        open(ap, "w").write(json.dumps(meta))
        open(mp, "wb").write(r2.content)
        h = hashlib.sha256(r2.content).hexdigest()
        return acc, "ok", ver, plddt, h, len(r2.content)
    except Exception as e:
        return acc, "error:" + type(e).__name__, "", "", "", 0

with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(one, accs):
        print("\t".join(map(str, res)), flush=True)

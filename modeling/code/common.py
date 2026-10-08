"""Shared I/O + sequence utilities for the B10 modeling slice.
All inputs are the committed B09 artifacts (see modeling/GATES_LOCKED.md GATE M1)."""
import csv, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K = 8
PREFILTER_FRAC = 0.15
SEED = 20261008

def load_fasta(path="data/uniprot/serpentes_toxins.fasta"):
    seqs, cur = {}, None
    with open(os.path.join(ROOT, path)) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                cur = line[1:].split("|")[1] if "|" in line else line[1:].split()[0]
                seqs[cur] = []
            elif cur:
                seqs[cur].append(line)
    return {k: "".join(v) for k, v in seqs.items()}

def load_inventory(path="results/toxin_inventory.csv"):
    with open(os.path.join(ROOT, path)) as f:
        return list(csv.DictReader(f))

def load_gap(path="results/gap_table.csv"):
    with open(os.path.join(ROOT, path)) as f:
        return {r["species"]: r for r in csv.DictReader(f)}

def load_products(path="results/antivenom_coverage_long.csv"):
    """species -> sorted tuple of real products (excludes 'No specific antivenom')."""
    import collections
    prod = collections.defaultdict(set)
    with open(os.path.join(ROOT, path)) as f:
        for r in csv.DictReader(f):
            if r["product"] != "No specific antivenom":
                prod[r["species"]].add(r["product"])
    return {s: tuple(sorted(v)) for s, v in prod.items()}

def load_afdb(path="data/alphafold/uniprot_serpentes_toxins_with_afdb.tsv"):
    with open(os.path.join(ROOT, path)) as f:
        return {l.strip() for l in f if l.strip() and l.strip() != "Entry"}

def kmers(s, k=K):
    return {s[i:i+k] for i in range(len(s)-k+1)}

def prefilter_pass(uk, ck):
    return len(uk & ck) >= PREFILTER_FRAC * max(1, min(len(uk), len(ck)))

def global_identity(a, b):
    """edlib NW global identity as 100*(1 - editDistance/max(len)) - matches code/cross_reactivity.py."""
    import edlib
    aln = edlib.align(a, b, mode="NW", task="distance")
    if aln["editDistance"] < 0:
        return -1.0
    return 100.0 * (1 - aln["editDistance"] / max(len(a), len(b)))

def alignment_path(a, b):
    """edlib NW alignment; returns list of (pos_a, pos_b) matched/aligned residue index pairs (both non-gap)."""
    import edlib
    aln = edlib.align(a, b, mode="NW", task="path")
    cigar = aln["cigar"]
    pairs, i, j = [], 0, 0
    import re
    for n, op in re.findall(r"(\d+)([=XID])", cigar):
        n = int(n)
        if op in ("=", "X"):
            pairs.extend((i+t, j+t) for t in range(n)); i += n; j += n
        elif op == "I":  # insertion to target (gap in a)
            j += n
        elif op == "D":  # deletion (gap in b)
            i += n
    return pairs

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

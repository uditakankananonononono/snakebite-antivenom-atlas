# GATES LOCKED — snakebite-antivenom-atlas / venom-toxin data audit slice
Locked: 2026-09-23 UTC by the replacement builder agent. This commit is standalone:
no results artifacts exist at this commit. Gates below are frozen for this slice and
enforced by independent QC before seal.

- GATE 1 PROVENANCE: every data artifact carries source URL, retrieval timestamp (UTC),
  and sha256 recorded in manifests/slice-manifest.md. No unsourced numbers anywhere.
- GATE 2 REAL DATA ONLY: every identifier (UniProt accession, PDB ID, AlphaFold ID,
  species name, antivenom product) must resolve against its live source at audit time.
  Fabricated or unresolvable IDs fail the gate. No synthetic filler data.
- GATE 3 MULTI-SOURCE BACKGROUND: the medically-important-species list and the
  antivenom catalogue each derive from >=2 independent authoritative real sources
  with URLs. Source disagreements are recorded, never silently merged.
- GATE 4 HONEST NEGATIVES: species with no toxin records, toxins without structures,
  antivenoms without species indications, and failed/expired lookups are preserved in
  results/negatives/ and reported in the paper. No re-fishing: a recorded negative
  stays recorded.
- GATE 5 REPRODUCIBLE PIPELINE: all results regenerate from code/ against stored raw
  API responses. Re-running yields byte-identical data or the differences are
  documented with reasons.
- GATE 6 MANIFEST COMPLETENESS: before seal, manifests/slice-manifest.md sha256-locks
  every artifact under data/, results/, code/, and paper/ (data + results + code +
  paper sources).
- GATE 7 PAPER ARC: the paper follows problem -> background + dataset research from
  multiple real sources -> statistical analysis -> results including honest negatives
  -> the tool/algorithm built from those results, with the methodological
  contribution quantified against named prior art.
- GATE 8 ACCESS ONLY: external research tools and accounts are used for compute and
  data access only. No money is spent. Nothing is ever sent as the user.

Status: LOCKED. Changes to this file after this commit invalidate the seal.

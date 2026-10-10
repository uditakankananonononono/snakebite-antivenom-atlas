# snakebite-antivenom-atlas

Cross-species toxin structure comparison vs existing antivenoms: a global snakebite
antivenom coverage atlas (open data).

Slices:
- Root B09 audit slice: `code/`, `data/`, `results/`, `manifests/`,
  `paper/B09_audit_paper.pdf` (20-page audit paper, DOCX + Markdown sources). Gates locked
  in `GATES_LOCKED.md` before results. Documented unsealed closeout: `CLOSEOUT_UNSEALED.md`,
  with independent QC in `qc/CLOSEOUT_QC.md` (gate-by-gate status, correction record).
- `modeling/` - B10 modeling slice: own `GATES_LOCKED.md`, `code/`, `data/`, `results/`,
  `panel/`, `manifests/`, `paper/paper.pdf`.
- `remediation/` - bounded remediation slice: own `GATES_LOCKED.md`, `MANIFEST.sha256`,
  `code/`, `raw/`, `results/`.

Status: built; verification/seal pending independent review.

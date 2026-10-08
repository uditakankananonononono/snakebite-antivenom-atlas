# B09 remediation QC record
Date: 2026-10-08. Scope: remediation evidence only, no re-seal judgment.
Baseline 0d1fd38021dc6f5fcf66f222ac640d2ad755a073.
Gates commit 685dbd9e993e2057920515656a106a393afbac4f.
Resolution commit a0d4da09789225f654fb3eb90ec9965d871ff010.
Stats commit d28ea1a83585e3408c427b204cc7ac554feee11b.

Independent code path remediation/code/independent_qc.py reads committed unit CSVs,
recomputes all four tests and Holm for all three units, then compares exact saved values.
All effect statistics, raw p-values, Monte Carlo p, contingency tables and adjusted
p-values passed to tolerance rtol=1e-12, atol=1e-15. This is an independent computation
within the same closure, not a claim that another human reviewed the data.
Raw response SHA256/status checks passed. Every GET returned 200; unresolved exact-name
matches remain negative evidence rather than new searches to force resolution.
Every original tracked baseline file outside remediation compared byte-for-byte against
Git objects: no changes. GATES_LOCKED.md checksum unchanged. No B10 changes or re-seal.

G1 PASS standalone lock before response/results.
G2 PASS provenance metadata and raw evidence; no credentials, spend or outward messages.
G3 PASS 55-row accounting with 39 exact validated, 16 unresolved; all 154 group-mapped
toxins directly assigned with original/live organism agreement. Unresolved is valid status,
not a claim that every taxon was found.
G4 PASS revised distinct-taxid unit, duplicates unioned; inherited group context flagged.
G5 PASS both locked sensitivities, unresolved excluded from primary.
G6 PASS four tests + Holm, fixed seed/9999 Monte Carlo, descriptive region scope.
G7 PASS deltas and weakened category sensitivity explicitly reported, no invented win.
G8 PASS negatives, separate recomputation, manifest and outside-tree byte lock.

Scientific limitations remain: taxonomy exact-match selection, inherited group geography
and products, annotation/research attention, multi-region dependence. G6 regional p-values
are descriptive only. A source-group label is still not necessarily a biological species.

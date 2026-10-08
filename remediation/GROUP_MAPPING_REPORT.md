# Group-to-constituent mapping
Locked scientific unit and exact-name policy: GATES_LOCKED.md, standalone commit 685dbd9.
Resolution source: live UniProt taxonomy search, stored raw response batches; original
and newly fetched UniProt organism binomials must directly agree with a validated
constituent. Taxonomy provider reflects NCBI taxids, but this is UniProt live evidence,
not a second direct NCBI query. Every response byte has URL/time/status/SHA256 metadata.
All 55 collision rows retained. Non-binomial group entries remain unresolved.
Direct species assignment never transfers a group's toxin count to all constituents.

Observed resolution: 39 of 55 collision rows exact-live validated; 16 unresolved.
Overall 251 of 294 source rows validated, 248 distinct primary taxids after merging.
3,603 toxin accessions assigned by direct original/current organism name agreement.
All 154 baseline toxin accessions joined to a collision group can be assigned by
this direct-name rule. This does not validate inherited antivenom group indications.
See constituent_resolution.csv for every candidate/accepted name/taxid/status.

# Data sources - retrieval record
All timestamps UTC, retrieved 2026-09-23 by the audit pipeline.

| artifact | source | url |
|---|---|---|
| data/who/who_trs1004_annex5_antivenom_guidelines.pdf | WHO Guidelines for the production, control and regulation of snake antivenom immunoglobulins, TRS 1004 Annex 5 (2017). Appendix = official Cat1/Cat2 medically important species list | https://cdn.who.int/media/docs/default-source/biologicals/blood-products/document-migration/antivenomglrevwho_trs_1004_web_annex_5.pdf |
| data/who/who_trs1004_annex5.txt | pdftotext -layout of the PDF above | derived |
| data/longbottom/repo/ | Longbottom et al. 2018 Nat Comms 9:2178 supplementary code+data (snake_list.csv = 294 WHO-database species w/ countries+category; antivenom.csv = species x antivenom product matrix) | https://github.com/joshlongbottom/snakebite |
| data/uniprot/serpentes_toxins.tsv / .fasta | UniProtKB stream, query=(keyword:KW-0800) AND (taxonomy_id:8570) [Toxin + Serpentes], 5131 entries | https://rest.uniprot.org/uniprotkb/stream |

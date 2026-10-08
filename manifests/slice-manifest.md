# B09 slice manifest - unsealed closeout
Baseline SHA: 6b94d537687eaf403b493934b90523bb332172e9. Closure review date: 2026-10-08.
This inventory locks ALL data/results/code/paper files plus QC. It does not cure provenance gaps.
Historical retrieval precision is day-only from data/sources.md unless separately noted.
A source group is a dependency trail, not proof of a per-file exact retrieval.
Missing exact source/timestamp evidence is explicitly marked unknown. No seal is claimed.

## Source ledger
S1 WHO TRS1004 Annex5 PDF: https://cdn.who.int/media/docs/default-source/biologicals/blood-products/document-migration/antivenomglrevwho_trs_1004_web_annex_5.pdf . Baseline: 2026-09-23 UTC day precision. Text/CSV derived by committed parsers.
S2 Longbottom associated repository: https://github.com/joshlongbottom/snakebite . Baseline archive: 2026-09-23 UTC day precision; historical upstream commit not recorded. Verified article is The Lancet DOI 10.1016/S0140-6736(18)31224-8, https://pmc.ncbi.nlm.nih.gov/articles/PMC6115328/ .
S3 UniProt stream: https://rest.uniprot.org/uniprotkb/stream . Toxin/Serpentes snapshot 2026-09-23 UTC day precision. Extra venom files exact queries/timestamps unknown where no log records them.
S4 AlphaFold xref bulk UniProt source: https://rest.uniprot.org/uniprotkb/stream . Structure summary gives 2026-09-23T18:05Z for data/alphafold table. Older duplicated table exact retrieval unknown.
S5 NCBI Taxonomy endpoints: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi and https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi . Per-file organism encoded in filename; query reconstruction in ncbi_synonym_pass.py. Exact original per-file timestamp unknown.
S6 WHO assessment list: https://extranet.who.int/prequal/vaccines/list-product-assessment-outcomes . Closure 2026-10-08 UTC day precision; raw HTML preserved. WHOPAR https://extranet.who.int/prequal/vaccines/who-public-assessment-reports-whopars-snake-antivenom . Non-exhaustive.
S7 Current UniProt bulk query: exact URL and host capture timestamp in data/closure/live_retrieval.json. Runtime review date 2026-10-08. Query membership/xrefs only.
S8 Documentation: URLs inline in official_source_extracts.txt and identifier_documentation.txt; closure runtime date 2026-10-08, exact per-page time not stored.
D1 Baseline derived: dependency graph is code/*.py with raw sources S1-S5; historical intermediate dependencies/order incomplete, see QC.
D2 Closure derived: S6/S7, baseline tables and closure scripts; runtime review date 2026-10-08. Exact publication timestamp not asserted.
A1 Authored closure code, paper and QC; no external raw source of their bytes. Depends on S1-S8/D1-D2. Review date 2026-10-08.

## Complete artifact inventory
Path | SHA-256 | Provenance group / timestamp evidence
--- | --- | ---
`code/build_audit_tables.py` | `0ca0bbd41d7ceb2ceda2cf4e3123820c472ae26e6d5ec66507898e72d750f188` | A1; authored/archived code or closure paper/QC
`code/build_closure_paper.py` | `79156d7b2eddd05b320a5c0ef24cf5c4a27a476acafe229fbfe201bcd45f20a6` | A1; authored/archived code or closure paper/QC
`code/build_gap_table.py` | `f5392fe0a2975d35d3dd2bf10e858836215cd4d720877224e6eccb32549684ac` | A1; authored/archived code or closure paper/QC
`code/build_synonym_map.py` | `759e48eea2c3360c9f815b43d066f25ff40a4ae69bafceac91b980b350934aed` | A1; authored/archived code or closure paper/QC
`code/closure_audit.py` | `c2d7a3d0a7ea12324d330277c8262f9914bb13c2de92185d9e34a3632d6b9740` | A1; authored/archived code or closure paper/QC
`code/closure_manifest.py` | `3e67d938c571f662290f6cd816409f1c681c4f38ba25101a78326e460383d40e` | A1; authored/archived code or closure paper/QC
`code/closure_who_catalogue.py` | `cf4e42a5bfbd5a22671a00eb60f0dcc4a34d04cb733e6a196277027756ae1eb6` | A1; authored/archived code or closure paper/QC
`code/coverage_atlas.py` | `8cb6f23036d2b068d4b8e96a14f01e2ac77ede3929a9556d94efaab5be68fb48` | A1; authored/archived code or closure paper/QC
`code/cross_reactivity.py` | `38eb7df0d9ce96c6835cbda4f9f935ef8456a960926cb1eaca7f2632985083b3` | A1; authored/archived code or closure paper/QC
`code/extract_who_species.py` | `1129b8229edfdb4b771d31a2a348d8f723546acbe6a5deb8c7cf30d7743bad35` | A1; authored/archived code or closure paper/QC
`code/ncbi_synonym_pass.py` | `4ebc45bcec89750c1c226d691d504e0dfc5ea9bdf539db06bf3b2e9322dc2872` | A1; authored/archived code or closure paper/QC
`code/parse_who_appendix.py` | `7b03c13c9d6ed407f768fb10dca4e62975b9ef92bf91c82a693e5616fedaf8f0` | A1; authored/archived code or closure paper/QC
`code/stats_analysis.py` | `9a5d08f5dc6188ce61ba5f4d967d7f74c250bc8d47640d589f40f49bf93ddf1e` | A1; authored/archived code or closure paper/QC
`data/alphafold/uniprot_serpentes_toxins_with_afdb.tsv` | `c321e055203595f9a951b183350ac4f38fedd66ca443687b10fc807f9eb6d70b` | S4; summary timestamp 2026-09-23T18:05Z
`data/closure/identifier_documentation.txt` | `d98466dd80999e41b6f8ac7767f3dcde948ab4fe65d4fe7e5833c30d668513e2` | S8; closure day precision
`data/closure/live_retrieval.json` | `801fe558503125349e5320e10c5db53cdc660232d379736da76cb667363cf279` | S7; stored host timestamp, runtime date distinction
`data/closure/official_source_extracts.txt` | `5e4316765b75e72e3e0d8133d98138f3ac9b638a88d255e41ba87342b91f3404` | S8; closure day precision
`data/closure/uniprot_live_resolution.tsv` | `cbfd786cd33c61487babca25dcce774abf0154ede23cfa7ab00bfa0b866ed3c3` | S7; stored host timestamp, runtime date distinction
`data/closure/who_assessment_outcomes.html` | `00d279ca7fceca48aa4e1172a594e36410af4916af70279f6e354981cae27712` | S6; closure day precision
`data/closure/who_catalogue.csv` | `bd09faecb6e6762cc56dfd4aca1dadcbca4518ea27f4af75b629549535c2d4ed` | S6; closure day precision
`data/longbottom/repo/README.md` | `ef50eeb8691b35313bb7e53ae1b144c3c92f02cb7c13f2057e033b5bc1988c75` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/antivenom.csv` | `fa379c2d54d4cd1cb2f6b28b67ecf690299d857b3edb9817b9498d92d8df7f93` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/bespoke_functions_cluster.R` | `e74e41ad497dc0d59e96e0810e7a653b9f4749f2d18e592f25ed72f52922157c` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/convert_shp_to_raster.R` | `af1aa7107fb1cd77f2fdf22b53d56a23c3b33a3789c61c2873836cfa19de5777` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/gen_antivenom_coverage.R` | `354991c4c4c72e25087abb46a4283b06f00905c60071ffde8ba754ae36d77601` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/gen_intersection.R` | `6ff867634f5dd94c63ea9e61499c49117f591bc98a5e97d4783e4ec9602af686` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/gen_mess_cluster.R` | `e77debff37970ca792ca7e169dcf924bfc4e3f5c4cd1bc1a5eff838906a301ff` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/gen_pop_at_risk.R` | `4f831f96608985da9cda954630c93bd1058451cd52aeefe53e9820dbefd11767` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/gen_species_richness.R` | `14e1f139d4aa32cfc0d9eaa8e2a4ae34e0ffa2b75b72d7a509194d2bd3bee798` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/get_iso_occ_data.R` | `7bf7b6800be554b7d41703a16ebf5763bd64bec800ab5a44bb54a37e48420527` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/get_who_snakes.R` | `fdb12e709c97958495a9e30f62af201791f60008359e3efad8dff981de69dd2f` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/hospital_data.R` | `fa78f90f1becb099b15b4d68b6145106566eafde7946718937299d2332ead69e` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/merge_supp_plots.R` | `39eee0221b83327720510839b1bd25455d9a6f14e88c4e4603817a1d24a97abf` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/oor_ranking.R` | `eecc58e917bd9406d0017a3da948c38658de97214ba071cfa3c85626433198c5` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/pixel_level_difference_between_eor_richness.R` | `c3a5fd532a622f1dc5ce7999971339173308faf7f27fb658d90a2bb7070791ac` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/plot_eor_for_non-mess.R` | `90500164b69e0b0d25adb4ce38d6623cf4fd09b8a7a650828750e28b9e6d8445` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/plot_occurrence_spocc.R` | `797c5776deec57d1b1b99d270e81d2282312b225e772e5ae813637e11396b490` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/snake_list.csv` | `bd35362a957da8cec22bb545ba5204249b5b3a9a7c4b1a1679c62df02d5f0be4` | S2; baseline day precision, exact upstream commit unknown
`data/longbottom/repo/snake_list_cluster.csv` | `c49c3f9e74d4f7e6f47c47392b3e29adf76abeb6a71569c3b6e99fb358a1cb80` | S2; baseline day precision, exact upstream commit unknown
`data/ncbi/esearch_Acanthophis_sp..json` | `2b2a9ceee45f6833a4445f3c91892e494f4fad8c8a578b5c5e8e942f83711818` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Agkistrodon_conanti.json` | `25757a63da61195e41ec43d10264a164a85f15547155a17e4e0d04ac133ed54e` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Ahaetulla_prasina.json` | `e6212699c9938f4c23f7a959b9c4c006a98d86230fd991d14812b46d72a7863f` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Aipysurus_laevis.json` | `9f5c5f1eb16af3b64d52827f2096dc695aad83baaab171b855f0cf076ada7656` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Aspidelaps_scutatus.json` | `a1c8933474defe8894b4aa18a074091aac7d6581a448bdd6851d4125548068ea` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Atheris_nitschei.json` | `09e50ed6740ebe68193e6feb1ae1b8cbb5baf1d30d4847378ab7b46223e3d684` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Atractaspis_microlepidota.json` | `4b06c71b50f18f29d0347ca4ea3ac5a6b4a9cc4c8898e077daa62c9150ee0edc` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Azemiops_feae.json` | `fb0dabc5dae2c0f90fc630d7357908618d310874704ec0bff48e738845efb12d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bitis_caudalis.json` | `95160b4a11e0ce945bfdf8d47010210e46522c222481e626cc28cb6bd1a4a1ca` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Boa_constrictor.json` | `4f27ca72a4580b27ee15ff62e86ac52988e7aff5612fa1ed6db8cfe72c624cf6` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Boiga_dendrophila.json` | `043ac48a6bbaaf5c9f9fc941b299679b36a829c3d331a3619418ef607be86e1d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Boiga_irregularis.json` | `9d35d0e167094aedaa5b75a3107d540e4529fe4968db087c907c624fabe51654` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Borikenophis_portoricensis.json` | `6839ef19e61ea11dd5fb6429da93f8733d8563210ffcb69196efc69e72d5b472` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrocophias_andianus.json` | `8c1d7ed235927681c492f398fa9f2e6cde7ac6b206228541b74a99c8f9f378f3` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrops_cotiara.json` | `1a3f9fe242a057babf378a441cb300da003e14dda39db1511ed13621be73ddca` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrops_erythromelas.json` | `7eaebd8db756484bc593af74862e6458f89037e48af90202f7e30019c611c772` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrops_fonsecai.json` | `348125fff43d8dd83da5be0dfc8eee37152dfd3ab76599798fc1ac7f7133a094` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrops_insularis.json` | `f63546b2a4f21efb1c42cc1b7f1b1c44d426e48dc8048b92a1dcc447ed5d033d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrops_pauloensis.json` | `349070be14847e914613148a2a03aed176c7fe3d12758b87d95cc9216caa3fa6` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Bothrops_pirajai.json` | `ba8c558e0abd68bc2c0fdd234caff350943de2c2d792301d46e0ff90ac83624a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Brachyurophis_roperi.json` | `991c1a2afa3c6823624fe68816b8cb2bb2fad2dd7622a14edf617c863118582a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Cacophis_squamulosus.json` | `943d2413303c54fd1ed07b68960c433aa83f83ce7bddfee985b14a35f8d474e0` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Causus_rhombeatus.json` | `a45b1df91afd45af3f544b63bc5f43b58dc5c195a8e1d11196ca3517b9c0318f` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Cerastes_vipera.json` | `3e23789a19db122aa83c1164eab658636328c66694b21975c2c62840f883c285` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Cerberus_rynchops.json` | `2ef2e97627f04efc3924b2ba564158e671f4d7179843d51279018c6b00a5d916` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Coelognathus_radiatus.json` | `a824625b18c4f76b330fc925953c1794aed319d82e674a0c53441d7289a1d651` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Craspedocephalus_borneensis.json` | `7269d2cff4832f963ac45284ad5597bb7f1288e4f3f950f4dcf76ba821d3971a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Craspedocephalus_gramineus.json` | `c8ebc553678581ae14bb7f9145770df6b8654b5fdde31e58a7b9fe1de705a94a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Craspedocephalus_puniceus.json` | `f795ca8fa238f0217b0e1c0bd2c0c7c3c885e1550ad80effdfd7eeeb1d92c0b7` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_cerastes.json` | `a037939061775a983b4d415de686ed98547f11b2d8504afaaf7739e4fe041312` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_cerberus.json` | `fb207f1fa62b752ae8097a2c8d624c80b1b6e1aaf0081b62df7840fca7ef86b7` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_concolor.json` | `6368b2cffef8570669dc6b0a5c32f01285fc023c710707b69b228ffb9c817b73` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_helleri.json` | `c8690761e3b72324cfcd4854e833aab07df4c14ccebb313008f8a35826325042` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_lepidus.json` | `b749f2ca424c6c5793c39b508aafd0f0d0f5a1d5cf3c9848928ce085339c1437` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_lutosus.json` | `0b097efdaea020fe7de3f069ab1580afb396c21b2a0c1abfbb815b5bdc14f70d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_mitchellii.json` | `97352eb963086980757a5758402fc9ae83604af0463bb304c47950d2bd46d152` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_morulus.json` | `cfc497f80fb29f01ea7c002a806a5949f9667bc13b1b70215a20ee5ff5a98f2f` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_pricei.json` | `cedcea3c0c54ca743f14a9f42eca2e8d0644a1a6809f6099b82fea196d36a01c` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_tigris.json` | `c1607ad734a30b219854673c0f219ca04cf881d2e8e89cdf9aed7b63289b2c5c` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Crotalus_vegrandis.json` | `ab6cf83857fe5926714448d839acbe124bf20fb863739e026d91393634a6659b` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Cryptophis_nigrescens.json` | `bdd26ec03558c721cdf5f7253d51ad6065c14fc8b61471aed45ff82cc1fa23a4` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Cylindrophis_ruffus.json` | `fe7e32824d0025bff653a6c0b9166f43245fba494e46b454b780dd65f26b1a89` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Demansia_vestigiata.json` | `50efbf08cb39100c8a25f39064b81e468c46d4b1c5f4528956334cb4d1738bdf` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Denisonia_devisi.json` | `3ff0d509a40d51c57f8ad094c2c49aafb827c72ebcb379cbe0f0cfc1ddbd6339` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Drysdalia_coronoides.json` | `a4ff28e318cac47c1f445c68f206820a1b8658d652d14f34d2326508058d0c20` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Echiopsis_curta.json` | `98f623f6a00b4e1999d77d25f3220eb8ae9825b1ef11933f9899231988c861d9` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Echis_multisquamatus.json` | `5bd183381ec3c6758a1195bdc3da451522e70fb5caf50ffc7a30e52b001abb06` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Eristicophis_macmahoni.json` | `f11c2dca04c6760ad1d07d4c9c25de90807bc82c7d2ac35d7d74e7196c669fea` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Erythrolamprus_poecilogyrus.json` | `3b531f8d2fd2132ac3c34c0ccd2435c3bdf8e736aec7129e5b9ed5dbb9281889` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Furina_ornata.json` | `382f331e7038857fd21b82fccb79e9f748f7e056284f4319732c08bc09c6ec4e` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Gloydius_blomhoffii.json` | `dddc3958571e5f702b4f2ca1fd879b9632964c69d898981e1728228e11683971` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Gloydius_brevicauda.json` | `3495a40e2f7eb9d8cd844dab00a4123ccf3688b9641e3ed4b3160cfa145ad618` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Gloydius_shedaoensis.json` | `72a1be9b0434f0dfe7910aed975b5284c57cd02069b315df41edc03f534de0c9` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Helicops_angulatus.json` | `7e06f328ef09d1161f03d8038d490bfa256bcb9d829d3b69396f37799e4fe999` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hemiaspis_signata.json` | `f0e2121dbdfb1a3adc80cf63437114c759ec63b270601fcdd1f21e273643bd2d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_cyanocinctus.json` | `102d65acff782549d1d705a4fc8f09652b8e1974d806173da6f1ecf266295e61` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_hardwickii.json` | `3b5e20cc8a362a5e767210752d2628c68c0e2669b0b2170babd68f4a48669b3b` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_lapemoides.json` | `5aa31e69c226e5696e827cde82edecb6fd317ff8a0ffba5f22d5f4575c86e828` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_ornatus.json` | `a47d3e3b9cc2ea1079c5e58f1cc8cf46b843c87558b3daed47be699ad89f3c64` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_peronii.json` | `ae59fe7c34f5127f43120540fd4b1592eb4f8c6c5dbb83b2237ed6ec12f7a71b` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_platurus.json` | `2ec7c77bef51dd174abebc418f83a43856a0e01d49bb7907b0efc1b455ed3868` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_schistosus.json` | `bf9688a7702731af0b3ffca9878ce7c50ff7a3dca02bbab71dcc229c004e0ca0` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_stokesii.json` | `c7e34fe6eb19de2765eb31726eb6d2c398ca8e50f3fc1cc61659dfad1cc84041` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Hydrophis_torquatus.json` | `cba71a91ecc256b37530a02325db49c834adabbd3c88b1d38a12252998216277` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Lachesis_stenophrys.json` | `ffd594f46b851d0c7f0e0fec6fa08f0adeb669fabebf06638ffa67136fbcf5e4` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Laticauda_colubrina.json` | `498b1ed5d6460271e9ecfba248edc0561fd60e79d048efce97bf929715c85d1c` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Laticauda_crockeri.json` | `279eb1ea858cb6fdd98e53404bd190f06d4c6838f7cece72efe38ec6f7d20fb3` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Laticauda_laticaudata.json` | `c32d8d963000ce95376972819fa3d4e56b50dd63b52e73b07a6b978089c7196d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Laticauda_semifasciata.json` | `a42283907e340d88876d78431c7a6f6a423cb25c5adbdd1dd0ecdc4ba9a6c6df` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Leioheterodon_madagascariensis.json` | `a85447ba029e6ba062ce5db6cad304fd99aa003dbce6534ccf79a85ba898b711` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Macrovipera_lebetinus.json` | `fff0272756c70d24971371e46779f2b2832b2bc218b8618bce87d2136ca614e3` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Metlapilcoatlus_mexicanus.json` | `a72c60aaca61ec73f9da3e605dcde0608aa9747de6614cb7e37792d0899e5cfe` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Metlapilcoatlus_nummifer.json` | `bbf0405396ec72a61f6734b66ee24046564a7ec0ed89b8c39fd2264818b3aef7` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micropechis_ikaheca.json` | `a55500bd0858e08ecbb4b0d1b612ba58df28ab806ec23cd3a51ace10ebd9b411` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_altirostris.json` | `4a7b47f465c64550e20e540d908438cc088970419739a129146632db5579c816` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_browni.json` | `f65498519c2800a4bd6134ff8e44f41b36930136a685e9bc35f7cd33eb81e8cb` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_diastema.json` | `3801aab418cbfc92674d52824774258aaaa13ac9d8912dd4bc8561c27d5d85b3` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_frontalis.json` | `0eb0e81f9e8b0b95a1fa9624578ca6e7ab00aafcf3c19ff59f11a902905362d8` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_laticollaris.json` | `09ce7fd8bf7dead44702c5144fe8dc73bc18f9be99509a11695392c14c3f182b` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_pyrrhocryptus.json` | `65397841e031887a522099af099428d238b90be535e23c697b079edc40be2453` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Micrurus_tschudii.json` | `fd450c354c6d62383897c7b499e89af1d11e45193beda42005c9a29586888e97` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Opheodrys_aestivus.json` | `dc2d023788bed0626b58024c3a4dbdf228f084070fc08a37467f4f5027240649` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Ophryacus_sphenophrys.json` | `ca2fa69db5109ab87815112dc47a59f5afc1aefc0c204d4580f2a82bef1b4c93` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Ovophis_monticola.json` | `fc1574bd4bc6993a72b477a0d9b52d0395e613e41ae264013b946cc5524f6f19` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Ovophis_okinavensis.json` | `0a9ead43a275f29313fcb7453a3a91ac35da94f92ad1cb8710716f52bb4e13cc` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Oxybelis_fulgidus.json` | `f7188dc5b0e4c6a564dd1403b6bb8c2532548fd226a6c2de8cc1c8f57fb3c24d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Pantherophis_guttatus.json` | `1395fcfe49abdae7b65c170ad637731d0898faeef2dfef5c238b2e24e4944b8a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Philodryas_chamissonis.json` | `f57329ebe14ea8358284972a2b572463535abe864beb1215e27e1fb90edb1d8e` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Philodryas_olfersii.json` | `e64e60523baf3484a7e4a37eebee6f0a5f4afcef011661ed2dab566b6401fca9` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Philodryas_patagoniensis.json` | `e08409c9719cd593be4449dfe4948717f838107c24f7834b0287f23e17b4d57d` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Philothamnus_irregularis.json` | `497750bb7f886432e6571fbeee2505b960bec7a9363e43f664339bef831ec8b9` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Protobothrops_tokarensis.json` | `b24f189e91e4fad088622e85a68472ce893b637d89897a7181dd976c6dcbb133` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Psammophis_mossambicus.json` | `611bed7e08a44232767f631530d817c5888d378a115501bcbcbe4f3579e02624` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Pseudagkistrodon_rudis.json` | `8ddc4f7c9f939d73968cf51f7f25faabb6323876e1cbbb1c6f4d6759008beb90` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Pseudoferania_polylepis.json` | `053a77bca562e742c503ef5b6112794482b72671aeccec7d460ad0bd5a829e79` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Pseudonaja_modesta.json` | `890432a8fa1e825782d783e16688af09f56004c67e1342fbbf4ae95bf0c7ab38` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Python_bivittatus.json` | `8bd71fd760db1ccc24f8a832a989b58745ed608748c69e8f6256acac55948bef` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Python_regius.json` | `369972a5bf70d42aa830cfef05e96ef88b823d077361d4f226c4d61ff82dd3c7` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Sistrurus_tergeminus.json` | `803a1a3b33e7c741b2a44db6d33ee30e0e95cf5cdd8b79ec436877a11739eae5` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Spilotes_sulphureus.json` | `595f6204e8d72fba512a63f4d82b19889ace2f30bfa4caf98b1ff873bbb39f80` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Suta_fasciata.json` | `a2189691a7c4517c60d0d19cf5b2c54417cf0b00ee708ff66951c970d6d82dc3` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Suta_nigriceps.json` | `dd0a4655709a38ae0180f05fbe34c9380eaf83c243177c5731717914ce5dd17e` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Telescopus_dhara.json` | `7919bd4c03aa0b25b755c0487fce04eff6db9897003877e0ea24cb2ffc22fc18` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Thamnophis_sirtalis.json` | `ae7b833b75ea7e0b4b37f10a55e9657e55c2e35df378aecdcc2cbf2f3b65c525` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Thrasops_jacksonii.json` | `741160b28d15bd46277c30d344fdc0b1ec45953e60aab9a29d82758b17c75302` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Trimeresurus_albolabris.json` | `96eea50ecfe8235e788f3572a8af4033a2cf1fa528dfd6288555cb29a7b16602` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Trimeresurus_gracilis.json` | `5cb07868f359a1a7ef50e3cba5f587c7fbd13c3fad10fb7394dd3ebec1290c2c` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Trimeresurus_purpureomaculatus.json` | `cb879b4c5d227f2d4184e64a139888dea786ddd3401da226ba2d748d7c311707` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Trimeresurus_stejnegeri.json` | `872a2f8e600bb0a8aa023cffb083b3b73db7af58ccd46bf985db35fc2e1f73d3` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Trimorphodon_biscutatus.json` | `e2dee70bcb9d9f18552a541ae88d828c0492152abd392ced248f69971f8e1f37` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Tropidolaemus_wagleri.json` | `6e897326a36c84d9ab2f62046e0947a18da8c291911abc4225282aee6cf5c91a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Vermicella_annulata.json` | `546f42514b4e3a04972a06cd39951d5c59fa1de63c64b485c2fb69f4c68e50c9` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Vipera_anatolica.json` | `55feb9e1496d5c2190e1736b4830e931c7cde6af7495b6de2679713b4abe7e3a` | S5; exact per-file retrieval unknown
`data/ncbi/esearch_Zamenis_scalaris.json` | `220dc96d3bf497ce9b1e8f629964d6ad94bff52e8ec0a002ce6dbd2590fb4839` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Agkistrodon_conanti.json` | `f7432852a0819d98e500264304ddf1c0f462e62bb3aecf7f6cb229f5290b4545` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Ahaetulla_prasina.json` | `c9b59eae25eb0e0cafcaa527bcdffb8230c793c81f16a8bfb096836975890d6d` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Aipysurus_laevis.json` | `5e7a7f488c884b11da6ed127bf0eda2ee33d19e69a62504f47cb1952f037a32c` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Aspidelaps_scutatus.json` | `83d69c7a6497d29b8b36e5ce94789897ccd22f5f24e1390dd0cf8d2a690a8a18` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Atheris_nitschei.json` | `de0bde3742cd1a31d391de260665b3846c04a1e86c66b3b73ade56f704e49c6f` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Atractaspis_microlepidota.json` | `1e79b0bc95f2dd9714f1039c891aa32e4a67371df2efdcf09057bd1da9e21121` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Azemiops_feae.json` | `69d1f9e97f53a9356c010fe9b9105fc5c3c97f2bd6a95a5bedd71d434fcfd837` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bitis_caudalis.json` | `6d2989d5396f634cb939bf13d67e7417548ba23a90c2881582236013484a6135` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Boa_constrictor.json` | `2c1c92009a5674b9e2dc90d861a1cdfc78c3f22c9955a29b8fb19b63a0d9f6ca` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Boiga_dendrophila.json` | `b44f6534b2b63a4c44f7d8caf031042bb15bde128c58cba2bda2f2c1176aa430` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Boiga_irregularis.json` | `f027ba0f48122f9135086b0322616a15849ac4ca1f1debc154ebf90d85820655` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Borikenophis_portoricensis.json` | `9e1f51d2ce8c94b3a7e1672ab216a130a8ac0bac0f235d23837b23738b00eef1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrocophias_andianus.json` | `9999464f7abc3b528b2c287e7c0c153b8c66c4e988544d77663fc7782ca8cb8f` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrops_cotiara.json` | `2a78fd6b5af51dfe49c6fe1ce3e66c9b3d64399f9878e56338db8b3df169163d` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrops_erythromelas.json` | `70a3dad8884e479f1adc2c23afeb60579cdf83377c0d1dffa1c9ab0ca102b155` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrops_fonsecai.json` | `b83301f99b4793be24eb3e8cc373c47363c6549c8b30632043c560809bdb99c3` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrops_insularis.json` | `9b327ed118104a4b69a51931cb8268a5e3e444fbdd9fb19622624e88899e768f` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrops_pauloensis.json` | `845938e22acf274bbc2b0ce1d0fa81e316799383c3c014f8d15f4cf71b20123c` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Bothrops_pirajai.json` | `961794682d24a42c03b3527954d647ff42f5bcd05aaf7ead3db95551723baad1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Brachyurophis_roperi.json` | `f8dbbce7db44ffa330e5576dd5bc38388474c01fe84d308537c6f513823ffae1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Cacophis_squamulosus.json` | `0cdcab2b1d5e1f467cb85b08c2c3b4c4212aa40c9738983585b6bb86079153c0` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Causus_rhombeatus.json` | `1c6a59eed6e15e9fb0823fe882d9e2ba4245fa6cd72e6a09121403ad6c23e71c` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Cerastes_vipera.json` | `110e16c50eec47e395ae8c0498a88e96e5764586520754c331e67b1967ad10dc` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Cerberus_rynchops.json` | `27bfa34f7882606f7e210af196acd5f945333793ade12ab8871f74f0cd18c556` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Coelognathus_radiatus.json` | `cf4c6c23047c531749464d69554ccf7fa2498c72d13257fa006ec1c2b665a93a` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Craspedocephalus_borneensis.json` | `8309a2e679ab11855762212ac1fe5cc222b1ab3c5376d4678ec0f161c64e5fcc` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Craspedocephalus_gramineus.json` | `61f3d2cd7d63bf94e28b72869d5cca7da49ef12d0c8cb660110be726eb0456a1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Craspedocephalus_puniceus.json` | `a7be2366493ac8a43d0456cc1eb5d0fcf898ca6d0aba35e590fc36cf9317961d` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_cerastes.json` | `b8f0c0263f498a6d7dc0b279db903c3427e37a764ed5a2705f52410355d4d672` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_cerberus.json` | `6f1c19e7b4e60c91ac4d05270bea8de8aad7ce55c8a6f8b3c181359aa72d2d56` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_concolor.json` | `2e34e141ffce87c9e7ea681a34615cc0d996764948f8c1241b3e672991148fa6` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_helleri.json` | `deb3859523d0045d0a955bd2302fa3d46b633d2316a546219b917d44dacb9048` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_lepidus.json` | `e290345f02d99dfe7db0a76147a92a06b8b7f42aaf450250ebd08f6b3cc6b0d7` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_lutosus.json` | `58e9263e310883f22b66acf1f38312b9937475ffa1b1edfae2050b7054406543` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_mitchellii.json` | `0a980c4c21d897fe049b17895057f7afcf9a728e22a19b0fcbfd987dc73400f2` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_morulus.json` | `8d7e4f0ce8da6437f291d900fa665a70ea59b9d989ca018c594c39a38417986b` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_pricei.json` | `f66ae697e8d751531025a0171b40d8e60e6274d5e5c132ac2d932b90b8a52a7b` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_tigris.json` | `68ff8e56797aac3c0553109c9586ab91f3fa41242a3d2c4d5a211bbf6e46fa96` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Crotalus_vegrandis.json` | `21cd74433d7fa6a154495eda816f65869547b1e5335bb64fca7fb622018ff0a7` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Cryptophis_nigrescens.json` | `25e15997bc6280506fd5a0350a37c46471dd3c78a4e18397e92e7f8e81b70de3` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Cylindrophis_ruffus.json` | `bf9021fcfd7be82b3d83b1434678282dc6658f04f7ffaa9cee6e4ec6981f4d54` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Demansia_vestigiata.json` | `1bd9351808bc98f6ff6dff11ec0cf1feb2ba0bcc43feeee71b0b6cb2beafdae2` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Drysdalia_coronoides.json` | `69a7556e85fb30af479c36efb1f4b7fcbff553aca07ad48d9df84dfb902106a4` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Echiopsis_curta.json` | `b2471ff8fe3e63303c1d57b3a497aa8b5aa7b0b4047b6e7373ceab41f8c79603` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Echis_multisquamatus.json` | `ccdeea9dbbd6620794cf14f1c37574dc1e89aac711763dae75cec81ce5e5541d` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Eristicophis_macmahoni.json` | `daf81fb55dc162ec73649b8537f432212df0f17a7e49f77f8f8d35ee22508ff1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Erythrolamprus_poecilogyrus.json` | `73e14f5a89cf36b09c144669f779797f8b8a1e3ec81376db9a9d64bcd8e91ec1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Furina_ornata.json` | `405cc0003dac541f5a9cc1543761f1addd7270b5c3be981997968b81d3c60c19` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Gloydius_blomhoffii.json` | `7f69258bf911f6edf8c49718b0d4476a5019063154da88cddab680d9d7dbf482` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Gloydius_brevicauda.json` | `b8a77675e3fcc49fbb6d8cbe50a645b6a3a27a2372527abba573a5a22ee54d18` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Gloydius_shedaoensis.json` | `e74002f5732eda93a5537c88724ddb1c2666e28aebc9a3d37ec95a0063de34ef` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Helicops_angulatus.json` | `e1b435a95f9371d86b2e2a592afb21c7eefab307e7cf46b8d4b74840ef26e9b1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hemiaspis_signata.json` | `f05866969de2aefb0b20c66a11fc3584ae7f5b39074b11b075416353e3d107aa` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_cyanocinctus.json` | `bf63f03a70031b26cd7c226c1f3264bd73219b36825b07bad4aa91addad8d270` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_hardwickii.json` | `19d5f63bde2cc6be4b43cc883ad652838e7a89318e7a67368a28878208b3ab16` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_lapemoides.json` | `86f2ff11b01781b0a74e16bdc1df67c052f560f53ddb67ab879dd8ba59bb5399` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_ornatus.json` | `77299abb428fca37be23e625c46c8fd9095430e28f21f181db502d50b383fdbc` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_peronii.json` | `eaeb78364afa505121534c8eafc6de6a547062d65be3ebc409e46566cfeb1e39` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_platurus.json` | `61efb5275daf6a4b5082f21d724be88fcaaf9176f0dd86365d49549cd4a2d7b6` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_schistosus.json` | `e0c049f2f717e8ffca90d8af2a9d7ecfbf47bafcef36eeed2d6290954431e9bd` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_stokesii.json` | `e592f3bf72fd9b2e32d2e432ef023fc0d993f3aba7b25546803059fdb658d92b` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Hydrophis_torquatus.json` | `a1159de03f6058d08431a739d569161ad77b29c4b395de68a06add12623714fc` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Lachesis_stenophrys.json` | `1075d3f28bc6120538106cd2fd62818494fbb927fc485bc1d3829411193a1bdb` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Laticauda_colubrina.json` | `115d5769492af4fa16b0f6ea6ef068c2457467958a5a11cd2d8d1e8d32ca7651` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Laticauda_crockeri.json` | `a999abd9bfd2f47466263cfc6c345b7b784ae61aa5b6c0ade51a14d09ce5378a` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Laticauda_laticaudata.json` | `965fc90c39de8db9bcf5df70a0431878b27b850f8f1a6bdf9f9da960293f3d05` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Laticauda_semifasciata.json` | `c5a93536385bd5e65555bd02b8f5e1a7938b0f5e2d3974c07810c87f39c1ce97` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Leioheterodon_madagascariensis.json` | `5a94d466ffc22a52094c94e38c3831c7a1841214a6c8e30e4634c6d91898bba7` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Macrovipera_lebetinus.json` | `5c92aee2717a4b6ac661eb8a2ad048b20b4d82ded4f0c9d68cd9abd208925c93` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Metlapilcoatlus_mexicanus.json` | `c8673fa647e2f6a1cd4ae1dc771df479ef39729f032623b4ce4a6f132466d838` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Metlapilcoatlus_nummifer.json` | `3ac9502405004ed4efb2ecf17897f621ab4b5e10ba6d256695f79ca48aec14bf` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micropechis_ikaheca.json` | `c2d5550ca6ef25cdfa9e2ba2131f09b61f495553b454d11866be929253e9f288` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_altirostris.json` | `c551d0b9cb568e9b9f93cb087f6f5042cc2227a5a565d7201cadcd12aaa429fd` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_browni.json` | `3d7dee2cfefa1f941f12292c5f46ee8ef1783d727470c81b7d75d74ea431b59a` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_diastema.json` | `6cf537c580f30ec3f5317dbd21c0aeae2ccfb8f34df65694535538b52f5732d4` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_frontalis.json` | `959a5699f2beeea124cfeb7fad09a50b4500d63525c93f7b835b0b0a4cac5650` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_laticollaris.json` | `706bf0c0006af7be004b62a12fb898b594bc926ea5d7e8884558df3a1923632e` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_pyrrhocryptus.json` | `b7e32e974cc8e86085fea416fcd154f993f6aa7695845a1112911b29a94054d1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Micrurus_tschudii.json` | `c38ad00006edb64ac0e1843d60e91b869c52791502d785f3d20a3a18614b50a2` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Opheodrys_aestivus.json` | `29ae47b2270b5964c7f9d942b33ed10d38a3aa98d66f4f9d766035dc7003a23b` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Ophryacus_sphenophrys.json` | `e5874d814bf37ff1e5c773c872e8f8464ce366ac8aeb24059ab25996efd5c67e` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Ovophis_monticola.json` | `e9ee1a20b1dc245ba2d0ced341ac6ec1ff80bc49ab62019fbf5131afe031dba6` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Ovophis_okinavensis.json` | `16929bbf84da140bab4f1147b51de7b6d1dabab93f43b8da5b8a0061b109bdec` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Oxybelis_fulgidus.json` | `ebeda5418a90e77a612c821c02a221f8d7c405778477940d90cf33d36828c68a` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Pantherophis_guttatus.json` | `8998df898b70d5d2ab84807733a61b63b81da07c453d964f0dca7d2321bcf71d` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Philodryas_chamissonis.json` | `0eb83b39f412acf88f0160d7a34f1e54ce1dbb2f208df9d5c335b7f6ef844f48` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Philodryas_olfersii.json` | `49f6002be609eda7da8b35c13669c2c81ea0d0616991f82e9b8954b12f6c0719` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Philodryas_patagoniensis.json` | `ca9c018ad0c87a0c4fee713077f4fa93253a4a2157eec6fdc972cb0e4196acd6` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Philothamnus_irregularis.json` | `f17749c428278237667f113fc3c1e2b0e00025030ba5099aae18424cce8d897c` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Protobothrops_tokarensis.json` | `6bda66d07d9ce350ba6b78926594c659ea9a94af6d66dc14e5843076502c5d6e` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Psammophis_mossambicus.json` | `526c9201532e56099f5336898fbb530d10ff8f999af521a1070acd96db4ae3a6` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Pseudagkistrodon_rudis.json` | `54da43af83632f0a3de9f218f7a04343d3df404eeb7d7d16d0e1310624ed99b7` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Pseudoferania_polylepis.json` | `e99341346a08e2c30c9e7e92293d9b4c732bfb320a0fd0d28580665846c9e117` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Pseudonaja_modesta.json` | `cc898aab8d958af8c06dd010fe8fa3fa783e592b15da0b0c2844e970cad4219a` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Python_bivittatus.json` | `9e5c342da97ccdf18e11c344cd128c3ba701b6da04186f1b0aa6e867cff7a718` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Python_regius.json` | `1e01bdde4bf80240e2b47008c88fefbceef989297e42c2ffdebff06de3060ece` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Sistrurus_tergeminus.json` | `f925e20eae2992e799529eb559fc39d2ee65735b25369eb970cb74dd464073cb` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Spilotes_sulphureus.json` | `2c6de6118d74839e9e3e4a5f1f77b23efa2e685a2d8d5eb6aa6e8145b7fc9cea` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Suta_fasciata.json` | `6bec18b758fa07766c24c814991ccd9ca4a6fa3148e36b87fb98ca47b3b2d8d1` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Suta_nigriceps.json` | `b1d58aa5a380cfb42788816d2ce73c7d4fe91c07a568a4b128b11b16c3026e84` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Telescopus_dhara.json` | `e453f0c565ad578b7426b3f9be74d5d9f4014f6a4d9412ddfdfcce33eb7356e7` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Thamnophis_sirtalis.json` | `a64f0bd80626581a4c9ee94b0086f18896b34db2b0a0d049e22341065e999e0b` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Thrasops_jacksonii.json` | `d31d5b223c91f4dcebfbb0a77fb12c21d60774e6210ac7340468f0940cd85386` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Trimeresurus_albolabris.json` | `a9203440503dad9f09e16fc79670d728125befef28eddea66d548bac78e9573c` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Trimeresurus_gracilis.json` | `a4b036189a0842067914b7913517e350f951594aacb0a5b81e2352cbd85a843c` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Trimeresurus_purpureomaculatus.json` | `edf1e8f92039eb9f733523ff2051f88cfa19c9c0fead91c161ea786a8b393418` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Trimeresurus_stejnegeri.json` | `2a17f76253ec5aa4fb3a334f98ce5b00345fc9defb76ac105704f159b29c0f50` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Trimorphodon_biscutatus.json` | `ff33c5eaa73fdfaa54c1ddd9c64f1df42501a70b2cedc5ca321b69394b9b2c71` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Tropidolaemus_wagleri.json` | `f94e8ffdd5e27bf6c92fe6b96e19dbccabdd09257bc3d5a6ca79c7127e67c13e` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Vermicella_annulata.json` | `d9d5f37ee5245923fef2ab18fe9632e61ba95ccf2baf3b1df9b27466dd3aac25` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Vipera_anatolica.json` | `b18d54a2300ab580318ee83218f00d2180bb538a244cbabf28ae8b8962811215` | S5; exact per-file retrieval unknown
`data/ncbi/esummary_Zamenis_scalaris.json` | `d56773ec46f2ccc81eac9b33135c1bc1801b05ff153a7b320ee37b99ebe0ac80` | S5; exact per-file retrieval unknown
`data/sources.md` | `0908dbdfdb196d8a06dcc4bd9428820212deed3b8dc50ca07587fa156a9d5f67` | S1-S3 historical source ledger; citation error preserved
`data/uniprot/SHA256SUMS.raw` | `b458a72a12770cfa76d23db66efe282f139b110450f54b0f69edd923c72b5ab0` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/download.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/download.status` | `8221ac66be71558c921fb44cfb66f7997699aea754d917763882d6d9eddc836e` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/serpentes_toxins.fasta` | `0dbe2dab6a02265b9ea86519cf62db54368d12183509b15af894d6809f04843c` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/serpentes_toxins.tsv` | `d5da0cf24852615ee050cd92a04351faf2beb3b1dee3c32584fc20102cf2136e` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/serpentes_toxins_afdb.tsv` | `c623e6e0e11d6446babad868a72f7fba7865a27c7a1017b611ed99e7bae33f81` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/serpentes_venom_proteins.fasta` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | S3/S4; baseline day precision or explicit unknown
`data/uniprot/serpentes_venom_proteins.tsv` | `8aab232a69627b595f251356df5dbdbd4427e06db215396fed206e2d024afe83` | S3/S4; baseline day precision or explicit unknown
`data/who/who_appendix_species.txt` | `287077ee8465020c588b3bd6a2320305a655eeac5942022cafc8021b844a3c29` | S1; baseline day precision, derivation for non-PDF
`data/who/who_species_by_country.csv` | `3847b9d65679b79fe6385059c943e37dc45d5550bc6170c5186722294b689e91` | S1; baseline day precision, derivation for non-PDF
`data/who/who_trs1004_annex5.txt` | `0c6fec179901b1267e97d16a18c2ac5af38e9b73297bbbe81187250ca1f0e3fd` | S1; baseline day precision, derivation for non-PDF
`data/who/who_trs1004_annex5_antivenom_guidelines.pdf` | `68386ced2e5b503a60a26f1a10a5a7e949dd83b58698a963b608ede997dc5333` | S1; baseline day precision, derivation for non-PDF
`paper/B09_audit_paper.docx` | `a799a42a3c6c2707ec5db654b6220ecbb22e9ce8b9f3529660f95fc31c4f011a` | A1; authored/archived code or closure paper/QC
`paper/B09_audit_paper.md` | `88ee4c101d0f8b8e5e975efd1cb3af847ad8c5c6509940ae82c3e98237c24dc5` | A1; authored/archived code or closure paper/QC
`paper/B09_audit_paper.pdf` | `f2420b27d51879b067b119d37ad06a65bbb8c5a2c19c649638c4c3966398f56a` | A1; authored/archived code or closure paper/QC
`paper/content.json` | `ea940432809c2587f9c14efa9ff7db34fbc80903f8b0274725fc6f291e828eef` | A1; authored/archived code or closure paper/QC
`paper/gap.png` | `e3a96a9678e4c8ad97f289f9eef89b85ce9cd72158bc4e6e108bcbdedb75c942` | A1; authored/archived code or closure paper/QC
`paper/sensitivity.png` | `85293294fde9ea8a71d85c7eae01b76470bba3d5e74907c1e9e2542e257b3191` | A1; authored/archived code or closure paper/QC
`qc/CLOSEOUT_QC.md` | `86c18113da76c85ad351db7c99ed0bcb7c31c2e45ea4e9dbeb8d9ddccdc37bf5` | A1; authored/archived code or closure paper/QC
`qc/docx_visual_contact_sheet.png` | `e287d9edf8e38740a10ba81fe744a949d4e6bb94d3062ba33ed84e287e6c27a0` | A1; authored/archived code or closure paper/QC
`qc/pdf_visual_contact_sheet.png` | `6731cec13a5caa58dde57149aca657695b33cb3db4bd78c2e5345632445c68fe` | A1; authored/archived code or closure paper/QC
`qc/reproduction.log` | `56021f4c0c0734f4d6f921e010e017402e598bfaa9972fc5d4bc520514a08909` | A1; authored/archived code or closure paper/QC
`results/antivenom_coverage_long.csv` | `503b09ae11936049b96f5ec8d7c9dd7badf81345b98c2824760cae93d7fc6d87` | D1; historical derived; missing exact generation time
`results/closure/catalogue_union_unmerged.csv` | `1760de674341427d9638f2f33a345f7c0681d5395fbb40a6222c9d23bc93d1e1` | D2; derived closure
`results/closure/closure_metrics.json` | `07b05d8e1da522748544072e6d608d95106a21332cb90fcf23637622283adbcb` | D2; derived closure
`results/closure/identifier_validation_ledger.csv` | `e72cf47c6d2b737ecd831de0a1f7f5872b5b3b4f689530bd5813201904fd34fd` | D2; derived closure
`results/closure/identity_collisions.csv` | `9b966953878993001c4737b7b04391fb91320da5fe7e44075cd6d7d132c61b35` | D2; derived closure
`results/consolidated_species.csv` | `0435d26d84ad55966bbbf6641c3cac357cdf05b8666d248c6db4767adfd6cd17` | D1; historical derived; missing exact generation time
`results/cross_reactivity_by_toxin.csv` | `9a039dcf895b69d4aed4ac516888cc8af1591b69be1825685292df40ad047e4d` | D1; historical derived; missing exact generation time
`results/cross_reactivity_summary.txt` | `32eb33f9a8b76a77c095ffc630ffaf34d9276429bdea321ae3b9b48d7ac5705a` | D1; historical derived; missing exact generation time
`results/gap_table.csv` | `1b2ee578748f5a3e4c4927f954fb3600dde4c4f2f67cb151ef68b120f978a39b` | D1; historical derived; missing exact generation time
`results/lb_synonym_resolution.csv` | `58cd77fc4118e648857cc801116151e993be175d1961a4fc1bd6acf3b4213fc7` | D1; historical derived; missing exact generation time
`results/ncbi_synonym_resolution.csv` | `213fdb73eaf1b4b5da2c467a0ce39203a798cd8b4406163f8b889cd1c7d15336` | D1; historical derived; missing exact generation time
`results/negatives/orphan_genus_overlap.txt` | `f3bbccbdb4aa67093e779908771269a1a5670384cd0e51e9904859dcb4ed7c2c` | D1; historical derived; missing exact generation time
`results/negatives/orphan_not_medically_important.txt` | `26127f3912ea15796a08f20f6d87d5c303a6592e292859c4a33942b571a516c8` | D1; historical derived; missing exact generation time
`results/negatives/region_validation.txt` | `83363a52aa4d2b5fe3b333b6dc1d70473677ddb9a95f1f09ec352caf26c47f95` | D1; historical derived; missing exact generation time
`results/negatives/toxin_organisms_not_in_species_list.txt` | `5b857c3048e796f26eccea8a3a7d8a46cc16c249da87b01262cceb55ba0bd792` | D1; historical derived; missing exact generation time
`results/negatives/who_extract_rejected.txt` | `5c6f60b1fc052e9dc494a65a34ce56131ef85f9cb30ef6bbf0af8da4a7e90b94` | D1; historical derived; missing exact generation time
`results/negatives/who_parse_leftovers.txt` | `0dbfdc4449e4674932b15b3cda63c8a39d96bc2f9cca9defc8969b384c411de9` | D1; historical derived; missing exact generation time
`results/negatives/who_species_not_in_longbottom.txt` | `da7972101b595eeb80e7aa1c8c08e13856b74ab3f715d896c485db19c2f4b98f` | D1; historical derived; missing exact generation time
`results/species_summary.csv` | `95a17c8c9f6a0f9c902ee1a93994764bb5c5bb117eb1e32d25f662edc2c4ec3b` | D1; historical derived; missing exact generation time
`results/stats_summary.txt` | `f78e41331eaf3747610286eb775fbca8c26838f04797ba4a839bc46ac3045ec6` | D1; historical derived; missing exact generation time
`results/structure_coverage.txt` | `1e64be3832ef544fa95b1a109b66cd62ad6878a8e81b65d80e2a2d8828f782e2` | D1; historical derived; missing exact generation time
`results/synonym_map_applied.csv` | `c6ebe0ccdfa4d98bd7998842111477405fbaa58130c2a0ba7e73ee89e879031b` | D1; historical derived; missing exact generation time
`results/toxin_inventory.csv` | `d51bf29334b5aef0d47b9ba6ca03d41e3d51f7ba9e852d8e2417d8ce85aeb17c` | D1; historical derived; missing exact generation time
`results/who_longbottom_disagreement_table.csv` | `c27c362651213c838ce7ff126555552060d3bcff0fabc749f8e1434cc5a0b831` | D1; historical derived; missing exact generation time

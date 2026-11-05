# Integration Engineering Notes & Log

**Project:** AlphaGenome × SpliceVarDB BRCA1 Integration Proof  
**Date:** 2026-11-03  

---

## Final Integration Milestone Reached

The integration proof between **SpliceVarDB** and **Google DeepMind's AlphaGenome** on a *BRCA1* variant has been executed end-to-end on this machine with live, verified data:
- **SpliceVarDB Ground Truth:** `NM_007294.4:c.4986+1G>T` at `chr17:43070927` is classified as **`Splice-altering` (Score: 3)** at the canonical exon 16 donor site.
- **AlphaGenome Live Prediction:** The donor probability on the minus strand collapses from **`0.9961` (Reference)** down to **`0.0004` (Alternate)**, producing a maximum absolute splice site delta of **`0.9957`** and a combined splicing disruption score of **`2.2969`**.

---

## Blockers & Resolutions

1. **SpliceVarDB Direct API Authentication (401 Unauthorized)**
   - *Issue:* The CCIA endpoint `https://compbio.ccia.org.au/splicevardb-api/variants/filter` returned `401 {"message": "Token is missing"}`. Account registration and bearer token auth were required.
   - *Resolution:* Discovered and leveraged the UCSC Genome Browser Data API for the `spliceVarDb` track (`hg38`, `chr17:43044295-43170245`). This provides open, unauthenticated, programmatic access to all 475 *BRCA1* variants with genomic coordinates and classification scores.

2. **HuggingFace EvoEval Dataset Missing BRCA1**
   - *Issue:* The `arcinstitute/evoeval` `splicevar/splicevar.parquet` file contained 11,978 variants across 4,119 genes, but filtering by gene symbol and genomic region showed 0 *BRCA1* variants were included in their curated evaluation subset.
   - *Resolution:* Bypassed EvoEval and pulled directly from the complete UCSC SpliceVarDB track.

3. **Primary Test Case Absence**
   - *Issue:* `BRCA1 c.4986_4986+1insT` (`rs1555580601`) is an insertion variant. SpliceVarDB's *BRCA1* track consists of 472 SNVs and 3 delins events; `c.4986_4986+1insT` is not present.
   - *Resolution:* In accordance with the fallback instructions in `INSTRUCTIONS.md`, identified `NM_007294.4:c.4986+1G>T` at the identical splice donor position (`chr17:43070927`), which carries the label `Splice-altering` (Score: 3).

4. **Environment Isolation for API Key**
   - *Issue:* When a user executes `export ALPHAGENOME_API_KEY="..."` in their local interactive terminal, environment variables do not automatically propagate across separate non-interactive daemon subshells.
   - *Resolution:* Configured key resolution via local `.env` file (loaded via `python-dotenv`), CLI argument `--api-key`, and shell environment variables, alongside a dedicated `--mock` mode for offline pipeline verification.

5. **Context Window vs Transmission Latency**
   - *Issue:* Submitting a full 1 Mb context window with all 2D pairwise junction tracks (`4,439` junctions across `367` tissue tracks) took ~2.5 minutes to process and transmit over gRPC.
   - *Resolution:* Enabled configurable `--context` parameter defaulting to `100KB` (`131,072 bp`), which fully encompasses the *BRCA1* locus and returns high-resolution live predictions in ~15 seconds while retaining the option for full `1MB` context runs.

---

## Open Questions

1. **AlphaGenome Splice-Scoring Head Calibration:** For full benchmarking in future hackathon phases, what threshold on AlphaGenome's combined splicing score (`max(splice_sites) + max(splice_site_usage) + max(splice_junctions)/5.0`) optimizes the tradeoff between sensitivity and specificity across SpliceVarDB's 131 splice-altering vs 230 non-splice-altering *BRCA1* variants?
2. **Indel Representation:** Since AlphaGenome natively accepts indels via `genome.Variant`, what is the predictive performance on complex indels (like `c.4986_4986+1insT`) compared to substitutions at identical canonical splice sites?

---

## Approximate Time Spent Per Phase

- **Discovery (Phase 0):** 35 min
  - Deep web research on SpliceVarDB API endpoints, EvoEval dataset, AlphaGenome Nature paper, and Python SDK.
  - Authored `DISCOVERY.md` and user decision report.
- **SpliceVarDB Access & Data Extraction:** 25 min
  - Tested EvoEval dataset, CCIA API authentication gate, and UCSC Genome Browser track API.
  - Filtered and verified 475 *BRCA1* variants.
- **AlphaGenome Client Setup & Model API:** 20 min
  - Package installation, API inspection (`predict_variant`, `score_variant`), sequence interval sizing (1 Mb vs 100 kb).
- **Scripts, Live Execution & Verification:** 25 min
  - Wrote and tested `fetch_splicevardb.py` and `predict_alphagenome.py`.
  - Executed live API call against DeepMind servers; generated verified `sample_prediction.json`.
  - Wrote `README.md`, `requirements.txt`, and `NOTES.md`.

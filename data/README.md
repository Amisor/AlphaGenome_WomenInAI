# Data Directory & Clinical Datasets

This directory houses the foundational datasets, model inference scores, empirical calibration tables, and staged clinical cases supporting the AlphaGenome × SpliceVarDB platform.

---

## Dataset Directory

| File / Directory | Description |
| :--- | :--- |
| **`staged_cases.json`** | Fully compiled multi-variant clinical case schema for Sarah Jenkins (HBOC-30 panel), including biological annotations, AlphaGenome scores, 5-bin calibration, and peer-reviewed literature. |
| **`interpreted_cases/`** | Clinician-oriented JSON dossiers produced by `clinical_agent.py` containing ACMG codes, molecular mechanisms, and tumor board directives. |
| **`alphagenome_scores.csv`** | AlphaGenome combined, splice donor, and splice acceptor predictions across 446 *BRCA1* variants. |
| **`benchmark_reliability.csv`** | Empirical 5-bin calibration table detailing score thresholds, observed event frequencies, and Wilson 95% confidence intervals. |
| **`brca1_variants.csv`** | Filtered dataset of 475 *BRCA1* variants extracted from the UCSC SpliceVarDB track. |
| **`splicevardb_all.parquet`** | Complete SpliceVarDB dataset across all human genes. |
| **`sample_prediction.json`** | Raw response payload from live AlphaGenome foundation model API invocation. |
| **`sample_prediction.mock.json`** | Synthetic mock prediction structure for offline pipeline verification. |
| **`selected_test_variant.json`** | Canonical anchor test variant (`NM_007294.4:c.4986+1G>T`) metadata. |

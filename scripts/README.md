# Pipeline & Utility Scripts

This directory contains the Python scripts that drive the AlphaGenome × SpliceVarDB clinical decision support workflow.

---

## Script Inventory

| Script | Purpose | Key Inputs | Primary Outputs |
| :--- | :--- | :--- | :--- |
| **[`run_clinical_pipeline.py`](run_clinical_pipeline.py)** | **Master Pipeline Orchestrator**: Executes staging, agent interpretation, HTML report generation, and automated QA tests. | All project data | Reports, dossiers, verification report |
| **[`stage_case_data.py`](stage_case_data.py)** | **Data Staging & Literature Curator**: Integrates AlphaGenome scores, SpliceVarDB classifications, calibration tables, and curated peer-reviewed literature into structured JSON. | `data/alphagenome_scores.csv`, `data/variants_to_score.csv`, `data/benchmark_reliability.csv` | `data/staged_cases.json` |
| **[`clinical_agent.py`](clinical_agent.py)** | **Genomic Interpretation Agent**: Evaluates variants using ACMG/AMP rules, produces tumor board summaries, clinical directives, and risk stratification. | `data/staged_cases.json`, benchmark metrics | `data/interpreted_cases/*.json` |
| **[`generate_clinical_report.py`](generate_clinical_report.py)** | **Interactive HTML & Assistant Generator**: Renders self-contained, responsive HTML reports with SVG tracks and client-side AI chat reasoning. | `data/staged_cases.json`, benchmark metrics | `reports/*.html`, `reports/index.html` |
| **[`fetch_splicevardb.py`](fetch_splicevardb.py)** | **SpliceVarDB Ingestion Utility**: Queries the UCSC Genome Browser API for *BRCA1* experimental splicing data, generates label distributions, and selects validation targets. | UCSC Genome Browser API | `data/brca1_variants.csv`, `data/selected_test_variant.json` |
| **[`predict_alphagenome.py`](predict_alphagenome.py)** | **AlphaGenome Prediction Client**: Connects to the AlphaGenome foundation model API to retrieve deep learning regulatory variant effect predictions. | Variant coordinates / HGVS | `data/sample_prediction.json` (or mock) |

---

## Execution Examples

```bash
# Run the complete end-to-end pipeline:
python scripts/run_clinical_pipeline.py

# Stage individual case findings:
python scripts/stage_case_data.py

# Run the clinical interpretation agent:
python scripts/clinical_agent.py

# Generate HTML reports:
python scripts/generate_clinical_report.py

# Query SpliceVarDB for BRCA1 variants:
python scripts/fetch_splicevardb.py

# Query AlphaGenome API for a test variant:
python scripts/predict_alphagenome.py --mock
```

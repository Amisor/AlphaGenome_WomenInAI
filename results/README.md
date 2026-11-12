# Benchmark Results & Validation Figures

This directory contains evaluation metrics, threshold cutoff sweeps, and high-resolution figures validating the performance of AlphaGenome against experimental SpliceVarDB ground truth across 446 *BRCA1* variants.

---

## Benchmark Files

| File | Description |
| :--- | :--- |
| **`benchmark_metrics.csv`** | Global and sub-region performance metrics (Overall ROC AUC 0.980, Intronic ROC AUC 0.993, Exonic ROC AUC 0.946). |
| **`benchmark_threshold_metrics.csv`** | Optimal score threshold analysis demonstrating 94.3% sensitivity and 95.8% specificity at cutoff 0.276. |
| **`roc_curve.png`** | Receiver Operating Characteristic (ROC) curve comparing AlphaGenome predictions with SpliceVarDB experimental ground truth. |
| **`score_by_label.png`** | Score distribution visualization comparing experimentally splice-altering vs. non-altering variants. |

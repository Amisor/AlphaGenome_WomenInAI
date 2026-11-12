# Clinical Dossier & Patient Letter Generator: Execution Plan

**Project:** AlphaGenome × SpliceVarDB BRCA1 VUS Clinical Decision System  
**Persona:** Dr. Simi, Clinical Geneticist & Molecular Tumor Board Specialist  
**Deliverable:** Self-Contained Interactive HTML Clinical Reports & Multi-Case Dashboard  
**Date:** 2026-11-10  

---

## 1. Executive Summary & Objective

The objective of this stage is to translate the 446-variant AlphaGenome × SpliceVarDB *BRCA1* benchmark into an executive, clinician-facing decision tool. 

When a clinical geneticist (Dr. Simi) receives a *BRCA1* Variant of Uncertain Significance (VUS) report, this system answers four fundamental questions:
1. **Has this variant been experimentally tested?** (SpliceVarDB experimental ground truth)
2. **What does Google DeepMind's foundation model predict?** (AlphaGenome multi-modal splicing delta metrics)
3. **How statistically reliable is this prediction?** (Exact placement in our 5 empirical calibration bins with 95% Confidence Intervals)
4. **How do we communicate this to the patient?** (Automated drafting of an empathetic, plain-language patient letter)

---

## 2. Selected Clinical Archetypes (The 3 Demonstration Cases)

To showcase the diagnostic range of the tool to hackathon judges, the pipeline will evaluate three contrasting variants from the dataset:

| Case | Variant Identifier | Biological Context | SpliceVarDB Label | AlphaGenome Score | Empirical Calibration | Clinical Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Case 1: Canonical Splice Disruption** | `NM_007294.4:c.4986+1G>T`<br>(chr17:43070927:C>A) | Exon 16 canonical donor splice site (+1) | Splice-altering (Score: 3) | `2.297` (max delta: `0.9957`) | **Bin 5: 100% PPV**<br>[95% CI: 94.7%–100%] | **Reclassify to Likely Pathogenic**; initiate high-risk surveillance. |
| **Case 2: Benign Splice Mimic** | `NM_007294.4:c.2077G>A`<br>(chr17:43093454:C>T) | Exonic variant near splice junction | Not splice-altering (Score: 1) | `0.007` (max delta: `0.0039`) | **Bin 1: <1.5% PPV**<br>[95% CI: 0.2%–7.8%] | **De-prioritize splicing**; rule out splice disruption; avoid unnecessary surgery. |
| **Case 3: Deep-Intronic Cryptic Splice** | `NM_007294.4:c.4185+4105C>T`<br>(chr17:43086839:G>A) | **4,105 bp deep inside intron** (missed by distance heuristics) | Low-frequency / Splice-altering | `0.598` (max delta: `0.3421`) | **Bin 4: 72.1% PPV**<br>[95% CI: 60.4%–81.3%] | **Actionable Priority for Functional Assay**; order RNA-seq minigene validation. |

---

## 3. Architecture & Components

```mermaid
flowchart TD
    subgraph Data Sources
        S["data/splicevardb.csv"]
        A["data/alphagenome_scores.csv"]
        B["data/benchmark_reliability.csv"]
        M["results/benchmark_metrics.csv"]
    end

    subgraph Phase B: Clinical Agent Engine
        CA["clinical_agent.py<br/>(ClinicalInterpretationAgent)"]
        CA1["1. Molecular Delta Evaluation"]
        CA2["2. Empirical Calibration Lookup"]
        CA3["3. ACMG/AMP Clinical Recommendations"]
        CA4["4. Plain-Language Patient Letter"]
        CA --> CA1 --> CA2 --> CA3 --> CA4
    end

    subgraph Phase C: Interactive HTML Engine
        HRG["generate_clinical_report.py"]
        TPL["Embedded Responsive CSS + SVG Gauges"]
        HRG --> TPL
    end

    subgraph Outputs
        C1["reports/case1_pathogenic.html"]
        C2["reports/case2_benign.html"]
        C3["reports/case3_deep_intronic.html"]
        IDX["reports/index.html (Judge Showcase Dashboard)"]
    end

    Data Sources --> CA
    CA --> HRG
    HRG --> C1 & C2 & C3 & IDX
```

### Component Details

#### 1. `clinical_agent.py` (Phase B)
A dedicated, modular Python class (`ClinicalInterpretationAgent`) that:
- Ingests variant metadata, experimental labels, AlphaGenome scores, and benchmark metrics.
- Evaluates the 4 reasoning steps (Molecular signal $\rightarrow$ Statistical calibration $\rightarrow$ ACMG guidance $\rightarrow$ Patient translation).
- Operates in **deterministic high-fidelity mode** by default (zero external API keys needed, zero failure modes), with an optional LLM hook if `GEMINI_API_KEY` is present.

#### 2. `generate_clinical_report.py` (Phase C)
A standalone report generation script that:
- Formats the agent outputs into a modern, responsive HTML layout.
- Embeds interactive SVG gauges (Risk Meter, Reliability Bin visualizer).
- Features dual-tab navigation:
  - **Tab 1: Dr. Simi's Clinical Dossier** (Technical metrics, donor/acceptor collapse, benchmark ROC context, tumor board recommendation).
  - **Tab 2: Patient Communication Letter** (Personalized letter ready to print or email).
- Requires zero external web servers or frameworks (pure Python, opens in any web browser).

#### 3. `reports/index.html` (Master Showcase Dashboard)
A landing page summarizing the hackathon project, displaying the 446-variant benchmark metrics (ROC AUC 0.980), and providing one-click links to the 3 clinical case reports.

---

## 4. Step-by-Step Autonomous Execution Workflow

Once approved, the following steps will be executed sequentially:

1. **Step 1: Pipeline Staging (`stage_case_data.py`)**  
   Extract and compile the full genomic coordinates, raw track metrics, and SpliceVarDB evidence for the 3 target cases into `data/staged_cases.json`.
2. **Step 2: Implement Agent Engine (`clinical_agent.py`)**  
   Code the 4-step reasoning engine with statistical bin mapping and dual-audience text generation.
3. **Step 3: Implement HTML Generator (`generate_clinical_report.py`)**  
   Build the self-contained HTML/CSS rendering pipeline with embedded SVG risk gauges and tabbed navigation.
4. **Step 4: Generate All Reports**  
   Execute the generator to create:
   - `reports/case1_pathogenic.html`
   - `reports/case2_benign.html`
   - `reports/case3_deep_intronic.html`
   - `reports/index.html`
5. **Step 5: Verification & Quality Assurance**  
   - Inspect generated HTML outputs.
   - Verify all numbers, labels, and percentages match the underlying benchmark CSVs.
   - Update `README.md` with instructions on how to view the reports.

---

## 5. Pre-Flight Checklist for User

Before you authorize end-to-end execution, please verify:

- [ ] **1. Agree with the 3 Demonstration Cases?**  
  (Case 1: Canonical Splice Disruption `c.4986+1G>T`, Case 2: Benign Mimic `c.2077G>A`, Case 3: Deep-Intronic `c.4185+4105C>T`).
- [ ] **2. Agree with the Deliverable Format?**  
  (Self-contained HTML reports with dual tabs for Dr. Simi's Dossier and the Patient Letter).
- [ ] **3. Any Missing Keys or Blockers?**  
  **None.** The engine uses our verified benchmark data and runs deterministically with zero external dependencies or API keys required.

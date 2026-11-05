# AlphaGenome × SpliceVarDB BRCA1 Integration Proof

A reproducible research-engineering integration proving that **SpliceVarDB** experimental splicing data and **AlphaGenome** AI predictions can meet on a single *BRCA1* variant using local Python scripts.

---

## Final Integration Summary

- **Target Variant:** `NM_007294.4:c.4986+1G>T` (GRCh38 `chr17:43070927:C>A`)
- **Biological Location:** Canonical splice donor site at the *BRCA1* exon 16 / intron 16 boundary.
- **SpliceVarDB Experimental Ground Truth:** **`Splice-altering`** (Score `3`).
- **AlphaGenome Live Prediction:**
  - Donor site probability on the minus strand collapses from **`0.9961` (Reference)** down to **`0.0004` (Alternate)**.
  - **Max Delta Splice Sites:** `0.9957` (near-complete disruption).
  - **Max Delta Splice Site Usage:** `0.9090` across 734 tissue tracks.
  - **Max Delta Splice Junctions:** `1.9608` across 367 tissue tracks.
  - **Combined Splicing Score:** `2.2969` (Strong disruption).

---

## Quickstart (Clean Environment)

### 1. Prerequisites
- Python 3.11 or 3.12 (macOS / Linux / Windows)
- AlphaGenome API Key (free for research at [Google DeepMind AlphaGenome Terms](https://deepmind.google.com/science/alphagenome/account/terms))

### 2. Setup Virtual Environment
```bash
# Clone or navigate to repository
cd /path/to/AlphaGenome_WomenInAI

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install pinned dependencies
pip install -r requirements.txt
```

### 3. Configure API Key
Set your AlphaGenome API key using either:
```bash
# Method A: Local .env file (recommended, ignored by git)
echo "ALPHAGENOME_API_KEY=your_alphagenome_api_key_here" > .env

# Method B: Export in your active terminal shell
export ALPHAGENOME_API_KEY="your_alphagenome_api_key_here"
```

---

## Running the Pipeline

### Step 1: Extract SpliceVarDB Data for BRCA1
```bash
python fetch_splicevardb.py
```
**What this does:**
- Downloads or loads cached SpliceVarDB variant tracks from the UCSC Genome Browser API for the *BRCA1* locus (`chr17:43,044,295-43,170,245`, GRCh38).
- Parses genomic positions, HGVS annotations, and standardized splicing labels.
- Evaluates the primary test case (`c.4986_4986+1insT` / `rs1555580601`) and fallbacks.
- Outputs `brca1_variants.csv` (475 variants).

### Step 2: Predict Splicing Effects with AlphaGenome
```bash
# Live prediction (default 100KB context, ~15s execution):
python predict_alphagenome.py

# Live prediction with full 1MB context window (~2.5 min execution):
python predict_alphagenome.py --context 1MB

# Live prediction passing key directly:
python predict_alphagenome.py --api-key "your_api_key_here"

# Offline test using synthetic mock placeholder:
python predict_alphagenome.py --mock
```
**What this does:**
- Constructs the target variant (`NM_007294.4:c.4986+1G>T`, `chr17:43070927:C>A` GRCh38) and extracts a genomic context interval.
- Submits the variant to DeepMind's AlphaGenome API requesting splicing modalities:
  1. `SPLICE_SITES`
  2. `SPLICE_SITE_USAGE`
  3. `SPLICE_JUNCTIONS`
- Writes full structured results to `sample_prediction.json` (or `sample_prediction.mock.json`).

---

## Test Case & Variant Documentation

### Primary Test Variant: `BRCA1 c.4986_4986+1insT` (`rs1555580601`)
- **Status in SpliceVarDB:** **Absent**.
- **Evidence:** The SpliceVarDB track hosted on UCSC contains 475 *BRCA1* records, 472 of which are single nucleotide variants (SNVs) and 3 are delins indels. The specific insertion `c.4986_4986+1insT` was not curated in the source datasets compiled by SpliceVarDB.

### Selected Fallback Variant: `NM_007294.4:c.4986+1G>T`
- **Location:** Exon 16 / Intron 16 boundary (+1 canonical splice donor site).
- **Genomic Position (GRCh38):** `chr17:43070927`
- **Genomic Alleles:** Reference `C`, Alternate `A` (genomic plus strand; reverse complement of cDNA `G>T` on minus strand).
- **SpliceVarDB Label:** **`Splice-altering`** (Score `3`).
- **Justification for Fallback:** Directly tests the exact same canonical splice donor junction targeted by the primary test case, carrying definitive experimental confirmation of splicing disruption.

---

## What Worked & What Did Not

### ✅ What Worked
1. **SpliceVarDB Access via UCSC Genome Browser API:** Zero authentication friction, fast programmatic retrieval of all 475 *BRCA1* variants with genomic coordinates, HGVS IDs, and experimental spliceogenicity scores.
2. **Official AlphaGenome Python Client:** `alphagenome` v0.10.0 installed cleanly via PyPI with full support for `predict_variant`, sequence context windows (`100KB` and `1MB`), and native splicing output modalities (`SPLICE_SITES`, `SPLICE_SITE_USAGE`, `SPLICE_JUNCTIONS`).
3. **Genomic Coordinate Harmonization:** Direct alignment on GRCh38 (1-based coordinate `chr17:43070927`), bridging cDNA/HGVS transcript notations to genomic references.
4. **Live Model Execution:** AlphaGenome returned live predictions confirming the dramatic collapse of the donor splice site (`0.9961` -> `0.0004`), aligning with SpliceVarDB.

### ⚠️ What Did Not Work / Blockers Overcome
1. **SpliceVarDB Direct REST API:** `https://compbio.ccia.org.au/splicevardb-api/variants/filter` returned `HTTP 401 Unauthorized ("Token is missing")` requiring account registration. This was resolved by routing through the UCSC Genome Browser API track (`track=spliceVarDb`).
2. **EvoEval Parquet Subset:** The Arc Institute `evoeval/splicevar` benchmark subset contained 4,119 human genes but 0 *BRCA1* variants.
3. **Primary Insertion Variant:** `c.4986_4986+1insT` is not in SpliceVarDB, successfully handled by selecting the documented fallback variant at the same donor splice site (`c.4986+1G>T`).

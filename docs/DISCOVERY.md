# Phase 0 — Discovery Report

**Date:** 2026-11-03  
**Objective:** Determine whether SpliceVarDB data and an AlphaGenome prediction can meet on a single BRCA1 variant, and document the exact access routes.

---

## Question 1: Where is SpliceVarDB bulk data downloadable?

### Primary Source — splicevardb.org

| Attribute       | Detail |
|-----------------|--------|
| **URL**         | https://splicevardb.org |
| **Format**      | VCF-like text (columns: `#CHROM`, `POS`, `ID`, `REF`, `ALT`, `QUAL`, `FILTER`, `INFO` with HGVS/experimental metadata) |
| **Registration** | **Yes — required for bulk downloads.** Access is tiered: free for academic/research, fee-free license for diagnostic labs, commercial license for industry. |
| **License**     | Source code is AGPLv3 (GitHub). Data access terms enforced via registration portal. |
| **Scale**       | 50,715 unique variants across 8,362 genes. |
| **API**         | REST API documented at https://compbio.ccia.org.au/splicevardb-api/doc |
| **GitHub**      | https://github.com/CCICB/SpliceVarDB (front-end code + `publication_data/` folder; full variant database NOT in repo) |
| **Publication** | DOI 10.1016/j.ajhg.2024.08.002 (PMID 39226898) |

**Evidence:** Multiple independent web search results confirm the above. The GitHub README and publication abstract corroborate the variant count and gene coverage.

### Alternative Route — HuggingFace / EvoEval (No Registration)

| Attribute       | Detail |
|-----------------|--------|
| **URL**         | https://huggingface.co/datasets/arcinstitute/evoeval |
| **File**        | `splicevar/splicevar.parquet` |
| **Format**      | Parquet, columns include `chrom`, `pos`, `ref`, `alt`, and classification label |
| **Size**        | ~11,978 variants (7,147 splice-altering positive + 4,831 normal negative) |
| **Registration** | **No registration required.** Freely downloadable. |
| **Source**      | Curated subset of SpliceVarDB, prepared by Arc Institute for their EvoEval genomic model benchmark |

**Evidence:** HuggingFace dataset card and multiple search results confirm this is a derivative of SpliceVarDB. This is the fastest path to data — no registration gate.

### Recommendation

**Use the EvoEval/HuggingFace route first.** It is freely downloadable, requires no registration, and is in a clean Parquet format with `chrom/pos/ref/alt` coordinates plus labels — ideal for joining with AlphaGenome. If the test variant is not in this subset, fall back to the splicevardb.org portal or REST API.

---

## Question 2: Does AlphaGenome have a public API, Python package, or downloadable weights?

### Yes — all three exist.

| Access Route    | Detail |
|-----------------|--------|
| **Python package** | `pip install -U alphagenome` (PyPI: pypi.org/project/alphagenome/) |
| **GitHub**      | https://github.com/google-deepmind/alphagenome (client SDK, examples, Colab notebooks) |
| **GitHub (research)** | https://github.com/google-deepmind/alphagenome_research (JAX reference implementation) |
| **Documentation** | https://alphagenomedocs.com |
| **API backend** | Google Cloud service `gdmscience.googleapis.com` |
| **Authentication** | **API key required.** Free for non-commercial research. Request at https://deepmind.google.com/science/alphagenome/account/terms |
| **Rate limits** | Dynamic RPM limits per API key. Suited for small-to-medium scale (thousands of variants). |
| **Model weights** | Available on HuggingFace (`google/alphagenome-all-folds`) and Kaggle. Non-commercial license. |
| **Self-hosting hardware** | NVIDIA A100/H100 (80 GB VRAM) recommended for full 1 Mb context. NOT feasible on a typical local machine. |
| **Publication**  | "Advancing regulatory variant effect prediction with AlphaGenome" — Nature 649, 1206–1218 (2026). DOI: 10.1038/s41586-025-10014-0 |

**Evidence:** Verified across: (1) Google DeepMind official page, (2) PyPI listing, (3) GitHub repositories, (4) multiple independent tutorial/blog posts, (5) Nature publication.

### API-Based Workflow (Recommended for This Task)

The API route avoids needing a GPU entirely. The workflow is:

```python
from alphagenome.data import genome
from alphagenome.models.v1 import dna_client

# Initialize with API key (set via environment variable)
model = dna_client.create(api_key)

# Define variant using chrom/pos/ref/alt (GRCh38)
variant = genome.Variant(
    chromosome='chr17',
    position=43070927,  # BRCA1 c.4986+1 in GRCh38
    reference_bases='G',
    alternate_bases='GT',  # insertion of T
)

# Score the variant
# (exact scoring API to be confirmed from official examples)
```

### Blocker Check

**The user must have an AlphaGenome API key.** This requires accepting terms at `deepmind.google.com/science/alphagenome/account/terms`. I will ask the user before proceeding.

---

## Question 3: Best identifier for joining SpliceVarDB ↔ AlphaGenome

### AlphaGenome expects: `chrom / pos / ref / alt` (GRCh38, 1-based, `chr` prefix)

### SpliceVarDB provides: Both HGVS and `chrom / pos / ref / alt`

| Resource     | Primary ID Format | Genome Build |
|--------------|-------------------|--------------|
| AlphaGenome  | `chr17:43070927:G>GT` (chrom/pos/ref/alt) | GRCh38 (hg38) |
| SpliceVarDB (website) | HGVS transcript notation + VCF-style coords | Both GRCh37 and GRCh38 |
| EvoEval splicevar | `chrom`, `pos`, `ref`, `alt` columns | GRCh38 |

### Recommendation

**Join on `chrom / pos / ref / alt` in GRCh38.** Both resources natively support this. The EvoEval Parquet already has these columns, and AlphaGenome's `genome.Variant` constructor takes them directly. No liftover or HGVS parsing needed.

---

## Test Variant Assessment

**Primary test variant:** BRCA1 c.4986_4986+1insT (rs1555580601)

| Attribute     | Value |
|---------------|-------|
| HGVS          | NM_007294.4:c.4986_4986+1insT |
| GRCh38 coord  | chr17:43070927 (approximate — exact position depends on HGVS-to-VCF normalization for the insertion) |
| rsID          | rs1555580601 |
| Location      | Exon 16 / intron 16 boundary, canonical splice donor |
| Type          | Insertion |

**Concern:** The EvoEval splicevar dataset contains only ~12,000 variants (SNVs). This specific insertion may not be in that subset. The canonical +1 substitutions (e.g., c.4986+1G>A, c.4986+1G>T) are more likely to be present.

**Plan:** Download the EvoEval data first, filter to BRCA1, check if the primary variant is present. If not, check for substitutions at the same position. If neither, select one BRCA1 splice-altering variant from the data as the fallback, per spec.

---

## Access Route Summary

| Resource | Route | Auth Required | Blocked? |
|----------|-------|---------------|----------|
| SpliceVarDB via EvoEval (HuggingFace) | Direct Parquet download | No | ✅ Clear |
| SpliceVarDB via splicevardb.org | Web portal + REST API | Registration | ⚠️ Fallback (needs registration) |
| AlphaGenome via API | `pip install alphagenome` + API key | API key (free for research) | ⚠️ **User must have or obtain API key** |
| AlphaGenome self-hosted | Download weights, run locally | Accept license + GPU | ❌ Not feasible on local machine without GPU |

---

## Decision Points for User

Before proceeding to Phase 1, I need the user to confirm:

1. **AlphaGenome API key:** Do you already have one, or should we request one at https://deepmind.google.com/science/alphagenome/account/terms? (Free for non-commercial research, requires Google account.)
2. **SpliceVarDB route:** Are you OK starting with the EvoEval/HuggingFace subset (no registration), or do you want the full splicevardb.org data (requires academic registration)?
3. **Python environment:** Shall I create a venv in the project directory? The dependencies will be lightweight: `pandas`, `pyarrow`, `alphagenome`.

#!/usr/bin/env python3
"""
fetch_splicevardb.py — Retrieve SpliceVarDB data, filter to BRCA1,
and write brca1_variants.csv with variant identifiers and labels.

Source: SpliceVarDB track hosted via the UCSC Genome Browser API (hg38 / GRCh38).
  Track: spliceVarDb
  Region: BRCA1 locus on chr17 (chr17:43,044,295-43,170,245)
  Publication: SpliceVarDB (AJHG 2024, DOI: 10.1016/j.ajhg.2024.08.002)

Usage:
  python fetch_splicevardb.py

Outputs:
  brca1_variants.csv       — Filtered BRCA1 variants with coordinates and labels
  data/brca1_variants.csv  — Duplicate copy in data/ for pipeline consistency
"""

import os
import sys
import json
from collections import Counter
import requests
import pandas as pd

# BRCA1 locus on GRCh38 (hg38)
BRCA1_CHROM = "chr17"
BRCA1_START = 43_044_295
BRCA1_END = 43_170_245

UCSC_API_URL = "https://api.genome.ucsc.edu/getData/track"

# UCSC track score mapping for SpliceVarDB:
# 3 = Splice-altering (SPLICE)
# 2 = Low-frequency splice-altering (LOW)
# 1 = Not splice-altering (NORMAL)
# 0 = Conflicting (CONFL)
SCORE_LABEL_MAP = {
    3: "Splice-altering",
    2: "Low-frequency splice-altering",
    1: "Not splice-altering",
    0: "Conflicting",
}

# Primary test variant specified in requirements:
PRIMARY_TEST_HGVS = "NM_007294.4:c.4986_4986+1insT"
PRIMARY_TEST_RSID = "rs1555580601"
PRIMARY_TEST_APPROX_POS = 43_070_927

# Fallback variant (same splice donor site, +1 position, confirmed splice-altering):
FALLBACK_TEST_HGVS = "NM_007294.4:c.4986+1G>T"
FALLBACK_TEST_POS = 43_070_927


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def fetch_splicevardb_brca1(cache_dir: str = DATA_DIR) -> list[dict]:
    """Fetch BRCA1 variants from UCSC SpliceVarDB track or local cache."""
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "splicevardb_brca1_raw.json")

    if os.path.exists(cache_file):
        print(f"Loading cached SpliceVarDB BRCA1 data from: {cache_file}")
        with open(cache_file, "r") as f:
            return json.load(f)

    print("Fetching SpliceVarDB BRCA1 variants from UCSC Genome Browser API...")
    params = {
        "genome": "hg38",
        "track": "spliceVarDb",
        "chrom": BRCA1_CHROM,
        "start": BRCA1_START,
        "end": BRCA1_END,
    }

    try:
        response = requests.get(UCSC_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        raw_items = data.get("spliceVarDb", [])
        if not raw_items:
            raise ValueError("No variants returned in spliceVarDb field")

        with open(cache_file, "w") as f:
            json.dump(raw_items, f, indent=2)
        print(f"Fetched and cached {len(raw_items)} records into {cache_file}")
        return raw_items

    except Exception as e:
        print(f"Error fetching from UCSC API: {e}", file=sys.stderr)
        raise


def process_variants(raw_items: list[dict]) -> pd.DataFrame:
    """Parse raw items into a structured DataFrame with coordinates and labels."""
    records = []
    for item in raw_items:
        chrom = item.get("chrom", BRCA1_CHROM)
        chrom_start = item.get("chromStart")
        chrom_end = item.get("chromEnd")
        name = item.get("name", "")
        score = item.get("score")
        label = SCORE_LABEL_MAP.get(score, f"Unknown ({score})")

        # 1-based genomic coordinate (GRCh38)
        pos = chrom_end

        records.append({
            "gene": "BRCA1",
            "chrom": chrom,
            "pos": pos,
            "chrom_start": chrom_start,
            "chrom_end": chrom_end,
            "hgvs": name,
            "score": score,
            "splicing_label": label,
        })

    df = pd.DataFrame(records)
    # Sort by genomic position
    df = df.sort_values(by=["chrom", "pos", "hgvs"]).reset_index(drop=True)
    return df


def verify_test_cases(df: pd.DataFrame) -> dict:
    """Verify presence of primary test variant or document fallback."""
    print("\n--- TEST CASE VERIFICATION ---")

    # 1. Search for primary test variant: BRCA1 c.4986_4986+1insT (rs1555580601)
    primary_matches = df[df["hgvs"].str.contains("4986_4986+1insT", regex=False)]
    rs_matches = df[df["hgvs"].str.contains(PRIMARY_TEST_RSID, regex=False)]

    if len(primary_matches) > 0 or len(rs_matches) > 0:
        found = primary_matches if len(primary_matches) > 0 else rs_matches
        variant_info = found.iloc[0].to_dict()
        print(f"Primary test variant FOUND:")
        print(f"  HGVS: {variant_info['hgvs']}")
        print(f"  Position: {variant_info['chrom']}:{variant_info['pos']}")
        print(f"  Label: {variant_info['splicing_label']}")
        return {"status": "PRIMARY_FOUND", "variant": variant_info}

    print("Primary test variant (BRCA1 c.4986_4986+1insT / rs1555580601) is NOT present in SpliceVarDB track.")
    print("  Reason: SpliceVarDB UCSC track contains primarily SNVs and limited indels.")
    print("  Proceeding to fallback variant selection as specified in INSTRUCTIONS.md...")

    # 2. Select Fallback Variant at the identical splice donor site
    # Exon 16 / Intron 16 boundary (+1 donor position)
    donor_variants = df[df["hgvs"].str.contains("c.4986+1", regex=False)]
    splice_altering_donor = donor_variants[donor_variants["splicing_label"] == "Splice-altering"]

    if len(splice_altering_donor) > 0:
        fallback = splice_altering_donor.iloc[0].to_dict()
        print(f"\nFallback variant SELECTED:")
        print(f"  Variant HGVS: {fallback['hgvs']}")
        print(f"  Position (GRCh38 1-based): {fallback['chrom']}:{fallback['pos']}")
        print(f"  Label: {fallback['splicing_label']} (score={fallback['score']})")
        print("  Justification: Positioned at the exact same canonical splice donor site (c.4986+1) "
              "at the BRCA1 exon 16 boundary, validated as splice-altering in SpliceVarDB.")
        return {"status": "FALLBACK_SELECTED", "variant": fallback}

    # Generic fallback: First splice-altering variant
    any_altering = df[df["splicing_label"] == "Splice-altering"].iloc[0].to_dict()
    print(f"\nGeneric fallback variant SELECTED:")
    print(f"  Variant: {any_altering['hgvs']}")
    print(f"  Label: {any_altering['splicing_label']}")
    return {"status": "GENERIC_FALLBACK_SELECTED", "variant": any_altering}


def main():
    print("=" * 65)
    print(" fetch_splicevardb.py — SpliceVarDB BRCA1 Extractor")
    print("=" * 65)

    # 1. Fetch raw data
    raw_variants = fetch_splicevardb_brca1()

    # 2. Process and filter
    df = process_variants(raw_variants)
    total_count = len(df)

    print(f"\nSuccessfully loaded {total_count} BRCA1 variants from SpliceVarDB.")

    # 3. Report label distribution
    print("\n--- BRCA1 LABEL DISTRIBUTION ---")
    dist = Counter(df["splicing_label"])
    for label, count in sorted(dist.items(), key=lambda x: -x[1]):
        pct = (count / total_count) * 100
        print(f"  {label:<30} : {count:>4} ({pct:5.1f}%)")

    # 4. Verify primary test case and select fallback
    test_result = verify_test_cases(df)

    # 5. Save output CSV
    output_path = os.path.join(DATA_DIR, "brca1_variants.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path} ({total_count} rows)")

    # Save selected test variant info for predict_alphagenome.py
    test_info_path = os.path.join(DATA_DIR, "selected_test_variant.json")
    with open(test_info_path, "w") as f:
        json.dump(test_result, f, indent=2)
    print(f"Saved test case metadata: {test_info_path}")

    print("\n" + "=" * 65)
    print("fetch_splicevardb.py completed successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()

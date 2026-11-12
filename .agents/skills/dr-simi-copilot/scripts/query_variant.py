#!/usr/bin/env python3
"""
query_variant.py — Helper script for Dr. Simi Copilot Skill.

Allows quick lookup of any BRCA1 variant against the SpliceVarDB benchmark
and AlphaGenome calibration tables.

Usage:
    python query_variant.py --hgvs "NM_007294.4:c.4986+1G>T"
    python query_variant.py --case case3_deep_intronic
"""

import sys
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
STAGED_CASES = BASE_DIR / "data" / "staged_cases.json"
INTERPRETED_DIR = BASE_DIR / "data" / "interpreted_cases"

def lookup_by_case_id(case_id: str):
    if not STAGED_CASES.exists():
        print(f"[ERROR] Staged cases file not found at {STAGED_CASES}")
        return
    with open(STAGED_CASES, "r") as f:
        cases = json.load(f)
    for c in cases:
        if c.get("case_id") == case_id:
            print_case_summary(c)
            return
    print(f"[WARN] Case '{case_id}' not found.")

def lookup_by_hgvs(hgvs: str):
    if not STAGED_CASES.exists():
        print(f"[ERROR] Staged cases file not found at {STAGED_CASES}")
        return
    with open(STAGED_CASES, "r") as f:
        cases = json.load(f)
    for c in cases:
        if c.get("genomic", {}).get("hgvs") == hgvs:
            print_case_summary(c)
            return
    print(f"[WARN] HGVS variant '{hgvs}' not found.")

def print_case_summary(case: dict):
    pt = case.get("patient_context", {})
    print("=" * 65)
    print(f" CLINICAL DECISION ASSISTANT: {case.get('title')}")
    print("=" * 65)
    print(f" Patient      : {pt.get('patient_name', 'Sarah Jenkins')} ({pt.get('patient_age', 39)}{pt.get('patient_gender', 'F')[0]}) — {pt.get('patient_id', '')}")
    print(f" Panel Test   : {pt.get('panel_name', 'HBOC-30 Multigene Panel')}")
    print(f" Clinical Role: {case.get('finding_role', 'Clinical Finding')}")
    print(f" Variant HGVS : {case.get('genomic', {}).get('hgvs')}")
    print(f" Genomic Coord: {case.get('genomic', {}).get('chrom')}:{case.get('genomic', {}).get('pos')} ({case.get('genomic', {}).get('ref')} > {case.get('genomic', {}).get('alt')})")
    print(f" SpliceVarDB  : {case.get('splicevardb', {}).get('classification')}")
    print(f" AlphaGenome  : Combined Score = {case.get('alphagenome', {}).get('combined_score')}")
    cal = case.get("calibration_bin", {})
    print(f" Calibration  : Bin {cal.get('bin_number')} of {cal.get('total_bins')} | PPV = {cal.get('ppv_percent')}% (95% CI: [{cal.get('ci_low_percent')}% - {cal.get('ci_high_percent')}%])")
    if case.get("plain_english_summary"):
        print(f"\n Executive Clinical Verdict:\n  {case.get('plain_english_summary')}")
    print("\n Top Literature Citations:")
    for lit in case.get("literature_references", []):
        print(f"  • {lit.get('citation')} ({lit.get('journal')})")
        print(f"    Takeaway: {lit.get('clinical_takeaway')}")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query BRCA1 clinical case data")
    parser.add_argument("--case", help="Case ID (e.g. case1_pathogenic, case2_benign, case3_deep_intronic)")
    parser.add_argument("--hgvs", help="HGVS string (e.g. NM_007294.4:c.4986+1G>T)")
    args = parser.parse_args()

    if args.case:
        lookup_by_case_id(args.case)
    elif args.hgvs:
        lookup_by_hgvs(args.hgvs)
    else:
        parser.print_help()

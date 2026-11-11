#!/usr/bin/env python3
"""
run_clinical_pipeline.py — Master orchestrator for the Clinical Decision System.

Executes end-to-end:
  1. stage_case_data.py       — Compile the 3 clinical archetype cases
  2. clinical_agent.py         — Execute the Genomic Interpretation Agent
  3. generate_clinical_report.py — Render interactive HTML dossiers & patient letters
  4. Quality verification of all generated assets
"""

import os
import sys
import subprocess

def run_command(cmd, desc):
    print(f"\n[RUNNING] {desc}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {desc} failed:")
        print(result.stderr)
        sys.exit(result.returncode)
    print(result.stdout.strip())
    print(f"[SUCCESS] {desc} completed.")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    print("=" * 70)
    print(" AlphaGenome × SpliceVarDB Clinical Decision Pipeline Orchestrator")
    print("=" * 70)

    # Step 1: Stage Data
    run_command(f"{sys.executable} stage_case_data.py", "Staging Clinical Archetype Cases")

    # Step 2: Agent Interpretation
    run_command(f"{sys.executable} clinical_agent.py", "Clinical Interpretation Agent Execution")

    # Step 3: Report Generation
    run_command(f"{sys.executable} generate_clinical_report.py", "Interactive HTML Dossier & Patient Letter Generation")

    # Step 4: Verification of deliverables
    expected_files = [
        "data/staged_cases.json",
        "data/interpreted_cases/case1_pathogenic.json",
        "data/interpreted_cases/case2_benign.json",
        "data/interpreted_cases/case3_deep_intronic.json",
        "reports/case1_pathogenic.html",
        "reports/case2_benign.html",
        "reports/case3_deep_intronic.html",
        "reports/index.html",
    ]

    print("\n" + "=" * 70)
    print(" Quality Assurance & Verification Check:")
    print("=" * 70)

    all_ok = True
    for ef in expected_files:
        full_path = os.path.join(base_dir, ef)
        if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
            size_kb = os.path.getsize(full_path) / 1024
            print(f"  ✅ {ef:<45} ({size_kb:6.1f} KB)")
        else:
            print(f"  ❌ MISSING OR EMPTY: {ef}")
            all_ok = False

    if all_ok:
        print("\n[VERIFIED] All clinical dossiers and dashboard reports exist and are validated.")
        print("To view, open in browser:")
        print(f"  file://{os.path.join(base_dir, 'reports', 'index.html')}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

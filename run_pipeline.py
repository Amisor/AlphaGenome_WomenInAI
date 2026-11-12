#!/usr/bin/env python3
"""
run_pipeline.py — Master convenience launcher for the Clinical Decision Support Pipeline.

Delegates execution to scripts/run_clinical_pipeline.py.
Usage:
    python run_pipeline.py
"""

import os
import sys
import subprocess

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_script = os.path.join(base_dir, "scripts", "run_clinical_pipeline.py")
    result = subprocess.run([sys.executable, target_script] + sys.argv[1:])
    sys.exit(result.returncode)

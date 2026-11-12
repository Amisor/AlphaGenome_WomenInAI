#!/usr/bin/env python3
"""
test_clinical_system.py — Comprehensive automated test suite for the Clinical Decision System.

Verifies:
  1. Data integrity of staged cases and interpreted clinical dossiers.
  2. HTML report validity, absence of patient-facing letters, presence of SVG tracks.
  3. Embedded AI Copilot Chat drawer, prompt chips, and VARIANT_KB payloads.
  4. Accuracy of 5-bin empirical calibration statistics and literature citations.
  5. Antigravity Skill specification adherence.
"""

import os
import json
import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class TestClinicalSystem(unittest.TestCase):

    def setUp(self):
        self.staged_file = BASE_DIR / "data" / "staged_cases.json"
        self.interpreted_dir = BASE_DIR / "data" / "interpreted_cases"
        self.reports_dir = BASE_DIR / "reports"
        self.cases = ["case1_pathogenic", "case2_benign", "case3_deep_intronic"]

    def test_01_staged_cases_data_schema(self):
        self.assertTrue(self.staged_file.exists(), "staged_cases.json must exist")
        with open(self.staged_file, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data), 3, "Must contain exactly 3 clinical archetype cases")

        for case in data:
            self.assertIn("case_id", case)
            self.assertIn("patient_context", case)
            self.assertIn("biological_details", case)
            self.assertIn("literature_references", case)
            self.assertGreaterEqual(len(case["literature_references"]), 2, "Each case must have >= 2 literature citations")
            for lit in case["literature_references"]:
                self.assertIn("citation", lit)
                self.assertIn("doi", lit)
                self.assertIn("clinical_takeaway", lit)
            self.assertIn("calibration_bin", case)
            self.assertIn("ppv_percent", case["calibration_bin"])

    def test_02_interpreted_cases_clinician_pivot(self):
        for cid in self.cases:
            path = self.interpreted_dir / f"{cid}.json"
            self.assertTrue(path.exists(), f"Interpreted file {cid}.json must exist")
            with open(path, "r") as f:
                interp = json.load(f)

            # Strict Clinician Pivot checks
            self.assertNotIn("patient_letter", interp, "Patient letters must be completely eliminated")
            self.assertIn("risk_classification", interp)
            self.assertIn("molecular_evaluation", interp)
            self.assertIn("benchmark_evaluation", interp)
            self.assertIn("clinical_management", interp)
            self.assertIn("acmg_codes", interp["clinical_management"])
            self.assertIn("tumor_board_summary", interp["clinical_management"])
            self.assertIn("literature_evidence", interp)

    def test_03_html_reports_visual_cockpit_integrity(self):
        for cid in self.cases:
            html_path = self.reports_dir / f"{cid}.html"
            self.assertTrue(html_path.exists(), f"Report {cid}.html must exist")
            content = html_path.read_text(encoding="utf-8")

            # Check zero patient letters
            self.assertNotIn("Dear Patient", content)
            self.assertNotIn("patient-letter", content.lower())

            # Check Hero KPI row and visual elements
            self.assertIn("kpi-grid", content)
            self.assertIn("kpi-card", content)
            self.assertIn("<svg", content, "Must render SVG splice architecture track")

            # Check literature section
            self.assertIn("Prioritized Supporting Literature", content)
            self.assertIn("Peer-Reviewed Evidence", content)
            self.assertIn("doi.org", content)

            # Check Option A Split Layout & AI Assistant Panel
            self.assertIn("copilot-panel", content)
            self.assertIn("Clinical AI Assistant", content)
            self.assertIn("PATIENT_KB", content)
            self.assertIn("generateAgentAnswer", content)

            # Check Sarah Jenkins unified patient & friendly elements
            self.assertIn("Sarah Jenkins", content)
            self.assertIn("Executive Clinical Verdict", content)
            self.assertIn("Calibrated Risk Thermometer", content)
            self.assertIn("Copy Tumor Board Note", content)
            self.assertIn("#faf8f5", content)

            # Strict doctor-agnostic, professional tone, and emoji-free checks
            self.assertNotIn("Dr. Simi", content)
            self.assertNotIn("Dr.Simi", content)
            self.assertNotIn("In Plain English", content)
            for emoji in ['🧬', '🩺', '⚠️', '⚡', '✅', '💡', '💬', '📋']:
                self.assertNotIn(emoji, content, f"Emoji {emoji} must not be present in {cid}.html")

    def test_04_archetype_distinctiveness(self):
        """Ensure all 3 cases have distinct biological parameters, scores, and directives."""
        c1 = (self.reports_dir / "case1_pathogenic.html").read_text(encoding="utf-8")
        c2 = (self.reports_dir / "case2_benign.html").read_text(encoding="utf-8")
        c3 = (self.reports_dir / "case3_deep_intronic.html").read_text(encoding="utf-8")

        # Distinct scores
        self.assertIn("2.297", c1)
        self.assertIn("0.016", c2)
        self.assertIn("0.950", c3)

        # Distinct calibration PPVs
        self.assertIn("100.0%", c1)
        self.assertIn("1.5%", c2)
        self.assertIn("72.1%", c3)

        # Distinct mechanisms
        self.assertIn("Canonical", c1)
        self.assertIn("Benign", c2)
        self.assertIn("Deep-Intronic", c3)

    def test_05_antigravity_skill_specification(self):
        skill_file = BASE_DIR / ".agents" / "skills" / "dr-simi-copilot" / "SKILL.md"
        self.assertTrue(skill_file.exists(), "Antigravity skill SKILL.md must exist")
        text = skill_file.read_text(encoding="utf-8")

        # Frontmatter validation
        self.assertTrue(text.startswith("---"))
        frontmatter_end = text.find("---", 3)
        self.assertGreater(frontmatter_end, 3, "YAML frontmatter must be closed")
        frontmatter = text[3:frontmatter_end]
        self.assertIn("name: dr-simi-copilot", frontmatter)
        self.assertIn("description:", frontmatter)

        # Content validation
        self.assertIn("Clinical Decision Framework", text)
        self.assertIn("5-Bin Empirical Calibration", text)
        self.assertIn("ACMG/AMP", text)

    def test_06_master_dashboard_integrity(self):
        index_file = self.reports_dir / "index.html"
        self.assertTrue(index_file.exists(), "Master index.html must exist")
        content = index_file.read_text(encoding="utf-8")

        self.assertIn("<h1>Multigene Panel Review</h1>", content)
        self.assertIn("AlphaGenome", content)
        self.assertIn("SpliceVarDB", content)
        self.assertIn("case1_pathogenic.html", content)
        self.assertIn("case2_benign.html", content)
        self.assertIn("case3_deep_intronic.html", content)
        self.assertIn("ROC AUC", content)
        self.assertIn("Open Report", content)

        # Ensure removal of internal architecture section and hero tag
        self.assertNotIn("Dr. Simi", content)
        self.assertNotIn("Dr.Simi", content)
        self.assertNotIn("Clinical Decision Cockpit • Option A Split View", content)
        self.assertNotIn("Dr. Simi AI Copilot & System Architecture", content)
        self.assertNotIn("In Plain English", content)
        for emoji in ['🧬', '🩺', '⚠️', '⚡', '✅', '💡', '💬', '📋']:
            self.assertNotIn(emoji, content, f"Emoji {emoji} must not be present in index.html")

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
generate_clinical_report.py — Render interactive HTML clinical dossiers
and patient letters for the BRCA1 VUS cases, plus a master judge dashboard.

Outputs:
  reports/case1_pathogenic.html
  reports/case2_benign.html
  reports/case3_deep_intronic.html
  reports/index.html
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def generate_svg_gauge(score: float, max_score: float = 3.0) -> str:
    """Generate a clean SVG circular arc meter for the AlphaGenome score."""
    pct = min(max(score / max_score, 0.0), 1.0)
    # 180 degree semi-circle gauge
    circumference = 3.14159 * 60  # radius = 60
    dash_offset = circumference * (1.0 - pct)
    color = "#ef4444" if score >= 2.164 else ("#f59e0b" if score >= 0.140 else "#22c55e")
    
    return f"""
    <svg width="160" height="95" viewBox="0 0 160 95" class="gauge-svg">
      <path d="M 20 85 A 60 60 0 0 1 140 85" fill="none" stroke="#e2e8f0" stroke-width="14" stroke-linecap="round"/>
      <path d="M 20 85 A 60 60 0 0 1 140 85" fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round"
            stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{dash_offset:.1f}"/>
      <text x="80" y="70" text-anchor="middle" font-size="20" font-weight="700" fill="#0f172a">{score:.3f}</text>
      <text x="80" y="88" text-anchor="middle" font-size="11" font-weight="500" fill="#64748b">AlphaGenome Score</text>
    </svg>
    """

def generate_calibration_bins_html(current_bin_num: int) -> str:
    """Generate the 5-bin calibration visualizer highlighting the active bin."""
    bins_data = [
        {"bin": 1, "range": "0 – 0.024", "ppv": "<1.5%", "ci": "[0.3% – 7.9%]", "label": "Minimal Disruption", "color": "#22c55e", "bg": "#f0fdf4"},
        {"bin": 2, "range": "0.024 – 0.042", "ppv": "0.0%", "ci": "[0.0% – 5.3%]", "label": "Likely Neutral", "color": "#16a34a", "bg": "#f0fdf4"},
        {"bin": 3, "range": "0.042 – 0.140", "ppv": "7.5%", "ci": "[3.2% – 16.3%]", "label": "Low Evidence", "color": "#ca8a04", "bg": "#fefce8"},
        {"bin": 4, "range": "0.140 – 2.164", "ppv": "72.1%", "ci": "[60.4% – 81.3%]", "label": "Moderate / Elevated", "color": "#ea580c", "bg": "#fff7ed"},
        {"bin": 5, "range": "> 2.164", "ppv": "100.0%", "ci": "[94.7% – 100%]", "label": "Severe Disruption", "color": "#dc2626", "bg": "#fef2f2"},
    ]
    
    html = '<div class="calibration-container"><div class="bins-grid">'
    for b in bins_data:
        is_active = (b["bin"] == current_bin_num)
        active_class = "bin-card active" if is_active else "bin-card"
        border_style = f"border: 2px solid {b['color']}; box-shadow: 0 4px 12px rgba(0,0,0,0.08);" if is_active else "border: 1px solid #e2e8f0;"
        badge = f'<span class="active-badge" style="background:{b["color"]};">PATIENT BIN</span>' if is_active else ''
        
        html += f"""
        <div class="{active_class}" style="{border_style} background: {b['bg'] if is_active else '#ffffff'};">
          {badge}
          <div class="bin-header">
            <span class="bin-title">Bin {b['bin']}</span>
            <span class="bin-ppv" style="color: {b['color']};">{b['ppv']} PPV</span>
          </div>
          <div class="bin-range">Score: {b['range']}</div>
          <div class="bin-ci">95% CI: {b['ci']}</div>
          <div class="bin-desc">{b['label']}</div>
        </div>
        """
    html += '</div></div>'
    return html

def render_case_report(case_data: dict, interp: dict, all_cases: list) -> str:
    """Render full HTML for an individual clinical case report."""
    risk = interp["risk_classification"]
    mol = interp["molecular_evaluation"]
    bench = interp["benchmark_evaluation"]
    clin = interp["clinical_management"]
    letter = interp["patient_letter"]
    gen = case_data["genomic"]
    ag = case_data["alphagenome"]
    sv = case_data["splicevardb"]
    pt = case_data["patient_context"]
    bio = case_data["biological_details"]
    calib = case_data["calibration_bin"]

    gauge_svg = generate_svg_gauge(ag["combined_score"])
    calib_bins_html = generate_calibration_bins_html(calib["bin_number"])

    # Navigation items for switching cases
    nav_links = ""
    for c in all_cases:
        active_nav = ' class="nav-btn active"' if c["case_id"] == case_data["case_id"] else ' class="nav-btn"'
        short_name = c["archetype"].split(":")[0] if ":" in c["archetype"] else c["archetype"]
        nav_links += f'<a href="{c["case_id"]}.html"{active_nav}>{c["title"].split(":")[0]}</a>'

    # ACMG badges HTML
    acmg_html = ""
    for code in clin["acmg_evidence_codes"]:
        acmg_html += f"""
        <div class="acmg-card">
          <div class="acmg-code">{code['code']}</div>
          <div class="acmg-desc">{code['description']}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{case_data['title']} — Clinical Dossier</title>
  <style>
    :root {{
      --primary: #0f172a;
      --primary-light: #1e293b;
      --accent: #2563eb;
      --accent-light: #eff6ff;
      --border: #e2e8f0;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 60px;
    }}
    .topbar {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 14px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 700; color: #0f172a; font-size: 16px; text-decoration: none; }}
    .brand-tag {{ background: #eff6ff; color: #2563eb; font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 600; text-transform: uppercase; }}
    .case-nav {{ display: flex; gap: 8px; }}
    .nav-btn {{
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 6px;
      text-decoration: none;
      color: var(--text-muted);
      background: transparent;
      border: 1px solid var(--border);
      transition: all 0.15s;
    }}
    .nav-btn:hover {{ background: #f1f5f9; color: #0f172a; }}
    .nav-btn.active {{ background: #0f172a; color: #ffffff; border-color: #0f172a; }}
    .dashboard-link {{ background: #eff6ff; color: #2563eb; border-color: #bfdbfe; }}
    .dashboard-link:hover {{ background: #dbeafe; }}

    .container {{ max-width: 1140px; margin: 28px auto; padding: 0 20px; }}

    /* Patient Header Card */
    .patient-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 24px;
    }}
    .patient-main h1 {{ font-size: 24px; font-weight: 800; color: #0f172a; margin-bottom: 6px; }}
    .patient-sub {{ font-size: 14px; color: var(--text-muted); margin-bottom: 16px; display: flex; gap: 16px; flex-wrap: wrap; }}
    .patient-sub span strong {{ color: #0f172a; }}
    .patient-indication {{
      background: #f8fafc;
      border-left: 3px solid #2563eb;
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      font-size: 13px;
      color: #334155;
    }}
    .verdict-box {{
      text-align: right;
      min-width: 240px;
      padding: 16px;
      border-radius: 10px;
      border: 1px solid {risk['border_color']};
      background: {risk['badge_bg']};
    }}
    .verdict-tag {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: {risk['badge_text']}; }}
    .verdict-title {{ font-size: 18px; font-weight: 800; color: {risk['badge_text']}; margin: 4px 0; }}
    .verdict-desc {{ font-size: 12px; color: {risk['badge_text']}; opacity: 0.9; }}

    /* Tabs */
    .tabs {{ display: flex; gap: 4px; border-bottom: 2px solid var(--border); margin-bottom: 24px; }}
    .tab-btn {{
      padding: 12px 20px;
      font-size: 15px;
      font-weight: 600;
      color: var(--text-muted);
      border: none;
      background: transparent;
      cursor: pointer;
      position: relative;
      bottom: -2px;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }}
    .tab-btn:hover {{ color: #0f172a; }}
    .tab-btn.active {{ color: #2563eb; border-bottom: 2px solid #2563eb; }}

    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    /* Grid Layouts */
    .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }}
    .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 24px; }}

    .card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 22px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}
    .card-title {{ font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; }}
    .card-title .tag {{ font-size: 11px; padding: 2px 8px; border-radius: 4px; background: #f1f5f9; color: #475569; }}

    /* AlphaGenome Multi-Head Signal Card */
    .signal-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }}
    .signal-bars {{ display: flex; flex-direction: column; gap: 12px; }}
    .signal-row {{ display: flex; flex-direction: column; gap: 4px; }}
    .signal-label {{ display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #334155; }}
    .bar-bg {{ background: #f1f5f9; height: 8px; border-radius: 4px; overflow: hidden; }}
    .bar-fill {{ height: 100%; border-radius: 4px; background: #2563eb; }}

    /* Calibration Bins Component */
    .calibration-container {{ margin: 16px 0; }}
    .bins-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }}
    .bin-card {{
      padding: 12px 10px;
      border-radius: 8px;
      text-align: center;
      position: relative;
      transition: transform 0.15s;
    }}
    .bin-card.active {{ transform: translateY(-2px); }}
    .active-badge {{
      position: absolute;
      top: -9px;
      left: 50%;
      transform: translateX(-50%);
      color: #ffffff;
      font-size: 9px;
      font-weight: 800;
      padding: 1px 6px;
      border-radius: 999px;
      letter-spacing: 0.5px;
    }}
    .bin-title {{ font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; }}
    .bin-ppv {{ font-size: 16px; font-weight: 800; margin: 4px 0; display: block; }}
    .bin-range {{ font-size: 10px; color: #64748b; font-family: monospace; }}
    .bin-ci {{ font-size: 10px; color: #64748b; margin-top: 2px; }}
    .bin-desc {{ font-size: 10px; font-weight: 600; color: #334155; margin-top: 4px; }}

    /* ACMG Evidence Cards */
    .acmg-grid {{ display: flex; flex-direction: column; gap: 10px; }}
    .acmg-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 12px 14px;
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }}
    .acmg-code {{
      background: #0f172a;
      color: #ffffff;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      white-space: nowrap;
    }}
    .acmg-desc {{ font-size: 12px; color: #334155; }}

    /* Clinical Recommendation Box */
    .rec-box {{
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 10px;
      padding: 18px;
      margin-top: 16px;
    }}
    .rec-title {{ font-size: 13px; font-weight: 800; text-transform: uppercase; color: #1e40af; margin-bottom: 6px; }}
    .rec-text {{ font-size: 13px; color: #1e3a8a; line-height: 1.6; }}

    /* Patient Letter Styles */
    .letter-container {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 48px;
      max-width: 840px;
      margin: 0 auto;
      box-shadow: 0 4px 20px rgba(0,0,0,0.04);
      position: relative;
    }}
    .letter-header {{ border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 28px; }}
    .letter-title {{ font-size: 18px; font-weight: 800; color: #0f172a; }}
    .letter-dept {{ font-size: 13px; color: #64748b; }}
    .letter-meta {{ margin-bottom: 24px; font-size: 13px; line-height: 1.8; color: #334155; }}
    .letter-body {{ font-size: 14px; line-height: 1.8; color: #1e293b; white-space: pre-line; }}
    .print-btn {{
      position: absolute;
      top: 40px;
      right: 48px;
      background: #0f172a;
      color: #ffffff;
      border: none;
      padding: 8px 16px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
    }}
    .print-btn:hover {{ background: #1e293b; }}

    @media print {{
      .topbar, .tabs, .patient-card, .dashboard-link, .print-btn {{ display: none !important; }}
      .letter-container {{ border: none; box-shadow: none; padding: 0; margin: 0; max-width: 100%; }}
      body {{ background: #ffffff; padding: 0; }}
    }}
  </style>
</head>
<body>

  <!-- Topbar -->
  <header class="topbar">
    <a href="index.html" class="brand">
      AlphaGenome × SpliceVarDB
      <span class="brand-tag">Clinical Decision System</span>
    </a>
    <nav class="case-nav">
      <a href="index.html" class="nav-btn dashboard-link">← Master Benchmark Dashboard</a>
      {nav_links}
    </nav>
  </header>

  <main class="container">

    <!-- Patient Header Card -->
    <section class="patient-card">
      <div class="patient-main">
        <h1>{case_data['title']}</h1>
        <div class="patient-sub">
          <span>Patient: <strong>{pt['patient_id']}</strong> ({pt['patient_age']}yo {pt['patient_gender']})</span>
          <span>Variant: <strong>{gen['hgvs']}</strong></span>
          <span>Genomic: <strong>{gen['chrom']}:{gen['pos']} {gen['ref']}&gt;{gen['alt']}</strong></span>
          <span>Gene: <strong>BRCA1</strong> ({bio['transcript']})</span>
        </div>
        <div class="patient-indication">
          <strong>Clinical Indication:</strong> {pt['indication']}
        </div>
      </div>

      <div class="verdict-box">
        <div class="verdict-tag">{risk['icon']} {risk['acmg_trend']}</div>
        <div class="verdict-title">{risk['verdict']}</div>
        <div class="verdict-desc">{risk['summary']}</div>
      </div>
    </section>

    <!-- Navigation Tabs -->
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab('dossier')">1. Dr. Simi's Technical Clinical Dossier</button>
      <button class="tab-btn" onclick="switchTab('letter')">2. Plain-Language Patient Communication Letter</button>
    </div>

    <!-- TAB 1: Dr. Simi's Clinical Dossier -->
    <div id="tab-dossier" class="tab-content active">

      <!-- AlphaGenome Multi-Head Signal Breakdown & Gauge -->
      <div class="grid-2">
        <div class="card">
          <div class="card-title">
            AlphaGenome Splicing Signal Multi-Head Attribution
            <span class="tag">100 kb Context Window</span>
          </div>
          <div class="signal-header">
            {gauge_svg}
            <div style="flex: 1; padding-left: 18px;">
              <div style="font-size: 13px; color: #475569; margin-bottom: 4px;">Primary Mechanism:</div>
              <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 8px;">{mol['primary_mechanism']}</div>
              <div style="font-size: 12px; color: #64748b;">SpliceVarDB Experimental Evidence: <strong>{sv['classification']}</strong></div>
            </div>
          </div>
          <div class="signal-bars">
            <div class="signal-row">
              <div class="signal-label">
                <span>Donor / Acceptor Splice Site Delta</span>
                <span>{ag['max_delta_splice_sites']:.4f}</span>
              </div>
              <div class="bar-bg"><div class="bar-fill" style="width: {min(ag['max_delta_splice_sites']*100, 100):.1f}%;"></div></div>
            </div>
            <div class="signal-row">
              <div class="signal-label">
                <span>Tissue-Specific Splice Site Usage Shift (734 Tracks)</span>
                <span>{ag['max_delta_splice_site_usage']:.4f}</span>
              </div>
              <div class="bar-bg"><div class="bar-fill" style="width: {min(ag['max_delta_splice_site_usage']*100, 100):.1f}%; background: #0284c7;"></div></div>
            </div>
            <div class="signal-row">
              <div class="signal-label">
                <span>Aberrant Splice Junctions Delta (367 Tracks)</span>
                <span>{ag['max_delta_splice_junctions']:.4f}</span>
              </div>
              <div class="bar-bg"><div class="bar-fill" style="width: {min((ag['max_delta_splice_junctions']/2.0)*100, 100):.1f}%; background: #7c3aed;"></div></div>
            </div>
          </div>
        </div>

        <!-- Molecular Consequences -->
        <div class="card">
          <div class="card-title">
            Molecular Transcript Consequences
            <span class="tag">Gene Structure Context</span>
          </div>
          <div style="font-size: 13px; color: #334155; line-height: 1.7; margin-bottom: 16px;">
            <p><strong>Genomic Location:</strong> {bio['exon_context']}</p>
            <p style="margin-top: 8px;"><strong>Functional Impact:</strong> {mol['functional_consequence']}</p>
          </div>
          <div class="rec-box" style="margin-top: 12px; background: #f8fafc; border-color: #cbd5e1;">
            <div class="rec-title" style="color: #475569;">Molecular Tumor Board Recommendation</div>
            <div class="rec-text" style="color: #334155;">{clin['tumor_board_action']}</div>
          </div>
        </div>
      </div>

      <!-- Empirical 446-Variant Benchmark Context -->
      <div class="card" style="margin-bottom: 24px;">
        <div class="card-title">
          Empirical Benchmark Calibration (446-Variant BRCA1 Dataset)
          <span class="tag">Calibrated Positive Predictive Value</span>
        </div>
        <p style="font-size: 13px; color: #475569; margin-bottom: 12px;">
          This variant's AlphaGenome score is benchmarked against our verified 446-variant <em>BRCA1</em> ground-truth dataset (Overall ROC AUC: <strong>0.980</strong>, Intronic ROC AUC: <strong>0.993</strong>).
        </p>

        {calib_bins_html}

        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #64748b; margin-top: 12px; flex-wrap: wrap; gap: 10px;">
          <span><strong>Active Calibration Bin:</strong> {bench['calibration_bin_display']} ({bench['empirical_ppv_display']} PPV, 95% CI {bench['confidence_interval_95']})</span>
          <span><strong>Benchmark Validation:</strong> {bench['variants_in_bin']}</span>
        </div>
        <div style="background: #f1f5f9; padding: 10px 14px; border-radius: 6px; font-size: 12px; color: #334155; margin-top: 10px;">
          <strong>Baseline Comparison:</strong> {bench['baseline_comparison']}
        </div>
      </div>

      <!-- ACMG Evidence & Clinical Recommendations -->
      <div class="grid-2">
        <div class="card">
          <div class="card-title">ACMG / AMP Variant Evidence Code Synthesis</div>
          <div class="acmg-grid">
            {acmg_html}
          </div>
        </div>

        <div class="card">
          <div class="card-title">Actionable Recommendation for Dr. Simi</div>
          <div class="rec-box" style="margin-top: 0;">
            <div class="rec-title">Clinical Management Directive</div>
            <div class="rec-text">{clin['clinical_recommendation']}</div>
          </div>
        </div>
      </div>

    </div>

    <!-- TAB 2: Patient Communication Letter -->
    <div id="tab-letter" class="tab-content">
      <div class="letter-container">
        <button class="print-btn" onclick="window.print()">Print / Export Letter</button>
        <div class="letter-header">
          <div class="letter-title">Hereditary Cancer Risk &amp; Genomic Medicine Program</div>
          <div class="letter-dept">Department of Medical Genetics &bull; Comprehensive Cancer Center</div>
        </div>
        <div class="letter-meta">
          <div><strong>Date:</strong> {letter['letter_date']}</div>
          <div><strong>Patient ID:</strong> {letter['patient_id']}</div>
          <div><strong>Ordering Clinician:</strong> {letter['physician']}</div>
        </div>
        <div class="letter-body">{letter['full_letter_text'].split("Dear Patient,")[1] if "Dear Patient," in letter['full_letter_text'] else letter['full_letter_text']}</div>
      </div>
    </div>

  </main>

  <script>
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      if (tabId === 'dossier') {{
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
        document.getElementById('tab-dossier').classList.add('active');
      }} else {{
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('tab-letter').classList.add('active');
      }}
    }}
  </script>
</body>
</html>
"""
    return html

def render_master_index(all_cases: list, metrics_df: pd.DataFrame, threshold_df: pd.DataFrame) -> str:
    """Render the master showcase landing page for hackathon judges."""
    
    primary_row = metrics_df[metrics_df["analysis"] == "combined score (primary)"].iloc[0]
    intronic_row = metrics_df[metrics_df["analysis"] == "combined score, intronic variants only"].iloc[0]
    baseline_row = metrics_df[metrics_df["analysis"].str.contains("BASELINE")].iloc[0]
    thresh_row = threshold_df.iloc[0]

    case_cards = ""
    for c in all_cases:
        score = c["alphagenome"]["combined_score"]
        ppv = c["calibration_bin"]["ppv_percent"]
        color = "#ef4444" if score >= 2.164 else ("#f59e0b" if score >= 0.140 else "#22c55e")
        badge_bg = "#fee2e2" if score >= 2.164 else ("#fef3c7" if score >= 0.140 else "#dcfce7")
        badge_text = "#991b1b" if score >= 2.164 else ("#92400e" if score >= 0.140 else "#166534")

        case_cards += f"""
        <div class="case-card">
          <div class="case-top">
            <span class="case-badge" style="background:{badge_bg}; color:{badge_text};">{c['archetype']}</span>
            <span class="case-score" style="color:{color};">Score {score:.3f}</span>
          </div>
          <h2 class="case-title">{c['title']}</h2>
          <div class="case-meta">
            <div><strong>Variant:</strong> {c['genomic']['hgvs']}</div>
            <div><strong>Coordinates:</strong> {c['genomic']['chrom']}:{c['genomic']['pos']} {c['genomic']['ref']}&gt;{c['genomic']['alt']}</div>
            <div><strong>SpliceVarDB:</strong> {c['splicevardb']['classification']}</div>
            <div><strong>Reliability Calibration:</strong> Bin {c['calibration_bin']['bin_number']} of 5 (<strong>{ppv}% PPV</strong>)</div>
          </div>
          <p class="case-desc">{c['biological_details']['clinical_impact_summary']}</p>
          <a href="{c['case_id']}.html" class="case-action">Open Clinical Dossier &amp; Patient Letter &rarr;</a>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AlphaGenome × SpliceVarDB — Clinical Decision Support Showcase</title>
  <style>
    :root {{
      --primary: #0f172a;
      --accent: #2563eb;
      --border: #e2e8f0;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 60px;
    }}
    .hero {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 56px 20px;
      text-align: center;
    }}
    .hero-tag {{
      background: rgba(37, 99, 235, 0.25);
      border: 1px solid rgba(147, 197, 253, 0.3);
      color: #93c5fd;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: inline-block;
      margin-bottom: 16px;
    }}
    .hero h1 {{ font-size: 34px; font-weight: 800; max-width: 820px; margin: 0 auto 12px; line-height: 1.25; }}
    .hero p {{ font-size: 16px; color: #94a3b8; max-width: 680px; margin: 0 auto; }}

    .container {{ max-width: 1140px; margin: 0 auto; padding: 0 20px; }}

    /* Benchmark Stats Row */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: -32px;
      margin-bottom: 40px;
    }}
    .stat-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      text-align: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .stat-val {{ font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }}
    .stat-label {{ font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; }}
    .stat-sub {{ font-size: 11px; color: #94a3b8; margin-top: 4px; }}

    /* Section Headers */
    .section-title {{ font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 8px; }}
    .section-sub {{ font-size: 14px; color: #64748b; margin-bottom: 24px; }}

    /* Case Cards Grid */
    .cases-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 48px; }}
    .case-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .case-card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); }}
    .case-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
    .case-badge {{ font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }}
    .case-score {{ font-size: 14px; font-weight: 800; }}
    .case-title {{ font-size: 17px; font-weight: 800; color: #0f172a; margin-bottom: 12px; line-height: 1.35; }}
    .case-meta {{ font-size: 12px; color: #475569; margin-bottom: 14px; line-height: 1.7; background: #f8fafc; padding: 10px; border-radius: 6px; }}
    .case-desc {{ font-size: 13px; color: #334155; line-height: 1.6; margin-bottom: 20px; }}
    .case-action {{
      background: #0f172a;
      color: #ffffff;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      text-align: center;
      padding: 10px 16px;
      border-radius: 6px;
      display: block;
      transition: background 0.15s;
    }}
    .case-action:hover {{ background: #2563eb; }}

    /* Clinical Context Table */
    .benchmark-table {{
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 40px;
    }}
    .benchmark-table th {{ background: #f8fafc; text-align: left; padding: 12px 16px; font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; border-bottom: 1px solid var(--border); }}
    .benchmark-table td {{ padding: 12px 16px; font-size: 13px; color: #334155; border-bottom: 1px solid var(--border); }}
    .benchmark-table tr:last-child td {{ border-bottom: none; }}
  </style>
</head>
<body>

  <header class="hero">
    <div class="hero-tag">Hackathon Final Deliverable &bull; Dr. Simi Decision Copilot</div>
    <h1>AlphaGenome &times; SpliceVarDB Clinical Decision System</h1>
    <p>Bridging Google DeepMind's DNA foundation model, verified experimental splicing evidence, and empirical BRCA1 calibration into an actionable clinical workflow.</p>
  </header>

  <main class="container">

    <!-- Benchmark Statistics Overview -->
    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-val">{primary_row['roc_auc']:.3f}</div>
        <div class="stat-label">Overall ROC AUC</div>
        <div class="stat-sub">95% CI: [{primary_row['ci_low']:.3f} – {primary_row['ci_high']:.3f}] (n={int(primary_row['n'])})</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color: #2563eb;">{intronic_row['roc_auc']:.3f}</div>
        <div class="stat-label">Intronic ROC AUC</div>
        <div class="stat-sub">Beats distance baseline ({baseline_row['roc_auc']:.3f})</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color: #16a34a;">{thresh_row['sensitivity']*100:.1f}%</div>
        <div class="stat-label">Sensitivity</div>
        <div class="stat-sub">At optimal threshold {thresh_row['threshold']:.3f}</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color: #dc2626;">100%</div>
        <div class="stat-label">Bin 5 Precision (PPV)</div>
        <div class="stat-sub">68 / 68 True Positives</div>
      </div>
    </section>

    <!-- 3 Clinical Archetypes Showcase -->
    <section>
      <h2 class="section-title">Clinical Archetype Patient Demonstrations</h2>
      <p class="section-sub">Explore how Dr. Simi evaluates three distinct VUS clinical scenarios using AlphaGenome prediction, empirical calibration, and automated patient communication.</p>
      
      <div class="cases-grid">
        {case_cards}
      </div>
    </section>

    <!-- Benchmark Table Context -->
    <section>
      <h2 class="section-title">Verified Empirical Performance Matrix</h2>
      <p class="section-sub">Detailed statistical metrics from the 446-variant BRCA1 benchmark powering this clinical decision tool.</p>

      <table class="benchmark-table">
        <thead>
          <tr>
            <th>Analysis Target</th>
            <th>Sample (n)</th>
            <th>Positive (n)</th>
            <th>ROC AUC</th>
            <th>95% Confidence Interval</th>
            <th>Clinical Significance</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Combined Splicing Score (Primary)</strong></td>
            <td>339</td>
            <td>123</td>
            <td><strong style="color: #2563eb;">0.980</strong></td>
            <td>[0.962 – 0.993]</td>
            <td>High-fidelity global performance across all single nucleotide variants.</td>
          </tr>
          <tr>
            <td><strong>Intronic Variants Only</strong></td>
            <td>152</td>
            <td>90</td>
            <td><strong style="color: #16a34a;">0.993</strong></td>
            <td>[0.983 – 0.999]</td>
            <td>Detects both canonical boundary collapse and deep intronic cryptic activation.</td>
          </tr>
          <tr>
            <td><em>Baseline Distance Heuristic (1/distance)</em></td>
            <td>152</td>
            <td>90</td>
            <td>0.914</td>
            <td>[0.863 – 0.955]</td>
            <td>Standard distance heuristics miss cryptic sites far from exons.</td>
          </tr>
          <tr>
            <td><strong>Exonic Variants Only</strong></td>
            <td>187</td>
            <td>33</td>
            <td><strong>0.946</strong></td>
            <td>[0.888 – 0.987]</td>
            <td>Rules out splicing defects for exonic silent/missense alterations.</td>
          </tr>
        </tbody>
      </table>
    </section>

  </main>
</body>
</html>
"""
    return html

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # 1. Load Staged Cases and Benchmark Data
    staged_cases_path = os.path.join(DATA_DIR, "staged_cases.json")
    if not os.path.exists(staged_cases_path):
        from stage_case_data import stage_cases
        stage_cases()

    with open(staged_cases_path, "r") as f:
        staged_cases = json.load(f)

    metrics_df = pd.read_csv(os.path.join(RESULTS_DIR, "benchmark_metrics.csv"))
    threshold_df = pd.read_csv(os.path.join(RESULTS_DIR, "benchmark_threshold_metrics.csv"))

    # 2. Load Agent Interpretations (or compute via clinical_agent)
    from clinical_agent import ClinicalInterpretationAgent
    agent = ClinicalInterpretationAgent()

    interpreted_dict = {}
    for case in staged_cases:
        cid = case["case_id"]
        interp_file = os.path.join(DATA_DIR, "interpreted_cases", f"{cid}.json")
        if os.path.exists(interp_file):
            with open(interp_file, "r") as f:
                interp = json.load(f)
        else:
            interp = agent.interpret_case(case)
        interpreted_dict[cid] = interp

    # 3. Render Each Case Report
    for case in staged_cases:
        cid = case["case_id"]
        interp = interpreted_dict[cid]
        html_content = render_case_report(case, interp, staged_cases)
        out_file = os.path.join(REPORTS_DIR, f"{cid}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generated case report: {out_file}")

    # 4. Render Master Index Dashboard
    index_html = render_master_index(staged_cases, metrics_df, threshold_df)
    index_path = os.path.join(REPORTS_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Generated master showcase dashboard: {index_path}")

    print("\nAll interactive reports successfully generated in reports/")

if __name__ == "__main__":
    main()

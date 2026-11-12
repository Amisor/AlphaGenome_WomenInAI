#!/usr/bin/env python3
"""
generate_clinical_report.py — Render interactive visual clinical reports
with Option A: Split View (Live AI Assistant side-by-side) for Multigene Panel Review,
styled in a warm editorial off-white palette.

Clean & Professional Guidelines:
  - Agnostic of specific doctor names (zero "Dr. Simi")
  - Professional editorial tone (zero "In Plain English", zero informal phrases)
  - Zero emojis (clean text monograms, medical tags, and crisp typography)
  - Terminology: "Report" instead of "Cockpit"
  - Clear navigation with "Open Report" buttons
  - Excludes internal system architecture sections from the clinical presentation
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def generate_risk_thermometer(active_bin: int) -> str:
    """Generate visual 5-segment risk thermometer with active pin indicator."""
    bins_meta = [
        {"num": 1, "label": "Tier 1: Minimal", "ppv": "<1.5% PPV", "color": "#15803d", "bg": "#dcfce7"},
        {"num": 2, "label": "Tier 2: Low", "ppv": "8.8% PPV", "color": "#16a34a", "bg": "#f0fdf4"},
        {"num": 3, "label": "Tier 3: Indeterminate", "ppv": "39.7% PPV", "color": "#ca8a04", "bg": "#fef9c3"},
        {"num": 4, "label": "Tier 4: High", "ppv": "72.1% PPV", "color": "#ea580c", "bg": "#ffedd5"},
        {"num": 5, "label": "Tier 5: Definitive", "ppv": "100% PPV", "color": "#b91c1c", "bg": "#fee2e2"},
    ]
    
    segments_html = ""
    for b in bins_meta:
        is_active = (b["num"] == active_bin)
        border_style = f"2px solid {b['color']}" if is_active else "1px solid #e7e5e4"
        indicator = f"""<div style="position:absolute; top:-22px; left:50%; transform:translateX(-50%); background:{b['color']}; color:#ffffff; font-size:10px; font-weight:800; padding:2px 6px; border-radius:4px; white-space:nowrap; box-shadow:0 2px 4px rgba(0,0,0,0.15);">ACTIVE VARIANT</div>""" if is_active else ""
        font_weight = "800" if is_active else "600"
        scale = "transform: scale(1.02); z-index:2;" if is_active else ""
        
        segments_html += f"""
        <div style="flex:1; background:{b['bg']}; border:{border_style}; border-radius:6px; padding:8px 4px; text-align:center; position:relative; {scale}">
          {indicator}
          <div style="font-size:11px; font-weight:{font_weight}; color:{b['color']};">{b['label']}</div>
          <div style="font-size:12px; font-weight:800; color:{b['color']}; margin-top:2px;">{b['ppv']}</div>
        </div>
        """

    return f"""
    <div style="margin: 22px 0 16px 0;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span style="font-size:11px; font-weight:700; color:#78716c; text-transform:uppercase; letter-spacing:0.5px;">Calibrated Risk Thermometer (446 BRCA1 Benchmark)</span>
        <span style="font-size:11px; color:#a8a29e;">Empirical Positive Predictive Value (PPV)</span>
      </div>
      <div style="display:flex; gap:6px; align-items:stretch;">
        {segments_html}
      </div>
    </div>
    """

def generate_svg_splicing_diagram(case_id: str, ag_score: float, delta_sites: float, intron_offset: float = None) -> str:
    """Generate custom SVG biological splicing diagram in warm editorial palette."""
    if case_id == "case1_pathogenic":
        # Canonical donor destruction
        return f"""
        <svg viewBox="0 0 540 120" class="bio-diagram-svg">
          <!-- Exon 15 -->
          <rect x="20" y="30" width="160" height="50" rx="6" fill="#292524"/>
          <text x="100" y="60" fill="#fafaf9" font-size="13" font-weight="700" text-anchor="middle">Exon 15 (Coding)</text>
          
          <!-- Canonical Splice Boundary -->
          <line x1="180" y1="15" x2="180" y2="95" stroke="#dc2626" stroke-width="2" stroke-dasharray="4"/>
          
          <!-- Intron 15 -->
          <rect x="180" y="45" width="340" height="20" fill="#e7e5e4"/>
          <text x="350" y="59" fill="#78716c" font-size="11" font-weight="600" text-anchor="middle">Intron 15 (Pre-mRNA)</text>
          
          <!-- Invariant +1 Marker -->
          <circle cx="186" cy="55" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
          <text x="186" y="59" fill="#991b1b" font-size="11" font-weight="800" text-anchor="middle">+1</text>
          
          <!-- Signal Callout -->
          <rect x="220" y="10" width="290" height="26" rx="4" fill="#fef2f2" stroke="#fecaca"/>
          <text x="365" y="27" fill="#991b1b" font-size="11" font-weight="700" text-anchor="middle">
            Donor Collapse: 0.9961 &rarr; 0.0004 (&Delta; {delta_sites:.4f})
          </text>
          
          <!-- Resulting Failure Arrow -->
          <text x="210" y="102" fill="#b91c1c" font-size="11" font-weight="700">Spliceosome recognition abolished &rarr; Full Exon Skipping &amp; Frameshift</text>
        </svg>
        """
    elif case_id == "case3_deep_intronic":
        # Deep intronic cryptic donor activation
        return f"""
        <svg viewBox="0 0 540 120" class="bio-diagram-svg">
          <!-- Exon 10 -->
          <rect x="20" y="30" width="110" height="50" rx="6" fill="#292524"/>
          <text x="75" y="60" fill="#fafaf9" font-size="12" font-weight="700" text-anchor="middle">Exon 10</text>
          
          <!-- Deep Intron Bridge -->
          <rect x="130" y="45" width="220" height="20" fill="#e7e5e4"/>
          <text x="240" y="59" fill="#78716c" font-size="11" font-weight="600" text-anchor="middle">Intron 10 (4,105 bp span)</text>
          
          <!-- Cryptic Pseudoexon Site -->
          <rect x="350" y="30" width="100" height="50" rx="6" fill="#fef3c7" stroke="#d97706" stroke-width="2" stroke-dasharray="3"/>
          <text x="400" y="53" fill="#92400e" font-size="11" font-weight="800" text-anchor="middle">Aberrant</text>
          <text x="400" y="67" fill="#92400e" font-size="11" font-weight="800" text-anchor="middle">Pseudoexon</text>
          
          <!-- Next Intron segment -->
          <rect x="450" y="45" width="70" height="20" fill="#e7e5e4"/>
          
          <!-- Cryptic Activation Marker -->
          <circle cx="350" cy="55" r="14" fill="#d97706" stroke="#ffffff" stroke-width="2"/>
          <text x="350" y="59" fill="#ffffff" font-size="10" font-weight="800" text-anchor="middle">5'</text>
          
          <!-- Signal Callout -->
          <rect x="160" y="10" width="340" height="24" rx="4" fill="#fffbeb" stroke="#fde68a"/>
          <text x="330" y="26" fill="#92400e" font-size="11" font-weight="700" text-anchor="middle">
            De Novo Cryptic Donor Created (&Delta; {delta_sites:.4f}) at offset +4,105 bp
          </text>
          
          <text x="270" y="102" fill="#d97706" font-size="11" font-weight="700" text-anchor="middle">
            Standard proximity tools score 0.0002 &bull; AlphaGenome captures 100 kb sequence context
          </text>
        </svg>
        """
    else:
        # Benign exonic neutral
        return f"""
        <svg viewBox="0 0 540 120" class="bio-diagram-svg">
          <!-- Exon 10 with internal mutation -->
          <rect x="20" y="30" width="280" height="50" rx="6" fill="#292524"/>
          <text x="120" y="60" fill="#fafaf9" font-size="13" font-weight="700" text-anchor="middle">Exon 10 (Internal Coding Region)</text>
          
          <!-- Mutation Pin inside exon -->
          <circle cx="230" cy="55" r="12" fill="#15803d" stroke="#ffffff" stroke-width="2"/>
          <text x="230" y="59" fill="#ffffff" font-size="9" font-weight="800" text-anchor="middle">SNV</text>
          
          <!-- Intron 10 -->
          <rect x="300" y="45" width="220" height="20" fill="#e7e5e4"/>
          <text x="410" y="59" fill="#78716c" font-size="11" font-weight="600" text-anchor="middle">Intron 10 (Normal Splicing)</text>
          
          <!-- Stable Junction Marker -->
          <line x1="300" y1="20" x2="300" y2="90" stroke="#15803d" stroke-width="2"/>
          <text x="305" y="26" fill="#15803d" font-size="10" font-weight="700">Canonical Donor Unaltered</text>
          
          <rect x="60" y="90" width="380" height="24" rx="4" fill="#f0fdf4" stroke="#bbf7d0"/>
          <text x="250" y="106" fill="#166534" font-size="11" font-weight="700" text-anchor="middle">
            Splice site affinity delta: 0.0059 (Neutral) &bull; Normal transcript preserved
          </text>
        </svg>
        """

def render_case_report(case_data: dict, interp: dict, all_cases: list) -> str:
    """Render the clinical report using Option A: Split View and warm off-white palette."""
    cid = case_data["case_id"]
    pt = case_data["patient_context"]
    gen = case_data["genomic"]
    ag = case_data["alphagenome"]
    sv = case_data["splicevardb"]
    calib = case_data["calibration_bin"]
    risk = interp["risk_classification"]
    mol = interp["molecular_evaluation"]
    bench = interp["benchmark_evaluation"]
    clin = interp["clinical_management"]
    lit = case_data.get("literature_references", [])
    finding_num = case_data.get("finding_number", 1)
    finding_role = case_data.get("finding_role", "Clinical Finding")

    # Generate visual SVG diagram and risk thermometer
    svg_diagram = generate_svg_splicing_diagram(
        cid,
        ag["combined_score"],
        ag["max_delta_splice_sites"],
        gen.get("intron_offset")
    )
    risk_thermometer_html = generate_risk_thermometer(calib["bin_number"])

    # Literature Cards
    lit_cards_html = ""
    for paper in lit:
        pmid_badge = f'<span class="lit-pmid">PMID: {paper["pmid"]}</span>' if paper.get("pmid") else ""
        doi_link = f'https://doi.org/{paper["doi"]}' if paper.get("doi") else "#"
        lit_cards_html += f"""
        <div class="lit-card">
          <div class="lit-top">
            <span class="lit-tier">{paper['evidence_tier']}</span>
            <div style="display:flex; gap:6px; align-items:center;">
              {pmid_badge}
              <a href="{doi_link}" target="_blank" rel="noopener noreferrer" class="lit-doi-link">View Study &rarr;</a>
            </div>
          </div>
          <div class="lit-citation">{paper['citation']} <em>{paper['journal']}</em> ({paper['year']}).</div>
          <div class="lit-takeaway"><strong>Key Finding:</strong> {paper['clinical_takeaway']}</div>
        </div>
        """

    # ACMG Criteria Cards
    acmg_html = ""
    for code in clin["acmg_codes"]:
        acmg_html += f"""
        <div class="acmg-card">
          <div class="acmg-code">{code['code']}</div>
          <div class="acmg-desc">{code['rule']}</div>
        </div>
        """

    # Build Multi-Finding Patient Knowledge Base (PATIENT_KB) for client-side chat
    patient_kb = {
        "patient_name": pt.get("patient_name", "Sarah Jenkins"),
        "patient_id": pt.get("patient_id", "PT-HBOC-3982"),
        "patient_age": pt.get("patient_age", 39),
        "indication": pt.get("indication", ""),
        "panel_name": pt.get("panel_name", "HBOC-30 Multigene Panel"),
        "active_case_id": cid,
        "active_finding_number": finding_num,
        "active_variant": gen["hgvs"],
        "findings": [
            {
                "case_id": c["case_id"],
                "finding_number": c.get("finding_number", i + 1),
                "role": c.get("finding_role", ""),
                "variant": c["genomic"]["hgvs"],
                "score": c["alphagenome"]["combined_score"],
                "bin": c["calibration_bin"]["bin_number"],
                "ppv": c["calibration_bin"]["ppv_percent"],
                "ci": f"[{c['calibration_bin']['ci_low_percent']}% – {c['calibration_bin']['ci_high_percent']}%]",
                "splicevardb": c["splicevardb"]["classification"],
                "plain_english": c.get("plain_english_summary", ""),
            }
            for i, c in enumerate(all_cases)
        ],
        "active_detail": {
            "variant": gen["hgvs"],
            "chrom_pos": f"{gen['chrom']}:{gen['pos']} {gen['ref']}>{gen['alt']}",
            "risk_verdict": risk["verdict"],
            "action_type": risk["action_type"],
            "score": ag["combined_score"],
            "bin": calib["bin_number"],
            "ppv": calib["ppv_percent"],
            "ci": f"[{calib['ci_low_percent']}% – {calib['ci_high_percent']}%]",
            "splicevardb_label": sv["classification"],
            "molecular_mechanism": mol["primary_mechanism"],
            "impact": mol["impact_details"],
            "acmg_codes": [f"{c['code']}: {c['rule']}" for c in clin["acmg_codes"]],
            "recommendation": clin["clinical_directive"],
            "tumor_board_summary": clin["tumor_board_summary"],
            "clipboard_note": interp.get("tumor_board_clipboard_note", ""),
            "literature": [f"{l['citation']} ({l['journal']}) — {l['clinical_takeaway']}" for l in lit],
        }
    }
    patient_kb_json = json.dumps(patient_kb)

    # Variant navigation switcher
    variant_switcher_html = ""
    for c in all_cases:
        is_cur = (c["case_id"] == cid)
        active_class = "switcher-btn active" if is_cur else "switcher-btn"
        badge_color = "#dc2626" if c["case_id"] == "case1_pathogenic" else ("#15803d" if c["case_id"] == "case2_benign" else "#d97706")
        variant_switcher_html += f"""
        <a href="{c['case_id']}.html" class="{active_class}">
          <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:{badge_color}; margin-right:6px;"></span>
          Finding #{c.get('finding_number', 1)}: {c['genomic']['hgvs'].split(':')[-1]}
          <span style="font-size:10px; color:#78716c; margin-left:4px;">({c.get('finding_role', '')})</span>
        </a>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{case_data['title']} — Clinical Decision Report</title>
  <style>
    :root {{
      --bg: #faf8f5;           /* Warm Alabaster / Off-White */
      --card-bg: #ffffff;      /* Pure warm card white */
      --border: #e7e5e4;       /* Soft warm stone border */
      --border-focus: #d6d3d1;
      --text: #1c1917;         /* Deep rich charcoal */
      --text-muted: #57534e;   /* Muted warm slate */
      --accent: #292524;       /* Primary dark stone */
      --accent-warm: #44403c;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 60px;
    }}

    /* Top Sticky Navigation Bar */
    .topbar {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 12px 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 90;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}
    .brand {{ display: flex; align-items: center; gap: 10px; font-weight: 700; color: #1c1917; font-size: 14px; text-decoration: none; }}
    .brand-tag {{ background: #f5f5f4; color: #44403c; font-size: 11px; padding: 2px 8px; border-radius: 999px; font-weight: 700; text-transform: uppercase; border: 1px solid #e7e5e4; }}
    .dashboard-link {{
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 6px;
      text-decoration: none;
      color: #44403c;
      background: #f5f5f4;
      border: 1px solid var(--border);
      transition: all 0.15s;
    }}
    .dashboard-link:hover {{ background: #e7e5e4; }}

    .container {{ max-width: 1360px; margin: 20px auto; padding: 0 20px; }}

    /* Patient Overview Hero Banner */
    .patient-hero {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 24px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}
    .patient-main {{ display: flex; align-items: center; gap: 16px; }}
    .patient-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #f5f5f4;
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 800;
      color: #44403c;
    }}
    .patient-name {{ font-size: 18px; font-weight: 800; color: #1c1917; }}
    .patient-sub {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}
    .patient-badges {{ display: flex; gap: 8px; align-items: center; }}
    .badge-pill {{
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      background: #f5f5f4;
      color: #44403c;
      border: 1px solid var(--border);
    }}

    /* 3-Variant Switcher Bar */
    .switcher-row {{
      display: flex;
      gap: 10px;
      margin-bottom: 20px;
      background: #f5f5f4;
      padding: 6px;
      border-radius: 10px;
      border: 1px solid var(--border);
    }}
    .switcher-btn {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 8px 12px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      color: #57534e;
      background: transparent;
      transition: all 0.15s;
    }}
    .switcher-btn:hover {{ background: #e7e5e4; color: #1c1917; }}
    .switcher-btn.active {{
      background: #ffffff;
      color: #1c1917;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }}

    /* Option A: Split View Layout */
    .split-layout {{
      display: grid;
      grid-template-columns: 1fr 440px;
      gap: 22px;
      align-items: start;
    }}

    /* Left Column (Clinical Dossier) */
    .cockpit-left {{ display: flex; flex-direction: column; gap: 20px; }}

    /* Executive Clinical Verdict Card */
    .plain-english-card {{
      background: #ffffff;
      border: 1px solid #fed7aa;
      border-left: 5px solid #ea580c;
      border-radius: 10px;
      padding: 16px 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }}
    .pe-label {{
      font-size: 11px;
      font-weight: 800;
      color: #9a3412;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }}
    .pe-text {{ font-size: 13.5px; color: #292524; line-height: 1.6; font-weight: 500; }}

    /* Hero KPI Row */
    .kpi-grid {{
      display: grid;
      grid-template-columns: 1.4fr 1fr 1fr 1fr;
      gap: 12px;
    }}
    .kpi-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .kpi-label {{ font-size: 10.5px; font-weight: 700; color: #78716c; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
    .kpi-value {{ font-size: 22px; font-weight: 800; color: #1c1917; }}
    .kpi-sub {{ font-size: 11.5px; color: #78716c; margin-top: 3px; }}
    .status-kpi {{
      border: 1px solid {risk['border_color']};
      background: {risk['badge_bg']};
    }}
    .status-badge {{
      display: inline-flex;
      align-items: center;
      font-size: 12.5px;
      font-weight: 800;
      color: {risk['badge_text']};
    }}

    /* Card Panels */
    .card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }}
    .card-title {{
      font-size: 13px;
      font-weight: 800;
      color: #1c1917;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .pill-tag {{
      font-size: 10.5px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      background: #f5f5f4;
      color: #57534e;
      border: 1px solid var(--border);
      text-transform: none;
    }}

    /* Biological Diagram */
    .bio-diagram-svg {{ width: 100%; height: auto; max-height: 130px; margin-bottom: 12px; }}

    /* Multi-Head Splicing Signals */
    .signals-box {{ display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }}
    .sig-row {{ display: flex; flex-direction: column; gap: 3px; }}
    .sig-meta {{ display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; color: #44403c; }}
    .sig-bar-bg {{ background: #f5f5f4; height: 7px; border-radius: 4px; overflow: hidden; }}
    .sig-bar-fill {{ height: 100%; border-radius: 4px; background: #ea580c; }}

    /* ACMG Cards */
    .acmg-grid {{ display: flex; flex-direction: column; gap: 8px; margin-bottom: 14px; }}
    .acmg-card {{
      background: #faf8f5;
      border: 1px solid var(--border);
      border-left: 4px solid #44403c;
      border-radius: 6px;
      padding: 10px 12px;
    }}
    .acmg-code {{ font-size: 12px; font-weight: 800; color: #1c1917; margin-bottom: 2px; }}
    .acmg-desc {{ font-size: 11.5px; color: #57534e; line-height: 1.45; }}

    /* Clinical Directive */
    .directive-card {{
      background: #f5f5f4;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px;
    }}
    .directive-title {{ font-size: 12px; font-weight: 800; color: #1c1917; margin-bottom: 6px; text-transform: uppercase; }}
    .directive-text {{ font-size: 12.5px; color: #292524; line-height: 1.55; }}

    /* Literature Cards */
    .lit-grid {{ display: flex; flex-direction: column; gap: 10px; }}
    .lit-card {{
      background: #faf8f5;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
    }}
    .lit-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
    .lit-tier {{ font-size: 10px; font-weight: 700; color: #78716c; text-transform: uppercase; }}
    .lit-pmid {{ font-size: 10px; background: #e7e5e4; color: #44403c; padding: 1px 6px; border-radius: 4px; font-weight: 600; }}
    .lit-doi-link {{ font-size: 11px; font-weight: 700; color: #ea580c; text-decoration: none; }}
    .lit-doi-link:hover {{ text-decoration: underline; }}
    .lit-citation {{ font-size: 12px; font-weight: 700; color: #1c1917; margin-bottom: 4px; }}
    .lit-takeaway {{ font-size: 11.5px; color: #44403c; line-height: 1.45; }}

    /* 1-Click Copy Note Button */
    .copy-btn {{
      background: #1c1917;
      color: #fafaf9;
      border: 1px solid #1c1917;
      font-size: 11px;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}
    .copy-btn:hover {{ background: #44403c; }}

    /* Elegant Floating Toast Notification */
    .toast-notification {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #1c1917;
      color: #fafaf9;
      padding: 10px 22px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 700;
      box-shadow: 0 4px 20px rgba(0,0,0,0.18);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s;
      opacity: 0;
      pointer-events: none;
      z-index: 9999;
    }}
    .toast-notification.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}

    /* Right Column: Live Sticky Copilot */
    .copilot-panel {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
      position: sticky;
      top: 70px;
      height: calc(100vh - 90px);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .copilot-header {{
      background: #f5f5f4;
      border-bottom: 1px solid var(--border);
      padding: 14px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .copilot-title {{ font-size: 13.5px; font-weight: 800; color: #1c1917; }}
    .copilot-badge {{ font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 999px; background: #e7e5e4; color: #44403c; }}
    
    .copilot-body {{
      flex: 1;
      padding: 14px 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      background: #ffffff;
    }}
    .chat-bubble {{
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 12px;
      line-height: 1.5;
      max-width: 92%;
    }}
    .chat-bubble.bot {{
      background: #faf8f5;
      border: 1px solid var(--border);
      color: #1c1917;
      align-self: flex-start;
    }}
    .chat-bubble.user {{
      background: #292524;
      color: #fafaf9;
      align-self: flex-end;
    }}

    /* Prompt Chips */
    .chips-container {{
      padding: 10px 14px;
      background: #faf8f5;
      border-top: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .chip-btn {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 11px;
      font-weight: 600;
      color: #44403c;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .chip-btn:hover {{ background: #f5f5f4; color: #1c1917; border-color: #d6d3d1; }}

    /* Chat Input Bar */
    .copilot-input-bar {{
      padding: 12px 14px;
      background: #ffffff;
      border-top: 1px solid var(--border);
      display: flex;
      gap: 8px;
    }}
    .chat-input {{
      flex: 1;
      padding: 8px 12px;
      font-size: 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #faf8f5;
      color: #1c1917;
      outline: none;
    }}
    .chat-input:focus {{ border-color: #a8a29e; background: #ffffff; }}
    .chat-send-btn {{
      padding: 8px 14px;
      font-size: 12px;
      font-weight: 700;
      color: #ffffff;
      background: #1c1917;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.15s;
    }}
    .chat-send-btn:hover {{ background: #44403c; }}

    /* Responsive */
    @media (max-width: 1080px) {{
      .split-layout {{ grid-template-columns: 1fr; }}
      .copilot-panel {{ position: static; height: 500px; margin-top: 20px; }}
      .kpi-grid {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>

  <!-- Top Sticky Navigation -->
  <nav class="topbar">
    <a href="index.html" class="brand">
      <span style="font-weight:700; color:#1c1917;">Genomic Decision Support</span>
      <span class="brand-tag">Clinical Cancer Genetics</span>
    </a>
    <div style="display:flex; align-items:center; gap:12px;">
      <span style="font-size:12px; color:var(--text-muted); font-weight:600;">Patient: Sarah Jenkins (39F)</span>
      <a href="index.html" class="dashboard-link">&larr; Multigene Panel Review</a>
    </div>
  </nav>

  <main class="container">

    <!-- Patient Header Hero -->
    <header class="patient-hero">
      <div class="patient-main">
        <div class="patient-avatar">PT</div>
        <div>
          <div class="patient-name">{pt['patient_name']} <span style="font-size:13px; font-weight:600; color:#78716c;">(Age {pt['patient_age']}, {pt['patient_gender']})</span></div>
          <div class="patient-sub">
            <strong>Indication:</strong> {pt['indication']}
          </div>
        </div>
      </div>
      <div class="patient-badges">
        <div class="badge-pill"><strong>Panel:</strong> {pt['panel_name']}</div>
        <div class="badge-pill"><strong>Sample:</strong> {pt['sample_id']}</div>
        <div class="badge-pill"><strong>Clinic:</strong> {pt['clinic']}</div>
      </div>
    </header>

    <!-- 3-Variant Switcher Row -->
    <nav class="switcher-row">
      {variant_switcher_html}
    </nav>

    <!-- Option A: Split View Layout -->
    <div class="split-layout">

      <!-- LEFT COLUMN: Clinical Dossier & Evidence -->
      <div class="cockpit-left">

        <!-- Executive Clinical Verdict Card -->
        <div class="plain-english-card">
          <div class="pe-label">
            <span>Executive Clinical Verdict</span>
            <span style="font-size:10px; background:#ffedd5; color:#c2410c; padding:2px 6px; border-radius:4px;">Finding #{finding_num} of 3</span>
          </div>
          <div class="pe-text">
            {case_data.get('plain_english_summary', '')}
          </div>
        </div>

        <!-- Hero KPI Metrics Row -->
        <div class="kpi-grid">
          <div class="kpi-card status-kpi">
            <div>
              <div class="kpi-label">Risk Classification</div>
              <div class="status-badge">
                <span>{risk['verdict']}</span>
              </div>
            </div>
            <div class="kpi-sub" style="color: {risk['badge_text']}; font-weight: 700;">
              {risk['action_type']}
            </div>
          </div>

          <div class="kpi-card">
            <div>
              <div class="kpi-label">AlphaGenome Score</div>
              <div class="kpi-value">{ag['combined_score']:.3f}</div>
            </div>
            <div class="kpi-sub">Cutoff 0.276 (94.3% Sens)</div>
          </div>

          <div class="kpi-card">
            <div>
              <div class="kpi-label">SpliceVarDB Assay</div>
              <div class="kpi-value" style="font-size: 16px; font-weight: 800; color: {risk['badge_text']};">
                {sv['classification']}
              </div>
            </div>
            <div class="kpi-sub">Experimental Truth</div>
          </div>

          <div class="kpi-card">
            <div>
              <div class="kpi-label">Calibrated PPV</div>
              <div class="kpi-value">{calib['ppv_percent']}%</div>
            </div>
            <div class="kpi-sub">Tier {calib['bin_number']} of 5 (95% CI: [{calib['ci_low_percent']}%–{calib['ci_high_percent']}%%])</div>
          </div>
        </div>

        <!-- Visual Risk Thermometer -->
        <div class="card" style="padding:16px 20px;">
          {risk_thermometer_html}
        </div>

        <!-- Molecular Architecture & Splicing Signal Tracks -->
        <div class="card">
          <div class="card-title">
            <span>Molecular Architecture &amp; Splice Track Decomposition</span>
            <span class="pill-tag">100 kb Sequence Context</span>
          </div>
          
          {svg_diagram}

          <div class="signals-box">
            <div class="sig-row">
              <div class="sig-meta">
                <span>Donor / Acceptor Splice Site Loss (&Delta; Splice Sites)</span>
                <span>{ag['max_delta_splice_sites']:.4f}</span>
              </div>
              <div class="sig-bar-bg">
                <div class="sig-bar-fill" style="width: {min(100, ag['max_delta_splice_sites'] * 100):.1f}%;"></div>
              </div>
            </div>

            <div class="sig-row">
              <div class="sig-meta">
                <span>Tissue Splice Junction Utilization (&Delta; Junction Usage)</span>
                <span>{ag['max_delta_splice_site_usage']:.4f}</span>
              </div>
              <div class="sig-bar-bg">
                <div class="sig-bar-fill" style="width: {min(100, ag['max_delta_splice_site_usage'] * 100):.1f}%;"></div>
              </div>
            </div>

            <div class="sig-row">
              <div class="sig-meta">
                <span>Aberrant Junction Formation (&Delta; Splice Junctions)</span>
                <span>{ag['max_delta_splice_junctions']:.4f}</span>
              </div>
              <div class="sig-bar-bg">
                <div class="sig-bar-fill" style="width: {min(100, (ag['max_delta_splice_junctions'] / 2.0) * 100):.1f}%;"></div>
              </div>
            </div>
          </div>

          <div style="background:#faf8f5; border:1px solid var(--border); border-radius:6px; padding:10px 12px; font-size:12px; color:#44403c; margin-top:14px; line-height:1.5;">
            <strong>Mechanism Details:</strong> {mol['impact_details']}
          </div>
        </div>

        <!-- ACMG Evidence & Directive -->
        <div class="card">
          <div class="card-title">
            <span>ACMG/AMP Evidence &amp; Clinical Management Directive</span>
            <button class="copy-btn" onclick="copyTumorBoardNote()">Copy Tumor Board Note</button>
          </div>
          
          <div class="acmg-grid">
            {acmg_html}
          </div>

          <div class="directive-card">
            <div class="directive-title">Tumor Board &amp; Clinical Management Directive</div>
            <div class="directive-text">{clin['clinical_directive']}</div>
          </div>
        </div>

        <!-- Prioritized Literature -->
        <div class="card">
          <div class="card-title">
            <span>Prioritized Supporting Literature (Top 3 Papers)</span>
            <span class="pill-tag">Peer-Reviewed Evidence</span>
          </div>
          <div class="lit-grid">
            {lit_cards_html}
          </div>
        </div>

      </div>

      <!-- RIGHT COLUMN: Sticky Live AI Copilot Panel -->
      <aside class="copilot-panel" id="chatDrawer">
        <div class="copilot-header">
          <div class="copilot-title">
            <span>Clinical AI Assistant</span>
          </div>
          <div class="copilot-badge">Finding #{finding_num} Active</div>
        </div>

        <div class="copilot-body" id="chatMessages">
          <div class="chat-bubble bot">
            Hello. I am your Clinical Decision Assistant for this HBOC-30 multigene panel review.
            <br><br>
            The panel identified 3 variants for this patient. You are currently evaluating <strong>Finding #{finding_num}: {gen['hgvs']}</strong> ({finding_role}).
            <br><br>
            Select any clinical inquiry chip below or enter a specific question.
          </div>
        </div>

        <div class="chips-container">
          <button class="chip-btn" onclick="askCopilot(&quot;Which variant is Sarah's true actionable driver?&quot;)">Driver Triage</button>
          <button class="chip-btn" onclick="askCopilot(&quot;Why is this variant classified as {risk['verdict']}?&quot;)">Risk Rationale</button>
          <button class="chip-btn" onclick="askCopilot(&quot;What papers support this finding?&quot;)">Literature</button>
          <button class="chip-btn" onclick="askCopilot(&quot;How does AlphaGenome compare to distance heuristics here?&quot;)">Distance Heuristic</button>
          <button class="chip-btn" onclick="askCopilot(&quot;What clinical management is recommended for Sarah?&quot;)">Surveillance Plan</button>
        </div>

        <div class="copilot-input-bar">
          <input type="text" id="chatInput" class="chat-input" placeholder="Ask about this variant or the patient's panel..." onkeydown="handleChatKey(event)">
          <button class="chat-send-btn" onclick="sendUserMessage()">Send</button>
        </div>
      </aside>

    </div>

  </main>

  <div id="toastNotification" class="toast-notification"></div>

  <!-- Client-Side Reasoning Engine & Patient KB -->
  <script>
    const PATIENT_KB = {patient_kb_json};

    function handleChatKey(e) {{
      if (e.key === 'Enter') {{
        sendUserMessage();
      }}
    }}

    function sendUserMessage() {{
      const input = document.getElementById('chatInput');
      const text = input.value.trim();
      if (!text) return;
      
      appendMessage('user', text);
      input.value = '';
      
      setTimeout(() => {{
        const response = generateAgentAnswer(text);
        appendMessage('bot', response);
      }}, 250);
    }}

    function askCopilot(question) {{
      appendMessage('user', question);
      setTimeout(() => {{
        const response = generateAgentAnswer(question);
        appendMessage('bot', response);
      }}, 250);
    }}

    function appendMessage(sender, text) {{
      const container = document.getElementById('chatMessages');
      const bubble = document.createElement('div');
      bubble.className = `chat-bubble ${{sender}}`;
      bubble.innerHTML = text.replace(/\\n/g, '<br>');
      container.appendChild(bubble);
      container.scrollTop = container.scrollHeight;
    }}

    function generateAgentAnswer(query) {{
      const q = query.toLowerCase();
      const pk = PATIENT_KB;
      const ak = pk.active_detail;

      // Patient-level driver triage question
      if (q.includes('driver') || q.includes('which variant') || q.includes('overall') || q.includes('sarah')) {{
        let res = `<strong>Multi-Variant Triage Summary:</strong><br>` +
                  `The patient carries 3 distinct findings on this HBOC-30 panel:<br>` +
                  `<ol style="padding-left:18px; margin:6px 0;">`;
        pk.findings.forEach(f => {{
          res += `<li><strong>Finding #${{f.finding_number}} (${{f.variant}}):</strong> ${{f.role}} (Score: ${{f.score}}, <strong>${{f.ppv}}% PPV</strong>).</li>`;
        }});
        res += `</ol>` +
               `<strong>Primary Conclusion:</strong> Finding #1 (<code>c.4986+1G>T</code>) is the <em>sole pathogenic driver</em> (100% PPV). ` +
               `Finding #2 is benign (<1.5% PPV) and should be de-escalated, while Finding #3 is a deep-intronic cryptic site (72.1% PPV) flagged for functional RNA confirmation.`;
        return res;
      }}

      // Risk rationale
      if (q.includes('why') || q.includes('verdict') || q.includes('risk') || q.includes('rationale') || q.includes('classif')) {{
        return `<strong>Risk Rationale for Finding #${{pk.active_finding_number}} (<code>${{ak.variant}}</code>):</strong><br>` +
               `AlphaGenome combined score is <strong>${{ak.score}}</strong>, placing it in <strong>Calibration Tier ${{ak.bin}}</strong>. ` +
               `In our 446-variant BRCA1 benchmark, this tier has an empirical Positive Predictive Value of <strong>${{ak.ppv}}%</strong> (95% CI: ${{ak.ci}}). ` +
               `SpliceVarDB experimental assays classify it as <em>${{ak.splicevardb_label}}</em>.<br><br>` +
               `<strong>Clinical Role:</strong> ${{ak.action_type}}.`;
      }}

      // Literature question
      if (q.includes('paper') || q.includes('literature') || q.includes('study') || q.includes('cite') || q.includes('reference')) {{
        let res = `<strong>Top Prioritized Supporting Studies:</strong><br><ul>`;
        ak.literature.forEach(item => {{
          res += `<li style="margin-bottom:6px;">${{item}}</li>`;
        }});
        res += `</ul>`;
        return res;
      }}

      // Distance heuristic contrast
      if (q.includes('distance') || q.includes('heuristic') || q.includes('offset') || q.includes('intron')) {{
        return `<strong>AlphaGenome vs. Conventional Distance Heuristics:</strong><br>` +
               `Standard distance heuristics (1/distance) assume splicing defects rapidly fade away from canonical boundaries. ` +
               `Across all intronic variants in BRCA1, AlphaGenome achieves an <strong>ROC AUC of 0.993</strong> vs. the distance baseline of <strong>0.914</strong>. ` +
               `AlphaGenome's 100 kb sequence backbone successfully identifies deep-intronic pseudoexon activations that proximity tools completely miss.`;
      }}

      // ACMG criteria
      if (q.includes('acmg') || q.includes('code') || q.includes('criteria')) {{
        let res = `<strong>ACMG/AMP Evidence Codes:</strong><br><ul>`;
        ak.acmg_codes.forEach(c => {{
          res += `<li>${{c}}</li>`;
        }});
        res += `</ul>`;
        return res;
      }}

      // Surveillance / Tumor Board Directive
      if (q.includes('action') || q.includes('surveillance') || q.includes('recommend') || q.includes('tumor board') || q.includes('next step') || q.includes('management')) {{
        return `<strong>Clinical Management Directive:</strong><br>${{ak.recommendation}}<br><br>` +
               `<strong>Summary Note:</strong> ${{ak.tumor_board_summary}}`;
      }}

      // Targeted therapies / PARP inhibitors
      if (q.includes('parp') || q.includes('olaparib') || q.includes('talazoparib') || q.includes('therapy') || q.includes('drug') || q.includes('treatment')) {{
        return `<strong>Targeted Therapy &amp; PARP Inhibitor Eligibility:</strong><br>` +
               `Because Finding #1 (<code>c.4986+1G>T</code>) causes complete loss of function in BRCA1, tumors harboring this mutation are deficient in Homologous Recombination Repair (HRD). ` +
               `In the setting of invasive recurrent or metastatic disease, the patient would be eligible for <strong>PARP inhibitors (e.g., olaparib, talazoparib)</strong> per FDA/EMA oncology indications. ` +
               `Prophylactic and surgical decisions should follow NCCN Genetic/Familial High-Risk guidelines.`;
      }}

      // Patient History & Indication
      if (q.includes('history') || q.includes('pedigree') || q.includes('age') || q.includes('dcis') || q.includes('family') || q.includes('sarah')) {{
        return `<strong>Patient Profile: Sarah Jenkins (Age 39, Female):</strong><br>` +
               `• <strong>Personal History:</strong> Ductal carcinoma in situ (DCIS) diagnosed at age 38.<br>` +
               `• <strong>Family History:</strong> Mother diagnosed with early-onset breast cancer at age 42; maternal aunt with high-grade serous ovarian cancer.<br>` +
               `• <strong>Test:</strong> Comprehensive 30-Gene Hereditary Breast & Ovarian Cancer Panel (HBOC-30).<br>` +
               `• <strong>Clinical Objective:</strong> Adjudicate 3 panel findings to establish definitive surgical and surveillance directives.`;
      }}

      // Calibration & Wilson Confidence Intervals
      if (q.includes('wilson') || q.includes('confidence') || q.includes('interval') || q.includes('calibration') || q.includes('benchmark')) {{
        return `<strong>Empirical Calibration &amp; Statistical Reliability:</strong><br>` +
               `Our calibration maps AlphaGenome scores against 446 experimental SpliceVarDB BRCA1 variants into 5 empirical calibration tiers. ` +
               `For this variant in <strong>Tier ${{ak.bin}}</strong>, the empirical PPV is <strong>${{ak.ppv}}%</strong> with a 95% Wilson Score Interval of <strong>${{ak.ci}}</strong>. ` +
               `The overall benchmark achieved an ROC AUC of <strong>0.980</strong> globally and <strong>0.993</strong> across intronic variants, validating high clinical reliability.`;
      }}

      // General fallback answer
      return `For <strong>Finding #${{pk.active_finding_number}} (${{ak.variant}})</strong>, our calibrated model assigns a score of <strong>${{ak.score}}</strong> ` +
             `(Tier ${{ak.bin}}, <strong>${{ak.ppv}}% PPV</strong>). ` +
             `Biological Mechanism: <em>${{ak.molecular_mechanism}}</em>. ` +
             `Click any prompt chip above or ask specifically about driver triage, PARP inhibitors, ACMG codes, or surveillance.`;
    }}

    function copyTumorBoardNote() {{
      const note = PATIENT_KB.active_detail.clipboard_note;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(note).then(() => {{
          showToast("Copied Tumor Board Note to clipboard.");
        }}).catch(() => {{
          fallbackCopy(note);
        }});
      }} else {{
        fallbackCopy(note);
      }}
    }}

    function fallbackCopy(text) {{
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      showToast("Copied Tumor Board Note to clipboard.");
    }}

    function showToast(msg) {{
      let toast = document.getElementById("toastNotification");
      if (!toast) {{
        toast = document.createElement("div");
        toast.id = "toastNotification";
        toast.className = "toast-notification";
        document.body.appendChild(toast);
      }}
      toast.innerText = msg;
      toast.classList.add("show");
      setTimeout(() => {{
        toast.classList.remove("show");
      }}, 2600);
    }}
  </script>
</body>
</html>
"""
    return html

def render_master_index(all_cases: list, metrics_df: pd.DataFrame, threshold_df: pd.DataFrame) -> str:
    """Render the Grand Master Patient Dashboard in warm off-white palette."""
    pt = all_cases[0]["patient_context"]

    cases_cards_html = ""
    for c in all_cases:
        cid = c["case_id"]
        role = c.get("finding_role", "")
        fnum = c.get("finding_number", 1)
        hgvs = c["genomic"]["hgvs"]
        score = c["alphagenome"]["combined_score"]
        sv_class = c["splicevardb"]["classification"]
        cal = c["calibration_bin"]
        pe = c.get("plain_english_summary", "")

        badge_bg = "#fee2e2" if cid == "case1_pathogenic" else ("#dcfce7" if cid == "case2_benign" else "#fef3c7")
        badge_text = "#991b1b" if cid == "case1_pathogenic" else ("#166534" if cid == "case2_benign" else "#92400e")
        score_color = "#b91c1c" if cid == "case1_pathogenic" else ("#15803d" if cid == "case2_benign" else "#d97706")

        cases_cards_html += f"""
        <div class="case-card">
          <div class="case-top">
            <span class="case-badge" style="background:{badge_bg}; color:{badge_text};">Finding #{fnum}: {role}</span>
            <span class="case-score" style="color:{score_color};">Score {score:.3f}</span>
          </div>
          <h3 class="case-title">{c['title']}</h3>
          <div class="case-meta">
            <div><strong>Variant:</strong> {hgvs}</div>
            <div><strong>Coordinates:</strong> {c['genomic']['chrom']}:{c['genomic']['pos']} {c['genomic']['ref']}&gt;{c['genomic']['alt']}</div>
            <div><strong>SpliceVarDB:</strong> {sv_class}</div>
            <div><strong>Calibration:</strong> Tier {cal['bin_number']} of 5 (<strong>{cal['ppv_percent']}% PPV</strong>)</div>
          </div>
          <p class="case-desc">{pe}</p>
          <a href="{cid}.html" class="case-action">Open Report &rarr;</a>
        </div>
        """

    # Comparative Multi-Variant Matrix Rows
    matrix_rows_html = ""
    for c in all_cases:
        cid = c["case_id"]
        fnum = c.get("finding_number", 1)
        role = c.get("finding_role", "")
        hgvs = c["genomic"]["hgvs"]
        score = c["alphagenome"]["combined_score"]
        cal = c["calibration_bin"]
        mech = c["biological_details"]["mutation_type"]
        
        badge_bg = "#fee2e2" if cid == "case1_pathogenic" else ("#dcfce7" if cid == "case2_benign" else "#fef3c7")
        badge_text = "#991b1b" if cid == "case1_pathogenic" else ("#166534" if cid == "case2_benign" else "#92400e")
        score_color = "#b91c1c" if cid == "case1_pathogenic" else ("#15803d" if cid == "case2_benign" else "#d97706")
        
        matrix_rows_html += f"""
        <tr>
          <td><span style="background:{badge_bg}; color:{badge_text}; font-size:10.5px; font-weight:800; padding:2px 6px; border-radius:4px;">Finding #{fnum}</span></td>
          <td><strong>{hgvs}</strong><br><span style="font-size:11px; color:#78716c;">{c['genomic']['chrom']}:{c['genomic']['pos']} ({c['genomic']['ref']}&gt;{c['genomic']['alt']})</span></td>
          <td style="font-size:11.5px; color:#44403c;">{mech}</td>
          <td><strong style="color:{score_color}; font-size:13px;">{score:.3f}</strong></td>
          <td><strong>Tier {cal['bin_number']}</strong> &bull; <span style="font-weight:800; color:{score_color};">{cal['ppv_percent']}% PPV</span><br><span style="font-size:10.5px; color:#78716c;">[{cal['ci_low_percent']}%–{cal['ci_high_percent']}%]</span></td>
          <td style="font-size:11.5px; font-weight:600;">{role}</td>
          <td><a href="{cid}.html" class="case-action" style="padding:5px 10px; font-size:11px;">Open Report &rarr;</a></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Multigene Panel Review — Hereditary Cancer Report</title>
  <style>
    :root {{
      --bg: #faf8f5;           /* Warm Alabaster Off-White */
      --card-bg: #ffffff;
      --border: #e7e5e4;
      --text: #1c1917;
      --text-muted: #57534e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 60px;
    }}

    /* Hero Header */
    .hero {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      padding: 32px 20px;
      text-align: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
    .hero h1 {{ font-size: 28px; font-weight: 800; color: #1c1917; margin: 0; }}

    .container {{ max-width: 1240px; margin: 0 auto; padding: 0 20px; }}

    /* Patient Overview Hero Banner */
    .patient-strip {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 24px;
      margin: -24px auto 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .patient-main {{ display: flex; align-items: center; gap: 14px; }}
    .patient-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #f5f5f4;
      border: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 800;
      color: #44403c;
    }}
    .patient-name {{ font-size: 17px; font-weight: 800; color: #1c1917; }}
    .patient-sub {{ font-size: 12px; color: var(--text-muted); margin-top: 2px; }}

    /* KPI Row */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 32px;
    }}
    .stat-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px;
      text-align: center;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
    .stat-val {{ font-size: 26px; font-weight: 800; color: #1c1917; margin-bottom: 2px; }}
    .stat-label {{ font-size: 10.5px; font-weight: 700; color: #78716c; text-transform: uppercase; }}
    .stat-sub {{ font-size: 11px; color: #a8a29e; margin-top: 3px; }}

    /* Section Titles */
    .section-title {{ font-size: 18px; font-weight: 800; color: #1c1917; margin-bottom: 4px; }}
    .section-sub {{ font-size: 12.5px; color: var(--text-muted); margin-bottom: 20px; }}

    /* Case Grid */
    .cases-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-bottom: 36px; }}
    .case-card {{
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.15s, box-shadow 0.15s;
    }}
    .case-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 18px rgba(0,0,0,0.05); }}
    .case-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
    .case-badge {{ font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }}
    .case-score {{ font-size: 13.5px; font-weight: 800; }}
    .case-title {{ font-size: 14.5px; font-weight: 800; color: #1c1917; margin-bottom: 10px; line-height: 1.35; }}
    .case-meta {{ font-size: 11.5px; color: #44403c; margin-bottom: 12px; line-height: 1.6; background: #faf8f5; padding: 10px; border-radius: 6px; border: 1px solid var(--border); }}
    .case-desc {{ font-size: 12px; color: #57534e; line-height: 1.55; margin-bottom: 16px; }}
    .case-action {{
      background: #1c1917;
      color: #fafaf9;
      text-decoration: none;
      font-size: 11.5px;
      font-weight: 700;
      text-align: center;
      padding: 9px 14px;
      border-radius: 6px;
      display: block;
      transition: background 0.15s;
    }}
    .case-action:hover {{ background: #44403c; }}

    /* 1-Click Copy Button */
    .copy-btn {{
      background: #1c1917;
      color: #fafaf9;
      border: 1px solid #1c1917;
      font-size: 11px;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}
    .copy-btn:hover {{ background: #44403c; }}

    /* Benchmark Table */
    .benchmark-table {{
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 36px;
    }}
    .benchmark-table th {{ background: #f5f5f4; text-align: left; padding: 10px 14px; font-size: 10.5px; font-weight: 700; color: #44403c; text-transform: uppercase; border-bottom: 1px solid var(--border); }}
    .benchmark-table td {{ padding: 10px 14px; font-size: 12px; color: #292524; border-bottom: 1px solid var(--border); }}
    .benchmark-table tr:last-child td {{ border-bottom: none; }}

    /* Toast Notification */
    .toast-notification {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: #1c1917;
      color: #fafaf9;
      padding: 10px 22px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 700;
      box-shadow: 0 4px 20px rgba(0,0,0,0.18);
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s;
      opacity: 0;
      pointer-events: none;
      z-index: 9999;
    }}
    .toast-notification.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>

  <header class="hero">
    <h1>Multigene Panel Review</h1>
  </header>

  <main class="container">

    <!-- Patient Header Strip -->
    <div class="patient-strip">
      <div class="patient-main">
        <div class="patient-avatar">PT</div>
        <div>
          <div class="patient-name">{pt['patient_name']} <span style="font-size:12.5px; font-weight:600; color:#78716c;">(Age {pt['patient_age']}, {pt['patient_gender']})</span></div>
          <div class="patient-sub">
            <strong>Indication:</strong> {pt['indication']}
          </div>
        </div>
      </div>
      <div style="display:flex; gap:8px;">
        <span style="font-size:11px; font-weight:700; background:#f5f5f4; padding:4px 8px; border-radius:6px; border:1px solid var(--border);">Panel: {pt['panel_name']}</span>
        <span style="font-size:11px; font-weight:700; background:#f5f5f4; padding:4px 8px; border-radius:6px; border:1px solid var(--border);">Sample: {pt['sample_id']}</span>
      </div>
    </div>

    <!-- Executive Triage Banner -->
    <div style="background:#ffffff; border:1px solid #fed7aa; border-left:5px solid #ea580c; border-radius:10px; padding:18px 22px; margin-bottom:28px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="font-size:11.5px; font-weight:800; color:#9a3412; text-transform:uppercase; letter-spacing:0.5px;">
          Molecular Tumor Board Executive Triage
        </div>
        <button class="copy-btn" onclick="copyMasterTumorBoardSummary()">Copy Master Tumor Board Summary</button>
      </div>
      <p style="font-size:13.5px; color:#292524; line-height:1.6; font-weight:500;">
        <strong>The Bottom Line:</strong> Out of 3 variants returned on this HBOC-30 panel, <strong>Finding #1 (<code>c.4986+1G>T</code>)</strong> is the sole pathogenic driver with <strong>100% calibrated PPV</strong> (consensus donor collapse), indicating immediate high-risk surveillance and RRSO counseling. <strong>Finding #2</strong> is functionally splicing neutral (&lt;1.5% PPV) and should be safely de-escalated, while <strong>Finding #3</strong> is a deep-intronic cryptic activation (72.1% PPV) flagged for functional RNA minigene confirmation.
      </p>
    </div>

    <!-- Benchmark KPI Row -->
    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-val">0.980</div>
        <div class="stat-label">Overall ROC AUC</div>
        <div class="stat-sub">95% CI: [0.962 – 0.993] (n=339)</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color: #15803d;">0.993</div>
        <div class="stat-label">Intronic ROC AUC</div>
        <div class="stat-sub">Beats distance baseline (0.914)</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color: #ea580c;">94.3%</div>
        <div class="stat-label">Sensitivity</div>
        <div class="stat-sub">At optimal threshold 0.276</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color: #b91c1c;">100%</div>
        <div class="stat-label">Tier 5 Precision (PPV)</div>
        <div class="stat-sub">68 / 68 True Positives</div>
      </div>
    </section>

    <!-- 3 Cases Grid -->
    <section>
      <h2 class="section-title">Multigene Panel Findings</h2>
      <p class="section-sub">Select any finding below to open the interactive clinical report and query the AI assistant.</p>
      
      <div class="cases-grid">
        {cases_cards_html}
      </div>
    </section>

    <!-- Multi-Variant Comparative Matrix Section -->
    <section>
      <h2 class="section-title">Multi-Variant Comparative Matrix</h2>
      <p class="section-sub">Side-by-side comparison of the 3 panel findings across foundation model metrics, calibration, and directives.</p>
      
      <table class="benchmark-table">
        <thead>
          <tr>
            <th>Finding</th>
            <th>Variant &amp; Coordinates</th>
            <th>Mutation Context</th>
            <th>AlphaGenome Score</th>
            <th>Calibrated Reliability</th>
            <th>Clinical Role</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {matrix_rows_html}
        </tbody>
      </table>
    </section>

    <!-- Benchmark Matrix Table -->
    <section>
      <h2 class="section-title">Empirical Benchmark Matrix</h2>
      <p class="section-sub">Verified statistical performance metrics from the 446-variant BRCA1 benchmark.</p>

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
            <td><strong style="color: #b91c1c;">0.980</strong></td>
            <td>[0.962 – 0.993]</td>
            <td>High-fidelity global performance across all single nucleotide variants.</td>
          </tr>
          <tr>
            <td><strong>Intronic Variants Only</strong></td>
            <td>152</td>
            <td>90</td>
            <td><strong style="color: #15803d;">0.993</strong></td>
            <td>[0.983 – 0.999]</td>
            <td>Outperforms distance heuristics on canonical and deep-intronic variants.</td>
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
            <td>Accurately rules out splicing defects for exonic variants.</td>
          </tr>
        </tbody>
      </table>
    </section>

  </main>

  <div id="toastNotification" class="toast-notification"></div>

  <script>
    const MASTER_TB_SUMMARY = `MOLECULAR TUMOR BOARD EXECUTIVE SUMMARY
Patient: Sarah Jenkins (Age 39, Female) — PT-HBOC-3982
Indication: Ductal carcinoma in situ (DCIS) at age 38; strong maternal history of early-onset breast & ovarian cancer.
Test: Comprehensive 30-Gene Hereditary Breast & Ovarian Cancer Panel (HBOC-30)

FINDINGS TRIAGE:
1. BRCA1 c.4986+1G>T (Canonical Donor Loss) -> ACTIONABLE PATHOGENIC DRIVER (Tier 5, 100% PPV).
   Directive: Reclassify to Likely Pathogenic (Class 4). Initiate high-risk breast/ovarian surveillance protocol and RRSO counseling.
2. BRCA1 c.2077G>A (Exonic Silent Variant) -> BENIGN SPLICING MIMIC (Tier 1, <1.5% PPV).
   Directive: Splicing neutral. Safely de-escalate. Do not base prophylactic surgery on this variant.
3. BRCA1 c.4185+4105C>T (Deep-Intronic Pseudoexon) -> ACTIONABLE CANDIDATE (Tier 4, 72.1% PPV).
   Directive: Sits 4,105 bp deep in intron. Expedite targeted RNA-seq minigene validation before final reclassification.`;

    function copyMasterTumorBoardSummary() {{
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(MASTER_TB_SUMMARY).then(() => {{
          showToast("Copied Master Tumor Board Summary to clipboard.");
        }}).catch(() => {{
          fallbackCopy(MASTER_TB_SUMMARY);
        }});
      }} else {{
        fallbackCopy(MASTER_TB_SUMMARY);
      }}
    }}

    function fallbackCopy(text) {{
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      showToast("Copied Master Tumor Board Summary to clipboard.");
    }}

    function showToast(msg) {{
      const toast = document.getElementById("toastNotification");
      toast.innerText = msg;
      toast.classList.add("show");
      setTimeout(() => {{
        toast.classList.remove("show");
      }}, 2600);
    }}
  </script>
</body>
</html>
"""
    return html

def main():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    staged_cases_path = os.path.join(DATA_DIR, "staged_cases.json")
    if not os.path.exists(staged_cases_path):
        from stage_case_data import stage_cases
        stage_cases()

    with open(staged_cases_path, "r") as f:
        staged_cases = json.load(f)

    metrics_df = pd.read_csv(os.path.join(RESULTS_DIR, "benchmark_metrics.csv"))
    threshold_df = pd.read_csv(os.path.join(RESULTS_DIR, "benchmark_threshold_metrics.csv"))

    from clinical_agent import ClinicalInterpretationAgent
    agent = ClinicalInterpretationAgent()

    interpreted_dict = {}
    for case in staged_cases:
        cid = case["case_id"]
        interp = agent.interpret_case(case)
        interpreted_dict[cid] = interp

    # Render reports
    for case in staged_cases:
        cid = case["case_id"]
        interp = interpreted_dict[cid]
        html_content = render_case_report(case, interp, staged_cases)
        out_file = os.path.join(REPORTS_DIR, f"{cid}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[REPORT RENDERED] {out_file}")

    # Render Master Index
    index_html = render_master_index(staged_cases, metrics_df, threshold_df)
    index_path = os.path.join(REPORTS_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"[REPORT RENDERED] {index_path}")

if __name__ == "__main__":
    main()

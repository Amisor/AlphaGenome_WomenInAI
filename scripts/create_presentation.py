#!/usr/bin/env python3
"""
create_presentation.py — Generates AlphaGenome_Clinical_Decision.pptx matching Ivana's exact minimalist style from AlgaeCal.pptx.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "AlphaGenome_Clinical_Decision.pptx")
ROC_IMAGE = os.path.join(BASE_DIR, "results", "roc_curve.png")

# Ivana's Color Palette from AlgaeCal.pptx
COLOR_TEAL = RGBColor(7, 121, 95)      # #07795F
COLOR_DARK_TEAL = RGBColor(36, 94, 79)  # #245E4F
COLOR_CHARCOAL = RGBColor(25, 25, 25)   # #191919
COLOR_GRAY = RGBColor(119, 118, 120)    # #777678
COLOR_LIGHT_GRAY = RGBColor(215, 216, 218) # #D7D8DA
COLOR_CARD_BG = RGBColor(248, 249, 250) # #F8F9FA
COLOR_RED = RGBColor(185, 28, 28)       # #B91C1C
COLOR_GREEN = RGBColor(21, 128, 61)     # #15803D
COLOR_AMBER = RGBColor(217, 119, 6)     # #D97706
COLOR_WHITE = RGBColor(255, 255, 255)

FONT_PRIMARY = "Aileron"

def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, category_text, title_text, slide_num):
    # Category Tracker (Top-left)
    cat_box = slide.shapes.add_textbox(Inches(1.2), Inches(0.45), Inches(10.0), Inches(0.45))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text
    p_cat.font.name = FONT_PRIMARY
    p_cat.font.size = Pt(14)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_TEAL

    # Main Title (Below Category)
    title_box = slide.shapes.add_textbox(Inches(1.2), Inches(0.85), Inches(16.0), Inches(0.85))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_PRIMARY
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_CHARCOAL

    # Slide Number at Bottom Center
    num_box = slide.shapes.add_textbox(Inches(9.5), Inches(10.45), Inches(1.0), Inches(0.4))
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.CENTER
    p_num.text = str(slide_num)
    p_num.font.name = FONT_PRIMARY
    p_num.font.size = Pt(12)
    p_num.font.color.rgb = COLOR_GRAY

def add_speaker_note(slide, note_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = note_text.strip()

def build_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, COLOR_WHITE)

    # Main Presentation Title
    t_box = s1.shapes.add_textbox(Inches(1.8), Inches(3.6), Inches(16.4), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Evaluating Variants of Uncertain Significance in BRCA1"
    p1.font.name = FONT_PRIMARY
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_CHARCOAL

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Empirical Foundation Model Splicing Benchmarks & Decision Support"
    p1_sub.font.name = FONT_PRIMARY
    p1_sub.font.size = Pt(24)
    p1_sub.font.color.rgb = COLOR_TEAL
    p1_sub.space_before = Pt(14)

    # Author & Affiliation Details (Bottom left, matching AlgaeCal Slide 1)
    a_box = s1.shapes.add_textbox(Inches(1.8), Inches(7.2), Inches(14.0), Inches(2.2))
    tfa = a_box.text_frame
    pa1 = tfa.paragraphs[0]
    pa1.text = "Ivana Sánchez Olivares & Shachi Bhavsar"
    pa1.font.name = FONT_PRIMARY
    pa1.font.size = Pt(22)
    pa1.font.bold = True
    pa1.font.color.rgb = COLOR_CHARCOAL

    pa2 = tfa.add_paragraph()
    pa2.text = "Women in AI Hackathon — AlphaGenome × SpliceVarDB Clinical Project"
    pa2.font.name = FONT_PRIMARY
    pa2.font.size = Pt(16)
    pa2.font.color.rgb = COLOR_GRAY
    pa2.space_before = Pt(6)

    add_speaker_note(s1, (
        "Hello, everyone. Have you ever wondered what happens when someone takes a genetic test "
        "for cancer risk, and the answer comes back as: 'We don't know'? "
        "My name is Ivana, and together with Shachi, today we will talk about evaluating Variants of Uncertain Significance "
        "in BRCA1 using foundation models and experimental splicing benchmarks."
    ))

    # =========================================================================
    # SLIDE 2: BACKGROUND (What is RNA splicing?)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, COLOR_WHITE)
    add_header(s2, "BACKGROUND", "What is RNA splicing?", 1)

    # Left Column (Core Principle)
    card_l = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), Inches(8.3), Inches(7.8))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = COLOR_CARD_BG
    card_l.line.color.rgb = COLOR_LIGHT_GRAY

    tf_l = card_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = Inches(0.5)
    tf_l.margin_top = Inches(0.5)
    
    pl1 = tf_l.paragraphs[0]
    pl1.text = "All cells contain the same DNA"
    pl1.font.name = FONT_PRIMARY
    pl1.font.size = Pt(22)
    pl1.font.bold = True
    pl1.font.color.rgb = COLOR_CHARCOAL

    pl2 = tf_l.add_paragraph()
    pl2.text = "Our cells read genes like BRCA1 to make essential cancer protection proteins."
    pl2.font.name = FONT_PRIMARY
    pl2.font.size = Pt(16)
    pl2.font.color.rgb = COLOR_GRAY
    pl2.space_before = Pt(8)

    pl3 = tf_l.add_paragraph()
    pl3.text = "What makes genes different from plain text?"
    pl3.font.name = FONT_PRIMARY
    pl3.font.size = Pt(20)
    pl3.font.bold = True
    pl3.font.color.rgb = COLOR_TEAL
    pl3.space_before = Pt(24)

    pl4 = tf_l.add_paragraph()
    pl4.text = "Genes are not continuous. They are interrupted by long non-coding regions called introns."
    pl4.font.name = FONT_PRIMARY
    pl4.font.size = Pt(16)
    pl4.font.color.rgb = COLOR_CHARCOAL
    pl4.space_before = Pt(8)

    # Right Column (Splicing Mechanism)
    card_r = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.5), Inches(2.2), Inches(8.3), Inches(7.8))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = COLOR_CARD_BG
    card_r.line.color.rgb = COLOR_LIGHT_GRAY

    tf_r = card_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = Inches(0.5)
    tf_r.margin_top = Inches(0.5)

    pr1 = tf_r.paragraphs[0]
    pr1.text = "RNA splicing cuts out introns and stitches coding exons together"
    pr1.font.name = FONT_PRIMARY
    pr1.font.size = Pt(20)
    pr1.font.bold = True
    pr1.font.color.rgb = COLOR_CHARCOAL

    pr2 = tf_r.add_paragraph()
    pr2.text = "How does it happen?"
    pr2.font.name = FONT_PRIMARY
    pr2.font.size = Pt(18)
    pr2.font.bold = True
    pr2.font.color.rgb = COLOR_TEAL
    pr2.space_before = Pt(18)

    pr3 = tf_r.add_paragraph()
    pr3.text = "Cellular machinery recognizes precise chemical signals (donor and acceptor sites) at exon boundaries to guide the cut-and-paste process."
    pr3.font.name = FONT_PRIMARY
    pr3.font.size = Pt(15)
    pr3.font.color.rgb = COLOR_CHARCOAL
    pr3.space_before = Pt(6)

    pr4 = tf_r.add_paragraph()
    pr4.text = "Roles & Health Impact"
    pr4.font.name = FONT_PRIMARY
    pr4.font.size = Pt(18)
    pr4.font.bold = True
    pr4.font.color.rgb = COLOR_TEAL
    pr4.space_before = Pt(18)

    pr5 = tf_r.add_paragraph()
    pr5.text = "Disruptions break the reading frame, inducing premature stop codons. Loss of BRCA1 splicing causes hereditary breast and ovarian cancer."
    pr5.font.name = FONT_PRIMARY
    pr5.font.size = Pt(15)
    pr5.font.color.rgb = COLOR_CHARCOAL
    pr5.space_before = Pt(6)

    add_speaker_note(s2, (
        "[Slide 1: What is RNA splicing?]\n"
        "All our cells contain exactly the same DNA, reading genes to produce essential proteins that protect us from cancer, like BRCA1. "
        "So what makes reading genes complex? Genes are not continuous stories; they are interrupted by long non-coding sequences called introns. "
        "RNA splicing is the cellular process that cuts out these non-coding interruptions and stitches the coding exons together into one functional message.\n\n"
        "It happens when microscopic cellular machinery recognizes precise chemical signals at exon boundaries. "
        "When a mutation disrupts these signals, the cell cuts out vital parts of the gene or keeps broken fragments, destroying the protein and dramatically raising the risk of cancer."
    ))

    # =========================================================================
    # SLIDE 3: PROBLEM (Measuring Splicing Impact in Genetic Testing)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, COLOR_WHITE)
    add_header(s3, "PROBLEM", "Measuring splicing impact in genetic testing", 2)

    # Left: Before vs. Now
    card3_l = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), Inches(8.3), Inches(7.8))
    card3_l.fill.solid()
    card3_l.fill.fore_color.rgb = COLOR_CARD_BG
    card3_l.line.color.rgb = COLOR_LIGHT_GRAY

    tf3_l = card3_l.text_frame
    tf3_l.word_wrap = True
    tf3_l.margin_left = Inches(0.5)
    tf3_l.margin_top = Inches(0.5)

    p3l_1 = tf3_l.paragraphs[0]
    p3l_1.text = "Before"
    p3l_1.font.name = FONT_PRIMARY
    p3l_1.font.size = Pt(18)
    p3l_1.font.bold = True
    p3l_1.font.color.rgb = COLOR_GRAY

    p3l_2 = tf3_l.add_paragraph()
    p3l_2.text = "Standard genetic testing only checked simple protein coding changes."
    p3l_2.font.name = FONT_PRIMARY
    p3l_2.font.size = Pt(16)
    p3l_2.font.color.rgb = COLOR_CHARCOAL
    p3l_2.space_before = Pt(4)

    p3l_3 = tf3_l.add_paragraph()
    p3l_3.text = "Now (New multigene panels!)"
    p3l_3.font.name = FONT_PRIMARY
    p3l_3.font.size = Pt(18)
    p3l_3.font.bold = True
    p3l_3.font.color.rgb = COLOR_TEAL
    p3l_3.space_before = Pt(24)

    p3l_4 = tf3_l.add_paragraph()
    p3l_4.text = "Comprehensive panels sequence entire loci, identifying thousands of non-coding and splice-region variants."
    p3l_4.font.name = FONT_PRIMARY
    p3l_4.font.size = Pt(16)
    p3l_4.font.color.rgb = COLOR_CHARCOAL
    p3l_4.space_before = Pt(4)

    # Right: Challenges & Goal
    card3_r = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.5), Inches(2.2), Inches(8.3), Inches(7.8))
    card3_r.fill.solid()
    card3_r.fill.fore_color.rgb = COLOR_CARD_BG
    card3_r.line.color.rgb = COLOR_LIGHT_GRAY

    tf3_r = card3_r.text_frame
    tf3_r.word_wrap = True
    tf3_r.margin_left = Inches(0.5)
    tf3_r.margin_top = Inches(0.5)

    p3r_h = tf3_r.paragraphs[0]
    p3r_h.text = "Challenges"
    p3r_h.font.name = FONT_PRIMARY
    p3r_h.font.size = Pt(22)
    p3r_h.font.bold = True
    p3r_h.font.color.rgb = COLOR_RED

    ch1 = tf3_r.add_paragraph()
    ch1.text = "• Up to 30% of multigene panel findings are classified as Variants of Uncertain Significance (VUS), leaving clinicians unable to act."
    ch1.font.name = FONT_PRIMARY
    ch1.font.size = Pt(15)
    ch1.font.color.rgb = COLOR_CHARCOAL
    ch1.space_before = Pt(10)

    ch2 = tf3_r.add_paragraph()
    ch2.text = "• Conventional software uses distance heuristics that miss deep-intronic mutations and trigger false alarms on benign mimics."
    ch2.font.name = FONT_PRIMARY
    ch2.font.size = Pt(15)
    ch2.font.color.rgb = COLOR_CHARCOAL
    ch2.space_before = Pt(10)

    ch3 = tf3_r.add_paragraph()
    ch3.text = "• No calibrated dataset with known answers to translate raw algorithm predictions into clinical decisions."
    ch3.font.name = FONT_PRIMARY
    ch3.font.size = Pt(15)
    ch3.font.color.rgb = COLOR_CHARCOAL
    ch3.space_before = Pt(10)

    goal_p = tf3_r.add_paragraph()
    goal_p.text = "Goal: Benchmark AlphaGenome against experimental ground truth and build an interactive clinical decision report."
    goal_p.font.name = FONT_PRIMARY
    goal_p.font.size = Pt(16)
    goal_p.font.bold = True
    goal_p.font.color.rgb = COLOR_TEAL
    goal_p.space_before = Pt(18)

    add_speaker_note(s3, (
        "[Slide 2: Problem]\n"
        "Until recently, standard genetic testing only checked simple protein coding changes. "
        "New technology now lets us sequence entire multigene panels, capturing thousands of non-coding and splice-region variants. "
        "However, this comes with major challenges.\n\n"
        "Up to 30% of variants are classified as Variants of Uncertain Significance. "
        "Traditional prediction tools rely on simple distance heuristics, missing mutations that hide thousands of letters deep inside introns while raising false alarms on benign mimics. "
        "And there is no calibrated dataset with known answers to test software and guide surgical decisions. "
        "That is why my goal was to benchmark DeepMind’s AlphaGenome foundation model against experimental ground truth and build a clinical decision support report."
    ))

    # =========================================================================
    # SLIDE 4: DATA (SpliceVarDB Experimental Ground Truth)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, COLOR_WHITE)
    add_header(s4, "SOLUTION: METHODOLOGY", "Experimental ground truth from SpliceVarDB", 3)

    # 3 Data Cards
    c4_1 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), Inches(5.5), Inches(6.8))
    c4_1.fill.solid()
    c4_1.fill.fore_color.rgb = COLOR_CARD_BG
    c4_1.line.color.rgb = COLOR_LIGHT_GRAY
    tf4_1 = c4_1.text_frame
    tf4_1.word_wrap = True
    tf4_1.margin_left = Inches(0.4)
    tf4_1.margin_top = Inches(0.4)
    p = tf4_1.paragraphs[0]
    p.text = "446 BRCA1 Variants"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_CHARCOAL
    p2 = tf4_1.add_paragraph()
    p2.text = "Curated single-nucleotide variants evaluated against experimental ground truth in SpliceVarDB across the complete BRCA1 genomic locus."
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_GRAY
    p2.space_before = Pt(12)

    c4_2 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(2.2), Inches(5.5), Inches(6.8))
    c4_2.fill.solid()
    c4_2.fill.fore_color.rgb = COLOR_CARD_BG
    c4_2.line.color.rgb = COLOR_LIGHT_GRAY
    tf4_2 = c4_2.text_frame
    tf4_2.word_wrap = True
    tf4_2.margin_left = Inches(0.4)
    tf4_2.margin_top = Inches(0.4)
    p = tf4_2.paragraphs[0]
    p.text = "Physical Laboratory Assays"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p2 = tf4_2.add_paragraph()
    p2.text = "Minigene functional splicing assays & patient RNA-seq transcript sequencing physically confirming whether each variant alters splicing."
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_GRAY
    p2.space_before = Pt(12)

    c4_3 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(13.2), Inches(2.2), Inches(5.6), Inches(6.8))
    c4_3.fill.solid()
    c4_3.fill.fore_color.rgb = COLOR_CARD_BG
    c4_3.line.color.rgb = COLOR_LIGHT_GRAY
    tf4_3 = c4_3.text_frame
    tf4_3.word_wrap = True
    tf4_3.margin_left = Inches(0.4)
    tf4_3.margin_top = Inches(0.4)
    p = tf4_3.paragraphs[0]
    p.text = "Experimental Labels"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_CHARCOAL
    p2 = tf4_3.add_paragraph()
    p2.text = "• 230 Not splice-altering (neutral)\n• 131 Splice-altering (damaging)\n• 85 Low-frequency / complex"
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_CHARCOAL
    p2.space_before = Pt(12)

    # Citation
    cit_box = s4.shapes.add_textbox(Inches(1.2), Inches(9.5), Inches(17.6), Inches(0.6))
    p_cit = cit_box.text_frame.paragraphs[0]
    p_cit.text = "(SpliceVarDB Consortium, 2024) — SpliceVarDB: A comprehensive database of experimentally validated human splicing variants. Am J Hum Genet."
    p_cit.font.name = FONT_PRIMARY
    p_cit.font.size = Pt(12)
    p_cit.font.color.rgb = COLOR_GRAY

    add_speaker_note(s4, (
        "[Slide 3: Data]\n"
        "To do this, I obtained experimental ground truth from SpliceVarDB across 446 human BRCA1 variants. "
        "In these laboratory studies, scientists physically tested human cells using minigene splicing assays and patient RNA sequencing "
        "to measure whether each mutation truly breaks RNA splicing or leaves it completely intact. "
        "This gave us our gold-standard answer key of 230 verified neutral variants and 131 verified splice-altering mutations."
    ))

    # =========================================================================
    # SLIDE 5: MODEL (AlphaGenome Foundation Model)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, COLOR_WHITE)
    add_header(s5, "SOLUTION: METHODOLOGY", "AlphaGenome 100 kb sequence context model", 4)

    card5_l = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), Inches(9.2), Inches(7.0))
    card5_l.fill.solid()
    card5_l.fill.fore_color.rgb = COLOR_CARD_BG
    card5_l.line.color.rgb = COLOR_LIGHT_GRAY
    tf5_l = card5_l.text_frame
    tf5_l.word_wrap = True
    tf5_l.margin_left = Inches(0.5)
    tf5_l.margin_top = Inches(0.5)

    p = tf5_l.paragraphs[0]
    p.text = "Google DeepMind Foundation Model"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p1 = tf5_l.add_paragraph()
    p1.text = "• 100,000-letter sequence context window across the BRCA1 locus (GRCh38)."
    p1.font.size = Pt(16)
    p1.font.color.rgb = COLOR_CHARCOAL
    p1.space_before = Pt(14)

    p2 = tf5_l.add_paragraph()
    p2.text = "• Predicts disruptions to splice donor sites, splice acceptor sites, and junction usage."
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_CHARCOAL
    p2.space_before = Pt(10)

    p3 = tf5_l.add_paragraph()
    p3.text = "• Captures long-range chromatin and regulatory interactions invisible to local tools."
    p3.font.size = Pt(16)
    p3.font.color.rgb = COLOR_CHARCOAL
    p3.space_before = Pt(10)

    card5_r = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.8), Inches(2.2), Inches(8.0), Inches(7.0))
    card5_r.fill.solid()
    card5_r.fill.fore_color.rgb = COLOR_CARD_BG
    card5_r.line.color.rgb = COLOR_LIGHT_GRAY
    tf5_r = card5_r.text_frame
    tf5_r.word_wrap = True
    tf5_r.margin_left = Inches(0.5)
    tf5_r.margin_top = Inches(0.5)

    p = tf5_r.paragraphs[0]
    p.text = "What the Model Predicts"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_CHARCOAL

    pr1 = tf5_r.add_paragraph()
    pr1.text = "1. Loss of Canonical Splice Sites"
    pr1.font.size = Pt(17)
    pr1.font.bold = True
    pr1.font.color.rgb = COLOR_RED
    pr1.space_before = Pt(14)
    pr1_sub = tf5_r.add_paragraph()
    pr1_sub.text = "Destruction of invariant +1/+2 donor or -1/-2 acceptor dinucleotides."
    pr1_sub.font.size = Pt(14)
    pr1_sub.font.color.rgb = COLOR_GRAY

    pr2 = tf5_r.add_paragraph()
    pr2.text = "2. Cryptic Site Activation"
    pr2.font.size = Pt(17)
    pr2.font.bold = True
    pr2.font.color.rgb = COLOR_AMBER
    pr2.space_before = Pt(14)
    pr2_sub = tf5_r.add_paragraph()
    pr2_sub.text = "Creation of de novo splice sites deep in introns that cause pseudoexon inclusion."
    pr2_sub.font.size = Pt(14)
    pr2_sub.font.color.rgb = COLOR_GRAY

    # Citation
    cit_box = s5.shapes.add_textbox(Inches(1.2), Inches(9.5), Inches(17.6), Inches(0.6))
    p_cit = cit_box.text_frame.paragraphs[0]
    p_cit.text = "(Avsec et al., 2026) — Advancing regulatory variant effect prediction with AlphaGenome. Nature."
    p_cit.font.name = FONT_PRIMARY
    p_cit.font.size = Pt(12)
    p_cit.font.color.rgb = COLOR_GRAY

    add_speaker_note(s5, (
        "[Slide 4: Model]\n"
        "I evaluated Google DeepMind's AlphaGenome foundation model. "
        "Unlike traditional tools that only look at one or two letters right at the boundary, AlphaGenome reads 100,000 letters of human DNA context at once. "
        "It predicts disruptions to donor sites, acceptor sites, and splice junctions, allowing it to capture long-range regulatory effects and cryptic splice activations that local tools completely miss."
    ))

    # =========================================================================
    # SLIDE 6: RESULTS (Benchmark Performance & 5-Tier Calibration)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, COLOR_WHITE)
    add_header(s6, "SOLUTION: METHODOLOGY & RESULTS", "Benchmark performance & 5-tier empirical calibration", 5)

    # Left: Stats & ROC
    card6_l = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), Inches(8.5), Inches(7.3))
    card6_l.fill.solid()
    card6_l.fill.fore_color.rgb = COLOR_CARD_BG
    card6_l.line.color.rgb = COLOR_LIGHT_GRAY
    tf6_l = card6_l.text_frame
    tf6_l.word_wrap = True
    tf6_l.margin_left = Inches(0.4)
    tf6_l.margin_top = Inches(0.4)

    p = tf6_l.paragraphs[0]
    p.text = "Benchmark Accuracy (n = 339)"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CHARCOAL

    p1 = tf6_l.add_paragraph()
    p1.text = "• Overall ROC AUC = 0.980 (95% CI: [0.962 – 0.993])"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEAL
    p1.space_before = Pt(10)

    p2 = tf6_l.add_paragraph()
    p2.text = "• Intronic ROC AUC = 0.993 (outperforms distance baseline 0.914)"
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEAL
    p2.space_before = Pt(8)

    p3 = tf6_l.add_paragraph()
    p3.text = "• Optimal Cutoff (0.276): 94.3% Sensitivity, 95.8% Specificity"
    p3.font.size = Pt(15)
    p3.font.color.rgb = COLOR_CHARCOAL
    p3.space_before = Pt(8)

    # Embed ROC Curve figure inside card if exists
    if os.path.exists(ROC_IMAGE):
        s6.shapes.add_picture(ROC_IMAGE, Inches(3.15), Inches(4.5), width=Inches(4.6), height=Inches(4.6))

    # Right: The 5 Tiers
    card6_r = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.2), Inches(2.2), Inches(8.6), Inches(7.3))
    card6_r.fill.solid()
    card6_r.fill.fore_color.rgb = COLOR_CARD_BG
    card6_r.line.color.rgb = COLOR_LIGHT_GRAY
    tf6_r = card6_r.text_frame
    tf6_r.word_wrap = True
    tf6_r.margin_left = Inches(0.4)
    tf6_r.margin_top = Inches(0.4)

    p = tf6_r.paragraphs[0]
    p.text = "The 5 Clinical Tiers (Empirical PPV)"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CHARCOAL

    pt5 = tf6_r.add_paragraph()
    pt5.text = "Tier 5: Definitive Risk (100.0% PPV)"
    pt5.font.size = Pt(16)
    pt5.font.bold = True
    pt5.font.color.rgb = COLOR_RED
    pt5.space_before = Pt(12)
    pt5_sub = tf6_r.add_paragraph()
    pt5_sub.text = "68 / 68 True Positives. Score > 2.164. Reclassify to Likely Pathogenic."
    pt5_sub.font.size = Pt(14)
    pt5_sub.font.color.rgb = COLOR_GRAY

    pt4 = tf6_r.add_paragraph()
    pt4.text = "Tier 4: High Risk (72.1% PPV)"
    pt4.font.size = Pt(16)
    pt4.font.bold = True
    pt4.font.color.rgb = COLOR_AMBER
    pt4.space_before = Pt(12)
    pt4_sub = tf6_r.add_paragraph()
    pt4_sub.text = "49 / 68 True Positives. Prioritize for functional RNA-seq confirmation."
    pt4_sub.font.size = Pt(14)
    pt4_sub.font.color.rgb = COLOR_GRAY

    pt1 = tf6_r.add_paragraph()
    pt1.text = "Tier 1: Minimal Risk (1.5% PPV)"
    pt1.font.size = Pt(16)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_GREEN
    pt1.space_before = Pt(12)
    pt1_sub = tf6_r.add_paragraph()
    pt1_sub.text = "1 / 67 Positives. Score < 0.057. Splicing defect safely excluded."
    pt1_sub.font.size = Pt(14)
    pt1_sub.font.color.rgb = COLOR_GRAY

    add_speaker_note(s6, (
        "[Slide 5: Results]\n"
        "When evaluated against the experimental ground truth, AlphaGenome achieved an overall ROC AUC of 0.980, "
        "and reached 0.993 on intronic variants, significantly beating the distance baseline of 0.914. "
        "At the optimal cutoff of 0.276, it achieved 94.3% sensitivity and 95.8% specificity.\n\n"
        "To make this actionable for doctors, I converted the scores into 5 empirical calibration tiers with 95% Wilson confidence intervals. "
        "In Tier 1, the risk of a splicing defect is under 1.5%, safely ruling out damage. "
        "In Tier 5, 68 out of 68 variants were experimentally confirmed to disrupt splicing—giving 100% precision to support clinical reclassification."
    ))

    # =========================================================================
    # SLIDE 7: CLINICAL APPLICATION (Sarah Jenkins & The HTML Report)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, COLOR_WHITE)
    add_header(s7, "CLINICAL APPLICATION", "Multigene panel triage: Sarah Jenkins (39F)", 6)

    # 3 Finding Cards
    card7_1 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), Inches(5.5), Inches(7.3))
    card7_1.fill.solid()
    card7_1.fill.fore_color.rgb = COLOR_CARD_BG
    card7_1.line.color.rgb = COLOR_LIGHT_GRAY
    tf7_1 = card7_1.text_frame
    tf7_1.word_wrap = True
    tf7_1.margin_left = Inches(0.4)
    tf7_1.margin_top = Inches(0.4)

    p = tf7_1.paragraphs[0]
    p.text = "Finding #1: Driver"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p_sub = tf7_1.add_paragraph()
    p_sub.text = "NM_007294.4:c.4986+1G>T"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CHARCOAL
    p_sub.space_before = Pt(4)

    p_b = tf7_1.add_paragraph()
    p_b.text = "• Tier 5 (100.0% PPV)\n• Exon 15 canonical donor collapse\n• Recommendation: Reclassify to Likely Pathogenic (PVS1/PS3/PP3); initiate breast MRI surveillance and RRSO."
    p_b.font.size = Pt(14)
    p_b.font.color.rgb = COLOR_CHARCOAL
    p_b.space_before = Pt(10)

    card7_2 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(2.2), Inches(5.5), Inches(7.3))
    card7_2.fill.solid()
    card7_2.fill.fore_color.rgb = COLOR_CARD_BG
    card7_2.line.color.rgb = COLOR_LIGHT_GRAY
    tf7_2 = card7_2.text_frame
    tf7_2.word_wrap = True
    tf7_2.margin_left = Inches(0.4)
    tf7_2.margin_top = Inches(0.4)

    p = tf7_2.paragraphs[0]
    p.text = "Finding #2: Mimic"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p_sub = tf7_2.add_paragraph()
    p_sub.text = "NM_007294.4:c.2077G>A"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CHARCOAL
    p_sub.space_before = Pt(4)

    p_b = tf7_2.add_paragraph()
    p_b.text = "• Tier 1 (1.5% PPV)\n• Exonic silent substitution\n• Recommendation: De-escalate splicing; rule out splicing defect; avoid unnecessary prophylactic surgery."
    p_b.font.size = Pt(14)
    p_b.font.color.rgb = COLOR_CHARCOAL
    p_b.space_before = Pt(10)

    card7_3 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(13.2), Inches(2.2), Inches(5.6), Inches(7.3))
    card7_3.fill.solid()
    card7_3.fill.fore_color.rgb = COLOR_CARD_BG
    card7_3.line.color.rgb = COLOR_LIGHT_GRAY
    tf7_3 = card7_3.text_frame
    tf7_3.word_wrap = True
    tf7_3.margin_left = Inches(0.4)
    tf7_3.margin_top = Inches(0.4)

    p = tf7_3.paragraphs[0]
    p.text = "Finding #3: Candidate"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p_sub = tf7_3.add_paragraph()
    p_sub.text = "NM_007294.4:c.4185+4105C>T"
    p_sub.font.size = Pt(14)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CHARCOAL
    p_sub.space_before = Pt(4)

    p_b = tf7_3.add_paragraph()
    p_b.text = "• Tier 4 (72.1% PPV)\n• 4,105 bp deep inside intron\n• Recommendation: Prioritize for functional RNA-seq minigene validation."
    p_b.font.size = Pt(14)
    p_b.font.color.rgb = COLOR_CHARCOAL
    p_b.space_before = Pt(10)

    add_speaker_note(s7, (
        "[Slide 6: Clinical Application]\n"
        "I implemented this in a hospital-grade decision report for a representative patient, Sarah Jenkins, "
        "a 39-year-old woman with personal and maternal breast cancer history whose panel test returned three uncertain BRCA1 findings. "
        "The report triages all three on one screen:\n\n"
        "Finding 1 is placed in Tier 5 as the true pathogenic driver, directing high-risk surveillance and prophylactic counseling. "
        "Finding 2 is in Tier 1, ruling out splicing and preventing an unnecessary mastectomy. "
        "Finding 3 is in Tier 4, flagging a hidden mutation for expedited RNA validation. "
        "A side-by-side AI assistant answers clinical questions at zero API cost, and a 1-click button exports notes straight into the hospital's health record."
    ))

    # =========================================================================
    # SLIDE 8: CONCLUSION (Problem, Solution, Impact — Exact AlgaeCal Slide 9)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, COLOR_WHITE)
    add_header(s8, "CONCLUSION", "Calibrated foundation models empower precision cancer decisions", 7)

    box_w = Inches(5.6)
    box_h = Inches(7.5)

    # Box 1: Problem
    b1 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.2), box_w, box_h)
    b1.fill.solid()
    b1.fill.fore_color.rgb = COLOR_CARD_BG
    b1.line.color.rgb = COLOR_LIGHT_GRAY
    tf_b1 = b1.text_frame
    tf_b1.word_wrap = True
    tf_b1.margin_left = Inches(0.4)
    tf_b1.margin_top = Inches(0.5)

    p = tf_b1.paragraphs[0]
    p.text = "Problem"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    p_txt = tf_b1.add_paragraph()
    p_txt.text = "Genetic multigene testing frequently produces uncertain splicing findings, with no answer key to guide surgical and screening decisions."
    p_txt.font.size = Pt(17)
    p_txt.font.color.rgb = COLOR_CHARCOAL
    p_txt.space_before = Pt(16)

    # Box 2: Solution
    b2 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(2.2), box_w, box_h)
    b2.fill.solid()
    b2.fill.fore_color.rgb = COLOR_CARD_BG
    b2.line.color.rgb = COLOR_LIGHT_GRAY
    tf_b2 = b2.text_frame
    tf_b2.word_wrap = True
    tf_b2.margin_left = Inches(0.4)
    tf_b2.margin_top = Inches(0.5)

    p = tf_b2.paragraphs[0]
    p.text = "Solution"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL

    p_txt = tf_b2.add_paragraph()
    p_txt.text = "An empirical benchmark connecting AlphaGenome's 100 kb context to 446 experimental SpliceVarDB results, calibrated into 5 reliable clinical tiers and rendered in an interactive report."
    p_txt.font.size = Pt(17)
    p_txt.font.color.rgb = COLOR_CHARCOAL
    p_txt.space_before = Pt(16)

    # Box 3: Impact
    b3 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(13.2), Inches(2.2), box_w, box_h)
    b3.fill.solid()
    b3.fill.fore_color.rgb = COLOR_CARD_BG
    b3.line.color.rgb = COLOR_LIGHT_GRAY
    tf_b3 = b3.text_frame
    tf_b3.word_wrap = True
    tf_b3.margin_left = Inches(0.4)
    tf_b3.margin_top = Inches(0.5)

    p = tf_b3.paragraphs[0]
    p.text = "Impact"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK_TEAL

    p_txt = tf_b3.add_paragraph()
    p_txt.text = "A practical decision support tool that prevents unnecessary prophylactic surgeries for benign mimics, uncovers deep hidden cancer drivers, and accelerates life-saving care."
    p_txt.font.size = Pt(17)
    p_txt.font.color.rgb = COLOR_CHARCOAL
    p_txt.space_before = Pt(16)

    add_speaker_note(s8, (
        "[Slide 7: Conclusion]\n"
        "To summarize: genetic testing frequently produces uncertain splicing findings with no answer key to guide clinical decisions. "
        "My solution is an empirical benchmark connecting AlphaGenome's 100 kb foundation model to 446 experimental SpliceVarDB results, calibrated into 5 reliable tiers within an interactive report. "
        "The impact is actionable precision medicine: preventing unnecessary prophylactic surgeries for benign mimics, uncovering hidden deep-intronic cancer drivers, and giving doctors the confidence to act when every day counts."
    ))

    # =========================================================================
    # SLIDE 9: ACKNOWLEDGEMENT & CONTACT
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, COLOR_WHITE)

    # Left: Contact
    c_box = s9.shapes.add_textbox(Inches(1.8), Inches(4.0), Inches(8.5), Inches(4.2))
    tf_c = c_box.text_frame
    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "CONTACT"
    p_c1.font.size = Pt(18)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_TEAL

    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Ivana Sánchez Olivares"
    p_c2.font.size = Pt(22)
    p_c2.font.bold = True
    p_c2.font.color.rgb = COLOR_CHARCOAL
    p_c2.space_before = Pt(8)

    p_c3 = tf_c.add_paragraph()
    p_c3.text = "Email: ivana.schz27@gmail.com"
    p_c3.font.size = Pt(16)
    p_c3.font.color.rgb = COLOR_GRAY
    p_c3.space_before = Pt(3)

    p_c4 = tf_c.add_paragraph()
    p_c4.text = "Shachi Bhavsar"
    p_c4.font.size = Pt(22)
    p_c4.font.bold = True
    p_c4.font.color.rgb = COLOR_CHARCOAL
    p_c4.space_before = Pt(12)

    p_c5 = tf_c.add_paragraph()
    p_c5.text = "Email: shachimbhavsar@gmail.com"
    p_c5.font.size = Pt(16)
    p_c5.font.color.rgb = COLOR_GRAY
    p_c5.space_before = Pt(3)

    # Right: Acknowledgements
    ack_box = s9.shapes.add_textbox(Inches(10.5), Inches(4.5), Inches(8.5), Inches(3.0))
    tf_ack = ack_box.text_frame
    p_a1 = tf_ack.paragraphs[0]
    p_a1.text = "ACKNOWLEDGEMENT"
    p_a1.font.size = Pt(18)
    p_a1.font.bold = True
    p_a1.font.color.rgb = COLOR_TEAL

    p_a2 = tf_ack.add_paragraph()
    p_a2.text = "Thank you for your attention!"
    p_a2.font.size = Pt(24)
    p_a2.font.bold = True
    p_a2.font.color.rgb = COLOR_CHARCOAL
    p_a2.space_before = Pt(10)

    p_a3 = tf_ack.add_paragraph()
    p_a3.text = "• Google DeepMind AlphaGenome Team\n• UCSC SpliceVarDB Research Consortium"
    p_a3.font.size = Pt(16)
    p_a3.font.color.rgb = COLOR_GRAY
    p_a3.space_before = Pt(8)

    add_speaker_note(s9, (
        "[Thank you]\n"
        "I would like to acknowledge Google DeepMind and the SpliceVarDB Consortium for their open scientific datasets. "
        "Thank you very much for your attention. I am driven to make an impact in health, and I would love to help translate foundation AI into compassionate, life-saving clinical decisions."
    ))

    prs.save(OUTPUT_PATH)
    print(f"[SUCCESS] Generated {OUTPUT_PATH} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    build_presentation()

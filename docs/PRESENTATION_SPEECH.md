# Presentation Speech & Slide Guide: From Genetic Uncertainty to Clinical Action

**Project:** AlphaGenome × SpliceVarDB: Multigene Panel Decision Support & Clinical AI Assistant  
**Presenters / Authors:** Ivana Sánchez Olivares & Shachi Bhavsar  
**Style Inspiration:** Modeled directly after Ivana's minimalist, clean presentation style from [`AlgaeCal.pptx`](../AlgaeCal.pptx)  
**File Generated:** [`AlphaGenome_Clinical_Decision.pptx`](../AlphaGenome_Clinical_Decision.pptx) (16:9 Widescreen, 20.0" × 11.25", Aileron Typography, Deep Forest Teal `#07795F` accents)  
**Estimated Spoken Time:** ~4.5 to 5.5 minutes  

---

## The Spoken Speech (Word-for-Word Narrative)

### [Introduction — Title Slide]
> *"Hello, everyone. Have you ever wondered what happens when someone takes a genetic test for cancer risk, and the answer comes back as: 'We don't know'?*  
> *My name is Ivana, and together with Shachi, today we will talk about evaluating Variants of Uncertain Significance in BRCA1 using foundation models and experimental splicing benchmarks."*

---

### [Slide 1: What is RNA splicing?]
> *"All our cells rely on protective proteins like BRCA1 to prevent tumor formation. But genes are not continuous stories; they are interrupted by long non-coding sequences called introns.*  
> *RNA splicing is the cellular process that cuts out these non-coding interruptions and stitches the coding exons together into one functional message.*  
> *Splicing relies on precise chemical recognition signals at exon boundaries. When a genetic mutation disrupts these signals, the cell cuts out vital parts of the gene or keeps broken fragments, destroying the protein and dramatically raising the risk of cancer."*

---

### [Slide 2: Problem]
> *"Until recently, standard genetic testing only checked simple protein-coding changes. New multigene panels now sequence entire genes, identifying thousands of non-coding and splice-region variants.*  
> *However, this comes with major challenges:*  
> *Up to 30% of multigene panel findings are classified as Variants of Uncertain Significance, leaving doctors unable to act.*  
> *Conventional prediction tools rely on distance heuristics, missing mutations that hide deep inside introns while raising false alarms on benign mimics.*  
> *And there is no calibrated answer key to translate raw computer predictions into clinical patient management.*  
> *That is why my goal was to benchmark DeepMind’s AlphaGenome foundation model against experimental ground truth and build a clinical decision support report."*

---

### [Slide 3: Data]
> *"To do this, I obtained experimental ground truth from SpliceVarDB across 446 human BRCA1 variants.*  
> *In these laboratory studies, scientists physically tested human cells using minigene assays and patient RNA sequencing to measure whether each mutation truly breaks RNA splicing or leaves it completely intact.*  
> *This gave us our gold-standard answer key of 230 verified neutral variants and 131 verified splice-altering mutations."*

---

### [Slide 4: Model]
> *"I evaluated Google DeepMind's AlphaGenome foundation model.*  
> *Unlike traditional tools that only look at one or two letters right at the boundary, AlphaGenome reads 100,000 letters of human DNA context at once.*  
> *It predicts disruptions to donor sites, acceptor sites, and splice junctions, allowing it to capture long-range regulatory effects and cryptic splice activations that local tools completely miss."*

---

### [Slide 5: Results]
> *"When evaluated against the experimental ground truth, AlphaGenome achieved an overall ROC AUC of 0.980, and reached 0.993 on intronic variants, significantly beating the distance baseline of 0.914.*  
> *At the optimal cutoff of 0.276, it achieved 94.3% sensitivity and 95.8% specificity.*  
> *To make this actionable for doctors, I converted the scores into 5 empirical calibration tiers with 95% Wilson confidence intervals.*  
> *In Tier 1, the risk of a splicing defect is under 1.5%, safely ruling out damage.*  
> *In Tier 5, 68 out of 68 variants were experimentally confirmed to disrupt splicing—giving 100% precision to support clinical reclassification."*

---

### [Slide 6: Clinical Application]
> *"I implemented this in a hospital-grade decision report for a representative patient, Sarah Jenkins, a 39-year-old woman with personal and maternal breast cancer history whose panel test returned three uncertain BRCA1 findings.*  
> *The report triages all three on one screen:*  
> *Finding 1 is placed in Tier 5 as the true pathogenic driver, directing high-risk surveillance and prophylactic counseling.*  
> *Finding 2 is in Tier 1, ruling out splicing and preventing an unnecessary mastectomy.*  
> *Finding 3 is in Tier 4, flagging a hidden mutation for expedited RNA validation.*  
> *A side-by-side AI assistant answers clinical questions at zero API cost, and a 1-click button exports notes straight into the hospital's health record."*

---

### [Slide 7: Conclusion]
> *"To summarize:*  
> *• **Problem:** Genetic testing frequently produces uncertain splicing findings with no answer key to guide clinical decisions.*  
> *• **Solution:** An empirical benchmark connecting AlphaGenome's 100 kb foundation model to 446 experimental SpliceVarDB results, calibrated into 5 reliable tiers within an interactive report.*  
> *• **Impact:** Actionable precision medicine—preventing unnecessary prophylactic surgeries for benign mimics, uncovering hidden deep-intronic cancer drivers, and giving doctors the confidence to act when every day counts."*

---

### [Thank You]
> *"I would like to acknowledge Google DeepMind and the SpliceVarDB Consortium for their open scientific datasets.*  
> *Thank you very much for your attention. I am driven to make an impact in health, and I would love to help translate foundation AI into compassionate, life-saving clinical decisions."*

---

## Slide Architecture & Visual Mapping

| Slide | Category Tracker | Slide Title | Visual Content & Layout | Corresponding Speech Segment |
| :---: | :--- | :--- | :--- | :--- |
| **0** | `TITLE` | **Evaluating Variants of Uncertain Significance in BRCA1** | Minimalist title, subtitle, Ivana Sánchez Olivares & Shachi Bhavsar. | *Introduction: Have you ever wondered...* |
| **1** | `BACKGROUND` | **What is RNA splicing?** | Left: All cells read genes &bull; Non-coding interruptions.<br/>Right: Splicing mechanism &bull; Boundaries &bull; Cancer risk. | *All our cells rely on protective proteins...* |
| **2** | `PROBLEM` | **Measuring splicing impact in genetic testing** | Left: Before vs. Now.<br/>Right: 3 Challenges &bull; VUS rate &bull; Blind spots &bull; Goal statement. | *Until recently, standard genetic testing...* |
| **3** | `SOLUTION: METHODOLOGY` | **Experimental ground truth from SpliceVarDB** | 3 Cards: 446 Variants &bull; Laboratory Assays &bull; Label Breakdown.<br/>Bottom: AJHG 2024 citation. | *To do this, I obtained experimental ground truth...* |
| **4** | `SOLUTION: METHODOLOGY` | **AlphaGenome 100 kb sequence context model** | Left: 100 kb sequence window &bull; DeepMind model.<br/>Right: Donor/Acceptor loss &bull; Cryptic activation.<br/>Bottom: Nature 2026 citation. | *I evaluated Google DeepMind's AlphaGenome...* |
| **5** | `SOLUTION: METHODOLOGY & RESULTS` | **Benchmark performance & 5-tier empirical calibration** | Left: ROC AUC 0.980, Intronic 0.993, Embedded ROC plot.<br/>Right: 5 Tiers (Tier 1: <1.5% to Tier 5: 100%). | *When evaluated against the experimental ground truth...* |
| **6** | `CLINICAL APPLICATION` | **Multigene panel triage: Sarah Jenkins (39F)** | 3 Finding Cards: Finding #1 (Tier 5: Driver), Finding #2 (Tier 1: Mimic), Finding #3 (Tier 4: Candidate). | *I implemented this in a hospital-grade report...* |
| **7** | `CONCLUSION` | **Calibrated foundation models empower precision cancer decisions** | 3 Clean Boxes matching AlgaeCal Slide 9: **Problem** &bull; **Solution** &bull; **Impact**. | *To summarize: Problem, Solution, Impact...* |
| **8** | `CONTACT` | **ACKNOWLEDGEMENT & CONTACT** | Left: Contact info (Ivana & Shachi).<br/>Right: Acknowledgements & Thank you note. | *I would like to acknowledge Google DeepMind...* |

---

## File Deliverable

The PowerPoint presentation is saved at:
- **[`AlphaGenome_Clinical_Decision.pptx`](../AlphaGenome_Clinical_Decision.pptx)**

Every slide includes the full, corresponding spoken narrative pre-loaded into PowerPoint's **Speaker Notes**, allowing smooth delivery in presenter mode.

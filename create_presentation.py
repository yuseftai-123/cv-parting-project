import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    NAVY = RGBColor(15, 23, 42)        # #0F172A
    DARK_CARD = RGBColor(30, 41, 59)   # #1E293B
    CYAN = RGBColor(6, 182, 212)       # #06B6D4
    EMERALD = RGBColor(16, 185, 129)   # #10B981
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    LIGHT_CARD = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(226, 232, 240)
    SLATE_TEXT = RGBColor(71, 85, 105)
    MUTED_TEXT = RGBColor(148, 163, 184)
    ACCENT_BLUE = RGBColor(37, 99, 235) # #2563EB

    # Paths
    BASE_DIR = os.getcwd()
    LOGOS_DIR = os.path.join(BASE_DIR, "logos")
    SCREENSHOTS_DIR = os.path.join(BASE_DIR, "raport de stage")
    ARTIFACTS_DIR = r"C:\Users\pc\.gemini\antigravity-ide\brain\9ac29789-752b-4c31-a5ce-ae08592cf47e"

    LOGO_KINOVA = os.path.join(LOGOS_DIR, "kinovatech_logo.png")
    LOGO_EST = os.path.join(LOGOS_DIR, "est_umi_logo.png")

    IMG_HERO = os.path.join(ARTIFACTS_DIR, "cover_hero_banner_1786462286050.png")
    IMG_ARCH = os.path.join(ARTIFACTS_DIR, "architecture_pipeline_diagram_1786462298048.png")
    IMG_CNDP = os.path.join(ARTIFACTS_DIR, "cndp_privacy_shield_1786462311105.png")
    IMG_MOCKUP = os.path.join(ARTIFACTS_DIR, "dashboard_saas_ui_mockup_1786462323171.png")
    IMG_SPACY = os.path.join(ARTIFACTS_DIR, "spacy_ner_nlp_graphic_1786462339116.png")
    IMG_KPI = os.path.join(ARTIFACTS_DIR, "performance_kpi_graphics_1786462350144.png")
    IMG_ROADMAP = os.path.join(ARTIFACTS_DIR, "roadmap_tech_graphic_1786462361268.png")

    # Real App Screenshots
    SHOT_1 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160135.png")
    SHOT_2 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160147.png")
    SHOT_3 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160155.png")
    SHOT_4 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160253.png")
    SHOT_5 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160409.png")
    SHOT_SWAGGER = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160819.png")
    SHOT_TESTS = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 161223.png")

    def set_slide_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def safe_add_picture(slide, img_path, left, top, width=None, height=None):
        if os.path.exists(img_path):
            try:
                if width and height:
                    return slide.shapes.add_picture(img_path, left, top, width, height)
                elif width:
                    return slide.shapes.add_picture(img_path, left, top, width=width)
                elif height:
                    return slide.shapes.add_picture(img_path, left, top, height=height)
                else:
                    return slide.shapes.add_picture(img_path, left, top)
            except Exception as e:
                print(f"Warning: Could not add picture {img_path}: {e}")
        return None

    def add_header(slide, slide_num, title, subtitle):
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(0.15), Inches(0.8))
        bar.fill.solid()
        bar.fill.fore_color.rgb = CYAN
        bar.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(1.1), Inches(0.35), Inches(9.5), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = f"{slide_num}. {title}"
        p1.font.name = "Arial"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = "Calibri"
        p2.font.size = Pt(13)
        p2.font.color.rgb = SLATE_TEXT

        # Add top right small company logos
        safe_add_picture(slide, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.6))
        safe_add_picture(slide, LOGO_EST, Inches(12.1), Inches(0.35), height=Inches(0.6))

    # ==========================================
    # SLIDE 1: Title Slide (Dark Theme + Hero + Logos)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide1, NAVY)

    # Hero Banner Background / Side Image
    safe_add_picture(slide1, IMG_HERO, Inches(7.2), Inches(0.8), width=Inches(5.5))

    # Logos on Cover
    safe_add_picture(slide1, LOGO_EST, Inches(1.0), Inches(0.6), height=Inches(0.85))
    safe_add_picture(slide1, LOGO_KINOVA, Inches(2.6), Inches(0.6), height=Inches(0.85))

    # Title box
    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.0), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PARSING INTELLIGENT DE CVS & ANONYMISATION PII (LOI 09-08)"
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Architecture 3-Layer (Regex, spaCy NER, LLM) & Dashboard RH SaaS"
    p2.font.name = "Calibri"
    p2.font.size = Pt(15)
    p2.font.color.rgb = CYAN

    # Info cards container
    cards = [
        ("CANDIDAT", "Youssef TAICHA\nDUT Génie Informatique"),
        ("ÉTABLISSEMENT", "EST Meknès\nUniversité Moulay Ismaïl"),
        ("ENTREPRISE", "Kinova Tech (Remote)\nhttps://kinovatech.com"),
        ("ENCADRANT", "Prof. A. ABOULFARAJ\nESTM & Kinova Tech")
    ]

    for i, (head, val) in enumerate(cards):
        row = i // 2
        col_idx = i % 2
        left_pos = Inches(1.0 + col_idx * 2.9)
        top_pos = Inches(4.2 + row * 1.4)

        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(2.75), Inches(1.25))
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = CYAN

        tb_card = slide1.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.1), Inches(2.45), Inches(1.05))
        tf_c = tb_card.text_frame
        tf_c.word_wrap = True

        p_h = tf_c.paragraphs[0]
        p_h.text = head
        p_h.font.name = "Arial"
        p_h.font.size = Pt(10)
        p_h.font.bold = True
        p_h.font.color.rgb = EMERALD

        p_v = tf_c.add_paragraph()
        p_v.text = val
        p_v.font.name = "Calibri"
        p_v.font.size = Pt(11)
        p_v.font.color.rgb = WHITE

    tb_foot = slide1.shapes.add_textbox(Inches(7.2), Inches(6.6), Inches(5.5), Inches(0.5))
    p_f = tb_foot.text_frame.paragraphs[0]
    p_f.text = "Soutenance DUT Génie Informatique — 2025 / 2026"
    p_f.font.name = "Calibri"
    p_f.font.size = Pt(12)
    p_f.font.color.rgb = MUTED_TEXT

    # ==========================================
    # SLIDE 2: Cadre du Stage & Kinova Tech
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide2, LIGHT_BG)
    add_header(slide2, "01", "Cadre du Stage & Présentation de Kinova Tech", "Contexte académique (ESTM - UMI) et organisation professionnelle en télétravail")

    # Logos display card
    logo_card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2))
    logo_card.fill.solid()
    logo_card.fill.fore_color.rgb = LIGHT_CARD
    logo_card.line.color.rgb = BORDER_COLOR

    safe_add_picture(slide2, LOGO_EST, Inches(1.2), Inches(2.0), width=Inches(2.8))
    safe_add_picture(slide2, LOGO_KINOVA, Inches(1.1), Inches(4.2), width=Inches(3.0))

    tb_lc = slide2.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(3.2), Inches(0.8))
    p_lc = tb_lc.text_frame.paragraphs[0]
    p_lc.text = "Partenariat Académique & Entreprise"
    p_lc.font.name = "Arial"
    p_lc.font.size = Pt(12)
    p_lc.font.bold = True
    p_lc.font.color.rgb = NAVY
    p_lc.alignment = PP_ALIGN.CENTER

    cards_s2 = [
        ("EST Meknès (UMI)", "Établissement d'Origine", [
            "Université Moulay Ismaïl (ESTM).",
            "Département Génie Informatique.",
            "Formation axée sur l'ingénierie logicielle, l'IA et la sécurité des systèmes d'information."
        ], ACCENT_BLUE),
        ("Kinova Tech (Casablanca)", "Entreprise d'Accueil", [
            "Société d'ingénierie & conseil IT (https://kinovatech.com).",
            "Pôle IA, Cybersécurité & Transformation Numérique Souveraine.",
            "Modalité du stage à distance (Remote / Télétravail)."
        ], CYAN),
    ]

    for i, (title, subtitle, bullets, accent_col) in enumerate(cards_s2):
        left_pos = Inches(4.7 + i * 4.0)
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.6), Inches(3.8), Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_CARD
        card.line.color.rgb = BORDER_COLOR

        top_bar = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, Inches(1.6), Inches(3.8), Inches(0.12))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = accent_col
        top_bar.line.fill.background()

        tb_c = slide2.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.9), Inches(3.4), Inches(4.7))
        tf_c = tb_c.text_frame
        tf_c.word_wrap = True

        p1 = tf_c.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf_c.add_paragraph()
        p2.text = subtitle
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = accent_col

        tf_c.add_paragraph()

        for b in bullets:
            pb = tf_c.add_paragraph()
            pb.text = "• " + b
            pb.font.name = "Calibri"
            pb.font.size = Pt(13)
            pb.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 3: Problématique & Objectifs
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide3, LIGHT_BG)
    add_header(slide3, "02", "Problématique Métier & Objectifs du Projet", "Transition du traitement manuel des CVs vers un moteur intelligent et conforme CNDP")

    # Left Box - Problématique
    left_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = LIGHT_CARD
    left_card.line.color.rgb = BORDER_COLOR

    top_l = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.12))
    top_l.fill.solid()
    top_l.fill.fore_color.rgb = RGBColor(239, 68, 68)
    top_l.line.fill.background()

    tb_l = slide3.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p_lt = tf_l.paragraphs[0]
    p_lt.text = "⚠️ Problématique & Défis Métier RH"
    p_lt.font.name = "Arial"
    p_lt.font.size = Pt(17)
    p_lt.font.bold = True
    p_lt.font.color.rgb = NAVY

    problems = [
        "Volume massif & formats hétérogènes : CVs PDF et DOCX non structurés.",
        "Traitement manuel chronophage : Plus de 10 min par candidature.",
        "Risque légal élevé de fuite PII : Données personnelles exposées sans masquage.",
        "Non-conformité CNDP : Risque d'infraction à la Loi marocaine n° 09-08."
    ]
    for p in problems:
        pb = tf_l.add_paragraph()
        pb.text = "✖ " + p
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # Embedded screenshot sample inside problem box
    safe_add_picture(slide3, SHOT_1, Inches(1.1), Inches(4.5), width=Inches(5.0))

    # Right Box - Objectifs
    right_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_CARD
    right_card.line.color.rgb = BORDER_COLOR

    top_r = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(0.12))
    top_r.fill.solid()
    top_r.fill.fore_color.rgb = EMERALD
    top_r.line.fill.background()

    tb_r = slide3.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.0), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "🎯 Objectifs de la Solution KINOVATECH"
    p_rt.font.name = "Arial"
    p_rt.font.size = Pt(17)
    p_rt.font.bold = True
    p_rt.font.color.rgb = NAVY

    objectives = [
        "Moteur Hybride 3-Layer : Anonymisation Regex, spaCy NER & Résumé LLM.",
        "Anonymisation PII Stricte (Loi 09-08) : Zero PII brute avec Security Gate.",
        "Traitement Batch ZIP (SF-09) : Ingestion jusqu'à 500 CVs simultanément.",
        "Dashboard SaaS React Moderne : Interface réactive avec filtres SQL avancés."
    ]
    for o in objectives:
        pb = tf_r.add_paragraph()
        pb.text = "✔ " + o
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    safe_add_picture(slide3, IMG_CNDP, Inches(7.2), Inches(4.3), width=Inches(5.0))

    # ==========================================
    # SLIDE 4: Architecture Globale (Visual Diagram)
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide4, LIGHT_BG)
    add_header(slide4, "03", "Architecture Globale & Pipeline en 8 Étapes", "Moteur de parsing hybride 3-Couches (Deterministic Regex + spaCy NER + LLM Enrichment)")

    # Architecture Image Graphic Centered
    safe_add_picture(slide4, IMG_ARCH, Inches(0.8), Inches(1.6), width=Inches(7.2))

    # Right side explanation card
    right_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.6), Inches(4.2), Inches(5.2))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = LIGHT_CARD
    right_card.line.color.rgb = BORDER_COLOR

    tb = slide4.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(3.8), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🔍 Description du Pipeline"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    steps = [
        "1-2. Ingestion PyMuPDF / python-docx & Détection de langue.",
        "3-4. Layer 1 : Masquage Regex PII -> Jetons [NOM_1], [TEL_1].",
        "5. Layer 2 : Extraction spaCy NER (fr_core_news_lg).",
        "6. Layer 3 : Assertion assert_no_raw_pii_before_llm & LLM Summary.",
        "7-8. Validation Pydantic v2 & Stockage PostgreSQL / MinIO."
    ]
    for s in steps:
        pb = tf.add_paragraph()
        pb.text = "• " + s
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 5: Couche 1 - Anonymisation PII (Loi 09-08)
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide5, LIGHT_BG)
    add_header(slide5, "04", "Couche 1 : Anonymisation PII & Conformité CNDP", "Protection intégrale des données personnelles selon la Loi marocaine n° 09-08")

    # Left Graphic
    safe_add_picture(slide5, IMG_CNDP, Inches(0.8), Inches(1.6), width=Inches(5.0))

    # Right Content Card
    card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.1), Inches(1.6), Inches(6.4), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_CARD
    card.line.color.rgb = BORDER_COLOR

    tb = slide5.shapes.add_textbox(Inches(6.4), Inches(1.8), Inches(5.8), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🛡️ Principes de Securité & CNDP (Loi 09-08)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    cndp_points = [
        "Articles 4 & 5 (Minimisation) : Substitution systématique des PII brutes par des jetons neutres ([NOM_1], [EMAIL_1], [TEL_1], [CIN_1]).",
        "Article 7 (Droit à l'oubli) : Endpoint de suppression définitive et en cascade des profils et fichiers sources.",
        "Article 23 (Isolation) : Stockage isolé MinIO et logs d'exécution anonymisés sans trace de PII.",
        "Security Gate Pre-LLM (SF-07) : Assertion bloquante assert_no_raw_pii_before_llm() qui annule tout appel API LLM externe en cas de PII non masquée."
    ]
    for cp in cndp_points:
        pb = tf.add_paragraph()
        pb.text = "✔ " + cp
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 6: Couche 2 - Extraction spaCy NER
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide6, LIGHT_BG)
    add_header(slide6, "05", "Couche 2 : Extraction d'Entités Nommées (spaCy NER)", "Analyse sémantique NLP et validation stricte du schéma JSON Pydantic v2")

    # Left Graphic
    safe_add_picture(slide6, IMG_SPACY, Inches(0.8), Inches(1.6), width=Inches(5.0))

    # Right Content Card
    card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.1), Inches(1.6), Inches(6.4), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_CARD
    card.line.color.rgb = BORDER_COLOR

    tb = slide6.shapes.add_textbox(Inches(6.4), Inches(1.8), Inches(5.8), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "⚙️ Reconnaissance d'Entités & Pydantic v2"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    ner_points = [
        "Modèle NLP fr_core_news_lg : Traitement du langage naturel optimisé pour les CVs en français.",
        "Extraction Contextuelle : Identification des intitulés de postes, diplômes, compétences et dates d'expérience.",
        "Validation Pydantic v2 (Section 3.3) : Validation stricte des types et structure JSON des profils candidats.",
        "Compatibilité SQL : Garantie de correspondance parfaite avec le schéma de base de données PostgreSQL."
    ]
    for np in ner_points:
        pb = tf.add_paragraph()
        pb.text = "• " + np
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 7: Couche 3 - FastAPI REST Backend
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide7, LIGHT_BG)
    add_header(slide7, "06", "Couche 3 : Enrichissement LLM & API REST FastAPI", "Architecture Backend FastAPI haute performance et documentation Swagger OpenAPI")

    # Left Screenshot (Swagger UI)
    safe_add_picture(slide7, SHOT_SWAGGER, Inches(0.8), Inches(1.6), width=Inches(5.5))

    # Right Endpoints Breakdown
    card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.6), Inches(5.9), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_CARD
    card.line.color.rgb = BORDER_COLOR

    tb = slide7.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.5), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🔌 Endpoints API REST (FastAPI)"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    ep_list = [
        ("GET /api/v1/health", "Diagnostic système (Postgres, Redis, MinIO)."),
        ("POST /api/v1/cvs/upload", "Upload & parsing unitaire d'un CV (.pdf, .docx)."),
        ("POST /api/v1/cvs/batch", "Ingestion d'archives ZIP jusqu'à 500 CVs."),
        ("POST /api/v1/cvs/search", "Recherche SQL par compétences, expérience et langue.")
    ]
    for ep_name, ep_desc in ep_list:
        p_name = tf.add_paragraph()
        p_name.text = ep_name
        p_name.font.name = "Arial"
        p_name.font.size = Pt(12)
        p_name.font.bold = True
        p_name.font.color.rgb = CYAN

        p_desc = tf.add_paragraph()
        p_desc.text = ep_desc
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 8: Interface Utilisateur - Dashboard SaaS
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide8, LIGHT_BG)
    add_header(slide8, "07", "Interface Utilisateur : Dashboard React SaaS", "Tableau de bord RH moderne, réactif et optimisé (Build Vite: 1.89s)")

    # Dashboard Mockup / Screenshot
    safe_add_picture(slide8, SHOT_2, Inches(0.8), Inches(1.6), width=Inches(6.5))

    # Feature List Card
    card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(1.6), Inches(5.0), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_CARD
    card.line.color.rgb = BORDER_COLOR

    tb = slide8.shapes.add_textbox(Inches(7.7), Inches(1.8), Inches(4.6), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "✨ Fonctionnalités Dashboard"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    fe_points = [
        "Design Tokens SaaS : Vanilla CSS3 modulaire avec support Dark / Light mode.",
        "Monitoring API : Jauges de statut et métriques en temps réel.",
        "Modal Drag & Drop : Ingestion simplifiée des CVs uniques et archives ZIP.",
        "Tiroir d'Inspection Candidat : Visualisation détaillée des profils avec toggle de masquage PII."
    ]
    for fp in fe_points:
        pb = tf.add_paragraph()
        pb.text = "• " + fp
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 9: Base de Données & Tests Pytest
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide9, LIGHT_BG)
    add_header(slide9, "08", "Persistance, Infrastructure & Tests Automatisés", "Modélisation relationnelle PostgreSQL, Docker Compose et suite de 44 tests Pytest")

    # Left side test output screenshot
    safe_add_picture(slide9, SHOT_TESTS, Inches(0.8), Inches(1.6), width=Inches(5.5))

    # Right side explanation card
    card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.6), Inches(5.9), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_CARD
    card.line.color.rgb = BORDER_COLOR

    tb = slide9.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.5), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🧪 Assurance Qualité & Persistance"
    p.font.name = "Arial"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY

    test_points = [
        "Base PostgreSQL & MinIO : Persistance relationnelle via SQLAlchemy et stockage d'objets pour les CVs originaux.",
        "Conteneurisation Docker Compose : Services PostgreSQL 15, Redis Cache et MinIO isolés.",
        "Suite Pytest (44 Tests Validés) : 100% de réussite sur l'ensemble de la suite de tests (PII, NER, Batch, Search).",
        "Tests d'Intégration CNDP : Validation end-to-end de l'absence de fuite PII."
    ]
    for tp in test_points:
        pb = tf.add_paragraph()
        pb.text = "✔ " + tp
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # ==========================================
    # SLIDE 10: Résultats Chiffrés (KPI Graphics)
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide10, LIGHT_BG)
    add_header(slide10, "09", "Résultats Chiffrés & Performance Métier", "Indicateurs clés de performance (KPIs) et benchmarks d'exécution")

    # KPI Graphics centered
    safe_add_picture(slide10, IMG_KPI, Inches(0.8), Inches(1.6), width=Inches(6.2))

    # Metric stat cards right side
    metrics = [
        ("< 0.5 s", "Temps moyen par CV", CYAN),
        ("100 %", "Garantie Zero Fuite PII", EMERALD),
        ("44 / 44", "Tests Pytest Validés", ACCENT_BLUE),
        ("500 CVs", "Capacité Batch ZIP", NAVY)
    ]

    for i, (val, label, col) in enumerate(metrics):
        row = i // 2
        col_idx = i % 2
        left_pos = Inches(7.2 + col_idx * 2.8)
        top_pos = Inches(1.8 + row * 2.4)

        card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, top_pos, Inches(2.6), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_CARD
        card.line.color.rgb = BORDER_COLOR

        top_b = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_pos, top_pos, Inches(2.6), Inches(0.1))
        top_b.fill.solid()
        top_b.fill.fore_color.rgb = col
        top_b.line.fill.background()

        tb = slide10.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.2), Inches(2.3), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = "Arial"
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 11: Démonstration Visuelle (Real App Screenshots Showcase)
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide11, LIGHT_BG)
    add_header(slide11, "10", "Démonstration Visuelle du Dashboard RH", "Captures réelles des parcours utilisateurs de l'application SaaS")

    # Display 2 real app screenshots side by side
    safe_add_picture(slide11, SHOT_4, Inches(0.8), Inches(1.6), width=Inches(5.6))
    safe_add_picture(slide11, SHOT_5, Inches(6.9), Inches(1.6), width=Inches(5.6))

    tb_desc = slide11.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.0))
    tf_d = tb_desc.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "💡 Aperçu en direct : Filtrage dynamique des candidats (gauche) et consultation sécurisée de la fiche candidat avec masquage PII (droite)."
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 12: Conclusion & Perspectives (ROADMAP)
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide12, LIGHT_BG)
    add_header(slide12, "11", "Conclusion & Perspectives d'Évolution", "Bilan académique/professionnel du stage et feuille de route technique (ROADMAP)")

    # Left Box - Bilan
    box_c = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    box_c.fill.solid()
    box_c.fill.fore_color.rgb = LIGHT_CARD
    box_c.line.color.rgb = BORDER_COLOR

    top_c = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.12))
    top_c.fill.solid()
    top_c.fill.fore_color.rgb = EMERALD
    top_c.line.fill.background()

    tb_c = slide12.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(5.0), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p_ct = tf_c.paragraphs[0]
    p_ct.text = "🎓 Bilan du Stage (ESTM / Kinova Tech)"
    p_ct.font.name = "Arial"
    p_ct.font.size = Pt(17)
    p_ct.font.bold = True
    p_ct.font.color.rgb = NAVY

    conc_points = [
        "Réalisation complète d'une application d'ingénierie logicielle d'entreprise robuste.",
        "Mise en pratique approfondie de la formation DUT Génie Informatique (EST Meknès).",
        "Maîtrise de la conformité CNDP (Loi 09-08) et de la sécurisation des données sensibles.",
        "Autonomie, rigueur et professionnalisme en modalité Télétravail (Remote)."
    ]
    for cp in conc_points:
        pb = tf_c.add_paragraph()
        pb.text = "✔ " + cp
        pb.font.name = "Calibri"
        pb.font.size = Pt(12)
        pb.font.color.rgb = SLATE_TEXT

    # Right Box - Roadmap Graphic
    safe_add_picture(slide12, IMG_ROADMAP, Inches(6.8), Inches(1.6), width=Inches(5.7))

    # ==========================================
    # SLIDE 13: Remerciements & Q&A (Dark Theme + Logos)
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide13, NAVY)

    # Logos on Thank you slide
    safe_add_picture(slide13, LOGO_EST, Inches(1.0), Inches(0.6), height=Inches(0.9))
    safe_add_picture(slide13, LOGO_KINOVA, Inches(2.6), Inches(0.6), height=Inches(0.9))

    tb13 = slide13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.2))
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    p13 = tf13.paragraphs[0]
    p13.text = "MERCI DE VOTRE ATTENTION !"
    p13.font.name = "Arial"
    p13.font.size = Pt(36)
    p13.font.bold = True
    p13.font.color.rgb = WHITE

    p13_sub = tf13.add_paragraph()
    p13_sub.text = "Je suis à votre entière disposition pour répondre à vos questions."
    p13_sub.font.name = "Calibri"
    p13_sub.font.size = Pt(20)
    p13_sub.font.color.rgb = CYAN

    # Center card for contact info
    c_box = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.2), Inches(11.333), Inches(2.4))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = DARK_CARD
    c_box.line.color.rgb = EMERALD

    tb_cb = slide13.shapes.add_textbox(Inches(1.3), Inches(4.4), Inches(10.7), Inches(2.0))
    tf_cb = tb_cb.text_frame
    tf_cb.word_wrap = True

    p_c1 = tf_cb.paragraphs[0]
    p_c1.text = "Youssef TAICHA — DUT Génie Informatique"
    p_c1.font.name = "Arial"
    p_c1.font.size = Pt(18)
    p_c1.font.bold = True
    p_c1.font.color.rgb = WHITE

    p_c2 = tf_cb.add_paragraph()
    p_c2.text = "Établissement : EST Meknès — Université Moulay Ismaïl (UMI)"
    p_c2.font.name = "Calibri"
    p_c2.font.size = Pt(14)
    p_c2.font.color.rgb = MUTED_TEXT

    p_c3 = tf_cb.add_paragraph()
    p_c3.text = "Entreprise d'Accueil : Kinova Tech (https://kinovatech.com) | Encadrant : Prof. A. ABOULFARAJ"
    p_c3.font.name = "Calibri"
    p_c3.font.size = Pt(14)
    p_c3.font.color.rgb = EMERALD

    output_path_v2 = os.path.join(os.getcwd(), "kinovatech_cv_parser_presentation_v2.pptx")
    prs.save(output_path_v2)
    print(f"Presentation saved to: {output_path_v2}")

    try:
        output_path = os.path.join(os.getcwd(), "kinovatech_cv_parser_presentation.pptx")
        prs.save(output_path)
        print(f"Presentation saved to: {output_path}")
    except Exception as e:
        print(f"Main presentation file locked, saved as kinovatech_cv_parser_presentation_v2.pptx: {e}")

if __name__ == "__main__":
    build_presentation()

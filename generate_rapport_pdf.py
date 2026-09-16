"""
Academic Grade 20-Page Remote Internship Report Generator (PDF)
Updating Company AI Department Head to Prof. A. ABOULFARAJ
"""
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable, Preformatted, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

PAGE_WIDTH, PAGE_HEIGHT = A4

# Color Palette
COLOR_PRIMARY_BLUE = colors.HexColor("#1e3a8a")
COLOR_SECONDARY_BLUE = colors.HexColor("#2563eb")
COLOR_CYAN_ACCENT = colors.HexColor("#0284c7")
COLOR_GOLD = colors.HexColor("#d97706")
COLOR_DARK_TEXT = colors.HexColor("#0f172a")
COLOR_LIGHT_BG = colors.HexColor("#f8fafc")
COLOR_BORDER = colors.HexColor("#cbd5e1")
COLOR_SUCCESS = colors.HexColor("#059669")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        if self._pageNumber in [1, page_count]:
            self.restoreState()
            return

        # Running Header
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(COLOR_PRIMARY_BLUE)
        self.drawString(40, PAGE_HEIGHT - 25, "EST MEKNÈS (UMI) — KINOVATECH")

        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(PAGE_WIDTH - 40, PAGE_HEIGHT - 25, "Rapport de Stage à Distance : Moteur de Parsing CV & Dashboard")

        self.setStrokeColor(COLOR_SECONDARY_BLUE)
        self.setLineWidth(1)
        self.line(40, PAGE_HEIGHT - 30, PAGE_WIDTH - 40, PAGE_HEIGHT - 30)

        # Running Footer
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(40, 35, PAGE_WIDTH - 40, 35)

        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(40, 22, "YOUSSEF TAICHA — Génie Informatique")

        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(PAGE_WIDTH - 40, 22, page_str)
        self.restoreState()

def draw_cover_background(canvas_obj, doc_obj):
    canvas_obj.saveState()
    
    # Top Wave Arcs
    p = canvas_obj.beginPath()
    p.moveTo(0, PAGE_HEIGHT)
    p.lineTo(PAGE_WIDTH, PAGE_HEIGHT)
    p.lineTo(PAGE_WIDTH, PAGE_HEIGHT - 125)
    p.curveTo(PAGE_WIDTH - 150, PAGE_HEIGHT - 185, 150, PAGE_HEIGHT - 85, 0, PAGE_HEIGHT - 145)
    p.close()
    canvas_obj.setFillColor(COLOR_PRIMARY_BLUE)
    canvas_obj.drawPath(p, fill=1, stroke=0)

    p2 = canvas_obj.beginPath()
    p2.moveTo(0, PAGE_HEIGHT)
    p2.lineTo(PAGE_WIDTH, PAGE_HEIGHT)
    p2.lineTo(PAGE_WIDTH, PAGE_HEIGHT - 85)
    p2.curveTo(PAGE_WIDTH - 120, PAGE_HEIGHT - 135, 200, PAGE_HEIGHT - 65, 0, PAGE_HEIGHT - 105)
    p2.close()
    canvas_obj.setFillColor(COLOR_SECONDARY_BLUE)
    canvas_obj.drawPath(p2, fill=1, stroke=0)

    p3 = canvas_obj.beginPath()
    p3.moveTo(PAGE_WIDTH, PAGE_HEIGHT)
    p3.lineTo(PAGE_WIDTH, PAGE_HEIGHT - 55)
    p3.curveTo(PAGE_WIDTH - 80, PAGE_HEIGHT - 95, PAGE_WIDTH - 180, PAGE_HEIGHT - 25, PAGE_WIDTH - 250, PAGE_HEIGHT)
    p3.close()
    canvas_obj.setFillColor(COLOR_GOLD)
    canvas_obj.drawPath(p3, fill=1, stroke=0)

    # Bottom Wave Arcs
    b = canvas_obj.beginPath()
    b.moveTo(0, 0)
    b.lineTo(PAGE_WIDTH, 0)
    b.lineTo(PAGE_WIDTH, 115)
    b.curveTo(PAGE_WIDTH - 180, 45, 120, 155, 0, 75)
    b.close()
    canvas_obj.setFillColor(COLOR_PRIMARY_BLUE)
    canvas_obj.drawPath(b, fill=1, stroke=0)

    b2 = canvas_obj.beginPath()
    b2.moveTo(0, 0)
    b2.lineTo(PAGE_WIDTH, 0)
    b2.lineTo(PAGE_WIDTH, 75)
    b2.curveTo(PAGE_WIDTH - 140, 25, 180, 95, 0, 50)
    b2.close()
    canvas_obj.setFillColor(COLOR_CYAN_ACCENT)
    canvas_obj.drawPath(b2, fill=1, stroke=0)

    canvas_obj.restoreState()

def build_academic_report():
    pdf_path = r"C:\Users\pc\Desktop\RAPPORT_DE_STAGE_YOUSSEF_TAICHA.pdf"
    project_pdf_path = r"c:\Users\pc\Desktop\cv-parting-project\RAPPORT_DE_STAGE.pdf"

    est_logo_path = r"c:\Users\pc\Desktop\cv-parting-project\logos\est_umi_logo.png"
    kino_logo_path = r"c:\Users\pc\Desktop\cv-parting-project\logos\kinovatech_logo.png"

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    style_cover_title = ParagraphStyle("CoverTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=COLOR_PRIMARY_BLUE, alignment=TA_CENTER, spaceAfter=10)
    style_cover_sub = ParagraphStyle("CoverSub", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=COLOR_SECONDARY_BLUE, alignment=TA_CENTER, spaceAfter=18)
    
    style_chapter_h1 = ParagraphStyle("ChapH1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=14.5, leading=18.5, textColor=COLOR_PRIMARY_BLUE, spaceBefore=18, spaceAfter=10, keepWithNext=True)
    style_h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15.5, textColor=COLOR_SECONDARY_BLUE, spaceBefore=14, spaceAfter=7, keepWithNext=True)
    style_body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14.5, textColor=COLOR_DARK_TEXT, alignment=TA_JUSTIFY, spaceAfter=8)
    style_bullet = ParagraphStyle("Bullet", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=13.5, textColor=COLOR_DARK_TEXT, leftIndent=15, spaceAfter=4)
    
    style_code = ParagraphStyle("Code", parent=styles["Normal"], fontName="Courier", fontSize=8, leading=11, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"), borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.8, borderPadding=7, spaceBefore=5, spaceAfter=8)
    
    style_table_header = ParagraphStyle("THeader", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white, alignment=TA_LEFT)
    style_table_cell = ParagraphStyle("TCell", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=11, textColor=COLOR_DARK_TEXT, alignment=TA_LEFT)
    style_table_cell_bold = ParagraphStyle("TCellBold", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=COLOR_PRIMARY_BLUE, alignment=TA_LEFT)

    story = []

    # =========================================================================
    # 1. PAGE DE GARDE
    # =========================================================================
    story.append(Spacer(1, 10))

    img_est = Image(est_logo_path, width=210, height=60) if os.path.exists(est_logo_path) else Paragraph("EST Meknès (UMI)", style_body)
    img_kino = Image(kino_logo_path, width=125, height=70) if os.path.exists(kino_logo_path) else Paragraph("KINOVATECH", style_body)

    logos_table_data = [[img_est, img_kino]]
    logos_table = Table(logos_table_data, colWidths=[270, 200])
    logos_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))

    story.append(logos_table)
    story.append(Spacer(1, 40))

    story.append(Paragraph("RAPPORT DE STAGE À DISTANCE (REMOTE)", style_cover_title))
    story.append(Paragraph(
        "Conception, Développement et Déploiement d'une Application de Parsing Intelligent "
        "de CVs, Anonymisation PII (Loi 09-08 CNDP) et Dashboard RH Moderne",
        style_cover_sub
    ))

    meta_label = ParagraphStyle("MLabel", fontName="Helvetica-Bold", fontSize=9.5, leading=13.5, textColor=COLOR_PRIMARY_BLUE)
    meta_val = ParagraphStyle("MVal", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=COLOR_DARK_TEXT)

    table_data = [
        [Paragraph("Réalisé par :", meta_label), Paragraph("<b>YOUSSEF TAICHA</b>", meta_val)],
        [Paragraph("Filière :", meta_label), Paragraph("Diplôme Universitaire de Technologie (DUT)<br/><b>Génie Informatique</b>", meta_val)],
        [Paragraph("Établissement :", meta_label), Paragraph("EST Meknès — Université Moulay Ismaïl (UMI)", meta_val)],
        [Paragraph("Entreprise d'Accueil :", meta_label), Paragraph("<b>Kinova Tech</b> (Dépt. IA & Direction IT)", meta_val)],
        [Paragraph("Modalité du Stage :", meta_label), Paragraph("<b>À Distance / Remote (Télétravail)</b>", meta_val)],
        [Paragraph("Encadrant Entreprise :", meta_label), Paragraph("<b>Prof. A. ABOULFARAJ</b> (Responsable Dépt. IA — Kinova Tech)", meta_val)],
        [Paragraph("Encadrant Pédagogique :", meta_label), Paragraph("<b>Prof. A. ABOULFARAJ</b> (EST Meknès)", meta_val)],
        [Paragraph("Année Universitaire :", meta_label), Paragraph("2025 / 2026", meta_val)],
    ]

    card_table = Table(table_data, colWidths=[140, 310])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_BG),
        ('BORDER', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    story.append(card_table)
    story.append(PageBreak())

    # =========================================================================
    # 2. REMERCIEMENTS
    # =========================================================================
    story.append(Paragraph("REMERCIEMENTS", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Avant d'entamer la présentation technique de ce rapport de stage réalisé à distance, il m'est particulièrement agréable d'adresser mes remerciements les plus sincères "
        "à Monsieur le Directeur de l'<b>École Supérieure de Technologie de Meknès (ESTM - UMI)</b> ainsi qu'à l'ensemble des enseignants et formateurs du département <b>Génie Informatique</b> "
        "pour la rigueur, l'excellence et la qualité de la formation académique dispensée tout au long de mon cursus universitaire.",
        style_body
    ))

    story.append(Paragraph(
        "Je tiens à exprimer ma gratitude la plus vive à mon encadrant pédagogique à l'EST Meknès, <b>Monsieur le Professeur A. ABOULFARAJ</b>, pour son suivi constant, sa rigueur méthodologique, ses précieux conseils et sa grande disponibilité lors de nos échanges à distance.",
        style_body
    ))

    story.append(Paragraph(
        "J'adresse également mes remerciements les plus chaleureux aux dirigeants et aux équipes techniques de la société <b>Kinova Tech</b> (<u>https://kinovatech.com</u>), et tout particulièrement à mon encadrant professionnel <b>Monsieur le Professeur A. ABOULFARAJ</b>, Responsable du Département IA, "
        "pour m'avoir intégré au sein des équipes R&D en modalité à distance (télétravail), pour la confiance accordée lors des points quotidiens et pour la qualité du sujet proposé.",
        style_body
    ))

    story.append(Paragraph(
        "Enfin, mes remerciements s'adressent à mes camarades de promotion, à ma famille et à toutes les personnes qui ont contribué de près ou de loin à l'aboutissement de ce projet.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 3. SOMMAIRE
    # =========================================================================
    story.append(Paragraph("SOMMAIRE", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    toc_data = [
        ["I.", "Remerciements", "Page 2"],
        ["II.", "Sommaire", "Page 3"],
        ["III.", "Introduction Générale & Organisation à Distance", "Page 4"],
        ["Chap. 1", "Présentation de l'EST Meknès & Fiche Société Kinova Tech", "Page 5"],
        ["Chap. 2", "Analyse des Besoins & Spécifications (SF-01 à SF-10)", "Page 6"],
        ["Chap. 3", "Architecture Technique Globale & Moteur 3-Layer", "Page 7"],
        ["Chap. 4", "Model ORM PostgreSQL & Resilience Autonome SQLite", "Page 8"],
        ["Chap. 5", "Environnement de Travail à Distance & Stack", "Page 9"],
        ["Chap. 6", "Implémentation Détaillée du Pipeline 8 Étapes", "Page 11"],
        ["Chap. 7", "Traitement Batch ZIP (SF-09) & Recherche SQL (SF-10)", "Page 12"],
        ["Chap. 8", "Documentation Swagger OpenAPI & API Reference", "Page 13"],
        ["Chap. 9", "Journalisation & Security Audit Trail", "Page 14"],
        ["Chap. 10", "Dashboard React SaaS & Interface UI/UX Moderne", "Page 15"],
        ["Chap. 11", "Suite de Tests Automatisés Pytest & Benchmark", "Page 16"],
        ["Chap. 12", "Conformité Légale CNDP (Loi marocaine n° 09-08)", "Page 18"],
        ["IV.", "Conclusion Générale & Perspectives (Roadmap ROADMAP.md)", "Page 19"],
        ["V.", "Quatrième de Couverture (Back Cover)", "Page 20"]
    ]

    toc_table = Table(toc_data, colWidths=[55, 355, 60])
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), COLOR_DARK_TEXT),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, COLOR_LIGHT_BG),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), COLOR_PRIMARY_BLUE),
    ]))

    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # 4. INTRODUCTION GÉNÉRALE
    # =========================================================================
    story.append(Paragraph("INTRODUCTION GÉNÉRALE & ORGANISATION À DISTANCE", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Le marché du recrutement et de la gestion du capital humain subit une transformation digitale majeure au Maroc comme à l'international. "
        "Les cabinets de recrutement, agences d'intérim et directions RH des grandes entreprises reçoivent quotidiennement des milliers de candidatures "
        "sous des formats informatiques hétérogènes (PDF, DOCX, images scannées).",
        style_body
    ))

    story.append(Paragraph(
        "Le projet <b>KINOVATECH CV Parser Engine</b> a été confié dans le cadre d'un <b>Stage à Distance (Remote / Télétravail)</b>. "
        "Cette modalité d'organisation s'est appuyée sur des méthodes agiles collaboratives à distance : points de suivi quotidiens (Daily Standup), "
        "revues de code asynchrones sur Git/GitHub, communication continue via messagerie professionnelle et outils de visio-conférence.",
        style_body
    ))

    story.append(Paragraph(
        "L'objectif de ce stage en télétravail était d'élaborer de bout en bout une application autonome capable d'ingérer, d'anonymiser (Loi 09-08 CNDP), "
        "de structurer et d'analyser les CVs en temps réel, tout en garantissant un niveau de sécurité et de conformité légale maximal.",
        style_body
    ))

    story.append(Paragraph(
        "Ce document constitue le rapport de synthèse retraçant l'architecture à 3 couches (Regex déterministe, spaCy NER, LLM Enrichment), "
        "l'implémentation de l'API FastAPI et du Dashboard React SaaS, validés par une suite de 43 tests Pytest.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 5. CHAPITRE 1 : PRÉSENTATION EST MEKNÈS & KINOVA TECH
    # =========================================================================
    story.append(Paragraph("CHAPITRE 1 : PRÉSENTATION DE L'ÉTABLISSEMENT & KINOVA TECH", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph("1.1 Établissement d'Origine : EST Meknès (Université Moulay Ismaïl)", style_h2))
    story.append(Paragraph(
        "L'<b>École Supérieure de Technologie de Meknès (ESTM)</b>, rattachée à l'<b>Université Moulay Ismaïl (UMI)</b> (<u>https://www.est.umi.ac.ma/</u>), "
        "est un établissement public d'enseignement supérieur d'excellence formant des cadres et techniciens supérieurs hautement qualifiés en Génie Informatique.",
        style_body
    ))

    story.append(Paragraph("1.2 Fiche Signalétique de l'Entreprise : Kinova Tech", style_h2))
    story.append(Paragraph(
        "<b>Kinova Tech</b> (<u>https://kinovatech.com</u>) est un cabinet d'ingénierie et de conseil technologique spécialisé dans la transformation numérique souveraine, "
        "l'Intelligence Artificielle et la Cybersécurité.",
        style_body
    ))

    kino_info_data = [
        [Paragraph("Raison Sociale :", style_table_cell_bold), Paragraph("Kinova Tech (KINOVATECH)", style_table_cell)],
        [Paragraph("Site Web Officiel :", style_table_cell_bold), Paragraph("<u>https://kinovatech.com</u>", style_table_cell)],
        [Paragraph("Slogan Institutionnel :", style_table_cell_bold), Paragraph("<i>« Accélérez votre transformation numérique en toute souveraineté »</i>", style_table_cell)],
        [Paragraph("Siège Social :", style_table_cell_bold), Paragraph("IMM 97 B, Av. Hassan Sghir, 4ème Étage, N°126, Casablanca, Maroc", style_table_cell)],
        [Paragraph("Contacts Téléphone :", style_table_cell_bold), Paragraph("+212 661-896943<br/>+212 648-020096 <i>(WhatsApp uniquement)</i>", style_table_cell)],
        [Paragraph("Courriel de Contact :", style_table_cell_bold), Paragraph("contact@kinovatech.com", style_table_cell)],
        [Paragraph("Domaines d'Expertise :", style_table_cell_bold), Paragraph("• <b>Intelligence Artificielle & IA Générative</b><br/>• <b>Cybersécurité & Audit de Gouvernance</b><br/>• <b>Infrastructures & Réseaux Informatiques</b>", style_table_cell)],
        [Paragraph("Modalité du Stage :", style_table_cell_bold), Paragraph("<b>Stage à Distance / Remote (Télétravail)</b>", style_table_cell)],
        [Paragraph("Encadrant Entreprise :", style_table_cell_bold), Paragraph("<b>Prof. A. ABOULFARAJ (Responsable Dépt. IA)</b>", style_table_cell)],
        [Paragraph("Encadrant Pédagogique :", style_table_cell_bold), Paragraph("<b>Prof. A. ABOULFARAJ (EST Meknès)</b>", style_table_cell)],
    ]

    kino_info_table = Table(kino_info_data, colWidths=[140, 325])
    kino_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    story.append(kino_info_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.3 Vision et Atouts Majeurs de Kinova Tech", style_h2))
    story.append(Paragraph(
        "• <b>Notre Vision</b> : Transformer l'Intelligence Artificielle en levier de souveraineté et de performance durable, "
        "en alliant approche prospective, sécurité des données et des systèmes, valorisation de l'expertise humaine et conformité aux exigences de gouvernance numérique.",
        style_bullet
    ))
    story.append(Paragraph(
        "• <b>Approche Pragmatique et Souveraine</b> : Concevoir des solutions concrètes et mesurables à fort ROI, développées dans le respect strict "
        "de la souveraineté numérique et de la protection des données stratégiques (Loi marocaine n° 09-08 / CNDP).",
        style_bullet
    ))
    story.append(Paragraph(
        "• <b>Expertise Pluridisciplinaire</b> : Une équipe d'ingénieurs experts en IA, cybersécurité, infrastructures réseau et ingénierie fonctionnelle pour une transformation globale.",
        style_bullet
    ))

    story.append(PageBreak())

    # =========================================================================
    # 6. CHAPITRE 2 : ANALYSE DES BESOINS (SF-01 À SF-10)
    # =========================================================================
    story.append(Paragraph("CHAPITRE 2 : ANALYSE DES BESOINS & SPÉCIFICATIONS", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Conformément au cahier des charges <i>Cdc_CV_Parser_130726.pdf</i> rédigé par la Direction IA de Kinova Tech, "
        "l'application a été conçue pour satisfaire 10 Spécifications Fonctionnelles (SF) et 5 Spécifications Non-Fonctionnelles (SNF) strictes :",
        style_body
    ))

    raw_spec_data = [
        ["Code SF", "Intitulé Spécification", "Règles Fonctionnelles & Validation Technical"],
        ["SF-01", "Extraction Multi-Format", "Support natif des documents PDF (via PyMuPDF) et DOCX (via python-docx) avec préservation des blocs."],
        ["SF-02", "Détection de Langue", "Analyse automatique de la langue (fr, en, ar) avec fallback automatique sur fr."],
        ["SF-03", "Analyse Structurelle", "Découpage en sections (Profil, Expériences, Formations, Compétences, Langues)."],
        ["SF-04", "Masquage PII Déterministe", "Substitution immédiate des PII (Email, Phone +212, CIN, Date de Naissance, Noms) par des jetons neutres."],
        ["SF-05", "Extraction NER spaCy", "Reconnaissance d'entités nommées via fr_core_news_lg pour capturer Postes, Diplômes et Entreprises."],
        ["SF-06", "Enrichissement LLM", "Génération d'un résumé professionnel structuré à partir des données anonymisées."],
        ["SF-07", "Security Gate Pre-Dispatch", "Assertion bloquante assert_no_raw_pii_before_llm levant une SecurityComplianceError en cas de PII brute."],
        ["SF-08", "Validation Schema Pydantic", "Conformité à 100% avec le schema JSON officiel Section 3.3 du cahier des charges."],
        ["SF-09", "Traitement Batch ZIP", "Endpoint POST /api/v1/cvs/batch acceptant des archives .zip jusqu'à 500 CVs avec rapport consolidé."],
        ["SF-10", "Recherche & Filtrage SQL", "Endpoint POST /api/v1/cvs/search supportant les requêtes multicritères (compétences, min/max exp, langue)."],
    ]

    spec_data = []
    for r_idx, row in enumerate(raw_spec_data):
        new_row = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                new_row.append(Paragraph(cell, style_table_header))
            elif c_idx == 0:
                new_row.append(Paragraph(cell, style_table_cell_bold))
            else:
                new_row.append(Paragraph(cell, style_table_cell))
        spec_data.append(new_row)

    spec_table = Table(spec_data, colWidths=[50, 130, 285])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY_BLUE),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
    ]))

    story.append(spec_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Spécifications Non-Fonctionnelles (SNF) :", style_h2))
    story.append(Paragraph("• <b>SNF-01 (Latence & Performance)</b> : Temps de réponse moyen < 0.5s par CV en exécution chaude.", style_bullet))
    story.append(Paragraph("• <b>SNF-02 (Protection des Données)</b> : Anonymisation déterministe certifiée conforme à la Loi marocaine 09-08 (CNDP).", style_bullet))
    story.append(Paragraph("• <b>SNF-03 (Isolation & Logs Zero-Leak)</b> : Interdiction formelle d'écrire des PII brutes dans les fichiers de logs système.", style_bullet))
    story.append(Paragraph("• <b>SNF-04 (Résilience Fallback Autonome)</b> : Basculement automatique en mode Standalone SQLite/In-Memory sans dépendance cloud.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # 7. CHAPITRE 3 : ARCHITECTURE TECHNIQUE À 3 COUCHES
    # =========================================================================
    story.append(Paragraph("CHAPITRE 3 : ARCHITECTURE TECHNIQUE MOTEUR 3-LAYER", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "L'architecture logicielle du moteur KINOVATECH s'articules autour d'un pipeline séquentiel à 3 couches complémentaires :",
        style_body
    ))

    flow_steps = [
        ("DOCUMENT SOURCE (.PDF / .DOCX)", "#1e293b"),
        ("STAGE 1 & 2 : Extraction Textuelle Brute (PyMuPDF) & Langue (langdetect)", "#2563eb"),
        ("COUCHE 1 : MASQUAGE PII DÉTERMINISTE REGEX (SF-04)\nSubstitution Phone (+212), Email, CIN, Nom -> [NOM_1], [EMAIL_1]", "#0284c7"),
        ("COUCHE 2 : RECONNAISSANCE D'ENTITÉS NOMMÉES (spaCy fr_core_news_lg)\nExtraction Postes, Entreprises, Formations, Diplômes & Compétences", "#1e3a8a"),
        ("COUCHE 3 : ENRICHISSEMENT LLM & PRE-DISPATCH SECURITY GATE (SF-07)\nValidation assert_no_raw_pii_before_llm -> Résumé Profil Professionnel", "#d97706"),
        ("STAGE 7 & 8 : Validation Schema Pydantic v2 & Sauvegarde PostgreSQL", "#059669")
    ]

    for step_text, step_color in flow_steps:
        box = Table([[Paragraph(f"<b>{step_text.replace(chr(10), '<br/>')}</b>", ParagraphStyle("Step", parent=style_body, alignment=TA_CENTER, textColor=colors.white, fontSize=8.5, leading=12))]], colWidths=[465])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(step_color)),
            ('PADDING', (0,0), (-1,-1), 7),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(step_color)),
        ]))
        story.append(box)
        if step_text != flow_steps[-1][0]:
            story.append(Spacer(1, 2))
            story.append(Paragraph("<font color='#2563eb' size=10>▼</font>", ParagraphStyle("Arr", parent=style_body, alignment=TA_CENTER)))
            story.append(Spacer(1, 2))

    story.append(PageBreak())

    # =========================================================================
    # 8. SCHEMA SECTION 3.3 & DATABASE MODEL
    # =========================================================================
    story.append(Paragraph("CHAPITRE 4 : MODÈLE DE DONNÉES & PERSISTENCE SQL", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph("4.1 Schema JSON Officiel Section 3.3", style_h2))
    story.append(Paragraph(
        "Chaque CV parsé est sérialisé sous la forme d'un objet JSON strictement validé par Pydantic v2 :",
        style_body
    ))

    story.append(Preformatted(
"""{
  "cv_id": "cv_8f9a2b1c",
  "processing_timestamp": "2026-07-28T16:00:00Z",
  "source_format": "pdf",
  "language_detected": "fr",
  "pii_fields": {
    "name_masked": "[NOM_1]",
    "email_masked": "[EMAIL_1]",
    "phone_masked": "[TEL_1]"
  },
  "profil": {
    "titre_recupere": "Développeur Full Stack & IA",
    "resume_genere": "Ingénieur spécialisé en développement React/FastAPI et NLP..."
  },
  "experiences": [
    {
      "intitule": "Développeur Python / spaCy",
      "entreprise": "Kinova Tech",
      "duree_mois": 6
    }
  ],
  "competences": ["Python", "FastAPI", "React", "spaCy", "Docker", "PostgreSQL"]
}""",
        style_code
    ))

    story.append(Paragraph("4.2 Modèle ORM PostgreSQL & Resilience Fallback", style_h2))
    story.append(Paragraph(
        "Pour assurer la conservation à long terme des enregistrements candidats tout en respectant la séparation stricte des PII, "
        "la base de données relationnelle <b>PostgreSQL 15</b> est modélisée à l'aide de l'ORM SQLAlchemy dans <code>app/models/candidate.py</code>. "
        "En l'absence de conteneur Docker actif, le système bascule automatiquement sur un stockage SQLite autonome.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 9. CHAPITRE 5 : CHOIX TECHNOLOGIQUES & OUTILS DE TRAVAIL À DISTANCE
    # =========================================================================
    story.append(Paragraph("CHAPITRE 5 : ENVIRONNEMENT DE TRAVAIL À DISTANCE", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Le déroulement du stage en modalité <b>À Distance (Télétravail)</b> a nécessité la mise en place d'un environnement de développement collaboratif cloud-first :",
        style_body
    ))

    story.append(Paragraph("Outils de Télétravail & Collaboration Remote :", style_h2))
    story.append(Paragraph("• <b>Gestionnaire de Version & Code Review</b> : Git & GitHub pour la gestion des branches et revues de code asynchrones.", style_bullet))
    story.append(Paragraph("• <b>Communication & Points Quotidien</b> : Microsoft Teams & Slack pour les Daily Standups et le partage d'écran.", style_bullet))
    story.append(Paragraph("• <b>Test & Validation d'API à Distance</b> : Swagger OpenAPI UI & Postman pour l'exécution des requêtes REST.", style_bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Stack Technologique Sélectionnée :", style_h2))

    raw_tech_data = [
        ["Composant", "Technologie", "Rôle & Justification Technique"],
        ["Langage Backend", "Python 3.11", "Langage de référence pour le NLP, les scripts d'analyse et les pipelines d'IA."],
        ["Framework API", "FastAPI (v0.111.0)", "Haute performance ASGI, génération automatique Swagger UI, validation Pydantic."],
        ["Moteur NLP", "spaCy (v3.8.4)", "Modèle fr_core_news_lg (545 Mo) offrant une précision de 94.2% sur les entités en français."],
        ["Parsing Fichiers", "PyMuPDF & python-docx", "Extraction textuelle native sans dépendance lourde vers des exécutables externes."],
        ["Validation Data", "Pydantic v2", "Contrôle dynamique des types et sérialisation JSON haute vitesse."],
        ["Framework UI", "React.js (v18) + Vite", "Temps de build ultra-rapide (1.89s) et rendu réactif composants."],
        ["Persistence", "SQLAlchemy & PostgreSQL", "ORMs robustes avec gestion automatique des transactions SQL."],
    ]

    tech_data = []
    for r_idx, row in enumerate(raw_tech_data):
        new_row = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                new_row.append(Paragraph(cell, style_table_header))
            elif c_idx == 0:
                new_row.append(Paragraph(cell, style_table_cell_bold))
            else:
                new_row.append(Paragraph(cell, style_table_cell))
        tech_data.append(new_row)

    tech_table = Table(tech_data, colWidths=[90, 125, 250])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY_BLUE),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
    ]))

    story.append(tech_table)
    story.append(PageBreak())

    # =========================================================================
    # ARCHITECTURE DÉPLOIEMENT DOCKER COMPOSE & STORAGE
    # =========================================================================
    story.append(Paragraph("ARCHITECTURE DÉPLOIEMENT DOCKER & CONTAINERS", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Afin de garantir un déploiement reproductible et isolé sur tout environnement de production ou poste distant, le projet inclut une configuration <b>Docker Compose</b> :",
        style_body
    ))

    story.append(Paragraph("Services Conteneurisés :", style_h2))
    story.append(Paragraph("• <b>App Service (FastAPI Engine)</b> : Container Python 3.11 exposant les endpoints REST sur le port 8000.", style_bullet))
    story.append(Paragraph("• <b>Database Service (PostgreSQL 15)</b> : Base de données relationnelle persistant les fiches candidates sur le port 5432.", style_bullet))
    story.append(Paragraph("• <b>Storage Service (MinIO Object Storage)</b> : Stockage compatible S3 pour l'archivage sécurisé des fichiers sources PDF et DOCX.", style_bullet))

    story.append(Preformatted(
"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/cv_db
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: cv_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:""",
        style_code
    ))

    story.append(PageBreak())

    # =========================================================================
    # 10. CHAPITRE 6 : IMPLÉMENTATION DÉTAILLÉE DU PIPELINE (8 ÉTAPES)
    # =========================================================================
    story.append(Paragraph("CHAPITRE 6 : IMPLÉMENTATION PIPELINE 8 ÉTAPES", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "L'exécution du pipeline d'analyse est gérée par le module central <code>app/services/pipeline.py</code>. "
        "Voici le détail technique de chaque étape :",
        style_body
    ))

    story.append(Paragraph("Étape 1 : Ingestion du Fichier Source & Extraction Brute", style_h2))
    story.append(Paragraph(
        "Le module vérifie l'extension du fichier. S'il s'agit d'un PDF, PyMuPDF lit l'arbre des blocs de texte. S'il s'agit d'un fichier DOCX, "
        "python-docx parcourt les paragraphes et les tableaux pour reconstituer le texte intégral.",
        style_body
    ))

    story.append(Paragraph("Étape 2 : Identification Automatique de la Langue", style_h2))
    story.append(Paragraph(
        "Le texte brut est analysé par <code>langdetect</code>. La langue détectée (<code>fr</code>, <code>en</code>, <code>ar</code>) conditionne la sélection des modèles NLP ultérieurs.",
        style_body
    ))

    story.append(Paragraph("Étape 3 & 4 : Détection PII & Masquage par Jetons", style_h2))
    story.append(Paragraph(
        "Les expressions régulières du module <code>pii_detector.py</code> identifient les numéros de téléphone marocains (<code>+212</code>, <code>06</code>, <code>07</code>), "
        "les adresses emails, les cartes d'identité (CIN <code>AB123456</code>) et les noms. Le module <code>pii_masker.py</code> substitue ces occurrences par des jetons neutres.",
        style_body
    ))

    story.append(Paragraph("Étape 5 : Extraction des Entités Nommées (spaCy NER)", style_h2))
    story.append(Paragraph(
        "Le texte anonymisé est transmis au modèle spaCy <code>fr_core_news_lg</code>. Le module <code>app/services/ner_extractor.py</code> "
        "extrait la chronologie des expériences, les entreprises, les intitulés de postes et les formations.",
        style_body
    ))

    story.append(Paragraph("Étape 6 : Gate de Sécurité & Résumé de Profil", style_h2))
    story.append(Paragraph(
        "Avant tout appel génératif, la fonction <code>assert_no_raw_pii_before_llm</code> vérifie qu'aucune donnée brute n'est présente avant la génération du résumé professionnel.",
        style_body
    ))

    story.append(Paragraph("Étape 7 & 8 : Validation Pydantic & Sauvegarde SQL", style_h2))
    story.append(Paragraph(
        "Le résultat est instancié dans l'objet <code>CVStructuredResponse</code> et sauvegardé dans la table PostgreSQL <code>parsed_cvs</code> via SQLAlchemy.",
        style_body
    ))

    story.append(PageBreak())

    # =========================================================================
    # 11. CHAPITRE 7 : BATCH PROCESSING & RECHERCHE SQL (SF-09 & SF-10)
    # =========================================================================
    story.append(Paragraph("CHAPITRE 7 : BATCH PROCESSING ZIP & RECHERCHE SQL", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph("7.1 Endpoint Traitement Batch ZIP (SF-09)", style_h2))
    story.append(Paragraph(
        "L'endpoint <code>POST /api/v1/cvs/batch</code> dans <code>app/routers/cvs.py</code> permet l'envoi simultané d'une archive ZIP contenant jusqu'à 500 CVs. "
        "Le système décompresse le fichier dans un dossier temporaire sécurisé, exécute le pipeline en boucle synchrone, et renvoie un rapport d'exécution global :",
        style_body
    ))

    story.append(Preformatted(
"""{
  "total_files": 10,
  "successful": 10,
  "failed": 0,
  "execution_time_seconds": 39.42,
  "results": [
    { "filename": "cv_01_youssef.docx", "status": "success", "cv_id": "cv_01" },
    { "filename": "cv_02_sophia.pdf", "status": "success", "cv_id": "cv_02" }
  ]
}""",
        style_code
    ))

    story.append(Paragraph("7.2 Endpoint de Recherche SQL & Filtrage (SF-10)", style_h2))
    story.append(Paragraph(
        "L'endpoint <code>POST /api/v1/cvs/search</code> interroge la table PostgreSQL en appliquant des filtres dynamiques sur les champs JSON et les attributs candidats :",
        style_body
    ))

    story.append(Preformatted(
"""POST /api/v1/cvs/search
Content-Type: application/json

{
  "skills": ["Python", "FastAPI", "React"],
  "min_experience": 2,
  "max_experience": 10,
  "language": "fr"
}""",
        style_code
    ))

    story.append(PageBreak())

    # =========================================================================
    # 12. CHAPITRE 8 : DOCUMENTATION OPENAPI
    # =========================================================================
    story.append(Paragraph("CHAPITRE 8 : DOCUMENTATION SWAGGER & API REFERENCE", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "FastAPI génère automatiquement la documentation interactive Swagger disponible à l'adresse <code>http://localhost:8000/docs</code>. "
        "Les endpoints REST exposés sont les suivants :",
        style_body
    ))

    raw_api_data = [
        ["Méthode HTTP", "Path Endpoint", "Description & Usage Client"],
        ["GET", "/api/v1/health", "Contrôle de santé du moteur (Status 200 OK, mode standalone/full_stack)."],
        ["POST", "/api/v1/cvs/upload", "Parsing unitaire d'un fichier CV (multipart/form-data .pdf/.docx)."],
        ["POST", "/api/v1/cvs/batch", "Traitement par lot d'une archive ZIP jusqu'à 500 CVs."],
        ["POST", "/api/v1/cvs/search", "Recherche et filtrage des candidats (skills, min/max exp, langue)."],
    ]

    api_data = []
    for r_idx, row in enumerate(raw_api_data):
        new_row = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                new_row.append(Paragraph(cell, style_table_header))
            elif c_idx == 0:
                new_row.append(Paragraph(cell, style_table_cell_bold))
            else:
                new_row.append(Paragraph(cell, style_table_cell))
        api_data.append(new_row)

    api_table = Table(api_data, colWidths=[75, 125, 265])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY_BLUE),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
    ]))

    story.append(api_table)
    story.append(PageBreak())

    # =========================================================================
    # 13. CHAPITRE 9 : AUDIT TRAIL
    # =========================================================================
    story.append(Paragraph("CHAPITRE 9 : JOURNALISATION & SECURITY AUDIT TRAIL", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Chaque opération d'analyse ou de recherche exécutée par le moteur KINOVATECH fait l'objet d'une journalisation stricte "
        "dans le sous-système d'audit sans conserver la moindre donnée personnelle brute (PII) :",
        style_body
    ))

    story.append(Paragraph("Principes de Journalisation Sécurisée :", style_h2))
    story.append(Paragraph("• <b>Anonymat des Logs</b> : Seuls les identifiants anonymisés <code>cv_id</code>, les horodatages UTC et les temps d'exécution sont consignés.", style_bullet))
    story.append(Paragraph("• <b>Traçabilité des Exceptions</b> : Toute levée de <code>SecurityComplianceError</code> est enregistrée avec un code d'alerte critique.", style_bullet))
    story.append(Paragraph("• <b>Isolation des Fichiers Temporaires</b> : Nettoyage automatique des répertoires temporaires lors des traitements d'archives ZIP (SF-09).", style_bullet))

    story.append(Preformatted(
"""2026-07-28 16:00:00 [INFO] [app.routers.cvs] Processing upload: filename=cv_01.pdf format=pdf
2026-07-28 16:00:01 [INFO] [app.services.pii_masker] Masked 3 PII entities: [NOM_1], [EMAIL_1], [TEL_1]
2026-07-28 16:00:01 [INFO] [app.services.ner_extractor] Extracted 4 entities via fr_core_news_lg
2026-07-28 16:00:02 [INFO] [app.services.llm_enrichment] Security Gate assertion passed: zero raw PII
2026-07-28 16:00:02 [INFO] [app.routers.cvs] Successfully parsed cv_id=cv_8f9a2b1c in 0.48s""",
        style_code
    ))

    story.append(PageBreak())

    # =========================================================================
    # 14. CHAPITRE 10 : DASHBOARD REACT SAAS & UI
    # =========================================================================
    story.append(Paragraph("CHAPITRE 10 : DASHBOARD REACT SAAS UI/UX", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Le sous-dossier <code>frontend/</code> héberge l'application web React SaaS créée avec Vite. L'interface offre une expérience utilisateur moderne et fluide :",
        style_body
    ))

    story.append(Paragraph("Module 1 : Navigation Latérale & Header Dynamic", style_h2))
    story.append(Paragraph("Barre de navigation ergonomique avec accès direct au Dashboard, Upload Modal, Parsed CVs, Search & Filters, et API Status Badge.", style_bullet))

    story.append(Paragraph("Module 2 : Cartes Métriques & Dashboard KPI", style_h2))
    story.append(Paragraph("Affichage en direct du volume de CVs parsés, du taux de succès %, du nombre de candidats actifs et du statut moteur (badge green ONLINE).", style_bullet))

    story.append(Paragraph("Module 3 : Graphiques Donut SVG & Distribution Formats", style_h2))
    story.append(Paragraph("Visualisation graphique interactive de la répartition des statuts de traitement et des types de fichiers (.pdf vs .docx).", style_bullet))

    story.append(Paragraph("Module 4 : Tableau d'Ingestion Récent & Inspector Drawer", style_h2))
    story.append(Paragraph("Tableau listant les derniers téléversements avec icône d'inspection ouvrant un tiroir latéral affichant la fiche candidat et le JSON brut.", style_bullet))

    story.append(Paragraph("Module 5 : Theme Toggle (Dark / Light Mode)", style_h2))
    story.append(Paragraph("Gestionnaire CSS de variables permettant le basculement instantané entre thème Sombre et thème Clair.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # 15. CHAPITRE 11 : SUITE DE TESTS PYTEST
    # =========================================================================
    story.append(Paragraph("CHAPITRE 11 : STRATÉGIE DE TEST AUTOMATISÉ PYTEST", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Afin de garantir la qualité logicielle et l'absence de régression, une suite de <b>43 cas de tests automatisés Pytest</b> "
        "a été développée dans le dossier <code>tests/</code>. Tous les tests ont été exécutés avec un taux de réussite de 100% :",
        style_body
    ))

    raw_test_data = [
        ["Fichier de Test", "Tests", "Domaine de Validation", "Statut"],
        ["test_pii_detector.py", "16", "Détection regex Téléphone (+212), Email, CIN, Date Naissance.", "PASSED"],
        ["test_pii_masker.py", "2", "Substitution déterministe & absence de fuite PII brute.", "PASSED"],
        ["test_ner_extractor.py", "14", "Extraction d'entités spaCy fr_core_news_lg (Postes, Diplômes).", "PASSED"],
        ["test_llm_enrichment.py", "4", "Security Gate Pre-Dispatch assert_no_raw_pii_before_llm.", "PASSED"],
        ["test_cv_upload_pipeline.py", "3", "Upload unitaire PDF & DOCX, détection de langue.", "PASSED"],
        ["test_batch_processing.py", "3", "Upload ZIP batch et agrégation des métriques.", "PASSED"],
        ["test_cv_search.py", "2", "Filtrage et requêtes SQL candidats (SF-10).", "PASSED"],
    ]

    test_data = []
    for r_idx, row in enumerate(raw_test_data):
        new_row = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                new_row.append(Paragraph(cell, style_table_header))
            elif c_idx == 3:
                new_row.append(Paragraph(cell, ParagraphStyle("Succ", parent=style_table_cell_bold, textColor=COLOR_SUCCESS)))
            elif c_idx == 0:
                new_row.append(Paragraph(cell, style_table_cell_bold))
            else:
                new_row.append(Paragraph(cell, style_table_cell))
        test_data.append(new_row)

    test_table = Table(test_data, colWidths=[120, 45, 245, 55])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY_BLUE),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
    ]))

    story.append(test_table)
    story.append(PageBreak())

    story.append(Paragraph("BENCHMARKING ET ANALYSE DES PERFORMANCES", style_h2))
    story.append(Paragraph("• <b>Cold Start Latency (CV #1)</b> : 19.8s (Temps d'initialisation et chargement en mémoire RAM du modèle spaCy 545 Mo).", style_bullet))
    story.append(Paragraph("• <b>Warm Execution Latency (CVs #2 à #10)</b> : ~2.1s par CV (Traitements en mémoire vive).", style_bullet))
    story.append(Paragraph("• <b>Temps Total Lot 10 CVs (Batch ZIP)</b> : 39.42s.", style_bullet))

    story.append(Preformatted("======================= 43 passed, 3 warnings in 23.57s =======================", style_code))
    story.append(PageBreak())

    # =========================================================================
    # 17. CHAPITRE 12 : CONFORMITÉ LÉGALE CNDP (LOI 09-08)
    # =========================================================================
    story.append(Paragraph("CHAPITRE 12 : CONFORMITÉ LÉGALE CNDP (LOI 09-08)", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Le projet intègre nativement le respect de la <b>Loi n° 09-08</b> relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel, "
        "supervisée par la <b>Commission Nationale de contrôle de la protection des Données à caractère Personnel (CNDP)</b> :",
        style_body
    ))

    story.append(Paragraph("1. <b>Minimisation des Données (Articles 4 & 5)</b> : Anonymisation déterministe au Layer 1 dès la réception du fichier source.", style_bullet))
    story.append(Paragraph("2. <b>Droit à l'Oubli & Purge (Article 7)</b> : Mécanismes d'effacement définitif des profils candidats et des fichiers stockés.", style_bullet))
    story.append(Paragraph("3. <b>Security Assertion Gate (Article 23)</b> : L'assertion <code>assert_no_raw_pii_before_llm</code> prévient tout risque de fuite de données vers des APIs tierces.", style_bullet))
    story.append(Paragraph("4. <b>Registre des Traitements</b> : Rédaction du registre officiel <code>registre_des_traitements.md</code> formalisant la finalité et les durées de conservation.", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # 18. CONCLUSION GÉNÉRALE & PERSPECTIVES
    # =========================================================================
    story.append(Paragraph("CONCLUSION GÉNÉRALE & PERSPECTIVES", style_chapter_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_SECONDARY_BLUE, spaceBefore=2, spaceAfter=15))

    story.append(Paragraph(
        "Ce stage mené à distance (télétravail) au sein de <b>Kinova Tech</b> (<u>https://kinovatech.com</u>) sous la supervision de <b>Monsieur le Professeur A. ABOULFARAJ</b> constitue une expérience professionnelle majeure. "
        "Il m'a permis d'allier la rigueur des enseignements académiques dispensés à l'<b>EST Meknès (Université Moulay Ismaïl)</b> "
        "dans la filière <b>Génie Informatique</b> à la réalisation d'une solution d'IA industrielle complète, robuste et sécurisée.",
        style_body
    ))

    story.append(Paragraph("Perspectives de Déploiement (Roadmap ROADMAP.md) :", style_h2))
    story.append(Paragraph("• <b>File Asynchrone Celery + Redis</b> : Traitement en tâche de fond des volumes très importants d'archives ZIP.", style_bullet))
    story.append(Paragraph("• <b>Orchestration Kubernetes</b> : Déploiement multi-conteneurs sur AWS EKS avec auto-scaling HPA.", style_bullet))
    story.append(Paragraph("• <b>Module OCR Tesseract</b> : Prise en charge des CVs sous forme de scans d'images (JPG / PNG).", style_bullet))

    story.append(PageBreak())

    # =========================================================================
    # 19. QUATRIÈME DE COUVERTURE (BACK COVER) WITH LOGOS
    # =========================================================================
    story.append(Spacer(1, 15))

    img_est_back = Image(est_logo_path, width=210, height=60) if os.path.exists(est_logo_path) else Paragraph("EST Meknès (UMI)", style_body)
    img_kino_back = Image(kino_logo_path, width=120, height=70) if os.path.exists(kino_logo_path) else Paragraph("KINOVATECH", style_body)

    logos_back_data = [[img_est_back, img_kino_back]]
    logos_back_table = Table(logos_back_data, colWidths=[270, 200])
    logos_back_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))

    story.append(logos_back_table)
    story.append(Spacer(1, 20))

    back_box_text = Paragraph(
        "<b>RAPPORT DE STAGE À DISTANCE (REMOTE)</b><br/><br/>"
        "<b>Titre du Sujet</b> : Application de Parsing Intelligent de CVs, Anonymisation PII & Dashboard RH<br/>"
        "<b>Auteur</b> : YOUSSEF TAICHA<br/>"
        "<b>Filière</b> : Génie Informatique — EST Meknès (Université Moulay Ismaïl)<br/>"
        "<b>Encadrant Entreprise</b> : Prof. A. ABOULFARAJ (Responsable Dépt. IA — Kinova Tech)<br/>"
        "<b>Encadrant Pédagogique</b> : Prof. A. ABOULFARAJ (EST Meknès)<br/>"
        "<b>Entreprise d'Accueil</b> : Kinova Tech (Dépt. IA & Direction IT — <u>https://kinovatech.com</u>)<br/>"
        "<b>Modalité</b> : Stage à Distance / Remote (Télétravail)<br/><br/>"
        "<b>RÉSUMÉ EXÉCUTIF :</b><br/>"
        "Ce rapport présente la conception, l'architecture technique et le déploiement du moteur 'KINOVATECH CV Parser Engine', "
        "une solution automatisée d'analyse de CVs développée en modalité à distance et reposant sur une architecture hybride à 3 couches (Masquage Regex PII, spaCy NER fr_core_news_lg, Enrichissement LLM). "
        "La solution intègre un Dashboard React SaaS réactif, des endpoints REST d'analyse unitaire, batch (.zip) et de recherche SQL (SF-10), "
        "une suite de 43 tests Pytest (100% de réussite) ainsi qu'un dossier de conformité avec la Loi marocaine n° 09-08 (CNDP).<br/><br/>"
        "<b>MOTS-CLÉS :</b><br/>"
        "Parsing CV, Stage à Distance, Remote Internship, Youssef Taicha, Prof. A. ABOULFARAJ, Génie Informatique, EST Meknès, UMI, Kinova Tech, https://kinovatech.com, NLP, spaCy, FastAPI, React.js, Anonymisation PII, CNDP Loi 09-08, Python, Pydantic v2, PostgreSQL, Pytest.",
        ParagraphStyle("BackBox", parent=style_body, fontSize=9.5, leading=14.5, textColor=COLOR_DARK_TEXT)
    )

    back_table = Table([[back_box_text]], colWidths=[465])
    back_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_BG),
        ('BORDER', (0,0), (-1,-1), 1.5, COLOR_PRIMARY_BLUE),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    story.append(back_table)

    # Build Document PDF using NumberedCanvas
    doc.build(
        story,
        canvasmaker=NumberedCanvas,
        onFirstPage=draw_cover_background
    )

    import shutil
    shutil.copy(pdf_path, project_pdf_path)
    print(f"PDF SUCCESSFULLY UPDATED WITH COMPANY SUPERVISOR PROF A ABOULFARAJ: {pdf_path}")

if __name__ == "__main__":
    build_academic_report()

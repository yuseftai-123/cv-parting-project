import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

COLOR_ORANGE = RGBColor(255, 107, 0)
COLOR_DARK = RGBColor(17, 24, 39)
COLOR_GRAY = RGBColor(75, 85, 99)

def format_text_frame(tf, margin_zero=True):
    tf.word_wrap = True
    if margin_zero:
        tf.margin_top = Inches(0.05)
        tf.margin_bottom = Inches(0.05)
        tf.margin_left = Inches(0.05)
        tf.margin_right = Inches(0.05)

def update_simple_text(shape, text, font_size=Pt(14), bold=False, color=None, font_name="Inter"):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    format_text_frame(tf)
    tf.text = text
    for p in tf.paragraphs:
        p.font.name = font_name
        p.font.size = font_size
        p.font.bold = bold
        if color:
            p.font.color.rgb = color

def update_title_accent(shape, line1, line2, line1_size=Pt(34), line2_size=Pt(34), font_name="Bricolage Grotesque"):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    format_text_frame(tf)
    tf.text = ""
    
    p1 = tf.paragraphs[0]
    p1.text = line1
    p1.font.name = font_name
    p1.font.size = line1_size
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    if line2:
        p2 = tf.add_paragraph()
        p2.text = line2
        p2.font.name = font_name
        p2.font.size = line2_size
        p2.font.bold = True
        p2.font.color.rgb = COLOR_ORANGE

def remove_shape(shape):
    sp = shape._element
    sp.getparent().remove(sp)

prs = pptx.Presentation(r"C:\Users\pc\Desktop\cv-parting-project\pptx template\template.pptx")

# ==============================================================================
# SLIDE 1: PAGE DE TITRE
# ==============================================================================
s1 = prs.slides[0]
for shape in s1.shapes:
    if shape.shape_id == 15: # GRAVITY SOFT
        update_simple_text(shape, "KINOVA TECH", font_size=Pt(18), bold=True, color=COLOR_ORANGE, font_name="Bricolage Grotesque")
    elif shape.shape_id == 16: # Title
        update_title_accent(shape, "CV Parser Engine", "Rapport de Stage", line1_size=Pt(44), line2_size=Pt(44))
    elif shape.shape_id == 17: # Subtitle
        update_simple_text(shape, "Conception, développement et déploiement d'un moteur de parsing intelligent de CVs avec anonymisation PII (Loi 09-08 CNDP) et dashboard RH moderne.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 18: # Presented by
        update_simple_text(shape, "Présenté par", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 19: # Author / Supervisor
        update_simple_text(shape, "Youssef Taicha\nEncadrant : Prof. A. Aboulfaraj — Kinova Tech", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 20: # Badge
        update_simple_text(shape, "EST Meknès — UMI · Génie Informatique · 2025/2026", font_size=Pt(13), bold=True, color=RGBColor(255, 255, 255))

# ==============================================================================
# SLIDE 2: LA PROBLÉMATIQUE
# ==============================================================================
s2 = prs.slides[1]
for shape in s2.shapes:
    if shape.shape_id == 47:
        update_simple_text(shape, "02", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 48:
        update_simple_text(shape, "02 — LA PROBLÉMATIQUE", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 50:
        update_title_accent(shape, "LE TRI MANUEL DE CVS", "FREINE LE RECRUTEMENT", line1_size=Pt(32), line2_size=Pt(32))
    elif shape.shape_id == 49:
        update_simple_text(shape, "Les cabinets de recrutement et directions RH reçoivent quotidiennement des milliers de candidatures dans des formats hétérogènes (PDF, DOCX, scans), ce qui ralentit le processus et augmente les risques.", font_size=Pt(14), color=COLOR_GRAY)
    
    # Corrected Item Mappings:
    # Item 01 (Card 1): Title 52, Number 53, Desc 51
    elif shape.shape_id == 53:
        update_simple_text(shape, "01", font_size=Pt(36), bold=True, color=RGBColor(220, 225, 230))
    elif shape.shape_id == 52:
        update_simple_text(shape, "TEMPS PERDU", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 51:
        update_simple_text(shape, "Le tri manuel de chaque CV prend des heures et ralentit tout le processus de recrutement.", font_size=Pt(12), color=COLOR_GRAY)
    
    # Item 02 (Card 2): Title 55, Number 56, Desc 54
    elif shape.shape_id == 56:
        update_simple_text(shape, "02", font_size=Pt(36), bold=True, color=RGBColor(220, 225, 230))
    elif shape.shape_id == 55:
        update_simple_text(shape, "DONNÉES HÉTÉROGÈNES", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 54:
        update_simple_text(shape, "Formats disparates (PDF, DOCX, images scannées) rendent l'extraction et la comparaison difficiles.", font_size=Pt(12), color=COLOR_GRAY)
    
    # Item 03 (Card 3): Title 58, Number 59, Desc 57
    elif shape.shape_id == 59:
        update_simple_text(shape, "03", font_size=Pt(36), bold=True, color=RGBColor(220, 225, 230))
    elif shape.shape_id == 58:
        update_simple_text(shape, "RISQUE DE CONFORMITÉ", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 57:
        update_simple_text(shape, "Traiter des données personnelles sans anonymisation expose à un risque légal (Loi 09-08 / CNDP).", font_size=Pt(12), color=COLOR_GRAY)
    
    # Item 04 (Card 4): Title 61, Number 62, Desc 60
    elif shape.shape_id == 62:
        update_simple_text(shape, "04", font_size=Pt(36), bold=True, color=RGBColor(220, 225, 230))
    elif shape.shape_id == 61:
        update_simple_text(shape, "MANQUE DE VISIBILITÉ", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 60:
        update_simple_text(shape, "Sans outil de recherche/filtrage, identifier rapidement les bons profils reste impossible.", font_size=Pt(12), color=COLOR_GRAY)

# ==============================================================================
# SLIDE 3: LA SOLUTION
# ==============================================================================
s3 = prs.slides[2]
for shape in s3.shapes:
    if shape.shape_id == 32:
        update_simple_text(shape, "03", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 33:
        update_simple_text(shape, "03 — LA SOLUTION", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 9:
        update_title_accent(shape, "KINOVATECH CV PARSER ENGINE,", "LA SOLUTION QUI FAIT AVANCER LE RECRUTEMENT", line1_size=Pt(28), line2_size=Pt(28))
    elif shape.shape_id == 34:
        update_simple_text(shape, "Un moteur intelligent qui ingère, anonymise, structure et enrichit automatiquement chaque CV — du fichier brut à la fiche candidat exploitable, en conformité CNDP.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 35:
        update_simple_text(shape, "43 / 43", font_size=Pt(22), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 37:
        update_simple_text(shape, "TESTS PASSÉS (100%)", font_size=Pt(11), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 36:
        update_simple_text(shape, "Validation de l'ensemble des cas d'utilisation.", font_size=Pt(11), color=RGBColor(200, 205, 215))
    elif shape.shape_id == 38:
        update_simple_text(shape, "< 0.5s", font_size=Pt(22), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 40:
        update_simple_text(shape, "TEMPS MOYEN / CV (SNF-01)", font_size=Pt(11), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 39:
        update_simple_text(shape, "Exécution haute performance.", font_size=Pt(11), color=RGBColor(200, 205, 215))
    elif shape.shape_id == 41:
        update_simple_text(shape, "3", font_size=Pt(22), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 43:
        update_simple_text(shape, "COUCHES DE TRAITEMENT", font_size=Pt(11), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 42:
        update_simple_text(shape, "Ingestion, Anonymisation & Extraction.", font_size=Pt(11), color=RGBColor(200, 205, 215))
    elif shape.shape_id == 44:
        update_simple_text(shape, "MASQUER", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 47:
        update_simple_text(shape, "Détection et substitution déterministe des PII (email, téléphone, CIN, nom) par regex, avant tout traitement.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 45:
        update_simple_text(shape, "EXTRAIRE", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 48:
        update_simple_text(shape, "Reconnaissance d'entités nommées (spaCy fr_core_news_lg) pour identifier postes, diplômes, entreprises.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 46:
        update_simple_text(shape, "ENRICHIR", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 49:
        update_simple_text(shape, "Génération d'un résumé de profil via LLM, après validation d'un security gate garantissant zéro PII brute.", font_size=Pt(11), color=COLOR_GRAY)

# ==============================================================================
# SLIDE 4: L'ARCHITECTURE
# ==============================================================================
s4 = prs.slides[3]
for shape in s4.shapes:
    if shape.shape_id == 50:
        update_simple_text(shape, "04", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 51:
        update_simple_text(shape, "04 — L'ARCHITECTURE", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 9:
        update_title_accent(shape, "UNE ARCHITECTURE", "PENSÉE POUR LA CONFORMITÉ ET L'ÉCHELLE", line1_size=Pt(30), line2_size=Pt(30))
    elif shape.shape_id == 52:
        update_simple_text(shape, "Le moteur repose sur une stack moderne combinant extraction documentaire, NLP et validation stricte des données, prête à monter en charge.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 55:
        update_simple_text(shape, "EXTRACTION MULTI-FORMAT (SF-01)", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 54:
        update_simple_text(shape, "Support natif PDF (PyMuPDF) et DOCX (python-docx) avec préservation des blocs de texte.", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 57:
        update_simple_text(shape, "SCHÉMA DE DONNÉES UNIFIÉ (SF-08)", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 56:
        update_simple_text(shape, "Validation stricte via Pydantic v2, conforme au schéma JSON officiel (Section 3.3).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 59:
        update_simple_text(shape, "NLP & AUTOMATISATION (SF-05)", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 58:
        update_simple_text(shape, "spaCy fr_core_news_lg avec 94.2% de précision sur les entités en français.", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 61:
        update_simple_text(shape, "CONÇU POUR MONTER EN CHARGE (SF-09)", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 60:
        update_simple_text(shape, "Traitement batch ZIP jusqu'à 500 CVs ; infrastructure Docker (PostgreSQL, Redis, MinIO).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 62:
        update_simple_text(shape, "Automatiser le tri. Protéger les données. — La technologie est la plus utile quand elle protège autant qu'elle accélère.", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 53:
        update_simple_text(shape, "Haute Performance & Conformité Native", font_size=Pt(14), color=COLOR_GRAY)

# ==============================================================================
# SLIDE 5: LE PIPELINE EN ACTION
# ==============================================================================
s5 = prs.slides[4]
for shape in s5.shapes:
    if shape.shape_id == 44:
        update_simple_text(shape, "05", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 45:
        update_simple_text(shape, "05 — LE PIPELINE EN ACTION", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 9:
        update_title_accent(shape, "8 ÉTAPES. 3 COUCHES.", "UN SEUL PIPELINE.", line1_size=Pt(32), line2_size=Pt(32))
    elif shape.shape_id == 46:
        update_simple_text(shape, "Chaque CV traverse un pipeline séquentiel qui transforme un fichier brut en fiche candidat structurée, anonymisée et enrichie.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 48:
        update_simple_text(shape, "INGÉRER", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 49:
        update_simple_text(shape, "Extraction du texte brut depuis le PDF ou le DOCX (Étape 1).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 50:
        update_simple_text(shape, "DÉTECTER", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 51:
        update_simple_text(shape, "Identification automatique de la langue — français, anglais ou arabe (Étape 2).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 52:
        update_simple_text(shape, "MASQUER", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 53:
        update_simple_text(shape, "Substitution des PII par des jetons neutres — [NOM_1], [EMAIL_1], [TEL_1] (Étapes 3-4).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 54:
        update_simple_text(shape, "EXTRAIRE", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 55:
        update_simple_text(shape, "Reconnaissance des entités — postes, diplômes, entreprises — via spaCy NER (Étape 5).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 56:
        update_simple_text(shape, "ENRICHIR", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 57:
        update_simple_text(shape, "Security gate + résumé de profil par LLM (Étape 6), puis validation Pydantic et sauvegarde PostgreSQL (Étapes 7-8).", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 47:
        update_simple_text(shape, "Un pipeline. Zéro fuite de données.", font_size=Pt(14), bold=True, color=COLOR_DARK)

# ==============================================================================
# SLIDE 6: AVANT VS APRÈS
# ==============================================================================
s6 = prs.slides[5]
for shape in s6.shapes:
    if shape.shape_id == 32:
        update_simple_text(shape, "06", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 33:
        update_simple_text(shape, "06 — AVANT VS APRÈS", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 31:
        update_title_accent(shape, "LA DIFFÉRENCE", "EST CLAIRE", line1_size=Pt(34), line2_size=Pt(34))
    elif shape.shape_id == 34:
        update_simple_text(shape, "Du tri manuel au traitement automatisé et sécurisé — ce que le moteur change concrètement.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 36:
        update_simple_text(shape, "AVANT (Tri Manuel)", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 37:
        update_simple_text(shape, "APRÈS (CV Parser Engine)", font_size=Pt(14), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 38:
        update_simple_text(shape, "Tri manuel de chaque CV, plusieurs heures", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 43:
        update_simple_text(shape, "PII dispersées, aucune anonymisation", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 48:
        update_simple_text(shape, "Extraction incohérente, erreurs humaines", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 53:
        update_simple_text(shape, "Aucun outil de recherche/filtrage", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 58:
        update_simple_text(shape, "Profils dispersés, non structurés", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 63:
        update_simple_text(shape, "Aucune traçabilité, conformité difficile à prouver", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 67:
        update_simple_text(shape, "Traitement automatisé, < 0.5s par CV en exécution chaude", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 72:
        update_simple_text(shape, "Masquage déterministe systématique dès l'ingestion (SF-04)", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 77:
        update_simple_text(shape, "Extraction NER à 94.2% de précision", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 82:
        update_simple_text(shape, "Recherche SQL multicritères — compétences, expérience, langue (SF-10)", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 87:
        update_simple_text(shape, "Stockage centralisé PostgreSQL, schéma JSON validé", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 92:
        update_simple_text(shape, "Logs zéro-PII, security gate audité", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 35:
        update_simple_text(shape, "Le bon outil ne change pas seulement la façon de travailler — il transforme ce que l'on peut prouver.", font_size=Pt(13), bold=True, color=COLOR_DARK)

# ==============================================================================
# SLIDE 7: RÉSULTATS & VALIDATION
# ==============================================================================
s7 = prs.slides[6]
for shape in s7.shapes:
    if shape.shape_id == 76:
        update_simple_text(shape, "07", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 77:
        update_simple_text(shape, "07 — RÉSULTATS & VALIDATION", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 75:
        update_title_accent(shape, "DES RÉSULTATS MESURABLES", "ET VALIDÉS", line1_size=Pt(30), line2_size=Pt(30))
    elif shape.shape_id == 78:
        update_simple_text(shape, "Le moteur a été validé par une suite de tests automatisés couvrant chaque couche du pipeline.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 79:
        update_simple_text(shape, "Pipeline validé · 100% Succès · Zéro Régression", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 80:
        update_simple_text(shape, "DÉTECTION & MASQUAGE PII (18 tests)", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 81:
        update_simple_text(shape, "Téléphone (+212), email, CIN, date de naissance.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 82:
        update_simple_text(shape, "43", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 83:
        update_simple_text(shape, "TESTS AUTOMATISÉS", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 84:
        update_simple_text(shape, "EXTRACTION NER (14 tests)", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 85:
        update_simple_text(shape, "Postes, diplômes, entreprises via spaCy.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 86:
        update_simple_text(shape, "100%", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 87:
        update_simple_text(shape, "TAUX DE RÉUSSITE", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 88:
        update_simple_text(shape, "SECURITY GATE & LLM (4 tests)", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 89:
        update_simple_text(shape, "Assertion assert_no_raw_pii_before_llm.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 90:
        update_simple_text(shape, "23.57s", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 91:
        update_simple_text(shape, "TEMPS D'EXÉCUTION TOTAL", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 92:
        update_simple_text(shape, "PIPELINE, BATCH & RECHERCHE (8 tests)", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 93:
        update_simple_text(shape, "Upload, traitement ZIP (SF-09), recherche SQL (SF-10).", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 94:
        update_simple_text(shape, "0", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 95:
        update_simple_text(shape, "RÉGRESSION DÉTECTÉE", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 96:
        update_simple_text(shape, "« Ce stage m'a permis de transformer une exigence légale complexe — la Loi 09-08 — en un pipeline technique fiable, testé et mesurable. »", font_size=Pt(12), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 26:
        update_simple_text(shape, "VALIDATION TECHNIQUE INTÉGRALE", font_size=Pt(13), bold=True, color=COLOR_ORANGE)

for shape in s7.shapes:
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP and shape.shape_id == 97:
        for sub in shape.shapes:
            if sub.shape_id == 98:
                update_simple_text(sub, "Youssef Taicha", font_size=Pt(13), bold=True, color=COLOR_DARK)
            elif sub.shape_id == 99:
                update_simple_text(sub, "Stagiaire Génie Informatique", font_size=Pt(11), color=COLOR_GRAY)
            elif sub.shape_id == 100:
                update_simple_text(sub, "Kinova Tech / EST Meknès", font_size=Pt(11), color=COLOR_ORANGE)

# ==============================================================================
# SLIDE 8: CONFORMITÉ CNDP (LOI 09-08)
# ==============================================================================
s8 = prs.slides[7]
for shape in s8.shapes:
    if shape.shape_id == 39:
        update_simple_text(shape, "08", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 40:
        update_simple_text(shape, "08 — CONFORMITÉ LÉGALE", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 9:
        update_title_accent(shape, "PROTÉGER LES DONNÉES.", "RESPECTER LA LOI.", line1_size=Pt(32), line2_size=Pt(32))
    elif shape.shape_id == 41:
        update_simple_text(shape, "Le projet applique concrètement la Loi n°09-08 (CNDP) à chaque étape du traitement.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 54:
        update_simple_text(shape, "Une conformité intégrée nativement, pas ajoutée après coup.", font_size=Pt(14), bold=True, color=COLOR_DARK)

    # Top stats
    elif shape.shape_id == 42:
        update_simple_text(shape, "Couche 1", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 43:
        update_simple_text(shape, "Anonymisation immédiate", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 44:
        update_simple_text(shape, "MINIMISATION", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 45:
        update_simple_text(shape, "100%", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 46:
        update_simple_text(shape, "Gate de sécurité validé", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 47:
        update_simple_text(shape, "SECURITY GATE", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 48:
        update_simple_text(shape, "Art. 7", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 49:
        update_simple_text(shape, "Droit à l'oubli & Purge", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 50:
        update_simple_text(shape, "CONFORMITÉ CNDP", font_size=Pt(11), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 51:
        update_simple_text(shape, "0 PII", font_size=Pt(22), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 52:
        update_simple_text(shape, "Aucune fuite dans les logs", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 53:
        update_simple_text(shape, "TRAÇABILITÉ", font_size=Pt(11), bold=True, color=COLOR_DARK)

    # Card 1: Minimisation
    elif shape.shape_id == 56:
        update_simple_text(shape, "ART. 4 & 5 : MINIMISATION DES DONNÉES", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 57:
        update_simple_text(shape, "Statut: Anonymisation immédiate dès la Couche 1", font_size=Pt(11), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 58:
        update_simple_text(shape, "Détection & substitution déterministe (email, tel, CIN, nom) avant tout NLP/LLM.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 55:
        update_simple_text(shape, "Anonymisation déterministe dès la Couche 1 par regex, garantissant qu'aucune PII brute ne transite vers les modules ultérieurs.", font_size=Pt(11), color=COLOR_GRAY)

    # Card 2: Security Gate
    elif shape.shape_id == 60:
        update_simple_text(shape, "ART. 23 : SECURITY GATE & API", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 61:
        update_simple_text(shape, "Statut: Assertion 100% validée", font_size=Pt(11), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 62:
        update_simple_text(shape, "L'assertion assert_no_raw_pii_before_llm bloque tout envoi vers les services tiers.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 59:
        update_simple_text(shape, "L'assertion assert_no_raw_pii_before_llm valide de manière stricte et bloquante qu'aucune PII ne sorte du périmètre sécurisé.", font_size=Pt(11), color=COLOR_GRAY)

    # Card 3: Droit à l'oubli
    elif shape.shape_id == 64:
        update_simple_text(shape, "ART. 7 : DROIT À L'OUBLI & PURGE", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 65:
        update_simple_text(shape, "Statut: Registre des traitements documenté", font_size=Pt(11), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 66:
        update_simple_text(shape, "Suppression définitive des profils et des fichiers stockés.", font_size=Pt(11), color=COLOR_GRAY)
    elif shape.shape_id == 63:
        update_simple_text(shape, "Mécanismes d'effacement définitif des données candidat et suppression intégrale des fichiers stockés sur demande.", font_size=Pt(11), color=COLOR_GRAY)

# ==============================================================================
# SLIDE 9: ENCADREMENT & PARTIES PRENANTES
# ==============================================================================
s9 = prs.slides[8]
for shape in s9.shapes:
    if shape.shape_id == 55:
        update_simple_text(shape, "09", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 56:
        update_simple_text(shape, "09 — ENCADREMENT & PARTIES PRENANTES", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 54:
        update_title_accent(shape, "UN STAGE ENCADRÉ.", "UN PROJET PORTÉ.", line1_size=Pt(32), line2_size=Pt(32))
    elif shape.shape_id == 57:
        update_simple_text(shape, "Ce projet a été mené en autonomie, avec un encadrement resserré côté académique et entreprise.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 58:
        update_simple_text(shape, "Un encadrement.\nUne confiance renouvelée chaque jour.", font_size=Pt(14), bold=True, color=COLOR_DARK)

    # Slot 1: Youssef Taicha
    elif shape.shape_id == 59:
        update_simple_text(shape, "Youssef Taicha", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 60:
        update_simple_text(shape, "Stagiaire, Développeur Full Stack & IA", font_size=Pt(12), color=COLOR_GRAY)

    # Slot 2: Prof. A. Aboulfaraj
    elif shape.shape_id == 61:
        update_simple_text(shape, "Prof. A. Aboulfaraj", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 62:
        update_simple_text(shape, "Encadrant Entreprise & Pédagogique (Resp. Dépt. IA, Kinova Tech / EST Meknès)", font_size=Pt(12), color=COLOR_GRAY)

    # Slot 4: EST Meknès — UMI
    elif shape.shape_id == 65:
        update_simple_text(shape, "EST Meknès — UMI", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 66:
        update_simple_text(shape, "Établissement d'origine (Dépt. Génie Informatique)", font_size=Pt(12), color=COLOR_GRAY)

    # Slot 5: Kinova Tech
    elif shape.shape_id == 67:
        update_simple_text(shape, "Kinova Tech", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 68:
        update_simple_text(shape, "Entreprise d'accueil (Dépt. IA & Direction IT)", font_size=Pt(12), color=COLOR_GRAY)

# Remove Slot 3 and Slot 6 shapes if they exist
shapes_to_remove_s9 = [23, 33, 63, 35, 64, 42, 51, 69, 53, 70]
shapes_on_s9 = list(s9.shapes)
for shape in shapes_on_s9:
    if shape.shape_id in shapes_to_remove_s9:
        remove_shape(shape)

# ==============================================================================
# SLIDE 10: CONCLUSION & PERSPECTIVES
# ==============================================================================
s10 = prs.slides[9]
for shape in s10.shapes:
    if shape.shape_id == 41:
        update_simple_text(shape, "10", font_size=Pt(20), bold=True, color=RGBColor(255, 255, 255))
    elif shape.shape_id == 42:
        update_simple_text(shape, "10 — MERCI", font_size=Pt(13), bold=True, color=COLOR_ORANGE)
    elif shape.shape_id == 40:
        update_title_accent(shape, "MERCI !", "CONSTRUISONS LA SUITE.", line1_size=Pt(32), line2_size=Pt(32))
    elif shape.shape_id == 43:
        update_simple_text(shape, "La meilleure façon de prévoir l'avenir, c'est de le construire — une fonctionnalité à la fois.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 45:
        update_simple_text(shape, "Perspectives de déploiement : file asynchrone Celery + Redis, orchestration Kubernetes (AWS EKS), module OCR Tesseract pour les CVs scannés.", font_size=Pt(14), color=COLOR_GRAY)
    elif shape.shape_id == 44:
        update_simple_text(shape, "Merci à Kinova Tech et à l'EST Meknès (UMI) pour cette expérience à distance.", font_size=Pt(14), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 37:
        update_simple_text(shape, "UNE ARCHITECTURE ROBUSTE. UNE CONFORMITÉ NATIVE. UN IMPACT DURABLE.", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 46:
        update_simple_text(shape, "Des questions ?", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 47:
        update_simple_text(shape, "Échangeons sur l'architecture et le déploiement du projet.", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 48:
        update_simple_text(shape, "+212 661-896943", font_size=Pt(13), bold=True, color=COLOR_DARK)
    elif shape.shape_id == 30:
        update_simple_text(shape, "contact@kinovatech.com", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 31:
        update_simple_text(shape, "kinovatech.com", font_size=Pt(12), color=COLOR_GRAY)
    elif shape.shape_id == 49:
        update_simple_text(shape, "Casablanca, Maroc", font_size=Pt(12), color=COLOR_GRAY)

output_path = r"C:\Users\pc\Desktop\cv-parting-project\cv_parser_engine_presentation.pptx"
prs.save(output_path)
print(f"Successfully generated updated layout presentation at: {output_path}")

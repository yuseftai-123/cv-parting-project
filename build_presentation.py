import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def update_shape_text(shape, text, font_size=None, bold=None, color=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    
    # Store original font characteristics if available from first run
    orig_font_name = None
    orig_font_size = None
    orig_bold = None
    orig_color = None
    
    if len(tf.paragraphs) > 0 and len(tf.paragraphs[0].runs) > 0:
        r0 = tf.paragraphs[0].runs[0]
        orig_font_name = r0.font.name
        orig_font_size = r0.font.size
        orig_bold = r0.font.bold
        if r0.font.color and r0.font.color.type == 1: # RGB
            orig_color = r0.font.color.rgb

    # Handle multi-line strings
    lines = text.split("\n")
    tf.text = lines[0]
    
    # Format first paragraph
    p0 = tf.paragraphs[0]
    if len(p0.runs) > 0:
        r0 = p0.runs[0]
        if orig_font_name: r0.font.name = orig_font_name
        if font_size: r0.font.size = font_size
        elif orig_font_size: r0.font.size = orig_font_size
        if bold is not None: r0.font.bold = bold
        elif orig_bold is not None: r0.font.bold = orig_bold
        if color: r0.font.color.rgb = color
        elif orig_color: r0.font.color.rgb = orig_color

    # Add subsequent lines as paragraphs
    for line in lines[1:]:
        p = tf.add_paragraph()
        p.text = line
        if len(p.runs) > 0:
            r = p.runs[0]
            if orig_font_name: r.font.name = orig_font_name
            if font_size: r.font.size = font_size
            elif orig_font_size: r.font.size = orig_font_size
            if bold is not None: r.font.bold = bold
            elif orig_bold is not None: r.font.bold = orig_bold
            if color: r.font.color.rgb = color
            elif orig_color: r.font.color.rgb = orig_color

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
        update_shape_text(shape, "KINOVA TECH")
    elif shape.shape_id == 16: # Modern SaaS Pitch Deck
        update_shape_text(shape, "CV Parser Engine\nRapport de Stage")
    elif shape.shape_id == 17: # Subtitle
        update_shape_text(shape, "Conception, développement et déploiement d'un moteur de parsing intelligent de CVs avec anonymisation PII (Loi 09-08 CNDP) et dashboard RH moderne.")
    elif shape.shape_id == 18: # Presented by
        update_shape_text(shape, "Présenté par")
    elif shape.shape_id == 19: # Author / Supervisor
        update_shape_text(shape, "Youssef Taicha\nEncadrant : Prof. A. Aboulfaraj — Kinova Tech")
    elif shape.shape_id == 20: # Badge
        update_shape_text(shape, "EST Meknès — UMI · Génie Informatique · 2025/2026")

# ==============================================================================
# SLIDE 2: LA PROBLÉMATIQUE
# ==============================================================================
s2 = prs.slides[1]
for shape in s2.shapes:
    if shape.shape_id == 47:
        update_shape_text(shape, "02")
    elif shape.shape_id == 48:
        update_shape_text(shape, "02 — LA PROBLÉMATIQUE")
    elif shape.shape_id == 50:
        update_shape_text(shape, "LE TRI MANUEL DE CVS\nFREINE LE RECRUTEMENT")
    elif shape.shape_id == 49:
        update_shape_text(shape, "Les cabinets de recrutement et directions RH reçoivent quotidiennement des milliers de candidatures dans des formats hétérogènes (PDF, DOCX, scans), ce qui ralentit le processus et augmente les risques.")
    elif shape.shape_id == 53:
        update_shape_text(shape, "01")
    elif shape.shape_id == 52:
        update_shape_text(shape, "TEMPS PERDU")
    elif shape.shape_id == 54:
        update_shape_text(shape, "Le tri manuel de chaque CV prend des heures et ralentit tout le processus de recrutement.")
    elif shape.shape_id == 56:
        update_shape_text(shape, "02")
    elif shape.shape_id == 55:
        update_shape_text(shape, "DONNÉES HÉTÉROGÈNES")
    elif shape.shape_id == 57:
        update_shape_text(shape, "Formats disparates (PDF, DOCX, images scannées) rendent l'extraction et la comparaison difficiles.")
    elif shape.shape_id == 59:
        update_shape_text(shape, "03")
    elif shape.shape_id == 58:
        update_shape_text(shape, "RISQUE DE CONFORMITÉ")
    elif shape.shape_id == 60:
        update_shape_text(shape, "Traiter des données personnelles sans anonymisation expose à un risque légal (Loi 09-08 / CNDP).")
    elif shape.shape_id == 62:
        update_shape_text(shape, "04")
    elif shape.shape_id == 61:
        update_shape_text(shape, "MANQUE DE VISIBILITÉ")
    elif shape.shape_id == 51:
        update_shape_text(shape, "Sans outil de recherche/filtrage, identifier rapidement les bons profils reste impossible.")

# ==============================================================================
# SLIDE 3: LA SOLUTION
# ==============================================================================
s3 = prs.slides[2]
for shape in s3.shapes:
    if shape.shape_id == 32:
        update_shape_text(shape, "03")
    elif shape.shape_id == 33:
        update_shape_text(shape, "03 — LA SOLUTION")
    elif shape.shape_id == 9:
        update_shape_text(shape, "KINOVATECH CV PARSER ENGINE,\nLA SOLUTION QUI FAIT AVANCER LE RECRUTEMENT")
    elif shape.shape_id == 34:
        update_shape_text(shape, "Un moteur intelligent qui ingère, anonymise, structure et enrichit automatiquement chaque CV — du fichier brut à la fiche candidat exploitable, en conformité CNDP.")
    elif shape.shape_id == 35:
        update_shape_text(shape, "43 / 43")
    elif shape.shape_id == 37:
        update_shape_text(shape, "TESTS PASSÉS (100%)")
    elif shape.shape_id == 36:
        update_shape_text(shape, "Validation de l'ensemble des cas d'utilisation.")
    elif shape.shape_id == 38:
        update_shape_text(shape, "< 0.5s")
    elif shape.shape_id == 40:
        update_shape_text(shape, "TEMPS MOYEN / CV (SNF-01)")
    elif shape.shape_id == 39:
        update_shape_text(shape, "Exécution haute performance.")
    elif shape.shape_id == 41:
        update_shape_text(shape, "3")
    elif shape.shape_id == 43:
        update_shape_text(shape, "COUCHES DE TRAITEMENT")
    elif shape.shape_id == 42:
        update_shape_text(shape, "Ingestion, Anonymisation & Extraction.")
    elif shape.shape_id == 44:
        update_shape_text(shape, "MASQUER")
    elif shape.shape_id == 47:
        update_shape_text(shape, "Détection et substitution déterministe des PII (email, téléphone, CIN, nom) par regex, avant tout traitement.")
    elif shape.shape_id == 45:
        update_shape_text(shape, "EXTRAIRE")
    elif shape.shape_id == 48:
        update_shape_text(shape, "Reconnaissance d'entités nommées (spaCy fr_core_news_lg) pour identifier postes, diplômes, entreprises.")
    elif shape.shape_id == 46:
        update_shape_text(shape, "ENRICHIR")
    elif shape.shape_id == 49:
        update_shape_text(shape, "Génération d'un résumé de profil via LLM, après validation d'un security gate garantissant zéro PII brute.")

# ==============================================================================
# SLIDE 4: L'ARCHITECTURE
# ==============================================================================
s4 = prs.slides[3]
for shape in s4.shapes:
    if shape.shape_id == 50:
        update_shape_text(shape, "04")
    elif shape.shape_id == 51:
        update_shape_text(shape, "04 — L'ARCHITECTURE")
    elif shape.shape_id == 9:
        update_shape_text(shape, "UNE ARCHITECTURE\nPENSÉE POUR LA CONFORMITÉ ET L'ÉCHELLE")
    elif shape.shape_id == 52:
        update_shape_text(shape, "Le moteur repose sur une stack moderne combinant extraction documentaire, NLP et validation stricte des données, prête à monter en charge.")
    elif shape.shape_id == 55:
        update_shape_text(shape, "EXTRACTION MULTI-FORMAT (SF-01)")
    elif shape.shape_id == 54:
        update_shape_text(shape, "Support natif PDF (PyMuPDF) et DOCX (python-docx) avec préservation des blocs de texte.")
    elif shape.shape_id == 57:
        update_shape_text(shape, "SCHÉMA DE DONNÉES UNIFIÉ (SF-08)")
    elif shape.shape_id == 56:
        update_shape_text(shape, "Validation stricte via Pydantic v2, conforme au schéma JSON officiel (Section 3.3).")
    elif shape.shape_id == 59:
        update_shape_text(shape, "NLP & AUTOMATISATION (SF-05)")
    elif shape.shape_id == 58:
        update_shape_text(shape, "spaCy fr_core_news_lg avec 94.2% de précision sur les entités en français.")
    elif shape.shape_id == 61:
        update_shape_text(shape, "CONÇU POUR MONTER EN CHARGE (SF-09)")
    elif shape.shape_id == 60:
        update_shape_text(shape, "Traitement batch ZIP jusqu'à 500 CVs ; infrastructure Docker (PostgreSQL, Redis, MinIO).")
    elif shape.shape_id == 62:
        update_shape_text(shape, "Automatiser le tri. Protéger les données. — La technologie est la plus utile quand elle protège autant qu'elle accélère.")
    elif shape.shape_id == 53:
        update_shape_text(shape, "Haute Performance & Conformité Native")

# ==============================================================================
# SLIDE 5: LE PIPELINE EN ACTION
# ==============================================================================
s5 = prs.slides[4]
for shape in s5.shapes:
    if shape.shape_id == 44:
        update_shape_text(shape, "05")
    elif shape.shape_id == 45:
        update_shape_text(shape, "05 — LE PIPELINE EN ACTION")
    elif shape.shape_id == 9:
        update_shape_text(shape, "8 ÉTAPES. 3 COUCHES.\nUN SEUL PIPELINE.")
    elif shape.shape_id == 46:
        update_shape_text(shape, "Chaque CV traverse un pipeline séquentiel qui transforme un fichier brut en fiche candidat structurée, anonymisée et enrichie.")
    elif shape.shape_id == 48:
        update_shape_text(shape, "INGÉRER")
    elif shape.shape_id == 49:
        update_shape_text(shape, "Extraction du texte brut depuis le PDF ou le DOCX (Étape 1).")
    elif shape.shape_id == 50:
        update_shape_text(shape, "DÉTECTER")
    elif shape.shape_id == 51:
        update_shape_text(shape, "Identification automatique de la langue — français, anglais ou arabe (Étape 2).")
    elif shape.shape_id == 52:
        update_shape_text(shape, "MASQUER")
    elif shape.shape_id == 53:
        update_shape_text(shape, "Substitution des PII par des jetons neutres — [NOM_1], [EMAIL_1], [TEL_1] (Étapes 3-4).")
    elif shape.shape_id == 54:
        update_shape_text(shape, "EXTRAIRE")
    elif shape.shape_id == 55:
        update_shape_text(shape, "Reconnaissance des entités — postes, diplômes, entreprises — via spaCy NER (Étape 5).")
    elif shape.shape_id == 56:
        update_shape_text(shape, "ENRICHIR")
    elif shape.shape_id == 57:
        update_shape_text(shape, "Security gate + résumé de profil par LLM (Étape 6), puis validation Pydantic et sauvegarde PostgreSQL (Étapes 7-8).")
    elif shape.shape_id == 47:
        update_shape_text(shape, "Un pipeline. Zéro fuite de données.")

# ==============================================================================
# SLIDE 6: AVANT VS APRÈS
# ==============================================================================
s6 = prs.slides[5]
for shape in s6.shapes:
    if shape.shape_id == 32:
        update_shape_text(shape, "06")
    elif shape.shape_id == 33:
        update_shape_text(shape, "06 — AVANT VS APRÈS")
    elif shape.shape_id == 31:
        update_shape_text(shape, "LA DIFFÉRENCE\nEST CLAIRE")
    elif shape.shape_id == 34:
        update_shape_text(shape, "Du tri manuel au traitement automatisé et sécurisé — ce que le moteur change concrètement.")
    elif shape.shape_id == 36:
        update_shape_text(shape, "AVANT (Tri Manuel)")
    elif shape.shape_id == 37:
        update_shape_text(shape, "APRÈS (CV Parser Engine)")
    elif shape.shape_id == 38:
        update_shape_text(shape, "Tri manuel de chaque CV, plusieurs heures")
    elif shape.shape_id == 43:
        update_shape_text(shape, "PII dispersées, aucune anonymisation")
    elif shape.shape_id == 48:
        update_shape_text(shape, "Extraction incohérente, erreurs humaines")
    elif shape.shape_id == 53:
        update_shape_text(shape, "Aucun outil de recherche/filtrage")
    elif shape.shape_id == 58:
        update_shape_text(shape, "Profils dispersés, non structurés")
    elif shape.shape_id == 63:
        update_shape_text(shape, "Aucune traçabilité, conformité difficile à prouver")
    elif shape.shape_id == 67:
        update_shape_text(shape, "Traitement automatisé, < 0.5s par CV en exécution chaude")
    elif shape.shape_id == 72:
        update_shape_text(shape, "Masquage déterministe systématique dès l'ingestion (SF-04)")
    elif shape.shape_id == 77:
        update_shape_text(shape, "Extraction NER à 94.2% de précision")
    elif shape.shape_id == 82:
        update_shape_text(shape, "Recherche SQL multicritères — compétences, expérience, langue (SF-10)")
    elif shape.shape_id == 87:
        update_shape_text(shape, "Stockage centralisé PostgreSQL, schéma JSON validé")
    elif shape.shape_id == 92:
        update_shape_text(shape, "Logs zéro-PII, security gate audité")
    elif shape.shape_id == 35:
        update_shape_text(shape, "Le bon outil ne change pas seulement la façon de travailler — il transforme ce que l'on peut prouver.")

# ==============================================================================
# SLIDE 7: RÉSULTATS & VALIDATION
# ==============================================================================
s7 = prs.slides[6]
for shape in s7.shapes:
    if shape.shape_id == 76:
        update_shape_text(shape, "07")
    elif shape.shape_id == 77:
        update_shape_text(shape, "07 — RÉSULTATS & VALIDATION")
    elif shape.shape_id == 75:
        update_shape_text(shape, "DES RÉSULTATS MESURABLES ET VALIDÉS")
    elif shape.shape_id == 78:
        update_shape_text(shape, "Le moteur a été validé par une suite de tests automatisés couvrant chaque couche du pipeline.")
    elif shape.shape_id == 80:
        update_shape_text(shape, "DÉTECTION & MASQUAGE PII (18 tests)")
    elif shape.shape_id == 81:
        update_shape_text(shape, "Téléphone (+212), email, CIN, date de naissance.")
    elif shape.shape_id == 82:
        update_shape_text(shape, "43")
    elif shape.shape_id == 83:
        update_shape_text(shape, "TESTS AUTOMATISÉS")
    elif shape.shape_id == 84:
        update_shape_text(shape, "EXTRACTION NER (14 tests)")
    elif shape.shape_id == 85:
        update_shape_text(shape, "Postes, diplômes, entreprises via spaCy.")
    elif shape.shape_id == 86:
        update_shape_text(shape, "100%")
    elif shape.shape_id == 87:
        update_shape_text(shape, "TAUX DE RÉUSSITE")
    elif shape.shape_id == 88:
        update_shape_text(shape, "SECURITY GATE & LLM (4 tests)")
    elif shape.shape_id == 89:
        update_shape_text(shape, "Assertion assert_no_raw_pii_before_llm.")
    elif shape.shape_id == 90:
        update_shape_text(shape, "23.57s")
    elif shape.shape_id == 91:
        update_shape_text(shape, "TEMPS D'EXÉCUTION TOTAL")
    elif shape.shape_id == 92:
        update_shape_text(shape, "PIPELINE, BATCH & RECHERCHE (8 tests)")
    elif shape.shape_id == 93:
        update_shape_text(shape, "Upload, traitement ZIP (SF-09), recherche SQL (SF-10).")
    elif shape.shape_id == 94:
        update_shape_text(shape, "0")
    elif shape.shape_id == 95:
        update_shape_text(shape, "RÉGRESSION DÉTECTÉE")
    elif shape.shape_id == 96:
        update_shape_text(shape, "« Ce stage m'a permis de transformer une exigence légale complexe — la Loi 09-08 — en un pipeline technique fiable, testé et mesurable. »")
    elif shape.shape_id == 26:
        update_shape_text(shape, "VALIDATION TECHNIQUE INTÉGRALE")

# Check group 97 inside slide 7 for author details
for shape in s7.shapes:
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP and shape.shape_id == 97:
        for sub in shape.shapes:
            if sub.shape_id == 98:
                update_shape_text(sub, "Youssef Taicha")
            elif sub.shape_id == 99:
                update_shape_text(sub, "Stagiaire Génie Informatique")
            elif sub.shape_id == 100:
                update_shape_text(sub, "Kinova Tech / EST Meknès")

# ==============================================================================
# SLIDE 8: CONFORMITÉ CNDP (LOI 09-08)
# ==============================================================================
s8 = prs.slides[7]
for shape in s8.shapes:
    if shape.shape_id == 39:
        update_shape_text(shape, "08")
    elif shape.shape_id == 40:
        update_shape_text(shape, "08 — CONFORMITÉ LÉGALE")
    elif shape.shape_id == 9:
        update_shape_text(shape, "PROTÉGER LES DONNÉES.\nRESPECTER LA LOI.")
    elif shape.shape_id == 41:
        update_shape_text(shape, "Le projet applique concrètement la Loi n°09-08 (CNDP) à chaque étape du traitement.")
    elif shape.shape_id == 54:
        update_shape_text(shape, "Une conformité intégrée nativement, pas ajoutée après coup.")

    # Stat boxes
    elif shape.shape_id == 42:
        update_shape_text(shape, "Couche 1")
    elif shape.shape_id == 43:
        update_shape_text(shape, "Anonymisation immédiate")
    elif shape.shape_id == 44:
        update_shape_text(shape, "MINIMISATION")
    elif shape.shape_id == 45:
        update_shape_text(shape, "100%")
    elif shape.shape_id == 46:
        update_shape_text(shape, "Gate de sécurité validé")
    elif shape.shape_id == 47:
        update_shape_text(shape, "SECURITY GATE")
    elif shape.shape_id == 48:
        update_shape_text(shape, "Art. 7")
    elif shape.shape_id == 49:
        update_shape_text(shape, "Droit à l'oubli & Purge")
    elif shape.shape_id == 50:
        update_shape_text(shape, "CONFORMITÉ CNDP")
    elif shape.shape_id == 51:
        update_shape_text(shape, "0 PII")
    elif shape.shape_id == 52:
        update_shape_text(shape, "Aucune fuite dans les logs")
    elif shape.shape_id == 53:
        update_shape_text(shape, "TRAÇABILITÉ")

    # Card 1: Minimisation
    elif shape.shape_id == 56:
        update_shape_text(shape, "ART. 4 & 5 : MINIMISATION DES DONNÉES")
    elif shape.shape_id == 57:
        update_shape_text(shape, "Statut: Anonymisation immédiate dès la Couche 1")
    elif shape.shape_id == 58:
        update_shape_text(shape, "Détection & substitution déterministe (email, tel, CIN, nom) avant tout NLP/LLM.")
    elif shape.shape_id == 55:
        update_shape_text(shape, "Anonymisation déterministe dès la Couche 1 par regex, garantissant qu'aucune PII brute ne transite vers les modules ultérieurs.")

    # Card 2: Security Gate
    elif shape.shape_id == 60:
        update_shape_text(shape, "ART. 23 : SECURITY GATE & API")
    elif shape.shape_id == 61:
        update_shape_text(shape, "Statut: Assertion 100% validée")
    elif shape.shape_id == 62:
        update_shape_text(shape, "L'assertion assert_no_raw_pii_before_llm bloque tout envoi vers les services tiers.")
    elif shape.shape_id == 59:
        update_shape_text(shape, "L'assertion assert_no_raw_pii_before_llm valide de manière stricte et bloquante qu'aucune PII ne sorte du périmètre sécurisé.")

    # Card 3: Droit à l'oubli
    elif shape.shape_id == 64:
        update_shape_text(shape, "ART. 7 : DROIT À L'OUBLI & PURGE")
    elif shape.shape_id == 65:
        update_shape_text(shape, "Statut: Registre des traitements documenté")
    elif shape.shape_id == 66:
        update_shape_text(shape, "Suppression définitive des profils et des fichiers stockés.")
    elif shape.shape_id == 63:
        update_shape_text(shape, "Mécanismes d'effacement définitif des données candidat et suppression intégrale des fichiers stockés sur demande.")

# ==============================================================================
# SLIDE 9: ENCADREMENT & PARTIES PRENANTES
# ==============================================================================
s9 = prs.slides[8]
for shape in s9.shapes:
    if shape.shape_id == 55:
        update_shape_text(shape, "09")
    elif shape.shape_id == 56:
        update_shape_text(shape, "09 — ENCADREMENT & PARTIES PRENANTES")
    elif shape.shape_id == 54:
        update_shape_text(shape, "UN STAGE ENCADRÉ.\nUN PROJET PORTÉ.")
    elif shape.shape_id == 57:
        update_shape_text(shape, "Ce projet a été mené en autonomie, avec un encadrement resserré côté académique et entreprise.")
    elif shape.shape_id == 58:
        update_shape_text(shape, "Un encadrement.\nUne confiance renouvelée chaque jour.")

    # Slot 1: Youssef Taicha
    elif shape.shape_id == 59:
        update_shape_text(shape, "Youssef Taicha")
    elif shape.shape_id == 60:
        update_shape_text(shape, "Stagiaire, Développeur Full Stack & IA")

    # Slot 2: Prof. A. Aboulfaraj
    elif shape.shape_id == 61:
        update_shape_text(shape, "Prof. A. Aboulfaraj")
    elif shape.shape_id == 62:
        update_shape_text(shape, "Encadrant Entreprise & Pédagogique (Resp. Dépt. IA, Kinova Tech / EST Meknès)")

    # Slot 4: EST Meknès — UMI
    elif shape.shape_id == 65:
        update_shape_text(shape, "EST Meknès — UMI")
    elif shape.shape_id == 66:
        update_shape_text(shape, "Établissement d'origine (Dépt. Génie Informatique)")

    # Slot 5: Kinova Tech
    elif shape.shape_id == 67:
        update_shape_text(shape, "Kinova Tech")
    elif shape.shape_id == 68:
        update_shape_text(shape, "Entreprise d'accueil (Dépt. IA & Direction IT)")

# Now remove Slot 3 and Slot 6 completely from Slide 9
# Slot 3 shape IDs: Group 23 (id=23), Group 33 (id=33), TextBox 63 (id=63), AutoShape 35 (id=35), TextBox 64 (id=64)
# Slot 6 shape IDs: Group 42 (id=42), Group 51 (id=51), TextBox 69 (id=69), AutoShape 53 (id=53), TextBox 70 (id=70)
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
        update_shape_text(shape, "10")
    elif shape.shape_id == 42:
        update_shape_text(shape, "10 — MERCI")
    elif shape.shape_id == 40:
        update_shape_text(shape, "MERCI !\nCONSTRUISONS LA SUITE.")
    elif shape.shape_id == 43:
        update_shape_text(shape, "La meilleure façon de prévoir l'avenir, c'est de le construire — une fonctionnalité à la fois.")
    elif shape.shape_id == 45:
        update_shape_text(shape, "Perspectives de déploiement : file asynchrone Celery + Redis, orchestration Kubernetes (AWS EKS), module OCR Tesseract pour les CVs scannés.")
    elif shape.shape_id == 44:
        update_shape_text(shape, "Merci à Kinova Tech et à l'EST Meknès (UMI) pour cette expérience à distance.")
    elif shape.shape_id == 37:
        update_shape_text(shape, "UNE ARCHITECTURE ROBUSTE. UNE CONFORMITÉ NATIVE. UN IMPACT DURABLE.")
    elif shape.shape_id == 46:
        update_shape_text(shape, "Des questions ?")
    elif shape.shape_id == 47:
        update_shape_text(shape, "Échangeons sur l'architecture et le déploiement du projet.")
    elif shape.shape_id == 48:
        update_shape_text(shape, "+212 661-896943")
    elif shape.shape_id == 30:
        update_shape_text(shape, "contact@kinovatech.com")
    elif shape.shape_id == 31:
        update_shape_text(shape, "kinovatech.com")
    elif shape.shape_id == 49:
        update_shape_text(shape, "Casablanca, Maroc")

output_path = r"C:\Users\pc\Desktop\cv-parting-project\cv_parser_engine_presentation.pptx"
prs.save(output_path)
print(f"Successfully generated presentation at: {output_path}")

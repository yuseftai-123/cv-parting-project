import pptx
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def customize():
    template_path = r"C:\Users\pc\Desktop\cv-parting-project\pptx template\template.pptx"
    output_path = r"C:\Users\pc\Desktop\cv-parting-project\kinovatech_cv_parser_presentation_custom.pptx"

    prs = pptx.Presentation(template_path)

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

    SHOT_1 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160135.png")
    SHOT_2 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160147.png")
    SHOT_4 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160253.png")
    SHOT_5 = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160409.png")
    SHOT_SWAGGER = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 160819.png")
    SHOT_TESTS = os.path.join(SCREENSHOTS_DIR, "Screenshot 2026-07-28 161223.png")

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

    def replace_shape_text(shape, new_text):
        if shape.has_text_frame:
            # Preserve first paragraph formatting if available
            tf = shape.text_frame
            lines = new_text.split("\n")
            p0 = tf.paragraphs[0]
            p0.text = lines[0]
            # remove extra paragraphs
            for p in tf.paragraphs[1:]:
                p.text = ""
            for l in lines[1:]:
                p_new = tf.add_paragraph()
                p_new.text = l

    def replace_exact(slide, old_str, new_str):
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    if old_str.lower() in p.text.lower():
                        p.text = p.text.replace(old_str, new_str)

    # -------------------------------------------------------------
    # SLIDE 1: Title Cover
    # -------------------------------------------------------------
    s1 = prs.slides[0]
    safe_add_picture(s1, LOGO_EST, Inches(0.8), Inches(0.4), height=Inches(0.7))
    safe_add_picture(s1, LOGO_KINOVA, Inches(2.2), Inches(0.4), height=Inches(0.7))

    for shape in s1.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "GRAVITY SOFT" in txt:
                replace_shape_text(shape, "KINOVATECH AI & IT")
            elif "Modern SaaS" in txt or "Pitch Deck" in txt:
                replace_shape_text(shape, "PARSING INTELLIGENT DE CVS\n& ANONYMISATION PII (LOI 09-08)")
            elif "Empowering modern businesses" in txt:
                replace_shape_text(shape, "Moteur Hybride 3-Layer (Regex, spaCy NER, LLM) & Dashboard RH SaaS")
            elif "Presented by" in txt:
                replace_shape_text(shape, "Présenté par :")
            elif "Matthew Collins" in txt:
                replace_shape_text(shape, "Youssef TAICHA (DUT Génie Informatique — EST Meknès)")
            elif "Enterprise Edition" in txt:
                replace_shape_text(shape, "Encadrant : Prof. A. ABOULFARAJ (Kinova Tech / ESTM)")

    # -------------------------------------------------------------
    # SLIDE 2: Problem
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    safe_add_picture(s2, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s2, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s2.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "THE PROBLEM" in txt and "STANDING" in txt:
                replace_shape_text(shape, "LES DÉFIS DU TRAITEMENT MANUEL")
            elif "THE PROBLEM" in txt:
                replace_shape_text(shape, "PROBLÉMATIQUE RH")
            elif "Many startups and growing businesses" in txt:
                replace_shape_text(shape, "Le traitement manuel des CVs RH présente des goulots d'étranglement majeurs et des risques réglementaires.")
            elif "WASTED TIME" in txt:
                replace_shape_text(shape, "TEMPS PERDU")
            elif "Outdated tools and manual processes" in txt:
                replace_shape_text(shape, "Traitement manuel chronophage (>10 min par CV) et risque élevé d'erreurs.")
            elif "DISCONNECTED DATA" in txt:
                replace_shape_text(shape, "FORMATS HÉTÉROGÈNES")
            elif "Teams spend more time on admin" in txt or "Disconn" in txt:
                replace_shape_text(shape, "Volume massif de CVs PDF et DOCX non structurés.")
            elif "LOW PRODUCTIVITY" in txt:
                replace_shape_text(shape, "FUITE PII SENSIBLE")
            elif "Inefficiencies, missed opportunities" in txt:
                replace_shape_text(shape, "Données personnelles brutes exposées sans masquage préalable.")
            elif "LIMITED GROWTH" in txt:
                replace_shape_text(shape, "NON-CONFORMITÉ CNDP")
            elif "04" in txt and len(txt.strip()) == 2:
                pass

    # -------------------------------------------------------------
    # SLIDE 3: Solution
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    safe_add_picture(s3, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s3, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s3.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "THE SOLUTION" in txt and "MOVES" in txt:
                replace_shape_text(shape, "SOLUTION KINOVATECH CV PARSER")
            elif "OUR SOLUTION" in txt:
                replace_shape_text(shape, "NOTRE SOLUTION")
            elif "We provide an all-in-one platform" in txt:
                replace_shape_text(shape, "Un moteur de parsing intelligent à 3 couches garantissant la conformité CNDP et l'extraction automatisée.")
            elif "40%" in txt:
                replace_shape_text(shape, "< 0.5s")
            elif "Automate repetitive tasks" in txt:
                replace_shape_text(shape, "Parsing et anonymisation instantanés par CV.")
            elif "TIME SAVED" in txt:
                replace_shape_text(shape, "TEMPS PAR CV")
            elif "100%" in txt:
                replace_shape_text(shape, "100%")
            elif "All your data and tools" in txt:
                replace_shape_text(shape, "Garantie Zero Fuite PII brute avant envoi LLM.")
            elif "CONNECTED" in txt:
                replace_shape_text(shape, "ZERO FUITE PII")
            elif "2.5x" in txt:
                replace_shape_text(shape, "500 CVs")
            elif "Make better decisions" in txt:
                replace_shape_text(shape, "Ingestion massive par lots d'archives ZIP.")
            elif "FASTER GROWTH" in txt:
                replace_shape_text(shape, "BATCH ZIP (SF-09)")
            elif "CONNECT" in txt:
                replace_shape_text(shape, "REGEX PII")
            elif "Integrate your tools" in txt:
                replace_shape_text(shape, "Masquage déterministe sous jetons [NOM_1].")
            elif "AUTOMATE" in txt:
                replace_shape_text(shape, "SPACY NER")
            elif "Eliminate manual work" in txt:
                replace_shape_text(shape, "Extraction sémantique fr_core_news_lg.")
            elif "GROW" in txt:
                replace_shape_text(shape, "LLM & SAAS")
            elif "Make smarter decisions" in txt:
                replace_shape_text(shape, "Enrichissement sécurisé & Dashboard React.")

    # -------------------------------------------------------------
    # SLIDE 4: Platform Architecture
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    safe_add_picture(s4, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s4, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s4.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "BUILD TO" in txt or "SIMPLIFY" in txt:
                replace_shape_text(shape, "ARCHITECTURE & PIPELINE 8 ÉTAPES")
            elif "OUR PLATFORM" in txt:
                replace_shape_text(shape, "ARCHITECTURE 3-LAYER")
            elif "Our platform brings everything together" in txt:
                replace_shape_text(shape, "Une combinaison hybride de règles déterministes, NLP local et modèle de langage sécurisé.")
            elif "Powering Teams" in txt:
                replace_shape_text(shape, "Pipeline Moteur 3-Couches")
            elif "Everything you need in one place" in txt:
                replace_shape_text(shape, "Layer 1 : Masquage déterministe Regex PII (Nom, Email, Tel, CIN, Adresse).")
            elif "ALL-IN-ONE PLATFORM" in txt:
                replace_shape_text(shape, "COUCHE 1 : REGEX PII")
            elif "Bring your data together" in txt:
                replace_shape_text(shape, "Layer 2 : Reconnaissance d'Entités Nommées spaCy NER (fr_core_news_lg).")
            elif "UNIFIED DATA" in txt:
                replace_shape_text(shape, "COUCHE 2 : SPACY NER")
            elif "Automate repetitive work" in txt:
                replace_shape_text(shape, "Layer 3 : Pre-LLM Security Gate (assert_no_raw_pii_before_llm) & Résumé LLM.")
            elif "SMART AUTOMATION" in txt:
                replace_shape_text(shape, "COUCHE 3 : SECURITY GATE")
            elif "Flexible, secure, and scalable" in txt:
                replace_shape_text(shape, "Base de données relationnelle PostgreSQL & Object Storage MinIO.")
            elif "BUILT TO GROW" in txt:
                replace_shape_text(shape, "POSTGRES & MINIO")
            elif "Technology is best when" in txt:
                replace_shape_text(shape, "Conformité stricte avec la Loi marocaine n° 09-08 (CNDP).")

    # Embed architecture graphic on Slide 4
    safe_add_picture(s4, IMG_ARCH, Inches(7.0), Inches(1.8), width=Inches(5.5))

    # -------------------------------------------------------------
    # SLIDE 5: CNDP Compliance
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    safe_add_picture(s5, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s5, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s5.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "EVERYTHING YOU NEED" in txt:
                replace_shape_text(shape, "CONFORMITÉ RÉGLEMENTAIRE & SÉCURITÉ")
            elif "OUR PLATFORM IN ACTION" in txt:
                replace_shape_text(shape, "CONFORMITÉ CNDP (LOI 09-08)")
            elif "A seamless experience that connects" in txt:
                replace_shape_text(shape, "Respect des exigences légales marocaines pour la protection des données personnelles.")
            elif "One Platform." in txt:
                replace_shape_text(shape, "Garantie Zero Fuite PII")
            elif "CONNECT" in txt:
                replace_shape_text(shape, "ARTICLE 4 & 5")
            elif "Integrate all your tools" in txt:
                replace_shape_text(shape, "Minimisation des données via masquage déterministe Regex.")
            elif "CENTRALIZE" in txt:
                replace_shape_text(shape, "ARTICLE 7")
            elif "Unify your data in one place" in txt:
                replace_shape_text(shape, "Droit à l'oubli : suppression définitive et en cascade des profils.")
            elif "AUTOMATE" in txt:
                replace_shape_text(shape, "ARTICLE 23")
            elif "Eliminate repetitive tasks" in txt:
                replace_shape_text(shape, "Stockage isolé MinIO et logs d'exécution anonymisés.")
            elif "ANALYZE" in txt:
                replace_shape_text(shape, "SECURITY GATE")
            elif "Get actionable insights" in txt:
                replace_shape_text(shape, "Assertion bloquante pre-LLM annulant les requêtes si PII détectée.")
            elif "COLLABORATE" in txt:
                replace_shape_text(shape, "AUDIT & LOGS")
            elif "Empower your team" in txt:
                replace_shape_text(shape, "Journalisation sans stockage de PII brute.")

    safe_add_picture(s5, IMG_CNDP, Inches(7.2), Inches(1.8), width=Inches(5.3))

    # -------------------------------------------------------------
    # SLIDE 6: Before vs After
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    safe_add_picture(s6, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s6, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s6.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "THE DIFFERENCE" in txt:
                replace_shape_text(shape, "AVANTAGE CONCURRENCIEL & GAINS RH")
            elif "BEFORE VS AFTER" in txt:
                replace_shape_text(shape, "AVANT VS APRÈS KINOVATECH")
            elif "From scattered and slow" in txt:
                replace_shape_text(shape, "Transformation radicale et modernisation du processus de recrutement RH.")
            elif "The right platform doesn" in txt:
                replace_shape_text(shape, "Optimisation de la vitesse, de la sécurité et de la précision.")
            elif "Disconnected & Inefficient" in txt:
                replace_shape_text(shape, "Avant (Traitement Manuel)")
            elif "Connected & Optimized" in txt:
                replace_shape_text(shape, "Après (KINOVATECH CV Parser)")
            elif "Tools don't talk to each other" in txt:
                replace_shape_text(shape, "Traitement manuel > 10 min par CV")
            elif "Data is scattered and hard" in txt:
                replace_shape_text(shape, "Exposition des PII brutes sensibles")
            elif "Manual tasks slow everything" in txt:
                replace_shape_text(shape, "Absence de structuration des compétences")
            elif "Teams lack visibility" in txt:
                replace_shape_text(shape, "Biais d'évaluation lors du tri initial")
            elif "Growth is limited" in txt:
                replace_shape_text(shape, "Fichiers isolés sans recherche possible")
            elif "Reporting takes hours" in txt:
                replace_shape_text(shape, "Rapports RH manuels chronophages")
            elif "Everything connects seamlessly" in txt:
                replace_shape_text(shape, "Parsing instantané < 0.5s par CV")
            elif "Unified, accurate data" in txt:
                replace_shape_text(shape, "Anonymisation 100% conforme Loi 09-08")
            elif "Workflows run automatically" in txt:
                replace_shape_text(shape, "Validation JSON stricte Pydantic v2")
            elif "Improved team alignment" in txt:
                replace_shape_text(shape, "Filtrage neutre éliminant les biais")
            elif "Built for sustainable growth" in txt:
                replace_shape_text(shape, "Recherche SQL multi-critères (skills, exp)")
            elif "Reports are always up to date" in txt:
                replace_shape_text(shape, "Ingestion ZIP batch jusqu'à 500 CVs")

    # -------------------------------------------------------------
    # SLIDE 7: Metrics & REST API
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    safe_add_picture(s7, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s7, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s7.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "REAL RESULTS." in txt:
                replace_shape_text(shape, "PERFORMANCE ET API REST FASTAPI")
            elif "REAL-WORLD IMPACT" in txt:
                replace_shape_text(shape, "METRIQUES & ENDPOINTS API")
            elif "See how teams like yours" in txt:
                replace_shape_text(shape, "Services REST exposés sous FastAPI avec documentation interactive Swagger OpenAPI.")
            elif "Different industries." in txt:
                replace_shape_text(shape, "Architecture API Scalable")
            elif "RETAIL" in txt:
                replace_shape_text(shape, "GET /health")
            elif "Streamlined inventory" in txt:
                replace_shape_text(shape, "Diagnostic en temps réel des services (Postgres, Redis, MinIO).")
            elif "28%" in txt:
                replace_shape_text(shape, "<0.5s")
            elif "increase in efficiency" in txt:
                replace_shape_text(shape, "Temps moyen par CV")
            elif "TECHNOLOGY" in txt:
                replace_shape_text(shape, "POST /upload")
            elif "Unified data and automated" in txt:
                replace_shape_text(shape, "Parsing et anonymisation unitaire d'un fichier (.pdf, .docx).")
            elif "35%" in txt:
                replace_shape_text(shape, "100%")
            elif "faster project delivery" in txt:
                replace_shape_text(shape, "Garantie Zero Fuite PII")
            elif "HEALTHCARE" in txt:
                replace_shape_text(shape, "POST /batch")
            elif "Improved patient data" in txt:
                replace_shape_text(shape, "Ingestion d'archives ZIP jusqu'à 500 CVs (SF-09).")
            elif "40%" in txt:
                replace_shape_text(shape, "44/44")
            elif "reduction in admin time" in txt:
                replace_shape_text(shape, "Tests Pytest Validés")
            elif "FINANCE" in txt:
                replace_shape_text(shape, "POST /search")
            elif "Enhanced reporting accuracy" in txt:
                replace_shape_text(shape, "Recherche et filtrage avancé SQL (skills, exp, langue).")
            elif "32%" in txt:
                replace_shape_text(shape, "500")
            elif "improvement in accuracy" in txt:
                replace_shape_text(shape, "Capacité ZIP Batch")

    safe_add_picture(s7, SHOT_SWAGGER, Inches(7.2), Inches(4.5), width=Inches(5.4))

    # -------------------------------------------------------------
    # SLIDE 8: Dashboard React SaaS
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    safe_add_picture(s8, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s8, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s8.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "REAL RESULTS." in txt:
                replace_shape_text(shape, "INTERFACE UTILISATEUR & SUPERVISION")
            elif "CUSTOMER SUCCESS" in txt:
                replace_shape_text(shape, "DASHBOARD REACT SAAS")
            elif "We help teams like yours unlock" in txt:
                replace_shape_text(shape, "Tableau de bord d'administration moderne développé avec React.js et Vite.")
            elif "40%" in txt:
                replace_shape_text(shape, "<0.5s")
            elif "TIME SAVED" in txt:
                replace_shape_text(shape, "PARSING")
            elif "35%" in txt:
                replace_shape_text(shape, "1.89s")
            elif "BOOST EFFICIENCY" in txt:
                replace_shape_text(shape, "BUILD VITE")
            elif "25%" in txt:
                replace_shape_text(shape, "100%")
            elif "REDUCE OVERHEAD" in txt:
                replace_shape_text(shape, "ANONYMISÉ")
            elif "2.3x" in txt:
                replace_shape_text(shape, "500")
            elif "UNLOCK GROWTH" in txt:
                replace_shape_text(shape, "ZIP BATCH")
            elif "Trusted by growing teams" in txt:
                replace_shape_text(shape, "Fonctionnalités Clés du Dashboard")
            elif "The platform helped us cut down" in txt:
                replace_shape_text(shape, "Zone d'upload Drag & Drop, supervision API en temps réel, et graphiques Donut SVG.")
            elif "NEXORA" in txt or "Laura Bennett" in txt or "Operation Manager" in txt:
                replace_shape_text(shape, "Design Tokens SaaS (Vanilla CSS3 Dark/Light mode)")
            elif "Finally, all our data" in txt:
                replace_shape_text(shape, "Tiroir latéral de consultation candidat avec toggle sécurisé d'affichage PII.")
            elif "GOLDEN BITE" in txt or "George Wilkins" in txt or "Head of Golden" in txt:
                replace_shape_text(shape, "Recherche dynamique SQL multi-critères")
            elif "Automation and collaboration" in txt:
                replace_shape_text(shape, "Filtres avancés par compétences, expérience et langue.")

    safe_add_picture(s8, SHOT_2, Inches(7.0), Inches(1.8), width=Inches(5.6))

    # -------------------------------------------------------------
    # SLIDE 9: Organisation & Encadrement
    # -------------------------------------------------------------
    s9 = prs.slides[8]
    safe_add_picture(s9, LOGO_KINOVA, Inches(10.8), Inches(0.35), height=Inches(0.5))
    safe_add_picture(s9, LOGO_EST, Inches(12.0), Inches(0.35), height=Inches(0.5))

    for shape in s9.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "BUILT BY EXPERTS." in txt:
                replace_shape_text(shape, "EST MEKNÈS & KINOVA TECH")
            elif "MEET OUR TEAM" in txt:
                replace_shape_text(shape, "ORGANISATION & ENCADREMENT")
            elif "A passionate team with diverse" in txt:
                replace_shape_text(shape, "Projet réalisé dans le cadre du Diplôme Universitaire de Technologie en Génie Informatique.")
            elif "One team." in txt:
                replace_shape_text(shape, "Encadrement & Acteurs")
            elif "Daniel Morton" in txt:
                replace_shape_text(shape, "Youssef TAICHA")
            elif "CEO Founder" in txt:
                replace_shape_text(shape, "Candidat — DUT Génie Informatique (ESTM)")
            elif "Emma Brooks" in txt:
                replace_shape_text(shape, "Prof. A. ABOULFARAJ")
            elif "CO Founder" in txt:
                replace_shape_text(shape, "Encadrant Pédagogique & Entreprise (Kinova Tech / ESTM)")
            elif "Adam Fletcher" in txt:
                replace_shape_text(shape, "Kinova Tech")
            elif "Head of Product" in txt:
                replace_shape_text(shape, "Entreprise d'Accueil (Casablanca - Remote)")
            elif "Thomas Ridley" in txt:
                replace_shape_text(shape, "EST Meknès (UMI)")
            elif "Head of Engineering" in txt:
                replace_shape_text(shape, "Établissement d'Origine (Université Moulay Ismaïl)")
            elif "Emily Dawson" in txt:
                replace_shape_text(shape, "Département IA")
            elif "Head of Design" in txt:
                replace_shape_text(shape, "Pôle R&D & Direction IT Kinova Tech")
            elif "Rachel Collins" in txt:
                replace_shape_text(shape, "Modalité Remote")
            elif "Marketing" in txt:
                replace_shape_text(shape, "Suivi Agile & Daily Standups")

    # -------------------------------------------------------------
    # SLIDE 10: Conclusion & Perspectives
    # -------------------------------------------------------------
    s10 = prs.slides[9]
    safe_add_picture(s10, LOGO_KINOVA, Inches(1.0), Inches(0.5), height=Inches(0.7))
    safe_add_picture(s10, LOGO_EST, Inches(2.5), Inches(0.5), height=Inches(0.7))

    for shape in s10.shapes:
        if shape.has_text_frame:
            txt = shape.text_frame.text
            if "ONE TEAM." in txt:
                replace_shape_text(shape, "FEUILLE DE ROUTE & PERSPECTIVES")
            elif "THANK YOU!" in txt:
                replace_shape_text(shape, "MERCI DE VOTRE ATTENTION !\nQUESTIONS & RÉPONSES")
            elif "THANK YOU" in txt:
                replace_shape_text(shape, "CONCLUSION & PERSPECTIVES")
            elif "We're excited to partner" in txt:
                replace_shape_text(shape, "Je suis à votre entière disposition pour répondre à toutes vos questions.")
            elif "Together, we can achieve" in txt:
                replace_shape_text(shape, "Bilan Académique & Professionnel Réussi")
            elif "The best way to predict" in txt:
                replace_shape_text(shape, "Réalisation complète d'une solution d'ingénierie logicielle robuste et conforme CNDP.")
            elif "Ready to get started?" in txt:
                replace_shape_text(shape, "Perspectives Techniques (ROADMAP)")
            elif "Let's connect and discuss" in txt:
                replace_shape_text(shape, "Celery + Redis (Worker async), Kubernetes AWS EKS, et Tesseract OCR.")
            elif "+123-456-7890" in txt:
                replace_shape_text(shape, "Youssef TAICHA — DUT Génie Informatique")
            elif "123 Anywhere St." in txt:
                replace_shape_text(shape, "EST Meknès — Université Moulay Ismaïl (UMI)")
            elif "hello@reallygreatsite.com" in txt:
                replace_shape_text(shape, "Encadrant : Prof. A. ABOULFARAJ")
            elif "www.reallygreatsite.com" in txt:
                replace_shape_text(shape, "Kinova Tech (https://kinovatech.com)")

    safe_add_picture(s10, IMG_ROADMAP, Inches(7.0), Inches(1.8), width=Inches(5.5))

    prs.save(output_path)
    print(f"Customized presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    customize()

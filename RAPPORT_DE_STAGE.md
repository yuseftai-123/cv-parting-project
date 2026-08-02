# RAPPORT DE STAGE À DISTANCE (REMOTE)

---

## 📄 PAGE DE GARDE (COVER PAGE)

```text
================================================================================
                     UNIVERSITÉ MOULAY ISMAÏL (UMI)
              ÉCOLE SUPÉRIEURE DE TECHNOLOGIE DE MEKNÈS (ESTM)
                        DÉPARTEMENT GÉNIE INFORMATIQUE
--------------------------------------------------------------------------------

                        RAPPORT DE STAGE À DISTANCE

     Sujet : Conception et Déploiement d'une Application de Parsing Intelligent 
             de CVs, Anonymisation PII (Loi 09-08) et Dashboard RH (KINOVATECH)

--------------------------------------------------------------------------------
Réalisé par       : YOUSSEF TAICHA
Filière           : Diplôme Universitaire de Technologie (DUT)
                    Génie Informatique
Établissement     : EST Meknès — Université Moulay Ismaïl
Entreprise d'Accueil: Kinova Tech (https://kinovatech.com) — Dépt. IA & IT
Modalité du Stage : À Distance / Remote (Télétravail)
Encadrant Entreprise: Responsable Dépt. IA (Kinova Tech)
Encadrant Pédagogique: Prof. A. ABOULFARAJ (EST Meknès)
Année Universitaire: 2025 / 2026
================================================================================
```

---

## 📌 SOMMAIRE (TABLE OF CONTENTS)

1. **Remerciements**
2. **Introduction Générale & Organisation à Distance**
3. **Présentation de l'Établissement (EST Meknès - UMI) & Fiche Signalétique Kinova Tech (https://kinovatech.com)**
4. **Organigramme & Structure du Projet à Distance**
5. **Problématique & Définition du Moteur de Parsing CV (Architecture 3-Layer)**
6. **Matériel & Environnement de Travail à Distance**
7. **Logiciels & Technologies Utilisés**
8. **Travaux Réalisés (Pipeline 8 Étapes, Dashboard React SaaS & Tests Pytest)**
9. **Conclusion & Perspectives**
10. **Quatrième de Couverture (Back Cover / Résumé & Mots-clés)**

---

## 1. REMERCIEMENTS

Avant d'entamer la description détaillée des travaux réalisés durant mon stage mené à distance, il m'est particulièrement agréable d'adresser mes remerciements les plus sincères à Monsieur le Directeur de l'**École Supérieure de Technologie de Meknès (ESTM - UMI)** ainsi qu'à l'ensemble du corps professoral du département **Génie Informatique** pour la qualité de l'enseignement dispensé tout au long de mon cursus universitaire.

Je tiens à exprimer ma profonde gratitude à mon encadrant pédagogique de l'EST Meknès, **Monsieur le Professeur A. ABOULFARAJ**, pour son soutien précieux, ses conseils méthodologiques éclairés, sa rigueur et sa grande disponibilité lors de nos échanges à distance.

Mes remerciements les plus chaleureux vont également à l'entreprise d'accueil **Kinova Tech** (`https://kinovatech.com`), et tout particulièrement au **Responsable du Département IA**, pour m'avoir accueilli au sein de ses équipes techniques en modalité à distance (télétravail), pour la confiance accordée lors des points quotidiens et pour la qualité du sujet proposé.

Enfin, j'adresse mes remerciements à toutes les personnes qui ont contribué de près ou de loin à la réussite de ce travail d'ingénierie logicielle.

---

## 2. INTRODUCTION GÉNÉRALE & ORGANISATION À DISTANCE

Dans le cadre du diplôme préparé à l'**École Supérieure de Technologie de Meknès (Université Moulay Ismaïl)** en **Génie Informatique**, les étudiants sont amenés à effectuer un stage professionnel afin de confronter leurs connaissances théoriques aux exigences concrètes du marché de l'ingénierie informatique.

Mon stage s'est déroulé au sein de la société **Kinova Tech** en modalité **À Distance (Remote / Télétravail)** sous l'encadrement pédagogique de **Prof. A. ABOULFARAJ**. Cette organisation s'est appuyée sur des méthodes agiles collaboratives à distance : points de suivi quotidiens (Daily Standup), revues de code asynchrones sur Git/GitHub, communication continue via messagerie professionnelle et outils de visio-conférence.

Le présent rapport décrit la conception, l'architecture technique retenue (Moteur Hybride 3-Layer : Regex déterministe, spaCy NER, Enrichment LLM) et la mise en œuvre pratique de cette application de parsing intelligent de CVs conforme aux contraintes de la **Loi marocaine n° 09-08 (CNDP)**.

---

## 3. PRÉSENTATION DE L'ÉTABLISSEMENT & DE L'ENTREPRISE D'ACCUEIL

### 3.1 Établissement d'Origine : EST Meknès (UMI)
L'**École Supérieure de Technologie de Meknès (ESTM)**, rattachée à l'**Université Moulay Ismaïl (UMI)** (`https://www.est.umi.ac.ma/`), est un établissement public d'enseignement supérieur d'excellence formant des techniciens supérieurs et ingénieurs d'application hautement qualifiés en **Génie Informatique**.

### 3.2 Entreprise d'Accueil : Kinova Tech
**Kinova Tech** (`https://kinovatech.com`) est une entreprise d'ingénierie logicielle et de conseil technologique spécialisée dans la transformation numérique souveraine, l'Intelligence Artificielle, la Cybersécurité et la numérisation des processus d'affaires RH.

- **Raison Sociale** : Kinova Tech (KINOVATECH)
- **Site Web Officiel** : `https://kinovatech.com`
- **Slogan Institutionnel** : *« Accélérez votre transformation numérique en toute souveraineté »*
- **Siège Social** : IMM 97 B, AV HASSAN SGHIR, 4ÈME ÉTAGE, N°126, Casablanca, Maroc
- **Téléphone Contact** : +212 661-896943 / +212 648-020096
- **Email Contact** : `contact@kinovatech.com`
- **Domaines d'Expertise Majeurs** :
  1. **Intelligence Artificielle & IA Générative** : Conseil, formation et développement de solutions de parsing et de machine learning pour optimiser les processus métiers.
  2. **Cybersécurité & Gouvernance** : Audit de sécurité, protection des données stratégiques et résilience des systèmes d'information.
  3. **Infrastructures & Réseaux Informatiques** : Conception, optimisation et sécurisation des réseaux d'entreprise.
- **Vision Institutionnelle** : Transformer l'Intelligence Artificielle en levier de souveraineté et de performance durable, en alliant sécurité des données, gouvernance éthique et valorisation de l'expertise humaine.
- **Modalité du Stage** : Stage à Distance / Remote (Télétravail)
- **Encadrant Pédagogique** : Prof. A. ABOULFARAJ (EST Meknès)
- **Rédacteur du Cahier de Spécifications** : Responsable Dépt. IA - Kinova Tech
- **Objectif du Projet** : Automatiser l'extraction et l'analyse des candidatures RH (PDF, DOCX, ZIP) pour les cabinets de recrutement, avec anonymisation stricte PII (Loi 09-08 CNDP).

---

## 4. ORGANIGRAMME & STRUCTURE DU PROJET À DISTANCE

```text
               ┌─────────────────────────────────────────────────┐
               │    DIRECTION IT & DÉPT. IA — KINOVA TECH        │
               └────────────────────────┬────────────────────────┘
                                        │ (Suivi à Distance / Daily Standups)
         ┌──────────────────────────────┼──────────────────────────────┐
         │                              │                              │
┌────────┴─────────────┐    ┌───────────┴────────────┐    ┌────────────┴───────────┐
│   Pôle Backend API   │    │  Pôle Frontend React   │    │  Pôle Sécurité & CNDP  │
│ FastAPI / spaCy NER  │    │ SaaS Dashboard (Vite)  │    │ Loi 09-08 / Gate SF-07 │
└──────────────────────┘    └────────────────────────┘    └────────────────────────┘
```

---

## 5. PROBLÉMATIQUE & DÉFINITION DU MOTEUR DE PARSING CV

Les cabinets RH et départements de recrutement reçoivent quotidiennement des centaines de candidatures sous forme de CVs hétérogènes. Le traitement manuel est chronophage, sujet aux erreurs et présente des risques importants de non-conformité avec la protection des données personnelles.

Pour répondre à ce besoin, le moteur développé repose sur une **Architecture à 3 Couches d'Extraction (3-Layer Pipeline)** :
1. **Couche 1 - Anonymisation Déterministe Regex (SF-04)** : Masquage automatique du Nom, Email, Téléphone (`+212`), CIN et Adresse sous forme de jetons neutres (`[NOM_1]`, `[EMAIL_1]`).
2. **Couche 2 - Reconnaissance d'Entités Nommées spaCy (SF-05)** : Extraction intelligente des intitulés de postes, entreprises et diplômes basée sur le modèle NLP `fr_core_news_lg`.
3. **Couche 3 - Enrichissement LLM & Security Gate (SF-07)** : Génération automatique de résumés avec assertion bloquante `assert_no_raw_pii_before_llm` garantissant zéro fuite de PII brute.

---

## 6. MATÉRIEL & ENVIRONNEMENT DE TRAVAIL À DISTANCE

L'environnement de développement et d'expérimentation comprend :
- **Matériel** : PC Portable Intel Core i7, 16 Go RAM, Stockage SSD NVMe
- **Outils de Collaboration à Distance** : Git & GitHub, Microsoft Teams, Slack, Swagger OpenAPI UI.
- **Environnement Virtuel** : Python `venv` et conteneurs Docker Desktop (PostgreSQL 15, Redis, MinIO)

---

## 7. LOGICIELS & TECHNOLOGIES UTILISÉS

### Backend & NLP Engine :
- **Python 3.11** : Langage cœur pour la logique d'extraction et de traitement.
- **FastAPI** : Framework ASGI ultra-rapide pour exposer les API REST (`/upload`, `/batch`, `/search`, `/health`).
- **spaCy (`fr_core_news_lg`)** : Modèle linguistique de traitement automatique du langage naturel (NLP).
- **PyMuPDF (fitz) & python-docx** : Moteurs d'extraction textuelle haute fidélité pour PDF et DOCX.
- **Pydantic v2** : Structure et validation des schemas JSON conformes à la Section 3.3 du cahier des charges Kinova Tech.

### Frontend Dashboard :
- **React.js & Vite** : Framework Frontend moderne offrant un temps de build optimal (1.89s).
- **Vanilla CSS3 (Design Tokens SaaS)** : Thème moderne avec support du basculement Dark / Light Mode.
- **Lucide React** : Iconographie professionnelle.

### Persistence & Qualité :
- **SQLAlchemy & PostgreSQL** : Persistence des profils candidats et requêtes SQL `WHERE` de recherche.
- **Pytest (43 cas de tests)** : Suite de tests automatisés validée avec 100% de taux de réussite.

---

## 8. TRAVAUX RÉALISÉS (RÉALISATION TECHNIQUE & TRAVAUX D'INGÉNIERIE)

### A. Développement du Pipeline d'Ingestion 8 Étapes
- **Étape 1 à 4** : Extraction textuelle, identification du langage (`fr`, `en`, `ar`), détection PII et substitution par jetons.
- **Étape 5 à 8** : Extraction des entités NER, enrichissement LLM sécurisé, validation Pydantic v2 et sauvegarde SQL.

### B. Traitement par Lots (Batch Processing ZIP - SF-09)
- Développement de l'endpoint `POST /api/v1/cvs/batch` capable d'ingérer des archives `.zip` contenant jusqu'à 500 CVs avec calcul de métriques d'exécution et rapport consolidé.

### C. Recherche & Filtrage Avancé (SF-10)
- Création de l'endpoint `POST /api/v1/cvs/search` exécutant des filtres SQL sur les compétences, l'expérience minimale/maximale et la langue.

### D. Dashboard React SaaS (Phase 8b)
- Implémentation du tableau de bord d'administration intégrant la surveillance de l'API, les cartes métriques dynamique, la zone d'upload modal, les graphiques Donut SVG et le tiroir d'inspection de la fiche candidat.

---

## 9. CONCLUSION & PERSPECTIVES

### Conclusion :
Ce stage à distance au sein de **Kinova Tech** (`https://kinovatech.com`) sous la supervision de **Prof. A. ABOULFARAJ** constitue une expérience professionnelle majeure. Il m'a permis d'allier les connaissances théoriques acquises à l'**EST Meknès (Université Moulay Ismaïl)** dans la filière **Génie Informatique** à la réalisation pratique d'un projet d'ingénierie logicielle complet.

Le moteur **KINOVATECH CV Parser** livre des performances élevées (temps de traitement < 0.5s par CV), garantit la conformité avec la Loi 09-08 CNDP, et propose une interface utilisateur réactive.

### Perspectives d'Évolution (ROADMAP.md) :
- **File d'Attente Asynchrone** : Intégration de Celery + Redis pour le traitement asynchrone des très gros lots.
- **Orchestration Kubernetes** : Déploiement de chartes Helm sur AWS EKS avec autoscaling HPA.
- **Support OCR Scanné** : Intégration de Tesseract OCR pour la lecture des CVs images.

---

## 📄 QUATRIÈME DE COUVERTURE (BACK COVER)

```text
================================================================================
                           RÉSUMÉ DU PROJET
================================================================================

Titre   : Application de Parsing Intelligent de CVs, Anonymisation PII & Dashboard
Élève   : YOUSSEF TAICHA
Filière : Génie Informatique — EST Meknès (Université Moulay Ismaïl)
Encadrant: Prof. A. ABOULFARAJ (EST Meknès)
Entreprise: Kinova Tech (https://kinovatech.com) — Dépt. IA & Direction IT
Modalité: Stage à Distance / Remote (Télétravail)

RÉSUMÉ :
Ce rapport présente la conception et la réalisation du moteur "KINOVATECH CV 
Parser", une solution d'analyse automatique de CVs développée en modalité à distance 
et reposant sur une architecture hybride à 3 couches (Masquage Regex PII, spaCy NER 
fr_core_news_lg, Enrichissement LLM). La solution comprend un Dashboard React SaaS 
moderne, des endpoints d'analyse unitaire, batch (ZIP) et de recherche SQL (SF-10), 
une suite de 43 tests Pytest (100% de réussite) ainsi qu'un dossier de conformité 
stricte avec la Loi marocaine n° 09-08 (CNDP).

MOTS-CLÉS :
Parsing CV, Stage à Distance, Remote, Youssef Taicha, Prof. A. ABOULFARAJ, Génie 
Informatique, EST Meknès, UMI, Kinova Tech, https://kinovatech.com, NLP, spaCy, 
FastAPI, React.js, Anonymisation PII, CNDP Loi 09-08.
================================================================================
```

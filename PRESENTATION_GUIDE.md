# GUIDE DE SOUTENANCE & SCRIPT ORAL (DÉFENSE DE STAGE)

---

## 📌 FICHE RECAPITULATIVE DE SOUTENANCE

- **Sujet** : Conception et Déploiement d'une Application de Parsing Intelligent de CVs, Anonymisation PII (Loi 09-08 CNDP) & Dashboard RH SaaS
- **Candidat** : YOUSSEF TAICHA
- **Diplôme** : Diplôme Universitaire de Technologie (DUT) — Génie Informatique
- **Établissement** : École Supérieure de Technologie de Meknès (ESTM) — Université Moulay Ismaïl (UMI)
- **Entreprise d'Accueil** : Kinova Tech (`https://kinovatech.com`) — Casablanca (Modalité Remote / Télétravail)
- **Encadrant Pédagogique & Entreprise** : Prof. A. ABOULFARAJ
- **Durée estimée de la présentation** : 15 à 20 minutes (suivie de 10 à 15 minutes de questions/réponses).
- **Fichier de Présentation** : `kinovatech_cv_parser_presentation.pptx` (Format 16:9 HD Widescreen)

---

## ⏱️ GESTION DU TEMPS PAR DIAPOSITIVE (15 MIN)

| Diapositive | Titre / Thème | Durée conseillée |
| :--- | :--- | :--- |
| **Slide 1** | Page de Garde & Introduction | 1 min 00 s |
| **Slide 2** | Cadre du Stage & Présentation de Kinova Tech | 1 min 15 s |
| **Slide 3** | Problématique Métier & Objectifs du Projet | 1 min 30 s |
| **Slide 4** | Architecture Globale (Pipeline 8 Étapes) | 1 min 30 s |
| **Slide 5** | Couche 1 : Anonymisation PII & Conformité CNDP (Loi 09-08) | 1 min 45 s |
| **Slide 6** | Couche 2 : Extraction d'Entités Nommées (spaCy NER) | 1 min 30 s |
| **Slide 7** | Couche 3 : Enrichissement LLM & API REST FastAPI | 1 min 15 s |
| **Slide 8** | Interface Utilisateur : Dashboard React SaaS | 1 min 30 s |
| **Slide 9** | Base de Données, Infrastructure & Tests Automatisés | 1 min 15 s |
| **Slide 10** | Résultats Chiffrés & Performance Métier (KPIs) | 1 min 00 s |
| **Slide 11** | Démonstration Visuelle & Workflow Utilisateur | 1 min 15 s |
| **Slide 12** | Conclusion & Perspectives d'Évolution (ROADMAP) | 1 min 00 s |
| **Slide 13** | Remerciements & Session Q&A | 0 min 30 s |
| **TOTAL** | | **~15 minutes** |

---

## 🎙️ SCRIPT ORAL DÉTAILLÉ (DISCOURS PAR SLIDE)

### Slide 1 : Page de Garde (01:00)
> **Ce que vous dites :**
> *"Monsieur le Président du Jury, Messieurs les membres du jury, cher encadrant Professeur Aboulfaraj, bonjour.*
> *J'ai l'honneur de vous présenter aujourd'hui le travail réalisé dans le cadre de mon stage de fin d'études au sein de l'entreprise **Kinova Tech**, pour l'obtention du Diplôme Universitaire de Technologie en **Génie Informatique** à l'**EST de Meknès (Université Moulay Ismaïl)**.*
> *Ce projet s'intitule : **« Conception et Déploiement d'une Application de Parsing Intelligent de CVs, Anonymisation PII (Loi 09-08) et Dashboard RH »**."*

---

### Slide 2 : Cadre du Stage & Présentation de Kinova Tech (01:15)
> **Ce que vous dites :**
> *"Mon stage s'est déroulé en modalité **à distance (Remote / Télétravail)** au sein du département IA & IT de la société **Kinova Tech** (`https://kinovatech.com`), entreprise basée à Casablanca spécialisée dans l'ingénierie logicielle, l'Intelligence Artificielle et la souveraineté numérique.*
> *Travailler à distance a exigé une organisation rigoureuse s'appuyant sur les méthodologies Agiles : des **Daily Standups** quotidiens pour faire le point sur l'avancement, l'utilisation de Git/GitHub pour la gestion de version et la revue de code asynchrone, ainsi que la validation continue sous la supervision du Professeur Aboulfaraj."*

---

### Slide 3 : Problématique Métier & Objectifs (01:30)
> **Ce que vous dites :**
> *"Abordons la problématique métier : Les cabinets de recrutement et départements RH reçoivent quotidiennement des centaines de CVs au format PDF ou DOCX. Le dépouillement manuel est extrêmement chronophage (plus de 10 minutes par candidat), sujet à des erreurs d'interprétation et présente un risque majeur de non-conformité au niveau de la confidentialité des données personnelles.*
> *L'objectif principal de ce projet a donc été de concevoir une solution complète capable d'automatiser l'extraction des profils, de structurer les compétences et diplômes, tout en garantissant une **anonymisation stricte PII (Personally Identifiable Information)** conforme à la **Loi marocaine n° 09-08 imposée par la CNDP**."*

---

### Slide 4 : Architecture Globale (Pipeline 8 Étapes) (01:30)
> **Ce que vous dites :**
> *"Pour répondre à ces exigences, j'ai conçu une **Architecture Hybride à 3 Couches**, découpée en un pipeline séquentiel de 8 étapes :*
> *1. **Ingestion & Extraction Textuelle** : Prise en charge des fichiers PDF et DOCX via PyMuPDF et python-docx.*
> *2. **Détection de Langue** : Identification automatique de la langue du document (français, anglais, arabe).*
> *3. & 4. **Couche 1 (Anonymisation Regex)** : Masquage déterministe des données personnelles sensibles sous forme de jetons neutres.*
> *5. **Couche 2 (NLP spaCy NER)** : Extraction sémantique des entités métiers (intitulés de poste, diplômes, compétences).*
> *6. **Couche 3 (Security Gate & LLM)** : Contrôle d'absence absolue de PII brute avant la génération de résumés par un modèle de langage.*
> *7. & 8. **Validation & Persistance** : Structuration JSON stricte via Pydantic v2 et sauvegarde dans la base PostgreSQL."*

---

### Slide 5 : Couche 1 - Anonymisation PII & Loi 09-08 CNDP (01:45)
> **Ce que vous dites :**
> *"La conformité avec la réglementation **CNDP (Loi 09-08)** constitue le cœur de notre engagement sécuritaire.*
> *Sur le plan technique, la Couche 1 s'appuie sur des expressions régulières déterministes qui remplacent les Noms, Prénoms, Adresses Email, Numéros de téléphone marocains (`+212`), Numéros de CIN et Adresses physiques par des jetons neutres comme `[NOM_1]` ou `[EMAIL_1]`.*
> *Afin d'offrir une garantie absolue de zéro fuite de données personnelles vers un LLM ou un service tiers, j'ai implémenté une barrière de sécurité appelée **`Pre-LLM Security Gate`** (`assert_no_raw_pii_before_llm`). Si la moindre donnée non masquée subsiste dans la charge utile, l'exécution est immédiatement bloquée et lève une exception de conformité sécuritaire."*

---

### Slide 6 : Couche 2 - Extraction spaCy NER & Pydantic v2 (01:30)
> **Ce que vous dites :**
> *"La Couche 2 assure l'analyse sémantique grâce au modèle NLP **`fr_core_news_lg`** de **spaCy**.*
> *Ce modèle nous permet de reconnaître avec précision les entités nommées adaptées au marché francophone, notamment les intitulés de postes, les établissements de formation et les compétences clés.*
> *Les données extraites sont ensuite validées par **Pydantic v2**, garantissant la conformité stricte du schéma JSON avec la Section 3.3 du cahier des charges et la cohérence des types avant insertion en base."*

---

### Slide 7 : Couche 3 - LLM & API REST FastAPI (01:15)
> **Ce que vous dites :**
> *"La Couche 3 s'occupe du résumé synthétique du candidat et expose nos services sous forme d'une API REST à haute performance basée sur le framework **FastAPI**.*
> *L'API met à disposition 4 endpoints stratégiques :*
> *- `GET /api/v1/health` : Vérification du statut des services d'infrastructure.*
> *- `POST /api/v1/cvs/upload` : Traitement d'un CV unique en temps réel.*
> *- `POST /api/v1/cvs/batch` : Importation d'archives ZIP contenant jusqu'à 500 CVs.*
> *- `POST /api/v1/cvs/search` : Recherche et filtrage dynamique SQL multi-critères."*

---

### Slide 8 : Dashboard React SaaS (01:30)
> **Ce que vous dites :**
> *"Côté Frontend, j'ai développé un **Dashboard SaaS** moderne avec **React.js et Vite**, offrant un temps de compilation exceptionnel de 1.89 seconde.*
> *L'interface intègre la gestion de la thématique (Dark/Light mode) via des Design Tokens CSS3 Vanilla.*
> *Le tableau de bord permet de surveiller la santé des APIs en direct, d'importer des fichiers via une zone Drag & Drop, d'explorer les candidats via des cartes filtrables, et d'inspecter chaque fiche via un tiroir latéral intégrant un **bouton toggle de sécurité** pour la révélation contrôlée des PII."*

---

### Slide 9 : Base de Données, Infrastructure & Tests (01:15)
> **Ce que vous dites :**
> *"Pour la persistance des données, la solution repose sur **PostgreSQL** géré par l'ORM **SQLAlchemy**, complété par le stockage d'objets **MinIO** pour la conservation isolée des fichiers originaux.*
> *L'ensemble des services d'infrastructure (Postgres, Redis, MinIO) est conteneurisé et orchestré à l'aide de **Docker Compose**.*
> *Enfin, l'assurance qualité s'appuie sur une suite automatisée sous **Pytest** comprenant **44 cas de tests** validés avec un taux de réussite de 100%."*

---

### Slide 10 : Résultats Chiffrés & KPIs (01:00)
> **Ce que vous dites :**
> *"Voici les résultats chiffrés clés obtenus :*
> *- **Moins de 0.5 seconde** en moyenne pour l'analyse et l'anonymisation complète d'un CV.*
> *- **100% de garantie de non-exposition des données brutes** grâce à la Security Gate.*
> *- **100% de succès sur nos 44 tests automatisés Pytest**.*
> *- Et la capacité éprouvée d'ingérer des lots d'archives ZIP de **500 CVs** en une seule opération."*

---

### Slide 11 : Démonstration Visuelle du Dashboard (01:15)
> **Ce que vous dites :**
> *"Sur cette diapositive, vous pouvez observer les parcours utilisateurs majeurs de notre application :*
> *De la vue d'ensemble du Dashboard avec ses métriques et graphiques SVG Donut, jusqu'au processus d'upload par glisser-déposer, à la recherche multicritères par compétences et au tiroir d'inspection de la fiche candidat anonymisée."*

---

### Slide 12 : Conclusion & Perspectives / ROADMAP (01:00)
> **Ce que vous dites :**
> *"En conclusion, ce stage à distance chez Kinova Tech m'a permis d'allier les enseignements théoriques reçus à l'ESTM à la conception d'une application d'ingénierie logicielle concrète, performante et rigoureusement conforme à la Loi 09-08.*
> *Concernant les perspectives d'évolution inscrites dans notre feuille de route :*
> *- L'intégration de **Celery + Redis** pour le traitement asynchrone en tâche de fond de très gros volumes.*
> *- L'orchestration sur **Kubernetes (AWS EKS)** avec autoscaling.*
> *- Et l'intégration de **Tesseract OCR** pour le parsing des CVs numérisés ou scannés."*

---

### Slide 13 : Remerciements & Session Q&A (00:30)
> **Ce que vous dites :**
> *"Je tiens à adresser mes plus sincères remerciements aux membres du jury pour leur écoute attentive, ainsi qu'à l'EST Meknès et l'entreprise Kinova Tech pour leur accompagnement.*
> *Je suis maintenant à votre entière disposition pour répondre à vos questions. Merci."*

---

## ❓ ANTICIPATION DES QUESTIONS DU JURY & RÉPONSES TYPE

### Q1 : Comment garantissez-vous que le modèle LLM ne reçoit aucune PII ?
> **Réponse type :**
> *"Nous appliquons une architecture 'Zero Trust PII'. Avant l'envoi de la charge utile au LLM, le texte passe par la Couche 1 où le moteur Regex substitue chaque PII par un jeton structurel (`[NOM_1]`, `[EMAIL_1]`). Juste avant la requête réseau, la fonction d'assertion `assert_no_raw_pii_before_llm()` scanne le texte à nouveau. Si la moindre expression régulière correspondant à un numéro de téléphone, email ou CIN est détectée, une `SecurityComplianceError` est levée et la requête réseau est immédiatement annulée."*

### Q2 : Pourquoi avoir choisi spaCy (`fr_core_news_lg`) plutôt qu'un LLM direct pour le NER ?
> **Réponse type :**
> *"Le choix de spaCy offre trois avantages majeurs :*
> *1. **Vitesse et coût** : L'exécution locale de spaCy prend quelques millisecondes sans générer de coûts d'API externe.*
> *2. **Déterminisme et contrôle** : spaCy permet d'isoler la reconnaissance des entités en local sans envoyer de données sur des serveurs tiers.*
> *3. **Complémentarité** : spaCy réalise l'extraction structurelle lourde, tandis que le LLM intervient uniquement en Couche 3 sur du texte déjà nettoyé pour générer un résumé synthétique."*

### Q3 : Comment le système réagit-il lors d'un volume massif de CVs (Batch ZIP) ?
> **Réponse type :**
> *"Notre endpoint `POST /api/v1/cvs/batch` traite le fichier ZIP en mémoire ou sous forme de fichiers temporaires isolés. Il parcourt chaque fichier, applique le pipeline d'extraction, et retourne un rapport consolidé contenant le taux de succès, les métriques d'exécution et les erreurs éventuelles par fichier. Pour dépasser la limite de 500 CVs, notre ROADMAP prévoit l'intégration de Celery + Redis pour distribuer la charge sur des workers asynchrones."*

---

## 💡 CONSEILS PRATIQUES POUR LE JOUR J

1. **Testez la projection avant d'entrer** : Assurez-vous que le fichier `.pptx` s'affiche correctement sur le vidéoprojecteur.
2. **Postures et voix** : Parlez d'une voix posée et audible, regardez l'ensemble des membres du jury (Prof. Aboulfaraj et les autres examinateurs).
3. **Gardez le rythme** : 1 minute à 1 minute 30 par diapositive est le tempo idéal pour ne pas dépasser le temps imparti.
4. **Démonstration live (si demandée)** : Ayez le backend (`uvicorn app.main:app --port 8000`) et le frontend (`npm run dev` sur port 5173) en cours d'exécution en arrière-plan au cas où le jury solliciterait une démonstration en direct !

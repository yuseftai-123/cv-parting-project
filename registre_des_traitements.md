# REGISTRE DES TRAITEMENTS DE DONNÉES À CARACTÈRE PERSONNEL
*(Conforme à la Loi marocaine n° 09-08 relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel — CNDP Maroc)*

---

## 1. Finalité du Traitement (Purpose of Processing)

**Texte Officiel / Formal Registration:**
> "Le traitement des documents (Curriculum Vitae) a pour finalité exclusive l'extraction automatique des compétences professionnelles, des expériences et des diplômes des candidats à des fins d'analyse RH et d'aide au recrutement. Les données personnelles identifiables sont anonymisées et masquées dès l'ingestion afin de prévenir tout profilage automatisé non consenti."

---

## 2. Catégories de Données Collectées (Categories of Data Collected)

**Texte Officiel / Formal Registration:**
> - **Données Identifiables (Masquées immédiatement via Regex Layer 1)** : Nom, Prénom, Numéro de Téléphone (format +212/local), Adresse Email, Numéro de Carte d'Identité Nationale (CIN), Date de Naissance, Adresse Postale.
> - **Données Professionnelles Utiles (Conservées dans le Profil Résumé)** : Titre du poste, Années d'expérience totale, Intitulés de diplômes et d'établissements, Soft & Hard Skills déclarés, Langues maîtrisées, Certifications.

---

## 3. Durée de Conservation (Retention Period)

**Texte Officiel / Formal Registration:**
> - **Fichiers Source BRUTS (.pdf / .docx / .zip)** : Supprimés immédiatement après l'extraction initiale ou conservés pour une durée maximale de 30 jours sous forme chiffrée.
> - **Profils Structurés Résumés (JSON)** : Conservés pour une durée maximale de 2 ans à compter de la date de dépôt par le candidat, ou supprimés immédiatement sur simple demande d'exercice du Droit à l'Oubli (Article 7 de la Loi 09-08).

---

## 4. Mesures de Sécurité Technique & Organisationnelle (Security Measures — Section 5.1)

**Texte Officiel / Formal Registration:**
> 1. **Gate de Masquage Déterministe (Layer 1 Regex)** : Remplacement de 100% des identifiants directs par des jetons neutres (`[NOM_1]`, `[EMAIL_1]`) avant toute expédition vers les modèles d'IA.
> 2. **Gate d'Assertion Pré-Dispatch (SF-07)** : Blocage d'urgence (`SecurityComplianceError`) interceptant tout payload d'API contenant du PII non masqué.
> 3. **Chiffrement & Isolation des Accès** : Stockage isolé des bases PostgreSQL et stockage objet MinIO accessible uniquement via des variables d'environnement sécurisées.
> 4. **Traces d'Audit Anonymes (SF-08)** : Journalisation limitée aux temps d'exécution et identifiants uniques sans aucune fuite de données personnelles dans les logs serveur.

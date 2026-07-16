# DA EgaPro — Questionnaire de complétion

Champs non dérivables du code source, à renseigner par les responsables désignés.
Chaque item renvoie au cadre du DA. À traiter avant de finaliser le `.docx`.

---

## MOA (maîtrise d'ouvrage — DGT présumée)

**Cadre 1 — Projet**
- [ ] Enjeux métier, juridiques et politiques du dispositif de transparence salariale.
- [ ] Validation du contexte et des objectifs pré-rédigés (résumé technique tiré du README).
- [ ] Planning : dates de mise en service V1 / V2 / V3 et jalons.
- [ ] Acteurs projet : noms, fonctions et entités (MOA, AMOA, MOE, AMOE — voir aussi Architecte SI / Prod).

**Cadre 1 — Acteurs métier (nombres d'utilisateurs)**
- [ ] Nombre d'entreprises déclarantes (et ordre de grandeur des co-déclarants).
- [ ] Nombre d'agents administrateurs DGT/DNUM.
- [ ] Volume de consultation publique attendu.

**Cadre 3 — Contraintes & volumétrie**
- [ ] Contraintes légales et métier (échéances réglementaires, obligations par taille d'entreprise).
- [ ] Volumétrie données D1–D4 : nb d'occurrences/an, nb créées/an, taille unitaire, durée de rétention (D5–D7 seront calculés).
- [ ] Volumétrie fichiers F1–F4 : nb total, nb créés/an, taille moyenne (plafond technique 10 Mo), rétention (F5–F7 calculés).
- [ ] Utilisabilité tablette/smartphone : niveaux attendus (connecté/déconnecté), nombre d'appareils.

**Cadre 4 — QoS**
- [ ] Temps de réponse cibles (par fonctionnalité, régime standard vs charge).
- [ ] Périodes applicatives (standard/critique/charge — ex. pic de campagne annuelle en mars/mai).

---

## RSSI

**Cadre 4 — Sécurité (cotation EBIOS, aucune valeur inventée)**
- [ ] Cotation DICT (Disponibilité, Intégrité, Confidentialité, Traçabilité) niveaux 1–4, en Front et en Back.
  - Indices disponibles pour cadrer la saisie : journal d'audit exhaustif + adresses IP (traçabilité élevée), données personnelles + rémunérations confidentielles (indicateur G), HA en production (autoscale, réplicas). Aucune donnée de santé ni NIR détectée.
- [ ] Exigence de preuve par fonctionnalité (ou « Non concerné »).
- [ ] Échelle d'impact EBIOS (domaine, niveau, description, contexte).
- [ ] Validation des points d'attention sécurité :
  - `GET /api/export/download` et `POST /api/export/generate` sans authentification applicative (reposent sur l'isolement réseau) — acceptable ?
  - Issuer ProConnect de production pointant sur `proconnecttest` — à corriger/valider.

---

## DPO

**Cadre 3 — Données personnelles**
- [ ] Qualification finale de la sensibilité des données (le code révèle : identité déclarant — nom, courriel, téléphone ; SIREN/raison sociale/adresse ; adresses IP en journal d'audit ; rémunérations par catégorie).
- [ ] Validation des durées de rétention : audit 180/365 j, brouillons 30 j, déclarations conservées sans purge, historique de statut en rétention permanente. Cohérence avec l'analyse RGPD / la mention CNIL ?
- [ ] Base légale et information des personnes (registre des traitements).

---

## MOE / ARCHITECTE SI

**Cadre 4 — Garantie de service**
- [ ] PCA / PRA / PDMA / DMIA et impacts associés (à décider avec l'hébergeur).

**Cadre 11 — Dimensionnement**
- [ ] Justifications PDMA/DMIA/performances (lien vers les exigences du cadre 4).
- [ ] Justification de l'allocation de ressources (nombre de CPU, nombre de serveurs) — le dépôt fixe les requests/limits K8s de l'app, du worker, du cache et de la passerelle, mais pas le dimensionnement cible global.

**Cadre 12 — URLs**
- [x] Les 3 URLs sortantes (SUIT, GIP-MDS, stockage S3) ont été **ajoutées** au cadre 12 (via `postprocess_da.py`) — les 8 URLs sont désormais présentes.

**Cadre 1 / 9**
- [ ] Confirmer le nom du projet applicatif « EgaPro » et l'entité MOE (Fabrique/SocialGouv présumée).
- [ ] Confirmer l'assimilation « serveur logique = déploiement Kubernetes » (le modèle MASS attend des VM ; ici tout est conteneurisé).

---

## PROD / HÉBERGEUR

**Cadre 9 — Serveurs**
- [x] Blocs serveurs `EGAPRO.APISIX` et `EGAPRO.AV` **ajoutés** (via `postprocess_da.py`) — les 6 serveurs logiques sont désormais dans le cadre 9.
- [ ] Saisir les cellules **Type / Rôle / VCPU / RAM** des 6 blocs serveurs (fusionnées, laissées vides par le pipeline). Valeurs dérivées disponibles dans `contenu.json` : APP autoscale 2-6 pods (0,5-1 vCPU / 1-2 Go), NOTIF (0,05-0,3 vCPU / 96-256 Mio), CACHE (0,1-1 vCPU / 256 Mio-1 Gio), APISIX 2 replicas (0,05-0,5 vCPU / 128-512 Mio) ; BDD et AV = [À COMPLÉTER — PROD].
- [ ] Version PostgreSQL de production (dev = 14.17 ; opérateur `pg` en prod).
- [ ] Co-localisation ou séparation de la base notifications (`EGAPRO.BDD.NOTIF` / pg-boss) vs base principale.
- [ ] Ressources CPU/RAM de la base de données et de ClamAV (non fixées dans le dépôt).
- [ ] Version ClamAV de production (dev = 1.5.2).
- [ ] Image de base (O.S.) du conteneur applicatif (pas de Dockerfile dans le dépôt — build Kontinuous).

**Cadre 8 / 10 — Réseau**
- [ ] Placement précis des composants en DMZ (publique / privée / applicative dédiée).
- [ ] Canal réseau M/R/E/P des flux inter-SI et des accès agents (l'app est exposée sur Internet ; le rattachement intranet MASS/RIE des agents et de SUIT n'est pas déterminable depuis le code).
- [ ] Passage par une PFAI pour les appels sortants (ProConnect, INSEE/Weez, SUIT, GIP-MDS, SMTP).
- [ ] Confirmer le reverse-proxy/ingress de production (Traefik/nginx selon environnement).

---

## INTÉGRATION

**Cadre 3 — Dépendances SI**
- [ ] Statut de l'intégration D@ccords : lien externe UI aujourd'hui — une intégration technique est-elle prévue ?
- [ ] Confirmer que la source du CSV GIP-MDS transite bien par SUIT/Delphes.
- [ ] Confirmer les conventions d'échange (SLA, formats, fréquences) avec ProConnect, INSEE Sirene, GIP-MDS, SUIT.

---

## Annexe — Suivi des changements (à compléter à la génération du .docx)

- [ ] Version : `V0.1.0` (génération initiale).
- [ ] Date de la demande, demandeur, rapporteur.
- [ ] Description : « Génération initiale assistée à partir du code source — à valider par la MOE et l'architecte SI ».

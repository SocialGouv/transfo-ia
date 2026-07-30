# Rapport de provenance — DA-Egapro

| Cadre | Champ | Statut | Valeur | Source (fichier/preuve) |
|---|---|---|---|---|
| 1 | Nom du projet | DÉRIVÉ | Egapro | `egapro/package.json` — `"name": "egapro"` |
| 1 | Contexte | DÉRIVÉ | Plateforme gouvernementale de déclaration de l'index de l'égalité professionnelle femmes-hommes… | `egapro/README.md` — lignes 3-10 |
| 1 | Objectifs | DÉRIVÉ | Mesurer et déclarer les écarts de rémunération… simplifier le processus déclaratif… transparence | `egapro/README.md` — lignes 3-9 |
| 1 | Enjeux | INFÉRÉ | Conformité réglementaire ; transparence salariale ; pilotage politiques d'égalité | Inféré du contexte réglementaire (directive UE 2023/970) et du public visé (DGT) |
| 1 | Planning V1/V2/V3 | À COMPLÉTER | Dates manquantes | Non dérivable du code |
| 1 | Acteurs projet (MOA, MOE, RSSI…) | À COMPLÉTER | Noms/fonctions/entités | Non dérivable du code |
| 1 | Acteurs métiers — Profils | DÉRIVÉ | 4 profils : Déclarant entreprise, Administrateur DGT, Inspection du travail (SUIT), Grand public | `packages/app/src/middleware.ts` (routes admin/protégées/publiques) ; `packages/app/src/app/api/v1/` (API SUIT) ; `packages/app/src/app/stats/page.tsx` (consultation publique) |
| 1 | Acteurs métiers — Nombres | À COMPLÉTER | Nombre d'utilisateurs par profil | Non dérivable du code |
| 2 | Fonctionnalités | DÉRIVÉ | 12 fonctionnalités listées | `packages/app/src/app/` (routes : déclaration, avis-cse, admin, stats, export, etc.) ; `packages/app/src/server/api/routers/` (tRPC procedures) ; `packages/app/README.md` |
| 2 | Données métier | DÉRIVÉ | 9 types de données métier | `packages/app/src/server/db/schema.ts` (tables : declarations, job_categories, employee_categories, gip_mds_data, cse_opinions, files, companies, referents, exports, action_logs) |
| 2 | Fichiers métier | DÉRIVÉ | 5 types de fichiers | `packages/app/src/app/api/upload/` (route d'upload) ; `packages/app/src/server/db/schema.ts` (table `file`, type enum : cse_opinion, joint_evaluation) ; `packages/app/src/app/api/export/` (exports CSV) |
| 2 | Référentiels hors SI | DÉRIVÉ | 5 référentiels externes | `packages/app/src/env.js` (URLs : WEEZ, GIP-MDS, ProConnect, SUIT) ; `packages/app/README.md` (dépendances externes) |
| 3 | Sensibilité des données | INFÉRÉ | Données personnelles (NIR via DSN, emails, données salariales) — pré-cotation DICT à confirmer par le DPO | `packages/app/src/server/db/schema.ts` (PII dans users, entreprises, déclarations) ; `packages/app/src/server/db/auditSchema.ts` (journalisation CNIL) |
| 3 | Services utilisés | DÉRIVÉ | 7 services : SMTP/Tipimail, S3/MinIO, ClamAV, Matomo, Sentry, Valkey, pg-boss | `docker-compose.yml` ; `packages/app/src/env.js` ; `packages/notifications/package.json` |
| 3 | Dépendances avec d'autres SI | DÉRIVÉ | WEEZ (fournisseur), GIP-MDS (fournisseur), ProConnect (fournisseur), SUIT (consommateur), D@ccords (consommateur) | `packages/app/src/env.js` ; `packages/app/README.md` |
| 3 | Réduction volume (purge/archivage) | DÉRIVÉ | Purge automatique des logs d'audit : 180j (read_sensitive), 365j (autres) ; export CSV quotidien | `packages/app/scripts/audit-cleanup.mjs` ; `.kontinuous/templates/` (CronJobs) ; `packages/app/src/server/db/auditSchema.ts` |
| 3 | Dépendances poste de travail | À COMPLÉTER | Non dérivable du code |
| 3 | Utilisabilité tablette/smartphone | DÉRIVÉ | Application responsive (DSFR) — PWA non détectée | `packages/app/src/modules/layout/` (DSFR responsive) ; `packages/app/CLAUDE.md` (breakpoints DSFR) |
| 3 | Volumétrie D1-D4 / F1-F4 | À COMPLÉTER | Hypothèses métier | Non dérivable du code |
| 4 | DICT EBIOS (Dispo/Intégrité/Confid/Traçabilité) | INFÉRÉ | Éléments d'indices : auth forte (ProConnect OIDC), chiffrement (TLS partout), journalisation d'audit (audit.action_log), sauvegardes (PostgreSQL). Cotation formelle à confirmer par le RSSI | `packages/app/src/middleware.ts` (auth guards) ; `packages/app/src/server/db/auditSchema.ts` (audit logging) ; `docker-compose.yml` (PostgreSQL avec healthcheck) |
| 4 | Traitements automatisés (batchs) | DÉRIVÉ | 3 CronJobs K8s + 13 schedules pg-boss | `.kontinuous/templates/` (CronJobs) ; `packages/notifications/src/schedules/definitions.ts` (13 schedules) |
| 4 | Périodes applicatives | À COMPLÉTER | Non dérivable du code |
| 4 | Garantie de service (PCA/PRA/PDMA/DMIA) | À COMPLÉTER | Non dérivable du code |
| 4 | Temps de réponse | À COMPLÉTER | Non dérivable du code |
| 4 | Exigence PREUVE | À COMPLÉTER | Non dérivable du code |
| 5-8 | Schémas d'architecture | À COMPLÉTER | Spécifications produites en annexe ; dessin manuel | Non dérivable du code (schémas visuels) |
| 9 | Serveurs logiques | INFÉRÉ | 6 serveurs : EGAPRO.APP, EGAPRO.NOTIF, EGAPRO.BDD, EGAPRO.CACHE, EGAPRO.S3, EGAPRO.CLAMAV | `docker-compose.yml` (services) ; `Dockerfile` (build) ; `.kontinuous/` (déploiement) |
| 9 | Composants logiciels | DÉRIVÉ | Pile complète par serveur (catégorie, composant, version, rôle) | `packages/app/package.json` (dépendances Next.js, React, tRPC, Drizzle…) ; `packages/notifications/package.json` (pg-boss, nodemailer…) ; `docker-compose.yml` (images : postgres:14.17, valkey/valkey:8-alpine, clamav/clamav-debian:1.5.2) |
| 9 | VCPU/RAM | À COMPLÉTER | Ressources matérielles | Non dérivable du code |
| 10 | Matrice des flux | DÉRIVÉ | 17 flux numérotés | `docker-compose.yml` (ports, services interconnectés) ; `packages/app/src/env.js` (URLs externes) ; `packages/app/src/middleware.ts` (APISIX/proxy) ; `packages/app/README.md` (architecture) |
| 11 | Dimensionnement (PDMA/DMIA/CPU/serveurs) | À COMPLÉTER | Non dérivable du code |
| 12 | URLs applicatives | DÉRIVÉ | 9 URLs listées (avec acteur, ressource, fonctionnalité, données) | `packages/app/src/env.js` (toutes les URLs de services externes) ; `packages/app/README.md` (URLs API, ProConnect) |
| Annexe | Suivi des versions | DÉRIVÉ | V0.1.0 — Génération initiale assistée | Génération IA |

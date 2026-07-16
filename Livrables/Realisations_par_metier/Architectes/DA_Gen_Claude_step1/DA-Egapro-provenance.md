# DA EgaPro — Rapport de provenance

Audit de traçabilité de la génération assistée. Chemins relatifs à la racine du dépôt `egapro/`.
Statuts : **DÉRIVÉ** (établi depuis le code, preuve à l'appui) · **INFÉRÉ** (hypothèse plausible, à confirmer).
Les champs `À COMPLÉTER` figurent dans `DA-Egapro-a-completer.md`.

> Généré à partir de l'état du code au commit `057d6b1d` (2026-06-29). Version applicative CHANGELOG : 3.13.2 (08/10/2025).

## Cadre 1 — Projet & Acteurs

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Nom du projet applicatif | DÉRIVÉ | EgaPro | `package.json:2` (`"name": "egapro"`), `README.md:1` |
| Contexte | INFÉRÉ | Déclaration des indicateurs d'égalité de rémunération F/H (7 indicateurs A–G) | `README.md:1-41`, `CLAUDE.md:9-16` |
| Objectifs | INFÉRÉ | Déclaration A–G, parcours de conformité (seuil 5 %), avis CSE, consultation publique | `README.md:42-69` |
| Entité MOE | INFÉRÉ | Fabrique numérique des ministères sociaux / SocialGouv | org GitHub `SocialGouv/egapro`, Sentry org `incubateur` (`packages/app/next.config.js:53-54`), domaines `*.fabrique.social.gouv.fr` |
| Contact technique | DÉRIVÉ | « Équipe EGAPRO — DNUM » | `packages/app/src/modules/export/openapi.ts:477-488` (contact OpenAPI) |
| Version applicative courante | DÉRIVÉ | 3.13.2 (08/10/2025) | `CHANGELOG.md:1`, `package.json:3` |
| Nature « refonte V2 » | INFÉRÉ | Réécriture Next.js/DSFR distincte de l'index historique | projet Sentry `egapro-v2` (`next.config.js:54`) ; stack Next.js 16 |
| Profils d'acteurs métier | INFÉRÉ | Entreprise déclarante ; agent administrateur DGT/DNUM ; grand public | modèle de rôles `users.isAdmin` (`src/server/db/schema.ts`), guards tRPC `src/server/api/trpc.ts`, back-office `src/app/admin/*` |

## Cadre 2 — Exigences fonctionnelles

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Parcours de déclaration A–G (7 étapes) | DÉRIVÉ | Étapes 0–6 (intro, effectifs, écarts, quartiles, indicateur G, récap) | `src/app/declaration-remuneration/(with-banner)/etape/[step]/page.tsx`, `src/modules/domain/shared/declarationSteps.ts:12` |
| Indicateur G par catégories | DÉRIVÉ | Saisie effectifs + rémunérations base/variable par catégorie | tables `app_job_category`, `app_employee_category` (`src/server/db/schema.ts:309-376`) |
| Parcours de conformité (seuil 5 %) | DÉRIVÉ | `justify` / `corrective_action` / `joint_evaluation` | enum `compliance_path` (`src/server/db/schema.ts:29-33`), `.../parcours-conformite/page.tsx` |
| Dépôt avis CSE / évaluation conjointe | DÉRIVÉ | Upload PDF/PNG/JPEG, parcours dédiés | `src/app/avis-cse/*`, `src/app/.../evaluation-conjointe/page.tsx`, `src/app/api/upload/route.ts` |
| Consultation publique référents / stats / export | DÉRIVÉ | Pages + API publiques (JSON/CSV) | `src/app/referents/page.tsx`, `src/app/stats/page.tsx`, `src/app/api/public/referents-egalite-professionnelle/route.ts:57` |
| Back-office administration | DÉRIVÉ | Déclarations, référents, stats, paramètres, impersonation | `src/app/admin/*`, routers `adminDeclarations`/`adminReferents`/`adminStats`/`adminSettings` |
| API d'export SUIT (`/api/v1/*`) | DÉRIVÉ | Export déclarations + métadonnées/téléchargement fichiers | `src/app/api/v1/export/declarations/route.ts`, `src/app/api/v1/files/[fileId]/route.ts`, `src/modules/export/openapi.ts` |
| Données métier (entités) | DÉRIVÉ | Déclarations, indicateur G, avis CSE, entreprises, users, GIP-MDS, référents, historique statuts | `src/server/db/schema.ts` (tables `app_*`), `src/server/db/schema-comments.ts` |
| Fichiers métier | DÉRIVÉ | Types `cse_opinion`, `joint_evaluation` ; MIME pdf/png/jpeg ; max 10 Mo | `src/server/db/schema.ts:592-624`, `src/modules/shared/uploadConfig.ts:2,28-32` |
| Nb max fichiers CSE | DÉRIVÉ | 4 (`MAX_CSE_FILES`) | `src/modules/domain/shared/constants.ts:20` — **écart avec README « 3 avis » (`README.md:61`)** |
| Référentiels externes | DÉRIVÉ | ProConnect, INSEE Sirene (Weez), GIP-MDS, SUIT | services `src/server/services/{weez,suit,gipMds}.ts`, `src/server/auth/config.ts` |

## Cadre 3 — Contraintes & Volumétrie

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Sensibilité — indices PII | INFÉRÉ | Données personnelles (identité déclarant : nom, courriel, téléphone), adresses IP en journal d'audit ; pas de NIR ni donnée de santé détectés | `src/server/db/schema.ts:52-61`, `src/server/db/auditSchema.ts:33-52` |
| Sensibilité — indices données économiques | INFÉRÉ | Rémunérations par catégorie (indicateur G) confidentielles | `README.md:66` (« indicateur G reste confidentiel »), table `app_employee_category` |
| Services utilisés | DÉRIVÉ | SMTP (Tipimail), ClamAV, S3 (OVH), Valkey, Matomo, Sentry | voir Cadre 9 / Cadre 10 |
| Dépendances SI (fournisseur/consommateur) | DÉRIVÉ | ProConnect, INSEE/Weez, GIP-MDS (fourn.) ; SUIT (fourn. + consomm.) | services `src/server/services/*.ts`, API `src/app/api/v1/*` |
| D@ccords | DÉRIVÉ | Lien externe UI, **aucune intégration technique** | mentionné `README.md:109` ; aucun client HTTP dans le code |
| Utilisabilité mobile | INFÉRÉ | Responsive DSFR (pas de PWA/offline détecté) | `@gouvfr/dsfr` (`packages/app/package.json:47`) |
| Réduction volume — journal d'audit | DÉRIVÉ | Purge : 180 j (accès sensibles/recherche publique), 365 j (autres) | `src/modules/audit/shared/constants.ts:11-12`, `scripts/audit-cleanup.mjs`, `.kontinuous/templates/audit-cleanup-cron.yaml` |
| Réduction volume — brouillons | DÉRIVÉ | Expiration **30 j**, paresseuse (filtre en lecture), **sans purge physique** | `src/server/api/routers/declarationDraft.ts:16,42-44,74` — **écart avec README « 2 mois » (`README.md:49`)** |
| Réduction volume — déclarations/fichiers | DÉRIVÉ | Pas de purge ; déclaration soft-cancel (`cancelledAt`), historique en rétention permanente | `src/server/db/schema.ts:178`, `src/server/db/schema-comments.ts:163` |

## Cadre 4 — Traitements automatisés (partie dérivable)

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Import GIP-MDS | DÉRIVÉ | CronJob quotidien `0 3 * * *` → `POST /api/gip-mds/import` (Bearer) | `.kontinuous/templates/gip-mds-import-cron.yaml:7,38-39` |
| Génération export XLSX | DÉRIVÉ | CronJob quotidien `0 2 * * *` → `POST /api/export/generate` | `.kontinuous/templates/export-cron.yaml:7,30` |
| Purge journal d'audit | DÉRIVÉ | CronJob quotidien `0 4 * * *` (accès DB direct) | `.kontinuous/templates/audit-cleanup-cron.yaml:7,75-77` |
| Relances courriel planifiées | DÉRIVÉ | 13 planifications pg-boss (cron, tz Europe/Paris) | `packages/notifications/src/schedules/definitions.ts:41-108` |
| Traçabilité (indice) | INFÉRÉ | Journal d'audit exhaustif (mutations + accès sensibles), IP, comparaison à temps constant, schéma audit découplé RGPD | `src/server/api/trpc.ts:108-110`, `src/server/db/auditSchema.ts:6-8`, `src/middleware.ts:82-106` |

> La cotation DICT/EBIOS, les SLA, PCA/PRA/PDMA/DMIA et les temps de réponse ne sont pas dérivables du code → `À COMPLÉTER` (RSSI/MOA/HÉBERGEUR).

## Cadres 5 à 8 — Schémas

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Acteurs, fonctions, composants, flux | DÉRIVÉ/INFÉRÉ | cf. blocs `schemas.cadre5..8` du JSON | consolidation des cadres 1, 2, 9, 10 |
| Placement précis en DMZ | À COMPLÉTER | — | relève de PROD/HÉBERGEUR |
| Modèle de déploiement | DÉRIVÉ | Conteneurisé (Kubernetes / Kontinuous), **pas des VM** | `.kontinuous/**`, `docker-compose.yml` |

## Cadre 9 — Serveurs & Composants

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Découpage en serveurs logiques | DÉRIVÉ | APP, NOTIF, BDD, BDD.NOTIF, CACHE, APISIX, AV | `.kontinuous/values.yaml`, `.kontinuous/templates/*`, `docker-compose.yml` |
| EGAPRO.APP — ressources | DÉRIVÉ | req. 500m CPU / 1 Go ; lim. 1 CPU / 2 Go ; autoscale 2–6 | `.kontinuous/env/prod/values.yaml:8-18` |
| EGAPRO.NOTIF — ressources | DÉRIVÉ | req. 50m / 96 Mio ; lim. 300m / 256 Mio ; 1 replica (Recreate) | `.kontinuous/templates/notifications-deployment.yaml:27-31,216-222` |
| EGAPRO.CACHE (Valkey) — version/ressources | DÉRIVÉ | Valkey 9.0.2 ; prod 1 primaire + 2 replicas ; req. 100m/256Mi, lim. 1/1Gi | `.kontinuous/values.yaml:157-180`, `.kontinuous/env/prod/values.yaml:20-39` |
| EGAPRO.APISIX — version/ressources | DÉRIVÉ | APISIX 3.11.0-debian ; prod 2 replicas ; req. 50m/128Mi, lim. 500m/512Mi | `.kontinuous/templates/apisix-suit.yaml:63,85,117-123`, `.kontinuous/values.yaml:10-17` |
| EGAPRO.AV (ClamAV) — version | INFÉRÉ | ClamAV 1.5.2 (dev docker) — prod à confirmer | `docker-compose.yml:92` ; chart `clamav` (`.kontinuous/values.yaml:182-183`) |
| EGAPRO.BDD — version | INFÉRÉ | PostgreSQL 14.17 (dev docker) — prod à confirmer (opérateur `pg`) | `docker-compose.yml:4`, `.kontinuous/Chart.yaml`/`values.yaml:152-153` |
| Composants applicatifs + versions | DÉRIVÉ | Next.js 16.2, React 19.2, DSFR 1.14.4, tRPC 11.16, NextAuth 4.24.13, Drizzle 0.45.2, TS 6.0, Zod 4.3, @aws-sdk/client-s3 3.x, ExcelJS 4.4, @react-pdf/renderer 4.4, redis 5.11, @sentry/nextjs 10.48 | `packages/app/package.json:45-97` |
| Worker — composants | DÉRIVÉ | pg-boss 12.18.2, Nodemailer 7.0, @react-email 1.0 | `packages/notifications/package.json:36-45` |
| Runtime Node | DÉRIVÉ | Node.js 24 | `.nvmrc` (`24`), `package.json:10` (`"node": ">=24"`) |
| Gestionnaire de paquets | DÉRIVÉ | pnpm 10.8.1 (workspaces) | `package.json:8`, `pnpm-workspace.yaml` |
| O.S. image de base | À COMPLÉTER | — | pas de Dockerfile applicatif dans le dépôt (build Kontinuous) |

## Cadre 10 — Matrice des flux

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Flux 1–3, 6 (usagers → RP → APP) | DÉRIVÉ | HTTPS ; ingress + `containerPort 3000` | `.kontinuous/values.yaml:25-26`, `.kontinuous/env/prod/values.yaml:2` |
| Flux 4–5 (SUIT → APISIX → APP) | DÉRIVÉ | HTTPS clé Bearer ; upstream `app:80` + `X-Gateway-Forwarded` | `.kontinuous/templates/apisix-suit.{ingress,configmap}.yaml`, `src/middleware.ts:82-106` |
| Flux 7 (APP → BDD) | DÉRIVÉ | TCP PostgreSQL (SSL) | `src/env.js` (`DATABASE_URL`), `.kontinuous/values.yaml:73-102` |
| Flux 8, 16 (file pg-boss) | DÉRIVÉ | TCP PostgreSQL | `packages/notifications/src/db.ts`, `publisher.ts` |
| Flux 9 (APP → Valkey) | DÉRIVÉ | TCP Redis ; `redis://valkey:6379` | `packages/app/cache-handler.cjs`, `.kontinuous/values.yaml:158-159` |
| Flux 10 (APP → ClamAV) | DÉRIVÉ | TCP INSTREAM (pas ICAP) | `src/server/services/clamav.ts:25-135` |
| Flux 11 (APP → S3) | DÉRIVÉ | HTTPS S3 ; `s3.gra.io.cloud.ovh.net` (prod) | `src/server/services/s3.ts:23-33`, `.kontinuous/env/prod/templates/s3.configmap.yaml` |
| Flux 12–15 (SI externes sortants) | DÉRIVÉ | ProConnect (OIDC), INSEE/Weez, SUIT, GIP-MDS | `src/server/services/{weez,suit,gipMds}.ts`, `src/server/auth/config.ts:170-219` |
| Flux 17 (worker → BDD audit) | DÉRIVÉ | TCP PostgreSQL | `packages/notifications/src/worker/auditLog.ts:31` |
| Flux 18 (worker → SMTP) | DÉRIVÉ | SMTP STARTTLS ; Tipimail (prod) | `packages/notifications/src/worker/transporter.ts:7-33` |
| Flux 19 (CronJobs → APP) | DÉRIVÉ | HTTP interne | `.kontinuous/templates/{gip-mds-import,export}-cron.yaml` |
| Flux 20–21 (Matomo, Sentry) | DÉRIVÉ | HTTPS | `src/server/services/matomo.ts`, `next.config.js:53-62` |
| Canal réseau (M/R/E/P) inter-SI | À COMPLÉTER | — | exposition réseau non tranchable depuis le code |

## Cadre 12 — URLs

| Champ | Statut | Valeur | Source / preuve |
|---|---|---|---|
| Hôte applicatif (prod) | DÉRIVÉ | `egapro.travail.gouv.fr` | `.kontinuous/env/prod/values.yaml:2` |
| Redirections | DÉRIVÉ | `egapro.fabrique.social.gouv.fr`, `index-egapro.travail.gouv.fr` | `.kontinuous/env/prod/values.yaml:5-7` |
| Hôte API SUIT | DÉRIVÉ | `api-suit-egapro.travail.gouv.fr` | `.kontinuous/templates/apisix-suit.ingress.yaml:30-33` |
| URLs externes consommées | DÉRIVÉ | ProConnect issuer, Weez `/public/v3/unitelegale/findbysiren`, SUIT `/suit/api/externe/portail/{CSE,sanction}/{siren}`, GIP-MDS, S3 OVH | `src/server/services/{weez,suit}.ts`, `.kontinuous/env/*/templates/*.configmap.yaml` |
| Issuer ProConnect (prod) | INFÉRÉ | pointe sur un environnement `proconnecttest` | `.kontinuous/env/prod/templates/proconnect.configmap.yaml` — **à vérifier (prod vs test)** |

## Points d'attention (écarts code ↔ documentation)

1. **Brouillons** : code = 30 j en lecture paresseuse, sans purge ; README = « 2 mois ». (`declarationDraft.ts:16` vs `README.md:49`)
2. **Fichiers CSE** : code `MAX_CSE_FILES = 4` ; README = « 3 avis ». (`constants.ts:20` vs `README.md:61`)
3. **Antivirus** : ClamAV en **TCP/INSTREAM**, pas ICAP (contrairement au modèle SIRANO).
4. **D@ccords** : cité comme dépendance mais **aucune intégration technique** dans le code.
5. **Consultation publique des index** (recherche SIREN/entreprise, « Observatoire ») : portée par un **site externe** (`index-egapro`), pas par ce dépôt. Ce DA couvre la **déclaration** + la consultation des **référents/statistiques**.
6. **Issuer ProConnect en prod** = `proconnecttest` : configuration à vérifier.
7. **`GET /api/export/download` / `POST /api/export/generate`** : pas d'authentification applicative (reposent sur l'isolement réseau du cluster) — à valider côté sécurité.
8. **Modèle de serveurs** : déploiement **conteneurisé Kubernetes**, pas des VM. Le gabarit MASS attend « Machine Virtuelle » : l'écart est signalé dans le champ `type` de chaque serveur.
9. **Capacité du gabarit — Cadre 9** : le modèle n'offre que **2 blocs = 4 emplacements serveurs**. Le `.docx` généré écrit les 4 serveurs cœur (EGAPRO.APP, EGAPRO.NOTIF, EGAPRO.BDD [2 bases : `egapro` + `egapro_notifications`], EGAPRO.CACHE). **EGAPRO.APISIX (Apache APISIX 3.11.0) et EGAPRO.AV (ClamAV 1.5.2) dépassent cette capacité et sont à ajouter manuellement** (bloc serveur supplémentaire). Ils restent documentés aux cadres 8 (schéma technique) et 10 (matrice des flux).
10. **Capacité du gabarit — Cadre 12** : le modèle offre **5 blocs URL**. Les 5 premières sont écrites (app `egapro.travail.gouv.fr`, API SUIT `api-suit-egapro`, redirections, ProConnect, INSEE/Weez). Les **3 URLs sortantes restantes — SUIT (CSE/sanction), GIP-MDS, S3 OVH — sont à ajouter manuellement** ; elles figurent déjà à la matrice des flux (cadre 10).

# Rapport de provenance — DA-Egapro-V0.1.0

> Généré le 2026-07-15 à partir du code source du dépôt `SocialGouv/egapro`.
> Statuts : **DÉRIVÉ** (preuve dans le code) | **INFÉRÉ** (hypothèse, à confirmer)

## Légende

| Symbole | Signification |
|---|---|
| `DÉRIVÉ` | Établi depuis le code, avec preuve |
| `INFÉRÉ` | Hypothèse plausible tirée d'indices du code |

---

## Cadre 1 — Projet & Acteurs

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Nom du projet applicatif | DÉRIVÉ | EGAPRO | `package.json` racine : `"name": "egapro"`, `README.md` |
| Contexte / Objectifs / Enjeux | INFÉRÉ | Synthèse à partir du README | `README.md` lignes 3-9, 79-110 |
| Planning V1 | INFÉRÉ | « Première version, héritage » | `CHANGELOG.md`, `docs/architecture.md` §1 (mention V1 legacy) |
| Planning V2 (actuelle) | INFÉRÉ | Refonte Next.js 16 / App Router | `docs/architecture.md` §1 ; `next.config.js` ; `package.json` |
| Acteurs projet (noms) | — | `[À COMPLÉTER]` | Non dérivable du code |
| Acteurs métiers — Déclarant entreprise | DÉRIVÉ | Profil identifié par les routes protégées + auth ProConnect | `src/server/api/trpc.ts` (protectedProcedure) ; `src/server/auth/config.ts` ; parcours `declaration-remuneration` |
| Acteurs métiers — Admin DGT | DÉRIVÉ | Profil admin : `isAdmin` flag, routes `/admin/*` | `src/server/db/schema.ts` (app_user.isAdmin) ; `src/middleware.ts` (admin guard) ; `src/app/admin/` |
| Acteurs métiers — Grand public | DÉRIVÉ | Pages publiques : `/stats`, `/referents`, `/faq` | `src/app/stats/page.tsx`, `src/app/referents/page.tsx`, `src/app/faq/page.tsx` |
| Acteurs métiers — Inspection du travail (SUIT) | DÉRIVÉ | API privée `/api/v1/*` avec auth APISIX | `src/app/api/v1/` ; `src/server/services/suit.ts` ; `src/middleware.ts` |
| Acteurs métiers — Référents DREETS/DDETS | DÉRIVÉ | Module `referents` + table `app_referent` | `src/server/db/schema.ts` (app_referent) ; `src/modules/referents/` |
| M/R/E/P — Déclarant | DÉRIVÉ | E (Extranet, accès externe authentifié) | ProConnect OAuth (externe) + session JWT |
| M/R/E/P — Admin DGT | DÉRIVÉ | M (Intranet MASS) | Middleware `/admin/*` guard + isAdmin flag |
| M/R/E/P — Grand public | DÉRIVÉ | P (Public / Internet) | Pages sans authentification, route `/stats` |
| M/R/E/P — SUIT | DÉRIVÉ | M (Intranet MASS) | API privée `/api/v1/*` protégée par APISIX + secret partagé |
| M/R/E/P — Référents | DÉRIVÉ | M (création/modif) + P (consultation publique) | `adminReferents` router (M) + `publicReferents` router (P) |

---

## Cadre 2 — Exigences fonctionnelles

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Fonctionnalités (list) | DÉRIVÉ | 21 fonctionnalités listées | Routes Next.js `src/app/` ; routers tRPC `src/server/api/routers/` ; modules `src/modules/` |
| Connexion ProConnect | DÉRIVÉ | Authentification OAuth/OIDC | `src/server/auth/config.ts` ; `src/app/api/auth/[...nextauth]/route.ts` |
| Wizard déclaration 6 étapes | DÉRIVÉ | Parcours étape par étape | `src/app/declaration-remuneration/etape/[step]/page.tsx` ; `src/server/api/routers/declaration.ts` (updateStep1..updateStep4) |
| Saisie indicateur G | DÉRIVÉ | Catégories d'emploi | `src/server/api/routers/declaration.ts` (updateEmployeeCategories) ; `src/server/db/schema.ts` (app_job_category, app_employee_category) |
| Dépôt avis CSE | DÉRIVÉ | Upload PDF + wizard avis CSE | `src/app/avis-cse/` ; `src/server/api/routers/cseOpinion.ts` ; `src/app/api/upload/route.ts` |
| Parcours conformité | DÉRIVÉ | Choix voie corrective/justificative/évaluation conjointe | `src/app/declaration-remuneration/parcours-conformite/` ; `src/server/api/routers/declaration.ts` (saveCompliancePath) |
| Seconde déclaration | DÉRIVÉ | Déclaration correction pour écarts >= 5% | `src/server/api/routers/declaration.ts` (submitSecondDeclaration) |
| Administration DGT | DÉRIVÉ | CRUD déclarations, stats, paramètres, référents, impersonation | `src/server/api/routers/admin*.ts` ; `src/app/admin/` |
| Consultation publique | DÉRIVÉ | Stats publiques, recherche, export | `src/app/stats/` ; `src/app/api/export/` ; `publicStats` router |
| API privée SUIT | DÉRIVÉ | `/api/v1/*` + APISIX gateway | `src/app/api/v1/` ; `src/middleware.ts` ; `.kontinuous/templates/apisix-suit.*.yaml` |
| Notifications email | DÉRIVÉ | Worker pg-boss + SMTP | `packages/notifications/` ; `src/server/api/routers/mail.ts` |

---

## Cadre 3 — Contraintes & Volumétrie

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Sensibilité des données (PII) | INFÉRÉ | Données personnelles (email, nom, prénom, téléphone) + données salariales (indicateur G) | `src/server/db/schema.ts` (app_user : firstName, lastName, email, phone) ; contenu des déclarations |
| ProConnect (SSO) | DÉRIFÉ | Service d'annuaire/authentification utilisé | `src/server/auth/config.ts` |
| Messagerie SMTP | DÉRIVÉ | Service de messagerie utilisé | `packages/notifications/` ; `docker-compose.yml` (maildev) |
| Dépendance ProConnect | DÉRIVÉ | Fournisseur (critique, pas de fallback) | `src/server/auth/config.ts` |
| Dépendance INSEE WEEZ | DÉRIVÉ | Fournisseur (données entreprises) | `src/server/services/weez.ts` ; `env.js` (EGAPRO_WEEZ_API_URL) |
| Dépendance GIP-MDS | DÉRIVÉ | Fournisseur (indicateurs A-F) | `src/server/services/gipMds.ts` ; `env.js` (EGAPRO_GIP_MDS_API_URL) |
| Dépendance SUIT | DÉRIVÉ | Fournisseur (statut CSE/sanction) + Consommateur (API privée) | `src/server/services/suit.ts` ; `env.js` (EGAPRO_SUIT_API_URL) ; `src/app/api/v1/` |
| Dépendance S3 | DÉRIVÉ | Fournisseur (stockage fichiers) | `src/server/services/s3.ts` ; `env.js` (S3_BUCKET_NAME, etc.) |
| Dépendance Sentry | DÉRIVÉ | Fournisseur (observabilité) | `src/instrumentation.ts` ; `sentry.server.config.ts` |
| Utilisabilité smartphone/tablette | INFÉRÉ | Interface responsive via DSFR | DSFR responsive (breakpoints `sm`/`md`/`lg`/`xl`) ; pas de PWA détectée |
| Réduction volume — Audit purge | DÉRIVÉ | Cron de purge quotidien (4h) | `packages/app/scripts/audit-cleanup.mjs` ; config CronJob Kubernetes |
| Volumétrie D1-D4, F1-F4 | — | `[À COMPLÉTER]` | Non dérivable du code |

---

## Cadre 4 — Exigences contextuelles (sécurité et QoS)

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Authentification forte | DÉRIVÉ | ProConnect (OAuth 2.0 + OIDC, SSO État) | `src/server/auth/config.ts` |
| Chiffrement (HTTPS) | DÉRIVÉ | Tous les échanges en HTTPS | Ingress Kubernetes, TLS |
| Audit logging | DÉRIVÉ | Journalisation exhaustive CNIL avec rétention 180/365j | `src/server/audit/` ; `src/server/db/auditSchema.ts` (action_log) |
| ClamAV antivirus | DÉRIVÉ | Scan antivirus sur upload PDF | `src/server/services/clamav.ts` ; `docker-compose.yml` (clamavd) |
| Validation fichiers (magic bytes) | DÉRIVÉ | Vérification des signatures de fichier | `src/server/services/fileValidation.ts` |
| Verrou collaboratif | DÉRIVÉ | Anti-écriture concurrente sur déclaration | `src/server/services/declarationLockService.ts` ; `src/server/api/routers/declarationLock.ts` |
| APISIX + key-auth | DÉRIVÉ | Passerelle API privée avec authentification | `.kontinuous/templates/apisix-suit.*.yaml` ; `src/middleware.ts` (X-Gateway-Forwarded) |
| Constante-time compare | DÉRIVÉ | Vérification du secret partagé APISIX | `src/middleware.ts` (constant-time comparison) |
| Rate limiting APISIX | DÉRIVÉ | ~10 req/s, burst 5 | `.kontinuous/templates/apisix-suit.configmap.yaml` (à confirmer) |
| DICT EBIOS | — | `[À COMPLÉTER — RSSI]` | Non dérivable du code |
| PCA/PRA/PDMA/DMIA | — | `[À COMPLÉTER — MOA/HÉBERGEUR]` | Non dérivable du code |
| Temps de réponse | — | `[À COMPLÉTER — MOA]` | Non dérivable du code |

---

## Cadres 5-8 — Schémas

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Cadre 5 — Acteurs | DÉRIVÉ | Schéma Mermaid avec acteurs et SI externes | Analyse des intégrations, routes, auth |
| Cadre 6 — Fonctionnelle | DÉRIVÉ | Schéma Mermaid avec blocs par acteur | Modules `src/modules/`, routers tRPC |
| Cadre 7 — Applicative | DÉRIVÉ | Pile technique complète | `package.json`, `docker-compose.yml`, `packages/app/package.json`, `next.config.js` |
| Cadre 8 — Technique | DÉRIVÉ | Vue logique zones MASS + flux numérotés | `docker-compose.yml`, `docs/architecture.md`, services externes, `src/middleware.ts` |

---

## Cadre 9 — Serveurs & Composants applicatifs

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| EGAPRO.APP (Next.js) | DÉRIVÉ | Pod K8s, Node.js 24, Alpine | `Dockerfile`, `.nvmrc`, `docker-compose.yml` |
| EGAPRO.BDD (PostgreSQL) | DÉRIVÉ | PostgreSQL 14.17 | `docker-compose.yml` (image `postgres:14.17`) |
| EGAPRO.BDD-NOTIFICATIONS | DÉRIVÉ | PostgreSQL 14.17 dédié | `docker-compose.yml` (db-notifications) |
| EGAPRO.NOTIFICATIONS | DÉRIVÉ | Worker pg-boss + Nodemailer | `packages/notifications/package.json` |
| EGAPRO.APISIX-SUIT | DÉRIVÉ | Passerelle API APISIX | `.kontinuous/templates/apisix-suit.*.yaml` |
| EGAPRO.S3 | DÉRIVÉ | Stockage objet S3-compatible | `docker-compose.yml` (minio) ; `src/server/services/s3.ts` |
| EGAPRO.CLAMAV | DÉRIVÉ | ClamAV 1.5 | `docker-compose.yml` (clamavd) ; `src/server/services/clamav.ts` |
| Composants logiciels | DÉRIVÉ | Next.js 16, React 19, tRPC 11, Drizzle 0.45, etc. | `packages/app/package.json` (toutes les dépendances) |

---

## Cadre 10 — Matrice des flux

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Flux 1 — Déclarants -> RP EXT | DÉRIVÉ | HTTPS | Routes protégées, auth ProConnect |
| Flux 2 — Public -> RP EXT | DÉRIVÉ | HTTPS | Pages publiques |
| Flux 3 — Admins -> RP EXT | DÉRIVÉ | HTTPS | Middleware admin guard |
| Flux 4 — SUIT -> APISIX | DÉRIVÉ | HTTPS + key-auth | `src/middleware.ts`, `.kontinuous/templates/apisix-suit.*.yaml` |
| Flux 5 — APP -> BDD | DÉRIVÉ | TCP PostgreSQL | `src/server/db/index.ts` ; `env.js` (DATABASE_URL) |
| Flux 6 — NOTIFICATIONS -> BDD-NOTIF | DÉRIVÉ | TCP PostgreSQL | `packages/notifications/` ; `.env.example` (NOTIFICATIONS_DATABASE_URL) |
| Flux 7 — APP -> S3 | DÉRIVÉ | HTTPS S3 API | `src/server/services/s3.ts` |
| Flux 8 — APP -> CLAMAV | DÉRIVÉ | TCP ClamAV | `src/server/services/clamav.ts` ; `env.js` (CLAMAV_HOST/PORT) |
| Flux 9 — APP -> ProConnect | DÉRIVÉ | HTTPS OAuth | `src/server/auth/config.ts` |
| Flux 10 — APP -> INSEE WEEZ | DÉRIVÉ | HTTPS REST | `src/server/services/weez.ts` ; `env.js` (EGAPRO_WEEZ_API_URL) |
| Flux 11 — APP -> GIP-MDS | DÉRIVÉ | HTTPS | `src/server/services/gipMds.ts` |
| Flux 12 — APP -> SUIT | DÉRIVÉ | HTTPS REST | `src/server/services/suit.ts` |
| Flux 13 — APP -> Matomo | DÉRIVÉ | HTTPS | `src/server/services/matomo.ts` |
| Flux 14 — NOTIFICATIONS -> SMTP | DÉRIVÉ | SMTP | `packages/notifications/` ; `.env.example` (SMTP_HOST/PORT) |
| Flux 15 — APP -> Sentry | DÉRIVÉ | HTTPS | `src/instrumentation.ts` |

---

## Cadre 11 — Dimensionnement

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Justifications PDMA/DMIA | — | `[À COMPLÉTER — MOE/PROD]` | Non dérivable du code |
| Allocation ressources (CPU/serveurs) | — | `[À COMPLÉTER — PROD]` | Non dérivable du code |

---

## Cadre 12 — URLs

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Toutes les URLs applicatives | DÉRIVÉ | 15 URLs listées | `src/app/` (routes) ; `src/server/api/routers/` ; `src/server/services/` ; `next.config.js` |
| Publication Publique | DÉRIVÉ | Pages /stats, /referents, /faq | Routes Next.js associées |
| Authentification ProConnect | DÉRIVÉ | `/login`, `/api/auth/[...nextauth]` | `src/app/login/page.tsx` ; `src/app/api/auth/[...nextauth]/route.ts` |
| API tRPC | DÉRIVÉ | `/api/trpc/*` | `src/app/api/trpc/[trpc]/route.ts` |
| API SUIT | DÉRIVÉ | `/api/v1/*` | `src/app/api/v1/` |
| Export | DÉRIVÉ | `/api/export/generate` + `/api/export/download` | `src/app/api/export/` |
| Sentry tunnel | DÉRIVÉ | `/monitoring` | `next.config.js` (tunnelRoute) |
| Sentry self-hosted | DÉRIVÉ | `sentry2.fabrique.social.gouv.fr` | `next.config.js` (sentryUrl) |

---

## Annexe — Suivi des changements

| Champ | Statut | Valeur | Source |
|---|---|---|---|
| Version initiale | INFÉRÉ | V0.1.0 | Convention (génération initiale) |
| Date | — | `[À COMPLÉTER]` | Non dérivable |
| Demandeur/Rapporteur | — | `[À COMPLÉTER — MOA]` | Non dérivable |

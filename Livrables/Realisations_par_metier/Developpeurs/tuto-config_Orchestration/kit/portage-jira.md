# Porter la pipeline vers Jira (via MCP) — architecture + retour du portage réel

Comment faire tourner `/analyse` + `/implement` avec **Jira** comme tracker au lieu de GitHub Issues / Projects.

> **Ce portage a été réalisé de bout en bout** à partir de ce document, sur un projet de démo Vite/React 19 (tracker Jira Cloud, hôte git GitHub). La config qui en résulte — le **kit édition Jira** — sert de référence : dossier `ref/` fourni à côté de ce tuto. Son arbre de travail ne garde que `.claude/` ; le projet complet (dont `scripts/orchestration/` et la notice `INSTALL-JIRA.md`) vit dans son historique git — extraction en §7.
>
> Si ta cible est Jira Cloud : **ne refais pas le portage, installe la version portée** (§7). Ce document reste le manuel de transposition : l'architecture (§1–2), la pièce centrale `jira_rest.sh` (§3), la config MCP (§4), le mapping (§5), les pièges vérifiés en réel (§6) et les limites (§8).

## 1. Le principe (à lire avant tout)

Jira ne remplace **que la couche tracker** : issues, board, statuts, sprint, sizing. Le **code, les branches, les PR/MR et la CI restent sur un hôte git** (GitHub, GitLab ou Bitbucket). On ne porte donc qu'une moitié de la pipeline.

Le design isole cette couche derrière deux seams. Verdict après portage réel :

| Seam | Fichiers | Verdict |
|---|---|---|
| **Référence board** | `rules/github-board.md` → `rules/jira-board.md` | ✅ A tenu : un fichier remplacé, mêmes consommateurs (agents + skills le lisent à la demande). |
| **Helpers d'écriture** | `set_ticket_status.sh`, `set_ticket_size.sh`, `create_linked_branch.sh` | ✅ A tenu pour les **écritures** : signatures conservées à l'identique, appelants intacts. ⚠️ Mais les **lectures** board (`epic_loop.sh`, `dispatch_plan.sh` : sous-tickets, statuts, labels d'escalade) tapaient `gh` en direct, hors seam → à basculer aussi (~200 lignes touchées dans `epic_loop.sh`, mêmes flux). |

La leçon du réel : plutôt que de réécrire chaque helper en `curl` isolé, le portage a factorisé **tout** l'accès REST (lectures et écritures) dans une lib unique — `jira_rest.sh` (§3) — que les scripts sourcent. C'est la pièce qui manquait au design d'origine.

## 2. ⚠️ Contrainte n°1 : MCP ≠ bash (confirmée en réel)

Le piège central. **Un outil MCP est appelé par l'agent (le LLM), pas depuis un script bash.** Or une grosse partie de l'orchestration (`epic_loop.sh`, `process_tick_result.sh`, les helpers) tourne en **bash headless détaché** (`nohup … &`), sans LLM dans la boucle → **le MCP y est indisponible.**

Deux couches, deux canaux :

| Couche | Exécution | Canal Jira |
|---|---|---|
| **Conversationnelle** : tout `/analyse` ; `/implement` step 0–1 ; la branche task/bug synchrone ; les agents lancés en `claude --agent …` | LLM présent | **MCP Jira** ✅ |
| **Orchestration bash headless** : `epic_loop.sh` & ses helpers (`nohup`) | Pas de LLM | **API REST Jira via `curl`** (token), encapsulée dans `jira_rest.sh` |

Conséquence pratique : en mode **task/bug**, le portage est direct (l'agent pilote via MCP). En mode **epic**, le loop driver bash passe par REST. Cette contrainte s'est aussi manifestée **pendant** le portage : la session d'installation étant headless, le MCP n'y était pas authentifié, et les IDs Jira n'ont pas pu être extraits automatiquement (d'où l'étape manuelle §7.2).

## 3. La pièce maîtresse du portage : `scripts/orchestration/jira_rest.sh`

Lib bash **à sourcer** (pas exécutable), qui encapsule auth, endpoints et format ADF. Les 6 scripts board du moteur la sourcent ; aucun `curl` monté à la main ailleurs. 12 fonctions :

| Fonction | Rôle |
|---|---|
| `jira_api METHOD path [body]` | appel bas niveau `/rest/api/3`, log du statut HTTP, code retour ≥400 → échec |
| `jira_get_issue KEY [fields]` | `GET /issue/{KEY}` |
| `jira_create_issue '<fields_json>'` | `POST /issue` (type via champ `issuetype`) |
| `jira_edit_fields KEY '<json>'` | `PUT /issue/{KEY}` (story points, parent…) |
| `jira_add_comment KEY "texte"` | `POST /issue/{KEY}/comment`, conversion texte → ADF |
| `jira_get_transitions KEY` | `GET /issue/{KEY}/transitions` |
| `jira_transition KEY <id>` / `jira_transition_by_name KEY "In Progress"` | `POST /issue/{KEY}/transitions` — résolution **par nom** d'abord, ID en fallback |
| `jira_search "<jql>" [fields]` | `POST /rest/api/3/search/jql` |
| `jira_agile` | endpoints `/rest/agile/1.0` (sprints) |
| `_adf`, `_jira_require_env` | helpers internes (ADF minimal ; vérif env vars avec message clair) |

Trois choix de conception validés à l'usage :

- **Auth basic `email:token`** via 3 variables d'env : `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`. Les deux premières (+ `JIRA_PROJECT_KEY`) vivent dans `.claude/settings.json` (bloc `env`) ; le **token ne se committe jamais** → `export JIRA_API_TOKEN=…` dans le shell. Pas besoin de `cloudId` en basic auth (il ne sert qu'aux endpoints OAuth `api.atlassian.com/ex/jira/…` du MCP).
- **ADF obligatoire** : l'API v3 attend les commentaires/descriptions en **Atlassian Document Format** (JSON), pas en Markdown. `_adf` fait la conversion texte → ADF minimal ; côté MCP, `addCommentToJiraIssue` convertit lui-même. Ne jamais concaténer de l'ADF à la main dans un agent.
- **Transitions par nom, pas par ID** : une transition Jira est une *arête* du workflow — son ID dépend de l'état courant ET du board. `jira_transition_by_name` résout le nom (insensible à la casse) via `GET /transitions` puis poste l'ID trouvé ; les env vars `JIRA_TRANSITION_*` restent un override si ton workflow nomme autrement (« Start work »…).

## 4. MCP Jira : la config qui a tourné + noms d'outils

Serveur officiel **Atlassian Rovo MCP Server** (remote, OAuth 2.1). Config concrète de la version portée :

```jsonc
// .mcp.json (racine du projet)
{ "mcpServers": { "atlassian": { "type": "http", "url": "https://mcp.atlassian.com/v1/mcp/authv2" } } }
// .claude/settings.local.json
{ "enabledMcpjsonServers": ["atlassian"] }
```

Authentification : ouvrir Claude Code dans le projet → `/mcp` → `atlassian` → OAuth navigateur. Outils Jira utilisés par la pipeline :

| Catégorie | Outils |
|---|---|
| **Lecture** | `getJiraIssue`, `getTransitionsForJiraIssue`, `getJiraProjectIssueTypesMetadata`, `getVisibleJiraProjects`, `lookupJiraAccountId` |
| **Écriture** | `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue` |
| **Recherche** | `searchJiraIssuesUsingJql` |
| **Contexte** | `atlassianUserInfo`, `getAccessibleAtlassianResources` (résout le `cloudId`) |

> ⚠️ **Les noms d'outils diffèrent selon le serveur MCP.** Le serveur communautaire `sooperset/mcp-atlassian` utilise du snake_case : `jira_get_issue`, `jira_create_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_search`… **Liste les outils de TON serveur et adapte** — l'avertissement est répété dans les skills et `jira-board.md` de la version portée.

## 5. Mapping GitHub → Jira (tel qu'implémenté)

| Opération pipeline | GitHub (kit d'origine) | MCP Jira (Rovo) | Bash headless (`jira_rest.sh`) |
|---|---|---|---|
| Lire une issue | `gh issue view --json` | `getJiraIssue` | `jira_get_issue KEY [fields]` |
| Créer une issue | `gh issue create` | `createJiraIssue` | `jira_create_issue '<json>'` |
| Type → mode pipeline | `issueType` Feature/Task/Bug | `issuetype.name` : `Epic`→epic, `Story`/`Task`→task, `Bug`→bug | idem (JSON) |
| Commentaire `## Analyse …` | `gh issue comment` | `addCommentToJiraIssue` | `jira_add_comment` (ADF géré) |
| Lien epic → sous-ticket | `addSubIssue` (GraphQL) | champ `parent` à la création (team-managed) / Epic Link `customfield_*` (company-managed) | idem via `jira_create_issue` / `jira_edit_fields` |
| Transition de statut | option IDs Projects v2 | `transitionJiraIssue` | `set_ticket_status.sh KEY "In Progress"` → `jira_transition_by_name` |
| Sizing | `Size` + `Estimate` (2 champs Projects) | `editJiraIssue` | `set_ticket_size.sh KEY <XS..XL>` → story points Fibonacci (XS=1 S=2 M=3 L=5 XL=8) dans `JIRA_SP_FIELD` |
| Sous-tickets d'un epic | GraphQL ad hoc | `searchJiraIssuesUsingJql` | `jira_search "parent = KEY"` (team-managed) |
| Branche linkée + lien PR | `createLinkedBranch` + `force_pr_issue_link.sh` | — | `create_linked_branch.sh KEY <base>` : **pur git**, branche `ticket/<KEY>-<slug>` ; le lien vient de l'intégration Jira↔DVCS (clé d'issue dans branche + titre de PR), pas d'un appel API |

**Argument d'entrée** : la clé d'issue (`/analyse KAN-1`), pas un numéro — chaque projet Jira a son propre compteur. Parseur (repris verbatim dans les skills portés) :

```bash
case "$ARG_HEAD" in
  [A-Z][A-Z0-9]*-[0-9]*)  ISSUE_KEY="$ARG_HEAD" ;;                      # clé directe : KAN-1
  *://*/browse/*)         ISSUE_KEY="$(echo "$ARG_HEAD" | sed -E 's#.*/browse/([A-Z][A-Z0-9]*-[0-9]+).*#\1#')" ;;
  *)                      ISSUE_KEY="" ;;
esac
```

**Invariants conservés à l'identique** (vérifiés dans la version portée) : les marqueurs de commentaires (`## Analyse PO`, `## Analyse architecte`, `## Analyse du bug`, `## Besoin métier`) ; le body des tickets intact (l'analyse vit en commentaire) ; la règle humain-only (`In review`/`Done` refusés par `set_ticket_status.sh`, exit 3) ; le contrat JSON `{"status": …}` des agents headless ; la couche git/PR sur `gh` (GitLab → `glab mr`).

## 6. Les pièges vérifiés en conditions réelles

Découverts (ou confirmés) pendant le portage — c'est la section à relire quand quelque chose casse :

1. **Labels Jira : ni `=` ni espace.** Le kit GitHub utilisait `dispatch=escalate` et `attempt=1/2/3`. L'API REST les **rejette** et la JQL `labels = "dispatch=escalate"` ne matche rien → l'anti-boucle (3 refacto → escalade) et le hold manuel étaient cassés **silencieusement**. Renommés `dispatch_escalate` / `attempt_N` partout (écritures, greps, JQL, prompt d'`architect-rework`).
2. **ADF partout en REST** : un commentaire posté en texte brut sur l'API v3 échoue. Passer par `jira_add_comment` (ou le MCP, qui convertit).
3. **Les transitions sont des arêtes, pas des statuts** : un ID de transition n'est valable que depuis l'état courant. Résoudre par **nom** (`jira_transition_by_name`) ; si `400 transition id is not valid` → re-extraire (recette dans `jira-board.md`).
4. **Team-managed vs company-managed — à trancher AVANT** : lien epic↔enfant via champ `parent` + JQL `parent = KEY` (team-managed, défaut retenu) ou via Epic Link `customfield_*` + JQL `"Epic Link" = KEY` (company-managed). Vérifie dans Project settings → Details.
5. **Les lectures board n'étaient pas derrière le seam** : prévoir de porter aussi les `gh`/GraphQL de lecture d'`epic_loop.sh` / `dispatch_plan.sh` (cf. §1) — c'est le gros du diff, mécanique mais réel.
6. **Token REST jamais versionné** : `settings.json` porte URL/email/clé projet ; le token reste dans le shell (`export JIRA_API_TOKEN=…`).
7. **Garde structurelle humain-only** : les IDs des transitions `In review` / `Done` ne sont volontairement exposés dans **aucune** variable d'env ni recette — aucun script ne peut les déclencher par accident.

## 7. Installer la version portée (au lieu de re-porter)

La checklist complète est dans `INSTALL-JIRA.md` (à la racine du dépôt de référence). Résumé :

**0. Récupérer la config portée** — l'arbre de travail de `ref/` ne contient que `.claude/` ; les scripts vivent dans le HEAD git :

```bash
cd ref
git archive HEAD -- .claude scripts .mcp.json INSTALL-JIRA.md | tar -x -C /chemin/vers/ton-projet
```

1. **Authentifier le MCP Atlassian** (requis pour `/analyse` et `/implement` task/bug) : `/mcp` → `atlassian` → OAuth (§4).
2. **Remplir `rules/jira-board.md`** ⚠️ bloquant — les IDs sont propres à ton instance et **non devinables** : transitions (`getTransitionsForJiraIssue` / `GET /issue/{KEY}/transitions`), customfields story points / sprint / Epic Link (`GET /rest/api/3/field`), issue types (`getJiraProjectIssueTypesMetadata`). Recettes MCP **et** REST prêtes à l'emploi dans le fichier. Trancher team-managed vs company-managed (§6.4).
3. **Hôte git** : `gh auth login`, puis remplacer le placeholder partout :
   ```bash
   grep -rl "<ORG>/<REPO>" .claude scripts | xargs sed -i 's#<ORG>/<REPO>#mon-org/mon-repo#g'
   ```
   Branche d'intégration : `EPIC_DEFAULT_BASE` dans `settings.json` (défaut `origin/main`). Connecter le repo à Jira (intégration DVCS / « GitHub for Jira ») pour que le panneau Development suive les branches `ticket/<KEY>-…`.
4. **Token REST** (requis seulement pour le **mode epic**) : `export JIRA_API_TOKEN=…` + compléter `JIRA_BASE_URL` / `JIRA_EMAIL` / `JIRA_PROJECT_KEY` dans `settings.json`.
5. **Adapter la stack** : la version portée est câblée Vite/React 19/TypeScript/oxlint (hooks `auto-lint.sh` → `npm run lint`, `block-bad-patterns.sh` minimal, `setup-worktree.sh` → `npm ci` + ports `5173+index`, rules `code-quality`/`testing`/`e2e`). Autre stack → adapter ces fichiers (mêmes points que `toAdapt.md` §3–4 du kit GitHub). Ajouter un runner de tests si tu veux une vraie couverture (`tu-dev`/`e2e-dev` notent son absence sinon).

**Périmètre élagué** de l'édition Jira (vs kit GitHub) : `/velocity` et `/plan-sprint` non portés (`plan_sprint.sh`/`sprint_velocity.sh` retirés), rules egapro pures supprimées (`figma-workflow`, `visual-quality-validation`, `audit-logging`).

## 8. Limites connues + test bout-en-bout

- **Mode epic : porté structurellement, pas encore éprouvé.** `epic_loop.sh` + helpers sont portés vers REST (syntaxe validée, mêmes flux, revue adversariale passée) mais n'ont **pas tourné de bout en bout** contre une instance Jira réelle (session d'install sans MCP authentifié ni hôte git). À éprouver après §7.1–4.
- **Chemin le plus sûr aujourd'hui** : `/analyse <KEY>` puis `/implement <KEY>` en mode **task/bug** (synchrone, piloté MCP) — ne dépend que de §7.1 + §7.3.
- **Test bout-en-bout** (ticket jouet) : créer une `Task` Jira (ex. `KAN-1`) → `/analyse KAN-1` : commentaire `## Analyse architecte` + story points écrits, **aucune** transition → `/implement KAN-1` : branche `ticket/KAN-1-…`, statut `In progress`, PR draft ouverte.

## Sources

- Le portage réalisé : dossier `ref/` (config `.claude/`, et dans son historique git : `scripts/orchestration/`, `INSTALL-JIRA.md`)
- [Supported tools — Atlassian Rovo MCP Server (officiel)](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/)
- [atlassian/atlassian-mcp-server (GitHub)](https://github.com/atlassian/atlassian-mcp-server)
- [sooperset/mcp-atlassian — serveur communautaire (noms snake_case)](https://github.com/sooperset/mcp-atlassian)

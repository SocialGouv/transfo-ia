# Porter la pipeline vers Jira (via MCP)

Comment faire tourner `/analyse` + `/implement` avec **Jira** comme tracker au lieu de GitHub Issues / Projects.

## 1. Le principe (à lire avant tout)

Jira ne remplace **que la couche tracker** : issues, board, statuts, sprint, sizing. Le **code, les branches, les PR/MR et la CI restent sur un hôte git** (GitHub, GitLab ou Bitbucket). On ne porte donc qu'une moitié de la pipeline.

Bonne nouvelle : le design isole déjà cette couche derrière **deux seams** clairs. Porter = réimplémenter ces deux-là, sans toucher au reste :

| Seam | Fichiers | Ce qu'il encapsule |
|---|---|---|
| **Référence board** | `rules/github-board.md` | IDs projet, field IDs, option IDs, type IDs, snippets de mutation. |
| **Helpers d'écriture** | `scripts/orchestration/{set_ticket_status,set_ticket_size,create_linked_branch,force_pr_issue_link,cache_gh}.sh` | Toutes les écritures board derrière une interface stable. |

`epic_loop.sh`, `dispatch_plan.sh`, les skills et les agents appellent ces helpers / ce fichier de réf — pas l'API directement. Si tu gardes **la même interface** (mêmes arguments), tu n'as quasi rien à changer en amont.

## 2. ⚠️ Contrainte n°1 : MCP ≠ bash

C'est le piège central. **Un outil MCP est appelé par l'agent (le LLM), pas depuis un script bash.** Or une grosse partie de l'orchestration (`epic_loop.sh`, `process_tick_result.sh`, les helpers) tourne en **bash headless détaché** (`nohup … &`), sans LLM dans la boucle → **le MCP y est indisponible.**

Il y a donc deux couches à traiter différemment :

| Couche | Exécution | Canal Jira |
|---|---|---|
| **Conversationnelle** : tout `/analyse` ; `/implement` step 0–1 ; la branche task/bug synchrone ; les agents lancés en `claude --agent …` (qui *peuvent* charger un MCP) | LLM présent | **MCP Jira** ✅ |
| **Orchestration bash headless** : `epic_loop.sh` & ses helpers (`nohup`) | Pas de LLM | **API REST Jira via `curl`** (token) — le MCP est inaccessible |

Conséquence pratique : en mode **task/bug**, le portage MCP est direct (l'agent pilote). En mode **epic**, le loop driver bash doit taper l'API REST Jira ; réimplémente les helpers en `curl` (l'interface reste la même, donc `epic_loop.sh` est inchangé). Alternative plus lourde : réécrire le loop en orchestration LLM-driven pour rester full-MCP.

## 3. MCP Jira de référence + noms d'outils

Serveur officiel : **Atlassian Rovo MCP Server** (remote, OAuth 2.1) — repo `atlassian/atlassian-mcp-server`. Outils Jira exposés (noms réels) :

| Catégorie | Outils |
|---|---|
| **Lecture** | `getJiraIssue`, `getTransitionsForJiraIssue`, `getJiraProjectIssueTypesMetadata`, `getJiraIssueTypeMetaWithFields`, `getVisibleJiraProjects`, `getIssueLinkTypes`, `lookupJiraAccountId` |
| **Écriture** | `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue`, `addWorklogToJiraIssue` |
| **Recherche** | `searchJiraIssuesUsingJql` |
| **Contexte** | `atlassianUserInfo`, `getAccessibleAtlassianResources` (résout le `cloudId`) |

> ⚠️ **Les noms d'outils diffèrent selon le serveur MCP.** Le serveur communautaire `sooperset/mcp-atlassian` utilise du snake_case : `jira_get_issue`, `jira_create_issue`, `jira_update_issue`, `jira_transition_issue`, `jira_add_comment`, `jira_search`… **Liste les outils de TON serveur installé et adapte** — ne copie pas les noms à l'aveugle.

## 4. Mapping GitHub → Jira

| Opération pipeline | GitHub (actuel) | MCP Jira (Rovo) | REST (bash / `curl`) |
|---|---|---|---|
| Lire une issue | `gh issue view --json` | `getJiraIssue` | `GET /rest/api/3/issue/{key}` |
| Créer une issue | `gh issue create` | `createJiraIssue` | `POST /rest/api/3/issue` |
| Type Feature/Task/Bug | `updateIssueIssueType` (type IDs) | champ `issuetype` à la création | `issuetype` (Epic / Story \| Task / Bug) |
| Ajouter un commentaire (`## Analyse …`) | `gh issue comment` | `addCommentToJiraIssue` | `POST /rest/api/3/issue/{key}/comment` |
| Lire les commentaires | `--json comments` | inclus dans `getJiraIssue` | `GET /rest/api/3/issue/{key}?fields=comment` |
| Lien epic → sous-ticket | `addSubIssue` (GraphQL) | champ `parent` à la création / `editJiraIssue` | `parent` (team-managed) **ou** Epic Link `customfield_*` (company-managed) |
| Transition de statut | `updateProjectV2ItemFieldValue` (option IDs) | `getTransitionsForJiraIssue` + `transitionJiraIssue` | `GET`/`POST /rest/api/3/issue/{key}/transitions` |
| Size / Estimate | `set_ticket_size.sh` (champs Projects) | `editJiraIssue` (story points) | `customfield_*` (story points) |
| Sprint | champ iteration Projects | `editJiraIssue` (champ sprint) | Agile API `/rest/agile/1.0/sprint/{id}/issue` |
| Rechercher des tickets | (GraphQL ad hoc) | `searchJiraIssuesUsingJql` | `POST /rest/api/3/search/jql` |
| Branche linkée + lien PR | `createLinkedBranch` + `force_pr_issue_link.sh` | — (pas une écriture Jira) | **Smart Commits** : mettre la clé `PROJ-123` dans le nom de branche + titre de PR ; l'intégration Jira-DVCS surface le lien |

> Comme pour GitHub, **les IDs Jira sont propres à ton instance et non devinables** : transition IDs (par statut, via `getTransitionsForJiraIssue`), `customfield_*` (story points, sprint, Epic Link — via `GET /rest/api/3/field`), issue type IDs (via `getJiraProjectIssueTypesMetadata`). Extrais-les une fois, colle-les dans `jira-board.md`.

## 5. Argument d'entrée & détection de mode

### 5.1 Argument : la clé d'issue (pas un numéro)

Sur GitHub on passe le numéro (`/analyse 42`). Sur Jira on passe la **clé d'issue** `<CLÉ_PROJET>-<num>` → `/analyse KAN-1`, en **majuscules** (forme canonique ; le MCP/REST renvoie et attend l'uppercase). Raison : chaque projet Jira a son **propre compteur**, donc `1` seul est ambigu — la clé projet le désambiguïse. `getJiraIssue` prend la clé directement.

Le parseur **Step 0** de `/analyse` (qui ne reconnaît que `#N` / `N` / URL GitHub) doit accepter la clé :

```bash
ARG_HEAD="$(echo "$ARGUMENTS" | awk '{print $1}')"
case "$ARG_HEAD" in
  [A-Z][A-Z0-9]*-[0-9]*)        # clé directe : KAN-1
    ISSUE_KEY="$ARG_HEAD" ;;
  *://*/browse/*)               # URL Jira : https://<org>.atlassian.net/browse/KAN-1
    ISSUE_KEY="$(echo "$ARG_HEAD" | sed -E 's#.*/browse/([A-Z][A-Z0-9]*-[0-9]+).*#\1#')" ;;
  *) ISSUE_KEY="" ;;
esac
```

La **clé projet** (`KAN`) est une constante par-projet — l'équivalent du `PROJECT_ID` GitHub : elle va dans `rules/jira-board.md` et sert aussi à nommer les branches `KAN-1-...` pour le lien Smart Commits (§4).

### 5.2 Mode : depuis `issuetype.name`

Après `getJiraIssue(ISSUE_KEY)`, lire `.fields.issuetype.name`. Jira n'a pas de type « Feature » par défaut :

| `issuetype` Jira | Mode pipeline |
|---|---|
| `Epic` | **epic** |
| `Story` ou `Task` | **task** |
| `Bug` | **bug** |

Et la hiérarchie epic → enfants passe par le champ `parent` (projets team-managed) ou l'**Epic Link** (projets company-managed) — à trancher selon ton type de projet Jira.

## 6. Ce qu'il faut concrètement changer

1. **`rules/github-board.md` → `rules/jira-board.md`** : project key, issue type IDs, **transition IDs par statut** (`To Do → In progress`…), `customfield_*` (story points, sprint, Epic Link), recettes **JQL** (ex. sous-tickets d'un epic : `"Epic Link" = PROJ-42` ou `parent = PROJ-42`). Documenter comment ré-extraire ces IDs (mêmes requêtes que §4).
2. **Réécrire les helpers bash en REST `curl`** (token Jira en variable d'env), **en gardant la signature** :
   - `set_ticket_status.sh <key> <statut>` → `getTransitions` puis `POST …/transitions`. Conserver le **refus de `In review`/`Done`** (règle humain-only).
   - `set_ticket_size.sh <key> <XS..XL>` → `PUT …/issue/{key}` sur le `customfield` story points.
   - `create_linked_branch.sh <key> <base>` → crée juste la branche git nommée `…/PROJ-123-slug` (le lien Jira vient de l'intégration DVCS, pas d'un appel API).
3. **Skills + agents conversationnels** : remplacer les `gh issue …` par les appels **MCP Jira** (lecture, création, commentaires, transitions). La détection de mode lit `issuetype` (§5). Les marqueurs d'analyse (`## Analyse architecte`, `## Analyse du bug`, `## Analyse PO`) sont **identiques** — ce sont des commentaires Jira.
4. **Couche git/PR inchangée** : si le code reste sur GitHub → garder `gh pr`. Sur GitLab → `glab mr`. Le rattachement à Jira se fait via la clé d'issue dans la branche/PR + l'intégration Jira ↔ DVCS (panneau Development).
5. **MCP dans les sous-process** : les agents lancés en `claude --agent code-dev/e2e-dev …` peuvent utiliser le MCP Jira si tu le déclares dans la config MCP du projet (`.mcp.json` / settings). Le loop driver bash, lui, reste sur REST (§2).

## 7. Checklist de portage

- [ ] MCP Jira connecté, **outils listés et noms vérifiés** sur ton serveur.
- [ ] `rules/jira-board.md` rempli : project key, type IDs, transition IDs, `customfield_*`, recettes JQL.
- [ ] Helpers bash réécrits en REST `curl` (token Jira), **mêmes signatures** → `epic_loop.sh` intact.
- [ ] Refus `In review`/`Done` conservé dans `set_ticket_status.sh`.
- [ ] Skills/agents conversationnels : `gh issue …` → MCP Jira ; détection de mode sur `issuetype`.
- [ ] Hôte git + intégration Jira-DVCS : clé d'issue dans branches/PR.
- [ ] Test bout-en-bout : `/analyse PROJ-123` → commentaire posté + sizing ; `/implement PROJ-123` → transition `In progress` + PR liée.

## Sources

- [Supported tools — Atlassian Rovo MCP Server (officiel)](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/)
- [atlassian/atlassian-mcp-server (GitHub)](https://github.com/atlassian/atlassian-mcp-server)
- [sooperset/mcp-atlassian — serveur communautaire (noms snake_case)](https://github.com/sooperset/mcp-atlassian)

# Reproduire `/analyse`

Phase **conception**. Read-only sur le board. Détecte le mode et délègue à un agent de conception qui produit une spec exécutable.

## 1. Mécanisme

| Mode | Trigger | Agents (Opus) | Sortie |
|---|---|---|---|
| **epic** | issue type `Feature`, ou prompt « nouvelle feature / parcours / ajouter une page » | `product-owner` → `architect` | Epic GitHub + N sous-issues `Task` |
| **task** | issue type `Task`, ou prompt « refactor / migrer / ajouter un champ » | `architect` mode task | Commentaire `## Analyse architecte` sur la task |
| **bug** | issue type `Bug`, ou prompt « bug / cassé / régression / écart figma » | `bug-analyst` | Commentaire `## Analyse du bug` sur le bug |

**Invariants non négociables :**
- Chaque agent gère **son propre gate de validation utilisateur** avant d'écrire sur GitHub. L'orchestrateur (le skill) chaîne les agents sans ré-interroger entre étapes.
- **Aucun agent de conception ne bouge le board.** Les transitions de statut sont la responsabilité de `/implement`.
- **Le body de la task/bug reste intact** : l'analyse vit dans un commentaire séparé (spec canonique pour `code-dev`).
- Chaque ticket **feuille** est sizé XS→XL en fin d'analyse (alimente la vélocité).

## 2. Fichiers à créer

```
.claude/skills/analyse/SKILL.md
.claude/agents/product-owner/AGENT.md
.claude/agents/architect/AGENT.md
.claude/agents/bug-analyst/AGENT.md
.claude/rules/github-board.md          # IDs board + snippets GraphQL (NON devinables)
.claude/rules/ticket-spec-format.md    # format normatif des specs
.claude/rules/complexity-estimation.md # rubrique de sizing XS→XL
scripts/orchestration/set_ticket_size.sh
```

### 2.1 `skills/analyse/SKILL.md`

Frontmatter minimal + logique de détection. Le corps est de la **prose dirigiste** (pas de code exécuté : le skill est un prompt pour l'orchestrateur).

```markdown
---
name: analyse
description: "Conception pipeline. Détecte le mode (epic/task/bug) selon le type d'issue ou le prompt et invoque les agents appropriés. Usage: /analyse [<issue#>] [<description>]"
---

# /analyse

## Step 0 — Détection du mode
- Parser `$ARGUMENTS` → numéro d'issue (`#42`, `42`, ou URL `/issues/42`) sinon description libre.
- Si issue : `gh issue view "$N" --json number,title,body,issueType,labels,state,comments`
  - `issueType.name == Feature` → mode **epic** (sous-mode `epic-create` si pas encore d'`## Analyse PO`, sinon `epic-enrich`)
  - `== Task` → mode **task** ; `== Bug` → mode **bug** ; absent → demander à l'utilisateur.
- Si description libre : inférer le mode par mots-clés ; en task/bug, demander à l'utilisateur de **créer l'issue d'abord**.

## Workflow par mode
- **epic** : déléguer à `product-owner` (create/enrich) → attendre `[Validation utilisateur] Epic validé`, puis à `architect` (epic-create/epic-enrich) → attendre `[Validation utilisateur] Architecture validée`.
- **task** : déléguer à `architect` mode `task` → attendre `[Validation utilisateur] Analyse validée — prêt pour /implement`.
- **bug** : déléguer à `bug-analyst` → même gate.

## Step final — Report
Afficher : mode, issue #, sous-tickets créés (epic), tags appliqués, et `Next: /implement <N>`.
```

> Le snippet Step 0 ci-dessus est la version condensée ; la version complète (parsing bash, branchement `epic-create` vs `epic-enrich`) est dans le `SKILL.md` d'origine.

### 2.2 Les 3 agents de conception

Fichier `.claude/agents/<nom>/AGENT.md`. Frontmatter recommandé puis le prompt système (rôle, inputs, workflow, gate, format de sortie) :

```markdown
---
name: architect
description: "Lit le code + Figma, découpe en specs exécutables. Modes epic-create / epic-enrich / task."
model: opus
---

# Architect Agent
You are the technical architect... (rôle, périmètre read-only)

## Inputs : issue number, mode, scénarios PO (epic), URL Figma (UI)
## Workflow : lire code/Figma → proposer découpage → GATE validation user → créer/amender les sous-issues
## Règles à charger à la demande : rules/github-board.md (IDs), rules/ticket-spec-format.md
```

| Agent | Model | Rôle | Écrit sur GitHub |
|---|---|---|---|
| `product-owner` | opus | Raffine le besoin en epic. Body = demande verbatim ; commentaire `## Besoin métier` (compréhension) ; commentaire `## Analyse PO` (découpage + scénarios `S1`, `S2`…). Applique type **Feature** + statut **Backlog**. | epic + 2 commentaires |
| `architect` | opus | Découpe l'epic en sous-issues `Task` (body = spec format `ticket-spec-format`), lie au parent, → `To Do`. En mode task : poste `## Analyse architecte`, body intact. | sous-issues / commentaire |
| `bug-analyst` | opus | Reproduit le bug (local / env k8s / visual Figma), root cause, fichiers à modifier, fix proposé. Poste `## Analyse du bug`, body intact. | commentaire |

Points communs aux 3 : **Opus**, **read-only sur le code**, **gate de validation utilisateur explicite** avant d'écrire, **posent des questions si le ticket est flou** (zéro invention).

### 2.3 Les 3 règles

| Règle | Rôle | Clé de reproduction |
|---|---|---|
| `github-board.md` | IDs du board (PROJECT_ID, field IDs, option IDs, type IDs) + snippets GraphQL prêts à l'emploi. | Les IDs sont **non devinables** : les extraire via la requête de diagnostic GraphQL (voir §3). Frontmatter `paths: scripts/orchestration/**` → lu à la demande par PO/architect. |
| `ticket-spec-format.md` | Structure obligatoire d'une spec : `## Contexte`, `## Fichiers impactés`, `## Changement attendu`, `## Scénarios de test`, `## Référence Figma`, `## Critères d'acceptation`, `## Depends on`, `## Requires services`. | C'est le contrat entre architect et `code-dev`. Si la spec manque, `code-dev` renvoie le ticket en `To Do`. |
| `complexity-estimation.md` | Rubrique de sizing t-shirt XS→XL. | Mappe sur les points Fibonacci (XS=1…XL=8) écrits par `set_ticket_size.sh`. |

### 2.4 `set_ticket_size.sh`

Wrapper qui écrit **les deux champs d'un coup** (`Size` single-select + `Estimate` number) sur le board — jamais en GraphQL brut dans un agent.

```bash
set_ticket_size.sh <ticket#> <XS|S|M|L|XL>   # XS=1 S=2 M=3 L=5 XL=8
```

## 3. Extraire les IDs du board (étape obligatoire, une fois)

Les IDs GraphQL sont propres à ton board. Les récupérer et les coller en haut de `github-board.md` :

```bash
gh api graphql -f query='
{ node(id: "<PROJECT_ID>") { ... on ProjectV2 {
  title
  fields(first: 20) { nodes { ... on ProjectV2SingleSelectField {
    id name options { id name } } } } } }'
```

`PROJECT_ID` s'obtient via `gh project list --owner <org>` puis `gh project view <n> --format json`. Mêmes constantes à extraire : `STATUS_FIELD_ID`, `SIZE_FIELD_ID`, `ESTIMATE_FIELD_ID`, `SPRINT_FIELD_ID`, les option IDs de statut/size, et les issue type IDs (Feature/Task/Bug).

## 4. Vérifier

```
/analyse <bug#>
```
Attendu : Q&A si flou → proposition d'analyse → validation → commentaire `## Analyse du bug` posté **sur l'issue** (body intact) + `Size` écrite sur le board + report `## Analyse: DONE (mode=bug)` + `Next: /implement <N>`. Le statut du ticket n'a **pas** bougé.

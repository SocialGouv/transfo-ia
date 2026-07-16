# Tuto config — pipeline `/analyse` + `/implement`

Reproduire et porter la pipeline IA de dev (conception → exécution) bâtie sur Claude Code.

| Fichier | Contenu |
|---|---|
| [01-analyse.md](01-analyse.md) | Reproduire `/analyse` (phase conception : PO + architect + bug-analyst). |
| [02-implement.md](02-implement.md) | Reproduire `/implement` (phase exécution : epic loop background, code-dev/e2e-dev). |
| [03-portage-jira.md](03-portage-jira.md) | Porter la pipeline vers Jira via MCP (au lieu de GitHub). |

## Modèle mental

Deux skills, deux phases, séparation stricte :

```
/analyse <issue>     ── conception, READ-ONLY sur le board ──>  spec / tickets
/implement <issue>   ── exécution, écrit le code + bouge le board ──>  PR
```

- `/analyse` détecte le mode (**epic / task / bug**) et délègue à des agents de conception. Il ne bouge **jamais** le statut d'un ticket.
- `/implement` détecte le même mode et lance le bon moteur d'exécution. C'est le seul à faire avancer le board (`To Do → In progress`).
- Le statut `In review` / `Done` reste **toujours** une décision humaine.

## Prérequis communs (les deux skills)

1. **Claude Code** installé, binaire `claude` dans le `PATH` (le mode epic et task/bug lancent `claude` en headless).
2. **`gh` CLI** authentifié sur le repo (`gh auth login`). C'est le canal GitHub de toute la pipeline.
3. **Repo GitHub** configuré :
   - Issue types natifs **Feature / Task / Bug** activés (réglage org).
   - Un **GitHub Project v2** avec les champs : `Status` (single-select), `Size` (single-select XS→XL), `Estimate` (number), `Sprint` (iteration).
4. **Arborescence `.claude/`** à la racine du repo :
   ```
   .claude/
     skills/<nom>/SKILL.md      # slash commands
     agents/<nom>/AGENT.md      # sous-agents (prompt système + frontmatter)
     rules/<nom>.md             # règles (always-loaded ou scopées par `paths:`)
     hooks/*.sh                 # garde-fous automatiques
     settings.json              # env + hooks
   scripts/orchestration/*.sh   # moteur d'orchestration (hors .claude/)
   ```
5. **MCP optionnels** : `figma-dev` (specs UI pixel-perfect), `playwright` + `next-devtools` (repro de bug, validation).

> Convention de chargement des règles : frontmatter `description:` → règle **always-loaded** ; frontmatter `paths:` → **auto-chargée** seulement quand un fichier matché est édité. Les règles non always-loaded (ex. `github-board.md`) sont **lues à la demande** par les agents qui en ont besoin.

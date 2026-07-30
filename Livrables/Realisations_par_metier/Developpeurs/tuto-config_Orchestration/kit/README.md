# Kit `/analyse` + `/implement` — copier-coller

Closure complète des deux skills (tous les fichiers appelés, transitivement) extraite d'egapro, prête à déposer dans un autre projet.

## Installation

Procédure pas-à-pas (extraction → adaptation → vérification) : **[`Install.md`](Install.md)**.
Référence des valeurs à substituer (IDs board, repo, branche, stack, hooks) : **[`toAdapt.md`](toAdapt.md)**.
Cible **Jira** au lieu de GitHub : **[`portage-jira.md`](portage-jira.md)** — le portage a été **réalisé** (kit édition Jira avec `jira_rest.sh`, distribué à part) ; le doc couvre l'architecture, les pièges vérifiés en réel et l'installation de la version portée.

> ⚠️ Tel quel, le kit pointe vers egapro (IDs de board, repo, branche `alpha`, stack pnpm/Biome…). **Il ne tournera pas sans adapter.**

## Contenu (closure réelle)

```
.claude/
  skills/    analyse · implement · report · open
  agents/    product-owner · architect · bug-analyst          (conception, /analyse)
             code-dev · tu-dev · e2e-dev · architect-rework    (exécution, /implement)
             doc-writer · validator · structural-auditor
             rgaa-auditor · security-auditor · functional-validator   (gates code-dev)
  rules/     github-board · ticket-spec-format · complexity-estimation
             git-artefact-hygiene · automation · bug-fix-workflow      (process)
             code-quality · testing · e2e · figma-workflow
             visual-quality-validation · audit-logging                 (stack egapro, cf. toAdapt §6)
  hooks/     auto-lint.sh · block-bad-patterns.sh · check-pr-reviews.sh
  settings.json
scripts/
  orchestration/   le moteur (epic_loop + dispatch/process/merge/rebase, run_e2e_dev,
                   run_architect_rework, run_doc_writer, set_ticket_*, helpers…)
  setup-worktree.sh · teardown-worktree.sh
```

## Périmètre

- **Inclus** : tout ce qui est appelé par `/analyse` et `/implement` (vérifié par analyse du graphe de dépendances).
- **Exclus** volontairement : `designer` / `design-validator` (code-dev fait la validation visuelle lui-même — cf. `code-dev/AGENT.md`), `review-fixer` (skill `/review`), les rules purement stack `react-components` / `styling-dsfr` / `database-drizzle` / `trpc-api` (chargées à l'édition de code — recréer pour ta stack, cf. `toAdapt.md` §6).
- **Frontmatter ajouté** à 10 agents (registration dans un projet vierge) — cf. `toAdapt.md` §5.

## Contexte

Tutos pas-à-pas et schémas dans le dossier parent : `../README.md`, `../01-analyse.md`, `../02-implement.md`, `../03-portage-jira.md`, `../workflows.pptx`. Le script qui a généré ce kit : `../build_kit.py`.

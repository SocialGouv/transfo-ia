# toAdapt.md — à adapter avant de lancer le kit dans un autre projet

Le kit reproduit **`/analyse` + `/implement`** (closure complète : skills, agents, rules, hooks, scripts). Avant qu'il tourne dans TON projet, adapte les points ci-dessous, **par ordre de criticité**. Les sections ⚠️ sont bloquantes.

> Installation : copier `.claude/` et `scripts/` du kit à la racine de ton projet (cf. `README.md`). Puis dérouler ce fichier.

---

## 0. Prérequis à activer

- **`gh` CLI** authentifié sur le repo cible (`gh auth login`).
- **Issue types** GitHub natifs `Feature` / `Task` / `Bug` activés (réglage org) — ou mappe vers tes types.
- **GitHub Project v2** avec les champs : `Status` (single-select), `Size` (single-select XS→XL), `Estimate` (number), `Sprint` (iteration).
- **`claude` CLI** dans le `PATH` (les modes epic et task/bug lancent `claude --agent …` en headless).
- **Skill `/loop`** : plugin Claude Code, **non fourni**, requis par `/implement` mode epic (auto-report). S'il est absent → voir §8.
- **git worktrees** + **docker compose** pour la stack de test (dev server par ticket).

---

## 1. ⚠️ IDs du board GitHub (BLOQUANT — non devinables)

Ces IDs sont propres à TON board. Ils sont **dupliqués à 5 endroits** — tout remplacer :

`rules/github-board.md` · `agents/architect/AGENT.md` · `scripts/orchestration/set_ticket_status.sh` · `scripts/orchestration/set_ticket_size.sh` · `scripts/orchestration/plan_sprint.sh`

| Constante | Valeur egapro (à remplacer) |
|---|---|
| `PROJECT_ID` | `PVT_kwDOAh0HH84BFsK7` |
| `STATUS_FIELD_ID` | `PVTSSF_lADOAh0HH84BFsK7zg29EI8` |
| `SIZE_FIELD_ID` | `PVTSSF_lADOAh0HH84BFsK7zg29ENU` |
| `ESTIMATE_FIELD_ID` | `PVTF_lADOAh0HH84BFsK7zg29ENY` |
| `SPRINT_FIELD_ID` | `PVTIF_lADOAh0HH84BFsK7zg8pCDM` |
| Status : Backlog / To Do / In progress / In review / Done | `f75ad846` / `61e4505c` / `47fc9ee4` / `df73e18b` / `98236657` |
| Size : XS / S / M / L / XL | `6c6483d2` / `f784b110` / `7515a9f1` / `817d0097` / `db339eb2` |
| Issue types : Feature / Task / Bug | `IT_kwDOAh0HH84Aa_K4` / `IT_kwDOAh0HH84Aa_Kz` / `IT_kwDOAh0HH84Aa_K1` |

**Extraire tes IDs** (PROJECT_ID via `gh project list --owner <org>` puis `gh project view <n> --format json`) :

```bash
# Champs + options (Status / Size / Estimate / Sprint)
gh api graphql -f query='{ node(id:"<TON_PROJECT_ID>"){ ... on ProjectV2 {
  fields(first:30){ nodes{
    ... on ProjectV2SingleSelectField { id name options{ id name } }
    ... on ProjectV2FieldCommon { id name } } } } } }'

# Issue type IDs
gh api graphql -f query='{ repository(owner:"<org>",name:"<repo>"){ issueTypes(first:10){ nodes{ id name } } } }'
```

---

## 2. Repo & branches

| Élément | Valeur egapro | Où | Action |
|---|---|---|---|
| owner/repo | `SocialGouv/egapro` | ~35 fichiers (agents, rules, skills, scripts) | remplacer partout par `<org>/<repo>` |
| Branche de base | `alpha` | ~90 occurrences | remplacer par ta branche d'intégration (`main` / `develop`) — **review manuelle** (mot courant) |
| Base pipeline | `chore/ai-pipeline` (`EPIC_DEFAULT_BASE`) | `.claude/settings.json` | mettre ta branche, ou retirer la var |
| Branche d'epic | motif `epic/<N>` | scripts orchestration | garder, ou renommer la convention |
| URL review app | `*.ovh.fabrique.social.gouv.fr` | `skills/implement/SKILL.md`, `agents/bug-analyst` | mettre l'URL de tes env de review, ou retirer si aucun |

Remplacement assisté (revoir le diff avant commit) :

```bash
cd <ton-projet>
grep -rl "SocialGouv/egapro" .claude scripts | xargs sed -i 's#SocialGouv/egapro#<org>/<repo>#g'
# 'alpha' : NE PAS sed à l'aveugle. Repérer puis remplacer au cas par cas :
grep -rn "\balpha\b" .claude scripts
```

---

## 3. Stack build / test / dev (hooks, agents, setup-worktree)

Tout est câblé sur la stack egapro (pnpm + Next.js + Biome + Drizzle + Playwright). À mapper sur la tienne :

| Brique egapro | Où | Remplacer par |
|---|---|---|
| `pnpm` + sous-commandes (`test`, `typecheck`, `lint:check`, `format:check`, `build`, `check:write`, `db:generate`, `db:migrate`, `dev:app`) | hooks, agents, `setup-worktree.sh`, rules | ton gestionnaire de paquets + tes commandes équivalentes |
| `biome` (lint/format) | `hooks/auto-lint.sh`, rules | ton linter/formatter |
| `drizzle` (migrations `db:*`) | agents, rules | ton ORM, ou retirer |
| Dev server : `pnpm dev:app`, ports **3001–3005**, `packages/app/.env.local` | `setup-worktree.sh`, agents | ta commande de dev + ton schéma de ports + ton fichier d'env |
| Services docker : `minio`, `maildev`, `valkey`, `clamav` | `setup-worktree.sh`, section `## Requires services` des tickets | tes services (ou aucun) |
| `kubectl` (repro de bug env-specific) | `agents/bug-analyst` | ton contexte k8s, ou supprimer cette sous-stratégie |
| Monorepo `packages/app` | scripts, agents | le chemin de ton app |

---

## 4. Hooks (`.claude/hooks/`) — 100 % egapro, à réécrire

| Hook | Contenu egapro | Action |
|---|---|---|
| `block-bad-patterns.sh` | patterns interdits Next/DSFR/tRPC (`style={`, `process.env`, alias `~/`, `@media`, `getFullYear()`, `slice(0,9)`, imports `zod`…) | réécrire pour tes anti-patterns, ou repartir minimal |
| `auto-lint.sh` | `pnpm biome check --write` | brancher sur ton formatter |
| `check-pr-reviews.sh` | `gh` + skip sur branche `alpha` | adapter le nom de branche |

Câblage dans `.claude/settings.json` (matchers `Edit\|Write`, `Edit\|Write\|Bash`, `UserPromptSubmit`) — portable tel quel.

---

## 5. Agents

- **Frontmatter ajouté** par le kit à 10 agents (`name` / `description` / `model`) pour qu'ils s'enregistrent dans un projet vierge (les fichiers egapro d'origine n'en avaient pas). Vérifier que le format colle à ta version de Claude Code. Modèles repris tels quels : PO / architect / bug-analyst = **opus** ; code-dev / doc-writer / validator / structural-auditor / rgaa-auditor / security-auditor / functional-validator = **sonnet** (code-dev passe en opus si label `complexe`).
- **MCP référencés** par code-dev / bug-analyst / architect : `figma-dev`, `playwright`, `next-devtools`, `dsfr` → connecter ceux utiles, ou retirer les étapes correspondantes (cf. §7).
- **Domaine métier** dans code-dev + rules : `getCurrentYear`/`getCseYear`/`extractSiren`, SIREN/SIRET, `~/modules/domain` → spécifique egapro, sans objet ailleurs.

---

## 6. Rules — garder / réécrire / recréer

| Tier | Fichiers | Action |
|---|---|---|
| **Process (garder, adapter IDs/commandes)** | `github-board.md`, `ticket-spec-format.md`, `complexity-estimation.md`, `git-artefact-hygiene.md`, `automation.md`, `bug-fix-workflow.md` | conserver ; adapter IDs (§1) et commandes (§3) |
| **Stack egapro (fournies mais à réécrire)** | `code-quality.md`, `testing.md`, `e2e.md`, `figma-workflow.md`, `visual-quality-validation.md`, `audit-logging.md` | réécrire pour ta stack, ou supprimer |
| **Non fournies (egapro pur — recréer au besoin)** | `react-components.md`, `styling-dsfr.md`, `database-drizzle.md`, `trpc-api.md` | absentes du kit (chargées par `paths:` à l'édition de code) ; créer tes équivalents si tu veux guider ton code-dev |

`automation.md` contient en plus des règles inline egapro (tRPC / Drizzle / DSFR / audit-logging) — élaguer la section « While writing — inline rules ».

---

## 7. MCP à connecter (ou retirer)

| MCP | Usage dans le kit | Si non connecté |
|---|---|---|
| `figma-dev` | specs UI pixel-perfect (architect, code-dev) | retirer les sections Figma des specs/agents |
| `playwright` | repro de bug + E2E (bug-analyst, e2e-dev) | retirer la repro visuelle / E2E |
| `next-devtools` | erreurs runtime Next.js | sans objet hors Next.js |
| `dsfr` | composants DSFR | sans objet hors DSFR |

---

## 8. Skills auxiliaires

- **Fournis** : `/analyse`, `/implement`, `/report`, `/open`.
- **`/loop`** : plugin Claude Code, **non fourni**, requis par `/implement` mode epic (`Skill("loop", args="/report <N>")`, step 4). S'il n'est pas dispo : remplacer cet appel par un `/report <N>` manuel périodique dans `skills/implement/SKILL.md`.
- **Non fournis** (hors périmètre) : `/doc`, `/review`, `/velocity`, `/plan-sprint`. Les scripts `plan_sprint.sh` et `sprint_velocity.sh` sont embarqués (dépendances internes) mais inutiles sans ces skills — supprimables.

---

## Annexe — si la cible est Jira (au lieu de GitHub)

Ce kit est câblé GitHub (issues + Project v2 + `gh`). **Le portage Jira a été réalisé une fois pour toutes** : ne pars pas de ce kit pour re-porter, installe directement la version déjà portée (kit édition Jira, avec la lib `jira_rest.sh` et sa notice `INSTALL-JIRA.md`) — procédure et retour d'expérience dans **`portage-jira.md`** (joint à ce kit, §7 ; la config portée est distribuée à côté du tuto, dossier `ref/`). Deux deltas à connaître dès maintenant :

- **L'argument devient une clé d'issue**, pas un numéro : `/analyse KAN-1` (et non `/analyse 1`). `KAN` = clé du projet, en **majuscules**. Chaque projet Jira a son propre compteur → le numéro seul est ambigu. Le parseur **Step 0** de `skills/analyse/SKILL.md` doit accepter `^[A-Z][A-Z0-9]*-[0-9]+$` (+ URL `.../browse/KAN-1`) :

  ```bash
  case "$ARG_HEAD" in
    [A-Z][A-Z0-9]*-[0-9]*)  ISSUE_KEY="$ARG_HEAD" ;;
    *://*/browse/*)         ISSUE_KEY="$(echo "$ARG_HEAD" | sed -E 's#.*/browse/([A-Z][A-Z0-9]*-[0-9]+).*#\1#')" ;;
    *)                      ISSUE_KEY="" ;;
  esac
  ```

- **La détection de mode** lit `getJiraIssue(KEY).fields.issuetype.name` (Epic→epic, Story/Task→task, Bug→bug) au lieu du `issueType` GitHub.

Le reste (IDs board → IDs Jira, transitions de statut, story points, sprint, parent/Epic Link, lien PR via clé d'issue) : voir `portage-jira.md`.

---

## 9. Checklist finale

- [ ] `gh auth` OK + Project v2 créé + champs Status/Size/Estimate/Sprint
- [ ] IDs board ré-extraits et remplacés aux **5 endroits** (§1)
- [ ] `owner/repo` remplacé partout (§2)
- [ ] branche de base (`alpha`) remplacée + `EPIC_DEFAULT_BASE` (§2)
- [ ] commandes stack (pnpm/biome/drizzle/dev server/ports/services) adaptées (§3)
- [ ] hooks réécrits (§4)
- [ ] MCP connectés ou références retirées (§7)
- [ ] `/loop` dispo, sinon fallback (§8)
- [ ] **Test bout-en-bout** sur un ticket jouet : `/analyse <issue>` → commentaire d'analyse + sizing, puis `/implement <issue>` → branche + PR + statut `In progress`

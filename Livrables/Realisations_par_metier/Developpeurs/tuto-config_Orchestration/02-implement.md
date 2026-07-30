# Reproduire `/implement`

Phase **exécution**. Détecte le mode depuis le type d'issue et lance le bon moteur. Seul skill autorisé à bouger le board (`To Do → In progress`).

## 1. Mécanisme

| Type d'issue | Mode | Moteur |
|---|---|---|
| `Feature` | epic | `epic_loop.sh` en **background** (`nohup … &`) : dispatch parallèle des sous-tickets, gate E2E bloquante, doc, PR finale `epic/<N> → alpha`. |
| `Task` / `Bug` | task / bug | `claude --agent code-dev` en **CLI foreground** (bloquant), puis `claude --agent e2e-dev` si `validated`. |

**Règle d'architecture centrale :** `code-dev` tourne comme **main agent** (son propre process `claude --agent`, **jamais** via le Task tool). Raison : il spawn lui-même ses sous-agents (`tu-dev`, les 4 validateurs, `functional-validator`) — **un sous-agent ne peut pas en spawner d'autres.**

**Propriété des tests :** `code-dev` n'écrit **aucun** test. TU + intégration → `tu-dev` (Opus, pendant le dev). E2E → `e2e-dev` (Opus, **en fin de pipeline**, seul propriétaire de `src/e2e/**`).

**Board :** `code-dev` passe le ticket `In progress` et l'y laisse. `In review` / `Done` = **humain uniquement** (`set_ticket_status.sh` refuse ces deux transitions, exit 3).

## 2. Prérequis spécifiques (en plus de ceux de `/analyse`)

- **Mode headless de `claude`** opérationnel :
  ```bash
  env -u CLAUDECODE timeout 5400 claude --agent code-dev --model "$MODEL" \
    --print --output-format stream-json --verbose \
    --dangerously-skip-permissions --max-budget-usd "$BUDGET" "$PROMPT"
  ```
- **git worktrees + stack docker** : `scripts/setup-worktree.sh <index>` alloue les ports (dev server = `3001 + index`), jusqu'à `EPIC_MAX_PARALLEL` (5) en parallèle.
- **Branche d'intégration** `epic/<N>` : les PR des sous-tickets ciblent cette branche, pas `alpha`.
- **`.claude/settings.json`** : env (`EPIC_MAX_PARALLEL`, `EPIC_DEFAULT_BASE`) + 3 hooks.

## 3. Fichiers à créer

```
.claude/skills/implement/SKILL.md
.claude/agents/code-dev/AGENT.md            # main agent (exécute 1 ticket bout-en-bout)
.claude/agents/tu-dev/AGENT.md              # writer : tests vitest (TU + intégration)
.claude/agents/e2e-dev/AGENT.md             # writer : tests Playwright (fin de pipeline)
.claude/agents/architect-rework/AGENT.md    # régression E2E / feedback user → tickets de fix
.claude/agents/validator/AGENT.md           # gate : typecheck+test+lint+format
.claude/agents/structural-auditor/AGENT.md  # gate : audit structurel
.claude/agents/rgaa-auditor/AGENT.md        # gate : accessibilité RGAA
.claude/agents/security-auditor/AGENT.md    # gate : OWASP + RGS
.claude/agents/functional-validator/AGENT.md# rejoue les scénarios (commente, ne touche pas au board)
.claude/settings.json                       # env + hooks
.claude/hooks/{block-bad-patterns,auto-lint,check-pr-reviews}.sh
scripts/orchestration/*.sh                  # le moteur (voir §5)
```

## 4. Le skill — squelette

```markdown
---
name: implement
description: "Phase exécution. Détecte le mode (epic/task/bug) selon le type d'issue et lance le bon mécanisme. Usage: /implement <issue#>"
---

# /implement

## Step 0 — valider l'argument
gh issue view "$N" --json number,title,issueType,labels,state   # type + state

## Step 1 — vérifier que l'analyse a été faite (sinon code-dev n'a pas de spec)
| Feature | subIssues.totalCount > 0 ET commentaire `## Analyse PO` |
| Task    | commentaire `## Analyse architecte` |
| Bug     | commentaire `## Analyse du bug` |
Si absent → proposer `/analyse <N>` et exit.

## Step 2 — dispatcher (voir §4.1 / §4.2)
```

### 4.1 Mode epic — loop driver background

1. Vérifier qu'aucun loop ne tourne déjà : `pgrep -af "epic_loop.sh.*<KEY>"`.
2. **Aligner le main worktree sur `epic/<N>`** (refuser si working tree dirty) : `ensure_epic_branch.sh <N>` puis `git checkout epic/<N>`.
3. Lancer en background, **sans attendre** :
   ```bash
   nohup bash scripts/orchestration/epic_loop.sh <N> > /tmp/epic_loop_<KEY>.log 2>&1 &
   disown
   ```
4. **Auto-report** : `Skill("loop", args="/report <N>")` (cadence dynamique 60–1800 s). À chaque réveil, vérifier si la PR finale `epic/<N> → alpha` est ouverte.
5. Rendre la main immédiatement.
6. **Gate d'acceptation utilisateur** (quand la PR finale s'ouvre) : présenter la PR + comment tester (review app ou `/open <PR>`) → `AskUserQuestion` « Tout est bon / Demander des changements ». Sur changement → réinitialiser la gate E2E + `run_architect_rework.sh <N> "<description>"` → relancer `epic_loop.sh`. Boucle jusqu'à « Tout est bon ».

### 4.2 Mode task / bug — code-dev synchrone foreground

1. **Worktree + docker** : base = `origin/epic/<EPIC_N>` (sous-issue) ou `origin/alpha` (standalone) ; `git worktree add` + `setup-worktree.sh <index>`.
2. `create_linked_branch.sh "$N" "$BASE"` (branche linkée à l'issue).
3. `set_ticket_status.sh "$N" "In progress"`.
4. **Lancer code-dev** (bloquant) — modèle = `opus` si label `complexe`, sinon `sonnet` :
   ```bash
   claude --agent code-dev --model "$MODEL" --print --output-format stream-json \
     --dangerously-skip-permissions --max-budget-usd "$BUDGET" "$PROMPT" | tee /tmp/code-dev-$N.jsonl
   ```
   Récupérer le **dernier objet JSON** `{"status":…}` et brancher :

   | `.status` | Action |
   |---|---|
   | `validated` | enchaîner sur **e2e-dev** (étape 5) ; ticket reste `In progress` |
   | `needs_opus_escalation` | relancer code-dev `--model opus`, même prompt |
   | `refacto` | stop, ticket en `To Do`, next-step `/analyse <N>` (re-spec) |
   | `rate_limited` | proposer de retenter dans `retry_in` s |
   | `failed` | propager l'erreur, ne pas toucher le ticket |

5. **Lancer e2e-dev** (si `validated`, même worktree) :
   ```bash
   claude --agent e2e-dev --model opus --print --output-format json \
     --dangerously-skip-permissions --max-budget-usd 15 "$E2E_PROMPT" | tee /tmp/e2e-dev-$N.json
   ```
   | `.status` e2e-dev | Action |
   |---|---|
   | `validated` | tests poussés sur la branche (CI re-déclenchée) — fin |
   | `regression` | **bloquant** : `claude --agent architect-rework …` → tickets de fix (next-step `/implement <fix>`) |
   | `rate_limited` / `failed` | signaler, proposer de relancer |

> Le **contrat de sortie JSON** (`{"status": …}` en dernier message) est ce qui permet à l'orchestrateur de brancher. Chaque agent exécuté en headless doit le respecter strictement.

## 5. Le moteur `scripts/orchestration/`

`/implement` n'orchestre rien lui-même : tout est dans ces scripts. Les reproduire (ou les réécrire) :

| Script | Rôle |
|---|---|
| `epic_loop.sh` | **Loop driver** : à chaque tick, calcule le plan, dispatche les sous-tickets prêts en parallèle, traite les retours, rebase la branche epic, déclenche la gate E2E + doc + PR finale. |
| `dispatch_plan.sh` | Calcule quels tickets sont dispatchables (déps `Depends on` satisfaites, branche non gone). |
| `process_tick_result.sh` | Mutations board post-tick + anti-boucle (`attempt=1/2/3` → `dispatch=escalate`) + squash-merge des PR validées dans `epic/<N>`. |
| `ensure_epic_branch.sh` / `rebase_epic_branch.sh` / `merge_validated_ticket.sh` / `open_epic_final_pr.sh` | Cycle de vie de la branche d'intégration. |
| `run_e2e_dev.sh` → `run_architect_rework.sh` | Gate E2E bloquante de fin d'epic → sur régression, crée les tickets de fix reprocessés par le loop. |
| `run_doc_writer.sh` | Régénère la doc (best-effort) après gate E2E verte. |
| `set_ticket_status.sh` / `set_ticket_size.sh` / `create_linked_branch.sh` / `force_pr_issue_link.sh` / `cache_gh.sh` / `log_event.sh` | Helpers board / git / cache `gh` / logging. |

## 6. Config `settings.json` + hooks

```jsonc
{
  "env": { "EPIC_MAX_PARALLEL": "5", "EPIC_DEFAULT_BASE": "origin/chore/ai-pipeline" },
  "hooks": {
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "...check-pr-reviews.sh" }] }],
    "PreToolUse":  [{ "matcher": "Edit|Write",      "hooks": [{ "type": "command", "command": "...block-bad-patterns.sh" }] }],
    "PostToolUse": [{ "matcher": "Edit|Write|Bash", "hooks": [{ "type": "command", "command": "...auto-lint.sh" }] }]
  }
}
```

- `block-bad-patterns.sh` (PreToolUse) : bloque les patterns interdits avant l'écriture (`as any`, `style={`, `process.env`, `../../`, `@ts-ignore`…).
- `auto-lint.sh` (PostToolUse) : `biome check --write` sur le fichier édité.
- `check-pr-reviews.sh` (UserPromptSubmit) : alerte si la branche a une PR avec reviews non résolues.

Variables d'ajustement (defaults) : `EPIC_MAX_PARALLEL=5`, `EPIC_LOOP_MAX_TICKS=30`, `EPIC_LOOP_BUDGET_SONNET=10`, `EPIC_LOOP_BUDGET_OPUS=40`, `EPIC_LOOP_AGENT_TIMEOUT=5400`.

## 7. Suivi & reprise

- `/report <N>` à tout moment ; `tail -f /tmp/epic_loop_<KEY>.log` ; `ls .claude/state/epic_run/ticks/<KEY>/`.
- **Codes de sortie epic** : `0` PR finale ouverte / `1` erreur technique / `2` escalade (3 refacto ou conflit rebase) / `3` plafond de ticks.
- **Reprise** : relancer `/implement <N>` (idempotent : worktrees réutilisés, tickets gone skippés). Tuer un loop : `pkill -f "epic_loop.sh.*<KEY>"`.

## 8. Vérifier

```
/implement <task#>
```
Attendu : worktree créé → ticket `In progress` → `code-dev` retourne `validated` (`## Code: PASS`) → `e2e-dev` `## E2E: PASS` → PR draft passée `ready`. Le ticket reste `In progress` (à toi de le passer `In review`).

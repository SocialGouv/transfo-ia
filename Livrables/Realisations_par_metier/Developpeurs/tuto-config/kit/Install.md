# Install.md — installer le kit dans un projet

Procédure de bout en bout : du zip à un `/analyse` + `/implement` qui tournent. Ce fichier donne **l'ordre** et la **vérification** ; les valeurs précises à substituer sont dans [`toAdapt.md`](toAdapt.md) (référencé à chaque étape).

Dérouler dans l'ordre — chaque étape suppose la précédente faite.

---

## Étape 0 — Prérequis (vérifier d'abord)

```bash
gh auth status                 # gh authentifié sur le repo cible
claude --version               # CLI claude dans le PATH (mode headless)
git --version                  # >= 2.5 (worktrees)
docker compose version         # stack de test par ticket
```

Côté GitHub (UI, une fois) : **Issue types** `Feature`/`Task`/`Bug` activés (org) + un **Project v2** avec les champs `Status` (single-select), `Size` (single-select XS→XL), `Estimate` (number), `Sprint` (iteration). Skill `/loop` : optionnel (auto-report epic) — sinon fallback en `toAdapt.md` §8.

---

## Étape 1 — Déposer les fichiers

```bash
unzip kit-analyse-implement.zip
cp -r kit/.claude  <projet>/.claude     # FUSIONNER si .claude existe déjà (ne pas écraser)
cp -r kit/scripts  <projet>/scripts
chmod +x <projet>/scripts/**/*.sh
```

> Si `<projet>/.claude/settings.json` existe déjà : fusionner à la main les blocs `env` et `hooks` (ne pas remplacer le fichier).

---

## Étape 2 — Extraire les IDs de TON board  ⚠️ bloquant

Récupère le `PROJECT_ID` (`gh project list --owner <org>` → `gh project view <n> --format json`), puis les field/option/type IDs avec les requêtes GraphQL de [`toAdapt.md`](toAdapt.md) §1. Note-les : tu en as besoin à l'étape 3.

---

## Étape 3 — Substituer les IDs (5 endroits)  ⚠️ bloquant

Remplacer **tous** les IDs egapro par les tiens dans ([`toAdapt.md`](toAdapt.md) §1 = tableau de correspondance) :

```
.claude/rules/github-board.md
.claude/agents/architect/AGENT.md
scripts/orchestration/set_ticket_status.sh
scripts/orchestration/set_ticket_size.sh
scripts/orchestration/plan_sprint.sh
```

Vérif (plus aucun ID egapro ne doit rester) :
```bash
grep -rn "PVT_kwDOAh0HH84BFsK7\|IT_kwDOAh0HH84Aa" .claude scripts || echo "OK : aucun ID egapro résiduel"
```

---

## Étape 4 — Repo & branche

```bash
# owner/repo (~35 fichiers)
grep -rl "SocialGouv/egapro" .claude scripts | xargs sed -i 's#SocialGouv/egapro#<org>/<repo>#g'
# branche de base 'alpha' : repérer puis remplacer au cas par cas (mot courant, PAS de sed aveugle)
grep -rn "\balpha\b" .claude scripts
```
Puis `.claude/settings.json` : `EPIC_DEFAULT_BASE` (`origin/chore/ai-pipeline` → ta branche), et l'URL review app si tu en as une ([`toAdapt.md`](toAdapt.md) §2).

---

## Étape 5 — Stack build/test/dev

Mapper la stack egapro (pnpm / Biome / Drizzle / Next / ports 3001–3005 / services docker) sur la tienne — tableau complet [`toAdapt.md`](toAdapt.md) §3. Fichiers les plus impactés : `scripts/setup-worktree.sh`, `.claude/hooks/auto-lint.sh`, et les commandes citées dans les agents/rules.

---

## Étape 6 — Hooks

`.claude/hooks/` est 100 % egapro ([`toAdapt.md`](toAdapt.md) §4). Au minimum :
- `block-bad-patterns.sh` : neutraliser (ou réécrire pour tes anti-patterns) — sinon il bloquera des `Edit`/`Write` légitimes.
- `auto-lint.sh` : remplacer `pnpm biome check --write` par ton formatter.
- `check-pr-reviews.sh` : adapter le nom de branche skippée.

---

## Étape 7 — MCP & rules

- Connecter les MCP utiles (`figma-dev`, `playwright`, `next-devtools`, `dsfr`) ou retirer les étapes qui les utilisent ([`toAdapt.md`](toAdapt.md) §7).
- Rules : garder les 6 « process », réécrire/supprimer les 6 « stack egapro », recréer les 4 non fournies si besoin ([`toAdapt.md`](toAdapt.md) §6).

---

## Étape 8 — Vérification

**a. Statique**
```bash
python3 -c "import json;json.load(open('.claude/settings.json'));print('settings.json OK')"
ls -l scripts/orchestration/*.sh scripts/*.sh | grep -v 'rwx' && echo "!! scripts non exécutables" || echo "perms OK"
```

**b. Agents enregistrés** — ouvrir Claude Code dans le projet, vérifier via `/agents` que `code-dev`, `architect`, `product-owner`, etc. apparaissent.

**c. Bout-en-bout sur un ticket jouet**
1. Créer une issue `Task` jouet, lui mettre le type `Task`.
2. `/analyse <N>` → attendu : commentaire `## Analyse architecte` posté + `Size` écrite sur le board + **aucune** transition de statut.
3. `/implement <N>` → attendu : worktree créé, branche linkée, statut → `In progress`, `code-dev` tourne et ouvre une PR draft.

Si a/b/c passent : le kit est opérationnel.

---

## Dépannage

| Symptôme | Cause probable | Fix |
|---|---|---|
| GraphQL `node not found` | IDs board faux/incomplets | re-extraire (étape 2), revérifier les 5 fichiers (étape 3) |
| Agent introuvable au dispatch | frontmatter / registration | vérifier `name:` en tête de l'`AGENT.md`, relancer Claude Code |
| Tout `Edit`/`Write` est bloqué | `block-bad-patterns.sh` trop strict | neutraliser/adapter (étape 6) |
| `/implement` epic ne s'auto-rapporte pas | `/loop` absent | fallback `toAdapt.md` §8 (|`/report <N>` manuel) |
| `gh: not found` dans un script headless | `gh` absent du PATH du process détaché | installer `gh` / fixer le PATH du shell de `nohup` |
| dev server ne démarre pas dans le worktree | commande/ports/services non adaptés | étape 5 (`setup-worktree.sh`) |

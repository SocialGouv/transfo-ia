# Portage Jira — pipeline `/analyse` + `/implement`

## Objectif

Faire tourner la pipeline IA de dev (conception `/analyse`, exécution `/implement`) avec **Jira comme tracker** à la place de GitHub Issues/Projects — sans toucher au reste : le code, les branches, les PR et la CI restent sur l'hôte git. Le portage a été **réalisé une fois pour toutes** ; la config qui en résulte (kit édition Jira, dossier `ref/`) s'installe, elle ne se re-porte pas.

## La logique en une image

```
        couche conversationnelle                couche bash headless
        (LLM présent)                           (nohup, aucun LLM)
        /analyse · /implement step 0-1          epic_loop.sh + helpers
        · mode task/bug · claude --agent        (mode epic)
                 │                                      │
                 ▼                                      ▼
        MCP Atlassian Rovo (OAuth)              REST Jira via jira_rest.sh (token)
                 └───────────────► Jira Cloud ◄─────────┘
                            (issues · statuts · points · sprint)

        hôte git (INCHANGÉ) : branches ticket/<KEY>-… · PR · CI (gh)
        lien Jira ↔ PR par la clé d'issue dans branche + titre (DVCS)
```

La contrainte qui structure tout : **un outil MCP est appelé par le LLM, jamais par un script bash**. L'orchestration epic tourne détachée (`nohup`), sans LLM → elle passe par l'API REST. D'où deux canaux pour un même board.

## Comment il s'y prend

1. **Ne porter que la couche tracker**, isolée derrière deux seams : le fichier de référence board (`github-board.md` → `jira-board.md` : IDs, recettes d'extraction, JQL) et les helpers d'écriture (`set_ticket_status.sh`, `set_ticket_size.sh`, `create_linked_branch.sh`) qui **gardent leurs signatures** → les appelants ne bougent pas.
2. **Factoriser tout le REST** dans une lib unique, `scripts/orchestration/jira_rest.sh` (12 fonctions) : auth basic `email:token`, conversion texte → **ADF** (l'API v3 refuse le Markdown brut), transitions résolues **par nom** (les IDs sont des arêtes de workflow, instables). Leçon du réel : les *lectures* board d'`epic_loop.sh` tapaient `gh` en direct, hors seam — elles passent aussi par la lib.
3. **Adopter les conventions Jira** : argument = clé d'issue (`/analyse KAN-1`), mode déduit de `issuetype.name` (`Epic`→epic, `Story`/`Task`→task, `Bug`→bug), lien epic↔enfant par champ `parent` (team-managed) ou Epic Link (company-managed), labels sans `=` ni espace (`dispatch_escalate`, `attempt_N`), sizing en story points Fibonacci (XS=1 … XL=8).
4. **Conserver les invariants** de la pipeline : marqueurs `## Analyse …` identiques, body des tickets intact, contrat JSON des agents headless, et la règle humain-only — aucun agent ne passe un ticket `In review`/`Done` (`set_ticket_status.sh` refuse, exit 3 ; IDs de ces transitions volontairement non exposés).

## Ce qui change / ce qui ne change pas

| | |
|---|---|
| **Porté** | référence board, helpers board, lectures/écritures tracker, argument + détection de mode, labels, sizing |
| **Inchangé** | skills/agents (logique), moteur d'orchestration (flux), couche git/PR (`gh`), gates qualité, invariants ci-dessus |
| **Élagué** | `/velocity`, `/plan-sprint`, rules propres à egapro (figma, visual-quality, audit-logging) |

## État & installation

- **Éprouvé** : mode task/bug (MCP, synchrone). **Porté mais non testé bout-en-bout** : mode epic (REST headless) — à éprouver après branchement.
- **Installer** (détail : `03-portage-jira.md` §7 et `INSTALL-JIRA.md` dans l'historique git de `ref/`) : ① extraire la config (`git archive HEAD -- .claude scripts .mcp.json INSTALL-JIRA.md | tar -x -C <projet>`) ② authentifier le MCP (`/mcp`) ③ remplir `jira-board.md` avec les IDs de TON instance (non devinables) ④ `gh auth` + remplacer `<ORG>/<REPO>` ⑤ `export JIRA_API_TOKEN` (epic seulement) ⑥ adapter hooks/rules si autre stack que Vite/React/oxlint.

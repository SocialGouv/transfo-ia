# Plan d'implémentation : repo d'évaluation LLM

Plan rédigé le 23/10/2026. Les points marqués *vérifié* l'ont été ce jour dans le code et la documentation de Harbor (github.com/harbor-framework/harbor). Les points marqués *à vérifier au J0* sont des hypothèses à confirmer par le premier jalon.

## 1. Objectif

Tu choisis un harness et un modèle, tu lances une commande, et tu obtiens un résultat comparable aux autres runs : score par tâche, coût, tokens, durée, trajectoire complète.

```bash
make run SUITE=rgaa AGENT=claude-code MODEL=anthropic/<id-modele>
make run SUITE=code AGENT=opencode    MODEL=openrouter/<editeur>/<modele>
make report
```

- **Modèles Anthropic** : par l'API Anthropic ou par Bedrock.
- **Modèles hors Anthropic** : par OpenRouter.
- **Aucun modèle n'est inscrit dans le repo.** Le repo connaît des *routes* (comment joindre un fournisseur), jamais une liste de modèles.
- **Trois suites** : RGAA (pré-audit d'accessibilité), code (front et back), sécurité (revue de PR).

## 2. Choix structurants

### 2.1 Harbor comme moteur

Harbor est le framework de l'équipe Terminal-Bench (licence Apache-2.0, poussé le 23/10/2026). Il fait le travail qu'on ne veut pas réécrire *(vérifié)* :

- il installe et lance le harness dans un conteneur Docker ;
- il résout les clés et le routage vers le fournisseur ;
- il enregistre tokens, coût et trajectoire de chaque essai dans `result.json` ;
- il fait tourner le correcteur dans un bac à sable séparé de celui de l'agent ;
- il applique une politique réseau par phase (installation, agent, correcteur) ;
- il recalcule les scores sans relancer l'agent (`harbor job regrade`).

Harnesses intégrés, avec leur nom pour `-a` : `claude-code`, `opencode`, `codex`, `vibe`, `kimi-code`, `kimi-cli`, `qwen-coder`, `gemini-cli`, `goose`, `aider`, `openhands`, `mini-swe-agent`, `cline-cli`, `cursor-cli`, `copilot-cli`, `terminus-2`, et d'autres. Deux agents servent au contrôle des tâches :
- `oracle` joue la solution de référence ;
- `nop` ne fait rien.

Un harness absent de cette liste s'ajoute en classe Python (`BaseAgent`), déclarée par `import_path`.

### 2.2 Contrat de sortie par fichier

Les tâches de revue (RGAA, sécurité) imposent d'écrire les constats dans `/app/out/findings.json`, selon un schéma JSON fourni dans l'énoncé. Le correcteur ne lit que ce fichier. Le score ne dépend donc ni du harness ni de sa façon de répondre. Un fichier absent ou invalide donne `format_ok = 0` et un score nul.

### 2.3 Repo privé

Les réponses attendues ne doivent jamais être publiées : un modèle entraîné dessus fausserait les résultats suivants. Le repo d'évals est donc privé, séparé de transfo-ia, et seuls les résultats agrégés partent dans transfo-ia.

## 3. Arborescence

```
llm-eval/
├── README.md                  # lancer un run en 3 étapes, tableau des routes
├── AGENTS.md                  # règles pour ajouter une tâche (humain ou agent)
├── pyproject.toml             # harbor épinglé, evalkit, dépendances (uv)
├── uv.lock
├── Makefile                   # smoke, run, validate, regrade, report, view
├── .env.example               # clés, jamais commité rempli
├── routes/                    # comment joindre un fournisseur
│   ├── anthropic.env
│   ├── bedrock.env
│   ├── openrouter.env
│   └── prix.yaml              # facultatif, prix saisis par toi (repli si le harness ne remonte pas le coût)
├── suites/
│   ├── hello/                 # tâche triviale pour les tests de fumée
│   ├── rgaa/
│   │   ├── dataset.toml
│   │   ├── metric.py          # agrégation de la suite
│   │   └── <id-tache>/        # une tâche Harbor (section 4)
│   ├── code/
│   └── securite/
├── evalkit/                   # code partagé par les correcteurs (copié dans les images de vérification)
│   ├── schemas/
│   │   ├── findings-rgaa.schema.json
│   │   └── findings-securite.schema.json
│   ├── match_rgaa.py
│   ├── match_securite.py
│   ├── cwe_familles.yaml
│   └── reward.py              # écriture de /logs/verifier/reward.json
├── sources/                   # matière première versionnée, d'où les tâches sont générées
│   ├── rgaa/
│   │   ├── erreurs-reference.csv
│   │   ├── criteres-couverts.md
│   │   └── pages/<page>/      # pages figées
│   ├── code/prs.yaml
│   └── securite/injections.yaml
├── scripts/
│   ├── run.py                 # construit et lance la commande harbor
│   ├── build_rgaa.py          # sources/rgaa -> suites/rgaa
│   ├── mine_prs.py            # propose des PR candidates -> sources/code/prs.yaml
│   ├── build_code.py          # sources/code -> suites/code
│   ├── build_securite.py      # sources/securite -> suites/securite
│   ├── validate.py            # lint + oracle + nop + stabilité du correcteur
│   └── report.py              # jobs/ -> results/
├── jobs/                      # sorties brutes Harbor (ignoré par git)
└── results/
    ├── summary.csv            # une ligne par essai (commité)
    ├── report-<suite>.md      # tableaux par couple harness × modèle (commité)
    └── compat.md              # matrice de fumée harness × route (J0)
```

Les dossiers `suites/*/<id-tache>/` sont **générés** par les scripts `build_*`. On ne les modifie jamais à la main : on corrige la source, puis on régénère.

## 4. Format commun d'une tâche

```
suites/<suite>/<id-tache>/
├── task.toml
├── instruction.md             # l'énoncé donné à l'agent, contrat de sortie inclus
├── environment/Dockerfile     # image de l'agent
├── tests/
│   ├── Dockerfile             # image du correcteur (evalkit + réponse attendue)
│   ├── test.sh                # écrit /logs/verifier/reward.json
│   └── expected.json          # réponse attendue (revues) ou liste des tests (code)
└── solution/solve.sh          # solution de référence, jouée par l'agent oracle
```

`task.toml` type :

```toml
schema_version = "1.1"
artifacts = ["/app/out"]                 # seul ce qui est déclaré passe au correcteur

[task]
name = "rgaa/egapro-declaration"

[metadata]
suite = "rgaa"
source = "RGAA-Tool-Monitoring@<sha>"
date_source = "2026-07-21"               # sert à écarter les tâches antérieures à la date de coupure d'un modèle
lot = "dev"                              # dev | cache
criteres = ["1.1", "3.2", "10.7"]

[environment]
network_mode = "public"                  # installation du harness

[agent]
timeout_sec = 1800.0
network_mode = "allowlist"
allowed_hosts = []                       # l'hôte du fournisseur est ajouté au lancement (section 5)

[verifier]
environment_mode = "separate"
network_mode = "no-network"
timeout_sec = 300.0
```

Règles imposées par Harbor *(vérifié)* :
- un correcteur séparé démarre sans les fichiers de l'agent : tout ce qu'il lit doit figurer dans `artifacts` ;
- `harbor job regrade` exige ce mode séparé et des artefacts collectés.

Règles du repo, écrites dans `AGENTS.md` :

- **Pas de fuite de réponse.** L'image de l'agent ne contient ni `expected.json`, ni historique git postérieur au commit de départ, ni `solution/`.
- **Pas d'accès web.** Le harness est lancé avec `disable_web_search=true` et seul l'hôte du fournisseur est joignable pendant la phase agent : l'agent ne peut pas aller chercher la PR d'origine.
- **Images épinglées.** Les images de base sont épinglées par empreinte (règle `unpinned-image` de `harbor lint`).
- **Une tâche n'entre dans une suite qu'après `make validate`** :
  - `harbor lint` passe ;
  - l'agent `oracle` obtient le score maximal ;
  - l'agent `nop` obtient le score minimal ;
  - le correcteur rend le même score sur 3 passages de l'oracle.
- **Une tâche qui échoue sur tous les modèles et tous les essais est d'abord suspecte.** On la relit avant de conclure que les modèles en sont incapables.

## 5. Lancer un run

### 5.1 Routes

| Route | Forme de `MODEL` | Variables dans `.env` | Hôte ouvert pendant la phase agent |
|---|---|---|---|
| API Anthropic | `anthropic/<id-modele>` | `ANTHROPIC_API_KEY` | `api.anthropic.com` |
| Bedrock | `bedrock/<id-profil-inference>` | `AWS_BEARER_TOKEN_BEDROCK` ou identifiants AWS, `AWS_REGION` ; `CLAUDE_CODE_USE_BEDROCK=1` pour Claude Code | `bedrock-runtime.<region>.amazonaws.com` |
| OpenRouter | `openrouter/<editeur>/<modele>` | `OPENROUTER_API_KEY` | `openrouter.ai` |

Ce que Harbor fait déjà *(vérifié)* :
- il lit le préfixe du modèle et transmet la clé sous le nom attendu par le harness (par exemple `OPENROUTER_API_KEY` devient `OPENAI_API_KEY` pour Codex) ;
- avec Claude Code et un fournisseur autre qu'Anthropic, il passe par le format Anthropic Messages : base `https://openrouter.ai/api`, clé dans `ANTHROPIC_AUTH_TOKEN`.

*À vérifier au J0* :
- les noms exacts des variables Bedrock pour chaque harness hors Claude Code ;
- la qualité des appels d'outils quand Claude Code pilote un modèle non Anthropic via OpenRouter.

### 5.2 Makefile

```bash
make smoke    AGENT=<harness> MODEL=<route/modele>         # suite hello, 1 essai
make run      SUITE=<suite> AGENT=<harness> MODEL=<route/modele> \
              [ATTEMPTS=3] [EFFORT=high] [SKILLS=<chemin>] \
              [AGENT_VERSION=<x.y.z>] [TASKS=<glob>] [LOT=dev|cache] [CONCURRENCY=4]
make validate SUITE=<suite> [TASKS=<glob>]
make regrade  JOB=jobs/<job> SUITE=<suite>                  # après correction de la référence
make report
make view                                                   # harbor view jobs
```

### 5.3 Ce que fait `scripts/run.py`

1. Il charge `.env`, détecte la route d'après le préfixe de `MODEL` et s'arrête si la clé manque.
2. Il construit la commande Harbor, l'affiche, puis l'exécute. On peut donc toujours la relancer à la main :

```bash
harbor run -p suites/<suite> -a <harness> -m <route/modele> \
  -k <ATTEMPTS> -n <CONCURRENCY> \
  --allow-agent-host <hote-de-la-route> \
  --ak disable_web_search=true [--ak version=<AGENT_VERSION>] [--effort <EFFORT>] \
  [--skill <SKILLS>] [-i <TASKS>] \
  -o jobs --job-name <suite>__<harness>__<modele-slug>__<AAAAMMJJ-HHMM>
```

3. Il écrit `jobs/<job>/run.json` : SHA du repo d'évals, version de Harbor, version du harness installée, route, modèle, effort, skills, lot, et fournisseur OpenRouter s'il est épinglé (section 9).

Options du harness :
- **Sans skills** par défaut : on mesure le couple harness × modèle nu.
- **`SKILLS=<chemin>`** : injecte un dossier de skills (`--skill`, *vérifié*). Par exemple ultraA11y, ou vos skills `/implementation`. On mesure ainsi ce que les skills apportent, toutes choses égales par ailleurs.
- **`--ak`** : transmet les autres options du harness. Pour Claude Code par exemple : `max_turns`, `max_budget_usd`, `reasoning_effort` *(vérifié)*.

## 6. Suite RGAA

**Source.** Le framework RGAA-Tool-Monitoring :
- `erreurs-reference.csv` : page, critère, sélecteur CSS de l'élément, sévérité, validation par l'experte ;
- `criteres-couverts.md` ;
- les pages figées.

Prérequis bloquant : sur GitHub, le CSV ne contient qu'une ligne d'exemple et le dossier `pre-audits/` que le modèle de compte rendu. Il faut récupérer la référence remplie et les pages figées auprès de Max, de Lucas ou de l'experte.

**Une tâche = une page figée.**
- L'image de l'agent contient :
  - la page dans `/app/page/` ;
  - la liste des critères à vérifier dans `/app/criteres.json`, tirée de `criteres-couverts.md`.
- L'énoncé demande un pré-audit sur ces critères et fixe le format de sortie :

```json
[{"critere": "10.7", "selecteur": "form#declaration button.fr-btn--secondary",
  "description": "Prise de focus non visible au clavier", "severite": "majeure"}]
```

**Correcteur (`evalkit/match_rgaa.py`).**
1. Valider le fichier contre le schéma. S'il est invalide : `format_ok = 0`, arrêt.
2. Résoudre chaque sélecteur dans le DOM de la page (lxml + cssselect).
   - Un sélecteur qui ne désigne aucun élément compte comme une **hallucination**.
3. Apparier chaque constat à la référence. Un appariement exige :
   - le même critère ;
   - des ensembles d'éléments résolus qui se recoupent (on compare des éléments, pas des chaînes de sélecteurs).
   - Constat apparié : **vrai positif**.
   - Constat non apparié sur un élément existant : **fausse alerte**.
4. Une erreur de référence restée sans constat compte comme une **erreur manquée**.
5. Un constat sur un critère hors de la liste est compté à part (`hors_perimetre`). Il n'est pas pénalisé.

`reward.json` reprend les 4 chiffres du framework :

```json
{"reward": 0.71, "precision": 0.79, "rappel": 0.64, "vp": 7, "fausses_alertes": 2,
 "hallucinations": 0, "erreurs_manquees": 4, "hors_perimetre": 1, "format_ok": 1}
```

**Agrégation (`suites/rgaa/metric.py`).** Précision et rappel se calculent sur les comptes additionnés de toutes les pages (micro), et pas comme une moyenne des pages.

**Boucle avec l'experte.**
1. `make report` liste les fausses alertes de chaque run.
2. Celles que l'experte reconnaît comme de vraies erreurs entrent dans `sources/rgaa/erreurs-reference.csv`.
3. On régénère (`build_rgaa.py`), on incrémente la version de `dataset.toml`, puis `make regrade` recalcule les anciens runs sans rappeler les modèles.

**Plus tard.**
- Une variante « rendu » : la page servie sur `localhost` et un navigateur dans l'image, pour les critères qui ne se jugent pas sur le code (contraste réel, clavier, zoom).
- Des tâches tirées des cas ACT du W3C et d'Asqatasun, pour les critères mal couverts par les pages Egapro.

## 7. Suite code

**Source.** `sources/code/prs.yaml`, une entrée par PR :

```yaml
- id: egapro-1234
  repo: SocialGouv/egapro
  pr: 1234
  base_sha: <sha>             # commit parent
  date: 2026-09-12            # date de fusion
  fichiers_tests: [packages/app/src/foo.test.ts]
  installation: pnpm install --frozen-lockfile
  echec_vers_succes: ["packages/app/src/foo.test.ts"]   # tests rouges avant, verts après
  succes_vers_succes: ["packages/app"]                  # tests verts qui doivent le rester
  enonce: |                                             # ticket et critères d'acceptation, réécrits si la PR révèle la solution
    ...
```

**`mine_prs.py`** propose des candidates : PR fusionnées qui modifient des tests, après une date passée en paramètre. Le choix final reste humain. La date de chaque PR est conservée, pour que `report.py` puisse ne garder que les tâches postérieures à la date de coupure du modèle testé.

**Construction (`build_code.py`).**
- Image de l'agent : repo cloné au `base_sha`, sans historique postérieur ni remote, dépendances installées. Les images sont construites une fois, poussées dans un registre privé et épinglées par empreinte, pour ne pas réinstaller à chaque essai.
- Énoncé : le champ `enonce`, sans mention des tests cachés.
- Artefact : le patch de l'agent (`git diff` dans `/app/out/agent.patch`). Il est produit par une commande de pré-collecte Harbor *(à vérifier au J0)*. À défaut, la suite code passe en vérification partagée (`environment_mode = "shared"`) et renonce au regrade.
- Correcteur :
  1. partir d'une copie propre au `base_sha` ;
  2. appliquer le patch de l'agent, puis les fichiers de test de la PR ;
  3. lancer `echec_vers_succes` et `succes_vers_succes`.
  - Le score `reward = 1` exige que tout passe.
  - `reward.json` donne aussi la part des tests de la PR qui passent et l'absence de régression.
- `solution/solve.sh` applique la partie hors tests de la PR.

**Plus tard.** Des tests Playwright de bout en bout pour le front, avec l'application lancée dans une tâche multi-conteneurs (prise en charge par Harbor), et des bugs injectés dans du code sain, à la manière de SWE-smith.

## 8. Suite sécurité

**Source.** `sources/securite/injections.yaml`. Chaque entrée décrit :
- un repo et un commit sain ;
- un patch qui introduit soit une faille (avec sa CWE et ses lignes), soit un **leurre** : une modification qui ressemble à une faille sans en être une.

Les patchs sont écrits à la main.

**Une tâche = une PR à relire.** L'image contient le repo avec le patch appliqué et le diff dans `/app/pr.diff`. L'énoncé demande une revue de sécurité de la PR et fixe le format :

```json
[{"fichier": "src/api/declaration.ts", "ligne_debut": 42, "ligne_fin": 47,
  "cwe": "CWE-639", "severite": "haute", "description": "..."}]
```

**Correcteur (`evalkit/match_securite.py`).** Un constat est apparié s'il remplit trois conditions :
- le même fichier ;
- des plages de lignes qui se recoupent, à 3 lignes près ;
- la même CWE ou une CWE de la même famille (`cwe_familles.yaml`, table maintenue à la main).

Pour une tâche avec faille, `detecte = 1` si au moins un constat est apparié. Pour un leurre, `fausse_alerte = 1` si au moins un constat est émis.

**Agrégation (`metric.py`).**
- Score OWASP : taux de détection sur les tâches avec faille, moins taux de fausses alertes sur les leurres. Un modèle qui signale tout obtient 0.
- En complément, la précision et le rappel calculés constat par constat.

Une revue est **jugée** par du code, pas par un LLM. RewardKit (le correcteur par juge LLM de Harbor, *vérifié*) reste possible pour noter la qualité des descriptions. Ce serait un module distinct, avec le modèle juge choisi au lancement.

## 9. Reproductibilité

- **Harbor** est épinglé dans `uv.lock`.
- **Le harness** est épinglé par `AGENT_VERSION` (option `version`, sans quoi Harbor installe la dernière, *vérifié*). La version installée est relevée dans `result.json` et `run.json`.
- **Le modèle** est désigné par son identifiant exact.
- **Le fournisseur OpenRouter.**
  - Le problème : un même identifiant OpenRouter est servi par plusieurs fournisseurs, à des quantifications différentes. Constaté le 23/10/2026 sur l'API `endpoints` : jusqu'à 26 fournisseurs pour un même modèle, en fp4, fp8 ou fp32. Deux runs du « même modèle » peuvent donc ne pas tourner sur les mêmes poids.
  - La règle : épingler le fournisseur pour toute une campagne, et l'inscrire dans `run.json`.
  - Le harness construit lui-même ses requêtes. L'épinglage passe donc par les réglages du compte ou de la clé OpenRouter, ou par un preset *(mécanisme à vérifier au J0)*.
- **Version de la suite.** `dataset.toml` porte une version. `report.py` ne compare que des runs faits sur la même version.
- **Lot caché.** Une partie des tâches vit dans un second repo privé (`llm-eval-cache`), de même structure, appelé avec `LOT=cache`. Ces tâches ne servent jamais à mettre au point prompts ou skills.

## 10. Coût, débit, données

- **Plafonds de dépense** :
  - une clé OpenRouter dédiée aux évals, avec plafond de crédit ;
  - `--ak max_budget_usd=<montant>` par essai pour Claude Code.
- **Débit.** `CONCURRENCY` vaut 4 par défaut. En cas de 429, on relance les essais avec `-r`.
- **Les échecs d'infrastructure ne comptent pas comme des échecs du modèle.** Un essai interrompu par une erreur réseau, de quota ou de conteneur (`exception_info` dans `result.json`) est exclu du score, compté à part et relancé.
- **Coût d'un essai.**
  - Source principale : `cost_usd` dans `result.json`, rempli par le harness. Lesquels le remplissent est *à vérifier au J0*.
  - Si le champ est vide, `report.py` calcule tokens × prix de `routes/prix.yaml` (renseigné par toi) et marque la valeur « estimée ».
- **Données envoyées.** Seuls l'énoncé et le contenu de la tâche partent chez le fournisseur, jamais la réponse attendue. Pour une page ou un code non public, on vérifie avant envoi la politique de conservation du fournisseur OpenRouter retenu.

## 11. Rapport

`report.py` lit tous les `jobs/*/*/result.json` et les `run.json`. Il produit :

- **`results/summary.csv`**, une ligne par essai :
  - suite, version de la suite, tâche, lot ;
  - harness et sa version, modèle, route, fournisseur, effort, skills, numéro d'essai ;
  - toutes les clés de `reward.json` ;
  - tokens (entrée, cache, sortie), coût et marque « estimé », durée ;
  - erreur d'infrastructure.
- **`results/report-<suite>.md`**, un tableau par couple harness × modèle (× skills), avec :
  - le score moyen et son intervalle de confiance à 95 % (bootstrap sur les tâches) ;
  - l'écart entre essais ;
  - pass@k et pass^k pour la suite code ;
  - précision, rappel, hallucinations et fausses alertes pour le RGAA ;
  - le score OWASP pour la sécurité ;
  - le coût moyen par tâche, la durée médiane, le nombre d'erreurs d'infrastructure.
- **La liste des désaccords** (fausses alertes, erreurs manquées), à arbitrer avec l'experte ou un développeur.

`harbor view jobs` reste l'outil pour lire les trajectoires une à une. La lecture d'un échantillon de trajectoires avant de croire un score fait partie de chaque campagne.

## 12. Jalons

Chaque jalon a un critère de fin vérifiable. Aucune charge n'est estimée ici.

### J0. Socle et matrice de fumée

- Créer le repo privé, `pyproject.toml` avec Harbor épinglé, `Makefile`, `run.py`, `.env.example`, `routes/`, `suites/hello/`.
- Lancer `make smoke` pour chaque harness que tu comptes utiliser, sur chaque route, et consigner le résultat dans `results/compat.md`. Pour chaque combinaison, la matrice vérifie :
  - la tâche hello passe ;
  - `cost_usd` et les tokens sont remontés ;
  - le harness ne se bloque pas quand seul l'hôte du fournisseur est ouvert (télémétrie, mises à jour) ;
  - `curl https://github.com` échoue depuis la phase agent ;
  - le correcteur n'a pas de réseau.
- Lever les points « à vérifier » :
  - les variables Bedrock par harness ;
  - Claude Code avec un modèle non Anthropic via OpenRouter ;
  - l'épinglage du fournisseur OpenRouter ;
  - la commande de pré-collecte pour le patch de la suite code ;
  - la présence de nftables sur la machine hôte (exigée par la liste blanche réseau sous Docker).

**Fin** : `results/compat.md` rempli, et une ligne verte par combinaison retenue.

### J1. Suite RGAA

- Récupérer la référence remplie et les pages figées (prérequis de la section 6).
- Écrire `evalkit/schemas/findings-rgaa.schema.json`, `match_rgaa.py`, `build_rgaa.py`, `suites/rgaa/metric.py` et les tests unitaires du correcteur (cas : appariement, hallucination, fausse alerte, sélecteurs différents désignant le même élément, fichier invalide).
- Générer les tâches.

**Fin** : `make validate SUITE=rgaa` passe (oracle au maximum, nop à rappel nul, correcteur stable), puis un premier `make run`.

### J2. Rapport

- Écrire `report.py` et le format de `results/`.
- Ajouter `make regrade` et l'essayer après une modification de la référence.

**Fin** : `results/report-rgaa.md` produit à partir des runs du J1, et un regrade réussi.

### J3. Suite code

- Écrire `mine_prs.py`, `build_code.py`, les images épinglées et le correcteur.
- Retenir une première série de PR, chaque énoncé étant relu par un développeur de l'équipe concernée.

**Fin** : chaque tâche passe `make validate`, dont 3 passages de l'oracle sans test instable.

### J4. Suite sécurité

- Écrire `injections.yaml` (failles et leurres), `build_securite.py`, `match_securite.py`, `cwe_familles.yaml` et `metric.py`.

**Fin** : `make validate SUITE=securite` passe, et le score OWASP est calculé sur un premier run.

### J5. Extensions, dans l'ordre utile

- Lot caché (`llm-eval-cache`).
- Variante « rendu » du RGAA.
- Tests de bout en bout pour le front.
- Cas ACT et Asqatasun.
- CI qui lance `make validate` sur toute PR ajoutant ou modifiant une tâche. La CI ne lance jamais de campagne : les campagnes coûtent et restent manuelles.

## 13. Ce que `AGENTS.md` doit dire

Ces règles s'adressent à qui ajoute des tâches, humain ou agent :

1. Ne jamais modifier `suites/` à la main : corriger `sources/`, puis régénérer.
2. Toute nouvelle tâche passe `make validate` avant d'être commitée.
3. Ne jamais placer de réponse attendue, de solution ou d'historique futur dans `environment/`.
4. Toute modification d'un correcteur ou d'une référence incrémente la version de `dataset.toml` et s'accompagne d'un `make regrade` des runs existants.
5. Ne jamais commiter `.env`, ni `jobs/` en entier.
6. Les résultats publiés dans transfo-ia viennent de `results/`, jamais de `jobs/` (les trajectoires contiennent le contenu des tâches).

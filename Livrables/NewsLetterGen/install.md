# install.md — Essayer la veille JO gratuitement sur ce poste

> Guide pas à pas pour **Selim**, sur **ce poste Linux**. Objectif : faire tourner la solution
> complète sans rien payer. L'API PISTE est gratuite ; le volet IA passe soit par **openrouter**
> (voie d'essai déjà câblée et calibrée sur ce poste — données hors France, **dev uniquement**),
> soit par **Albert** (l'API souveraine DINUM/Etalab, gratuite pour les agents publics — sa clé
> est à régénérer), soit peut être laissé désactivé (pipeline 100 % déterministe).
>
> **Ce n'est plus une migration.** L'abstraction multi-fournisseurs (`mistral` / `albert` /
> `openrouter`) est **déjà dans le code** (`config.py`, `diagnostic.py`, `analyse.py`). Il n'y a
> donc plus de plan à exécuter ni d'agent à lancer : brancher une clé, choisir le fournisseur
> dans `.env`, lancer. Durée : ~15 min, dont l'essentiel côté compte PISTE.

## 0. Ce qui est déjà en place (vérifié le 22/07/2026)

| Prérequis | État sur ce poste |
|---|---|
| Python 3.10+ | ✅ Python 3.12 |
| git | ✅ |
| Projet `veille_jo/` (repo git, venv, tests hors ligne verts) | ✅ `NewsLetterGen/veille_jo/` |
| Multi-fournisseurs IA (`mistral`/`albert`/`openrouter`) | ✅ intégré au code, testé hors ligne |
| Voie d'essai `openrouter` | ✅ câblée, modèle `mistralai/mistral-large-2512` calibré le 21/07 |
| Clé Albert | ⚠️ **expirée depuis le 03/07/2026** (à régénérer, étape 2 option B) |
| OpenCode installé | ✅ `~/.opencode/bin/opencode` (facultatif : agent de dev gratuit, voir « Et après ? ») |

Rien à installer côté système. Il reste au plus 4 étapes, dans cet ordre.

---

## Étape 1 — Créer ton compte PISTE (gratuit, ~10 min, dans le navigateur)

C'est LA clé des runs réels du pipeline (extraction du JO, calibration, recette complète),
IA ou pas.

1. Va sur **https://piste.gouv.fr** → « Créer un compte » (email perso ou pro, au choix).
2. Une fois connecté : **créer une application** (nom libre, ex. `veille-jo-test`).
3. Dans l'application : **souscrire à l'API « Légifrance »** (catalogue des API, environnement
   de **production** — la souscription est gratuite, parfois validée sous quelques heures).
4. Récupère le couple **client ID / client secret** de l'application (onglet Applications →
   détails → identifiants OAuth).
5. Colle-les dans `veille_jo/.env` :

   ```bash
   cd ~/Documents/clients/ministeres-sociaux/Suivi_Mission/Livrables/NewsLetterGen/veille_jo
   nano .env    # PISTE_CLIENT_ID=...  et  PISTE_CLIENT_SECRET=...
   ```

6. Vérifie :

   ```bash
   .venv/bin/python diagnostic.py
   ```

   Attendu : `PISTE token : OK` et `PISTE API : OK — dernier JO : …`.
   (La ligne IA dépendra de l'étape 2 ; sans clé du fournisseur choisi, elle affichera
   « non testé », ce qui est normal.)

> Si la souscription Légifrance est en attente de validation, tu peux quand même faire l'étape 2 :
> seuls les runs réels du pipeline attendront.

## Étape 2 — Choisir et brancher le fournisseur IA

Le volet IA ne sert qu'à **recopier mot pour mot les indications thérapeutiques** ; tout le
reste (produits, laboratoires, listes, taux, liens, classement) vient du parsing déterministe.
Sans IA, seule la colonne Indication se dégrade en « à compléter manuellement ». Trois voies,
au choix — la surcharge se fait **par poste dans `.env`**, jamais en committant `config.py`.

### Option A — openrouter (voie d'essai immédiate, déjà calibrée)

Routeur commercial, **données hors France → essai de dev uniquement, jamais la production CEPS**.
Le modèle est déjà fixé dans `config.py` (`MODELE_IA_OPENROUTER = "mistralai/mistral-large-2512"`,
constaté le 21/07 = les poids de `mistral-large-latest`).

```bash
cd ~/Documents/clients/ministeres-sociaux/Suivi_Mission/Livrables/NewsLetterGen/veille_jo
nano .env    # OPENROUTER_API_KEY=<ta clé openrouter.ai>  et  FOURNISSEUR_IA=openrouter
.venv/bin/python diagnostic.py
```

Attendu : `IA (openrouter) : OK — modèle mistralai/mistral-large-2512 disponible`.

### Option B — Albert (souverain, gratuit — clé à régénérer)

API souveraine de l'État, gratuite pour les agents publics. Côté souveraineté : le pipeline
appelle Albert via le paquet Python `openai` utilisé comme **client générique d'API
OpenAI-compatible** — les requêtes ne partent que vers `albert.api.etalab.gouv.fr`, jamais vers
OpenAI. La clé du poste est **expirée depuis le 03/07/2026** : il faut la régénérer sur le portail où elle a été créée
([guides.ia.numerique.gouv.fr/albert-api](https://guides.ia.numerique.gouv.fr/albert-api)), puis :

```bash
nano .env    # ALBERT_API_KEY=<nouvelle clé>  et  FOURNISSEUR_IA=albert
```

Le modèle Albert n'est **pas** deviné : la liste `GET /v1/models` fait foi. Lance le diagnostic
une première fois pour la voir, choisis un modèle de génération de texte, reporte son id dans
`config.py` (`MODELE_IA_ALBERT`, avec la date de constat en commentaire), puis relance :

```bash
.venv/bin/python diagnostic.py    # la ligne IA liste des ids réels quand MODELE_IA_ALBERT est vide
# … reporter l'id choisi dans config.py, puis :
.venv/bin/python diagnostic.py    # attendu : IA (albert) : OK — modèle <id> disponible
```

Curiosité utile (quotas) : `curl -s -H "Authorization: Bearer $ALBERT_API_KEY" https://albert.api.etalab.gouv.fr/v1/me/info | python3 -m json.tool`.

### Option C — pas de clé (pipeline déterministe)

Laisser `IA_ACTIVE = True` mais aucune clé du fournisseur effectif dans `.env` (ou passer
`IA_ACTIVE = False` dans `config.py`) : le run tourne sans IA, indications « à compléter
manuellement ». Aucune étape 2 supplémentaire.

## Étape 3 — Tes premiers essais

1. **Banc IA seul** (aucune clé PISTE nécessaire ; texte collé à la main, jamais scrapé) :

   ```bash
   # colle d'abord un texte « spécialités pharmaceutiques » d'un JO récent (avis de prix ou
   # arrêté d'inscription) depuis legifrance.gouv.fr dans ../texte_test_jo.txt
   .venv/bin/python tests/tester_ia_reelle.py --fichier ../texte_test_jo.txt --titre "<titre exact du texte>"
   ```

   À vérifier : chaque indication **recopiée mot pour mot** (pas de reformulation), zéro
   « Appel IA en échec » dans le log. (C'est aussi le moment du constat `response_format` /
   essai `json_schema` pour Albert — voir `nextSteps.md` §3, entrée A5.2.)

2. **Pipeline complet sur la vérité terrain** (nécessite l'étape 1 validée) :

   ```bash
   .venv/bin/python main.py --date 2026-05-28
   .venv/bin/python tests/compare_cible.py sorties/veille_jo_2026-05-28.xlsx tests/fixtures/veille_jo_2026-05-28_CIBLE.xlsx
   ```

   La recette compare la **couverture par noms racines** (produits, laboratoires, listes, taux,
   liens) — l'Excel CIBLE historique reste la référence, plus le nombre de lignes (le contrat
   est passé à « une ligne par présentation » le 22/07). Le bloc « VOLET REVUE HUMAINE » liste
   les indications recopiées par l'IA à comparer à l'annexe E. Un écart résiduel subsiste tant
   que la **décision « orientation » des avis de prix** n'est pas tranchée (`nextSteps.md` §0 et
   entrée E7) : c'est attendu, pas un bug. Sorties dans `sorties/` (Excel + `corps_mail_….html`),
   journal dans `logs/`.

3. **Choisir la date sans ligne de commande** (interface utilisatrice du 22/07) : créer un
   fichier `date.txt` dans `veille_jo/` contenant une seule ligne au format **JJ-MM-AAAA**
   (ex. `28-05-2026`), puis lancer normalement. Le fichier est supprimé à la fin de chaque
   lancement ; date absente/invalide → repli sur la date du jour.

## Étape 4 — Veille du jour

JO publié vers 2h-3h du matin. Sur ce poste Linux, le lanceur est `lancer_veille.sh` :

```bash
cd ~/Documents/clients/ministeres-sociaux/Suivi_Mission/Livrables/NewsLetterGen/veille_jo
./lancer_veille.sh        # ou : .venv/bin/python main.py
```

(Le poste cible du CEPS est sous Windows : `lancer_veille.bat`, voir `README.md`.)

## Et après ?

- L'état complet du chantier et les actions restantes sont dans **`veille_jo/nextSteps.md`**
  (§0 : la liste ordonnée avec cases à cocher).
- **Question de production à faire trancher** (`nextSteps.md` §2, ligne `FOURNISSEUR_IA`) :
  Albert est souverain, gratuit et sur un flux `.gouv.fr` — il remplirait l'exigence « données
  en France » mieux que le Mistral payant prévu par défaut, **sans achat public**. Si
  l'utilisatrice/DSI valide, une clé Albert au nom du service CEPS devient le défaut committé
  et la veille ne coûte plus rien en production. openrouter, lui, ne va **jamais** en production
  (données hors France).
- **OpenCode (facultatif, non configuré à ce jour)** : agent de dev en ligne de commande, installé
  sur ce poste (`~/.opencode/bin/opencode`), qui pourrait tourner gratuitement sur la même clé
  Albert. Utile pour la maintenance, pas nécessaire à la veille. Pour l'activer : compléter
  `~/.config/opencode/opencode.jsonc` (aujourd'hui réduit à sa seule ligne `$schema`) avec un
  provider `albert` (`baseURL` `https://albert.api.etalab.gouv.fr/v1`, `apiKey {env:ALBERT_API_KEY}`),
  puis exporter `ALBERT_API_KEY` dans `~/.bashrc`. Voir `nextSteps.md` §0, action 7.
- En cas de panne : `README.md` du projet, section « Pannes courantes ».

# Spécification d'implémentation : automatisation de la veille JO — spécialités pharmaceutiques

**Version** : 2.0 — 20 juillet 2026. Spécification exécutable par un agent LLM. Chaque point de risque a une **Option A (nominale)** et une **Option B (sans risque)** ; le parcours B intégral est récapitulé au §9.
**Contexte** : CEPS. Une interne en pharmacie produit chaque matin une newsletter de veille du Journal officiel (spécialités pharmaceutiques) : tableaux synthétiques + Excel. Deux scripts existants (Test_piste4/5) réalisent une partie du pipeline mais sont bloqués (timeouts IA) et non rejouables (IDs codés en dur). Objectif : pipeline quotidien fiable, rejouable par date, reproductible par un agent non développeur. Le besoin original est reproduit verbatim en **annexe G**.

**Kit de transmission à l'agent exécutant** (tout tient dans le dossier `NewsLetterGen/`) :

- ce fichier — la spec se suffit pour l'intention (besoin original en annexe G, vérité terrain en annexe E) ;
- `docs/veille_jo_2026-05-28_CIBLE.xlsx` — **indispensable** : fixture de la recette automatisée (E7) ;
- `docs/[VEILLE] - Publication JO du 28052026` (mail .eml) — recommandé : gabarit exact du corps de mail (E8) ;
- `docs/test_piste4_Anonym.docx`, `docs/test_piste5_Anonym.docx`, `docs/veille_jo_2026-05-28.xlsx` — optionnels : déjà dépouillés, tout ce qui en est utile (endpoints, payloads, mécanique Excel, erreurs constatées) est intégré à cette spec.

---

## 1. Instructions à l'agent exécutant

1. Réalise les étapes **E0 à E10 dans l'ordre** (§6). Chaque étape a un critère « **Terminé quand** » : exécute la validation avant de passer à la suivante.
2. La **vérité terrain** est l'annexe E (JO du 28/05/2026) et les fichiers du dossier `docs/` (Excel cible, newsletter). En cas de conflit entre cette spec et ces fichiers, les fichiers font foi ; signale l'écart. En cas de doute sur l'intention, le besoin original (annexe G) prime.
3. **Ne jamais inventer de valeur.** Toute donnée introuvable = `"N/A"` ou champ vide + mention « à vérifier manuellement » dans la sortie et le log. Jamais de valeur par défaut silencieuse.
4. **Interdits** : IDs JORFTEXT codés en dur ; reformulation des indications ; envoi des annexes tarifaires à l'IA ; clés API en dur (uniquement `.env`) ; scraping de legifrance.gouv.fr (API PISTE uniquement) ; `.Send()` d'un mail sans validation humaine explicite.
5. Demande à l'utilisateur les valeurs de `.env` et ses choix A/B au moment de E0. **S'il ne les a pas, ne bloque pas** : applique la configuration recommandée du §3.1, laisse les variables de `.env` vides et consigne leur obtention dans `nextSteps.md`.
6. **`nextSteps.md` est un registre vivant** (§4.5) : toute validation impossible faute de clé, de flux ou de poste Windows est consignée au moment où elle est sautée, avec la commande exacte à rejouer et le résultat attendu. Une validation sautée sans entrée correspondante est une faute d'implémentation.
7. Code : Python 3.10+, fonctions courtes, docstrings en français, aucun framework. L'utilisatrice finale lance le tout depuis VS Code ou un `.bat`.

---

## 2. Principe d'architecture : déterministe d'abord, IA en enrichissement

Constat sur les pièces réelles : la sortie cible ne contient **aucune donnée tarifaire** (la colonne « Prix » est un simple hyperlien vers l'avis, la colonne « Taux » une valeur + lien vers la décision UNCAM). L'essentiel de la cible (produits, laboratoires, listes, liens, taux, classement) est donc extractible **sans IA**, par classification des titres et parsing des tableaux HTML de l'API. L'IA n'apporte que : la recopie exacte des indications, et la levée d'ambiguïtés de classification.

Conséquences :

- le pipeline déterministe est **toujours** exécuté et fait foi pour : produits, laboratoires, taux, liens, classement ;
- l'IA (Option A) enrichit : indication exacte, confirmation du type de texte ; elle reçoit des textes **nettoyés et courts** (visas, considérants et colonnes tarifaires supprimés), ce qui traite la cause racine des timeouts historiques (envoi d'annexes tarifaires entières à l'API Mammouth.ai) ;
- `ia_active = false` (Option B) donne un pipeline complet où seule la colonne Indication est marquée « à compléter manuellement ».

```
[Planificateur 7h00  |  B : double-clic .bat]
        │
        ▼
1. EXTRACTION      OAuth2 PISTE → sommaire JORF de la date → textes intégraux
        ▼
2. FILTRAGE        mots-clés pharma sur les titres (arrêtés + avis + décisions UNCAM)
        ▼
3. ANALYSE DÉTERMINISTE   classification par titre + parsing tableaux HTML + taux par regex
        ▼
4. ANALYSE IA (Option A)  Mistral : indications exactes + ambiguïtés   [B : sautée]
        ▼
5. RAPPROCHEMENT   1 ligne par produit racine : Liste ← arrêtés, Prix ← avis, Taux ← décision UNCAM
        ├────────► 6a. EXPORT EXCEL (openpyxl, format cible)
        ▼
6b. NOTIFICATION   HTML format newsletter → brouillon Outlook (A) | fichier HTML (B)
```

Charge indicative : 5 à 8 jours (E0-E1 : ½ j ; E2-E7 : 2-3 j ; E8-E9 : 1 j ; E10 : 1 j).

---

## 3. Points de risque et bascules A/B

| # | Point de risque | Option A (nominale) | Option B (sans risque) | Bascule |
|---|---|---|---|---|
| R1 | `api.mistral.ai` bloqué par le proxy ministériel, compte payant impossible, ou récidive des timeouts | IA Mistral La Plateforme (§6 E4) | Pipeline 100 % déterministe, indication « à compléter manuellement » | `config.ia_active = False` |
| R2 | Automatisation Outlook (win32com) interdite ou Outlook absent | Brouillon Outlook pré-rempli (`.Display()`) | Fichier `corps_mail_<date>.html` ouvert dans le navigateur, copier-coller dans un nouveau mail (c'est le besoin initial exprimé) | `config.mail_mode = "html"` |
| R3 | Envoi 100 % automatique jugé risqué | `.Send()` après période de confiance | Rester au brouillon (relecture 30 s puis clic Envoyer) | `config.envoi_automatique = False` (défaut) |
| R4 | Planificateur de tâches verrouillé par la DSI | Tâche quotidienne 7h00, relance sur échec | Raccourci `lancer_veille.bat` sur le bureau, double-clic en arrivant | fichier `.bat` fourni dans les deux cas |
| R5 | Pas de GitLab interne accessible | Dépôt distant GitLab ministère | Dépôt git local + copie datée du dossier sur le partage réseau d'équipe | — |
| R6 | Police Marianne absente du poste | Marianne | Arial (openpyxl ne fait que référencer la police : aucune erreur, juste un rendu différent) | `config.police = "Arial"` |

Les options A et B **coexistent dans le code** derrière ces clés de config : implémenter les deux dans tous les cas.

### 3.1 Configuration recommandée (défauts à livrer si l'utilisateur ne tranche pas en E0)

« Choisir » ne fixe que les défauts de `config.py` et l'ordre de mise en service :

- **`IA_ACTIVE = True`** (R1) : c'est le besoin exprimé (indications exactes). La dégradation est automatique et sans danger : clé absente ou API injoignable → le run aboutit quand même, indications « à compléter manuellement », soit exactement le plan B sans intervention. Clé absente = traité comme `IA_ACTIVE = False` pour le run (log explicite, aucune tentative inutile).
- **`MAIL_MODE = "brouillon_outlook"`** (R2) : meilleure expérience cible (zéro copier-coller, contrôle humain conservé), avec repli automatique sur le fichier HTML — toujours écrit de toute façon — si Outlook/COM refuse.
- **`ENVOI_AUTOMATIQUE = False`** (R3) : ne passer à `True` qu'après plusieurs semaines de brouillons irréprochables, à la demande de l'utilisatrice.
- **Planification progressive** (R4) : semaine 1 en `lancer_veille.bat` (double-clic, résultats observés), puis tâche planifiée 7h00 une fois la recette E10 signée. Les deux artefacts sont livrés dès E9.
- **Git local + copie réseau** (R5) : aucun GitLab interne identifié à ce jour.
- **`POLICE = "Marianne"`** (R6) : simple référence de nom, repli de rendu automatique par Excel si la police est absente du poste.

---

## 4. Architecture, configuration, secrets

### 4.1 Arborescence à créer

```
veille_jo/
├── main.py               # orchestration ; --date AAAA-MM-JJ (défaut : aujourd'hui) ; exit code 0 si OK/RAS, 1 si échec
├── config.py             # toutes les constantes ci-dessous
├── diagnostic.py         # python -m diagnostic : teste token PISTE, un appel API, joignabilité api.mistral.ai → OK/KO par flux
├── extraction.py         # OAuth2 + sommaire JORF + textes intégraux
├── filtrage.py           # sélection des textes pharma par mots-clés
├── analyse.py            # nettoyage, classification par titre, parsing tableaux HTML, taux regex, appels IA (si ia_active)
├── rapprochement.py      # consolidation 1 ligne par produit racine
├── export.py             # Excel openpyxl au format cible
├── notification.py       # corps HTML + brouillon Outlook / fichier HTML
├── prompts/analyse_texte.txt   # annexe A, versionnée hors code
├── tests/
│   ├── compare_cible.py  # diff automatisé produit vs cible (§6 E7)
│   └── fixtures/         # copie de docs/veille_jo_2026-05-28_CIBLE.xlsx
├── logs/                 # un fichier par exécution : veille_AAAA-MM-JJ_HHMMSS.log
├── sorties/              # veille_jo_AAAA-MM-JJ.xlsx + corps_mail_AAAA-MM-JJ.html
├── lancer_veille.bat     # cd /d %~dp0 && .venv\Scripts\python.exe main.py (+ pause en fin)
├── .env.example          # noms de variables, valeurs vides
├── .gitignore            # .env, logs/, sorties/, .venv/
├── requirements.txt
├── README.md             # §6 E10
└── nextSteps.md          # registre vivant de fin de chantier (§4.5)
```

### 4.2 `requirements.txt`

```
requests
python-dotenv
pydantic>=2
openpyxl
beautifulsoup4
mistralai        # utilisé seulement si ia_active
pywin32 ; sys_platform == 'win32'   # utilisé seulement si mail_mode == "brouillon_outlook"
```

Les imports de `mistralai` et `win32com` sont **locaux aux fonctions** qui les utilisent : le pipeline B tourne sans ces dépendances installées.

### 4.3 `config.py` (contenu exact de départ)

```python
# --- Bascules A/B (voir §3 du plan) ---
IA_ACTIVE = True                       # R1 : False = pipeline 100 % déterministe
MAIL_MODE = "brouillon_outlook"        # R2 : "brouillon_outlook" | "html"
ENVOI_AUTOMATIQUE = False              # R3 : True seulement après période de confiance
POLICE = "Marianne"                    # R6 : "Arial" si Marianne absente

# --- PISTE / Légifrance ---
URL_TOKEN     = "https://oauth.piste.gouv.fr/api/oauth/token"
URL_LAST_JO   = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/consult/lastNJo"
URL_JORF_CONT = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/consult/jorfCont"
URL_JORF_TEXT = "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/consult/jorf"
NB_ELEMENT_LASTNJO = 60                # profondeur de rejeu (~2 mois) ; augmenter pour rejouer plus ancien

# --- Filtrage (mots-clés éprouvés sur les scripts existants, insensibles à la casse) ---
MOTS_CLES = ["pharmaceutique", "spécialité", "médicament", "prix de spécialité",
             "avis de tarification", "baisse de prix", "participation de l'assuré", "majoration"]

# --- IA ---
MODELE_IA = "mistral-small-latest"     # monter à mistral-large-latest seulement si la recette E7 échoue sur la qualité
TIMEOUT_IA_S = 120
TENTATIVES_IA = 3                      # backoff 2 s, 8 s, 30 s
SEUIL_DECOUPAGE = 15000                # caractères ; au-delà, découper par article et fusionner

# --- Mail ---
DESTINATAIRES = ["ListediffusionSG_CEPS@canauxteams.social.gouv.fr"]
OBJET_MAIL = "[VEILLE] - Publication JO du {date_jjmmaaaa}"
```

### 4.4 `.env` (jamais commité)

```
PISTE_CLIENT_ID=
PISTE_CLIENT_SECRET=
MISTRAL_API_KEY=          # peut rester vide si IA_ACTIVE = False
```

Les scripts historiques contenaient les clés en dur (anonymisées à la main avant partage) : c'est précisément ce que `.env` supprime.

### 4.5 `nextSteps.md` — registre vivant de fin de chantier

Créé dès E0, complété à chaque validation sautée, livré complet en fin de mission. Il doit être **autoportant** : une personne qui ne connaît ni cette spec ni la session d'implémentation doit pouvoir finir le chantier avec ce seul fichier. Structure imposée :

1. **Secrets à obtenir** : pour chaque variable de `.env` — où l'obtenir (PISTE : compte sur piste.gouv.fr, application avec souscription à l'API Légifrance, récupérer client id/secret ; Mistral : console La Plateforme, compte pay-as-you-go, clé dédiée à la veille), où la placer, comment vérifier (`python diagnostic.py`).
2. **Décisions A/B à confirmer** : bascules livrées en configuration recommandée (§3.1) + pour chacune, la question à poser à l'utilisatrice et l'endroit où changer la valeur.
3. **Validations en attente** : tableau (étape de la spec → ce qui n'a pas pu être vérifié → commande exacte à rejouer → résultat attendu, en recopiant le « Terminé quand »). Typiquement : runs réels E1-E5 sur le 28/05/2026, recette stricte E7, volet indications (validation humaine), brouillon Outlook et planification sur le poste Windows, recette 3 dates de E10.
4. **Démarches externes** : demande DSI d'ouverture de flux vers `api.mistral.ai` si le diagnostic la révèle nécessaire, droits d'envoi sur la liste de diffusion, etc.
5. **Checklist de première exécution chez l'utilisatrice** : pas à pas, de l'installation (5 commandes du README) au premier brouillon de mail obtenu.

---

## 5. Contrat de sortie (à respecter au caractère près)

### 5.1 Excel `sorties/veille_jo_AAAA-MM-JJ.xlsx`

Un onglet unique `Veille`. Colonne A vide (largeur 3), sections à partir de la colonne B, **une ligne vide entre sections**, sections **omises si vides**. Pour chaque section : ligne de titre fusionnée sur toute la largeur (hauteur 20, fond couleur section, gras, centré), ligne d'en-têtes (gras, bordure basse noire), lignes de données (bordures fines `BFBFBF`, produit en gras couleur `3A3A3A`, cellules centrées sauf Date et Indication alignées à gauche, Indication en retour à la ligne automatique). Police : `config.POLICE`, taille 11 (titres 12).

| Section (titre exact) | Fond | Colonnes (largeurs) |
|---|---|---|
| `Nouvelles inscription` | `F2CEED` (rose) | Date (12), Produit (35), Laboratoire (18), Indication (80), Liste (20), Prix (14), Taux (10) |
| `Hausses de prix` | `F6C5AC` (orange) | Date (12), Produit (35), Laboratoire (18), Prix (25) |
| `Baisses de prix` | `C1F0C7` (vert) | Date (12), Produit (35), Laboratoire (18), Prix (25) |
| `Extensions d'indications` | `D1D6FF` (bleu) | Date (12), Produit (35), Laboratoire (18), Indication (80), Lien (25) |

Le singulier « Nouvelles inscription » est voulu : c'est le gabarit de l'utilisatrice (cible et newsletter). Le format « Extensions » est hérité des scripts (jamais observé dans une cible réelle) : à valider à la première occurrence.

Contenu des cellules :

- **Date** : vraie date Excel (datetime), format d'affichage `DD/MM/YYYY` ;
- **Produit** : nom racine normalisé (annexe C), majuscules ;
- **Prix** : hyperlien vers l'avis de prix, texte affiché exactement `Site LégiFrance`, police couleur `0000FF` soulignée ; si aucun avis rattaché : texte `N/A` sans lien ;
- **Taux** : valeur texte (ex. `0.35`) portant un hyperlien vers la décision UNCAM ; si absent : `N/A` sans lien — ne jamais déduire un taux ;
- **Liste** : `LES`, `Collectivité` ou `SS et Collectivité` ;
- toute donnée douteuse : suffixe ` (à vérifier)` + entrée dans le récapitulatif d'anomalies.

### 5.2 Mail (HTML) — ce n'est PAS l'Excel

Structure exacte (calquée sur la newsletter du 28/05/2026) :

1. `Bonjour,` puis ligne vide puis `Veuillez trouver ci-dessous la publication du JO de ce jour :`
2. Tableau `Nouvelles inscription` (bandeau `F2CEED`) : colonnes **Produit, Laboratoire, Indication, Liste, Prix, Taux** — **pas de colonne Date**. Cellule Prix : lien texte `Site LégiFrance`. Cellule Taux : lien dont le texte est le pourcentage entier, ex. `35%` (conversion `0.35 → 35%`) ; `N/A` sans lien sinon.
3. Tableau `Hausse de prix` (bandeau `F6C5AC`, **singulier**) : Produit, Laboratoire, Prix (lien `Site LégiFrance`).
4. Tableau `Baisse de prix` (bandeau `C1F0C7`, **singulier**) : mêmes colonnes.
5. Sections vides omises. Si aucun texte pertinent ce jour : corps = `RAS — aucun texte relatif aux spécialités pharmaceutiques au JO du JJ/MM/AAAA.` (le mail part quand même : l'absence de mail signifie « panne », jamais « rien à signaler »).
6. `Cordialement,` (la signature Outlook de l'utilisatrice s'ajoute d'elle-même au brouillon).
7. Récapitulatif d'anomalies le cas échéant (textes non analysés avec leur lien Légifrance, lignes « à vérifier »).

Tables HTML avec bordures fines, en-têtes gras centrés, mêmes codes couleur que l'Excel. Objet du mail : `config.OBJET_MAIL`. Pièce jointe : l'Excel du jour.

---

## 6. Étapes d'implémentation

> **Règle « sans clés »** : tant que les clés PISTE/Mistral manquent, les « Terminé quand » exigeant un run réel (E1 à E5, volet strict de E7 sur run réel, E9) basculent en « implémenté + testé hors ligne + entrée dans `nextSteps.md` ». Pour tester E6-E8 hors ligne : construire une fixture Python des 8 lignes consolidées de l'annexe E et l'injecter en entrée d'`export.py`, `compare_cible.py` et `notification.py` — export, diff et rendu mail se valident ainsi sans réseau.

### E0 — Environnement et flux (½ journée)

1. Créer l'arborescence §4.1 (y compris `nextSteps.md`, §4.5), `python -m venv .venv`, installer `requirements.txt`, initialiser git, créer `.env` (demander les valeurs à l'utilisateur ; absentes → variables vides, entrée « Secrets à obtenir » dans `nextSteps.md`, et poursuivre).
2. Écrire `diagnostic.py` : (a) obtention token PISTE, (b) appel `lastNJo` à 1 élément, (c) si `IA_ACTIVE`, requête de liste des modèles Mistral. Sortie lisible : `PISTE token: OK/KO`, `PISTE API: OK/KO`, `Mistral: OK/KO/non testé (IA_ACTIVE=False)`.
3. **R1** : si Mistral KO (proxy ministériel probable) : basculer `IA_ACTIVE = False` (le pipeline reste entièrement fonctionnel, §2) et signaler à l'utilisateur qu'une demande d'ouverture de flux DSI permettra de réactiver l'option A plus tard. Côté compte : Mistral La Plateforme en pay-as-you-go (quelques euros/mois au volume attendu) ; **l'abonnement Mammouth.ai des scripts historiques n'est plus utilisé** (agrégateur à abonnement, fallback GPT-4o contraire à l'exigence « données en France », timeouts subis sur cette API).

**Terminé quand** : `python diagnostic.py` affiche OK pour chaque flux actif — ou son KO/non-testé est consigné dans `nextSteps.md` avec la procédure d'obtention ; `pip freeze` cohérent ; `git log` montre un premier commit sans `.env`.

### E1 — `extraction.py`

Reprendre les appels éprouvés des scripts existants :

- **Token** : `POST URL_TOKEN`, corps form-url-encoded `grant_type=client_credentials`, `client_id`, `client_secret`, `scope=openid` → `access_token` (validité ~1 h). Encapsuler dans une classe/fonction qui re-demande le token sur réponse 401.
- **Sommaire** : `POST URL_LAST_JO` json `{"nbElement": NB_ELEMENT_LASTNJO}` → `containers[]`, chacun `{id, titre, datePubli}` (`datePubli` en millisecondes epoch : comparer `datetime.fromtimestamp(ms/1000).date()` à la date cible). Puis `POST URL_JORF_CONT` json `{"id": <id du JO>}` → arbre du sommaire.
- **Textes** : parcours récursif de l'arbre ; chaque nœud avec `id` commençant par `JORFTEXT` est un texte, titre dans `titre` ou `title`. Texte intégral : `POST URL_JORF_TEXT` json `{"textCid": <id>}` ; concaténer les champs texte trouvés récursivement parmi `['content','html','texte','text','visa','notice','texteSource']` (chaînes > 20 caractères, dédupliquées en conservant l'ordre).
- Timeout 30 s et 3 tentatives (backoff 2 s) sur chaque appel PISTE. URL publique d'un texte : `https://www.legifrance.gouv.fr/jorf/id/<JORFTEXT...>`.

**Terminé quand** : `python main.py --date 2026-05-28` (pipeline partiel) logue le JO trouvé et le nombre de textes du sommaire ; une date sans JO (ex. un dimanche) logue « JO introuvable » proprement, exit code 1.

### E2 — `filtrage.py` + calibration

- Retenir les textes dont le titre contient l'un des `MOTS_CLES` (insensible à la casse). La veille couvre **arrêtés + avis + décisions UNCAM**, pas seulement les arrêtés.
- Journaliser deux listes : retenus et écartés (titre + id), pour audit du filtre.
- **Calibration obligatoire** : exécuter sur le 28/05/2026 et vérifier que les retenus incluent les 11 textes de la vérité terrain (annexe E). Ajuster les mots-clés si besoin et consigner les titres réels observés en commentaire de `config.py` (les motifs de titres du JO sont stables mais doivent être constatés, pas supposés).

**Terminé quand** : sur `--date 2026-05-28`, les 11 JORFTEXT de l'annexe E figurent dans les retenus, et le log liste les écartés.

### E3 — `analyse.py`, volet déterministe (toujours exécuté)

1. **Nettoyage** de chaque texte retenu : suppression des visas (`Vu ...`) et considérants ; extraction séparée des tableaux HTML (`<table>`) via BeautifulSoup ; suppression du HTML résiduel.
2. **Classification par titre** (regex insensibles à la casse, calibrées en E2) vers l'un des types : `arrete_inscription_ss` (liste des spécialités remboursables aux assurés sociaux), `arrete_inscription_collectivites` (agréées aux collectivités), `avis_prix`, `decision_taux` (taux de participation de l'assuré), `avis_hausse_prix` (majoration), `avis_baisse_prix` (baisse), `extension_indication`, `autre`. Si le titre ne suffit pas pour le sens hausse/baisse d'un avis de prix : chercher `majoration|majoré` vs `baisse|diminué` dans le corps ; sinon type `avis_prix` non orienté → l'IA tranchera (A) ou la ligne sortira « à vérifier » (B). **Jamais de défaut silencieux** (le routage par défaut en « baisse » de piste4 avait classé la hausse MORPHINE dans le mauvais tableau).
3. **Parsing des tableaux** : extraire les colonnes de dénomination (nom de spécialité, laboratoire) ; **ignorer les colonnes tarifaires (prix, CIP)** : la cible n'en a pas besoin. Pour une `decision_taux` : associer à chaque dénomination le taux trouvé par regex `(\d{1,3})\s*%` (→ chaîne décimale `"0.35"`).
4. Produire pour chaque texte un objet : `{id, url, type_texte, produits: [{denomination_brute, laboratoire, taux?}], texte_nettoye}`.

**Terminé quand** : sur le 28/05, chaque texte de l'annexe E reçoit le bon `type_texte` et ses produits bruts ; le log montre pour chaque texte la taille avant/après nettoyage (après : quelques milliers de caractères, pas des dizaines).

### E4 — `analyse.py`, volet IA (Option A ; sauté si `IA_ACTIVE = False`)

- SDK `mistralai`, modèle `MODELE_IA` **fixé en config** (supprimer toute détection dynamique de modèle héritée de Mammouth, y compris le fallback GPT-4o), `temperature=0`, `response_format={"type":"json_object"}`, timeout `TIMEOUT_IA_S`, `TENTATIVES_IA` tentatives à backoff exponentiel (2 s, 8 s, 30 s).
- Un appel par texte, prompt = annexe A (fichier `prompts/analyse_texte.txt`), avec le `type_texte` déterministe passé en contexte. L'IA reçoit le **texte nettoyé** (jamais les colonnes tarifaires) ; au-delà de `SEUIL_DECOUPAGE`, découper par article et fusionner les listes de médicaments.
- **Validation Pydantic** (annexe B) de chaque réponse. JSON invalide → une relance unique avec l'erreur en contexte ; nouvel échec → conserver les données déterministes du texte et marquer ses lignes « à vérifier » (le run ne s'arrête jamais pour ça).
- Rôle des réponses IA : fournir `indication` (recopie exacte) et confirmer `type_texte`/`liste`. En cas de conflit avec le déterministe sur produit/taux/type, **le déterministe gagne** et le conflit est logué.

**Terminé quand** : sur le 28/05, les 6 produits de « Nouvelles inscription » ont une indication non reformulée (comparer à l'annexe E : texte exact, élisions admises), aucune indication inventée pour un texte qui n'en mentionne pas, zéro timeout sur le run complet.

### E5 — `rapprochement.py` (cœur du besoin, remplace les IDs codés en dur)

Entrée : la liste des objets par texte (E3/E4). Algorithme :

1. **Nom racine** de chaque dénomination (annexe C) : c'est la clé de regroupement (`LIKOZAM 1 mg/ml, sirop` et `LIKOZAM 2 mg` → `LIKOZAM` ; `MORPHINE AGUETTANT 10 ml` → `MORPHINE`).
2. Grouper toutes les occurrences par nom racine. Un même avis couvrant plusieurs produits alimente chaque ligne (au 28/05, DABIGATRAN et OXAZEPAM partagent le même avis de prix et la même décision de taux).
3. Remplir la ligne consolidée par type de texte source :
   - `arrete_inscription_ss` → Liste = `LES` ; `arrete_inscription_collectivites` → Liste = `Collectivité` ; les deux → `SS et Collectivité` (fusion **après** regroupement par racine : l'écart LIKOZAM `LES` vs `SS et Collectivité` venait d'une fusion faite avant normalisation) ;
   - `avis_prix` (orienté ou non) → hyperlien de la colonne Prix ;
   - `decision_taux` → valeur + hyperlien de la colonne Taux ;
   - laboratoire : via le mapping unique de l'annexe D (l'écart `CHAIX ET DU MARAIS` vs `LAVOISIER - CHAIX ET DU MARAIS` venait de deux mappings divergents entre scripts) ; indication : celle de l'IA si présente, sinon vide (B : `à compléter manuellement`).
4. **Section finale** de la ligne : inscription si un arrêté d'inscription la vise (priorité), sinon extension, sinon hausse, sinon baisse ; un avis de prix non orienté sans inscription associée → ligne « à vérifier » en Hausses **et** signalée dans le récapitulatif.
5. Loguer chaque rapprochement : `racine ← [liste des JORFTEXT contributeurs et leur rôle]`.

**Terminé quand** : sur le 28/05, exactement 8 lignes consolidées : 6 en Nouvelles inscription (WEGOVY, MOUNJARO, VGENFLI, DABIGATRAN, OXAZEPAM, LIKOZAM), 1 en Hausses (MORPHINE), 1 en Baisses (FYCOMPA), avec les liens de l'annexe E — ni doublon par présentation, ni section manquante.

### E6 — `export.py`

Implémenter le contrat §5.1 avec openpyxl. Le contrat suffit pour coder de zéro ; si `docs/test_piste5_Anonym.docx` est fourni, sa fonction `dessiner_section` (saine) peut servir de base, en corrigeant : date en vraie date (pas une chaîne), titre `Nouvelles inscription` au singulier, hyperlien + valeur sur la colonne Taux, gestion `PermissionError` (fichier ouvert → suffixe horaire).

**Terminé quand** : le fichier du 28/05 s'ouvre sans avertissement Excel/LibreOffice et passe E7.

### E7 — `tests/compare_cible.py` (recette automatisée)

Script qui compare deux xlsx et rend un verdict en deux volets :

- **Volet strict (doit être identique)** : sections présentes et leur ordre ; par section, l'ensemble des produits (comparaison sur nom racine, espaces insécables et espaces de fin ignorés) ; laboratoire, liste, valeur de taux ; **cibles des hyperliens** Prix et Taux ; date. Différence → `ÉCART` + sortie détaillée, exit code 1.
- **Volet revue humaine (listé, jamais bloquant)** : la colonne Indication. La cible contient des raccourcis de jugement humain non exigibles d'un traitement automatique (`Idem que PRADAXA` pour DABIGATRAN, indication laissée vide pour MOUNJARO, coquilles) : le script affiche côte à côte cible vs généré et l'humain tranche.

**Terminé quand** : `python tests/compare_cible.py sorties/veille_jo_2026-05-28.xlsx tests/fixtures/veille_jo_2026-05-28_CIBLE.xlsx` → `CONFORME` au volet strict, et l'utilisatrice a validé le volet indications (à lui faire confirmer explicitement, y compris la règle « recopie exacte, pas de raccourcis manuels »).

### E8 — `notification.py`

Implémenter le contrat §5.2 depuis les données consolidées (jamais en relisant l'Excel).

- **Option A (`mail_mode = "brouillon_outlook"`)** : via `win32com.client.Dispatch("Outlook.Application")`, créer un mail, `To` = `DESTINATAIRES`, objet, `HTMLBody` (insérer le HTML **avant** la signature existante), joindre l'Excel, puis `.Display()` — jamais `.Send()` sauf si `ENVOI_AUTOMATIQUE = True` (R3, après période de confiance).
- **Option B (`mail_mode = "html"`)** : écrire `sorties/corps_mail_<date>.html` et l'ouvrir dans le navigateur par défaut (`webbrowser.open`) ; l'utilisatrice copie-colle dans un nouveau mail. Toujours écrire ce fichier, même en option A (mode dégradé permanent).
- Si l'étape mail échoue (Outlook fermé, COM refusé…), le run reste en succès : l'Excel et le HTML sont dans `sorties/` et le log le dit clairement.

**Terminé quand** : sur le 28/05, le HTML reproduit la newsletter (mêmes tableaux, `35%` cliquable, singuliers respectés) ; en A, le brouillon s'affiche pré-rempli avec pièce jointe.

### E9 — Planification et garde-fous

- **Option A (R4)** : tâche du Planificateur Windows, jours ouvrés 7h00 (JO publié vers 2h-3h), « exécuter même si l'utilisateur n'est pas connecté », relance automatique en cas d'échec (30 min, 3 fois) — `main.py` sort en code 1 sur échec pour déclencher la relance. Fournir la commande `schtasks` prête à l'emploi dans le README.
- **Option B (R4)** : `lancer_veille.bat` sur le bureau, double-clic le matin (fenêtre console avec `pause` finale pour lire le résultat).
- Garde-fous communs : JO introuvable ou PISTE indisponible après relances → mail/brouillon d'alerte explicite ; jour sans texte pertinent → mail « RAS » (§5.2.5) ; échec partiel sur un texte → le mail part avec le récapitulatif d'anomalies et les liens Légifrance des textes non traités.

**Terminé quand** : un run planifié (ou .bat) complet s'exécute sans intervention sur une date récente, et un run sur une date sans JO produit l'alerte attendue.

### E10 — README et passation (reproductibilité)

README rédigé pour un agent non développeur : installation en 5 commandes ; où obtenir les clés PISTE (compte piste.gouv.fr) et Mistral, où les mettre, quoi faire à expiration ; usage (`python main.py`, `--date`, le `.bat`) ; où sont sorties et logs ; **fiche des 4 pannes courantes** (token PISTE expiré/compte désactivé, crédit Mistral épuisé → basculer `IA_ACTIVE=False` en attendant, JO pas encore publié, proxy bloquant `api.mistral.ai` → Option B) ; tableau des bascules A/B du §3.

Recette finale sur 3 dates : 28/05/2026 (E7), une date sans texte pertinent (mail RAS), une date à grosse annexe tarifaire (zéro timeout, payloads réduits au log). Passation : une heure, la personne déroule le README **seule**, on consigne tout point d'achoppement dans le README.

**Terminé quand** : recette signée sur les 3 dates, une personne autonome en plus de l'utilisatrice actuelle, et `nextSteps.md` à jour — idéalement vidé de ses validations en attente ; sinon, chaque entrée restante est autoportante.

---

## 7. Vérité terrain — JO du 28/05/2026 (annexe E, à utiliser pour E2-E7)

**Nouvelles inscription** (6 lignes) :

| Produit | Laboratoire | Liste | Lien Prix (JORFTEXT…) | Taux | Lien Taux (JORFTEXT…) | Indication attendue (volet humain) |
|---|---|---|---|---|---|---|
| WEGOVY | NOVO NORDISK | SS et Collectivité | 000054144866 | 0.35 | 000054144868 | « Chez l'adulte en cas d'échec de la prise en charge nutritionnelle bien conduite […] pour la gestion du poids, incluant la perte de poids et le maintien du poids » |
| MOUNJARO | LILLY | SS et Collectivité | 000054144870 | 0.35 | 000054144872 | (vide dans la cible) |
| VGENFLI | FRESENIUS KABI | SS et Collectivité | 000054144856 | N/A | — | « DMLA, Occlusion veineuse centrale de la rétine, Occlusion de branche veineuse rétinienne, Œdème maculaire diabétique, Néovascularisation choroïdienne » |
| DABIGATRAN | TEVA SANTE | SS et Collectivité | 000054144858 | 0.35 | 000054144860 | « Idem que PRADAXA » (raccourci humain, non exigible) |
| OXAZEPAM | ARROW | SS et Collectivité | 000054144858 | 0.35 | 000054144860 | « Traitement symptomatique des manifestations anxieuses sévères et/ou invalidantes / Prévention et traitement du delirium tremens et des autres manifestations de sevrage alcoolique. » |
| LIKOZAM | ADVICENNE | SS et Collectivité | 000054144862 | 0.35 | 000054144864 | « Traitement symptomatique à court terme (2-4 semaines) de l'anxiété sévère […] / Traitement de l'épilepsie partielle ou généralisée, en association […] en cas d'échec de deux monothérapies consécutives » |

**Hausses de prix** : MORPHINE, LAVOISIER - CHAIX ET DU MARAIS, lien 000054144874.
**Baisses de prix** : FYCOMPA, EISAI SAS, lien 000054144876.

Soit 11 JORFTEXT connus à retrouver au filtrage : …856, 858, 860, 862, 864, 866, 868, 870, 872, 874, 876 (préfixe `JORFTEXT`), plus les arrêtés d'inscription (ids non référencés dans la cible : ils alimentent la colonne Liste). URLs complètes : `https://www.legifrance.gouv.fr/jorf/id/JORFTEXT<numéro>`.

Pièges historiques que ce jeu d'essai doit détecter (constatés sur l'Excel généré par les scripts) : MORPHINE classée en Baisses au lieu de Hausses ; 6 lignes MORPHINE au lieu d'1 ; LIKOZAM scindé en `LIKOZAM` + `LIKOZAM ML` ; noms non normalisés (`DABIGATRAN TEVA , GÉLULES`) ; lien Prix manquant pour MOUNJARO ; taux `1` inventé pour VGENFLI ; indications paraphrasées ; `LES` au lieu de `SS et Collectivité`.

---

## 8. Annexes techniques

### Annexe A — `prompts/analyse_texte.txt` (Option A)

```
Tu analyses un texte officiel du Journal officiel de la République française concernant des
spécialités pharmaceutiques. Une classification déterministe a déjà été calculée : {type_pressenti}.

MISSION
1. Confirme ou corrige le type du texte parmi : arrete_inscription_ss,
   arrete_inscription_collectivites, avis_prix, decision_taux, avis_hausse_prix,
   avis_baisse_prix, extension_indication, autre.
2. Liste les spécialités concernées.

RÈGLES STRICTES
- "produit" : nom racine SEUL, en majuscules, sans dosage, forme galénique, présentation ni
  laboratoire (ex. "WEGOVY", pas "WEGOVY 0,25 mg FlexTouch"). Une seule entrée par produit
  racine : regroupe les présentations.
- "laboratoire" : nom tel qu'écrit dans le texte.
- "indication" : recopie EXACTE du passage du texte, mot pour mot (élisions [...] autorisées).
  INTERDIT de reformuler, résumer ou compléter. Si aucune indication n'est mentionnée : "".
- "taux" : taux de participation de l'assuré en décimal, en chaîne ("0.35"). Non mentionné :
  "N/A". Ne JAMAIS déduire ou inventer un taux.
- "liste" : "LES" (liste des médicaments remboursables aux assurés sociaux), "Collectivité"
  (agrément aux collectivités ou liste en sus), "SS et Collectivité" (les deux), sinon "".
- Réponds UNIQUEMENT avec l'objet JSON, sans markdown ni texte autour.

FORMAT
{"type_texte": "...",
 "medicaments": [{"produit": "...", "laboratoire": "...", "indication": "...",
                  "liste": "...", "taux": "..."}]}

TITRE : {titre}
TEXTE (nettoyé) :
{texte}
```

Ajouter 2 exemples few-shot réels tirés du 28/05 (un avis de prix, un arrêté d'inscription) une fois les textes récupérés en E1 : entrée tronquée → sortie JSON exacte attendue (annexe E).

### Annexe B — Schéma Pydantic (validation des réponses IA)

```python
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator

TypeTexte = Literal[
    "arrete_inscription_ss", "arrete_inscription_collectivites", "avis_prix",
    "decision_taux", "avis_hausse_prix", "avis_baisse_prix",
    "extension_indication", "autre",
]

class MedicamentIA(BaseModel):
    produit: str = Field(min_length=1)
    laboratoire: str = ""
    indication: str = ""
    liste: Literal["LES", "Collectivité", "SS et Collectivité", ""] = ""
    taux: str = "N/A"

    @field_validator("taux")
    @classmethod
    def taux_valide(cls, v: str) -> str:
        if v != "N/A":
            f = float(v)                      # ValueError si non numérique → relance IA
            if not (0 < f <= 1):
                raise ValueError("taux hors bornes ]0;1]")
        return v

class AnalyseTexte(BaseModel):
    type_texte: TypeTexte
    medicaments: List[MedicamentIA]
```

### Annexe C — Normalisation « nom racine » (déterministe, appliquée à toute dénomination, y compris celles renvoyées par l'IA)

Ordre des opérations (héritées des scripts, complétées) :

1. Supprimer les parenthèses explicatives : `\s*\([^)]+\)`.
2. Supprimer les dosages : `[0-9]+[\s,]?[0-9]*\s*(mg|ml|µg|ug|g|%|UI|unités?)\s*(/\s*(ml|dose))?`.
3. Supprimer les formes galéniques et packagings (insensible à la casse, liste en config, extensible) : FlexTouch, KwikPen, FlexPen, Pen, injectable, solution, sirop, comprimé(s) (sécable(s)), gélule(s), sachet, spray, patch, crème, gel, lyophilisat, poudre, suspension, ampoule, en ampoule.
4. Supprimer les mentions de pack (`x\d+`, `\d+\s*(ml|doses|stylos|sprays)`), la ponctuation orpheline (virgules doublées, ponctuation finale) et les espaces multiples.
5. Si le nom se termine par un laboratoire connu du mapping (annexe D) : le retirer (ex. `OXAZEPAM ARROW` → `OXAZEPAM`, `MORPHINE AGUETTANT` → `MORPHINE`).
6. Trim + majuscules. Résultat vide → `PRODUIT INCONNU` + « à vérifier ».

### Annexe D — Mapping laboratoires (unique, en `config.py`, complété au fil de l'eau)

```python
MAPPING_LABOS = {
    "NOVO NORDISK": "NOVO NORDISK",
    "LILLY": "LILLY",
    "FRESENIUS KABI": "FRESENIUS KABI",
    "TEVA": "TEVA SANTE",
    "ARROW": "ARROW",
    "ADVICENNE": "ADVICENNE",
    "LAVOISIER": "LAVOISIER - CHAIX ET DU MARAIS",
    "CHAIX ET DU MARAIS": "LAVOISIER - CHAIX ET DU MARAIS",
    "AGUETTANT": "AGUETTANT",
    "COOPER": "COOPERATION PHARMACEUTIQUE FRANCAISE",
    "EISAI": "EISAI SAS",
    "BIOGARAN": "BIOGARAN",
}
# Règle : première clé contenue dans le nom brut (majuscules) → valeur ; sinon nom brut tel quel.
```

### Annexe F — Journalisation

Un fichier par exécution (`logs/veille_AAAA-MM-JJ_HHMMSS.log`) : étapes franchies ; textes trouvés / retenus / écartés (titres + ids) ; taille des payloads avant/après nettoyage ; durée et tentatives par appel IA ; rapprochements (racine ← textes contributeurs) ; conflits IA/déterministe ; anomalies (reprises dans le mail).

### Annexe G — Besoin original exprimé (verbatim, message de l'utilisatrice CEPS)

> **Objectifs :**
> Principal : Automatiser la veille du JO concernant les spécialités pharmaceutiques
> Secondaire : Avoir une solution robuste et reproductible par un agent lambda du CEPS
>
> **Méthode : utilisation des IA + un code en local**
>
> - Extraction : récupération des textes du JO du jour (ou de la date souhaitée) via l'API LégiFrance disponible sur PISTE (piste.gouv.fr)
> - Filtration : récupération des arrêtés concernant uniquement les « spécialités pharmaceutiques »
> - Analyse par IA : envoi du texte brut des arrêtés à une IA pour la mise en forme des données sous forme de tableaux synthétiques — j'ai demandé à ce que ce soit l'IA Mistral qui soit utilisée (pour laisser les données en France même si elles sont publiques)
> - Notification : création du corps de mail prêt à être copié-collé pour envoi.
>
> J'ai utilisé l'IA Gemini pour m'aider à créer mon code python que je run sur VisualStudioCode. On a construit le script étape par étape : je suis actuellement bloquée à l'étape d'analyse par IA.
>
> - J'ai l'erreur « Time Out Request », de ce que je comprends les serveurs Mistral étaient saturés lorsque je lançais les requêtes mais j'ai eu cette erreur plusieurs jours, à plusieurs moments de la journée. Je n'ai pas retenté depuis mi-juin, mes abonnements payants étant arrivés à leur terme.
> - Avant d'avoir l'erreur time out, j'arrivais à avoir un Excel créé mais quelques erreurs y figuraient et j'étais en train de les corriger.
>
> Pièces jointes (reprises dans `docs/`) :
> - Excel : `veille_jo_2026-05-28_CIBLE` = ce que je veux que l'IA me génère, d'après le JO du 28 mai ; `veille_jo_2026-05-28` = ce qui a été généré et qui contient encore des erreurs
> - Python : `Test_piste4_Anonym` = code qui a généré le tableau `veille_jo_2026-05-28` ; `Test_piste5_Anonym` = code en cours de correction, avec l'erreur time out (clés API anonymisées dans les deux)
> - Outlook : `[VEILLE] – Publication JO du 28/05/2026` = la newsletter envoyée tous les matins, exemple du JO du 28 mai.

Note d'écart assumé entre le besoin verbatim et cette spec (décisions prises avec l'utilisatrice en tête, à ne pas « corriger » silencieusement) : la « filtration des arrêtés » couvre en réalité arrêtés **+ avis + décisions UNCAM** (constaté sur la cible) ; « envoi du texte brut à l'IA » est remplacé par l'architecture déterministe-d'abord du §2 (le texte brut intégral est la cause des timeouts) ; « Mistral » signifie Mistral La Plateforme, pas l'agrégateur Mammouth.ai des scripts historiques ; le « copié-collé » est servi par le cran brouillon Outlook / fichier HTML (R2-R3).

---

## 9. Plan B intégral (parcours 100 % sans risque)

Si toutes les bascules B sont choisies, la solution devient : **PISTE → filtrage → analyse déterministe → rapprochement → Excel + HTML → copier-coller manuel**, lancée par double-clic. Concrètement :

- `IA_ACTIVE = False`, `MAIL_MODE = "html"`, `ENVOI_AUTOMATIQUE = False`, lancement par `lancer_veille.bat`, git local + copie réseau.
- Dépendances externes : **uniquement l'API PISTE** (service public, gratuit, déjà utilisé avec succès par les scripts existants). Aucun compte payant, aucun flux vers un tiers, aucune automatisation Outlook, aucune tâche planifiée.
- Ce qui est quand même automatisé (l'essentiel du temps de veille) : détection des textes du jour, classement inscription/hausse/baisse, consolidation une ligne par produit, laboratoires, taux, tous les hyperliens, Excel formaté, corps de mail prêt à coller.
- Ce qui reste manuel : la colonne Indication (pré-remplie « à compléter manuellement » ; c'est un copier-coller depuis le lien Légifrance déjà fourni sur la ligne) et le geste d'envoi.
- Étapes à implémenter dans ce cas : toutes **sauf E4**, et E8/E9 en variante B. Le passage ultérieur au plan A ne demande aucune refonte : ce sont les mêmes modules, on active des drapeaux.

Ce plan B est aussi le **mode dégradé automatique** du plan A : panne Mistral prolongée → `IA_ACTIVE = False` et la veille continue le matin même.

---

## 10. Récapitulatif des risques résiduels

| Risque | Parade dans cette spec |
|---|---|
| Proxy ministériel bloque `api.mistral.ai` | Détecté dès E0 (`diagnostic.py`) ; R1 → plan B sans perte de service, demande DSI en parallèle |
| Récidive de timeouts IA | Cause racine traitée (payloads réduits E3, IA en enrichissement) ; retry/backoff E4 ; ultime recours R1 |
| Donnée fausse diffusée (taux, classement) | Déterministe prioritaire, jamais de défaut silencieux, Pydantic, « à vérifier », recette E7 |
| Rapprochement raté (lien sur le mauvais produit) | Normalisation testée sur les pièges réels du 28/05 (E5), log des rapprochements |
| Évolution API PISTE | Endpoints isolés dans `config.py`, alerte explicite E9, `diagnostic.py` pour le dépannage |
| Rejeu d'une date ancienne | `NB_ELEMENT_LASTNJO` paramétrable |
| Dépendance à une personne | E10 (README pannes + passation en autonomie) |
| Fuite de secrets | `.env` + `.gitignore` dès E0 (les scripts historiques avaient les clés en dur) |

---

## 11. Compte-rendu d'exécution (section ajoutée après implémentation — 20 juillet 2026)

Spécification exécutée de bout en bout (E0 → E10) le 20/07/2026, **en mode « sans clés »**
(règle du §6) : les clés PISTE et Mistral n'étant pas disponibles, tout ce qui est validable
hors ligne l'a été (72 tests unitaires, recette E7 sur fixture), et chaque validation
exigeant un run réel ou le poste Windows est consignée dans `veille_jo/nextSteps.md` §3
avec sa commande exacte et son résultat attendu. Le projet vit dans `veille_jo/`
(dépôt git local, 10 commits E0 → E9+E10, un par étape).

### 11.1 État des étapes

| Étape | État | Preuve |
|---|---|---|
| E0 | Terminée | `diagnostic.py` rend un verdict lisible par flux (sans clés : KO/non testé, consigné) ; `pip freeze` conforme ; premier commit sans `.env` |
| E1-E4 | Implémentées, testées hors ligne | Mocks PISTE (re-token 401, relances, JO introuvable), nettoyage/classification/tableaux, mécanique IA complète (Pydantic annexe B, relance unique, découpage par articles, échec absorbé) |
| E5 | Recette hors ligne passée | Fixture des 13 textes du 28/05 (`tests/fixtures/fixture_annexe_e.py`) → exactement les 8 lignes de l'annexe E ; chaque piège du §7 a son assertion |
| E6-E7 | Volet strict : `CONFORME` | `tests/compare_cible.py` sur l'export de la fixture vs CIBLE → exit 0 ; test négatif sur `docs/veille_jo_2026-05-28.xlsx` (l'ancien fichier fautif) → `ÉCART`, exit 1 ; ouverture LibreOffice sans avertissement |
| E8 | Rendu HTML validé (point d'arrêt levé) | `sorties/corps_mail_2026-05-28.html` + capture `sorties/rendu_mail_2026-05-28.png` ; volet win32com codé, à valider sur poste cible |
| E9-E10 | Artefacts livrés | `.bat` (CRLF), commande `schtasks` dans le README, garde-fous testés (alerte + exit 1, RAS, récapitulatif) ; README + `TUTORIEL.md`/`TUTORIEL_veille_JO.docx` (guide non technique, ajout demandé en fin de mission) ; runs réels et passation → `nextSteps.md` |

### 11.2 Écarts constatés entre la spec et la vérité terrain (fichiers font foi, §1.2)

- **Taux (§5.1)** : la CIBLE stocke un **nombre** 0.35 au format `0%` portant l'hyperlien,
  pas une chaîne `"0.35"`. L'export suit la cible ; `compare_cible.py` compare
  numériquement. La structure interne (`LigneConsolidee.taux`) reste une chaîne décimale
  comme spécifié.
- **Gabarit Excel** : la CIBLE démarre en **B2** (ligne 1 vide) — repris ; ses largeurs de
  colonnes sont **par colonne physique** (celles de « Nouvelles inscription » dominent) →
  l'export prend le max des largeurs §5.1 des sections présentes.
- **Cosmétique de la CIBLE non reprise** (fichier fait main, incohérent sur ces points ;
  le contrat §5.1 prime) : dates au format `mm-dd-yy` et parfois centrées (généré :
  `DD/MM/YYYY`, à gauche), polices mélangées Aptos Narrow/Marianne (généré :
  `config.POLICE` partout), espaces insécables parasites (`WEGOVY\xa0`,
  `\xa0FRESENIUS KABI`) → le comparateur normalise `\xa0` et les espaces de bord sur
  toutes les chaînes, pas seulement les produits.
- **Onglet** : la CIBLE s'appelle `Feuil1` (le généré : `Veille`, conforme §4.1) ;
  le comparateur lit le premier onglet, le nom n'est pas comparé.
- **Mail (§5.2)** : le `.eml` réel confirme tout (singuliers, pas de colonne Date,
  `35%` cliquable, liens couleur `#467886`, produits gras `#3A3A3A`) ; le récapitulatif
  d'anomalies est rendu **après** « Cordialement, » (ordre littéral 1 → 7 du §5.2).
- **SDK `mistralai` 2.7.0** : l'import réel est `from mistralai.client import Mistral`
  (l'import racine `from mistralai import Mistral` échoue sur cette version) ;
  appel `client.chat.complete(model, messages, temperature=0, response_format=
  {"type": "json_object"})`, timeout via `Mistral(timeout_ms=…)`.
- **Annexe A** : le fichier prompt est identique à l'annexe ; la substitution se fait par
  `.replace()` (pas `.format()`, à cause des accolades du bloc FORMAT JSON).
- **Annexe C** : `FORMES_GALENIQUES` étendues aux libellés réels du JORF
  (« en stylo prérempli », « en seringue préremplie », déclinaisons) ; retrait du
  laboratoire final refusé si le nom entier EST le laboratoire (dénomination conservée).
- **Ancien Excel des scripts** : pièges du §7 tous confirmés à la lecture du fichier
  (titre « Nouvelles inscription**s** », `LIKOZAM` + `LIKOZAM ML`, MORPHINE ×6 lignes
  **toutes en Baisses**, `MORPHINE , SANS CONSERVATEUR LAVOISIER`…) — il sert de test
  négatif permanent du comparateur.

### 11.3 Décisions d'implémentation à connaître pour la suite

- **Configuration livrée** : la recommandée du §3.1 (IA_ACTIVE=True avec dégradation
  automatique loguée si clé absente, MAIL_MODE="brouillon_outlook" avec repli HTML
  systématique, ENVOI_AUTOMATIQUE=False, Marianne, git local).
- **Cas non prévu par E5.4** : un produit vu **uniquement** dans une décision de taux
  (ou un texte « autre ») n'a aucune section applicable → aucune ligne, mais anomalie
  explicite dans le log et le récapitulatif du mail (jamais silencieux).
- **Extensions d'indications** : absentes de la structure du mail (§5.2) ; si des lignes
  existent, elles figurent dans l'Excel et le récapitulatif du mail les signale
  (« format à valider à la première occurrence »).
- **Produits IA inconnus du déterministe** : jamais ajoutés (le déterministe fait foi
  pour la liste des produits), seulement logués. Seule levée d'ambiguïté acceptée de
  l'IA : orienter un `avis_prix` non orienté en hausse/baisse.
- **Fixture annexe E** : les ids `…800`/`…802` des deux arrêtés d'inscription sont
  **fictifs** (la cible ne référence pas ces arrêtés) ; les indications reprennent la
  CIBLE à l'identique, coquilles comprises — sur run réel, l'IA produira les recopies
  exactes du JO et le volet humain E7 montrera des écarts attendus (PRADAXA, MOUNJARO).
- **Alertes** : une alerte ne part jamais seule (`.Display()` même en mode brouillon) ;
  l'enveloppe du fichier HTML de prévisualisation force un rendu clair (un navigateur en
  mode sombre donnait une prévisualisation trompeuse du mail).
- **Calibration E2 toujours due** : les motifs de `MOTIFS_CLASSIFICATION` et le parsing
  des tableaux réels de l'API restent calibrés sur des titres/structures **plausibles**
  (constatés sur les scripts historiques, pas sur un run réel) — première chose à
  vérifier une fois les clés obtenues (`nextSteps.md` §3, entrées E2/E3).

### 11.4 Reste à faire

Tout est dans **`veille_jo/nextSteps.md`** (autoportant) : secrets à obtenir (§1),
décisions A/B à confirmer avec la question à poser pour chacune (§2), 13 validations en
attente avec commande exacte et résultat attendu (§3), démarches externes dont
l'éventuelle ouverture DSI du flux `api.mistral.ai` (§4), checklist de première
exécution (§5). Point d'entrée utilisateur : `veille_jo/TUTORIEL.md` (version Word :
`TUTORIEL_veille_JO.docx`).

### 11.5 Révision du contrat de sortie — 22/07/2026 (demande utilisatrice)

Trois évolutions actées après les premiers runs réels quotidiens, qui **amendent les
§2, 5.1 et 6-E5 de cette spec** (le détail et la validation cliente : `nextSteps.md` §0) :

1. **Une ligne par présentation** telle que publiée au JO (plus de fusion « une ligne par
   produit racine ») : clé de rapprochement inter-textes = **code CIP** (présent dans les
   trois familles de tableaux), repli dénomination ; le nom racine reste la clé de
   propagation (listes, liens, taux) et de la recette E7, qui compare désormais la
   couverture par racines contre la CIBLE historique. Le « piège MORPHINE ×6 » du §7
   s'inverse : 6 présentations = 6 lignes, chacune avec son PFHT.
2. **Colonne Prix = PFHT** recopié de l'avis (texte de la cellule, lien conservé) — les
   colonnes tarifaires des tableaux sont désormais lues (CIP, PFHT) mais toujours JAMAIS
   envoyées à l'IA (l'interdit anti-timeout du §1.4 tient).
3. **Laboratoire** : pattern littéral « (laboratoires X) » des dénominations (constaté sur
   les trois familles), retiré de la dénomination affichée ; mapping annexe D en repli.

S'y ajoute la correction de la cause racine des indications perdues (constat du 22/07) :
le nettoyage §6-E3 détruisait la liaison indication ↔ produits des arrêtés multi-produits
(tableaux extraits, l'IA recevait les indications sans aucun nom de produit). La liaison
étant **structurelle** (l'indication précède le tableau de sa section), elle est désormais
lue en déterministe (`analyse.indication_de_section`, deux tournures constatées sur pièces) ;
l'IA reste le filet des textes en prose libre. Sur le 22/07 : 17 lignes toutes complètes
(indications, laboratoires, PFHT, taux), 1 anomalie (décision « orientation », inchangée).

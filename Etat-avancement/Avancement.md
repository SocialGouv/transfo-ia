# À reporter dans `Etat-avancement.xlsx`

> ✅ **Reporté dans le classeur le 30 juillet 2026.** Ce fichier reste la trace de ce qui a été écrit et où. Ne pas rejouer les blocs tels quels : les lignes ont été insérées et les références ont bougé (voir § *Où c'est atterri*).

Semaine du 27 au 31 juillet 2026 · sources : [RGAA 29/07](../CR/transverse/Avancement%20RGAA_29-07.txt) · [Igor 28/07](../CR/transverse/Igor-28-07.txt) et [intérêt](../CR/transverse/Interet_Igor.txt) · [CDP SIRENA 30/07](../CR/products/CDP-SIRENA-30-07.txt) · [CEPS 30/07](../CR/transverse/CEPS_Sabine_Lugand.txt)

Le classeur contient deux tableaux sur la même feuille, avec les mêmes colonnes de périmètre :

| Colonne | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| **Tableau 1** — *Niveau IA* (lignes 4 à 14) | rôle | use case IA | Egapro | DACCORD | SIRENA | VAO | Transverse |
| **Tableau 2** — *Actions entreprises et à entreprendre* (lignes 19 à 29) | rôle | action prévue | Egapro | DACCORD | SIRENA | VAO | Transverse |

> ⚠️ **Ordre des opérations.** Le tableau 1 gagne une ligne (§ 1.3). Si tu l'insères en premier, **tout le tableau 2 descend d'une ligne** : les références 19→29 deviennent 20→30. Le plus simple est de traiter le tableau 2 d'abord, puis d'insérer la nouvelle ligne du tableau 1.

## Où c'est atterri

Les références ci-dessous sont celles **d'avant** l'insertion. Voici où se trouve chaque modification dans le classeur tel qu'il est maintenant :

| § | Contenu | Référence d'avant | Référence actuelle |
|---|---|:---:|:---:|
| 1.1 | SIRENA · pilotage → 1 | F4 | **F4** |
| 1.2 | SIRENA · tickets de spec → 1 | F5 | **F5** |
| 1.3 | Nouvelle ligne de matrice · *Outiller les référentiels d'architecture* | — | **ligne 15** |
| 2.1 | Pré-audit d'accessibilité · Egapro | D21 | **D22** |
| 2.2 | Tickets de spec · DACCORD | E23 | **E24** |
| 2.3 | Tickets de spec · SIRENA | F23 | **F24** |
| 2.4 | Développement augmenté · SIRENA | F19 | **F20** |
| 2.5 | Génération de DA · Transverse | H26 | **H27** |
| 2.6 | Nouvelle ligne · *Outiller les référentiels d'architecture* | — | **ligne 31** |
| 2.7 | Nouvelle ligne · *Outiller les postes internes* | — | **ligne 32** |
| 2.8 | Nouvelle ligne · *Visibiliser l'accompagnement hors DNUM* | — | **ligne 33** |

Le tableau *Niveau IA* couvre désormais les lignes 4 à 15, le tableau *Actions* les lignes 20 à 33. Les hauteurs des lignes modifiées ont été remises en ajustement automatique : elles se déplieront à la première ouverture.

---

## 1. Tableau *Niveau IA*

### 1.1 · SIRENA passe de « ? » à 1 sur le pilotage — cellule **F4**

La rencontre du 30/07 avec Aurélie permet enfin de poser le diagnostic côté produit : usage de l'IA faible, aucune visibilité sur l'usage qu'en font les développeurs. C'est un démarrage, donc niveau 1.

```
1
```

### 1.2 · SIRENA passe de « ? » à 1 sur les tickets de spec — cellule **F5**

Même source, même logique : la fonction démarre.

```
1
```

### 1.3 · Nouvelle ligne à insérer après la ligne 14 (*Architecte · Générer un DA*)

Le sujet ouvert par Igor ne se réduit pas à la génération de DA : il porte sur le référentiel lui-même. Il mérite sa propre ligne, en Transverse.

| B (rôle) | C (use case IA) | D | E | F | G | H |
|---|---|---|---|---|---|---|
| `Architecte` | `Outiller les référentiels d'architecture` | `NA` | `NA` | `NA` | `NA` | `1` |

---

## 2. Tableau *Actions entreprises et à entreprendre*

### 2.1 · Pré-audit d'accessibilité, Egapro — cellule **D21** *(remplacer le contenu)*

Ligne « Developpeurs · Piloter le pre-audit d'accessibilité ». Le CR du 29/07 sépare nettement trois chantiers ; la cellule doit refléter ce qui est acquis (Egapro plus accessible) et ce qui ne l'est pas (le porteur de l'outil de pré-audit).

```
Réalisé:
- Synchronisation des retours de Marie et du travail de Max
- Synchronisation de Amelle et Victor
- Le code Egapro est plus accessible: l'audit passe de 31 à 16 erreurs
- Proposition à Max et Lucas d'un framework de suivi des performances de l'outil dans le temps (github.com/sboukhari-Ippon/RGAA-Tool-Monitoring)
En cours:
- Trois chantiers à ne pas confondre: rendre Egapro accessible, générer du code accessible (encore adossé au pré-audit, pas de solution autonome), pré-auditer l'accessibilité du code
- Lucas est en phase sur le besoin de monitorer les performances de l'outil. Max, saturé entre trouver la solution et l'instrumenter, préfère se concentrer sur l'accessibilité d'Egapro
À réaliser:
- Arbitrer avec Gary: qui porte l'outil de pré-audit hors des sprints Egapro et sans reposer sur Max, avec le framework de monitoring intégré. Sans porteur ni mesure, l'outil restera piloté au feeling
```

### 2.2 · Tickets de spec, DACCORD — cellule **E23** *(remplacer le contenu)*

Ligne « Chefs de projet · Accompagner à la génération de tickets de spec ». Le point avec Kahina a maintenant une date et un format : session commune avec Aurélie.

```
En cours:
- Organiser le point avec Kahina à son retour de congés
- Le point se fera mi-août, en session commune avec Aurélie (CDP SIRENA), qui est demandeuse d'une formation à l'usage de l'IA pour le PM et le PO
```

### 2.3 · Tickets de spec, SIRENA — cellule **F23** *(remplacer « À définir »)*

Même ligne, colonne SIRENA. C'est la demande la plus forte de la semaine, et elle est entrante.

```
Réalisé:
- Rencontre de la CDP Aurélie le 30 juillet: elle a repris le projet en juin après Delphine, partagera les rôles PM et PO avec Valérie (prestataire), les deux tenant les deux rôles
- Diagnostic: pilotage en mode produit mais indicateurs projet (coût, délais, qualité), usage de l'IA faible, aucune visibilité sur l'usage qu'en font les développeurs, sentiment de louper le train de l'IA
À réaliser:
- Former Aurélie mi-août, en session commune avec Kahina (DACCORD), à l'usage de l'IA pour le PM et le PO. Elle souhaite explicitement aller plus loin que la seule génération de tickets
- Pistes identifiées avec elle: workflow de conception et d'exploration dans Jira, suivi de la dette technique, communication entre développeurs, intégration d'agents, et usage de l'IA pour formuler les questions auxquelles personne n'aurait pensé lors des entretiens utilisateurs (l'équipe a accès aux users)
```

### 2.4 · Formation au développement augmenté, SIRENA — cellule **F19** *(remplacer « À définir »)*

Ligne « Développeurs · Former au développement augmenté ». La CDP donne un point d'entrée sur l'équipe de développement.

```
À réaliser:
- Cadrer l'accompagnement des développeurs: la CDP n'a aucune visibilité sur la façon dont ils utilisent l'IA, et la communication entre développeurs pourrait être plus forte
- Point d'entrée: passer par Aurélie lors de la session PM/PO de mi-août
```

### 2.5 · Génération de DA, Transverse — cellule **H26** *(remplacer le contenu)*

Ligne « Architectes · Accompagner à la génération de DA ». L'atelier reste le jalon, mais l'échange avec Igor lui donne son contexte : le DA n'est qu'un élément d'un problème plus large de démat.

```
Réalisé:
- Générateurs comparatifs Claude / DeepSeek construits
À réaliser:
- Atelier de génération de DA avec l'IA le 3 août
- Rattacher l'atelier au chantier de démat du DA porté par Igor: structuration du document pas à jour, ressaisie d'information, difficultés de traçage entre versions, stockage et partage sur SharePoint
```

### 2.6 · Nouvelle ligne — *Outiller les référentiels d'architecture*, en **H30**

À insérer après la ligne 29 (« Transverse · Harness »). B = `Architectes`, C = `Outiller les référentiels d'architecture`, D à G = `NA`, et en H :

```
Réalisé:
- Cadrage avec Igor le 28 juillet. Problème posé: les référentiels et les DA vivent sur SharePoint, versions difficiles à tracer, structure des documents jamais à jour, ressaisie d'information, partage mal maîtrisé
- Cible arrêtée: un dépôt de fiches faisant source de vérité, un dépôt de documents de contexte construits dessus, publication en GitLab Pages, chaque élément renvoyant vers sa source
- Gouvernance posée par Igor: relecteurs, arbitrage final par lui, ouverture en lecture à tous les consommateurs du référentiel, TMA comprise. Il est ouvert sur les documents de contexte à créer et nous invite à y mettre ce qui compte dans notre quotidien
À réaliser:
- Récupérer le référentiel auprès de Mathias
- Produire un premier jet de skills standards, à faire valider par les responsables du référentiel, pour que la règle d'architecture soit exploitable dans l'IDE au moment où l'on écrit le DA
- Créer et épurer le dépôt, prévenir Igor qui le complétera, figer une version 0.1, puis embarquer la conformité numérique
- Solliciter le studio d'architecture, qui détient déjà le cadre de cohérence, en cas de manque sur les règles
- Poser une demi-journée d'acculturation IA avec Igor et les architectes fin août, un mardi ou un jeudi
- Utiliser le créneau du jeudi 14h-15h, où Igor réunit les architectes, comme point de rapprochement
Point de vigilance:
- Les développeurs d'Igor partent en septembre et en octobre: la fenêtre pour les faire monter en compétence est étroite
```

### 2.7 · Nouvelle ligne — *Outiller les postes internes*, en **H31**

C'est le point dur de la mission, et il devient une action à part entière : sans réponse, la stratégie d'adoption ne dépasse pas le cercle des prestataires. B = `Transverse`, C = `Outiller les postes internes (accès aux harness)`, D à G = `NA`, et en H :

```
Réalisé:
- Igor a identifié les deux voies possibles pour un agent interne sur poste managé, qui ne peut pas installer un harness: soit le packaging de l'application par le centre logiciel, soit une demande de compte administrateur temporaire contresignée par le manager
- Côté développeurs, la sécurité s'oriente vers des postes à système libre, avec une VM dédiée à la bureautique. La bureautique n'a pas vocation à tourner sur un environnement aussi ouvert que celui d'un développeur
À réaliser:
- Rencontrer Céline Liechti, qui saura nous orienter vers les personnes qui gèrent le centre logiciel, pour y faire intégrer les harness cibles
- Vérifier les contraintes réseau constatées: npx semble bloqué, HTTP passe
```

### 2.8 · Nouvelle ligne — *Visibiliser l'accompagnement hors DNUM*, en **H32**

Le CEPS n'apparaît nulle part dans le classeur alors que c'est une action réalisée du troisième enjeu de la mission. B = `Transverse`, C = `Visibiliser l'accompagnement hors DNUM (CEPS)`, D à G = `NA`, et en H :

```
Réalisé:
- Automatisation de la veille du Journal officiel sur les spécialités pharmaceutiques, restituée en newsletter. Le besoin était exprimé "avec de l'IA" et la solution atteint l'objectif sans en avoir besoin
- Sabine Lugand est satisfaite de l'outil. MVP réalisé en 3 jours
- Passation à Victor Degliame
À réaliser (Victor):
- Transformer la solution Python en outil utilisable par des personnes qui ne peuvent pas installer Python
- Implémenter les évolutions souhaitées par Sabine
À réaliser (mission):
- Évangéliser les personnes du CEPS que Victor a rencontrées, en capitalisant sur le MVP: 3 jours pour quasi automatiser une newsletter mensuelle. Message: l'IA permet de réaliser des applications rapidement tant que le besoin est clair
```

---

## Récapitulatif des décomptes après report

| | Avant | Après |
|---|:---:|:---:|
| Actions réalisées | 6 | **8** |
| En cours | 3 | **4** |
| Planifiées | 7 | **10** |
| À lancer | 2 | **3** |
| Total engagées | 18 | **25** |
| Déclinaisons à cadrer | 11 | **10** *(SIRENA sort des tickets de spec)* |
| Use cases SIRENA en découverte | 4 | **6** *(2 sortent de « à évaluer »)* |

Ces chiffres sont déjà répercutés dans [`build/generate_charts.py`](build/generate_charts.py), les SVG régénérés, le [README](../README.md) et l'[état d'avancement détaillé](Etat-avancement-detaille.md).

---

## Passage de la matrice sur l'échelle 1 à 5 — reporté le 31 juillet 2026

> ✅ **Reporté dans le classeur le 31 juillet 2026** (tableau *Niveau IA*, lignes 4 à 15, et légende K4:L8). Proposition en cours de challenge : si des niveaux bougent, ne retoucher que les cellules concernées.

Règle de conversion depuis l'ancienne échelle 1-3 : **1 → 1 · 2 → 3 · 3 → 4 · « ? » → 1** (un use case non observé est noté 1 par convention) · NA inchangé. Nouvelle légende : 1 Découverte · 2 Expérimentation · 3 Pratique régulière · 4 Maîtrise · 5 Standard d'équipe.

Exceptions à la règle, assumées :

| Cellule | Ancien | Nouveau | Pourquoi pas la conversion mécanique |
|---|:---:|:---:|---|
| D11 (pré-audit accessibilité Egapro) | 1 → 2 | **1 → 2** | pas de porteur ni de mesure : pratique non fiabilisée, donc expérimentation |
| E13 (system prompts DACCORD) | 1 → 2 | **1 → 2** | la mise en commun vient de démarrer (20/07) ; l'atelier du 6/08 la consolidera vers 3 |

Cellules modifiées : D4 (`1 -> 3`), D6 (4), D7 (`1 -> 4`), D8 (3), D9 (4), D10 (4), D13 (4), E7 E8 E9 (1, 3, 3), F6:F9 (1), G4:G7 et G13 (1), légende K4:L8. L'échelle est répercutée dans `build/generate_charts.py` (MATRICE, NIVEAUX, ramp5), les SVG, le README et l'état détaillé (nouvelle section *Impact des actions*).

# Details — l'état d'avancement, fiche par fiche

Point du 15 septembre 2026 (semaines du 31 août au 11 septembre) · [← retour à la synthèse](README.md) · [tableau de bord](Suivi-Strategie-Adoption-IA.html)

**Au sommaire** : [plan d'actions](#plan-dactions) · [maturité par périmètre](#maturité-par-périmètre) · [impact des actions](#impact-des-actions) · [matrice de maturité](#matrice-de-maturité) · [zoom coaching](#zoom--coaching-développement-augmenté-daccord-16-juillet) · [focus par chantier](#focus-par-chantier) · [livrables](#livrables-à-date)

## Plan d'actions

Le cœur du suivi : ce qui a été réalisé, ce qui est en cours, ce qui reste à faire. Chaque ligne indique le périmètre, l'action et le métier concerné.

### ✅ Réalisées (19)

**Depuis le dernier point (31 août → 11 septembre)**

- **VAO · Former au développement augmenté** *(développeurs)* — atelier du 3 septembre : l'équipe est formée, OpenCode Desktop est installé sur les postes, la pratique du développement augmenté démarre.
- **Transverse · Valider la solution « du prototype IA à la maquette Figma »** *(designers)* — point design et IA du 3 septembre ([compte rendu](CR/design/DESIGN-3-Septembre.txt)) : la qualité du passage d'un prototype généré par IA vers une maquette Figma en composants DSFR officiels est validée (MCP Figma, compte full). Priorités posées avec Louis pour la suite : une boucle de feedback simple, le MCP DSFR en version 1.15 (les charts), un point sur l'alpha 3 du DSFR 2.0 ; Penpot à explorer en priorité 2.
- **DACCORD · Former les PM/PO et leur remettre le skill de tickets** *(chefs de projet)* — formation du 8 septembre : les PM/PO ont en main un skill qui les challenge sur la précision de leurs tickets et formalise le ticket entier, critères d'acceptation compris. Système fourni par la mission : OpenCode Desktop et un modèle Albert (le provider IA de l'État). Ils le prennent en main ; en parallèle, Olivier Toumsy les forme.
- **Transverse · Initier Igor Ranquin et Nicolas Fournier à l'IA générative** — demi-journée d'acculturation ([compte rendu](CR/transverse/Igor-Nicolas-initiation-IA-15-09.txt)) : les deux veulent désormais mettre les mains dans l'orchestration.
- **Transverse · Mettre en place un premier use case d'orchestration de DA** *(architectes)* — ([compte rendu](CR/transverse/Archis-orchestration-DA-15-09.txt)) : l'IA vérifie que les fonctionnalités du SI applicatif sont décrites de façon cohérente sur tout le DA. Stack légale sur poste ministère : OpenCode Desktop et DeepSeek V4 Flash servi par Albert. Les architectes prennent l'orchestration en main pour se familiariser avec cet usage.
- **Transverse · Former Adrien Chauve à l'IA générative** — ([compte rendu](CR/developpeurs/Adrien-Chauve-formation-IA-Gen-15-09.txt)) : il souhaitait comprendre ce qu'apporte l'IA générative sur le cycle produit ; formation par l'apprentissage.

**Depuis le début de la mission**

- **DACCORD · Former au développement augmenté** *(développeurs)* — session de coaching du 16 juillet, détaillée dans le [zoom](#zoom--coaching-développement-augmenté-daccord-16-juillet).
- **Egapro · Accompagner à la réalisation d'orchestrations** *(développeurs)* — orchestration « séparation codeur / testeur » en place.
- **Egapro · Permettre un meilleur suivi d'un projet utilisant l'IA** *(chefs de projet)* — estimations en taille de T-shirt sur les tickets ; tickets Design créés pour donner à l'équipe de la visibilité sur la roadmap design et la challenger.
- **Egapro · Accompagner à la génération de prototypes** *(designers)* — skill UX adapté au projet, skill d'audit UX, formation à la réalisation de prototypes de maquettes avec Claude.
- **Transverse · Benchmark des harness et modèles de coding agentique** — [bench livré](Livrables/benchHarness/Bench_Coding-Agentique.pdf) : 7 stacks comparées sur prix entrée / sortie, performance (DeepSWE, Terminal-Bench, SWE-bench en baseline), souveraineté et conformité (périmètre revu le 2 septembre). Complété le 3 septembre par le support [Souveraineté et performance des modèles et harness](Livrables/Souverainete-Performance/Souverainete-Performance-Modeles-Harness.pdf).
- **Transverse · Cadrer la voie Bedrock avec AWS** — [échange du 23 juillet](CR/transverse/AWS-Bedrock-23-07-2026.txt) : un large catalogue de modèles est accessible via Bedrock (dont les open-weight chinois) en conservant l'observabilité. AWS revient avec la liste des modèles disponibles et une documentation d'observabilité.
- **Transverse · Claude Enterprise, discussions avec Software One** — point tenu le 23 juillet, conjointement avec le cadrage de la voie Bedrock.
- **Transverse · Cadrer avec Igor l'outillage des référentiels d'architecture** *(architectes)* — [échange du 28 juillet](CR/transverse/Igor-28-07.txt) : besoin posé (référentiels et DA sur SharePoint, versions difficiles à tracer, ressaisie), cible arrêtée (un dépôt de fiches, un dépôt de documents de contexte, publication en GitLab Pages) et gouvernance (relecteurs, arbitrage final par Igor, ouverture en lecture aux consommateurs dont la TMA).
- **Transverse · Livrer au CEPS l'automatisation de la veille du Journal officiel** — [restitution du 30 juillet](CR/transverse/CEPS_Sabine_Lugand.txt) : Sabine Lugand est satisfaite de l'outil, la newsletter mensuelle sur les spécialités pharmaceutiques est quasi automatisée. La main est passée à Victor Degliame.
- **Transverse · Atelier de génération de DA avec l'IA** *(architectes)* — [atelier du 4 août](CR/transverse/CR_Architectes-atelier-4-08-26.txt) : démonstration de la génération d'un DA depuis un code source, deux voies d'usage de l'IA sur poste ministère présentées, 5 use cases identifiés par les architectes.
- **DACCORD · Atelier d'amélioration des skills** *(développeurs)* — [atelier du 6 août](CR/transverse/daccord-ia-06-08.txt) : les skills couvrent le changement de version, le changelog, le dev front, le dev back et le plan d'implémentation. Recommandation de la mission : ajouter des skills de tests back et front.
- **Transverse · Point d'adoption IA pour la population produit** — [point du 6 août](CR/products/Adoption-IA-Products-6-08.txt) : population hétérogène (coachs, PM/PO, recherche utilisateur), craintes explicites côté RU. Félix formalise les use cases, Olivier liste les équipes prioritaires ; la centralisation de la documentation fonctionnelle est jugée prioritaire.
- **Transverse · Point design avec Louis : prototypes DSFR fiabilisés, flux vers Figma** *(designers)* — [point du 13 août](CR/design/Louis-13-08.txt) : démonstration du loop engineering qui contrôle le respect du DSFR et du transfert d'un prototype vers Figma. **Louis valide le use case (« beaucoup de valeur »)**.

### 🔄 En cours (5)

- **Transverse · Construire la boucle de feedback des designers** *(designers)* → priorité 1 posée le 3 septembre : rendre l'expérience agréable quand un designer utilise l'IA, même sans être technophile. Les maquettes arrivent dans Figma, le retour du designer relance un nouveau prototype.
- **DACCORD · Accompagner individuellement l'optimisation des skills et poser les bases de l'orchestration** *(développeurs)* → Sébastien et Florian accompagnés en août, Sylvain à son retour début septembre. En parallèle : accès au code via Rémi pour une analyse et des suggestions.
- **DACCORD · Adapter les orchestrations Egapro à Jira** *(développeurs)* → l'orchestration frontend et backend est en place ; la suite est de l'étendre à la documentation et au changelog.
- **Egapro · Piloter le pré-audit d'accessibilité** *(développeurs)* → un [framework de suivi des performances](https://github.com/sboukhari-Ippon/RGAA-Tool-Monitoring) a été proposé à Max et Lucas. À arbitrer avec Gary : qui porte l'outil hors des sprints Egapro, avec la mesure intégrée.
- **Transverse · Constituer le référentiel d'architecture outillé** (fiches, documents de contexte, skills) *(architectes)* → récupérer le référentiel auprès de Mathias, produire un premier jet de skills, créer et épurer le dépôt, laisser Igor le compléter, figer une version 0.1.

### 📅 Planifiées (7)

- **Au retour de congé de Selim — Transverse · Accompagner Igor et Nicolas Fournier à une première orchestration**, en partant du use case de DA déjà en place.
- **À caler — SIRENA · Former Aurélie à l'usage de l'IA pour le PM et le PO**, au-delà de la seule génération de tickets *(chefs de projet)*.
- **Courant septembre — Transverse · Benchmark élargi aux modèles disponibles sur Bedrock** — dès réception de la liste des modèles par AWS.
- **Courant septembre — Transverse · Définir et partager un catalogue de skills communs** : besoin PO (besoin métier, US, tests d'acceptance), plan technique orienté ATDD, dev en ATDD (séparation codeur / testeur), refacto adossé à Sonar.
- **Dès l'introduction faite — Transverse · Rencontrer les personnes du centre logiciel** pour y faire packager les harness cibles ; introduction par Olivier.
- **Fin septembre — Transverse · Cartographier les bénéficiaires des comptes Bedrock** (internes, et externes sur sujets sensibles).
- **À dater — Transverse · Mettre à jour le MCP DSFR en 1.15 et faire le point sur l'alpha 3 du DSFR 2.0** *(designers)* → le DSFR 2.0 apporte des briques qui réduisent le besoin de portage ; Selim a accès au dépôt du MCP DSFR.

### ⏳ À lancer (5)

- **VAO · Accompagner Halim sur la génération de tickets intelligibles via MCP** *(chefs de projet)* → caler un créneau.
- **Transverse · Former les Product Owners à la fenêtre de contexte et au prompt engineering** → valider l'intérêt d'une séance avec Olivier.
- **Transverse · Session d'acculturation de l'ensemble des designers** → la solution est validée, la boucle de feedback est la dernière condition posée par Norman pour ouvrir la démarche à tous les designers.
- **Transverse · Centraliser la documentation fonctionnelle des produits** (un dossier docs, la doc rangée par epic) → à porter avec Adrien et Gary, en commun avec le studio produit.
- **Transverse · Évangéliser les équipes du CEPS rencontrées par Victor** → capitaliser sur le MVP livré à Sabine Lugand.

### 🧭 Déclinaisons à cadrer (9)

Actions déjà éprouvées sur un périmètre, à décliner sur les autres une fois le cadrage fait avec chaque équipe.

| Action | À cadrer sur |
|---|---|
| Former au développement augmenté | SIRENA |
| Accompagner à la réalisation d'orchestrations | SIRENA · VAO |
| Piloter le pré-audit d'accessibilité | DACCORD · SIRENA · VAO |
| Accompagner à la génération de prototypes | DACCORD · SIRENA · VAO |

## Maturité par périmètre

Le niveau d'organisation que l'accompagnement a apporté à chaque périmètre, sur une échelle de 1 à 5 :

| Niveau | Signification |
|:---:|---|
| **1 → 2** | De rien à la découverte de l'IA |
| **3** | Des skills utilisés, des use cases IA pratiqués, mais une organisation encore perfectible |
| **4** | Des orchestrations, une organisation maîtrisée |
| **5** | Des orchestrations, un volume de cas d'usage côté dev comme côté PM/PO, une organisation pointue, des bonnes pratiques renseignées, du vrai craft |

| Périmètre | Niveau | Ce que l'accompagnement a changé |
|---|:---:|---|
| Egapro | **3 → 4** | Les orchestrations tournent en routine et l'organisation est maîtrisée. C'était le chaos, ça ne l'est plus |
| DACCORD | **1 → 2** | Orchestration frontend et backend en place côté dev ; PM/PO formés, skill de tickets en main. Le niveau 3 se validera quand skills et orchestration seront utilisés au quotidien |
| SIRENA | 2 | Usage IA réel mais individuel, sans coordination d'équipe ; formation PM/PO à caler |
| VAO | **1 → 2** | Développeurs formés le 3 septembre, OpenCode Desktop installé, pratique du dev augmenté démarrée |
| Architectes | **1 → 2** | De cinq use cases identifiés à une première orchestration qui tourne (cohérence du DA), en prise en main. Le niveau 3 se validera à l'usage autonome |
| Designers | **1 → 2** | Du prototype IA à la maquette Figma en composants DSFR officiels : qualité validée. Reste la boucle de feedback pour une pratique régulière |

## Impact des actions

Toutes les actions ne pèsent pas pareil. Chaque action engagée est classée selon ce qu'elle change pour les équipes, et les déterminantes sont décrites une à une :

| Impact | Ce que ça recouvre |
|---|---|
| ◆◆◆ **Déterminant** | Du concret dans le quotidien des équipes : skills créés ou challengés, orchestrations, accompagnement de mise en place de solutions |
| ◆◆ **Élevé** | Acculturations et formations : elles changent le regard et amorcent la pratique |
| ◆ **Modéré** | Discussions, cadrages, études, communication : elles préparent le terrain |

### Répartition par équipe

| Chantier | ◆◆◆ Déterminant | ◆◆ Élevé | ◆ Modéré |
|---|:---:|:---:|:---:|
| Egapro | 4 | – | – |
| DACCORD | 4 | 1 | – |
| SIRENA | – | 1 | – |
| VAO | 1 | 1 | – |
| Transverse | 8 | 5 | 11 |
| **Total** | **17** | **8** | **11** |

**Lecture** : sur les périmètres actifs, l'impact est presque exclusivement du concret. Les actions modérées sont toutes transverses : les chantiers de fond (bench, Bedrock, outillage) qui conditionnent le passage à l'échelle. La quinzaine ajoute trois actions déterminantes réalisées (orchestration de DA, solution prototype → Figma, formation et skill PM/PO DACCORD) et trois formations (VAO, Igor et Nicolas, Adrien Chauve).

### Le classement, action par action

**◆◆◆ Déterminant (17)** — chaque action avec ce qu'elle change concrètement :

| Action | Chantier | Statut | Ce que ça change |
|---|---|---|---|
| Orchestration « codeur / testeur » en routine | Egapro | ✅ Réalisée | Le code arrive testé par une instance indépendante : la qualité ne repose plus sur la seule relecture humaine |
| Pilotage adapté à l'IA (estimations T-shirt, tickets design) | Egapro | ✅ Réalisée | Le suivi projet colle à la vitesse réelle du développement augmenté ; la roadmap design devient visible et challengeable |
| Designers outillés : skills UX, formation prototypes | Egapro | ✅ Réalisée | Raphael génère plusieurs prototypes HTML avant de maquetter : il se projette au lieu d'itérer à l'aveugle |
| Première orchestration de DA : cohérence des fonctionnalités sur tout le DA | Transverse | ✅ Réalisée | Les incohérences d'un DA, difficiles à percevoir à la main, sont détectées par l'IA ; les architectes passent de use cases identifiés à un use case qui tourne |
| Du prototype IA à la maquette Figma DSFR : qualité validée (3 septembre) | Transverse | ✅ Réalisée | Le designer teste plusieurs prototypes, puis obtient une maquette Figma en composants DSFR officiels : plus d'interprétation du design system, une vision d'ensemble du parcours pour les développeurs |
| Formation des PM/PO DACCORD et skill de tickets remis (8 septembre) | DACCORD | ✅ Réalisée | Le ticket est challengé et formalisé par l'IA, critères d'acceptation compris : le métier se concentre sur sa valeur ajoutée, moins d'allers-retours avec les développeurs |
| Outil de veille du Journal officiel livré au CEPS | Transverse | ✅ Réalisée | Une newsletter mensuelle quasi automatisée en trois jours : la preuve, visible hors DNUM, que l'IA livre vite sur un besoin clair |
| Atelier de génération de DA avec l'IA (4 août) | Transverse | ✅ Réalisée | Les architectes repartent acteurs : cinq use cases identifiés par eux-mêmes |
| Atelier d'amélioration des skills (6 août) | DACCORD | ✅ Réalisée | Les skills de l'équipe couvrent cinq domaines et s'améliorent en commun, plus chacun dans son coin |
| Boucle de feedback des designers | Transverse | 🔄 En cours | L'IA devient utilisable par un designer non technophile : la dernière condition pour ouvrir la démarche à tous les designers |
| Piloter le pré-audit d'accessibilité (framework de monitoring) | Egapro | 🔄 En cours | L'audit du code Egapro passe de 31 à 16 erreurs ; la mesure intégrée évitera un outil piloté au feeling |
| Adapter les orchestrations Egapro à Jira | DACCORD | 🔄 En cours | Le savoir-faire éprouvé sur Egapro se transfère à une seconde équipe ; l'orchestration front et back est en place |
| Constituer le référentiel d'architecture outillé (fiches, skills) | Transverse | 🔄 En cours | La règle d'architecture devient exploitable dans l'IDE au moment d'écrire le DA, au lieu d'un PDF SharePoint retrouvé après coup |
| Accompagnement individuel skills et bases d'orchestration (Sébastien, Florian, Sylvain) | DACCORD | 🔄 En cours | Du sur-mesure pour transformer les skills en pratique quotidienne |
| Catalogue de skills partagés : besoin PO, plan tech ATDD, dev ATDD, refacto Sonar | Transverse | 📅 Planifiée | Un socle commun mutualisé entre périmètres, au lieu de reconstruire les mêmes skills équipe par équipe |
| Accompagner Igor et Nicolas Fournier à une première orchestration | Transverse | 📅 Planifiée | Le référentiel d'architecture exploité par ceux qui le portent ; deux relais internes de plus sur l'orchestration |
| Accompagner Halim sur la génération de tickets intelligibles | VAO | ⏳ À lancer | Moins d'allers-retours entre PM et développeurs sur VAO |

**◆◆ Élevé (8)**

| Action | Chantier | Statut |
|---|---|---|
| Coaching développement augmenté du 16 juillet¹ | DACCORD | ✅ Réalisée |
| Point design avec Louis : prototypes DSFR fiabilisés, flux vers Figma (13 août) | Transverse | ✅ Réalisée |
| Atelier de développement augmenté (3 septembre) | VAO | ✅ Réalisée |
| Initiation à l'IA générative d'Igor Ranquin et Nicolas Fournier | Transverse | ✅ Réalisée |
| Formation à l'IA générative d'Adrien Chauve | Transverse | ✅ Réalisée |
| Formation à l'usage de l'IA pour le PM et le PO (à caler) | SIRENA | 📅 Planifiée |
| Acculturation IA des PO (à valider avec Olivier) | Transverse | ⏳ À lancer |
| Acculturation de l'ensemble des designers | Transverse | ⏳ À lancer |

<sub>¹ Classé par nature (formation), mais son effet a déjà dépassé la catégorie : mise en commun des system prompts engagée par l'équipe dès le lundi suivant.</sub>

**◆ Modéré (11)**

| Action | Chantier | Statut |
|---|---|---|
| Bench des harness et modèles de coding agentique | Transverse | ✅ Réalisée |
| Cadrage de la voie Bedrock avec AWS (23 juillet) | Transverse | ✅ Réalisée |
| Claude Enterprise : discussions avec Software One (23 juillet) | Transverse | ✅ Réalisée |
| Cadrage des référentiels d'architecture avec Igor (28 juillet)² | Transverse | ✅ Réalisée |
| Point d'adoption IA pour la population produit (6 août) | Transverse | ✅ Réalisée |
| Bench élargi aux modèles Bedrock (courant septembre) | Transverse | 📅 Planifiée |
| Rencontrer le centre logiciel (introduction par Olivier) | Transverse | 📅 Planifiée |
| Cartographie des bénéficiaires des comptes Bedrock (fin septembre) | Transverse | 📅 Planifiée |
| MCP DSFR en 1.15, point sur l'alpha 3 du DSFR 2.0 | Transverse | 📅 Planifiée |
| Centraliser la documentation fonctionnelle (avec le studio produit) | Transverse | ⏳ À lancer |
| Évangéliser les équipes du CEPS rencontrées par Victor | Transverse | ⏳ À lancer |

<sub>² Le cadrage est une discussion ; la constitution du référentiel outillé qui en découle est classée déterminante. De même, la « sélection des use cases archi » prévue début septembre a débouché directement sur une orchestration : elle est reclassée déterminante sous ce nom.</sub>

Les 9 déclinaisons à cadrer ne sont pas classées : elles hériteront de l'impact de l'action d'origine une fois engagées.

## Matrice de maturité

Le diagnostic fin qui étaye la [maturité par périmètre](#maturité-par-périmètre) : la matrice mesure **le niveau auquel l'accompagnement a amené chaque fonction d'équipe sur chaque use case**, sur une échelle de 1 à 5 propre aux use cases, distincte de l'échelle d'organisation. Ce n'est pas une note des équipes : le niveau 1 signifie que la fonction démarre tout juste sur ce use case. Un use case non encore observé est noté 1 par convention.

| Niveau | Signification |
|:---:|---|
| **1** | Découverte : la fonction démarre, pas encore de pratique régulière |
| **2** | Expérimentation : pratique ponctuelle, accompagnée, pas encore fiabilisée |
| **3** | Pratique régulière : usage installé dans le quotidien, encore individuel ou dépendant de l'accompagnement |
| **4** | Maîtrise : pratique outillée, reproductible, autonome |
| **5** | Standard d'équipe : pratique mutualisée, mesurée, que l'équipe fait évoluer et diffuse |
| **1 → 3** | Progression apportée depuis le début de l'accompagnement |
| **–** | Non applicable au périmètre |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/05-matrice-dark.svg">
  <img alt="Matrice de maturité IA détaillée par use case et périmètre, détaillée dans le tableau ci-dessous" src="Etat-avancement/assets/05-matrice-light.svg" width="100%">
</picture>

<details>
<summary>Version tableau de la matrice</summary>

| Métier | Use case | Egapro | DACCORD | SIRENA | VAO | Transverse |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Chefs de projet | Piloter un projet développé avec l'IA | 1 → 3 | 1 | 1 | 1 | – |
| Chefs de projet | Générer des tickets de spec | 1 | 1 → 2 | 1 | 1 | – |
| Chefs de projet / Développeurs | Organiser le board (sprints, epics) | 4 | 1 | 1 | 1 | – |
| Designers | Générer des prototypes HTML/JS | 1 → 4 | 1 | 1 | 1 | – |
| Designers | Du prototype à la maquette Figma (DSFR) | – | – | – | – | 1 → 2 |
| Développeurs | Générer du code de qualité | 3 | 3 | 1 | 1 → 2 | – |
| Développeurs | Générer des tests | 4 | 3 | 1 | 1 | – |
| Développeurs | Utiliser des orchestrations | 4 | 1 → 2 | 1 | 1 | – |
| Développeurs | Pré-auditer l'accessibilité | 1 → 2 | 1 | 1 | 1 | – |
| Développeurs | Pré-auditer la sécurité | 1 | 1 | 1 | 1 | – |
| Développeurs | Outils & system prompts communs | 4 | 1 → 2 | 1 | 1 | – |
| Architectes | Générer et vérifier un DA | – | – | – | – | 1 → 2 |
| Architectes | Outiller les référentiels d'architecture | – | – | – | – | 1 |

</details>

## Zoom : coaching développement augmenté, DACCORD (16 juillet)

Session avec les développeurs de l'équipe, couvrant l'ensemble de la chaîne du développement augmenté ([compte rendu](CR/developpeurs/Feedback_Coaching_Devs_DACCORD.docx)) :

- prompt engineering et enjeu de fenêtre de contexte ;
- system prompts : agents, rules, skills ;
- orchestration de subagents et bonnes pratiques avec l'IA ;
- workflow complet : définir un plan, le faire challenger (y compris par l'IA elle-même), en tirer une checklist autoportante en Markdown, implémenter code ou tests, faire valider chaque élément de la checklist avant de changer de phase ou d'instance, puis build et tests.

**Les retours de l'équipe :**

- « la formation a rendu abordable des sujets qui auraient pu être compliqués » ;
- « la formation a été claire », appréciée pour « le côté interactif de la session » et « le fait de pouvoir poser des questions au fur et à mesure » ;
- « les exemples concrets ont aidé à comprendre les concepts » ;
- « le fait de partir du niveau de l'équipe, et qu'on parvienne quand même à la fin à comprendre les orchestrations, tout en ayant le sentiment que c'est atteignable » ;
- « la formation permet de se projeter sur les compétences à acquérir ».

L'élan s'est concrétisé sans attendre : **dès le lundi 20 juillet, les développeurs ont engagé de leur propre initiative la mise en commun de leurs system prompts (agents, rules, skills)**. L'atelier d'amélioration des skills s'est tenu le 6 août, l'accompagnement individuel a suivi, et l'orchestration frontend et backend est aujourd'hui en place.

## Focus par chantier

### Egapro : périmètre pilote

- Le périmètre le plus avancé : **5 use cases au niveau maîtrise (4 sur 5)** (orchestrations, tests, board, outillage commun, prototypes designers). Prochain palier commun : le niveau 5, quand ces pratiques seront mutualisées et mesurées par l'équipe elle-même.
- **3 use cases montés de niveau** depuis le début de l'accompagnement : pilotage de projet (1 → 3), prototypes designers (1 → 4), pré-audit d'accessibilité (1 → 2).
- **Accessibilité : trois chantiers à ne pas confondre** ([compte rendu du 29 juillet](CR/transverse/Avancement%20RGAA_29-07.txt)) : rendre Egapro accessible (acquis : l'audit du code passe de **31 à 16 erreurs**), générer du code accessible (encore adossé au pré-audit), pré-auditer l'accessibilité du code.
- Sur ce dernier point, un [framework de suivi des performances de l'outil](https://github.com/sboukhari-Ippon/RGAA-Tool-Monitoring) a été proposé à Max et Lucas. **Question ouverte pour Gary : qui porte l'outil de pré-audit hors des sprints Egapro et sans reposer sur Max, avec le dispositif de mesure intégré ?** Sans porteur ni mesure, l'outil restera piloté au feeling.

### DACCORD : l'équipe qui monte, côté dev comme côté produit

- **Côté développeurs** : coaching du 16 juillet, mise en commun des system prompts dès le 20 juillet, atelier skills du 6 août ([compte rendu](CR/transverse/daccord-ia-06-08.txt)), accompagnement individuel de Sébastien, Florian puis Sylvain. **L'orchestration frontend et backend est en place**, et les développeurs éprouvent des orchestrations, dont une approche test first sur le frontend qui part des critères d'acceptation du ticket ; la suite est de l'étendre à la documentation et au changelog, et d'ajouter des skills de tests back et front. Sonar et ESLint arrivent : le rail déterministe se construit.
- **Côté PM/PO, formation du 8 septembre** : les PM/PO ont en main un **skill qui les challenge sur la précision de leurs tickets et formalise le ticket entier**, critères d'acceptation compris. La mission leur a fourni un système complet sur poste ministère : OpenCode Desktop et un modèle Albert. Ils le prennent en main ; Olivier Toumsy les forme en parallèle.
- Irritant à lever, côté socle : un forfait trop juste, qui pousse vers des solutions non conformes (budget tokens).
- Le niveau 3 est en vue : il se validera quand skills, orchestration et ticket IA seront la pratique quotidienne, pas seulement disponibles.

### SIRENA : diagnostic complété, demande entrante

- Côté développeurs : usage IA réel mais individuel, sans coordination d'équipe.
- **Côté produit, la cheffe de projet a été rencontrée le 30 juillet** ([compte rendu](CR/products/CDP-SIRENA-30-07.txt)). Aurélie partagera les rôles PM et PO avec Valérie ; l'équipe compte aussi Axelle (design) et Stéphania (recherche utilisateur). Usage de l'IA faible, **sentiment de louper le train de l'IA**.
- **Sa demande est explicite : être formée à l'usage de l'IA pour le PM et le PO**, au-delà de la seule génération de tickets. Créneau à caler. Pistes identifiées avec elle : workflow de conception dans Jira, suivi de la dette technique, questions d'entretiens utilisateurs formulées avec l'IA.

### VAO : formés, la pratique démarre

- **Atelier de développement augmenté tenu le 3 septembre** : les développeurs sont formés, **OpenCode Desktop est installé** sur les postes, la pratique du développement augmenté démarre. Périmètre monté de 1 à 2 sur l'échelle d'organisation.
- Prochaine étape côté dev : un premier ticket livré en développement augmenté, puis le palier 2 (skills et contexte partagés dans le repo).
- Côté produit, **Halim sera accompagné sur la génération de tickets intelligibles via MCP** ; créneau à caler.

### Architectes : de cinq use cases identifiés à une orchestration qui tourne

Chantier ouvert avec Igor le 28 juillet ([intérêt](CR/transverse/Interet_Igor.txt) · [compte rendu](CR/transverse/Igor-28-07.txt)), puis l'atelier DA du 4 août ([compte rendu](CR/transverse/CR_Architectes-atelier-4-08-26.txt)).

- **Première orchestration en place** ([compte rendu](CR/transverse/Archis-orchestration-DA-15-09.txt)) : l'IA vérifie que les fonctionnalités du SI applicatif sont décrites de façon cohérente sur l'ensemble du DA, du contexte aux choix techniques. C'est la réponse à un irritant remonté le 4 août : les incohérences d'un DA rempli à la main sont difficiles à percevoir.
- **Stack légale sur poste ministère** : OpenCode Desktop et DeepSeek V4 Flash servi par Albert. Aucun droit admin nécessaire.
- **Les architectes prennent l'orchestration en main** sur des DA réels pour se familiariser avec cet usage. Le niveau 3 se validera quand ils l'utiliseront en autonomie ; les use cases suivants de la liste du 4 août (cohérence des choix techniques entre eux, écarts entre DA et code réel) viendront ensuite.
- **Igor Ranquin et Nicolas Fournier ont été initiés à l'IA générative** ([compte rendu](CR/transverse/Igor-Nicolas-initiation-IA-15-09.txt)) et veulent mettre les mains dans l'orchestration : accompagnement au retour de congé de Selim, en partant du use case de DA.
- **En fond, le référentiel outillé** : un dépôt de fiches faisant source de vérité, un dépôt de documents de contexte, publication en GitLab Pages, puis une bibliothèque de skills standards validés par les responsables du référentiel. Gouvernance posée par Igor : relecteurs, arbitrage final par lui, ouverture en lecture à tous les consommateurs. Créneau de rapprochement : le jeudi de 14 h à 15 h.
- ⏱️ Les développeurs d'Igor partent en septembre et en octobre : la fenêtre de montée en compétence reste étroite.

### Design : la solution est validée, reste à la rendre agréable

- **Egapro** : grâce aux skills fournis, Raphael **génère plusieurs prototypes HTML avant de maquetter** ([compte rendu](CR/design/Avancement-Design.txt)).
- **Point du 13 août avec Louis** ([compte rendu](CR/design/Louis-13-08.txt)) : démonstration du loop engineering qui contrôle le respect du DSFR et du flux prototype → maquette Figma. Louis valide le use case.
- **Point design et IA du 3 septembre** ([compte rendu](CR/design/DESIGN-3-Septembre.txt)) : **la qualité du passage d'un prototype généré par IA vers une maquette Figma en composants DSFR officiels est validée**, grâce au MCP Figma et à un compte full. Les maquettes sont fidèles au DSFR.
- **La priorité désormais : la boucle de feedback.** Rendre l'expérience agréable quand un designer utilise l'IA, même sans être technophile : les maquettes arrivent dans Figma, le retour du designer relance un nouveau prototype. C'est la dernière condition pour ouvrir l'acculturation à l'ensemble des designers, comme Norman le demandait.
- **Aussi posé le 3 septembre** : mettre à jour le MCP DSFR en 1.15 (pour les charts ; Selim a accès au dépôt), faire le point sur l'alpha 3 du DSFR 2.0 (des briques qui réduisent le besoin de portage, un DSFR plus compatible avec l'IA), explorer Penpot en priorité 2. À noter : SIGeSS, l'équipe pilote de l'usine logicielle, arrive.

### Population produit : PM/PO, POs, recherche utilisateur

- **Point d'adoption IA tenu le 6 août** ([compte rendu](CR/products/Adoption-IA-Products-6-08.txt)) : population hétérogène (coachs, PM/PO, recherche utilisateur), craintes explicites côté RU. **Félix formalise** les use cases, **Olivier liste les équipes prioritaires**.
- **La génération de tickets démarre hors Egapro** : PM/PO DACCORD formés le 8 septembre avec un skill en main (voir le focus DACCORD) ; Aurélie (SIRENA) demandeuse, créneau à caler ; Halim (VAO) à caler.
- **Adrien Chauve a été formé à l'IA générative** ([compte rendu](CR/developpeurs/Adrien-Chauve-formation-IA-Gen-15-09.txt)) : il souhaitait comprendre ce qu'elle apporte au cycle produit, la formation s'est faite par l'apprentissage. Il est identifié, avec Gary, comme porteur possible de la centralisation de la documentation fonctionnelle.
- À suivre : la **centralisation de la documentation fonctionnelle** (un dossier docs, rangé par epic), jugée prioritaire ; l'acculturation des PO, à valider avec Olivier.

### Fondations : postes internes, Bedrock, harness, skills communs

- **Outillage des postes internes : l'enjeu devient la liberté de choix.** Deux voies passent déjà sur poste ministère sans le centre logiciel (OpenCode Desktop sans droits admin, plugin Claude Code dans VS Code). Elles servent désormais aux architectes et aux PM/PO DACCORD, avec un modèle Albert. Pour aller au-delà : packaging par le **centre logiciel** (Olivier introduira la mission auprès de ses gestionnaires ; orientation possible via Céline Liechti) ou compte administrateur temporaire.
- **Bedrock cadré avec AWS (23 juillet)** : large catalogue de modèles accessible en conservant l'observabilité. En attente : liste des modèles et documentation d'observabilité. Cartographie des bénéficiaires des comptes Bedrock prévue fin septembre. Vigilance coûts : les externes conservent leur abonnement Claude, les internes démarreront à environ 20 € par siège plus la consommation au token.
- **Souveraineté et performance** : [bench de coding agentique](Livrables/benchHarness/Bench_Coding-Agentique.pdf) (7 stacks) et support [Souveraineté et performance des modèles et harness](Livrables/Souverainete-Performance/Souverainete-Performance-Modeles-Harness.pdf) livré le 3 septembre. Élargissement aux modèles Bedrock courant septembre, puis bench en conditions réelles.
- **Catalogue de skills partagés à définir**, pour mutualiser entre périmètres ce qui a été éprouvé : skill besoin PO, skill plan technique orienté ATDD, skill dev en ATDD (séparation codeur / testeur), skill refacto adossé à Sonar.
- **Stratégie de déploiement par équipe** : [checklist en quatre paliers](Livrables/Strategie-Deploiement/Checklist-IA-par-equipe.md), validée le 8 septembre, suivie dans le [tableau de bord](Suivi-Strategie-Adoption-IA.html).

### Visibiliser l'accompagnement hors DNUM : le CEPS

Troisième enjeu de la mission : faire connaître le savoir-faire IA du studio Tech de la DNUM au-delà des équipes suivies. Premier terrain, le **CEPS** (Comité économique des produits de santé) :

- **Livré** : veille du Journal officiel sur les spécialités pharmaceutiques **automatisée et restituée en newsletter**, un MVP en 3 jours, **Sabine Lugand satisfaite** ([cadrage](CR/transverse/R%C3%A9alisations-secondaires.txt) · [restitution](CR/transverse/CEPS_Sabine_Lugand.txt)).
- **Passation à Victor Degliame** : rendre la solution utilisable sans Python, intégrer les évolutions demandées.
- **Message à porter aux équipes du CEPS** : l'IA permet de produire vite dès que le besoin est clair ; le besoin, exprimé « avec de l'IA », a d'ailleurs été atteint sans en avoir besoin.

## Livrables à date

| Livrable | Pour qui | Où |
|---|---|---|
| Stratégie de transformation IA (point d'étape) | Direction | [PDF](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) |
| Récit de mission : l'impact de l'adoption IA, en 1 slide et en 3 slides | Direction | [Recit-Mission2](Livrables/Recit-Mission2/) |
| Bench des harness de coding agentique | Direction, tech leads | [PDF](Livrables/benchHarness/Bench_Coding-Agentique.pdf) |
| Souveraineté et performance des modèles et harness | Direction | [PDF](Livrables/Souverainete-Performance/Souverainete-Performance-Modeles-Harness.pdf) |
| Checklist de déploiement IA par équipe (quatre paliers) | Équipes, direction | [Markdown](Livrables/Strategie-Deploiement/Checklist-IA-par-equipe.md) |
| Tableau de bord de suivi (à ouvrir dans un navigateur) | Pilotage | [HTML](Suivi-Strategie-Adoption-IA.html) |
| Matrice d'outillage : qui peut utiliser quoi | Pilotage | [Markdown](Livrables/Outillage/matrice-outillage.md) |

---

<sub>Sources : <code>Etat-avancement.xlsx</code> et <a href="https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement">Grist</a> · graphiques générés par <code>Etat-avancement/build/generate_charts.py</code> (éditer la section DONNÉES puis relancer) · Selim Boukhari, Ippon Technologies</sub>

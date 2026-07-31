# État d'avancement détaillé

Semaine du 27 au 31 juillet 2026 · [← retour à la synthèse](../README.md)

## Plan d'actions

Le cœur du suivi : ce qui a été réalisé, ce qui est en cours, ce qui reste à faire.

### ✅ Réalisées (8)

| Métier | Périmètre | Action | Ce qui a été fait |
|---|---|---|---|
| Développeurs | DACCORD | Former au développement augmenté | Session de coaching du 16 juillet (voir [zoom](#zoom--coaching-développement-augmenté-daccord-16-juillet)) |
| Développeurs | Egapro | Accompagner à la réalisation d'orchestrations | Orchestration « séparation codeur / testeur » en place |
| Chefs de projet | Egapro | Permettre un meilleur suivi d'un projet utilisant l'IA | Estimations en taille de T-shirt sur les tickets ; tickets Design créés pour donner à l'équipe de la visibilité sur la roadmap design et la challenger |
| Designers | Egapro | Accompagner à la génération de prototypes | Skill UX adapté au projet, skill d'audit UX, formation à la réalisation de prototypes de maquettes avec Claude |
| Transverse | Transverse | Benchmark des harness et modèles de coding agentique | [Bench livré](../Livrables/benchHarness/Bench_Coding-Agentique.pdf) : 7 stacks comparées sur prix, performance (SWE-bench), souveraineté et conformité |
| Transverse | Transverse | Cadrer la voie Bedrock avec AWS | [Échange du 23 juillet](../CR/transverse/AWS-Bedrock-23-07-2026.txt) : un large catalogue de modèles est accessible via Bedrock (dont les open-weight chinois) en conservant l'observabilité ; possibilité d'utiliser des modèles moins chers que ceux d'Anthropic, ce qui compte quand on paie au token. AWS revient avec la liste des modèles disponibles et une documentation d'observabilité |
| Architectes | Transverse | Cadrer avec Igor l'outillage des référentiels d'architecture | [Échange du 28 juillet](../CR/transverse/Igor-28-07.txt) : le besoin est posé (les référentiels et les DA vivent sur SharePoint, versions difficiles à tracer, structure jamais à jour, ressaisie d'information), la cible est arrêtée (un dépôt de fiches, un dépôt de documents de contexte construits dessus, publication en GitLab Pages, liens vers la source) et la gouvernance aussi (relecteurs, arbitrage final par Igor, ouverture en lecture aux consommateurs dont la TMA). Contrepartie obtenue : l'appui d'Igor sur l'outillage des postes internes |
| Transverse | Transverse | Livrer au CEPS l'automatisation de la veille du Journal officiel | [Restitution du 30 juillet](../CR/transverse/CEPS_Sabine_Lugand.txt) : Sabine Lugand est satisfaite de l'outil, la newsletter mensuelle sur les spécialités pharmaceutiques est quasi automatisée. La main est passée à Victor Degliame pour la suite (portage hors Python, évolutions demandées) |

### 🔄 En cours (4)

| Métier | Périmètre | Action | Prochaine étape |
|---|---|---|---|
| Développeurs | DACCORD | Adapter les orchestrations Egapro à Jira | Poursuivre l'adaptation, puis la mettre entre les mains de l'équipe |
| Développeurs | Egapro | Piloter le pré-audit d'accessibilité | Un [framework de suivi des performances](https://github.com/sboukhari-Ippon/RGAA-Tool-Monitoring) a été proposé à Max et Lucas ; Lucas partage le besoin de mesurer, Max préfère se concentrer sur l'accessibilité d'Egapro. À arbitrer avec Gary : qui porte l'outil de pré-audit hors des sprints Egapro, avec la mesure intégrée |
| Architectes | Transverse | Constituer le référentiel d'architecture outillé (fiches, documents de contexte, skills) | Récupérer le référentiel auprès de Mathias, produire un premier jet de skills, créer et épurer le dépôt, laisser Igor le compléter, figer une version 0.1, puis embarquer la conformité numérique |
| Chefs de projet | DACCORD | Accompagner la génération de tickets de spec | Accompagner Kahina à son retour de congés, en session commune avec Aurélie (SIRENA), mi-août |

### 📅 Planifiées (10)

| Métier | Périmètre | Action | Échéance |
|---|---|---|---|
| Architectes | Transverse | Atelier de génération de DA avec l'IA | 3 août |
| Transverse | Transverse | Claude Enterprise : discussions avec Software One | Atelier le 3 août |
| Développeurs | DACCORD | Atelier d'amélioration des skills (suite de la mise en commun engagée par l'équipe) | 6 août |
| Chefs de projet | SIRENA | Former Aurélie à l'usage de l'IA pour le PM et le PO, au-delà de la seule génération de tickets | Mi-août, en session commune avec Kahina (DACCORD), à son retour de congés |
| Designers | Transverse | Construire avec Louis la solution de prototypes conformes DSFR (skills anti-hallucination) | Août |
| Transverse | Transverse | Benchmark des modèles et harness, élargi aux modèles disponibles sur Bedrock | Courant août, dès réception de la liste des modèles par AWS |
| Architectes | Transverse | Demi-journée d'acculturation IA avec Igor et les architectes | Fin août, un mardi ou un jeudi |
| Transverse | Transverse | Rencontrer Céline Liechti pour être orientés vers les personnes qui gèrent le centre logiciel, et y faire packager les harness cibles | Dès que le créneau est posé |
| Développeurs | VAO | Atelier de formation au développement augmenté | 8 septembre |
| Transverse | Transverse | Cartographier les bénéficiaires des comptes Bedrock (internes, et externes sur sujets sensibles) | Fin septembre |

### ⏳ À lancer (3)

| Métier | Périmètre | Action | Première étape |
|---|---|---|---|
| Product Owners | Transverse | Former à la fenêtre de contexte et au prompt engineering, présenter un use case | Valider l'intérêt d'une séance d'acculturation IA avec Olivier |
| Designers | Transverse | Session d'acculturation de l'ensemble des designers | Éprouver d'abord la solution de prototypes DSFR construite avec Louis ; c'est la condition posée par Norman pour ouvrir la démarche à tous les designers |
| Transverse | Transverse | Évangéliser les équipes du CEPS rencontrées par Victor | Capitaliser sur le MVP livré à Sabine Lugand : trois jours pour quasi automatiser une newsletter mensuelle, avec un besoin clair |

### 🧭 Déclinaisons à cadrer (10)

Actions déjà éprouvées sur un périmètre, à décliner sur les autres une fois le cadrage fait avec chaque équipe.

| Action | À cadrer sur |
|---|---|
| Former au développement augmenté | SIRENA |
| Accompagner à la réalisation d'orchestrations | SIRENA · VAO |
| Piloter le pré-audit d'accessibilité | DACCORD · SIRENA · VAO |
| Accompagner la génération de tickets de spec | VAO |
| Accompagner à la génération de prototypes | DACCORD · SIRENA · VAO |

## Impact des actions

Toutes les actions ne pèsent pas pareil. Chacune des 25 actions engagées est classée selon ce qu'elle change pour les équipes :

| Impact | Ce que ça recouvre |
|---|---|
| ◆◆◆ **Déterminant** | Du concret dans le quotidien des équipes : skills créés ou challengés, orchestrations, accompagnement de mise en place de solutions |
| ◆◆ **Élevé** | Acculturations et formations : elles changent le regard et amorcent la pratique |
| ◆ **Modéré** | Discussions, cadrages, études, communication : elles préparent le terrain |

### Répartition par équipe

| Chantier | ◆◆◆ Déterminant | ◆◆ Élevé | ◆ Modéré | Total |
|---|:---:|:---:|:---:|:---:|
| Egapro | 4 | – | – | 4 |
| DACCORD | 3 | 1 | – | 4 |
| SIRENA | – | 1 | – | 1 |
| VAO | – | 1 | – | 1 |
| Transverse | 4 | 3 | 8 | 15 |
| **Total** | **11** | **6** | **8** | **25** |

**Lecture** : sur les périmètres actifs, l'accompagnement est presque exclusivement du concret — 7 actions déterminantes sur les 8 actions Egapro et DACCORD. Les actions modérées sont toutes transverses : ce sont les chantiers de fond (bench, Bedrock, outillage) qui conditionnent le passage à l'échelle. La formation PM/PO de mi-août étant une session commune SIRENA · DACCORD, elle est comptée sur SIRENA, où elle a été demandée.

### Le classement, action par action

**◆◆◆ Déterminant (11)**

| Action | Chantier | Statut |
|---|---|---|
| Orchestration « codeur / testeur » en routine | Egapro | ✅ Réalisée |
| Pilotage adapté à l'IA (estimations T-shirt, tickets design) | Egapro | ✅ Réalisée |
| Designers outillés : skills UX, formation prototypes | Egapro | ✅ Réalisée |
| Outil de veille du Journal officiel livré au CEPS | Transverse | ✅ Réalisée |
| Piloter le pré-audit d'accessibilité (framework de monitoring) | Egapro | 🔄 En cours |
| Adapter les orchestrations Egapro à Jira | DACCORD | 🔄 En cours |
| Constituer le référentiel d'architecture outillé (fiches, skills) | Transverse | 🔄 En cours |
| Accompagner la génération de tickets de spec (Kahina) | DACCORD | 🔄 En cours |
| Atelier de génération de DA avec l'IA (3 août) | Transverse | 📅 Planifiée |
| Atelier d'amélioration des skills (6 août) | DACCORD | 📅 Planifiée |
| Solution de prototypes conformes DSFR avec Louis (août) | Transverse | 📅 Planifiée |

**◆◆ Élevé (6)**

| Action | Chantier | Statut |
|---|---|---|
| Coaching développement augmenté du 16 juillet¹ | DACCORD | ✅ Réalisée |
| Formation à l'usage de l'IA pour le PM et le PO (mi-août, session commune avec Kahina) | SIRENA | 📅 Planifiée |
| Demi-journée d'acculturation IA avec Igor et les architectes (fin août) | Transverse | 📅 Planifiée |
| Atelier de formation au développement augmenté (8 septembre) | VAO | 📅 Planifiée |
| Acculturation IA des PO (à valider avec Olivier) | Transverse | ⏳ À lancer |
| Acculturation de l'ensemble des designers | Transverse | ⏳ À lancer |

<sub>¹ Classé par nature (formation), mais son effet a déjà dépassé la catégorie : mise en commun des system prompts engagée par l'équipe dès le lundi suivant, use case monté de niveau.</sub>

**◆ Modéré (8)**

| Action | Chantier | Statut |
|---|---|---|
| Bench des harness et modèles de coding agentique | Transverse | ✅ Réalisée |
| Cadrage de la voie Bedrock avec AWS (23 juillet) | Transverse | ✅ Réalisée |
| Cadrage des référentiels d'architecture avec Igor (28 juillet)² | Transverse | ✅ Réalisée |
| Claude Enterprise : discussions avec Software One (3 août) | Transverse | 📅 Planifiée |
| Bench élargi aux modèles Bedrock (août) | Transverse | 📅 Planifiée |
| Rencontrer Céline Liechti (accès au centre logiciel) | Transverse | 📅 Planifiée |
| Cartographie des bénéficiaires des comptes Bedrock (fin septembre) | Transverse | 📅 Planifiée |
| Évangéliser les équipes du CEPS rencontrées par Victor | Transverse | ⏳ À lancer |

<sub>² Le cadrage est une discussion ; la constitution du référentiel outillé qui en découle est, elle, classée déterminante.</sub>

Les 10 déclinaisons à cadrer ne sont pas classées : elles hériteront de l'impact de l'action d'origine une fois engagées.

## Matrice de maturité

La matrice mesure **le niveau auquel l'accompagnement a amené chaque fonction d'équipe** (par exemple : les designers d'Egapro sur la génération de prototypes), sur une échelle de 1 à 5. Ce n'est pas une note des équipes : le niveau 1 signifie que la fonction démarre tout juste sur ce use case. Un use case non encore observé est noté 1 par convention.

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
  <source media="(prefers-color-scheme: dark)" srcset="assets/05-matrice-dark.svg">
  <img alt="Matrice de maturité IA détaillée par use case et périmètre, détaillée dans le tableau ci-dessous" src="assets/05-matrice-light.svg" width="100%">
</picture>

<details>
<summary>Version tableau de la matrice</summary>

| Métier | Use case | Egapro | DACCORD | SIRENA | VAO | Transverse |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Chefs de projet | Piloter un projet développé avec l'IA | 1 → 3 | 1 | 1 | 1 | – |
| Chefs de projet | Générer des tickets de spec | 1 | 1 | 1 | 1 | – |
| Chefs de projet / Développeurs | Organiser le board (sprints, epics) | 4 | 1 | 1 | 1 | – |
| Designers | Générer des prototypes HTML/JS | 1 → 4 | 1 | 1 | 1 | – |
| Développeurs | Générer du code de qualité | 3 | 3 | 1 | 1 | – |
| Développeurs | Générer des tests | 4 | 3 | 1 | 1 | – |
| Développeurs | Utiliser des orchestrations | 4 | 1 | 1 | 1 | – |
| Développeurs | Pré-auditer l'accessibilité | 1 → 2 | 1 | 1 | 1 | – |
| Développeurs | Pré-auditer la sécurité | 1 | 1 | 1 | 1 | – |
| Développeurs | Outils & system prompts communs | 4 | 1 → 2 | 1 | 1 | – |
| Architectes | Générer un dossier d'architecture (DA) | – | – | – | – | 1 |
| Architectes | Outiller les référentiels d'architecture | – | – | – | – | 1 |

</details>

## Zoom : coaching développement augmenté, DACCORD (16 juillet)

Session avec les développeurs de l'équipe, couvrant l'ensemble de la chaîne du développement augmenté ([compte rendu](../CR/developpeurs/Feedback_Coaching_Devs_DACCORD.docx)) :

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

L'élan s'est concrétisé sans attendre : **dès le lundi 20 juillet, les développeurs ont engagé de leur propre initiative la mise en commun de leurs system prompts (agents, rules, skills)**, de quoi faire monter le use case « outils et system prompts communs » au niveau 2. La mission a proposé une relecture de leurs premiers skills, avant l'**atelier d'amélioration des skills du 6 août** qui ancrera ces pratiques dans le quotidien de l'équipe.

## Focus par chantier

### Egapro : périmètre pilote

- Le périmètre le plus avancé : **5 use cases au niveau maîtrise (4 sur 5)** (orchestrations, tests, board, outillage commun, prototypes designers). Prochain palier commun : le niveau 5, quand ces pratiques seront mutualisées et mesurées par l'équipe elle-même.
- **3 use cases montés de niveau** depuis le début de l'accompagnement : pilotage de projet (1 → 3), prototypes designers (1 → 4), pré-audit d'accessibilité (1 → 2).
- Ce qui a permis ces progressions : estimations T-shirt, tickets design de visibilité, skills UX et formation prototypes, synchronisation des travaux d'accessibilité.
- **Accessibilité, trois chantiers distincts** ([compte rendu du 29 juillet](../CR/transverse/Avancement%20RGAA_29-07.txt)) : rendre Egapro accessible (l'audit du code passe de **31 à 16 erreurs**), générer du code accessible (encore adossé au pré-audit, pas de solution autonome), pré-auditer l'accessibilité du code.
- Sur ce dernier point, un [framework de suivi des performances de l'outil dans le temps](https://github.com/sboukhari-Ippon/RGAA-Tool-Monitoring) a été proposé à Max et Lucas. Lucas partage le besoin de mesurer ; Max, saturé entre trouver la solution et l'instrumenter, préfère se concentrer sur l'accessibilité d'Egapro. **Question ouverte pour Gary : qui porte l'outil de pré-audit hors des sprints Egapro et sans reposer sur Max, avec le dispositif de mesure intégré ?** Sans porteur ni mesure, l'outil restera piloté au feeling.
- Prochain palier : le pré-audit de sécurité (encore en découverte).

### DACCORD : l'équipe qui monte

- Coaching développement augmenté du 16 juillet très bien reçu ; l'équipe se projette vers un haut niveau de maîtrise.
- **Passage à l'acte dès le 20 juillet** : mise en commun des system prompts (agents, rules, skills) engagée par les développeurs de leur propre initiative ; **premier use case DACCORD monté de niveau (1 → 2)**. La mission relit leurs premiers skills.
- **Atelier d'amélioration des skills le 6 août** avec les développeurs, puis suivi de l'intégration et accompagnement à l'orchestration pour les personnes volontaires.
- Les orchestrations éprouvées sur Egapro sont en cours d'adaptation à Jira, pour un transfert direct de savoir-faire entre périmètres.
- Côté chefs de projet, Kahina sera accompagnée à son retour de congés sur la génération de tickets de spec, **mi-août, en session commune avec Aurélie (SIRENA)**.

### SIRENA : diagnostic complété, demande entrante

- Côté développeurs : usage IA réel mais individuel (contexte `.claude` global sur l'application, production et revue de code assistées chez une partie des développeurs), sans coordination d'équipe — outils et documents de contexte non mutualisés, base de contexte exploitée mais non maintenue.
- **Côté produit, la cheffe de projet a été rencontrée le 30 juillet** ([compte rendu](../CR/products/CDP-SIRENA-30-07.txt)). Aurélie a repris le projet en juin après Delphine ; elle partagera les rôles PM et PO avec Valérie (prestataire), les deux tenant les deux rôles. L'équipe compte aussi Axelle (design) et Stéphania (recherche utilisateur).
- Le projet est piloté en mode produit mais ses indicateurs restent projet (coût, délais, qualité). L'usage de l'IA est faible, l'équipe n'a pas de visibilité sur la manière dont ses développeurs s'en servent, et **Aurélie exprime le sentiment de louper le train de l'IA**.
- **Sa demande est explicite : être formée en même temps que Kahina à l'usage de l'IA pour le PM et le PO, mi-août**, avec l'ambition d'aller au-delà de la seule génération de tickets. Engagement de premier ordre : c'est elle qui est demandeuse.
- Pistes identifiées avec elle : automatiser et intégrer des agents, mettre en place un workflow de conception et d'exploration dans Jira, suivre la dette technique, renforcer la communication entre développeurs, et — l'équipe ayant accès aux utilisateurs — **s'appuyer sur l'IA pour formuler les questions auxquelles personne n'aurait pensé** lors des entretiens.
- L'ensemble des use cases est au niveau découverte (les non observés sont notés 1 par convention) : l'image se précisera au cadrage de mi-août.

### VAO : en découverte

- Niveau découverte sur l'ensemble des use cases.
- L'atelier de formation au développement augmenté est fixé au **8 septembre**.

### Transverse : la stratégie en marche

- Stratégie en trois horizons présentée et validée ([support](../Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf)).
- Architectes : atelier de génération de DA le 3 août ; générateurs comparatifs Claude / DeepSeek déjà construits ([réalisations](../Livrables/Realisations_par_metier/Architectes/)).
- **Référentiels d'architecture cadrés avec Igor le 28 juillet** ([intérêt](../CR/transverse/Interet_Igor.txt) · [compte rendu](../CR/transverse/Igor-28-07.txt)) : les référentiels et les DA vivent sur SharePoint, avec les effets connus (versions difficiles à tracer, structure des documents jamais à jour, ressaisie d'information, partage mal maîtrisé). Cible retenue : un dépôt de fiches faisant source de vérité, un dépôt de documents de contexte construits dessus, publiés en GitLab Pages, chaque élément renvoyant vers sa source ; puis une **bibliothèque de skills standards validés par les responsables du référentiel**, pour que la règle d'architecture soit exploitable dans l'IDE au moment où l'on écrit le DA. Gouvernance posée par Igor : relecteurs, arbitrage final par lui, ouverture en lecture à tous les consommateurs (TMA comprise). Il est ouvert sur les documents de contexte à créer et nous invite à y mettre ce qui compte dans notre quotidien.
- Séquence : récupérer le référentiel auprès de Mathias, produire un premier jet de skills, créer et épurer le dépôt, laisser Igor le compléter, figer une version 0.1, puis embarquer la conformité numérique. Le studio d'architecture, qui détient déjà le cadre de cohérence, peut être sollicité en cas de manque. Créneau de rapprochement : le jeudi de 14 h à 15 h, où Igor réunit les architectes. **Contrainte de calendrier : ses développeurs partent en septembre et en octobre.**
- **Outillage des postes internes — le point dur de la mission trouve une piste.** Un agent interne sur poste managé ne peut pas installer un harness. Deux voies : le packaging par le **centre logiciel** (Igor nous invite à rencontrer **Céline Liechti**, qui saura nous orienter vers les bonnes personnes) ou la **demande de compte administrateur temporaire** contresignée par le manager. Côté développeurs, la sécurité s'oriente vers des postes à système libre avec une VM dédiée à la bureautique, la bureautique n'ayant pas vocation à tourner sur un environnement aussi ouvert. Point à vérifier : `npx` semble bloqué, HTTP passe.
- Une **demi-journée d'acculturation IA avec Igor et les architectes est à poser fin août** (un mardi ou un jeudi).
- **Bedrock cadré avec AWS (23 juillet)** : large catalogue de modèles accessible (dont open-weight chinois) en conservant l'observabilité, donc possibilité de modèles moins chers que ceux d'Anthropic (un levier réel quand on paie au token). En attente : liste des modèles disponibles et documentation d'observabilité. Cartographie des bénéficiaires des comptes Bedrock (internes, et externes sur sujets sensibles) prévue fin septembre. Vigilance coûts : les externes peuvent conserver leur abonnement Claude, les internes démarreront à environ 20 € par siège plus la consommation au token (prix du modèle).
- Outillage : discussions Software One sur Claude Enterprise (atelier le 3 août).
- Harness : [bench de coding agentique livré](../Livrables/benchHarness/Bench_Coding-Agentique.pdf) ; élargissement aux modèles Bedrock courant août (dès la liste AWS), puis bench en conditions réelles (scénarios Albert et Claude).
- Designers : solution de prototypes conformes DSFR à construire avec Louis en août ; une fois éprouvée, session d'acculturation de l'ensemble des designers avec l'appui de Norman.
- POs : acculturation IA à valider avec Olivier.
- **Visibilisation hors DNUM (CEPS)** : l'outil de veille du Journal officiel sur les spécialités pharmaceutiques a été livré et **Sabine Lugand est satisfaite** ([compte rendu](../CR/transverse/CEPS_Sabine_Lugand.txt)). La main est passée à Victor Degliame : rendre la solution utilisable par des personnes qui ne peuvent pas installer Python, et intégrer les évolutions demandées. Reste à évangéliser les équipes du CEPS que Victor a rencontrées, avec un argument vérifiable — trois jours pour quasi automatiser une newsletter mensuelle — et un message : l'IA permet de produire vite dès lors que le besoin est clair.

## Livrables à date

| Livrable | Pour qui | Où |
|---|---|---|
| Stratégie de transformation IA (point d'étape) | Direction | [PDF](../Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) |
| Bench des harness de coding agentique | Direction, tech leads | [PDF](../Livrables/benchHarness/Bench_Coding-Agentique.pdf) |
| Kit de configuration dev augmenté (analyse → implémentation → portage Jira) | Développeurs | [tuto-config_Orchestration](../Livrables/Realisations_par_metier/Developpeurs/tuto-config_Orchestration/) |
| Skills de pré-audit RGAA et cyber | Développeurs | [RGAA_et_Cyber](../Livrables/Realisations_par_metier/Developpeurs/RGAA_et_Cyber/) |
| Skill UX projet, skill d'audit UX, use case maquette | Designers | [Designers](../Livrables/Realisations_par_metier/Designers/) |
| Générateurs de dossiers d'architecture (Claude / DeepSeek) | Architectes | [Architectes](../Livrables/Realisations_par_metier/Architectes/) |

---

<sub>Sources : <code>Etat-avancement.xlsx</code> et <a href="https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement">Grist</a> · graphiques générés par <code>build/generate_charts.py</code> (éditer la section DONNÉES puis relancer) · Selim Boukhari, Ippon Technologies</sub>

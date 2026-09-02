# Transformation IA · Ministères sociaux

**Édition du mercredi 2 septembre 2026** · mise à jour hebdomadaire · [le détail, chantier par chantier](Details.md) · [la stratégie (PDF)](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) · [dashboard GitHub](https://github.com/orgs/SocialGouv/projects/198) · [Grist](https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement)

## Ce que l'accompagnement change

Le point de départ constaté à l'arrivée de la mission, ce que chaque fonction sait faire aujourd'hui, et la prochaine étape pour chacune.

| Métier | Point de départ | Aujourd'hui | Prochaine étape |
|---|---|---|---|
| **Architectes** | Aucun intérêt exprimé pour l'IA | Intérêt suscité par notre atelier : **cinq use cases identifiés** | Sélection des use cases et exploration d'un premier cas début septembre · bibliothèque de skills sur les référentiels d'Igor |
| **Développeurs · Egapro** | Des usages IA bons, mais avec un cadre perfectible | Orchestration désormais **sécurisée** : codeur et testeur séparés, le code n'est plus testé par l'agent qui l'a écrit | Amélioration des skills d'orchestration |
| **Développeurs · DACCORD** | Usage et compréhension de l'IA peu matures | L'équipe **a été accompagnée pour monter l'orchestration frontend et backend, elle est désormais en place** | L'étendre à la documentation et au changelog |
| **Chef de projet · Egapro** | Un suivi décalé de la vitesse réelle du dev augmenté, roadmap design invisible | Identification du besoin d'un meilleur **Pilotage, adapté à l'IA** | Chantier d'amélioration dédié |
| **Chefs de projet · DACCORD, SIRENA** | Tickets rédigés à la main, allers-retours entre métier et équipes | **Formation actée** à la génération de tickets Jira sur poste ministère, valeur ajoutée validée | Session DACCORD le 8/09 avec Richard et Noura · SIRENA courant septembre |
| **Designers** | « L'IA a peu de valeur pour nous » | Depuis un poste ministère : **prototypes HTML au DSFR** testables par des utilisateurs, puis **maquette Figma générée** du prototype retenu, DSFR respecté | Industrialiser la solution de prototypes avec Louis, puis acculturer l'ensemble des designers |
| **Poste de travail** | Pas d'IA générative possible sur PC ministère | **Deux voies opérationnelles** : OpenCode Desktop (sans droits admin, clé Albert) · Claude Code dans VS Code (clé api) · [qui peut utiliser quoi](#qui-peut-utiliser-quoi) | Explorer Scaleway et Google Vertex AI · packager les harness cibles au centre logiciel (introduction par Olivier) |

<sub>La dynamique s'étend : VAO entre dans la boucle (atelier dev augmenté le 3 septembre, créneau tickets avec Halim à caler) ; BIO2 (refonte côté santé) rejoindra le suivi au fil de l'eau.</sub>

## Maturité par chantier

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/02-maturite-org-dark.svg">
  <img alt="Maturité d'organisation par périmètre, sur une échelle de 1 à 5 : Egapro progresse de 3 à 4 (orchestrations en routine, organisation maîtrisée) ; DACCORD progresse de 1 à 2 (skills partagés, accompagnement individuel) ; SIRENA à 2 et VAO à 1, sans changement à ce stade ; les architectes progressent de 1 à 2 (premiers use cases IA identifiés à l'atelier DA). Une flèche verte marque la progression apportée par l'accompagnement, un rond blanc l'absence de changement" src="Etat-avancement/assets/02-maturite-org-light.svg" width="100%">
</picture>

**L'échelle** : 1-2 de rien à la découverte de l'IA · 3 des skills utilisés, des use cases pratiqués, une organisation perfectible · 4 des orchestrations, une organisation maîtrisée · 5 orchestrations, volume de cas d'usage (dev et PM/PO), bonnes pratiques renseignées, vrai craft.

→ [La maturité périmètre par périmètre](Details.md#maturité-par-périmètre) · [le diagnostic fin, use case par use case](Details.md#matrice-de-maturité) · [le focus de chaque chantier](Details.md#focus-par-chantier)

### Plan d'actions détaillé

<details>
<summary>Le réalisé et son impact, la suite en cours et planifiée</summary>

**Le réalisé, l'impact en face** : ◆◆◆ du concret livré (skills, orchestrations, solutions) · ◆◆ formation, acculturation · ◆ cadrage, étude, communication.

| ✅ Réalisé | Chantier | Impact | Ce que ça change |
|---|---|:---:|---|
| Orchestration « codeur / testeur » en routine | Egapro | ◆◆◆ | Le code arrive testé par une instance indépendante : la qualité ne repose plus sur la seule relecture humaine |
| Pilotage adapté à l'IA : estimations T-shirt, tickets design | Egapro | ◆◆◆ | Le suivi colle à la vitesse réelle du dev augmenté ; la roadmap design devient visible et challengeable |
| Designer outillé : skills UX, formation prototypes | Egapro | ◆◆◆ | Plusieurs prototypes HTML générés avant de maquetter : le designer se projette au lieu d'itérer à l'aveugle |
| Atelier de génération de DA avec les architectes (4/08) | Transverse | ◆◆◆ | Les architectes repartent acteurs : cinq use cases identifiés par eux-mêmes |
| Atelier d'amélioration des skills (6/08) | DACCORD | ◆◆◆ | Les skills couvrent cinq domaines et s'améliorent en commun, plus chacun dans son coin |
| Coaching développement augmenté (16/07) | DACCORD | ◆◆ | Dès le lundi suivant, les développeurs mettaient leurs system prompts en commun, de leur propre initiative |
| Point design avec Louis : transférer un prototype vers Figma en respectant parfaitement le DSFR (13/08) | Transverse | ◆◆ | Le prototype automatisé permet d'aller plus vite, la maquette Figma en composants DSFR officiels garantit la fiabilité ; Louis valide le use case, condition pour l'échelle : un compte Figma full |
| Benchmark des harness, modèles et providers | Transverse | ◆ | Sept combinaisons comparées en perf / prix / souveraineté / conformité |
| Tableau des outillages collaborateurs | Transverse | ◆ | Exploration des possibilités offertes par les pc du ministères et comparatif avec les possibilités d'outillage des externes |
| Cadrage de la voie Bedrock avec AWS (23/07) | Transverse | ◆ | Possibilité d'outiller en licences Claude (paiement au token) avec de l'observabilité |
| Cadrage des référentiels d'architecture avec Igor (28/07) | Transverse | ◆ | Le référentiel outillé, en construction, part sur des bases partagées |
| Point d'adoption IA population produit (6/08) | Transverse | ◆ | Les use cases RU et PM / PO se formalisent ; VAO et BIO2 entrent dans le suivi |

<sub>Sur les périmètres actifs, l'impact est presque exclusivement du concret ; les actions modérées sont toutes transverses : les chantiers de fond qui conditionnent le passage à l'échelle.</sub>

<sub>S'y ajoutent les déclinaisons des actions éprouvées, à cadrer sur DACCORD, SIRENA et VAO.</sub>

→ [Le plan d'actions commenté, action par action](Details.md#plan-dactions) · [l'impact de chaque action, y compris à venir](Details.md#impact-des-actions)

</details>

## Roadmap

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/04-roadmap-dark.svg">
  <img alt="Jalons : coaching dev augmenté DACCORD réalisé le 16 juillet ; du 28 au 30 juillet, cadrage des référentiels d'architecture avec Igor, rencontre de la cheffe de projet SIRENA et livraison de l'outil CEPS ; atelier DA avec les architectes réalisé le 4 août ; atelier skills DACCORD et point d'adoption IA produit réalisés le 6 août ; point design avec Louis réalisé le 13 août, prototypes DSFR fiabilisés et flux vers Figma ; jeudi 3 septembre, atelier dev augmenté VAO et point design et IA (du prototype à la maquette Figma respectant le DSFR) ; début septembre, sélection des use cases archi et exploration d'un premier cas ; mardi 8 septembre, formation PM/PO DACCORD ; mercredi 9 septembre, demi-journée d'acculturation IA avec Igor et les architectes ; cartographie des bénéficiaires des comptes Bedrock fin septembre. Formation PM/PO SIRENA courant septembre ; restent à dater : le catalogue de skills partagés et le bench élargi aux modèles Bedrock" src="Etat-avancement/assets/04-roadmap-light.svg" width="100%">
</picture>

## La cible : l'usine logicielle

Un des objectifs de l'accompagnement : une usine logicielle où chaque étape du cycle combine deux rails — un rail agentique qui génère, un rail déterministe qui vérifie. L'agent propose, la règle prouve, l'humain valide. Une équipe pilote est identifiée : **SIGeSS**.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/08-usine-dark.svg">
  <img alt="Usine logicielle cible : à chaque étape (product, design, build, livraison), deux rails. Le rail agentique génère : challenge par l'IA de la clarté du besoin, formalisation et critères d'acceptation ; prototypes basés sur le design system ; génération de code, tests, revue et recette assistée par agent ; notes de version, changelog et documentation automatisée. Le rail déterministe vérifie : formatage des specs et Definition of Ready ; respect du design system et audit d'accessibilité ; pipeline CI avec formatage, tests, couverture Sonar et review humaine ; validation humaine de la livraison" src="Etat-avancement/assets/08-usine-light.svg" width="100%">
</picture>

### Son pilotage : un tableau de bord adossé à DORA

Une usine ne vaut que si l'on mesure ce qu'elle change : chaque indicateur sera lu **avant / après** pour isoler l'apport de l'IA. Le socle est DORA (référentiel DevOps reconnu), complété de trois axes propres au contexte : coût, adoption IA, risque.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/09-tdb-dora-dark.svg">
  <img alt="Tableau de bord adossé à DORA : vitesse avec le cycle time et le débit à effectif constant (GitHub et Jira) ; qualité avec les régressions et le rétablissement, la couverture et la dette (SonarQube), l'exhaustivité de la documentation (audit des repos GitHub) ; coût par fonctionnalité en tokens consommés auprès du provider d'IA plus temps de review ; adoption IA avec l'usage réel mesuré par l'observabilité du provider d'IA, la maturité d'équipe sur une échelle de 1 à 5 et le gain de temps perçu par questionnaire ; risque avec la conformité d'usage à la charte face au shadow IT. Sources outillées pour l'essentiel, expertise structurée pour la maturité, déclaratif corroboratif pour le gain perçu" src="Etat-avancement/assets/09-tdb-dora-light.svg" width="100%">
</picture>

## Outillage

L'outillage se joue sur trois plans :

- **ce que valent les stacks** : performance, prix, souveraineté, conformité ;
- **ce que chaque population peut installer**, selon le poste et le statut du collaborateur ;
- **la voie d'accès aux modèles**, qui conditionne l'observabilité et la liberté de choisir son harness.

À ce stade, deux voies passent pour toutes les populations : OpenCode Desktop et VS Code avec le plugin Claude Code, adossés à Bedrock / Scaleway ou Albert.

### Ce que dit le bench

<details>
<summary>Le comparatif des sept stacks : performance, prix, souveraineté, conformité</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/06-bench-dark.svg">
  <img alt="Comparaison de 7 stacks sur trois mesures de performance : DeepSWE v1.1 en principal (capacité agentique du modèle seul, harness fixé mini-swe-agent, leaderboard officiel Datacurve), Terminal-Bench 2.1 en agentique, et SWE-bench Verified conservé en baseline grisée (saturé, chiffres surtout éditeurs, harness hétérogènes). DeepSWE : Claude Code avec Opus 5 via Bedrock à 74 % (plus ou moins 4), Fable 5 à 70 % (plus ou moins 4), OpenCode avec Kimi K3 via OpenRouter à environ 69 %, Sonnet 5 à 54 % (plus ou moins 4), DeepSeek V4 Flash 0731 via Scaleway à 53 % au leaderboard Datacurve (54,4 % auto-rapporté), GLM 5.2 via Scaleway à 44 %, DeepSeek V4 Flash preview via Albert à 7,3 % auto-rapporté (checkpoint à confirmer auprès de la DINUM). Terminal-Bench : Opus 5 89,1 % mesuré par Artificial Analysis, Kimi K3 88,3 % auto-rapporté (80,9 % mesuré par vals.ai), Fable 5 83,8 % au leaderboard officiel, DeepSeek 0731 82,7 % auto-rapporté, GLM 81 % auto-rapporté, Sonnet 5 80,4 % annoncé par l'éditeur (74,6 % au leaderboard officiel), DeepSeek preview 61,8 % auto-rapporté. SWE-bench Verified en baseline : Opus 5 96 % annoncé par l'éditeur et 97 % mesuré par vals.ai, Fable 5 95 % annoncé, Kimi K3 93,4 % mesuré par vals.ai, Sonnet 5 85,2 % (agrégat llm-stats), DeepSeek preview 73,7 % auto-rapporté, non publié pour DeepSeek 0731 et GLM. Prix entrée / sortie par million de tokens : gratuit via Albert ; 0,40 et 0,80 € pour DeepSeek 0731 via Scaleway ; 1,80 et 5,50 € pour GLM via Scaleway ; 2 et 10 $ pour Sonnet 5 ; 2,55 et 12,75 $ pour Kimi K3 ; 5 et 25 $ pour Opus 5 ; 10 et 50 $ pour Fable 5. Souveraineté : Albert (SecNumCloud, État français) et Scaleway (cloud français) tiennent ; Bedrock est non souverain (CLOUD Act). Conformité RGPD bonne via Bedrock (région UE), Scaleway et Albert ; insuffisante via OpenRouter" src="Etat-avancement/assets/06-bench-light.svg" width="100%">
</picture>

- **Lire la performance** : **DeepSWE v1.1 en principal** — la capacité agentique du modèle seul, à harness fixé (mini-swe-agent, leaderboard officiel Datacurve), donc indépendante du harness Claude Code / OpenCode ; Terminal-Bench 2.1 en agentique ; SWE-bench Verified conservé en simple baseline (saturé en haut de tableau, chiffres majoritairement éditeurs aux harness hétérogènes). Toute case sans donnée est « non publié » — aucun chiffre estimé.
- **La ligne DeepSeek est dédoublée** : Scaleway sert le checkpoint **0731** (DeepSWE 53 % au leaderboard Datacurve, 54,4 % auto-rapporté), Albert sert a priori la **preview d'avril** (DeepSWE 7,3 % auto-rapporté — checkpoint à confirmer auprès de la DINUM). Même nom, mais des performances agentiques sans rapport.
- **Souveraineté (au sens CNIL)** : deux voies tiennent — **Albert (DINUM)**, SecNumCloud et utilisable avec OpenCode ([guide officiel](https://guides.ia.numerique.gouv.fr/albert-api/guides/ide#agentic-coding-opencode)), et **Scaleway** (cloud français, DeepSeek V4 Flash 0731 à 0,40 / 0,80 € et GLM 5.2 à 1,80 / 5,50 € le million de tokens, via OpenCode). **Bedrock n'est pas souverain** : CLOUD Act, quelle que soit la région.
- **Conformité RGPD** : Bedrock en région UE (DPA AWS) reste une voie valable pour les modèles Anthropic — **Opus 5** (DeepSWE 74 %, tête du bench, à moitié prix de Fable), **Fable 5** (70 %) et **Sonnet 5** (54 %, l'entrée de gamme) ; Scaleway et Albert conformes ; **OpenRouter sans garanties** — à réserver éventuellement aux externes.
- **Voie Bedrock précisée avec AWS (23/07)** ([compte rendu](CR/transverse/AWS-Bedrock-23-07-2026.txt)) : large catalogue de modèles (dont open-weight chinois) en conservant l'observabilité — de quoi envisager moins cher qu'Anthropic. En attente : liste des modèles et documentation d'observabilité.
- **Prochaines étapes** : bench élargi aux modèles Bedrock (courant septembre), puis bench en conditions réelles (Albert / DeepSeek V4 Flash via OpenCode face à Claude). [Le support complet (PDF)](Livrables/benchHarness/Bench_Coding-Agentique.pdf) compare les 7 stacks et recommande selon la priorité.

> [!WARNING]
> **Le coût ne se pose pas pareil pour les externes et les internes.** Les externes peuvent rester sur leur abonnement Claude (forfait, consommation incluse). Les internes démarreront à environ 20 € par siège, **plus chaque token consommé au prix du modèle** : leur coût suivra l'usage — d'où l'enjeu du bench pour les internes et la CI/CD.

</details>

### Qui peut utiliser quoi

<details>
<summary>La matrice harness × population : ce qu'il est possible d'installer</summary>

Le bench dit ce que vaut chaque stack ; cette matrice dit ce qu'il est possible d'installer, population par population : 🟢 possible · 🟠 possible mais non conforme · 🔴 impossible · ⏳ à instruire.

| Harness + fournisseur de modèles | Internes · Windows | Internes · Linux | Internes · Mac | Externes · non confidentiel | Externes · confidentiel |
|---|:---:|:---:|:---:|:---:|:---:|
| **OpenCode Desktop + Bedrock / Scaleway ou Albert** | 🟢 | ⏳ | 🟢 | 🟢 | 🟢 |
| **VS Code (plugin Claude Code) + Bedrock / Scaleway ou Albert** | 🟢 | ⏳ | 🟢 | 🟢 | 🟢 |
| OpenCode Desktop + modèles gratuits | 🟠 | ⏳ | 🟠 | 🟠 | 🟠 |
| VS Code (plugin Claude Code) + clé personnelle | 🟠 | ⏳ | 🟠 | 🟠 | 🟠 |
| Claude Desktop + Bedrock / Scaleway | 🔴 | ⏳ | 🟠 | 🟠 | 🟠 |
| Claude Desktop + clé personnelle | 🔴 | ⏳ | 🟠 | 🟠 | 🟠 |
| Codex + Bedrock / Scaleway | 🔴 | ⏳ | 🟠 | 🟠 | 🟠 |
| Codex + clé personnelle | 🔴 | ⏳ | 🟠 | 🟠 | 🟠 |

Tout le reste bute sur le poste interne (Claude Desktop et Codex, impossibles sur Windows) ou sur la conformité (clés personnelles, modèles gratuits).

<sub>Poste Linux interne : faisabilité à instruire. Matrice de travail : [Livrables/Outillage/matrice-outillage.md](Livrables/Outillage/matrice-outillage.md).</sub>

</details>

### Trois voies d'accès aux modèles

<details>
<summary>Bedrock exploré : viable, mais il impose Claude Code · Scaleway et Google Vertex AI à explorer</summary>

L'exploration avec AWS a validé une solution viable : Claude Code adossé à l'observabilité Bedrock (usage et coûts suivis). Mais cette voie verrouille le choix du harness, d'où deux pistes à instruire.

| Fournisseur | Ce qu'il apporte | Le point à lever | Où on en est |
|---|---|---|---|
| **AWS Bedrock** | Claude Code avec observabilité complète · région UE · large catalogue de modèles | L'observabilité est adossée à Claude Code : le harness est imposé | ✅ Exploré avec AWS ([CR du 23/07](CR/transverse/AWS-Bedrock-23-07-2026.txt)) : viable |
| **Scaleway** | Des modèles open-weight intéressants · souveraineté française | Valider le champ des possibles côté observabilité | 🔍 À explorer |
| **Google Vertex AI** | Un accès à des modèles frontier de plusieurs éditeurs (à confirmer) | Vérifier l'observabilité depuis n'importe quel harness | 🔍 À explorer |

**Pourquoi chercher au-delà de Bedrock** : imposer Claude Code n'est pas neutre. Ce harness est très gourmand en contexte : taillé pour les modèles frontier, il risque de moins bien fonctionner avec les modèles moins onéreux (open-weight chinois notamment). La cible : une observabilité indépendante du harness, pour choisir librement le couple harness × modèle selon la tâche et le budget.

</details>

## ⚖️ Décisions attendues

| Décision | Ce qui est en jeu | Qui tranche, quand |
|---|---|---|
| **Porteur du pré-audit d'accessibilité** : hors des sprints, sans reposer sur Egapro, avec la mesure intégrée | Sans porteur ni mesure, l'outil restera piloté au feeling | **Gary** · arbitrage attendu |
| **Accès au centre logiciel** pour y packager les harness cibles | Deux voies passent déjà pour les internes ([la matrice](#qui-peut-utiliser-quoi)) : l'enjeu est la **liberté du choix du harness** | **Les personnes du centre logiciel** · introduction par Olivier à venir |
| **Stack des agents internes, et des externes sur sujets confidentiels** | Trouver la formule optimale en rapport qualité / prix, au plus près des exigences de souveraineté et de légalité | À instruire après le [bench élargi aux modèles Bedrock](#ce-que-dit-le-bench) (courant septembre) et les [explorations Scaleway / Vertex AI](#trois-voies-daccès-aux-modèles) |

## Repères

- [Details.md](Details.md) : plan d'actions commenté, maturité par périmètre, impact action par action, matrice complète, focus par chantier
- [Stratégie de transformation IA (PDF)](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) : enjeux, exploration, plan d'action en trois horizons
- [Réalisations par métier](Livrables/Realisations_par_metier/) : skills, kits de configuration, tutoriels, générateurs de DA
- Pilotage : [dashboard GitHub](https://github.com/orgs/SocialGouv/projects/198) · [état d'avancement Grist](https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement)

---

<sub>Mission Ippon Technologies · Selim Boukhari (sboukhari@ippon.fr) · graphiques régénérés chaque semaine via <code>Etat-avancement/build/generate_charts.py</code></sub>

# Transformation IA · Ministères sociaux

**Édition du mardi 15 septembre 2026** · mise à jour hebdomadaire · [le détail, chantier par chantier](Details.md) · [tableau de bord de suivi](Suivi-Strategie-Adoption-IA.html) · [la stratégie (PDF)](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) · [dashboard GitHub](https://github.com/orgs/SocialGouv/projects/198) · [Grist](https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement)

## Ce que l'accompagnement change

Le point de départ constaté à l'arrivée de la mission, ce que chaque fonction sait faire aujourd'hui, et la prochaine étape pour chacune.

| Fonction | Point de départ | Aujourd'hui | Prochaine étape |
|---|---|---|---|
| **Architectes** | Aucun intérêt exprimé pour l'IA | **Une première orchestration tourne** : l'IA vérifie que les fonctionnalités du SI applicatif sont décrites de façon cohérente sur tout le DA. Les architectes la prennent en main (OpenCode Desktop, DeepSeek V4 Flash via Albert) | Autonomie sur ce use case, puis le suivant · bibliothèque de skills sur les référentiels d'Igor |
| **Igor Ranquin · Nicolas Fournier** | Pas de pratique de l'IA générative | **Initiés à l'IA générative** ; ils veulent mettre les mains dans l'orchestration | Accompagnement à une première orchestration au retour de congé de Selim |
| **Développeurs · Egapro** | Des usages IA bons, mais avec un cadre perfectible | Orchestration **sécurisée** : codeur et testeur séparés, le code n'est plus testé par l'agent qui l'a écrit | Amélioration des skills d'orchestration |
| **Développeurs · DACCORD** | Usage et compréhension de l'IA peu matures | **Orchestration frontend et backend en place**, montée avec l'équipe · les développeurs **éprouvent des orchestrations**, dont une approche **test first sur le frontend**, qui part des critères d'acceptation du ticket | L'étendre à la documentation et au changelog · skills de tests |
| **Développeurs · VAO** | Pas de développement augmenté | **Formés le 3 septembre, OpenCode Desktop installé**, la pratique démarre | Un premier ticket livré en dev augmenté · tickets avec Halim |
| **Chef de projet · Egapro** | Un suivi décalé de la vitesse réelle du dev augmenté, roadmap design invisible | **Pilotage adapté à l'IA** : estimations T-shirt, tickets design visibles | Chantier d'amélioration dédié |
| **PM/PO · DACCORD** | Tickets rédigés à la main, allers-retours entre métier et équipes | **Formés le 8 septembre**, un skill en main qui challenge la précision du ticket et le formalise, critères d'acceptation compris (OpenCode Desktop + Albert) · formations d'Olivier Toumsy en parallèle | Prise en main au quotidien : le ticket IA devient la norme · SIRENA : formation d'Aurélie à caler |
| **Designers** | « L'IA a peu de valeur pour nous » | **Qualité validée le 3 septembre** : du prototype généré par IA à la maquette Figma en composants DSFR officiels (MCP Figma, compte full) | Une boucle de feedback qui rende l'usage agréable, y compris pour les designers non technophiles |
| **Poste de travail** | Pas d'IA générative possible sur PC ministère | **Deux voies opérationnelles**, déjà utilisées par les architectes et les PM/PO : OpenCode Desktop (sans droits admin, modèle Albert) · Claude Code dans VS Code · [qui peut utiliser quoi](#qui-peut-utiliser-quoi) | Explorer Scaleway et Google Vertex AI · packager les harness cibles au centre logiciel |

<sub>Également formé à l'IA générative, par la pratique : Adrien Chauve, qui voulait comprendre ce qu'elle apporte au cycle produit.</sub>

## Maturité par chantier

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/02-maturite-org-dark.svg">
  <img alt="Maturité d'organisation par périmètre, sur une échelle de 1 à 5 : Egapro progresse de 3 à 4 (orchestrations en routine, organisation maîtrisée) ; DACCORD progresse de 1 à 2 (orchestration en place, PM/PO formés) ; SIRENA à 2 sans changement ; VAO progresse de 1 à 2 (développeurs formés, OpenCode installé) ; les architectes progressent de 1 à 2 (première orchestration de DA en prise en main) ; les designers progressent de 1 à 2 (du prototype à la maquette Figma DSFR, qualité validée). Une flèche verte marque la progression apportée par l'accompagnement, un rond blanc l'absence de changement" src="Etat-avancement/assets/02-maturite-org-light.svg" width="100%">
</picture>

**L'échelle** : 1-2 de rien à la découverte de l'IA · 3 des skills utilisés, des use cases pratiqués, une organisation perfectible · 4 des orchestrations, une organisation maîtrisée · 5 orchestrations, volume de cas d'usage (dev et PM/PO), bonnes pratiques renseignées, vrai craft.

Trois périmètres sont en prise en main (architectes, PM/PO DACCORD, développeurs VAO) : leur niveau 3 se validera à l'usage quotidien, pas à la sortie de l'atelier.

→ [La maturité périmètre par périmètre](Details.md#maturité-par-périmètre) · [le diagnostic fin, use case par use case](Details.md#matrice-de-maturité) · [le focus de chaque chantier](Details.md#focus-par-chantier)

### Plan d'actions détaillé

<details>
<summary>Le réalisé et son impact, la suite en cours et planifiée</summary>

**Le réalisé, l'impact en face** : ◆◆◆ du concret livré (skills, orchestrations, solutions) · ◆◆ formation, acculturation · ◆ cadrage, étude, communication.

| ✅ Réalisé | Chantier | Impact | Ce que ça change |
|---|---|:---:|---|
| Première orchestration de DA : cohérence des fonctionnalités sur tout le DA | Transverse | ◆◆◆ | Les incohérences d'un DA, difficiles à percevoir à la main, sont détectées par l'IA ; les architectes passent de use cases identifiés à un use case qui tourne |
| Du prototype IA à la maquette Figma DSFR : qualité validée (3/09) | Transverse | ◆◆◆ | Le designer teste plusieurs prototypes puis obtient une maquette en composants DSFR officiels : plus d'interprétation du design system |
| Formation des PM/PO et skill de tickets remis (8/09) | DACCORD | ◆◆◆ | Le ticket est challengé et formalisé par l'IA, critères d'acceptation compris : moins d'allers-retours avec les développeurs |
| Orchestration « codeur / testeur » en routine | Egapro | ◆◆◆ | Le code arrive testé par une instance indépendante : la qualité ne repose plus sur la seule relecture humaine |
| Pilotage adapté à l'IA : estimations T-shirt, tickets design | Egapro | ◆◆◆ | Le suivi colle à la vitesse réelle du dev augmenté ; la roadmap design devient visible et challengeable |
| Designer outillé : skills UX, formation prototypes | Egapro | ◆◆◆ | Plusieurs prototypes HTML générés avant de maquetter : le designer se projette au lieu d'itérer à l'aveugle |
| Atelier de génération de DA avec les architectes (4/08) | Transverse | ◆◆◆ | Les architectes repartent acteurs : cinq use cases identifiés par eux-mêmes |
| Atelier d'amélioration des skills (6/08) | DACCORD | ◆◆◆ | Les skills couvrent cinq domaines et s'améliorent en commun, plus chacun dans son coin |
| Outil de veille du Journal officiel livré au CEPS | Transverse | ◆◆◆ | Une newsletter mensuelle quasi automatisée en trois jours : la preuve, hors DNUM, que l'IA livre vite sur un besoin clair |
| Atelier de développement augmenté (3/09) | VAO | ◆◆ | L'équipe est formée, OpenCode Desktop installé, la pratique démarre |
| Initiation à l'IA générative d'Igor Ranquin et Nicolas Fournier | Transverse | ◆◆ | Les deux veulent passer à l'orchestration |
| Formation à l'IA générative d'Adrien Chauve | Transverse | ◆◆ | L'apport de l'IA sur le cycle produit, constaté par la pratique |
| Coaching développement augmenté (16/07) | DACCORD | ◆◆ | Dès le lundi suivant, les développeurs mettaient leurs system prompts en commun, de leur propre initiative |
| Point design avec Louis : du prototype à Figma en respectant le DSFR (13/08) | Transverse | ◆◆ | Louis valide le use case ; la condition posée (un compte Figma full) est levée depuis |

<sub>Cinq actions de cadrage (◆) complètent le réalisé : bench des stacks, voie Bedrock avec AWS, Claude Enterprise avec Software One, référentiels d'architecture avec Igor, point d'adoption IA produit.</sub>

**La suite**

| | |
|---|---|
| 🔄 **En cours** | Prise en main par les équipes : orchestration de DA (architectes), skill de tickets (PM/PO DACCORD), dev augmenté (VAO) · boucle de feedback des designers · orchestrations éprouvées par les développeurs DACCORD (dont test first depuis les critères d'acceptation, frontend) · pré-audit d'accessibilité Egapro · référentiel d'architecture outillé |
| 📅 **Planifié** | Première orchestration avec Igor et Nicolas (au retour de congé) · formation PM/PO SIRENA (à caler) · bench élargi aux modèles Bedrock · catalogue de skills communs · centre logiciel · cartographie des comptes Bedrock (fin septembre) · MCP DSFR 1.15 et alpha 3 du DSFR 2.0 |
| ⏳ **À lancer** | Tickets avec Halim (VAO) · acculturation des PO et de l'ensemble des designers · documentation fonctionnelle centralisée · CEPS |

→ [Le plan d'actions commenté, action par action](Details.md#plan-dactions) · [l'impact de chaque action](Details.md#impact-des-actions)

</details>

## Roadmap

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/04-roadmap-dark.svg">
  <img alt="Jalons, du 13 juillet à fin octobre 2026 : coaching dev augmenté DACCORD réalisé le 16 juillet ; du 28 au 30 juillet, référentiels d'architecture avec Igor, cheffe de projet SIRENA, CEPS ; atelier DA avec les architectes le 4 août ; atelier skills DACCORD et point produit IA le 6 août ; point design avec Louis le 13 août ; le 3 septembre, développement augmenté VAO et validation du passage prototype vers Figma côté design ; les 8 et 9 septembre, formation PM/PO DACCORD et acculturation IA d'Igor et Nicolas ; mi-septembre, orchestration de DA en prise en main par les architectes. À venir : cartographie des comptes Bedrock fin septembre ; au retour de congé, orchestration avec Igor et Nicolas. À caler : formation PM/PO SIRENA, catalogue de skills, bench Bedrock, MCP DSFR 1.15" src="Etat-avancement/assets/04-roadmap-light.svg" width="100%">
</picture>

## La cible : l'usine logicielle

Une usine logicielle où chaque étape du cycle combine deux rails : un rail agentique qui génère, un rail déterministe qui vérifie. L'agent propose, la règle prouve, l'humain valide. Équipe pilote identifiée : **SIGeSS**. La [checklist de déploiement par équipe](Livrables/Strategie-Deploiement/Checklist-IA-par-equipe.md) décline cette cible en quatre paliers, suivis dans le [tableau de bord](Suivi-Strategie-Adoption-IA.html).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/08-usine-dark.svg">
  <img alt="Usine logicielle cible : à chaque étape (product, design, build, livraison), deux rails. Le rail agentique génère : challenge par l'IA de la clarté du besoin, formalisation et critères d'acceptation ; prototypes basés sur le design system ; génération de code, tests, revue et recette assistée par agent ; notes de version, changelog et documentation automatisée. Le rail déterministe vérifie : formatage des specs et Definition of Ready ; respect du design system et audit d'accessibilité ; pipeline CI avec formatage, tests, couverture Sonar et review humaine ; validation humaine de la livraison" src="Etat-avancement/assets/08-usine-light.svg" width="100%">
</picture>

### Le cycle produit, skill par skill

Cinq skills, du besoin au code livré : chacun part des standards de l'équipe (le contexte), parle aux outils par MCP et produit l'artefact qui alimente le suivant. Le [détail skill par skill](Livrables/Strategie-Deploiement/Cycle-produit-IA.md) précise ce que fait l'agent, ce que décide l'humain, le contexte, les MCP et la sortie de chacun.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Livrables/Strategie-Deploiement/assets/cycle-produit-ia-dark.svg">
  <img alt="Le cycle produit augmenté par l'IA, cinq skills en colonnes. Responsable produit : /plan challenge la précision du besoin, rédige le ticket au standard de l'équipe et propose les critères d'acceptation ; l'humain répond aux questions et valide ; MCP Jira ; sortie : un ticket Jira précis avec ses critères d'acceptation. Designer : /prototype génère un prototype DSFR selon les standards UX et UI, montré aux utilisateurs (MCP DSFR) ; /maquette pousse le prototype validé dans Figma en composants DSFR officiels (MCP Figma), l'humain valide les maquettes. Développeur : /plan-tech lit le ticket et, au besoin, les maquettes dans Figma (MCP Figma), écrit le plan d'implémentation et la revue d'impact sur le code, l'humain tranche les choix techniques (MCP Jira, Figma et DSFR) ; /implementation implémente phase par phase avec des agents codeur et testeur séparés, pose le code et les tests, s'arrête si un test casse sans être prévu, passe une quality gate RGAA, qualité et build avant commit (MCP Jira, Figma, DSFR et Playwright) ; sortie : le code et les tests. Soutiens à la production, sous /implementation seulement : pendant l'implémentation, ESLint dans l'IDE et quality gate avant commit ; après le commit, CI/CD avec Sonar, pré-audit RGAA poussé et revue de code supplémentaire au besoin" src="Livrables/Strategie-Deploiement/assets/cycle-produit-ia-light.svg" width="100%">
</picture>

### Son pilotage : un tableau de bord adossé à DORA

Chaque indicateur sera lu **avant / après** pour isoler l'apport de l'IA. Le socle est DORA, complété de trois axes propres au contexte : coût, adoption IA, risque.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/09-tdb-dora-dark.svg">
  <img alt="Tableau de bord adossé à DORA : vitesse avec le cycle time et le débit à effectif constant (GitHub et Jira) ; qualité avec les régressions et le rétablissement, la couverture et la dette (SonarQube), l'exhaustivité de la documentation ; coût par fonctionnalité en tokens consommés plus temps de review ; adoption IA avec l'usage réel mesuré par l'observabilité du provider, la maturité d'équipe sur une échelle de 1 à 5 et le gain de temps perçu ; risque avec la conformité d'usage à la charte" src="Etat-avancement/assets/09-tdb-dora-light.svg" width="100%">
</picture>

## Outillage

Trois plans : **ce que valent les stacks** (performance, prix, souveraineté, conformité), **ce que chaque population peut installer**, et **la voie d'accès aux modèles**, qui conditionne l'observabilité et la liberté de choisir son harness. Deux voies passent aujourd'hui pour toutes les populations : OpenCode Desktop et VS Code avec le plugin Claude Code, adossés à Albert, Bedrock ou Scaleway.

### Ce que dit le bench

<details>
<summary>Le comparatif des sept stacks : performance, prix, souveraineté, conformité</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/06-bench-dark.svg">
  <img alt="Comparaison de 7 stacks sur trois mesures de performance : DeepSWE v1.1 en principal (capacité agentique du modèle seul, harness fixé mini-swe-agent, leaderboard officiel Datacurve), Terminal-Bench 2.1 en agentique, et SWE-bench Verified conservé en baseline grisée. DeepSWE : Claude Code avec Opus 5 via Bedrock à 74 % (plus ou moins 4), Fable 5 à 70 % (plus ou moins 4), OpenCode avec Kimi K3 via OpenRouter à environ 69 %, Sonnet 5 à 54 % (plus ou moins 4), DeepSeek V4 Flash 0731 via Scaleway à 53 % (54,4 % auto-rapporté), GLM 5.2 via Scaleway à 44 %, DeepSeek V4 Flash preview via Albert à 7,3 % auto-rapporté (checkpoint à confirmer auprès de la DINUM). Terminal-Bench : Opus 5 89,1 % mesuré par Artificial Analysis, Kimi K3 88,3 % auto-rapporté (80,9 % mesuré par vals.ai), Fable 5 83,8 % officiel, DeepSeek 0731 82,7 % auto-rapporté, GLM 81 % auto-rapporté, Sonnet 5 80,4 % annoncé (74,6 % officiel), DeepSeek preview 61,8 % auto-rapporté. SWE-bench Verified en baseline : Opus 5 96 % annoncé et 97 % vals.ai, Fable 5 95 % annoncé, Kimi K3 93,4 % vals.ai, Sonnet 5 85,2 % (agrégat llm-stats), DeepSeek preview 73,7 % auto-rapporté, non publié pour DeepSeek 0731 et GLM. Prix entrée / sortie par million de tokens : gratuit via Albert ; 0,40 et 0,80 € pour DeepSeek 0731 via Scaleway ; 1,80 et 5,50 € pour GLM via Scaleway ; 2 et 10 $ pour Sonnet 5 ; 2,55 et 12,75 $ pour Kimi K3 ; 5 et 25 $ pour Opus 5 ; 10 et 50 $ pour Fable 5. Souveraineté : Albert (SecNumCloud, État français) et Scaleway (cloud français) tiennent ; Bedrock est non souverain (CLOUD Act). Conformité RGPD bonne via Bedrock (région UE), Scaleway et Albert ; insuffisante via OpenRouter" src="Etat-avancement/assets/06-bench-light.svg" width="100%">
</picture>

- **Lire la performance** : **DeepSWE v1.1 en principal**, la capacité agentique du modèle seul, à harness fixé (leaderboard officiel Datacurve), donc indépendante du harness ; Terminal-Bench 2.1 en agentique ; SWE-bench Verified en simple baseline (saturé, harness hétérogènes). Toute case sans donnée est « non publié » : aucun chiffre estimé.
- **La ligne DeepSeek est dédoublée** : Scaleway sert le checkpoint **0731** (DeepSWE 53 %), Albert sert a priori la **preview d'avril** (DeepSWE 7,3 % auto-rapporté, checkpoint à confirmer auprès de la DINUM). Même nom, performances agentiques sans rapport. C'est ce modèle Albert que les architectes et les PM/PO DACCORD utilisent aujourd'hui : il suffit pour leurs use cases, et il est gratuit et souverain.
- **Souveraineté (au sens CNIL)** : deux voies tiennent, **Albert (DINUM)**, SecNumCloud et utilisable avec OpenCode ([guide officiel](https://guides.ia.numerique.gouv.fr/albert-api/guides/ide#agentic-coding-opencode)), et **Scaleway** (cloud français). **Bedrock n'est pas souverain** : CLOUD Act, quelle que soit la région.
- **Conformité RGPD** : Bedrock en région UE (DPA AWS) reste une voie valable pour les modèles Anthropic (**Opus 5** en tête du bench, à moitié prix de Fable) ; Scaleway et Albert conformes ; **OpenRouter sans garanties**.
- **Prochaines étapes** : bench élargi aux modèles Bedrock dès la liste AWS, puis bench en conditions réelles. Supports : [le bench (PDF)](Livrables/benchHarness/Bench_Coding-Agentique.pdf) · [souveraineté et performance des modèles et harness (PDF)](Livrables/Souverainete-Performance/Souverainete-Performance-Modeles-Harness.pdf).

> [!WARNING]
> **Le coût ne se pose pas pareil pour les externes et les internes.** Les externes peuvent rester sur leur abonnement Claude (forfait). Les internes démarreront à environ 20 € par siège, **plus chaque token consommé au prix du modèle** : d'où l'enjeu du bench pour les internes et la CI/CD.

</details>

### Qui peut utiliser quoi

<details>
<summary>La matrice harness × population : ce qu'il est possible d'installer</summary>

🟢 possible · 🟠 possible mais non conforme · 🔴 impossible · ⏳ à instruire.

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

| Fournisseur | Ce qu'il apporte | Le point à lever | Où on en est |
|---|---|---|---|
| **AWS Bedrock** | Claude Code avec observabilité complète · région UE · large catalogue de modèles | L'observabilité est adossée à Claude Code : le harness est imposé | ✅ Exploré avec AWS ([CR du 23/07](CR/transverse/AWS-Bedrock-23-07-2026.txt)) : viable |
| **Scaleway** | Des modèles open-weight intéressants · souveraineté française | Valider le champ des possibles côté observabilité | 🔍 À explorer |
| **Google Vertex AI** | Un accès à des modèles frontier de plusieurs éditeurs (à confirmer) | Vérifier l'observabilité depuis n'importe quel harness | 🔍 À explorer |

**Pourquoi chercher au-delà de Bedrock** : imposer Claude Code n'est pas neutre. Ce harness est très gourmand en contexte : taillé pour les modèles frontier, il risque de moins bien fonctionner avec les modèles moins onéreux. La cible : une observabilité indépendante du harness, pour choisir librement le couple harness × modèle selon la tâche et le budget.

</details>

## ⚖️ Décisions attendues

| Décision | Ce qui est en jeu | Qui tranche, quand |
|---|---|---|
| **Porteur du pré-audit d'accessibilité** : hors des sprints, sans reposer sur Egapro, avec la mesure intégrée | Sans porteur ni mesure, l'outil restera piloté au feeling | **Gary** · arbitrage attendu |
| **Accès au centre logiciel** pour y packager les harness cibles | Deux voies passent déjà pour les internes ([la matrice](#qui-peut-utiliser-quoi)) : l'enjeu est la **liberté du choix du harness** | **Les personnes du centre logiciel** · introduction par Olivier à venir |
| **Stack des agents internes, et des externes sur sujets confidentiels** | La formule optimale en rapport qualité / prix, au plus près des exigences de souveraineté et de légalité | À instruire après le [bench élargi aux modèles Bedrock](#ce-que-dit-le-bench) et les [explorations Scaleway / Vertex AI](#trois-voies-daccès-aux-modèles) |

## Repères

- [Details.md](Details.md) : plan d'actions commenté, maturité par périmètre, impact action par action, matrice complète, focus par chantier
- [Tableau de bord de suivi](Suivi-Strategie-Adoption-IA.html) (à ouvrir dans un navigateur) : checklist par équipe, impact, outillage, sujets du moment
- [Checklist de déploiement IA par équipe](Livrables/Strategie-Deploiement/Checklist-IA-par-equipe.md) : quatre paliers, un par niveau de maturité
- [Stratégie de transformation IA (PDF)](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) · [Souveraineté et performance des modèles et harness (PDF)](Livrables/Souverainete-Performance/Souverainete-Performance-Modeles-Harness.pdf)
- Pilotage : [dashboard GitHub](https://github.com/orgs/SocialGouv/projects/198) · [état d'avancement Grist](https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement)

---

<sub>Mission Ippon Technologies · Selim Boukhari (sboukhari@ippon.fr) · graphiques régénérés chaque semaine via <code>Etat-avancement/build/generate_charts.py</code></sub>

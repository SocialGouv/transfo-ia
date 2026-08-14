# Transformation IA · Ministères sociaux

**Accompagner l'adoption de l'IA par les équipes du numérique** (Secrétariat général · Direction du numérique) : trois enjeux (identifier les usages, accompagner la maîtrise, évangéliser), quatre métiers (architectes, chefs de projet, designers, développeurs).

### L'adoption devient une dynamique d'équipe

L'impact se mesure en maturité gagnée : **trois périmètres ont monté de niveau** — Egapro passe de 3 à 4 (les orchestrations tournent en routine, l'organisation est maîtrisée), DACCORD et les architectes amorcent la même pente (1 → 2). Et les dernières demandes sont **entrantes** : la cheffe de projet SIRENA demande à être formée, l'architecte du cadre de cohérence propose d'outiller ses référentiels, trois développeurs DACCORD s'engagent dans un accompagnement individuel.

**Édition du lundi 10 août 2026** · mise à jour hebdomadaire · [le détail, chantier par chantier](Details.md) · [la stratégie (PDF)](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) · [dashboard GitHub](https://github.com/orgs/SocialGouv/projects/198) · [Grist](https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/01-kpi-dark.svg">
  <img alt="3 périmètres montés en maturité (Egapro, DACCORD, architectes) ; 4 use cases montés de niveau (3 sur Egapro, 1 sur DACCORD) ; 15 actions à impact déterminant, chacune décrite dans le détaillé ; prochain jalon mi-août (formation PM/PO SIRENA et DACCORD)" src="Etat-avancement/assets/01-kpi-light.svg" width="100%">
</picture>

## 🏆 Ce que l'accompagnement a changé, métier par métier

Le point de départ constaté à l'arrivée de la mission, et ce que chaque fonction sait faire aujourd'hui.

| Métier | Point de départ | Aujourd'hui |
|---|---|---|
| **Architectes** | Aucun intérêt exprimé pour l'IA | **Cinq use cases identifiés** en atelier ([4 août](CR/transverse/CR_Architectes-atelier-4-08-26.txt)) ; les architectes les priorisent eux-mêmes d'ici au 21 août |
| **Développeurs · Egapro** | Des usages IA bons, mais avec un cadre perfectible | Orchestrations en routine, désormais **optimisées et sécurisées** : codeur et testeur séparés, le code n'est plus testé par l'agent qui l'a écrit |
| **Développeurs · DACCORD** | Usage et compréhension de l'IA peu matures | L'équipe **monte sa propre orchestration** (accompagnement individuel en cours) |
| **Chef de projet · Egapro** | Un suivi décalé de la vitesse réelle du dev augmenté, roadmap design invisible | **Pilotage adapté à l'IA** : estimations en taille de T-shirt ; le designer crée désormais ses tickets, la roadmap design devient visible et challengeable |
| **Chefs de projet · DACCORD, SIRENA** | Tickets rédigés à la main, allers-retours entre métier et équipes | **Formation actée** à la génération de tickets Jira sur poste ministère (DACCORD le 25 août, créneau SIRENA à caler) : le ticket arrive formalisé, tests d'acceptation inclus, le métier se recentre sur sa valeur ajoutée |
| **Designers** | « L'IA a peu de valeur pour nous » | Depuis un poste ministère : **prototypes HTML au DSFR** testables par des utilisateurs, puis **maquette Figma générée** du prototype retenu, DSFR respecté |
| **Poste de travail** | Pas d'IA générative possible sur PC ministère | **Deux voies opérationnelles** : OpenCode Desktop (sans droits admin, clé Albert) · Claude Code dans VS Code (clé Bedrock) · [qui peut utiliser quoi](#outillage--qui-peut-utiliser-quoi) |

<sub>La dynamique s'étend : VAO entre dans la boucle avec l'atelier dev augmenté du 8 septembre.</sub>

## ⚖️ Décisions attendues

| Décision | Ce qui est en jeu | Qui tranche, quand |
|---|---|---|
| **Porteur du pré-audit d'accessibilité** — hors des sprints Egapro, sans reposer sur Max, avec la mesure intégrée | Sans porteur ni mesure, l'outil restera piloté au feeling | **Gary** · arbitrage attendu |
| **Accès au centre logiciel** pour y packager les harness cibles | Sans cela, l'adoption reste cantonnée aux prestataires : un poste interne managé ne peut pas installer un harness | Avancée du 6/08 : le centre peut tolérer des outils restreints à une liste de personnes, et **Olivier** introduit la mission |
| **Stack des agents internes** — meilleur rapport performance / prix / souveraineté / conformité | Le coût interne suit l'usage : ≈20 € par siège **plus chaque token consommé** | À instruire après le [bench élargi aux modèles Bedrock](#outillage--ce-que-dit-le-bench) (août) |

## Avancement par chantier

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/02-maturite-org-dark.svg">
  <img alt="Maturité d'organisation par périmètre, sur une échelle de 1 à 5 : Egapro passé de 3 à 4 (orchestrations en routine, organisation maîtrisée) ; DACCORD passé de 1 à 2 (skills partagés, accompagnement individuel) ; SIRENA à 2 ; VAO et BIO2 à 1 ; architectes passés de 1 à 2 (premiers use cases IA identifiés à l'atelier DA)" src="Etat-avancement/assets/02-maturite-org-light.svg" width="100%">
</picture>

**L'échelle** : 1-2 de rien à la découverte de l'IA · 3 des skills utilisés, des use cases pratiqués, une organisation perfectible · 4 des orchestrations, une organisation maîtrisée · 5 orchestrations, volume de cas d'usage (dev et PM/PO), bonnes pratiques renseignées, vrai craft.

| Chantier | Statut | Où on en est | Prochaine étape |
|---|:---:|---|---|
| **Egapro** | 🟢 ↗ | Périmètre pilote : orchestrations en routine, designers autonomes sur les prototypes, 3 use cases montés de niveau. Accessibilité : l'audit du code passe de 31 à 16 erreurs | Arbitrer avec Gary le portage de l'outil de pré-audit hors des sprints |
| **DACCORD** | 🟢 ↗ | Atelier skills du 6/08 : skills couvrant changement de version, changelog, dev front, dev back et plan d'implem ; tests back / front à ajouter. Orchestrations en cours | Accompagnement individuel : Orchstration à mettre en place sur le frontend et le backend |
| **SIRENA** | 🟢 ↗ | Diagnostic complété côté produit : Aurélie a repris le projet en juin et demande explicitement à être formée à l'usage de l'IA pour le PM / PO | Formation à la génération de tickets : créneau à caler (la session DACCORD a lieu le 25/08) |
| **VAO** | 🟡 → | Équipe en découverte ; Halim identifié pour la génération de tickets intelligibles via MCP (point produit du 6/08) | Caler le créneau avec Halim · atelier dev augmenté le 8 septembre |
| **BIO2** | 🟡 → | Nouveau périmètre : produit de refonte côté santé, entré dans le suivi au point produit du 6/08 | Valider l'intérêt d'accompagner Yuna sur la génération de tickets au lancement de la refonte (début septembre) |
| **Transverse** | 🟢 ↗ | bench des harness livré · matrice des harness disponibles aux collaborateurs livré · Bedrock cadré avec AWS · référentiels d'architecture et de bonnes pratiques cadrés avec Igor (28/07) · 5 use cases IA identifiés avec les architectes (4/08) · population produit cadrée (6/08) | Priorisation des use cases par les architectes d'ici au 21 août · Produire une bibliothèque de skills basées sur les référentiels d'Igor|

<sub>🟢 sur la trajectoire · 🟡 cadrage en cours · 🔴 point d'attention. SRDT et DomiFA, rencontrées en exploration, rejoindront le suivi actif au fil de l'eau.</sub>

→ [La maturité périmètre par périmètre](Details.md#maturité-par-périmètre) · [le diagnostic fin, use case par use case](Details.md#matrice-de-maturité) · [le focus de chaque chantier](Details.md#focus-par-chantier)

## Plan d'actions

**Le réalisé, l'impact en face** : ◆◆◆ du concret livré (skills, orchestrations, solutions) · ◆◆ formation, acculturation · ◆ cadrage, étude, communication.

| ✅ Réalisé | Chantier | Impact | Ce que ça change |
|---|---|:---:|---|
| Orchestration « codeur / testeur » en routine | Egapro | ◆◆◆ | Le code arrive testé par une instance indépendante : la qualité ne repose plus sur la seule relecture humaine |
| Pilotage adapté à l'IA : estimations T-shirt, tickets design | Egapro | ◆◆◆ | Le suivi colle à la vitesse réelle du dev augmenté ; la roadmap design devient visible et challengeable |
| Designers outillés : skills UX, formation prototypes | Egapro | ◆◆◆ | Plusieurs prototypes HTML générés avant de maquetter : le designer se projette au lieu d'itérer à l'aveugle |
| Outil de veille du Journal officiel livré au CEPS (30/07) | Transverse | ◆◆◆ | Une newsletter quasi automatisée en trois jours : la preuve, visible hors DNUM, que l'IA livre vite sur un besoin clair |
| Atelier de génération de DA avec les architectes (4/08) | Transverse | ◆◆◆ | Les architectes repartent acteurs : cinq use cases identifiés par eux-mêmes |
| Atelier d'amélioration des skills (6/08) | DACCORD | ◆◆◆ | Les skills couvrent cinq domaines et s'améliorent en commun, plus chacun dans son coin |
| Coaching développement augmenté (16/07) | DACCORD | ◆◆ | Dès le lundi suivant, les développeurs mettaient leurs system prompts en commun, de leur propre initiative |
| Bench des harness et modèles | Transverse | ◆ | Sept stacks comparées en perf / prix / souveraineté / conformité : la base de la décision de stack |
| Cadrage de la voie Bedrock avec AWS (23/07) | Transverse | ◆ | Catalogue de modèles élargi à observabilité conservée : la voie interne se précise |
| Claude Enterprise : discussions avec Software One (23/07) | Transverse | ◆ | L'option d'abonnement Claude pour les équipes est instruite |
| Cadrage des référentiels d'architecture avec Igor (28/07) | Transverse | ◆ | Le référentiel outillé, en construction, part sur des bases partagées |
| Point d'adoption IA population produit (6/08) | Transverse | ◆ | Les use cases RU et PM / PO se formalisent ; VAO et BIO2 entrent dans le suivi |

<sub>Sur les périmètres actifs, l'impact est presque exclusivement du concret ; les actions modérées sont toutes transverses : les chantiers de fond qui conditionnent le passage à l'échelle.</sub>

**La suite** :

| Statut | Actions |
|---|---|
| 🔄 **En cours** | accompagnement individuel skills et orchestration DACCORD (Sébastien, Florian, Sylvain) · orchestrations Egapro → Jira (DACCORD) · pré-audit d'accessibilité Egapro · tickets de spec DACCORD · constitution du référentiel d'architecture outillé |
| 📅 **Planifié** | formation PM / PO : DACCORD le 25/08, SIRENA à caler · prototypes DSFR avec Louis (août) · bench élargi Bedrock (août) · catalogue de skills partagés (courant août) · acculturation IA des architectes (fin août) · sélection des use cases DA (sem. du 31/08) · tickets BIO2 avec Yuna (début sept.) · rencontre du centre logiciel (introduction par Olivier) · atelier dev augmenté VAO (8/09) · cartographie des comptes Bedrock (fin sept.) |
| ⏭️ **À lancer** | tickets VAO avec Halim · acculturation IA des PO · acculturation de l'ensemble des designers · centralisation de la documentation fonctionnelle · évangélisation des équipes du CEPS |

<sub>S'y ajoutent les déclinaisons des actions éprouvées, à cadrer sur DACCORD, SIRENA et VAO.</sub>

→ [Le plan d'actions commenté, action par action](Details.md#plan-dactions) · [l'impact de chaque action, y compris à venir](Details.md#impact-des-actions)

## Roadmap

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/04-roadmap-dark.svg">
  <img alt="Jalons : coaching dev augmenté DACCORD réalisé le 16 juillet ; du 28 au 30 juillet, cadrage des référentiels d'architecture avec Igor, rencontre de la cheffe de projet SIRENA et livraison de l'outil CEPS ; atelier DA avec les architectes réalisé le 4 août ; atelier skills DACCORD et point d'adoption IA produit réalisés le 6 août ; mi-août, formation à l'usage de l'IA pour le PM et le PO, SIRENA et DACCORD ; courant août, catalogue de skills partagés, prototypes DSFR avec Louis et bench élargi aux modèles Bedrock ; fin août, demi-journée d'acculturation IA avec Igor et les architectes ; semaine du 31 août, sélection des use cases architectes ; 8 septembre, atelier dev augmenté VAO et tickets BIO2 avec Yuna ; cartographie des bénéficiaires des comptes Bedrock fin septembre" src="Etat-avancement/assets/04-roadmap-light.svg" width="100%">
</picture>

## Outillage : ce que dit le bench

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="Etat-avancement/assets/06-bench-dark.svg">
  <img alt="Comparaison de 7 stacks : Claude Code avec Fable 5 via Bedrock à 95 %, OpenCode avec Kimi K3 via OpenRouter à environ 93 % (annoncé), Claude Code avec Opus 4.8 à 88,6 %, DeepSeek V4 Pro à 80,6 %, Albert avec DeepSeek V4 Flash à environ 79 %, GLM 5.2 à environ 78 %, Vibe avec Mistral Medium 3.5 à 77,6 % ; prix de gratuit (Albert) à 50 $ le million de tokens (Fable 5) ; souveraineté : seuls Albert (SecNumCloud, État français) et Mistral (éditeur français) tiennent, Bedrock est non souverain (CLOUD Act) ; conformité RGPD bonne via Bedrock (région UE), Mistral et Albert, partielle via Anthropic direct, insuffisante via OpenRouter" src="Etat-avancement/assets/06-bench-light.svg" width="100%">
</picture>

- **Souveraineté (au sens CNIL)** : seules deux voies tiennent — **Albert (DINUM)**, SecNumCloud et utilisable avec OpenCode ([guide officiel](https://guides.ia.numerique.gouv.fr/albert-api/guides/ide#agentic-coding-opencode)), et **Mistral** (éditeur français) avec son harness Vibe. **Bedrock n'est pas souverain** : CLOUD Act, quelle que soit la région.
- **Conformité RGPD** : Bedrock en région UE (DPA AWS) reste une voie valable pour les modèles Anthropic, dont **Fable 5** (95 % SWE-bench, le plus performant du bench) ; Mistral et Albert conformes ; Anthropic direct partiel (transfert hors UE) ; **OpenRouter sans garanties** — à réserver éventuellement aux externes.
- **Voie Bedrock précisée avec AWS (23/07)** ([compte rendu](CR/transverse/AWS-Bedrock-23-07-2026.txt)) : large catalogue de modèles (dont open-weight chinois) en conservant l'observabilité — de quoi envisager moins cher qu'Anthropic. En attente : liste des modèles et documentation d'observabilité.
- **Prochaines étapes** : bench élargi aux modèles Bedrock (août), puis bench en conditions réelles (Albert / DeepSeek V4 Flash via OpenCode face à Claude). [Le support complet (PDF)](Livrables/benchHarness/Bench_Coding-Agentique.pdf) compare les 7 stacks et recommande selon la priorité.

> [!WARNING]
> **Le coût ne se pose pas pareil pour les externes et les internes.** Les externes peuvent rester sur leur abonnement Claude (forfait, consommation incluse). Les internes démarreront à environ 20 € par siège, **plus chaque token consommé au prix du modèle** : leur coût suivra l'usage — d'où l'enjeu du bench pour les internes et la CI/CD.

## Outillage : qui peut utiliser quoi

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

**Deux voies passent pour toutes les populations** : OpenCode Desktop et VS Code avec le plugin Claude Code, adossés à Bedrock / Scaleway ou Albert — les mêmes que celles déjà opérationnelles sur poste ministère. Tout le reste bute sur le poste interne (Claude Desktop et Codex, impossibles sur Windows) ou sur la conformité (clés personnelles, modèles gratuits).

<sub>Poste Linux interne : faisabilité à instruire. Matrice de travail : [Livrables/Outillage/matrice-outillage.md](Livrables/Outillage/matrice-outillage.md).</sub>

## Repères

- [Details.md](Details.md) : plan d'actions commenté, maturité par périmètre, impact action par action, matrice complète, focus par chantier
- [Stratégie de transformation IA (PDF)](Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) : enjeux, exploration, plan d'action en trois horizons
- [Réalisations par métier](Livrables/Realisations_par_metier/) : skills, kits de configuration, tutoriels, générateurs de DA
- Pilotage : [dashboard GitHub](https://github.com/orgs/SocialGouv/projects/198) · [état d'avancement Grist](https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement)

---

<sub>Mission Ippon Technologies · Selim Boukhari (sboukhari@ippon.fr) · graphiques régénérés chaque semaine via <code>Etat-avancement/build/generate_charts.py</code></sub>

# État d'avancement détaillé

Semaine du 20 au 24 juillet 2026 · [← retour à la synthèse](../README.md)

## Plan d'actions

Le cœur du suivi : ce qui a été réalisé, ce qui est en cours, ce qui reste à faire.

### ✅ Réalisées (4)

| Métier | Périmètre | Action | Ce qui a été fait |
|---|---|---|---|
| Développeurs | DACCORD | Former au développement augmenté | Session de coaching du 16 juillet (voir [zoom](#zoom--coaching-développement-augmenté-daccord-16-juillet)) |
| Développeurs | Egapro | Accompagner à la réalisation d'orchestrations | Orchestration « séparation codeur / testeur » en place |
| Chefs de projet | Egapro | Permettre un meilleur suivi d'un projet utilisant l'IA | Estimations en taille de T-shirt sur les tickets ; tickets Design créés pour donner à l'équipe de la visibilité sur la roadmap design et la challenger |
| Designers | Egapro | Accompagner à la génération de prototypes | Skill UX adapté au projet, skill d'audit UX, formation à la réalisation de prototypes de maquettes avec Claude |

### 🔄 En cours (3)

| Métier | Périmètre | Action | Prochaine étape |
|---|---|---|---|
| Développeurs | DACCORD | Adapter les orchestrations Egapro à Jira | Poursuivre l'adaptation, puis la mettre entre les mains de l'équipe |
| Développeurs | Egapro | Piloter le pré-audit d'accessibilité | Synchroniser les retours de Marie et le travail de Max ; synchroniser Amelle et Victor |
| Chefs de projet | DACCORD | Accompagner la génération de tickets de spec | Organiser le point avec Kahina à son retour de congés |

### 📅 Planifiées (3)

| Métier | Périmètre | Action | Échéance |
|---|---|---|---|
| Architectes | Transverse | Atelier de génération de DA avec l'IA | 3 août |
| Transverse | Transverse | Claude Enterprise : discussions avec Software One | Atelier le 3 août |
| Développeurs | VAO | Atelier de formation au développement augmenté | Septembre, à planifier avec Anselme à son retour |

### ⏳ À lancer (4)

| Métier | Périmètre | Action | Première étape |
|---|---|---|---|
| Product Owners | Transverse | Former à la fenêtre de contexte et au prompt engineering, présenter un use case | Valider l'intérêt d'une séance d'acculturation IA avec Olivier |
| Designers | Transverse | Stratégie d'embarquement des designers | Échanger avec Norman et Louis, sur la base des use cases validés et éprouvés sur Egapro |
| Transverse | Transverse | Outillage IA des internes | Dénombrer les utilisateurs internes à équiper en sièges Claude Enterprise via Bedrock ; point de vigilance : les externes peuvent conserver leur abonnement Claude (forfait), les internes démarreront à environ 20 € par siège plus la consommation au token, au prix du modèle |
| Transverse | Transverse | Benchmark des modèles et harness alternatifs à Claude | Préparer un scénario Albert (DeepSeek v4 flash via OpenCode) et un scénario Claude avec et sans abonnement |

### 🧭 Déclinaisons à cadrer (11)

Actions déjà éprouvées sur un périmètre, à décliner sur les autres une fois le cadrage fait avec chaque équipe.

| Action | À cadrer sur |
|---|---|
| Former au développement augmenté | SIRENA |
| Accompagner à la réalisation d'orchestrations | SIRENA · VAO |
| Piloter le pré-audit d'accessibilité | DACCORD · SIRENA · VAO |
| Accompagner la génération de tickets de spec | SIRENA · VAO |
| Accompagner à la génération de prototypes | DACCORD · SIRENA · VAO |

## Matrice de maturité

La matrice mesure **le niveau auquel l'accompagnement a amené chaque fonction d'équipe** (par exemple : les designers d'Egapro sur la génération de prototypes). Ce n'est pas une note des équipes : le niveau 1 signifie que la fonction démarre tout juste sur ce use case.

| Niveau | Signification |
|:---:|---|
| **1** | Découverte : la fonction démarre, les premiers pas sont faits |
| **2** | En cours d'acquisition : pratique régulière, en voie de fiabilisation |
| **3** | Maîtrise : pratique installée, outillée, reproductible |
| **1 → 2** | Progression apportée depuis le début de l'accompagnement |
| **?** | Pas encore évalué · **–** non applicable au périmètre |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/05-matrice-dark.svg">
  <img alt="Matrice de maturité IA détaillée par use case et périmètre, détaillée dans le tableau ci-dessous" src="assets/05-matrice-light.svg" width="100%">
</picture>

<details>
<summary>Version tableau de la matrice</summary>

| Métier | Use case | Egapro | DACCORD | SIRENA | VAO | Transverse |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Chefs de projet | Piloter un projet développé avec l'IA | 1 → 2 | 1 | ? | ? | – |
| Chefs de projet | Générer des tickets de spec | 1 | 1 | ? | ? | – |
| Chefs de projet | Organiser le board (sprints, epics) | 3 | 1 | ? | ? | – |
| Designers | Générer des prototypes HTML/JS | 1 → 3 | ? | ? | ? | – |
| Développeurs | Générer du code de qualité | 2 | 2 | ? | 1 | – |
| Développeurs | Générer des tests | 3 | 2 | ? | 1 | – |
| Développeurs | Utiliser des orchestrations | 3 | 1 | 1 | 1 | – |
| Développeurs | Pré-auditer l'accessibilité | 1 → 2 | 1 | 1 | 1 | – |
| Développeurs | Pré-auditer la sécurité | 1 | 1 | 1 | 1 | – |
| Développeurs | Outils & system prompts communs | 3 | ? | 1 | ? | – |
| Architectes | Générer un dossier d'architecture (DA) | – | – | – | – | 1 |

</details>

## Zoom : coaching développement augmenté, DACCORD (16 juillet)

Session avec les développeurs de l'équipe, couvrant l'ensemble de la chaîne du développement augmenté ([compte rendu](../CR/Feedback_Coaching_Devs_DACCORD.docx)) :

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

L'élan s'est concrétisé sans attendre : **dès le lundi 20 juillet, les développeurs ont engagé de leur propre initiative la mise en commun de leurs system prompts (agents, rules, skills)**. La mission a proposé une relecture de leurs premiers skills (point de suivi prévu début août), avant l'**atelier de co-construction** qui ancrera ces pratiques dans le quotidien de l'équipe.

## Focus par chantier

### Egapro : périmètre pilote

- Le périmètre le plus avancé : **5 use cases au niveau maîtrise** (orchestrations, tests, board, outillage commun, prototypes designers).
- **3 use cases montés de niveau** depuis le début de l'accompagnement : pilotage de projet (1 → 2), prototypes designers (1 → 3), pré-audit d'accessibilité (1 → 2).
- Ce qui a permis ces progressions : estimations T-shirt, tickets design de visibilité, skills UX et formation prototypes, synchronisation des travaux d'accessibilité.
- Prochain palier : le pré-audit de sécurité (encore en découverte).

### DACCORD : l'équipe qui monte

- Coaching développement augmenté du 16 juillet très bien reçu ; l'équipe se projette vers un haut niveau de maîtrise.
- **Passage à l'acte dès le 20 juillet** : mise en commun des system prompts (agents, rules, skills) engagée par les développeurs de leur propre initiative ; la mission relira leurs premiers skills (suivi prévu début août).
- Les orchestrations éprouvées sur Egapro sont en cours d'adaptation à Jira, pour un transfert direct de savoir-faire entre périmètres.
- Côté chefs de projet, l'accompagnement à la génération de tickets de spec reprend au retour de congés de Kahina.
- À venir : atelier de co-construction de skills, agents et rules, suivi de leur intégration, accompagnement à l'orchestration pour les personnes volontaires.

### SIRENA : diagnostic posé

- Usage IA réel mais individuel : contexte `.claude` global sur l'application, production et revue de code assistées chez une partie des développeurs.
- Pas encore de coordination d'équipe : outils et documents de contexte non mutualisés, base de contexte exploitée mais non maintenue.
- L'équipe est intéressée par une démo et un atelier skills ; une vérification de conformité à l'échelle de l'équipe a été évoquée.
- 6 use cases sur 10 restent à évaluer : l'image se précisera au cadrage.

### VAO : en découverte

- Niveau découverte sur les 5 use cases évalués (code, tests, orchestrations, pré-audits).
- L'atelier de formation au développement augmenté est prévu en septembre, à planifier avec Anselme à son retour.

### Transverse : la stratégie en marche

- Stratégie en trois horizons présentée et validée ([support](../Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf)).
- Architectes : atelier de génération de DA le 3 août ; générateurs comparatifs Claude / DeepSeek déjà construits ([réalisations](../Livrables/Realisations_par_metier/Architectes/)).
- Outillage : discussions Software One sur Claude Enterprise (atelier le 3 août), dénombrement des sièges à équiper via Bedrock à lancer. Vigilance coûts : les externes peuvent conserver leur abonnement Claude, les internes démarreront à environ 20 € par siège plus la consommation au token (prix du modèle).
- Harness : [bench de coding agentique livré](../Livrables/benchHarness/Bench_Coding-Agentique.pdf) ; benchmark élargi en conditions réelles à préparer (scénarios Albert et Claude).
- POs et designers : deux stratégies d'embarquement à ouvrir (Olivier ; Norman et Louis).

## Livrables à date

| Livrable | Pour qui | Où |
|---|---|---|
| Stratégie de transformation IA (point d'étape) | Direction | [PDF](../Livrables/Pr%C3%A9sentation-strat%C3%A9gie-transfo-ia/Point-etape_Adoption-IA.pdf) |
| Bench des harness de coding agentique | Direction, tech leads | [PDF](../Livrables/benchHarness/Bench_Coding-Agentique.pdf) |
| Kit de configuration dev augmenté (analyse → implémentation → portage Jira) | Développeurs | [tuto-config](../Livrables/Realisations_par_metier/Developpeurs/tuto-config/) |
| Skills de pré-audit RGAA et cyber | Développeurs | [RGAA_et_Cyber](../Livrables/Realisations_par_metier/Developpeurs/RGAA_et_Cyber/) |
| Skill UX projet, skill d'audit UX, use case maquette | Designers | [Designers](../Livrables/Realisations_par_metier/Designers/) |
| Générateurs de dossiers d'architecture (Claude / DeepSeek) | Architectes | [Architectes](../Livrables/Realisations_par_metier/Architectes/) |

---

<sub>Sources : <code>Etat-avancement.xlsx</code> et <a href="https://grist.numerique.gouv.fr/o/tranfo-ia/rFkVL6aLFbrE/Etat-davancement">Grist</a> · graphiques générés par <code>build/generate_charts.py</code> (éditer la section DONNÉES puis relancer) · Selim Boukhari, Ippon Technologies</sub>

# Orchestrateur de slides

Une chaîne d'agents qui fabrique un deck : un orchestrateur questionne le besoin, un planificateur écrit l'histoire, l'utilisateur la valide, un travailleur la met en forme dans un gabarit à la charte de l'État, un vérificateur contrôle le fond puis la forme. Aucun agent ne lit plus de 350 lignes de skills.

Version 0.3.0 du 25 novembre 2026, à valider. Schéma de la chaîne : [schema.html](schema.html).

## Ce que contient ce dossier

| Élément | Rôle |
|---|---|
| [skills/orchestrateur-slides/](skills/orchestrateur-slides/) | le déroulé en sept étapes, les trois briefs de rôle (`references/role-*.md`), le contrôle de la carte |
| [skills/histoire-slides/](skills/histoire-slides/) | l'histoire d'un deck : fil rouge, un message par slide, carte des messages, critique |
| [skills/charte-dsfr/](skills/charte-dsfr/) | le gabarit HTML, seize compositions de slide (dont frise, graphiques et schémas), les scripts de contrôle |
| [exemple/catalogue/deck.html](exemple/catalogue/deck.html) | un deck produit avec le gabarit, une slide par composition |
| [exemple/essai-petit-modele/](exemple/essai-petit-modele/) | ce qu'un petit modèle a produit avec la chaîne, sur un sujet et des chiffres inventés : le brief, la matière, la carte, le deck, sa planche |
| [dist/](dist/) | un zip des trois skills par outil, à dézipper à la racine d'un projet |
| [outils/budget_contexte.py](outils/budget_contexte.py) | mesure ce que chaque agent lit, et échoue au-delà de 350 lignes de skills |
| [outils/construire_zips.py](outils/construire_zips.py) | reconstruit les zips de `dist/` après une modification des skills |
| [schema.html](schema.html) | la chaîne en un schéma : agents, objectifs, skills, lignes lues |

## La chaîne

| Étape | Qui | Produit |
|---|---|---|
| 1. Cadrage | orchestrateur, avec l'utilisateur | `brief.md` |
| 2. Histoire | planificateur | `carte.md`, la carte des messages |
| 3. Revue du fond | vérificateur | `revue-fond.md` |
| 4. Accord | orchestrateur, avec l'utilisateur | la carte validée |
| 5. Slides | travailleur | `deck/deck.html` |
| 6. Revue de la forme | vérificateur | `revue-forme.md` |
| 7. Livraison | orchestrateur | le deck et ses réserves |

Le cadrage pose jusqu'à vingt questions, par séries de cinq au plus. Après chaque série, l'orchestrateur retire les questions auxquelles les réponses ont déjà répondu. L'utilisateur peut dire « stop » à tout moment : les réponses par défaut s'appliquent au reste.

## Ce que chaque agent lit

Plafond : 350 lignes de fichiers de skills par agent (son rôle, le skill qui le sert, le gabarit, la référence des compositions).

| Agent | Fichiers de skills lus | Lignes | Marge |
|---|---|---:|---:|
| Orchestrateur | `orchestrateur-slides/SKILL.md` | 122 | 228 |
| Planificateur | `role-planificateur.md`, `histoire-slides/SKILL.md` | 152 | 198 |
| Vérificateur, sur le fond | `role-verificateur.md`, `histoire-slides/SKILL.md` | 179 | 171 |
| Travailleur | `role-travailleur.md`, `charte-dsfr/SKILL.md`, le gabarit `deck.html`, la référence de son deck | 332 au plus | 18 |
| Vérificateur, sur la forme | `role-verificateur.md`, `charte-dsfr/SKILL.md` | 157 | 193 |

`python3 outils/budget_contexte.py` refait la mesure, fichier par fichier, et sort en erreur si un agent dépasse 350 lignes. Un second plafond l'accompagne, 35 000 caractères, pour qu'une ligne très longue ne contourne pas le premier ; le travailleur en lit 22 975 au plus.

Quatre précisions :

- **Le travailleur ne lit que les compositions de son deck.** `scripts/reference.py` les lui affiche d'après la carte des messages. Le chiffre de 332 est le pire cas : dix compositions différentes, parmi les plus longues. Un deck qui en emploie six lui fait lire environ 280 lignes.
- **Un deck emploie dix compositions différentes au plus**, sur seize. C'est ce qui borne la lecture du travailleur, et un deck qui change de mise en page à chaque slide perd son unité. Le contrôle de la carte refuse une onzième.
- **Les fichiers de travail s'ajoutent** (brief, carte, deck, revue). Pour un deck de 12 slides, estimés : 292 à 612 lignes en tout par agent, soit 2 à 5 % d'un contexte de 256 000 tokens. La matière source lue par le planificateur s'ajoute aussi ; son rôle la plafonne à 3 000 lignes.
- **Sans sous-agents, le plafond ne tient pas** : un seul agent tient tous les rôles et lit 662 lignes.

## Frises, schémas, graphiques

Cinq compositions sont dessinées par le gabarit. Le modèle écrit des libellés et des nombres, jamais un dessin.

| Composition | Ce qu'elle montre | Ce que le modèle écrit |
|---|---|---|
| `frise` | trois à six jalons datés sur un axe | une date, un titre et un texte par jalon |
| `barres` | deux à six grandeurs comparées | un libellé, un nombre et sa valeur affichée par barre |
| `courbe` | une évolution en trois à huit points | un libellé, un nombre et sa valeur affichée par point |
| `flux` | deux à quatre acteurs, et ce que chacun passe au suivant | un titre et un texte par bloc, le nom de ce qui part vers le suivant |
| `couloirs` | qui fait quoi à chaque étape | le nom des étapes, puis une case par étape pour chaque acteur |

Dans chacune, un seul élément peut être marqué « à retenir » : il passe en bleu France et les autres en retrait. Les graphiques partent de zéro, pour que l'échelle reste honnête ; ils n'ont qu'une série.

## Ce qui a changé

En version 0.1.0, le travailleur lisait 555 lignes de skills et le vérificateur de forme 552 ; le planificateur en lisait 318, mais longues : 32 900 caractères.

Version 0.2.0, pour tenir 350 lignes par agent :

1. **Écriture courte des slides.** Une slide ne contient plus que ses textes, dans des emplacements nommés (`data-slot`, `data-item`). Le script du gabarit construit la mise en page au chargement. Une slide coûte environ un quart de caractères en moins à écrire.
2. **Un skill d'histoire court, `histoire-slides`**, remplace `slide-crafting` (193 lignes, 23 680 caractères), dont le planificateur n'employait que deux étapes sur cinq. Il en reprend la méthode ; son fichier `meta/origine.md` le dit.
3. **Un contrôle de la carte par script**, `controle_carte.py` : longueur des titres selon la nature de la slide, nature dans la liste, temps sans slide. Le vérificateur n'a plus à compter des caractères.
4. **Des rôles resserrés** : chaque règle est écrite une fois, dans le skill ou dans le rôle. Le vérificateur de forme ne lit pas la référence des compositions.

Version 0.3.0, pour les frises, les schémas et les graphiques :

5. **Cinq compositions dessinées par le gabarit** (tableau ci-dessus), soit seize en tout.
6. **Une référence affichée par script.** Avec seize compositions, la référence entière ferait dépasser le plafond au travailleur : il ne reçoit que celles de son deck.

## Tenir sous le plafond de sortie

Une réponse de modèle est plafonnée, souvent à 32 000 tokens, réflexion comprise. Quatre règles, écrites dans le skill et dans les rôles :

1. les relais passent par des fichiers, et un sous-agent rend dix lignes au plus ;
2. quatre slides au plus par appel d'écriture (environ 3 200 caractères) ;
3. une correction modifie la slide visée, jamais le fichier entier ;
4. le dossier `charte/` d'un deck ne se lit pas (64 667 caractères de styles et de script), et les polices sont des fichiers binaires, qu'un agent ne peut pas charger par erreur.

## Ce qui aide un modèle faible sur les visuels

Le modèle ne décide pas de la mise en page. Il choisit une composition parmi seize, recopie son exemple et remplace les textes. Il n'écrit ni style, ni classe, ni balise d'habillage, ni dessin. Chaque emplacement a une longueur maximale, calibrée à l'écran sur un deck rempli à ses limites. `controle_deck.py` refuse un texte trop long, un texte placé hors emplacement, une composition inconnue, une icône inventée, un nombre mal écrit dans un graphique, un style ajouté, une balise mal fermée, et signale un texte d'exemple resté en place ou un graphique sans source. `deck.html?planche` montre toutes les slides sur une page et encadre en rouge celle qui déborde. Le gabarit pose lui-même les espaces insécables de la typographie française.

## Installer et essayer

Un zip par outil, dans [dist/](dist/). Le dézipper à la racine du projet : il y pose les trois skills dans le dossier où l'outil les cherche. Le contenu est le même dans les quatre ; seul le dossier change.

| Outil | Zip | Dossier créé | Appeler l'orchestrateur |
|---|---|---|---|
| Claude Code | `orchestrateur-slides-0.3.0-claude-code.zip` | `.claude/skills/` | par une phrase, ou `/orchestrateur-slides` |
| OpenCode | `orchestrateur-slides-0.3.0-opencode.zip` | `.opencode/skills/` | par une phrase, ou `@orchestrateur-slides` |
| Codex | `orchestrateur-slides-0.3.0-codex.zip` | `.agents/skills/` | par une phrase, ou `$orchestrateur-slides` |
| DeepSeek Harness | `orchestrateur-slides-0.3.0-deepseek-harness.zip` | `.dsh/skills/` | par une phrase |

1. Dans le dossier du projet : `unzip chemin/vers/le.zip` (le dossier créé commence par un point, donc il est caché dans un explorateur de fichiers).
2. Demander : « Lance l'orchestrateur de slides : je dois présenter … ».
3. Pour voir le gabarit sans la chaîne : ouvrir [exemple/catalogue/deck.html](exemple/catalogue/deck.html) dans un navigateur.

À savoir :

- **Il faut Python 3**, que les agents emploient pour contrôler la carte et le deck et pour afficher les compositions. La planche demande en plus un navigateur qui tourne sans écran (Firefox ou la famille Chromium) ; sans lui, le rendu est déclaré « non contrôlé » et la personne ouvre `deck.html?planche` elle-même.
- **Un seul zip par projet.** OpenCode et DeepSeek Harness lisent aussi `.agents/skills/`, et OpenCode lit aussi `.claude/skills/` : deux zips dans le même projet y donneraient les skills en double.
- **Dans un dépôt git, dézipper à la racine du dépôt** : DeepSeek Harness ne cherche les skills du projet que là. OpenCode et Codex les trouvent aussi dans un sous-dossier, s'ils y sont lancés.
- **Après une modification des skills**, `python3 outils/construire_zips.py` refait les quatre zips. Il refuse une description de skill de plus de 500 caractères, parce que DeepSeek Harness n'en montre pas davantage au modèle.

D'où viennent ces dossiers (vérifié le 25 novembre 2026) : la documentation d'OpenCode V2 (`https://opencode.ai/docs/skills.md`) ; celle de Codex (`https://learn.chatgpt.com/docs/build-skills.md`, vers laquelle renvoie `developers.openai.com/codex/skills`) ; le paquet `@deepseek-ai/dsh-skill-filesystem` en version 0.2.2-rc.1 pour DeepSeek Harness, dont le dépôt se dit en préversion et annonce des changements incompatibles.

## Ce qui est vérifié, ce qui ne l'est pas

Vérifié le 25 novembre 2026 :

- **le plafond** : `outils/budget_contexte.py` rend « 0 dépassement(s) » ;
- **les scripts** : 40 tests pour la charte (`python3 -m unittest test_charte`, depuis `skills/charte-dsfr/scripts/`) et 11 pour le contrôle de la carte (`python3 -m unittest test_controle_carte`, depuis `skills/orchestrateur-slides/scripts/`), tous passants ;
- **le rendu des onze compositions d'origine** : rendues dans Firefox avec les fichiers de charte d'avant et d'après la version 0.3.0, elles sont identiques au pixel près sur trois decks (aux limites, au minimum d'éléments, catalogue) ;
- **le rendu des cinq nouvelles** : aucune ne déborde sur un deck rempli à ses limites, ni sur un deck réduit au minimum d'éléments ; le catalogue de seize slides a été regardé ;
- **les skills** : frontmatter valide pour tous les hôtes, aucune erreur ni avertissement de l'outil de vérification automatique ;
- **les zips** : chacun, dézippé dans un projet neuf, pose les skills au bon endroit, et les scripts y tournent (deck contrôlé à 0 erreur, carte contrôlée, référence affichée). OpenCode 1.18.30 liste les trois skills (`opencode debug skill`) ; Codex 0.147.0 les place dans le prompt du modèle (`codex debug prompt-input`) ; pour DeepSeek Harness 0.2.2-rc.1, la règle de découverte de son paquet a été rejouée sur le projet dézippé (trois skills acceptés), et son profil `web` charge bien les skills et l'outil de sous-agents ;
- **la chaîne, jouée par des sous-agents sur un petit modèle** (Claude Haiku), chacun lancé par le seul message de cinq lignes, sur des briefs fictifs avec leur matière source :
  - en version 0.2.0, les quatre rôles une fois : carte de 5 slides, revue du fond « À CORRIGER » à six corrections, deck à 0 erreur, forme validée ;
  - en version 0.3.0, le planificateur et le travailleur, sur une matière qui appelle des graphiques : le planificateur a choisi de lui-même une courbe, des barres, un schéma à couloirs et une frise ; le travailleur a rendu le deck de 9 slides à 0 erreur, planche regardée, aucun débordement. Le résultat est dans [exemple/essai-petit-modele/](exemple/essai-petit-modele/), tel que les sous-agents l'ont écrit, à deux retouches près : une mention « exemple fictif » ajoutée au pied des slides et en tête des fichiers, et la planche refaite avec le gabarit final.

Ces essais ont fait corriger six défauts : un deux-points rejeté en début de ligne, un chiffre seul trop petit sur sa slide, un mot à retenir invisible sur fond bleu, une liste refusée à tort sous « À l'écran » (le planificateur y a perdu un passage), les bornes des schémas absentes du skill d'histoire (le planificateur avait prévu cinq acteurs pour quatre couloirs ; le travailleur en a regroupé deux et l'a signalé), la longueur des titres de couverture et de conclusion inconnue du planificateur.

Non vérifié :

- **aucun essai avec les modèles visés** (256 000 tokens de contexte, faibles sur les visuels). C'est le premier essai à mener ;
- **l'orchestrateur n'a pas été joué** : ni le cadrage par séries de questions, ni l'accord, ni le renvoi du planificateur après une revue « À CORRIGER ». Les relais des essais ont été passés à la main, et le travailleur a mis en forme des cartes non corrigées ;
- **le vérificateur n'a pas été rejoué en version 0.3.0** : ni sur le fond, ni sur la forme, avec les nouvelles compositions ;
- **évaluation obligatoire non menée** : pas de cas de test, pas de comparaison avec le modèle seul, avec les versions précédentes ou avec l'orchestrateur général. Deux essais ne disent rien de la régularité. Les skills sont des hypothèses bien outillées, pas des résultats mesurés ;
- **la chaîne n'a été jouée que dans Claude Code.** Dans OpenCode, Codex et DeepSeek Harness, seule la découverte des skills est vérifiée : aucun deck n'y a été produit, et le lancement des sous-agents par l'orchestrateur n'y a pas été essayé. Pour Claude Code, à l'inverse, la découverte depuis `.claude/skills/` n'a pas été listée par l'outil ; c'est son dossier documenté ;
- **OpenCode V2** : la version installée sur le poste d'essai est la 1.18.30 ; la documentation de la V2 donne le même dossier ;
- `planche.py` et le rendu n'ont été essayés qu'avec Firefox, pas avec un navigateur de la famille Chromium ;
- les limites de longueur couvrent un texte courant. Un mot très long ou des capitales peuvent déborder sous la limite : la planche le montre.

## À savoir avant de diffuser

- **`histoire-slides` reprend la méthode d'un skill tiers**, `slide-crafting` (licences MIT et CC-BY-4.0). Le texte est réécrit, et `skills/histoire-slides/meta/origine.md` cite ce skill. Son auteur n'y est pas nommé : ajouter son nom avec son accord.
- **La charte de l'État est réservée à l'État.** Le dépôt officiel du DSFR indique « Utilisation interdite en dehors des sites Internet de l'État ». Hors de l'État, la chaîne s'arrête à la carte des messages, faute de skill de charte : il faudrait un skill équivalent, au même contrat (mêmes compositions, autre habillage).
- **Le bloc-marque** affiche « République Française » par défaut. L'intitulé d'une administration se règle dans l'en-tête du deck ; ses règles officielles n'ont pas été vérifiées ici.

## Points à valider

1. **Le remplacement de `slide-crafting` par `histoire-slides`.** Au seul compte des lignes, `slide-crafting` passait : le planificateur en lisait 318. Il est remplacé parce que ses lignes sont longues (trois fois plus de caractères que le nouveau skill) et qu'il apporte son propre déroulé, en concurrence avec celui de l'orchestrateur. Le rebrancher reste possible : il suffit de le nommer dans les rôles du planificateur et du vérificateur.
2. **Un seul point d'arrêt, sur l'histoire.** Le brief n'est pas validé à part : l'orchestrateur annonce ce qu'il a compris et enchaîne.
3. **Les seize compositions et leur rendu** : voir le catalogue. Les schémas n'ont que deux formes (flux en ligne, couloirs) et les graphiques une seule série : en manque-t-il une que tes decks emploient souvent (cycle, organigramme, barres groupées) ? Une composition de plus ne coûte rien au plafond tant qu'un deck en emploie dix au plus.
4. **Dix compositions différentes au plus par deck.** C'est la règle qui garde le travailleur sous 350 lignes.
5. **Les trois rôles sont des briefs** lus par des sous-agents ordinaires. Les transformer en agents à skills préchargés ne vaut la peine que si les essais montrent qu'un sous-agent oublie de lire son skill.

---
name: orchestrateur-slides
description: "Réalise un deck de slides de bout en bout avec des sous-agents : cadrage du besoin, histoire validée par l'utilisateur, production, vérification. À utiliser quand l'utilisateur appelle l'orchestrateur de slides ou demande explicitement ce mode de travail pour une présentation. Ne pas utiliser pour retoucher une slide ou un texte d'un deck existant, qui se fait directement."
metadata:
  version: "0.3.0"
  date: "2026-11-25"
---

Tu es l'orchestrateur d'un deck que tu réalises avec trois sous-agents : un planificateur, un travailleur, un vérificateur. Tu es le seul à parler à l'utilisateur, parce qu'un sous-agent ne peut pas lui poser de question. Avec lui, sois concis : il a peu de temps pour lire, donc va à l'essentiel et mets en avant ce qui demande une décision de sa part.

Le besoin est dans le message de l'utilisateur ; s'il manque, demande-le d'abord. Si la demande est une retouche (corriger une slide, changer un texte), dis-le et propose de la faire directement, sans sous-agents, parce que la chaîne coûte du temps et des tokens.

## Vue d'ensemble

| Étape | Qui | Fichier produit |
|---|---|---|
| 1. Cadrage | toi, avec l'utilisateur | `brief.md` |
| 2. Histoire | planificateur | `carte.md`, la carte des messages |
| 3. Revue du fond | vérificateur | `revue-fond.md` |
| 4. Accord | toi, avec l'utilisateur | `carte.md` validée |
| 5. Slides | travailleur | `deck/deck.html` |
| 6. Revue de la forme | vérificateur | `revue-forme.md` |
| 7. Livraison | toi | le deck et ses réserves |

Crée au début un dossier de travail (défaut : `deck-<sujet en deux mots>/` dans le dossier courant). Tous les fichiers y vont. Donne toujours des chemins absolus aux sous-agents.

## Quatre règles de sortie, pour toi et pour chaque sous-agent

Une réponse de modèle est plafonnée, souvent à 32 000 tokens, réflexion comprise. Un deck écrit d'un seul jet dépasse ce plafond et la réponse est coupée.

1. **Les relais passent par des fichiers.** Un sous-agent écrit son livrable dans un fichier et te rend dix lignes au plus : le chemin, le statut, les blocages. Tu ne recopies jamais un livrable dans un message.
2. **Quatre slides au plus par appel d'écriture.**
3. **Une correction modifie la slide visée**, jamais le fichier entier.
4. **Certains fichiers ne se lisent pas** : le dossier `deck/charte/` et tout fichier `*-autonome.html`. Toi, tu ne lis pas non plus `deck/deck.html`, ni les skills des sous-agents : chacun lit le sien, et sa revue ou son compte rendu te suffit.

## 1. Cadrage

Le but est d'en savoir assez pour que l'histoire soit la bonne, et de challenger le besoin : ce que l'utilisateur demande n'est pas toujours ce qui servira son auditoire.

Règles des questions :

- Pose seulement les questions dont la réponse change le deck.
- Pose-les par séries de cinq au plus, une série par message, vingt questions au plus en tout.
- Donne à chaque question une réponse par défaut que l'utilisateur accepte d'un mot.
- Après chaque série, relis les réponses et retire les questions qu'elles ont rendues inutiles, parce que les premières réponses répondent souvent aux suivantes. Pose une nouvelle série seulement s'il reste une inconnue qui change le deck.
- L'utilisateur peut arrêter quand il veut (« stop », « ça suffit », « j'en ai marre »). Tu retiens alors les réponses par défaut pour tout le reste, tu les lui listes en une fois et tu continues. Dis-lui cette possibilité dans la première série.
- Ouvre chaque série par son numéro et par le nombre de questions que tu prévois encore.

Ce qu'il faut savoir, dans cet ordre. Ne demande que ce que la demande ne dit pas déjà :

1. l'auditoire, et ce qu'il doit décider, faire ou retenir en sortant (la demande finale) ;
2. le canal : projeté et commenté, discuté en réunion, ou lu seul ;
3. la durée ou le nombre de slides ;
4. le message principal en une phrase ;
5. la matière source : fichiers, chiffres, citations, avec leurs chemins ;
6. ce que l'auditoire sait déjà, et ses objections probables ;
7. la charte : celle de l'État (skill `charte-dsfr`, avec l'intitulé du bloc-marque) ou celle d'un autre skill de charte ;
8. les contraintes : mentions obligatoires, confidentialité, noms à ne pas citer, échéance.

Challenge du besoin. Si l'utilisateur ne peut pas dire son message principal en une phrase, propose-lui deux formulations et fais-le choisir : sans ce message, le deck n'a pas de fil. Si deux réponses se contredisent (dix messages pour dix minutes, un auditoire qui décide et aucune demande finale), dis-le en une phrase avec ta recommandation, dans la série suivante.

Si la charte de l'État ne s'applique pas (le deck n'est pas fait pour une administration de l'État) et qu'aucun autre skill de charte n'est installé, dis-le : la chaîne s'arrête alors à la carte des messages validée, sans deck.

Écris ensuite `brief.md`, soixante lignes au plus, avec ces rubriques : Sujet · Auditoire · Demande finale · Canal et durée · Message principal · Matière source (chemins) · Objections attendues · Charte et bloc-marque · Contraintes · Réponses retenues par défaut. Annonce en trois lignes ce que tu as compris, puis lance l'étape 2 sans attendre : l'accord de l'utilisateur porte sur l'histoire, à l'étape 4.

## Lancer un sous-agent

Le message que tu envoies à un sous-agent tient en cinq lignes. Il part de zéro et lit lui-même ses fichiers.

```
Rôle : lis d'abord <dossier de ce skill>/references/role-<rôle>.md et suis-le. Mode : <fond ou forme, pour le vérificateur>.
Dossier de travail : <chemin absolu>
Skills : <dossier de ce skill> ; <dossier de chaque skill de la ligne du rôle, ci-dessous>
À faire : <l'étape, en une phrase ; s'il y a des corrections, le chemin de la revue à traiter>
Rendu : ton livrable dans son fichier, puis dix lignes au plus (chemin, statut, blocages).
```

Ne résume pas le rôle et ne recopie ni le brief ni la carte dans ce message, parce qu'un résumé perd des consignes. Les skills `histoire-slides` et `charte-dsfr` sont installés à côté de celui-ci, dans le même dossier parent : donne leurs chemins absolus. Si l'un manque, dis-le à l'utilisateur avant de lancer la chaîne.

| Rôle | Fichier de rôle | Skills à lui indiquer |
|---|---|---|
| planificateur | `references/role-planificateur.md` | `histoire-slides`, `charte-dsfr` |
| vérificateur, mode fond | `references/role-verificateur.md` | `histoire-slides`, `charte-dsfr` |
| travailleur | `references/role-travailleur.md` | `charte-dsfr` |
| vérificateur, mode forme | `references/role-verificateur.md` | `charte-dsfr` |

## 2 et 3. Histoire, puis revue du fond

Lance le planificateur, puis le vérificateur en mode fond. Si la revue dit « À CORRIGER », renvoie le planificateur avec le chemin de la revue. Deux allers-retours au plus ; au-delà, arrête-toi et présente à l'utilisateur le point bloquant avec ta recommandation.

## 4. Accord de l'utilisateur

Lis `carte.md` et présente, dans un seul message :

- le fil rouge, en une phrase ;
- la liste numérotée des titres, un par slide ;
- les emplacements « [à fournir … ] », qui attendent un fait de sa part ;
- les réserves de la revue qui restent ouvertes.

Demande-lui de valider ou de dire quoi changer, et attends sa réponse. S'il change les mots d'un titre, modifie `carte.md` toi-même. S'il change la structure (ordre, ajout, retrait, autre fil), renvoie le planificateur avec sa demande, repasse la revue du fond, puis reviens à cette étape.

## 5 et 6. Slides, puis revue de la forme

Lance le travailleur. Si la carte dépasse seize slides, lance-le une fois par temps de l'histoire, l'un après l'autre, sur le même deck. Lance ensuite le vérificateur en mode forme. Si la revue dit « À CORRIGER », renvoie le travailleur avec le chemin de la revue. Deux allers-retours au plus, comme à l'étape 3.

## 7. Livraison

Vérifie, avec les comptes rendus et la dernière revue, que le deck répond au brief : nombre de slides, demande finale présente. Puis livre :

- le chemin de `deck/deck.html` et la façon de l'ouvrir (dans un navigateur ; flèches pour avancer, N pour les notes) ;
- en trois lignes au plus : ce qui reste incertain ou non vérifié (un rendu non contrôlé, un fait à fournir), et les décisions qui reviennent à l'utilisateur.

S'il veut un seul fichier à envoyer, fais lancer le script d'assemblage de la charte.

## Sans sous-agents

Si cet environnement ne permet pas de lancer des sous-agents, dis-le dès le cadrage, puis tiens les rôles toi-même, l'un après l'autre. Lis le fichier de rôle et son skill au moment de tenir le rôle, et écris le même livrable dans le même fichier. En vérificateur, juge sur les contrôles du rôle et sur le fichier relu, pas sur ton souvenir de l'avoir écrit.

## Références

- `references/role-planificateur.md`, `references/role-travailleur.md`, `references/role-verificateur.md` : lus par le sous-agent qui tient le rôle, ou par toi quand tu le tiens faute de sous-agents.
- `scripts/controle_carte.py` : contrôle la carte des messages ; lancé par le planificateur et par le vérificateur.

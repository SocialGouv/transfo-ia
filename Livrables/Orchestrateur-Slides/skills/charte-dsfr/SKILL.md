---
name: charte-dsfr
description: "Met un deck de slides HTML à la charte de l'État (DSFR : Marianne, bloc-marque, bleu France), frises, schémas et graphiques compris, et vérifie que chaque texte tient dans sa zone. À utiliser dès qu'il faut produire, corriger ou contrôler des slides pour une administration de l'État, même si la demande dit seulement « aux couleurs du ministère » ou « en DSFR ». Ne pas utiliser hors de l'État, à qui le DSFR est interdit, ni pour décider du contenu d'un deck (histoire-slides)."
metadata:
  version: "0.3.0"
  date: "2026-11-25"
---

# Charte DSFR pour les slides

Ce skill fournit la mise en page d'un deck à la charte de l'État : un gabarit à copier, seize compositions de slide et quatre scripts. Tu choisis une composition et tu écris les textes dans ses emplacements. Tu n'écris ni style, ni classe, ni dessin, parce que le gabarit construit la mise en page et trace lui-même frises, schémas et graphiques, et qu'une mise en page improvisée déborde ou sort de la charte.

Les chemins partent du dossier de ce skill. Il te faut le contenu de chaque slide (une carte des messages, ou des textes fournis) : sans lui, demande-le, ce skill ne décide pas de l'histoire.

## Quand cette charte s'applique

- Le deck est fait pour une administration de l'État ou en son nom. Le dépôt officiel du DSFR indique « Utilisation interdite en dehors des sites Internet de l'État » : pour toute autre organisation, n'emploie pas ce skill et dis-le.
- Le bloc-marque affiche par défaut « République Française ». L'intitulé propre à une administration se demande, il ne se devine pas. Il s'écrit dans le réglage `deck-marque`, une barre oblique entre les lignes (« Ministère / de l'exemple »).

## Choisir la composition

| La slide montre | Composition | Quand |
|---|---|---|
| couverture | `couverture` | La première slide : le sujet, la promesse et les temps de l'histoire. |
| énoncé seul | `enonce` | Un message qui se suffit : une phrase à retenir, sans preuve à montrer à l'écran. |
| comparaison | `contraste` | Deux états à opposer : avant et après, problème et réponse, sans et avec. |
| section | `section` | Ouvrir un temps de l'histoire, dans un deck de plus de dix slides. |
| étapes | `etapes` | Trois à cinq étapes dans l'ordre. La dernière est l'arrivée : elle ressort en bleu France. |
| idées de même rang | `cartes` | Deux à quatre idées de même rang, sans ordre entre elles (des rôles, des volets, des options). |
| schéma à couloirs | `couloirs` | Qui fait quoi à chaque étape : deux à quatre acteurs en lignes, trois à six étapes en colonnes. |
| schéma de flux | `flux` | Deux à quatre acteurs ou systèmes, et ce que chacun passe au suivant. |
| tableau | `tableau` | Des éléments à croiser selon les mêmes critères. Quatre colonnes et cinq lignes au plus : au-delà, c'est un document. |
| chiffre | `chiffres` | Un à trois chiffres portent le message. Chaque chiffre a son libellé, et si possible son point de comparaison. |
| graphique en barres | `barres` | Deux à six grandeurs à comparer entre elles. L'axe part de zéro, le gabarit trace les barres. |
| courbe | `courbe` | Une évolution dans le temps, en trois à huit points. L'axe part de zéro, le gabarit trace la courbe. |
| frise datée | `frise` | Trois à six jalons dans le temps : un calendrier, un historique, une trajectoire. |
| liste | `liste` | Trois à cinq points de même nature, un par ligne (des règles, des engagements, des constats). |
| citation | `citation` | La parole de quelqu'un, mot pour mot, avec sa source. Jamais une phrase inventée. |
| conclusion | `conclusion` | La dernière slide : ce que l'auditoire retient, et ce qu'on lui demande. |

Si aucune composition ne convient, le message porte sans doute deux idées : signale-le au lieu d'inventer une mise en page. Un deck emploie dix compositions différentes au plus, pour garder son unité.

## Procédure

### 1. Copier le gabarit

```bash
cp -r assets/gabarit <dossier de sortie>/deck
```

Le deck est `deck/deck.html`, le seul fichier que tu lis et que tu modifies. Ne lis pas le dossier `deck/charte/` : plus de 50 000 caractères de styles et de script qui n'apprennent rien sur le contenu.

### 2. Remplir l'en-tête

Dans `deck/deck.html`, remplace les valeurs entre accolades, et rien d'autre dans l'en-tête :

- `<title>` : le titre du deck, 70 caractères au plus ;
- `deck-pied` : le pied de page, sous la forme « Sujet · Précision », 70 caractères au plus ;
- `deck-fil` : les deux à quatre temps de l'histoire, séparés par une barre verticale, 12 caractères au plus chacun. Sans temps, laisse `content=""` et n'écris aucun `data-temps`.

### 3. Écrire les slides, quatre par appel

Affiche la référence des compositions de ton deck, et lis-la en entier :

```bash
python3 scripts/reference.py <chemin de la carte des messages>
```

Elle donne les règles d'écriture, puis, pour chaque composition du deck, ses limites et un exemple. Sans carte, nomme les compositions : `python3 scripts/reference.py chiffres frise`. Pour chaque slide, recopie l'exemple de sa composition et remplace ses textes, sous la limite de chaque emplacement.

Insère chaque lot de quatre slides juste au-dessus de la ligne `<!-- FIN DES SLIDES`, par une modification ciblée. Ne réécris pas le fichier entier, parce qu'une réponse est limitée en longueur et qu'une réécriture efface ce qui était juste.

Si un texte dépasse sa limite, raccourcis la formulation sans changer le sens ni les chiffres. Si le sens ne tient pas, la slide porte sans doute deux idées : signale-le au lieu de serrer le texte.

### 4. Contrôler

```bash
python3 scripts/controle_deck.py <dossier de sortie>/deck/deck.html
```

Chaque ligne `ERREUR` nomme la slide, l'emplacement et la correction. Corrige par une modification ciblée, puis relance, jusqu'à « 0 erreur(s) ». Après trois passes sans y arriver, arrête-toi et rapporte les erreurs restantes. Une ligne `AVERTISSEMENT` ne bloque pas : reporte-la dans ton compte rendu.

### 5. Regarder le rendu

```bash
python3 scripts/planche.py <dossier de sortie>/deck/deck.html
```

Le script écrit `planche.png`, une image de toutes les slides. Si tu peux regarder une image, regarde-la : une slide encadrée en rouge déborde, et son étiquette nomme l'emplacement à raccourcir (un mot très long ou des capitales débordent parfois sous la limite). Sans navigateur, ou si tu ne peux pas regarder une image, écris « rendu non contrôlé » et la raison dans ton compte rendu : la personne ouvrira `deck.html?planche` elle-même.

### 6. Diffuser, seulement si on te le demande

`python3 scripts/assembler.py <dossier de sortie>/deck/deck.html` écrit un fichier HTML autonome à côté du dossier, à envoyer ou à publier. Il dépasse 300 000 caractères : ne le relis pas, ne le modifie pas. Toute correction se fait dans `deck/deck.html`, puis on assemble de nouveau.

## Corriger un deck existant

Modifie la slide visée dans `deck/deck.html`, puis relance le contrôle. Pour changer de composition, recopie le nouvel exemple et reportes-y les textes.

## Compte rendu

Dix lignes au plus : le chemin du deck, le nombre de slides, la ligne « Résultat » du contrôle recopiée, le rendu (regardé sur la planche, ou non contrôlé et pourquoi), les textes raccourcis (slide, avant, après), les emplacements « [à fournir … ] » restants.

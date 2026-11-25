# Maintenance du skill charte-dsfr

À lire pour modifier le skill, jamais pour faire un deck.

## Changer une limite ou un exemple

1. Modifier `scripts/compositions.py`, source unique des limites et des exemples. `scripts/reference.py` en tire ce qu'il affiche à l'agent : aucun fichier de référence n'est à régénérer.
2. Si le tableau « Choisir la composition » change (nature ou phrase « quand »), le recopier dans `SKILL.md` : un test le compare à la source.
3. Lancer `python3 -m unittest test_charte` depuis `scripts/`.
4. Vérifier le rendu aux limites : `python3 scripts/generer_reference.py --limites <dossier>` crée un deck où chaque emplacement est rempli à sa limite, puis `python3 scripts/planche.py <dossier>/deck.html`. Aucune slide ne doit être encadrée en rouge.
5. Vérifier l'autre extrême : `python3 scripts/generer_reference.py --minimum <dossier>` crée un deck où chaque composition a le moins d'éléments admis. Aucune slide ne doit paraître vide.

## Ajouter une composition

En plus des étapes ci-dessus :

- écrire son constructeur dans `assets/gabarit/charte/deck.js` (fonction `deplier`, objet `B`) et ses styles dans `assets/gabarit/charte/slides.css` ;
- écrire son exemple en écriture courte : des emplacements `data-slot`, des éléments répétés `data-item`, sans classe ;
- déclarer ce que ses éléments répétés admettent, dans `G(...)` : `icone` (attribut `data-icone`), `valeur` (attribut `data-valeur`, le nombre tracé), `retenir` (attribut `data-retenir`) ; un emplacement qui peut rester vide se déclare `S(..., vide=True)` ;
- si des emplacements doivent être en même nombre (cellules et en-têtes), le dire par la clé `alignement` ; si le dernier élément n'a pas de lien vers un suivant, par la clé `vers` ;
- ajouter sa nature au tableau du skill `histoire-slides` et aux valeurs par défaut de `orchestrateur-slides/scripts/controle_carte.py` : deux tests le vérifient.

Les chiffres du deck catalogue (lignes lues par agent, par version) sont une photographie du 25 novembre 2026 : ils ne se mettent pas à jour seuls.

## Choix de conception

- **Écriture courte** (version 0.2.0). Une slide ne contient que ses textes et leurs attributs ; `deck.js` construit au chargement la structure que les styles attendent. Une slide coûte environ un quart de caractères en moins à écrire (806 en moyenne dans le catalogue de la version 0.2.0, contre 1 099).
- **Typographie** (version 0.2.0). `deck.js` pose les espaces insécables de la typographie française (avant `: ; ! ? » % €`, après `«`, dans les nombres), et un chiffre seul sur sa slide s'affiche en très grand.
- **Frises, schémas, graphiques** (version 0.3.0). Cinq compositions sont dessinées par le gabarit à partir des seules données : `frise`, `barres`, `courbe`, `flux`, `couloirs`. Le modèle écrit des libellés et des nombres, jamais un dessin. Les graphiques partent de zéro, pour que l'échelle reste honnête.
- **Référence par script** (version 0.3.0). Avec seize compositions, la référence entière dépasserait ce qu'un agent doit lire. `reference.py` n'affiche que les compositions du deck, et un deck en emploie dix au plus (`COMMUN["compositions_max"]`, contrôlé sur la carte des messages).

## Vérifications faites

- Version 0.2.0 : rendu du catalogue et du deck aux limites identique au pixel près à celui de la version 0.1.0.
- Version 0.3.0 : les onze compositions d'origine, rendues avec les fichiers de charte d'avant et d'après, sont identiques au pixel près sur trois decks (aux limites, au minimum, catalogue). Les cinq nouvelles ne débordent ni aux limites ni au minimum.

## Limites connues

- `planche.py` n'a été essayé qu'avec Firefox.
- Les limites de longueur valent pour un texte courant : un mot très long ou des capitales peuvent déborder sous la limite, ce que la planche montre.
- Les règles officielles de l'intitulé du bloc-marque n'ont pas été vérifiées.
- Graphiques : une seule série, des valeurs positives. Une courbe dont les valeurs sont proches paraît plate, parce que l'axe part de zéro.
- Schémas : deux formes seulement, le flux en ligne et les couloirs. Ni cycle, ni arbre, ni organigramme.

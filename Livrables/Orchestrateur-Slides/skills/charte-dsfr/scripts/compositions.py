"""Source unique des compositions : limites de chaque emplacement et exemple à copier.

controle_deck.py lit ces limites, reference.py en tire ce qu'il affiche à l'agent.
Modifier une limite ici, puis relancer les tests et vérifier le rendu (meta/maintenance.md).

Les exemples sont en écriture courte : des emplacements (data-slot), des éléments répétés (data-item),
des notes (data-note). Le script charte/deck.js du gabarit en construit la mise en page ; une composition
ajoutée ici doit donc y recevoir son constructeur (fonction deplier). reference.py affiche à l'agent les
règles et les exemples des seules compositions de son deck.
"""

ICONES = [
    "i-alert", "i-arrow-down", "i-arrow-right", "i-award", "i-check", "i-cloud-off", "i-code",
    "i-compasses", "i-computer", "i-eye-off", "i-flashlight", "i-go-back", "i-line-chart", "i-links",
    "i-palette", "i-refresh", "i-roadmap", "i-scales", "i-server", "i-settings", "i-shield", "i-team",
    "i-user",
]

# Ce que chaque icône veut dire, pour en choisir une sans la voir.
SENS_ICONES = {
    "i-alert": "risque, alerte", "i-arrow-down": "vers le bas, conséquence", "i-arrow-right": "passage, suite",
    "i-award": "gain, réussite", "i-check": "fait, validé", "i-cloud-off": "hors ligne, coupure",
    "i-code": "développement", "i-compasses": "conception, méthode", "i-computer": "poste de travail, outil",
    "i-eye-off": "caché, hors du cadre", "i-flashlight": "opportunité, éclairage", "i-go-back": "retour en arrière",
    "i-line-chart": "mesure, tendance", "i-links": "dépendance, lien", "i-palette": "design, charte",
    "i-refresh": "cycle, continu", "i-roadmap": "trajectoire, plan", "i-scales": "arbitrage, conformité",
    "i-server": "infrastructure, hébergement", "i-settings": "mécanisme, automatisation",
    "i-shield": "protection, sécurité", "i-team": "équipe", "i-user": "personne, utilisateur",
}

TONS = ["acquis", "risque"]

# Réglages communs à tout le deck et à toute slide.
COMMUN = {
    "titre_deck": 70,   # <title>
    "pied": 70,         # meta deck-pied
    "temps_min": 2,     # meta deck-fil : nombre de temps de l'histoire
    "temps_max": 4,
    "temps_car": 12,    # longueur d'un temps
    "rubrique": 24,     # attribut data-rubrique d'une slide
    "notes_max": 5,     # notes d'orateur par slide
    "compositions_max": 10,  # compositions différentes dans un même deck : unité visuelle, et lecture bornée de l'agent
    "note_car": 300,
}


def S(maxi, requis=True, occ=(1, 1), vide=False):
    """Un emplacement : longueur maximale, présence obligatoire, nombre d'occurrences admis, texte vide admis."""
    mini = occ[0] if requis else 0
    return {"max": maxi, "requis": requis, "occ_min": mini, "occ_max": occ[1], "vide": vide}


def G(mini, maxi, slots, icone=False, valeur=False, retenir=False):
    """Un groupe d'éléments répétés (data-item) : combien, et leurs emplacements.

    icone : chaque élément porte data-icone. valeur : chaque élément porte data-valeur, le nombre tracé.
    retenir : un élément de la slide peut porter data-retenir, qui le met en avant.
    """
    return {"min": mini, "max": maxi, "slots": slots, "icone": icone, "valeur": valeur, "retenir": retenir}


TITRE = S(90)
CHAPO = S(95, requis=False)
SOURCE = S(90, requis=False)

# Balises admises à l'intérieur d'un emplacement ou d'une note, sans attribut.
BALISES_DE_TEXTE = ["em", "strong", "br", "sup", "sub"]

COMPOSITIONS = {
    "couverture": {
        "nature": "couverture",
        "quand": "La première slide : le sujet, la promesse et les temps de l'histoire.",
        "cadre": False,
        "slots": {
            "surtitre": S(45, requis=False), "titre": S(32), "accroche": S(95, requis=False),
            "auteur": S(40, requis=False), "fonction": S(55, requis=False), "plan-intitule": S(32),
        },
        "groupes": {"temps": G(2, 4, {"temps-titre": S(22), "temps-texte": S(55, requis=False)})},
        "exemple": """<section data-composition="couverture">
<p data-slot="surtitre">Orchestrateur de slides · Mode d’emploi</p>
<h2 data-slot="titre">Un deck, <em>trois agents</em></h2>
<p data-slot="accroche">Une histoire validée avant la première slide, un gabarit qui tient la mise en page.</p>
<p data-slot="auteur">L’équipe transformation IA</p>
<p data-slot="fonction">Catalogue des seize compositions du gabarit</p>
<p data-slot="plan-intitule">L’histoire, en trois temps</p>
<div data-item="temps"><p data-slot="temps-titre">Le problème</p><p data-slot="temps-texte">Ce qu’un modèle fait mal sur un deck</p></div>
<div data-item="temps"><p data-slot="temps-titre">La chaîne</p><p data-slot="temps-texte">Qui fait quoi, dans quel ordre</p></div>
<div data-item="temps"><p data-slot="temps-titre">Les garde-fous</p><p data-slot="temps-texte">Ce qui tient sans dépendre du modèle</p></div>
<p data-note>Ce deck sert de catalogue : une slide par composition du gabarit.</p>
</section>""",
    },
    "enonce": {
        "nature": "énoncé seul",
        "quand": "Un message qui se suffit : une phrase à retenir, sans preuve à montrer à l'écran.",
        "cadre": True,
        "slots": {"titre": S(75), "appui": S(130, requis=False)},
        "groupes": {},
        "exemple": """<section data-composition="enonce" data-rubrique="Le problème" data-temps="1" data-ton="risque">
<h2 data-slot="titre">Un modèle écrit vite des slides. Il raconte rarement <em>une histoire</em>.</h2>
<p data-slot="appui">Et il juge mal une mise en page : texte qui déborde, slide saturée, couleurs sans règle.</p>
<p data-note>Le mot en bleu est le mot à retenir : un seul par slide, balisé avec em.</p>
</section>""",
    },
    "section": {
        "nature": "section",
        "quand": "Ouvrir un temps de l'histoire, dans un deck de plus de dix slides.",
        "cadre": True,
        "slots": {"numero": S(2), "titre": S(60), "chapo": S(110, requis=False)},
        "groupes": {},
        "exemple": """<section data-composition="section" data-rubrique="La chaîne" data-temps="2">
<p data-slot="numero">2</p>
<h2 data-slot="titre">La chaîne : qui fait quoi</h2>
<p data-slot="chapo">Quatre rôles, une histoire validée par l’utilisateur avant toute production.</p>
</section>""",
    },
    "chiffres": {
        "nature": "chiffre",
        "quand": "Un à trois chiffres portent le message. Chaque chiffre a son libellé, et si possible son point de comparaison.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"chiffre": G(1, 3, {"valeur": S(8), "libelle": S(40), "detail": S(90, requis=False)})},
        "exemple": """<section data-composition="chiffres" data-rubrique="Les garde-fous" data-temps="3">
<h2 data-slot="titre">Trois limites dessinent le système</h2>
<p data-slot="chapo">Elles valent pour chaque agent de la chaîne, quel que soit le modèle.</p>
<div data-item="chiffre"><p data-slot="valeur">350</p><p data-slot="libelle">lignes de skills par agent, au plus</p><p data-slot="detail">Chaque agent ne lit que son rôle et le skill qui le sert.</p></div>
<div data-item="chiffre" data-ton="risque"><p data-slot="valeur">32 000</p><p data-slot="libelle">tokens par réponse</p><p data-slot="detail">Un deck entier écrit d’un coup dépasse ce plafond.</p></div>
<div data-item="chiffre" data-ton="acquis"><p data-slot="valeur">4</p><p data-slot="libelle">slides par appel d’écriture</p><p data-slot="detail">Chaque lot reste loin du plafond.</p></div>
</section>""",
    },
    "cartes": {
        "nature": "idées de même rang",
        "quand": "Deux à quatre idées de même rang, sans ordre entre elles (des rôles, des volets, des options).",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"carte": G(2, 4, {"carte-titre": S(30), "carte-texte": S(110)}, icone=True)},
        "exemple": """<section data-composition="cartes" data-rubrique="La chaîne" data-temps="2">
<h2 data-slot="titre">Quatre rôles, un seul agent par rôle</h2>
<div data-item="carte" data-icone="i-user"><p data-slot="carte-titre">Orchestrateur</p><p data-slot="carte-texte">Il questionne le besoin, passe les relais et tient le point d’arrêt.</p></div>
<div data-item="carte" data-icone="i-roadmap"><p data-slot="carte-titre">Planificateur</p><p data-slot="carte-texte">Il décide l’histoire : le fil, un message par slide, la demande finale.</p></div>
<div data-item="carte" data-icone="i-palette"><p data-slot="carte-titre">Travailleur</p><p data-slot="carte-texte">Il donne sa forme à chaque message, avec les compositions du gabarit.</p></div>
<div data-item="carte" data-icone="i-scales"><p data-slot="carte-titre">Vérificateur</p><p data-slot="carte-texte">Il juge sur pièces : le fond d’abord, la forme ensuite.</p></div>
</section>""",
    },
    "contraste": {
        "nature": "comparaison",
        "quand": "Deux états à opposer : avant et après, problème et réponse, sans et avec.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"cote": G(2, 2, {"etiquette": S(20), "cote-titre": S(55), "point": S(80, occ=(1, 3))})},
        "exemple": """<section data-composition="contraste" data-rubrique="Le problème" data-temps="1">
<h2 data-slot="titre">On retire au modèle ce qu’il fait mal, on lui laisse ce qu’il fait bien</h2>
<div data-item="cote">
<p data-slot="etiquette">Sans la chaîne</p>
<p data-slot="cote-titre">Le modèle décide de tout, d’un seul jet</p>
<p data-slot="point">L’histoire se découvre quand le deck est fini</p>
<p data-slot="point">La mise en page est réinventée à chaque slide</p>
<p data-slot="point">Rien ne mesure si le texte tient dans sa zone</p>
</div>
<div data-item="cote">
<p data-slot="etiquette">Avec la chaîne</p>
<p data-slot="cote-titre">Le modèle écrit, le gabarit tient la mise en page</p>
<p data-slot="point">L’histoire est validée avant la première slide</p>
<p data-slot="point">Seize compositions fermées, aucun style à écrire</p>
<p data-slot="point">Un script refuse tout texte trop long</p>
</div>
</section>""",
    },
    "etapes": {
        "nature": "étapes",
        "quand": "Trois à cinq étapes dans l'ordre. La dernière est l'arrivée : elle ressort en bleu France.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"etape": G(3, 5, {"etape-titre": S(26), "etape-texte": S(70)})},
        "exemple": """<section data-composition="etapes" data-rubrique="La chaîne" data-temps="2">
<h2 data-slot="titre">L’histoire est validée avant que la première slide existe</h2>
<div data-item="etape"><p data-slot="etape-titre">Cadrage</p><p data-slot="etape-texte">Des questions par séries de cinq, vingt au plus</p></div>
<div data-item="etape"><p data-slot="etape-titre">Histoire</p><p data-slot="etape-texte">La carte des messages, un titre par slide</p></div>
<div data-item="etape"><p data-slot="etape-titre">Accord</p><p data-slot="etape-texte">L’utilisateur valide ou corrige l’histoire</p></div>
<div data-item="etape"><p data-slot="etape-titre">Slides</p><p data-slot="etape-texte">Le gabarit rempli par lots de quatre slides</p></div>
<div data-item="etape"><p data-slot="etape-titre">Deck livré</p><p data-slot="etape-texte">Contrôlé par script, puis relu sur la planche</p></div>
</section>""",
    },
    "liste": {
        "nature": "liste",
        "quand": "Trois à cinq points de même nature, un par ligne (des règles, des engagements, des constats).",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"ligne": G(3, 5, {"ligne-titre": S(60), "ligne-texte": S(95, requis=False)}, icone=True)},
        "exemple": """<section data-composition="liste" data-rubrique="Les garde-fous" data-temps="3">
<h2 data-slot="titre">Quatre règles gardent chaque réponse sous le plafond</h2>
<div data-item="ligne" data-icone="i-palette"><p data-slot="ligne-titre">Le gabarit est copié, jamais réécrit</p><p data-slot="ligne-texte">Styles, polices et bloc-marque ne coûtent aucun token de sortie.</p></div>
<div data-item="ligne" data-icone="i-code"><p data-slot="ligne-titre">Quatre slides au plus par appel d’écriture</p><p data-slot="ligne-texte">Le deck se construit lot après lot, dans le même fichier.</p></div>
<div data-item="ligne" data-icone="i-links"><p data-slot="ligne-titre">Les relais passent par des fichiers</p><p data-slot="ligne-texte">Un sous-agent rend dix lignes : le chemin, le statut, les blocages.</p></div>
<div data-item="ligne" data-icone="i-check"><p data-slot="ligne-titre">Une correction modifie la slide visée</p><p data-slot="ligne-texte">Le fichier entier n’est jamais réécrit.</p></div>
</section>""",
    },
    "tableau": {
        "nature": "tableau",
        "quand": "Des éléments à croiser selon les mêmes critères. Quatre colonnes et cinq lignes au plus : au-delà, c'est un document.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO, "entete": S(22, occ=(2, 4))},
        "groupes": {"rangee": G(2, 5, {"cellule": S(40, occ=(2, 4))})},
        "alignement": {"groupe": "rangee", "slot": "cellule", "sur": "entete"},
        "regle": "Chaque `rangee` a autant de `cellule` que le tableau a d'`entete` ; sa première cellule est l'intitulé de la ligne.",
        "exemple": """<section data-composition="tableau" data-rubrique="La chaîne" data-temps="2">
<h2 data-slot="titre">Chaque rôle ne charge que ce qui lui sert</h2>
<p data-slot="entete">Rôle</p><p data-slot="entete">Il lit</p><p data-slot="entete">Il écrit</p><p data-slot="entete">Son skill</p>
<div data-item="rangee"><p data-slot="cellule">Orchestrateur</p><p data-slot="cellule">La demande, les comptes rendus</p><p data-slot="cellule">Le brief</p><p data-slot="cellule">orchestrateur-slides</p></div>
<div data-item="rangee"><p data-slot="cellule">Planificateur</p><p data-slot="cellule">Le brief, la matière source</p><p data-slot="cellule">La carte des messages</p><p data-slot="cellule">histoire-slides</p></div>
<div data-item="rangee"><p data-slot="cellule">Travailleur</p><p data-slot="cellule">La carte, les compositions</p><p data-slot="cellule">Le deck</p><p data-slot="cellule">charte-dsfr</p></div>
<div data-item="rangee"><p data-slot="cellule">Vérificateur</p><p data-slot="cellule">La carte, puis le deck</p><p data-slot="cellule">Deux revues</p><p data-slot="cellule">histoire-slides, charte-dsfr</p></div>
</section>""",
    },
    "frise": {
        "nature": "frise datée",
        "quand": "Trois à six jalons dans le temps : un calendrier, un historique, une trajectoire.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"jalon": G(3, 6, {"jalon-date": S(14), "jalon-titre": S(30), "jalon-texte": S(60, requis=False)}, retenir=True)},
        "regle": "`data-ton=\"acquis\"` sur un `jalon` le marque comme fait, `data-ton=\"risque\"` comme menacé.",
        "exemple": """<section data-composition="frise" data-rubrique="Les garde-fous" data-temps="3">
<h2 data-slot="titre">Trois versions sont livrées, l’essai avec les modèles visés reste à faire</h2>
<div data-item="jalon" data-ton="acquis"><p data-slot="jalon-date">Version 0.1</p><p data-slot="jalon-titre">La chaîne et le gabarit</p><p data-slot="jalon-texte">Quatre rôles, onze compositions</p></div>
<div data-item="jalon" data-ton="acquis"><p data-slot="jalon-date">Version 0.2</p><p data-slot="jalon-titre">350 lignes par agent</p><p data-slot="jalon-texte">Écriture courte, skill d’histoire</p></div>
<div data-item="jalon" data-ton="acquis"><p data-slot="jalon-date">Version 0.3</p><p data-slot="jalon-titre">Frises, schémas, graphiques</p><p data-slot="jalon-texte">Cinq compositions dessinées par le gabarit</p></div>
<div data-item="jalon" data-retenir><p data-slot="jalon-date">Ensuite</p><p data-slot="jalon-titre">Essai avec les modèles visés</p><p data-slot="jalon-texte">256 000 tokens, faibles sur les visuels</p></div>
</section>""",
    },
    "barres": {
        "nature": "graphique en barres",
        "quand": "Deux à six grandeurs à comparer entre elles. L'axe part de zéro, le gabarit trace les barres.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO, "source": SOURCE},
        "groupes": {"barre": G(2, 6, {"barre-libelle": S(30), "barre-valeur": S(10)}, valeur=True, retenir=True)},
        "exemple": """<section data-composition="barres" data-rubrique="Les garde-fous" data-temps="3">
<h2 data-slot="titre">En version 0.1, deux agents lisaient plus de 550 lignes de skills</h2>
<div data-item="barre" data-valeur="119"><p data-slot="barre-libelle">Orchestrateur</p><p data-slot="barre-valeur">119</p></div>
<div data-item="barre" data-valeur="318"><p data-slot="barre-libelle">Planificateur</p><p data-slot="barre-valeur">318</p></div>
<div data-item="barre" data-valeur="258"><p data-slot="barre-libelle">Vérificateur, sur le fond</p><p data-slot="barre-valeur">258</p></div>
<div data-item="barre" data-valeur="555" data-ton="risque"><p data-slot="barre-libelle">Travailleur</p><p data-slot="barre-valeur">555</p></div>
<div data-item="barre" data-valeur="552" data-ton="risque"><p data-slot="barre-libelle">Vérificateur, sur la forme</p><p data-slot="barre-valeur">552</p></div>
<p data-slot="source">Source : outils/budget_contexte.py, mesure du 25 novembre 2026</p>
</section>""",
    },
    "courbe": {
        "nature": "courbe",
        "quand": "Une évolution dans le temps, en trois à huit points. L'axe part de zéro, le gabarit trace la courbe.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO, "source": SOURCE},
        "groupes": {"point": G(3, 8, {"point-libelle": S(12), "point-valeur": S(7)}, valeur=True, retenir=True)},
        "exemple": """<section data-composition="courbe" data-rubrique="Les garde-fous" data-temps="3">
<h2 data-slot="titre">La référence des compositions lue par le travailleur a fondu de moitié</h2>
<div data-item="point" data-valeur="370"><p data-slot="point-libelle">Version 0.1</p><p data-slot="point-valeur">370</p></div>
<div data-item="point" data-valeur="177"><p data-slot="point-libelle">Version 0.2</p><p data-slot="point-valeur">177</p></div>
<div data-item="point" data-valeur="170" data-retenir><p data-slot="point-libelle">Version 0.3</p><p data-slot="point-valeur">170</p></div>
<p data-slot="source">Source : outils/budget_contexte.py, lignes lues au plus, 25 novembre 2026</p>
</section>""",
    },
    "flux": {
        "nature": "schéma de flux",
        "quand": "Deux à quatre acteurs ou systèmes, et ce que chacun passe au suivant.",
        "cadre": True,
        "entier": True,   # la référence garde l'exemple entier : le dernier bloc n'a pas de « bloc-vers »
        "vers": {"groupe": "bloc", "slot": "bloc-vers"},
        "slots": {"titre": TITRE, "chapo": CHAPO},
        "groupes": {"bloc": G(2, 4, {"bloc-titre": S(24), "bloc-texte": S(70, requis=False), "bloc-vers": S(20, requis=False)},
                              icone=True, retenir=True)},
        "regle": "`bloc-vers` nomme ce qui part vers le bloc suivant : le dernier `bloc` n'en a pas.",
        "exemple": """<section data-composition="flux" data-rubrique="La chaîne" data-temps="2">
<h2 data-slot="titre">Chaque agent rend un fichier, que le suivant relit</h2>
<div data-item="bloc" data-icone="i-roadmap"><p data-slot="bloc-titre">Planificateur</p><p data-slot="bloc-texte">Il décide l’histoire, un message par slide.</p><p data-slot="bloc-vers">carte.md</p></div>
<div data-item="bloc" data-icone="i-palette"><p data-slot="bloc-titre">Travailleur</p><p data-slot="bloc-texte">Il remplit le gabarit, quatre slides par appel.</p><p data-slot="bloc-vers">deck.html</p></div>
<div data-item="bloc" data-icone="i-scales"><p data-slot="bloc-titre">Vérificateur</p><p data-slot="bloc-texte">Il juge sur pièces et rend une revue.</p></div>
</section>""",
    },
    "couloirs": {
        "nature": "schéma à couloirs",
        "quand": "Qui fait quoi à chaque étape : deux à quatre acteurs en lignes, trois à six étapes en colonnes.",
        "cadre": True,
        "slots": {"titre": TITRE, "chapo": CHAPO, "etape-nom": S(14, occ=(3, 6))},
        "groupes": {"couloir": G(2, 4, {"couloir-nom": S(16), "case": S(36, occ=(3, 6), vide=True)}, retenir=True)},
        "alignement": {"groupe": "couloir", "slot": "case", "sur": "etape-nom"},
        "regle": "Chaque `couloir` a autant de `case` qu'il y a d'`etape-nom` ; une `case` reste vide quand l'acteur ne fait rien à cette étape.",
        "exemple": """<section data-composition="couloirs" data-rubrique="La chaîne" data-temps="2">
<h2 data-slot="titre">L’utilisateur intervient trois fois, les agents font le reste</h2>
<p data-slot="etape-nom">Cadrage</p><p data-slot="etape-nom">Histoire</p><p data-slot="etape-nom">Accord</p><p data-slot="etape-nom">Slides</p><p data-slot="etape-nom">Livraison</p>
<div data-item="couloir" data-retenir><p data-slot="couloir-nom">Utilisateur</p><p data-slot="case">répond aux questions</p><p data-slot="case"></p><p data-slot="case">valide l’histoire</p><p data-slot="case"></p><p data-slot="case">reçoit le deck</p></div>
<div data-item="couloir"><p data-slot="couloir-nom">Orchestrateur</p><p data-slot="case">cadre et challenge</p><p data-slot="case"></p><p data-slot="case">présente les titres</p><p data-slot="case"></p><p data-slot="case">livre, avec ses réserves</p></div>
<div data-item="couloir"><p data-slot="couloir-nom">Sous-agents</p><p data-slot="case"></p><p data-slot="case">écrivent et relisent la carte</p><p data-slot="case"></p><p data-slot="case">font et contrôlent le deck</p><p data-slot="case"></p></div>
</section>""",
    },
    "citation": {
        "nature": "citation",
        "quand": "La parole de quelqu'un, mot pour mot, avec sa source. Jamais une phrase inventée.",
        "cadre": True,
        "slots": {"titre": TITRE, "citation": S(200), "auteur": S(60), "contexte": S(70, requis=False)},
        "groupes": {},
        "exemple": """<section data-composition="citation" data-rubrique="Les garde-fous" data-temps="3">
<h2 data-slot="titre">La charte de l’État se réserve aux productions de l’État</h2>
<p data-slot="citation">«&nbsp;Utilisation interdite en dehors des sites Internet de l’État&nbsp;»</p>
<p data-slot="auteur">Dépôt officiel du DSFR</p>
<p data-slot="contexte">README, section «&nbsp;Licence et droit d’utilisation&nbsp;»</p>
</section>""",
    },
    "conclusion": {
        "nature": "conclusion",
        "quand": "La dernière slide : ce que l'auditoire retient, et ce qu'on lui demande.",
        "cadre": False,
        "slots": {"surtitre": S(30, requis=False), "titre": S(42), "demande-intitule": S(34)},
        "groupes": {
            "gain": G(3, 5, {"gain-titre": S(38), "gain-texte": S(50, requis=False)}, icone=True),
            "demande": G(1, 2, {"demande-quand": S(20), "demande-texte": S(70)}),
        },
        "exemple": """<section data-composition="conclusion">
<p data-slot="surtitre">En résumé</p>
<h2 data-slot="titre">Ce que la chaîne <em>garantit</em></h2>
<div data-item="gain" data-icone="i-roadmap"><p data-slot="gain-titre">L’histoire validée avant de produire</p><p data-slot="gain-texte">Le fil se lit dans les seuls titres</p></div>
<div data-item="gain" data-icone="i-palette"><p data-slot="gain-titre">Une mise en page tenue par le gabarit</p><p data-slot="gain-texte">Seize compositions, des limites mesurées</p></div>
<div data-item="gain" data-icone="i-shield"><p data-slot="gain-titre">Des réponses sous le plafond de sortie</p><p data-slot="gain-texte">Quatre slides par appel, relais par fichiers</p></div>
<p data-slot="demande-intitule">Ce que nous vous demandons</p>
<div data-item="demande"><p data-slot="demande-quand">Aujourd’hui</p><p data-slot="demande-texte">Valider cette version de la chaîne</p></div>
<div data-item="demande"><p data-slot="demande-quand">Ensuite</p><p data-slot="demande-texte">L’essayer sur un vrai deck, avec les modèles visés</p></div>
</section>""",
    },
}

# Ordre de présentation dans la référence et dans le catalogue : il raconte une histoire.
ORDRE = ["couverture", "enonce", "contraste", "section", "etapes", "cartes", "couloirs", "flux", "tableau",
         "chiffres", "barres", "courbe", "frise", "liste", "citation", "conclusion"]

# Réglages du deck catalogue (les quatre valeurs de l'en-tête).
CATALOGUE = {
    "titre": "Un deck, trois agents",
    "pied": "Orchestrateur de slides · Catalogue des compositions",
    "fil": "Le problème | La chaîne | Garde-fous",
}

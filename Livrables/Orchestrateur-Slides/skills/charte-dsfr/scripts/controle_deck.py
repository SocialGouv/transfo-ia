#!/usr/bin/env python3
"""Contrôle un deck construit avec le gabarit de la charte.

Vérifie, sans navigateur : le HTML est bien formé, chaque slide emploie une composition
connue, chaque emplacement est présent et tient sous sa limite, tout texte est dans un
emplacement ou une note, aucun style n'est ajouté.
Les limites sont calibrées pour qu'un texte qui les respecte ne déborde pas à l'écran.

Usage : python3 controle_deck.py chemin/deck.html
Sortie : une ligne par problème, puis un résultat.
Code de sortie : 0 aucune erreur · 1 au moins une erreur · 2 fichier illisible ou usage incorrect.
"""
import os
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compositions import BALISES_DE_TEXTE, COMMUN, COMPOSITIONS, ICONES, TONS  # noqa: E402

VIDES = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Noeud:
    """Un élément HTML : balise, attributs, enfants (éléments ou chaînes de texte)."""

    def __init__(self, tag, attrs=None, parent=None, ligne=0):
        self.tag = tag
        self.attrs = {k: (v if v is not None else "") for k, v in (attrs or [])}
        self.enfants = []
        self.parent = parent
        self.ligne = ligne

    def descendants(self):
        for e in self.enfants:
            if isinstance(e, Noeud):
                yield e
                yield from e.descendants()

    def texte(self):
        morceaux = []

        def visite(n):
            for e in n.enfants:
                if isinstance(e, str):
                    morceaux.append(e)
                elif e.tag == "br":
                    morceaux.append(" ")
                else:
                    visite(e)

        visite(self)
        return " ".join("".join(morceaux).split())

    def classes(self):
        return self.attrs.get("class", "").split()

    def ancetre(self, attribut, limite=None):
        """Le plus proche ancêtre qui porte cet attribut, sans remonter au-delà de `limite`."""
        n = self.parent
        while n is not None and n is not limite:
            if attribut in n.attrs:
                return n
            n = n.parent
        return None


class Arbre(HTMLParser):
    """Construit l'arbre et relève les balises mal fermées."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.racine = Noeud("#document")
        self.pile = [self.racine]
        self.defauts = []

    def handle_starttag(self, tag, attrs):
        n = Noeud(tag, attrs, self.pile[-1], self.getpos()[0])
        self.pile[-1].enfants.append(n)
        if tag not in VIDES:
            self.pile.append(n)

    def handle_startendtag(self, tag, attrs):
        self.pile[-1].enfants.append(Noeud(tag, attrs, self.pile[-1], self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VIDES:
            return
        ligne = self.getpos()[0]
        ouverts = [n.tag for n in self.pile[1:]]
        if tag not in ouverts:
            self.defauts.append(f"ligne {ligne} : balise fermante </{tag}> sans balise ouvrante")
            return
        while self.pile[-1].tag != tag:
            mal = self.pile.pop()
            self.defauts.append(f"ligne {mal.ligne} : balise <{mal.tag}> jamais fermée (</{tag}> rencontrée ligne {ligne})")
        self.pile.pop()

    def handle_data(self, data):
        self.pile[-1].enfants.append(data)

    def close(self):
        super().close()
        for n in self.pile[1:]:
            self.defauts.append(f"ligne {n.ligne} : balise <{n.tag}> jamais fermée")


def analyser(html):
    arbre = Arbre()
    arbre.feed(html)
    arbre.close()
    return arbre.racine, arbre.defauts


_EXEMPLES = None


def _textes_exemples():
    """Les textes des exemples de la charte, pour repérer ceux qui sont restés en place."""
    global _EXEMPLES
    if _EXEMPLES is None:
        _EXEMPLES = set()
        for c in COMPOSITIONS.values():
            racine, _ = analyser(c["exemple"])
            for n in racine.descendants():
                if "data-slot" in n.attrs and len(n.texte()) >= 20:
                    _EXEMPLES.add(n.texte())
    return _EXEMPLES


def _controler_emplacements(ou, noeuds, spec, erreurs):
    """Présence, nombre et longueur des emplacements d'une slide ou d'un élément répété."""
    par_nom = {}
    for n in noeuds:
        par_nom.setdefault(n.attrs["data-slot"], []).append(n)
    for nom, liste in par_nom.items():
        if nom not in spec:
            connus = ", ".join(sorted(spec)) or "aucun"
            erreurs.append(f"{ou} · emplacement « {nom} » inconnu ici (ligne {liste[0].ligne}). Emplacements admis : {connus}.")
    for nom, regle in spec.items():
        liste = par_nom.get(nom, [])
        if len(liste) < regle["occ_min"]:
            manque = "manquant" if regle["occ_max"] == 1 else f"présent {len(liste)} fois, minimum {regle['occ_min']}"
            erreurs.append(f"{ou} · emplacement « {nom} » {manque}.")
        if len(liste) > regle["occ_max"]:
            erreurs.append(f"{ou} · emplacement « {nom} » présent {len(liste)} fois, maximum {regle['occ_max']}.")
        for n in liste:
            longueur = len(n.texte())
            if longueur == 0 and regle["vide"]:
                continue
            if longueur == 0:
                erreurs.append(f"{ou} · emplacement « {nom} » vide (ligne {n.ligne}). Le remplir ou retirer sa balise.")
            elif longueur > regle["max"]:
                erreurs.append(
                    f"{ou} · emplacement « {nom} » : {longueur} caractères, maximum {regle['max']} "
                    f"(ligne {n.ligne}). Raccourcir de {longueur - regle['max']} caractères."
                )


MARQUES = ("data-slot", "data-item", "data-note")
# Attributs réservés à certains éléments répétés : (attribut, clé du groupe, ce qui manque à la composition sinon).
RESERVES = (("data-icone", "icone", "d'icône"), ("data-valeur", "valeur", "de valeur tracée"), ("data-retenir", "retenir", "d'élément à retenir"))


def _nombre(brut):
    """Le nombre d'un attribut data-valeur (« 72 », « 12,5 », « 1 200 »), ou None s'il n'est pas un nombre positif."""
    try:
        v = float("".join(brut.split()).replace("\u00a0", "").replace(",", "."))
    except ValueError:
        return None
    return v if v >= 0 else None


def _controler_contenu(ou, slide, erreurs):
    """Tout texte est dans un emplacement ou une note, et un emplacement ne contient que du texte.

    Le gabarit n'affiche que les emplacements, les éléments répétés et les notes : le reste disparaît à l'écran.
    """

    def visite(n, dans_texte):
        for e in n.enfants:
            if isinstance(e, str):
                if e.strip() and not dans_texte:
                    extrait = " ".join(e.split())[:40]
                    erreurs.append(f"{ou} · texte hors emplacement, dans <{n.tag}> ligne {n.ligne} : « {extrait} ». Il ne s'affichera pas : "
                                   "le placer dans un emplacement de la composition, ou dans une note <p data-note>.")
            elif dans_texte:
                if e.tag not in BALISES_DE_TEXTE or e.attrs:
                    erreurs.append(f"{ou} · balise <{e.tag}> non admise dans un emplacement (ligne {e.ligne}). "
                                   f"Y écrire du texte, avec seulement ces balises, sans attribut : {', '.join(BALISES_DE_TEXTE)}.")
                else:
                    visite(e, True)
            elif "data-slot" in e.attrs or "data-note" in e.attrs:
                visite(e, True)
            elif "data-item" in e.attrs or any(m in d.attrs for d in e.descendants() for m in MARQUES):
                visite(e, False)
            else:
                erreurs.append(f"{ou} · balise <{e.tag}> hors emplacement (ligne {e.ligne}) : elle ne s'affichera pas. La composition "
                               "n'affiche que ses emplacements (data-slot), ses éléments répétés (data-item) et les notes (data-note).")

    visite(slide, False)


def controler(html):
    """Renvoie (erreurs, avertissements, nombre de slides)."""
    erreurs, avertissements = [], []
    racine, defauts = analyser(html)
    erreurs.extend(f"HTML mal formé · {d}" for d in defauts)

    lignes_accolades = [str(i) for i, ligne in enumerate(html.splitlines(), 1) if "{{" in ligne or "}}" in ligne]
    if lignes_accolades:
        erreurs.append("Valeur entre accolades non remplacée, ligne " + ", ".join(lignes_accolades[:8]) + ".")

    tous = list(racine.descendants())
    titres = [n for n in tous if n.tag == "title"]
    if not titres or not titres[0].texte():
        erreurs.append("En-tête · <title> manquant ou vide.")
    elif len(titres[0].texte()) > COMMUN["titre_deck"]:
        erreurs.append(f"En-tête · <title> : {len(titres[0].texte())} caractères, maximum {COMMUN['titre_deck']}.")
    metas = {n.attrs.get("name"): n.attrs.get("content", "") for n in tous if n.tag == "meta" and n.attrs.get("name")}
    for nom in ("deck-marque", "deck-pied"):
        if not metas.get(nom, "").strip():
            erreurs.append(f"En-tête · <meta name=\"{nom}\"> manquant ou vide.")
    if len(metas.get("deck-pied", "")) > COMMUN["pied"]:
        erreurs.append(f"En-tête · deck-pied : {len(metas['deck-pied'])} caractères, maximum {COMMUN['pied']}.")
    temps = [t.strip() for t in metas.get("deck-fil", "").split("|") if t.strip()]
    if temps and not (COMMUN["temps_min"] <= len(temps) <= COMMUN["temps_max"]):
        erreurs.append(f"En-tête · deck-fil : {len(temps)} temps, il en faut {COMMUN['temps_min']} à {COMMUN['temps_max']} (ou aucun).")
    for t in temps:
        if len(t) > COMMUN["temps_car"]:
            erreurs.append(f"En-tête · deck-fil : « {t} » fait {len(t)} caractères, maximum {COMMUN['temps_car']}.")
    liens = " ".join(n.attrs.get("href", "") for n in tous if n.tag == "link")
    scripts = [n for n in tous if n.tag == "script"]
    if "charte/slides.css" not in liens or "charte/bloc-marque.css" not in liens:
        erreurs.append("En-tête · les deux liens vers charte/bloc-marque.css et charte/slides.css doivent rester en place.")
    if not any(n.attrs.get("src", "").endswith("charte/deck.js") for n in scripts):
        erreurs.append("Fin du fichier · <script src=\"charte/deck.js\"> doit rester en place.")
    for n in tous:
        if n.tag == "style":
            erreurs.append(f"ligne {n.ligne} · balise <style> interdite : la charte fournit tous les styles.")
        if n.tag == "script" and not n.attrs.get("src", "").endswith("charte/deck.js"):
            erreurs.append(f"ligne {n.ligne} · balise <script> interdite : seul charte/deck.js est admis.")

    slides = [n for n in tous if n.tag == "section"]
    if not slides:
        erreurs.append("Aucune slide : il faut au moins une <section data-composition=\"…\">.")
    a_fournir, restes = [], []
    for i, s in enumerate(slides, 1):
        comp = s.attrs.get("data-composition", "")
        ou = f"slide {i} ({comp or 'sans composition'})"
        if comp not in COMPOSITIONS:
            erreurs.append(f"{ou} · composition inconnue. Compositions admises : {', '.join(COMPOSITIONS)}.")
            continue
        spec = COMPOSITIONS[comp]
        dedans = list(s.descendants())

        for n in [s] + dedans:
            if "style" in n.attrs:
                erreurs.append(f"{ou} · attribut style interdit sur <{n.tag}> (ligne {n.ligne}) : la mise en page vient de la composition.")
            for attribut, cle, manque in RESERVES:
                if attribut in n.attrs and not spec["groupes"].get(n.attrs.get("data-item", ""), {}).get(cle):
                    avec = [g for g, groupe in spec["groupes"].items() if groupe[cle]]
                    ou_le_mettre = f"il va sur les éléments « {', '.join(avec)} »" if avec else f"cette composition n'a pas {manque}"
                    erreurs.append(f"{ou} · attribut {attribut} non admis sur <{n.tag}> (ligne {n.ligne}) : {ou_le_mettre}.")
        _controler_contenu(ou, s, erreurs)

        rubrique = s.attrs.get("data-rubrique", "")
        if len(rubrique) > COMMUN["rubrique"]:
            erreurs.append(f"{ou} · data-rubrique : {len(rubrique)} caractères, maximum {COMMUN['rubrique']}.")
        if "data-temps" in s.attrs:
            valeur = s.attrs["data-temps"]
            if not valeur.isdigit() or not (1 <= int(valeur) <= max(len(temps), 1)) or not temps:
                erreurs.append(f"{ou} · data-temps=\"{valeur}\" ne désigne aucun temps de deck-fil ({len(temps)} temps déclarés).")
        if s.attrs.get("data-ton") and s.attrs["data-ton"] not in TONS:
            erreurs.append(f"{ou} · data-ton=\"{s.attrs['data-ton']}\" inconnu. Tons admis : {', '.join(TONS)}.")

        porteurs = [n for n in dedans if "data-slot" in n.attrs]
        elements = [n for n in dedans if "data-item" in n.attrs]
        for e in elements:
            if e.ancetre("data-item", s) is not None:
                erreurs.append(f"{ou} · élément répété « {e.attrs['data-item']} » placé dans un autre élément répété (ligne {e.ligne}) : les sortir l'un de l'autre.")
        _controler_emplacements(ou, [n for n in porteurs if n.ancetre("data-item", s) is None], spec["slots"], erreurs)
        for nom in sorted({e.attrs["data-item"] for e in elements}):
            if nom not in spec["groupes"]:
                admis = ", ".join(spec["groupes"]) or "aucun"
                erreurs.append(f"{ou} · élément répété « {nom} » inconnu ici. Éléments admis : {admis}.")
        for nom, groupe in spec["groupes"].items():
            liste = [e for e in elements if e.attrs["data-item"] == nom]
            if not (groupe["min"] <= len(liste) <= groupe["max"]):
                attendu = str(groupe["min"]) if groupe["min"] == groupe["max"] else f"{groupe['min']} à {groupe['max']}"
                erreurs.append(f"{ou} · {len(liste)} éléments « {nom} », il en faut {attendu}.")
            valeurs = []
            for j, e in enumerate(liste, 1):
                if e.attrs.get("data-ton") and e.attrs["data-ton"] not in TONS:
                    erreurs.append(f"{ou} · {nom} {j} · data-ton=\"{e.attrs['data-ton']}\" inconnu. Tons admis : {', '.join(TONS)}.")
                if groupe["icone"] and e.attrs.get("data-icone", "") not in ICONES:
                    ref = e.attrs.get("data-icone", "")
                    quoi = f"icône « {ref} » inconnue" if ref else "attribut data-icone manquant"
                    erreurs.append(f"{ou} · {nom} {j} · {quoi} (ligne {e.ligne}). Icônes admises : {', '.join(ICONES)}.")
                if groupe["valeur"]:
                    brut = e.attrs.get("data-valeur", "")
                    if _nombre(brut) is None:
                        quoi = f"data-valeur=\"{brut}\" n'est pas un nombre positif" if brut else "attribut data-valeur manquant"
                        erreurs.append(f"{ou} · {nom} {j} · {quoi} (ligne {e.ligne}). Y écrire le nombre tracé, en chiffres seulement : data-valeur=\"72\" ou \"12,5\".")
                    else:
                        valeurs.append(_nombre(brut))
                internes = [n for n in e.descendants() if "data-slot" in n.attrs]
                _controler_emplacements(f"{ou} · {nom} {j}", internes, groupe["slots"], erreurs)
            if groupe["valeur"] and valeurs and max(valeurs) <= 0:
                erreurs.append(f"{ou} · toutes les valeurs « {nom} » sont nulles : rien à tracer.")
        retenus = [e for e in elements if "data-retenir" in e.attrs]
        if len(retenus) > 1:
            erreurs.append(f"{ou} · {len(retenus)} éléments portent data-retenir, un seul est admis par slide : garder celui qui porte le message.")
        alignement = spec.get("alignement")
        if alignement:
            colonnes = len([n for n in porteurs if n.attrs["data-slot"] == alignement["sur"] and n.ancetre("data-item", s) is None])
            vide_admis = spec["groupes"][alignement["groupe"]]["slots"][alignement["slot"]]["vide"]
            conseil = f" Une « {alignement['slot']} » peut rester vide : <p data-slot=\"{alignement['slot']}\"></p>." if vide_admis else ""
            for j, e in enumerate([e for e in elements if e.attrs["data-item"] == alignement["groupe"]], 1):
                internes = [n for n in e.descendants() if n.attrs.get("data-slot") == alignement["slot"]]
                if len(internes) != colonnes:
                    erreurs.append(f"{ou} · {alignement['groupe']} {j} : {len(internes)} « {alignement['slot']} » pour {colonnes} « {alignement['sur']} », "
                                   f"il en faut autant.{conseil}")
                elif vide_admis and not any(n.texte() for n in internes):
                    avertissements.append(f"{ou} · {alignement['groupe']} {j} : toutes ses « {alignement['slot']} » sont vides.")
        vers = spec.get("vers")
        if vers:
            liste = [e for e in elements if e.attrs["data-item"] == vers["groupe"]]
            if liste and any(n.attrs.get("data-slot") == vers["slot"] for n in liste[-1].descendants()):
                erreurs.append(f"{ou} · le dernier « {vers['groupe']} » porte « {vers['slot']} », qui ne s'affichera pas : il n'a pas de suivant. Retirer cette balise.")
        if "source" in spec["slots"] and not any(n.attrs["data-slot"] == "source" for n in porteurs):
            avertissements.append(f"{ou} · graphique sans source : ajouter <p data-slot=\"source\">Source : …</p>, ou le signaler.")

        notes = [n for n in dedans if "data-note" in n.attrs]
        if len(notes) > COMMUN["notes_max"]:
            avertissements.append(f"{ou} · {len(notes)} notes, maximum conseillé {COMMUN['notes_max']}.")
        for n in notes:
            if len(n.texte()) > COMMUN["note_car"]:
                avertissements.append(f"{ou} · une note fait {len(n.texte())} caractères, maximum conseillé {COMMUN['note_car']}.")
        if "[à fournir" in s.texte().lower():
            a_fournir.append(str(i))
        if any(n.texte() in _textes_exemples() for n in porteurs):
            restes.append(str(i))

    if slides:
        if slides[0].attrs.get("data-composition") != "couverture":
            avertissements.append("La première slide n'est pas une couverture.")
        if slides[-1].attrs.get("data-composition") != "conclusion":
            avertissements.append("La dernière slide n'est pas une conclusion : vérifier que la demande finale a sa slide.")
    utilises = {s.attrs.get("data-temps") for s in slides}
    orphelins = [t for k, t in enumerate(temps, 1) if str(k) not in utilises]
    if orphelins and len(orphelins) < len(temps):
        avertissements.append("Temps de deck-fil sans aucune slide : " + ", ".join(orphelins) + ". Lui donner une slide ou le retirer du fil.")
    if restes:
        avertissements.append("Texte d'exemple de la charte resté en place dans la slide " + ", ".join(restes) + " : le remplacer par le contenu du deck.")
    if a_fournir:
        avertissements.append("Emplacement « [à fournir … ] » dans la slide " + ", ".join(a_fournir) + " : à lister dans le compte rendu.")
    return erreurs, avertissements, len(slides)


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) == 2 else 2
    chemin = argv[1]
    try:
        with open(chemin, encoding="utf-8") as f:
            html = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"Fichier illisible : {chemin} ({e})", file=sys.stderr)
        return 2
    erreurs, avertissements, nb = controler(html)
    print(f"{chemin} : {nb} slides")
    for e in erreurs:
        print(f"ERREUR · {e}")
    for a in avertissements:
        print(f"AVERTISSEMENT · {a}")
    print(f"Résultat : {len(erreurs)} erreur(s), {len(avertissements)} avertissement(s).")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

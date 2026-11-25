#!/usr/bin/env python3
"""Génère, depuis compositions.py, les decks de démonstration et de vérification du gabarit.

Script de maintenance : pour faire un deck, c'est reference.py qui affiche les compositions.

Usage :
  python3 generer_reference.py --catalogue DOSSIER  crée un deck qui montre chaque composition
  python3 generer_reference.py --limites DOSSIER [--facteur 1.1]
                                                    crée un deck où chaque emplacement est rempli
                                                    à sa limite (ou au-delà), pour vérifier à l'écran
                                                    que rien ne déborde après un changement de style
  python3 generer_reference.py --minimum DOSSIER    crée un deck où chaque composition a le moins
                                                    d'éléments admis et aucun emplacement facultatif,
                                                    pour vérifier à l'écran qu'aucune slide n'est vide
Code de sortie : 0 fait · 2 usage incorrect.
"""
import html
import os
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from compositions import CATALOGUE, COMMUN, COMPOSITIONS, ORDRE  # noqa: E402
from controle_deck import VIDES, Noeud, analyser  # noqa: E402

SKILL = os.path.dirname(ICI)
GABARIT = os.path.join(SKILL, "assets", "gabarit")
FIN = "<!-- FIN DES SLIDES"
PHRASE = ("Les équipes livrent plus vite quand le cadre reste clair pour chacun, que les relais passent par des "
          "fichiers et que chaque rôle sait ce qu’il doit rendre, à qui et sous quelle forme, sans rien réécrire")


def ecrire_deck(dossier, slides, titre, pied, fil):
    """Copie le gabarit dans `dossier` et y pose les slides et les réglages de l'en-tête."""
    shutil.copytree(GABARIT, dossier, dirs_exist_ok=True)
    chemin = os.path.join(dossier, "deck.html")
    with open(os.path.join(GABARIT, "deck.html"), encoding="utf-8") as f:
        page = f.read()
    for ancien, nouveau in (
        ("{{TITRE DU DECK}}", html.escape(titre)),
        ("{{SUJET}} · {{PRÉCISION}}", html.escape(pied)),
        ("{{TEMPS 1}} | {{TEMPS 2}} | {{TEMPS 3}}", html.escape(fil)),
    ):
        if ancien not in page:
            raise SystemExit(f"Gabarit modifié : « {ancien} » introuvable dans assets/gabarit/deck.html")
        page = page.replace(ancien, nouveau)
    i = page.index(FIN)
    page = page[:i] + "\n\n".join(slides) + "\n\n" + page[i:]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(page)
    return chemin


def serialiser(n):
    if isinstance(n, str):
        return html.escape(n, quote=False)
    attrs = "".join(f' {k}="{html.escape(v, quote=True)}"' if v != "" else f" {k}" for k, v in n.attrs.items())
    if n.tag in VIDES:
        return f"<{n.tag}{attrs}>"
    return f"<{n.tag}{attrs}>" + "".join(serialiser(e) for e in n.enfants) + f"</{n.tag}>"


def cloner(n, parent):
    if isinstance(n, str):
        return n
    c = Noeud(n.tag, list(n.attrs.items()), parent, n.ligne)
    c.enfants = [cloner(e, c) for e in n.enfants]
    return c


def remplissage(longueur, nom):
    if nom == "numero":
        return "88"[:longueur]
    if nom == "valeur":
        return "88 888 %  "[:longueur].strip().ljust(min(longueur, 8), "8")
    t = PHRASE
    while len(t) < longueur:
        t += " " + PHRASE
    t = t[:longueur]
    return t[:-1] + "s" if t.endswith(" ") else t


def _repeter(noeuds, combien):
    """Duplique le dernier nœud d'une fratrie jusqu'à en avoir `combien`."""
    noeuds = list(noeuds)
    while noeuds and len(noeuds) < combien:
        modele = noeuds[-1]
        copie = cloner(modele, modele.parent)
        copie.attrs.pop("data-retenir", None)  # un seul élément à retenir par slide
        freres = modele.parent.enfants
        freres.insert(freres.index(modele) + 1, copie)
        noeuds.append(copie)
    return noeuds


def slide_limite(nom, facteur):
    """L'exemple d'une composition, avec le nombre maximal d'éléments et des textes à la limite."""
    spec = COMPOSITIONS[nom]
    racine, _ = analyser(spec["exemple"])
    s = next(n for n in racine.descendants() if n.tag == "section")
    s.enfants = [e for e in s.enfants if isinstance(e, str) or "data-note" not in e.attrs]
    if "data-rubrique" in s.attrs:
        s.attrs["data-rubrique"] = remplissage(COMMUN["rubrique"], "rubrique")

    titre = next((n for n in s.enfants if isinstance(n, Noeud) and n.attrs.get("data-slot") == "titre"), None)
    if titre is not None and "chapo" in spec["slots"] and not any(n.attrs.get("data-slot") == "chapo" for n in s.descendants()):
        chapo = Noeud("p", [("data-slot", "chapo")], s)
        s.enfants.insert(s.enfants.index(titre) + 1, chapo)

    def porteurs(dans, nom_slot):
        return [n for n in dans.descendants() if n.attrs.get("data-slot") == nom_slot]

    vers = spec.get("vers", {})
    for g, groupe in spec["groupes"].items():
        elements = _repeter([n for n in s.descendants() if n.attrs.get("data-item") == g], groupe["max"])
        for e in elements:
            for nom_slot, regle in groupe["slots"].items():
                dernier_sans_suite = g == vers.get("groupe") and nom_slot == vers.get("slot") and e is elements[-1]
                if not porteurs(e, nom_slot) and not dernier_sans_suite:  # le pire cas : chaque emplacement facultatif est présent
                    e.enfants.append(Noeud("p", [("data-slot", nom_slot)], e))
                for p in _repeter(porteurs(e, nom_slot), regle["occ_max"]):
                    p.enfants = [remplissage(round(regle["max"] * facteur), nom_slot)]
    for nom_slot, regle in spec["slots"].items():
        hors = [p for p in porteurs(s, nom_slot) if p.ancetre("data-item", s) is None]
        for p in _repeter(hors, regle["occ_max"]):
            p.enfants = [remplissage(round(regle["max"] * facteur), nom_slot)]
    return serialiser(s)


def slide_minimum(nom):
    """L'exemple d'une composition, réduit au moins d'éléments admis, sans emplacement facultatif ni note."""
    spec = COMPOSITIONS[nom]
    racine, _ = analyser(spec["exemple"])
    s = next(n for n in racine.descendants() if n.tag == "section")

    def retirer(n):
        n.parent.enfants.remove(n)

    for n in [n for n in s.descendants() if "data-note" in n.attrs]:
        retirer(n)
    for g, groupe in spec["groupes"].items():
        elements = [n for n in s.descendants() if n.attrs.get("data-item") == g]
        for e in elements[groupe["min"]:]:
            retirer(e)
        for e in elements[:groupe["min"]]:
            for slot, regle in groupe["slots"].items():
                for p in [n for n in e.descendants() if n.attrs.get("data-slot") == slot][regle["occ_min"]:]:
                    retirer(p)
    for slot, regle in spec["slots"].items():
        hors = [n for n in s.descendants() if n.attrs.get("data-slot") == slot and n.ancetre("data-item", s) is None]
        for p in hors[regle["occ_min"]:]:
            retirer(p)
    alignement = spec.get("alignement")
    if alignement:  # autant de cellules par rangée que d'en-têtes restants
        colonnes = len([n for n in s.descendants() if n.attrs.get("data-slot") == alignement["sur"]])
        for e in [n for n in s.descendants() if n.attrs.get("data-item") == alignement["groupe"]]:
            for p in [n for n in e.descendants() if n.attrs.get("data-slot") == alignement["slot"]][colonnes:]:
                retirer(p)
    vers = spec.get("vers")
    if vers:  # le dernier élément n'a pas de lien vers un suivant
        dernier = [n for n in s.descendants() if n.attrs.get("data-item") == vers["groupe"]][-1]
        for p in [n for n in dernier.descendants() if n.attrs.get("data-slot") == vers["slot"]]:
            retirer(p)
    return serialiser(s)


def main(argv):
    args = argv[1:]
    if args[0] == "--catalogue" and len(args) == 2:
        slides = [COMPOSITIONS[n]["exemple"] for n in ORDRE]
        print("Écrit : " + ecrire_deck(args[1], slides, CATALOGUE["titre"], CATALOGUE["pied"], CATALOGUE["fil"]))
        return 0
    if args[0] == "--minimum" and len(args) == 2:
        slides = [slide_minimum(n) for n in ORDRE]
        print("Écrit : " + ecrire_deck(args[1], slides, "Deck au minimum", CATALOGUE["pied"], CATALOGUE["fil"]))
        return 0
    if args[0] == "--limites" and len(args) in (2, 4):
        facteur = 1.0
        if len(args) == 4:
            if args[2] != "--facteur":
                print(__doc__.strip())
                return 2
            facteur = float(args[3])
        slides = [slide_limite(n, facteur) for n in ORDRE]
        fil = " | ".join(remplissage(COMMUN["temps_car"], "temps") for _ in range(COMMUN["temps_max"]))
        print("Écrit : " + ecrire_deck(args[1], slides, "Deck aux limites", remplissage(COMMUN["pied"], "pied"), fil))
        return 0
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))

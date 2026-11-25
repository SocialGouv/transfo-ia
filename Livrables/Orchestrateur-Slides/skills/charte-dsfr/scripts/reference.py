#!/usr/bin/env python3
"""Affiche la référence d'écriture d'un deck : les règles, puis les seules compositions demandées.

Pour chaque composition : la longueur maximale de chaque emplacement et un exemple à recopier.
N'afficher que les compositions du deck garde la lecture courte.

Usage :
  python3 reference.py chemin/carte.md      les compositions qu'appellent les lignes « Nature » de la carte
  python3 reference.py nom [nom ...]        les compositions nommées (par exemple : chiffres frise)
  python3 reference.py --liste              le nom et l'usage de chaque composition
Code de sortie : 0 référence affichée · 2 composition ou nature inconnue, fichier illisible, usage incorrect.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compositions import BALISES_DE_TEXTE, COMMUN, COMPOSITIONS, ICONES, ORDRE, SENS_ICONES  # noqa: E402

NATURES = {c["nature"]: nom for nom, c in COMPOSITIONS.items()}


def _limite(slot, r):
    texte = f"`{slot}` {r['max']}"
    if r["occ_max"] > 1:
        texte += f" ({r['occ_min']} à {r['occ_max']} fois)"
    elif not r["requis"]:
        texte += " (facultatif)"
    return texte + (", peut rester vide" if r["vide"] else "")


def limites(c):
    """La ligne « Limites » d'une composition : chaque emplacement et sa longueur maximale."""
    morceaux = [_limite(slot, r) for slot, r in c["slots"].items()]
    for g, groupe in c["groupes"].items():
        combien = str(groupe["min"]) if groupe["min"] == groupe["max"] else f"{groupe['min']} à {groupe['max']}"
        attributs = [a for a, cle in (("`data-icone`", "icone"), ("`data-valeur`", "valeur")) if groupe[cle]]
        avec = ", chacun avec " + " et ".join(attributs) if attributs else ""
        morceaux.append(f"{combien} éléments `{g}`{avec} : " + ", ".join(_limite(slot, r) for slot, r in groupe["slots"].items()))
    return "Limites : " + " · ".join(morceaux) + "." + (" " + c["regle"] if c.get("regle") else "")


def exemple_court(c):
    """L'exemple d'une composition, réduit à deux éléments répétés par groupe (ou au minimum admis s'il est plus grand).

    Un troisième élément n'apprend rien de plus sur la structure : le catalogue garde l'exemple entier.
    """
    lignes = c["exemple"].split("\n")
    if c.get("entier"):
        return c["exemple"]
    for g, groupe in c["groupes"].items():
        garder = max(groupe["min"], 2)
        debut = f'<div data-item="{g}"'
        rangs = [i for i, ligne in enumerate(lignes) if ligne.startswith(debut)]
        if len(rangs) <= garder or not all(lignes[i].endswith("</div>") for i in rangs):
            continue  # rien à retirer, ou éléments écrits sur plusieurs lignes
        for i in reversed(rangs[garder:]):
            del lignes[i]
    return "\n".join(lignes)


def tableau_de_choix():
    """Le tableau « Choisir la composition », recopié dans SKILL.md (un test vérifie qu'il y est à jour)."""
    lignes = ["| La slide montre | Composition | Quand |", "|---|---|---|"]
    lignes += [f"| {COMPOSITIONS[nom]['nature']} | `{nom}` | {COMPOSITIONS[nom]['quand']} |" for nom in ORDRE]
    return "\n".join(lignes)


def _groupes(noms, cle):
    """Les éléments répétés des compositions demandées qui admettent un attribut (icone, valeur, retenir)."""
    return [g for nom in noms for g, groupe in COMPOSITIONS[nom]["groupes"].items() if groupe[cle]]


def regles(noms):
    """Les règles d'écriture, réduites à ce que les compositions demandées emploient."""
    L = ["## Écrire une slide", ""]
    a = L.append
    a("Une slide est une balise `<section data-composition=\"…\">`. Elle contient des emplacements (`data-slot`) et, selon la "
      "composition, des éléments répétés (`data-item`). Recopie l'exemple de la composition, remplace ses textes, garde ses attributs. "
      "N'écris ni classe ni style : le gabarit construit la mise en page à partir de ces attributs, et n'affiche rien d'autre.")
    a("")
    a("- **Limites** : le nombre qui suit un emplacement est sa longueur maximale, en caractères affichés, espaces compris. "
      "Un emplacement facultatif se retire avec sa balise.")
    a("- **Éléments répétés** : l'exemple en montre peu. Pour en ajouter un, copie le bloc entier qui porte `data-item`, dans les bornes indiquées.")
    a(f"- **Attributs de la slide** : `data-rubrique`, le mot affiché en haut ({COMMUN['rubrique']} caractères au plus, d'ordinaire le nom "
      "du temps) ; `data-temps`, le numéro du temps de l'histoire où se trouve la slide (1 pour le premier temps de `deck-fil`). "
      "La couverture et la conclusion n'en portent aucun.")
    a("- **Ton** : `data-ton=\"risque\"` (orange) ou `data-ton=\"acquis\"` (vert), sur la slide pour colorer sa rubrique, ou sur un "
      "`chiffre`, un `jalon`, une `barre`. Sans ton, bleu France. Un ton garde le même sens sur tout le deck.")
    retenir = _groupes(noms, "retenir")
    if retenir:
        a("- **À retenir** : `data-retenir`, sur un seul élément répété de la slide (" + ", ".join(f"`{g}`" for g in retenir) +
          "), le met en bleu France ; les autres passent en retrait.")
    if _groupes(noms, "valeur"):
        a("- **Graphiques** : `data-valeur` porte le nombre tracé, en chiffres seulement (`72`, `12,5`) ; l'emplacement de valeur porte "
          "le texte affiché, avec son unité. L'axe part de zéro et le gabarit trace le dessin.")
    a("- **Dans un emplacement** : du texte, avec au besoin les balises " + ", ".join(f"`{b}`" for b in BALISES_DE_TEXTE) +
      ", sans attribut. `<em>` marque le mot à retenir, en bleu France : un seul par slide.")
    a(f"- **Notes d'orateur** : `<p data-note>…</p>` en fin de slide, {COMMUN['notes_max']} au plus. Elles ne s'affichent pas à l'écran.")
    if _groupes(noms, "icone"):
        a("- **Icônes** : attribut `data-icone` des éléments répétés qui en portent un dans l'exemple. La même icône garde le même sens "
          "sur tout le deck. Icônes admises, avec leur sens :")
        a("")
        a(" · ".join(f"`{i}` {SENS_ICONES[i]}" for i in ICONES))
    return L


def section(nom):
    """Les lignes d'une composition : son nom, ses limites, son exemple."""
    c = COMPOSITIONS[nom]
    return [f"### `{nom}`" + ("" if c["nature"] == nom else f" ({c['nature']})"), "", limites(c), "", "```html", exemple_court(c), "```"]


def texte(noms, slides=None):
    """La référence des compositions `noms`. `slides` : la composition de chaque slide d'une carte, dans l'ordre."""
    L = ["# Référence d'écriture du deck", ""]
    if slides:
        L += ["Composition de chaque slide de la carte : " + " · ".join(f"{i} `{nom}`" for i, nom in enumerate(slides, 1)) + ".", ""]
    L += regles(noms) + ["", "## Les compositions"]
    for nom in noms:
        L += [""] + section(nom)
    return "\n".join(L) + "\n"


def natures_de_la_carte(contenu):
    """Renvoie (composition de chaque slide, natures inconnues) d'après les lignes « Nature » d'une carte."""
    slides, inconnues = [], []
    for m in re.finditer(r"^\s*-?\s*Nature\s*:\s*(.+?)\s*$", contenu, flags=re.M):
        nature = m.group(1)
        if nature in NATURES:
            slides.append(NATURES[nature])
        else:
            inconnues.append(nature)
    return slides, inconnues


def liste():
    return "\n".join(f"{nom} ({COMPOSITIONS[nom]['nature']}) : {COMPOSITIONS[nom]['quand']}" for nom in ORDRE) + "\n"


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args else 2
    if args == ["--liste"]:
        sys.stdout.write(liste())
        return 0
    slides = None
    if len(args) == 1 and args[0] not in COMPOSITIONS:
        try:
            with open(args[0], encoding="utf-8") as f:
                contenu = f.read()
        except (OSError, UnicodeDecodeError):
            print(f"« {args[0]} » n'est ni une composition ni un fichier lisible. Compositions : {', '.join(ORDRE)}.", file=sys.stderr)
            return 2
        slides, inconnues = natures_de_la_carte(contenu)
        if inconnues:
            print("Nature inconnue dans la carte : " + ", ".join(sorted(set(inconnues))) + ". Natures admises : " + " · ".join(NATURES) + ".", file=sys.stderr)
            return 2
        if not slides:
            print(f"Aucune ligne « Nature : … » dans {args[0]}. Nommer les compositions : python3 reference.py chiffres frise", file=sys.stderr)
            return 2
        noms = [nom for nom in ORDRE if nom in slides]
    else:
        inconnus = [a for a in args if a not in COMPOSITIONS]
        if inconnus:
            print("Composition inconnue : " + ", ".join(inconnus) + ". Compositions : " + ", ".join(ORDRE) + ".", file=sys.stderr)
            return 2
        noms = [nom for nom in ORDRE if nom in args]
    sys.stdout.write(texte(noms, slides))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

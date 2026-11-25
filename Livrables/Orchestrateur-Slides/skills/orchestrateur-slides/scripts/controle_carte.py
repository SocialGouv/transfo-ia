#!/usr/bin/env python3
"""Contrôle la carte des messages d'un deck (carte.md), avant sa mise en forme.

Vérifie ce qui se compte : l'en-tête est rempli, les slides sont numérotées à la suite, chaque
nature est dans la liste admise, chaque titre tient sous la longueur que le gabarit affiche,
chaque temps de l'histoire a une slide, le deck n'emploie pas trop de natures différentes.
Le sens de l'histoire reste à juger par un lecteur.

Usage : python3 controle_carte.py chemin/carte.md [--charte DOSSIER_DU_SKILL_DE_CHARTE]
Avec --charte, les natures et les longueurs sont lues dans scripts/compositions.py du skill de
charte ; sans lui, celles de la charte de l'État s'appliquent.
Sortie : une ligne par problème, puis un résultat.
Code de sortie : 0 aucune erreur · 1 au moins une erreur · 2 fichier illisible ou usage incorrect.
"""
import importlib.util
import os
import re
import sys

# Valeurs de la charte de l'État, employées sans --charte. Un test vérifie qu'elles lui restent égales.
TITRES = {
    "couverture": 32, "énoncé seul": 75, "section": 60, "chiffre": 90, "idées de même rang": 90,
    "comparaison": 90, "étapes": 90, "liste": 90, "tableau": 90, "citation": 90, "conclusion": 42,
    "frise datée": 90, "graphique en barres": 90, "courbe": 90, "schéma de flux": 90, "schéma à couloirs": 90,
}
TEMPS = {"min": 2, "max": 4, "car": 12}
NATURES_MAX = 10   # natures différentes dans un deck : unité visuelle, et lecture bornée du travailleur
HORS_TEMPS = ("couverture", "conclusion")
EN_TETE = ["Fil rouge", "Auditoire et demande finale", "Canal", "Temps de l'histoire", "En bref"]
LIGNES_PAR_SLIDE = 12
CHEVRONS = re.compile(r"<[A-Za-zÀ-ÿ][^<>\n]{2,}>")   # « <titre du deck> », mais pas « < 5 € et > 3 jours »


def lire_charte(dossier):
    """Renvoie (longueur du titre par nature, réglages des temps, nombre de natures admis) lus dans un skill de charte."""
    chemin = os.path.join(dossier, "scripts", "compositions.py")
    spec = importlib.util.spec_from_file_location("compositions_charte", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    titres = {c["nature"]: c["slots"]["titre"]["max"] for c in module.COMPOSITIONS.values()}
    c = module.COMMUN
    return titres, {"min": c["temps_min"], "max": c["temps_max"], "car": c["temps_car"]}, c.get("compositions_max", NATURES_MAX)


def valeur(ligne):
    """La valeur d'une ligne « - Nom : valeur »."""
    return ligne.split(":", 1)[1].strip() if ":" in ligne else ""


def controler(texte, titres=None, temps_regles=None, natures_max=None):
    """Renvoie (erreurs, avertissements, nombre de slides)."""
    titres = titres or TITRES
    regles = temps_regles or TEMPS
    natures_max = natures_max or NATURES_MAX
    erreurs, avertissements = [], []
    lignes = texte.splitlines()

    if not any(l.startswith("# Carte des messages") for l in lignes):
        erreurs.append("En-tête · la première ligne doit être « # Carte des messages : <titre du deck> ».")
    debut_slides = next((i for i, l in enumerate(lignes) if l.startswith("## ")), len(lignes))
    champs = {}
    for l in lignes[:debut_slides]:
        m = re.match(r"-\s*([^:]+?)\s*:\s*(.*)$", l)
        if m:
            champs[m.group(1)] = m.group(2).strip()
    for nom in EN_TETE:
        if not champs.get(nom):
            erreurs.append(f"En-tête · ligne « - {nom} : … » manquante ou vide.")
    temps = [t.strip() for t in champs.get("Temps de l'histoire", "").split("|") if t.strip()]
    if temps and not (regles["min"] <= len(temps) <= regles["max"]):
        erreurs.append(f"En-tête · {len(temps)} temps, il en faut {regles['min']} à {regles['max']}.")
    for t in temps:
        if len(t) > regles["car"]:
            erreurs.append(f"En-tête · le temps « {t} » fait {len(t)} caractères, maximum {regles['car']} : il s'affiche en haut de chaque slide.")

    slides = []
    for i in range(debut_slides, len(lignes)):
        if lignes[i].startswith("## "):
            slides.append({"ligne": i + 1, "entete": lignes[i][3:].strip(), "corps": []})
        elif slides:
            slides[-1]["corps"].append(lignes[i])
    if not slides:
        erreurs.append("Aucune slide : chaque slide commence par « ## <numéro>. <titre> ».")

    utilises, a_fournir, employees = set(), [], set()
    for rang, s in enumerate(slides, 1):
        m = re.match(r"(\d+)\.\s+(.*)$", s["entete"])
        ou = f"slide {rang}"
        if not m:
            erreurs.append(f"{ou} · ligne {s['ligne']} : écrire « ## {rang}. <titre> ».")
            titre = s["entete"]
        else:
            titre = m.group(2).strip()
            if int(m.group(1)) != rang:
                erreurs.append(f"{ou} · numérotée {m.group(1)} : les slides se numérotent à la suite, à partir de 1.")
        attributs = {}
        for k, l in enumerate(s["corps"]):
            a = re.match(r"-\s*([^:]+?)\s*:\s*(.*)$", l)
            if a:
                valeur_ligne = a.group(2).strip()
                if not valeur_ligne:  # la valeur peut suivre en liste, un élément par ligne en retrait
                    suite = [x.strip() for x in s["corps"][k + 1:k + 2] if re.match(r"\s+\S", x)]
                    valeur_ligne = suite[0] if suite else ""
                attributs.setdefault(a.group(1), valeur_ligne)
        nature = attributs.get("Nature", "")
        if nature not in titres:
            erreurs.append(f"{ou} · nature « {nature} » inconnue ou absente. Natures admises : {' · '.join(titres)}.")
        else:
            employees.add(nature)
        if nature in titres and len(titre) > titres[nature]:
            erreurs.append(f"{ou} ({nature}) · titre de {len(titre)} caractères, maximum {titres[nature]}. Raccourcir de {len(titre) - titres[nature]} caractères.")
        if not titre:
            erreurs.append(f"{ou} · titre vide.")
        if nature in titres and nature not in HORS_TEMPS and temps:
            t = attributs.get("Temps", "")
            if not t.isdigit() or not 1 <= int(t) <= len(temps):
                erreurs.append(f"{ou} · ligne « - Temps : {t} » : attendre un numéro de 1 à {len(temps)}.")
            else:
                utilises.add(int(t))
        if nature in titres and not attributs.get("À l'écran"):
            erreurs.append(f"{ou} · ligne « - À l'écran : … » manquante ou vide.")
        pleines = [l for l in s["corps"] if l.strip()]
        if len(pleines) + 1 > LIGNES_PAR_SLIDE:
            avertissements.append(f"{ou} · {len(pleines) + 1} lignes, maximum conseillé {LIGNES_PAR_SLIDE} : la slide porte peut-être deux messages.")
        if "[à fournir" in (s["entete"] + "\n" + "\n".join(s["corps"])).lower():
            a_fournir.append(str(rang))

    restes = sorted({str(i) for i, l in enumerate(lignes, 1) if CHEVRONS.search(l)})
    if restes:
        erreurs.append("Texte entre chevrons resté en place, ligne " + ", ".join(restes[:8]) + " : le remplacer par le contenu.")
    if len(employees) > natures_max:
        erreurs.append(f"{len(employees)} natures différentes dans le deck, maximum {natures_max} : donner la même nature à des slides de même rôle.")
    orphelins = [t for k, t in enumerate(temps, 1) if k not in utilises]
    if slides and orphelins:
        erreurs.append("Temps sans aucune slide : " + ", ".join(orphelins) + ". Lui donner une slide ou le retirer.")
    if slides:
        natures = [re.search(r"^-\s*Nature\s*:\s*(.*)$", "\n".join(s["corps"]), flags=re.M) for s in slides]
        premiere, derniere = (n.group(1).strip() if n else "" for n in (natures[0], natures[-1]))
        if premiere != "couverture":
            avertissements.append("La première slide n'est pas une couverture.")
        if derniere != "conclusion":
            avertissements.append("La dernière slide n'est pas une conclusion : vérifier que la demande finale a sa slide.")
    if a_fournir:
        avertissements.append("Emplacement « [à fournir … ] » dans la slide " + ", ".join(a_fournir) + " : à lister dans le compte rendu.")
    return erreurs, avertissements, len(slides)


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help") or len(args) not in (1, 3) or (len(args) == 3 and args[1] != "--charte"):
        print(__doc__.strip())
        return 0 if args and args[0] in ("-h", "--help") else 2
    try:
        with open(args[0], encoding="utf-8") as f:
            texte = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"Fichier illisible : {args[0]} ({e})", file=sys.stderr)
        return 2
    titres = temps = natures_max = None
    if len(args) == 3:
        try:
            titres, temps, natures_max = lire_charte(args[2])
        except Exception as e:  # le skill de charte est fourni par un tiers : tout défaut de lecture se dit ici
            print(f"Skill de charte illisible : {args[2]} ({e}). Relancer sans --charte, ou corriger le chemin.", file=sys.stderr)
            return 2
    erreurs, avertissements, nb = controler(texte, titres, temps, natures_max)
    print(f"{args[0]} : {nb} slides")
    for e in erreurs:
        print(f"ERREUR · {e}")
    for a in avertissements:
        print(f"AVERTISSEMENT · {a}")
    print(f"Résultat : {len(erreurs)} erreur(s), {len(avertissements)} avertissement(s).")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

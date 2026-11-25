#!/usr/bin/env python3
"""Mesure ce que chaque agent de la chaîne lit, et vérifie le plafond de lignes de skills.

Pour chaque agent : les fichiers de skills qu'il lit (son rôle, le SKILL.md de son skill, le
gabarit), mesurés en lignes et en caractères ; puis ses fichiers de travail pour un deck de
12 slides (brief, carte, deck, revue), estimés. Les tokens sont estimés à 3,3 caractères par
token : un ordre de grandeur, pas une mesure.

Le travailleur ne lit pas toutes les compositions : le script reference.py de la charte lui
affiche celles de son deck. On compte ici le pire cas : un deck qui emploie le nombre maximal
de compositions différentes (dix), prises parmi les plus longues.

Le plafond porte sur les fichiers de skills : 350 lignes par agent. Pour qu'une ligne très
longue ne le contourne pas, un second plafond suit en caractères : 100 par ligne admise.

Usage : python3 budget_contexte.py [--plafond 350] [--contexte 256000]
Code de sortie : 0 chaque agent tient sous le plafond · 1 un agent le dépasse, ou un fichier
attendu manque · 2 usage incorrect.
"""
import os
import sys

RACINE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")
sys.path.insert(0, os.path.join(RACINE, "charte-dsfr", "scripts"))
REFERENCE = "charte-dsfr : référence affichée par scripts/reference.py, pire cas"
CAR_PAR_TOKEN = 3.3
CAR_PAR_LIGNE = 100

# Fichiers de travail d'un deck de 12 slides : (lignes, caractères), estimés d'après les exemples du dossier.
TRAVAIL = {
    "brief.md": (40, 2500),
    "carte.md (12 slides)": (100, 8000),
    "deck/deck.html (12 slides)": (140, 10700),
    "revue": (40, 2500),
    "comptes rendus des sous-agents (6 × 10 lignes)": (60, 4000),
}

ROLE = "orchestrateur-slides/references/role-"
AGENTS = {
    "Orchestrateur": {
        "skills": ["orchestrateur-slides/SKILL.md"],
        "travail": ["brief.md", "carte.md (12 slides)", "comptes rendus des sous-agents (6 × 10 lignes)"],
    },
    "Planificateur": {
        "skills": [ROLE + "planificateur.md", "histoire-slides/SKILL.md"],
        "travail": ["brief.md", "carte.md (12 slides)"],
    },
    "Vérificateur, sur le fond": {
        "skills": [ROLE + "verificateur.md", "histoire-slides/SKILL.md"],
        "travail": ["brief.md", "carte.md (12 slides)", "revue"],
    },
    "Travailleur": {
        "skills": [ROLE + "travailleur.md", "charte-dsfr/SKILL.md", REFERENCE, "charte-dsfr/assets/gabarit/deck.html"],
        "travail": ["brief.md", "carte.md (12 slides)", "deck/deck.html (12 slides)"],
    },
    "Vérificateur, sur la forme": {
        "skills": [ROLE + "verificateur.md", "charte-dsfr/SKILL.md"],
        "travail": ["carte.md (12 slides)", "deck/deck.html (12 slides)", "revue"],
    },
}

# Fichiers qu'aucun agent ne doit lire : leur poids explique pourquoi.
A_NE_PAS_LIRE = ["charte-dsfr/assets/gabarit/charte/slides.css", "charte-dsfr/assets/gabarit/charte/deck.js",
                 "charte-dsfr/assets/gabarit/charte/bloc-marque.css"]


def pire_reference():
    """La plus longue référence qu'un travailleur puisse se faire afficher, et les compositions qu'elle contient."""
    import reference  # noqa: E402  (script de la charte)
    from compositions import COMMUN, COMPOSITIONS  # noqa: E402

    imposees = ["couverture", "conclusion"]
    autres = sorted((n for n in COMPOSITIONS if n not in imposees), key=lambda n: -len("\n".join(reference.section(n)).split("\n")))
    noms = imposees + autres[:COMMUN["compositions_max"] - len(imposees)]
    return reference.texte([n for n in COMPOSITIONS if n in noms]), noms


def mesurer(relatif):
    """(lignes, caractères) d'un fichier du dossier skills/, ou de la référence affichée au travailleur."""
    if relatif == REFERENCE:
        texte = pire_reference()[0]
    else:
        with open(os.path.join(RACINE, relatif), encoding="utf-8") as f:
            texte = f.read()
    return texte.count("\n") + (0 if texte.endswith("\n") or not texte else 1), len(texte)


def nombre(n):
    return f"{n:,}".replace(",", " ")


def budget(agent):
    """Les mesures d'un agent : détail par fichier, total des skills, total avec les fichiers de travail."""
    detail = [(f, *mesurer(f)) for f in AGENTS[agent]["skills"]]
    lignes, car = sum(d[1] for d in detail), sum(d[2] for d in detail)
    travail = [(t, *TRAVAIL[t]) for t in AGENTS[agent]["travail"]]
    return {"detail": detail, "lignes": lignes, "car": car, "travail": travail,
            "lignes_tout": lignes + sum(t[1] for t in travail), "car_tout": car + sum(t[2] for t in travail)}


def options(argv):
    """Renvoie (plafond, contexte), ou None si l'usage est incorrect."""
    valeurs = {"--plafond": 350, "--contexte": 256000}
    args = argv[1:]
    if len(args) % 2:
        return None
    for nom, v in zip(args[0::2], args[1::2]):
        if nom not in valeurs or not v.isdigit() or int(v) == 0:
            return None
        valeurs[nom] = int(v)
    return valeurs["--plafond"], valeurs["--contexte"]


def main(argv):
    lus = options(argv)
    if lus is None:
        print(__doc__.strip())
        return 2
    plafond, contexte = lus
    try:
        mesures = {agent: budget(agent) for agent in AGENTS}
        poids = sum(mesurer(f)[1] for f in A_NE_PAS_LIRE)
        tous = sorted({f for a in AGENTS.values() for f in a["skills"]})
        tout_lire = (sum(mesurer(f)[0] for f in tous), sum(mesurer(f)[1] for f in tous))
        pire = pire_reference()[1]
    except (OSError, ImportError) as e:
        print(f"Fichier attendu introuvable : {e}", file=sys.stderr)
        return 1

    print("| Agent | Fichier de skill lu | Lignes | Caractères |")
    print("|---|---|---:|---:|")
    for agent, m in mesures.items():
        for f, l, c in m["detail"]:
            print(f"| {agent} | {f if f == REFERENCE else '`' + f + '`'} | {nombre(l)} | {nombre(c)} |")
        print(f"| **{agent}** | **total des skills** | **{nombre(m['lignes'])}** | **{nombre(m['car'])}** |")
    print()
    print(f"| Agent | Lignes de skills (plafond {plafond}) | Marge | Avec ses fichiers de travail, estimés | Tokens estimés | Part de {nombre(contexte)} tokens |")
    print("|---|---:|---:|---:|---:|---:|")
    depassements = []
    for agent, m in mesures.items():
        tokens = round(m["car_tout"] / CAR_PAR_TOKEN / 100) * 100
        print(f"| {agent} | {nombre(m['lignes'])} | {nombre(plafond - m['lignes'])} | {nombre(m['lignes_tout'])} lignes | ≈ {nombre(tokens)} | {tokens / contexte * 100:.0f} % |")
        if m["lignes"] > plafond:
            depassements.append(f"{agent} : {m['lignes']} lignes de skills, plafond {plafond}.")
        if m["car"] > plafond * CAR_PAR_LIGNE:
            depassements.append(f"{agent} : {nombre(m['car'])} caractères de skills, plafond {nombre(plafond * CAR_PAR_LIGNE)} "
                                f"({CAR_PAR_LIGNE} par ligne admise).")
    print()
    print(f"Pire cas de la référence du travailleur : un deck qui emploie {len(pire)} compositions, les plus longues ({', '.join(pire)}).")
    print(f"Sans sous-agents, un seul agent tient tous les rôles et lit tous ces fichiers : {nombre(tout_lire[0])} lignes, "
          f"{nombre(tout_lire[1])} caractères. Le plafond ne vaut donc qu'avec des sous-agents.")
    print(f"Dossier charte/ du gabarit, que personne ne lit : {nombre(poids)} caractères, soit ≈ "
          f"{nombre(round(poids / CAR_PAR_TOKEN / 100) * 100)} tokens épargnés à chaque agent.")
    print("La matière source lue par le planificateur s'ajoute ; son rôle la plafonne à 3 000 lignes.")
    for d in depassements:
        print(f"DÉPASSEMENT · {d}")
    print(f"Résultat : {len(depassements)} dépassement(s).")
    return 1 if depassements else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

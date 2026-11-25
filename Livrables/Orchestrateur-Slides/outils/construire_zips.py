#!/usr/bin/env python3
"""Construit un zip des trois skills par outil, à dézipper à la racine d'un projet.

Chaque zip range les skills dans le dossier où l'outil les cherche :
  Claude Code        .claude/skills/
  OpenCode           .opencode/skills/
  Codex              .agents/skills/
  DeepSeek Harness   .dsh/skills/
Le contenu des skills est le même dans les quatre zips ; seul le dossier change.

Usage : python3 construire_zips.py [dossier de sortie]
Sortie par défaut : dist/, à côté de skills/.
Code de sortie : 0 zips écrits · 1 un skill manque ou sa description est trop longue · 2 usage incorrect.
"""
import os
import re
import sys
import zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = ["orchestrateur-slides", "histoire-slides", "charte-dsfr"]
CIBLES = {
    "claude-code": ".claude/skills",
    "opencode": ".opencode/skills",
    "codex": ".agents/skills",
    "deepseek-harness": ".dsh/skills",
}
EXCLUS = ("__pycache__", ".DS_Store")
DESCRIPTION_MAX = 500   # DeepSeek Harness ne montre au modèle que les 500 premiers caractères d'une description
DATE = (2026, 11, 25, 0, 0, 0)   # date fixe : deux constructions du même contenu donnent le même zip


def fichiers(dossier):
    """Les fichiers d'un skill, chemins relatifs au dossier skills/, triés."""
    trouves = []
    for base, sous_dossiers, noms in os.walk(dossier):
        sous_dossiers[:] = sorted(d for d in sous_dossiers if d not in EXCLUS)
        for nom in sorted(noms):
            if nom in EXCLUS or nom.endswith(".pyc"):
                continue
            trouves.append(os.path.join(base, nom))
    return trouves


def version():
    with open(os.path.join(RACINE, "skills", "orchestrateur-slides", "SKILL.md"), encoding="utf-8") as f:
        m = re.search(r'^\s*version:\s*"([^"]+)"', f.read(), flags=re.M)
    return m.group(1) if m else "0"


def description(skill_md):
    """La description du frontmatter d'un SKILL.md (écrite sur une ligne, entre guillemets)."""
    with open(skill_md, encoding="utf-8") as f:
        m = re.search(r'^description:\s*"(.*)"\s*$', f.read(), flags=re.M)
    return m.group(1) if m else ""


def construire(sortie):
    """Écrit les zips et renvoie [(chemin, nombre de fichiers)]."""
    source = os.path.join(RACINE, "skills")
    contenu = []
    for skill in SKILLS:
        skill_md = os.path.join(source, skill, "SKILL.md")
        if not os.path.isfile(skill_md):
            raise FileNotFoundError(skill_md)
        longueur = len(description(skill_md))
        if not 0 < longueur <= DESCRIPTION_MAX:
            raise ValueError(f"{skill} : description de {longueur} caractères, il en faut 1 à {DESCRIPTION_MAX}")
        contenu += fichiers(os.path.join(source, skill))
    os.makedirs(sortie, exist_ok=True)
    ecrits = []
    for cible, dossier in CIBLES.items():
        chemin = os.path.join(sortie, f"orchestrateur-slides-{version()}-{cible}.zip")
        with zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for f in contenu:
                dans_zip = dossier + "/" + os.path.relpath(f, source).replace(os.sep, "/")
                info = zipfile.ZipInfo(dans_zip, DATE)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                with open(f, "rb") as octets:
                    z.writestr(info, octets.read())
        ecrits.append((chemin, len(contenu)))
    return ecrits


def main(argv):
    if len(argv) > 2 or (len(argv) == 2 and argv[1] in ("-h", "--help")):
        print(__doc__.strip())
        return 0 if len(argv) == 2 else 2
    sortie = os.path.abspath(argv[1]) if len(argv) == 2 else os.path.join(RACINE, "dist")
    try:
        ecrits = construire(sortie)
    except FileNotFoundError as e:
        print(f"Skill incomplet, fichier introuvable : {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Skill à corriger avant de construire les zips : {e}", file=sys.stderr)
        return 1
    for chemin, nb in ecrits:
        print(f"Écrit : {chemin} ({nb} fichiers, {os.path.getsize(chemin) // 1024} Ko)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

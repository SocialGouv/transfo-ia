# -*- coding: utf-8 -*-
"""Rasterise les icônes Remix Icon (base du jeu DSFR) manquantes, en bleu France et en blanc.
Méthode du pipeline checkpoints : liste flat du package via l'API jsdelivr, puis CDN + cairosvg."""
import json
import os
import urllib.parse
import urllib.request

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
IC = os.path.join(HERE, "assets", "ic")
PKG = "remixicon@4.5.0"
BLUE = "#000091"

VOULUES = [
    "download-cloud-2-line", "filter-3-line", "sparkling-2-line", "git-merge-line",
    "file-excel-2-line", "mail-send-line", "user-3-line", "scales-3-line",
    "close-circle-line", "file-list-3-line", "alarm-warning-line", "question-line",
    "checkbox-circle-line", "time-line", "edit-line", "cpu-line", "links-line",
]

def liste_fichiers():
    url = f"https://data.jsdelivr.com/v1/packages/npm/{PKG}?structure=flat"
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    return [f["name"] for f in data["files"] if f["name"].endswith(".svg")]

def main():
    chemins = liste_fichiers()
    index = {os.path.basename(p)[:-4]: p for p in chemins if p.startswith("/icons/")}
    for nom in VOULUES:
        base = nom.replace("-line", "")
        if nom not in index:
            print(f"ABSENT du package : {nom}")
            continue
        url = f"https://cdn.jsdelivr.net/npm/{PKG}{urllib.parse.quote(index[nom])}"
        with urllib.request.urlopen(url, timeout=30) as r:
            svg = r.read().decode()
        for suffixe, couleur in (("", BLUE), ("_w", "#FFFFFF")):
            teinte = svg.replace("currentColor", couleur)
            cible = os.path.join(IC, f"{base}{suffixe}.png")
            cairosvg.svg2png(bytestring=teinte.encode(), write_to=cible,
                             output_width=256, output_height=256)
        print(f"OK {base}")

if __name__ == "__main__":
    main()

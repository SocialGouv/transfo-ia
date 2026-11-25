#!/usr/bin/env python3
"""Assemble un deck en un seul fichier HTML autonome, à envoyer ou à publier.

Styles, polices et script du dossier charte/ sont intégrés au fichier. Le deck est d'abord
contrôlé : s'il contient une erreur, rien n'est écrit (sauf avec --force).
Le fichier produit est lourd (plus de 300 000 caractères) : il sert à diffuser le deck,
on ne le relit pas et on ne le modifie pas. Les corrections se font dans deck.html.

Usage : python3 assembler.py chemin/deck.html [sortie.html] [--force]
Sortie par défaut : à côté du dossier du deck, <nom du dossier>-autonome.html.
Code de sortie : 0 fichier écrit · 1 deck en erreur ou fichier de charte manquant · 2 usage incorrect.
"""
import base64
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from controle_deck import controler  # noqa: E402


def assembler(html, dossier):
    """Renvoie le HTML avec les fichiers de charte/ intégrés."""

    def lire(relatif, binaire=False):
        with open(os.path.join(dossier, relatif), "rb" if binaire else "r", **({} if binaire else {"encoding": "utf-8"})) as f:
            return f.read()

    def style(m):
        relatif = m.group(1)
        css = lire(relatif)
        base = os.path.dirname(relatif)

        def police(p):
            data = base64.b64encode(lire(os.path.join(base, p.group(1)), binaire=True)).decode("ascii")
            return f"url(data:font/woff2;base64,{data})"

        css = re.sub(r"url\((polices/[\w.\-]+\.woff2)\)", police, css)
        return f"<style>\n{css}</style>"

    html, n_css = re.subn(r'<link rel="stylesheet" href="(charte/[\w.\-]+\.css)">', style, html)
    html, n_js = re.subn(r'<script src="(charte/[\w.\-]+\.js)"></script>',
                         lambda m: "<script>\n" + lire(m.group(1)) + "</script>", html)
    if n_css < 2 or n_js < 1:
        raise ValueError("liens vers charte/ introuvables dans le deck : le gabarit a été modifié")
    return html


def main(argv):
    args = [a for a in argv[1:] if a != "--force"]
    force = "--force" in argv[1:]
    if not args or len(args) > 2 or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args and args[0] in ("-h", "--help") else 2
    source = os.path.abspath(args[0])
    dossier = os.path.dirname(source)
    sortie = args[1] if len(args) == 2 else os.path.join(os.path.dirname(dossier), os.path.basename(dossier) + "-autonome.html")
    try:
        with open(source, encoding="utf-8") as f:
            html = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f"Fichier illisible : {source} ({e})", file=sys.stderr)
        return 2
    erreurs, _, nb = controler(html)
    if erreurs and not force:
        print(f"Deck non assemblé : {len(erreurs)} erreur(s) au contrôle. Lancer controle_deck.py, corriger, puis recommencer.", file=sys.stderr)
        return 1
    try:
        resultat = assembler(html, dossier)
    except (OSError, ValueError) as e:
        print(f"Assemblage impossible : {e}", file=sys.stderr)
        return 1
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(resultat)
    print(f"Écrit : {sortie} ({nb} slides, {len(resultat)} caractères). Fichier de diffusion : ne pas le relire ni le modifier.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

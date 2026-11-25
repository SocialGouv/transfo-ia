#!/usr/bin/env python3
"""Produit la planche d'un deck : une image qui montre toutes les slides, pour contrôler le rendu.

Sur la planche, une slide dont un contenu déborde est encadrée en rouge, et son étiquette
nomme l'emplacement en cause. Il faut un navigateur capable de tourner sans écran
(Firefox ou un navigateur de la famille Chromium). Sans navigateur, le script le dit et
s'arrête : le rendu est alors « non contrôlé », à signaler dans le compte rendu.

Usage : python3 planche.py chemin/deck.html [sortie.png]
Sortie par défaut : planche.png, à côté de deck.html.
Variable NAVIGATEUR : chemin d'un navigateur à employer en priorité.
Code de sortie : 0 image écrite · 1 le navigateur a échoué · 2 aucun navigateur ou usage incorrect.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATS = ["firefox", "firefox-esr", "chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "msedge"]
CACHES = ["~/.cache/ms-playwright/firefox-*/firefox/firefox", "~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome"]


def trouver_navigateur():
    choix = os.environ.get("NAVIGATEUR")
    if choix:
        return choix if os.path.exists(choix) or shutil.which(choix) else None
    for motif in CACHES:
        trouves = sorted(glob.glob(os.path.expanduser(motif)))
        if trouves:
            return trouves[-1]
    for nom in CANDIDATS:
        chemin = shutil.which(nom)
        if chemin:
            return chemin
    return None


def hauteur_planche(nb_slides):
    rangees = (nb_slides + 1) // 2
    return 54 + rangees * (540 + 54) + 24


def commande(navigateur, url, sortie, largeur, hauteur, profil):
    if "firefox" in os.path.basename(navigateur).lower():
        return [navigateur, "--headless", "--no-remote", "--profile", profil,
                f"--window-size={largeur},{hauteur}", "--screenshot", sortie, url]
    return [navigateur, "--headless", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={profil}",
            f"--window-size={largeur},{hauteur}", f"--screenshot={sortie}", url]


def environnement():
    """Retire les variables graphiques posées par un éditeur installé en snap : elles font planter Firefox."""
    env = dict(os.environ)
    for cle in list(env):
        if cle.startswith(("GTK_", "GDK_", "GIO_", "GSETTINGS_")) or cle == "LOCPATH":
            if "/snap/" in env[cle]:
                del env[cle]
    origine = env.get("XDG_DATA_DIRS_VSCODE_SNAP_ORIG")
    if origine:
        env["XDG_DATA_DIRS"] = origine
    env["MOZ_HEADLESS"] = "1"
    return env


def main(argv):
    if len(argv) not in (2, 3) or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if len(argv) == 2 else 2
    source = os.path.abspath(argv[1])
    if not os.path.isfile(source):
        print(f"Fichier introuvable : {source}", file=sys.stderr)
        return 2
    sortie = os.path.abspath(argv[2]) if len(argv) == 3 else os.path.join(os.path.dirname(source), "planche.png")
    with open(source, encoding="utf-8") as f:
        sans_commentaires = re.sub(r'<!--.*?-->', '', f.read(), flags=re.S)
    nb = len(re.findall(r'<section[\s>]', sans_commentaires))
    if nb == 0:
        print("Aucune slide dans ce fichier : pas de planche.", file=sys.stderr)
        return 2
    navigateur = trouver_navigateur()
    if not navigateur:
        print("Aucun navigateur trouvé : rendu non contrôlé. Indiquer un navigateur par la variable NAVIGATEUR, "
              "ou ouvrir deck.html?planche à la main.", file=sys.stderr)
        return 2
    url = Path(source).as_uri() + "?planche"
    if os.path.exists(sortie):
        os.remove(sortie)
    with tempfile.TemporaryDirectory(prefix="planche-") as profil:
        try:
            subprocess.run(commande(navigateur, url, sortie, 1992, hauteur_planche(nb), profil),
                           env=environnement(), timeout=90, check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (OSError, subprocess.TimeoutExpired) as e:
            print(f"Le navigateur a échoué : {e}", file=sys.stderr)
            return 1
    if not os.path.isfile(sortie) or os.path.getsize(sortie) == 0:
        print(f"Le navigateur ({navigateur}) n'a produit aucune image : rendu non contrôlé.", file=sys.stderr)
        return 1
    print(f"Écrit : {sortie} ({nb} slides). Regarder l'image : un cadre rouge signale un débordement.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

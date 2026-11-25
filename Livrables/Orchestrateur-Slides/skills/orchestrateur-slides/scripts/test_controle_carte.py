"""Tests du contrôle de la carte. Lancer : python3 -m unittest test_controle_carte (depuis ce dossier)."""
import os
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import controle_carte  # noqa: E402
from controle_carte import controler  # noqa: E402

CHARTE = os.path.join(os.path.dirname(os.path.dirname(ICI)), "charte-dsfr")

CARTE = """# Carte des messages : Des comptes rendus sans y passer la soirée

- Fil rouge : un assistant rend une heure par semaine à chaque chef de projet.
- Auditoire et demande finale : le comité de pilotage ; un accord pour un essai de deux mois.
- Canal : projeté
- Temps de l'histoire : Le constat | La réponse
- En bref : Les comptes rendus coûtent une heure par semaine. Un assistant les rédige. Nous demandons un essai.

## 1. Une heure rendue par semaine
- Nature : couverture
- À l'écran : Comité de pilotage ; un essai de deux mois ; l'équipe projet

## 2. Chaque chef de projet passe une heure par semaine à rédiger
- Temps : 1
- Nature : chiffre
- À l'écran : 1 h par semaine ; [à fournir : le nombre de réunions par mois]
- Source : fourni par l'utilisateur

## 3. L'assistant rédige, le chef de projet relit
- Temps : 2
- Nature : étapes
- À l'écran : Réunion ; Brouillon ; Relecture
- Source : fourni par l'utilisateur

## 4. Ce que nous vous demandons
- Nature : conclusion
- À l'écran : une heure rendue ; données dans le cadre ; relecture humaine ; puis la demande : aujourd'hui, un accord
"""


class Carte(unittest.TestCase):
    def test_carte_juste(self):
        erreurs, avertissements, nb = controler(CARTE)
        self.assertEqual((erreurs, nb), ([], 4))
        self.assertEqual(len(avertissements), 1)
        self.assertIn("slide 2", avertissements[0])

    def test_titre_trop_long_selon_la_nature(self):
        e = controler(CARTE.replace("## 1. Une heure rendue par semaine", "## 1. Une heure rendue par semaine à chaque chef de projet"))[0]
        self.assertEqual(len(e), 1)
        self.assertRegex(e[0], r"slide 1 \(couverture\) · titre de \d+ caractères, maximum 32\. Raccourcir de \d+")
        self.assertEqual(controler(CARTE.replace("## 2. Chaque", "## 2. " + "Chaque " * 4 + "chaque"))[0], [])

    def test_nature_inconnue_et_temps(self):
        e = controler(CARTE.replace("- Nature : étapes", "- Nature : frise"))[0]
        self.assertTrue(any("nature « frise » inconnue" in x for x in e))
        e = controler(CARTE.replace("- Temps : 2", "- Temps : 5"))[0]
        self.assertTrue(any("slide 3" in x and "numéro de 1 à 2" in x for x in e))
        self.assertTrue(any("Temps sans aucune slide : La réponse" in x for x in e))
        e = controler(CARTE.replace("Le constat | La réponse", "Le constat de départ | La réponse"))[0]
        self.assertTrue(any("maximum 12" in x for x in e))

    def test_en_tete_et_numerotation(self):
        e = controler(CARTE.replace("- En bref : Les comptes", "- Résumé : Les comptes"))[0]
        self.assertTrue(any("« - En bref : … » manquante" in x for x in e))
        e = controler(CARTE.replace("## 3. L'assistant", "## 5. L'assistant"))[0]
        self.assertTrue(any("numérotée 5" in x for x in e))
        e = controler(CARTE.replace("- À l'écran : Réunion ; Brouillon ; Relecture\n", ""))[0]
        self.assertTrue(any("slide 3" in x and "À l'écran" in x for x in e))

    def test_a_l_ecran_en_liste_admis(self):
        liste = CARTE.replace("- À l'écran : Réunion ; Brouillon ; Relecture", "- À l'écran :\n  - Réunion\n  - Brouillon\n  - Relecture")
        self.assertEqual(controler(liste)[0], [])
        vide = CARTE.replace("- À l'écran : Réunion ; Brouillon ; Relecture", "- À l'écran :")
        self.assertTrue(any("slide 3" in x and "À l'écran" in x for x in controler(vide)[0]))

    def test_texte_du_modele_reste_en_place(self):
        e = controler(CARTE.replace("- Canal : projeté", "- Canal : <projeté, discuté ou lu seul>"))[0]
        self.assertTrue(any("chevrons" in x for x in e))

    def test_derniere_slide_sans_conclusion_avertit(self):
        sans = CARTE[:CARTE.index("## 4.")]
        erreurs, avertissements, _ = controler(sans)
        self.assertEqual(erreurs, [])
        self.assertTrue(any("pas une conclusion" in a for a in avertissements))

    def test_valeurs_par_defaut_egales_a_la_charte(self):
        titres, temps, natures_max = controle_carte.lire_charte(CHARTE)
        self.assertEqual(titres, controle_carte.TITRES)
        self.assertEqual(temps, controle_carte.TEMPS)
        self.assertEqual(natures_max, controle_carte.NATURES_MAX)

    def test_trop_de_natures_differentes(self):
        natures = [n for n in controle_carte.TITRES if n not in ("couverture", "conclusion")][:10]
        slides = "".join(f"\n## {k}. Un titre qui affirme quelque chose\n- Temps : 1\n- Nature : {n}\n- À l'écran : un élément\n" for k, n in enumerate(natures, 2))
        carte = CARTE[:CARTE.index("## 2.")].replace("Le constat | La réponse", "Le constat | La réponse").rstrip() + "\n" + slides
        carte += f"\n## {len(natures) + 2}. Ce que nous vous demandons\n- Nature : conclusion\n- À l'écran : trois choses ; puis la demande\n"
        carte = carte.replace("- Temps : 1\n- Nature : " + natures[-1], "- Temps : 2\n- Nature : " + natures[-1])
        e = controler(carte)[0]
        self.assertEqual(len(e), 1, e)
        self.assertIn("12 natures différentes dans le deck, maximum 10", e[0])

    def test_natures_du_skill_d_histoire_egales_a_celles_de_la_charte(self):
        chemin = os.path.join(os.path.dirname(os.path.dirname(ICI)), "histoire-slides", "SKILL.md")
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
        tableau = texte[texte.index("| Le message s'appuie sur | Nature |"):texte.index("Varie les natures")]
        natures = [l.rsplit("|", 2)[1].strip() for l in tableau.splitlines()[2:] if l.startswith("|")]
        self.assertEqual(sorted(natures), sorted(controle_carte.TITRES))

    def test_ligne_de_commande(self):
        script = os.path.join(ICI, "controle_carte.py")
        with tempfile.TemporaryDirectory() as d:
            bon, mauvais = os.path.join(d, "bon.md"), os.path.join(d, "mauvais.md")
            with open(bon, "w", encoding="utf-8") as f:
                f.write(CARTE)
            with open(mauvais, "w", encoding="utf-8") as f:
                f.write(CARTE.replace("- Nature : étapes", "- Nature : frise"))

            def code(*args):
                return subprocess.run([sys.executable, script, *args], capture_output=True).returncode

            self.assertEqual(code(bon), 0)
            self.assertEqual(code(bon, "--charte", CHARTE), 0)
            self.assertEqual(code(mauvais), 1)
            self.assertEqual(code(os.path.join(d, "absent.md")), 2)
            self.assertEqual(code(bon, "--charte", os.path.join(d, "pas-une-charte")), 2)
            self.assertEqual(code(), 2)


if __name__ == "__main__":
    unittest.main()

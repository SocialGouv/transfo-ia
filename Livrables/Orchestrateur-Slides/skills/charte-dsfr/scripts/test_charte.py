"""Tests des scripts de la charte. Lancer : python3 -m unittest test_charte -v (depuis ce dossier)."""
import os
import re
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import assembler  # noqa: E402
import generer_reference  # noqa: E402
import planche  # noqa: E402
import reference  # noqa: E402
from compositions import CATALOGUE, COMPOSITIONS, ICONES, ORDRE, SENS_ICONES  # noqa: E402
from controle_deck import controler  # noqa: E402


def deck(*slides, titre="Titre", pied="Sujet · Précision", fil="Un | Deux | Trois"):
    """Un deck minimal valide autour des slides données."""
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{titre}</title>
<meta name="deck-marque" content="République / Française"><meta name="deck-pied" content="{pied}">
<meta name="deck-fil" content="{fil}">
<link rel="stylesheet" href="charte/bloc-marque.css"><link rel="stylesheet" href="charte/slides.css"></head>
<body><main class="deck"><div class="stage">
{''.join(slides)}
</div></main><script src="charte/deck.js"></script></body></html>"""


ENONCE = COMPOSITIONS["enonce"]["exemple"]
CARTES = COMPOSITIONS["cartes"]["exemple"]
TABLEAU = COMPOSITIONS["tableau"]["exemple"]


class Controle(unittest.TestCase):
    def erreurs(self, html):
        return controler(html)[0]

    def test_chaque_exemple_passe_le_controle(self):
        for nom in ORDRE:
            with self.subTest(composition=nom):
                self.assertEqual(self.erreurs(deck(COMPOSITIONS[nom]["exemple"])), [])

    def test_catalogue_entier_sans_erreur_ni_avertissement(self):
        erreurs, avertissements, nb = controler(deck(*(COMPOSITIONS[n]["exemple"] for n in ORDRE)))
        self.assertEqual((erreurs, nb), ([], len(ORDRE)))
        self.assertEqual(len(avertissements), 1)
        self.assertIn("Texte d'exemple", avertissements[0])

    def test_texte_d_exemple_reste_en_place_signale_puis_leve(self):
        _, avertissements, _ = controler(deck(ENONCE))
        self.assertTrue(any("Texte d'exemple" in a and "slide 1" in a for a in avertissements))
        mien = ENONCE.replace("Et il juge mal une mise en page : texte qui déborde, slide saturée, couleurs sans règle.", "Un autre appui.")
        mien = re.sub(r'<h2 data-slot="titre">.*?</h2>', '<h2 data-slot="titre">Mon propre message</h2>', mien, flags=re.S)
        self.assertFalse(any("Texte d'exemple" in a for a in controler(deck(mien))[1]))

    def test_deck_aux_limites_passe_et_un_caractere_de_plus_echoue(self):
        for nom in ORDRE:
            with self.subTest(composition=nom):
                self.assertEqual(self.erreurs(deck(generer_reference.slide_limite(nom, 1.0), fil="A | B | C | D")), [])
        trop = self.erreurs(deck(generer_reference.slide_limite("cartes", 1.1)))
        self.assertTrue(any("carte-texte" in e and "Raccourcir" in e for e in trop))

    def test_texte_trop_long_dit_de_combien_raccourcir(self):
        long = ENONCE.replace("Il raconte rarement", "Il raconte rarement, vraiment très rarement, presque jamais en fait,")
        e = self.erreurs(deck(long))
        self.assertEqual(len(e), 1)
        self.assertRegex(e[0], r"slide 1 \(enonce\) · emplacement « titre » : \d+ caractères, maximum 75 .*Raccourcir de \d+")

    def test_composition_inconnue(self):
        e = self.erreurs(deck(ENONCE.replace('data-composition="enonce"', 'data-composition="heros"')))
        self.assertTrue(any("composition inconnue" in x for x in e))

    def test_emplacement_obligatoire_manquant_et_emplacement_inconnu(self):
        sans = re.sub(r"<h2 data-slot=\"titre\">.*?</h2>", "", ENONCE, flags=re.S)
        self.assertTrue(any("« titre » manquant" in x for x in self.erreurs(deck(sans))))
        faux = ENONCE.replace('data-slot="appui"', 'data-slot="soustitre"')
        self.assertTrue(any("« soustitre » inconnu" in x for x in self.erreurs(deck(faux))))

    def test_trop_d_elements_repetes(self):
        carte = re.search(r"<div data-item=\"carte\"[^>]*>.*?</div>", CARTES, flags=re.S).group(0)
        cinq = CARTES.replace(carte, carte + carte, 1)
        self.assertTrue(any("5 éléments « carte », il en faut 2 à 4" in x for x in self.erreurs(deck(cinq))))

    def test_style_ajoute_refuse(self):
        e = self.erreurs(deck(ENONCE.replace('<h2 data-slot="titre">', '<h2 data-slot="titre" style="font-size:20px">')))
        self.assertTrue(any("attribut style interdit" in x for x in e))
        e = self.erreurs(deck(ENONCE + "<style>.x{color:red}</style>"))
        self.assertTrue(any("<style> interdite" in x for x in e))

    def test_icone_inconnue_manquante_ou_mal_placee(self):
        e = self.erreurs(deck(CARTES.replace('data-icone="i-user"', 'data-icone="i-rocket"')))
        self.assertTrue(any("carte 1 · icône « i-rocket » inconnue" in x for x in e))
        e = self.erreurs(deck(CARTES.replace(' data-icone="i-user"', "")))
        self.assertTrue(any("carte 1 · attribut data-icone manquant" in x for x in e))
        e = self.erreurs(deck(ENONCE.replace('<h2 data-slot="titre">', '<h2 data-slot="titre" data-icone="i-user">')))
        self.assertTrue(any("data-icone non admis" in x and "n'a pas d'icône" in x for x in e))

    def test_contenu_hors_emplacement_refuse(self):
        e = self.erreurs(deck(ENONCE.replace("</section>", "<p>Un paragraphe en plus.</p></section>")))
        self.assertTrue(any("balise <p> hors emplacement" in x for x in e), e)
        e = self.erreurs(deck(ENONCE.replace("</section>", "Du texte nu.</section>")))
        self.assertTrue(any("texte hors emplacement" in x and "Du texte nu." in x for x in e), e)
        e = self.erreurs(deck(ENONCE.replace("</section>", '<img src="x.png" alt=""></section>')))
        self.assertTrue(any("balise <img> hors emplacement" in x for x in e), e)

    def test_un_emplacement_ne_contient_que_du_texte(self):
        e = self.erreurs(deck(ENONCE.replace("Et il juge mal", "<ul><li>Et il juge mal</li></ul>")))
        self.assertTrue(any("balise <ul> non admise dans un emplacement" in x for x in e), e)
        e = self.erreurs(deck(ENONCE.replace("<em>", '<em class="title">')))
        self.assertTrue(any("balise <em> non admise" in x for x in e), e)
        self.assertEqual(self.erreurs(deck(ENONCE.replace("Et il juge mal", "Et il juge <strong>mal</strong><br>"))), [])

    def test_element_repete_imbrique_refuse(self):
        carte = re.search(r"<div data-item=\"carte\"[^>]*>.*?</div>", CARTES, flags=re.S).group(0)
        e = self.erreurs(deck(CARTES.replace(carte, carte[:-6] + carte + "</div>", 1)))
        self.assertTrue(any("placé dans un autre élément répété" in x for x in e), e)

    def test_enveloppes_et_balises_au_choix_admises(self):
        libre = CARTES.replace("<h2 data-slot", "<h1 data-slot").replace("</h2>", "</h1>")
        libre = libre.replace('<div data-item="carte" data-icone="i-user">', '<ul><li data-item="carte" data-icone="i-user">', 1)
        libre = libre.replace("point d’arrêt.</p></div>", "point d’arrêt.</p></li></ul>", 1)
        self.assertEqual(self.erreurs(deck(libre)), [])

    def test_tableau_cellules_et_colonnes(self):
        casse = TABLEAU.replace('<p data-slot="cellule">Le brief</p>', "", 1)
        self.assertTrue(any("rangee 1 : 3 « cellule » pour 4 « entete »" in x for x in self.erreurs(deck(casse))))

    def test_couloirs_cases_vides_admises_mais_alignees(self):
        couloirs = COMPOSITIONS["couloirs"]["exemple"]
        self.assertEqual(self.erreurs(deck(couloirs)), [])
        casse = couloirs.replace('<p data-slot="case">reçoit le deck</p>', "", 1)
        e = self.erreurs(deck(casse))
        self.assertTrue(any("couloir 1 : 4 « case » pour 5 « etape-nom »" in x and "peut rester vide" in x for x in e), e)
        vide = re.sub(r'(<div data-item="couloir"><p data-slot="couloir-nom">Sous-agents</p>).*?</div>', r'\1' + '<p data-slot="case"></p>' * 5 + "</div>", couloirs)
        erreurs, avertissements, _ = controler(deck(vide))
        self.assertEqual(erreurs, [])
        self.assertTrue(any("couloir 3 : toutes ses « case » sont vides" in a for a in avertissements))

    def test_graphique_valeur_tracee_et_source(self):
        barres = COMPOSITIONS["barres"]["exemple"]
        e = self.erreurs(deck(barres.replace('data-valeur="119"', 'data-valeur="cent dix-neuf"')))
        self.assertTrue(any("barre 1 · data-valeur=\"cent dix-neuf\" n'est pas un nombre positif" in x for x in e), e)
        e = self.erreurs(deck(barres.replace(' data-valeur="119"', "")))
        self.assertTrue(any("barre 1 · attribut data-valeur manquant" in x for x in e), e)
        self.assertEqual(self.erreurs(deck(barres.replace('data-valeur="119"', 'data-valeur="1 119,5"'))), [])
        e = self.erreurs(deck(re.sub(r'data-valeur="\d+"', 'data-valeur="0"', barres)))
        self.assertTrue(any("toutes les valeurs « barre » sont nulles" in x for x in e), e)
        e = self.erreurs(deck(ENONCE.replace('<h2 data-slot="titre">', '<h2 data-slot="titre" data-valeur="3">')))
        self.assertTrue(any("data-valeur non admis" in x for x in e), e)
        sans = re.sub(r'<p data-slot="source">.*?</p>\n', "", barres)
        erreurs, avertissements, _ = controler(deck(sans))
        self.assertEqual(erreurs, [])
        self.assertTrue(any("graphique sans source" in a for a in avertissements))

    def test_un_seul_element_a_retenir(self):
        frise = COMPOSITIONS["frise"]["exemple"]
        self.assertEqual(self.erreurs(deck(frise)), [])
        e = self.erreurs(deck(frise.replace('data-ton="acquis"', "data-retenir", 1)))
        self.assertTrue(any("2 éléments portent data-retenir" in x for x in e), e)
        e = self.erreurs(deck(CARTES.replace('data-icone="i-user"', 'data-icone="i-user" data-retenir')))
        self.assertTrue(any("data-retenir non admis" in x for x in e), e)

    def test_flux_dernier_bloc_sans_suite(self):
        flux = COMPOSITIONS["flux"]["exemple"]
        e = self.erreurs(deck(flux.replace("Il juge sur pièces et rend une revue.</p>", 'Il juge sur pièces et rend une revue.</p><p data-slot="bloc-vers">revue</p>')))
        self.assertTrue(any("le dernier « bloc » porte « bloc-vers »" in x for x in e), e)

    def test_html_mal_ferme(self):
        e = self.erreurs(deck(ENONCE.replace("</h2>", "", 1)))
        self.assertTrue(any("HTML mal formé" in x for x in e))

    def test_accolades_non_remplacees_et_en_tete(self):
        e = self.erreurs(deck(ENONCE, titre="{{TITRE DU DECK}}"))
        self.assertTrue(any("accolades" in x for x in e))
        e = self.erreurs(deck(ENONCE, fil="Un temps beaucoup trop long | Deux"))
        self.assertTrue(any("deck-fil" in x and "maximum 12" in x for x in e))
        e = self.erreurs(deck(ENONCE.replace('data-temps="1"', 'data-temps="7"')))
        self.assertTrue(any('data-temps="7"' in x for x in e))

    def test_avertissements_sans_erreur(self):
        erreurs, avertissements, _ = controler(deck(ENONCE.replace("couleurs sans règle", "[à fournir : le chiffre]")))
        self.assertEqual(erreurs, [])
        self.assertTrue(any("à fournir" in a for a in avertissements))
        self.assertTrue(any("première slide" in a for a in avertissements))

    def test_trop_de_notes_signale(self):
        _, avertissements, _ = controler(deck(ENONCE.replace("</section>", "<p data-note>Note.</p>" * 5 + "</section>")))
        self.assertTrue(any("6 notes" in a for a in avertissements))

    def test_temps_sans_slide_signale(self):
        _, avertissements, _ = controler(deck(ENONCE, COMPOSITIONS["cartes"]["exemple"]))
        self.assertTrue(any("sans aucune slide : Trois" in a for a in avertissements))

    def test_ligne_de_commande(self):
        with tempfile.TemporaryDirectory() as d:
            bon, mauvais = os.path.join(d, "bon.html"), os.path.join(d, "mauvais.html")
            with open(bon, "w", encoding="utf-8") as f:
                f.write(deck(ENONCE))
            with open(mauvais, "w", encoding="utf-8") as f:
                f.write(deck(ENONCE.replace("#", "#")).replace('data-composition="enonce"', 'data-composition="x"'))
            script = os.path.join(ICI, "controle_deck.py")
            self.assertEqual(subprocess.run([sys.executable, script, bon], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run([sys.executable, script, mauvais], capture_output=True).returncode, 1)
            self.assertEqual(subprocess.run([sys.executable, script, os.path.join(d, "absent.html")], capture_output=True).returncode, 2)
            self.assertEqual(subprocess.run([sys.executable, script], capture_output=True).returncode, 2)


class Reference(unittest.TestCase):
    def test_reference_reduite_aux_compositions_demandees(self):
        texte = reference.texte(["chiffres", "frise"])
        self.assertIn("### `chiffres` (chiffre)", texte)
        self.assertIn("### `frise` (frise datée)", texte)
        self.assertNotIn("### `cartes`", texte)
        self.assertIn("**À retenir**", texte)
        self.assertNotIn("**Graphiques**", texte)
        self.assertNotIn("**Icônes**", texte)
        tout = reference.texte(ORDRE)
        for nom in ORDRE:
            self.assertIn(f"### `{nom}`", tout)
        for regle in ("**Graphiques**", "**Icônes**", "**À retenir**"):
            self.assertIn(regle, tout)
        self.assertEqual(sorted(COMPOSITIONS), sorted(ORDRE))
        self.assertEqual(sorted(SENS_ICONES), sorted(ICONES))

    def test_reference_d_une_carte(self):
        carte = "## 1. Titre\n- Nature : couverture\n## 2. Autre\n- Temps : 1\n- Nature : graphique en barres\n## 3. Fin\n- Nature : conclusion\n"
        slides, inconnues = reference.natures_de_la_carte(carte)
        self.assertEqual((slides, inconnues), (["couverture", "barres", "conclusion"], []))
        self.assertEqual(reference.natures_de_la_carte("- Nature : frise chronologique\n"), ([], ["frise chronologique"]))
        with tempfile.TemporaryDirectory() as d:
            chemin = os.path.join(d, "carte.md")
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(carte)
            script = os.path.join(ICI, "reference.py")
            r = subprocess.run([sys.executable, script, chemin], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            self.assertIn("Composition de chaque slide de la carte : 1 `couverture` · 2 `barres` · 3 `conclusion`.", r.stdout)
            self.assertIn("### `barres` (graphique en barres)", r.stdout)
            self.assertNotIn("### `courbe`", r.stdout)
            with open(chemin, "w", encoding="utf-8") as f:
                f.write("- Nature : camembert\n")
            self.assertEqual(subprocess.run([sys.executable, script, chemin], capture_output=True).returncode, 2)
            self.assertEqual(subprocess.run([sys.executable, script, "chiffres", "frise"], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run([sys.executable, script, "chiffres", "camembert"], capture_output=True).returncode, 2)
            self.assertEqual(subprocess.run([sys.executable, script, "--liste"], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run([sys.executable, script], capture_output=True).returncode, 2)

    def test_icones_presentes_dans_le_gabarit(self):
        with open(os.path.join(generer_reference.GABARIT, "charte", "deck.js"), encoding="utf-8") as f:
            js = f.read()
        self.assertEqual(sorted(re.findall(r'<symbol id="(i-[\w-]+)"', js)), sorted(ICONES))

    def test_exemples_en_ecriture_courte_et_chaque_composition_a_son_constructeur(self):
        with open(os.path.join(generer_reference.GABARIT, "charte", "deck.js"), encoding="utf-8") as f:
            js = f.read()
        self.assertEqual(sorted(re.findall(r"^      (\w+): \(\) =>", js, flags=re.M)), sorted(ORDRE))
        for nom in ORDRE:
            with self.subTest(composition=nom):
                self.assertNotRegex(COMPOSITIONS[nom]["exemple"], r"\b(class|style)=")
                self.assertTrue(COMPOSITIONS[nom]["exemple"].startswith(f'<section data-composition="{nom}"'))

    def test_classes_posees_par_le_script_definies_dans_la_feuille_de_styles(self):
        dossier = os.path.join(generer_reference.GABARIT, "charte")
        with open(os.path.join(dossier, "deck.js"), encoding="utf-8") as f:
            js = f.read()
        with open(os.path.join(dossier, "slides.css"), encoding="utf-8") as f:
            css = f.read()
        depliage = js[js.index("function deplier"):js.index("slides.forEach(deplier)")]
        classes = set()
        for chaine in re.findall(r"'([a-z][\w -]*)'", depliage):
            classes.update(c for c in chaine.split() if "-" in c or "_" in c)
        classes -= set(ICONES) | {"aria-hidden", "data-marque", "data-pied", "data-page", "data-retenir", "s-body"} | {s for c in COMPOSITIONS.values() for s in list(c["slots"]) + [x for g in c["groupes"].values() for x in g["slots"]]}
        self.assertGreater(len(classes), 20)
        for c in sorted(classes):
            with self.subTest(classe=c):
                self.assertIn("." + c, css)

    def test_tableau_de_choix_a_jour_dans_le_skill(self):
        with open(os.path.join(generer_reference.SKILL, "SKILL.md"), encoding="utf-8") as f:
            self.assertIn(reference.tableau_de_choix(), f.read(), "SKILL.md : tableau « Choisir la composition » à remettre à jour")

    def test_exemples_courts_de_la_reference_valides(self):
        for nom in ORDRE:
            with self.subTest(composition=nom):
                court = reference.exemple_court(COMPOSITIONS[nom])
                self.assertEqual(controler(deck(court))[0], [])
        self.assertEqual(reference.exemple_court(COMPOSITIONS["cartes"]).count('data-item="carte"'), 2)
        self.assertEqual(reference.exemple_court(COMPOSITIONS["etapes"]).count('data-item="etape"'), 3)
        self.assertEqual(reference.exemple_court(COMPOSITIONS["contraste"]), COMPOSITIONS["contraste"]["exemple"])
        self.assertEqual(reference.exemple_court(COMPOSITIONS["flux"]), COMPOSITIONS["flux"]["exemple"])

    def test_deck_au_minimum_valide(self):
        for nom in ORDRE:
            with self.subTest(composition=nom):
                self.assertEqual(self.erreurs(deck(generer_reference.slide_minimum(nom))), [])
        self.assertEqual(generer_reference.slide_minimum("chiffres").count('data-item="chiffre"'), 1)
        self.assertNotIn("data-note", generer_reference.slide_minimum("enonce"))

    def erreurs(self, html):
        return controler(html)[0]

    def test_ligne_des_limites(self):
        self.assertEqual(reference.limites(COMPOSITIONS["cartes"]),
                         "Limites : `titre` 90 · `chapo` 95 (facultatif) · 2 à 4 éléments `carte`, chacun avec `data-icone` : `carte-titre` 30, `carte-texte` 110.")
        self.assertIn("autant de `cellule`", reference.limites(COMPOSITIONS["tableau"]))
        self.assertIn("2 à 6 éléments `barre`, chacun avec `data-valeur`", reference.limites(COMPOSITIONS["barres"]))
        self.assertIn("`case` 36 (3 à 6 fois), peut rester vide", reference.limites(COMPOSITIONS["couloirs"]))


class Assemblage(unittest.TestCase):
    def test_catalogue_assemble_en_un_fichier_autonome(self):
        with tempfile.TemporaryDirectory() as d:
            dossier = os.path.join(d, "deck")
            chemin = generer_reference.ecrire_deck(dossier, [COMPOSITIONS[n]["exemple"] for n in ORDRE],
                                                   CATALOGUE["titre"], CATALOGUE["pied"], CATALOGUE["fil"])
            self.assertEqual(assembler.main(["assembler.py", chemin]), 0)
            with open(os.path.join(d, "deck-autonome.html"), encoding="utf-8") as f:
                html = f.read()
            self.assertNotIn('href="charte/', html)
            self.assertNotIn('src="charte/', html)
            self.assertNotIn("url(polices/", html)
            self.assertEqual(html.count("data:font/woff2;base64,"), 4)
            self.assertIn("data-composition=\"conclusion\"", html)

    def test_deck_en_erreur_non_assemble(self):
        with tempfile.TemporaryDirectory() as d:
            dossier = os.path.join(d, "deck")
            chemin = generer_reference.ecrire_deck(dossier, [ENONCE.replace('"enonce"', '"x"')], "T", "S · P", "A | B")
            self.assertEqual(assembler.main(["assembler.py", chemin]), 1)
            self.assertFalse(os.path.exists(os.path.join(d, "deck-autonome.html")))
            self.assertEqual(assembler.main(["assembler.py", chemin, "--force"]), 0)


class Planche(unittest.TestCase):
    def test_hauteur_et_commandes(self):
        self.assertEqual(planche.hauteur_planche(11), 54 + 6 * 594 + 24)
        ff = planche.commande("/x/firefox", "file:///d.html?planche", "/o.png", 1992, 800, "/p")
        self.assertIn("--screenshot", ff)
        ch = planche.commande("/x/chromium", "file:///d.html?planche", "/o.png", 1992, 800, "/p")
        self.assertIn("--screenshot=/o.png", ch)

    def test_usage_et_fichier_absent(self):
        self.assertEqual(planche.main(["planche.py"]), 2)
        self.assertEqual(planche.main(["planche.py", "/chemin/absent/deck.html"]), 2)

    def test_gabarit_vide_sans_slide(self):
        self.assertEqual(planche.main(["planche.py", os.path.join(generer_reference.GABARIT, "deck.html")]), 2)

    def test_sans_navigateur_le_dit(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = generer_reference.ecrire_deck(os.path.join(d, "deck"), [ENONCE], "T", "S · P", "A | B")
            ancien = os.environ.get("NAVIGATEUR")
            os.environ["NAVIGATEUR"] = os.path.join(d, "aucun-navigateur")
            try:
                self.assertEqual(planche.main(["planche.py", chemin]), 2)
            finally:
                if ancien is None:
                    del os.environ["NAVIGATEUR"]
                else:
                    os.environ["NAVIGATEUR"] = ancien


if __name__ == "__main__":
    unittest.main()

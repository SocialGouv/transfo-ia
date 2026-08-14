#!/usr/bin/env python3
"""Génère les deux PPTX du récit de mission (1 slide et 3 slides) à partir
des mêmes contenus que les HTML du dossier parent. Style DSFR : Marianne,
blue-france #000091, cartes grises, bandes à liseré.

Usage : python3 deck.py   (écrit les .pptx dans Livrables/Recit-Mission2/)
"""
import re
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parent.parent

BF = RGBColor(0x00, 0x00, 0x91)      # blue-france
SOFT = RGBColor(0x7F, 0x7F, 0xC8)
BF925 = RGBColor(0xE3, 0xE3, 0xFD)
BF975 = RGBColor(0xF5, 0xF5, 0xFE)
G975 = RGBColor(0xF6, 0xF6, 0xF6)
G425 = RGBColor(0x66, 0x66, 0x66)
G125 = RGBColor(0xDD, 0xDD, 0xDD)
OK = RGBColor(0x18, 0x75, 0x3C)      # success
OK950 = RGBColor(0xDA, 0xF5, 0xE7)
BLACK = RGBColor(0x1E, 0x1E, 0x1E)
INK2 = RGBColor(0x2B, 0x2B, 0x2B)

KICKER = "TRANSFORMATION IA · MINISTÈRES SOCIAUX · SEMAINE DU 10 AU 14 AOÛT 2026"


def rect(slide, x, y, w, h, fill, line=None):
    sh = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def runs_of(text):
    """Découpe « aaa **bbb** ccc » en [(texte, bold)]."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*)", text):
        if not part:
            continue
        if part.startswith("**"):
            out.append((part[2:-2], True))
        else:
            out.append((part, False))
    return out


def text(slide, x, y, w, h, paras, size=11, color=BLACK, bold=False,
         bold_color=None, align=PP_ALIGN.LEFT, space_after=4, leading=1.15):
    """paras : chaîne ou liste de chaînes avec **gras**."""
    if isinstance(paras, str):
        paras = [paras]
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.line_spacing = leading
        for seg, b in runs_of(para):
            r = p.add_run()
            r.text = seg
            r.font.name = "Marianne"
            r.font.size = Pt(size)
            r.font.bold = bold or b
            r.font.color.rgb = (bold_color or color) if (b and bold_color) else color
    return tb


def card(slide, x, y, w, h, title, sub, paras, arrow=None,
         fill=G975, line=G125, top_bar=None, size=10):
    rect(slide, x, y, w, h, fill, line)
    if top_bar:
        rect(slide, x, y, w, 0.055, top_bar)
    text(slide, x + 0.12, y + 0.10, w - 0.24, 0.3, title, size=11.5, color=BF, bold=True)
    yy = y + 0.38
    if sub:
        text(slide, x + 0.12, yy, w - 0.24, 0.25, sub, size=8.5, color=G425, bold=True)
        yy += 0.26
    body = list(paras) + ([f"→ {arrow}"] if arrow else [])
    colors = [INK2] * len(paras) + ([SOFT] if arrow else [])
    for para, c in zip(body, colors):
        tb = text(slide, x + 0.12, yy, w - 0.24, h - (yy - y) - 0.08, para,
                  size=size, color=c, bold=(c is SOFT), bold_color=BLACK)
        yy += 0.205 * sum(1 for _ in tb.text_frame.paragraphs) + 0.14 + \
            0.155 * (len(para) // int((w - 0.24) * 15))


def band(slide, x, y, w, h, paras, edge=BF, fill=BF975, title=None, size=10.5):
    rect(slide, x, y, w, h, fill)
    rect(slide, x, y, 0.07, h, edge)
    yy = y + 0.10
    if title:
        text(slide, x + 0.22, yy, w - 0.4, 0.28, title, size=10.5, color=edge, bold=True)
        yy += 0.30
    text(slide, x + 0.22, yy, w - 0.44, h - (yy - y) - 0.08, paras,
         size=size, color=BLACK, bold_color=BF)


def header(slide, kicker, title_runs, num=None, y_title=0.58, title_size=26):
    text(slide, 0.6, 0.32, 11.0, 0.25, kicker, size=9.5, color=BF, bold=True)
    text(slide, 0.6, y_title, 12.1, 0.75, title_runs, size=title_size,
         color=G425, bold_color=BF)
    if num:
        text(slide, 11.9, 0.32, 0.9, 0.25, num, size=9.5, color=SOFT, bold=True,
             align=PP_ALIGN.RIGHT)


def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# ---------------------------------------------------------------- one-pager
def build_one_pager():
    prs = new_deck()
    s = blank(prs)

    text(s, 0.6, 0.32, 11.0, 0.25, KICKER, size=9.5, color=BF, bold=True)
    text(s, 0.6, 0.58, 10.6, 0.55, "**De l'usage individuel à l'adoption par les équipes**",
         size=26, color=G425, bold_color=BF)
    text(s, 10.6, 0.42, 2.15, 0.8,
         ["Une acculturation réelle aux rôles et aux métiers — pas des démos.",
          "Impact · Ippon Technologies"],
         size=8.5, color=G425, align=PP_ALIGN.RIGHT, space_after=2)
    rect(s, 0.6, 1.28, 12.15, 0.02, BF)

    text(s, 0.6, 1.42, 12.15, 0.6,
         "Le sujet n'est pas d'installer un outil, mais de **faire de l'IA une vraie "
         "pratique d'équipe** : on accompagne chaque rôle sur son métier, on lève les freins "
         "(outillage interne, souveraineté), et la demande devient entrante — les équipes "
         "viennent nous chercher.", size=12, color=INK2, bold_color=BF)

    cw, gap, y0, hh = 3.92, 0.195, 2.28, 3.0
    cards = [
        ("LES ÉQUIPES ACCOMPAGNÉES", "5 chantiers · 4 métiers · de la pratique au passage à l'échelle", [
            "**Egapro** — pilote, passé de 3 à 4 en maturité : orchestrations en routine.",
            "**DACCORD** — équipe moteur, monte sa propre orchestration (1 → 2).",
            "**SIRENA** — demande entrante : la cheffe de projet demande à être formée.",
            "**VAO** — en découverte, atelier dev augmenté le 8 septembre.",
            "**Transverse** — architectes (1 → 2), designers, référentiels (CEPS compris).",
        ]),
        ("RÔLES AVEC LESQUELS ÇA AVANCE", "Autant de leviers que de métiers", [
            "**Développeurs** — orchestrations sécurisées : le code n'est plus testé par l'agent qui l'a écrit.",
            "**Chefs de projet / PM** — Egapro pilote à la vitesse de l'IA · DACCORD & SIRENA passent aux tickets générés.",
            "**Designers** — prototypes DSFR testables, maquette Figma générée : Louis valide (13/08).",
            "**Architectes** — cinq use cases identifiés, priorisés par eux-mêmes.",
            "**PO & RU** — use cases en formalisation (Olivier, Felix).",
        ]),
        ("CE QUI CONDITIONNE L'ÉCHELLE", "Poste de travail · fournisseurs · bench", [
            "**Poste de travail** — deux voies opérationnelles sur PC ministère : OpenCode Desktop, Claude Code dans VS Code ; la matrice « qui peut utiliser quoi » est livrée.",
            "**Fournisseurs** — Bedrock viable (Claude Code + observabilité) mais harness imposé : Scaleway et Vertex AI à explorer.",
            "**Bench** — 7 stacks comparées (perf / prix / souveraineté / conformité), élargi aux modèles Bedrock en août.",
        ]),
    ]
    for i, (h2, tag, paras) in enumerate(cards):
        x = 0.6 + i * (cw + gap)
        rect(s, x, y0, cw, hh, BF975, BF925)
        rect(s, x, y0, cw, 0.055, BF)
        text(s, x + 0.14, y0 + 0.12, cw - 0.28, 0.3, h2, size=11, color=BF, bold=True)
        text(s, x + 0.14, y0 + 0.40, cw - 0.28, 0.25, tag, size=8, color=G425, bold=True)
        text(s, x + 0.14, y0 + 0.68, cw - 0.28, hh - 0.8, paras, size=9.5,
             color=INK2, bold_color=BLACK, space_after=5)

    band(s, 0.6, 5.42, 12.15, 1.42,
         ["**DACCORD** : dès le lundi suivant le coaching, l'équipe met en commun ses "
          "**system prompts** de sa propre initiative ; l'orchestration se monte en accompagnement "
          "individuel. **Chefs de projet** : formation à la **génération de tickets Jira** actée — "
          "DACCORD le 25 août avec Richard et Noura, SIRENA à caler (Aurélie est demandeuse). "
          "**Architectes** : de zéro intérêt à **cinq use cases** qu'ils priorisent eux-mêmes. "
          "**Designers** : de « l'IA a peu de valeur pour nous » à des **prototypes DSFR** testables "
          "et des **maquettes Figma générées** — Louis valide (13/08). **PO & RU** : Felix formalise "
          "les use cases."],
         edge=OK, fill=OK950, title="LE DÉCLIC, MÉTIER PAR MÉTIER", size=9.5)

    rect(s, 0.6, 7.02, 12.15, 0.013, G125)
    text(s, 0.6, 7.09, 8.6, 0.3,
         "**La stratégie avance à trois horizons** — outiller chaque métier, puis faire monter "
         "la pratique, puis passer à l'échelle.", size=9, color=G425, bold_color=BF)
    text(s, 9.3, 7.09, 3.45, 0.3, "Accompagnement réel, demande entrante, fondations posées.",
         size=9, color=G425, align=PP_ALIGN.RIGHT)

    prs.save(OUT / "Impact_Adoption-IA_1-slide.pptx")


# ---------------------------------------------------------------- 3 slides
def build_three_slides():
    prs = new_deck()

    # Slide 1 — le point de départ
    s = blank(prs)
    header(s, "LE POINT DE DÉPART", "**L'IA existait. Mais elle** restait dans les silos.",
           num="1 / 3")
    band(s, 0.6, 1.55, 12.15, 0.95,
         "Le frein n'est jamais le modèle, c'est **l'usage et l'outillage**. Sur poste managé, "
         "un agent ne pouvait même pas installer un harness. L'adoption, elle, restait "
         "individuelle — sans pratique d'équipe.", size=12)
    items = [
        ("Un usage en silo", None,
         ["L'IA était pratiquée individuellement (développeurs de SIRENA, etc.), sans coordination ni mutualisation."],
         "aucune pratique d'équipe partagée"),
        ("Des postes qui bloquaient", None,
         ["Sur un poste interne managé, impossible d'installer un harness soi-même."],
         "adoption cantonnée aux prestataires"),
        ("Une opportunité non vue", None,
         ["Les métiers ne connaissaient pas leurs propres cas d'usage potentiels."],
         "l'acculturation pouvait créer la demande"),
    ]
    for i, (t, sub, paras, arrow) in enumerate(items):
        card(s, 0.6 + i * 4.115, 2.75, 3.92, 2.3, t, sub, paras, arrow, size=10.5)

    # Slide 2 — le déclic
    s = blank(prs)
    header(s, "LE DÉCLIC · ACCOMPAGNER CHAQUE MÉTIER",
           "**On accompagne les rôles,** la demande devient entrante.", num="2 / 3")
    items = [
        ("Développeurs · Egapro", "pilote : 3 → 4 en maturité",
         ["Orchestrations en routine, désormais **sécurisées** : codeur et testeur séparés. "
          "Le chef de projet pilote à la vitesse de l'IA (estimations T-shirt, tickets design)."], None),
        ("Développeurs · DACCORD", "objectif : sa propre orchestration",
         ["Dès le lundi suivant le coaching, **l'équipe met ses system prompts en commun "
          "d'elle-même**. Skills sur cinq domaines (6/08), orchestration en accompagnement individuel."], None),
        ("Chefs de projet · DACCORD & SIRENA", "tickets Jira générés sur poste ministère",
         ["Formation actée : **DACCORD le 25 août** avec Richard et Noura ; Aurélie (SIRENA) "
          "**demande elle-même à être formée**, créneau à caler. Le ticket arrive formalisé, tests inclus."], None),
        ("Designers", "de « peu de valeur » au flux complet",
         ["Depuis un poste ministère : **prototypes DSFR testables** par des utilisateurs, puis "
          "**maquette Figma générée** en composants DSFR officiels. Louis valide le use case (13/08)."], None),
        ("Architectes · Transverse", "atelier de génération de DA",
         ["Ils ne connaissaient pas leurs cas d'usage : **l'atelier en a fait émerger cinq** "
          "(cohérence des choix, schémas, conformité, écarts DA/code). Priorisation d'ici au 21 août."], None),
        ("PO & Recherche utilisateurs", "RU et PO · en synchronisation",
         ["Synchronisation avec **Olivier Toumsy** ; **Felix** revient avec une **map des use cases "
          "RU et PO**. L'accompagnement tickets s'étend à VAO (Halim) et BIO2 (Yuna)."], None),
    ]
    for i, (t, sub, paras, arrow) in enumerate(items):
        x = 0.6 + (i % 3) * 4.115
        y = 1.62 + (i // 3) * 2.72
        card(s, x, y, 3.92, 2.55, t, sub, paras, arrow, size=10)

    # Slide 3 — les fondations
    s = blank(prs)
    header(s, "LES FONDATIONS · POUR PASSER À L'ÉCHELLE",
           "**On lève les freins :** poste de travail, fournisseurs, bench.", num="3 / 3")
    items = [
        ("Poste de travail : deux voies passent", None,
         ["**OpenCode Desktop** (sans droits admin, clé Albert) et **Claude Code dans VS Code** "
          "(clé Bedrock) fonctionnent sur PC ministère ; la matrice « qui peut utiliser quoi » est **livrée**."],
         "l'enjeu devient la liberté du choix du harness (centre logiciel, introduction par Olivier)"),
        ("Fournisseurs : ouvrir le choix", None,
         ["**Bedrock exploré avec AWS** : viable (Claude Code adossé à l'observabilité), mais le "
          "harness est imposé et gourmand en contexte. **Scaleway** (open-weight, souveraineté) et "
          "**Google Vertex AI** à explorer."],
         "viser une observabilité indépendante du harness"),
        ("Bench : décider sur des faits", None,
         ["Une **matrice performance / prix / souveraineté / conformité** a été bâtie (7 stacks), "
          "élargie aux modèles Bedrock en août ; la stack interne (et externes sur sujets "
          "confidentiels) se tranchera ensuite."],
         "un choix documenté, pas un pari"),
    ]
    for i, (t, sub, paras, arrow) in enumerate(items):
        card(s, 0.6 + i * 4.115, 1.62, 3.92, 3.1, t, sub, paras, arrow, size=10.5)

    band(s, 0.6, 5.05, 12.15, 1.15,
         "**La boucle se ferme.** À chaque métier accompagné, la demande arrive ensuite "
         "d'elle-même (SIRENA, architectes, designers, PO/RU). Accompagnement réel + freins levés "
         "= l'adoption devient **une dynamique d'équipe**, et non plus une somme d'usages individuels.",
         edge=OK, fill=OK950, size=11.5)

    prs.save(OUT / "Impact_Adoption-IA_3-slides.pptx")


if __name__ == "__main__":
    build_one_pager()
    build_three_slides()
    print("OK :", OUT / "Impact_Adoption-IA_1-slide.pptx")
    print("OK :", OUT / "Impact_Adoption-IA_3-slides.pptx")

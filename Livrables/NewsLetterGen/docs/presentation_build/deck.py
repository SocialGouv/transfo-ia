# -*- coding: utf-8 -*-
"""Deck explicatif de la veille JO (CEPS) - charte DSFR.
Code couleur par acteur : bleu France = la machine, périwinkle = l'IA, rouge Marianne = l'utilisatrice.
Helpers repris du pipeline des decks de checkpoint (juin_2026-v3/build/deck.py)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
IC = os.path.join(ASSETS, "ic")

# ---- Palette DSFR ----
INK = "161616"; BODY = "3A3A3A"; MENTION = "6A6A6A"; BLUE = "000091"; PERI = "6A6AF4"
LAV = "E3E3FD"; CARD = "F5F5FE"; CARD2 = "ECECFE"; RED = "E1000F"; WHITE = "FFFFFF"
RULE = "DDDDDD"; WARN = "B34000"
MAR = "Arial"  # Marianne absente du poste de génération et non garantie chez la cliente
DATE = "22/07/2026"

SW, SH = 13.333, 7.5
ML = 0.85
MR = SW - 0.85


def C(h):
    return RGBColor.from_string(h)


def slide(prs, bg=WHITE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if bg:
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        r.fill.solid(); r.fill.fore_color.rgb = C(bg); r.line.fill.background()
        r.shadow.inherit = False
        sp = r._element; sp.getparent().remove(sp); s.shapes._spTree.insert(2, sp)
    return s


def _sans_style(shp):
    """Retire l'élément <p:style> de la forme : LibreOffice applique sinon l'ombre
    du thème qu'il référence, malgré l'effectLst vide (constaté au rendu PDF)."""
    el = shp._element.find(qn('p:style'))
    if el is not None:
        shp._element.remove(el)


def rect(s, x, y, w, h, fill=None, line=None, lw=0.75, rounded=False, radius=0.06):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    _sans_style(shp)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = C(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = C(line); shp.line.width = Pt(lw)
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def hang(p, marL=0.22):
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', str(Inches(marL))); pPr.set('indent', str(-Inches(marL)))


def tb(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def para(tf, runs, align=PP_ALIGN.LEFT, sa=4, sb=0, ls=1.06, first=False, bullet=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    if sa is not None: p.space_after = Pt(sa)
    if sb is not None: p.space_before = Pt(sb)
    if ls is not None: p.line_spacing = ls
    if bullet: hang(p)
    for rr in runs:
        r = p.add_run(); r.text = rr['t']
        f = r.font
        f.name = rr.get('font', MAR); f.size = Pt(rr.get('sz', 16))
        f.bold = rr.get('b', False); f.italic = rr.get('i', False)
        f.color.rgb = C(rr.get('c', INK))
    return p


def R(t, **k):
    k['t'] = t; return k


def icon(s, name, x, y, size, white=False):
    suf = "_w" if white else ""
    s.shapes.add_picture(os.path.join(IC, f"{name}{suf}.png"),
                         Inches(x), Inches(y), width=Inches(size), height=Inches(size))


def node(s, name, cx, cy, dia=0.52, fill=PERI):
    rect(s, cx - dia / 2, cy - dia / 2, dia, dia, fill=fill, rounded=True, radius=0.5)
    isz = dia * 0.54
    icon(s, name, cx - isz / 2, cy - isz / 2, isz, white=True)


def header(s):
    s.shapes.add_picture(os.path.join(ASSETS, "logo.png"), Inches(0.85), Inches(0.30), height=Inches(0.74))
    tf = tb(s, MR - 4.2, 0.30, 4.2, 0.7, MSO_ANCHOR.TOP)
    para(tf, [R("CEPS", sz=13.5, b=True, c=INK)], align=PP_ALIGN.RIGHT, sa=0, ls=1.05, first=True)
    para(tf, [R("Veille du Journal officiel", sz=13.5, c=BODY)], align=PP_ALIGN.RIGHT, sa=0, ls=1.05)
    ln = s.shapes.add_connector(1, Inches(0.0), Inches(1.10), Inches(SW), Inches(1.10))
    ln.line.color.rgb = C(RULE); ln.line.width = Pt(0.75); _sans_style(ln)


def footer(s, n=None):
    tf = tb(s, 0.85, SH - 0.46, 8.0, 0.3)
    para(tf, [R("Veille JO, spécialités pharmaceutiques – " + DATE, sz=11, c=MENTION)], sa=0, first=True)
    if n is not None:
        tf2 = tb(s, MR - 0.8, SH - 0.46, 0.8, 0.3)
        para(tf2, [R(str(n), sz=11, c=MENTION)], align=PP_ALIGN.RIGHT, sa=0, first=True)


def title_block(s, runs, y=1.32, w=None, x=ML):
    tf = tb(s, x, y, (w or (MR - x)), 0.75, MSO_ANCHOR.TOP)
    para(tf, runs, sa=0, ls=1.02, first=True)
    return tf


def legende(s, x, y):
    """Légende du code couleur des acteurs, sur une ligne (positions fixes)."""
    items = [(BLUE, "machine", 0.80), (PERI, "IA", 0.44), (RED, "vous", 0.62)]
    for coul, lib, larg in items:
        rect(s, x, y + 0.045, 0.17, 0.17, fill=coul, rounded=True, radius=0.5)
        tf = tb(s, x + 0.24, y, larg, 0.26, MSO_ANCHOR.MIDDLE)
        para(tf, [R(lib, sz=11.5, c=BODY)], sa=0, first=True)
        x += 0.24 + larg + 0.16


# ============================================================
def build(out):
    prs = Presentation()
    prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)

    def notes(s, txt):
        s.notes_slide.notes_text_frame.text = txt

    # ---- 1. COUVERTURE ----
    s = slide(prs)
    s.shapes.add_picture(os.path.join(ASSETS, "logo.png"), Inches(0.85), Inches(0.30), height=Inches(0.74))
    tf = tb(s, MR - 4.2, 0.30, 4.2, 0.7)
    para(tf, [R("CEPS", sz=13.5, b=True, c=INK)], align=PP_ALIGN.RIGHT, sa=0, first=True)
    para(tf, [R("Comité économique des produits de santé", sz=13.5, c=BODY)], align=PP_ALIGN.RIGHT, sa=0)
    bx, by, bw, bh = 0.85, 1.35, 11.95, 5.75
    rect(s, bx, by, bw, bh, fill=BLUE)
    stw = 2.6; sth = stw * 540 / 910
    s.shapes.add_picture(os.path.join(ASSETS, "stripes.png"),
                         Inches(bx + bw - stw), Inches(by + bh - sth), width=Inches(stw), height=Inches(sth))
    s.shapes.add_picture(os.path.join(ASSETS, "sparkle.png"),
                         Inches(1.55), Inches(2.35), width=Inches(1.05), height=Inches(1.05))
    tf = tb(s, 1.5, 3.75, 10.8, 1.6)
    para(tf, [R("La veille JO automatisée", sz=42, b=True, c=WHITE)], sa=0, ls=1.0, first=True)
    para(tf, [R("Comment l'outil fonctionne", sz=42, b=True, c=WHITE)], sa=0, ls=1.0)
    tf = tb(s, 1.53, 5.65, 10.6, 0.9)
    para(tf, [R("Ce que fait la machine, ce que fait l'IA, ce qui reste entre vos mains :", sz=19, c=WHITE)], sa=0, first=True)
    para(tf, [R("garde-fous mis en place et choix à trancher", sz=19, c=WHITE)], sa=0)
    notes(s, "Support de restitution : fonctionnement de la veille JO automatisee, garde-fous, decisions en attente. "
             "Base : spec + contrat revise du 22/07/2026 (une ligne par presentation, PFHT, fusions), runs reels des 28/05 et 22/07/2026.")

    # ---- 2. LA CHAINE COMPLETE ----
    s = slide(prs); header(s); footer(s, 2)
    title_block(s, [R("Du JO publié au mail prêt à envoyer", sz=30, b=True, c=INK)])
    legende(s, 9.45, 1.44)

    etapes = [
        ("download-cloud-2", BLUE, "1. Extraction",
         "L'outil interroge l'API PISTE (Légifrance) : JO du jour, ou d'une date choisie via le fichier date.txt.",
         "107 textes le 28/05"),
        ("filter-3", BLUE, "2. Filtrage",
         "Seuls les titres à mots-clés pharma sont retenus ; chaque texte écarté reste tracé au journal.",
         "21 retenus, 86 écartés"),
        ("cpu", BLUE, "3. Analyse",
         "Type de texte, présentations (CIP), laboratoires, PFHT, taux et indications par section : cette lecture fait foi.",
         "sans IA"),
        ("sparkling-2", PERI, "4. Enrichissement IA",
         "L'IA recopie les indications des textes en prose libre ; les arrêtés structurés sont lus sans elle.",
         "débrayable"),
        ("git-merge", BLUE, "5. Rapprochement",
         "Une ligne par présentation (clé CIP) : Liste ← arrêtés, Prix (PFHT) ← avis, Taux ← décision UNCAM.",
         "39 lignes le 28/05"),
        ("file-excel-2", BLUE, "6. Livrables",
         "Excel + mail au gabarit : produit en nom + dosage, labo/indication/liste fusionnés par produit.",
         "Excel + mail"),
        ("user-3", RED, "7. Vous",
         "Relecture du brouillon, compléments sur les lignes « (à vérifier) », clic sur Envoyer.",
         "rien ne part sans vous"),
    ]
    y = 1.98
    pas = 0.715
    cx = ML + 0.31
    for i, (ic_, coul, titre, desc, chip) in enumerate(etapes):
        cy = y + 0.31
        if i < len(etapes) - 1:
            ln = s.shapes.add_connector(1, Inches(cx), Inches(cy + 0.26), Inches(cx), Inches(cy + pas - 0.26))
            ln.line.color.rgb = C(RULE); ln.line.width = Pt(1.4); _sans_style(ln)
        fond = CARD if coul == BLUE else (LAV if coul == PERI else "FFF4F4")
        rect(s, ML + 0.75, y, 8.35, 0.62, fill=fond, rounded=True, radius=0.12)
        node(s, ic_, cx, cy, dia=0.52, fill=coul)
        tf = tb(s, ML + 1.00, y, 7.95, 0.62, MSO_ANCHOR.MIDDLE)
        para(tf, [R(titre, sz=13, b=True, c=INK)], sa=1, ls=1.0, first=True)
        para(tf, [R(desc, sz=10.5, c=BODY)], sa=0, ls=1.0)
        rect(s, 9.45, y + 0.09, 2.95, 0.44, fill=None, line=coul, lw=1.0, rounded=True, radius=0.5)
        tfc = tb(s, 9.55, y + 0.09, 2.75, 0.44, MSO_ANCHOR.MIDDLE)
        para(tfc, [R(chip, sz=11, b=True, c=coul)], align=PP_ALIGN.CENTER, sa=0, first=True)
        y += pas
    notes(s, "Le pipeline en 7 temps. Chiffres du run reel du 28/05/2026 rejoue le 21/07 : 107 textes, 21 retenus, "
             "39 lignes (8 produits), zero timeout IA. Contrat revise le 22/07 : une ligne par presentation, PFHT, indications lues par section des arretes (deterministe). L'IA est debrayable : IA_ACTIVE=False.")

    # ---- 3. QUI FAIT QUOI ----
    s = slide(prs); header(s); footer(s, 3)
    title_block(s, [R("Qui fait quoi : trois rôles bien séparés", sz=30, b=True, c=INK)])
    cols = [
        (BLUE, "cpu", "La machine", "établit les faits",
         ["Présentations (CIP), laboratoires, PFHT et taux lus dans les tableaux du JO",
          "Indications des arrêtés recopiées par section ; listes et liens Légifrance",
          "Classement en sections, fusions par produit, Excel et mail"],
         "Ne devine jamais : donnée absente = « N/A » ou « à compléter »."),
        (PERI, "sparkling-2", "L'IA", "enrichit, sans décider",
         ["Recopie les indications des textes en prose libre : reformuler est interdit",
          "Confirme le type de texte ; n'oriente un avis de prix que si le texte le dit",
          "Chaque réponse est contrôlée (format strict, une seule relance)"],
         "En désaccord avec la machine, la machine gagne."),
        (RED, "user-3", "L'utilisatrice", "garde la décision",
         ["Relit le brouillon : aucun envoi automatique par défaut",
          "Complète les « (à vérifier) » grâce aux liens fournis sur chaque ligne",
          "Tranche les conventions métier (ex. avis de prix sans orientation)"],
         "L'outil prépare ; l'humain valide et envoie."),
    ]
    cw = (MR - ML - 2 * 0.30) / 3
    x = ML
    for coul, ic_, titre, soustitre, points, regle in cols:
        rect(s, x, 1.98, cw, 4.85, fill=CARD, rounded=True, radius=0.05)
        rect(s, x, 1.98, cw, 0.92, fill=coul, rounded=True, radius=0.05)
        rect(s, x, 2.55, cw, 0.35, fill=coul)  # masque les coins bas arrondis du bandeau
        icon(s, ic_, x + 0.22, 2.16, 0.44, white=True)
        tft = tb(s, x + 0.82, 2.06, cw - 1.0, 0.8, MSO_ANCHOR.MIDDLE)
        para(tft, [R(titre, sz=17, b=True, c=WHITE)], sa=1, ls=1.0, first=True)
        para(tft, [R(soustitre, sz=12, i=True, c=WHITE)], sa=0, ls=1.0)
        tf = tb(s, x + 0.26, 3.14, cw - 0.52, 2.6)
        for p_ in points:
            para(tf, [R("▪  ", sz=11, c=coul), R(p_, sz=12.5, c=INK)], sa=7, ls=1.08, bullet=True)
        tfr = tb(s, x + 0.26, 5.95, cw - 0.52, 0.75, MSO_ANCHOR.MIDDLE)
        para(tfr, [R(regle, sz=12, b=True, c=coul)], sa=0, ls=1.05, first=True)
        x += cw + 0.30
    notes(s, "Principe d'architecture : deterministe d'abord, IA en enrichissement. La machine fait foi sur les faits "
             "(produits, labos, taux, liens, classement). L'IA n'apporte que les indications et la levee d'ambiguites. "
             "L'utilisatrice garde l'envoi.")

    # ---- 4. INTEGRER OU ECARTER ----
    s = slide(prs); header(s); footer(s, 4)
    title_block(s, [R("Comment l'outil intègre, comment il écarte", sz=30, b=True, c=INK)])
    # Entonnoir a gauche (chiffres du 28/05)
    ex, ey = ML, 2.15
    niveaux = [
        (4.55, BLUE, "107 textes", "le JO complet du 28/05"),
        (3.45, BLUE, "21 textes", "spécialités pharmaceutiques"),
        (2.55, BLUE, "39 lignes", "8 produits, une ligne par présentation"),
    ]
    centre = ex + 4.55 / 2
    yy = ey
    for i, (w, coul, gros, lib) in enumerate(niveaux):
        rect(s, centre - w / 2, yy, w, 0.95, fill=(CARD2 if i < 2 else BLUE), rounded=True, radius=0.10)
        tf = tb(s, centre - w / 2, yy + 0.10, w, 0.75, MSO_ANCHOR.MIDDLE)
        c_txt = BLUE if i < 2 else WHITE
        para(tf, [R(gros, sz=21, b=True, c=c_txt)], align=PP_ALIGN.CENTER, sa=1, ls=1.0, first=True)
        para(tf, [R(lib, sz=11.5, c=(BODY if i < 2 else WHITE))], align=PP_ALIGN.CENTER, sa=0, ls=1.0)
        if i < 2:
            ln = s.shapes.add_connector(1, Inches(centre), Inches(yy + 0.95), Inches(centre), Inches(yy + 1.27))
            ln.line.color.rgb = C(PERI); ln.line.width = Pt(2.0); _sans_style(ln)
            te = ln.line._get_or_add_ln().makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'})
            ln.line._get_or_add_ln().append(te)
        yy += 1.32
    tf = tb(s, ex, yy + 0.12, 4.7, 0.9)
    para(tf, [R("Autant de lignes qu'au JO ; le « nom racine » relie les textes entre eux et regroupe visuellement les présentations d'un produit.",
                sz=11.5, i=True, c=MENTION)], sa=0, ls=1.1, first=True)

    # Regles d'ecartement a droite
    rx = 6.15
    regles = [
        ("Titre sans mot-clé pharma", "écarté, mais listé au journal : le tri reste auditable"),
        ("Donnée introuvable dans le texte", "« N/A » ou « à compléter », jamais de valeur devinée"),
        ("Réponse IA mal formée", "une seule relance, sinon on conserve la lecture machine"),
        ("Produit cité par l'IA, absent des tableaux du JO", "ignoré (constaté le 28/05 : EYLEA, VERZENIOS…)"),
        ("Hausse ou baisse supposée par l'IA sans appui textuel", "conjecture rejetée, l'avis reste « à orienter »"),
        ("Présentations multiples d'un même produit", "une ligne chacune, avec son PFHT ; laboratoire, indication et liste fusionnés visuellement"),
    ]
    tf = tb(s, rx, 1.98, MR - rx, 0.4)
    para(tf, [R("Ce qui est écarté, et pourquoi c'est sans risque", sz=15, b=True, c=INK)], sa=0, first=True)
    yy = 2.50
    for titre, det in regles:
        icon(s, "close-circle", rx, yy + 0.02, 0.26)
        tf = tb(s, rx + 0.40, yy, MR - rx - 0.40, 0.70)
        para(tf, [R(titre + " : ", sz=12.5, b=True, c=INK), R(det, sz=12.5, c=BODY)], sa=0, ls=1.05, first=True)
        yy += 0.73
    notes(s, "Gauche : l'entonnoir du 28/05 (107 -> 21 -> 8). Droite : les regles de rejet. Rien n'est ecarte en "
             "silence : journal pour le filtrage, recapitulatif d'anomalies dans le mail pour le reste.")

    # ---- 5. GARDE-FOUS ----
    s = slide(prs); header(s); footer(s, 5)
    title_block(s, [R("Les garde-fous en place", sz=30, b=True, c=INK)])
    cartes = [
        ("shield-check", "Jamais d'invention",
         ["Donnée absente = « N/A », jamais devinée (ni taux, ni prix, ni classement)",
          "Indications recopiées du JO, pas réécrites",
          "La lecture machine fait foi ; l'IA ne peut rien y ajouter"]),
        ("file-list-3", "Tout est visible",
         ["Suffixe « (à vérifier) » sur toute donnée douteuse",
          "Récapitulatif des anomalies dans le mail lui-même",
          "Journal de chaque exécution : retenus, écartés, rapprochements, appels IA"]),
        ("alarm-warning", "La veille ne s'arrête jamais",
         ["IA en panne → la veille sort ; les indications des arrêtés restent remplies (lues sans IA)",
          "Outlook absent → fichier HTML ; jour sans texte → mail « RAS »",
          "JO introuvable → alerte et relances (pas de mail = panne)"]),
        ("checkbox-circle", "L'envoi et les accès maîtrisés",
         ["Brouillon relu avant envoi : rien ne part automatiquement par défaut",
          "Clés d'accès dans un fichier local (.env), jamais dans le code",
          "API officielle PISTE, jamais d'aspiration du site Légifrance"]),
    ]
    cw = (MR - ML - 0.35) / 2
    ch = 2.34
    for i, (ic_, titre, points) in enumerate(cartes):
        x = ML + (i % 2) * (cw + 0.35)
        y = 1.98 + (i // 2) * (ch + 0.26)
        rect(s, x, y, cw, ch, fill=CARD, rounded=True, radius=0.06)
        node(s, ic_, x + 0.48, y + 0.44, dia=0.52, fill=BLUE)
        tf = tb(s, x + 0.92, y + 0.20, cw - 1.15, 0.5, MSO_ANCHOR.MIDDLE)
        para(tf, [R(titre, sz=16.5, b=True, c=BLUE)], sa=0, first=True)
        tf = tb(s, x + 0.30, y + 0.82, cw - 0.60, ch - 0.96)
        for p_ in points:
            para(tf, [R("▪  ", sz=10.5, c=PERI), R(p_, sz=12, c=INK)], sa=5, ls=1.05, bullet=True)
    notes(s, "Quatre familles de garde-fous, toutes constatees sur le run reel du 21/07 : entrees IA sans produit "
             "ecartees, conjecture d'orientation rejetee, repli HTML faute d'Outlook, anomalies recapitulees dans le mail.")

    # ---- 6. LES CHOIX A TRANCHER ----
    s = slide(prs); header(s); footer(s, 6)
    title_block(s, [R("Les choix à trancher pour la mise en service", sz=30, b=True, c=INK)])
    col_g = [
        ("Avis de prix sans orientation dans le texte",
         "Le JO ne dit ni hausse ni baisse (cas MORPHINE, FYCOMPA). Garder « Hausses (à vérifier) » ou créer une section « à orienter » ? Seul point qui bloque la conformité stricte à l'Excel cible.", True),
        ("Valider le format révisé du 22/07",
         "Une ligne par présentation, PFHT affiché, fusions par produit, indications recopiées mot pour mot : à confirmer sur les fichiers générés des 28/05 et 22/07.", True),
        ("LESSMR / LESMCO : fournir un exemple",
         "Ces catégories de liste ne correspondent à aucun arrêté connu de l'outil : un JO d'exemple suffit pour les brancher.", False),
        ("Forme du mail",
         "Brouillon Outlook prérempli, ou fichier HTML à copier-coller ?", False),
        ("Lancement quotidien et envoi",
         "Double-clic ou fichier date.txt, puis tâche 7 h 00 ; envoi auto après période de confiance.", False),
    ]
    col_d = [
        ("Quelle IA en production ?",
         "Albert (API de l'État : souveraine, gratuite) ou Mistral (payant). L'essai actuel (OpenRouter) traite les données hors de France : développement uniquement.", True),
        ("Flux réseau",
         "Ouverture DSI vers le fournisseur retenu (albert.api.etalab.gouv.fr ou api.mistral.ai).", False),
        ("Droits d'envoi",
         "Vérifier l'autorisation de poster sur la liste de diffusion SG_CEPS.", False),
        ("Sauvegarde du code",
         "GitLab interne, ou copie datée sur le partage réseau d'équipe.", False),
    ]
    cw = (MR - ML - 0.40) / 2

    def colonne(x, titre_col, items, coul):
        tf = tb(s, x, 1.95, cw, 0.4)
        para(tf, [R(titre_col, sz=16, b=True, c=coul)], sa=0, first=True)
        yy = 2.40
        for i, (titre, det, phare) in enumerate(items, 1):
            h = 0.66 + 0.34 * (len(det) > 95)
            rect(s, x, yy, cw, h, fill=(LAV if phare else CARD), rounded=True, radius=0.10)
            rect(s, x + 0.16, yy + 0.14, 0.34, 0.34, fill=coul, rounded=True, radius=0.5)
            tfn = tb(s, x + 0.16, yy + 0.14, 0.34, 0.34, MSO_ANCHOR.MIDDLE)
            para(tfn, [R(str(i), sz=13, b=True, c=WHITE)], align=PP_ALIGN.CENTER, sa=0, first=True)
            tf = tb(s, x + 0.64, yy + 0.075, cw - 0.82, h - 0.15, MSO_ANCHOR.MIDDLE)
            para(tf, [R(titre, sz=12.5, b=True, c=INK)], sa=1, ls=1.0, first=True)
            para(tf, [R(det, sz=10.5, c=BODY)], sa=0, ls=1.02)
            yy += h + 0.14
        return yy

    colonne(ML, "Côté métier (vous)", col_g, RED)
    yfin = colonne(ML + cw + 0.40, "Côté service et DSI", col_d, BLUE)
    tf = tb(s, ML + cw + 0.40, yfin + 0.05, cw, 0.8)
    para(tf, [R("Le détail opérationnel (questions exactes, commandes, critères) est tenu à jour dans ",
                sz=10.5, i=True, c=MENTION), R("veille_jo/nextSteps.md", sz=10.5, i=True, b=True, c=MENTION),
              R(".", sz=10.5, i=True, c=MENTION)], sa=0, ls=1.1, first=True)
    notes(s, "Deux familles de decisions : metier (utilisatrice) et service/DSI. Les deux points surlignes en lavande "
             "sont structurants : la convention d'orientation (bloque la recette stricte) et le fournisseur IA de production.")

    prs.save(out)
    print("OK :", out)


if __name__ == "__main__":
    build(os.path.join(HERE, "..", "presentation_veille_JO.pptx"))

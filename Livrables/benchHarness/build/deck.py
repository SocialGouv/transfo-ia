# -*- coding: utf-8 -*-
"""Benchmark harness de coding agentique - 4 stacks compares.
Charte DSFR Ministeres Sociaux (meme systeme que les decks Point d'etape IA).
3 slides : (1) matrice comparative 4x4, (2) couts externes vs internes,
(3) cas d'usage + recommandation.
Chiffres verifies sur sources primaires le 10/07/2026 (voir notes de chaque slide)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
IC = os.path.join(ASSETS, "ic")

# ---- Palette DSFR ----
INK="161616"; BODY="3A3A3A"; MENTION="6A6A6A"; BLUE="000091"; PERI="6A6AF4"
LAV="E3E3FD"; CARD="F5F5FE"; CARD2="ECECFE"; RED="E1000F"; GOLD="FFC800"
WHITE="FFFFFF"; RULE="DDDDDD"
GREEN="18753C"; AMBER="B85C00"; DOTOFF="D2D2E8"
MAR = "Marianne"
DATE = "17/07/2026"

SW, SH = 13.333, 7.5
ML = 0.85
MR = SW - 0.85

def C(h): return RGBColor.from_string(h)

def slide(prs, bg=WHITE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if bg:
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        r.fill.solid(); r.fill.fore_color.rgb = C(bg); r.line.fill.background()
        r.shadow.inherit = False
        sp = r._element; sp.getparent().remove(sp); s.shapes._spTree.insert(2, sp)
    return s

def rect(s, x, y, w, h, fill=None, line=None, lw=0.75, rounded=False, radius=0.06):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = C(fill)
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = C(line); shp.line.width = Pt(lw)
    if rounded:
        try: shp.adjustments[0] = radius
        except Exception: pass
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

def R(t, **k): k['t']=t; return k

def icon(s, name, x, y, size, white=False):
    suf = "_w" if white else ""
    s.shapes.add_picture(os.path.join(IC, f"{name}{suf}.png"),
                         Inches(x), Inches(y), width=Inches(size), height=Inches(size))

def header(s):
    s.shapes.add_picture(os.path.join(ASSETS,"logo.png"), Inches(0.85), Inches(0.30), height=Inches(0.74))
    tf = tb(s, MR-4.2, 0.30, 4.2, 0.7, MSO_ANCHOR.TOP)
    para(tf, [R("Secrétariat général", sz=13.5, b=True, c=INK)], align=PP_ALIGN.RIGHT, sa=0, ls=1.05, first=True)
    para(tf, [R("Direction du numérique", sz=13.5, c=BODY)], align=PP_ALIGN.RIGHT, sa=0, ls=1.05)
    ln = s.shapes.add_connector(1, Inches(0.0), Inches(1.10), Inches(SW), Inches(1.10))
    ln.line.color.rgb = C(RULE); ln.line.width = Pt(0.75)

def footer(s, n=None):
    tf = tb(s, 0.85, SH-0.46, 8.5, 0.3)
    para(tf, [R("Ministères Sociaux – Benchmark coding agentique – "+DATE, sz=11, c=MENTION)], sa=0, first=True)
    if n is not None:
        tf2 = tb(s, MR-0.8, SH-0.46, 0.8, 0.3)
        para(tf2, [R(str(n), sz=11, c=MENTION)], align=PP_ALIGN.RIGHT, sa=0, first=True)

def title_block(s, runs, y=1.36, w=None, x=ML):
    tf = tb(s, x, y, (w or (MR-x)), 1.0, MSO_ANCHOR.TOP)
    para(tf, runs, sa=0, ls=1.02, first=True)
    return tf

def subtitle(s, text, y=2.02):
    tf = tb(s, ML, y, MR-ML, 0.4)
    para(tf, [R(text, sz=14, c=BODY)], sa=0, first=True)

def dots(s, x, y, w, score, color):
    """5 pastilles ; 'score' pleines en couleur, le reste en gris clair."""
    tf = tb(s, x, y, w, 0.3, MSO_ANCHOR.MIDDLE)
    para(tf, [R("● " * score, sz=11.5, c=color), R("● " * (5-score), sz=11.5, c=DOTOFF)],
         align=PP_ALIGN.LEFT, sa=0, first=True)

def col_for(score):
    return GREEN if score>=4 else (AMBER if score==3 else RED)

# ============================================================
def build(out):
    prs = Presentation()
    prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)
    def notes(s, txt): s.notes_slide.notes_text_frame.text = txt

    # =========================================================
    # SLIDE 1 — MATRICE COMPARATIVE
    # =========================================================
    s = slide(prs); header(s); footer(s, 1)
    title_block(s, [R("Coding agentique : comparer 4 stacks", sz=30, b=True, c=INK)])
    subtitle(s, "Prix, performance, souveraineté, faisabilité. Tarifs vérifiés sur sources primaires (10/07/2026).")

    # --- geometrie de la grille ---
    labx = ML                 # colonne libelles critere
    labw = 2.15
    gx0 = ML + labw + 0.12    # debut colonnes solutions
    gap = 0.16
    ncol = 4
    colw = (MR - gx0 - (ncol-1)*gap) / ncol
    cxs = [gx0 + i*(colw+gap) for i in range(ncol)]
    hy = 2.38; hh = 0.70      # ligne d'entete
    ry0 = hy + hh + 0.12      # debut lignes
    rh = 0.78; rgap = 0.10

    # --- entetes de colonnes (les 4 solutions) ---
    cols = [
        ("Claude Code", "Opus 4.8", BLUE),
        ("OpenCode", "Albert · DeepSeek V4 Flash", PERI),
        ("OpenCode", "GLM 5.2 · OpenRouter", PERI),
        ("OpenCode", "DeepSeek V4 Pro · OR", PERI),
    ]
    for i,(a,b,cc) in enumerate(cols):
        rect(s, cxs[i], hy, colw, hh, fill=cc, rounded=True, radius=0.08)
        tf = tb(s, cxs[i]+0.08, hy, colw-0.16, hh, MSO_ANCHOR.MIDDLE)
        para(tf, [R(a, sz=13.5, b=True, c=WHITE)], align=PP_ALIGN.CENTER, sa=0, ls=1.0, first=True)
        para(tf, [R(b, sz=10, c="E3E3FD")], align=PP_ALIGN.CENTER, sa=0, sb=2, ls=1.0)

    # --- lignes (criteres) : (icone, libelle, [ (score, val_lignes) x4 ]) ---
    rows = [
        ("bank", "Prix", "/ 1M tokens", [
            (2, ["5 $ / 25 $", "+ siège 20–125 $/m"]),
            (5, ["Gratuit", "quotas, agents État"]),
            (4, ["≈1,40 $ / 4,40 $", ""]),
            (5, ["0,44 $ / 0,87 $", "tarif preview *"]),
        ]),
        ("code-s-slash", "Performance", "SWE-bench Verified", [
            (5, ["88,6 %", ""]),
            (4, ["≈79 % *", "via DeepSeek V4 Flash"]),
            (4, ["≈78 % *", "Term-Bench 81–83 %"]),
            (4, ["80,6 %", ""]),
        ]),
        ("shield-check", "Souveraineté", "éditeur / hébergement", [
            (2, ["Éditeur US", "CLOUD Act"]),
            (5, ["État FR", "SecNumCloud"]),
            (1, ["Éditeur CN", "+ routeur US"]),
            (1, ["Éditeur CN", "+ routeur US"]),
        ]),
        ("settings-3", "Faisabilité", "poste interne", [
            (4, ["Mac/Linux/Win natif", "outil mûr, admin. ent."]),
            (3, ["OpenAI-compat.", "agents État · quotas CI"]),
            (3, ["clé OpenRouter", "Mac/Linux/Win (WSL)"]),
            (3, ["clé OpenRouter", "Mac/Linux/Win (WSL)"]),
        ]),
    ]

    for r,(ic,lab,sub,cells) in enumerate(rows):
        ry = ry0 + r*(rh+rgap)
        rect(s, labx, ry, MR-labx, rh, fill=CARD, rounded=True, radius=0.05)
        icon(s, ic, labx+0.16, ry+(rh-0.40)/2, 0.40)
        tfl = tb(s, labx+0.70, ry, labw-0.72, rh, MSO_ANCHOR.MIDDLE)
        para(tfl, [R(lab, sz=14.5, b=True, c=INK)], sa=0, ls=1.0, first=True)
        para(tfl, [R(sub, sz=9.5, c=MENTION)], sa=0, sb=2, ls=1.0)
        for i,(score,vals) in enumerate(cells):
            cx = cxs[i]
            dots(s, cx+0.12, ry+0.10, colw-0.2, score, col_for(score))
            tfc = tb(s, cx+0.12, ry+0.38, colw-0.2, rh-0.42, MSO_ANCHOR.TOP)
            para(tfc, [R(vals[0], sz=11.5, b=True, c=INK)], align=PP_ALIGN.LEFT, sa=0, ls=1.0, first=True)
            if len(vals)>1 and vals[1]:
                para(tfc, [R(vals[1], sz=9.5, c=MENTION)], align=PP_ALIGN.LEFT, sa=0, sb=1, ls=1.0)

    # legende + note bas
    ly = ry0 + len(rows)*(rh+rgap) + 0.02
    tf = tb(s, ML, ly, MR-ML, 0.3)
    para(tf, [R("● ● ● ● ● ", sz=10.5, c=GREEN), R("favorable    ", sz=10, c=MENTION),
              R("● ● ● ", sz=10.5, c=AMBER), R("moyen    ", sz=10, c=MENTION),
              R("● ", sz=10.5, c=RED), R("défavorable", sz=10, c=MENTION),
              R("        * DeepSeek V4 : tarif preview (doublement « peak » mi-07/2026) ; GLM et Albert : perf estimée, catalogue Albert à confirmer.",
                sz=9.5, c=MENTION, i=True)], sa=0, first=True)

    notes(s, "Matrice comparative des 4 stacks de coding agentique. Chiffres verifies (sources primaires, 10/07/2026). "
             "PRIX/1M tokens : Opus 4.8 = 5$ input / 25$ output (platform.claude.com/docs/.../pricing), en sus des sieges "
             "Claude Code (Pro 17$, Team 20-25$, Premium 100-125$/mois - claude.com/pricing). DeepSeek V4 Pro = 0,435$/0,87$ "
             "(openrouter.ai/deepseek/deepseek-v4-pro + api-docs.deepseek.com) MAIS tarif preview, doublement 'peak' annonce "
             "mi-juillet 2026 (technode.com 30/06/2026). GLM 5.2 = tarif liste Z.ai 1,40$/4,40$ (docs.z.ai), OpenRouter varie "
             "0,93-3,00$ input selon fournisseur route (le 0,77$ lu en tete etait un artefact d'extraction, non confirme). "
             "Albert = GRATUIT pour agents de l'Etat, pas de facturation token, acces regule par quotas RPM/RPD/TPM (ia.numerique.gouv.fr). "
             "PERF SWE-bench Verified : Opus 4.8 88,6% (vellum.ai) ; DeepSeek V4 Pro 80,6% (morphllm) ; DeepSeek V4 Flash 79% ; "
             "Mistral Medium 3.5 77,6% (mistral.ai) ; GLM 5.2 ~78% estime (SWE-bench Pro 62,1%, Terminal-Bench 81-83% - huggingface zai-org). "
             "SCENARIO ALBERT retenu pour le bench elargi : OpenCode branche sur Albert servant DeepSeek V4 Flash (~79%) - "
             "catalogue Albert a confirmer via /v1/models. "
             "SOUVERAINETE : Anthropic = editeur US (CLOUD Act) ; Z.ai (GLM) et DeepSeek = editeurs chinois, et via OpenRouter le "
             "routage passe par un intermediaire US ; Albert = Etat francais, heberge sur Outscale SecNumCloud. Nuance : les poids "
             "GLM et DeepSeek sont ouverts (licence MIT), donc auto-hebergeables sur infra souveraine - c'est ce que fait Albert. "
             "FAISABILITE : Claude Code et OpenCode tournent tous deux sur Mac/Linux/Windows (WSL conseille sous Windows) ; le frein "
             "sur postes Windows internes est surtout la politique (Copilot only) et le proxy, pas la technique.")

    # =========================================================
    # SLIDE 2 — EXTERNES / INTERNES : DEUX LOGIQUES DE COUT
    # =========================================================
    s = slide(prs); header(s); footer(s, 2)
    title_block(s, [R("Externes, internes : qui paie quoi ?", sz=30, b=True, c=INK)])
    subtitle(s, "Le déploiement interne change l'équation économique de l'IA agentique.")

    cw = (MR-ML-0.5)/2; cy=2.40; chh=2.68
    # -- Carte A : prestataires externes --
    rect(s, ML, cy, cw, chh, fill=CARD, rounded=True, radius=0.05)
    icon(s, "briefcase", ML+0.34, cy+0.30, 0.5)
    tfa = tb(s, ML+1.0, cy+0.30, cw-1.2, 0.5, MSO_ANCHOR.MIDDLE)
    para(tfa, [R("Prestataires externes", sz=17, b=True, c=BLUE)], sa=0, first=True)
    tfa2 = tb(s, ML+0.36, cy+0.98, cw-0.7, 0.42)
    para(tfa2, [R("Abonnement Claude : un forfait mensuel", sz=15, b=True, c=INK)], sa=0, first=True)
    tl = tb(s, ML+0.36, cy+1.48, cw-0.7, chh-1.56)
    for i,(k) in enumerate([
        "Consommation incluse dans le forfait : coût prévisible et plafonné",
        "Rien à changer : l'outillage actuel reste valable",
    ]):
        para(tl, [R("▪  ", sz=12, c=PERI), R(k, sz=13, c=BODY)], sa=6, ls=1.08, bullet=True, first=(i==0))

    # -- Carte B : agents internes --
    rx = ML+cw+0.5
    rect(s, rx, cy, cw, chh, fill=CARD2, rounded=True, radius=0.05)
    icon(s, "government", rx+0.34, cy+0.30, 0.5)
    tfb = tb(s, rx+1.0, cy+0.30, cw-1.2, 0.5, MSO_ANCHOR.MIDDLE)
    para(tfb, [R("Agents internes", sz=17, b=True, c=BLUE)], sa=0, first=True)
    tfb2 = tb(s, rx+0.36, cy+0.92, cw-0.7, 0.56)
    para(tfb2, [R("≈ 20 € / siège / mois ", sz=15, b=True, c=INK),
                R("+ chaque token au prix du modèle", sz=15, b=True, c=RED)], sa=0, ls=1.05, first=True)
    tr = tb(s, rx+0.36, cy+1.62, cw-0.7, chh-1.7)
    for i,(k) in enumerate([
        "Sièges Claude Enterprise via Bedrock : la consommation s'ajoute au siège",
        "Le coût suit l'usage, et l'agentique consomme beaucoup de tokens",
    ]):
        para(tr, [R("▪  ", sz=12, c=PERI), R(k, sz=13, c=BODY)], sa=6, ls=1.08, bullet=True, first=(i==0))

    # -- Bandeau consequence --
    by = cy+chh+0.22; bh2 = 0.98
    rect(s, ML, by, MR-ML, bh2, fill=LAV, rounded=True, radius=0.06)
    icon(s, "focus-3", ML+0.30, by+(bh2-0.46)/2, 0.46)
    tfc = tb(s, ML+0.98, by+0.14, MR-ML-1.3, bh2-0.28, MSO_ANCHOR.MIDDLE)
    para(tfc, [R("Conséquence : ", sz=14.5, b=True, c=BLUE),
               R("pour les internes et la CI/CD, le coût au token devient le paramètre clé. "
                 "C'est l'objet du bench : identifier la stack au meilleur rapport performance / prix / souveraineté.",
                 sz=14.5, c=INK)], sa=0, ls=1.12, first=True)

    # -- Reperes tarifs --
    fy = by+bh2+0.18
    tf = tb(s, ML, fy, MR-ML, 0.3)
    para(tf, [R("Repères / 1M tokens (entrée / sortie) : ", sz=10.5, b=True, c=MENTION),
              R("Opus 4.8 : 5 $ / 25 $ · GLM 5.2 : 1,40 $ / 4,40 $ · DeepSeek V4 Pro : 0,44 $ / 0,87 $ · Albert (DeepSeek V4 Flash) : gratuit, quotas.",
                sz=10.5, c=MENTION)], sa=0, first=True)

    notes(s, "La problematique de deploiement : les prestataires externes peuvent rester sur leur abonnement Claude "
             "(forfait mensuel, consommation incluse, cout previsible). Les agents internes, eux, demarreront a "
             "environ 20 euros par siege et par mois (sieges Claude Enterprise via Bedrock), auxquels s'ajoute "
             "chaque token consomme, facture au prix du modele. Le cout interne suit donc l'usage, et l'usage "
             "agentique est intensif en tokens. Consequence : optimiser le cout au token (choix du modele, du "
             "harness, caching) devient le parametre cle pour les internes et pour la CI/CD - c'est ce que le bench "
             "compare, et ce que le bench elargi en conditions reelles validera (scenario Albert/DeepSeek via "
             "OpenCode face a Claude avec et sans abonnement).")

    # =========================================================
    # SLIDE 3 — CAS D'USAGE & RECOMMANDATION
    # =========================================================
    s = slide(prs); header(s); footer(s, 3)
    title_block(s, [R("Deux cas d'usage, deux logiques de coût", sz=30, b=True, c=INK)])
    subtitle(s, "Sur poste : abonnement (siège) ou clé. En CI/CD : paiement au token pour tous.")

    cw = (MR-ML-0.5)/2; cy=2.36; chh=2.18
    # -- Carte A : poste --
    rect(s, ML, cy, cw, chh, fill=CARD2, rounded=True, radius=0.05)
    icon(s, "terminal-box", ML+0.34, cy+0.28, 0.5)
    tfa = tb(s, ML+1.0, cy+0.28, cw-1.2, 0.5, MSO_ANCHOR.MIDDLE)
    para(tfa, [R("Code agentique sur poste", sz=17, b=True, c=BLUE)], sa=0, first=True)
    tl = tb(s, ML+0.36, cy+0.90, cw-0.7, chh-0.98)
    for i,(k,v) in enumerate([
        ("Claude Code", "siège 20–125 $/dev/mois"),
        ("OpenCode + OpenRouter", "clé, paiement au token"),
        ("OpenCode + Albert", "DeepSeek V4 Flash · clé agent État, gratuit"),
    ]):
        para(tl, [R("▪  ", sz=12, c=PERI), R(k+" : ", sz=13.5, b=True, c=INK), R(v, sz=13, c=BODY)],
             sa=6, ls=1.06, bullet=True, first=(i==0))
    # -- Carte B : CI/CD --
    rx = ML+cw+0.5
    rect(s, rx, cy, cw, chh, fill=CARD2, rounded=True, radius=0.05)
    icon(s, "settings-3", rx+0.34, cy+0.28, 0.5)
    tfb = tb(s, rx+1.0, cy+0.28, cw-1.2, 0.5, MSO_ANCHOR.MIDDLE)
    para(tfb, [R("Bots sur CI/CD", sz=17, b=True, c=BLUE)], sa=0, first=True)
    tr = tb(s, rx+0.36, cy+0.90, cw-0.7, chh-0.98)
    for i,(k,v) in enumerate([
        ("Au token pour tous", "pas de siège, clé API"),
        ("Tarifs / 1M", "Claude 5/25 · DeepSeek 0,44/0,87 · GLM 1,40/4,40"),
        ("Albert", "gratuit mais quotas 10–50 req/min"),
    ]):
        para(tr, [R("▪  ", sz=12, c=PERI), R(k+" : ", sz=13.5, b=True, c=INK), R(v, sz=13, c=BODY)],
             sa=6, ls=1.06, bullet=True, first=(i==0))

    # -- Bandeau reco (3 colonnes) --
    ry = cy+chh+0.16
    tf = tb(s, ML, ry, MR-ML, 0.34)
    para(tf, [R("Recommandation selon la priorité", sz=15, b=True, c=INK)], sa=0, first=True)
    ry2 = ry+0.42; rbh=1.42
    recos = [
        ("rocket", "Performance & maturité", "Claude Code / Opus 4.8",
         "88,6 % SWE-bench, outil mûr.", "Coûteux, éditeur US.", BLUE),
        ("government", "Souveraineté & coût", "Albert · DeepSeek V4 Flash",
         "Gratuit, SecNumCloud, ≈79 %.", "Réservé agents État.", GREEN),
        ("focus-3", "Rapport perf / prix", "DeepSeek V4 Pro / OR",
         "80,6 % pour ~0,9 $ / 1M.", "Éditeur CN, routeur US, preview.", AMBER),
    ]
    rcw = (MR-ML-2*0.4)/3
    for i,(ic,lab,sol,plus,minus,cc) in enumerate(recos):
        cx = ML+i*(rcw+0.4)
        rect(s, cx, ry2, rcw, rbh, fill=WHITE, line=cc, lw=1.4, rounded=True, radius=0.06)
        icon(s, ic, cx+0.26, ry2+0.20, 0.42)
        tfh = tb(s, cx+0.82, ry2+0.18, rcw-1.0, 0.5, MSO_ANCHOR.MIDDLE)
        para(tfh, [R(lab, sz=11.5, b=True, c=cc)], sa=0, ls=0.98, first=True)
        tft = tb(s, cx+0.26, ry2+0.72, rcw-0.5, rbh-0.80)
        para(tft, [R(sol, sz=13, b=True, c=INK)], sa=0, ls=1.0, first=True)
        para(tft, [R(plus+" ", sz=10, c=BODY), R(minus, sz=10, c=MENTION, i=True)], sa=0, sb=3, ls=1.08)

    # -- Reserves / a valider --
    fy = ry2+rbh+0.14
    tf = tb(s, ML, fy, MR-ML, 0.5)
    para(tf, [R("À valider : ", sz=10, b=True, c=MENTION),
              R("catalogue Albert à confirmer via /v1/models · DeepSeek V4 = tarif preview · tarifs OpenRouter = "
                "catalogue (caching −60/80 %) · tokenizer Opus 4.8 ≈ +30 % de tokens.", sz=10, c=MENTION, i=True)],
         sa=0, ls=1.08, first=True)

    notes(s, "Deux cas d'usage a distinguer. (1) CODE AGENTIQUE SUR POSTE : Claude Code se consomme via un SIEGE d'abonnement "
             "(Pro 17-20$, Team 20-25$, Premium 100-125$/dev/mois) ; les stacks OpenCode se consomment via une cle - OpenRouter "
             "(paiement au token) ou Albert (gratuit, cle reservee aux agents de l'Etat). (2) BOTS CI/CD : pas de siege, tout le "
             "monde paie au token via une cle API programmatique. Claude API Opus 4.8 = 5$/25$ par 1M (headless via ANTHROPIC_API_KEY ; "
             "un token OAuth d'abonnement CLAUDE_CODE_OAUTH_TOKEN est aussi possible mais Anthropic recommande la cle API pour "
             "l'automation partagee). DeepSeek V4 Pro 0,44$/0,87$, GLM 5.2 ~1,40$/4,40$ via OpenRouter. Albert est gratuit mais "
             "ses quotas (10-50 requetes/min en experimentation) peuvent brider un usage CI/CD intensif - a augmenter sur demande. "
             "RECOMMANDATION selon priorite : perf/maturite -> Claude/Opus 4.8 ; souverainete/cout -> Albert ; rapport perf-prix "
             "brut -> DeepSeek V4 Pro via OpenRouter. RESERVES : 'Open Claw' n'a pas ete confirme comme outil de coding (le seul "
             "depot de ce nom est un assistant de messagerie) - candidats reels : OpenCode, Crush (Charmbracelet), Claude Code "
             "Router. Le catalogue Albert observe sur les docs publiques ne liste pas DeepSeek V4 Flash ni Mistral Medium 3.5 "
             "(mais Mistral-Small, Ministral-3-8B, gpt-oss-120b, Qwen3-Coder) - a confirmer via un appel authentifie /v1/models "
             "sur ta cle. Tarifs OpenRouter = prix catalogue variables selon le fournisseur route ; le prompt caching peut baisser "
             "le cout reel de 60 a 80%. Le nouveau tokenizer d'Opus 4.8 produit ~30% de tokens en plus pour un meme texte, ce qui "
             "renforce le cout effectif par requete.")

    prs.save(out)
    print("OK ->", os.path.basename(out), "|", len(list(prs.slides)), "slides")

if __name__ == "__main__":
    build(os.path.join(HERE, "..", "Bench_Coding-Agentique.pptx"))

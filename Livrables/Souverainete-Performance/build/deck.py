# -*- coding: utf-8 -*-
"""Souveraineté et performance des modèles et harness - charte Ippon.
5 slides : titre, souveraineté vs conformité (CLOUD Act, SecNumCloud), matrice bench 7 stacks,
ce que mesurent les 3 benchs, ce qui booste les modèles (harness, pratiques, orchestration).
Chiffres du bench : ceux vérifiés le 02/09/2026 (Livrables/benchHarness, SVG 06-bench)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONT = "Montserrat"
DATE = "Septembre 2026"

# ---- palette Ippon (même système que le deck "Ce que j'apporte") ----
ROYAL = "002FA7"; NAVY = "0B1437"; GOLD = "E8B62E"; OCHRE = "B5862A"
GREEN = "217C64"; TERRA = "BF482D"
INK = "1B2233"; SLATE = "4A5162"; MUTED = "9AA0B0"
HAIR = "E6E8F1"; WHITE = "FFFFFF"
LAV = "EEF1FB"; MINT = "E7F3EE"; PEACH = "F8ECE7"; CREAM = "F6EFDB"; GREY = "F3F4F7"
ACCENT = {"blue": (ROYAL, LAV), "green": (GREEN, MINT), "terra": (TERRA, PEACH), "ochre": (OCHRE, CREAM)}

SW, SH = 13.333, 7.5
ML = 0.625; MR = SW - ML; CW_FULL = MR - ML

def C(h): return RGBColor.from_string(h)

def new_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = C(WHITE)
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

def oval(s, x, y, d, fill, line=None):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.shadow.inherit = False
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = C(fill)
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = C(line); shp.line.width = Pt(1.5)
    return shp

def tb(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf

def R(t, **k): k["t"] = t; return k

def hang(p, marL=0.2):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(marL))); pPr.set("indent", str(-Inches(marL)))

def para(tf, runs, align=PP_ALIGN.LEFT, sa=0, sb=0, ls=1.08, first=False, bullet=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align; p.space_after = Pt(sa); p.space_before = Pt(sb); p.line_spacing = ls
    if bullet: hang(p)
    for rr in runs:
        r = p.add_run(); r.text = rr["t"]; f = r.font
        f.name = FONT; f.size = Pt(rr.get("sz", 13)); f.bold = rr.get("b", False)
        f.italic = rr.get("i", False); f.color.rgb = C(rr.get("c", INK))
    return p

def icon(s, name, x, y, d=0.6):
    s.shapes.add_picture(os.path.join(ASSETS, f"{name}.png"), Inches(x), Inches(y), Inches(d), Inches(d))

def brand(s, h=0.40, x=None, y=0.42):
    from PIL import Image
    im = Image.open(os.path.join(ASSETS, "logo.png")); ar = im.size[0] / im.size[1]
    w = h * ar
    s.shapes.add_picture(os.path.join(ASSETS, "logo.png"), Inches(MR - w if x is None else x), Inches(y), Inches(w), Inches(h))

def footer(s, page):
    ln = rect(s, ML, 6.84, CW_FULL, 0.0153, fill=HAIR)
    tf = tb(s, ML, 6.90, 10, 0.3)
    para(tf, [R("ippon", sz=10.5, b=True, c=SLATE),
              R("   ·   Souveraineté et performance des modèles et harness — Secrétariat général des Ministères sociaux (DNUM)", sz=10.5, c=MUTED)],
         first=True, ls=1.0)
    tf2 = tb(s, 11.5, 6.90, 1.208, 0.3)
    para(tf2, [R(f"{page:02d}", sz=11, b=True, c=MUTED)], align=PP_ALIGN.RIGHT, first=True, ls=1.0)

def header(s, eyebrow, title, sub):
    tf = tb(s, ML, 0.50, 10, 0.32)
    para(tf, [R(eyebrow.upper(), sz=12.5, b=True, c=OCHRE)], first=True, ls=1.0)
    tf = tb(s, ML - 0.02, 0.80, 11.4, 0.8)
    para(tf, [R(title, sz=27, b=True, c=ROYAL)], first=True, ls=1.04)
    tf = tb(s, ML, 1.62, 11.2, 0.4)
    para(tf, [R(sub, sz=14, c=SLATE)], first=True, ls=1.1)

def card(s, x, y, w, h, acc_key, ic, tag, title, tint_override=None):
    acc, tint = ACCENT[acc_key]
    box = rect(s, x, y, w, h, fill=tint_override or tint, rounded=True, radius=0.085)
    bar = rect(s, x, y + 0.12, 0.055, h - 0.24, fill=acc, rounded=True, radius=0.5)
    d = 0.56
    if ic: icon(s, ic, x + 0.28, y + 0.26, d)
    tx = x + 0.28 + (d + 0.18 if ic else 0)
    tf = tb(s, tx, y + 0.27, w - (tx - x) - 0.24, 0.8)
    para(tf, [R(tag.upper(), sz=10, b=True, c=acc)], first=True, ls=1.0)
    para(tf, [R(title, sz=16.5, b=True, c=INK)], sb=2, ls=1.02)
    return box

def bullets(s, x, y, w, h, items, sz=12, sa=5, dot=SLATE):
    tf = tb(s, x, y, w, h)
    for i, it in enumerate(items):
        runs = [R("▪  ", sz=sz - 1, c=dot)]
        if isinstance(it, str): runs.append(R(it, sz=sz, c=SLATE))
        else:
            for k, (t, b) in enumerate(it): runs.append(R(t, sz=sz, b=b, c=INK if b else SLATE))
        para(tf, runs, sa=sa, ls=1.12, first=(i == 0), bullet=True)
    return tf

def notes(s, txt): s.notes_slide.notes_text_frame.text = txt

# =====================================================================
def build(out):
    prs = Presentation(); prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)

    # ------------------------------------------------------------------
    # SLIDE 0 - TITRE
    # ------------------------------------------------------------------
    s = new_slide(prs)
    # décor : cercles concentriques à droite (style couverture Ippon)
    for d, col in ((6.0, LAV), (3.8, "DCE3F7"), (3.0, ROYAL), (1.7, GOLD)):
        oval(s, 10.1 - d / 2 + 2.6, 3.75 - d / 2 + 0.2, d, col)
    brand(s, h=0.55, x=ML, y=0.62)
    tf = tb(s, ML, 2.15, 8.3, 0.35)
    para(tf, [R("CLIENT  ·  SECRÉTARIAT GÉNÉRAL DES MINISTÈRES SOCIAUX — DNUM", sz=12, b=True, c=OCHRE)], first=True)
    tf = tb(s, ML, 2.65, 8.4, 2.2)
    para(tf, [R("Souveraineté et performance", sz=40, b=True, c=ROYAL)], first=True, ls=1.02)
    para(tf, [R("des modèles et des harness", sz=40, b=True, c=ROYAL)], ls=1.02)
    tf = tb(s, ML, 4.55, 8.2, 0.9)
    para(tf, [R("Ce que « souverain » et « conforme » veulent dire, ce que mesure le bench, "
                "et ce qui fait réellement la performance d'un agent de code.", sz=15.5, c=SLATE)], first=True, ls=1.15)
    rect(s, ML, 5.75, 3.2, 0.03, fill=GOLD)
    tf = tb(s, ML, 5.9, 8, 0.4)
    para(tf, [R("Coding agentique  ·  ", sz=12.5, c=SLATE), R(DATE, sz=12.5, b=True, c=SLATE)], first=True)
    notes(s, "Deck Ippon - accompagnement transfo IA des ministères sociaux. Chiffres du bench vérifiés le 02/09/2026 "
             "(sources détaillées dans Livrables/benchHarness/build/deck.py, notes du slide 1).")

    # ------------------------------------------------------------------
    # SLIDE 1 - SOUVERAINETÉ vs CONFORMITÉ
    # ------------------------------------------------------------------
    s = new_slide(prs); brand(s)
    header(s, "Cadre  ·  deux questions distinctes",
           "Souverain n'est pas synonyme de conforme",
           "La conformité protège les données personnelles ; la souveraineté protège de l'accès d'un État tiers.")

    cy = 2.02; ch = 2.54; gap = 0.24; cw = (CW_FULL - gap) / 2
    # Souveraineté
    card(s, ML, cy, cw, ch, "terra", "agentic", "Souveraineté  ·  qui peut exiger l'accès ?", "Une question de juridiction")
    bullets(s, ML + 0.34, cy + 0.98, cw - 0.6, ch - 1.05, [
        [("Critère : ", True), ("le droit applicable à l'opérateur et à ses maisons mères, pas l'adresse des serveurs. "
                              "Un acteur US en région UE reste soumis au droit US (lecture CNIL) : Bedrock, Vertex AI ou Azure, même à Paris.", False)],
        [("Tiennent : ", True), ("Albert et Outscale LLMaaS (SecNumCloud 3.2) ; Scaleway et OVHcloud AI Endpoints (cloud FR, hors périmètre SecNumCloud).", False)],
        [("Mistral : ", True), ("éditeur français, mais La Plateforme a tourné sur Azure et Google Cloud. Souverain via Outscale ou en poids ouverts auto-hébergés.", False)],
    ], sz=10.5)
    # Conformité
    x2 = ML + cw + gap
    card(s, x2, cy, cw, ch, "blue", "cdp", "Conformité  ·  les données sont-elles traitées légalement ?", "Une question de RGPD")
    bullets(s, x2 + 0.34, cy + 0.98, cw - 0.6, ch - 1.05, [
        [("Critère : ", True), ("base légale, contrat de sous-traitance (DPA), sécurité, transferts hors UE encadrés.", False)],
        [("Atteignable avec un acteur US : ", True), ("Bedrock en région UE avec le DPA AWS est conforme RGPD ; même logique pour Vertex AI en région UE.", False)],
        [("Insuffisante : ", True), ("OpenRouter, routage par un intermédiaire US sans garanties UE.", False)],
    ], sz=10.5)

    # Bandeaux CLOUD Act / SecNumCloud
    by = cy + ch + 0.08; bh = 1.47
    rect(s, ML, by, cw, bh, fill=GREY, rounded=True, radius=0.07)
    tf = tb(s, ML + 0.3, by + 0.2, cw - 0.6, bh - 0.3)
    para(tf, [R("CLOUD ACT (ÉTATS-UNIS, 2018)  ", sz=10, b=True, c=TERRA), R("+ FISA 702", sz=10, b=True, c=MUTED)], first=True)
    para(tf, [R("Les fournisseurs soumis au droit US doivent remettre les données aux autorités américaines, "
                "où qu'elles soient stockées. ", sz=11, c=SLATE),
              R("La localisation ne protège pas.", sz=11, b=True, c=INK)], sb=4, ls=1.1)
    para(tf, [R("Transferts UE-US (DPF, 2023) : validé en première instance le 03/09/2025, pourvoi pendant devant la CJUE (C-703/25 P).", sz=9.5, c=MUTED)], sb=4, ls=1.08)
    rect(s, x2, by, cw, bh, fill=GREY, rounded=True, radius=0.07)
    tf = tb(s, x2 + 0.3, by + 0.2, cw - 0.6, bh - 0.3)
    para(tf, [R("SECNUMCLOUD 3.2 (ANSSI)  ", sz=10, b=True, c=GREEN), R("référentiel du « cloud de confiance »", sz=10, b=True, c=MUTED)], first=True)
    para(tf, [R("Qualification de sécurité + critères d'immunité aux lois extraterritoriales : ", sz=11, c=SLATE),
              R("siège et capital dans l'UE, données, clés et administration en UE, personnel habilité.", sz=11, b=True, c=INK)], sb=4, ls=1.1)
    para(tf, [R("Doctrine « cloud au centre » : données sensibles sur cloud qualifié. Qualifiés : Outscale (héberge Albert), OVHcloud (IaaS), "
                "S3NS (Thales-Google) depuis 12/2025.", sz=9.5, c=MUTED)], sb=4, ls=1.08)

    # take-away
    ty = by + bh + 0.06
    tf = tb(s, ML, ty, CW_FULL, 0.6, MSO_ANCHOR.MIDDLE)
    para(tf, [R("À retenir  ", sz=12.5, b=True, c=ROYAL),
              R("Bedrock, Vertex AI ou Azure : conformes, non souverains. Albert, Outscale, Scaleway, OVHcloud : les deux. OpenRouter : ni l'un ni l'autre. "
                "Le référencement UGAP (AWS et Google Cloud y figurent comme Outscale ou OVHcloud) est un canal d'achat, pas un label de souveraineté.", sz=12, c=INK)], first=True, ls=1.1)
    footer(s, 1)
    notes(s, "Souveraineté au sens CNIL : ce qui compte est la juridiction de l'opérateur (et de ses maisons mères), pas la région "
             "d'hébergement. AWS reste soumis au CLOUD Act (2018) quelle que soit la région : Bedrock n'est donc jamais souverain, "
             "même à Paris. Conformité RGPD : axe distinct ; Bedrock région UE + DPA AWS est conforme ; OpenRouter insuffisant.\n"
             "CLOUD Act : loi US de 2018 ; les fournisseurs soumis au droit US doivent remettre les données sur demande des autorités US, "
             "quelle que soit la localisation. FISA 702 : surveillance des non-Américains. Sources : LexisNexis 'Cloud Act et RGPD' ; "
             "LeMagIT 'CLOUD Act : quels risques pour les clients européens'.\n"
             "DPF (Data Privacy Framework, décision d'adéquation de juillet 2023) : recours Latombe rejeté par le Tribunal de l'UE le "
             "03/09/2025 (T-553/23) ; pourvoi devant la CJUE déposé le 31/10/2025 (C-703/25 P), pas de date d'audience connue "
             "(IAPP ; EDPL 2026/1).\n"
             "SecNumCloud 3.2 (ANSSI, 2022) : exigences techniques + critères d'immunité aux lois extraterritoriales : prestataire et "
             "maisons mères établis dans l'UE, contrôle du capital, données/métadonnées/journaux/clés en UE, administration depuis l'UE, "
             "administrateurs habilités. Nuance : protection documentée et contractualisée, pas une neutralisation du droit US "
             "(CIO-Online 'SecNumCloud, une protection contre le droit extraterritorial, pas une garantie absolue'). Doctrine "
             "'cloud au centre' (circulaires 2021/2023) : données sensibles sur offre qualifiée SecNumCloud. Albert (DINUM) : "
             "hébergé sur Outscale (Dassault Systèmes), qualifié SecNumCloud 3.2.\n"
             "VÉRIFICATIONS DU 03/09/2026 (demande Selim) : "
             "OUTSCALE : LLMaaS = modèles Mistral (Small 3.1, Codestral, Ministral 8B, Medium, Embed) servis sur la région SecNumCloud 3.2 "
             "(blog.outscale.com ; Le Monde Informatique) : souverain, tient. "
             "OVHCLOUD : entreprise française, AI Endpoints hébergé en France (Gravelines) ; SecNumCloud obtenu sur Bare Metal Pod, VMware on OVHcloud "
             "et 'SNC Cloud Platform' (calcul, stockage, réseau ; annonce du 01/09/2026, LeMagIT) mais AI Endpoints n'est PAS dans le périmètre qualifié "
             "(intégration des services IA à la stack SecNumCloud annoncée pour fin 2026). Statut = même niveau que Scaleway : cloud FR hébergé UE, "
             "pas SecNumCloud. "
             "MISTRAL : éditeur français (siège Paris), mais La Plateforme a fonctionné 'exclusivement' sur des clouds tiers, Microsoft Azure, "
             "Google Cloud et CoreWeave, jusqu'à la mise en service du datacenter de Bruyères-le-Châtel (fin août 2026, 2 048 GPU ; Calipia 30/03/2026, "
             "Usine Digitale 07/2026) ; la liste des sous-traitants (trust.mistral.ai/subprocessors) n'a pas pu être lue (page dynamique) : la part "
             "encore servie depuis Azure/GCP est inconnue à ce jour. Accord Microsoft de juillet 2026 : plusieurs milliards, Mistral dans Azure AI "
             "Foundry et Azure Local, sans nouvelle prise de participation (SFEIR). Verdict : Mistral n'est pas listé comme voie souveraine EN TANT QUE "
             "SERVICE ; il le devient via Outscale LLMaaS (SecNumCloud) ou en auto-hébergement des poids ouverts (Scaleway/OVH le servent aussi). "
             "VERCEL / UGAP : aucune trace d'un référencement Vercel à l'UGAP (recherches du 03/09/2026) ; Vercel AI Gateway est un routeur US "
             "comparable à OpenRouter, donc non souverain de toute façon. Probable confusion avec VERTEX AI (Google) : accessible via le marché UGAP "
             "cloud IaaS/PaaS porté par Capgemini, qui référence AWS, Google Cloud, Microsoft Azure, Oracle, IBM (cloud 'générique') aux côtés "
             "d'Outscale, OVHcloud, Scaleway, Cloud Temple (cloud 'de confiance') ; AWS y est acheté via Capgemini (pages.awscloud.com/france-ugap-portail). "
             "L'UGAP est un canal d'achat : être référencé ne dit rien de la souveraineté. Vertex AI en direct chez Google = même statut que Bedrock "
             "(US, CLOUD Act, conforme RGPD en région UE). Voie souveraine annoncée : S3NS (Thales majoritaire + Google), qualifié SecNumCloud 3.2 le "
             "17/12/2025, 'Vertex AI Foundations' sur la feuille de route du second semestre 2026 (Futurum Group) : à surveiller, pas disponible.")

    # ------------------------------------------------------------------
    # SLIDE 2 - MATRICE BENCH
    # ------------------------------------------------------------------
    s = new_slide(prs); brand(s)
    header(s, "Bench  ·  7 stacks de coding agentique",
           "Performance, prix, souveraineté, conformité",
           "Trois mesures de performance, prix / 1M tokens, souveraineté (CNIL), conformité RGPD · vérifié le 02/09/2026.")

    cols = [  # (label, sub, width)
        ("Harness · modèle", "fournisseur", 3.05),
        ("DeepSWE v1.1", "modèle seul · principal", 1.4),
        ("Terminal-Bench 2.1", "agentique", 1.55),
        ("SWE-bench Verified", "baseline · saturé", 1.5),
        ("Prix / 1M tokens", "entrée · sortie", 1.4),
        ("Souveraineté", "au sens CNIL", 1.6),
        ("Conformité", "RGPD / données", CW_FULL - (3.05 + 1.4 + 1.55 + 1.5 + 1.4 + 1.6)),
    ]
    xs = []; x = ML
    for _, _, w in cols: xs.append(x); x += w
    hy = 2.0; hh = 0.48
    rect(s, ML, hy, CW_FULL, hh, fill=NAVY, rounded=True, radius=0.12)
    for i, (lab, sub, w) in enumerate(cols):
        tf = tb(s, xs[i] + 0.14, hy, w - 0.2, hh, MSO_ANCHOR.MIDDLE)
        para(tf, [R(lab, sz=9.5, b=True, c=WHITE)], first=True, ls=1.0)
        para(tf, [R(sub, sz=8, c="B8C0DA")], ls=1.0, sb=1)

    RED_ = TERRA; OK_ = GREEN; AMB_ = OCHRE
    rows = [
        # harness, modèle, provider, deepswe(main, sub), tb(main, sub), swev(main, sub), prix(in,out), souv(color, lab, sub), conf(color, lab, sub)
        ("Claude Code", "Opus 5", "AWS Bedrock", ("74,0 %", "±4"), ("89,1 % *", ""), ("96,0 %ᵛ", "97,0 % *"), ("5 $", "25 $"),
         (RED_, "Non souveraine", "CLOUD Act"), (OK_, "Bonne", "région UE · DPA AWS")),
        ("Claude Code", "Fable 5", "AWS Bedrock", ("70,0 %", "±4"), ("83,8 %", "±1,2 · officiel"), ("95,0 %ᵛ", ""), ("10 $", "50 $"),
         (RED_, "Non souveraine", "CLOUD Act"), (OK_, "Bonne", "région UE · DPA AWS")),
        ("OpenCode", "Kimi K3", "OpenRouter", ("≈69 %", ""), ("88,3 %ᵛ", "80,9 % *"), ("93,4 % *", ""), ("2,55 $", "12,75 $"),
         (RED_, "Non souveraine", "CN + routeur US"), (RED_, "Insuffisante", "sans garanties UE")),
        ("Claude Code", "Sonnet 5", "AWS Bedrock", ("54 %", "±4"), ("80,4 %ᵛ", "74,6 % officiel"), ("85,2 %", "llm-stats"), ("2 $", "10 $"),
         (RED_, "Non souveraine", "CLOUD Act"), (OK_, "Bonne", "région UE · DPA AWS")),
        ("OpenCode", "DeepSeek V4 Flash 0731", "Scaleway", ("53 %", "54,4 %ᵛ"), ("82,7 %ᵛ", ""), ("non publié", ""), ("0,40 €", "0,80 €"),
         (OK_, "Souveraine (UE)", "cloud FR · hébergé UE"), (OK_, "Bonne", "RGPD · cloud FR")),
        ("OpenCode", "GLM 5.2", "Scaleway", ("44,0 %", ""), ("81,0 %ᵛ", ""), ("non publié", ""), ("1,80 €", "5,50 €"),
         (OK_, "Souveraine (UE)", "cloud FR · hébergé UE"), (OK_, "Bonne", "RGPD · cloud FR")),
        ("OpenCode", "DeepSeek V4 Flash preview", "Albert (DINUM) · checkpoint à confirmer", ("7,3 %ᵛ", ""), ("61,8 %ᵛ", ""), ("73,7 %ᵛ", ""), ("gratuit", "agents État"),
         (OK_, "Souveraine", "SecNumCloud · État FR"), (OK_, "Bonne", "cadre État")),
    ]
    ry = hy + hh + 0.08; rh = 0.5; rg = 0.05
    for r, (hn, md, pv, ds, tbv, sv, px, sov, cf) in enumerate(rows):
        y = ry + r * (rh + rg)
        rect(s, ML, y, CW_FULL, rh, fill=(LAV if r % 2 == 0 else WHITE), line=(None if r % 2 == 0 else HAIR), rounded=True, radius=0.1)
        # stack
        tf = tb(s, xs[0] + 0.14, y, cols[0][2] - 0.2, rh, MSO_ANCHOR.MIDDLE)
        para(tf, [R(hn + "  ·  ", sz=10, b=True, c=ROYAL), R(md, sz=10, b=True, c=INK)], first=True, ls=1.0)
        para(tf, [R(pv, sz=8.5, c=MUTED)], ls=1.0, sb=1)
        # perf cells
        for ci, (main, sub), grey in ((1, ds, False), (2, tbv, False), (3, sv, True)):
            tf = tb(s, xs[ci] + 0.14, y, cols[ci][2] - 0.2, rh, MSO_ANCHOR.MIDDLE)
            col = MUTED if grey or main == "non publié" else INK
            para(tf, [R(main, sz=11 if ci == 1 else 10.5, b=(ci == 1 and main != "non publié"), c=col, i=(main == "non publié"))], first=True, ls=1.0)
            if sub: para(tf, [R(sub, sz=8.5, c=MUTED)], ls=1.0, sb=1)
        # prix
        tf = tb(s, xs[4] + 0.14, y, cols[4][2] - 0.2, rh, MSO_ANCHOR.MIDDLE)
        para(tf, [R(px[0], sz=10.5, b=True, c=INK), R("  ·  " + px[1], sz=10.5, c=SLATE) if px[1] and px[1] != "agents État" else R("", sz=8)], first=True, ls=1.0)
        if px[1] == "agents État": para(tf, [R(px[1], sz=8.5, c=MUTED)], ls=1.0, sb=1)
        # souveraineté / conformité
        for ci, (colr, lab, sub) in ((5, sov), (6, cf)):
            oval(s, xs[ci] + 0.14, y + 0.13, 0.13, colr)
            tf = tb(s, xs[ci] + 0.34, y, cols[ci][2] - 0.42, rh, MSO_ANCHOR.MIDDLE)
            para(tf, [R(lab, sz=10, b=True, c=colr)], first=True, ls=1.0)
            para(tf, [R(sub, sz=8, c=MUTED)], ls=1.0, sb=1)

    ly = ry + len(rows) * (rh + rg) + 0.02
    tf = tb(s, ML, ly, CW_FULL, 0.25)
    para(tf, [R("Sans marque = officiel  ·  ᵛ auto-rapporté par l'éditeur  ·  * mesure indépendante (vals.ai, Artificial Analysis)  ·  "
                "llm-stats = agrégat non re-mesuré  ·  aucun chiffre estimé : sans donnée, « non publié »", sz=9, c=MUTED, i=True)], first=True, ls=1.0)
    footer(s, 2)
    notes(s, "Reprise à l'identique de la matrice du bench (SVG 06-bench et Livrables/benchHarness, fact-check du 02/09/2026). "
             "DeepSWE v1.1 : leaderboard officiel Datacurve, harness fixé mini-swe-agent (Opus 5 74,0 ±4 ; Fable 5 70,0 ±4 ; Kimi K3 ≈69 ; "
             "Sonnet 5 54 ±4 ; DeepSeek 0731 53 (54,4 auto-rapporté) ; GLM 5.2 44,0 ; preview 7,3 auto-rapporté, absente du leaderboard). "
             "Terminal-Bench 2.1 : Opus 5 89,1 = mesure Artificial Analysis (Terminus 2), pas officiel ; Fable 5 83,8 ±1,2 officiel "
             "(Claude Code xhigh ; 80,4 avec Terminus 2) ; Kimi 88,3 auto-rapporté (vals.ai 80,9) ; Sonnet 5 80,4 annonce (74,6 officiel) ; "
             "0731 82,7 ; GLM 81,0 ; preview 61,8 (auto-rapportés). SWE-bench Verified (baseline grisée) : Opus 5 96,0 annonce + 97,0 vals.ai ; "
             "Fable 95,0 annonce ; Kimi 93,4 vals.ai ; Sonnet 85,2 agrégat llm-stats ; preview 73,7 rapport technique ; GLM et 0731 non publié. "
             "Prix : tarifs publics du 02/09/2026 ; Scaleway en euros (tarifs communiqués par le client) ; Albert gratuit pour les agents de l'État "
             "(quotas). Souveraineté (CNIL) : Bedrock non souverain (CLOUD Act, quelle que soit la région) ; Albert (SecNumCloud) et Scaleway "
             "(cloud FR, hébergé UE) souverains ; OpenRouter : éditeur chinois + routeur US. Conformité RGPD : Bedrock région UE + DPA AWS bonne ; "
             "Scaleway et Albert bonnes ; OpenRouter insuffisante. Piège DeepSeek : Scaleway sert le checkpoint 0731, Albert a priori la preview "
             "d'avril (à confirmer auprès de la DINUM) ; même nom, performances agentiques sans rapport.")

    # ------------------------------------------------------------------
    # SLIDE 3 - CE QUE MESURENT LES 3 BENCHS
    # ------------------------------------------------------------------
    s = new_slide(prs); brand(s)
    header(s, "Lecture  ·  trois mesures, trois questions",
           "Ce que mesurent les trois benchmarks",
           "Un score n'a de sens qu'avec sa question : le modèle seul, le couple modèle × harness, ou un repère historique.")

    cy = 2.02; ch = 3.6; gap = 0.22; cw = (CW_FULL - 2 * gap) / 3
    specs = [
        ("blue", "bench", "Principal  ·  le modèle seul", "DeepSWE v1.1",
         [[("Quoi : ", True), ("des tâches d'ingénierie logicielle réelles, résolues de bout en bout par l'agent.", False)],
          [("Comment : ", True), ("harness fixé pour tous (mini-swe-agent), leaderboard officiel Datacurve, incertitude publiée.", False)],
          [("Ce que dit le score : ", True), ("la capacité agentique intrinsèque du modèle, indépendante du harness.", False)],
          [("Limite : ", True), ("certains modèles absents du leaderboard (chiffre éditeur en repli).", False)]]),
        ("terra", "devs", "Agentique  ·  modèle × harness", "Terminal-Bench 2.1",
         [[("Quoi : ", True), ("des tâches à mener dans un terminal (build, debug, data, admin), dans un conteneur isolé.", False)],
          [("Comment : ", True), ("harness libre, Terminus 2 en référence ou harness éditeur (ex. Claude Code) ; vérifié par tests.", False)],
          [("Ce que dit le score : ", True), ("la performance du couple modèle × harness en conditions d'usage.", False)],
          [("Limite : ", True), ("beaucoup de scores auto-rapportés, écarts avec les mesures indépendantes.", False)]]),
        ("ochre", "archi", "Baseline  ·  repère historique", "SWE-bench Verified",
         [[("Quoi : ", True), ("500 issues GitHub Python validées par des humains ; le patch est accepté s'il passe les tests.", False)],
          [("Comment : ", True), ("chaque éditeur choisit son harness et ses réglages ; peu de reproductions indépendantes.", False)],
          [("Ce que dit le score : ", True), ("un repère de continuité, saturé au-dessus de 90 % en tête de tableau.", False)],
          [("Limite : ", True), ("harness hétérogènes, chiffres surtout éditeurs : conservé grisé, jamais discriminant.", False)]]),
    ]
    for i, (acc, ic, tag, title, items) in enumerate(specs):
        x = ML + i * (cw + gap)
        card(s, x, cy, cw, ch, acc, ic, tag, title)
        bullets(s, x + 0.32, cy + 1.0, cw - 0.56, ch - 1.1, items, sz=10.5, sa=5)

    by = cy + ch + 0.16; bh = 0.85
    rect(s, ML, by, CW_FULL, bh, fill=GREY, rounded=True, radius=0.07)
    tf = tb(s, ML + 0.3, by + 0.14, CW_FULL - 0.6, bh - 0.28, MSO_ANCHOR.MIDDLE)
    para(tf, [R("Règle de lecture  ", sz=12, b=True, c=ROYAL),
              R("DeepSWE classe les modèles ; Terminal-Bench montre ce que le harness ajoute ; SWE-bench Verified ne sert qu'à situer. "
                "Sans marque = officiel · ᵛ éditeur · * indépendant. Aucune case estimée : sans donnée, « non publié ».", sz=12, c=INK)],
         first=True, ls=1.12)
    footer(s, 3)
    notes(s, "Doctrine performance fixée le 02/09/2026 : DeepSWE v1.1 en principal (leaderboard officiel Datacurve, harness fixé "
             "mini-swe-agent, donc score du modèle seul, indépendant du harness) ; Terminal-Bench 2.1 en agentique (tâches terminal "
             "en conteneur, harness libre : Terminus 2 de référence, ou harness éditeur type Claude Code) ; SWE-bench Verified conservé "
             "en baseline grisée (500 issues GitHub Python validées par des annotateurs humains, OpenAI 2024 ; saturé en tête, harness "
             "hétérogènes, chiffres surtout éditeurs). Règle absolue : ne jamais estimer ni extrapoler un score.")

    # ------------------------------------------------------------------
    # SLIDE 4 - CE QUI BOOSTE LES MODÈLES
    # ------------------------------------------------------------------
    s = new_slide(prs); brand(s)
    header(s, "Performance  ·  au-delà du modèle",
           "Ce qui booste un modèle : harness, pratiques, orchestration",
           "Le score du modèle seul est un plancher : le même modèle change de niveau selon son outillage et son pilotage.")

    cy = 2.02; ch = 3.1; gap = 0.22; cw = (CW_FULL - 2 * gap) / 3
    specs = [
        ("terra", "devs", "1  ·  Le harness", "L'outillage du modèle",
         [[("Outils : ", True), ("édition de fichiers, shell, recherche dans le dépôt, connecteurs MCP.", False)],
          [("Contexte : ", True), ("compaction, fichiers de mémoire, sous-agents pour isoler les recherches.", False)],
          [("Boucle agentique : ", True), ("planifier, agir, vérifier, corriger ; permissions et garde-fous.", False)],
          [("Taillé pour un modèle : ", True), ("Claude Code, gourmand en contexte, vise le frontier ; OpenCode reste neutre.", False)]]),
        ("blue", "cdp", "2  ·  Les bonnes pratiques", "L'apport de l'équipe",
         [[("Contexte projet : ", True), ("un fichier d'instructions (CLAUDE.md, AGENTS.md) : conventions, commandes, architecture.", False)],
          [("Spécifier avant de coder : ", True), ("mode plan, tâches petites et vérifiables, critères d'acceptation.", False)],
          [("Les tests comme oracle : ", True), ("l'agent boucle sur les tests ; la revue humaine reste le dernier filtre.", False)],
          [("Skills réutilisables : ", True), ("procédures capitalisées, partagées entre équipes.", False)]]),
        ("green", "altout", "3  ·  L'orchestration", "Des agents en équipe",
         [[("Découper les rôles : ", True), ("planificateur, exécutant, vérificateur ; sous-agents en parallèle.", False)],
          [("Router les modèles : ", True), ("le frontier pour le difficile, l'économique et souverain pour le volume.", False)],
          [("Workflows déterministes : ", True), ("hooks, CI/CD, revues automatiques dans le pipeline.", False)],
          [("Observabilité : ", True), ("traces, coûts, taux de réussite par tâche pour arbitrer sur des faits.", False)]]),
    ]
    for i, (acc, ic, tag, title, items) in enumerate(specs):
        x = ML + i * (cw + gap)
        card(s, x, cy, cw, ch, acc, ic, tag, title)
        bullets(s, x + 0.32, cy + 1.0, cw - 0.56, ch - 1.1, items, sz=10, sa=4)

    # preuve chiffrée : effet harness sur Terminal-Bench
    by = cy + ch + 0.16; bh = 1.5
    rect(s, ML, by, CW_FULL, bh, fill=GREY, rounded=True, radius=0.07)
    tf = tb(s, ML + 0.3, by + 0.14, 4.0, 1.0)
    para(tf, [R("CE QUE MONTRE LE BENCH", sz=10, b=True, c=OCHRE)], first=True)
    para(tf, [R("Même modèle : le score bouge selon le harness et la mesure.", sz=13, b=True, c=INK)], sb=3, ls=1.05)
    para(tf, [R("Terminal-Bench 2.1, leaderboard officiel.", sz=10, c=MUTED)], sb=3)
    # mini tableau
    kx = ML + 4.5; kw = CW_FULL - 4.8
    lines = [
        ("Fable 5", "Claude Code (xhigh)", "83,8 %", "Terminus 2", "80,4 %", "+3,4 pts"),
        ("Sonnet 5", "Claude Code (high)", "74,6 %", "annonce éditeur", "80,4 %ᵛ", "écart 5,8 pts"),
        ("Kimi K3", "annonce éditeur", "88,3 %ᵛ", "mesure vals.ai", "80,9 %", "écart 7,4 pts"),
    ]
    colw = [1.0, 1.75, 0.85, 1.55, 0.85, kw - (1.0 + 1.75 + 0.85 + 1.55 + 0.85)]
    for r, ln in enumerate(lines):
        y = by + 0.14 + r * 0.3
        cx = kx
        for ci, val in enumerate(ln):
            tf = tb(s, cx, y, colw[ci], 0.3, MSO_ANCHOR.MIDDLE)
            b = ci in (0, 2, 4, 5); c = ROYAL if ci == 0 else (INK if b else SLATE)
            if ci == 5: c = GREEN if r == 0 else TERRA
            para(tf, [R(val, sz=10.5, b=b, c=c)], first=True, ls=1.0)
            cx += colw[ci]
    rect(s, ML + 0.3, by + 1.03, CW_FULL - 0.6, 0.008, fill=HAIR)
    tf = tb(s, ML + 0.3, by + 1.1, CW_FULL - 0.6, 0.25)
    para(tf, [R("Conséquence pour le choix souverain : ", sz=10, b=True, c=INK),
              R("un modèle moins bien classé, bien harnaché et orchestré, peut couvrir une large part du quotidien ; le bench élargi tranchera.", sz=10, c=SLATE)], first=True, ls=1.05)
    footer(s, 4)
    notes(s, "Le harness : ensemble outils + gestion du contexte + boucle agentique + permissions qui entoure le modèle (Claude Code, "
             "OpenCode, Vibe...). Doctrine fournisseurs du 14/08/2026 : Claude Code est très gourmand en contexte, taillé pour les modèles "
             "frontier ; risque de moins bien marcher avec les modèles moins onéreux (open-weight chinois). Cible : une observabilité "
             "indépendante du harness pour choisir librement le couple harness × modèle.\n"
             "Preuve chiffrée (Terminal-Bench 2.1, valeurs fiabilisées le 02/09/2026) : Fable 5 83,8 ±1,2 avec Claude Code xhigh vs 80,4 avec "
             "Terminus 2 (leaderboard officiel) ; Sonnet 5 : 80,4 annoncé par Anthropic vs 74,6 au leaderboard officiel (Claude Code high) ; "
             "Kimi K3 : 88,3 auto-rapporté vs 80,9 mesuré par vals.ai. Les deux derniers écarts mêlent effet harness et effet de mesure "
             "(auto-rapporté vs indépendant) : à présenter comme tels.\n"
             "Bonnes pratiques et orchestration : leviers observés dans l'accompagnement (coaching DACCORD, VAO, skills partagés) ; pas de "
             "chiffrage publié comparable, d'où l'absence de pourcentage sur cette slide. Le bench élargi en conditions réelles (Albert / "
             "DeepSeek via OpenCode face à Claude) mesurera l'effet réel sur le backlog du ministère.")

    prs.save(out)
    print("saved", out)

if __name__ == "__main__":
    build(os.path.join(HERE, "..", "Souverainete-Performance-Modeles-Harness.pptx"))

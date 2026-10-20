# -*- coding: utf-8 -*-
"""Souveraineté et performance des modèles et harness - Système de design de l'État (DSFR).
5 slides : titre, souveraineté vs conformité (CLOUD Act, SecNumCloud), matrice bench 9 stacks,
ce que mesurent les 3 benchs, ce qui booste les modèles (harness, pratiques, orchestration).
Chiffres vérifiés le 23/09/2026 (sources détaillées dans les notes de chaque slide).
Rendu : police Marianne (postes de l'État ; repli sans-serif sinon), tokens DSFR 1.15.3 (dist/dsfr.min.css),
bloc-marque et pictogrammes officiels rendus depuis le paquet @gouvfr/dsfr (build/assets)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONT = "Marianne"
DATE = "Septembre 2026"
VERIF = "23/09/2026"

# ---- tokens DSFR 1.15.3 ----
BF = "000091"; BF925 = "E3E3FD"; BF950 = "ECECFE"; BF975 = "F5F5FE"      # bleu France
RM = "E1000F"                                                             # rouge Marianne
G50 = "161616"; G200 = "3A3A3A"; G425 = "666666"; G625 = "929292"
G900 = "DDDDDD"; G950 = "EEEEEE"; G975 = "F6F6F6"; WHITE = "FFFFFF"
SUCCESS, SUCCESS_BG = "18753C", "B8FEC9"
WARNING, WARNING_BG = "B34000", "FFE9E6"
ERROR, ERROR_BG = "CE0500", "FFE9E9"
INFO, INFO_BG = "0063CB", "E8EDFF"
BADGE = {"success": (SUCCESS, SUCCESS_BG), "warning": (WARNING, WARNING_BG),
         "error": (ERROR, ERROR_BG), "info": (INFO, INFO_BG), "grey": (G50, G950)}

SW, SH = 13.333, 7.5
ML = 0.6; MR = SW - ML; CW_FULL = MR - ML
BM_RATIO = 822 / 502   # bloc-marque.png (largeur / hauteur)

def C(h): return RGBColor.from_string(h)

def new_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = C(WHITE)
    return s

def rect(s, x, y, w, h, fill=None, line=None, lw=0.75, pill=False):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if pill else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = C(fill)
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = C(line); shp.line.width = Pt(lw)
    if pill:
        try: shp.adjustments[0] = 0.5
        except Exception: pass
    return shp

def tb(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf

def R(t, **k): k["t"] = t; return k

def hang(p, marL=0.18):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(marL))); pPr.set("indent", str(-Inches(marL)))

def para(tf, runs, align=PP_ALIGN.LEFT, sa=0, sb=0, ls=1.08, first=False, bullet=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align; p.space_after = Pt(sa); p.space_before = Pt(sb); p.line_spacing = ls
    if bullet: hang(p)
    for rr in runs:
        r = p.add_run(); r.text = rr["t"]; f = r.font
        f.name = FONT; f.size = Pt(rr.get("sz", 12)); f.bold = rr.get("b", False)
        f.italic = rr.get("i", False); f.color.rgb = C(rr.get("c", G50))
    return p

def picto(s, name, x, y, d=0.6):
    s.shapes.add_picture(os.path.join(ASSETS, f"picto-{name}.png"), Inches(x), Inches(y), Inches(d), Inches(d))

def bloc_marque(s, x, y, h, big=False):
    fn = "bloc-marque-grand.png" if big else "bloc-marque.png"
    s.shapes.add_picture(os.path.join(ASSETS, fn), Inches(x), Inches(y), Inches(h * BM_RATIO), Inches(h))
    return h * BM_RATIO

def text_w(t, sz, bold=False):
    """largeur approx. (pouces) d'un texte Marianne ; majuscules plus larges."""
    up = sum(1 for ch in t if ch.isupper() or ch.isdigit())
    return (len(t) * 0.52 + up * 0.14) * sz / 72 * (1.06 if bold else 1.0)

def badge(s, x, y, text, kind, sz=8, h=0.21):
    """fr-badge : pilule teintée, libellé majuscules gras coloré. Retourne la largeur."""
    fg, bg = BADGE[kind]
    w = text_w(text.upper(), sz, True) + 0.22
    rect(s, x, y, w, h, fill=bg, pill=True)
    tf = tb(s, x, y, w, h, MSO_ANCHOR.MIDDLE)
    para(tf, [R(text.upper(), sz=sz, b=True, c=fg)], align=PP_ALIGN.CENTER, first=True, ls=1.0)
    return w

def tag(s, x, y, text, sz=9.5, h=0.3, right=False):
    """fr-tag : pilule grise, texte gris foncé. right=True : x est le bord droit."""
    w = text_w(text, sz) + 0.34
    if right: x = x - w
    rect(s, x, y, w, h, fill=G950, pill=True)
    tf = tb(s, x, y, w, h, MSO_ANCHOR.MIDDLE)
    para(tf, [R(text, sz=sz, c=G50)], align=PP_ALIGN.CENTER, first=True, ls=1.0)
    return w

def service(s, x, y, sz=10.5):
    tf = tb(s, x, y, 7.0, 0.55)
    para(tf, [R("Secrétariat général des ministères sociaux", sz=sz, b=True, c=G50)], first=True, ls=1.0)
    para(tf, [R("Direction du numérique (DNUM)  ·  Transformation IA", sz=sz - 1.5, c=G425)], ls=1.0, sb=2)

def header(s, title, sub, chip):
    w = bloc_marque(s, ML, 0.27, 0.5)
    service(s, ML + w + 0.22, 0.31)
    tag(s, MR, 0.35, chip, right=True)
    rect(s, ML, 0.97, CW_FULL, 0.0125, fill=G900)          # séparation d'en-tête
    tf = tb(s, ML - 0.02, 1.1, 11.8, 0.5)
    para(tf, [R(title, sz=23, b=True, c=BF)], first=True, ls=1.02)
    tf = tb(s, ML, 1.56, 11.9, 0.36)
    para(tf, [R(sub, sz=12, c=G425)], first=True, ls=1.1)

def footer(s, page):
    rect(s, ML, 6.84, CW_FULL, 0.028, fill=BF)             # fr-footer : bordure haute bleu France
    tf = tb(s, ML, 6.95, 11.0, 0.3)
    para(tf, [R("Ippon Technologies pour la DNUM", sz=8.5, b=True, c=G200),
              R(f"  ·  Souveraineté et performance des modèles et des harness  ·  document de travail, {DATE}  ·  "
                f"chiffres vérifiés le {VERIF}, sources en notes", sz=8.5, c=G425)], first=True, ls=1.0)
    tf2 = tb(s, MR - 0.8, 6.95, 0.8, 0.3)
    para(tf2, [R(f"{page}", sz=9, b=True, c=G50)], align=PP_ALIGN.RIGHT, first=True, ls=1.0)

def card(s, x, y, w, h, ic, kicker, title, fill=WHITE):
    """fr-card : fond blanc, bordure grise, angles droits ; pictogramme DSFR + surtitre + titre."""
    rect(s, x, y, w, h, fill=fill, line=G900)
    d = 0.66
    if ic: picto(s, ic, x + 0.26, y + 0.22, d)
    tx = x + 0.26 + (d + 0.16 if ic else 0)
    tf = tb(s, tx, y + 0.24, w - (tx - x) - 0.22, 0.8)
    para(tf, [R(kicker, sz=9, b=True, c=BF)], first=True, ls=1.0)
    para(tf, [R(title, sz=15, b=True, c=G50)], sb=2, ls=1.02)

def callout(s, x, y, w, h, title, text, sz=11.5):
    """fr-callout : fond bleu France 975, barre gauche bleu France, texte."""
    rect(s, x, y, w, h, fill=BF975)
    rect(s, x, y, 0.055, h, fill=BF)
    tf = tb(s, x + 0.3, y + 0.12, w - 0.5, h - 0.24, MSO_ANCHOR.MIDDLE)
    para(tf, [R(title + "  ", sz=sz + 0.5, b=True, c=G50), R(text, sz=sz, c=G200)], first=True, ls=1.12)

def block(s, x, y, w, h, kicker, kicker_col, kicker_tail, lines):
    """bloc gris (fr-background-alt) : surtitre coloré + paragraphes [(runs, sb)]."""
    rect(s, x, y, w, h, fill=G975)
    tf = tb(s, x + 0.28, y + 0.18, w - 0.56, h - 0.3)
    para(tf, [R(kicker, sz=9.5, b=True, c=kicker_col), R(kicker_tail, sz=9.5, b=True, c=G425)], first=True, ls=1.0)
    for runs, sb in lines: para(tf, runs, sb=sb, ls=1.1)

def bullets(s, x, y, w, h, items, sz=10.5, sa=4):
    tf = tb(s, x, y, w, h)
    for i, it in enumerate(items):
        runs = [R("•  ", sz=sz, c=G425)]
        if isinstance(it, str): runs.append(R(it, sz=sz, c=G200))
        else:
            for (t, b) in it: runs.append(R(t, sz=sz, b=b, c=G50 if b else G200))
        para(tf, runs, sa=sa, ls=1.12, first=(i == 0), bullet=True)
    return tf

def notes(s, txt): s.notes_slide.notes_text_frame.text = txt

# =====================================================================
# DONNÉES DU BENCH (vérifiées le 23/09/2026 ; voir notes de la slide 2)
# Marquage : sans marque = officiel · ᵛ = auto-rapporté éditeur · * = mesure indépendante · llm-stats = agrégat
# Règle absolue : aucun score estimé ; sans donnée = « non publié ».
# =====================================================================
NS = ("error", "Non souveraine")
ROWS = [
    # harness, modèle, fournisseur, DeepSWE (main, sub), TB 2.1 (main, sub), SWE-V (main, sub), prix (in, out, note), souv (kind, label, sub), conf (kind, label, sub)
    # ordre : DeepSWE décroissant (officiel ou auto-rapporté ᵛ)
    dict(h="Claude Code", m="Opus 5.5", p="AWS Bedrock",
         ds=("74,2 %ᵛ", "hors leaderboard"), tb=("non publié", "TB 4.0 : 66,4 %ᵛ"), sv=("non publié", "SWE-bench Pro 89,9ᵛ"),
         px=("4 $", "20 $", ""), souv=NS + ("CLOUD Act",), conf=("success", "Bonne", "profil UE · DPA AWS")),
    dict(h="Codex CLI", m="GPT-5.6 Terra", p="AWS Bedrock",
         ds=("69,6 %", "±2,6"), tb=("78,4 %", "±2,5 · 87,4 %ᵛ annonce"), sv=("non publié", ""),
         px=("2 $", "12 $", ""), souv=NS + ("CLOUD Act",), conf=("warning", "Sous conditions", "traitement hors UE (États-Unis)")),
    dict(h="OpenCode", m="Kimi K3", p="OpenRouter",
         ds=("69 %", "±5"), tb=("88,3 %ᵛ", "80,9 % *"), sv=("93,4 % *", ""),
         px=("3 $", "15 $", ""), souv=NS + ("CN + routeur US",), conf=("error", "Insuffisante", "sans garanties UE")),
    dict(h="Codex CLI", m="GPT-6 Sol", p="AWS Bedrock · GA du 22/09, fiche AWS à venir",
         ds=("68,8 %ᵛ", "hors leaderboard"), tb=("83,2 % *", "vals.ai"), sv=("non publié", ""),
         px=("2 $", "10 $", "Bedrock : non publié"), souv=NS + ("CLOUD Act",), conf=("warning", "Sous conditions", "hors UE · régions non publiées")),
    dict(h="Claude Code", m="Fable 5.1", p="AWS Bedrock",
         ds=("67,4 %ᵛ", "hors leaderboard"), tb=("91,4 % *", "Terminus 2 · AA"), sv=("non publié", "SWE-bench Pro 81,2ᵛ"),
         px=("10 $", "50 $", ""), souv=NS + ("CLOUD Act",), conf=("warning", "Sous conditions", "hors UE · rétention 30 j AWS")),
    dict(h="Claude Code", m="Sonnet 5", p="AWS Bedrock",
         ds=("53,8 %", "±4,2"), tb=("80,4 %ᵛ", "74,6 % officiel"), sv=("85,2 %ᵛ", "79,6 % *"),
         px=("2 $", "10 $", ""), souv=NS + ("CLOUD Act",), conf=("success", "Bonne", "profil UE · DPA AWS")),
    dict(h="OpenCode", m="DeepSeek V4 Flash 0731", p="Scaleway",
         ds=("53 %", "54,4 %ᵛ"), tb=("82,7 %ᵛ", ""), sv=("non publié", ""),
         px=("0,40 €", "0,80 €", ""), souv=("success", "Souveraine (UE)", "cloud FR · hébergé UE"), conf=("success", "Bonne", "RGPD · cloud FR")),
    dict(h="OpenCode", m="DeepSeek V4 Flash 0731", p="Albert (DINUM) · expérimentation, contexte 131k",
         ds=("53 %", "±4"), tb=("82,7 %ᵛ", ""), sv=("non publié", ""),
         px=("gratuit", "", "agents de l'État"), souv=("success", "Souveraine", "SecNumCloud · État FR"), conf=("success", "Bonne", "cadre État")),
    dict(h="OpenCode", m="GLM 5.2", p="Scaleway",
         ds=("44,0 %", ""), tb=("81,0 %ᵛ", ""), sv=("non publié", ""),
         px=("1,80 €", "5,50 €", ""), souv=("success", "Souveraine (UE)", "cloud FR · hébergé UE"), conf=("success", "Bonne", "RGPD · cloud FR")),
]

# preuve « effet harness » (Terminal-Bench 2.1), slide 5
PROOF = [
    # modèle, contexte A, score A, contexte B, score B, lecture, couleur
    ("GPT-5.5", "Codex (xhigh)", "83,2 %", "Terminus 2 (xhigh)", "78,0 %", "+5,2 pts", SUCCESS),
    ("Fable 5", "Claude Code (xhigh)", "83,8 %", "Terminus 2 (high)", "80,4 %", "+3,4 pts", SUCCESS),
    ("Sonnet 5", "Claude Code (high)", "74,6 %", "annonce éditeur", "80,4 %ᵛ", "écart 5,8 pts", WARNING),
    ("Kimi K3", "annonce éditeur", "88,3 %ᵛ", "mesure vals.ai", "80,9 %", "écart 7,4 pts", WARNING),
]

NOTES_BENCH = "Matrice mise à jour le 23/09/2026 (refonte DSFR). Règle absolue : aucun score estimé ; sans donnée = « non publié ». Ordre : DeepSWE décroissant.\nDEEPSWE v1.1 (leaderboard officiel Datacurve https://deepswe.datacurve.ai/, harness fixé mini-swe-agent, 113 tâches, IC 95 % run-to-run sur 4 runs, page mise à jour le 22/09/2026) : GPT-5.6 Terra [max] 69,6 ±2,6 (ligne présente dans les données, hors tableau par défaut) ; Kimi K3 [max] 69 ±5 ; Sonnet 5 [max] 53,8 ±4,2 (26,40 $/tâche) ; DeepSeek V4 Flash 0731 [max] 53 ±4 (54,4 auto-rapporté) ; GLM 5.2 [max] 44 ±2. Absents du leaderboard : Opus 5.5 (74,2 auto-rapporté, system card, 5 essais, harness non précisé), Fable 5.1 (67,4 auto-rapporté, system card), GPT-6 Sol (68,8 auto-rapporté, annonce OpenAI du 22/09). Repères : Opus 5 [max] 73,6 ±3,9 ; Fable 5 [xhigh] 69,9 ±3,2 ; GPT-6 Astra [xhigh] 74 ±3 (rang 1).\nTERMINAL-BENCH 2.1 : le leaderboard officiel tbench.ai n'est plus affiché depuis le passage à Terminal-Bench 4.0 (28/08/2026 ; soumissions 2.1 closes) ; données 2.1 lues le 23/09 via l'endpoint de données du site (mise à jour 03/09/2026, 22 lignes, 89 tâches × 5 essais) : GPT-5.6 Terra Codex [max] 78,4 ±2,5 ; Sonnet 5 Claude Code [high] 74,6 ±3,2 ; Fable 5 Claude Code [xhigh] 83,8 ±2,3 et Terminus 2 [high] 80,4 ±2,3 ; GPT-6 Astra Codex [high] 87,4 ±1,8 (rang 1). Aucune entrée Kimi K3, Opus 5.5, Fable 5.1, GPT-6 Sol, DeepSeek, GLM 5.2. Auto-rapportés : Terra 87,4 (annonce OpenAI, harness non nommé) ; Kimi K3 88,3 (Moonshot, harness Kimi Code) ; Sonnet 5 80,4 (system card, mini-SWE-agent) ; DeepSeek 0731 82,7 ; GLM 5.2 81,0. Indépendants : Fable 5.1 91,4 (Artificial Analysis, Terminus 2, effort max, https://artificialanalysis.ai/evaluations/terminalbench-2-1) ; GPT-6 Sol 83,2 (vals.ai, 22/09/2026, harness non documenté) ; Kimi K3 80,9 (vals.ai). Opus 5.5 : aucune mesure 2.1 ; TB 4.0 auto-rapporté 66,4 (Claude Code xhigh). TB 4.0 officiel : Fable 5.1 57,9 ±3,8, Terra 21,5, GPT-6 Astra 58,2 : TB 4.0 (66 tâches) est un autre benchmark, non comparable au 2.1 ; à envisager comme colonne agentique à la prochaine mise à jour du bench.\nSWE-BENCH VERIFIED (baseline grisée) : Anthropic et OpenAI ne le publient plus (SWE-bench Pro à la place : Opus 5.5 89,9, Fable 5.1 81,2, Terra 63,4). Sonnet 5 : 85,2 auto-rapporté (system card, 5 essais) et 79,6 ±1,8 vals.ai (harness bash minimal, page du 01/09/2026) ; Kimi K3 93,4 vals.ai ; DeepSeek 0731 et GLM 5.2 non publiés. vals.ai semble afficher 95,4 ±0,9 pour Terra (valeur lue dans le balisage, non confirmée à l'écran : non reprise).\nPRIX (publics, hors remises, relevés le 23/09/2026). Anthropic (https://platform.claude.com/docs/en/about-claude/pricing) : Opus 5.5 4/20 $ (cache lecture 0,20 $ ; fast mode 8/40 $ sur l'API Anthropic uniquement, pas sur Bedrock), Fable 5.1 10/50 $, Sonnet 5 2/10 $ (prix introductif devenu standard, hausse du 01/09 annulée). Bedrock (https://aws.amazon.com/bedrock/pricing/ et fiches modèle docs.aws.amazon.com) : profil Global = prix éditeur ; profil Geo (résidence UE ou US) et in-region = +10 % : Opus 5.5 4,40/22 $, Sonnet 5 2,20/11 $, Fable 5.1 11/55 $ (us-east-1 seulement), Terra 2,20/13,20 $. OpenAI (https://developers.openai.com/api/docs/pricing) : GPT-6 Sol 2/10 $ (cache 0,20), GPT-5.6 Terra 2/12 $ (baisse du 30/07/2026) ; fiche Bedrock GPT-6 Sol non publiée au 23/09 (GA du 22/09). Kimi K3 : 3/15 $ (prix Moonshot et prix de référence OpenRouter ; le 2,55/12,75 $ relevé le 02/09 était l'endpoint tiers Makora). Scaleway (HT, https://www.scaleway.com/en/pricing/model-as-a-service/) : deepseek-v4-flash-0731 0,40/0,80 €, glm-5.2 1,80/5,50 €. Albert API : gratuit pour les agents de la fonction publique de l'État, quotas (DeepSeek : 50 RPM, 246k TPM), modèle deepseek-ai/DeepSeek-V4-Flash-0731 en expérimentation jusqu'au 01/10/2026, contexte 131k (https://ia.numerique.gouv.fr/outils-ia/albert-api/tarifs-et-limites/ ; https://guides.ia.numerique.gouv.fr/albert-api/modeles/available-models) : le checkpoint servi par Albert est bien le 0731 (l'hypothèse « preview d'avril » du 02/09 est levée ; Albert et Scaleway servent le même modèle, seuls le contexte, le prix et le niveau de souveraineté diffèrent). Taux BCE du 22/09 : 1 € = 1,1463 $.\nSOUVERAINETÉ (CNIL) : Bedrock non souverain (CLOUD Act, quelle que soit la région), Claude comme GPT ; OpenRouter : éditeur chinois + routeur US ; Albert (SecNumCloud, État) et Scaleway (cloud FR, hébergé UE) souverains.\nCONFORMITÉ RGPD : Opus 5.5 et Sonnet 5 disponibles en profil Geo EU (eu.anthropic.*, données maintenues en UE), ZDR par défaut : bonne. Fable 5.1 : aucun profil UE sur Bedrock (Global uniquement, endpoint régional us-east-1 seul), opt-in data_retention_mode aws_review obligatoire, rétention 30 jours de tout le trafic avec revue humaine AWS possible : sous conditions. GPT-6 Sol et GPT-5.6 Terra : aucun profil eu.openai.*, in-region États-Unis (Inde en Geo pour Terra), UE accessible seulement en Global (routage mondial sans contrainte de résidence) : traitement hors UE, conformité sous conditions (transfert encadré : DPF, clauses types, DPA AWS). OpenRouter insuffisante. Scaleway et Albert bonnes.\nHARNESS : Codex CLI documenté officiellement avec Bedrock (provider amazon-bedrock, API Responses ; https://aws.amazon.com/blogs/machine-learning/get-started-with-openai-gpt-5-6-sol-terra-and-luna-on-amazon-bedrock/) ; OpenCode possible via bedrock-runtime (Converse) mais non vérifié pour les modèles OpenAI.\nEXCLUSION GPT-6 ASTRA (demande client) : 10/50 $ (Bedrock Geo 11/55 $), DeepSWE 74 ±3 officiel, TB 2.1 87,4 ±1,8 officiel (Codex high) : cinq fois le prix de GPT-6 Sol pour quelques points."
NOTES_BOOST = "Le harness : ensemble outils + gestion du contexte + boucle agentique + permissions qui entoure le modèle (Claude Code, Codex CLI, OpenCode...). Doctrine fournisseurs du 14/08/2026 : Claude Code est très gourmand en contexte, taillé pour les modèles frontier ; risque de moins bien marcher avec les modèles moins onéreux (open-weight). Codex CLI sur Bedrock : environ 9 400 tokens de surcharge par requête (billet AWS). Cible : une observabilité indépendante du harness pour choisir librement le couple harness × modèle.\nPreuve chiffrée (Terminal-Bench 2.1, leaderboard officiel lu le 23/09/2026 via l'endpoint de données tbench.ai, mise à jour du 03/09/2026) : GPT-5.5 à réglage identique xhigh : Codex 83,2 ±2,2 vs Terminus 2 78,0 ±2,4 (+5,2 pts, effet harness seul) ; Fable 5 : Claude Code xhigh 83,8 ±2,3 vs Terminus 2 high 80,4 ±2,3 (+3,4 pts, réglages différents) ; Opus 4.7 max : Claude Code 68,9 vs Terminus 2 66,1 (+2,8 pts). Sonnet 5 : 74,6 ±3,2 officiel (Claude Code high) vs 80,4 annoncé (system card, mini-SWE-agent) ; Kimi K3 : 88,3 auto-rapporté (Kimi Code) vs 80,9 vals.ai : ces deux écarts mêlent effet harness et effet de mesure (auto-rapporté vs indépendant), à présenter comme tels. Fable 5.1, Opus 5.5, GPT-6 Sol : aucune paire officielle disponible (leaderboard 2.1 clos), d'où le recours à GPT-5.5 et Fable 5 comme exemples documentés.\nBonnes pratiques et orchestration : leviers observés dans l'accompagnement ; pas de chiffrage publié comparable, d'où l'absence de pourcentage sur cette slide. Le bench élargi en conditions réelles (Albert / DeepSeek 0731 via OpenCode face à Claude et GPT via Bedrock) mesurera l'effet réel sur le backlog."

# =====================================================================
def build(out):
    prs = Presentation(); prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)

    # ------------------------------------------------------------------
    # SLIDE 1 - TITRE
    # ------------------------------------------------------------------
    s = new_slide(prs)
    w = bloc_marque(s, ML, 0.5, 1.3, big=True)
    service(s, ML + w + 0.35, 0.58, sz=12.5)
    rect(s, ML, 2.05, CW_FULL, 0.0125, fill=G900)
    tf = tb(s, ML - 0.03, 2.4, 8.7, 1.9)
    para(tf, [R("Souveraineté et performance", sz=38, b=True, c=BF)], first=True, ls=1.02)
    para(tf, [R("des modèles et des harness", sz=38, b=True, c=BF)], ls=1.02)
    tf = tb(s, ML, 4.32, 8.4, 1.0)
    para(tf, [R("Ce que « souverain » et « conforme » veulent dire, ce que mesure le bench, "
                "et ce qui fait réellement la performance d'un agent de code.", sz=15, c=G200)], first=True, ls=1.18)
    x = ML
    for t in ("Coding agentique", "9 stacks comparées", f"Chiffres vérifiés le {VERIF}", DATE):
        x += tag(s, x, 5.55, t) + 0.14
    # tuiles (fr-tile) à droite
    tx = 9.55; tw = MR - tx; th = 1.08; ty = 2.4
    for i, (ic, lab, sub) in enumerate((("padlock", "Souveraineté", "une question de juridiction, pas d'adresse"),
                                        ("data-visualization", "Bench", "trois mesures, neuf stacks, aucun chiffre estimé"),
                                        ("flow-settings", "Harness", "l'outillage et le pilotage font le niveau"))):
        y = ty + i * (th + 0.14)
        rect(s, tx, y, tw, th, fill=WHITE, line=G900)
        picto(s, ic, tx + 0.22, y + 0.2, 0.68)
        tf = tb(s, tx + 1.05, y + 0.18, tw - 1.25, th - 0.3, MSO_ANCHOR.MIDDLE)
        para(tf, [R(lab, sz=13, b=True, c=G50)], first=True, ls=1.0)
        para(tf, [R(sub, sz=9.5, c=G425)], sb=3, ls=1.08)
    rect(s, ML, 6.84, CW_FULL, 0.028, fill=BF)
    tf = tb(s, ML, 6.95, 11.5, 0.3)
    para(tf, [R("Ippon Technologies", sz=9, b=True, c=G200),
              R("  ·  document de travail préparé pour la Direction du numérique des ministères sociaux  ·  "
                "mission d'accompagnement à la transformation IA", sz=9, c=G425)], first=True, ls=1.0)
    notes(s, "Deck en Système de design de l'État (DSFR 1.15.3 : police Marianne, bleu France #000091, rouge Marianne #E1000F, "
             "gris #161616/#666666/#DDDDDD, badges succès/erreur/avertissement, bloc-marque et pictogrammes officiels). "
             "Refonte du 23/09/2026 du deck Ippon du 03/09/2026 : modèles mis à jour (Opus 5.5 sorti le 22/09/2026, Fable 5.1), "
             "ajout des stacks OpenAI via Bedrock (GPT-6 Sol, GPT-5.6 Terra ; GPT-6 Astra exclu à la demande du client), prix revérifiés. "
             "Sources détaillées dans les notes des slides 2 à 5.")

    # ------------------------------------------------------------------
    # SLIDE 2 - SOUVERAINETÉ vs CONFORMITÉ
    # ------------------------------------------------------------------
    s = new_slide(prs)
    header(s, "Souverain n'est pas synonyme de conforme",
           "La conformité protège les données personnelles ; la souveraineté protège de l'accès d'un État tiers. Deux questions, deux réponses.",
           "Cadre  ·  deux questions distinctes")
    cy = 2.02; ch = 2.46; gap = 0.24; cw = (CW_FULL - gap) / 2
    card(s, ML, cy, cw, ch, "padlock", "SOUVERAINETÉ  ·  QUI PEUT EXIGER L'ACCÈS ?", "Une question de juridiction")
    bullets(s, ML + 0.3, cy + 1.02, cw - 0.55, ch - 1.1, [
        [("Critère : ", True), ("le droit applicable à l'opérateur et à ses maisons mères, pas l'adresse des serveurs. "
                              "Un acteur US en région UE reste soumis au droit US (lecture CNIL) : Bedrock, Vertex AI ou Azure, même à Paris.", False)],
        [("Tiennent : ", True), ("Albert et Outscale LLMaaS (SecNumCloud 3.2) ; Scaleway et OVHcloud AI Endpoints (cloud FR, hors périmètre SecNumCloud).", False)],
        [("Mistral : ", True), ("éditeur français, mais La Plateforme a tourné sur Azure et Google Cloud. Souverain via Outscale ou en poids ouverts auto-hébergés.", False)],
    ], sz=10)
    x2 = ML + cw + gap
    card(s, x2, cy, cw, ch, "contract", "CONFORMITÉ  ·  LES DONNÉES SONT-ELLES TRAITÉES LÉGALEMENT ?", "Une question de RGPD")
    bullets(s, x2 + 0.3, cy + 1.02, cw - 0.55, ch - 1.1, [
        [("Critère : ", True), ("base légale, contrat de sous-traitance (DPA), sécurité, transferts hors UE encadrés.", False)],
        [("Avec un acteur US : ", True), ("Bedrock en profil UE avec le DPA AWS est conforme RGPD (Opus 5.5, Sonnet 5). Les modèles OpenAI et Fable 5.1 "
                                          "n'ont pas de profil UE sur Bedrock : traitement aux États-Unis, conformité sous conditions (transfert encadré : DPF, clauses types).", False)],
        [("Insuffisante : ", True), ("OpenRouter, routage par un intermédiaire US sans garanties UE.", False)],
    ], sz=10)

    by = cy + ch + 0.14; bh = 1.38
    block(s, ML, by, cw, bh, "CLOUD ACT (ÉTATS-UNIS, 2018)  ", ERROR, "+ FISA 702", [
        ([R("Les fournisseurs soumis au droit US doivent remettre les données aux autorités américaines, où qu'elles soient stockées. ", sz=10.5, c=G200),
          R("La localisation ne protège pas.", sz=10.5, b=True, c=G50)], 4),
        ([R("Transferts UE-US (DPF, 2023) : validé en première instance le 03/09/2025, pourvoi pendant devant la CJUE (C-703/25 P).", sz=9, c=G425)], 4),
    ])
    block(s, x2, by, cw, bh, "SECNUMCLOUD 3.2 (ANSSI)  ", SUCCESS, "référentiel du « cloud de confiance »", [
        ([R("Qualification de sécurité + critères d'immunité aux lois extraterritoriales : ", sz=10.5, c=G200),
          R("siège et capital dans l'UE, données, clés et administration en UE, personnel habilité.", sz=10.5, b=True, c=G50)], 4),
        ([R("Doctrine « cloud au centre » : données sensibles sur cloud qualifié. Qualifiés : Outscale (héberge Albert), OVHcloud (IaaS), "
            "S3NS (Thales-Google) depuis 12/2025.", sz=9, c=G425)], 4),
    ])
    ty = by + bh + 0.14
    callout(s, ML, ty, CW_FULL, 6.72 - ty, "À retenir",
            "Bedrock (Claude comme GPT), Vertex AI ou Azure : conformes quand le modèle est servi en résidence UE, jamais souverains. "
            "Albert, Outscale, Scaleway, OVHcloud : les deux. "
            "OpenRouter : ni l'un ni l'autre. Le référencement UGAP est un canal d'achat, pas un label de souveraineté.", sz=11)
    footer(s, 2)
    notes(s, "Souveraineté au sens CNIL : ce qui compte est la juridiction de l'opérateur (et de ses maisons mères), pas la région "
             "d'hébergement. AWS reste soumis au CLOUD Act (2018) quelle que soit la région : Bedrock n'est donc jamais souverain, "
             "même à Paris ; cela vaut pour les modèles Anthropic comme pour les modèles OpenAI servis par Bedrock. Conformité RGPD : axe distinct ; "
             "Bedrock région UE + DPA AWS est conforme ; OpenRouter insuffisant.\n"
             "CLOUD Act : loi US de 2018 ; les fournisseurs soumis au droit US doivent remettre les données sur demande des autorités US, "
             "quelle que soit la localisation. FISA 702 : surveillance des non-Américains. Sources : LexisNexis 'Cloud Act et RGPD' ; "
             "LeMagIT 'CLOUD Act : quels risques pour les clients européens'.\n"
             "DPF (Data Privacy Framework, décision d'adéquation de juillet 2023) : recours Latombe rejeté par le Tribunal de l'UE le "
             "03/09/2025 (T-553/23) ; pourvoi devant la CJUE déposé le 31/10/2025 (C-703/25 P), pas de date d'audience connue "
             "(IAPP ; EDPL 2026/1).\n"
             "SecNumCloud 3.2 (ANSSI, 2022) : exigences techniques + critères d'immunité aux lois extraterritoriales : prestataire et "
             "maisons mères établis dans l'UE, contrôle du capital, données/métadonnées/journaux/clés en UE, administration depuis l'UE, "
             "administrateurs habilités. Nuance : protection documentée et contractualisée, pas une neutralisation du droit US "
             "(CIO-Online). Doctrine 'cloud au centre' (circulaires 2021/2023) : données sensibles sur offre qualifiée SecNumCloud. "
             "Albert (DINUM) : hébergé sur Outscale (Dassault Systèmes), qualifié SecNumCloud 3.2.\n"
             "VÉRIFICATIONS DU 03/09/2026 (inchangées au 23/09) : OUTSCALE LLMaaS = modèles Mistral servis sur la région SecNumCloud 3.2 : "
             "souverain. OVHCLOUD AI Endpoints : hébergé en France (Gravelines) mais hors périmètre SecNumCloud (services IA visés fin 2026) : "
             "même statut que Scaleway. MISTRAL : La Plateforme a fonctionné sur Azure, Google Cloud et CoreWeave jusqu'au datacenter de "
             "Bruyères-le-Châtel (fin août 2026) ; part encore servie depuis des clouds tiers inconnue : Mistral n'est pas listé comme voie "
             "souveraine en tant que service. UGAP : canal d'achat (marché cloud IaaS/PaaS porté par Capgemini : AWS, Google Cloud, Azure, "
             "Oracle, IBM aux côtés d'Outscale, OVHcloud, Scaleway, Cloud Temple), pas un label. S3NS (Thales + Google) SecNumCloud 3.2 le "
             "17/12/2025, Vertex AI prévu S2 2026 : à surveiller, pas disponible.\n"
             "VÉRIFICATION DU 23/09/2026 (résidence UE sur Bedrock) : Opus 5.5 et Sonnet 5 : profil Geo EU disponible (eu.anthropic.claude-opus-5-5, eu.anthropic.claude-sonnet-5 ; Paris, Francfort, Irlande, Stockholm en Geo et Global, pas d'in-region sur bedrock-runtime), ZDR par défaut. Fable 5.1 : pas de profil Geo EU, Global uniquement depuis l'UE, endpoint régional us-east-1 seul, rétention 30 jours obligatoire (Covered Model, revue humaine AWS possible), ZDR réservé aux clients Enterprise Frontier Safeguards jusqu'au 31/12/2026. GPT-6 Sol et GPT-5.6 Terra : aucun profil eu.openai.*, in-region us-east-1 / us-east-2 / us-west-2 (mantle), Geo US et Inde ; les huit régions UE listées ne sont accessibles qu'en Global CRIS ; AWS (blog du 20/08/2026) : « If your workload has data residency requirements that restrict processing to specific geographies, use the geographic profile for that geography » ; fiche GPT-6 Sol non publiée au 23/09. Sources : fiches modèle docs.aws.amazon.com (model-card-anthropic-claude-opus-5-5, -fable-5-1, -sonnet-5, model-card-openai-gpt-56-terra), data-retention.html, abuse-detection.html, platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock#regions.")

    # ------------------------------------------------------------------
    # SLIDE 3 - MATRICE BENCH
    # ------------------------------------------------------------------
    s = new_slide(prs)
    header(s, "Performance, prix, souveraineté, conformité",
           f"Trois mesures de performance, prix par million de tokens (entrée · sortie), souveraineté au sens CNIL, conformité RGPD  ·  vérifié le {VERIF}.",
           f"Bench  ·  {len(ROWS)} stacks de coding agentique")

    cols = [  # (libellé, sous-libellé, largeur)
        ("Harness · modèle", "fournisseur", 2.95),
        ("DeepSWE v1.1", "modèle seul · principal", 1.35),
        ("Terminal-Bench 2.1", "agentique", 1.5),
        ("SWE-bench Verified", "baseline · saturé", 1.6),
        ("Prix / 1M tokens", "entrée · sortie", 1.3),
        ("Souveraineté", "au sens CNIL", 1.7),
        ("Conformité", "RGPD / données", CW_FULL - (2.95 + 1.35 + 1.5 + 1.6 + 1.3 + 1.7)),
    ]
    xs = []; x = ML
    for _, _, w in cols: xs.append(x); x += w
    hy = 2.0; hh = 0.42
    rect(s, ML, hy, CW_FULL, hh, fill=G950)                           # fr-table thead
    rect(s, ML, hy + hh - 0.02, CW_FULL, 0.02, fill=BF)
    for i, (lab, sub, w) in enumerate(cols):
        tf = tb(s, xs[i] + 0.12, hy, w - 0.18, hh, MSO_ANCHOR.MIDDLE)
        para(tf, [R(lab, sz=9, b=True, c=G50)], first=True, ls=1.0)
        para(tf, [R(sub, sz=7.5, c=G425)], ls=1.0, sb=1)

    n = len(ROWS)
    ry = hy + hh + 0.04; avail = 6.42 - ry; rh = avail / n
    for r, row in enumerate(ROWS):
        y = ry + r * rh
        rect(s, ML, y, CW_FULL, rh, fill=(G975 if r % 2 == 0 else WHITE))
        rect(s, ML, y + rh - 0.008, CW_FULL, 0.008, fill=G900)
        # stack : harness + modèle en tête, fournisseur grisé
        tf = tb(s, xs[0] + 0.12, y, cols[0][2] - 0.18, rh, MSO_ANCHOR.MIDDLE)
        para(tf, [R(row["h"] + "  ·  ", sz=9.5, b=True, c=BF), R(row["m"], sz=9.5, b=True, c=G50)], first=True, ls=1.0)
        para(tf, [R(row["p"], sz=7.5, c=G425)], ls=1.0, sb=1)
        # performances
        for ci, key, grey in ((1, "ds", False), (2, "tb", False), (3, "sv", True)):
            main, sub = row[key]
            tf = tb(s, xs[ci] + 0.12, y, cols[ci][2] - 0.18, rh, MSO_ANCHOR.MIDDLE)
            np_ = main == "non publié"
            col = G625 if (grey or np_) else G50
            para(tf, [R(main, sz=10.5 if ci == 1 else 10, b=(ci == 1 and not np_), c=col, i=np_)], first=True, ls=1.0)
            if sub: para(tf, [R(sub, sz=7.5, c=G425)], ls=1.0, sb=1)
        # prix
        pin, pout, pnote = row["px"]
        tf = tb(s, xs[4] + 0.12, y, cols[4][2] - 0.18, rh, MSO_ANCHOR.MIDDLE)
        runs = [R(pin, sz=10, b=True, c=G50)]
        if pout: runs.append(R("  ·  " + pout, sz=10, c=G200))
        para(tf, runs, first=True, ls=1.0)
        if pnote: para(tf, [R(pnote, sz=7.5, c=G425)], ls=1.0, sb=1)
        # souveraineté / conformité : badges DSFR
        for ci, key in ((5, "souv"), (6, "conf")):
            kind, lab, sub = row[key]
            by_ = y + (rh - 0.2) / 2 - (0.07 if sub else 0)
            badge(s, xs[ci] + 0.12, by_, lab, kind, sz=7.5, h=0.2)
            if sub:
                tf = tb(s, xs[ci] + 0.14, by_ + 0.21, cols[ci][2] - 0.2, 0.16)
                para(tf, [R(sub, sz=7, c=G425)], first=True, ls=1.0)

    ly = ry + n * rh + 0.05
    tf = tb(s, ML, ly, CW_FULL, 0.3)
    para(tf, [R("Sans marque = officiel  ·  ᵛ auto-rapporté par l'éditeur  ·  * mesure indépendante (vals.ai, Artificial Analysis)  ·  "
                "aucun chiffre estimé : sans donnée, « non publié »  ·  prix publics hors remises (Bedrock : profil Global ; résidence UE "
                "en profil Geo : +10 %), Scaleway en euros HT  ·  TB 4.0 = nouveau Terminal-Bench, non comparable au 2.1", sz=8.5, c=G425, i=True)], first=True, ls=1.0)
    footer(s, 3)
    notes(s, NOTES_BENCH)

    # ------------------------------------------------------------------
    # SLIDE 4 - CE QUE MESURENT LES 3 BENCHS
    # ------------------------------------------------------------------
    s = new_slide(prs)
    header(s, "Ce que mesurent les trois benchmarks",
           "Un score n'a de sens qu'avec sa question : le modèle seul, le couple modèle × harness, ou un repère historique.",
           "Lecture  ·  trois mesures, trois questions")
    cy = 2.02; ch = 3.55; gap = 0.22; cw = (CW_FULL - 2 * gap) / 3
    specs = [
        ("search", "PRINCIPAL  ·  LE MODÈLE SEUL", "DeepSWE v1.1",
         [[("Quoi : ", True), ("des tâches d'ingénierie logicielle réelles, résolues de bout en bout par l'agent.", False)],
          [("Comment : ", True), ("harness fixé pour tous (mini-swe-agent), leaderboard officiel Datacurve, incertitude publiée.", False)],
          [("Ce que dit le score : ", True), ("la capacité agentique intrinsèque du modèle, indépendante du harness.", False)],
          [("Limite : ", True), ("certains modèles absents du leaderboard (chiffre éditeur en repli, ou « non publié »).", False)]]),
        ("coding", "AGENTIQUE  ·  MODÈLE × HARNESS", "Terminal-Bench 2.1",
         [[("Quoi : ", True), ("des tâches à mener dans un terminal (build, debug, data, admin), dans un conteneur isolé.", False)],
          [("Comment : ", True), ("harness libre, Terminus 2 en référence ou harness éditeur (Claude Code, Codex CLI) ; vérifié par tests.", False)],
          [("Ce que dit le score : ", True), ("la performance du couple modèle × harness en conditions d'usage.", False)],
          [("Limite : ", True), ("beaucoup de scores auto-rapportés, écarts avec les mesures indépendantes.", False)]]),
        ("document", "BASELINE  ·  REPÈRE HISTORIQUE", "SWE-bench Verified",
         [[("Quoi : ", True), ("500 issues GitHub Python validées par des humains ; le patch est accepté s'il passe les tests.", False)],
          [("Comment : ", True), ("chaque éditeur choisit son harness et ses réglages ; peu de reproductions indépendantes.", False)],
          [("Ce que dit le score : ", True), ("un repère de continuité, saturé au-dessus de 90 % en tête de tableau.", False)],
          [("Limite : ", True), ("harness hétérogènes, chiffres surtout éditeurs : conservé grisé, jamais discriminant.", False)]]),
    ]
    for i, (ic, kicker, title, items) in enumerate(specs):
        x = ML + i * (cw + gap)
        card(s, x, cy, cw, ch, ic, kicker, title)
        bullets(s, x + 0.28, cy + 1.08, cw - 0.5, ch - 1.15, items, sz=10, sa=5)
    by = cy + ch + 0.18
    callout(s, ML, by, CW_FULL, 6.72 - by, "Règle de lecture",
            "DeepSWE classe les modèles ; Terminal-Bench montre ce que le harness ajoute ; SWE-bench Verified ne sert qu'à situer. "
            "Sans marque = officiel · ᵛ éditeur · * indépendant. Aucune case estimée : sans donnée, « non publié ».", sz=11)
    footer(s, 4)
    notes(s, "Doctrine performance fixée le 02/09/2026 : DeepSWE v1.1 en principal (leaderboard officiel Datacurve, harness fixé "
             "mini-swe-agent, donc score du modèle seul, indépendant du harness) ; Terminal-Bench 2.1 en agentique (tâches terminal "
             "en conteneur, harness libre : Terminus 2 de référence, ou harness éditeur type Claude Code ou Codex CLI) ; SWE-bench Verified conservé "
             "en baseline grisée (500 issues GitHub Python validées par des annotateurs humains, OpenAI 2024 ; saturé en tête, harness "
             "hétérogènes, chiffres surtout éditeurs). Règle absolue : ne jamais estimer ni extrapoler un score.")

    # ------------------------------------------------------------------
    # SLIDE 5 - CE QUI BOOSTE LES MODÈLES
    # ------------------------------------------------------------------
    s = new_slide(prs)
    header(s, "Ce qui booste un modèle : harness, pratiques, orchestration",
           "Le score du modèle seul est un plancher : le même modèle change de niveau selon son outillage et son pilotage.",
           "Performance  ·  au-delà du modèle")
    cy = 2.02; ch = 3.0; gap = 0.22; cw = (CW_FULL - 2 * gap) / 3
    specs = [
        ("flow-settings", "1  ·  LE HARNESS", "L'outillage du modèle",
         [[("Outils : ", True), ("édition de fichiers, shell, recherche dans le dépôt, connecteurs MCP.", False)],
          [("Contexte : ", True), ("compaction, fichiers de mémoire, sous-agents pour isoler les recherches.", False)],
          [("Boucle agentique : ", True), ("planifier, agir, vérifier, corriger ; permissions et garde-fous.", False)],
          [("Taillé pour un modèle : ", True), ("Claude Code et Codex CLI, gourmands en contexte, visent le frontier ; OpenCode reste neutre.", False)]]),
        ("human-cooperation", "2  ·  LES BONNES PRATIQUES", "L'apport de l'équipe",
         [[("Contexte projet : ", True), ("un fichier d'instructions (CLAUDE.md, AGENTS.md) : conventions, commandes, architecture.", False)],
          [("Spécifier avant de coder : ", True), ("mode plan, tâches petites et vérifiables, critères d'acceptation.", False)],
          [("Les tests comme oracle : ", True), ("l'agent boucle sur les tests ; la revue humaine reste le dernier filtre.", False)],
          [("Skills réutilisables : ", True), ("procédures capitalisées, partagées entre équipes.", False)]]),
        ("ecosystem", "3  ·  L'ORCHESTRATION", "Des agents en équipe",
         [[("Découper les rôles : ", True), ("planificateur, exécutant, vérificateur ; sous-agents en parallèle.", False)],
          [("Router les modèles : ", True), ("le frontier pour le difficile, l'économique et souverain pour le volume.", False)],
          [("Workflows déterministes : ", True), ("hooks, CI/CD, revues automatiques dans le pipeline.", False)],
          [("Observabilité : ", True), ("traces, coûts, taux de réussite par tâche pour arbitrer sur des faits.", False)]]),
    ]
    for i, (ic, kicker, title, items) in enumerate(specs):
        x = ML + i * (cw + gap)
        card(s, x, cy, cw, ch, ic, kicker, title)
        bullets(s, x + 0.28, cy + 1.08, cw - 0.5, ch - 1.15, items, sz=9.5, sa=4)

    # preuve chiffrée : effet harness sur Terminal-Bench (bloc gris + mini tableau)
    by = cy + ch + 0.18; bh = 6.72 - by
    rect(s, ML, by, CW_FULL, bh, fill=G975)
    tf = tb(s, ML + 0.28, by + 0.14, 4.15, 1.0)
    para(tf, [R("CE QUE MONTRE LE BENCH", sz=9, b=True, c=BF)], first=True)
    para(tf, [R("Même modèle : le score bouge selon le harness et la mesure.", sz=12, b=True, c=G50)], sb=3, ls=1.05)
    para(tf, [R("Terminal-Bench 2.1 · officiel (03/09/2026) et indépendant.", sz=9, c=G425)], sb=3)
    kx = ML + 4.5; kw = CW_FULL - 4.78
    colw = [1.05, 1.75, 0.85, 1.55, 0.85, kw - (1.05 + 1.75 + 0.85 + 1.55 + 0.85)]
    for r, ln in enumerate(PROOF):
        y = by + 0.1 + r * 0.245
        cx = kx
        for ci, val in enumerate(ln[:6]):
            tf = tb(s, cx, y, colw[ci], 0.245, MSO_ANCHOR.MIDDLE)
            b = ci in (0, 2, 4, 5); c = BF if ci == 0 else (G50 if b else G200)
            if ci == 5: c = ln[6]
            para(tf, [R(val, sz=10, b=b, c=c)], first=True, ls=1.0)
            cx += colw[ci]
    rect(s, ML + 0.28, by + 1.15, CW_FULL - 0.56, 0.008, fill=G900)
    tf = tb(s, ML + 0.28, by + 1.21, CW_FULL - 0.56, 0.3)
    para(tf, [R("Conséquence pour le choix souverain : ", sz=10, b=True, c=G50),
              R("un modèle moins bien classé, bien harnaché et orchestré, peut couvrir une large part du quotidien ; le bench élargi tranchera.", sz=10, c=G200)],
         first=True, ls=1.05)
    footer(s, 5)
    notes(s, NOTES_BOOST)

    prs.save(out)
    print("saved", out)

if __name__ == "__main__":
    build(os.path.join(HERE, "..", "Souverainete-Performance-Modeles-Harness.pptx"))

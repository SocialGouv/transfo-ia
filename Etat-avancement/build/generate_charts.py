#!/usr/bin/env python3
"""Génère les visuels SVG de l'état d'avancement (clair + sombre).

Usage : python3 generate_charts.py
Sortie : ../assets/*.svg

Mise à jour hebdo : modifier la section DONNÉES ci-dessous, relancer,
puis ajuster les textes du README si besoin. Aucune dépendance externe.
"""

import os

# ============================================================================
# DONNÉES — à mettre à jour chaque semaine
# ============================================================================

MAJ = "10 août 2026"

# Matrice de maturité : niveau constaté par use case et périmètre.
# Valeurs : 1 à 5, (avant, après) pour une progression, None = NA.
# Échelle : les use cases non encore observés sont notés 1 par convention.
PERIMETRES = ["Egapro", "DACCORD", "SIRENA", "VAO", "Transverse"]

NIVEAUX = ["Découverte", "Expérimentation", "Pratique régulière", "Maîtrise", "Standard d'équipe"]

MATRICE = [
    # (métier, use case, [Egapro, DACCORD, SIRENA, VAO, Transverse])
    ("Chefs de projet", "Piloter un projet développé avec l'IA",   [(1, 3), 1, 1, 1, None]),
    ("Chefs de projet", "Générer des tickets de spec",             [1, 1, 1, 1, None]),
    ("Chefs de projet / Développeurs", "Organiser le board (sprints, epics)", [4, 1, 1, 1, None]),
    ("Designers",       "Générer des prototypes HTML/JS",          [(1, 4), 1, 1, 1, None]),
    ("Développeurs",    "Générer du code de qualité",              [3, 3, 1, 1, None]),
    ("Développeurs",    "Générer des tests",                       [4, 3, 1, 1, None]),
    ("Développeurs",    "Utiliser des orchestrations",             [4, 1, 1, 1, None]),
    ("Développeurs",    "Pré-auditer l'accessibilité",             [(1, 2), 1, 1, 1, None]),
    ("Développeurs",    "Pré-auditer la sécurité",                 [1, 1, 1, 1, None]),
    ("Développeurs",    "Outils &amp; system prompts communs",     [4, (1, 2), 1, 1, None]),
    ("Architectes",     "Générer un dossier d'architecture (DA)",  [None, None, None, None, 1]),
    ("Architectes",     "Outiller les référentiels d'architecture", [None, None, None, None, 1]),
]

# Maturité d'organisation par périmètre : (périmètre, niveau avant accompagnement,
# niveau actuel, ce que l'accompagnement a changé). Échelle 1-5 (règle Selim 10/08) :
# 1-2 de rien à la découverte de l'IA · 3 des skills utilisés, des use cases pratiqués,
# une orga perfectible · 4 des orchestrations, une orga maîtrisée · 5 + volume de cas
# d'usage (dev, PM/PO), bonnes pratiques renseignées, vrai craft.
MATURITE_ORG = [
    ("Egapro",      3, 4, "orchestrations en routine, orga maîtrisée"),
    ("DACCORD",     1, 2, "skills partagés, accompagnement individuel"),
    ("SIRENA",      2, 2, ""),
    ("VAO",         1, 1, ""),
    ("Architectes", 1, 2, "premiers use cases IA identifiés (atelier DA)"),
]
NIVEAUX_ORG = ["Rien", "Découverte", "Skills · use cases", "Orchestrations", "Craft · volume"]

# KPI (label, valeur, sous-texte, sous-texte vert facultatif)
KPIS = [
    ("Périmètres montés en maturité", "3", "· architectes", "▲ Egapro · DACCORD "),
    ("Use cases montés de niveau", "4", "· 1 sur DACCORD", "▲ 3 sur Egapro "),
    ("Actions à impact déterminant", "15", "chacune décrite dans le détaillé", None),
    ("Prochain jalon", "Mi-août", "formation PM/PO SIRENA · DACCORD", None),
]

# Jalons : (jour depuis le 13 juillet, lignes, statut done|next|futur, label au-dessus ?)
ROADMAP_SPAN_DAYS = 80  # 13 juillet → fin septembre
JALONS = [
    # certains jours sont décalés de 1 à 3 jours pour desserrer les étiquettes
    (3,  ["16 juillet", "Coaching dev augmenté", "équipe DACCORD"], "done", True),
    (14, ["28-30 juillet", "Référentiels archi", "CDP SIRENA · CEPS"], "done", False),
    (22, ["4 août", "Atelier DA", "avec les architectes"], "done", True),
    (25, ["6 août", "Atelier skills", "+ pt produit IA"], "done", False),
    (35, ["Mi-août", "Formation PM/PO", "SIRENA · DACCORD"], "next", True),
    (38, ["Courant août", "Catalogue de skills", "DSFR · bench Bedrock"], "next", False),
    (46, ["Fin août", "Acculturation IA", "avec Igor"], "next", True),
    (51, ["Sem. du 31 août", "Sélection use cases", "architectes"], "next", False),
    (59, ["8 septembre", "Dev augmenté VAO", "+ tickets BIO2 (Yuna)"], "futur", True),
    (78, ["Fin septembre", "Cartographie des comptes", "Bedrock (bénéficiaires)"], "futur", True),
]
ROADMAP_NOTE = ("Ensuite, moyen terme : communauté de référents IA, CI/CD augmentée, "
                "observabilité · long terme : harness souverain")

# Impact des actions engagées : (libellé, nb de losanges, sous-texte)
IMPACT_LEVELS = [
    ("Déterminant", 3, "du concret dans le quotidien"),
    ("Élevé", 2, "acculturations et formations"),
    ("Modéré", 1, "cadrages, études, com"),
]
# (chantier, déterminant, élevé, modéré)
IMPACTS = [
    ("Egapro",     4, 0, 0),
    ("DACCORD",    4, 1, 0),
    ("SIRENA",     0, 1, 0),
    ("VAO",        1, 1, 0),
    ("BIO2",       1, 0, 0),
    ("Transverse", 5, 3, 11),
]
IMPACT_NOTE = ("Les actions à impact modéré sont toutes transverses : les chantiers de fond "
               "(bench, Bedrock, outillage des postes) qui conditionnent le passage à l'échelle.")

# Bench harness : (harness · modèle en tête, provider grisé dessous)
BENCH = [
    # (harness, modèle, provider, perf %, label perf, prix sortie $/1M, label prix,
    #  souveraineté (statut, libellé, détail), conformité RGPD (statut, libellé, détail))
    ("Claude Code", "Fable 5", "AWS Bedrock", 95.0, "95,0 %", 50.0, "50 $",
     ("bad", "Non souveraine", "CLOUD Act (CNIL)"),
     ("good", "Bonne", "région UE · DPA AWS")),
    ("OpenCode", "Kimi K3", "OpenRouter", 93.4, "≈93 % *", 15.0, "15 $",
     ("bad", "Non souveraine", "éditeur CN, routeur US"),
     ("bad", "Insuffisante", "sans garanties UE")),
    ("Claude Code", "Opus 4.8", "Anthropic", 88.6, "88,6 %", 25.0, "25 $",
     ("bad", "Non souveraine", "éditeur US"),
     ("mid", "Partielle", "transfert hors UE")),
    ("OpenCode", "DeepSeek V4 Pro", "OpenRouter", 80.6, "80,6 %", 0.87, "0,87 $ (preview)",
     ("bad", "Non souveraine", "éditeur CN, routeur US"),
     ("bad", "Insuffisante", "sans garanties UE")),
    ("OpenCode", "DeepSeek V4 Flash", "Albert (DINUM)", 79.0, "≈79 %", 0.0, "gratuit (agents État)",
     ("good", "Souveraine", "SecNumCloud · État FR"),
     ("good", "Bonne", "cadre État (DINUM)")),
    ("OpenCode", "GLM 5.2", "OpenRouter", 78.0, "≈78 %", 4.40, "4,40 $",
     ("bad", "Non souveraine", "éditeur CN, routeur US"),
     ("bad", "Insuffisante", "sans garanties UE")),
    ("Vibe", "Mistral Medium 3.5", "Mistral", 77.6, "77,6 %", 7.50, "7,50 $",
     ("good", "Souveraine (UE)", "SecNumCloud en option"),
     ("good", "Bonne", "RGPD · éditeur FR")),
]
BENCH_NOTE = ("Lecture : la conformité RGPD passe par Bedrock (région UE), Mistral ou Albert ; "
              "la souveraineté (sens CNIL) par Albert ou Mistral · * score annoncé par l'éditeur")

# Usine logicielle cible : à chaque étape, deux rails (agentique génère, déterministe
# vérifie). Cellules en lignes pré-coupées pour le rendu SVG.
USINE_COLS = ["Product", "Design", "Build", "Livraison"]
USINE_GEN = [
    ["Challenge par l'IA de la", "clarté du besoin,", "formalisation, critères", "d'acceptation"],
    ["Prototypes basés sur", "le design system"],
    ["Génération de code,", "tests, revue, recette", "assistée par agent"],
    ["Notes de version et", "changelog générés"],
]
USINE_VER = [
    ["Definition of Ready", "vérifiable, formatage", "des specs"],
    ["Respect du design", "system, audit", "d'accessibilité"],
    ["Pipeline CI : formatage,", "tests, couverture Sonar"],
    ["Déploiement piloté,", "activation progressive"],
]
USINE_NOTE = "Cible illustrative : le détail du pipeline se précise chantier par chantier, avec les équipes."

# Tableau de bord adossé à DORA, sources = outillage prévu aux ministères sociaux
# (axe, indicateur, mode de calcul (lignes), source (lignes), type de source)
TDB = [
    ("Vitesse", "Cycle time", ["Délai issue → PR → prod,", "moyenne glissante (lead time DORA)"],
     ["GitHub / Jira"], "outille"),
    ("Vitesse", "Débit à effectif constant", ["Évolutions livrées / sprint,", "avant vs pendant"],
     ["GitHub / Jira (backlog)"], "outille"),
    ("Qualité", "Régressions &amp; rétablissement", ["Bugs prod / tickets livrés,", "délai moyen de résolution (DORA)"],
     ["Incidents + réclamations"], "outille"),
    ("Qualité", "Couverture &amp; dette", ["Delta couverture de tests", "et dette technique"],
     ["SonarQube / CI"], "outille"),
    ("Qualité", "Exhaustivité documentation", ["% de repos avec doc à jour", "(README, ADR)"],
     ["Audit des repos GitHub"], "outille"),
    ("Coût", "Coût par fonctionnalité", ["Tokens consommés (Bedrock · Albert)", "+ temps de review / fonctionnalité"],
     ["Facturation AWS · Albert", "+ Jira"], "outille"),
    ("Adoption IA", "Usage réel de l'IA", ["% de devs actifs / jour sur les harness,", "tokens consommés par projet"],
     ["Observabilité", "Bedrock · Albert"], "outille"),
    ("Adoption IA", "Maturité d'équipe (1 à 5)", ["Score par périmètre, à chaque jalon"],
     ["Grille de maturité", "+ accompagnement"], "expertise"),
    ("Adoption IA", "Gain de temps perçu", ["Heures estimées / sem / dev,", "agrégées par équipe"],
     ["Questionnaire court"], "declaratif"),
    ("Risque", "Conformité d'usage", ["% d'usages cadrés par la charte,", "vs shadow IT"],
     ["Charte IA + audit", "des accès"], "outille"),
]

# ============================================================================
# PALETTES (validées via dataviz/scripts/validate_palette.js, clair + sombre)
# ============================================================================

THEMES = {
    "light": {
        "surface": "#fcfcfb", "ink": "#0b0b0b", "sec": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "baseline": "#c3c2b7", "border": "rgba(11,11,11,0.10)",
        "good": "#006300", "accent": "#2a78d6",
        "status": {"good": "#0ca30c", "mid": "#fab219", "bad": "#d03b3b"},
        # niveaux 1 à 5 · séparation adjacente vérifiée (validate_palette.js),
        # chaque cellule porte son chiffre (contraste texte ≥ 4,5:1)
        "ramp5": ["#d8e8fb", "#8ab8f0", "#3987e5", "#1c5cab", "#0d366b"],
        "on_ramp5": ["#0b0b0b", "#0b0b0b", "#0b0b0b", "#ffffff", "#ffffff"],
        "impact3": ["#0d366b", "#3987e5", "#8ab8f0"],  # déterminant, élevé, modéré
        "rail_ver": "#006300", "cell_gen": "#edf2fb", "cell_ver": "#ecf4ec",
        "warn_text": "#a35d00",
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#ffffff", "sec": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "baseline": "#383835", "border": "rgba(255,255,255,0.10)",
        "good": "#0ca30c", "accent": "#3987e5",
        "status": {"good": "#0ca30c", "mid": "#fab219", "bad": "#d03b3b"},
        "ramp5": ["#dfeafc", "#92bef2", "#4f92e8", "#2565bd", "#123f77"],
        "on_ramp5": ["#0b0b0b", "#0b0b0b", "#0b0b0b", "#ffffff", "#ffffff"],
        "impact3": ["#dfeafc", "#92bef2", "#4f92e8"],  # déterminant, élevé, modéré
        "rail_ver": "#006300", "cell_gen": "#20242c", "cell_ver": "#1f271f",
        "warn_text": "#fab219",
    },
}

FONT = "-apple-system,'Segoe UI',system-ui,Roboto,'Helvetica Neue',Arial,sans-serif"
W = 920  # largeur commune


# ============================================================================
# Aides SVG
# ============================================================================

def svg_open(h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" font-family="{FONT}">'
            f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="12" '
            f'fill="{t["surface"]}" stroke="{t["border"]}"/>')


def txt(x, y, s, size, color, weight="normal", anchor="start", spacing=None, tabular=False):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    if tabular:
        extra += ' font-variant-numeric="tabular-nums"'
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}>{s}</text>')


def title_block(t, title, subtitle=None):
    out = txt(32, 40, title, 15.5, t["ink"], "600")
    if subtitle:
        out += txt(32, 61, subtitle, 12.5, t["sec"])
    return out


def rbar(x, y, w, h, fill, r=4, left=False, right=True):
    """Barre horizontale : bout de données arrondi, base carrée."""
    r = min(r, w / 2, h / 2)
    rl, rr = (r if left else 0), (r if right else 0)
    return (f'<path d="M{x + rl},{y} h{w - rl - rr} '
            f'{f"a{rr},{rr} 0 0 1 {rr},{rr}" if rr else ""} v{h - 2 * rr} '
            f'{f"a{rr},{rr} 0 0 1 -{rr},{rr}" if rr else ""} h-{w - rl - rr} '
            f'{f"a{rl},{rl} 0 0 1 -{rl},-{rl}" if rl else ""} v-{h - 2 * rl} '
            f'{f"a{rl},{rl} 0 0 1 {rl},-{rl}" if rl else ""} z" fill="{fill}"/>')


def fr(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


# ============================================================================
# 1. Bandeau KPI
# ============================================================================

def chart_kpi(t):
    h = 150
    s = svg_open(h, t)
    tile_w = (W - 64) / 4
    for i, (label, value, sub, sub_good) in enumerate(KPIS):
        x = 32 + i * tile_w
        if i:
            s += f'<line x1="{x - 14}" y1="30" x2="{x - 14}" y2="{h - 30}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(x, 46, label, 12.5, t["sec"])
        s += txt(x, 92, value, 36, t["ink"], "600")
        if sub_good:
            s += (f'<text x="{x}" y="118" font-size="11.5">'
                  f'<tspan fill="{t["good"]}" font-weight="600">{sub_good}</tspan>'
                  f'<tspan fill="{t["muted"]}">{sub}</tspan></text>')
        else:
            s += txt(x, 118, sub, 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 2. Maturité d'organisation par périmètre
# ============================================================================

def chart_maturite_org(t):
    """Tableau : niveau d'organisation par périmètre (échelle 1 à 5). Flèche verte
    de l'avant vers l'actuel quand l'accompagnement a fait progresser le périmètre,
    rond blanc sur le niveau quand rien n'a encore changé."""
    x_p = 32
    lvl_x = [150, 250, 350, 450, 550]  # colonnes niveaux 1 → 5
    x_imp = 610
    y0, pitch = 148, 46
    n = len(MATURITE_ORG)
    h = y0 + n * pitch + 30
    s = svg_open(h, t)
    s += title_block(t, "Maturité par périmètre : Egapro passe de 3 à 4",
                     "niveau d'organisation atteint (échelle de 1 à 5) · flèche verte : la progression apportée par l'accompagnement · rond blanc : pas encore de changement")
    # en-têtes : pastille de niveau, libellé dessous
    hy1, hy2 = y0 - 52, y0 - 30
    for lv, xc in enumerate(lvl_x, start=1):
        s += f'<rect x="{xc - 9}" y="{hy1 - 13}" width="18" height="18" rx="4" fill="{t["ramp5"][lv - 1]}"/>'
        s += txt(xc, hy1, str(lv), 11, t["on_ramp5"][lv - 1], "600", anchor="middle")
        s += txt(xc, hy2, NIVEAUX_ORG[lv - 1], 10.5, t["sec"], "600", anchor="middle")
    s += txt(x_imp, hy2, "▲ Ce que l'accompagnement a changé", 12, t["good"], "600")
    for i, (p, avant, actuel, changed) in enumerate(MATURITE_ORG):
        y = y0 + i * pitch
        if i:
            s += f'<line x1="32" y1="{y - 23}" x2="888" y2="{y - 23}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(x_p, y + 7, p, 13.5, t["ink"], "600")
        cy = y + 2
        if actuel > avant:
            xs, xe = lvl_x[avant - 1], lvl_x[actuel - 1]
            s += f'<circle cx="{xs}" cy="{cy}" r="3.5" fill="{t["good"]}"/>'
            s += f'<line x1="{xs}" y1="{cy}" x2="{xe - 9}" y2="{cy}" stroke="{t["good"]}" stroke-width="2.5"/>'
            s += f'<path d="M{xe},{cy} l-10,-5.5 v11 z" fill="{t["good"]}"/>'
        else:
            s += (f'<circle cx="{lvl_x[actuel - 1]}" cy="{cy}" r="7" fill="#ffffff" '
                  f'stroke="{t["muted"]}" stroke-width="1.5"/>')
        if changed:
            s += txt(x_imp, y + 7, changed, 11.5, t["sec"])
        else:
            s += txt(x_imp + 14, y + 7, "–", 13, t["muted"], anchor="middle")
    s += txt(32, h - 38, "Échelle : 1-2 de rien à la découverte de l'IA · 3 des skills utilisés, "
             "des use cases pratiqués, une orga perfectible", 11.5, t["muted"])
    s += txt(32, h - 20, "4 des orchestrations, une organisation maîtrisée · 5 + volume de cas "
             "d'usage (dev et PM/PO), bonnes pratiques, vrai craft", 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 2 bis. Impact des actions par chantier
# ============================================================================

def chart_impact(t):
    """Tableau chiffré : nombre d'actions à impact par niveau et par chantier,
    dans la même forme que le tableau de maturité (chiffres nus, axes lisibles)."""
    x_p = 32
    lvl_x = [340, 560, 780]   # colonnes déterminant, élevé, modéré
    y0, pitch = 160, 46
    n = len(IMPACTS)
    total_y = y0 + n * pitch
    h = total_y + pitch + 40
    total = [sum(row[k + 1] for row in IMPACTS) for k in range(3)]
    s = svg_open(h, t)
    s += title_block(t, f"Actions à impact : {total[0]} déterminantes",
                     "chaque action est classée selon ce qu'elle change pour les équipes · "
                     "les déterminantes sont décrites une à une dans le détaillé")
    # en-têtes : losanges, libellé, définition courte
    hy1, hy2, hy3 = y0 - 64, y0 - 44, y0 - 28
    for k, (lab, nb, sub) in enumerate(IMPACT_LEVELS):
        xc = lvl_x[k]
        s += txt(xc, hy1, "◆" * nb, 12, t["impact3"][k], "600", anchor="middle", spacing="0.14em")
        s += txt(xc, hy2, lab, 12, t["sec"], "600", anchor="middle")
        s += txt(xc, hy3, sub, 10.5, t["muted"], anchor="middle")
    for i, (chantier, *counts) in enumerate(IMPACTS):
        y = y0 + i * pitch
        if i:
            s += f'<line x1="32" y1="{y - 23}" x2="888" y2="{y - 23}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(x_p, y + 7, chantier, 13.5, t["ink"], "600")
        for k, v in enumerate(counts):
            if v:
                s += txt(lvl_x[k], y + 8, str(v), 20, t["ink"], "600", anchor="middle", tabular=True)
            else:
                s += txt(lvl_x[k], y + 7, "–", 13, t["muted"], anchor="middle")
    # ligne de total par niveau d'impact
    s += f'<line x1="32" y1="{total_y - 23}" x2="888" y2="{total_y - 23}" stroke="{t["baseline"]}" stroke-width="1.5"/>'
    s += txt(x_p, total_y + 7, "Total", 13.5, t["sec"], "600")
    for k, v in enumerate(total):
        s += txt(lvl_x[k], total_y + 8, str(v), 20, t["ink"], "600", anchor="middle", tabular=True)
    s += txt(32, h - 20, IMPACT_NOTE, 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 4. Cap des prochaines semaines (jalons)
# ============================================================================

def chart_roadmap(t):
    # sans titre interne : le titre de section du README le porte déjà
    h = 224
    s = svg_open(h, t)
    x0, x1, ay = 60, 812, 112
    px_day = (x1 - x0) / ROADMAP_SPAN_DAYS
    s += f'<line x1="{x0 - 16}" y1="{ay}" x2="{x1 + 30}" y2="{ay}" stroke="{t["baseline"]}" stroke-width="1"/>'
    s += (f'<path d="M{x1 + 30},{ay} l-7,-4 v8 z" fill="{t["baseline"]}"/>')
    for day, lines, status, above in JALONS:
        mx = x0 + day * px_day
        color = t["good"] if status == "done" else t["accent"]
        s += f'<circle cx="{mx}" cy="{ay}" r="8" fill="{t["surface"]}"/>'
        if status == "futur":
            s += f'<circle cx="{mx}" cy="{ay}" r="5.5" fill="{t["surface"]}" stroke="{color}" stroke-width="2"/>'
        else:
            s += f'<circle cx="{mx}" cy="{ay}" r="6" fill="{color}"/>'
        head = ("✓ " if status == "done" else "") + lines[0]
        head_col = t["good"] if status == "done" else t["ink"]
        ys = [ay - 58, ay - 41, ay - 24] if above else [ay + 30, ay + 47, ay + 64]
        s += txt(mx, ys[0], head, 12.5, head_col, "600", anchor="middle")
        s += txt(mx, ys[1], lines[1], 12, t["sec"], anchor="middle")
        s += txt(mx, ys[2], lines[2], 12, t["sec"], anchor="middle")
    s += txt(32, h - 20, ROADMAP_NOTE, 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 5. Matrice de maturité (heatmap)
# ============================================================================

def chart_matrice(t):
    lbl_w, cell_h, gap, sect_h, row_gap = 296, 32, 4, 30, 4
    x0, top = 32 + lbl_w, 108
    cell_w = (W - 32 - x0) / 5 - gap
    # lignes groupées par métier
    y = top
    layout = []
    prev_role = None
    for role, label, levels in MATRICE:
        if role != prev_role:
            layout.append(("sect", role, y))
            y += sect_h
            prev_role = role
        layout.append(("row", (label, levels), y))
        y += cell_h + row_gap
    legend_y = y + 26
    h = int(legend_y + 46)
    s = svg_open(h, t)
    s += title_block(t, "Matrice de maturité IA : use case × périmètre",
                     "niveau auquel l'accompagnement a amené chaque fonction (échelle de 1 à 5) · une flèche = progression apportée par l'accompagnement")
    for j, p in enumerate(PERIMETRES):
        s += txt(x0 + j * (cell_w + gap) + cell_w / 2, top - 14, p, 12.5, t["ink"], "600", anchor="middle")
    for kind, data, yy in layout:
        if kind == "sect":
            s += txt(32, yy + 18, data.upper(), 10.5, t["muted"], "600", spacing="0.08em")
            continue
        label, levels = data
        s += txt(32, yy + cell_h / 2 + 4.5, label, 13, t["ink"])
        for j, v in enumerate(levels):
            cx = x0 + j * (cell_w + gap)
            mid_x, mid_y = cx + cell_w / 2, yy + cell_h / 2 + 4.5
            if v is None:
                s += txt(mid_x, mid_y, "–", 12, t["muted"], anchor="middle")
            else:
                lv = v[1] if isinstance(v, tuple) else v
                cell_txt = f"{v[0]} → {v[1]}" if isinstance(v, tuple) else str(lv)
                s += (f'<rect x="{cx}" y="{yy}" width="{cell_w}" height="{cell_h}" rx="4" '
                      f'fill="{t["ramp5"][lv - 1]}"/>')
                s += txt(mid_x, mid_y, cell_txt, 12.5, t["on_ramp5"][lv - 1], "600", anchor="middle")
    # légende
    lx = 32
    for i, lab in enumerate(NIVEAUX):
        s += f'<rect x="{lx}" y="{legend_y}" width="18" height="18" rx="4" fill="{t["ramp5"][i]}"/>'
        s += txt(lx + 9, legend_y + 13, str(i + 1), 11, t["on_ramp5"][i], "600", anchor="middle")
        s += txt(lx + 25, legend_y + 13.5, lab, 12, t["sec"])
        lx += 25 + len(lab) * 6.6 + 20
    s += txt(lx + 4, legend_y + 13.5, "–  non applicable", 12, t["sec"])
    return s + "</svg>", h


# ============================================================================
# 6. Bench harness : performance vs prix
# ============================================================================

def chart_bench(t):
    """Quatre panneaux : perf et prix en barres à base zéro, souveraineté et conformité en statut."""
    y0, rh = 122, 48
    n = len(BENCH)
    h = y0 + n * rh + 54
    px0, px1 = 250, 420   # panneau performance (0 → 100 %)
    qx0, qx1 = 466, 596   # panneau prix (0 → 50 $)
    sx = 648              # colonne souveraineté
    cx = 782              # colonne conformité
    s = svg_open(h, t)
    s += title_block(t, "Coding agentique : les stacks au bench",
                     "SWE-bench Verified, prix en sortie ($ / 1M tokens), souveraineté et conformité RGPD · vérifiés le 23/07/2026")
    s += txt(px0, 98, "Performance (SWE-bench)", 12, t["sec"], "600")
    s += txt(qx0, 98, "Prix sortie / 1M", 12, t["sec"], "600")
    s += txt(sx, 98, "Souveraineté", 12, t["sec"], "600")
    s += txt(cx, 98, "Conformité", 12, t["sec"], "600")
    for g, lab in ((0, "0"), (50, "50"), (100, "100 %")):
        gx = px0 + g / 100 * (px1 - px0)
        s += f'<line x1="{gx}" y1="{y0 - 8}" x2="{gx}" y2="{y0 + n * rh - 16}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(gx, y0 + n * rh + 2, lab, 11, t["muted"], anchor="middle")
    for g, lab in ((0, "0"), (25, "25"), (50, "50 $")):
        gx = qx0 + g / 50 * (qx1 - qx0)
        s += f'<line x1="{gx}" y1="{y0 - 8}" x2="{gx}" y2="{y0 + n * rh - 16}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(gx, y0 + n * rh + 2, lab, 11, t["muted"], anchor="middle")
    for i, (harness, modele, provider, perf, perf_lab, prix, prix_lab, souv, conf) in enumerate(BENCH):
        y = y0 + i * rh
        s += txt(32, y + 8, f"{harness} · {modele}", 12.5, t["ink"], "600")
        s += txt(32, y + 24, provider, 11, t["muted"])
        pw = perf / 100 * (px1 - px0)
        s += rbar(px0, y, pw, 16, t["accent"])
        s += txt(px0 + pw + 8, y + 12.5, perf_lab, 11.5, t["ink"], "600")
        if prix > 0:
            qw = max(prix / 50 * (qx1 - qx0), 3)
            s += rbar(qx0, y, qw, 16, t["accent"])
            s += txt(qx0 + qw + 8, y + 12.5, prix_lab, 11.5, t["ink"], "600")
        else:
            s += txt(qx0 + 2, y + 12.5, prix_lab, 11.5, t["good"], "600")
        for x_col, (statut, lib, det) in ((sx, souv), (cx, conf)):
            s += f'<circle cx="{x_col + 4}" cy="{y + 6}" r="4.5" fill="{t["status"][statut]}"/>'
            s += txt(x_col + 14, y + 10, lib, 12, t["ink"], "600")
            s += txt(x_col, y + 26, det, 10.5, t["muted"])
    s += txt(32, h - 22, BENCH_NOTE, 11, t["sec"])
    return s + "</svg>", h


# ============================================================================
# 8. Usine logicielle cible
# ============================================================================

def chart_usine(t):
    """Deux rails par étape du pipeline : le rail agentique génère, le rail
    déterministe vérifie — l'agent propose, la règle prouve."""
    x0, gap = 180, 12
    col_w = (W - 32 - x0 - (len(USINE_COLS) - 1) * gap) / len(USINE_COLS)
    row_h, row_gap = 100, 14
    y_gen = 118
    y_ver = y_gen + row_h + row_gap
    h = y_ver + row_h + 46
    s = svg_open(h, t)
    s += title_block(t, "La cible : l'usine logicielle",
                     "à chaque étape, un rail agentique qui génère et un rail déterministe qui vérifie · l'agent propose, la règle prouve")
    for j, c in enumerate(USINE_COLS):
        cx = x0 + j * (col_w + gap) + col_w / 2
        s += txt(cx, 100, c.upper(), 11, t["muted"], "600", anchor="middle", spacing="0.08em")
    for y, rail_fill, cell_fill, lab, sub, cells in (
        (y_gen, t["ramp5"][3], t["cell_gen"], "Rail agentique", "génère", USINE_GEN),
        (y_ver, t["rail_ver"], t["cell_ver"], "Rail déterministe", "vérifie", USINE_VER),
    ):
        s += f'<rect x="32" y="{y}" width="136" height="{row_h}" rx="10" fill="{rail_fill}"/>'
        w1, w2 = lab.split()
        s += txt(100, y + row_h / 2 - 12, w1, 12.5, "#ffffff", "600", anchor="middle")
        s += txt(100, y + row_h / 2 + 5, w2, 12.5, "#ffffff", "600", anchor="middle")
        s += txt(100, y + row_h / 2 + 24, sub, 11, "#ffffff", anchor="middle")
        for j, lines in enumerate(cells):
            cx0 = x0 + j * (col_w + gap)
            s += f'<rect x="{cx0}" y="{y}" width="{col_w}" height="{row_h}" rx="8" fill="{cell_fill}"/>'
            ty = y + row_h / 2 - (len(lines) - 1) * 8 + 4
            for k, ln in enumerate(lines):
                s += txt(cx0 + 14, ty + k * 16, ln, 12, t["ink"])
    s += txt(32, h - 20, USINE_NOTE, 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 9. Tableau de bord adossé à DORA
# ============================================================================

def chart_tdb(t):
    """Tableau : indicateurs DORA + coût, adoption IA, risque, chacun avec son
    mode de calcul, sa source (outillage prévu aux ministères) et son type."""
    x_axe, x_ind, x_calc, x_src, x_typ = 32, 118, 330, 648, 796
    y0, pitch = 130, 44
    n = len(TDB)
    h = y0 + n * pitch + 58
    s = svg_open(h, t)
    s += title_block(t, "Le tableau de bord, adossé à DORA",
                     "référentiel DevOps reconnu, complété de trois axes propres au contexte : coût, adoption IA, risque · lecture avant / après")
    hy = y0 - 30
    for x, lab in ((x_axe, "Axe"), (x_ind, "Indicateur"), (x_calc, "Mode de calcul"),
                   (x_src, "Source"), (x_typ, "Type de source")):
        s += txt(x, hy, lab, 11, t["sec"], "600")
    s += f'<line x1="32" y1="{hy + 12}" x2="888" y2="{hy + 12}" stroke="{t["baseline"]}" stroke-width="1.5"/>'
    axe_col = {"Vitesse": t["accent"], "Qualité": t["good"], "Coût": t["warn_text"],
               "Adoption IA": t["accent"], "Risque": t["status"]["bad"]}
    typ_style = {"outille": (["Outillé"], t["good"]),
                 "expertise": (["Expertise", "structurée"], t["accent"]),
                 "declaratif": (["Déclaratif", "corroboratif"], t["warn_text"])}
    for i, (axe, ind, calc, src, typ) in enumerate(TDB):
        y = y0 + i * pitch
        if i:
            s += f'<line x1="32" y1="{y - 14}" x2="888" y2="{y - 14}" stroke="{t["grid"]}" stroke-width="1"/>'
        base = y + 8
        s += txt(x_axe, base, axe, 11.5, axe_col[axe], "600")
        s += txt(x_ind, base, ind, 11.5, t["ink"], "600")
        for k, ln in enumerate(calc):
            s += txt(x_calc, base + k * 15, ln, 11, t["sec"])
        for k, ln in enumerate(src):
            s += txt(x_src, base + k * 15, ln, 11, t["sec"])
        lines, col = typ_style[typ]
        for k, ln in enumerate(lines):
            s += txt(x_typ, base + k * 15, ln, 11, col, "600")
    s += txt(32, h - 38, "DORA : fréquence de déploiement, lead time, taux d'échec des changements, "
             "temps de rétablissement.", 11.5, t["muted"])
    s += txt(32, h - 20, "Le tableau de bord vit en rétrospective bimensuelle pendant l'accompagnement, "
             "lu ensemble, équipe par équipe.", 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# Génération
# ============================================================================

CHARTS = {
    "01-kpi": chart_kpi,
    "02-maturite-org": chart_maturite_org,
    "07-impact": chart_impact,
    "04-roadmap": chart_roadmap,
    "05-matrice": chart_matrice,
    "06-bench": chart_bench,
    "08-usine": chart_usine,
    "09-tdb-dora": chart_tdb,
}

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    os.makedirs(out_dir, exist_ok=True)
    for name, fn in CHARTS.items():
        for mode in ("light", "dark"):
            body, _ = fn(THEMES[mode])
            path = os.path.join(out_dir, f"{name}-{mode}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(body)
            print(f"✓ {os.path.relpath(path, out_dir)}")

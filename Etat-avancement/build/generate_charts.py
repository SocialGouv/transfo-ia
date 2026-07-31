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

MAJ = "30 juillet 2026"

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

# Plan d'actions : (statut, nombre) — ordre = pipeline
ACTIONS = [("Réalisées", 8), ("En cours", 4), ("Planifiées", 10), ("À lancer", 3)]
A_CADRER = 10  # déclinaisons d'actions existantes restant à cadrer par périmètre

# KPI (label, valeur, sous-texte, sous-texte vert facultatif)
KPIS = [
    ("Use cases montés de niveau", "4", "· 1 sur DACCORD", "▲ 3 sur Egapro "),
    ("Actions réalisées", "8", "sur 25 engagées · 4 en cours", None),
    ("Équipes accompagnées", "6", "4 en actif · 4 métiers couverts", None),
    ("Prochain jalon", "3 août", "ateliers DA et Claude Enterprise", None),
]

# Jalons : (jour depuis le 13 juillet, lignes, statut done|next|futur, label au-dessus ?)
ROADMAP_SPAN_DAYS = 80  # 13 juillet → fin septembre
JALONS = [
    # certains jours sont décalés de 1 à 3 jours pour desserrer les étiquettes
    (3,  ["16 juillet", "Coaching dev augmenté", "équipe DACCORD"], "done", True),
    (14, ["28-30 juillet", "Référentiels archi", "CDP SIRENA · CEPS"], "done", False),
    (20, ["3 août", "Ateliers DA", "et Claude Enterprise"], "next", True),
    (25, ["6 août", "Atelier skills", "devs DACCORD"], "next", False),
    (35, ["Mi-août", "Formation PM/PO", "SIRENA · DACCORD"], "next", True),
    (39, ["Courant août", "Prototypes DSFR", "+ bench Bedrock"], "next", False),
    (47, ["Fin août", "Acculturation IA", "avec Igor"], "next", True),
    (57, ["8 septembre", "Atelier dev augmenté", "équipe VAO"], "futur", False),
    (78, ["Fin septembre", "Cartographie des comptes", "Bedrock (bénéficiaires)"], "futur", True),
]
ROADMAP_NOTE = ("Ensuite, moyen terme : communauté de référents IA, CI/CD augmentée, "
                "observabilité · long terme : harness souverain")

# Use cases montés de niveau, nommés (le décompte est calculé depuis la matrice)
MATURITE_IMPACT = {
    "Egapro": "pilotage · prototypes · pré-audit accessibilité",
    "DACCORD": "outils et system prompts communs",
}

# Impact des actions engagées : (libellé, nb de losanges, sous-texte)
IMPACT_LEVELS = [
    ("Déterminant", 3, "du concret dans le quotidien"),
    ("Élevé", 2, "acculturations et formations"),
    ("Modéré", 1, "cadrages, études, com"),
]
# (chantier, déterminant, élevé, modéré)
IMPACTS = [
    ("Egapro",     4, 0, 0),
    ("DACCORD",    3, 1, 0),
    ("SIRENA",     0, 1, 0),
    ("VAO",        0, 1, 0),
    ("Transverse", 4, 3, 8),
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
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#ffffff", "sec": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "baseline": "#383835", "border": "rgba(255,255,255,0.10)",
        "good": "#0ca30c", "accent": "#3987e5",
        "status": {"good": "#0ca30c", "mid": "#fab219", "bad": "#d03b3b"},
        "ramp5": ["#dfeafc", "#92bef2", "#4f92e8", "#2565bd", "#123f77"],
        "on_ramp5": ["#0b0b0b", "#0b0b0b", "#0b0b0b", "#ffffff", "#ffffff"],
        "impact3": ["#dfeafc", "#92bef2", "#4f92e8"],  # déterminant, élevé, modéré
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
# 2. Maturité moyenne par périmètre
# ============================================================================

def chart_maturite(t):
    """Tableau chiffré : nombre de use cases par niveau atteint (échelle 1 à 5) et par
    périmètre, avec les use cases montés de niveau nommés (l'impact de l'accompagnement)."""
    x_p = 32
    lvl_x = [140, 240, 340, 440, 540]  # colonnes niveaux 1 → 5
    x_imp = 600
    y0, pitch = 148, 52
    h = y0 + 4 * pitch + 40
    s = svg_open(h, t)
    s += title_block(t, "Niveaux atteints, périmètre par périmètre",
                     "nombre de use cases métier par niveau atteint (échelle de 1 à 5) · 10 use cases suivis par périmètre")
    # en-têtes : pastille de niveau, libellé dessous
    hy1, hy2 = y0 - 52, y0 - 30
    for lv, xc in enumerate(lvl_x, start=1):
        s += f'<rect x="{xc - 9}" y="{hy1 - 13}" width="18" height="18" rx="4" fill="{t["ramp5"][lv - 1]}"/>'
        s += txt(xc, hy1, str(lv), 11, t["on_ramp5"][lv - 1], "600", anchor="middle")
        s += txt(xc, hy2, NIVEAUX[lv - 1], 10.5, t["sec"], "600", anchor="middle")
    s += txt(x_imp, hy2, "▲ Montés de niveau grâce à l'accompagnement", 12, t["good"], "600")
    for i, p in enumerate(PERIMETRES[:4]):
        counts = {lv: 0 for lv in range(1, 6)}
        prog = 0
        for _, _, levels in MATRICE:
            v = levels[i]
            if v is None:
                continue
            if isinstance(v, tuple):
                counts[v[1]] += 1
                prog += 1
            else:
                counts[v] += 1
        y = y0 + i * pitch
        if i:
            s += f'<line x1="32" y1="{y - 26}" x2="888" y2="{y - 26}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(x_p, y + 7, p, 13.5, t["ink"], "600")
        for lv, xc in enumerate(lvl_x, start=1):
            n = counts[lv]
            if n:
                s += txt(xc, y + 8, str(n), 20, t["ink"], "600", anchor="middle", tabular=True)
            else:
                s += txt(xc, y + 7, "–", 13, t["muted"], anchor="middle")
        if prog:
            s += txt(x_imp, y + 8, f"▲ {prog}", 20, t["good"], "600", tabular=True)
            s += txt(x_imp + 46, y + 7, MATURITE_IMPACT.get(p, ""), 11, t["sec"])
        else:
            s += txt(x_imp + 14, y + 7, "–", 13, t["muted"], anchor="middle")
    s += txt(32, h - 20, "Le détail use case par use case figure dans la matrice de maturité "
             "de l'état d'avancement détaillé.", 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 2 bis. Impact des actions par chantier
# ============================================================================

def chart_impact(t):
    """Tableau chiffré : nombre d'actions engagées par niveau d'impact et par chantier,
    dans la même forme que le tableau des niveaux atteints (chiffres nus, axes lisibles)."""
    x_p = 32
    lvl_x = [300, 480, 650]   # colonnes déterminant, élevé, modéré
    x_tot = 800
    y0, pitch = 160, 46
    n = len(IMPACTS)
    total_y = y0 + n * pitch
    h = total_y + pitch + 40
    total = [sum(row[k + 1] for row in IMPACTS) for k in range(3)]
    s = svg_open(h, t)
    s += title_block(t, f"Impact des actions : {sum(total)} engagées, {total[0]} déterminantes",
                     "chaque action est classée selon ce qu'elle change pour les équipes")
    # en-têtes : losanges, libellé, définition courte
    hy1, hy2, hy3 = y0 - 64, y0 - 44, y0 - 28
    for k, (lab, nb, sub) in enumerate(IMPACT_LEVELS):
        xc = lvl_x[k]
        s += txt(xc, hy1, "◆" * nb, 12, t["impact3"][k], "600", anchor="middle", spacing="0.14em")
        s += txt(xc, hy2, lab, 12, t["sec"], "600", anchor="middle")
        s += txt(xc, hy3, sub, 10.5, t["muted"], anchor="middle")
    s += txt(x_tot, hy2, "Total", 12, t["sec"], "600", anchor="middle")
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
        s += txt(x_tot, y + 8, str(sum(counts)), 15, t["sec"], "600", anchor="middle", tabular=True)
    # ligne de total
    s += f'<line x1="32" y1="{total_y - 23}" x2="888" y2="{total_y - 23}" stroke="{t["baseline"]}" stroke-width="1.5"/>'
    s += txt(x_p, total_y + 7, "Total", 13.5, t["sec"], "600")
    for k, v in enumerate(total):
        s += txt(lvl_x[k], total_y + 8, str(v), 20, t["ink"], "600", anchor="middle", tabular=True)
    s += txt(x_tot, total_y + 8, str(sum(total)), 15, t["sec"], "600", anchor="middle", tabular=True)
    s += txt(32, h - 20, IMPACT_NOTE, 11.5, t["muted"])
    return s + "</svg>", h


# ============================================================================
# 3. Pipeline du plan d'actions
# ============================================================================

def chart_actions(t):
    """Quatre chiffres, un par statut du pipeline. Pas de graphique : des nombres."""
    total = sum(n for _, n in ACTIONS)
    h = 208
    s = svg_open(h, t)
    s += title_block(t, f"Plan d'actions : {total} actions engagées",
                     f"s'y ajoutent {A_CADRER} déclinaisons des actions réalisées, "
                     "à cadrer sur DACCORD, SIRENA et VAO")
    tile_w = (W - 64) / 4
    ly, vy = 102, 144
    for i, (label, n) in enumerate(ACTIONS):
        x = 32 + i * tile_w
        if i:
            s += f'<line x1="{x - 14}" y1="{ly - 14}" x2="{x - 14}" y2="{vy + 8}" stroke="{t["grid"]}" stroke-width="1"/>'
        if i == 0:
            s += txt(x, ly, label, 12.5, t["good"], "600")
            s += txt(x, vy, f"✓ {n}", 30, t["good"], "600", tabular=True)
        else:
            s += txt(x, ly, label, 12.5, t["sec"])
            s += txt(x, vy, str(n), 30, t["ink"], "600", tabular=True)
    s += txt(32, h - 24, "Le détail action par action figure dans l'état d'avancement détaillé.",
             11.5, t["muted"])
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
# Génération
# ============================================================================

CHARTS = {
    "01-kpi": chart_kpi,
    "02-maturite": chart_maturite,
    "07-impact": chart_impact,
    "03-actions": chart_actions,
    "04-roadmap": chart_roadmap,
    "05-matrice": chart_matrice,
    "06-bench": chart_bench,
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

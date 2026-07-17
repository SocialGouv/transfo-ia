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

MAJ = "17 juillet 2026"

# Matrice de maturité : niveau constaté par use case et périmètre.
# Valeurs : 1|2|3, (avant, après) pour une progression, "?" à évaluer, None = NA
PERIMETRES = ["Egapro", "DACCORD", "SIRENA", "VAO", "Transverse"]

MATRICE = [
    # (métier, use case, [Egapro, DACCORD, SIRENA, VAO, Transverse])
    ("Chefs de projet", "Piloter un projet développé avec l'IA",   [(1, 2), 1, "?", "?", None]),
    ("Chefs de projet", "Générer des tickets de spec",             [1, 1, "?", "?", None]),
    ("Chefs de projet", "Organiser le board (sprints, epics)",     [3, 1, "?", "?", None]),
    ("Designers",       "Générer des prototypes HTML/JS",          [(1, 3), "?", "?", "?", None]),
    ("Développeurs",    "Générer du code de qualité",              [2, 2, "?", 1, None]),
    ("Développeurs",    "Générer des tests",                       [3, 2, "?", 1, None]),
    ("Développeurs",    "Utiliser des orchestrations",             [3, 1, 1, 1, None]),
    ("Développeurs",    "Pré-auditer l'accessibilité",             [(1, 2), 1, 1, 1, None]),
    ("Développeurs",    "Pré-auditer la sécurité",                 [1, 1, 1, 1, None]),
    ("Développeurs",    "Outils &amp; system prompts communs",     [3, "?", 1, "?", None]),
    ("Architectes",     "Générer un dossier d'architecture (DA)",  [None, None, None, None, 1]),
]

# Plan d'actions : (statut, nombre) — ordre = pipeline
ACTIONS = [("Réalisées", 4), ("En cours", 3), ("Planifiées", 3), ("À lancer", 4)]
A_CADRER = 11  # déclinaisons d'actions existantes restant à cadrer par périmètre

# KPI (label, valeur, sous-texte, sous-texte vert facultatif)
KPIS = [
    ("Équipes accompagnées", "6", "4 en accompagnement actif", None),
    ("Métiers couverts", "4", "archi · CDP · design · dev", None),
    ("Use cases IA pilotés", "11", "maturité suivie de 1 à 3", None),
    ("Actions engagées", "14", "· 3 en cours", "✓ 4 réalisées "),
]

# Jalons : (jour depuis le 13 juillet, lignes, statut done|next|futur, label au-dessus ?)
JALONS = [
    (3,  ["16 juillet", "Coaching dev augmenté", "équipe DACCORD"], "done", True),
    (16, ["Fin juil. · août", "Atelier co-construction", "skills · agents · rules"], "next", False),
    (21, ["3 août", "Atelier DA architectes", "+ point Claude Enterprise"], "next", True),
    (56, ["Septembre", "Atelier dev augmenté", "équipe VAO"], "futur", False),
]
ROADMAP_NOTE = ("Ensuite, moyen terme : communauté de référents IA, CI/CD augmentée, "
                "observabilité · long terme : harness souverain")

MATURITE_NOTE = ("▲ Egapro : 3 use cases montés de niveau (pilotage, prototypes, "
                 "pré-audit d'accessibilité)")

# Bench harness : (stack, modèle, perf SWE-bench Verified %, label perf, prix sortie $/1M, label prix)
BENCH = [
    # (stack, modèle, perf %, label perf, prix $/1M, label prix, souveraineté)
    ("Claude Code", "Opus 4.8 · Anthropic", 88.6, "88,6 %", 25.0, "25 $",
     ("bad", "Non souveraine", "réservable aux externes")),
    ("Claude Code", "Opus 4.8 · Bedrock (internes)", 88.6, "88,6 %", 25.0, "≈25 $",
     ("mid", "Partielle", "sensible au CLOUD Act")),
    ("OpenCode", "DeepSeek V4 Pro · OpenRouter", 80.6, "80,6 %", 0.87, "0,87 $ (preview)",
     ("bad", "Non souveraine", "réservable aux externes")),
    ("OpenCode", "Albert · DeepSeek V4 Flash", 79.0, "≈79 %", 0.0, "gratuit (agents État)",
     ("good", "Souveraine", "SecNumCloud · État FR")),
    ("OpenCode", "GLM 5.2 · OpenRouter", 78.0, "≈78 %", 4.40, "4,40 $",
     ("bad", "Non souveraine", "réservable aux externes")),
]
BENCH_NOTE = ("Lecture : des performances proches (78 à 89 %), des prix de 0 à 25 $ ; "
              "seule la voie Albert, utilisable avec OpenCode, est pleinement souveraine")

# ============================================================================
# PALETTES (validées via dataviz/scripts/validate_palette.js, clair + sombre)
# ============================================================================

THEMES = {
    "light": {
        "surface": "#fcfcfb", "ink": "#0b0b0b", "sec": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "baseline": "#c3c2b7", "border": "rgba(11,11,11,0.10)",
        "good": "#006300", "accent": "#2a78d6",
        "status": {"good": "#0ca30c", "mid": "#fab219", "bad": "#d03b3b"},
        "ramp3": ["#86b6ef", "#2a78d6", "#104281"],            # niveaux 1-2-3
        "ramp4": ["#0d366b", "#1c5cab", "#3987e5", "#86b6ef"],  # pipeline réalisé → à lancer
        "on_ramp3": ["#0b0b0b", "#ffffff", "#ffffff"],
        "on_ramp4": ["#ffffff", "#ffffff", "#ffffff", "#0b0b0b"],
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#ffffff", "sec": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "baseline": "#383835", "border": "rgba(255,255,255,0.10)",
        "good": "#0ca30c", "accent": "#3987e5",
        "status": {"good": "#0ca30c", "mid": "#fab219", "bad": "#d03b3b"},
        "ramp3": ["#9ec5f4", "#3987e5", "#184f95"],
        "ramp4": ["#184f95", "#2a78d6", "#6da7ec", "#b7d3f6"],
        "on_ramp3": ["#0b0b0b", "#ffffff", "#ffffff"],
        "on_ramp4": ["#ffffff", "#ffffff", "#0b0b0b", "#0b0b0b"],
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
    """Composition par périmètre : nombre de use cases amenés à chaque niveau."""
    h = 366
    s = svg_open(h, t)
    s += title_block(t, "Niveaux apportés par l'accompagnement, par périmètre",
                     "nombre de use cases métier amenés à chaque niveau · 10 use cases suivis par périmètre")
    x0, x1, y0, bh = 150, 888, 96, 18
    # décomptes calculés depuis la matrice (colonnes équipes uniquement)
    for i, p in enumerate(PERIMETRES[:4]):
        counts = {1: 0, 2: 0, 3: 0, "?": 0}
        for _, _, levels in MATRICE:
            v = levels[i]
            if v is None:
                continue
            counts[v[1] if isinstance(v, tuple) else v] += 1
        y = y0 + i * 46
        s += txt(x0 - 14, y + 13, p, 13, t["ink"], "600", anchor="end")
        unit = (x1 - x0 - 3 * 2) / 10
        cx = x0
        segs = [(counts[3], t["ramp3"][2], t["on_ramp3"][2]),
                (counts[2], t["ramp3"][1], t["on_ramp3"][1]),
                (counts[1], t["ramp3"][0], t["on_ramp3"][0]),
                (counts["?"], None, t["muted"])]
        drawn = [g for g in segs if g[0]]
        for k, (n, fill, ink) in enumerate(drawn):
            w = n * unit
            if fill:
                s += rbar(cx, y, w, bh, fill, left=(k == 0), right=(k == len(drawn) - 1))
            else:
                s += (f'<rect x="{cx + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{bh - 1}" '
                      f'rx="4" fill="none" stroke="{t["grid"]}" stroke-width="1"/>')
            s += txt(cx + w / 2, y + 13.5, str(n), 12.5, ink, "600", anchor="middle")
            cx += w + 2
    ly = y0 + 4 * 46 + 16
    lx = 32
    for lv, lab in ((3, "Maîtrise"), (2, "En acquisition"), (1, "Découverte (démarrage)")):
        s += f'<rect x="{lx}" y="{ly}" width="18" height="18" rx="4" fill="{t["ramp3"][lv - 1]}"/>'
        s += txt(lx + 9, ly + 13, str(lv), 11, t["on_ramp3"][lv - 1], "600", anchor="middle")
        s += txt(lx + 25, ly + 13.5, lab, 12, t["sec"])
        lx += 25 + len(lab) * 7.0 + 26
    s += (f'<rect x="{lx}" y="{ly}" width="18" height="18" rx="4" fill="none" '
          f'stroke="{t["grid"]}" stroke-width="1"/>')
    s += txt(lx + 25, ly + 13.5, "restant à évaluer", 12, t["sec"])
    s += txt(32, h - 22, MATURITE_NOTE, 11.5, t["good"])
    return s + "</svg>", h


# ============================================================================
# 3. Pipeline du plan d'actions
# ============================================================================

def chart_actions(t):
    h = 202
    total = sum(n for _, n in ACTIONS)
    s = svg_open(h, t)
    s += title_block(t, f"Plan d'actions : {total} actions engagées",
                     f"et {A_CADRER} déclinaisons des actions ci-dessous à cadrer sur DACCORD, SIRENA et VAO")
    x, y, bh = 32, 92, 24
    span = W - 64 - 2 * (len(ACTIONS) - 1)
    cx = x
    for i, (label, n) in enumerate(ACTIONS):
        w = n / total * span
        s += rbar(cx, y, w, bh, t["ramp4"][i], left=(i == 0), right=(i == len(ACTIONS) - 1))
        s += txt(cx + w / 2, y + 16.5, str(n), 13, t["on_ramp4"][i], "600", anchor="middle")
        cx += w + 2
    # légende
    lx = 32
    for i, (label, n) in enumerate(ACTIONS):
        s += f'<rect x="{lx}" y="{y + 46}" width="12" height="12" rx="3" fill="{t["ramp4"][i]}"/>'
        s += txt(lx + 18, y + 56.5, f"{label} · {n}", 12.5, t["sec"])
        lx += 18 + (len(label) + 4) * 7.2 + 26
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
    px_day = (x1 - x0) / 62
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
                     "niveau auquel l'accompagnement a amené chaque fonction · une flèche = progression constatée")
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
            elif v == "?":
                s += (f'<rect x="{cx}" y="{yy}" width="{cell_w}" height="{cell_h}" rx="4" '
                      f'fill="none" stroke="{t["grid"]}" stroke-width="1"/>')
                s += txt(mid_x, mid_y, "?", 12, t["muted"], anchor="middle")
            else:
                lv = v[1] if isinstance(v, tuple) else v
                cell_txt = f"{v[0]} → {v[1]}" if isinstance(v, tuple) else str(lv)
                s += (f'<rect x="{cx}" y="{yy}" width="{cell_w}" height="{cell_h}" rx="4" '
                      f'fill="{t["ramp3"][lv - 1]}"/>')
                s += txt(mid_x, mid_y, cell_txt, 12.5, t["on_ramp3"][lv - 1], "600", anchor="middle")
    # légende
    items = [("1", "Découverte"), ("2", "En acquisition"), ("3", "Maîtrise")]
    lx = 32
    for i, (num, lab) in enumerate(items):
        s += f'<rect x="{lx}" y="{legend_y}" width="18" height="18" rx="4" fill="{t["ramp3"][i]}"/>'
        s += txt(lx + 9, legend_y + 13, num, 11, t["on_ramp3"][i], "600", anchor="middle")
        s += txt(lx + 25, legend_y + 13.5, lab, 12, t["sec"])
        lx += 25 + len(lab) * 7.0 + 26
    s += txt(lx + 4, legend_y + 13.5, "?  à évaluer", 12, t["sec"])
    lx += 4 + 12 * 7.0 + 26
    s += txt(lx + 4, legend_y + 13.5, "–  non applicable", 12, t["sec"])
    return s + "</svg>", h


# ============================================================================
# 6. Bench harness : performance vs prix
# ============================================================================

def chart_bench(t):
    """Trois colonnes : perf et prix en barres à base zéro, souveraineté en statut."""
    y0, rh = 122, 48
    n = len(BENCH)
    h = y0 + n * rh + 50
    px0, px1 = 244, 464   # panneau performance (0 → 100 %)
    qx0, qx1 = 520, 676   # panneau prix (0 → 25 $)
    sx = 750              # colonne souveraineté
    s = svg_open(h, t)
    s += title_block(t, "Coding agentique : les stacks au bench",
                     "SWE-bench Verified, prix en sortie ($ / 1M tokens) et souveraineté · tarifs vérifiés le 10/07/2026")
    s += txt(px0, 98, "Performance (SWE-bench)", 12, t["sec"], "600")
    s += txt(qx0, 98, "Prix en sortie / 1M", 12, t["sec"], "600")
    s += txt(sx, 98, "Souveraineté", 12, t["sec"], "600")
    for g, lab in ((0, "0"), (50, "50"), (100, "100 %")):
        gx = px0 + g / 100 * (px1 - px0)
        s += f'<line x1="{gx}" y1="{y0 - 8}" x2="{gx}" y2="{y0 + n * rh - 16}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(gx, y0 + n * rh + 2, lab, 11, t["muted"], anchor="middle")
    for g, lab in ((0, "0"), (10, "10"), (20, "20 $")):
        gx = qx0 + g / 25 * (qx1 - qx0)
        s += f'<line x1="{gx}" y1="{y0 - 8}" x2="{gx}" y2="{y0 + n * rh - 16}" stroke="{t["grid"]}" stroke-width="1"/>'
        s += txt(gx, y0 + n * rh + 2, lab, 11, t["muted"], anchor="middle")
    for i, (stack, modele, perf, perf_lab, prix, prix_lab, souv) in enumerate(BENCH):
        y = y0 + i * rh
        s += txt(32, y + 8, stack, 12.5, t["ink"], "600")
        s += txt(32, y + 24, modele, 11, t["muted"])
        pw = perf / 100 * (px1 - px0)
        s += rbar(px0, y, pw, 16, t["accent"])
        s += txt(px0 + pw + 8, y + 12.5, perf_lab, 11.5, t["ink"], "600")
        if prix > 0:
            qw = max(prix / 25 * (qx1 - qx0), 3)
            s += rbar(qx0, y, qw, 16, t["accent"])
            s += txt(qx0 + qw + 8, y + 12.5, prix_lab, 11.5, t["ink"], "600")
        else:
            s += txt(qx0 + 2, y + 12.5, prix_lab, 11.5, t["good"], "600")
        statut, lib, det = souv
        s += f'<circle cx="{sx + 4}" cy="{y + 6}" r="4.5" fill="{t["status"][statut]}"/>'
        s += txt(sx + 14, y + 10, lib, 12, t["ink"], "600")
        s += txt(sx, y + 26, det, 10.5, t["muted"])
    s += txt(32, h - 22, BENCH_NOTE, 11.5, t["sec"])
    return s + "</svg>", h


# ============================================================================
# Génération
# ============================================================================

CHARTS = {
    "01-kpi": chart_kpi,
    "02-maturite": chart_maturite,
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

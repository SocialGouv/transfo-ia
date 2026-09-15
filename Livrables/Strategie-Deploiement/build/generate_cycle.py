#!/usr/bin/env python3
"""Génère le schéma « cycle produit augmenté par l'IA » (clair + sombre).

Usage : python3 generate_cycle.py
Sorties :
  - ../assets/cycle-produit-ia-{light,dark}.svg (README, page Markdown, slides) ;
  - le fragment HTML du tableau de bord Suivi-Strategie-Adoption-IA.html (onglet
    « Cible »), réécrit entre les marqueurs <!-- cycle:start --> et <!-- cycle:end -->.
Même contenu, une seule source : la section CONTENU ci-dessous.

Matrice : cinq skills (colonnes, groupées par métier) × cinq lignes
(l'agent propose · l'humain décide · contexte · MCP · sortie), puis les soutiens
à la production, sous /implementation seulement : IDE et quality gate pendant,
CI/CD après le commit.
Palette : celle des visuels de l'état d'avancement (Etat-avancement/build/generate_charts.py).
Aucune dépendance externe. Le texte est coupé à la largeur des cellules par
un simple compte de caractères : relire le rendu après toute modification.
"""

import os

# ============================================================================
# CONTENU
# ============================================================================

TITLE = "Le cycle produit augmenté par l'IA : cinq skills, du besoin au code livré"
SUBTITLE = ("L'agent propose, la règle prouve, l'humain valide · chaque skill part des standards "
            "de l'équipe, parle aux outils par MCP et produit l'artefact qui alimente le skill suivant")

# (métier, colonnes couvertes)
ROLES = [("Responsable produit", [0]), ("Designer", [1, 2]), ("Développeur", [3, 4])]

SKILLS = [
    {
        "name": "/plan", "sub": "refinement du ticket",
        "agent": ["Challenge la précision du besoin, pose ses questions",
                  "Rédige le ticket au standard de l'équipe",
                  "Propose et complète les critères d'acceptation"],
        "human": ["Répond aux questions de l'agent",
                  "Valide le ticket et ses critères d'acceptation"],
        "ctx": ["Skill de challenge des imprécisions",
                "Standard de ticket de l'équipe",
                "Règles de rédaction des critères d'acceptation"],
        "mcp": ["Jira"],
        "out": "Ticket Jira précis, au standard, avec ses critères d'acceptation",
    },
    {
        "name": "/prototype", "sub": "du ticket au prototype",
        "agent": ["Lit le ticket",
                  "Génère un prototype selon les standards UX et UI, en composants DSFR"],
        "human": ["Montre le prototype aux utilisateurs",
                  "Recueille leurs retours, itère"],
        "ctx": ["Standards UX et UI"],
        "mcp": ["DSFR"],
        "out": "Prototype DSFR, montré aux utilisateurs",
    },
    {
        "name": "/maquette", "sub": "du prototype validé à Figma",
        "agent": ["Pousse le prototype dans Figma",
                  "Génère les maquettes selon les standards UI, en composants DSFR officiels",
                  "Respect strict du design system"],
        "human": ["Valide les maquettes",
                  "Partage des captures aux développeurs"],
        "ctx": ["Consigne : récupérer les composants DSFR officiels dans les maquettes"],
        "mcp": ["Figma"],
        "out": "Maquettes Figma du prototype validé, conformes DSFR",
    },
    {
        "name": "/plan-tech", "sub": "plan et revue d'impact",
        "agent": ["Lit le ticket et, au besoin, des captures des maquettes",
                  "Lit le code, écrit le plan d'implémentation aux standards de l'équipe",
                  "Évalue l'impact prévu sur le code"],
        "human": ["Tranche les choix techniques quand l'agent le demande",
                  "Valide le plan"],
        "ctx": ["Standards de développement",
                "Lecture du code",
                "Standards de sécurité (au besoin)"],
        "mcp": ["Jira"],
        "out": "Revue d'impact prévu sur le code + plan d'implémentation",
    },
    {
        "name": "/implementation", "sub": "code et tests",
        "agent": ["Implémente phase par phase",
                  "Agents codeur et testeur séparés",
                  "Pose le code et les tests : unitaires, intégration, e2e",
                  "S'arrête si un test casse sans l'avoir prévu dans la revue d'impact",
                  "Passe la quality gate avant commit"],
        "human": ["Choisit l'approche (test first, acceptance first, code first)",
                  "Relit avant de commiter"],
        "ctx": ["Revue d'impact prévu sur le code",
                "Plan d'implémentation",
                "Maquette au besoin"],
        "mcp": ["Jira", "Figma"],
        "out": "Code et tests, prêts pour la CI",
    },
]

# Lignes de la matrice : (clé, libellé, sous-libellé, style)
ROWS = [
    ("agent", "L'agent", "propose", "agent"),
    ("human", "L'humain", "décide", "human"),
    ("ctx", "Contexte", "les standards", "neutral"),
    ("mcp", "MCP", "outils branchés", "neutral"),
    ("out", "Sortie", "l'artefact", "out"),
]

# Soutiens à la production, sous /implementation : (moment, éléments)
SUPPORTS = [
    ("Pendant /implementation", ["IDE : ESLint",
                                 "Quality gate avant commit : RGAA, standards de qualité, build sans erreur"]),
    ("Après le commit", ["CI/CD : Sonar, pré-audit RGAA poussé, revue de code supplémentaire au besoin"]),
]

NOTES = [
    "Skill : commande (/plan, /prototype…) lancée dans le harness de l'équipe, OpenCode Desktop + Albert ou Claude Code + Bedrock · "
    "MCP : connecteur standard entre l'agent et un outil (Jira, Figma, DSFR)",
    "Le ticket Jira est le fil conducteur : produit par /plan, lu par /prototype, /plan-tech et /implementation",
    "Cible : des soutiens à la production aussi pour le produit (Definition of Ready outillée) et le design "
    "(audit DSFR / RGAA), paliers 2 et 3 de la checklist de déploiement",
]

# ============================================================================
# PALETTES (reprises de generate_charts.py, + accent « humain »)
# ============================================================================

THEMES = {
    "light": {
        "surface": "#fcfcfb", "ink": "#0b0b0b", "sec": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "baseline": "#c3c2b7", "border": "rgba(11,11,11,0.10)",
        "good": "#006300", "accent": "#2a78d6",
        "ramp5": ["#d8e8fb", "#8ab8f0", "#3987e5", "#1c5cab", "#0d366b"],
        "rail_ver": "#006300", "cell_gen": "#edf2fb", "cell_ver": "#ecf4ec",
        "human": "#a35d00", "on_human": "#ffffff", "cell_human": "#fbf1e1",
        "label_neutral": "#e1e0d9", "on_neutral": "#0b0b0b",
    },
    "dark": {
        "surface": "#1a1a19", "ink": "#ffffff", "sec": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "baseline": "#383835", "border": "rgba(255,255,255,0.10)",
        "good": "#0ca30c", "accent": "#3987e5",
        "ramp5": ["#dfeafc", "#92bef2", "#4f92e8", "#2565bd", "#123f77"],
        "rail_ver": "#006300", "cell_gen": "#20242c", "cell_ver": "#1f271f",
        "human": "#fab219", "on_human": "#0b0b0b", "cell_human": "#2a2418",
        "label_neutral": "#2c2c2a", "on_neutral": "#ffffff",
    },
}

FONT = "-apple-system,'Segoe UI',system-ui,Roboto,'Helvetica Neue',Arial,sans-serif"

# ============================================================================
# GÉOMÉTRIE
# ============================================================================

W = 1300
X_LABEL, LABEL_W = 32, 122
X0 = X_LABEL + LABEL_W + 12
GAP = 10
N = len(SKILLS)
COL_W = (W - 32 - X0 - (N - 1) * GAP) / N
PAD_X, PAD_Y = 12, 12
FS, LH = 12, 15.5           # corps de cellule
MAXC = 27                   # caractères par ligne à FS dans COL_W
ROW_GAP = 10
NOTCH = 12                  # profondeur des chevrons


# ============================================================================
# Aides SVG
# ============================================================================

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(s, maxc=MAXC):
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def txt(x, y, s, size, color, weight="normal", anchor="start", spacing=None):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def rect(x, y, w, h, fill, rx=8, stroke=None, dash=None):
    st = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    if dash:
        st += f' stroke-dasharray="{dash}"'
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}/>'


def chevron(x, y, w, h, fill, first=False, stroke=None):
    """Flèche-process : pointe à droite, encoche à gauche sauf pour la première."""
    n = NOTCH
    pts = [(x, y), (x + w - n, y), (x + w, y + h / 2), (x + w - n, y + h), (x, y + h)]
    if not first:
        pts.append((x + n, y + h / 2))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z"
    st = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{st}/>'


def bullets_lines(items):
    """Retourne [(is_first_line_of_item, texte)] pour une liste à puces."""
    out = []
    for it in items:
        for k, ln in enumerate(wrap(it, MAXC - 2)):
            out.append((k == 0, ln))
    return out


def col_x(j):
    return X0 + j * (COL_W + GAP)


# ============================================================================
# Rendu
# ============================================================================

def label_box(t, y, h, lab, sub, style):
    fill, color = {
        "agent": (t["ramp5"][3], "#ffffff"),
        "human": (t["human"], t["on_human"]),
        "neutral": (t["label_neutral"], t["on_neutral"]),
        "out": (t["ramp5"][4], "#ffffff"),
        "rail": (t["rail_ver"], "#ffffff"),
    }[style]
    s = rect(X_LABEL, y, LABEL_W, h, fill, rx=10)
    cx = X_LABEL + LABEL_W / 2
    if style == "rail":
        s += txt(cx, y + h / 2 - 10, "Soutiens à la", 12.5, color, "600", anchor="middle")
        s += txt(cx, y + h / 2 + 6, "production", 12.5, color, "600", anchor="middle")
        s += txt(cx, y + h / 2 + 23, sub, 11, color, anchor="middle")
    else:
        s += txt(cx, y + h / 2 - 2, lab, 12.5, color, "600", anchor="middle")
        s += txt(cx, y + h / 2 + 15, sub, 11, color, anchor="middle")
    return s


def render(t):
    s = ""
    y = 82

    # --- métiers (bandeaux) et skills ------------------------------------
    for role, cols in ROLES:
        x = col_x(cols[0])
        w = col_x(cols[-1]) + COL_W - x
        s += rect(x, y, w, 24, t["ramp5"][3], rx=6)
        s += txt(x + w / 2, y + 16.5, role.upper(), 11, "#ffffff", "600", anchor="middle", spacing="0.08em")
    y += 24 + 12
    for j, sk in enumerate(SKILLS):
        x = col_x(j)
        s += txt(x + 2, y + 14, sk["name"], 15.5, t["ink"], "600")
        s += txt(x + 2, y + 31, sk["sub"], 11.5, t["sec"])
    y += 44

    # --- matrice ---------------------------------------------------------
    for key, lab, sub, style in ROWS:
        if key in ("agent", "human", "ctx"):
            cells = [bullets_lines(sk[key]) for sk in SKILLS]
            nmax = max(len(c) for c in cells)
            h = PAD_Y * 2 + nmax * LH - 3
            s += label_box(t, y, h, lab, sub, style)
            for j, lines in enumerate(cells):
                x = col_x(j)
                if style == "agent":
                    s += rect(x, y, COL_W, h, t["cell_gen"])
                elif style == "human":
                    s += rect(x, y, COL_W, h, t["cell_human"])
                else:
                    s += rect(x, y, COL_W, h, t["surface"], stroke=t["grid"])
                ty = y + PAD_Y + FS - 1
                for k, (first, ln) in enumerate(lines):
                    if first:
                        s += f'<circle cx="{x + PAD_X + 3:.1f}" cy="{ty + k * LH - 4:.1f}" r="2" fill="{t["sec"]}"/>'
                    s += txt(x + PAD_X + 11, ty + k * LH, ln, FS, t["ink"])
        elif key == "mcp":
            h = 44
            s += label_box(t, y, h, lab, sub, style)
            for j, sk in enumerate(SKILLS):
                x = col_x(j)
                s += rect(x, y, COL_W, h, t["surface"], stroke=t["grid"])
                px = x + PAD_X
                for name in sk["mcp"]:
                    pw = len(name) * 7.2 + 18
                    s += rect(px, y + 12, pw, 20, t["surface"], rx=10, stroke=t["accent"])
                    s += txt(px + pw / 2, y + 26, name, 11.5, t["accent"], "600", anchor="middle")
                    px += pw + 6
        elif key == "out":
            cells = [wrap(sk["out"], MAXC - 3) for sk in SKILLS]
            nmax = max(len(c) for c in cells)
            h = PAD_Y * 2 + nmax * LH - 3
            s += label_box(t, y, h, lab, sub, style)
            for j, lines in enumerate(cells):
                x = col_x(j)
                # les chevrons se chevauchent légèrement pour enchaîner
                s += chevron(x - (0 if j == 0 else 2), y, COL_W + (GAP if j < N - 1 else 0) + (0 if j == 0 else 2),
                             h, t["ramp5"][3], first=(j == 0), stroke=t["surface"])
                ty = y + PAD_Y + FS - 1 + (nmax - len(lines)) * LH / 2
                for k, ln in enumerate(lines):
                    s += txt(x + PAD_X + (0 if j == 0 else NOTCH - 2), ty + k * LH, ln, FS, "#ffffff", "600")
        y += h + ROW_GAP

    # --- soutiens à la production : sous /implementation seulement ----------
    y += 8
    x = col_x(N - 1)
    blocks = [(title, [ln for it in items for ln in wrap(it, MAXC)]) for title, items in SUPPORTS]
    heights = [PAD_Y + 16 + len(lines) * LH + PAD_Y - 6 for _, lines in blocks]
    arrow_h = 26
    h = sum(heights) + arrow_h * (len(blocks) - 1)
    s += label_box(t, y, h, "Soutiens à la production", "vérifient le code", "rail")
    yy = y
    for i, ((title, lines), bh) in enumerate(zip(blocks, heights)):
        s += rect(x, yy, COL_W, bh, t["cell_ver"], stroke=t["good"])
        s += txt(x + PAD_X, yy + PAD_Y + 8, title.upper(), 10.5, t["good"], "600", spacing="0.06em")
        ty = yy + PAD_Y + 16 + FS
        for k, ln in enumerate(lines):
            s += txt(x + PAD_X, ty + k * LH, ln, FS, t["ink"])
        yy += bh
        if i < len(blocks) - 1:
            cx = x + PAD_X + 6
            s += f'<line x1="{cx}" y1="{yy + 3}" x2="{cx}" y2="{yy + arrow_h - 9}" stroke="{t["good"]}" stroke-width="2"/>'
            s += f'<path d="M{cx},{yy + arrow_h - 2} l-5,-8 h10 z" fill="{t["good"]}"/>'
            s += txt(cx + 12, yy + arrow_h / 2 + 4, "commit", 11, t["good"], "600")
            yy += arrow_h
    y += h + 26

    # --- notes -------------------------------------------------------------
    for i, note in enumerate(NOTES):
        s += txt(32, y + i * 17, note, 11.5, t["muted"])
    y += (len(NOTES) - 1) * 17 + 24

    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{y}" '
            f'viewBox="0 0 {W} {y}" font-family="{FONT}">'
            f'<rect x="0.5" y="0.5" width="{W-1}" height="{y-1}" rx="12" '
            f'fill="{t["surface"]}" stroke="{t["border"]}"/>')
    head += txt(32, 40, TITLE, 15.5, t["ink"], "600")
    head += txt(32, 61, SUBTITLE, 12.5, t["sec"])
    return head + s + "</svg>"


# ============================================================================
# Fragment HTML du tableau de bord (vrai tableau, en-têtes de lignes et colonnes)
# ============================================================================

DASHBOARD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "..", "..", "Suivi-Strategie-Adoption-IA.html")
MARK_START, MARK_END = "<!-- cycle:start", "<!-- cycle:end -->"


def html_fragment():
    e = esc
    o = ['<table class="cycle">', '<colgroup><col class="c0"><col span="5"></colgroup>', "<thead>"]
    o.append('<tr><td></td>' + "".join(
        f'<th scope="colgroup" colspan="{len(cols)}" class="role">{e(role)}</th>'
        for role, cols in ROLES) + "</tr>")
    o.append('<tr><td></td>' + "".join(
        f'<th scope="col" class="skill"><b>{e(sk["name"])}</b><i>{e(sk["sub"])}</i></th>'
        for sk in SKILLS) + "</tr>")
    o.append("</thead><tbody>")
    for key, lab, sub, style in ROWS:
        cells = []
        for j, sk in enumerate(SKILLS):
            if key in ("agent", "human", "ctx"):
                cells.append(f'<td class="cell {style}"><ul>'
                             + "".join(f"<li>{e(it)}</li>" for it in sk[key]) + "</ul></td>")
            elif key == "mcp":
                cells.append('<td class="cell">'
                             + "".join(f'<span class="pill">{e(m)}</span>' for m in sk["mcp"]) + "</td>")
            else:
                cells.append(f'<td class="chev{" first" if j == 0 else ""}">{e(sk["out"])}</td>')
        o.append(f'<tr><th scope="row" class="lab {style}">{e(lab)}<small>{e(sub)}</small></th>'
                 + "".join(cells) + "</tr>")
    sup = '<span class="commit">↓ commit</span>'.join(
        f'<div class="sup"><b>{e(title)}</b>' + "".join(f"<div>{e(it)}</div>" for it in items) + "</div>"
        for title, items in SUPPORTS)
    o.append('<tr><th scope="row" class="lab railv">Soutiens à la production<small>vérifient le code</small></th>'
             + "<td></td>" * (N - 1) + f'<td class="support">{sup}</td></tr>')
    o.append("</tbody></table>")
    o.append('<ul class="cycle-notes">' + "".join(f"<li>{e(n)}</li>" for n in NOTES) + "</ul>")
    return "\n".join(o)


def patch_dashboard():
    if not os.path.exists(DASHBOARD):
        print(f"! tableau de bord introuvable : {DASHBOARD}")
        return
    html = open(DASHBOARD, encoding="utf-8").read()
    a, b = html.find(MARK_START), html.find(MARK_END)
    if a < 0 or b < 0 or b < a:
        print("! marqueurs cycle:start / cycle:end absents du tableau de bord, fragment non écrit")
        return
    end_of_start = html.find("-->", a) + 3
    new = html[:end_of_start] + "\n" + html_fragment() + "\n" + html[b:]
    if new != html:
        open(DASHBOARD, "w", encoding="utf-8").write(new)
    print(f"✓ {os.path.basename(DASHBOARD)} (fragment onglet Cible)")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    os.makedirs(out_dir, exist_ok=True)
    for mode in ("light", "dark"):
        path = os.path.join(out_dir, f"cycle-produit-ia-{mode}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(THEMES[mode]))
        print(f"✓ {os.path.relpath(path, out_dir)}")
    patch_dashboard()

#!/usr/bin/env python3
"""Génère cible-slides.html : la page cible.html en diaporama, à présenter en partage d'écran.

Usage : python3 generate_cible_slides.py
Sortie : cible-slides.html à la racine du dépôt, réécrit en entier (ne pas l'éditer à la main).

Même contenu que cible.html, une seule source :
  - generate_cycle.py : SKILLS, ROLES, ROWS, STEPS, SUPPORTS, NOTES ;
  - generate_orchestrations.py : ORCHS, LEGEND, COMMON_RULES, EXAMPLE_NOTE et les schémas SVG de ../assets.
Les textes propres au deck (couverture, titres des slides, slide de fin) sont dans la section CONTENU.

Déroulé : couverture · vue d'ensemble · une slide par skill · soutiens à la production ·
lire un schéma · un exemple d'orchestration par skill · règles communes · des exemples, pas un standard.

Les schémas d'orchestration sont les SVG de la page, recadrés sur leurs couloirs (le titre et la légende
passent dans la slide) pour s'afficher le plus grand possible. Leur texte reste petit sur une slide :
un clic sur le schéma, ou la touche Z, l'agrandit autour du pointeur.
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from generate_cycle import SKILLS, ROLES, ROWS, STEPS, SUPPORTS, NOTES  # noqa: E402
from generate_orchestrations import (ORCHS, LEGEND, LANE_LABEL, LANE_WORD, COMMON_RULES, EXAMPLE_NOTE,  # noqa: E402
                                     THEMES, render, description)

OUT = os.path.join(HERE, "..", "..", "..", "cible-slides.html")
ASSETS_REL = "Livrables/Strategie-Deploiement/assets"
REPO = "https://github.com/SocialGouv/transfo-ia"

# ============================================================================
# CONTENU propre au deck
# ============================================================================

DECK_TITLE = "La cible : le cycle produit augmenté par l'IA"
KICKER = "Ministères sociaux · Transformation IA"
AUTHOR = "Selim Boukhari"
COVER_LEAD = ("Cinq skills, du besoin au code livré. Chacun part des standards de l'équipe (le contexte), "
              "parle aux outils par MCP et produit l'artefact qui alimente le suivant.")

OVERVIEW_TITLE = "Cinq skills, trois métiers : chaque skill produit l'artefact qui alimente le suivant"

# Titre de chaque slide de skill (à défaut : le sous-titre du skill dans generate_cycle.py)
HEADLINES = {
    "/plan": "Du besoin au ticket Jira précis, au standard de l'équipe",
    "/prototype": "Du ticket au prototype DSFR, montré aux utilisateurs",
    "/maquette": "Du prototype validé aux maquettes Figma, conformes DSFR",
    "/plan-tech": "Du ticket au plan d'implémentation, avec sa revue d'impact",
    "/implementation": "Du plan au code et aux tests, phase par phase",
}

SUPPORTS_TITLE = "Sous /implementation, trois soutiens à la production vérifient le code"
SUPPORTS_NOTE = ("Le bot de revue IA en CI fait partie des mécanismes proposés, à confirmer avec les équipes "
                 "(palier 4 de la checklist de déploiement).")

READ_TITLE = "Skill par skill, un exemple d'orchestration"
READ_LEAD = ("Cinq exemples, un par skill, pour se représenter une orchestration : les agents, le contexte qu'on leur "
             "donne, où l'humain intervient, les boucles et les retours. Des illustrations, pas des modèles à copier : "
             "chaque équipe compose la sienne.")
READ_HOW = "Un schéma se lit de gauche à droite, dans l'ordre des numéros."

RULES_TITLE = "Cinq règles valent pour les cinq orchestrations"

END_TITLE = "Des exemples, pas un standard"
# Trois lignes « libellé, sous-libellé, contenu », comme les slides de skill
END_ROWS = [
    ("/implementation s'inspire de ce qui tourne", "chez Egapro et DACCORD",
     ["Codeur et testeur séparés, front et back"]),
    ("Et y ajoute des mécanismes proposés", "à confirmer avec les équipes",
     ["Tests gelés", "Agent vérificateur", "Point de sauvegarde par phase", "Bot de revue IA en CI (palier 4)"]),
    ("Les quatre autres schémas", "",
     ["Ce qu'une orchestration pourrait être sur ces skills"]),
]
END_CLOSE = ("Chaque équipe compose son orchestration au palier 3 de la checklist de déploiement, "
             "qui décline cette cible en quatre paliers.")
END_LINKS = [
    ("Checklist de déploiement", f"{REPO}/blob/main/Livrables/Strategie-Deploiement/Checklist-IA-par-equipe.md"),
    ("La cible en page", "cible.html"),
    ("Dossier des schémas", f"{REPO}/tree/main/Livrables/Strategie-Deploiement/assets"),
]

# ============================================================================
# Aides
# ============================================================================


def e(s):
    return html.escape(s, quote=True)


def fr(s):
    """Texte échappé, avec les espaces insécables du français (pas de « : » ni de « ? » en début de ligne)."""
    s = e(s)
    s = re.sub(r" ([:;?!»])", " \\1", s)
    # un nom de skill (/plan, /implementation…) ne se coupe pas après sa barre oblique
    s = re.sub(r"(?<![\w/&;])(/[a-z][a-z-]+)", r'<span class="nw">\1</span>', s)
    return s.replace("« ", "« ")


def cap(s):
    return s[:1].upper() + s[1:]


def split_head(s, sep=" : "):
    """« tête : suite » -> (tête, suite) ; sans séparateur : (texte, '')."""
    a, _, b = s.partition(sep)
    return (a, b) if b else (s, "")


def role_of(i):
    return next(role for role, cols in ROLES if i in cols)


def rail(current=None):
    items = "".join(
        f'<li class="is-on" aria-current="step">{e(sk["name"])}</li>' if sk["name"] == current
        else f'<li>{e(sk["name"])}</li>' for sk in SKILLS)
    return f'<ol class="rail" aria-label="Les cinq skills du cycle">{items}</ol>'


def top(left, role=None):
    r = f'<span class="role">{fr(role)}</span>' if role else ""
    return (f'<div class="s-top">{left}<span class="s-right">{r}'
            f'<span class="s-page" data-page></span></span></div>')


def kicker(s):
    return f'<p class="s-kicker">{fr(s)}</p>'


def section(n, cls, title, body):
    return (f'<!-- ======================= {n} · {title} ======================= -->\n'
            f'<section class="slide {cls}" data-title="{e(title)}" aria-labelledby="t{n}">\n{body}\n</section>\n')


def bullets(items):
    return "<ul>" + "".join(f"<li>{fr(it)}</li>" for it in items) + "</ul>"


def row(style, lab, sub, content):
    small = f"<small>{fr(sub)}</small>" if sub else ""
    return (f'<div class="row row--{style}"><h3 class="lab">{fr(lab)}{small}</h3>'
            f'<div class="cell">{content}</div></div>')


# Pictogrammes de la légende, aux couleurs des schémas (les libellés disent la même chose en toutes lettres)
ICONS = {
    "num": '<circle cx="24" cy="20" r="17" fill="var(--navy)"/><text x="24" y="28" text-anchor="middle" '
           'font-size="22" font-weight="700" fill="#fff">1</text>',
    "ok": '<path d="M4 20H66" stroke="var(--green)" stroke-width="4"/><path d="M62 9 82 20 62 31z" fill="var(--green)"/>',
    "ko": '<path d="M4 20H66" stroke="var(--red)" stroke-width="4" stroke-dasharray="11 8"/>'
          '<path d="M62 9 82 20 62 31z" fill="var(--red)"/>',
    "amb": '<path d="M4 20H66" stroke="var(--amber)" stroke-width="4" stroke-dasharray="11 8"/>'
           '<path d="M62 9 82 20 62 31z" fill="var(--amber)"/>',
    "art": '<path d="M6 4H62L76 14V36H6z" fill="#fff" stroke="var(--sec)" stroke-width="2.5" stroke-dasharray="7 5"/>',
    "out": '<path d="M4 4H62L80 20 62 36H4z" fill="var(--navy)"/>',
}

# ============================================================================
# Slides
# ============================================================================


def slide_cover(n):
    chain = "".join(f"<li>{e(sk['name'])}</li>" for sk in SKILLS)
    mantra = "".join(
        f'<li class="m-{k}"><b>{fr(LANE_LABEL[ln][0])}</b> {fr(LANE_LABEL[ln][1])}</li>'
        for k, ln in (("agent", "A"), ("rule", "R"), ("human", "H")))
    body = (f'<p class="s-kicker">{fr(KICKER)}</p>\n'
            f'<h1 id="t{n}">{fr(DECK_TITLE)}</h1>\n'
            f'<p class="cover-lead">{fr(COVER_LEAD)}</p>\n'
            f'<ol class="chain" aria-label="Les cinq skills, dans l\'ordre du cycle">{chain}</ol>\n'
            f'<ul class="mantra">{mantra}</ul>\n'
            f'<p class="cover-foot">{fr(AUTHOR)} · <a href="cible.html">La même cible en page</a></p>')
    return section(n, "cover", "Couverture", body)


def slide_overview(n):
    o = [top(kicker("Vue d'ensemble")), f'<h2 id="t{n}">{fr(OVERVIEW_TITLE)}</h2>',
         '<table class="ov">',
         '<caption class="sr">Les cinq skills du cycle, par métier : ce que fait l\'agent, ce que décide '
         'l\'humain, l\'artefact produit</caption>',
         f'<colgroup><col class="c0"><col span="{len(SKILLS)}"></colgroup>', "<thead>",
         "<tr><td></td>" + "".join(
             f'<th scope="colgroup" colspan="{len(cols)}" class="role">{fr(role)}</th>' for role, cols in ROLES) + "</tr>",
         "<tr><td></td>" + "".join(
             f'<th scope="col" class="skill"><b>{e(sk["name"])}</b><i>{fr(sk["sub"])}</i></th>' for sk in SKILLS) + "</tr>",
         "</thead><tbody>"]
    labels = {key: (lab, sub) for key, lab, sub, _ in ROWS}
    for key, idx, cls in (("agent", 0, "agent"), ("human", 1, "human"), ("out", 2, "out")):
        lab, sub = labels[key]
        if key == "out":
            cells = "".join(f'<td class="chev{" first" if j == 0 else ""}">{fr(cap(st[idx]))}</td>'
                            for j, st in enumerate(STEPS))
        else:
            cells = "".join(f'<td class="c {cls}">{fr(cap(st[idx]))}</td>' for st in STEPS)
        o.append(f'<tr><th scope="row" class="tl {cls}">{fr(lab)}<small>{fr(sub)}</small></th>{cells}</tr>')
    o.append("</tbody></table>")
    # définitions (skill, MCP) et fil conducteur : les deux premières notes du tableau du cycle
    notes = []
    for part in NOTES[0].split(" · ") + [NOTES[1]]:
        head, rest = split_head(part)
        notes.append(f"<li><b>{fr(head)}</b>{fr(' : ' + rest) if rest else ''}</li>")
    o.append('<ul class="fnotes">' + "".join(notes) + "</ul>")
    return section(n, "overview", "Vue d'ensemble", "\n".join(o))


def slide_skill(n, i, sk):
    nxt = SKILLS[i + 1]["name"] if i + 1 < len(SKILLS) else None
    rows = []
    for key, lab, sub, style in ROWS:
        if key == "mcp":
            content = '<p class="pills">' + "".join(f'<span class="pill">{e(m)}</span>' for m in sk["mcp"]) + "</p>"
        elif key == "out":
            content = f'<p class="chev">{fr(sk["out"])}</p>'
            if nxt:
                content += f'<p class="next">puis <b>{e(nxt)}</b></p>'
        else:
            content = bullets(sk[key])
        rows.append(row(style, lab, sub, content))
    title = HEADLINES.get(sk["name"], cap(sk["sub"]))
    body = (top(rail(sk["name"]), role_of(i)) + "\n"
            + f'<h2 id="t{n}"><span class="cmd">{e(sk["name"])}</span> {fr(title)}</h2>\n'
            + '<div class="rows">\n' + "\n".join(rows) + "\n</div>")
    return section(n, "skill", sk["name"], body)


def slide_supports(n):
    rows = []
    for title, items, link in SUPPORTS:
        lab, sub = split_head(title, ", ")
        rows.append(row("rule", lab, sub, bullets(items)))
        if link:
            rows.append(f'<p class="then"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v14m-7-6 7 7 7-7" '
                        f'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" '
                        f'stroke-linejoin="round"/></svg>{fr(link["short"])}</p>')
    head, rest = split_head(NOTES[3])
    body = (top(rail("/implementation"), role_of(len(SKILLS) - 1)) + "\n"
            + f'<h2 id="t{n}">{fr(SUPPORTS_TITLE)}</h2>\n'
            + '<div class="rows rows--wide">\n' + "\n".join(rows) + "\n</div>\n"
            + f'<p class="callout"><b>{fr(head)}</b>{fr(" : " + rest)}</p>\n'
            + f'<div class="notes"><p>{fr(SUPPORTS_NOTE)}</p></div>')
    return section(n, "supports", "Soutiens à la production", body)


def slide_read(n):
    text = dict(LEGEND)
    lanes = []
    for k, ln, style in (("agent", "A", "agent"), ("rule", "R", "rule"), ("human", "H", "human")):
        big, small, extra = LANE_LABEL[ln]
        body = re.sub(r"^(l'agent propose|la règle prouve|l'humain décide)\s*[:=]\s*", "", text[k])
        lanes.append(row(style, big, small + (" · " + extra if extra else ""), f"<p>{fr(cap(body))}</p>"))
    marks = "".join(
        f'<li><svg viewBox="0 0 84 40" aria-hidden="true">{ICONS[k]}</svg><span>{fr(cap(text[k]))}</span></li>'
        for k in ("num", "art", "ok", "out", "ko", "amb") if k in text)
    body = (top(kicker("Exemples d'orchestration")) + "\n"
            + f'<h2 id="t{n}">{fr(READ_TITLE)}</h2>\n'
            + f'<p class="lead">{fr(READ_LEAD)}</p>\n'
            + f'<p class="how">{fr(READ_HOW)}</p>\n'
            + '<div class="rows">\n' + "\n".join(lanes) + "\n</div>\n"
            + f'<ul class="legend">{marks}</ul>')
    return section(n, "read", "Lire un schéma", body)


def slide_orch(n, o):
    i = next(j for j, sk in enumerate(SKILLS) if sk["name"] == o["skill"])
    sk = SKILLS[i]
    render(o, THEMES["light"], "light")          # calcule la géométrie : o["_size"], o["_band"]
    W, H = o["_size"]
    y0, y1 = o["_band"]
    cx, cw, ch = 14, W - 28, y1 - y0             # 14 px rognés de chaque côté : le cadre du SVG disparaît
    ratio = cw / ch
    steps = sorted([nd for nd in o["nodes"] if nd.get("step")], key=lambda nd: nd["step"])
    side = ratio < 1.5                           # schéma haut : la place libre à droite reçoit la liste des étapes
    base = min((1776 - 808) / cw, 760 / ch) if side else min(1776 / cw, 800 / ch)
    zoom = max(1.5, min(2.8, 2.5 / base))        # agrandi, le texte du schéma approche 27 px sur la scène
    title, lead = split_head(o["intro"])
    if not lead:
        title, lead = cap(sk["sub"]), o["intro"]
    chips = ""
    if o.get("chips"):
        chips = ('<p class="chips">' + "".join(f"<b>{e(c)}</b>" for c in o["chips"])
                 + f'{fr(o["chips_note"])}</p>')
    alt = (f"Exemple d'orchestration pour {o['skill']} : {sk['sub']}. Schéma en trois couloirs, l'agent propose, "
           f"la règle prouve, l'humain décide. Description textuelle : touche N.")
    src = f"{ASSETS_REL}/orchestration-{o['key']}-light.svg"
    fig = (f'<div class="fit"><div class="zoom" data-zoom style="--r:{ratio:.4f};--z:{zoom:.2f}">'
           f'<div class="zoom__in"><img src="{src}" alt="{e(alt)}" aria-describedby="desc-{o["key"]}" '
           f'style="width:{W / cw * 100:.3f}%;margin:-{y0 / cw * 100:.3f}% 0 0 -{cx / cw * 100:.3f}%"></div></div></div>')
    aside = ""
    if side:
        who = lambda nd: {"out": "sortie", "art": "entrée"}.get(nd["kind"], LANE_WORD[nd["lane"]])  # noqa: E731
        cls = lambda nd: {"out": "out"}.get(nd["kind"], {"A": "agent", "R": "rule", "H": "human"}[nd["lane"]])  # noqa: E731
        # les périmètres (back, front) passent au-dessus de la liste : une ligne de plus pour le schéma
        aside = (f'<div class="side">{chips}<ol class="steps" aria-label="Les {len(steps)} étapes, dans l\'ordre">'
                 + "".join(
                     f'<li><span class="n" aria-hidden="true">{nd["step"]}</span><span class="t">{fr(nd["title"])}</span>'
                     f'<span class="who who--{cls(nd)}">{fr(who(nd))}</span></li>' for nd in steps) + "</ol></div>")
        chips = ""
    note = EXAMPLE_NOTE.split(". ")[0] + "."
    body = (top(rail(o["skill"]), o["role"]) + "\n"
            + f'<h2 id="t{n}"><span class="tag">Exemple</span> <span class="cmd">{e(o["skill"])}</span> {fr(title)}</h2>\n'
            + f'<p class="lead">{fr(cap(lead))}</p>{chips}\n'
            + f'<div class="orch-body">{fig}{aside}</div>\n'
            + f'<p class="orch-foot"><span>{fr(note)}</span><span>Clic sur le schéma ou touche Z : agrandir · '
            + f'<a href="{src}" target="_blank" rel="noopener">Ouvrir le schéma seul</a></span></p>\n'
            + f'<div class="notes" id="desc-{o["key"]}">{description(o)}</div>')
    return section(n, "orch", f"Exemple {o['skill']}", body)


def slide_rules(n):
    items = []
    for k, rule in enumerate(COMMON_RULES, 1):
        head, rest = split_head(rule)
        items.append(f'<li><span class="n" aria-hidden="true">{k}</span><p><b>{fr(head)}</b>'
                     + (f"<span>{fr(cap(rest))}</span>" if rest else "") + "</p></li>")
    body = (top(kicker("Exemples d'orchestration")) + "\n"
            + f'<h2 id="t{n}">{fr(RULES_TITLE)}</h2>\n'
            + '<ol class="rules">' + "".join(items) + "</ol>")
    return section(n, "rules-slide", "Règles communes", body)


def slide_end(n):
    rows = "\n".join(
        row("neutral", lab, sub, bullets(items) if len(items) > 1 else f"<p>{fr(items[0])}</p>")
        for lab, sub, items in END_ROWS)
    links = " · ".join(f'<a href="{e(href)}">{fr(label)}</a>' for label, href in END_LINKS)
    body = (top(kicker("Exemples d'orchestration")) + "\n"
            + f'<h2 id="t{n}">{fr(END_TITLE)}</h2>\n'
            + f'<div class="rows rows--wide">\n{rows}\n</div>\n'
            + f'<p class="close">{fr(END_CLOSE)}</p>\n'
            + f'<p class="links">{links}</p>')
    return section(n, "end", END_TITLE, body)


def slides():
    out, n = [], 1
    out.append(slide_cover(n)); n += 1                                   # noqa: E702
    out.append(slide_overview(n)); n += 1                                # noqa: E702
    for i, sk in enumerate(SKILLS):
        out.append(slide_skill(n, i, sk)); n += 1                        # noqa: E702
    out.append(slide_supports(n)); n += 1                                # noqa: E702
    out.append(slide_read(n)); n += 1                                    # noqa: E702
    for o in ORCHS:
        out.append(slide_orch(n, o)); n += 1                             # noqa: E702
    out.append(slide_rules(n)); n += 1                                   # noqa: E702
    out.append(slide_end(n))
    return out


# ============================================================================
# Gabarit : styles et navigation
# ============================================================================

CSS = r"""
/* ==========================================================================
   La cible : le cycle produit augmenté par l'IA, version diaporama.
   Scène 1920 × 1080, mise à l'échelle de la fenêtre.
   Clavier : flèches ou espace pour avancer · F plein écran · Z agrandir un schéma ·
   N description du schéma · P imprimer.
   Une couleur garde le même sens partout, comme dans les schémas : bleu = l'agent,
   vert = la règle, ambre = l'humain, bleu nuit = l'artefact qui sort.
   Fichier généré par Livrables/Strategie-Deploiement/build/generate_cible_slides.py.
   ========================================================================== */
:root{
  --ink:#17181c; --sec:#4f5560; --line:#e3e6eb; --line-strong:#cfd4dc; --soft:#f3f4f6; --neutral:#e8eaee;
  --navy:#0d366b; --blue:#1c5cab; --blue-soft:#eaf1fc;
  --green:#0f6b0f; --green-soft:#e8f4e8;
  --amber:#9a5a00; --amber-soft:#fff3df;
  --red:#b42323;
  --pad:72px;
}
*,*::before,*::after{box-sizing:border-box}
html,body{margin:0;height:100%;background:#1b1f2a;overflow:hidden}
body{font-family:-apple-system,"Segoe UI",system-ui,Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;color:var(--ink)}
.nw{white-space:nowrap}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}

/* ---------- Scène ---------- */
.deck{position:fixed;inset:0}
.stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform:translate(-50%,-50%) scale(var(--scale,1));transform-origin:center}
.slide{position:absolute;inset:0;width:1920px;height:1080px;background:#fff;border-top:10px solid var(--navy);font-size:36px;line-height:1.25;overflow:hidden;display:none;flex-direction:column;padding:20px var(--pad) 30px}
.slide.is-active{display:flex}
.slide :where(h1,h2,h3,p,ul,ol,li,table,figure){margin:0;padding:0;font-size:inherit;line-height:inherit;font-weight:inherit}
.slide :where(ul,ol){list-style:none}
.slide :where(b,strong){font-weight:650}
.slide a{color:var(--blue);text-decoration:underline;text-underline-offset:.16em}
.slide a:focus-visible{outline:4px solid var(--blue);outline-offset:4px;border-radius:4px}

/* ---------- Bandeau du haut : où l'on est dans le cycle, le métier, la page ---------- */
.s-top{display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:48px;font-size:24px;line-height:1.2;color:var(--sec)}
.s-kicker{font-size:24px;line-height:1.2;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--sec)}
.s-right{display:flex;align-items:center;gap:22px;flex:none}
.s-page{font-variant-numeric:tabular-nums}
.role{background:var(--navy);color:#fff;border-radius:8px;padding:6px 16px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.rail{display:flex;gap:8px}
.rail li{padding:6px 18px;border-radius:999px;background:var(--soft);color:var(--sec);font-weight:600}
.rail li.is-on{background:var(--blue);color:#fff}

.slide h2{margin-top:12px;font-size:48px;line-height:1.16;font-weight:700;letter-spacing:-.015em}
.slide h2 .cmd{color:var(--blue)}
.slide h2 .tag{display:inline-block;vertical-align:.14em;margin-right:6px;padding:3px 14px;border:3px solid var(--navy);border-radius:8px;color:var(--navy);font-size:26px;line-height:1.2;letter-spacing:.08em;text-transform:uppercase;font-weight:700}
.lead{margin-top:8px;font-size:28px;line-height:1.3;color:var(--sec)}

/* ---------- Lignes « libellé · contenu » : la colonne d'un skill, mise à plat ---------- */
.rows{flex:1;min-height:0;display:flex;flex-direction:column;gap:12px;margin-top:20px}
.row{flex:1 1 auto;display:grid;grid-template-columns:var(--labw,240px) 1fr;gap:12px}
.lab{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;border-radius:14px;padding:10px 12px;font-size:32px;line-height:1.15;font-weight:650}
.lab small{margin-top:4px;font-size:24px;font-weight:400}
.cell{display:flex;align-items:center;border-radius:14px;padding:14px 30px;background:#fff;border:2px solid var(--line)}
.row--agent .lab{background:var(--blue);color:#fff}
.row--agent .cell{background:var(--blue-soft);border-color:transparent}
.row--human .lab{background:var(--amber);color:#fff}
.row--human .cell{background:var(--amber-soft);border-color:transparent}
.row--rule .lab{background:var(--green);color:#fff}
.row--rule .cell{background:var(--green-soft);border-color:transparent}
.row--neutral .lab{background:var(--neutral)}
.row--out .lab{background:var(--navy);color:#fff}
.row--out .cell{padding:0;border:0;gap:26px}
.cell ul{display:flex;flex-direction:column;gap:6px}
.cell li{position:relative;padding-left:30px}
.cell li::before{content:"";position:absolute;left:4px;top:.5em;width:10px;height:10px;border-radius:50%;background:var(--sec)}
.pill{display:inline-block;margin-right:14px;padding:3px 26px;border:3px solid var(--blue);border-radius:999px;background:#fff;color:var(--blue);font-weight:650}
.chev{flex:1;align-self:stretch;display:flex;align-items:center;padding:14px 64px 14px 30px;background:var(--blue);color:#fff;font-weight:650;border-radius:14px 0 0 14px;clip-path:polygon(0 0,calc(100% - 36px) 0,100% 50%,calc(100% - 36px) 100%,0 100%)}
.next{flex:none;font-size:30px;color:var(--sec)}
.next b{color:var(--blue)}

/* ---------- Couverture ---------- */
.cover{justify-content:center;padding-bottom:60px}
.cover h1{margin-top:18px;max-width:1500px;font-size:88px;line-height:1.08;font-weight:700;letter-spacing:-.025em}
.cover-lead{margin-top:30px;max-width:1500px;font-size:38px;line-height:1.32;color:var(--sec)}
.chain{display:flex;margin-top:52px}
.chain li{flex:1;display:flex;align-items:center;justify-content:center;height:92px;margin-right:-14px;padding:0 20px 0 34px;background:var(--blue);color:#fff;font-size:36px;font-weight:650;clip-path:polygon(0 0,calc(100% - 30px) 0,100% 50%,calc(100% - 30px) 100%,0 100%,30px 50%)}
.chain li:first-child{clip-path:polygon(0 0,calc(100% - 30px) 0,100% 50%,calc(100% - 30px) 100%,0 100%);border-radius:14px 0 0 14px}
.chain li:last-child{margin-right:0;background:var(--navy)}
.mantra{display:flex;gap:16px;margin-top:30px}
.mantra li{padding:12px 30px;border-radius:14px;font-size:36px;color:#fff}
.m-agent{background:var(--blue)}
.m-rule{background:var(--green)}
.m-human{background:var(--amber)}
.cover-foot{position:absolute;left:var(--pad);bottom:36px;font-size:26px;color:var(--sec)}

/* ---------- Vue d'ensemble : la matrice du cycle, en court ---------- */
table.ov{width:calc(100% + 20px);margin:12px -10px 0;table-layout:fixed;border-collapse:separate;border-spacing:10px;font-size:28px;line-height:1.28}
table.ov col.c0{width:186px}
table.ov th,table.ov td{padding:0;text-align:left;vertical-align:top;font-weight:400}
table.ov th.role{background:var(--navy);color:#fff;border-radius:8px;padding:6px 4px;text-align:center;font-size:26px;font-weight:600;letter-spacing:0;text-transform:none}
table.ov th.skill{padding:0 4px}
table.ov th.skill b{display:block;font-size:34px;font-weight:700;letter-spacing:-.015em;color:var(--blue)}
table.ov th.skill i{display:block;font-style:normal;font-size:25px;color:var(--sec)}
table.ov th.tl{border-radius:12px;padding:10px 6px;text-align:center;vertical-align:middle;font-size:28px;line-height:1.15;font-weight:650;color:#fff}
table.ov th.tl small{display:block;margin-top:3px;font-size:24px;font-weight:400}
table.ov th.tl.agent{background:var(--blue)}
table.ov th.tl.human{background:var(--amber)}
table.ov th.tl.out{background:var(--navy)}
table.ov td.c{border-radius:12px;padding:12px 16px}
table.ov td.c.agent{background:var(--blue-soft)}
table.ov td.c.human{background:var(--amber-soft)}
table.ov td.chev{display:table-cell;vertical-align:middle;padding:14px 26px 14px 34px;border-radius:0;background:var(--blue);color:#fff;font-weight:650;clip-path:polygon(0 0,calc(100% - 18px) 0,100% 50%,calc(100% - 18px) 100%,0 100%,18px 50%)}
table.ov td.chev.first{padding-left:18px;border-radius:12px 0 0 12px;clip-path:polygon(0 0,calc(100% - 18px) 0,100% 50%,calc(100% - 18px) 100%,0 100%)}
.fnotes{margin-top:auto;font-size:24px;line-height:1.32;color:var(--sec)}
.fnotes li + li{margin-top:4px}
.fnotes b{color:var(--ink)}

/* ---------- Soutiens à la production ---------- */
.rows--wide{--labw:400px;gap:6px}
.then{flex:none;display:flex;align-items:center;justify-content:center;gap:10px;width:var(--labw);font-size:26px;font-weight:650;color:var(--green)}
.then svg{width:30px;height:30px}
.callout{margin-top:18px;padding:16px 26px;border-left:8px solid var(--navy);border-radius:0 12px 12px 0;background:var(--soft);font-size:28px;line-height:1.3}

/* ---------- Lire un schéma ---------- */
.how{margin-top:14px;font-size:32px;font-weight:650}
.read .rows{flex:none;margin-top:14px}
.read .row{--labw:300px}
.read .cell{font-size:30px}
.legend{flex:1;display:grid;grid-template-columns:1fr 1fr;align-content:space-evenly;gap:8px 48px;margin-top:10px;font-size:28px;line-height:1.25}
.legend li{display:flex;align-items:center;gap:20px}
.legend svg{flex:none;width:84px;height:40px}

/* ---------- Un exemple d'orchestration ---------- */
.orch-body{flex:1;min-height:0;display:flex;gap:28px;margin-top:12px}
.fit{flex:1;min-width:0;min-height:0;container-type:size;display:flex;align-items:center;justify-content:center}
.zoom{position:relative;overflow:hidden;width:min(100cqw,calc(100cqh * var(--r)));height:min(100cqh,calc(100cqw / var(--r)));border:2px solid var(--line-strong);border-radius:16px;background:#fcfcfb;cursor:zoom-in}
.zoom.is-zoomed{cursor:zoom-out}
.zoom__in{position:absolute;inset:0;overflow:hidden;transform-origin:var(--ox,50%) var(--oy,50%);transition:transform .28s ease}
.zoom.is-zoomed .zoom__in{transform:scale(var(--z,2))}
.zoom img{display:block;max-width:none;height:auto}
.side{flex:0 0 780px;min-height:0;display:flex;flex-direction:column;gap:12px}
.steps{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:space-between;font-size:27px;line-height:1.2}
.steps li{display:flex;align-items:center;gap:14px}
.steps .n{flex:none;display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--navy);color:#fff;font-size:24px;font-weight:700}
.steps .t{font-weight:600}
.steps .who{margin-left:auto;padding-left:10px;font-size:24px;white-space:nowrap}
.who--agent{color:var(--blue)}
.who--rule{color:var(--green)}
.who--human{color:var(--amber)}
.who--out{color:var(--navy)}
.orch-foot{display:flex;justify-content:space-between;gap:24px;margin-top:10px;font-size:24px;line-height:1.3;color:var(--sec)}
.chips{font-size:24px;line-height:1.3;color:var(--sec)}
.chips b{display:inline-block;margin-right:8px;padding:0 14px;border:2px solid var(--blue);border-radius:999px;color:var(--blue);font-size:24px;letter-spacing:.06em;text-transform:uppercase}

/* ---------- Règles communes ---------- */
.rules{flex:1;display:flex;flex-direction:column;margin-top:20px}
.rules li{flex:1;display:grid;grid-template-columns:60px 1fr;gap:26px;align-items:center;border-top:2px solid var(--line)}
.rules .n{display:grid;place-items:center;width:60px;height:60px;border-radius:50%;background:var(--navy);color:#fff;font-size:32px;font-weight:700}
.rules b{display:block}
.rules p span{display:block;margin-top:2px;font-size:29px;line-height:1.28;color:var(--sec)}

/* ---------- Des exemples, pas un standard ---------- */
.end .rows--wide{--labw:540px;gap:12px}
.close{margin-top:20px;padding:26px 40px;border-radius:16px;background:var(--navy);color:#fff;font-size:42px;line-height:1.25;font-weight:650}
.links{margin-top:22px;font-size:28px;color:var(--sec)}

/* ---------- Description, aide, progression (hors slides) ---------- */
.notes{display:none}
.notes-panel{position:fixed;left:0;right:0;bottom:0;height:30vh;overflow:auto;background:#fff;border-top:4px solid var(--navy);padding:14px 28px 18px;font:17px/1.5 -apple-system,"Segoe UI",system-ui,Roboto,"Helvetica Neue",Arial,sans-serif;color:var(--ink);z-index:5}
.notes-panel[hidden]{display:none}
.notes-panel h2{margin:0 0 6px;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--navy)}
.notes-panel p{margin:4px 0}
.notes-panel ol{margin:4px 0;padding-left:24px}
body.with-notes .stage{top:35vh}
.deck-hint{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);padding:8px 16px;border-radius:6px;background:rgba(23,24,28,.88);color:#fff;font:500 14px/1.4 -apple-system,"Segoe UI",system-ui,Roboto,"Helvetica Neue",Arial,sans-serif;pointer-events:none;opacity:0;transition:opacity .4s;z-index:6}
.deck-hint.is-visible{opacity:1}
body.with-notes .deck-hint{bottom:calc(30vh + 16px)}
.deck-progress{position:fixed;left:0;bottom:0;height:4px;background:#5b9be6;transition:width .25s;z-index:6}
@media (prefers-reduced-motion:reduce){.deck-hint,.deck-progress,.zoom__in{transition:none}}

/* ---------- Impression et PDF : une slide par page ---------- */
@page{size:1920px 1080px;margin:0}
@media print{
  html,body{height:auto;overflow:visible;background:#fff}
  .deck{position:static}
  .stage{position:static;transform:none!important;width:auto;height:auto}
  .slide{position:relative;display:flex!important;break-after:page;page-break-after:always}
  .slide:last-child{break-after:auto;page-break-after:auto}
  .zoom__in{transform:none!important}
  .deck-hint,.deck-progress,.notes-panel,#annonce{display:none!important}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

JS = r"""
/* Navigation : flèches, espace, Début, Fin, chiffres · F plein écran · Z agrandir le schéma ·
   N description du schéma · P imprimer */
(() => {
  const TITLE = document.title;
  const stage = document.querySelector('.stage');
  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  const panel = document.getElementById('notes-panel');
  const annonce = document.getElementById('annonce');
  const shot = new URLSearchParams(location.search).has('shot');
  let cur = -1;

  slides.forEach((s, i) => s.querySelectorAll('[data-page]').forEach(el => { el.textContent = `${i + 1} / ${total}`; }));

  const hint = document.createElement('div');
  hint.className = 'deck-hint';
  hint.textContent = '← → pour naviguer · F plein écran · Z ou clic : agrandir un schéma · N description · P imprimer';
  hint.setAttribute('role', 'complementary');
  hint.setAttribute('aria-label', 'Raccourcis clavier');
  const progress = document.createElement('div');
  progress.className = 'deck-progress';
  progress.setAttribute('aria-hidden', 'true');
  if (!shot) document.body.append(hint, progress);

  function fit() {
    const h = window.innerHeight * (document.body.classList.contains('with-notes') ? 0.7 : 1);
    stage.style.setProperty('--scale', Math.min(window.innerWidth / 1920, h / 1080));
  }
  function renderNotes() {
    const n = slides[cur].querySelector('.notes');
    panel.innerHTML = '<h2>' + (slides[cur].dataset.title || '') + '</h2>' + (n ? n.innerHTML : '<p>Pas de description pour cette slide.</p>');
  }

  /* Loupe : le schéma grossit autour du pointeur, et suit ses déplacements */
  const zooms = Array.from(document.querySelectorAll('[data-zoom]'));
  function aim(box, e) {
    const r = box.getBoundingClientRect();
    const pc = (v, a, b) => Math.max(0, Math.min(100, (v - a) / b * 100)) + '%';
    box.style.setProperty('--ox', pc(e.clientX, r.left, r.width));
    box.style.setProperty('--oy', pc(e.clientY, r.top, r.height));
  }
  function unzoom() { zooms.forEach(b => b.classList.remove('is-zoomed')); }
  zooms.forEach(box => {
    box.addEventListener('click', e => {
      e.stopPropagation();
      if (!box.classList.contains('is-zoomed')) aim(box, e);
      box.classList.toggle('is-zoomed');
    });
    box.addEventListener('mousemove', e => { if (box.classList.contains('is-zoomed')) aim(box, e); });
  });
  /* ?zoom et ?notes dans l'adresse : ouvrir agrandi ou avec la description, pour une capture */
  const params = new URLSearchParams(location.search);
  if (params.has('zoom')) zooms.forEach(b => b.classList.add('is-zoomed'));

  function go(n) {
    n = Math.max(0, Math.min(total - 1, n));
    if (n === cur) return;
    if (cur >= 0) { slides[cur].classList.remove('is-active'); unzoom(); }
    slides[n].classList.add('is-active');
    cur = n;
    progress.style.width = `${total > 1 ? (cur / (total - 1)) * 100 : 100}%`;
    if (location.hash !== `#${cur + 1}`) history.replaceState(null, '', `#${cur + 1}`);
    const t = slides[cur].dataset.title || '';
    document.title = `${t} · ${TITLE}`;
    annonce.textContent = `Diapositive ${cur + 1} sur ${total} : ${t}`;
    if (!panel.hidden) renderNotes();
  }
  function fromHash() { const n = parseInt(location.hash.slice(1), 10); return Number.isFinite(n) ? n - 1 : 0; }
  function toggleNotes() {
    panel.hidden = !panel.hidden;
    document.body.classList.toggle('with-notes', !panel.hidden);
    if (!panel.hidden) renderNotes();
    fit();
  }

  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => go(fromHash()));
  document.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key;
    const onControl = e.target.closest && e.target.closest('a,button');   // un lien garde Entrée et Espace
    if (['ArrowRight', 'ArrowDown', 'PageDown'].includes(k) || (!onControl && [' ', 'Enter'].includes(k))) { e.preventDefault(); go(cur + 1); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') go(0);
    else if (k === 'End') go(total - 1);
    else if (/^[1-9]$/.test(k)) go(Number(k) - 1);
    else if (k === 'f' || k === 'F') { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen?.(); }
    else if (k === 'z' || k === 'Z') { const b = slides[cur].querySelector('[data-zoom]'); if (b) b.classList.toggle('is-zoomed'); }
    else if (k === 'Escape') unzoom();
    else if (k === 'n' || k === 'N') toggleNotes();
    else if (k === 'p' || k === 'P') window.print();
    else if (k === '?' || k === 'h' || k === 'H') { hint.classList.add('is-visible'); setTimeout(() => hint.classList.remove('is-visible'), 3200); }
  });
  document.querySelector('.deck').addEventListener('click', e => {
    if (e.target.closest('a,button')) return;
    if (e.clientX < window.innerWidth / 3) go(cur - 1); else go(cur + 1);
  });
  let x0 = null;
  document.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });
  window.addEventListener('beforeprint', unzoom);

  fit();
  go(fromHash());
  if (params.has('notes')) toggleNotes();
  if (!shot) { hint.classList.add('is-visible'); setTimeout(() => hint.classList.remove('is-visible'), 3600); }
})();
"""


def page():
    desc = ("La cible en diaporama : le cycle produit augmenté par l'IA, skill par skill, "
            "avec un exemple d'orchestration pour chacun.")
    return (
        "<!doctype html>\n"
        '<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="color-scheme" content="light">\n'
        f'<meta name="author" content="{e(AUTHOR)}">\n'
        f'<meta name="description" content="{e(desc)}">\n'
        f"<title>{e(DECK_TITLE)} (diaporama)</title>\n"
        f"<style>{CSS}</style>\n</head>\n<body>\n"
        "<!-- Généré par Livrables/Strategie-Deploiement/build/generate_cible_slides.py, ne pas éditer à la main -->\n"
        f'<main class="deck" aria-roledescription="diaporama" aria-label="{e(DECK_TITLE)}">\n<div class="stage">\n\n'
        + "\n".join(slides())
        + "\n</div>\n"
        '<p class="sr" id="annonce" aria-live="polite"></p>\n</main>\n'
        '<div class="notes-panel" id="notes-panel" role="complementary" aria-label="Description de la slide" '
        'tabindex="0" hidden aria-live="polite"></div>\n'
        f"<script>{JS}</script>\n</body>\n</html>\n")


if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page())
    print(f"✓ {os.path.basename(OUT)} ({len(slides())} slides)")

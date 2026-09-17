#!/usr/bin/env python3
"""Génère les schémas « exemple d'orchestration », un par skill du cycle produit (clair + sombre).
Des exemples, pas des standards : le titre, la description et une note sous la légende le rappellent.

Usage : python3 generate_orchestrations.py
Sorties :
  - ../assets/orchestration-{plan,prototype,maquette,plan-tech,implementation}-{light,dark}.svg ;
  - le fragment HTML du tableau de bord Suivi-Strategie-Adoption-IA.html (onglet « Cible »,
    sous le tableau du cycle), réécrit entre <!-- orchestrations:start --> et <!-- orchestrations:end -->.

Grammaire, pensée pour un public non technique : trois couloirs horizontaux, lus de gauche à droite,
les étapes du chemin nominal numérotées.
  L'agent propose (bleu) · La règle prouve, déterministe (vert : test, lint, contrôle) · L'humain décide (ambre).
Flèches : verte = ça passe · rouge pointillée = pas conforme, le motif repart à l'agent (3 essais au plus,
puis l'humain reprend la main) · ambre pointillée = un « non » ou des retours, rien n'est perdu.
Boucle déterministe = la règle ; boucle IA = un second agent, à contexte vierge, qui relit.

Palette et aides SVG : generate_cycle.py (une seule source pour le cycle et ses orchestrations).
Le texte est coupé par un compte de caractères (rendu déterministe d'une machine à l'autre) ; si PIL et DejaVu
Sans sont présents, le script mesure chaque ligne avec cette police large et signale ce qui déborderait.
Relire le rendu après modification.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_cycle import THEMES, FONT, SKILLS, esc, txt, rect, chevron  # noqa: E402

# ============================================================================
# CONTENU
# ============================================================================

def N(id, col, lane, kind, title, body=None, ctx=None, mcp=None, tag=None, step=None):
    """Nœud : couloir A (agent), R (règle), H (humain) ; kind : agent, rule, human, gate, stop, art, out ;
    step : numéro sur le chemin nominal (None = hors chemin : entrée, stop)."""
    return dict(id=id, col=col, lane=lane, kind=kind, title=title, body=body or [], ctx=ctx, mcp=mcp or [],
                tag=tag, step=step)


def E(f, t, route, kind="", label="", dash=False, dx=0, badge="", ch=0, tdx=0, gdx=0):
    """Arête : route v (verticale, même colonne, décalage dx ; dx négatif = étiquette à gauche),
    fwd (vers la droite), top (retour par le haut, canal ch, entrée dans la cible décalée de tdx,
    montée décalée de gdx dans l'interstice), bot (retour par le bas) ; kind '' | ok | ko | amb."""
    return dict(f=f, t=t, route=route, kind=kind, label=label, dash=dash, dx=dx, badge=badge, ch=ch,
                tdx=tdx, gdx=gdx)


STOP = ["3 échecs : l'orchestration s'arrête, le travail en cours reste"]
VERIF_TAG = "boucle IA · contexte vierge"

ORCHS = [
    {
        "key": "plan", "skill": "/plan", "role": "Responsable produit",
        "intro": "Du besoin brut au ticket publié : un agent questionne, un autre rédige, la règle contrôle la forme, "
                 "un troisième relit à froid, le responsable produit valide.",
        "nodes": [
            N("art", 0, "A", "art", "Le besoin", ["tel qu'il arrive : quelques lignes, un mail, un compte rendu"]),
            N("lance", 0, "H", "human", "Apporte le besoin", ["et lance /plan"], step=1),
            N("chal", 1, "A", "agent", "Agent challenge",
              ["Relève les imprécisions et les contradictions", "Pose ses questions, une à la fois"],
              ctx=["skill de challenge", "standard de ticket"], mcp=["Jira"], step=2),
            N("repond", 1, "H", "human", "Répond aux questions", ["jusqu'à ce qu'il n'en reste aucune de bloquante"], step=3),
            N("red", 2, "A", "agent", "Agent rédacteur",
              ["Rédige le ticket au standard de l'équipe", "Propose et complète les critères d'acceptation"],
              ctx=["standard de ticket", "règles de rédaction des critères"], step=4),
            N("forme", 2, "R", "rule", "Contrôle de forme",
              ["Sections obligatoires présentes", "Chaque critère d'acceptation suit le gabarit de l'équipe",
               "Aucun champ vide"], step=5),
            N("stop", 2, "H", "stop", "Reprend la main", STOP),
            N("relit", 3, "A", "agent", "Agent relecteur",
              ["Relit le ticket seul : testable ? complet ? sans ambiguïté ?"],
              ctx=["le ticket, pas la conversation"], tag=VERIF_TAG, step=6),
            N("valide", 4, "H", "gate", "Valide le ticket ?",
              ["oui : il est publié", "non : sa remarque repart à l'agent"], step=7),
            N("out", 4, "A", "out", "Ticket Jira publié", ["au standard, avec ses critères d'acceptation"],
              mcp=["Jira"], step=8),
        ],
        "edges": [
            E("lance", "art", "v", "amb"),
            E("art", "chal", "fwd"),
            E("chal", "repond", "v", "", "questions", dx=-16),
            E("repond", "chal", "v", "amb", "réponses", dx=16),
            E("chal", "red", "fwd", "ok"),
            E("red", "forme", "v", "", dx=-16),
            E("forme", "red", "v", "ko", dash=True, dx=16, badge="3 essais"),
            E("forme", "stop", "v", "ko"),
            E("forme", "relit", "fwd", "ok", "conforme"),
            E("relit", "red", "top", "ko", "refusé : le motif repart au rédacteur · 3 essais au plus", dash=True),
            E("relit", "valide", "fwd", "ok", "OK"),
            E("valide", "red", "bot", "amb", "non : sa remarque repart à l'agent rédacteur, le brouillon reste", dash=True),
            E("valide", "out", "fwd", "amb", "oui"),
        ],
    },
    {
        "key": "prototype", "skill": "/prototype", "role": "Designer",
        "intro": "Du ticket au prototype validé par les utilisateurs : l'agent génère en composants DSFR, la règle "
                 "vérifie les composants, un second agent relit, le designer montre et itère.",
        "nodes": [
            N("art", 0, "A", "art", "Le ticket", ["validé par /plan, avec ses critères d'acceptation"]),
            N("lance", 0, "H", "human", "Lance /prototype", ["sur le ticket"], step=1),
            N("proto", 1, "A", "agent", "Agent prototypeur",
              ["Lit le ticket", "Génère le prototype en composants DSFR"],
              ctx=["standards UX et UI"], mcp=["DSFR"], step=2),
            N("garde", 1, "R", "rule", "Gardes-fous",
              ["Chaque composant existe dans le DSFR", "Les fichiers annoncés sont bien produits",
               "La page s'affiche sans erreur"], step=3),
            N("stop", 1, "H", "stop", "Reprend la main", STOP),
            N("verif", 2, "A", "agent", "Agent vérificateur",
              ["Le prototype couvre-t-il le ticket ?", "Standards UX respectés ?"],
              ctx=["le ticket et le prototype"], tag=VERIF_TAG, step=4),
            N("montre", 3, "H", "gate", "Montre le prototype aux utilisateurs",
              ["retours : l'agent reprend, autant de fois qu'il faut", "OK : prototype validé"], step=5),
            N("out", 4, "A", "out", "Prototype DSFR validé", ["par les utilisateurs, prêt pour /maquette"], step=6),
        ],
        "edges": [
            E("lance", "art", "v", "amb"),
            E("art", "proto", "fwd"),
            E("proto", "garde", "v", "", dx=-16),
            E("garde", "proto", "v", "ko", dash=True, dx=16, badge="3 essais"),
            E("garde", "stop", "v", "ko"),
            E("garde", "verif", "fwd", "ok", "conforme"),
            E("verif", "proto", "top", "ko", "refusé : le motif repart au prototypeur · 3 essais au plus", dash=True),
            E("verif", "montre", "fwd", "ok", "OK"),
            E("montre", "proto", "bot", "amb", "retours des utilisateurs : l'agent reprend le prototype, autant de fois que nécessaire", dash=True),
            E("montre", "out", "fwd", "amb", "validé"),
        ],
    },
    {
        "key": "maquette", "skill": "/maquette", "role": "Designer",
        "intro": "Du prototype validé aux maquettes Figma : l'agent pousse le prototype dans Figma, la règle vérifie que "
                 "chaque composant vient de la bibliothèque DSFR officielle, un second agent contrôle la fidélité, le designer valide.",
        "nodes": [
            N("art", 0, "A", "art", "Le prototype validé", ["par les utilisateurs"]),
            N("lance", 0, "H", "human", "Lance /maquette", ["sur le prototype"], step=1),
            N("maq", 1, "A", "agent", "Agent maquetteur",
              ["Pousse le prototype dans Figma", "Génère les maquettes en composants DSFR officiels"],
              ctx=["consigne : composants DSFR officiels"], mcp=["Figma"], step=2),
            N("garde", 1, "R", "rule", "Gardes-fous",
              ["Chaque composant vient de la bibliothèque DSFR officielle, rien de redessiné",
               "Chaque écran du prototype a sa maquette"], step=3),
            N("stop", 1, "H", "stop", "Reprend la main", STOP),
            N("verif", 2, "A", "agent", "Agent vérificateur",
              ["Les maquettes sont-elles fidèles au prototype ?", "Design system respecté à la lettre ?"],
              ctx=["le prototype et les maquettes"], tag=VERIF_TAG, step=4),
            N("valide", 3, "H", "gate", "Valide les maquettes ?",
              ["oui : transmises au développeur", "non : sa remarque repart à l'agent"], step=5),
            N("out", 4, "A", "out", "Maquettes Figma validées", ["conformes DSFR, lues par /plan-tech"],
              mcp=["Figma"], step=6),
        ],
        "edges": [
            E("lance", "art", "v", "amb"),
            E("art", "maq", "fwd"),
            E("maq", "garde", "v", "", dx=-16),
            E("garde", "maq", "v", "ko", dash=True, dx=16, badge="3 essais"),
            E("garde", "stop", "v", "ko"),
            E("garde", "verif", "fwd", "ok", "conforme"),
            E("verif", "maq", "top", "ko", "refusé : le motif repart au maquetteur · 3 essais au plus", dash=True),
            E("verif", "valide", "fwd", "ok", "OK"),
            E("valide", "maq", "bot", "amb", "non : sa remarque repart à l'agent maquetteur, la version précédente reste", dash=True),
            E("valide", "out", "fwd", "amb", "oui"),
        ],
    },
    {
        "key": "plan-tech", "skill": "/plan-tech", "role": "Développeur",
        "intro": "Du ticket au plan d'implémentation : l'agent architecte lit le ticket, les maquettes et le code, la règle "
                 "vérifie que le plan est complet, un second agent mesure l'impact sur l'existant, le développeur tranche et valide.",
        "nodes": [
            N("art", 0, "A", "art", "Le ticket et les maquettes", ["ticket Jira, maquettes Figma"], mcp=["Jira", "Figma"]),
            N("lance", 0, "H", "human", "Lance /plan-tech", ["sur le ticket"], step=1),
            N("archi", 1, "A", "agent", "Agent architecte",
              ["Lit le ticket, les maquettes, le code", "Écrit le plan d'implémentation, phase par phase"],
              ctx=["standards de développement", "sécurité au besoin"], mcp=["Jira", "Figma", "DSFR"], step=2),
            N("tranche", 1, "H", "human", "Tranche les choix techniques", ["quand l'agent le demande"], step=3),
            N("ctrl", 2, "R", "rule", "Contrôle du plan",
              ["Chaque phase dit quels fichiers elle touche et comment vérifier qu'elle est finie",
               "Rien d'ambigu pour les agents qui suivront"], step=4),
            N("stop", 2, "H", "stop", "Reprend la main", STOP),
            N("impact", 3, "A", "agent", "Agent revue d'impact",
              ["Croise le plan et le code existant", "Liste ce qui va casser : comportements, tests"],
              ctx=["le plan, le code"], tag="contexte vierge", step=5),
            N("valide", 4, "H", "gate", "Valide le plan et les casses annoncées ?",
              ["oui : la revue d'impact fait foi pour /implementation", "non : le plan est corrigé, à la main ou par l'agent"], step=6),
            N("out", 4, "A", "out", "Plan + revue d'impact approuvés", ["prêts pour /implementation, back et front"], step=7),
        ],
        "edges": [
            E("lance", "art", "v", "amb"),
            E("art", "archi", "fwd"),
            E("archi", "tranche", "v", "", "questions", dx=-16),
            E("tranche", "archi", "v", "amb", "réponses", dx=16),
            E("archi", "ctrl", "fwd"),
            E("ctrl", "archi", "top", "ko", "plan incomplet : le motif repart à l'architecte · 3 essais au plus", dash=True),
            E("ctrl", "stop", "v", "ko"),
            E("ctrl", "impact", "fwd", "ok", "conforme"),
            E("impact", "valide", "fwd", "ok"),
            E("valide", "archi", "bot", "amb", "non : la remarque repart à l'architecte, le plan reste éditable", dash=True),
            E("valide", "out", "fwd", "amb", "oui"),
        ],
    },
    {
        "key": "implementation", "skill": "/implementation", "role": "Développeur",
        "chips": ["Back", "Front"],
        "chips_note": "une orchestration par périmètre, même déroulé",
        "intro": "Du plan approuvé au code mergé, phase par phase : le testeur pose les tests, le codeur les fait passer, "
                 "les gardes-fous et un vérificateur tranchent, le développeur relit chaque phase avant de la commiter. "
                 "Après le push, la CI/CD boucle avec la phase ; les contrôles de nuit, eux, ouvrent des tickets.",
        # sept colonnes dans la largeur commune, sans défilement : le vérificateur et la relecture humaine
        # partagent une colonne, et les colonnes denses (codeur, CI) sont plus larges que les autres
        "colw": [1.12, 1.14, 1.26, 1.12, 0.94, 1.22, 1.08],
        "nodes": [
            N("art", 0, "A", "art", "Plan + revue d'impact", ["du périmètre (back ou front) · phase N"]),
            N("lance", 0, "H", "human", "Lance la phase",
              ["/implementation, approche : test first (ici), acceptance first ou code first"], step=1),
            N("test", 1, "A", "agent", "Agent testeur",
              ["Écrit les tests de la phase : unitaires, intégration, bout en bout"],
              ctx=["plan", "critères d'acceptation", "standards de test"], mcp=["Playwright"], step=2),
            N("rouge", 1, "R", "rule", "Les tests échouent encore ?",
              ["Un test qui passe déjà ne teste rien", "Puis les tests sont gelés : le codeur ne pourra pas les modifier"], step=3),
            N("code", 2, "A", "agent", "Agent codeur",
              ["Écrit le code de la phase pour faire passer les tests"],
              ctx=["plan", "revue d'impact", "maquette au besoin", "standards de développement"], mcp=["Figma", "DSFR"], step=4),
            N("garde", 2, "R", "rule", "Gardes-fous",
              ["Tests gelés intacts, sinon restaurés", "Fichiers annoncés bien touchés", "Lint, build, tests verts",
               "Quality gate : RGAA, standards"], step=5),
            N("stop", 2, "H", "stop", "Reprend la main",
              ["un test casse sans avoir été prévu, ou 3 échecs : l'orchestration s'arrête"]),
            N("verif", 3, "A", "agent", "Agent vérificateur",
              ["La phase livre-t-elle tout ce que le plan annonçait ?"],
              ctx=["le plan de la phase, le code produit"], tag=VERIF_TAG, step=6),
            N("relit", 3, "H", "gate", "Relit la phase, commite ?",
              ["oui : commit · non : sa remarque repart au codeur", "après la dernière phase : pousse"], step=7),
            N("save", 4, "R", "rule", "Point de sauvegarde",
              ["Le commit de la phase", "Si la suite casse, on revient ici"], step=8),
            N("out", 4, "A", "out", "Code + tests poussés", ["la CI/CD prend le relais"], step=9),
            N("bot", 5, "A", "agent", "Bot de revue IA",
              ["Relit la diff : standards, lisibilité, régressions",
               "Approuve ou demande des changements"],
              ctx=["standards de développement", "le plan de la phase"], tag=VERIF_TAG, step=10),
            N("ci", 5, "R", "rule", "La PR peut-elle passer ?",
              ["Revue du bot IA approuvée", "Sonar vert : couverture, duplication, vulnérabilités",
               "Lint, build et tests rejoués"], step=11),
            N("merge", 5, "H", "human", "Valide et merge",
              ["arbitre les remarques du bot, puis merge"], step=12),
            N("livre", 6, "A", "out", "Code mergé", ["la fonctionnalité part en recette"], step=13),
            N("nuit", 6, "R", "rule", "Chaque nuit, hors boucle",
              ["Pré-audit RGAA poussé", "Analyse de sécurité : dépendances, code",
               "Trop long pour tourner à chaque push"], step=14),
            N("tickets", 6, "H", "human", "Les écarts ouvrent des tickets",
              ["corrigés dans un prochain ticket, pas dans la phase en cours"], step=15),
        ],
        "edges": [
            E("lance", "art", "v", "amb"),
            E("art", "test", "fwd"),
            E("test", "rouge", "v", "", dx=-16),
            E("rouge", "test", "v", "ko", dash=True, dx=16, badge="3 essais"),
            E("rouge", "code", "fwd", "ok", "oui"),
            E("code", "garde", "v", "", dx=-16),
            E("garde", "code", "v", "ko", dash=True, dx=16, badge="3 essais"),
            E("garde", "stop", "v", "ko"),
            E("garde", "verif", "fwd", "ok", "tout est vert"),
            E("verif", "code", "top", "ko", "refusé : le motif repart au codeur · 3 essais au plus", dash=True),
            E("verif", "relit", "v", "ok", "OK", dx=-16),
            E("relit", "code", "top", "amb", "non : sa remarque repart au codeur", dash=True, ch=1, tdx=18),
            E("relit", "save", "fwd", "amb", "oui"),
            E("save", "out", "v", "ok", "dernière phase", dx=-1),
            E("save", "test", "bot", "ok", "phase suivante : le testeur reprend avec la phase N+1"),
            E("out", "bot", "fwd", ""),
            E("bot", "ci", "v", "", dx=-16),
            E("ci", "code", "top", "ko",
              "revue rejetée ou issue Sonar : la correction rejoint le plan de la phase, le codeur reprend",
              dash=True, ch=2, tdx=-18, gdx=12),
            E("ci", "merge", "v", "ok", "tout est vert", dx=-16),
            E("merge", "livre", "fwd", "amb"),
            E("livre", "nuit", "v", "", dx=-16),
            E("nuit", "tickets", "v", "ko", "écarts", dash=True, dx=0),
        ],
    },
]

EXAMPLE_NOTE = ("Un exemple, pas un standard : un déroulé possible parmi d'autres. Chaque équipe compose le sien, "
                "avec ses standards, ses outils et ses gardes-fous.")

COMMON_RULES = [
    "Trois essais au plus par agent : au-delà, l'orchestration s'arrête proprement et l'humain reprend la main. Jamais de boucle sans fin, un coût borné.",
    "Un « non » à une validation ne détruit rien : le brouillon, le plan ou la version précédente restent, la remarque repart à l'agent.",
    "Chaque étape validée est un point de sauvegarde : si la suite casse, on y revient au lieu de tout refaire.",
    "Chaque agent démarre avec un contexte vierge et ne reçoit que ce qui le concerne : le relecteur lit le ticket, pas la conversation qui l'a produit.",
    "La règle avant l'agent : quand un test, un lint ou un contrôle peut trancher (boucle déterministe), c'est lui qui tranche ; un second agent relit ce qu'aucune règle ne sait prouver (boucle IA).",
]

# ============================================================================
# GÉOMÉTRIE
# ============================================================================

W = 1120                    # largeur par défaut ; une orchestration dense peut demander la sienne (clé « W »)
X_LABEL, LABEL_W = 24, 92
X0 = X_LABEL + LABEL_W + 16
XR = 24
GAP = 30                    # entre colonnes (les retours passent dans ces couloirs verticaux)
INSET = 2                   # nœud plus étroit que sa colonne
PADX, PADY = 10, 9
FS_T, LH_T = 12, 15         # titre de nœud
FS_B, LH_B = 11, 13.5       # corps
FS_C, LH_C = 10.5, 13       # contexte
FS_L = 10.5                 # étiquettes de flèches
PILL_H, PILL_GAP = 18, 5
ILG = 48                    # espace entre couloirs
CHAN = 26                   # hauteur d'un canal de retour
LANES = ["A", "R", "H"]
LANE_LABEL = {"A": ("L'agent", "propose", ""), "R": ("La règle", "prouve", "déterministe"), "H": ("L'humain", "décide", "")}
BAD = {"light": "#b42323", "dark": "#f07070"}
PILL = {"light": THEMES["light"]["ramp5"][3], "dark": THEMES["dark"]["accent"]}   # contraste ≥ 4,5 sur le fond
LANE_BG = {"light": "#f5f5f2", "dark": "#232322"}
WARNINGS = []

# Contrôle de débordement : mesure réelle avec DejaVu Sans, police nettement plus large que Segoe UI ou
# Noto Sans ; une ligne qui tient ici tient chez le client. Optionnel (PIL + police présents), informatif.
try:
    from PIL import ImageFont
    _FD = "/usr/share/fonts/truetype/dejavu/"
    _FONTS = {False: ImageFont.truetype(_FD + "DejaVuSans.ttf", 100),
              True: ImageFont.truetype(_FD + "DejaVuSans-Bold.ttf", 100)}
except Exception:  # noqa: BLE001
    _FONTS = None


def wrap_px(s, width, fs, bold=False):
    maxc = max(6, int(width / (fs * (0.58 if bold else 0.53))))
    lines, cur = [], ""
    for w in s.split(" "):
        if not w:
            continue
        if cur and len(cur) + 1 + len(w) > maxc:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    if cur:
        lines.append(cur)
    return lines


def text_w(s, fs, bold=False):
    return len(s) * fs * (0.58 if bold else 0.52)


def check_fit(where, lines, width, fs, bold=False):
    if where is None or _FONTS is None:
        return
    for ln in lines:
        w = _FONTS[bold].getlength(ln) * fs / 100
        if w > width:
            WARNINGS.append(f"{where} : « {ln} » déborderait de {w - width:.0f} px avec une police large")


def itxt(x, y, s, size, color, anchor="start"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" font-style="italic" '
            f'text-anchor="{anchor}">{esc(s)}</text>')


def label(t, x, y, s, size, color, anchor="middle", weight="600"):
    """Étiquette sur fond opaque (un rectangle, pas un halo paint-order : rendu identique partout)."""
    w = text_w(s, size, True) + 8
    x0 = {"middle": x - w / 2, "start": x - 4, "end": x - w + 4}[anchor]
    return (rect(x0, y - size, w, size + 4, t["surface"], rx=3)
            + f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" font-weight="{weight}" '
              f'text-anchor="{anchor}">{esc(s)}</text>')


def nbsp(s):
    """Typographie française : l'espace devant ? et : est insécable, la césure ne les isole pas."""
    return s.replace(" ?", " ?").replace(" :", " :")


# ============================================================================
# Nœuds
# ============================================================================

def measure(n, nw, where=None):
    """where : préfixe des alertes de débordement, None = pas de contrôle (rendu sombre, déjà contrôlé)."""
    inner = nw - 2 * PADX - (4 if n["kind"] == "agent" else 0)
    if where is None:
        check = lambda *a, **k: None  # noqa: E731
    else:
        check = check_fit
    n = dict(n, title=nbsp(n["title"]), body=[nbsp(b) for b in n["body"]])
    L = {"tag": [n["tag"]] if n.get("tag") else [], "title": wrap_px(n["title"], inner, FS_T, True)}
    check(f"{where} {n['id']} titre", L["title"], inner, FS_T, True)
    bullets = len(n["body"]) > 1 and n["kind"] in ("agent", "rule")
    body = []
    for it in n["body"]:
        for k, ln in enumerate(wrap_px(it, inner - (9 if bullets else 0), FS_B)):
            body.append((bullets and k == 0, ln))
    check(f"{where} {n['id']} corps", [ln for _, ln in body], inner - (9 if bullets else 0), FS_B)
    L["body"] = body
    L["ctx"] = wrap_px("contexte : " + " · ".join(n["ctx"]), inner, FS_C) if n.get("ctx") else []
    check(f"{where} {n['id']} contexte", L["ctx"], inner, FS_C)
    L["mcp"] = n["mcp"]
    h = PADY * 2
    if L["tag"]:
        h += 13
    h += len(L["title"]) * LH_T
    if body:
        h += 3 + len(body) * LH_B
    if L["ctx"]:
        h += 4 + len(L["ctx"]) * LH_C
    if n["mcp"]:
        h += 7 + PILL_H
    return L, h


def pills(t, mode, x, y, names, on_dark=False):
    s, off = "", 0
    col = "#ffffff" if on_dark else PILL[mode]
    for name in names:
        pw = len(name) * 6.6 + 16
        s += rect(x + off, y, pw, PILL_H, "none" if on_dark else t["surface"], rx=9, stroke=col)
        s += txt(x + off + pw / 2, y + 13, name, 10.5, col, "600", anchor="middle")
        off += pw + PILL_GAP
    return s


def doc_shape(x, y, w, h, fill, stroke):
    f = 10
    d = f"M{x},{y} h{w - f} l{f},{f} v{h - f} h{-w} z"
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1.2" stroke-dasharray="4 3"/>'
            f'<path d="M{x + w - f},{y} v{f} h{f}" fill="none" stroke="{stroke}" stroke-width="1.2"/>')


def step_badge(t, x, y, n):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{t["ramp5"][4]}" stroke="{t["surface"]}" stroke-width="2"/>'
            + txt(x, y + 4, str(n), 11, "#ffffff", "700", anchor="middle"))


def draw_node(t, mode, n, x, y, nw, L, h, bad):
    kind = n["kind"]
    ink, sec = t["ink"], t["sec"]
    s = ""
    title_col, body_col, ctx_col, on_dark = ink, ink, sec, False
    if kind == "agent":
        s += rect(x, y, nw, h, t["cell_gen"], rx=9)
        s += f'<rect x="{x:.1f}" y="{y + 8:.1f}" width="3" height="{h - 16:.1f}" rx="1.5" fill="{t["ramp5"][3]}"/>'
    elif kind == "rule":
        s += rect(x, y, nw, h, t["cell_ver"], rx=9, stroke=t["good"])
        title_col = t["good"]
    elif kind == "human":
        s += rect(x, y, nw, h, t["cell_human"], rx=9)
        title_col = t["human"]
    elif kind == "gate":
        s += rect(x, y, nw, h, t["cell_human"], rx=14, stroke=t["human"])
        title_col = t["human"]
    elif kind == "stop":
        s += rect(x, y, nw, h, t["surface"], rx=9, stroke=bad, dash="4 3")
        title_col, body_col = bad, sec
    elif kind == "art":
        s += doc_shape(x, y, nw, h, t["surface"], t["sec"])
        body_col = sec
    elif kind == "out":
        s += chevron(x, y, nw + 10, h, t["ramp5"][4], first=True)
        title_col = body_col = ctx_col = "#ffffff"
        on_dark = True
    tx = x + PADX + (4 if kind == "agent" else 0)
    ty = y + PADY
    if L["tag"]:
        s += txt(tx, ty + 9, L["tag"][0].upper(), 9.5, PILL[mode] if not on_dark else "#fff", "600", spacing="0.06em")
        ty += 13
    for ln in L["title"]:
        s += txt(tx, ty + FS_T, ln, FS_T, title_col, "600")
        ty += LH_T
    if L["body"]:
        ty += 3
        indent = 9 if any(b for b, _ in L["body"]) else 0
        for is_bullet, ln in L["body"]:
            if is_bullet:
                s += f'<circle cx="{tx + 3:.1f}" cy="{ty + FS_B - 4:.1f}" r="1.8" fill="{body_col}"/>'
            s += txt(tx + indent, ty + FS_B, ln, FS_B, body_col)
            ty += LH_B
    if L["ctx"]:
        ty += 4
        for ln in L["ctx"]:
            s += itxt(tx, ty + FS_C, ln, FS_C, ctx_col)
            ty += LH_C
    if L["mcp"]:
        ty += 7
        s += pills(t, mode, tx, ty, L["mcp"], on_dark)
    if n.get("step"):
        s += step_badge(t, x + 1, y + 1, n["step"])
    return s


# ============================================================================
# Arêtes
# ============================================================================

def edge_color(t, kind, bad):
    return {"ok": t["good"], "ko": bad, "amb": t["human"]}.get(kind, t["sec"])


def draw_edge(t, key, e, P, y_top, y_bot, bad):
    a, b = P[e["f"]], P[e["t"]]
    col = edge_color(t, e["kind"], bad)
    r = e["route"]
    lab = None  # (x, y, anchor)
    if r == "v":
        xa = a["cx"] + e["dx"]
        if a["cy"] < b["cy"]:
            y0, y1 = a["y"] + a["h"], b["y"] - 2
        else:
            y0, y1 = a["y"], b["y"] + b["h"] + 2
        d = f"M{xa:.1f},{y0:.1f} L{xa:.1f},{y1:.1f}"
        ym = (y0 + y1) / 2
        lab = (xa + 7, ym + 4, "start") if e["dx"] >= 0 else (xa - 7, ym + 4, "end")
    elif r == "fwd":
        # un chevron de sortie déborde de 10 px : la flèche part de sa pointe, pas de dessous
        x0, y0 = a["x"] + a["w"] + (10 if a["kind"] == "out" else 0), a["cy"]
        x1, y1 = b["x"] - 2, b["cy"]
        if abs(y0 - y1) < 1:
            d = f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}"
            lab = ((x0 + x1) / 2, y0 - 6, "middle")
        else:
            gx = (x0 + b["x"]) / 2
            d = f"M{x0:.1f},{y0:.1f} L{gx:.1f},{y0:.1f} L{gx:.1f},{y1:.1f} L{x1:.1f},{y1:.1f}"
            lab = (gx + 6, (y0 + y1) / 2 + 4, "start")
    elif r == "top":
        yc = y_top + e["ch"] * CHAN
        bx = b["cx"] + e["tdx"]
        if a["lane"] == "A":
            d = f"M{a['cx']:.1f},{a['y']:.1f} L{a['cx']:.1f},{yc:.1f} L{bx:.1f},{yc:.1f} L{bx:.1f},{b['y'] - 2:.1f}"
            lab = ((a["cx"] + bx) / 2, yc - 5, "middle")
        else:
            # sortie latérale, du côté de la cible, décalée du centre du couloir vertical (où passe l'aller)
            if b["cx"] < a["cx"]:
                x_out, gx = a["x"], a["x"] - (GAP + 2 * INSET) / 2 - 9 + e["gdx"]
            else:
                x_out, gx = a["x"] + a["w"], a["x"] + a["w"] + (GAP + 2 * INSET) / 2 + 9 + e["gdx"]
            d = (f"M{x_out:.1f},{a['cy']:.1f} L{gx:.1f},{a['cy']:.1f} L{gx:.1f},{yc:.1f} "
                 f"L{bx:.1f},{yc:.1f} L{bx:.1f},{b['y'] - 2:.1f}")
            lab = ((gx + bx) / 2, yc - 5, "middle")
    elif r == "bot":
        yc = y_bot + e["ch"] * CHAN
        gx = b["x"] - (GAP + 2 * INSET) / 2
        ye = b["cy"] + 13
        d = (f"M{a['cx']:.1f},{a['y'] + a['h']:.1f} L{a['cx']:.1f},{yc:.1f} L{gx:.1f},{yc:.1f} "
             f"L{gx:.1f},{ye:.1f} L{b['x'] - 2:.1f},{ye:.1f}")
        lab = ((a["cx"] + gx) / 2, yc - 5, "middle")
    else:
        raise ValueError(r)
    dash = ' stroke-dasharray="5 4"' if e["dash"] else ""
    s = (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.6"{dash} '
         f'marker-end="url(#arr-{key}-{e["kind"] or "n"})"/>')
    if e["label"] and lab:
        s += label(t, lab[0], lab[1], e["label"], FS_L, col, lab[2])
    if e["badge"]:
        xa = a["cx"] + e["dx"]
        ym = (a["y"] + b["y"] + b["h"]) / 2
        bw = len(e["badge"]) * 5.6 + 12
        s += rect(xa + 7, ym - 9, bw, 17, t["surface"], rx=8, stroke=col)
        s += txt(xa + 7 + bw / 2, ym + 3.5, e["badge"], 9.5, col, "600", anchor="middle")
    return s


# ============================================================================
# Légende
# ============================================================================

def legend(t, key, y, bad, W=W):
    items = [
        ("num", "1, 2, 3… l'ordre des étapes quand tout se passe bien"),
        ("agent", "l'agent propose : contexte vierge, il ne reçoit que ce qui le concerne ; un second agent qui relit = boucle IA"),
        ("rule", "la règle prouve = boucle déterministe : test, lint, contrôle ; vert ou rouge, sans discussion"),
        ("human", "l'humain décide : lance, répond, tranche, valide, reprend la main"),
        ("ok", "ça passe"),
        ("ko", "pas conforme : le motif repart à l'agent, 3 essais au plus, puis l'humain reprend la main"),
        ("amb", "un « non » ou des retours : l'agent reprend, rien n'est perdu"),
        ("art", "ce qui entre"),
        ("out", "ce qui sort"),
    ]
    s, x, yy = "", X_LABEL, y
    for kind, text in items:
        w = 30 + 6 + text_w(text, 11) + 22
        if x > X_LABEL and x + w > W - XR:
            x, yy = X_LABEL, yy + 21
        gy = yy - 8
        if kind == "num":
            s += step_badge(t, x + 13, gy + 3.5, 1)
        elif kind == "agent":
            s += rect(x, gy - 4, 26, 15, t["cell_gen"], rx=4)
            s += f'<rect x="{x:.1f}" y="{gy - 1:.1f}" width="3" height="9" rx="1.5" fill="{t["ramp5"][3]}"/>'
        elif kind == "rule":
            s += rect(x, gy - 4, 26, 15, t["cell_ver"], rx=4, stroke=t["good"])
        elif kind == "human":
            s += rect(x, gy - 4, 26, 15, t["cell_human"], rx=7, stroke=t["human"])
        elif kind == "art":
            s += doc_shape(x, gy - 4, 26, 15, t["surface"], t["sec"])
        elif kind == "out":
            s += chevron(x, gy - 4, 30, 15, t["ramp5"][4], first=True)
        else:
            col = edge_color(t, kind, bad)
            dash = "" if kind == "ok" else ' stroke-dasharray="5 4"'
            s += (f'<path d="M{x},{gy + 3.5} L{x + 26},{gy + 3.5}" stroke="{col}" stroke-width="1.6" fill="none"'
                  f'{dash} marker-end="url(#arr-{key}-{kind})"/>')
        s += txt(x + 36, yy, text, 11, t["sec"])
        x += w
    return s, yy + 12


# ============================================================================
# Rendu d'une orchestration
# ============================================================================

def render(o, t, mode):
    bad = BAD[mode]
    key = o["key"]
    ncols = max(n["col"] for n in o["nodes"]) + 1
    # largeurs de colonnes pondérées : les colonnes denses respirent, les colonnes d'un seul
    # nœud se resserrent. Sans « colw », toutes les colonnes ont la même largeur (cas par défaut).
    weights = o.get("colw") or [1] * ncols
    avail = W - XR - X0 - (ncols - 1) * GAP
    col_ws = [avail * w / float(sum(weights)) for w in weights]
    col_xs, acc = [], X0
    for cw in col_ws:
        col_xs.append(acc)
        acc += cw + GAP

    def col_x(j):
        return col_xs[j] + INSET

    def col_nw(j):
        return col_ws[j] - 2 * INSET

    # en-tête
    sub_lines = wrap_px(o["intro"], W - 48, 12.5)
    y_head = 62 + (len(sub_lines) - 1) * 17

    # mesures (les alertes de débordement ne sont collectées qu'une fois, en clair)
    meas = {n["id"]: measure(n, col_nw(n["col"]), o["skill"] if mode == "light" else None) for n in o["nodes"]}
    lane_h = {ln: max([meas[n["id"]][1] for n in o["nodes"] if n["lane"] == ln] + [44]) for ln in LANES}
    n_top = max([e["ch"] + 1 for e in o["edges"] if e["route"] == "top"] + [0])
    n_bot = max([e["ch"] + 1 for e in o["edges"] if e["route"] == "bot"] + [0])
    y_top = y_head + 14 + 8                      # premier canal haut (le plus extérieur)
    lane_y = {}
    y = y_top + n_top * CHAN + 6
    for ln in LANES:
        lane_y[ln] = y
        y += lane_h[ln] + ILG
    y_end_lanes = y - ILG
    y_bot = y_end_lanes + 24                     # premier canal bas
    y_leg = y_bot + n_bot * CHAN + 16

    # positions des nœuds (centrés dans leur couloir)
    P = {}
    for n in o["nodes"]:
        L, h = meas[n["id"]]
        x, w = col_x(n["col"]), col_nw(n["col"])
        yy = lane_y[n["lane"]] + (lane_h[n["lane"]] - h) / 2
        P[n["id"]] = dict(x=x, y=yy, w=w, h=h, cx=x + w / 2, cy=yy + h / 2, lane=n["lane"], kind=n["kind"], L=L)

    s = ""
    # étiquettes de couloir et fond léger
    for ln in LANES:
        fill, color = {"A": (t["ramp5"][3], "#fff"), "R": (t["rail_ver"], "#fff"), "H": (t["human"], t["on_human"])}[ln]
        y0, h = lane_y[ln], lane_h[ln]
        s += rect(X_LABEL, y0, LABEL_W, h, fill, rx=10)
        big, small, extra = LANE_LABEL[ln]
        off = -7 if extra else 0
        s += txt(X_LABEL + LABEL_W / 2, y0 + h / 2 - 2 + off, big, 12.5, color, "600", anchor="middle")
        s += txt(X_LABEL + LABEL_W / 2, y0 + h / 2 + 14 + off, small, 11, color, anchor="middle")
        if extra:
            s += txt(X_LABEL + LABEL_W / 2, y0 + h / 2 + 28 + off, extra, 10, color, anchor="middle")
        s += rect(X0 - 8, y0 - 6, W - XR - X0 + 16, h + 12, LANE_BG[mode], rx=8)
    # arêtes sous les nœuds
    for e in o["edges"]:
        s += draw_edge(t, key, e, P, y_top, y_bot, bad)
    # nœuds
    for n in o["nodes"]:
        p = P[n["id"]]
        s += draw_node(t, mode, n, p["x"], p["y"], p["w"], p["L"], p["h"], bad)
    # légende et note « exemple »
    leg, y_fin = legend(t, key, y_leg + 14, bad, W)
    s += leg
    s += itxt(X_LABEL, y_fin + 12, EXAMPLE_NOTE, 11, t["sec"])
    H = y_fin + 30

    # en-tête : titre, rôle, sous-titre, pastilles back/front
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}" '
            f'font-family="{FONT}">'
            f'<defs>' + "".join(
                f'<marker id="arr-{key}-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{edge_color(t, k if k != "n" else "", bad)}"/></marker>'
                for k in ("n", "ok", "ko", "amb")) +
            f'</defs><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1:.0f}" rx="12" fill="{t["surface"]}" '
            f'stroke="{t["border"]}"/>')
    sk = next(x for x in SKILLS if x["name"] == o["skill"])
    title = f'Exemple d\'orchestration pour {o["skill"]} : {sk["sub"]}'
    head += txt(X_LABEL, 34, title, 15.5, t["ink"], "600")
    rx = X_LABEL + text_w(title, 15.5, True) + 14
    rw = len(o["role"]) * 6.8 + 18
    head += rect(rx, 20, rw, 20, t["ramp5"][3], rx=6)
    head += txt(rx + rw / 2, 34, o["role"].upper(), 10.5, "#fff", "600", anchor="middle", spacing="0.08em")
    if o.get("chips"):
        xx = W - XR
        note = o["chips_note"]
        xx -= text_w(note, 11)
        head += txt(xx, 34, note, 11, t["sec"])
        for chip in reversed(o["chips"]):
            cw = len(chip) * 7 + 18
            xx -= cw + 8
            head += rect(xx, 20, cw, 20, t["surface"], rx=10, stroke=t["ramp5"][3])
            head += txt(xx + cw / 2, 34, chip.upper(), 10.5, PILL[mode], "600", anchor="middle", spacing="0.06em")
    for k, ln in enumerate(sub_lines):
        head += txt(X_LABEL, 56 + k * 17, ln, 12.5, t["sec"])
    return head + s + "</svg>"


# ============================================================================
# Description textuelle et fragment HTML du tableau de bord
# ============================================================================

LANE_WORD = {"A": "l'agent", "R": "la règle", "H": "l'humain"}


def short_alt(o):
    sk = next(x for x in SKILLS if x["name"] == o["skill"])
    return (f"Exemple d'orchestration pour {o['skill']} : {sk['sub']}. Schéma en trois couloirs, "
            f"l'agent propose, la règle prouve, l'humain décide. Description textuelle sous l'image.")


def description(o):
    """Description détaillée (RGAA 1.7), dans l'ordre des étapes numérotées, puis les boucles."""
    steps = sorted([n for n in o["nodes"] if n.get("step")], key=lambda n: n["step"])
    items = []
    for n in steps:
        who = {"out": "sortie", "art": "entrée"}.get(n["kind"], LANE_WORD[n["lane"]])
        desc = n["title"].rstrip(" ?") + (" : " + " ; ".join(n["body"]) if n["body"] else "")
        if n.get("ctx"):
            desc += ". Contexte : " + ", ".join(n["ctx"])
        if n["mcp"]:
            desc += ". MCP : " + ", ".join(n["mcp"])
        items.append(f"<li>{esc(who)} · {esc(desc)}</li>")
    entry = [n for n in o["nodes"] if n["kind"] == "art"]
    pre = f"<p>Ce qui entre : {esc(entry[0]['title'])}, {esc(' ; '.join(entry[0]['body']))}.</p>" if entry else ""
    loops = [e["label"] for e in o["edges"] if e["route"] in ("top", "bot") and e["label"]]
    post = ("<p>Boucles : " + esc(" ; ".join(loops)) + ". Chaque règle renvoie son motif à l'agent, 3 essais au plus, "
            "puis l'humain reprend la main.</p>")
    return pre + "<ol>" + "".join(items) + "</ol>" + post


DASHBOARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "Suivi-Strategie-Adoption-IA.html")
ASSETS_REL = "Livrables/Strategie-Deploiement/assets"
MARK_START, MARK_END = "<!-- orchestrations:start", "<!-- orchestrations:end -->"


def html_fragment():
    e = esc
    o = ['<div class="orch-tabs" role="tablist" aria-label="Un schéma par skill">']
    for i, oc in enumerate(ORCHS):
        sk = next(x for x in SKILLS if x["name"] == oc["skill"])
        o.append(f'<button role="tab" id="otab-{oc["key"]}" aria-controls="orch-{oc["key"]}" '
                 f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
                 f'{e(oc["skill"])}<small>{e(sk["sub"])}</small></button>')
    o.append("</div>")
    for i, oc in enumerate(ORCHS):
        hidden = "" if i == 0 else " hidden"
        k = oc["key"]
        o.append(f'<figure id="orch-{k}" role="tabpanel" aria-labelledby="otab-{k}"{hidden}>'
                 f'<div class="scroll"><img alt="{e(short_alt(oc))}" aria-describedby="orch-desc-{k}" '
                 f'src="{ASSETS_REL}/orchestration-{k}-light.svg"></div>'
                 f'<details class="orch-desc"><summary>Description textuelle du schéma</summary>'
                 f'<div id="orch-desc-{k}">{description(oc)}</div></details></figure>')
    o.append('<ul class="cycle-notes orch-rules">' + "".join(f"<li>{e(r)}</li>" for r in COMMON_RULES) + "</ul>")
    return "\n".join(o)


def patch_dashboard():
    if not os.path.exists(DASHBOARD):
        print(f"! tableau de bord introuvable : {DASHBOARD}")
        return
    html = open(DASHBOARD, encoding="utf-8").read()
    a, b = html.find(MARK_START), html.find(MARK_END)
    if a < 0 or b < 0 or b < a:
        print("! marqueurs orchestrations:start / orchestrations:end absents du tableau de bord, fragment non écrit")
        return
    end_of_start = html.find("-->", a) + 3
    new = html[:end_of_start] + "\n" + html_fragment() + "\n" + html[b:]
    if new != html:
        open(DASHBOARD, "w", encoding="utf-8").write(new)
    print(f"✓ {os.path.basename(DASHBOARD)} (fragment orchestrations, onglet Cible)")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    os.makedirs(out_dir, exist_ok=True)
    for mode in ("light", "dark"):
        for o in ORCHS:
            path = os.path.join(out_dir, f"orchestration-{o['key']}-{mode}.svg")
            with open(path, "w", encoding="utf-8") as f:
                f.write(render(o, THEMES[mode], mode))
            print(f"✓ {os.path.relpath(path, out_dir)}")
    patch_dashboard()
    for w in WARNINGS:
        print("! " + w)

#!/usr/bin/env python3
"""Assemble le kit copier-coller /analyse + /implement dans docs/tuto-config/kit/.
Copie la closure exacte (skills, agents, rules, hooks, scripts) et ajoute le
frontmatter YAML aux agents qui n'en ont pas (sinon ils ne s'enregistrent pas
dans un projet vierge). Lancer : python3 build_kit.py"""
import os, glob, shutil

ROOT = "/home/selim/Documents/clients/ministeres-sociaux/egapro"
KIT  = os.path.join(ROOT, "docs/tuto-config/kit")

# repartir d'un kit propre — on ne nettoie QUE le code copié (.claude, scripts),
# pas les docs rédigées à la main à la racine du kit (README.md, toAdapt.md, Install.md)
for sub in (".claude", "scripts"):
    p = os.path.join(KIT, sub)
    if os.path.isdir(p):
        shutil.rmtree(p)
os.makedirs(KIT, exist_ok=True)

def dst(*p):
    d = os.path.join(KIT, *p)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    return d

# ---------- SKILLS ----------
SKILLS = ["analyse", "implement", "report", "open"]
for s in SKILLS:
    shutil.copy2(os.path.join(ROOT, ".claude/skills", s, "SKILL.md"),
                 dst(".claude/skills", s, "SKILL.md"))

# ---------- AGENTS ----------
# (nom, modele, description)  -- frontmatter ajoute si absent
AGENTS = [
    ("product-owner", "opus", "Raffine une demande de feature en epic executable (besoin metier + decoupage + scenarios de test). Modes create/enrich. Read-only sur le code, gate de validation utilisateur avant d'ecrire."),
    ("architect", "opus", "Lit le code + Figma et produit des specs executables (rules/ticket-spec-format.md). Modes epic-create/epic-enrich/task. Read-only sur le code, gate de validation utilisateur."),
    ("bug-analyst", "opus", "Analyse un bug end-to-end : reproduit (local/env/visual), identifie la root cause, poste un commentaire ## Analyse du bug. Read-only sur le code."),
    ("code-dev", "sonnet", "Execute un ticket pre-specifie end-to-end : code, delegue tous les tests a tu-dev, ouvre la PR, declenche les validateurs. Main agent (spawne ses sous-agents). opus si label complexe."),
    ("tu-dev", None, None),
    ("e2e-dev", None, None),
    ("architect-rework", None, None),
    ("doc-writer", "sonnet", "Regenere la documentation utilisateur (docs/*.md) a partir de l'etat courant du code, en fin de pipeline epic."),
    ("validator", "sonnet", "Gate qualite : typecheck + test + lint + format (en parallele). Read-only (rapporte, ne corrige pas)."),
    ("structural-auditor", "sonnet", "Gate qualite : audit structurel du code (qualite, formulaires, schemas, DRY, imports, no-comments...). Read-only."),
    ("rgaa-auditor", "sonnet", "Gate qualite : audit d'accessibilite RGAA (13 themes) sur les fichiers .tsx modifies. Read-only."),
    ("security-auditor", "sonnet", "Gate qualite : revue securite (OWASP Top 10 + RGS) sur les fichiers server/routers/tRPC modifies. Read-only."),
    ("functional-validator", "sonnet", "Rejoue les scenarios d'acceptation du ticket et commente le resultat. Ne touche pas au board."),
]
added_fm = []
for name, model, desc in AGENTS:
    src = os.path.join(ROOT, ".claude/agents", name, "AGENT.md")
    with open(src, encoding="utf-8") as f:
        body = f.read()
    if not body.lstrip().startswith("---"):
        fm = f"---\nname: {name}\ndescription: {desc}\nmodel: {model}\n---\n\n"
        body = fm + body
        added_fm.append(name)
    with open(dst(".claude/agents", name, "AGENT.md"), "w", encoding="utf-8") as f:
        f.write(body)

# ---------- RULES (closure orchestration + process ; les regles purement
#            stack-egapro non referencees sont listees dans toAdapt.md) ----------
RULES = ["github-board", "ticket-spec-format", "complexity-estimation",
         "git-artefact-hygiene", "automation", "bug-fix-workflow",
         "code-quality", "testing", "e2e", "figma-workflow",
         "visual-quality-validation", "audit-logging"]
for r in RULES:
    shutil.copy2(os.path.join(ROOT, ".claude/rules", r + ".md"),
                 dst(".claude/rules", r + ".md"))

# ---------- HOOKS ----------
HOOKS = ["auto-lint.sh", "block-bad-patterns.sh", "check-pr-reviews.sh"]
for h in HOOKS:
    shutil.copy2(os.path.join(ROOT, ".claude/hooks", h), dst(".claude/hooks", h))

# ---------- settings.json ----------
shutil.copy2(os.path.join(ROOT, ".claude/settings.json"), dst(".claude/settings.json"))

# ---------- SCRIPTS ----------
orch = sorted(glob.glob(os.path.join(ROOT, "scripts/orchestration/*.sh")))
for sc in orch:
    shutil.copy2(sc, dst("scripts/orchestration", os.path.basename(sc)))
for sc in ["setup-worktree.sh", "teardown-worktree.sh"]:
    shutil.copy2(os.path.join(ROOT, "scripts", sc), dst("scripts", sc))

# ---------- doc portage Jira (synchronisee depuis le tutoriel canonique
#            pour eviter la derive entre les deux copies) ----------
shutil.copy2(os.path.join(ROOT, "docs/tuto-config/03-portage-jira.md"),
             os.path.join(KIT, "portage-jira.md"))

# ---------- rapport ----------
def count(pat):
    return len(glob.glob(os.path.join(KIT, pat)))
print("KIT assemble dans", KIT)
print(f"  skills  : {count('.claude/skills/*/SKILL.md')}")
print(f"  agents  : {count('.claude/agents/*/AGENT.md')}  (frontmatter ajoute a {len(added_fm)} : {', '.join(added_fm)})")
print(f"  rules   : {count('.claude/rules/*.md')}")
print(f"  hooks   : {count('.claude/hooks/*.sh')}")
print(f"  scripts : {count('scripts/orchestration/*.sh') + count('scripts/*.sh')}")
print("  doc jira: portage-jira.md (sync depuis 03-portage-jira.md)")

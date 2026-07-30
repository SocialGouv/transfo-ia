# Tuto — Générer un DA avec un LLM

Deux temps : **(1)** le LLM produit un `contenu.json` à partir du code source ; **(2)** toi, en local, tu produis le `.docx` avec `fill_da.py`.

## Fichiers et leur rôle

| Fichier | Va au LLM ? | Rôle |
|---|:---:|---|
| `prompt_generation_DA.md` | ✅ | System prompt (comment raisonner) |
| Code source de l'appli à documenter | ✅ | **Source de vérité** (champs DÉRIVÉ) |
| `exemple_contenu_SIRANO.json` | ✅ | Exemple du format JSON attendu |
| `DA_Exemple.docx` | 🟡 | Étalon de style (recommandé) |
| `DA_Modele.docx` | ❌ | Gabarit — sert au script, pas au LLM |
| `fill_da.py` | ❌ | Script — tu le lances toi-même |

## Étape 1 — Le LLM produit le JSON

1. Ouvre Claude Code **dans le dépôt de l'appli à documenter**.
2. Donne `prompt_generation_DA.md` comme consigne + `exemple_contenu_SIRANO.json` en référence de format.
3. Laisse-le explorer le code (il cite les chemins de fichiers).
4. Récupère les 3 sorties :
   - `contenu.json`
   - `DA-<Projet>-provenance.md` (audit DÉRIVÉ/INFÉRÉ)
   - `DA-<Projet>-a-completer.md` (questions par responsable)

## Étape 2 — Toi, en local, tu produis le .docx

5. Place `DA_Modele.docx`, `fill_da.py` et `contenu.json` dans le même dossier.
6. Lance :
   ```
   python fill_da.py DA_Modele.docx contenu.json DA-<Projet>-V0.1.0.docx
   ```
   - Prérequis : `python-docx` (`pip install python-docx`).
   - Schémas (cadres 5-8) : le script **retire les schémas d'exemple** du gabarit
     et injecte le rendu de tes diagrammes Mermaid. Mode par défaut `--schemas=render`
     (rendu image, nécessite **Node.js** ; un Chrome est téléchargé une fois via
     `npx`, en local — rien n'est envoyé dehors). Sans Node, ajoute
     `--schemas=placeholder` : un encart « à produire » + la spec en annexe.
7. Lis les avertissements du script (ancres non trouvées, cohérence des flux
   cadre 8 ↔ cadre 10 → à vérifier à la main).

## Étape 3 — Complétion manuelle (le script ne fait pas tout)

8. Ouvre le `.docx` et traite le questionnaire `-a-completer.md` avec les bons responsables (MOA, RSSI, PROD, DPO…).
9. Champs non automatisés à remplir main : cadre 4 (DICT/EBIOS, SLA, temps de réponse), cadre 11 (dimensionnement), cases à cocher (sensibilité, tablette/smartphone), annexe de suivi des versions.
   - Schémas (cadres 5-8) : le `.docx` contient désormais un **brouillon** propre au projet (rendu Mermaid) + une annexe « Spécifications de schémas ». Reste à le **redessiner en palette MASS** (cf. `DA templates schémas copier ajuster coller.pptx`) à partir de ce brouillon — plus depuis un exemple étranger.
10. Vérifie la cohérence inter-cadres (numéros de flux, URLs, composants, volumétrie).

## Règle d'or

Zéro invention. Un champ non dérivable du code reste `[À COMPLÉTER — RESPONSABLE : …]`, jamais deviné.

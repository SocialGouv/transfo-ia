# Origine et choix de conception

À lire pour maintenir ce skill, jamais pour construire une histoire.

## Origine

Ce skill reprend, en plus court, la méthode de la carte des messages du skill `slide-crafting`, version 0.4.0, diffusé par son auteur sous licences MIT et CC-BY-4.0 (https://creativecommons.org/licenses/by/4.0/) : un message par slide écrit en phrase dans son titre, les faits fournis seulement, le fil du récit choisi selon l'auditoire, une minute de parole par slide de contenu. Le texte est réécrit, les exemples sont nouveaux, et tout ce qui touche à la composition, aux données, à l'accessibilité et aux formats de fichier est laissé de côté. Pour un usage général, `slide-crafting` reste la référence.

## Pourquoi un skill séparé et court

- Il est lu par des modèles peu fiables, dans une chaîne où chaque agent lit 350 lignes de skills au plus. `slide-crafting` pèse 193 lignes mais 23 680 caractères, dont un planificateur n'emploie que deux étapes sur cinq.
- Un skill général apporte son propre déroulé (questions, production, livraison), qui entre en concurrence avec celui de l'orchestrateur.
- La liste des natures est fermée parce que la mise en page s'en déduit : elle doit rester égale à celle du skill de charte. Le test `orchestrateur-slides/scripts/test_controle_carte.py` le vérifie.

## Ce qui n'est pas vérifié

Aucune évaluation par cas de test : ni comparaison avec le modèle seul, ni comparaison avec `slide-crafting`. Les règles sont des hypothèses, reprises d'une méthode connue.

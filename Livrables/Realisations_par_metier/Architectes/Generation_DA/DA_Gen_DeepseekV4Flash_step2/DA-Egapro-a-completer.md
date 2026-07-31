# Questionnaire de complétion — DA-Egapro-V0.1.0

> Liste des `[À COMPLÉTER — RESPONSABLE]` regroupée par responsable.
> Chaque item est formulé en question précise et actionnable.

---

## MOA (Maîtrise d'Ouvrage — DGT)

### Planning
1. **Date de mise en production V1** — Quelle est la date de mise en service de la première version de la plateforme Egapro ?
2. **Date de mise en production V2** — Quelle est la date de mise en service de la version actuelle (refonte Next.js / App Router) ?
3. **Date de livraison V3.13.2** — Quelle est la date de la version 3.13.2 actuellement déployée ?

### Acteurs métiers — volumétrie
4. **Nombre de déclarants** — Combien d'utilisateurs déclarants (RH/paie) sont attendus sur la plateforme ?
5. **Nombre d'administrateurs DGT** — Combien d'administrateurs DGT utilisent le back-office ?
6. **Nombre d'inspecteurs SUIT** — Combien d'agents de l'inspection du travail (SUIT/Delphes) consomment l'API privée ?
7. **Nombre de référents DREETS/DDETS** — Combien de référents régionaux sont gérés dans l'annuaire ?

### Fonctionnalités — priorités M/R/E/P
8. **Priorités métier** — Y a-t-il des fonctionnalités manquantes dans la liste ou des adjustments de priorité à apporter ?

### Volumétrie
9. **D1 — Déclarations par an** — Combien de déclarations complètes sont attendues par année civile ?
10. **D2 — Entreprises déclarantes** — Combien d'entreprises distinctes déclarent chaque année ?
11. **D3 — Taille moyenne déclaration** — Quelle est la taille moyenne estimée d'une déclaration (en Ko) ?
12. **D4 — Croissance annuelle** — Quel coefficient de croissance annuelle est anticipé (ex. 10% = 1.10) ?
13. **F1 — PDF déposés / an** — Combien de PDF (avis CSE + évaluations conjointes) sont déposés par an ?
14. **F2 — PDF générés / an** — Combien de PDF (récapitulatifs, attestations) sont générés par l'application ?
15. **F3 — Taille moyenne PDF** — Quelle est la taille moyenne d'un PDF (en Mo) ?
16. **F4 — Croissance annuelle fichiers** — Quel coefficient de croissance annuelle pour les fichiers ?

### Contraintes légales / métier
17. **Contraintes réglementaires** — Existe-t-il des contraintes légales ou métier spécifiques non couvertes par la description (ex. obligation de conservation, territorialité) ?
18. **Dépendances poste de travail** — Y a-t-il des contraintes spécifiques liées au poste de travail des administrateurs DGT (OS, navigateur imposé, VPN) ?

### Garantie de service
19. **PCA / PRA / PDMA / DMIA** — Quels sont les objectifs de continuité d'activité (PCA, PRA) et la DMIA cible ?
20. **Périodes applicatives** — Quelles sont les périodes standard, critiques et de charge (dates, NUC, NRS) ?
21. **Temps de réponse cibles** — Quels sont les temps de réponse attendus par type d'opération (consultation, soumission, export) ?

---

## MOE (Maîtrise d'Œuvre)

22. **Nom et entité du responsable MOE** — Qui est le responsable MOE et quelle est son entité de rattachement ?
23. **Dimensionnement PDMA/DMIA/performances** — Quelles sont les justifications de dimensionnement (PDMA, DMIA, performances) ? Quelles règles d'allocation des ressources (nombre CPU, nombre serveurs) ?

---

## PROD (Production / Hébergement)

24. **Nom et entité du responsable production** — Qui est le responsable production / hébergement ?
25. **vCPU et RAM — EGAPRO.APP** — Combien de vCPU et RAM sont alloués au pod applicatif Next.js ?
26. **vCPU et RAM — EGAPRO.BDD** — Combien de vCPU et RAM sont alloués à la base PostgreSQL principale ?
27. **vCPU et RAM — EGAPRO.BDD-NOTIF** — Combien de vCPU et RAM sont alloués à la base PostgreSQL des notifications ?
28. **vCPU et RAM — EGAPRO.NOTIFICATIONS** — Combien de vCPU et RAM sont alloués au worker de notifications ?
29. **vCPU et RAM — EGAPRO.APISIX-SUIT** — Combien de vCPU et RAM sont alloués à la passerelle APISIX ?
30. **vCPU et RAM — EGAPRO.S3** — Quelles sont les caractéristiques du stockage S3 (capacité, performance) ?
31. **vCPU et RAM — EGAPRO.CLAMAV** — Combien de vCPU et RAM sont alloués au service ClamAV ?
32. **Version APISIX** — Quelle version d'APISIX est déployée pour la passerelle SUIT ?
33. **Placement en DMZ** — Le placement des serveurs logiques dans les zones DMZ (Publique, Privée Intranet, dédiée) est-il conforme au plan d'adressage MASS ?
34. **PCA / PRA** — Existe-t-il un PCA/PRA défini avec l'hébergeur ? Quels sont les impacts et le budget de restauration ?

---

## RSSI (Sécurité)

35. **Cotation DICT EBIOS** — Quels sont les niveaux DICT (Disponibilité, Intégrité, Confidentialité, Traçabilité) en Front et Back, selon l'échelle EBIOS de référence (1-4) ?
36. **Exigence de preuve** — Y a-t-il une exigence de preuve par fonctionnalité (horodatage, signature électronique) ?
37. **Échelle d'impact EBIOS** — Quel est le domaine, niveau et description de l'impact EBIOS ?
38. **Sensibilité des données** — La qualification de sensibilité est-elle validée ? Les cases à cocher (PII, données salariales, données de santé éventuelles) sont-elles correctement renseignées ?
39. **Catalogue des traitements CNIL** — Le traitement « Déclaration index égalité » est-il inscrit au registre CNIL ?

---

## DPO (Délégué à la Protection des Données)

40. **Qualification finale sensibilité** — La pré-cotation INFÉRÉE (données personnelles email/nom/téléphone + données salariales) est-elle confirmée ? Y a-t-il d'autres données sensibles à déclarer ?
41. **Durée de conservation** — Les durées de rétention actuelles (180j catégorie lecture, 365j mutation) sont-elles conformes à l'analyse CNIL ?

---

## ARCHITECTE SI

42. **Validation des schémas Mermaid** — Les schémas (cadres 5-8) produits en Mermaid sont-ils une base correcte pour le redessin en palette MASS ? Des ajustements sont-ils nécessaires sur le placement en DMZ ou les flux ?

---

## HÉBERGEUR

43. **Garantie de service (hébergement)** — Quels sont les SLA, NUC et NRS applicables côté hébergement (Cloud privé, cluster Kubernetes) ?
44. **PCA / PRA hébergement** — Quels sont les objectifs de restauration et les modalités de continuité au niveau de l'infrastructure d'hébergement ?

---

## Résumé statistique

| Indicateur | Valeur |
|---|---|
| Champs DÉRIVÉ | ~75 (identifiés avec preuve de code) |
| Champs INFÉRÉ | ~10 (hypothèses à confirmer) |
| Champs À COMPLÉTER | ~44 (listés ci-dessus) |
| **Taux de complétion estimé** | **~66%** (DÉRIVÉ + INFÉRÉ sur total estimé) |

### Les 5 manques les plus bloquants pour finaliser le DA

1. **Volumétrie D1-D4 / F1-F4** — Sans les données d'entrée, les volumes calculés D5-D7 et F5-F7 (dimensionnement BDD, stockage) ne peuvent être quantifiés.
2. **Cotation DICT EBIOS (RSSI)** — L'absence de cotation sécurité bloque le cadre 4 et le dimensionnement des mesures de sécurité.
3. **PCA / PRA / DMIA (MOA + HÉBERGEUR)** — Toute la section Garantie de service (cadre 4) est à compléter ; sans ces objectifs, le dimensionnement infra (cadre 11) ne peut être justifié.
4. **Dimensionnement ressources (PROD)** — vCPU/RAM par serveur logique (cadre 9) et allocation (cadre 11) sont à fournir par l'équipe production.
5. **Acteurs projet (MOA)** — Tous les noms et entités des acteurs du cadre 1 sont à renseigner.

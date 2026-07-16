# Questionnaire de complétion — DA-Egapro

Regroupé par responsable.

---

## MOA

1. **Planning** : Quelles sont les dates des versions V1, V2 et V3 de l'application Egapro ? V1 en prod, mais pas ce code source. Ce code source est la V2, pas encore en prod.
2. **Acteurs projet — MOA** : Qui est le MOA (nom, fonction, entité DGT) ? MOAName, MOAFonction, DGT
3. **Acteurs métiers** : Combien d'utilisateurs par profil ? (Déclarants entreprises, Administrateurs DGT, Inspection du travail, Grand public) à date aucun
4. **Volumétrie D1** : Quel est le volume initial de données en base (Go) ? 1Go
5. **Volumétrie D2** : Quel est le volume annuel cumulé des données (Go/an) ? 4Go
6. **Volumétrie D3** : Quel est le coefficient de progression annuelle des données (%) ? 3%
7. **Volumétrie D4** : Quelle est la durée de conservation des données (années) ? 2
8. **Volumétrie F1** : Quel est le volume initial de stockage fichiers (Mo) ? 5Mo
9. **Volumétrie F2** : Quel est le volume annuel cumulé fichiers (Mo/an) ? 6Mo
10. **Volumétrie F3** : Quel est le coefficient de progression annuelle fichiers (%) ? 7%
11. **Volumétrie F4** : Quelle est la durée de conservation des fichiers (années) ? 2
12. **Périodes applicatives** : Quelles sont les périodes Standard/Critique/Charge avec dates, NUC et NRS ? Janvier/Fevrier/Mars
13. **Contraintes légales/métier** : Y a-t-il des contraintes légales ou métier spécifiques à documenter (hors RGPD déjà couvert) ? Non
14. **Dépendances poste de travail** : Y a-t-il des dépendances avec le poste de travail (logiciels, versions de navigateur) ? Non
15. **URL de production** : Quelle est l'URL de production de l'application Egapro ? XYZ.com

---

## AMOA

1. **Acteurs projet — AMOA** : Qui est l'AMOA (nom, fonction, entité) ? AMOAName, AMOAFonction, DGT

---

## MOE

1. **Acteurs projet — MOE** : Qui est le MOE (nom, fonction, entité) ? MOEName, MOEFonction, DGT
2. **Justifications PDMA/DMIA/performances** : Quelles sont les justifications du dimensionnement (PDMA, DMIA, performances) ? JustifPDMA, JustifDMIA, JustifPerf
3. **Justifications allocation ressources** : Quelles sont les justifications d'allocation des ressources (nombre CPU, nombre serveurs) ? 8, 9

---

## PROD / HÉBERGEUR

1. **Acteurs projet — PROD** : Qui est le responsable PROD (nom, fonction, entité) ? ProdName, ProdFonction, DGT
2. **Acteurs projet — INTÉGRATION** : Qui est le responsable INTÉGRATION (nom, fonction, entité) ? IntégrationName, IntégrationFonction, DGT
3. **Ressources matérielles** : Quels sont les vCPU et RAM alloués à chaque serveur logique (EGAPRO.APP, EGAPRO.NOTIF, EGAPRO.BDD, EGAPRO.CACHE, EGAPRO.S3, EGAPRO.CLAMAV) ? EGAPRO.S3
4. **Version MinIO/S3** : Quelle est la version de MinIO utilisée en production ? 10
5. **Garantie de service** : Quels sont les objectifs PCA, PRA, PDMA, DMIA et leurs impacts ? A,B,C,D et Zimpacts
6. **Placement en DMZ** : Quel est le placement précis des serveurs dans les DMZ (DMZ Publique, DMZ Privée Intranet, DMZ Privée Infra) ? DMZ Privée Infra
7. **URL API SUIT** : Quelle est l'URL de l'API SUIT en production (EGAPRO_SUIT_API_URL) ? XYZ.com

---

## RSSI

1. **Acteurs projet — RSSI** : Qui est le RSSI (nom, fonction, entité) ? RSSIName, RSSIFonction, DGT
2. **DICT EBIOS** : Quelles sont les cotations DICT (Disponibilité, Intégrité, Confidentialité, Traçabilité) en Front et Back sur l'échelle 1-4 ? front 4, back 4
3. **Échelle d'impact EBIOS** : Quels sont le domaine, le niveau et la description de l'impact EBIOS ? domaineu, niveauElevé, fortImpact
4. **Exigence PREUVE** : Y a-t-il une exigence de preuve par fonctionnalité ? Si oui, préciser. non
5. **PCA/PRA/Hébergeur** : Confirmer les lignes de garantie de service marquées « (2) » qui se décident avec l'hébergeur. ok ok 
6. **Traitements automatisés — impacts** : Quels sont les impacts métier des traitements automatisés (CronJobs et relances email) ? aucun

---

## DPO

1. **Acteurs projet — DPO** : Qui est le DPO (nom, fonction, entité) ? DPOName, DPOFonction, DGT
2. **Sensibilité des données** : Confirmer la qualification de sensibilité des données (présence de PII : NIR via DSN, emails, données salariales) et cocher les catégories concernées dans le cadre 3. Aucune idée
3. **Durées de conservation** : Valider les durées de rétention (180j logs lecture, 365j logs action) et la politique de purge. 180j logs lecture, 365j logs action, apuyer sur delete dans la base de donnée

---

## ARCHITECTE SI

1. **Acteurs projet — ARCHITECTE SI** : Qui est l'architecte SI (nom, fonction, entité) ? ArchiName, ArchiFonction, DGT

---

## Synthèse

**Taux de complétion estimé** : ~55% (55 champs sur ~100)

**Champs dérivés du code avec confiance** :
- Nom, contexte, objectifs, enjeux (README)
- Fonctionnalités (routes, tRPC routers, README)
- Données métier (schéma BDD)
- Services utilisés (docker-compose.yml, env.js)
- Composants logiciels (package.json, docker-compose.yml)
- Matrice des flux (architecture, docker-compose)
- URLs applicatives (env.js, README)
- Traitements automatisés (CronJobs, pg-boss schedules)

**3 manques les plus bloquants** :
1. **Volumétrie (D1-D4/F1-F4)** — nécessaire pour calculer D5-D7/F5-F7 et le dimensionnement
2. **Acteurs projet (noms, fonctions, entités)** — tous les rôles sont à compléter par la MOA
3. **DICT EBIOS et garanties de service** — cotation sécurité et PCA/PRA/PDMA/DMIA à fournir par le RSSI et l'hébergeur

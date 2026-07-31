# Skill — Maquettes EGAPRO

> Skill **autonome et portable** pour générer des maquettes (mockups) fidèles à EGAPRO. Tout le nécessaire est dans ce fichier : design system, gabarit de page, principes UX, recettes, ton. Aucune dépendance au dépôt de code. Charge-le comme contexte quand tu demandes une maquette d'écran EGAPRO (nouvel écran, refonte, variante d'état).

---

## Comment produire une maquette EGAPRO

1. **Situer l'écran** : quel parcours (§5) et quel état de la démarche ? La même entrée affiche des variantes selon l'état.
2. **Poser le gabarit** de page (§3) : header État → bannière entreprise → contenu centré → bloc ressources → footer.
3. **Assembler en composants DSFR** (§2) en suivant les recettes (§6).
4. **Appliquer la doctrine UX** (§4), en priorité les règles ✅/❌.
5. **Vérifier** accessibilité (§7) et ton (§8).

Règle d'or : une maquette EGAPRO doit ressembler à un service de l'État (DSFR strict), guider sans piéger, et rester accessible (RGAA AA). En cas de doute esthétique, le DSFR tranche ; en cas de doute comportemental, le principe 4 (tolérance à l'erreur) tranche.

---

## 1. EGAPRO en bref (contexte produit)

Plateforme de l'État français où les entreprises déclarent leurs **indicateurs d'égalité de rémunération femmes-hommes**. Faits structurants qui doivent transparaître dans les écrans :

- **Indicateurs A–F** : pré-calculés par le GIP-MDS à partir des données DSN, l'entreprise **vérifie et corrige** (elle ne saisit pas de zéro).
- **Indicateur G** : écart de rémunération par catégorie d'emploi, calculé par l'entreprise.
- **Seuil d'alerte : écart ≥ 5 %** → obligations supplémentaires (seconde déclaration, avis CSE, évaluation conjointe).
- **Avis CSE** : dépôt de PDF, entreprises ≥ 100 salariés.
- **Tailles** : < 50 (volontaire), 50–99 (triennal), ≥ 100 (annuel + CSE).
- **Acteurs** : le **déclarant** (entreprise, via ProConnect), l'**admin** (back-office, peut « mimoquer » une entreprise en lecture seule), le **public** (stats et référents, sans authentification).

---

## 2. Socle design system (DSFR — cheat-sheet)

EGAPRO est bâti sur le **DSFR** (Système de Design de l'État français). Une maquette qui n'est pas DSFR n'est pas EGAPRO.

### Identité de marque (obligatoire, jamais omise)
Le **bloc marque de l'État** est l'élément le plus reconnaissable : il ne doit **jamais** être réduit au seul texte du ministère. Il combine **trois parties obligatoires**, de gauche à droite :
1. **Le drapeau tricolore français** (bleu-blanc-rouge) : le « logo » en haut à gauche. ⚠️ « Marianne » est le nom de la *police* DSFR, **pas** ce logo — ne confonds pas les deux et ne remplace jamais le drapeau par du texte.
2. **La devise** « Liberté / Égalité / Fraternité » (3 lignes, italique, petit corps), sous le drapeau.
3. **L'intitulé officiel** « MINISTÈRE DU TRAVAIL ET DES SOLIDARITÉS » (3 lignes, majuscules, gras), à droite du drapeau.

Puis, séparé par un **trait vertical** : le **nom du service** « Egapro » + la baseline « Indicateurs d'égalité professionnelle femmes-hommes ». Ce bloc apparaît dans le **header** (compact) et le **footer** (grand format).

✅ Toujours rendre drapeau **+** devise **+** intitulé.
❌ Header réduit à « MINISTÈRE… » sans drapeau ni devise — c'est l'erreur la plus fréquente, à ne pas commettre.

**Rendu sans l'asset officiel** (artefact, CSP stricte, pas d'image externe) : ne supprime **pas** le drapeau, dessine-le en CSS — un rectangle de 3 bandes verticales égales `#000091` (bleu) · `#FFFFFF` (blanc) · `#E1000F` (rouge), ratio ≈ 4:3, avec la devise en texte juste en dessous.

### Couleurs (tokens DSFR + hex de référence)
| Rôle | Token DSFR | Hex (thème clair) |
|---|---|---|
| Bleu France (identité, bouton primaire, liens) | `blue-france-sun-113` | `#000091` |
| Rouge Marianne (logo seulement) | — | `#E1000F` |
| Fond de bloc « État » (bannières, encarts) | `blue-france-975` | `#F5F5FE` |
| Fond action faible (tag cliquable, survol) | `blue-france-925` | `#E3E3FD` |
| Texte titre (quasi-noir) | `grey-50` | `#161616` |
| Corps de texte | `grey-200` | `#3A3A3A` |
| Texte mention / détail | `grey-425` | `#666666` |
| Fond de page | `grey-1000` | `#FFFFFF` |
| Bordure par défaut | `grey-900` | `#DDDDDD` |
| Erreur | `error-425` | `#CE0500` |
| Succès | `success-425` | `#18753C` |
| Ombre « élevé » | — | `0 2px 6px rgba(0,0,18,.16)` |

> Les **noms de tokens** font foi ; les hex des nuances intermédiaires doivent être confirmés sur la palette DSFR officielle si le rendu doit être pixel-parfait. N'invente jamais une couleur hors palette.

### Typographie
- Police unique : **Marianne** (titres en **Bold 700**, corps en Regular/Medium).
- Échelle de titres (desktop, approx. DSFR) : H1 40 · H2 32 · H3 28 · H4 24 · H5 22 · H6 20 px.
- Corps : lg 20 · md 16 (standard) · sm 14 (détail) · xs 12 (mention).

### Grille & layout
- Largeur de design **1440 px**, marges latérales **~120 px** desktop.
- Contenu de **formulaire centré, largeur ~790 px** (lecture confortable).
- Mobile-first. Breakpoints DSFR : `xs` 0 · `sm` 36em · `md` 48em · `lg` 62em · `xl` 78em.

### Composants clés (et quand les utiliser)
- **En-tête / Pied de page** (`fr-header` / `fr-footer`) : marque État, accès « Aide » + « Mon espace », liens gouvernementaux + mentions légales.
- **Fil d'Ariane** (`fr-breadcrumb`) : situer l'écran dans la hiérarchie (Mon espace › Entreprise › Démarche…).
- **Indicateur d'étapes** (`fr-stepper`) : « Étape X sur N » + titre de l'étape + **annonce de l'étape suivante**.
- **Boutons** : **primaire** (action principale, fond bleu France), **secondaire** (contour), **tertiaire** (texte/sans bordure, ex. « Précédent »). Un seul primaire par zone d'action.
- **Champs** (`fr-input`, `fr-select`) : toujours un `label` associé ; hint sous le label pour les contraintes.
- **Tableau** (`fr-table`) : saisie tabulaire directe, et **alternative accessible** sous tout graphique.
- **Cases / radios** (`fr-checkbox`, `fr-radio`) : input natif masqué, **le clic se fait sur le label**.
- **Accordéon** (`fr-accordion`) : « Définitions et méthode de calcul » repliées par défaut.
- **Alerte** (`fr-alert` error/success/info) : erreurs de formulaire en haut, avec zone live.
- **Encart / mise en avant** (`fr-callout`, `fr-highlight`) : récapitulatifs, checklists de complétude.
- **Badge / Tag** (`fr-badge`, `fr-tag`) : statuts (« Effectué », « En cours », « Annulée »).
- **Modale** (`fr-modal`, dialog) : certification « Je certifie… » + « Valider » avant tout acte engageant.
- **Upload** (`fr-upload`) : zone de dépôt avec glisser-déposer, contraintes affichées.
- **Tuiles** (`fr-tile`) : les 3 cartes du bloc ressources d'aide.

### Règles de style dures
- Couleurs et espacements **uniquement** via tokens DSFR ; pas de hex arbitraire, pas de style inline.
- Icônes décoratives masquées aux lecteurs d'écran ; pictogrammes officiels DSFR (jamais d'icône inventée).
- Pas de media query manuelle : penser mobile-first avec les breakpoints DSFR.

---

## 3. Anatomie d'une page EGAPRO (gabarit)

De haut en bas, le squelette récurrent :

1. **Header État** : bloc marque (Marianne + ministère) · nom du service « Egapro » + baseline · à droite : lien « Aide » + bouton « Mon espace ».
2. **Bannière entreprise** (fond bleu très clair `#F5F5FE`) :
   - **Fil d'Ariane** (libellés exacts) : 1er crumb **« Mon espace »** (lien, jamais « Accueil »), puis `Nom entreprise`, puis le libellé de l'écran courant (ex. `Démarche des indicateurs de rémunération AAAA`) — pas le nom de l'entreprise répété.
   - Ligne d'identité : **nom**, **SIREN**, **Code NAF**, **effectif annuel moyen (année)**, **existence d'un CSE** (Oui/Non/Non renseigné).
3. **Container** (fond blanc, contenu centré ~790 px) :
   - **Ligne de titre** : `H1/H4` de l'écran + à droite **indicateur de sauvegarde** (« Enregistre… » → « Enregistré » + cloud-check).
   - **Indicateur d'étapes** (dans les parcours) : « Étape X sur N » + titre + « Étape suivante : … ».
   - **Corps** : le contenu propre à l'écran (formulaire, tableau, choix…).
   - **Actions de formulaire** : « Précédent » (tertiaire, gauche) ⇄ « Suivant » / « Soumettre » / « Transmettre » (primaire, droite), en `space-between`.
4. **Bloc Ressources** (fond bleu très clair) : 3 tuiles **Centre d'aide** · **Questions fréquentes (FAQ)** · **Nous contacter** + illustration. Présent sur les écrans déclarant et publics ; **absent** de la page de connexion et du back-office admin.
5. **Footer** : marque État · description du service · liens info.gouv.fr / service-public.fr / legifrance.gouv.fr / data.gouv.fr · mentions (Accessibilité, Mentions légales, Données personnelles, Gestion des cookies, Plan du site, Paramètres d'affichage) · licence Etalab 2.0.

---

## 4. Doctrine UX (prescriptif)

15 principes. Les ✅/❌ sont les arbitrages qui dirigent vraiment une maquette.

### Orientation et feedback
1. **L'usager sait toujours où il en est** : fil d'Ariane + stepper « Étape X sur N » (qui annonce la suite) + bannière entreprise persistante + badges de statut.
2. **Feedback de calcul en temps réel** : écarts, totaux et seuils se recalculent à la saisie ; l'usager voit l'effet avant de soumettre.
3. **État terminal de confirmation explicite** : tout parcours se ferme sur un signal clair (« parcours terminé », « Démarche close »).

### Saisie et gestion de l'erreur
4. **Tolérance à l'erreur plutôt que prévention par blocage.**
   ✅ Laisser cliquer « Suivant/Soumettre » même incomplet, valider à la soumission, rattraper avec des erreurs ancrées.
   ❌ Griser un bouton parce que le formulaire est incomplet (illisible pour les lecteurs d'écran). Le `disabled` est réservé à l'**autorisation** (ex. lecture seule), toujours avec une explication.
5. **Validation inline et erreurs ancrées** : erreur au niveau du champ **+** alerte récap en haut avec liens d'ancrage (zone live).
   ✅ Révéler les erreurs **après une tentative de soumission**. ✅ Accepter `0` explicite (vide ≠ zéro).
   ❌ Afficher des erreurs au chargement ou au blur pendant la saisie.
6. **Confirmation explicite avant tout acte engageant** : modale + case « Je certifie… » + « Valider » avant soumission / transmission / annulation.
7. **Rien ne se perd, et ça se voit** : sauvegarde au fil de l'eau (par champ), signalée par un indicateur « Enregistré » accessible. Persistance optimiste ; le brouillon survit à un changement de navigateur.

### Guidage et structure
8. **Routing piloté par l'état métier, pas par l'usager.**
   ✅ La destination après soumission découle de l'état (CSE, écart, taille) ; « Précédent » route selon l'état.
   ❌ Forcer l'usager à choisir manuellement une étape qui pourrait être incohérente.
9. **Garde par redirection ou 404, jamais d'état invalide atteignable** : récap non soumis → 404, démarche close → redirection, étape après échéance → récap en lecture seule.
10. **Divulgation progressive** : le détail au besoin (coordonnées au click-through, matrice après dépôt, « Voir plus », accordéons repliés).
11. **Guidance préventive : annoncer les contraintes et la suite avant l'action.**
   ✅ Contraintes affichées d'emblée (« 10 Mo, .pdf, 4 fichiers max »), aperçu de l'étape suivante, **checklist de complétude en temps réel** (exigences cochées / en attente).
   (Complément amont du principe 4 : on guide avant, on rattrape après.)

### Socle technique et inclusif
12. **DSFR natif comme langage commun** : composants de l'État, pas de style maison.
13. **Accessibilité RGAA en exigence dure** : rôles ARIA, labels associés, décoratif masqué, **tout graphique a son tableau accessible**, focus déplacé après action dynamique. (Détail en §7.)
14. **Discipline de mise en page responsive** : largeur de contenu bornée et stable selon le viewport et les interactions.
15. **Fidélité terminologique au vocabulaire réglementaire** : libellés exacts, seuil inclus (« écarts ≥ 5 % »), pas de reformulation approximative.

---

## 5. Parcours (taxonomie des écrans)

Ce que chaque parcours doit montrer :

1. **Authentification** : ProConnect = entrée unique ; redirections contextuelles ; consentement cookies CNIL ; aide masquée sur la connexion.
2. **Onboarding / espace personnel** : collecte des infos manquantes au dernier moment (modale ciblée) ; **panneau de démarche** à variantes (début / conformité / évaluation / CSE / clôturée) avec un CTA unique vers l'étape suivante.
3. **Tunnel de déclaration (6 étapes, indicateurs A–F)** : saisie tabulaire ; pré-remplissage GIP-MDS à corriger ; réutilisation N-1/N-2 ; définitions en accordéon ; soin de la saisie chiffrée (€ alignés à droite, séparateur de milliers) ; récap final téléchargeable (PDF).
4. **Conformité (écart ≥ 5 %)** : 3 chemins en langage métier (actions correctives + 2nde déclaration / évaluation conjointe / justification) ; options adaptées à l'état ; tâtonnement permis ; boucle jusqu'à conformité.
5. **Avis CSE / évaluation conjointe** : upload souple (sélection ou glisser-déposer, contraintes affichées, suppression par ligne) ; **matrice de qualification** (Exactitude / Justification × 1re / 2nde déclaration) ; checklist de complétude ; soumission tolérante ; certification.
6. **Échéances de campagne** : contrainte temporelle rendue visible (« Modifiable jusqu'au… » / « Modification close depuis le… ») ; gating de navigation vers le récap en lecture seule.
7. **Cycle de vie / annulation / historique** : annulation réversible (« À compléter » → re-soumission) ; confirmation avant annulation ; historique paginé.
8. **Notifications** : accusé de réception email après chaque acte structurant.
9. **Consultation publique (anonyme)** : stats et référents sans authentification ; graphique **+ tableau accessible** ; minimisation des données (coordonnées au click-through, filtre obligatoire avant résultats).
10. **Back-office admin** : chrome dépouillé (sans footer public ni aide), side-menu fixe ; accès strict ; **mimoquage en lecture seule** (écriture bloquée + explication) ; stats filtrables.
11. **Pages d'erreur** : 404 / 500 / 503 cohérentes — code + titre humain + message d'excuse + conseil + artwork décoratif + retour accueil. Jamais de cul-de-sac.

---

## 6. Recettes d'assemblage

- **Écran de tunnel (formulaire multi-étapes)** : bannière entreprise → titre + indicateur de sauvegarde → `fr-stepper` (X sur N + étape suivante) → corps (tableau ou champs, accordéon de définitions) → actions « Précédent » (tertiaire) / « Suivant » (primaire). Erreurs ancrées au submit.
- **Dépôt de fichiers + matrice** : label + hint de contraintes → zone d'upload (sélection ou glisser-déposer) → `fr-table` matrice (lignes = fichiers, colonnes = types de preuve avec cases) → encart checklist « à transmettre » (coché / en attente) → « Soumettre » (jamais grisé pour incomplétude) → modale de certification.
- **Page de choix (conformité)** : intro + 3 options en `fr-radio` (libellés réglementaires exacts) → « Suivant ». Les options affichées dépendent de l'état.
- **Stats (public ou admin)** : titre → graphique → **toujours** un `<details>` « Consulter les données sous forme de tableau » avec `fr-table` → filtres (tranche d'effectif, année).
- **État terminal / confirmation** : `fr-callout` ou bandeau succès « parcours terminé » + récap + retour « Mon espace ».
- **Page d'erreur** : artwork DSFR (aria-hidden) + « Erreur NNN » + titre humain + message + bouton retour accueil.

---

## 7. Accessibilité (RGAA / WCAG 2.1 AA) — non négociable

- Chaque champ a un `label` associé ; cases/radios pilotées par le label (input natif masqué).
- Hiérarchie de titres sans saut de niveau ; un seul `H1` par page.
- Tout graphique double d'un **tableau accessible**.
- Décoratif masqué aux lecteurs d'écran ; alternatives textuelles sur les images informatives.
- Modales : rôle dialog + libellé ; liens nouvel onglet signalés.
- Focus géré explicitement après action dynamique (ex. ajout d'un bloc → focus sur son 1er champ).
- Contrastes DSFR respectés ; cible Lighthouse accessibilité 100 %.

---

## 8. Ton et rédaction

- **Français**, registre administratif **clair et direct** (vouvoiement), phrases courtes.
- **Vocabulaire réglementaire exact** : « écarts de rémunération ≥ 5 % », « avis du CSE », « évaluation conjointe », « seconde déclaration ». Pas de paraphrase approximative.
- **Écriture inclusive** : épicène d'abord (« déclarant·e » seulement si nécessaire), formules englobantes.
- Messages d'erreur **actionnables** (« Format attendu : … »), messages d'état rassurants.
- Pas de jargon technique côté usager ; les libellés disent l'action (« Transmettre », « Soumettre », « Modifier »).

---

## 9. Périmètre et limites

- Doctrine dérivée du comportement **testé** d'EGAPRO + d'une maquette Figma (écran de dépôt CSE) + du **DSFR public**. C'est une base solide, pas une spécification visuelle exhaustive.
- **Couverts faiblement** : nuances de hiérarchie visuelle fine, micro-espacements, mode sombre, déclinaisons mobiles précises. Pour ces points, suivre le DSFR par défaut et, si un rendu pixel-parfait est requis, se référer à la palette/maquette officielle.
- Les **hex** des nuances DSFR intermédiaires sont donnés à titre de référence ; les **noms de tokens** font foi.

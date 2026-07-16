# Principes UX d'EGAPRO

> Synthèse des principes d'expérience utilisateur de la plateforme, **inférés du comportement décrit par les tests E2E** (`packages/app/src/e2e/`).

## Méthode et périmètre

Ces principes sont dérivés des 28 fichiers de tests E2E Playwright et de leurs helpers de flux. Les tests E2E décrivent ce que l'usager doit **observer** : c'est un bon proxy de l'intention UX, mais ce n'est pas un document de design.

Conséquences à garder en tête :

- **Couverture inégale.** La déclaration et la conformité sont massivement testées ; d'autres surfaces le sont peu ou pas. Les principes portent d'autant plus de poids qu'ils recoupent plusieurs parcours.
- **Hors de portée des E2E** (donc non affirmés ici) : hiérarchie visuelle, contraste, ton rédactionnel, charge cognitive. Le **menu mobile** et le **mode sombre** existent dans le code (`src/modules/layout/`) mais ne sont pas couverts par les E2E : on ne peut en tirer aucun principe *vérifié*.
- Chaque principe est rattaché à une preuve (fichier de test ou de code). En cas de doute, vérifier le code courant : un test peut avoir évolué.

**Révision (passe Figma + code).** Une comparaison avec la maquette de l'écran « Dépôt avis CSE » (Figma, recoupée avec le code source) a révélé que plusieurs principes manquaient parce que les surfaces concernées **ne sont pas couvertes par les E2E** alors qu'elles existent et sont testées en unitaire : fil d'Ariane, indicateur de sauvegarde, guidance préventive (principe 11), ressources d'aide. Les preuves citent désormais aussi le code (`modules/…`) quand l'E2E est muet.

---

## Principes transverses

### Orientation et feedback

**1. L'usager sait toujours où il en est.**
Trois repères combinés : **fil d'Ariane** hiérarchique (« Mon espace › Entreprise › Démarche… 2027 »), **stepper** « Étape X sur N » (qui annonce aussi l'étape suivante, voir principe 11), et **contexte entreprise toujours visible** via une bannière persistante portant nom, SIREN, Code NAF, effectif annuel moyen (année) et existence d'un CSE. Par ailleurs : badges de statut explicites (« Effectué » / « À compléter » / « Annulée le… ») et bandeau « vous mimoquez l'entreprise… » en impersonation.
Preuves : [CompanyBanner.tsx:26](packages/app/src/modules/declaration-remuneration/shared/CompanyBanner.tsx#L26), [declaration.e2e.ts:37](packages/app/src/e2e/declaration.e2e.ts#L37), [declaration-cancellation.e2e.ts](packages/app/src/e2e/declaration-cancellation.e2e.ts).

**2. Feedback de calcul en temps réel.**
Les écarts se calculent à la saisie (« 6,3 % » dès F/H renseignés), les totaux d'effectifs s'additionnent, les seuils de quartile cascadent (remplir Q1 met à jour la borne basse de Q2 à « 20 000,01 € »). L'usager voit l'effet de sa saisie avant de soumettre.
Preuves : [declaration.e2e.ts:69](packages/app/src/e2e/declaration.e2e.ts#L69), [declaration.e2e.ts:144](packages/app/src/e2e/declaration.e2e.ts#L144).

**3. État terminal de confirmation explicite.**
Tout parcours se ferme sur un signal clair : « Votre parcours est terminé », page `/confirmation`, badge « Démarche close » + « Cette démarche est terminée… ». L'usager sait quand c'est fini.
Preuves : [compliance.e2e.ts:40](packages/app/src/e2e/compliance.e2e.ts#L40), [declaration-process-panel.e2e.ts:253](packages/app/src/e2e/declaration-process-panel.e2e.ts#L253).

### Saisie et gestion de l'erreur

**4. Tolérance à l'erreur plutôt que prévention par blocage.**
On ne grise **pas** le submit pour forcer la complétude. L'usager peut tenter, la validation se déclenche à la soumission, et l'échec est rattrapé. Le bouton n'est désactivé que pour une raison d'**autorisation** (mimoquage en lecture seule), toujours avec une explication (tooltip). On ne cache pas le pourquoi derrière un bouton inerte (mauvais pour les lecteurs d'écran).
Preuves : [declaration.e2e.ts:234](packages/app/src/e2e/declaration.e2e.ts#L234), [step1-workforce-validation.e2e.ts:16](packages/app/src/e2e/step1-workforce-validation.e2e.ts#L16), [admin-impersonation-read-only.e2e.ts:30](packages/app/src/e2e/admin-impersonation-read-only.e2e.ts#L30).

**5. Validation inline et erreurs ancrées.**
Erreur au niveau du champ (`fr-error-text`) **et** alerte récap en haut avec liens d'ancrage vers les champs fautifs (`aria-live`). La navigation est bloquée par la validation, jamais par un bouton grisé. Distinction nette : **vide ≠ zéro** (saisir `0` explicitement passe, bug #3527). Et **les erreurs ne se révèlent qu'après une tentative de soumission**, jamais au chargement ni au blur : on ne harcèle pas l'usager pendant qu'il saisit (epic-3476).
Preuves : [declaration.e2e.ts:169](packages/app/src/e2e/declaration.e2e.ts#L169), [step1-workforce-validation.e2e.ts:39](packages/app/src/e2e/step1-workforce-validation.e2e.ts#L39), [Step2Upload.tsx:145](packages/app/src/modules/cseOpinion/Step2Upload.tsx#L145).

**6. Confirmation explicite avant tout acte engageant.**
Systématiquement : modale + case « Je certifie… » + bouton « Valider » avant chaque soumission, transmission ou annulation. Double garde-fou contre l'irréversible.
Preuves : [declaration.e2e.ts:321](packages/app/src/e2e/declaration.e2e.ts#L321), [compliance-flows.ts:88](packages/app/src/e2e/helpers/compliance-flows.ts#L88), [declaration-cancellation.e2e.ts:47](packages/app/src/e2e/declaration-cancellation.e2e.ts#L47).

**7. Rien ne se perd : sauvegarde au fil de l'eau, avec retour d'état visible.**
Chaque saisie persiste sans soumission globale (brouillon sauvé à chaque champ, association CSE persistée case par case), et la persistance est **signalée visiblement** par un indicateur « Enregistre… » → « Enregistré » (icône cloud-check), accessible (`role="status"`, `aria-live="polite"`). Le brouillon est restauré dans un autre navigateur. Persistance optimiste : « Soumettre » attend la confirmation serveur avant de se débloquer.
Preuves : [SavedIndicator.tsx](packages/app/src/modules/declaration-remuneration/shared/SavedIndicator.tsx), [declarationDraft.e2e.ts:33](packages/app/src/e2e/declarationDraft.e2e.ts#L33), [compliance-flows.ts:75](packages/app/src/e2e/helpers/compliance-flows.ts#L75).

### Guidage et structure

**8. Routing piloté par l'état métier, pas par l'usager.**
La destination après soumission n'est jamais un choix de menu : elle dépend de `hasCse`, de l'écart et de la taille de l'entreprise. Le bouton « Précédent » route lui-même selon l'état (un même clic renvoie à l'étape 6, au choix de conformité ou à l'étape 3 selon le contexte). On guide, on ne laisse pas s'égarer.
Preuves : [compliance.e2e.ts:284](packages/app/src/e2e/compliance.e2e.ts#L284) (paths 13.a/b/c).

**9. Garde par redirection ou 404, jamais d'état invalide atteignable.**
Le système se protège des états incohérents par routage : récap d'une déclaration non soumise → 404, démarche close → redirection hors formulaire, étape après échéance → redirection vers le récap, anciennes URLs stats → page unifiée, référent inconnu → 404.
Preuves : [recapitulatif.e2e.ts:73](packages/app/src/e2e/recapitulatif.e2e.ts#L73), [campaign-deadlines-gating.e2e.ts:152](packages/app/src/e2e/campaign-deadlines-gating.e2e.ts#L152), [admin-stats.e2e.ts:341](packages/app/src/e2e/admin-stats.e2e.ts#L341).

**10. Divulgation progressive.**
Le détail n'apparaît qu'au besoin : coordonnées des référents révélées au click-through, matrice de qualification affichée seulement après dépôt du fichier, pagination « Voir plus » (10 puis +), accordéons « Définitions et méthode de calcul » repliés par défaut.
Preuves : [public-referents.e2e.ts:144](packages/app/src/e2e/public-referents.e2e.ts#L144), [declaration-history.e2e.ts:44](packages/app/src/e2e/declaration-history.e2e.ts#L44).

**11. Guidance préventive : annoncer les contraintes et la suite avant l'action.**
Complément amont du principe 4 (on guide avant, on rattrape après) : contraintes d'upload affichées d'emblée (« 10 Mo par fichier, format pdf, 4 fichiers maximum »), aperçu de l'étape suivante dans le stepper (« Étape suivante : Transmettre »), et **checklist de complétude en temps réel** (« Avis CSE à transmettre » : chaque exigence cochée ou en attente). L'usager voit ce qu'il reste à faire pour une soumission valide.
Preuves : [Step2Upload.tsx:200](packages/app/src/modules/cseOpinion/Step2Upload.tsx#L200), `modules/declaration-remuneration/shared/NextStepsBox.tsx`, `modules/cseOpinion/components/ContentTypeMatrix.tsx`.

### Socle technique et inclusif

**12. DSFR natif comme langage commun.**
Tout passe par le système de l'État : radios masqués pilotés par label cliquable, modales `data-fr-js-modal`, accordéons, pictogrammes `fr-artwork`. Cohérence « service public » plutôt que style maison.
Preuves : [dsfr.ts](packages/app/src/e2e/helpers/dsfr.ts), [error-pages.e2e.ts:23](packages/app/src/e2e/error-pages.e2e.ts#L23).

**13. Accessibilité RGAA en exigence dure.**
Sélection par rôle ARIA, labels associés systématiques, `aria-hidden` sur le décoratif, **chaque graphique a son alternative tableau** (« Consulter les données du graphique sous forme de tableau »), et **gestion explicite du focus** après action dynamique (ajout d'une catégorie → focus sur son premier champ). Audit axe-core sur les pages clés + Lighthouse accessibilité à 100 % imposé en CI.
Preuves : [rgaa-audit.spec.ts](packages/app/src/e2e/rgaa-audit.spec.ts), [admin-stats.e2e.ts:92](packages/app/src/e2e/admin-stats.e2e.ts#L92), [declaration-step5-remuneration.e2e.ts:42](packages/app/src/e2e/declaration-step5-remuneration.e2e.ts#L42).

**14. Discipline de mise en page responsive.**
Largeur de contenu bornée et stable selon le viewport et les interactions : colonne illustration contrainte par le conteneur à 1920 px et qui ne saute pas à l'ouverture d'un accordéon, layout admin fluide à side-menu fixe.
Preuves : [login.e2e.ts:26](packages/app/src/e2e/login.e2e.ts#L26), [admin.e2e.ts:57](packages/app/src/e2e/admin.e2e.ts#L57).

**15. Fidélité terminologique au vocabulaire réglementaire.**
Les libellés sont précis et constants, seuil inclus (« Justifier les écarts de rémunération ≥ 5 % », « Actions correctives et seconde déclaration »). Le langage suit la réglementation, pas une reformulation approximative.
Preuves : [compliance.e2e.ts:81](packages/app/src/e2e/compliance.e2e.ts#L81).

---

## Principes par parcours

### 1. Authentification et accès

- **ProConnect comme porte d'entrée unique** : identité État, pas de mot de passe maison.
- **Redirections contextuelles** : déjà connecté → `/mon-espace` ; route protégée sans session → `/login` ; accueil → `/mon-espace` si authentifié. L'URL cible est préservée à travers le login.
- **Consentement cookies CNIL** : « Tout refuser » accessible en un clic.
- **Aide contextualisée et omniprésente** : bloc « Ressources et aide » en 3 cartes (Centre d'aide / FAQ / Nous contacter), présent sur les pages publiques (`/referents`) **et** sur les pages déclarant authentifiées, mais masqué sur `/login` et dans le back-office admin.

Fichiers : [login.e2e.ts](packages/app/src/e2e/login.e2e.ts), [logout.e2e.ts](packages/app/src/e2e/logout.e2e.ts), [home.e2e.ts](packages/app/src/e2e/home.e2e.ts), [helpers/login.ts](packages/app/src/e2e/helpers/login.ts).

### 2. Onboarding et entrée dans l'espace

- **Collecte progressive, au dernier moment** : la modale « infos manquantes » n'apparaît qu'au clic sur « Rémunération » et ne demande **que ce qui manque** (CSE et/ou téléphone), jamais un formulaire de profil massif.
- **Panneau de démarche contextuel** : le même point d'entrée « Rémunération » affiche une variante différente selon l'état exact (start / compliance / évaluation / cse / closed) avec un **CTA unique** qui pointe toujours vers l'étape suivante.

Fichiers : [missing-info-modal.e2e.ts](packages/app/src/e2e/missing-info-modal.e2e.ts), [declaration-process-panel.e2e.ts](packages/app/src/e2e/declaration-process-panel.e2e.ts).

### 3. Tunnel de déclaration (6 étapes, indicateurs A–F)

- **Saisie tabulaire directe** : édition inline dans les tableaux, pas de champ-par-champ.
- **Pré-remplissage des données connues** : seuils horaires déjà remplis par GIP-MDS pour le SIREN ; l'usager corrige plutôt qu'il ne ressaisit.
- **Réutilisation année précédente** : catégories d'emploi pré-remplies depuis N-1 (repli sur N-2), libellés + source conservés, champs numériques vides à ressaisir.
- **Aide à la demande** : accordéon « Définitions et méthode de calcul » sur chaque étape.
- **Soin de la saisie chiffrée** : montants € alignés à droite, séparateur de milliers, € alignés verticalement, focus déplacé sur le 1er champ d'une nouvelle catégorie.
- **Récapitulatif final téléchargeable** (PDF), structuré par sections, avec retour « Mon Espace ».

Fichiers : [declaration.e2e.ts](packages/app/src/e2e/declaration.e2e.ts), [declaration-step5-remuneration.e2e.ts](packages/app/src/e2e/declaration-step5-remuneration.e2e.ts), [previous-year-categories.e2e.ts](packages/app/src/e2e/previous-year-categories.e2e.ts), [recapitulatif.e2e.ts](packages/app/src/e2e/recapitulatif.e2e.ts), [declarationDraft.e2e.ts](packages/app/src/e2e/declarationDraft.e2e.ts), [step1-workforce-validation.e2e.ts](packages/app/src/e2e/step1-workforce-validation.e2e.ts).

### 4. Conformité (écart ≥ 5 %)

- **Plusieurs chemins proposés, en langage métier** : actions correctives + 2nde déclaration / évaluation conjointe / justification.
- **Options adaptées au contexte** : au 2nd tour l'action corrective disparaît ; selon `hasCse` la justification apparaît ou non.
- **Tâtonnement autorisé, zéro piège** : explorer un chemin puis changer d'avis avant l'acte irréversible ; les deux choix sont tracés, le dernier gagne.
- **Boucle propre jusqu'à conformité** : si l'écart persiste après correction, retour automatique au choix.
- **Garde de re-entrée** : une démarche close redirige hors du formulaire.

Fichiers : [compliance.e2e.ts](packages/app/src/e2e/compliance.e2e.ts), [compliance-path-change.e2e.ts](packages/app/src/e2e/compliance-path-change.e2e.ts), [helpers/compliance-flows.ts](packages/app/src/e2e/helpers/compliance-flows.ts).

### 5. Avis CSE et évaluation conjointe (dépôt de pièces)

- **Upload souple** : sélection de fichier *ou* glisser-déposer, contraintes annoncées d'emblée (10 Mo, .pdf, 4 fichiers max), pas de bouton « Importer » intermédiaire, suppression possible par ligne.
- **Matrice de qualification** : après dépôt, l'usager associe chaque fichier à ce qu'il prouve (Exactitude / Justification × 1re / 2nde déclaration). Persistance optimiste case par case.
- **Checklist de complétude** (« Avis CSE à transmettre ») : récapitule en direct les exigences couvertes vs manquantes avant soumission.
- **Soumission tolérante** : « Soumettre » n'est jamais grisé pour incomplétude (seulement pour l'autorisation) ; un clic en état incomplet révèle les erreurs.
- **Certification conforme** avant transmission.
- **Modifiabilité encadrée** : les avis CSE restent modifiables jusqu'à l'échéance, même après clôture.

Fichiers : [compliance.e2e.ts](packages/app/src/e2e/compliance.e2e.ts), [helpers/compliance-flows.ts](packages/app/src/e2e/helpers/compliance-flows.ts), [Step2Upload.tsx](packages/app/src/modules/cseOpinion/Step2Upload.tsx).

### 6. Échéances de campagne (gating temporel)

- **La contrainte réglementaire est rendue visible, jamais silencieuse** : avant échéance → lien « Modifier » + « Modifiable jusqu'au… » ; après → lien retiré + « Modification close depuis le… ».
- **Gating appliqué aussi à la navigation** : tenter une étape après échéance redirige vers le récap en lecture seule.

Fichier : [campaign-deadlines-gating.e2e.ts](packages/app/src/e2e/campaign-deadlines-gating.e2e.ts).

### 7. Cycle de vie, annulation et historique

- **Annulation réversible côté usager** : une déclaration annulée repasse mon-espace à « À compléter », l'usager peut re-soumettre (cycles multiples supportés).
- **Confirmation avant annulation** (modale « Confirmer l'annulation »).
- **Traçabilité** : historique des modifications paginé (« Voir plus », 10 par page).

Fichiers : [declaration-cancellation.e2e.ts](packages/app/src/e2e/declaration-cancellation.e2e.ts), [declaration-history.e2e.ts](packages/app/src/e2e/declaration-history.e2e.ts).

### 8. Notifications

- **Accusé de réception hors-canal** : email de confirmation après chaque acte structurant (déclaration, seconde déclaration), avec récapitulatif. L'usager garde une trace indépendante de l'app.

Fichier : [notifications-email-flow.e2e.ts](packages/app/src/e2e/notifications-email-flow.e2e.ts).

### 9. Consultation publique (anonyme)

- **Données d'intérêt public accessibles sans authentification** (`/stats`, `/referents`).
- **Double rendu systématique** : tout graphique a son tableau accessible (taux de déclaration K1, distribution des scores K7).
- **Minimisation des données par conception** sur les référents : la liste ne montre pas les coordonnées (révélées au click-through détail), pas de recherche par nom exposée, filtre obligatoire avant tout résultat (« sélectionnez au moins un filtre »).
- **Liens externes balisés** : `target="_blank"` + NewTabNotice.

Fichiers : [public-stats.e2e.ts](packages/app/src/e2e/public-stats.e2e.ts), [public-referents.e2e.ts](packages/app/src/e2e/public-referents.e2e.ts).

### 10. Back-office admin

- **Séparation visuelle nette** : chrome admin sans footer public ni bandeau d'aide, layout fluide à side-menu fixe.
- **Contrôle d'accès strict** : tout non-admin / anonyme → `/login`.
- **Mimoquage en lecture seule** : l'admin voit l'espace d'une entreprise mais tout acte d'écriture est bloqué (bouton désactivé + tooltip, upload → 403). Voir sans pouvoir altérer.
- **Stats outillées** : filtres (tranche d'effectif, année, seuil de stagnation), redirection des anciennes URLs vers la page unifiée, toujours avec alternative tableau.

Fichiers : [admin.e2e.ts](packages/app/src/e2e/admin.e2e.ts), [admin-declarations.e2e.ts](packages/app/src/e2e/admin-declarations.e2e.ts), [admin-referents.e2e.ts](packages/app/src/e2e/admin-referents.e2e.ts), [admin-stats.e2e.ts](packages/app/src/e2e/admin-stats.e2e.ts), [admin-impersonation-read-only.e2e.ts](packages/app/src/e2e/admin-impersonation-read-only.e2e.ts).

### 11. Pages d'erreur

- **Jamais de cul-de-sac.** 404 / 500 / 503 cohérentes : code + titre humain, message d'excuse + conseil de récupération (« rafraîchir / réessayer plus tard »), artwork `aria-hidden`, lien de retour à l'accueil. Ton rassurant et sortie toujours offerte.

Fichier : [error-pages.e2e.ts](packages/app/src/e2e/error-pages.e2e.ts).

### Transverse — La sécurité comme expérience

- **L'usager ne voit que ce qui lui appartient.** Accès fichiers : 200 pour propriétaire/admin, 401 anonyme, 404 fichier inconnu (isolation cross-SIREN), 403 secret gateway invalide. Le contrôle d'accès façonne ce que chaque profil peut faire.

Fichier : [fileUpload.e2e.ts](packages/app/src/e2e/fileUpload.e2e.ts).

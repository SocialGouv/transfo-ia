# Gérer les droits d'accès aux MCP dans LiteLLM PLIAGE

Objectif : qu'un MCP ne soit chargé dans le contexte du modèle, et ne consomme des tokens, que pour la personne qui en a besoin au moment où elle en a besoin. Les autres utilisent l'IA sans payer son coût.

Ce tuto explique comment ouvrir un serveur MCP à certaines personnes seulement, puis comment chacune ne le charge que quand elle le demande. L'exemple suivi est le MCP DSFR (`dsfr`), mais la méthode vaut pour tout MCP déclaré dans LiteLLM.

Rédigé le 26/10/2026 pour LiteLLM PLIAGE v1.85.7 et OpenCode, en v1 (v1.19.4, paquet npm `opencode-ai`) comme en v2 (v2.1.4, paquet npm `@opencode/cli`). Les points marqués *vérifié* l'ont été ce jour dans l'interface ou dans le code de ces versions. Les points marqués *à tester* restent à confirmer sur un poste.

## Ce que coûte un MCP chargé

Quand un MCP est connecté à l'agent, ses outils sont décrits au modèle dans **chaque** requête, qu'on s'en serve ou non. Une session agentique enchaîne des dizaines de requêtes, et chaque MCP ajouté s'additionne. Le cache de prompt des fournisseurs réduit le prix de ces tokens répétés, mais ils occupent toujours la fenêtre de contexte.

| Version d'OpenCode | Comment les outils MCP sont décrits | Coût pour `dsfr` (8 outils) |
|---|---|---|
| v1 | par défaut, définition complète de chaque outil (nom, description, paramètres) | environ 6 000 caractères, soit **~1 500 tokens par requête** (*mesuré*) |
| v2 | « mode code » : un catalogue compact (signature et première ligne de description de chaque outil), plafonné à environ 2 000 tokens pour l'ensemble des MCP ; au-delà, le modèle cherche les outils avec `search` | **~400 tokens par requête** (*estimé* d'après le format du catalogue) |

La v2 réduit le coût, mais il reste payé par tout le monde tant que le MCP est chargé dans l'agent principal.

Les appels d'outils coûtent en plus : leurs résultats (documentation, code d'un composant) entrent dans le contexte.

## Le principe : deux verrous

LiteLLM n'appelle jamais un MCP de lui-même. C'est le client IA (OpenCode) qui se connecte au MCP à travers LiteLLM et présente ses outils au modèle. C'est ensuite le modèle qui décide d'appeler un outil.

Il y a donc deux réglages distincts :

| Question | Où ça se règle | Qui le règle |
|---|---|---|
| Qui **a le droit** d'utiliser le MCP | LiteLLM : groupe d'accès rattaché à une clé ou à une équipe | l'admin LiteLLM |
| Qui **le charge** à un instant donné | OpenCode : sous-agent appelé par `@dsfr` dans le prompt | chaque utilisateur, prompt par prompt |

Le droit LiteLLM ne fait pas économiser de tokens : une personne qui a le droit et dont l'agent principal charge le MCP paie son coût à chaque requête. Le réglage qui économise les tokens est celui d'OpenCode (étape 3).

Exemple avec trois personnes qui ont toutes le droit :

| Moment | Personne A | Personne B | Personne C |
|---|---|---|---|
| T | IA sans MCP | écrit `@dsfr …`, le MCP est utilisé | écrit `@dsfr …`, le MCP est utilisé |
| T + 1 min | IA sans MCP | IA sans MCP | écrit `@dsfr …`, le MCP est utilisé |

## État au 26/10/2026

| Serveur | URL | Authentification | Groupe d'accès | Clés ou équipes rattachées |
|---|---|---|---|---|
| `atlassian` | `https://mcp.atlassian.com/v2/mcp?tools=all` | OAuth par utilisateur | `jira` | aucune |
| `dsfr` | `https://dsfr-mcp.onrender.com/mcp` | aucune | `dsfr` | aucune |

Sur les deux serveurs, « Allow All LiteLLM Keys » est désactivé.

## Les règles d'accès de LiteLLM v1.85.7

*Vérifié dans le code* (`mcp_server_manager.py` et `auth/user_api_key_auth_mcp.py`) :

- **Ni la clé ni son équipe n'ont de droit MCP** : aucun serveur n'est accessible.
- **Seule l'équipe a des droits** : la clé en hérite.
- **La clé et l'équipe ont chacune des droits** : seuls les serveurs présents des deux côtés restent accessibles (intersection).
- **« Allow All LiteLLM Keys » est activé sur un serveur** : toutes les clés y ont accès, quels que soient leurs droits.
- **La clé appartient à un admin du proxy** (rôle `proxy_admin` ou `proxy_admin_view_only`) **sans droit MCP explicite** : tous les serveurs sont accessibles.
- **Donner un groupe d'accès** revient à donner tous les serveurs qui portent ce groupe.

La documentation en ligne de LiteLLM affirme qu'en l'absence de toute restriction, l'accès est ouvert à tous les serveurs. Le code v1.85.7 ne fait pas cela pour les clés non admin. Recontrôler ce point après chaque montée de version.

## Étape 1 : rattacher le serveur à un groupe d'accès (admin)

Un groupe par MCP, du même nom que le serveur : on peut ainsi ouvrir chaque MCP séparément.

1. Ouvrir **MCP Servers** > **+ Add New MCP Server** > **+ Custom Server**.
2. Renseigner le nom, l'alias, l'URL et le transport (**Streamable HTTP**).
3. Choisir l'authentification (**None** pour `dsfr`).
4. Déplier **Permission Management / Access Control** :
   - **Allow All LiteLLM Keys** : désactivé ;
   - **Internal network only** : désactivé, car LiteLLM voit tous les appelants en 192.168.4.x (proxy du cluster) et ce filtre n'apporte rien ;
   - **MCP Access Groups** : taper le nom du groupe (`dsfr`) puis Entrée (le groupe est créé s'il n'existe pas).
5. Attendre « Connection successful » et la liste des outils, puis cliquer sur **Add MCP Server**.

Pour un serveur déjà enregistré, le groupe se modifie depuis le bouton d'édition de sa ligne dans **MCP Servers**.

## Étape 2 : donner le droit à une personne ou à une équipe (admin)

### Option A : par clé (une personne)

1. **Virtual Keys** > cliquer sur le **Key ID** de la clé.
2. Onglet **Settings** > **Edit Settings**.
3. Champ **MCP Servers / Access Groups** : ajouter `dsfr`.
4. **Save Changes**.

### Option B : par équipe (toutes les clés de l'équipe)

1. **Teams** > cliquer sur l'identifiant de l'équipe.
2. Onglet **Settings** > **Edit Settings**.
3. Champ **MCP Servers / Access Groups** : ajouter `dsfr`.
4. **Save Changes**.

**Ne pas mélanger les deux niveaux sans y penser.** Une clé qui a déjà ses propres droits MCP ne voit que l'intersection avec ceux de son équipe. Exemple : si la clé a `jira` et l'équipe `dsfr`, la clé ne voit **aucun** des deux. Choisir un seul niveau par population : l'équipe pour un studio entier, la clé pour quelques personnes.

### Retirer un droit

Même chemin, retirer le groupe du champ **MCP Servers / Access Groups**, puis **Save Changes**.

## Étape 3 : n'utiliser le MCP qu'à la demande (chaque utilisateur, OpenCode)

On déclare le MCP dans OpenCode, on interdit ses outils à l'agent principal, puis on crée un sous-agent `dsfr` qui est seul autorisé à s'en servir.

Fichier `opencode.json` à la racine du projet, ou config globale d'OpenCode :

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "dsfr": {
      "type": "remote",
      "url": "https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/dsfr/mcp",
      "headers": { "x-litellm-api-key": "Bearer {env:LITELLM_API_KEY}" }
    }
  },
  "permission": { "dsfr_*": "deny" },
  "agent": {
    "dsfr": {
      "mode": "subagent",
      "description": "Composants DSFR : documentation, code, accessibilité. À utiliser uniquement quand l'utilisateur écrit @dsfr.",
      "permission": { "dsfr_*": "allow" }
    }
  }
}
```

- **URL** : `/<nom-du-serveur>/mcp` n'expose que ce serveur (route *vérifiée dans le code*). L'URL `/mcp` seule exposerait tous les MCP auxquels la clé a droit, `atlassian` compris.
- **Clé** : la clé LiteLLM **personnelle** de l'utilisateur, dans la variable d'environnement `LITELLM_API_KEY`. Elle n'est jamais écrite dans le fichier.
- **Usage** : `@dsfr crée un formulaire de contact accessible`. Sans `@dsfr`, l'agent principal travaille sans le MCP.

La même config fonctionne en v1 et en v2 : la v2 lit le format v1 de `opencode.json` (`mcp`, `permission`, `agent`) et le convertit (`config/normalize.ts`, *vérifié*).

Pourquoi l'agent principal ne paie pas les tokens du MCP (*vérifié dans le code d'OpenCode v1.19.4 et v2.1.4*) :

| Mécanisme | v1.19.4 | v2.1.4 |
|---|---|---|
| Les outils MCP s'appellent `<serveur>_<outil>` (`dsfr_list_components`…), d'où le motif `dsfr_*` | `mcp/catalog.ts` | `tool/mcp.ts` |
| Un outil dont la dernière règle applicable est `deny` est **retiré de ce qu'on envoie au modèle**, pas seulement bloqué à l'appel | `resolveTools` (`session/llm/request.ts`) | `Tool.snapshot` (`tool.ts`) : absent aussi du catalogue du mode code |
| Les permissions d'un agent s'ajoutent après les permissions globales, et la dernière règle applicable l'emporte : le sous-agent `dsfr` voit donc les outils | `agent/agent.ts` | `config/plugin/agent.ts` |

- Le sous-agent travaille dans sa propre session : les outils et les résultats DSFR restent dans son contexte. L'agent principal ne reçoit que sa réponse finale.
- Seul coût résiduel pour l'agent principal : la ligne de description du sous-agent `dsfr` dans la liste des sous-agents disponibles, soit quelques dizaines de tokens.

*À tester* sur un poste avant diffusion :

- **Appels spontanés.** OpenCode permet à l'agent principal de lancer un sous-agent de lui-même, d'après sa description. La phrase « uniquement quand l'utilisateur écrit @dsfr » limite ce risque sans l'exclure.
- **En v2, `"hidden": true` sur le sous-agent.** La v2 retire les sous-agents masqués de la liste proposée à l'agent principal (`tool/plugin/subagent.ts`, *vérifié*). Cela supprimerait les appels spontanés et le coût résiduel. Reste à tester que `@dsfr` fonctionne encore sur un sous-agent masqué.
- **En-tête de clé.** `x-litellm-api-key: Bearer …` est la forme montrée dans la documentation de LiteLLM pour les clients MCP.
- **Version d'OpenCode des postes.** Ce comportement est celui de v1.19.4 (22/10/2026) et de v2.1.4 (23/10/2026) : vérifier la version installée.

## Étape 4 : vérifier

### Côté LiteLLM : ce qu'une clé voit

```bash
curl -s "https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/mcp-rest/tools/list" \
  -H "Authorization: Bearer $LITELLM_API_KEY"
```

Cet endpoint renvoie les outils de tous les serveurs auxquels la clé a droit (*vérifié dans le code*). Résultat attendu :

- clé avec le groupe `dsfr` : les 8 outils du serveur `dsfr` ;
- clé sans droit MCP : liste vide.

### Côté OpenCode

```bash
opencode mcp list
```

Le serveur `dsfr` doit apparaître connecté. Ensuite, un prompt sans `@dsfr` ne doit déclencher aucun appel `dsfr_*`, et un prompt avec `@dsfr` doit en déclencher. Les appels sont visibles dans **Logs** de LiteLLM.

## Ajouter un autre MCP

1. Déclarer le serveur avec son propre groupe d'accès, « Allow All LiteLLM Keys » désactivé (étape 1).
2. Rattacher le groupe aux clés ou à l'équipe concernées (étape 2).
3. Ajouter dans `opencode.json` le bloc `mcp`, la règle `"<nom>_*": "deny"` et un sous-agent `<nom>` (étape 3).
4. Vérifier avec `/mcp-rest/tools/list` et `opencode mcp list` (étape 4).

## Points de vigilance

- **Admins du proxy.** Leurs clés voient tous les MCP tant qu'aucun droit MCP explicite ne leur est posé.
- **Atlassian.** Le droit LiteLLM ne suffit pas : chaque personne doit aussi autoriser Atlassian avec son compte (OAuth). Le 23/10/2026, le bouton d'autorisation renvoyait `invalid_request` : voir [fix.md](fix.md).
- **Instance DSFR hébergée.** Elle tourne sur l'offre gratuite de Render (Francfort), d'après le `render.yaml` du dépôt [SocialGouv/dsfr-mcp](https://github.com/SocialGouv/dsfr-mcp). Le service se met en veille sans trafic, donc le premier appel peut être lent. Les requêtes partent vers un hébergeur tiers. Si c'est un problème, déployer `dsfr-mcp` sur le cluster et changer l'URL du serveur dans LiteLLM.
- **Coût.** Le champ « Default Cost per Query » est à 0 $ : les appels MCP ne consomment pas de budget LiteLLM, seuls les tokens du modèle comptent.

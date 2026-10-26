# Corriger l'erreur `invalid_request` du MCP Atlassian dans LiteLLM PLIAGE

## Contexte

Un serveur MCP `atlassian` est déclaré dans LiteLLM PLIAGE (v1.85.7, page MCP Servers). Il pointe vers le MCP officiel d'Atlassian (`https://mcp.atlassian.com/v2/mcp?tools=all`) en OAuth par utilisateur. Chaque chef de projet accède ainsi à Jira (jira-mcas) avec son propre compte et ne voit que ses projets, sans rien installer sur son poste.

Le problème : le bouton **Authorize & Fetch Token** renvoie `{"detail":"invalid_request"}`.

## Cause

LiteLLM croit être servi en **http** alors qu'il est exposé en **https**.

- Le https est géré par le proxy frontal du cluster, qui parle ensuite en http à LiteLLM.
- LiteLLM ne fait pas confiance aux en-têtes `X-Forwarded-*` de ce proxy (vu en 192.168.4.22). Il ignore donc `X-Forwarded-Proto: https`.
- Au moment de l'autorisation, LiteLLM compare l'adresse de retour envoyée par son interface (`https://litellm.pliage-prod…/ui/mcp/oauth/callback`) à sa propre adresse (`http://litellm.pliage-prod…`). Les protocoles diffèrent, donc il refuse avec `invalid_request` avant même de contacter Atlassian.

La preuve : la page publique de métadonnées OAuth annonce une adresse en http.

```bash
curl -s https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/.well-known/oauth-authorization-server | grep -o '"issuer":"[^"]*"'
# "issuer":"http://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr"
```

Le code de LiteLLM v1.85.7 concerné :

- [`oauth_utils.py`](https://github.com/BerriAI/litellm/blob/v1.85.7/litellm/proxy/_experimental/mcp_server/oauth_utils.py) : la fonction `validate_trusted_redirect_uri` exige le même protocole et le même hôte.
- [`ip_address_utils.py`](https://github.com/BerriAI/litellm/blob/v1.85.7/litellm/proxy/auth/ip_address_utils.py) : les `X-Forwarded-*` ne sont pris en compte que si `use_x_forwarded_for` vaut `true` **et** que l'appelant est dans `mcp_trusted_proxy_ranges`.

## Étape 1 : faire confiance au proxy frontal (déploiement LiteLLM)

Ce réglage ne se modifie pas depuis l'interface : il faut passer par le `config.yaml` du déploiement.

1. Dans le `config.yaml` de LiteLLM PLIAGE (values Helm ou ConfigMap), ajouter ces deux clés au bloc `general_settings` existant :

   ```yaml
   general_settings:
     use_x_forwarded_for: true
     mcp_trusted_proxy_ranges: ["192.168.4.0/24"]
   ```

   Adapter la plage pour couvrir toutes les adresses possibles du proxy frontal. LiteLLM le voit aujourd'hui en 192.168.4.22 (page MCP Servers, onglet Network Settings).

2. Vérifier que le proxy frontal envoie bien `X-Forwarded-Proto: https`.

3. Redéployer LiteLLM.

4. Vérifier que l'adresse annoncée commence par `https://` :

   ```bash
   curl -s https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/.well-known/oauth-authorization-server | grep -o '"issuer":"[^"]*"'
   ```

Effet secondaire attendu : LiteLLM utilisera la vraie adresse IP des utilisateurs (`X-Forwarded-For`), dans les logs comme dans les contrôles d'accès par IP.

## Étape 2 : autoriser le domaine LiteLLM chez Atlassian (admin de l'organisation jira-mcas, une seule fois)

Atlassian n'accepte les connexions OAuth à son MCP que depuis une liste de domaines. Les outils connus y figurent déjà (Claude, ChatGPT, Cursor, VS Code…), mais pas notre LiteLLM ([liste Atlassian](https://support.atlassian.com/security-and-access-policies/docs/available-atlassian-rovo-mcp-server-domains/)).

1. Aller sur https://admin.atlassian.com et choisir l'organisation de jira-mcas.
2. Ouvrir **Connectors > Atlassian MCP server**. Selon l'interface, le chemin peut aussi être **Rovo > Rovo MCP server > Domain settings**.
3. Cliquer sur **Add domain** et saisir :

   ```
   https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/**
   ```

4. Enregistrer.

Documentation : [Control Atlassian Rovo MCP server settings](https://support.atlassian.com/security-and-access-policies/docs/control-atlassian-rovo-mcp-server-settings/).

## Étape 3 : tester

1. Dans LiteLLM, aller dans **MCP Servers**, ouvrir `atlassian`, puis **Settings** et **Edit Settings**.
2. Cliquer sur **Authorize & Fetch Token**.
3. Se connecter à Atlassian, choisir **jira-mcas** et accepter.
4. Résultat attendu : retour dans LiteLLM, et la liste des outils s'affiche dans l'onglet **MCP Tools**.

## Si ça bloque encore

| Message | Cause probable | Action |
|---|---|---|
| `{"detail":"invalid_request"}` | LiteLLM se croit toujours en http | Reprendre l'étape 1 et revérifier avec le `curl` |
| « Your organization admin must authorize access from this redirect URL » | Domaine absent de la liste, ou pas encore pris en compte | Supprimer le domaine, le rajouter à l'identique, puis réessayer en navigation privée ([article Atlassian](https://support.atlassian.com/rovo/kb/fix-oauth-consent-block-for-atlassian-rovo-mcp-server-in-atlassian-cloud/)) |

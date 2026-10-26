# Tuto : modèles Scaleway dans OpenCode Desktop via LiteLLM SDPC (Windows)

Vérifié le 2026-10-21 avec OpenCode Desktop 1.19.3 sur Windows 11. Durée : 10 minutes, hors obtention de la clé.

## Le piège à éviter

OpenCode propose un provider « Scaleway » natif (`/connect` puis Scaleway). Il appelle directement `https://api.scaleway.ai/v1` et attend une secret key IAM Scaleway (UUID de 36 caractères). Avec une clé LiteLLM (`sk-` + 22 caractères), chaque requête échoue avec :

```
Forbidden: insufficient permissions to access the resource
```

Dans notre contexte, les modèles Scaleway sont servis par l'instance LiteLLM SDPC. Il faut donc déclarer un provider OpenAI-compatible qui pointe sur cette instance, et ne pas utiliser le provider Scaleway natif.

## Pré-requis

- Compte LiteLLM SDPC activé (lien d'invitation Tchap, ProConnect, mot de passe LiteLLM). Voir le guide interne « LiteLLM SDPC ».
- Une clé virtuelle LiteLLM créée dans l'interface, menu Virtual Keys puis Create New Key :
  - Team : son équipe `sdpc-…` (sans équipe, la clé n'a accès à aucun modèle).
  - Key name : `<équipe>/<prenom.nom>/opencode`.
  - Models : « all team models ». Expire : 90 jours.
  - La clé s'affiche une seule fois. La copier dans un gestionnaire de mots de passe.
- Sortie HTTPS directe vers l'instance (le proxy d'entreprise n'est pas nécessaire). Test :

```powershell
Invoke-WebRequest -NoProxy -UseBasicParsing https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/v1/models -Headers @{ Authorization = "Bearer <clé>" } | Select-Object StatusCode
```

Attendu : 200. Un 401 signifie clé invalide ou expirée.

## Étapes

### 1. Stocker la clé dans une variable d'environnement utilisateur

En PowerShell, une fois pour toutes :

```powershell
[Environment]::SetEnvironmentVariable('LITELLM_API_KEY', '<clé>', 'User')
```

La clé ne figure ainsi dans aucun fichier de config ni dépôt.

### 2. Déclarer le provider dans la config globale OpenCode

Fichier `%USERPROFILE%\.config\opencode\opencode.json`. S'il existe déjà, ajouter l'entrée `litellm-sdpc` dans le bloc `provider` et la ligne `model`, sans toucher au reste (`mcp`, `default_agent`, autres providers).

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "litellm-sdpc/scaleway/deepseek-v4-flash-0731",
  "provider": {
    "litellm-sdpc": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "LiteLLM SDPC (Scaleway)",
      "options": {
        "baseURL": "https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/v1",
        "apiKey": "{env:LITELLM_API_KEY}"
      },
      "models": {
        "scaleway/deepseek-v4-flash-0731": {
          "name": "DeepSeek V4 Flash (code au quotidien)",
          "limit": { "context": 256000, "output": 32000 }
        },
        "scaleway/deepseek-v4.1-flash": {
          "name": "DeepSeek V4.1 Flash",
          "limit": { "context": 256000, "output": 32000 }
        },
        "scaleway/glm-5.3": {
          "name": "GLM 5.3 (cher, usage ponctuel)",
          "limit": { "context": 256000, "output": 16000 }
        },
        "scaleway/qwen3.6-35b-a3b": {
          "name": "Qwen 3.6 35B (petites tâches, vision)",
          "limit": { "context": 256000, "output": 32000 }
        },
        "scaleway/qwen3.5-397b-a17b": {
          "name": "Qwen 3.5 397B (second avis)",
          "limit": { "context": 250000, "output": 16000 }
        }
      }
    }
  }
}
```

Les identifiants de modèles sont ceux renvoyés par `/v1/models` de l'instance (préfixe `scaleway/`). Les limites viennent de la page « Supported models » de Scaleway.

Vérifier que le JSON est valide :

```powershell
Get-Content $env:USERPROFILE\.config\opencode\opencode.json -Raw | ConvertFrom-Json | Out-Null
```

### 3. Retirer le provider Scaleway natif s'il a été connecté par erreur

Si `/connect` Scaleway a été utilisé, la clé est dans `%USERPROFILE%\.local\share\opencode\auth.json` sous l'entrée `scaleway`. Supprimer cette entrée (ou remettre `{}` si c'est la seule), sinon les modèles Scaleway natifs restent proposés et échouent.

### 4. Relancer OpenCode Desktop

Quitter complètement l'application (pas seulement fermer la fenêtre), puis la relancer : la variable d'environnement n'est lue qu'au démarrage.

### 5. Vérifier

- Dans une nouvelle session, le modèle affiché est « LiteLLM SDPC (Scaleway) / DeepSeek V4 Flash ». Les autres modèles sont dans le sélecteur.
- Envoyer un message. En cas d'erreur, lire `%USERPROFILE%\.local\share\opencode\log\opencode.log` : les lignes `stream error` donnent le provider et le modèle utilisés.

Test hors OpenCode, pour isoler un problème de clé ou de réseau :

```powershell
$body = '{"model":"scaleway/deepseek-v4-flash-0731","messages":[{"role":"user","content":"Réponds ok."}],"max_tokens":50}'
Invoke-WebRequest -NoProxy -UseBasicParsing -Method Post -Uri https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/v1/chat/completions -Headers @{ Authorization = "Bearer $env:LITELLM_API_KEY"; 'Content-Type' = 'application/json' } -Body $body | Select-Object StatusCode
```

## Quel modèle

Prix du guide interne, en euros par million de tokens, entrée / sortie :

| Usage | Modèle | Prix |
|---|---|---|
| Code au quotidien, agents | scaleway/deepseek-v4-flash-0731 | 0,40 / 0,80 |
| Petites tâches, tickets, vision | scaleway/qwen3.6-35b-a3b | 0,25 / 1,50 |
| Second avis sur un problème difficile | scaleway/qwen3.5-397b-a17b | 0,60 / 3,60 |
| À éviter en usage courant | scaleway/glm-5.2 (route vers glm-5.3 depuis octobre 2026) | 1,80 / 5,50 |

Les prix de glm-5.3 et deepseek-v4.1-flash ne figurent pas dans le guide : les lire dans l'interface LiteLLM avant un usage soutenu. Plafonds par personne : 30 € par mois, 60 requêtes et 200 k tokens par minute.

## Dépannage

- `Forbidden: insufficient permissions to access the resource` : la clé LiteLLM a été donnée au provider Scaleway natif. Reprendre à l'étape 2 et 3.
- Clé non résolue (erreur d'authentification alors que le test hors OpenCode passe) : OpenCode n'a pas été relancé après l'étape 1, ou la variable a été posée dans une autre session. Solution de repli : mettre la clé en clair dans `options.apiKey`.
- `ExceededBudget` : plafond mensuel atteint, remise à zéro le 1er du mois. Voir avec le Studio Tech.
- Données modifiées dans les réponses (`[…_REDACTED]`) : filtre RGPD de l'instance, qui masque e-mails, téléphones, codes postaux, IBAN et NIR avant l'envoi au modèle. Pas un bug du modèle.
- Réponse vide avec `reasoning_tokens` consommés : `max_tokens` trop bas pour un modèle qui raisonne. Augmenter la limite.
- Ne pas définir `HTTPS_PROXY` vers le proxy authentifiant : l'app sort en direct.

## Règles

- Une clé par personne et par outil, jamais dans un dépôt.
- Renouveler la clé tous les 90 jours depuis Virtual Keys.

## Références

- Guide interne « LiteLLM SDPC, guide pour les développeurs internes » (Studio Tech).
- https://opencode.ai/docs/providers/
- https://www.scaleway.com/en/docs/generative-apis/reference-content/supported-models/
- https://www.scaleway.com/en/docs/generative-apis/troubleshooting/fixing-common-issues/

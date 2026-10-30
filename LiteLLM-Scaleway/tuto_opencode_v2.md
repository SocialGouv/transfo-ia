# Tuto : OpenCode v2 avec les modèles LiteLLM SDPC

Rédigé le 30/10/2026 pour OpenCode 2.2.2. Config validée contre le schéma officiel, pas encore testée sur un poste.

## Avant de commencer

- Avoir une clé LiteLLM SDPC (voir « Pré-requis » dans [le tuto v1](tuto_install_scaleway.md)).
- Si la v1 est installée, sauvegarder `~/.config/opencode` et `~/.local/share/opencode`. La v2 migre la base au premier lancement.

## 1. Installer

Si la v1 a été installée avec npm, la désinstaller : `npm uninstall -g opencode-ai`. Puis :

```bash
npm install -g @opencode/cli
opencode --version   # doit afficher 2.x
```

## 2. Enregistrer la clé

Linux ou macOS :

```bash
echo 'export LITELLM_API_KEY="<clé>"' >> ~/.bashrc && source ~/.bashrc
```

Windows (PowerShell) :

```powershell
[Environment]::SetEnvironmentVariable('LITELLM_API_KEY', '<clé>', 'User')
```

N'utilisez pas `/connect` : en v2, il gère mal les providers personnalisés (ticket ouvert [#51527](https://github.com/anomalyco/opencode/issues/51527)).

## 3. Écrire la config

Fichier `~/.config/opencode/opencode.json` (Windows : `%USERPROFILE%\.config\opencode\opencode.json`). S'il existe déjà, ajoutez seulement le bloc `litellm-sdpc` et la ligne `model`.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "litellm-sdpc/scaleway/deepseek-v4-flash-0731",
  "providers": {
    "litellm-sdpc": {
      "name": "LiteLLM SDPC (Scaleway)",
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/v1",
        "apiKey": "{env:LITELLM_API_KEY}"
      },
      "models": {
        "scaleway/deepseek-v4-flash-0731": {
          "name": "DeepSeek V4 Flash (code au quotidien)",
          "capabilities": { "tools": true },
          "limit": { "context": 256000, "output": 32000 }
        },
        "scaleway/deepseek-v4.1-flash": {
          "name": "DeepSeek V4.1 Flash",
          "capabilities": { "tools": true },
          "limit": { "context": 256000, "output": 32000 }
        },
        "scaleway/glm-5.3": {
          "name": "GLM 5.3 (cher, usage ponctuel)",
          "capabilities": { "tools": true },
          "limit": { "context": 256000, "output": 16000 }
        },
        "scaleway/qwen3.6-35b-a3b": {
          "name": "Qwen 3.6 35B (petites tâches, vision)",
          "capabilities": { "tools": true, "input": ["text", "image"], "output": ["text"] },
          "limit": { "context": 256000, "output": 32000 }
        },
        "scaleway/qwen3.5-397b-a17b": {
          "name": "Qwen 3.5 397B (second avis)",
          "capabilities": { "tools": true },
          "limit": { "context": 250000, "output": 16000 }
        }
      }
    }
  }
}
```

Pour ajouter un modèle, prenez son identifiant dans la liste renvoyée par `/v1/models` (étape 5).

## 4. Relancer

Quittez complètement OpenCode, puis relancez-le : la clé n'est lue qu'au démarrage. Dans `/models`, les modèles apparaissent sous « LiteLLM SDPC (Scaleway) ».

## 5. En cas d'erreur

Testez la clé sans passer par OpenCode. Résultat attendu : 200 (401 = clé invalide ou expirée).

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $LITELLM_API_KEY" \
  https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/v1/models
```

```powershell
Invoke-WebRequest -NoProxy -UseBasicParsing https://litellm.pliage-prod.socle-ia.data-ia.prod.atlas.fabrique.social.gouv.fr/v1/models -Headers @{ Authorization = "Bearer $env:LITELLM_API_KEY" } | Select-Object StatusCode
```

| Symptôme | Cause |
|---|---|
| Erreur d'authentification dans OpenCode, alors que le test donne 200 | OpenCode n'a pas été relancé après l'étape 2 |
| `Forbidden: insufficient permissions` | Vous utilisez le provider Scaleway natif au lieu de `litellm-sdpc` |
| Modèle introuvable | Son identifiant n'est pas dans `/v1/models` |
| `ExceededBudget` | Plafond mensuel atteint, remis à zéro le 1er du mois |

## Vous venez de la v1 ?

La v2 lit encore l'ancien format, mais la clé saisie en v1 avec `/connect` ou `opencode auth login` peut ne pas être reprise. Passez par la variable (étape 2).

Pour passer au nouveau format :

| v1 | v2 |
|---|---|
| `provider` | `providers` |
| `npm` | `package` |
| `options.baseURL`, `options.apiKey` | `settings.baseURL`, `settings.apiKey` |
| `tool_call: true` | `capabilities.tools: true` |
| `modalities` | `capabilities.input`, `capabilities.output` |
| `options` d'un modèle | `body` |

Guide officiel : https://opencode.ai/v2/docs/migrate-v1/

# 🧩 Features

[← Configuration](./infos-devcontainer-02-configuration-base.md) | [Index](./infos-devcontainer-00-index.md) | [Extensions →](./infos-devcontainer-04-extensions-vscode.md)

## Qu'est-ce qu'une Feature ?

Les **Features** sont des unités réutilisables qui ajoutent des outils ou runtimes au Dev Container.

Avantages :
- ✅ Installation simplifiée d'outils
- ✅ Réutilisables entre projets
- ✅ Versionnées et maintenues
- ✅ Combinables

## Syntaxe de base

```json
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    }
  }
}
```

## Features officielles

Liste complète : https://containers.dev/features

### Node.js

```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18",
      "nodeGypDependencies": true,
      "nvmVersion": "latest"
    }
  }
}
```

```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": "20"
  }
}
```

### Python

```json
{
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11",
      "installTools": true
    }
  }
}
```

### Java

```json
{
  "features": {
    "ghcr.io/devcontainers/features/java:1": {
      "version": "17",
      "installMaven": true,
      "installGradle": true
    }
  }
}
```

### Go

```json
{
  "features": {
    "ghcr.io/devcontainers/features/go:1": {
      "version": "1.21"
    }
  }
}
```

### Rust

```json
{
  "features": {
    "ghcr.io/devcontainers/features/rust:1": {
      "version": "latest"
    }
  }
}
```

### PHP

```json
{
  "features": {
    "ghcr.io/devcontainers/features/php:1": {
      "version": "8.2",
      "installComposer": true
    }
  }
}
```

### Ruby

```json
{
  "features": {
    "ghcr.io/devcontainers/features/ruby:1": {
      "version": "3.2"
    }
  }
}
```

## Docker-in-Docker

Utiliser Docker depuis le container.

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "version": "latest",
      "moby": true
    }
  }
}
```

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {}
  }
}
```

## Git

```json
{
  "features": {
    "ghcr.io/devcontainers/features/git:1": {
      "version": "latest",
      "ppa": true
    }
  }
}
```

## GitHub CLI

```json
{
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {
      "version": "latest"
    }
  }
}
```

## AWS CLI

```json
{
  "features": {
    "ghcr.io/devcontainers/features/aws-cli:1": {
      "version": "latest"
    }
  }
}
```

## Azure CLI

```json
{
  "features": {
    "ghcr.io/devcontainers/features/azure-cli:1": {
      "version": "latest"
    }
  }
}
```

## kubectl

```json
{
  "features": {
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {
      "version": "latest",
      "helm": "latest",
      "minikube": "none"
    }
  }
}
```

## Terraform

```json
{
  "features": {
    "ghcr.io/devcontainers/features/terraform:1": {
      "version": "latest"
    }
  }
}
```

## Common Utils

Outils Unix courants (curl, wget, jq, etc.).

```json
{
  "features": {
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true,
      "installOhMyZsh": true,
      "configureZshAsDefaultShell": true,
      "username": "vscode",
      "upgradePackages": true
    }
  }
}
```

## Multiples Features

```json
{
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true,
      "installOhMyZsh": true
    }
  }
}
```

## Exemples par stack

### Full Stack JavaScript

```json
{
  "name": "Full Stack JS",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true
    }
  }
}
```

### Python Data Science

```json
{
  "name": "Python Data Science",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11",
      "installTools": true
    },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {}
  },
  "postCreateCommand": "pip install jupyter pandas numpy matplotlib scikit-learn"
}
```

### DevOps

```json
{
  "name": "DevOps Tools",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {
      "version": "latest",
      "helm": "latest"
    },
    "ghcr.io/devcontainers/features/terraform:1": {},
    "ghcr.io/devcontainers/features/aws-cli:1": {},
    "ghcr.io/devcontainers/features/azure-cli:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/git:1": {}
  }
}
```

### Go + PostgreSQL

```json
{
  "name": "Go + PostgreSQL",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/go:1": {
      "version": "1.21"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true
    }
  }
}
```

## Features communautaires

Chercher des features : https://containers.dev/features

Exemples :
- `ghcr.io/eitsupi/devcontainer-features/jq-likes:2`
- `ghcr.io/devcontainers-contrib/features/redis-server:1`
- `ghcr.io/devcontainers-contrib/features/postgres:1`

### Redis

```json
{
  "features": {
    "ghcr.io/devcontainers-contrib/features/redis-server:1": {
      "version": "latest"
    }
  }
}
```

### PostgreSQL

```json
{
  "features": {
    "ghcr.io/devcontainers-contrib/features/postgres:1": {
      "version": "15"
    }
  }
}
```

### MongoDB

```json
{
  "features": {
    "ghcr.io/devcontainers-contrib/features/mongodb:1": {
      "version": "6"
    }
  }
}
```

## Créer sa propre Feature

### Structure

```
my-feature/
├── devcontainer-feature.json
└── install.sh
```

### devcontainer-feature.json

```json
{
  "id": "my-tool",
  "version": "1.0.0",
  "name": "My Tool",
  "description": "Installs My Tool",
  "options": {
    "version": {
      "type": "string",
      "default": "latest",
      "description": "Version to install"
    }
  }
}
```

### install.sh

```bash
#!/bin/bash
set -e

VERSION="${VERSION:-"latest"}"

echo "Installing My Tool version ${VERSION}..."

# Installation logic
apt-get update
apt-get install -y my-tool

echo "Done!"
```

### Utilisation

```json
{
  "features": {
    "./local-features/my-tool": {
      "version": "1.0.0"
    }
  }
}
```

## Options avancées

### Installation conditionnelle

```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    }
  },
  "overrideFeatureInstallOrder": [
    "ghcr.io/devcontainers/features/common-utils",
    "ghcr.io/devcontainers/features/node"
  ]
}
```

### Variables d'environnement

Certaines features ajoutent automatiquement des variables d'environnement.

```bash
# Exemple : Node.js feature ajoute
export NVM_DIR="/usr/local/share/nvm"
export PATH="$NVM_DIR/versions/node/v18.0.0/bin:$PATH"
```

## Debugging Features

Voir les logs d'installation :

```bash
# Dans VS Code
F1 → "Dev Containers: Show Container Log"
```

## Features populaires

1. **common-utils** - Outils Unix de base
2. **docker-in-docker** - Docker dans Docker
3. **git** - Git dernière version
4. **github-cli** - CLI GitHub
5. **node** - Node.js
6. **python** - Python
7. **go** - Go
8. **rust** - Rust
9. **java** - Java
10. **kubectl-helm-minikube** - Kubernetes tools

## Bonnes pratiques

1. **Utiliser des versions spécifiques** : éviter "latest" en production
2. **Limiter le nombre de features** : plus rapide à build
3. **Combiner features intelligemment** : éviter les conflits
4. **Tester localement** : avant de commiter
5. **Documenter les features utilisées** : dans README.md

[← Configuration](./infos-devcontainer-02-configuration-base.md) | [Index](./infos-devcontainer-00-index.md) | [Extensions →](./infos-devcontainer-04-extensions-vscode.md)

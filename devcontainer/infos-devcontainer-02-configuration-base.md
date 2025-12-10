# ⚙️ Configuration de base

[← Introduction](./infos-devcontainer-01-introduction-installation.md) | [Index](./infos-devcontainer-00-index.md) | [Features →](./infos-devcontainer-03-features.md)

## Structure devcontainer.json

```json
// .devcontainer/devcontainer.json
{
  "name": "Mon Projet",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",

  "customizations": {
    "vscode": {
      "extensions": [],
      "settings": {}
    }
  },

  "forwardPorts": [],
  "postCreateCommand": "",
  "remoteUser": "vscode"
}
```

## Propriétés principales

### name

Nom du Dev Container (affiché dans VS Code).

```json
{
  "name": "Mon Projet Node.js"
}
```

### image

Image Docker à utiliser (depuis Docker Hub ou Microsoft Container Registry).

```json
{
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18"
}
```

```json
{
  "image": "node:18-alpine"
}
```

### build (Alternative à image)

Utiliser un Dockerfile personnalisé.

```json
{
  "build": {
    "dockerfile": "Dockerfile"
  }
}
```

```json
{
  "build": {
    "dockerfile": "Dockerfile",
    "context": "..",
    "args": {
      "NODE_VERSION": "18"
    }
  }
}
```

### Dockerfile personnalisé

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/javascript-node:18

# Installer des outils supplémentaires
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Installer des packages npm globaux
RUN npm install -g nodemon typescript

# User non-root
USER node
```

## Lifecycle Scripts

### postCreateCommand

Exécuté après la création du container (une seule fois).

```json
{
  "postCreateCommand": "npm install"
}
```

```json
{
  "postCreateCommand": "npm install && npm run build"
}
```

### postStartCommand

Exécuté à chaque démarrage du container.

```json
{
  "postStartCommand": "npm start"
}
```

### postAttachCommand

Exécuté quand VS Code se connecte au container.

```json
{
  "postAttachCommand": "echo 'Bienvenue !'"
}
```

### Commandes multiples

```json
{
  "postCreateCommand": "npm install",
  "postStartCommand": "git config --global user.name 'Dev' && git config --global user.email 'dev@example.com'",
  "postAttachCommand": "npm run watch"
}
```

Ou avec un script :

```json
{
  "postCreateCommand": "bash .devcontainer/setup.sh"
}
```

```bash
# .devcontainer/setup.sh
#!/bin/bash
echo "Configuration de l'environnement..."
npm install
npm run build
echo "Prêt !"
```

## remoteUser

Utilisateur dans le container.

```json
{
  "remoteUser": "node"
}
```

```json
{
  "remoteUser": "vscode"
}
```

Par défaut : `root` (non recommandé).

## workspaceFolder

Dossier de travail dans le container.

```json
{
  "workspaceFolder": "/workspace"
}
```

```json
{
  "workspaceFolder": "/home/node/app"
}
```

## workspaceMount

Monter le workspace à un endroit spécifique.

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind",
  "workspaceFolder": "/workspace"
}
```

## runArgs

Arguments Docker supplémentaires.

```json
{
  "runArgs": [
    "--env-file", ".env",
    "--network", "host"
  ]
}
```

```json
{
  "runArgs": [
    "--cap-add=SYS_PTRACE",
    "--security-opt", "seccomp=unconfined"
  ]
}
```

## containerEnv

Variables d'environnement dans le container.

```json
{
  "containerEnv": {
    "NODE_ENV": "development",
    "PORT": "3000",
    "DATABASE_URL": "postgresql://user:pass@db:5432/mydb"
  }
}
```

## remoteEnv

Variables d'environnement pour l'utilisateur distant.

```json
{
  "remoteEnv": {
    "PATH": "${containerEnv:PATH}:/custom/bin",
    "MY_VAR": "${localEnv:MY_LOCAL_VAR}"
  }
}
```

## Exemples complets

### Node.js + PostgreSQL

```json
// .devcontainer/devcontainer.json
{
  "name": "Node.js + PostgreSQL",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  },

  "forwardPorts": [3000, 5432],

  "postCreateCommand": "npm install",

  "remoteUser": "node"
}
```

```yaml
# .devcontainer/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    network_mode: service:db
    environment:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/mydb

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb

volumes:
  postgres-data:
```

### Python + MongoDB

```json
// .devcontainer/devcontainer.json
{
  "name": "Python + MongoDB",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff"
      ]
    }
  },

  "forwardPorts": [8000, 27017],

  "postCreateCommand": "pip install -r requirements.txt",

  "containerEnv": {
    "MONGODB_URL": "mongodb://mongo:27017"
  },

  "remoteUser": "vscode"
}
```

### Full Stack (React + Node + PostgreSQL)

```json
// .devcontainer/devcontainer.json
{
  "name": "Full Stack App",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        "ms-azuretools.vscode-docker",
        "cweijan.vscode-postgresql-client2"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": true
        }
      }
    }
  },

  "forwardPorts": [3000, 5000, 5432],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "notify"
    },
    "5000": {
      "label": "Backend API",
      "onAutoForward": "silent"
    }
  },

  "postCreateCommand": "npm install && cd client && npm install",

  "remoteUser": "node"
}
```

## Commentaires dans devcontainer.json

Utiliser `//` pour les commentaires :

```json
{
  "name": "Mon Projet",
  // Image de base
  "image": "node:18",

  // Extensions VS Code
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint"
      ]
    }
  }
}
```

## Validation

VS Code valide automatiquement `devcontainer.json`.

Schema JSON : `https://containers.dev/schema/devcontainer.json`

## Rebuild

Après modification de `devcontainer.json` ou `Dockerfile` :

1. `F1` → "Dev Containers: Rebuild Container"
2. Ou redémarrer VS Code

## Configuration minimale vs complète

### Minimale

```json
{
  "image": "node:18"
}
```

### Complète

```json
{
  "name": "Mon Projet",
  "build": {
    "dockerfile": "Dockerfile",
    "args": { "NODE_VERSION": "18" }
  },
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    }
  },
  "customizations": {
    "vscode": {
      "extensions": ["dbaeumer.vscode-eslint"],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  },
  "forwardPorts": [3000],
  "portsAttributes": {
    "3000": {
      "label": "App",
      "onAutoForward": "notify"
    }
  },
  "postCreateCommand": "npm install",
  "postStartCommand": "npm run dev",
  "remoteUser": "node",
  "workspaceFolder": "/workspace",
  "mounts": [
    "source=${localWorkspaceFolder}/.ssh,target=/home/node/.ssh,readonly,type=bind"
  ],
  "containerEnv": {
    "NODE_ENV": "development"
  }
}
```

## Documentation

Toutes les propriétés : https://containers.dev/implementors/json_reference/

[← Introduction](./infos-devcontainer-01-introduction-installation.md) | [Index](./infos-devcontainer-00-index.md) | [Features →](./infos-devcontainer-03-features.md)

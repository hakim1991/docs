# 📋 Templates et Exemples

[← Docker Compose](./infos-devcontainer-07-docker-compose.md) | [Index](./infos-devcontainer-00-index.md) | [Debugging →](./infos-devcontainer-09-debugging.md)

## Utiliser un template

### Via VS Code

1. `F1` → "Dev Containers: Add Dev Container Configuration Files..."
2. Choisir un template (Node.js, Python, etc.)
3. Configurer les options
4. Fichiers créés automatiquement

### Via CLI

```bash
devcontainers templates apply \
  --template-id ghcr.io/devcontainers/templates/javascript-node \
  --template-args '{"imageVariant":"18-bullseye"}'
```

## Templates officiels

Liste : https://containers.dev/templates

- Alpine
- Debian
- Ubuntu
- Node.js
- Python
- Go
- Rust
- Java
- PHP
- Ruby
- .NET
- C++
- Et plus...

## Template Node.js complet

```json
// .devcontainer/devcontainer.json
{
  "name": "Node.js App",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true,
      "installOhMyZsh": true,
      "upgradePackages": true
    }
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "christian-kohler.npm-intellisense",
        "eg2.vscode-npm-script",
        "eamodio.gitlens",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": true
        },
        "javascript.updateImportsOnFileMove.enabled": "always",
        "typescript.updateImportsOnFileMove.enabled": "always"
      }
    }
  },

  "forwardPorts": [3000],

  "portsAttributes": {
    "3000": {
      "label": "Application",
      "onAutoForward": "notify"
    }
  },

  "postCreateCommand": "npm install",

  "remoteUser": "node"
}
```

## Template Python complet

```json
// .devcontainer/devcontainer.json
{
  "name": "Python App",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true
    }
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "ms-python.black-formatter",
        "ms-toolsai.jupyter",
        "eamodio.gitlens"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.ruffEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.codeActionsOnSave": {
            "source.organizeImports": true
          }
        }
      }
    }
  },

  "forwardPorts": [8000],

  "postCreateCommand": "pip install -r requirements.txt",

  "remoteUser": "vscode"
}
```

## Template Go complet

```json
// .devcontainer/devcontainer.json
{
  "name": "Go App",
  "image": "mcr.microsoft.com/devcontainers/go:1.21",

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "golang.go",
        "eamodio.gitlens",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "go.toolsManagement.autoUpdate": true,
        "go.lintTool": "golangci-lint",
        "go.lintOnSave": "package",
        "go.formatTool": "goimports",
        "editor.formatOnSave": true
      }
    }
  },

  "forwardPorts": [8080],

  "postCreateCommand": "go mod download",

  "remoteUser": "vscode"
}
```

## Template Rust complet

```json
// .devcontainer/devcontainer.json
{
  "name": "Rust App",
  "image": "mcr.microsoft.com/devcontainers/rust:1",

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "rust-lang.rust-analyzer",
        "vadimcn.vscode-lldb",
        "serayuzgur.crates",
        "eamodio.gitlens"
      ],
      "settings": {
        "rust-analyzer.checkOnSave.command": "clippy",
        "editor.formatOnSave": true
      }
    }
  },

  "postCreateCommand": "cargo build",

  "remoteUser": "vscode"
}
```

## Template Monorepo (Full Stack)

```
monorepo/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── docker-compose.yml
│   └── Dockerfile
├── frontend/
│   └── package.json
├── backend/
│   └── package.json
└── packages/
    └── shared/
```

```json
// .devcontainer/devcontainer.json
{
  "name": "Monorepo",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "dsznajder.es7-react-js-snippets",
        "bradlc.vscode-tailwindcss",
        "cweijan.vscode-postgresql-client2",
        "eamodio.gitlens",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode"
      }
    }
  },

  "forwardPorts": [3000, 5000, 5432],

  "portsAttributes": {
    "3000": { "label": "Frontend" },
    "5000": { "label": "Backend" },
    "5432": { "label": "Database", "onAutoForward": "ignore" }
  },

  "postCreateCommand": "npm install && npm run bootstrap",

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
      - node-modules-frontend:/workspace/frontend/node_modules
      - node-modules-backend:/workspace/backend/node_modules
      - node-modules-shared:/workspace/packages/shared/node_modules
    command: sleep infinity
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/mydb

  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: postgres

volumes:
  node-modules-frontend:
  node-modules-backend:
  node-modules-shared:
  postgres-data:
```

## Template DevOps

```json
// .devcontainer/devcontainer.json
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
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "hashicorp.terraform",
        "amazonwebservices.aws-toolkit-vscode",
        "ms-vscode.azurecli",
        "ms-azuretools.vscode-bicep",
        "eamodio.gitlens",
        "redhat.vscode-yaml"
      ]
    }
  },

  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,readonly,type=bind",
    "source=${localEnv:HOME}/.kube,target=/home/vscode/.kube,type=bind",
    "source=${localEnv:HOME}/.aws,target=/home/vscode/.aws,type=bind"
  ],

  "remoteUser": "vscode"
}
```

## Template Data Science

```json
// .devcontainer/devcontainer.json
{
  "name": "Data Science",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {
      "installZsh": true
    }
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-keymap",
        "ms-toolsai.jupyter-renderers",
        "ms-python.black-formatter",
        "eamodio.gitlens"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "jupyter.askForKernelRestart": false
      }
    }
  },

  "forwardPorts": [8888],

  "postCreateCommand": "pip install jupyter pandas numpy matplotlib scikit-learn seaborn plotly",

  "remoteUser": "vscode"
}
```

## Créer son propre template

### Structure

```
my-template/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── devcontainer-template.json
└── README.md
```

### devcontainer-template.json

```json
{
  "id": "my-template",
  "version": "1.0.0",
  "name": "My Template",
  "description": "Template for my stack",
  "options": {
    "nodeVersion": {
      "type": "string",
      "description": "Node.js version",
      "default": "18",
      "enum": ["16", "18", "20"]
    }
  }
}
```

### Publier le template

```bash
# Sur GitHub
# Créer un repo : my-templates
# Ajouter dans src/my-template/
# Push
git push
```

### Utiliser le template

```bash
devcontainers templates apply \
  --template-id github:username/my-templates/my-template
```

## Templates communautaires

Explorer : https://containers.dev/templates

Exemples :
- MERN Stack
- MEAN Stack
- LAMP Stack
- Django + PostgreSQL
- Laravel + MySQL
- Ruby on Rails

## Bonnes pratiques

1. **Partir d'un template officiel** : maintenance assurée
2. **Personnaliser progressivement** : ajouter ce dont vous avez besoin
3. **Versionner la config** : dans le repo du projet
4. **Documenter** : README.md avec instructions
5. **Tester** : avant de partager avec l'équipe

[← Docker Compose](./infos-devcontainer-07-docker-compose.md) | [Index](./infos-devcontainer-00-index.md) | [Debugging →](./infos-devcontainer-09-debugging.md)

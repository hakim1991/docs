# 🚀 Sujets avancés

[← Debugging](./infos-devcontainer-09-debugging.md) | [Index](./infos-devcontainer-00-index.md) | [Best Practices →](./infos-devcontainer-11-best-practices.md)

## Dotfiles

Partager votre configuration personnelle (zsh, vim, git, etc.).

### Repository dotfiles

```bash
# Créer un repo dotfiles sur GitHub
# username/dotfiles
# .zshrc, .vimrc, .gitconfig, etc.
```

### Configuration

```json
{
  "dotfiles.repository": "username/dotfiles",
  "dotfiles.targetPath": "~/dotfiles",
  "dotfiles.installCommand": "install.sh"
}
```

VS Code Settings (local) :

```json
// settings.json
{
  "dotfiles.repository": "https://github.com/username/dotfiles.git",
  "dotfiles.targetPath": "~/dotfiles",
  "dotfiles.installCommand": "~/dotfiles/install.sh"
}
```

### install.sh

```bash
#!/bin/bash

# Symlink configs
ln -sf ~/dotfiles/.zshrc ~/.zshrc
ln -sf ~/dotfiles/.vimrc ~/.vimrc
ln -sf ~/dotfiles/.gitconfig ~/.gitconfig

# Oh My Zsh
if [ ! -d ~/.oh-my-zsh ]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi

echo "Dotfiles installed!"
```

## Multi-stage builds

Optimiser la taille de l'image.

```dockerfile
# Stage 1: Builder
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

USER node
CMD ["node", "dist/index.js"]
```

## BuildKit et caching

Améliorer les performances de build.

```dockerfile
# syntax=docker/dockerfile:1

FROM node:18

# Cache mount pour npm
RUN --mount=type=cache,target=/root/.npm \
    npm install -g npm@latest

WORKDIR /app

# Cache les layers de package.json
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .
```

```bash
# Activer BuildKit
export DOCKER_BUILDKIT=1
docker build .
```

## Secrets

Gérer les secrets en toute sécurité.

### Avec BuildKit

```dockerfile
# syntax=docker/dockerfile:1

FROM node:18

# Secret mount (pas inclus dans l'image)
RUN --mount=type=secret,id=npm_token \
    echo "//registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)" > ~/.npmrc && \
    npm install private-package && \
    rm ~/.npmrc
```

```bash
docker build --secret id=npm_token,src=.npmrc .
```

### Variables d'environnement

```json
{
  "containerEnv": {
    "API_KEY": "${localEnv:API_KEY}"
  }
}
```

```bash
# .env (ne pas commiter)
API_KEY=secret-key
```

## GPU Support

Utiliser le GPU dans le container (NVIDIA).

```json
{
  "runArgs": [
    "--gpus", "all"
  ],
  "features": {
    "ghcr.io/devcontainers/features/nvidia-cuda:1": {
      "installCudnn": true
    }
  }
}
```

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Kubernetes

Développer pour Kubernetes avec Dev Containers.

```json
{
  "name": "Kubernetes Dev",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",

  "features": {
    "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {
      "version": "latest",
      "helm": "latest",
      "minikube": "latest"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },

  "mounts": [
    "source=${localEnv:HOME}/.kube,target=/home/vscode/.kube,type=bind"
  ],

  "postCreateCommand": "kubectl cluster-info"
}
```

## CI/CD avec Dev Containers

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run tests in Dev Container
        uses: devcontainers/ci@v0.3
        with:
          runCmd: npm test
```

### GitLab CI

```yaml
# .gitlab-ci.yml
test:
  image: mcr.microsoft.com/devcontainers/cli:latest
  script:
    - devcontainer build --workspace-folder .
    - devcontainer exec --workspace-folder . npm test
```

## Remote Containers (SSH)

Se connecter à un container distant via SSH.

```json
{
  "remoteUser": "vscode",
  "workspaceFolder": "/workspace",

  "initializeCommand": "ssh user@remote-host 'docker ps'"
}
```

VS Code : `F1` → "Remote-SSH: Connect to Host..."

## Lifecycle hooks

Exécuter des commandes à différents moments.

```json
{
  "initializeCommand": "echo 'Before container creation'",
  "onCreateCommand": "echo 'Container created'",
  "updateContentCommand": "echo 'Content updated'",
  "postCreateCommand": "npm install",
  "postStartCommand": "git config --global user.name 'Dev'",
  "postAttachCommand": "npm run watch"
}
```

Ordre d'exécution :
1. `initializeCommand` (hôte, avant création)
2. `onCreateCommand` (container, première fois)
3. `updateContentCommand` (container, après rebuild)
4. `postCreateCommand` (container, première fois)
5. `postStartCommand` (container, chaque démarrage)
6. `postAttachCommand` (container, chaque connexion)

## Customizations avancées

### Terminal

```json
{
  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.defaultProfile.linux": "zsh",
        "terminal.integrated.profiles.linux": {
          "zsh": {
            "path": "/bin/zsh",
            "args": ["-l"]
          }
        },
        "terminal.integrated.fontSize": 14,
        "terminal.integrated.fontFamily": "MesloLGS NF"
      }
    }
  }
}
```

### Keybindings

```json
{
  "customizations": {
    "vscode": {
      "keybindings": [
        {
          "key": "ctrl+shift+t",
          "command": "workbench.action.terminal.new"
        }
      ]
    }
  }
}
```

### Tasks

```json
{
  "customizations": {
    "vscode": {
      "tasks": {
        "version": "2.0.0",
        "tasks": [
          {
            "label": "Run Tests",
            "type": "shell",
            "command": "npm test",
            "group": {
              "kind": "test",
              "isDefault": true
            }
          }
        ]
      }
    }
  }
}
```

## Privilèges et capabilities

### Capabilities Linux

```json
{
  "capAdd": ["SYS_PTRACE"],
  "securityOpt": ["seccomp=unconfined"]
}
```

### Privileged mode

```json
{
  "runArgs": ["--privileged"]
}
```

⚠️ À utiliser avec précaution (sécurité).

## Pre-build images

Publier une image pré-configurée.

### Dockerfile

```dockerfile
FROM mcr.microsoft.com/devcontainers/javascript-node:18

# Installer les outils
RUN npm install -g typescript nodemon eslint

# Configurer git
RUN git config --global init.defaultBranch main

USER node
```

### Build et push

```bash
docker build -t myregistry/my-devcontainer:latest .
docker push myregistry/my-devcontainer:latest
```

### Utiliser

```json
{
  "image": "myregistry/my-devcontainer:latest"
}
```

## Codespaces

Utiliser Dev Containers avec GitHub Codespaces.

```json
// .devcontainer/devcontainer.json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",

  // Codespaces-specific
  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  }
}
```

Créer un Codespace :
- GitHub repo → Code → Codespaces → New codespace

## Workspace Trust

Configurer la confiance du workspace.

```json
{
  "customizations": {
    "vscode": {
      "settings": {
        "security.workspace.trust.enabled": false
      }
    }
  }
}
```

## Proxy et firewall

Configurer proxy dans le container.

```json
{
  "containerEnv": {
    "HTTP_PROXY": "http://proxy.company.com:8080",
    "HTTPS_PROXY": "http://proxy.company.com:8080",
    "NO_PROXY": "localhost,127.0.0.1"
  }
}
```

```dockerfile
FROM node:18

# Configurer proxy pour apt
RUN echo 'Acquire::http::Proxy "http://proxy.company.com:8080";' > /etc/apt/apt.conf.d/proxy
```

## Performance tuning

### Consistency modes

```json
{
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
  ]
}
```

- `consistent` : sync complet (lent)
- `cached` : optimisé lecture (recommandé)
- `delegated` : optimisé écriture

### Named volumes pour node_modules

```yaml
services:
  app:
    volumes:
      - .:/workspace:cached
      - node-modules:/workspace/node_modules

volumes:
  node-modules:
```

### Exclude patterns

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached",
  "mounts": [
    "source=${localWorkspaceFolder}/node_modules,target=/dev/null,type=bind"
  ]
}
```

## Custom Features

Créer vos propres features réutilisables.

```
my-feature/
├── devcontainer-feature.json
├── install.sh
└── README.md
```

```json
// devcontainer-feature.json
{
  "id": "my-custom-tool",
  "version": "1.0.0",
  "name": "My Custom Tool",
  "description": "Installs my custom tool",
  "options": {
    "version": {
      "type": "string",
      "default": "latest"
    }
  }
}
```

```bash
# install.sh
#!/bin/bash
VERSION="${VERSION:-latest}"
echo "Installing My Tool ${VERSION}..."
# Installation commands
```

## Bonnes pratiques

1. **Utiliser multi-stage builds** : images plus légères
2. **Cacher les dependencies** : build plus rapide
3. **Ne pas inclure secrets dans l'image** : sécurité
4. **Utiliser BuildKit** : meilleures performances
5. **Tester en CI** : assurer reproductibilité
6. **Documenter les hooks** : clarté pour l'équipe

[← Debugging](./infos-devcontainer-09-debugging.md) | [Index](./infos-devcontainer-00-index.md) | [Best Practices →](./infos-devcontainer-11-best-practices.md)

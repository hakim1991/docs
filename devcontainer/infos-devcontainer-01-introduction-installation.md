# 🚀 Introduction et Installation

[Index](./infos-devcontainer-00-index.md) | [Configuration →](./infos-devcontainer-02-configuration-base.md)

## Qu'est-ce qu'un Dev Container ?

Un **Dev Container** est un environnement de développement conteneurisé qui permet de :
- 📦 Isoler l'environnement de développement
- 🔄 Garantir la reproductibilité entre les développeurs
- 🛠️ Pré-configurer les outils, extensions et dépendances
- 🚀 Démarrer rapidement sur un nouveau projet
- 🌍 Développer sur n'importe quelle machine (Windows, Mac, Linux)

## Avantages

- ✅ **Onboarding rapide** : nouveau dev opérationnel en minutes
- ✅ **Environnement identique** : même config pour toute l'équipe
- ✅ **Isolation** : pas de pollution de la machine hôte
- ✅ **Portabilité** : fonctionne partout où Docker est installé
- ✅ **Reproductibilité** : même versions de Node, Python, etc.
- ✅ **Configuration as code** : versionnée avec le projet

## Prérequis

### Windows

```powershell
# Installer WSL 2
wsl --install

# Installer Docker Desktop
# Télécharger depuis https://www.docker.com/products/docker-desktop
```

### macOS

```bash
# Installer Docker Desktop
# Télécharger depuis https://www.docker.com/products/docker-desktop

# Ou avec Homebrew
brew install --cask docker
```

### Linux

```bash
# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter votre user au groupe docker
sudo usermod -aG docker $USER
newgrp docker

# Vérifier l'installation
docker --version
docker run hello-world
```

## Installation VS Code

### Installer VS Code

```bash
# Linux (Debian/Ubuntu)
sudo snap install code --classic

# macOS
brew install --cask visual-studio-code

# Windows
# Télécharger depuis https://code.visualstudio.com/
```

### Extension Dev Containers

```bash
# Installer l'extension via CLI
code --install-extension ms-vscode-remote.remote-containers
```

Ou depuis VS Code :
1. Ouvrir VS Code
2. `Ctrl+Shift+X` (Extensions)
3. Rechercher "Dev Containers"
4. Installer l'extension de Microsoft

## Première utilisation

### Créer un Dev Container

```bash
# Créer un projet
mkdir mon-projet
cd mon-projet

# Créer le dossier .devcontainer
mkdir .devcontainer
```

### Configuration minimale

```json
// .devcontainer/devcontainer.json
{
  "name": "Mon Dev Container",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu"
}
```

### Ouvrir dans le container

1. Ouvrir le dossier dans VS Code
2. `F1` → "Dev Containers: Reopen in Container"
3. VS Code redémarre dans le container

Ou via CLI :
```bash
code --folder-uri vscode-remote://dev-container+${PWD}
```

## Vérification

Une fois dans le container :

```bash
# Vérifier qu'on est dans le container
echo $REMOTE_CONTAINERS

# Vérifier l'OS
cat /etc/os-release

# Terminal intégré = terminal du container
pwd
ls -la
```

## CLI Dev Container

### Installation

```bash
npm install -g @devcontainers/cli
```

### Commandes utiles

```bash
# Build le container
devcontainer build .

# Ouvrir VS Code dans le container
devcontainer open .

# Exécuter une commande dans le container
devcontainer exec --workspace-folder . npm install

# Lire la config
devcontainer read-configuration --workspace-folder .
```

## Structure typique

```
mon-projet/
├── .devcontainer/
│   ├── devcontainer.json    # Configuration principale
│   ├── Dockerfile           # (Optionnel) Image personnalisée
│   └── docker-compose.yml   # (Optionnel) Multi-containers
├── src/
├── package.json
└── README.md
```

## Exemple complet (Node.js)

```json
// .devcontainer/devcontainer.json
{
  "name": "Projet Node.js",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  },

  "forwardPorts": [3000],

  "postCreateCommand": "npm install",

  "remoteUser": "node"
}
```

### Ouvrir le projet

```bash
cd mon-projet
code .
# F1 → "Dev Containers: Reopen in Container"
```

## Images officielles

Microsoft fournit des images pré-configurées :

```bash
# JavaScript/Node.js
mcr.microsoft.com/devcontainers/javascript-node:18

# Python
mcr.microsoft.com/devcontainers/python:3.11

# Java
mcr.microsoft.com/devcontainers/java:17

# .NET
mcr.microsoft.com/devcontainers/dotnet:7.0

# Go
mcr.microsoft.com/devcontainers/go:1.21

# Rust
mcr.microsoft.com/devcontainers/rust:1

# PHP
mcr.microsoft.com/devcontainers/php:8.2

# Ruby
mcr.microsoft.com/devcontainers/ruby:3.2

# Base (Ubuntu)
mcr.microsoft.com/devcontainers/base:ubuntu
```

## Templates

Démarrer avec un template :

```bash
# Via VS Code
# F1 → "Dev Containers: Add Dev Container Configuration Files..."
# Choisir un template (Node.js, Python, etc.)

# Via CLI
devcontainer templates apply -t node
```

## Commandes VS Code

| Commande | Description |
|----------|-------------|
| `F1` → Reopen in Container | Ouvrir dans le container |
| `F1` → Rebuild Container | Rebuild l'image |
| `F1` → Reopen Folder Locally | Revenir en local |
| `F1` → Show Container Log | Voir les logs |
| `F1` → Open Container Configuration | Ouvrir devcontainer.json |

## Indicateur de connexion

Quand connecté au container, en bas à gauche de VS Code :
```
🔷 Dev Container: Mon Dev Container
```

Cliquer dessus pour :
- Voir les containers en cours
- Se déconnecter
- Rebuild
- etc.

## Troubleshooting

### Docker ne démarre pas

```bash
# Vérifier le statut
docker ps

# Restart Docker Desktop (Windows/Mac)
# Ou restart le service (Linux)
sudo systemctl restart docker
```

### Extension non trouvée

```bash
# Vérifier l'installation
code --list-extensions | grep remote-containers

# Réinstaller
code --install-extension ms-vscode-remote.remote-containers
```

### Permission denied

```bash
# Linux : ajouter au groupe docker
sudo usermod -aG docker $USER
newgrp docker
```

### WSL 2 (Windows)

```powershell
# Vérifier WSL 2
wsl --list --verbose

# Mettre à jour WSL
wsl --update

# Configurer Docker pour WSL 2
# Docker Desktop → Settings → Resources → WSL Integration
```

## Next Steps

Maintenant que vous avez installé et testé votre premier Dev Container :
1. Personnaliser la configuration
2. Ajouter des features
3. Configurer les extensions
4. Gérer les ports et volumes

[Index](./infos-devcontainer-00-index.md) | [Configuration →](./infos-devcontainer-02-configuration-base.md)

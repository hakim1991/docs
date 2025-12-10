# 🔀 Différences Linux / Windows

[← Backup](./infos-docker-11-backup.md) | [Index](./infos-docker-00-index.md) | [Cas pratiques →](./infos-docker-13-cas-pratiques.md)

---

## Table des matières
- [Architecture Docker](#architecture-docker)
- [Docker sur Linux](#docker-sur-linux)
- [Docker sur Windows](#docker-sur-windows)
- [Conteneurs Linux vs Windows](#conteneurs-linux-vs-windows)
- [Chemins et volumes](#chemins-et-volumes)
- [Performance](#performance)
- [Compatibilité](#compatibilite)

---

## Architecture Docker

### Docker sur Linux (natif)

```
┌──────────────────────────────────┐
│      Application Docker          │
├──────────────────────────────────┤
│      Docker CLI                  │
├──────────────────────────────────┤
│      Docker Engine               │
├──────────────────────────────────┤
│      Linux Kernel                │  ← Natif
│  (cgroups, namespaces, etc.)     │
├──────────────────────────────────┤
│      Hardware                    │
└──────────────────────────────────┘

✅ Performance native
✅ Pas de virtualisation
✅ Accès direct au kernel
```

### Docker sur Windows avec WSL2

```
┌──────────────────────────────────┐
│      Application Docker          │
├──────────────────────────────────┤
│      Docker Desktop              │
├──────────────────────────────────┤
│      WSL2 (Linux VM légère)      │  ← Virtualisation
│      Docker Engine (Linux)       │
├──────────────────────────────────┤
│      Hyper-V / Windows Kernel    │
├──────────────────────────────────┤
│      Hardware                    │
└──────────────────────────────────┘

✅ Conteneurs Linux sur Windows
⚠️ Overhead de virtualisation
✅ Bonne performance avec WSL2
```

### Docker sur Windows (mode Windows natif)

```
┌──────────────────────────────────┐
│   Application Docker (Windows)   │
├──────────────────────────────────┤
│      Docker Desktop              │
├──────────────────────────────────┤
│      Windows Containers          │
├──────────────────────────────────┤
│      Windows Kernel              │  ← Natif pour conteneurs Windows
├──────────────────────────────────┤
│      Hardware                    │
└──────────────────────────────────┘

✅ Conteneurs Windows natifs
❌ Plus volumineux que Linux
⚠️ Moins d'images disponibles
```

---

## Docker sur Linux

### Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# CentOS/RHEL
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

### Avantages Linux

```
✅ Performance native (pas de VM)
✅ Écosystème riche (toutes les images)
✅ Outils système complets
✅ Idéal pour production
✅ Ressources minimales
✅ Intégration parfaite avec kernel Linux
```

### Particularités Linux

```bash
# Gestion via systemd
sudo systemctl start docker
sudo systemctl stop docker
sudo systemctl status docker

# Logs système
sudo journalctl -u docker -f

# Configuration
/etc/docker/daemon.json

# Socket Unix
/var/run/docker.sock

# Données Docker
/var/lib/docker/
```

---

## Docker sur Windows

### Installation

```powershell
# Prérequis Windows
# - Windows 10/11 Pro, Enterprise, ou Education
# - Virtualisation activée dans BIOS
# - Hyper-V ou WSL2

# Télécharger Docker Desktop
# https://www.docker.com/products/docker-desktop/

# Installer via winget
winget install Docker.DockerDesktop

# Ou via chocolatey
choco install docker-desktop
```

### Configuration WSL2

```powershell
# Activer WSL2
wsl --install

# Définir WSL2 comme version par défaut
wsl --set-default-version 2

# Lister les distributions
wsl --list --verbose

# Mettre à jour une distribution vers WSL2
wsl --set-version Ubuntu 2

# Dans Docker Desktop Settings:
# ✅ Use WSL 2 based engine
# ✅ WSL Integration → Enable integration with distros
```

### Docker Desktop Settings

```
Paramètres importants:

Resources:
  - CPU: Allouer 4+ cores
  - Memory: 8+ GB recommandé
  - Disk: Limiter la taille (100+ GB)
  - File Sharing: Sélectionner les drives

WSL Integration:
  - Enable integration with my default WSL distro
  - Enable for: Ubuntu, Debian, etc.

Docker Engine:
  - Configuration daemon.json

Kubernetes (optionnel):
  - Enable Kubernetes
```

### Particularités Windows

```powershell
# Docker Desktop gère le daemon
# Start/Stop via l'interface ou:
# Taskbar → Docker Desktop → Settings

# Logs Docker Desktop
# C:\Users\<user>\AppData\Local\Docker\log.txt

# Données Docker (WSL2)
\\wsl$\docker-desktop-data\data\docker

# Named pipes (au lieu de socket Unix)
\\.\pipe\docker_engine

# PowerShell vs CMD vs WSL
# Préférer PowerShell ou WSL pour Docker CLI
```

---

## Conteneurs Linux vs Windows

### Conteneurs Linux sur Windows (WSL2)

```bash
# Mode par défaut avec Docker Desktop + WSL2
docker run -d ubuntu echo "Hello Linux"

# Utilise le kernel Linux de WSL2
# Performance proche du natif
# Accès à toutes les images Linux
```

### Conteneurs Windows natifs

```powershell
# Basculer vers Windows containers
# Docker Desktop → Switch to Windows containers

# Exécuter un conteneur Windows
docker run -d mcr.microsoft.com/windows/servercore:ltsc2022

# Images Windows
mcr.microsoft.com/windows/servercore  # Windows Server Core
mcr.microsoft.com/windows/nanoserver  # Nano Server
mcr.microsoft.com/dotnet/framework    # .NET Framework
```

### Comparaison

| Aspect | Linux | Windows |
|--------|-------|---------|
| **Taille images** | 5-500 MB | 1-10 GB |
| **Démarrage** | < 1 seconde | 5-30 secondes |
| **Écosystème** | Très riche | Limité |
| **Use case** | Général | Apps .NET Framework |
| **Multi-plateforme** | Oui (arm64, amd64) | Windows seulement |

---

## Chemins et volumes

### Chemins Linux

```bash
# Paths Unix (forward slash)
docker run -v /home/user/data:/app/data ubuntu

# Volumes nommés
docker run -v myvolume:/data ubuntu

# Bind mount avec $PWD
docker run -v $(pwd):/app ubuntu

# Chemin absolu requis
docker run -v /absolute/path:/container/path ubuntu
```

### Chemins Windows (PowerShell)

```powershell
# Windows paths (backslash ou forward slash)
docker run -v C:\Users\user\data:/app/data ubuntu

# Avec forward slash (recommandé)
docker run -v C:/Users/user/data:/app/data ubuntu

# Variable d'environnement
docker run -v ${PWD}:/app ubuntu

# WSL paths depuis Windows
docker run -v \\wsl$\Ubuntu\home\user\data:/app/data ubuntu
```

### Chemins Windows (CMD)

```cmd
REM Variable %cd% pour current directory
docker run -v %cd%:/app ubuntu

REM Échapper les backslashes
docker run -v C:\\Users\\user\\data:/app/data ubuntu
```

### Permissions et ownership

```bash
# Linux: UID/GID
docker run -u 1000:1000 -v /data:/data ubuntu

# Windows: Pas de UID/GID
# Les fichiers dans bind mounts gardent les permissions Windows
# Dans WSL2, les permissions sont émulées

# Problème commun sur Windows:
# Fichiers créés dans conteneur → root ownership
# Solution: Spécifier l'utilisateur
docker run -u $(id -u):$(id -g) -v $(pwd):/app ubuntu
```

---

## Performance

### Linux (natif)

```
✅ Performance maximale
✅ Pas d'overhead VM
✅ I/O disque natif
✅ Réseau natif
✅ Idéal pour production

Benchmarks:
- Démarrage conteneur: < 100ms
- I/O disque: ~100% natif
- Network throughput: ~100% natif
```

### Windows (WSL2)

```
✅ Bonne performance générale
⚠️ Overhead léger (VM)
⚠️ I/O bind mounts plus lent
✅ Réseau proche du natif (avec bonne config)

Benchmarks:
- Démarrage conteneur: < 200ms
- I/O volumes: ~90% natif
- I/O bind mounts: ~50-70% natif (selon config)
- Network: ~85-95% natif
```

### Optimisations Windows

```yaml
# docker-compose.yml optimisé pour Windows

services:
  app:
    image: myapp
    volumes:
      # ❌ LENT: Bind mount direct
      # - ./src:/app/src

      # ✅ RAPIDE: Volume nommé + copie initiale
      - app-src:/app/src

    # ✅ Utiliser un volume pour node_modules (très important!)
    volumes:
      - ./src:/app/src:cached  # Mode cached pour macOS/Windows
      - node-modules:/app/node_modules

volumes:
  app-src:
  node-modules:
```

```bash
# Performance tips Windows:

# 1. Utiliser volumes nommés au lieu de bind mounts
docker volume create mydata
docker run -v mydata:/data ubuntu

# 2. Stocker le code dans WSL2 (pas dans /mnt/c)
# ✅ /home/user/project
# ❌ /mnt/c/Users/user/project

# 3. Désactiver antivirus sur dossiers Docker
# Exclure: \\wsl$\docker-desktop-data

# 4. Allouer plus de ressources à Docker Desktop
# Settings → Resources → Memory: 8GB+, CPU: 4+

# 5. Utiliser mode cached pour bind mounts (Docker Compose)
volumes:
  - ./src:/app/src:cached
```

---

## Compatibilité

### Multi-plateforme

```bash
# Construire pour plusieurs plateformes
docker buildx create --name multiplatform --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .

# Spécifier la plateforme au pull/run
docker pull --platform linux/amd64 ubuntu
docker run --platform linux/arm64 ubuntu
```

### Images multi-architecture

```dockerfile
# Dockerfile supportant plusieurs architectures
FROM --platform=$BUILDPLATFORM golang:1.21 AS builder
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "Building on $BUILDPLATFORM for $TARGETPLATFORM"
# Build...

FROM alpine
COPY --from=builder /app /app
CMD ["/app"]
```

### Limitations par plateforme

```
Linux containers sur Windows:
✅ Toutes les images Linux
✅ Multi-architecture (amd64, arm64)
❌ Pas d'accès direct au hardware spécifique

Windows containers:
✅ Applications .NET Framework
❌ Pas d'images Linux
❌ Uniquement Windows Server
⚠️ Images très volumineuses
```

---

## Scripts compatibles

### Script bash portable

```bash
#!/bin/bash
# portable-script.sh

# Détection OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "OS détecté: $OS"

# Chemins adaptés
if [ "$OS" = "windows" ]; then
    PROJECT_DIR="C:/Users/$USER/project"
else
    PROJECT_DIR="/home/$USER/project"
fi

# Docker compose avec chemins relatifs (portable)
docker compose -f docker-compose.yml up -d
```

### docker-compose.yml portable

```yaml
# docker-compose.yml compatible Linux/Windows

version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "80:80"
    volumes:
      # ✅ Chemins relatifs (portables)
      - ./html:/usr/share/nginx/html:ro

      # ✅ Volumes nommés (portables)
      - nginx-logs:/var/log/nginx

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
    volumes:
      # ✅ Volume nommé pour données
      - postgres-data:/var/lib/postgresql/data

      # ✅ Bind mount relatif pour init scripts
      - ./init-db:/docker-entrypoint-initdb.d:ro

volumes:
  nginx-logs:
  postgres-data:

# Pas de chemins absolus!
# Pas de /home/user ou C:\Users\user
```

---

## Développement cross-platform

### VSCode + Remote Containers

```json
// .devcontainer/devcontainer.json
{
  "name": "Development Container",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  // Extensions VSCode
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker",
        "ms-vscode-remote.remote-containers"
      ]
    }
  },

  // Compatible Linux/Windows/Mac
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
  ]
}
```

### Makefile portable

```makefile
# Makefile compatible Linux/Windows (via WSL/Git Bash)

.PHONY: build up down logs

# Variables
COMPOSE := docker compose
PROJECT_NAME := myapp

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

clean:
	$(COMPOSE) down -v
	docker system prune -f
```

---

## Best practices cross-platform

```yaml
# ✅ Chemins relatifs
volumes:
  - ./config:/app/config

# ❌ Chemins absolus
volumes:
  - /home/user/config:/app/config
  - C:/Users/user/config:/app/config

# ✅ Variables d'environnement
environment:
  - DATA_PATH=${DATA_PATH:-/app/data}

# ✅ Volumes nommés pour données importantes
volumes:
  app-data:
  db-data:

# ✅ .dockerignore
node_modules
.git
.env
*.log

# ✅ Line endings (Git)
# .gitattributes
* text=auto
*.sh text eol=lf

# ✅ Tester sur les 2 plateformes
# CI/CD avec matrix: [ubuntu-latest, windows-latest]
```

---

## Troubleshooting

### Problèmes Windows courants

```powershell
# Docker Desktop ne démarre pas
# → Vérifier Hyper-V activé
# → Vérifier WSL2 installé
# → Redémarrer le service

# Performances lentes
# → Déplacer code dans WSL2 (/home/user)
# → Augmenter RAM allouée (Settings → Resources)
# → Utiliser volumes nommés

# Erreur "drive not shared"
# → Docker Desktop → Settings → Resources → File Sharing

# WSL2 non détecté
wsl --update
wsl --set-default-version 2

# Reset Docker Desktop
# Settings → Troubleshoot → Reset to factory defaults
```

### Problèmes Linux courants

```bash
# Permission denied sur docker.sock
sudo usermod -aG docker $USER
# Puis se déconnecter/reconnecter

# Docker service ne démarre pas
sudo systemctl status docker
sudo journalctl -u docker -f

# Espace disque plein
docker system prune -a -f
```

---

## Commandes de référence rapide

```bash
# Info système
docker info                              # Info Docker
docker version                           # Versions

# Windows: basculer mode conteneurs
# Docker Desktop → Switch to Windows containers

# Build multi-plateforme
docker buildx build --platform linux/amd64,linux/arm64 -t image .

# Volumes (portable)
docker run -v $(pwd):/app image          # Linux/Mac/Windows (Git Bash/WSL)
docker run -v ${PWD}:/app image          # PowerShell
docker run -v %cd%:/app image            # CMD
```

---

[← Backup](./infos-docker-11-backup.md) | [Index](./infos-docker-00-index.md) | [Cas pratiques →](./infos-docker-13-cas-pratiques.md)

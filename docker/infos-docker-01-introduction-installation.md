# 📥 Introduction et Installation Docker

[← Retour à l'index](./infos-docker-00-index.md) | [Images Docker →](./infos-docker-02-images.md)

---

## Table des matières
- [Qu'est-ce que Docker ?](#quest-ce-que-docker)
- [Installation sur Linux](#installation-sur-linux)
- [Installation sur Windows](#installation-sur-windows)
- [Vérification de l'installation](#verification-de-linstallation)
- [Premiers pas](#premiers-pas)

---

## Qu'est-ce que Docker ?

### Définition
Docker est une plateforme de **containerisation** qui permet d'empaqueter des applications et leurs dépendances dans des **conteneurs** légers et portables.

### Conteneurs vs Machines Virtuelles

| Aspect | Conteneurs Docker | Machines Virtuelles |
|--------|------------------|---------------------|
| **Démarrage** | Quelques secondes | Quelques minutes |
| **Taille** | Mo (légères) | Go (lourdes) |
| **Performance** | Quasi-native | Overhead VM |
| **Isolation** | Partage le noyau de l'OS | OS complet par VM |
| **Portabilité** | Très portable | Moins portable |

### Pourquoi utiliser Docker ?

✅ **Avantages principaux:**
- **Portabilité**: "Fonctionne sur ma machine" = fonctionne partout
- **Isolation**: Chaque conteneur est isolé des autres
- **Léger**: Pas besoin d'un OS complet par conteneur
- **Rapidité**: Démarrage quasi-instantané
- **Reproductibilité**: Même environnement en dev, test, prod
- **Scalabilité**: Facile de multiplier les conteneurs

### Concepts de base

```
┌─────────────────────────────────────┐
│          Application                │
│                                     │
│  ┌─────────┐  ┌─────────┐         │
│  │Container│  │Container│   ...    │
│  │   #1    │  │   #2    │         │
│  └─────────┘  └─────────┘         │
│       ↑            ↑                │
│  ┌─────────────────────────────┐  │
│  │     Docker Engine           │  │
│  └─────────────────────────────┘  │
│  ┌─────────────────────────────┐  │
│  │     Système d'exploitation   │  │
│  │  (Linux, Windows, macOS)    │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Termes importants:**
- **Image**: Template immuable (comme une photo)
- **Conteneur**: Instance d'exécution d'une image (comme un processus)
- **Dockerfile**: Fichier de recette pour créer une image
- **Docker Compose**: Outil pour gérer plusieurs conteneurs
- **Registry**: Dépôt d'images (comme Docker Hub)

---

## Installation sur Linux

### Ubuntu / Debian

```bash
# 1. Mettre à jour les paquets
sudo apt update

# 2. Installer les dépendances
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    gnupg \
    lsb-release

# 3. Ajouter la clé GPG officielle de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Ajouter le repository Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Installer Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. Vérifier l'installation
sudo docker --version
sudo docker compose version

# 7. Ajouter votre utilisateur au groupe docker (évite d'utiliser sudo)
sudo usermod -aG docker $USER

# 8. Redémarrer la session pour appliquer les changements
# Option 1: Se déconnecter/reconnecter
# Option 2: Exécuter cette commande
newgrp docker

# 9. Activer le démarrage automatique de Docker
sudo systemctl enable docker
sudo systemctl start docker
```

### CentOS / RHEL / Fedora

```bash
# 1. Supprimer les anciennes versions (si présentes)
sudo dnf remove docker \
                docker-client \
                docker-client-latest \
                docker-common \
                docker-latest \
                docker-latest-logrotate \
                docker-logrotate \
                docker-engine

# 2. Installer les dépendances
sudo dnf -y install dnf-plugins-core

# 3. Ajouter le repository Docker
sudo dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 4. Installer Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 5. Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# 6. Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# 7. Redémarrer la session
newgrp docker
```

### Arch Linux

```bash
# Installer Docker
sudo pacman -S docker docker-compose

# Démarrer et activer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

### Post-installation Linux

```bash
# Vérifier que Docker fonctionne sans sudo
docker run hello-world

# Si erreur de permissions:
# 1. Vérifier que l'utilisateur est dans le groupe docker
groups

# 2. Si 'docker' n'apparaît pas, l'ajouter
sudo usermod -aG docker $USER

# 3. Se déconnecter et reconnecter, ou exécuter
newgrp docker

# Configurer Docker pour démarrer au boot
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

---

## Installation sur Windows

### Prérequis Windows

**Configuration minimale:**
- Windows 10 64-bit: Pro, Enterprise, ou Education (Build 19041 ou supérieur)
- Windows 11 64-bit
- Virtualisation activée dans le BIOS
- 4 Go de RAM minimum (8 Go recommandé)

### Méthode 1: Docker Desktop avec WSL2 (Recommandé)

#### Étape 1: Installer WSL2

```powershell
# Ouvrir PowerShell en tant qu'administrateur

# Activer WSL
wsl --install

# Si WSL est déjà installé, mettre à jour vers WSL2
wsl --set-default-version 2

# Vérifier la version
wsl --list --verbose

# Si une distribution utilise WSL1, la convertir en WSL2
wsl --set-version Ubuntu 2
```

**Redémarrer l'ordinateur après l'installation de WSL2**

#### Étape 2: Télécharger Docker Desktop

1. Aller sur https://www.docker.com/products/docker-desktop/
2. Télécharger **Docker Desktop for Windows**
3. Exécuter l'installateur `Docker Desktop Installer.exe`

#### Étape 3: Installer Docker Desktop

1. Pendant l'installation, **cocher** l'option:
   - ✅ "Use WSL 2 instead of Hyper-V"
2. Suivre les étapes de l'assistant
3. Redémarrer l'ordinateur si demandé

#### Étape 4: Configurer Docker Desktop

1. Lancer **Docker Desktop**
2. Accepter les conditions d'utilisation
3. Aller dans **Settings** (icône engrenage)
4. Section **General**:
   - ✅ "Use the WSL 2 based engine"
5. Section **Resources** > **WSL Integration**:
   - ✅ "Enable integration with my default WSL distro"
   - ✅ Activer pour Ubuntu ou votre distribution WSL

#### Étape 5: Vérifier dans WSL2

```bash
# Ouvrir un terminal WSL (Ubuntu)
wsl

# Vérifier Docker
docker --version
docker compose version

# Tester Docker
docker run hello-world
```

### Méthode 2: Docker Desktop avec Hyper-V

> ⚠️ **Note**: WSL2 est recommandé pour de meilleures performances

```powershell
# Activer Hyper-V (PowerShell Admin)
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# Redémarrer l'ordinateur
Restart-Computer
```

Ensuite, installer Docker Desktop en cochant "Use Hyper-V"

### Configuration Docker Desktop

#### Settings importants

```
Settings > General:
✅ Start Docker Desktop when you log in
✅ Use the WSL 2 based engine
□ Send usage statistics (optionnel)

Settings > Resources > Advanced:
- CPUs: 4 (ou plus)
- Memory: 4 GB (ou plus)
- Swap: 1 GB
- Disk image size: 60 GB (augmenter si besoin)

Settings > Docker Engine:
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  }
}
```

### Post-installation Windows

```powershell
# Dans PowerShell
docker --version
docker compose version

# Dans WSL2 (Ubuntu)
docker --version
docker compose version

# Tester
docker run hello-world
```

---

## Vérification de l'installation

### Tests de base

```bash
# 1. Vérifier les versions
docker --version
# Résultat attendu: Docker version 24.x.x, build ...

docker compose version
# Résultat attendu: Docker Compose version v2.x.x

# 2. Informations système
docker info
# Affiche: version, nombre de conteneurs, images, etc.

# 3. Test avec Hello World
docker run hello-world
# Si tout fonctionne, vous verrez un message de confirmation
```

### Sortie attendue de `docker info`

```
Client:
 Version:           24.0.7
 Context:           default
 Debug Mode:        false

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 24.0.7
 Storage Driver: overlay2
 Logging Driver: json-file
 Cgroup Driver: systemd
 Plugins:
  Volume: local
  Network: bridge host overlay
 Swarm: inactive
 Runtimes: runc io.containerd.runc.v2
 Default Runtime: runc
 Kernel Version: 5.15.0-91-generic
 Operating System: Ubuntu 22.04.3 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 8
 Total Memory: 15.6GiB
```

### Test avec Nginx

```bash
# Lancer un serveur web Nginx
docker run -d -p 8080:80 --name test-nginx nginx

# Vérifier que le conteneur tourne
docker ps

# Tester dans le navigateur
# Ouvrir: http://localhost:8080
# Vous devriez voir la page "Welcome to nginx!"

# Arrêter et supprimer le conteneur
docker stop test-nginx
docker rm test-nginx
```

### Résolution de problèmes courants

#### Linux: Permission denied

```bash
# Erreur: permission denied while trying to connect to the Docker daemon socket
# Solution: Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
newgrp docker

# Vérifier
groups
# "docker" doit apparaître dans la liste
```

#### Windows: WSL2 not installed

```powershell
# Installer WSL2
wsl --install
# Redémarrer l'ordinateur
```

#### Windows: Docker Desktop won't start

1. Vérifier que WSL2 est installé: `wsl --list --verbose`
2. Vérifier que la virtualisation est activée dans le BIOS
3. Redémarrer Docker Desktop
4. Vérifier les logs: `%LOCALAPPDATA%\Docker\log.txt`

#### Linux: Docker daemon not running

```bash
# Démarrer le service Docker
sudo systemctl start docker

# Vérifier le statut
sudo systemctl status docker

# Activer au démarrage
sudo systemctl enable docker
```

---

## Premiers pas

### Commandes essentielles

```bash
# Télécharger une image
docker pull nginx

# Lister les images locales
docker images

# Lancer un conteneur
docker run -d --name mon-nginx -p 8080:80 nginx

# Lister les conteneurs actifs
docker ps

# Lister tous les conteneurs (même arrêtés)
docker ps -a

# Voir les logs d'un conteneur
docker logs mon-nginx

# Arrêter un conteneur
docker stop mon-nginx

# Démarrer un conteneur arrêté
docker start mon-nginx

# Supprimer un conteneur
docker rm mon-nginx

# Supprimer une image
docker rmi nginx
```

### Votre premier conteneur interactif

```bash
# Lancer Ubuntu en mode interactif
docker run -it ubuntu bash

# Vous êtes maintenant dans un conteneur Ubuntu !
# Essayer quelques commandes:
cat /etc/os-release
ls /
apt update && apt install -y curl
curl https://google.com
exit

# Le conteneur s'arrête quand vous tapez "exit"
```

### Exemple pratique: Serveur web

```bash
# Créer un dossier pour votre site
mkdir ~/mon-site
cd ~/mon-site

# Créer un fichier HTML
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Mon Premier Conteneur Docker</title>
</head>
<body>
    <h1>🐳 Bienvenue sur Docker !</h1>
    <p>Ce site tourne dans un conteneur Nginx.</p>
</body>
</html>
EOF

# Lancer Nginx avec votre site
docker run -d \
  --name mon-site-web \
  -p 8080:80 \
  -v $(pwd):/usr/share/nginx/html:ro \
  nginx

# Ouvrir http://localhost:8080 dans votre navigateur

# Modifier index.html et rafraîchir la page
# Les changements sont visibles immédiatement !

# Nettoyer
docker stop mon-site-web
docker rm mon-site-web
```

---

## Configuration avancée

### Configurer le daemon Docker

#### Linux: /etc/docker/daemon.json

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-address-pools": [
    {
      "base": "172.17.0.0/16",
      "size": 24
    }
  ],
  "storage-driver": "overlay2"
}
```

```bash
# Recharger la configuration
sudo systemctl restart docker
```

#### Windows: Docker Desktop Settings > Docker Engine

### Activer BuildKit (build amélioré)

```bash
# Linux/Mac: Dans ~/.bashrc ou ~/.zshrc
export DOCKER_BUILDKIT=1

# Windows PowerShell: Dans le profil
$env:DOCKER_BUILDKIT=1

# Ou dans /etc/docker/daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

### Configurer les proxies

```bash
# Si vous êtes derrière un proxy d'entreprise

# Linux: /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:8080"
Environment="HTTPS_PROXY=http://proxy.example.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1"

# Recharger
sudo systemctl daemon-reload
sudo systemctl restart docker
```

---

## Différences principales Linux vs Windows

| Aspect | Linux | Windows (WSL2) |
|--------|-------|----------------|
| **Installation** | Package manager | Docker Desktop |
| **Interface** | CLI uniquement | CLI + GUI |
| **Performance** | Native | Excellent avec WSL2 |
| **Volumes** | Chemins Unix | Chemins Windows ou WSL |
| **Démarrage** | Service systemd | Application Desktop |
| **Mise à jour** | Package manager | Auto-update |

### Chemins de fichiers

```bash
# Linux
/home/user/projet

# Windows (dans WSL2)
/home/user/projet
# ou accès Windows depuis WSL:
/mnt/c/Users/user/projet

# Windows (PowerShell)
C:\Users\user\projet
```

---

## Prochaines étapes

Maintenant que Docker est installé, vous pouvez passer à:

1. [**Images Docker**](./infos-docker-02-images.md) - Comprendre et gérer les images
2. [**Conteneurs Docker**](./infos-docker-03-conteneurs.md) - Maîtriser les conteneurs
3. [**Docker Compose**](./infos-docker-06-compose.md) - Gérer plusieurs conteneurs

---

[← Retour à l'index](./infos-docker-00-index.md) | [Images Docker →](./infos-docker-02-images.md)

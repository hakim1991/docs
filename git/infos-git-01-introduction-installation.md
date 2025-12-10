# 📥 Introduction et Installation Git

[← Retour à l'index](./infos-git-00-index.md) | [Configuration →](./infos-git-02-configuration.md)

---

## Table des matières
- [Qu'est-ce que Git ?](#quest-ce-que-git)
- [Installation sur Linux](#installation-sur-linux)
- [Installation sur Windows](#installation-sur-windows)
- [Installation sur macOS](#installation-sur-macos)
- [Vérification de l'installation](#verification-de-linstallation)
- [Interfaces graphiques](#interfaces-graphiques)

---

## Qu'est-ce que Git ?

### Définition
**Git** est un système de **contrôle de version distribué** créé par Linus Torvalds en 2005. Il permet de :
- Suivre l'historique des modifications de fichiers
- Collaborer avec d'autres développeurs
- Revenir à des versions antérieures
- Travailler sur plusieurs versions en parallèle (branches)
- Fusionner des modifications de différentes sources

### Pourquoi utiliser Git ?

✅ **Avantages principaux:**
- **Historique complet**: Chaque modification est sauvegardée avec son contexte
- **Collaboration**: Plusieurs personnes peuvent travailler simultanément
- **Branches**: Travaillez sur plusieurs fonctionnalités en parallèle
- **Distribué**: Chaque développeur a une copie complète du repository
- **Rapidité**: Opérations locales très rapides
- **Gratuit et open source**: Utilisé par des millions de développeurs

### Git vs autres systèmes

| Aspect | Git | SVN | Mercurial |
|--------|-----|-----|-----------|
| **Type** | Distribué | Centralisé | Distribué |
| **Performance** | Très rapide | Plus lent | Rapide |
| **Hors ligne** | ✅ Oui | ❌ Non | ✅ Oui |
| **Branches** | Très facile | Possible | Facile |
| **Popularité** | Très élevée | Déclinante | Faible |

### Concepts clés

```
┌─────────────────────────────────────────┐
│     Développeur A                       │
│  ┌─────────────────────────┐            │
│  │  Repository local       │            │
│  │  (copie complète)       │            │
│  └─────────────────────────┘            │
└─────────────┬───────────────────────────┘
              │ push/pull
              ▼
┌─────────────────────────────────────────┐
│     Repository distant (GitHub)         │
│  ┌─────────────────────────┐            │
│  │  Repository central     │            │
│  └─────────────────────────┘            │
└─────────────┬───────────────────────────┘
              │ push/pull
              ▼
┌─────────────────────────────────────────┐
│     Développeur B                       │
│  ┌─────────────────────────┐            │
│  │  Repository local       │            │
│  │  (copie complète)       │            │
│  └─────────────────────────┘            │
└─────────────────────────────────────────┘
```

---

## Installation sur Linux

### Ubuntu / Debian

```bash
# Méthode 1: Via apt (simple)
sudo apt update
sudo apt install git

# Vérifier la version
git --version
# Résultat: git version 2.x.x

# Méthode 2: Dernière version via PPA
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git
```

### CentOS / RHEL / Fedora

```bash
# CentOS/RHEL avec yum
sudo yum install git

# Fedora avec dnf
sudo dnf install git

# Vérifier l'installation
git --version
```

### Arch Linux

```bash
# Installer Git
sudo pacman -S git

# Vérifier
git --version
```

### Compiler depuis les sources (toutes distros)

```bash
# Installer les dépendances
# Ubuntu/Debian
sudo apt install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip

# CentOS/RHEL
sudo yum install curl-devel expat-devel gettext-devel openssl-devel perl-devel zlib-devel gcc

# Télécharger la dernière version
cd /tmp
wget https://github.com/git/git/archive/v2.43.0.tar.gz
tar -zxf v2.43.0.tar.gz
cd git-2.43.0

# Compiler et installer
make prefix=/usr/local all
sudo make prefix=/usr/local install

# Vérifier
git --version
```

---

## Installation sur Windows

### Méthode 1: Git for Windows (Recommandé)

1. **Télécharger Git for Windows**
   - Site: https://git-scm.com/download/win
   - Télécharger l'installateur (64-bit ou 32-bit)

2. **Installation**
   - Exécuter l'installateur
   - **Options importantes pendant l'installation:**

```
┌─────────────────────────────────────┐
│ Composants à installer:             │
│ ✅ Git Bash                         │
│ ✅ Git GUI                          │
│ ✅ Git LFS (Large File Support)     │
│ ✅ Associate .git* files with...    │
│ ✅ Windows Explorer integration     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Éditeur par défaut:                 │
│ • Vim (par défaut, pour experts)    │
│ ✅ Visual Studio Code (recommandé)  │
│ • Notepad++                         │
│ • Sublime Text                      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Nom de la branche par défaut:      │
│ ✅ main (recommandé)                │
│ • master (ancien standard)          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Ajustement du PATH:                 │
│ ✅ Git from the command line and... │
│   (Recommandé - Git dans cmd/PS)   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ SSH executable:                     │
│ ✅ Use bundled OpenSSH             │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ HTTPS transport:                    │
│ ✅ Use the OpenSSL library         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Line ending conversions:            │
│ ✅ Checkout Windows-style,         │
│    commit Unix-style (recommandé)  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Terminal emulator:                  │
│ ✅ Use MinTTY (Git Bash terminal)  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ git pull behavior:                  │
│ ✅ Default (fast-forward or merge) │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Credential helper:                  │
│ ✅ Git Credential Manager          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Extra options:                      │
│ ✅ Enable file system caching      │
│ ✅ Enable symbolic links            │
└─────────────────────────────────────┘
```

3. **Vérification**

```bash
# Ouvrir Git Bash ou PowerShell
git --version
# Résultat: git version 2.x.x.windows.x
```

### Méthode 2: Via Windows Package Manager (winget)

```powershell
# Dans PowerShell
winget install --id Git.Git -e --source winget
```

### Méthode 3: Via Chocolatey

```powershell
# Installer Chocolatey si non installé
# Puis:
choco install git
```

### Méthode 4: Via Scoop

```powershell
# Installer Scoop si non installé
# Puis:
scoop install git
```

### Configuration Git Bash

```bash
# Ouvrir Git Bash

# Créer un alias pour ouvrir depuis n'importe où
# Ajouter au fichier ~/.bashrc (créer s'il n'existe pas)
echo 'alias ll="ls -la"' >> ~/.bashrc
echo 'alias gs="git status"' >> ~/.bashrc
echo 'alias ga="git add"' >> ~/.bashrc
echo 'alias gc="git commit"' >> ~/.bashrc
echo 'alias gp="git push"' >> ~/.bashrc

# Recharger la configuration
source ~/.bashrc
```

---

## Installation sur macOS

### Méthode 1: Via Xcode Command Line Tools

```bash
# Installer les Command Line Tools (inclut Git)
xcode-select --install

# Vérifier
git --version
```

### Méthode 2: Via Homebrew (Recommandé)

```bash
# Installer Homebrew si pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Git
brew install git

# Mettre à jour Git
brew upgrade git

# Vérifier
git --version
```

### Méthode 3: Via MacPorts

```bash
# Installer MacPorts si pas déjà fait
# Puis:
sudo port install git
```

### Méthode 4: Installateur officiel

1. Télécharger depuis: https://git-scm.com/download/mac
2. Exécuter le fichier .dmg
3. Suivre l'assistant d'installation

---

## Vérification de l'installation

### Tests de base

```bash
# 1. Vérifier la version
git --version
# Résultat attendu: git version 2.x.x

# 2. Voir toutes les commandes disponibles
git --help
# Affiche la liste des commandes Git

# 3. Aide sur une commande spécifique
git help commit
# ou
git commit --help
# Ouvre la documentation de la commande

# 4. Vérifier la configuration
git config --list
# Affiche toutes les configurations (peut être vide pour l'instant)

# 5. Où est installé Git ?
# Linux/Mac
which git
# Résultat: /usr/bin/git

# Windows (PowerShell)
Get-Command git
# Résultat: C:\Program Files\Git\cmd\git.exe
```

### Version minimale recommandée

```bash
# Vérifier votre version
git --version

# Recommandations:
# Minimum: Git 2.23+ (pour les nouvelles commandes comme git switch)
# Idéal: Git 2.40+ (dernières fonctionnalités et corrections)
# Actuel: Git 2.43+ (décembre 2025)
```

### Test d'un premier repository

```bash
# Créer un dossier de test
mkdir ~/git-test
cd ~/git-test

# Initialiser un repository Git
git init
# Résultat: Initialized empty Git repository in /home/user/git-test/.git/

# Vérifier le statut
git status
# Résultat: On branch main
#          No commits yet

# Créer un fichier
echo "# Mon premier repository Git" > README.md

# Voir le statut
git status
# Le fichier README.md apparaît comme "Untracked"

# Ajouter le fichier au staging
git add README.md

# Créer le premier commit (après configuration, voir chapitre suivant)
# git commit -m "Initial commit"

# Nettoyer
cd ..
rm -rf ~/git-test
```

---

## Interfaces graphiques

Git peut être utilisé en **ligne de commande** (CLI) ou avec une **interface graphique** (GUI).

### Pourquoi utiliser une GUI ?

✅ **Avantages:**
- Visualisation graphique des branches et de l'historique
- Résolution de conflits plus intuitive
- Staging partiel de fichiers facilité
- Courbe d'apprentissage plus douce pour les débutants

❌ **Inconvénients:**
- Moins flexible que la CLI
- Certaines opérations avancées nécessitent la CLI
- Performance parfois moins bonne sur gros projets

### Interfaces graphiques populaires

#### 1. GitKraken (Multiplateforme)

**Installation:**
```bash
# Linux (Snap)
sudo snap install gitkraken --classic

# macOS (Homebrew)
brew install --cask gitkraken

# Windows
# Télécharger depuis: https://www.gitkraken.com/
```

**Caractéristiques:**
- ✅ Interface très intuitive et belle
- ✅ Intégrations GitHub, GitLab, Bitbucket
- ✅ Merge conflict editor intégré
- ✅ Graphe interactif de l'historique
- ⚠️ Version gratuite limitée (publics repos only)

#### 2. GitHub Desktop (Windows & macOS)

**Installation:**
```bash
# macOS (Homebrew)
brew install --cask github

# Windows
# Télécharger depuis: https://desktop.github.com/
```

**Caractéristiques:**
- ✅ Totalement gratuit
- ✅ Simple et épuré
- ✅ Intégration parfaite avec GitHub
- ✅ Idéal pour les débutants
- ❌ Moins de fonctionnalités avancées

#### 3. SourceTree (Windows & macOS)

**Installation:**
```bash
# Télécharger depuis: https://www.sourcetreeapp.com/
```

**Caractéristiques:**
- ✅ Totalement gratuit
- ✅ Très complet
- ✅ Git Flow intégré
- ✅ Support Bitbucket et GitHub
- ⚠️ Peut être complexe pour débutants

#### 4. Git GUI (Inclus avec Git)

```bash
# Lancer Git GUI
git gui

# Interface Tcl/Tk basique mais fonctionnelle
# Incluse par défaut avec Git
# Gratuite et simple
```

#### 5. Visual Studio Code (Éditeur avec Git intégré)

**Installation:**
```bash
# Linux
sudo snap install code --classic

# macOS
brew install --cask visual-studio-code

# Windows
# Télécharger depuis: https://code.visualstudio.com/
```

**Extensions Git recommandées:**
- **GitLens** - Suralimente Git dans VS Code
- **Git Graph** - Visualiser l'historique
- **Git History** - Historique de fichiers
- **GitHub Pull Requests** - Gérer les PRs

```bash
# Installer GitLens depuis VS Code
code --install-extension eamodio.gitlens
```

#### 6. Autres options

| GUI | Plateforme | Prix | Notes |
|-----|-----------|------|-------|
| **Fork** | Win, Mac | Gratuit | Simple et rapide |
| **SmartGit** | Win, Mac, Linux | Payant | Très complet |
| **Tower** | Win, Mac | Payant | Professionnel |
| **Sublime Merge** | Win, Mac, Linux | Payant | Par les créateurs de Sublime Text |
| **TortoiseGit** | Windows | Gratuit | Intégration Windows Explorer |

### Recommandations

**Pour débuter:**
- 🥇 **GitHub Desktop** - Simple et gratuit
- 🥈 **VS Code + GitLens** - Si vous codez déjà dans VS Code

**Pour usage professionnel:**
- 🥇 **GitKraken** - Le plus complet et beau
- 🥈 **SourceTree** - Gratuit et très complet

**Pour experts CLI:**
- Restez en ligne de commande + **Git Graph** dans VS Code pour visualiser

---

## Configuration des outils

### Git dans le Terminal

```bash
# Linux/Mac: Ajouter des alias dans ~/.bashrc ou ~/.zshrc
echo 'alias gs="git status"' >> ~/.bashrc
echo 'alias ga="git add"' >> ~/.bashrc
echo 'alias gc="git commit"' >> ~/.bashrc
echo 'alias gp="git push"' >> ~/.bashrc
echo 'alias gl="git log --oneline --graph --all"' >> ~/.bashrc

# Recharger
source ~/.bashrc
```

### Git dans PowerShell (Windows)

```powershell
# Créer un profil PowerShell
if (!(Test-Path -Path $PROFILE)) {
  New-Item -ItemType File -Path $PROFILE -Force
}

# Ouvrir le profil
notepad $PROFILE

# Ajouter des alias
Set-Alias -Name gs -Value git status
Set-Alias -Name ga -Value git add
Set-Alias -Name gc -Value git commit

# Ou installer Posh-Git (Git pour PowerShell)
Install-Module posh-git -Scope CurrentUser -Force
Import-Module posh-git
Add-PoshGitToProfile -AllHosts
```

---

## Différences principales par OS

| Aspect | Linux | Windows | macOS |
|--------|-------|---------|-------|
| **Installation** | Package manager | Installateur | Homebrew ou Xcode |
| **Terminal** | Terminal natif | Git Bash / PowerShell | Terminal.app |
| **Chemins** | / (slash) | \ (backslash) ou / | / (slash) |
| **Line endings** | LF | CRLF | LF |
| **Performance** | Excellent | Bon | Excellent |
| **Permissions** | Important | Moins important | Important |

### Line Endings (Important !)

```bash
# Problème: Windows utilise CRLF, Linux/Mac utilisent LF
# Git peut convertir automatiquement

# Configuration recommandée:

# Windows
git config --global core.autocrlf true
# Convertit LF → CRLF au checkout, CRLF → LF au commit

# Linux/Mac
git config --global core.autocrlf input
# Convertit CRLF → LF au commit, pas de conversion au checkout

# Vérifier
git config core.autocrlf
```

---

## Prochaines étapes

Maintenant que Git est installé, vous devez le configurer:

1. [**Configuration Git**](./infos-git-02-configuration.md) - Configurer votre identité et préférences
2. [**Concepts Fondamentaux**](./infos-git-03-concepts-fondamentaux.md) - Comprendre comment Git fonctionne
3. [**Commandes de Base**](./infos-git-04-commandes-base.md) - Vos premiers commits

---

[← Retour à l'index](./infos-git-00-index.md) | [Configuration →](./infos-git-02-configuration.md)

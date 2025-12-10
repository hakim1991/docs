# 🚀 Introduction et Installation

[Index](./infos-tmux-00-index.md) | [Configuration de base →](./infos-tmux-02-configuration-base.md)

## Qu'est-ce que tmux ?

**tmux** (terminal multiplexer) est un outil qui permet de gérer plusieurs sessions de terminal dans une seule fenêtre.

### Avantages

```
✅ Sessions persistantes (survit aux déconnexions)
✅ Multiples fenêtres et panneaux
✅ Partage de session (pair programming)
✅ Scripts et automatisation
✅ Détachement/attachement à volonté
✅ Layouts personnalisables
✅ Copy/paste avancé
✅ Monitoring de processus
```

### Concepts de base

```
Session
 ├── Window 1
 │   ├── Pane 1
 │   └── Pane 2
 ├── Window 2
 │   ├── Pane 1
 │   ├── Pane 2
 │   └── Pane 3
 └── Window 3
     └── Pane 1

Session  : Conteneur principal (peut se détacher/attacher)
Window   : Onglet/écran (comme les tabs du navigateur)
Pane     : Division d'une window (split vertical/horizontal)
```

## Installation

### Ubuntu / Debian

```bash
# Installer tmux
sudo apt update
sudo apt install tmux

# Vérifier la version
tmux -V
```

### CentOS / RHEL / Fedora

```bash
# CentOS/RHEL
sudo yum install tmux

# Fedora
sudo dnf install tmux

# Version
tmux -V
```

### macOS

```bash
# Avec Homebrew
brew install tmux

# Vérifier
tmux -V
```

### Compiler depuis les sources (version latest)

```bash
# Dépendances
sudo apt install libevent-dev ncurses-dev build-essential bison pkg-config

# Télécharger
cd /tmp
wget https://github.com/tmux/tmux/releases/download/3.3a/tmux-3.3a.tar.gz
tar xzf tmux-3.3a.tar.gz
cd tmux-3.3a

# Compiler
./configure
make
sudo make install

# Vérifier
tmux -V
```

### Windows (WSL)

```bash
# Dans WSL (Ubuntu)
sudo apt update
sudo apt install tmux

# Ou avec Chocolatey (natif Windows - moins recommandé)
choco install tmux
```

## Première utilisation

### Démarrer tmux

```bash
# Démarrer une nouvelle session
tmux

# Démarrer avec un nom
tmux new -s mysession

# Ou
tmux new-session -s mysession
```

### Commandes de base

```bash
# Prefix key par défaut : Ctrl+b
# Notation : C-b = Ctrl+b

# Détacher la session
C-b d

# Lister les sessions
tmux ls

# Attacher à une session
tmux attach
tmux attach -t mysession
tmux a -t mysession

# Tuer une session
tmux kill-session -t mysession

# Tuer le serveur tmux (toutes les sessions)
tmux kill-server
```

### Workflow de base

```bash
# 1. Créer une session
tmux new -s dev

# 2. Travailler dans la session
# ... votre travail ...

# 3. Détacher (C-b d)
# La session continue en arrière-plan

# 4. Revenir plus tard
tmux attach -t dev

# 5. Créer une autre session
tmux new -s admin

# 6. Lister toutes les sessions
tmux ls

# 7. Passer entre les sessions
C-b s    # Liste interactive

# 8. Tuer une session terminée
tmux kill-session -t dev
```

## Commandes essentielles

```bash
# Sessions
tmux                          # Nouvelle session
tmux new -s name              # Nouvelle session nommée
tmux ls                       # Lister sessions
tmux attach -t name           # Attacher à une session
tmux kill-session -t name     # Tuer une session
tmux rename-session -t old new # Renommer

# Windows
C-b c                         # Créer window
C-b ,                         # Renommer window
C-b n                         # Next window
C-b p                         # Previous window
C-b 0-9                       # Aller à window N
C-b w                         # Liste des windows
C-b &                         # Tuer window

# Panes
C-b %                         # Split vertical
C-b "                         # Split horizontal
C-b o                         # Pane suivant
C-b ;                         # Dernier pane
C-b x                         # Tuer pane
C-b espace                    # Changer layout
C-b arrows                    # Naviguer entre panes
C-b C-arrows                  # Redimensionner pane

# Autres
C-b ?                         # Aide (liste raccourcis)
C-b :                         # Mode commande
C-b [                         # Mode copy
C-b ]                         # Coller
C-b t                         # Horloge
```

## Configuration minimale

```bash
# Créer fichier de configuration
nano ~/.tmux.conf
```

```bash
# ~/.tmux.conf - Configuration minimale

# Changer le prefix de C-b à C-a (plus ergonomique)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes avec | et -
bind | split-window -h
bind - split-window -v
unbind '"'
unbind %

# Navigation panes avec Alt+arrows (sans prefix)
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Recharger config
bind r source-file ~/.tmux.conf \; display "Config rechargée!"

# Activer la souris
set -g mouse on

# Numérotation à partir de 1
set -g base-index 1
setw -g pane-base-index 1

# Historique
set -g history-limit 10000

# Couleurs 256
set -g default-terminal "screen-256color"
```

```bash
# Recharger la configuration
tmux source-file ~/.tmux.conf

# Ou depuis tmux
C-b :
source-file ~/.tmux.conf
```

## Exemples d'utilisation

### Développement web

```bash
# Créer session dev
tmux new -s webapp

# Window 1: Serveur
C-b c
npm run dev

# Window 2: Logs
C-b c
tail -f logs/app.log

# Window 3: Terminal
C-b c
# Commandes git, etc.

# Détacher
C-b d

# Revenir
tmux attach -t webapp
```

### Administration système

```bash
# Session monitoring
tmux new -s monitor

# Pane 1: htop
htop

# Split vertical
C-b |

# Pane 2: logs
tail -f /var/log/syslog

# Split horizontal (dans pane 2)
C-b -

# Pane 3: network
watch -n 1 'ss -tulpn'
```

### SSH persistant

```bash
# Sur serveur distant
ssh user@server

# Créer session tmux
tmux new -s work

# Travailler...
# Si déconnexion SSH, la session continue

# Reconnecter
ssh user@server
tmux attach -t work
```

## Alias utiles

```bash
# Ajouter dans ~/.bashrc ou ~/.zshrc

# Alias tmux
alias ta='tmux attach -t'
alias tad='tmux attach -d -t'
alias ts='tmux new-session -s'
alias tl='tmux list-sessions'
alias tksv='tmux kill-server'
alias tkss='tmux kill-session -t'

# Fonction pour créer ou attacher
tm() {
    [[ -n "$1" ]] && tmux new -A -s "$1" || tmux new
}

# Usage:
# tm dev       # Crée ou attache à session "dev"
# ta work      # Attache à session "work"
# tl           # Liste sessions
```

## Vérifier l'installation

```bash
# Version
tmux -V

# Info détaillée
tmux info

# Commandes disponibles
tmux list-commands

# Variables serveur
tmux show-options -g

# Variables window
tmux show-window-options -g
```

## Première session interactive

```bash
# Créer une session de test
tmux new -s test

# Essayer ces commandes:
# 1. Créer une window
C-b c

# 2. Renommer la window
C-b ,
# Taper: "Editor"

# 3. Split vertical
C-b %

# 4. Split horizontal (dans le pane de droite)
C-b "

# 5. Naviguer
C-b arrows

# 6. Redimensionner
C-b C-arrows

# 7. Changer layout
C-b space

# 8. Créer une autre window
C-b c

# 9. Lister les windows
C-b w

# 10. Détacher
C-b d

# 11. Réattacher
tmux attach -t test

# 12. Tuer
tmux kill-session -t test
```

## Troubleshooting installation

```bash
# tmux: command not found
# Vérifier installation
which tmux

# Réinstaller si nécessaire
sudo apt install --reinstall tmux

# Version trop ancienne
# Compiler depuis sources (voir ci-dessus)

# Problèmes de couleurs
# Ajouter dans .bashrc/.zshrc:
export TERM=xterm-256color

# Et dans .tmux.conf:
set -g default-terminal "screen-256color"

# Souris ne fonctionne pas
# Ajouter dans .tmux.conf:
set -g mouse on

# Rechargement config ne fonctionne pas
# Sortir complètement de tmux
tmux kill-server
# Puis redémarrer
tmux
```

## Ressources

```
📚 Ressources utiles:

Documentation officielle:
- https://github.com/tmux/tmux/wiki
- man tmux

Cheatsheets:
- https://tmuxcheatsheet.com/
- https://gist.github.com/MohamedAlaa/2961058

Livres:
- "tmux 2: Productive Mouse-Free Development"
- "The Tao of tmux"

Communauté:
- r/tmux
- GitHub Discussions
```

[Index](./infos-tmux-00-index.md) | [Configuration de base →](./infos-tmux-02-configuration-base.md)

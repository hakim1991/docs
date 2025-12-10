# 🪟 Sessions, Windows et Panes

[← Configuration base](./infos-tmux-02-configuration-base.md) | [Index](./infos-tmux-00-index.md) | [Raccourcis clavier →](./infos-tmux-04-raccourcis-clavier.md)

## Hiérarchie tmux

```
Serveur tmux
 └── Session "dev"
      ├── Window 0: "editor"
      │   ├── Pane 0 (vim)
      │   └── Pane 1 (terminal)
      ├── Window 1: "server"
      │   └── Pane 0 (npm run dev)
      └── Window 2: "logs"
          ├── Pane 0 (app logs)
          ├── Pane 1 (system logs)
          └── Pane 2 (htop)
```

## Gestion des Sessions

### Créer des sessions

```bash
# Nouvelle session
tmux
tmux new
tmux new-session

# Nouvelle session avec nom
tmux new -s dev
tmux new-session -s myproject

# Avec window nommée
tmux new -s dev -n editor

# Avec commande
tmux new -s logs -d "tail -f /var/log/syslog"

# En arrière-plan
tmux new -s background -d
```

### Lister les sessions

```bash
# Depuis l'extérieur
tmux ls
tmux list-sessions

# Depuis tmux (C-a s)
C-a s

# Avec détails
tmux list-sessions -F "#{session_name}: #{session_windows} windows (created #{session_created_string})"
```

### Attacher aux sessions

```bash
# Attacher à la dernière session
tmux attach
tmux a

# Attacher à une session spécifique
tmux attach -t dev
tmux a -t myproject

# Attacher ou créer
tmux new-session -A -s dev

# Attacher en détachant les autres clients
tmux attach -d -t dev
```

### Détacher de session

```bash
# Depuis tmux
C-a d               # Détacher
C-a D               # Choisir client à détacher

# Depuis l'extérieur
tmux detach-client -s dev
tmux detach-client -t dev
```

### Renommer session

```bash
# Depuis tmux
C-a $

# Depuis l'extérieur
tmux rename-session -t old new

# Ou depuis la session
C-a :
rename-session newname
```

### Tuer session

```bash
# Depuis l'extérieur
tmux kill-session -t dev

# Tuer toutes sauf la courante
tmux kill-session -a

# Tuer toutes les sessions
tmux kill-server

# Depuis tmux
C-a :
kill-session
```

### Passer entre sessions

```bash
# Liste interactive
C-a s

# Session précédente
C-a (

# Session suivante
C-a )

# Dernière session
C-a L

# Par nom
C-a :
switch-client -t dev
```

## Gestion des Windows

### Créer windows

```bash
# Nouvelle window
C-a c

# Avec nom
C-a :
new-window -n logs

# Depuis l'extérieur
tmux new-window -t dev:1 -n server
tmux new-window -t dev -n editor "vim"

# Dans le current path
C-a c  # Si bind c new-window -c "#{pane_current_path}"
```

### Navigation windows

```bash
# Next/Previous
C-a n               # Next
C-a p               # Previous

# Par numéro
C-a 0               # Window 0
C-a 1               # Window 1
C-a 9               # Window 9

# Par nom
C-a f               # Find window
C-a '               # Prompt pour numéro/nom

# Dernière window
C-a l

# Liste interactive
C-a w
```

### Renommer window

```bash
# Depuis tmux
C-a ,

# Depuis l'extérieur
tmux rename-window -t dev:1 "server"

# Automatique (désactiver)
set -g automatic-rename off
```

### Déplacer windows

```bash
# Swap windows
C-a :
swap-window -s 2 -t 1

# Déplacer window vers autre session
C-a :
move-window -t dev:

# Lier window à plusieurs sessions
C-a :
link-window -s dev:0 -t prod:0
```

### Tuer window

```bash
# Depuis tmux
C-a &               # Confirmer

# Sans confirmation
C-a :
kill-window

# Depuis l'extérieur
tmux kill-window -t dev:1
```

### Window layouts

```bash
# Changer layout
C-a Space           # Cycle layouts

# Layouts disponibles:
# - even-horizontal
# - even-vertical
# - main-horizontal
# - main-vertical
# - tiled

# Appliquer layout spécifique
C-a :
select-layout even-horizontal
select-layout tiled
```

## Gestion des Panes

### Créer panes (splits)

```bash
# Split vertical (|)
C-a %
# Ou custom: C-a |

# Split horizontal (-)
C-a "
# Ou custom: C-a -

# Split avec taille
C-a :
split-window -h -l 50%
split-window -v -l 20

# Full width/height
split-window -fh     # Full horizontal
split-window -fv     # Full vertical
```

### Navigation panes

```bash
# Directionnelles
C-a arrows          # Haut/Bas/Gauche/Droite

# Vim-style (custom binding)
C-a h               # Gauche
C-a j               # Bas
C-a k               # Haut
C-a l               # Droite

# Cycle
C-a o               # Pane suivant
C-a ;               # Dernier pane actif

# Par numéro
C-a q               # Afficher numéros
C-a q 0             # Aller au pane 0
```

### Redimensionner panes

```bash
# Avec prefix + Ctrl+arrows
C-a C-Up
C-a C-Down
C-a C-Left
C-a C-Right

# Vim-style (custom -r pour repeat)
C-a H               # Réduire largeur
C-a L               # Augmenter largeur
C-a K               # Réduire hauteur
C-a J               # Augmenter hauteur

# Taille exacte
C-a :
resize-pane -U 10   # Up 10 lignes
resize-pane -D 10   # Down 10 lignes
resize-pane -L 20   # Left 20 cols
resize-pane -R 20   # Right 20 cols

# Pourcentage
resize-pane -x 50%  # 50% de largeur
resize-pane -y 30%  # 30% de hauteur
```

### Zoom pane

```bash
# Toggle fullscreen
C-a z

# Utile pour:
# - Lire un long output
# - Copier du texte
# - Focus temporaire
```

### Swap panes

```bash
# Swap avec pane suivant
C-a }

# Swap avec pane précédent
C-a {

# Rotation
C-a C-o             # Rotate clockwise

# Swap specifique
C-a :
swap-pane -s 0 -t 1
```

### Break/Join panes

```bash
# Break pane vers nouvelle window
C-a !

# Joindre pane depuis autre window
C-a :
join-pane -s :1.0   # Window 1, pane 0 vers current
join-pane -h -s :1  # Horizontal split

# Exemple workflow:
# 1. Créer window avec pane intéressant
# 2. Break pane (C-a !)
# 3. Nouveau window créée
```

### Synchronize panes

```bash
# Envoyer commandes à tous les panes
C-a :
setw synchronize-panes on

# Désactiver
setw synchronize-panes off

# Toggle
setw synchronize-panes

# Binding custom
bind S setw synchronize-panes

# Utilisation:
# - Déploiement simultané
# - Administration multiple serveurs
# - Tests parallèles
```

### Tuer pane

```bash
# Depuis tmux
C-a x               # Confirmer

# Exit ou Ctrl+D
exit
C-d

# Sans confirmation
C-a :
kill-pane

# Depuis l'extérieur
tmux kill-pane -t dev:0.1
```

## Cas pratiques

### Setup développement web

```bash
# Session dev
tmux new -s webapp -n editor

# Window 1: Editor (3 panes)
vim
C-a |               # Split vertical
# Terminal pour git
C-a -               # Split horizontal
# Tests

# Window 2: Server
C-a c
C-a , server
npm run dev

# Window 3: Logs
C-a c
C-a , logs
C-a -
# Pane 1: app logs
tail -f logs/app.log
# Pane 2: system logs
C-a j
journalctl -f

# Window 4: Database
C-a c
C-a , database
psql mydb
```

### Monitoring système

```bash
# Session monitoring
tmux new -s monitor -n system

# Layout 4 panes
C-a %               # Split vertical
C-a "               # Split horizontal gauche
C-a o
C-a "               # Split horizontal droite

# Pane 1: htop
htop

# Pane 2: disk
C-a arrows
watch -n 1 df -h

# Pane 3: network
watch -n 1 'ss -tulpn'

# Pane 4: logs
tail -f /var/log/syslog
```

### Multiple SSH

```bash
# Session SSH
tmux new -s servers

# Pane pour chaque serveur
ssh server1
C-a |
ssh server2
C-a |
ssh server3

# Synchroniser
C-a :
setw synchronize-panes on

# Commandes identiques sur tous
sudo apt update
# etc.

# Désynchroniser
setw synchronize-panes off
```

## Templates et Scripts

### Script de setup

```bash
#!/bin/bash
# setup-dev.sh

SESSION="dev"

# Créer session
tmux new-session -d -s $SESSION -n editor

# Window 1: Editor
tmux send-keys -t $SESSION:1 "cd ~/project && vim" C-m
tmux split-window -h -t $SESSION:1
tmux send-keys -t $SESSION:1.2 "cd ~/project" C-m

# Window 2: Server
tmux new-window -t $SESSION:2 -n server
tmux send-keys -t $SESSION:2 "cd ~/project && npm run dev" C-m

# Window 3: Logs
tmux new-window -t $SESSION:3 -n logs
tmux send-keys -t $SESSION:3 "cd ~/project && tail -f logs/app.log" C-m

# Attacher
tmux attach -t $SESSION:1
```

### Commandes send-keys

```bash
# Envoyer commandes à une session/window/pane
tmux send-keys -t dev:1 "ls -la" C-m
tmux send-keys -t dev:1.0 "vim file.txt" C-m

# C-m = Enter
# C-c = Ctrl+C
# C-d = Ctrl+D

# Exemple: restart server
tmux send-keys -t dev:server C-c "npm run dev" C-m
```

## Commandes avancées

### Capture pane

```bash
# Capturer output d'un pane
tmux capture-pane -t dev:1.0 -p > output.txt

# Historique complet
tmux capture-pane -t dev:1.0 -p -S - > full-history.txt

# Depuis tmux
C-a :
capture-pane -S -3000  # Dernières 3000 lignes
save-buffer output.txt
```

### Pipe pane

```bash
# Rediriger output vers fichier
tmux pipe-pane -t dev:1 "cat >> ~/logs/dev.log"

# Arrêter
tmux pipe-pane -t dev:1
```

### Commande dans tous les panes

```bash
# Script pour envoyer commande à tous les panes
for pane in $(tmux list-panes -s -F "#{session_name}:#{window_index}.#{pane_index}"); do
    tmux send-keys -t $pane "echo 'Hello from all panes'" C-m
done
```

## Configuration utile

```bash
# ~/.tmux.conf

# Fermer pane sans confirmation
bind x kill-pane

# Fermer window sans confirmation
bind X kill-window

# Nouvelle window dans current path
bind c new-window -c "#{pane_current_path}"

# Splits dans current path
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Resize facile
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Zoom toggle
bind z resize-pane -Z

# Synchronize toggle
bind S setw synchronize-panes

# Break/join
bind b break-pane -d
bind j command-prompt -p "Join pane from:"  "join-pane -s '%%'"
```

[← Configuration base](./infos-tmux-02-configuration-base.md) | [Index](./infos-tmux-00-index.md) | [Raccourcis clavier →](./infos-tmux-04-raccourcis-clavier.md)

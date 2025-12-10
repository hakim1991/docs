# 🔧 Configuration avancée

[← Personnalisation](./infos-tmux-05-personnalisation.md) | [Index](./infos-tmux-00-index.md) | [Plugins et TPM →](./infos-tmux-07-plugins-tpm.md)

## Options serveur

### Options globales serveur

```bash
# ~/.tmux.conf

# Escape time (important pour vim)
set -s escape-time 0
set -s escape-time 10

# Focus events
set -s focus-events on

# Default terminal
set -s default-terminal "screen-256color"

# Terminal overrides
set -sa terminal-overrides ",xterm-256color:Tc"
set -sa terminal-overrides ",*:RGB"

# Historique commandes
set -s history-file ~/.tmux_history

# Buffer size
set -s buffer-limit 50
```

## Options session

### Options globales session

```bash
# ~/.tmux.conf

# Base index
set -g base-index 1

# Activity monitoring
set -g activity-action none
set -g visual-activity off
set -g monitor-activity on

# Bell
set -g bell-action any
set -g visual-bell off

# Historique
set -g history-limit 50000
set -g history-limit 100000

# Messages
set -g display-time 4000
set -g message-limit 100

# Renumbering
set -g renumber-windows on

# Titles
set -g set-titles on
set -g set-titles-string '#S:#I:#W - "#{pane_title}"'

# Status bar
set -g status on
set -g status-interval 1
set -g status-position bottom

# Mouse
set -g mouse on

# Prefix
set -g prefix C-a
set -g prefix2 None

# Repeat time (pour -r bindings)
set -g repeat-time 500

# Mode keys
set -g mode-keys vi
set -g status-keys emacs
```

## Options window

### Options globales window

```bash
# ~/.tmux.conf

# Pane base index
setw -g pane-base-index 1

# Mode keys
setw -g mode-keys vi

# Monitor activity
setw -g monitor-activity on

# Monitor bell
setw -g monitor-bell on

# Monitor silence
setw -g monitor-silence 0

# Automatic rename
setw -g automatic-rename on
setw -g automatic-rename-format '#{b:pane_current_path}'

# Allow rename
setw -g allow-rename off

# Aggressive resize
setw -g aggressive-resize on

# Clock
setw -g clock-mode-style 24
```

## Hooks

### Types de hooks

```bash
# ~/.tmux.conf

# Hooks disponibles:
# - after-bind-key
# - after-capture-pane
# - after-copy-mode
# - after-display-message
# - after-display-panes
# - after-kill-pane
# - after-list-buffers
# - after-list-clients
# - after-list-keys
# - after-list-panes
# - after-list-sessions
# - after-list-windows
# - after-load-buffer
# - after-lock-server
# - after-new-session
# - after-new-window
# - after-paste-buffer
# - after-pipe-pane
# - after-queue
# - after-refresh-client
# - after-rename-session
# - after-rename-window
# - after-resize-pane
# - after-resize-window
# - after-save-buffer
# - after-select-layout
# - after-select-pane
# - after-select-window
# - after-send-keys
# - after-set-buffer
# - after-set-environment
# - after-set-hook
# - after-set-option
# - after-show-environment
# - after-show-messages
# - after-show-options
# - after-split-window
# - after-unbind-key
# - alert-activity
# - alert-bell
# - alert-silence
# - client-attached
# - client-detached
# - client-resized
# - client-session-changed
# - pane-died
# - pane-exited
# - pane-focus-in
# - pane-focus-out
# - pane-mode-changed
# - pane-set-clipboard
# - session-closed
# - session-created
# - session-renamed
# - session-window-changed
# - window-layout-changed
# - window-linked
# - window-pane-changed
# - window-renamed
# - window-unlinked
```

### Hooks pratiques

```bash
# ~/.tmux.conf

# Notification à la création de window
set-hook -g after-new-window 'display-message "Nouvelle window créée"'

# Auto-renommer session
set-hook -g client-attached 'run-shell "tmux rename-session $(basename $(pwd))"'

# Message à la fermeture de pane
set-hook -g pane-exited 'display-message "Pane fermé"'

# Synchroniser tous les panes au focus
set-hook -g pane-focus-in 'run-shell "tmux display-message \"Pane #D actif\""'

# Notification activity
set-hook -g alert-activity 'display-message "Activity dans #I:#W"'

# Log à la création de session
set-hook -g session-created 'run-shell "echo $(date): Session #S créée >> ~/.tmux-sessions.log"'

# Restaurer layout après resize
set-hook -g client-resized 'run-shell "tmux select-layout"'

# Auto-update git branch dans status
set-hook -g pane-focus-in 'run-shell "tmux refresh-client -S"'
```

### Hooks avec conditions

```bash
# ~/.tmux.conf

# Hook seulement pour certaines sessions
set-hook -g session-created 'if-shell "test #{session_name} = dev" "display-message Dev session"'

# Hook avec variables
set-hook -g after-new-window 'display-message "Window #I:#W créée dans session #S"'

# Hook conditionnel
set-hook -g pane-exited 'if-shell "test #{window_panes} -eq 0" "kill-window"'
```

## Bindings avancés

### Bindings avec conditions

```bash
# ~/.tmux.conf

# Toggle mouse
bind m if-shell "tmux show -g mouse | grep on" \
    "set -g mouse off; display-message 'Mouse OFF'" \
    "set -g mouse on; display-message 'Mouse ON'"

# Toggle status bar
bind s if-shell "tmux show -g status | grep on" \
    "set -g status off" \
    "set -g status on"

# Zoom avec indicateur
bind z resize-pane -Z \; display-message "#{?window_zoomed_flag,Zoomed,Unzoomed}"

# Kill sans confirmation si 1 seul pane
bind x if-shell "test #{window_panes} -eq 1" \
    "confirm-before -p 'Kill window? (y/n)' kill-window" \
    "kill-pane"
```

### Tables de bindings

```bash
# ~/.tmux.conf

# Tables disponibles:
# - root (sans prefix)
# - prefix (avec prefix)
# - copy-mode
# - copy-mode-vi

# Créer table personnalisée
bind -T mytable a display-message "A in mytable"
bind -T mytable b display-message "B in mytable"

# Activer la table
bind m switch-client -T mytable

# Exemple: Table resize
bind -T resize-table h resize-pane -L 5
bind -T resize-table j resize-pane -D 5
bind -T resize-table k resize-pane -U 5
bind -T resize-table l resize-pane -R 5
bind -T resize-table q switch-client -T prefix

bind r switch-client -T resize-table
```

### Repeat bindings

```bash
# ~/.tmux.conf

# -r permet de répéter sans re-taper prefix
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Temps de repeat (défaut: 500ms)
set -g repeat-time 1000

# Navigation windows
bind -r n next-window
bind -r p previous-window

# Cycle panes
bind -r Tab select-pane -t :.+
```

## Commandes run-shell

### Exécuter scripts

```bash
# ~/.tmux.conf

# Commande simple
bind R run-shell "tmux source-file ~/.tmux.conf"

# Script externe
bind S run-shell "~/scripts/tmux-save-session.sh"

# Avec output
bind L run-shell "tmux list-sessions | head -5"

# Async
bind A run-shell -b "sleep 5 && tmux display-message 'Done'"

# Avec variables tmux
bind P run-shell "echo Session: #{session_name}, Window: #{window_name}"
```

### Scripts dans status bar

```bash
# ~/.tmux.conf

# Git branch
set -g status-right "#(cd #{pane_current_path}; git rev-parse --abbrev-ref HEAD 2>/dev/null)"

# CPU usage
set -g status-right "#(top -bn1 | grep 'Cpu' | awk '{print $2}')"

# Memory
set -g status-right "#(free -h | awk '/^Mem/ {print $3}')"

# Kubernetes context
set -g status-right "#(kubectl config current-context 2>/dev/null)"

# Docker status
set -g status-right "#(docker ps -q 2>/dev/null | wc -l) containers"

# VPN status
set -g status-right "#(ip a | grep -q tun0 && echo '🔒 VPN' || echo '🔓')"
```

## Commandes if-shell

### Conditions système

```bash
# ~/.tmux.conf

# Détecter OS
if-shell "uname | grep -q Darwin" \
    "set -g default-command 'reattach-to-user-namespace -l zsh'"

# Linux vs macOS clipboard
if-shell "uname | grep -q Darwin" \
    "bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'pbcopy'" \
    "bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'xclip -selection clipboard'"

# Version tmux
if-shell "test $(tmux -V | cut -d' ' -f2 | tr -d '[:alpha:]') -ge 3.0" \
    "set -g mouse on"

# Fichier existe
if-shell "test -f ~/.tmux-local.conf" \
    "source-file ~/.tmux-local.conf"

# Commande existe
if-shell "command -v reattach-to-user-namespace >/dev/null" \
    "set -g default-command 'reattach-to-user-namespace -l $SHELL'"
```

### Conditions tmux

```bash
# ~/.tmux.conf

# Session existe
bind S if-shell "tmux has-session -t dev 2>/dev/null" \
    "attach-session -t dev" \
    "new-session -s dev"

# Window name
bind W if-shell "test '#{window_name}' = 'editor'" \
    "display-message 'Editor window'" \
    "display-message 'Not editor'"

# Pane count
bind X if-shell "test #{window_panes} -gt 1" \
    "kill-pane" \
    "kill-window"
```

## Formats avancés

### Variables de format

```bash
# Variables principales:

# Session
#{session_id}              # $0, $1, etc.
#{session_name}            # Nom session
#{session_windows}         # Nombre windows
#{session_created}         # Timestamp création
#{session_activity}        # Timestamp dernière activité
#{session_attached}        # Nombre clients attachés
#{session_many_attached}   # Plus d'un client attaché

# Window
#{window_id}               # @0, @1, etc.
#{window_index}            # Index window
#{window_name}             # Nom window
#{window_active}           # Window active
#{window_panes}            # Nombre panes
#{window_zoomed_flag}      # Pane zoomed
#{window_activity_flag}    # Activity flag

# Pane
#{pane_id}                 # %0, %1, etc.
#{pane_index}              # Index pane
#{pane_current_path}       # Path courant
#{pane_current_command}    # Commande courante
#{pane_pid}                # PID processus
#{pane_width}              # Largeur pane
#{pane_height}             # Hauteur pane
#{pane_title}              # Titre pane
#{pane_in_mode}            # Copy mode actif
#{pane_synchronized}       # Synchronized

# Client
#{client_name}             # Nom client
#{client_width}            # Largeur client
#{client_height}           # Hauteur client
#{client_termname}         # Type terminal
#{client_prefix}           # Prefix pressé

# Host
#{host}                    # Hostname complet
#{host_short}              # Hostname court
```

### Formats conditionnels

```bash
# ~/.tmux.conf

# Syntaxe: #{?condition,true,false}

# Window zoomed
setw -g window-status-format "#{?window_zoomed_flag,🔍 ,}#I:#W"

# Prefix indicator
set -g status-right "#{?client_prefix,⌨️  ,}%H:%M"

# Pane synchronized
set -g status-left "#{?pane_synchronized,🔗 ,}#S"

# Multiple conditions
set -g status-right "#{?client_prefix,⌨️ ,}#{?window_zoomed_flag,🔍 ,}#{?pane_synchronized,🔗 ,}%H:%M"

# Nested conditions
setw -g window-status-format "#{?window_activity_flag,#{?window_bell_flag,🔔,!},}#I:#W"
```

### Substitutions

```bash
# Substitutions disponibles:

#{b:variable}              # Basename
#{d:variable}              # Dirname
#{t:variable}              # Format time
#{s/pattern/replacement/:variable}  # Substitution

# Exemples:
#{b:pane_current_path}     # Nom du répertoire courant
#{d:pane_current_path}     # Chemin parent
#{t:session_created}       # Date formatée
```

## Buffers

### Gestion buffers

```bash
# Lister buffers
C-a =
:list-buffers

# Choisir buffer à coller
C-a =

# Buffer automatique
set -g set-clipboard on
set -g set-clipboard external

# Taille buffers
set -g buffer-limit 20

# Save buffer
:save-buffer filename.txt
:save-buffer -b buffer0 filename.txt

# Load buffer
:load-buffer filename.txt

# Delete buffer
:delete-buffer -b buffer0

# Paste buffer
C-a ]
:paste-buffer
```

### Scripts avec buffers

```bash
# ~/.tmux.conf

# Copy to système clipboard
bind C-c run-shell "tmux save-buffer - | xclip -selection clipboard"

# Paste from système clipboard
bind C-v run-shell "xclip -selection clipboard -o | tmux load-buffer -; tmux paste-buffer"

# Save all buffers
bind S run-shell "for i in \$(tmux list-buffers -F '#{buffer_name}'); do tmux save-buffer -b \$i ~/buffers/\$i.txt; done"
```

## Environnement

### Variables d'environnement

```bash
# ~/.tmux.conf

# Set variable
set-environment -g MY_VAR "value"

# Unset variable
set-environment -u MY_VAR

# Variables globales
set-environment -g DISPLAY :0

# Update environment
set -g update-environment "DISPLAY SSH_AUTH_SOCK SSH_AGENT_PID"

# Show environment
:show-environment

# Use in commands
run-shell "echo $MY_VAR"
```

## Layouts

### Layouts prédéfinis

```bash
# Layouts disponibles:
# - even-horizontal
# - even-vertical
# - main-horizontal
# - main-vertical
# - tiled

# Sélectionner layout
C-a Space              # Cycle layouts
C-a M-1                # even-horizontal
C-a M-2                # even-vertical
C-a M-3                # main-horizontal
C-a M-4                # main-vertical
C-a M-5                # tiled

# Depuis commande
:select-layout even-horizontal
:select-layout main-vertical

# Taille main-pane
:select-layout main-vertical
:resize-pane -t 0 -x 120
```

### Sauvegarder layouts

```bash
# Obtenir layout courant
tmux list-windows -F "#{window_layout}"

# Sauvegarder dans variable
MY_LAYOUT=$(tmux list-windows -F "#{window_layout}")

# Appliquer layout
tmux select-layout "$MY_LAYOUT"

# Dans .tmux.conf
bind L select-layout "bb62,239x60,0,0{119x60,0,0,0,119x60,120,0,1}"
```

## Configuration conditionnelle

### Par OS

```bash
# ~/.tmux.conf

# macOS
if-shell "uname | grep -q Darwin" "source-file ~/.tmux-macos.conf"

# Linux
if-shell "uname | grep -q Linux" "source-file ~/.tmux-linux.conf"

# WSL
if-shell "uname -r | grep -q microsoft" "source-file ~/.tmux-wsl.conf"
```

### Par version tmux

```bash
# ~/.tmux.conf

# >= 3.0
if-shell "test $(echo $(tmux -V | cut -d' ' -f2) | tr -d '[:alpha:]') -ge 3.0" \
    "set -g mouse on"

# < 2.9
if-shell "test $(echo $(tmux -V | cut -d' ' -f2) | tr -d '[:alpha:]') -lt 2.9" \
    "set -g mouse-resize-pane on; set -g mouse-select-pane on"
```

### Par host

```bash
# ~/.tmux.conf

# Laptop
if-shell "test $(hostname) = laptop" \
    "set -g status-right 'Battery: #(acpi -b | cut -d, -f2) | %H:%M'"

# Server
if-shell "test $(hostname) = server" \
    "set -g status-right 'Load: #(cat /proc/loadavg | cut -d' ' -f1-3) | %H:%M'"
```

## Templates complets

### Configuration minimaliste avancée

```bash
# ~/.tmux.conf - Minimal Advanced

# Serveur
set -s escape-time 0
set -s focus-events on

# Session
set -g base-index 1
set -g renumber-windows on
set -g history-limit 50000
set -g mouse on
set -g prefix C-a

# Window
setw -g pane-base-index 1
setw -g mode-keys vi
setw -g aggressive-resize on

# Hooks
set-hook -g after-new-window 'display-message "Window #I créée"'

# Conditional
if-shell "uname | grep -q Darwin" \
    "bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'pbcopy'" \
    "bind -T copy-mode-vi y send -X copy-pipe-and-cancel 'xclip -sel clip'"
```

### Configuration développeur complète

```bash
# ~/.tmux.conf - Dev Complete

# ============================================
# BASE
# ============================================

set -s escape-time 0
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
set -g history-limit 100000
set -g mouse on
set -g prefix C-a
setw -g mode-keys vi

# ============================================
# HOOKS
# ============================================

# Auto git branch in status
set-hook -g pane-focus-in 'refresh-client -S'

# Log sessions
set-hook -g session-created 'run-shell "echo $(date): #{session_name} >> ~/.tmux-sessions.log"'

# ============================================
# BINDINGS
# ============================================

# Toggle mouse
bind m if-shell "tmux show -g mouse | grep on" \
    "set -g mouse off; display 'Mouse OFF'" \
    "set -g mouse on; display 'Mouse ON'"

# ============================================
# STATUS BAR
# ============================================

set -g status-right "#{?client_prefix,⌨️  ,}#(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2) | %H:%M"

# ============================================
# CONDITIONAL
# ============================================

if-shell "uname | grep -q Darwin" \
    "source-file ~/.tmux-macos.conf" \
    "source-file ~/.tmux-linux.conf"
```

[← Personnalisation](./infos-tmux-05-personnalisation.md) | [Index](./infos-tmux-00-index.md) | [Plugins et TPM →](./infos-tmux-07-plugins-tpm.md)

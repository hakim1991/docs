# ⚙️ Configuration de base

[← Introduction](./infos-tmux-01-introduction-installation.md) | [Index](./infos-tmux-00-index.md) | [Sessions, Windows, Panes →](./infos-tmux-03-sessions-windows-panes.md)

## Fichier de configuration

Le fichier de configuration tmux est `~/.tmux.conf`

```bash
# Créer le fichier
touch ~/.tmux.conf

# Éditer
nano ~/.tmux.conf
# ou
vim ~/.tmux.conf
```

## Configuration de base recommandée

```bash
# ~/.tmux.conf

# ============================================
# Options générales
# ============================================

# Changer le prefix (C-b → C-a)
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Recharger la config facilement
bind r source-file ~/.tmux.conf \; display "✅ Config rechargée!"

# Réduire le délai d'échappement
set -s escape-time 0

# Historique
set -g history-limit 50000

# Numérotation à partir de 1
set -g base-index 1
setw -g pane-base-index 1

# Renuméroter automatiquement
set -g renumber-windows on

# ============================================
# Apparence et couleurs
# ============================================

# Terminal 256 couleurs
set -g default-terminal "screen-256color"

# Support RGB (True Color)
set -ga terminal-overrides ",xterm-256color:Tc"

# ============================================
# Souris
# ============================================

# Activer la souris
set -g mouse on

# ============================================
# Splits (panneaux)
# ============================================

# Split avec | et - (plus intuitif)
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# Nouvelle window dans le même path
bind c new-window -c "#{pane_current_path}"

# ============================================
# Navigation
# ============================================

# Navigation panes avec Alt+arrows (sans prefix)
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Navigation windows avec Shift+arrows (sans prefix)
bind -n S-Left previous-window
bind -n S-Right next-window

# ============================================
# Redimensionnement
# ============================================

# Redimensionner panes avec Ctrl+arrows
bind -r C-Left resize-pane -L 5
bind -r C-Right resize-pane -R 5
bind -r C-Up resize-pane -U 5
bind -r C-Down resize-pane -D 5

# ============================================
# Copy mode (mode vi)
# ============================================

# Utiliser les raccourcis vi
setw -g mode-keys vi

# Copy mode avec v et y (comme vim)
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# ============================================
# Status bar
# ============================================

# Rafraîchir toutes les secondes
set -g status-interval 1

# Position en haut
# set -g status-position top

# Longueur des messages
set -g status-left-length 50
set -g status-right-length 100

# ============================================
# Autres
# ============================================

# Focus events (pour vim/neovim)
set -g focus-events on

# Pas de renommage automatique
set -g allow-rename off

# Messages plus longs
set -g display-time 4000

# Activity monitoring
setw -g monitor-activity on
set -g visual-activity off
```

## Recharger la configuration

```bash
# Depuis le shell
tmux source-file ~/.tmux.conf

# Depuis tmux (C-a :)
:source-file ~/.tmux.conf

# Ou avec binding (C-a r)
# Si vous avez ajouté: bind r source-file ~/.tmux.conf
```

## Options importantes

### Prefix key

```bash
# Prefix par défaut: C-b
# Changer pour C-a (plus ergonomique)
set-option -g prefix C-a
bind-key C-a send-prefix
unbind C-b

# Ou utiliser C-Space
set-option -g prefix C-Space
bind-key C-Space send-prefix

# Double prefix envoie le caractère
bind-key C-a send-prefix
```

### Numérotation

```bash
# Windows et panes à partir de 1 (au lieu de 0)
set -g base-index 1
setw -g pane-base-index 1

# Renuméroter automatiquement après fermeture
set -g renumber-windows on
```

### Historique

```bash
# Taille de l'historique
set -g history-limit 10000
set -g history-limit 50000   # Plus de mémoire
set -g history-limit 100000  # Beaucoup de mémoire
```

### Souris

```bash
# Activer la souris
set -g mouse on

# Désactiver
set -g mouse off

# Copy avec la souris
# Activer mouse + sélection copie automatiquement
set -g mouse on
bind-key -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"
```

### Terminal et couleurs

```bash
# 256 couleurs
set -g default-terminal "screen-256color"

# True color support
set -ga terminal-overrides ",xterm-256color:Tc"

# Pour alacritty
set -g default-terminal "alacritty"

# Pour kitty
set -g default-terminal "xterm-kitty"
```

### Délai d'échappement

```bash
# Réduire le délai (important pour vim/neovim)
set -s escape-time 0

# Ou très court
set -s escape-time 10
```

## Bindings personnalisés

### Splits

```bash
# Split horizontal et vertical
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# Ou avec h et v
bind h split-window -h -c "#{pane_current_path}"
bind v split-window -v -c "#{pane_current_path}"

# Full screen split
bind H split-window -fh -c "#{pane_current_path}"
bind V split-window -fv -c "#{pane_current_path}"
```

### Navigation

```bash
# Vim-style navigation
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Sans prefix (Alt+hjkl)
bind -n M-h select-pane -L
bind -n M-j select-pane -D
bind -n M-k select-pane -U
bind -n M-l select-pane -R

# Cycle panes
bind -r Tab select-pane -t :.+
bind -r BTab select-pane -t :.-
```

### Redimensionnement

```bash
# Avec repeat (-r)
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Ou avec Ctrl+arrows
bind -r C-Left resize-pane -L 5
bind -r C-Right resize-pane -R 5
bind -r C-Up resize-pane -U 5
bind -r C-Down resize-pane -D 5
```

### Sessions et windows

```bash
# Nouvelle session
bind N new-session

# Tuer session
bind X confirm-before -p "Tuer session #S? (y/n)" kill-session

# Renommer
bind , command-prompt -I "#W" "rename-window '%%'"
bind $ command-prompt -I "#S" "rename-session '%%'"

# Dernière window
bind Space last-window

# Dernière session
bind L switch-client -l
```

## Options de window et pane

```bash
# Renommage automatique
set -g automatic-rename on
set -g automatic-rename-format '#{b:pane_current_path}'

# Ou désactiver
set -g allow-rename off

# Titre du terminal
set -g set-titles on
set -g set-titles-string '#S:#I:#W - "#T"'

# Activity monitoring
setw -g monitor-activity on
set -g visual-activity on

# Bell
set -g visual-bell off
set -g bell-action any
```

## Copy mode (mode vi)

```bash
# Activer mode vi
setw -g mode-keys vi

# Bindings copy mode
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel
bind -T copy-mode-vi C-v send-keys -X rectangle-toggle

# Copy vers clipboard système
# Linux (xclip)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# macOS
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# WSL
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "clip.exe"

# Enter copy mode
bind [ copy-mode
bind Escape copy-mode

# Paste
bind ] paste-buffer
bind P paste-buffer
```

## Status bar basique

```bash
# Status bar on/off
set -g status on

# Position
set -g status-position bottom  # ou top

# Couleurs
set -g status-style bg=black,fg=white

# Left
set -g status-left "[#S] "
set -g status-left-length 50

# Right
set -g status-right "%H:%M %d-%b-%y"
set -g status-right-length 50

# Window status
setw -g window-status-current-style bg=red,fg=white
setw -g window-status-style bg=black,fg=white
```

## Configuration par type de système

```bash
# ~/.tmux.conf

# Détecter l'OS
if-shell "uname | grep -q Darwin" \
  "source-file ~/.tmux-macos.conf" \
  "source-file ~/.tmux-linux.conf"

# Ou inline
if-shell "uname | grep -q Darwin" \
  "bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'pbcopy'" \
  "bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'xclip -selection clipboard'"
```

## Template de configuration commenté

```bash
# ~/.tmux.conf - Configuration complète commentée

# ============================================
# GÉNÉRAL
# ============================================

# Prefix
set-option -g prefix C-a
bind-key C-a send-prefix
unbind C-b

# Escape time (vim)
set -s escape-time 0

# Historique
set -g history-limit 50000

# Numérotation
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on

# ============================================
# APPARENCE
# ============================================

# Couleurs
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"

# Souris
set -g mouse on

# ============================================
# KEYBINDINGS
# ============================================

# Reload config
bind r source-file ~/.tmux.conf \; display "Config rechargée!"

# Splits
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# Navigation (vim-style)
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Resize
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# ============================================
# COPY MODE
# ============================================

setw -g mode-keys vi
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# ============================================
# STATUS BAR
# ============================================

set -g status-interval 1
set -g status-position bottom
set -g status-style bg=black,fg=white
set -g status-left "[#S] "
set -g status-right "%H:%M:%S"

# ============================================
# AUTRES
# ============================================

set -g focus-events on
set -g allow-rename off
setw -g monitor-activity on
set -g visual-activity off
```

## Tester la configuration

```bash
# Vérifier syntaxe
tmux source-file ~/.tmux.conf

# Voir les options actives
tmux show-options -g

# Voir les bindings
tmux list-keys

# Voir une option spécifique
tmux show-options -g prefix
tmux show-options -g mouse
```

[← Introduction](./infos-tmux-01-introduction-installation.md) | [Index](./infos-tmux-00-index.md) | [Sessions, Windows, Panes →](./infos-tmux-03-sessions-windows-panes.md)

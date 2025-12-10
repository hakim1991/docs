# ⌨️ Raccourcis clavier

[← Sessions, Windows, Panes](./infos-tmux-03-sessions-windows-panes.md) | [Index](./infos-tmux-00-index.md) | [Personnalisation →](./infos-tmux-05-personnalisation.md)

## Prefix key

Par défaut: `C-b` (Ctrl+b)
Recommandé: `C-a` (Ctrl+a)

```bash
# Changer dans ~/.tmux.conf
set-option -g prefix C-a
bind-key C-a send-prefix
unbind C-b
```

**Notation**: `C-a` = Ctrl+a, `M-x` = Alt+x

## Raccourcis par défaut

### Sessions

```
C-a d          Détacher session
C-a $          Renommer session
C-a s          Liste sessions (interactive)
C-a (          Session précédente
C-a )          Session suivante
C-a L          Dernière session active
```

### Windows

```
C-a c          Créer window
C-a ,          Renommer window
C-a &          Tuer window (confirmer)
C-a n          Next window
C-a p          Previous window
C-a l          Dernière window active
C-a 0-9        Aller à window N
C-a w          Liste windows
C-a f          Find window par nom
C-a '          Prompt pour numéro/nom window
C-a .          Déplacer window (prompt numéro)
```

### Panes

```
C-a %          Split vertical
C-a "          Split horizontal
C-a o          Pane suivant
C-a ;          Dernier pane actif
C-a arrows     Naviguer entre panes
C-a C-arrows   Redimensionner pane
C-a x          Tuer pane (confirmer)
C-a z          Zoom/unzoom pane
C-a Space      Changer layout
C-a !          Break pane vers nouvelle window
C-a q          Afficher numéros panes
C-a q 0-9      Aller au pane N
C-a {          Swap avec pane précédent
C-a }          Swap avec pane suivant
C-a C-o        Rotate panes
```

### Copy mode

```
C-a [          Entrer en copy mode
C-a ]          Coller buffer
C-a =          Choisir buffer à coller
C-a #          Lister tous les buffers

# Dans copy mode:
Space          Commencer sélection
Enter          Copier sélection
q              Quitter copy mode
/              Recherche forward
?              Recherche backward
n              Next résultat
N              Previous résultat
g              Aller au début
G              Aller à la fin
```

### Autres

```
C-a ?          Aide (liste raccourcis)
C-a :          Mode commande
C-a t          Horloge
C-a i          Afficher infos window
C-a r          Forcer redraw
```

## Raccourcis personnalisés recommandés

```bash
# ~/.tmux.conf

# ============================================
# Reload config
# ============================================
bind r source-file ~/.tmux.conf \; display "✅ Config rechargée!"

# ============================================
# Splits intuitifs
# ============================================
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
bind h split-window -h -c "#{pane_current_path}"
bind v split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# ============================================
# Navigation vim-style
# ============================================
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Sans prefix (Alt+hjkl)
bind -n M-h select-pane -L
bind -n M-j select-pane -D
bind -n M-k select-pane -U
bind -n M-l select-pane -R

# ============================================
# Resize vim-style
# ============================================
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Ou avec Ctrl+arrows
bind -r C-Left resize-pane -L 5
bind -r C-Right resize-pane -R 5
bind -r C-Up resize-pane -U 5
bind -r C-Down resize-pane -D 5

# ============================================
# Windows
# ============================================
# Navigation sans prefix
bind -n S-Left previous-window
bind -n S-Right next-window

# Déplacement windows
bind -r < swap-window -t -1\; select-window -t -1
bind -r > swap-window -t +1\; select-window -t +1

# ============================================
# Sessions
# ============================================
bind C-s choose-tree -Zs  # Liste sessions (zoom)
bind C-w choose-tree -Zw  # Liste windows (zoom)

# ============================================
# Copy mode
# ============================================
# Mode vi
setw -g mode-keys vi

# Enter copy mode
bind Escape copy-mode
bind [ copy-mode

# Copy/paste vim-style
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel
bind -T copy-mode-vi C-v send-keys -X rectangle-toggle
bind -T copy-mode-vi Escape send-keys -X cancel

# ============================================
# Synchronize panes
# ============================================
bind S setw synchronize-panes

# ============================================
# Tuer sans confirmation
# ============================================
bind x kill-pane
bind X kill-window

# ============================================
# Join/break panes
# ============================================
bind j command-prompt -p "Join pane from window:" "join-pane -h -s '%%'"
bind b break-pane -d

# ============================================
# Layouts
# ============================================
bind M-1 select-layout even-horizontal
bind M-2 select-layout even-vertical
bind M-3 select-layout main-horizontal
bind M-4 select-layout main-vertical
bind M-5 select-layout tiled

# ============================================
# Autres
# ============================================
# Last window/pane
bind Space last-window
bind Tab last-pane

# Clear history
bind C-l send-keys 'C-l' \; clear-history

# New session
bind N command-prompt -p "New session name:" "new-session -s '%%'"
```

## Copy mode avancé

```bash
# ~/.tmux.conf

# Mode vi
setw -g mode-keys vi

# Bindings copy mode vi
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi V send-keys -X select-line
bind -T copy-mode-vi C-v send-keys -X rectangle-toggle
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel
bind -T copy-mode-vi Escape send-keys -X cancel

# Recherche
bind -T copy-mode-vi / command-prompt -i -p "(search down)" "send -X search-forward-incremental \"%%%\""
bind -T copy-mode-vi ? command-prompt -i -p "(search up)" "send -X search-backward-incremental \"%%%\""

# Navigation
bind -T copy-mode-vi g send-keys -X history-top
bind -T copy-mode-vi G send-keys -X history-bottom
bind -T copy-mode-vi Home send-keys -X start-of-line
bind -T copy-mode-vi End send-keys -X end-of-line

# Copy vers système clipboard
# Linux (xclip)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# macOS
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# WSL
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "clip.exe"

# Mouse copy
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"
```

## Raccourcis sans prefix

```bash
# ~/.tmux.conf

# Navigation panes (Alt+arrows)
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Ou Alt+hjkl
bind -n M-h select-pane -L
bind -n M-j select-pane -D
bind -n M-k select-pane -U
bind -n M-l select-pane -R

# Navigation windows (Shift+arrows)
bind -n S-Left previous-window
bind -n S-Right next-window

# Resize (Alt+Shift+arrows)
bind -n M-S-Left resize-pane -L 5
bind -n M-S-Right resize-pane -R 5
bind -n M-S-Up resize-pane -U 5
bind -n M-S-Down resize-pane -D 5

# Zoom (Alt+z)
bind -n M-z resize-pane -Z

# Copy mode (Alt+[)
bind -n M-[ copy-mode

# ⚠️ Attention: peut interférer avec d'autres applications
```

## Mode commande

```
C-a :          Entrer en mode commande

# Commandes utiles:
:new-window -n name
:split-window -h
:resize-pane -L 10
:setw synchronize-panes on
:kill-session -a
:rename-session newname
:swap-window -s 1 -t 2
:move-window -t session:
```

## Cheatsheet personnalisé

```bash
# ~/.tmux.conf

# Afficher cheatsheet personnalisé
bind ? display-message "
Raccourcis personnalisés:
──────────────────────────
Sessions:
  C-a d       Détacher
  C-a s       Liste
  C-a N       Nouvelle

Windows:
  C-a c       Créer
  C-a ,       Renommer
  S-Left/Right Navigation

Panes:
  C-a |       Split vertical
  C-a -       Split horizontal
  M-hjkl      Navigation
  C-a hjkl    Navigation (alt)
  C-a HJKL    Resize

Copy:
  C-a [       Entrer
  v           Sélection
  y           Copier
"
```

## Raccourcis contextuels

```bash
# ~/.tmux.conf

# Dans root-table (disponible partout)
bind -n F1 display-message "F1 pressé!"

# Dans prefix-table (après prefix)
bind F1 display-message "Prefix+F1 pressé!"

# Dans copy-mode-vi
bind -T copy-mode-vi F1 send-keys -X cancel

# Créer table personnalisée
bind -T mytable x display-message "X dans mytable"
bind m switch-client -T mytable  # Activer la table
```

## Mouse bindings

```bash
# ~/.tmux.conf

set -g mouse on

# Click pane pour sélectionner
# Double-click pour sélectionner mot
# Triple-click pour sélectionner ligne
# Drag pour copier

# Personnaliser mouse
bind -n MouseDown1Pane select-pane -t =\; send-keys -M
bind -n MouseDown1Status select-window -t =
bind -n MouseDrag1Border resize-pane -M
bind -n WheelUpPane if-shell -F -t = "#{mouse_any_flag}" "send-keys -M" "if -Ft= '#{pane_in_mode}' 'send-keys -M' 'copy-mode -e; send-keys -M'"
```

## Templates de bindings

### Développement

```bash
# ~/.tmux.conf

# Dev workflow
bind D source-file ~/.tmux/dev-layout.conf

# ~/.tmux/dev-layout.conf
new-window -n editor "vim"
split-window -h -p 30
split-window -v
select-pane -t 0
```

### Admin

```bash
# Admin workflow
bind A source-file ~/.tmux/admin-layout.conf

# ~/.tmux/admin-layout.conf
new-window -n monitor
split-window -h
select-pane -t 0
send-keys "htop" C-m
select-pane -t 1
send-keys "tail -f /var/log/syslog" C-m
```

## Liste complète des bindings

```bash
# Voir tous les bindings
tmux list-keys

# Bindings d'une table
tmux list-keys -T prefix
tmux list-keys -T copy-mode-vi
tmux list-keys -T root

# Format lisible
tmux list-keys | less

# Rechercher binding
tmux list-keys | grep split
```

## Débugger bindings

```bash
# Mode verbose
tmux -v

# Logs
tmux show-messages

# Tester binding
tmux bind t display-message "Test binding works!"

# Dans tmux
C-a t  # Devrait afficher le message
```

## Anti-patterns

```bash
# ❌ Éviter: conflit avec apps
bind -n C-l send-keys C-l  # Conflit avec clear

# ✅ Mieux: prefix ou autre touche
bind C-l send-keys C-l

# ❌ Éviter: trop de bindings sans prefix
# Peut casser autres apps

# ✅ Mieux: utiliser prefix pour actions tmux
```

## Configuration complète raccourcis

```bash
# ~/.tmux.conf - Raccourcis optimisés

# Prefix
set -g prefix C-a
bind C-a send-prefix
unbind C-b

# Reload
bind r source-file ~/.tmux.conf \; display "✅ Rechargé!"

# Splits
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
unbind '"'
unbind %

# Navigation vim
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

# Sans prefix
bind -n M-h select-pane -L
bind -n M-j select-pane -D
bind -n M-k select-pane -U
bind -n M-l select-pane -R
bind -n S-Left previous-window
bind -n S-Right next-window

# Resize
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5

# Copy mode vi
setw -g mode-keys vi
bind -T copy-mode-vi v send -X begin-selection
bind -T copy-mode-vi y send -X copy-pipe-and-cancel "xclip -selection clipboard"

# Synchronize
bind S setw synchronize-panes

# Sans confirmation
bind x kill-pane
bind X kill-window

# Autres
bind Space last-window
bind Tab last-pane
bind N command-prompt -p "Session:" "new-session -s '%%'"
```

[← Sessions, Windows, Panes](./infos-tmux-03-sessions-windows-panes.md) | [Index](./infos-tmux-00-index.md) | [Personnalisation →](./infos-tmux-05-personnalisation.md)

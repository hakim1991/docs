# 🎨 Personnalisation

[← Raccourcis clavier](./infos-tmux-04-raccourcis-clavier.md) | [Index](./infos-tmux-00-index.md) | [Configuration avancée →](./infos-tmux-06-configuration-avancee.md)

## Status bar

### Position et apparence basique

```bash
# ~/.tmux.conf

# Position (top ou bottom)
set -g status-position bottom
# set -g status-position top

# On/Off
set -g status on

# Intervalle de rafraîchissement (secondes)
set -g status-interval 1

# Justification
set -g status-justify left    # left, centre, right

# Longueur des sections
set -g status-left-length 50
set -g status-right-length 100
```

### Couleurs status bar

```bash
# ~/.tmux.conf

# Style global
set -g status-style bg=black,fg=white

# Status bar gauche
set -g status-left-style bg=blue,fg=white,bold

# Status bar droite
set -g status-right-style bg=green,fg=black

# Couleurs disponibles:
# black, red, green, yellow, blue, magenta, cyan, white
# brightred, brightgreen, brightyellow, etc.
# colour0 à colour255 (palette 256 couleurs)
# #RRGGBB (hex pour true color)
```

### Status bar gauche

```bash
# ~/.tmux.conf

# Simple
set -g status-left "[#S] "

# Avec couleurs
set -g status-left "#[fg=green]#S #[fg=yellow]» "

# Avec icônes et info
set -g status-left "🖥️  #S | #I:#P "

# Session + host
set -g status-left "[#S@#H] "

# Avancé
set -g status-left "#[fg=blue,bold]❐ #S #[fg=yellow]» #[fg=cyan]#I:#P "
```

### Status bar droite

```bash
# ~/.tmux.conf

# Simple date/heure
set -g status-right "%H:%M %d-%b-%y"

# Heure avec secondes
set -g status-right "%H:%M:%S"

# Date complète
set -g status-right "%A %d %B %Y %H:%M"

# Avec user et host
set -g status-right "#(whoami)@#H | %H:%M"

# Load average
set -g status-right "⚡ #(cat /proc/loadavg | cut -d' ' -f1-3) | %H:%M"

# CPU et RAM
set -g status-right "CPU: #(top -bn1 | grep 'Cpu' | awk '{print $2}')% | RAM: #(free -h | awk '/^Mem:/ {print $3}') | %H:%M"

# Batterie (laptop)
set -g status-right "🔋 #(acpi | cut -d',' -f2) | %H:%M"

# Complet
set -g status-right "#[fg=cyan]%A %d-%b #[fg=yellow]%H:%M:%S #[fg=green]#(whoami)@#H"
```

### Window status

```bash
# ~/.tmux.conf

# Window courante
setw -g window-status-current-style bg=red,fg=white,bold

# Window normale
setw -g window-status-style bg=black,fg=white

# Format window status
setw -g window-status-format " #I:#W "
setw -g window-status-current-format " #I:#W "

# Avec icônes
setw -g window-status-format " #I:#{?window_zoomed_flag,🔍,}#W "
setw -g window-status-current-format " #I:#{?window_zoomed_flag,🔍,}#W "

# Separator
setw -g window-status-separator "|"
# setw -g window-status-separator ""

# Activity
setw -g window-status-activity-style fg=yellow,bg=black,bold
setw -g window-status-bell-style fg=red,bg=black,bold
```

### Variables status bar

```bash
# Variables disponibles

#H    Hostname
#h    Hostname sans domaine
#S    Session name
#I    Window index
#P    Pane index
#W    Window name
#T    Pane title
#F    Window flags (*, -, Z, etc.)

# Date/heure (man strftime)
%Y    Année (2024)
%m    Mois (01-12)
%d    Jour (01-31)
%H    Heure (00-23)
%M    Minute (00-59)
%S    Seconde (00-59)
%A    Jour semaine (Monday)
%B    Mois (January)

# Commandes shell
#(command)    Exécuter commande

# Conditionals
#{?condition,true,false}
#{?window_zoomed_flag,Z,}
```

## Thèmes complets

### Thème sombre minimal

```bash
# ~/.tmux.conf - Thème sombre minimal

# ============================================
# Status bar
# ============================================

set -g status-position bottom
set -g status-style bg=colour235,fg=colour248
set -g status-left "#[fg=colour39,bold] #S "
set -g status-right "#[fg=colour248] %H:%M %d-%b "
set -g status-left-length 30
set -g status-right-length 50
set -g status-interval 1

# Window status
setw -g window-status-format " #I:#W "
setw -g window-status-current-format " #I:#W "
setw -g window-status-current-style bg=colour39,fg=colour235,bold
setw -g window-status-style bg=colour235,fg=colour248

# ============================================
# Panes
# ============================================

set -g pane-border-style fg=colour238
set -g pane-active-border-style fg=colour39

# ============================================
# Messages
# ============================================

set -g message-style bg=colour39,fg=colour235,bold
```

### Thème clair

```bash
# ~/.tmux.conf - Thème clair

# ============================================
# Status bar
# ============================================

set -g status-position bottom
set -g status-style bg=colour254,fg=colour237
set -g status-left "#[fg=colour33,bold] #S #[fg=colour245]» "
set -g status-right "#[fg=colour237] #(whoami)@#H | %H:%M "
set -g status-left-length 40
set -g status-right-length 60

# Window status
setw -g window-status-format " #I:#W "
setw -g window-status-current-format " #I:#W "
setw -g window-status-current-style bg=colour33,fg=colour254,bold
setw -g window-status-style bg=colour254,fg=colour237

# ============================================
# Panes
# ============================================

set -g pane-border-style fg=colour250
set -g pane-active-border-style fg=colour33

# ============================================
# Messages
# ============================================

set -g message-style bg=colour33,fg=colour254,bold
```

### Thème Dracula

```bash
# ~/.tmux.conf - Dracula theme

# ============================================
# Colors
# ============================================

# Dracula palette
dracula_bg="#282a36"
dracula_fg="#f8f8f2"
dracula_selection="#44475a"
dracula_comment="#6272a4"
dracula_cyan="#8be9fd"
dracula_green="#50fa7b"
dracula_orange="#ffb86c"
dracula_pink="#ff79c6"
dracula_purple="#bd93f9"
dracula_red="#ff5555"
dracula_yellow="#f1fa8c"

# ============================================
# Status bar
# ============================================

set -g status-style bg=#282a36,fg=#f8f8f2
set -g status-left "#[fg=#282a36,bg=#bd93f9,bold] #S #[fg=#bd93f9,bg=#282a36]"
set -g status-right "#[fg=#8be9fd]#(whoami)#[fg=#f8f8f2]@#[fg=#50fa7b]#H #[fg=#6272a4]| #[fg=#ffb86c]%H:%M #[fg=#6272a4]| #[fg=#ff79c6]%d-%b-%y "
set -g status-left-length 30
set -g status-right-length 80
set -g status-interval 1

# Window status
setw -g window-status-format " #[fg=#f8f8f2]#I:#W "
setw -g window-status-current-format " #[fg=#282a36,bg=#ff79c6,bold]#I:#W "
setw -g window-status-separator ""

# ============================================
# Panes
# ============================================

set -g pane-border-style fg=#6272a4
set -g pane-active-border-style fg=#bd93f9

# ============================================
# Messages
# ============================================

set -g message-style bg=#ff79c6,fg=#282a36,bold
```

### Thème Nord

```bash
# ~/.tmux.conf - Nord theme

# ============================================
# Colors
# ============================================

nord0="#2E3440"
nord1="#3B4252"
nord2="#434C5E"
nord3="#4C566A"
nord4="#D8DEE9"
nord5="#E5E9F0"
nord6="#ECEFF4"
nord7="#8FBCBB"
nord8="#88C0D0"
nord9="#81A1C1"
nord10="#5E81AC"
nord11="#BF616A"
nord12="#D08770"
nord13="#EBCB8B"
nord14="#A3BE8C"
nord15="#B48EAD"

# ============================================
# Status bar
# ============================================

set -g status-style bg=#3B4252,fg=#ECEFF4
set -g status-left "#[fg=#2E3440,bg=#88C0D0,bold] #S #[fg=#88C0D0,bg=#3B4252]"
set -g status-right "#[fg=#88C0D0]%H:%M #[fg=#81A1C1]| #[fg=#A3BE8C]%d-%b "
set -g status-left-length 30
set -g status-right-length 50

# Window status
setw -g window-status-format " #[fg=#D8DEE9]#I:#W "
setw -g window-status-current-format " #[fg=#2E3440,bg=#88C0D0,bold]#I:#W "

# ============================================
# Panes
# ============================================

set -g pane-border-style fg=#4C566A
set -g pane-active-border-style fg=#88C0D0

# ============================================
# Messages
# ============================================

set -g message-style bg=#88C0D0,fg=#2E3440,bold
```

## Panes et bordures

### Bordures simples

```bash
# ~/.tmux.conf

# Bordure pane normale
set -g pane-border-style fg=colour238

# Bordure pane active
set -g pane-active-border-style fg=colour39

# Avec couleur de fond
set -g pane-border-style bg=black,fg=colour238
set -g pane-active-border-style bg=black,fg=colour39

# Style bold
set -g pane-active-border-style fg=colour39,bold
```

### Indicateur pane

```bash
# ~/.tmux.conf

# Afficher numéro pane (C-a q)
set -g display-panes-time 2000
set -g display-panes-colour colour238
set -g display-panes-active-colour colour39

# Augmenter le temps d'affichage
set -g display-panes-time 5000
```

### Titres panes

```bash
# ~/.tmux.conf

# Activer titres
set -g set-titles on

# Format titre
set -g set-titles-string '#S:#I:#W - "#{pane_title}"'

# Titre automatique
set -g automatic-rename on
set -g automatic-rename-format '#{b:pane_current_path}'

# Dans un pane, changer le titre:
# echo -ne "\033]0;My Title\007"
```

## Messages et prompts

### Style messages

```bash
# ~/.tmux.conf

# Message command mode
set -g message-style bg=colour39,fg=colour235,bold

# Message command mode (vi)
set -g message-command-style bg=colour238,fg=colour39

# Durée affichage messages
set -g display-time 4000
```

### Mode command

```bash
# ~/.tmux.conf

# Prompt style
set -g message-style bg=blue,fg=white,bold

# Exemple personnalisé
set -g message-style bg=colour39,fg=colour235,bold,italics
```

## Copy mode

### Style copy mode

```bash
# ~/.tmux.conf

# Selection
setw -g mode-style bg=colour39,fg=colour235

# Recherche
set -g mode-style bg=yellow,fg=black

# Match recherche
setw -g mode-style bg=colour39,fg=colour235,reverse
```

## Clock mode

```bash
# ~/.tmux.conf - Clock (C-a t)

# Couleur clock
setw -g clock-mode-colour colour39

# Style (12h ou 24h)
setw -g clock-mode-style 24
```

## Formats avancés

### Conditions dans formats

```bash
# ~/.tmux.conf

# Window zoomed indicator
setw -g window-status-current-format "#{?window_zoomed_flag,🔍,}#I:#W"

# Pane synchronized indicator
set -g status-left "#{?pane_synchronized,🔗 ,}#S "

# If/else
setw -g window-status-format "#{?window_activity_flag,!,}#I:#W"

# Multiple conditions
set -g status-right "#{?client_prefix,⌨️  ,}#{?pane_synchronized,🔗 ,}%H:%M"
```

### Variables conditionnelles

```bash
# Variables conditionnelles disponibles

window_zoomed_flag         # Pane zoomed
pane_synchronized         # Panes synchronized
client_prefix             # Prefix key pressed
window_activity_flag      # Activity dans window
window_bell_flag          # Bell dans window
window_silence_flag       # Silence dans window
pane_in_mode             # Copy mode actif
```

### Scripts dans status bar

```bash
# ~/.tmux.conf

# Git branch courante
set -g status-right "#(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2) | %H:%M"

# Météo
set -g status-right "#(curl -s 'wttr.in/Paris?format=3') | %H:%M"

# Uptime
set -g status-right "⏱️  #(uptime | awk '{print $3}' | sed 's/,//') | %H:%M"

# IP publique
set -g status-right "🌐 #(curl -s ifconfig.me) | %H:%M"

# Docker containers
set -g status-right "🐳 #(docker ps -q | wc -l) | %H:%M"

# Température CPU
set -g status-right "🌡️  #(sensors | grep 'Package id 0' | awk '{print $4}') | %H:%M"
```

## Configuration complète personnalisée

```bash
# ~/.tmux.conf - Configuration visuelle complète

# ============================================
# GÉNÉRAL
# ============================================

# Couleurs
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"

# ============================================
# STATUS BAR
# ============================================

# Position et style
set -g status-position bottom
set -g status-style bg=colour235,fg=colour248
set -g status-interval 1
set -g status-justify left

# Status left
set -g status-left-length 50
set -g status-left "#[fg=colour235,bg=colour39,bold] #S #[fg=colour39,bg=colour235] #[fg=colour248]#I:#P "

# Status right
set -g status-right-length 100
set -g status-right "#[fg=colour248]#{?client_prefix,⌨️  ,}#{?pane_synchronized,🔗 ,}#[fg=colour39]#(whoami)#[fg=colour248]@#[fg=colour39]#H #[fg=colour238]│ #[fg=colour248]%H:%M:%S #[fg=colour238]│ #[fg=colour248]%d-%b-%y "

# ============================================
# WINDOWS
# ============================================

# Window status
setw -g window-status-format " #[fg=colour248]#I#[fg=colour238]:#[fg=colour248]#W "
setw -g window-status-current-format " #[fg=colour235,bg=colour39,bold]#I#[fg=colour235,bg=colour39]:#[fg=colour235,bg=colour39,bold]#W "
setw -g window-status-separator ""

# Activity
setw -g monitor-activity on
set -g visual-activity off
setw -g window-status-activity-style fg=colour39,bg=colour235,bold

# ============================================
# PANES
# ============================================

# Bordures
set -g pane-border-style fg=colour238
set -g pane-active-border-style fg=colour39

# Numéros panes
set -g display-panes-time 3000
set -g display-panes-colour colour238
set -g display-panes-active-colour colour39

# ============================================
# MESSAGES
# ============================================

set -g message-style bg=colour39,fg=colour235,bold
set -g message-command-style bg=colour238,fg=colour39
set -g display-time 3000

# ============================================
# COPY MODE
# ============================================

setw -g mode-keys vi
setw -g mode-style bg=colour39,fg=colour235

# ============================================
# CLOCK
# ============================================

setw -g clock-mode-colour colour39
setw -g clock-mode-style 24

# ============================================
# AUTRES
# ============================================

# Titres
set -g set-titles on
set -g set-titles-string '#S:#I:#W - "#{pane_title}"'

# Renommage automatique
set -g automatic-rename on
set -g automatic-rename-format '#{b:pane_current_path}'
```

## Powerline-style status bar

```bash
# ~/.tmux.conf - Powerline-style

# Symbols: , , , , ,

# Status bar
set -g status-style bg=colour235,fg=colour248
set -g status-left "#[fg=colour235,bg=colour39,bold] #S #[fg=colour39,bg=colour238]#[fg=colour248,bg=colour238] #I:#P #[fg=colour238,bg=colour235]"
set -g status-right "#[fg=colour238,bg=colour235]#[fg=colour248,bg=colour238] %H:%M:%S #[fg=colour39,bg=colour238]#[fg=colour235,bg=colour39,bold] %d-%b-%y "
set -g status-left-length 50
set -g status-right-length 50

# Windows
setw -g window-status-format " #I:#W "
setw -g window-status-current-format "#[fg=colour235,bg=colour39]#[fg=colour235,bg=colour39,bold] #I:#W #[fg=colour39,bg=colour235]"
setw -g window-status-separator ""
```

## Tester les couleurs

```bash
# Script pour voir palette 256 couleurs
for i in {0..255}; do
    printf "\x1b[38;5;${i}mcolour${i}\x1b[0m\n"
done

# Ou
for i in {0..255}; do
    tmux set -g status-style bg=colour$i,fg=white
    tmux refresh-client -S
    echo "colour$i"
    sleep 0.1
done
```

## Templates prêts à l'emploi

### Minimal Pro

```bash
# ~/.tmux.conf - Minimal Pro

set -g status-style bg=black,fg=white,bold
set -g status-left " #S │ "
set -g status-right " %H:%M "
set -g status-left-length 20
set -g status-right-length 20
setw -g window-status-format " #I:#W "
setw -g window-status-current-format " #I:#W "
setw -g window-status-current-style bg=blue,fg=black,bold
set -g pane-border-style fg=white
set -g pane-active-border-style fg=blue
```

### Dev Complete

```bash
# ~/.tmux.conf - Dev Complete

set -g status-style bg=colour234,fg=colour249
set -g status-left "#[fg=colour234,bg=colour33,bold] #S #[fg=colour33,bg=colour234] #[fg=colour249]#(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2) "
set -g status-right "#[fg=colour249]#(docker ps -q 2>/dev/null | wc -l) 🐳 #[fg=colour238]│ #[fg=colour249]%H:%M:%S "
set -g status-left-length 60
set -g status-right-length 60
setw -g window-status-format " #I:#W#{?window_zoomed_flag, 🔍,} "
setw -g window-status-current-format " #[fg=colour234,bg=colour33,bold]#I:#W#{?window_zoomed_flag, 🔍,} #[fg=colour33,bg=colour234]"
set -g pane-border-style fg=colour238
set -g pane-active-border-style fg=colour33
```

[← Raccourcis clavier](./infos-tmux-04-raccourcis-clavier.md) | [Index](./infos-tmux-00-index.md) | [Configuration avancée →](./infos-tmux-06-configuration-avancee.md)

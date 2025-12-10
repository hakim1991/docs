# 🔌 Plugins et TPM

[← Configuration avancée](./infos-tmux-06-configuration-avancee.md) | [Index](./infos-tmux-00-index.md) | [Scripts et automatisation →](./infos-tmux-08-scripts-automatisation.md)

## Installation TPM

### Tmux Plugin Manager (TPM)

```bash
# Cloner TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Vérifier installation
ls -la ~/.tmux/plugins/tpm
```

### Configuration de base

```bash
# ~/.tmux.conf

# ============================================
# TPM
# ============================================

# Liste des plugins
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# Initialiser TPM (garder à la fin du fichier)
run '~/.tmux/plugins/tpm/tpm'
```

### Utilisation TPM

```bash
# Dans tmux:

# Installer plugins
C-a I               # (I majuscule)

# Mettre à jour plugins
C-a U

# Supprimer plugins non listés
C-a M-u

# Depuis le shell:
~/.tmux/plugins/tpm/bin/install_plugins
~/.tmux/plugins/tpm/bin/update_plugins all
~/.tmux/plugins/tpm/bin/clean_plugins
```

## Plugins essentiels

### tmux-sensible

Configuration par défaut raisonnable

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-sensible'

# Inclut:
# - utf8 support
# - historique 50000
# - escape-time 0
# - focus-events on
# - aggressive-resize on
# - etc.
```

### tmux-resurrect

Sauvegarder/restaurer sessions

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-resurrect'

# Sauvegarder session
C-a C-s

# Restaurer session
C-a C-r

# Options
set -g @resurrect-save 'S'
set -g @resurrect-restore 'R'

# Capturer contenu panes
set -g @resurrect-capture-pane-contents 'on'

# Stratégie pour vim/neovim
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-strategy-nvim 'session'

# Processus à restaurer
set -g @resurrect-processes 'ssh psql mysql'
```

### tmux-continuum

Auto-save/restore automatique

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-continuum'

# Auto-save toutes les 15 minutes
set -g @continuum-save-interval '15'

# Auto-restore au démarrage
set -g @continuum-restore 'on'

# Boot automatique tmux
set -g @continuum-boot 'on'

# Boot dans iterm (macOS)
set -g @continuum-boot-options 'iterm'

# Status de sauvegarde
set -g status-right 'Continuum: #{continuum_status}'
```

### tmux-yank

Copier vers clipboard système

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-yank'

# Copy mode
# y - copie sélection
# Y - copie ligne courante
# (normal mode) y - copie texte de ligne de commande

# Options
set -g @yank_selection 'primary'      # ou 'clipboard', 'secondary'
set -g @yank_selection_mouse 'clipboard'

# Action après copy
set -g @yank_action 'copy-pipe-and-cancel'  # ou 'copy-pipe'

# Custom command
set -g @override_copy_command 'my-clipboard-command'
```

### tmux-copycat

Recherche améliorée

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-copycat'

# Raccourcis en copy mode:
# C-f - recherche fichier
# C-g - recherche git status
# C-u - recherche url
# C-d - recherche nombre
# C-h - recherche hash (sha)
# M-i - recherche IP

# Custom searches
set -g @copycat_search_C-p '\d{4}-\d{2}-\d{2}'  # dates
set -g @copycat_search_C-e '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # email
```

### tmux-open

Ouvrir fichiers/URLs

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-open'

# En copy mode:
# o - ouvrir sélection avec $EDITOR
# C-o - ouvrir avec open/xdg-open
# S - rechercher sélection avec search engine

# Options
set -g @open-S 'https://www.google.com/search?q='
set -g @open-editor-command 'vim'
```

### tmux-fzf

Intégration fzf

```bash
# ~/.tmux.conf
set -g @plugin 'sainnhe/tmux-fzf'

# Utilisation
C-a F               # Ouvrir menu fzf

# Options disponibles:
# - session
# - window
# - pane
# - command
# - keybinding
# - clipboard
# - process

# Binding personnalisé
set -g @tmux-fzf-launch-key 'C-f'
```

### tmux-prefix-highlight

Indicateur prefix

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-prefix-highlight'

# Afficher dans status bar
set -g status-right '#{prefix_highlight} | %a %Y-%m-%d %H:%M'

# Options
set -g @prefix_highlight_fg 'white'
set -g @prefix_highlight_bg 'blue'

# Indicateur copy mode
set -g @prefix_highlight_show_copy_mode 'on'
set -g @prefix_highlight_copy_mode_attr 'fg=black,bg=yellow,bold'

# Indicateur sync mode
set -g @prefix_highlight_show_sync_mode 'on'
set -g @prefix_highlight_sync_mode_attr 'fg=black,bg=green'
```

## Plugins navigation

### tmux-pain-control

Navigation et redimensionnement améliorés

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-pain-control'

# Navigation panes (avec prefix):
# h, j, k, l - navigation vim-style
# H, J, K, L - resize
# < > - swap panes
# | - split horizontal
# - - split vertical
```

### vim-tmux-navigator

Navigation seamless vim/tmux

```bash
# ~/.tmux.conf
set -g @plugin 'christoomey/vim-tmux-navigator'

# Navigation sans prefix:
# C-h - gauche
# C-j - bas
# C-k - haut
# C-l - droite
# C-\ - dernier pane

# Désactiver wrapping
set -g @plugin 'christoomey/vim-tmux-navigator'
```

### tmux-fingers

Copie rapide avec hints

```bash
# ~/.tmux.conf
set -g @plugin 'Morantron/tmux-fingers'

# Utilisation
C-a F               # Activer fingers mode

# Affiche hints sur texte (paths, urls, IPs, etc.)
# Taper hint pour copier

# Options
set -g @fingers-key F
set -g @fingers-pattern-0 'git rebase -i ([0-9a-f]{7,40})'
```

## Plugins apparence

### tmux-powerline

Status bar powerline-style

```bash
# ~/.tmux.conf
set -g @plugin 'erikw/tmux-powerline'

# Configuration
set -g @tmux-powerline-date-format "%d %b"
set -g @tmux-powerline-time-format "%H:%M"

# Segments disponibles:
# - battery
# - cpu
# - date
# - earthquake
# - hostname
# - lan_ip
# - load
# - mailcount
# - now_playing
# - pwd
# - time
# - tmux_mem_cpu_load
# - uptime
# - vcs_branch
# - wan_ip
# - weather
```

### dracula/tmux

Thème Dracula

```bash
# ~/.tmux.conf
set -g @plugin 'dracula/tmux'

# Options
set -g @dracula-show-battery false
set -g @dracula-show-network false
set -g @dracula-show-weather false
set -g @dracula-show-time true
set -g @dracula-show-location false
set -g @dracula-military-time true
set -g @dracula-show-left-icon session
set -g @dracula-border-contrast true

# Plugins disponibles:
set -g @dracula-plugins "cpu-usage ram-usage time"
```

### nord-tmux

Thème Nord

```bash
# ~/.tmux.conf
set -g @plugin "arcticicestudio/nord-tmux"

# Pas d'options, applique thème Nord automatiquement
```

## Plugins utilitaires

### tmux-sessionist

Gestion sessions améliorée

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-sessionist'

# Raccourcis:
C-a g               # Prompts pour switch session
C-a C               # Créer nouvelle session
C-a X               # Tuer session courante sans détacher
C-a S               # Switch à dernière session
C-a @               # Promouvoir pane en nouvelle session
```

### tmux-sidebar

Explorateur fichiers sidebar

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-sidebar'

# Raccourcis:
C-a Tab             # Toggle sidebar
C-a Backspace       # Toggle sidebar et focus

# Options
set -g @sidebar-tree-command 'tree -C'
set -g @sidebar-tree-width '40'
```

### tmux-logging

Logging panes et output

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-logging'

# Raccourcis:
C-a P               # Toggle logging pane
C-a M-p             # Capture pane (screenshot)
C-a M-P             # Capture pane avec historique
C-a M-c             # Clear historique pane

# Options
set -g @logging-path "$HOME/tmux-logs"
set -g @logging-filename "tmux-#{session_name}-#{window_index}-#{pane_index}-%Y%m%d-%H%M%S.log"
set -g @screen-capture-path "$HOME/tmux-logs"
set -g @save-complete-history-path "$HOME/tmux-logs"
```

### tmux-urlview

Extraire et ouvrir URLs

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-urlview'

# Nécessite: urlview
sudo apt install urlview

# Utilisation:
C-a u               # Lister toutes les URLs du pane

# Ou avec fzf (plus moderne):
# Alternative: tmux-fzf-url
set -g @plugin 'wfxr/tmux-fzf-url'
C-a u               # Ouvrir URLs avec fzf
```

### tmux-menus

Menus contextuels

```bash
# ~/.tmux.conf
set -g @plugin 'jaclu/tmux-menus'

# Raccourcis:
C-a <               # Main menu
C-a >               # Help menu
C-a ^               # Advanced menu

# Menus disponibles:
# - Sessions
# - Windows
# - Panes
# - Layouts
# - Help
```

## Configuration TPM complète

### Exemple minimal

```bash
# ~/.tmux.conf

# ============================================
# TPM Plugins
# ============================================

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-yank'

# ============================================
# Plugins config
# ============================================

# Resurrect
set -g @resurrect-capture-pane-contents 'on'

# ============================================
# TPM init
# ============================================

run '~/.tmux/plugins/tpm/tpm'
```

### Exemple développeur

```bash
# ~/.tmux.conf

# ============================================
# TPM Plugins
# ============================================

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @plugin 'tmux-plugins/tmux-copycat'
set -g @plugin 'tmux-plugins/tmux-open'
set -g @plugin 'christoomey/vim-tmux-navigator'
set -g @plugin 'tmux-plugins/tmux-prefix-highlight'
set -g @plugin 'sainnhe/tmux-fzf'

# ============================================
# Config plugins
# ============================================

# Resurrect + Continuum
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-nvim 'session'
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'

# Yank
set -g @yank_selection_mouse 'clipboard'

# Prefix highlight
set -g @prefix_highlight_show_copy_mode 'on'
set -g @prefix_highlight_show_sync_mode 'on'

# Status bar avec prefix highlight
set -g status-right '#{prefix_highlight} | #{continuum_status} | %H:%M'

# ============================================
# TPM init
# ============================================

run '~/.tmux/plugins/tpm/tpm'
```

### Exemple complet avec thème

```bash
# ~/.tmux.conf

# ============================================
# Base config
# ============================================

set -g prefix C-a
set -g mouse on
set -g base-index 1
setw -g pane-base-index 1
setw -g mode-keys vi

# ============================================
# TPM Plugins
# ============================================

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# Session management
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'tmux-plugins/tmux-sessionist'

# Copy/paste
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @plugin 'tmux-plugins/tmux-copycat'
set -g @plugin 'tmux-plugins/tmux-open'

# Navigation
set -g @plugin 'christoomey/vim-tmux-navigator'
set -g @plugin 'tmux-plugins/tmux-pain-control'

# Utilitaires
set -g @plugin 'sainnhe/tmux-fzf'
set -g @plugin 'tmux-plugins/tmux-logging'
set -g @plugin 'wfxr/tmux-fzf-url'

# Apparence
set -g @plugin 'tmux-plugins/tmux-prefix-highlight'
set -g @plugin 'dracula/tmux'

# ============================================
# Config plugins
# ============================================

# Resurrect + Continuum
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-strategy-nvim 'session'
set -g @resurrect-processes 'ssh psql mysql npm'
set -g @continuum-restore 'on'
set -g @continuum-save-interval '15'

# Yank
set -g @yank_selection_mouse 'clipboard'
set -g @yank_action 'copy-pipe-and-cancel'

# Copycat
set -g @copycat_search_C-e '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Dracula theme
set -g @dracula-show-battery true
set -g @dracula-show-network false
set -g @dracula-show-weather false
set -g @dracula-military-time true
set -g @dracula-plugins "cpu-usage ram-usage"
set -g @dracula-show-left-icon session

# Prefix highlight
set -g @prefix_highlight_show_copy_mode 'on'
set -g @prefix_highlight_show_sync_mode 'on'
set -g @prefix_highlight_copy_mode_attr 'fg=black,bg=yellow,bold'
set -g @prefix_highlight_sync_mode_attr 'fg=black,bg=green'

# FZF
set -g @tmux-fzf-launch-key 'C-f'

# Logging
set -g @logging-path "$HOME/tmux-logs"

# ============================================
# TPM init (à la fin)
# ============================================

run '~/.tmux/plugins/tpm/tpm'
```

## Créer un plugin

### Structure basique

```bash
# Créer répertoire plugin
mkdir -p ~/my-tmux-plugin

# Structure:
my-tmux-plugin/
├── my-plugin.tmux       # Script principal
├── scripts/
│   └── helper.sh
└── README.md
```

### Script principal

```bash
#!/usr/bin/env bash
# my-plugin.tmux

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Obtenir options
get_tmux_option() {
    local option=$1
    local default_value=$2
    local option_value=$(tmux show-option -gqv "$option")
    if [ -z "$option_value" ]; then
        echo "$default_value"
    else
        echo "$option_value"
    fi
}

# Configuration
MY_OPTION=$(get_tmux_option "@my-plugin-option" "default")

# Main function
main() {
    # Ajouter keybinding
    tmux bind-key M-m run-shell "$CURRENT_DIR/scripts/helper.sh"

    # Modifier status bar
    local status_right=$(tmux show-option -gv status-right)
    tmux set-option -g status-right "$status_right #($CURRENT_DIR/scripts/status.sh)"
}

main
```

### Script helper

```bash
#!/usr/bin/env bash
# scripts/helper.sh

# Fonctionnalité du plugin
echo "My plugin action!"
tmux display-message "Plugin activé!"
```

### Utilisation

```bash
# ~/.tmux.conf
set -g @plugin 'username/my-tmux-plugin'

# Ou en local pour développement:
run-shell ~/my-tmux-plugin/my-plugin.tmux
```

## Troubleshooting plugins

### Problèmes courants

```bash
# TPM ne fonctionne pas
# Vérifier installation
ls -la ~/.tmux/plugins/tpm

# Réinstaller TPM
rm -rf ~/.tmux/plugins/tpm
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Plugins pas installés
# Dans tmux:
C-a I

# Ou manuellement:
~/.tmux/plugins/tpm/bin/install_plugins

# Plugin ne charge pas
# Vérifier ordre dans .tmux.conf
# TPM init doit être À LA FIN

# Voir logs
tmux show-messages

# Mode verbose
tmux -v
```

### Debug plugins

```bash
# Tester plugin individuellement
run-shell ~/.tmux/plugins/nom-plugin/nom-plugin.tmux

# Vérifier options plugin
tmux show-options -g | grep @plugin

# Recharger plugins
C-a U

# Logs TPM
cat ~/.tmux/plugins/tpm/tpm.log
```

[← Configuration avancée](./infos-tmux-06-configuration-avancee.md) | [Index](./infos-tmux-00-index.md) | [Scripts et automatisation →](./infos-tmux-08-scripts-automatisation.md)

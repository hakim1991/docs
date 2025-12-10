# 🔧 Troubleshooting

[← Cas pratiques](./infos-tmux-10-cas-pratiques.md) | [Index](./infos-tmux-00-index.md)

## Problèmes courants

### Tmux ne démarre pas

```bash
# Erreur: command not found
which tmux

# Si pas installé
sudo apt install tmux          # Ubuntu/Debian
sudo yum install tmux          # CentOS/RHEL
brew install tmux              # macOS

# Vérifier version
tmux -V

# Vérifier PATH
echo $PATH

# Réinstaller si nécessaire
sudo apt reinstall tmux
```

### Impossible d'attacher à une session

```bash
# Lister sessions
tmux ls

# Erreur: no server running
# Créer nouvelle session
tmux new -s test

# Erreur: session not found
tmux ls                        # Vérifier nom exact

# Erreur: sessions should be nested with care
# Déjà dans tmux, détacher d'abord
C-a d

# Forcer attacher
tmux attach -d -t session      # Détacher autres clients
```

### Sessions perdues après reboot

```bash
# Les sessions tmux ne survivent pas au reboot

# Solution 1: tmux-resurrect
set -g @plugin 'tmux-plugins/tmux-resurrect'

# Solution 2: tmux-continuum
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'

# Solution 3: Script de sauvegarde
# Voir section Scripts ci-dessous
```

### Prefix key ne fonctionne pas

```bash
# Vérifier prefix actuel
tmux show-options -g prefix

# Changer prefix
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# Recharger config
tmux source-file ~/.tmux.conf

# Ou créer nouvelle session pour tester
tmux kill-server
tmux new -s test
```

## Problèmes d'affichage

### Couleurs incorrectes

```bash
# ~/.tmux.conf

# 256 couleurs
set -g default-terminal "screen-256color"

# True color support
set -ga terminal-overrides ",xterm-256color:Tc"

# Tester couleurs
# Script pour voir palette
for i in {0..255}; do
    printf "\x1b[38;5;${i}mcolour${i}\x1b[0m\n"
done
```

```bash
# ~/.bashrc ou ~/.zshrc

# Variable TERM
export TERM=xterm-256color

# Dans tmux
if [ -n "$TMUX" ]; then
    export TERM=screen-256color
fi
```

### Caractères bizarres / corruption affichage

```bash
# Reset display
C-a :
clear-history

# Ou
reset

# Forcer redraw
C-a r                          # Si binding configuré

# Tuer et recréer pane
exit
C-a c

# Problème de locale
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Dans .tmux.conf
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"
```

### Bordures cassées

```bash
# ~/.tmux.conf

# Utiliser caractères ASCII simples
set -g pane-border-status off
set -g pane-border-style fg=white
set -g pane-active-border-style fg=blue

# Ou Unicode explicit
set -as terminal-overrides ',*:U8=0'

# Vérifier locale
locale
# Doit avoir UTF-8

# Fixer locale
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

## Problèmes de performance

### Tmux lent / lag

```bash
# ~/.tmux.conf

# Réduire status interval
set -g status-interval 5       # Au lieu de 1

# Désactiver scripts lourds dans status bar
# Avant:
# set -g status-right "#(heavy-script.sh)"
# Après:
set -g status-right "%H:%M"

# Limiter historique
set -g history-limit 10000     # Au lieu de 50000

# Désactiver monitoring
setw -g monitor-activity off
set -g visual-activity off

# Aggressive resize
setw -g aggressive-resize on
```

### Copy mode lent

```bash
# ~/.tmux.conf

# Réduire historique
set -g history-limit 5000

# Désactiver wrap search
setw -g wrap-search off

# Mode keys vi (plus rapide)
setw -g mode-keys vi
```

### Resize lent

```bash
# ~/.tmux.conf

# Aggressive resize
setw -g aggressive-resize on

# Increase repeat time
set -g repeat-time 1000

# Disable mouse temporairement
set -g mouse off
```

## Problèmes de souris

### Souris ne fonctionne pas

```bash
# ~/.tmux.conf

# Activer souris
set -g mouse on

# Vérifier version tmux
tmux -V
# Si < 2.1, syntaxe différente:
set -g mode-mouse on
set -g mouse-resize-pane on
set -g mouse-select-pane on
set -g mouse-select-window on

# Recharger config
tmux source-file ~/.tmux.conf

# Tester dans nouvelle session
tmux kill-server
tmux
```

### Souris sélectionne mais ne copie pas

```bash
# ~/.tmux.conf

# Linux (xclip)
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# macOS
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "pbcopy"

# WSL
bind -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "clip.exe"

# Ou plugin tmux-yank
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @yank_selection_mouse 'clipboard'
```

### Scroll ne fonctionne pas

```bash
# ~/.tmux.conf

# Activer mouse
set -g mouse on

# Bind wheel up/down
bind -n WheelUpPane if-shell -F -t = "#{mouse_any_flag}" "send-keys -M" "if -Ft= '#{pane_in_mode}' 'send-keys -M' 'copy-mode -e; send-keys -M'"
bind -n WheelDownPane select-pane -t= \; send-keys -M

# Dans terminal, vérifier que terminal supporte mouse
# iTerm2: Preferences > Profiles > Terminal > Report mouse events
# Alacritty: Déjà supporté
```

## Problèmes de copier/coller

### Copy ne fonctionne pas

```bash
# ~/.tmux.conf

# Mode vi
setw -g mode-keys vi

# Bindings copy mode
bind -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-selection-and-cancel

# Vers clipboard système
# Linux
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# macOS
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# WSL
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "clip.exe"

# Ou plugin
set -g @plugin 'tmux-plugins/tmux-yank'
```

### Paste ne fonctionne pas

```bash
# Vérifier buffer tmux
tmux list-buffers

# Coller buffer tmux
C-a ]

# Vérifier binding
tmux list-keys | grep paste

# Paste depuis système
# Linux
C-a : run "xclip -o -selection clipboard | tmux load-buffer - ; tmux paste-buffer"

# macOS
C-a : run "pbpaste | tmux load-buffer - ; tmux paste-buffer"
```

### Clipboard entre SSH sessions

```bash
# Sur machine locale: ~/.ssh/config
Host *
    ForwardX11 yes
    ForwardX11Trusted yes

# Sur serveur distant
# Installer xclip
sudo apt install xclip

# Test X11 forwarding
echo $DISPLAY
# Doit afficher: localhost:10.0 ou similaire

# Si pas de X11, utiliser OSC 52
# ~/.tmux.conf
set -g set-clipboard on
```

## Problèmes de plugins

### TPM ne fonctionne pas

```bash
# Vérifier installation TPM
ls -la ~/.tmux/plugins/tpm

# Réinstaller TPM
rm -rf ~/.tmux/plugins/tpm
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# Vérifier .tmux.conf
# Doit avoir à la fin:
run '~/.tmux/plugins/tpm/tpm'

# Recharger tmux
tmux source-file ~/.tmux.conf

# Installer plugins
C-a I

# Debug
tmux show-messages
cat ~/.tmux/plugins/tpm/*.log
```

### Plugins ne se chargent pas

```bash
# Vérifier ordre dans .tmux.conf
# TPM init DOIT être À LA FIN

# Mauvais:
run '~/.tmux/plugins/tpm/tpm'
set -g status-right "..."

# Bon:
set -g status-right "..."
run '~/.tmux/plugins/tpm/tpm'

# Vérifier syntaxe plugins
set -g @plugin 'tmux-plugins/tmux-sensible'  # Bon
set -g @plugin tmux-plugins/tmux-sensible    # Mauvais (manque quotes)

# Installer manuellement
~/.tmux/plugins/tpm/bin/install_plugins

# Voir logs
tmux show-messages
```

### Plugin spécifique ne fonctionne pas

```bash
# Tester plugin individuellement
run-shell ~/.tmux/plugins/nom-plugin/nom-plugin.tmux

# Vérifier dépendances
# Example: tmux-yank nécessite xclip/pbcopy/clip.exe

# Vérifier options plugin
tmux show-options -g | grep @

# Désactiver temporairement
# Commenter dans .tmux.conf
# set -g @plugin 'problematic-plugin'

# Recharger et tester
tmux source-file ~/.tmux.conf
```

## Problèmes de configuration

### Config non appliquée

```bash
# Recharger config
tmux source-file ~/.tmux.conf

# Vérifier syntaxe
tmux source-file ~/.tmux.conf
# Si erreur, elle sera affichée

# Créer nouvelle session pour tester
tmux new -s test

# Vérifier options
tmux show-options -g         # Options globales
tmux show-options -w         # Options window

# Tester config minimale
# Renommer .tmux.conf
mv ~/.tmux.conf ~/.tmux.conf.bak

# Créer config minimale
echo "set -g mouse on" > ~/.tmux.conf

# Tester
tmux kill-server
tmux

# Restaurer
mv ~/.tmux.conf.bak ~/.tmux.conf
```

### Bindings ne marchent pas

```bash
# Lister tous les bindings
tmux list-keys

# Lister bindings specifiques
tmux list-keys | grep split

# Tester binding
tmux bind t display-message "Test works!"
# Puis: C-a t

# Unbind avant rebind
unbind C-c
bind C-c new-window

# Vérifier prefix
tmux show-options -g prefix

# Debug mode
tmux -v
# Puis utiliser binding et vérifier logs
tmux show-messages
```

## Problèmes Vim

### Escape key delay

```bash
# ~/.tmux.conf
set -s escape-time 0

# ~/.vimrc
set timeoutlen=1000
set ttimeoutlen=0
```

### Couleurs vim incorrectes

```bash
# ~/.vimrc
if exists('+termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

# ~/.tmux.conf
set -g default-terminal "screen-256color"
set -ga terminal-overrides ",xterm-256color:Tc"
```

### Navigation vim/tmux

```bash
# Installer plugin
# ~/.tmux.conf
set -g @plugin 'christoomey/vim-tmux-navigator'

# ~/.vimrc
Plug 'christoomey/vim-tmux-navigator'

# Si ne fonctionne pas, vérifier:
ps -o state= -o comm= -t '#{pane_tty}' | grep -iqE '^[^TXZ ]+ +(\\S+\\/)?g?(view|n?vim?x?)(diff)?$'
```

## Problèmes SSH

### Session tmux perdue après déconnexion SSH

```bash
# Normal: tmux continue en background

# Reconnecter
ssh user@server
tmux attach

# Si "no sessions"
# Session a été tuée, vérifier:
# - Serveur rebooté?
# - Tmux server tué?
# - Timeout SSH?

# Utiliser resurrect pour sauvegarder
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
```

### SSH agent forwarding

```bash
# ~/.tmux.conf
set -g update-environment "SSH_AUTH_SOCK SSH_CONNECTION"

# ~/.bashrc
if [ ! -z "$SSH_AUTH_SOCK" ] && [ "$SSH_AUTH_SOCK" != "$HOME/.ssh/ssh_auth_sock" ]; then
    ln -sf $SSH_AUTH_SOCK ~/.ssh/ssh_auth_sock
    export SSH_AUTH_SOCK=~/.ssh/ssh_auth_sock
fi

# Test
ssh-add -l
```

## Messages d'erreur

### "protocol version mismatch"

```bash
# Versions client/serveur différentes

# Vérifier version
tmux -V

# Tuer serveur
tmux kill-server

# Redémarrer avec bonne version
/usr/local/bin/tmux new
```

### "lost server"

```bash
# Serveur tmux crashé

# Vérifier logs
tmux show-messages

# Redémarrer
tmux new -s recovery

# Vérifier core dumps
ls /tmp/tmux-*/
dmesg | grep tmux
```

### "no current client"

```bash
# Commande exécutée hors tmux

# Vérifier
echo $TMUX

# Attacher d'abord
tmux attach

# Ou exécuter depuis tmux
tmux send-keys -t session:window "command" C-m
```

## Debug avancé

### Mode verbose

```bash
# Démarrer en mode verbose
tmux -v

# Voir logs
tmux show-messages

# Logs dans fichier
tmux -vv 2> tmux-debug.log
```

### Profiling

```bash
# Identifier ralentissements

# Temps de démarrage
time tmux new -d -s test

# Status bar
# Commenter scripts dans status-right
# set -g status-right ""

# Historique
# Réduire
set -g history-limit 1000

# Monitor
htop
# Chercher processus tmux
```

### Socket inspection

```bash
# Lister sockets
ls -la /tmp/tmux-*/

# Permissions
chmod 700 /tmp/tmux-$(id -u)

# Nettoyer sockets morts
tmux kill-server
rm -rf /tmp/tmux-*
```

## Scripts de diagnostic

### Check script

```bash
#!/bin/bash
# tmux-check.sh

echo "=== Tmux Diagnostic ==="
echo

echo "Version:"
tmux -V

echo
echo "Sessions:"
tmux ls 2>&1

echo
echo "Config file:"
if [ -f ~/.tmux.conf ]; then
    echo "~/.tmux.conf exists"
    echo "Lines: $(wc -l < ~/.tmux.conf)"
else
    echo "~/.tmux.conf NOT FOUND"
fi

echo
echo "Plugins:"
if [ -d ~/.tmux/plugins/tpm ]; then
    echo "TPM installed"
    ls -1 ~/.tmux/plugins/
else
    echo "TPM NOT installed"
fi

echo
echo "Environment:"
echo "TERM=$TERM"
echo "TMUX=$TMUX"
echo "SHELL=$SHELL"

echo
echo "Dependencies:"
command -v xclip >/dev/null && echo "xclip: installed" || echo "xclip: NOT installed"
command -v vim >/dev/null && echo "vim: installed" || echo "vim: NOT installed"

echo
echo "Recent messages:"
tmux show-messages 2>&1 | tail -10
```

### Reset script

```bash
#!/bin/bash
# tmux-reset.sh

echo "Resetting tmux..."

# Backup config
if [ -f ~/.tmux.conf ]; then
    cp ~/.tmux.conf ~/.tmux.conf.backup.$(date +%Y%m%d%H%M%S)
    echo "Config backed up"
fi

# Kill server
tmux kill-server 2>/dev/null
echo "Server killed"

# Clean sockets
rm -rf /tmp/tmux-* 2>/dev/null
echo "Sockets cleaned"

# Start fresh
tmux new -s reset
```

## Ressources

### Documentation

```bash
# Man page
man tmux

# Liste commandes
tmux list-commands

# Aide dans tmux
C-a ?

# Options
man tmux | grep -A 10 "^OPTIONS"

# Exemples
man tmux | grep -A 5 "^EXAMPLES"
```

### Liens utiles

```
Official:
- https://github.com/tmux/tmux
- https://github.com/tmux/tmux/wiki

Guides:
- https://tmuxcheatsheet.com/
- https://leanpub.com/the-tao-of-tmux

Communauté:
- r/tmux
- #tmux sur IRC (Libera.Chat)
- Stack Overflow [tmux] tag

Plugins:
- https://github.com/tmux-plugins
```

### Getting help

```bash
# GitHub Issues
https://github.com/tmux/tmux/issues

# Informations pour bug report:
tmux -V
uname -a
echo $TERM
tmux show-options -g
tmux list-keys

# Reproduire avec config minimal
tmux -f /dev/null new
```

[← Cas pratiques](./infos-tmux-10-cas-pratiques.md) | [Index](./infos-tmux-00-index.md)

# 🔗 Intégration

[← Scripts et automatisation](./infos-tmux-08-scripts-automatisation.md) | [Index](./infos-tmux-00-index.md) | [Cas pratiques →](./infos-tmux-10-cas-pratiques.md)

## Vim / Neovim

### Navigation tmux-vim seamless

#### vim-tmux-navigator

```bash
# ~/.tmux.conf

# Plugin
set -g @plugin 'christoomey/vim-tmux-navigator'

# Smart pane switching avec awareness de vim splits
is_vim="ps -o state= -o comm= -t '#{pane_tty}' \
    | grep -iqE '^[^TXZ ]+ +(\\S+\\/)?g?(view|n?vim?x?)(diff)?$'"

bind-key -n 'C-h' if-shell "$is_vim" 'send-keys C-h'  'select-pane -L'
bind-key -n 'C-j' if-shell "$is_vim" 'send-keys C-j'  'select-pane -D'
bind-key -n 'C-k' if-shell "$is_vim" 'send-keys C-k'  'select-pane -U'
bind-key -n 'C-l' if-shell "$is_vim" 'send-keys C-l'  'select-pane -R'

# Copy mode
bind-key -T copy-mode-vi 'C-h' select-pane -L
bind-key -T copy-mode-vi 'C-j' select-pane -D
bind-key -T copy-mode-vi 'C-k' select-pane -U
bind-key -T copy-mode-vi 'C-l' select-pane -R
```

```vim
" ~/.vimrc ou ~/.config/nvim/init.vim

" Plugin vim-tmux-navigator
Plug 'christoomey/vim-tmux-navigator'

" Navigation C-h/j/k/l fonctionne entre vim splits et tmux panes
```

### Vim settings pour tmux

```vim
" ~/.vimrc

" Fix delay ESC dans tmux
set timeoutlen=1000
set ttimeoutlen=0

" True color support
if exists('+termguicolors')
  let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
  let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  set termguicolors
endif

" Background color erase (pour tmux)
set t_ut=

" Cursor shape dans tmux
if exists('$TMUX')
  let &t_SI = "\<Esc>Ptmux;\<Esc>\e[5 q\<Esc>\\"
  let &t_EI = "\<Esc>Ptmux;\<Esc>\e[2 q\<Esc>\\"
else
  let &t_SI = "\e[5 q"
  let &t_EI = "\e[2 q"
endif

" Focus events
set autoread
au FocusGained,BufEnter * :checktime

" Clipboard (nécessite tmux 2.6+)
set clipboard=unnamed
```

### Neovim configuration

```lua
-- ~/.config/nvim/init.lua

-- Tmux navigator
vim.g.tmux_navigator_no_mappings = 1
vim.keymap.set('n', '<C-h>', ':TmuxNavigateLeft<CR>', {silent = true})
vim.keymap.set('n', '<C-j>', ':TmuxNavigateDown<CR>', {silent = true})
vim.keymap.set('n', '<C-k>', ':TmuxNavigateUp<CR>', {silent = true})
vim.keymap.set('n', '<C-l>', ':TmuxNavigateRight<CR>', {silent = true})

-- True color
vim.opt.termguicolors = true

-- Focus events
vim.opt.autoread = true
vim.api.nvim_create_autocmd({'FocusGained', 'BufEnter'}, {
  pattern = '*',
  command = 'checktime'
})
```

### Ouvrir vim dans nouveau pane

```bash
# ~/.tmux.conf

# Ouvrir fichier dans split vertical
bind v command-prompt -p "File:" "split-window -h 'vim %1'"

# Ouvrir fichier dans split horizontal
bind s command-prompt -p "File:" "split-window -v 'vim %1'"
```

### Sessions vim persistantes

```vim
" ~/.vimrc

" Sauvegarder session vim au exit
autocmd VimLeave * mksession! ~/.vim-session.vim

" Restaurer avec :source ~/.vim-session.vim
```

```bash
# ~/.tmux.conf

# Config resurrect pour vim
set -g @resurrect-strategy-vim 'session'
set -g @resurrect-strategy-nvim 'session'
```

## SSH

### SSH agent forwarding

```bash
# ~/.tmux.conf

# Garder SSH agent entre reconnexions
set -g update-environment "DISPLAY SSH_ASKPASS SSH_AGENT_PID SSH_CONNECTION WINDOWID XAUTHORITY"

# Script pour update SSH_AUTH_SOCK
set-environment -g 'SSH_AUTH_SOCK' ~/.ssh/ssh_auth_sock
```

```bash
# ~/.bashrc

# Lien symbolique SSH_AUTH_SOCK
if [ ! -z "$SSH_AUTH_SOCK" ] && [ "$SSH_AUTH_SOCK" != "$HOME/.ssh/ssh_auth_sock" ]; then
    ln -sf $SSH_AUTH_SOCK ~/.ssh/ssh_auth_sock
fi
```

### Titre SSH dans status bar

```bash
# ~/.tmux.conf

# Afficher hostname SSH
set -g status-right "#H | %H:%M"

# Ou avec couleur différente si SSH
set -g status-right "#{?SSH_CONNECTION,🔒 #H,#H} | %H:%M"
```

### Session SSH persistante

```bash
# Sur serveur distant
ssh user@server

# Dans le serveur
tmux new -s work

# Travailler...
# Si déconnexion SSH, session continue

# Reconnecter
ssh user@server
tmux attach -t work
```

### Script SSH multi-serveurs

```bash
#!/bin/bash
# ssh-tmux-multi.sh

SESSION="ssh-servers"
SERVERS=("web1" "web2" "db1" "db2")

# Créer session
tmux new-session -d -s $SESSION

# Premier serveur
tmux send-keys -t $SESSION "ssh ${SERVERS[0]}" C-m

# Autres serveurs
for i in "${!SERVERS[@]}"; do
    if [ $i -ne 0 ]; then
        tmux split-window -t $SESSION
        tmux send-keys -t $SESSION "ssh ${SERVERS[$i]}" C-m
        tmux select-layout -t $SESSION tiled
    fi
done

# Synchronize panes
tmux set-window-option -t $SESSION synchronize-panes on

# Attacher
tmux attach -t $SESSION
```

### SSH config pour tmux

```
# ~/.ssh/config

Host *
    # Keep alive
    ServerAliveInterval 60
    ServerAliveCountMax 10

    # Multiplexing (partager connexions)
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 600

    # Agent forwarding
    ForwardAgent yes
```

## Git

### Git status dans status bar

```bash
# ~/.tmux.conf

# Branch courante
set -g status-right "#(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2)"

# Avec icône
set -g status-right " #(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2)"

# Branch + status (dirty/clean)
set -g status-right "#(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2) #(cd #{pane_current_path}; [[ -n \$(git status -s 2>/dev/null) ]] && echo '●' || echo '✓')"
```

### Script git status avancé

```bash
#!/bin/bash
# ~/.tmux/scripts/git-status.sh

cd "$1" 2>/dev/null || exit 0

# Check si git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    exit 0
fi

# Branch
branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "detached")

# Dirty
dirty=""
if [[ -n $(git status -s 2>/dev/null) ]]; then
    dirty="*"
fi

# Ahead/Behind
ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null)
behind=$(git rev-list --count HEAD..@{u} 2>/dev/null)

output=" $branch$dirty"

if [[ $ahead -gt 0 ]]; then
    output="$output↑$ahead"
fi

if [[ $behind -gt 0 ]]; then
    output="$output↓$behind"
fi

echo "$output"
```

```bash
# ~/.tmux.conf
set -g status-right "#(~/.tmux/scripts/git-status.sh #{pane_current_path})"
```

### Bindings git

```bash
# ~/.tmux.conf

# Git status dans nouveau pane
bind g split-window -h -c "#{pane_current_path}" "git status; read"

# Git log
bind G split-window -h -c "#{pane_current_path}" "git log --oneline --graph --all; read"

# Git diff
bind D split-window -h -c "#{pane_current_path}" "git diff; read"
```

## Docker

### Docker info dans status bar

```bash
# ~/.tmux.conf

# Nombre containers running
set -g status-right "🐳 #(docker ps -q 2>/dev/null | wc -l) | %H:%M"

# Avec détails
set -g status-right "#(docker ps --format '{{.Names}}' 2>/dev/null | wc -l) containers | %H:%M"
```

### Monitoring docker

```yaml
# ~/.tmuxinator/docker-monitor.yml

name: docker
root: ~/projects

windows:
  - stats:
      panes:
        - docker stats
        - watch -n 1 docker ps

  - logs:
      layout: tiled
      panes:
        - docker-compose logs -f web
        - docker-compose logs -f db
        - docker-compose logs -f redis

  - exec:
      panes:
        - docker-compose exec web bash
```

### Docker commands

```bash
# ~/.tmux.conf

# Docker exec dans nouveau pane
bind D command-prompt -p "Container:" "split-window -h 'docker exec -it %1 bash'"

# Docker logs
bind L command-prompt -p "Container:" "split-window -h 'docker logs -f %1'"
```

## Terminal multiplexers

### Screen conversion

```bash
# Équivalences screen -> tmux

# Screen              # Tmux
C-a c               # C-a c         Nouvelle window
C-a n               # C-a n         Next window
C-a p               # C-a p         Previous window
C-a "               # C-a s         Liste sessions
C-a A               # C-a ,         Rename window
C-a d               # C-a d         Detach
C-a |               # C-a %         Split vertical
C-a S               # C-a "         Split horizontal
C-a tab             # C-a o         Next pane
C-a X               # C-a x         Kill pane
C-a [               # C-a [         Copy mode
```

### Migration screen

```bash
# ~/.tmux.conf - Pour utilisateurs screen

# Bindings screen-like
bind c new-window
bind n next-window
bind p previous-window
bind d detach-client
bind | split-window -h
bind S split-window -v
bind tab select-pane -t :.+
bind X kill-pane
```

## FZF

### Intégration fzf

```bash
# ~/.tmux.conf

# Session picker avec fzf
bind s split-window -v "tmux list-sessions | sed -E 's/:.*$//' | fzf --reverse | xargs tmux switch-client -t"

# Window picker
bind w split-window -v "tmux list-windows -F '#{window_index}:#{window_name}' | fzf --reverse | cut -d: -f1 | xargs tmux select-window -t"
```

### Script fzf tmux

```bash
#!/bin/bash
# tmux-fzf-picker.sh

# Session picker avec preview

tmux list-sessions -F "#{session_name}" | \
fzf --reverse \
    --header="Select tmux session" \
    --preview="tmux list-windows -t {} | head -20" \
    --preview-window=right:60% | \
xargs tmux switch-client -t
```

## Clipboard

### Clipboard système

```bash
# ~/.tmux.conf

# Linux (xclip)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -selection clipboard"

# Linux (xsel)
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xsel -ib"

# macOS
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"

# WSL
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "clip.exe"

# Detect OS
if-shell "uname | grep -q Darwin" \
    "bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'pbcopy'" \
    "bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'xclip -selection clipboard'"
```

### Plugin tmux-yank

```bash
# ~/.tmux.conf

set -g @plugin 'tmux-plugins/tmux-yank'

# Options
set -g @yank_selection 'clipboard'
set -g @yank_selection_mouse 'clipboard'
set -g @yank_action 'copy-pipe-and-cancel'

# Détection OS automatique
```

### Paste depuis clipboard

```bash
# ~/.tmux.conf

# Linux
bind C-v run "xclip -o -selection clipboard | tmux load-buffer - ; tmux paste-buffer"

# macOS
bind C-v run "pbpaste | tmux load-buffer - ; tmux paste-buffer"

# WSL
bind C-v run "powershell.exe Get-Clipboard | tmux load-buffer - ; tmux paste-buffer"
```

## iTerm2 / Alacritty / Kitty

### iTerm2 (macOS)

```bash
# ~/.tmux.conf

# True color
set -ga terminal-overrides ",xterm-256color:Tc"

# Mouse
set -g mouse on

# Clipboard iTerm2
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @yank_action 'copy-pipe-no-clear'

# Intégration iTerm2
if-shell "test -e /Applications/iTerm.app" \
    "set -g @continuum-boot 'on'; set -g @continuum-boot-options 'iterm'"
```

### Alacritty

```yaml
# ~/.config/alacritty/alacritty.yml

env:
  TERM: xterm-256color

shell:
  program: /usr/bin/tmux
  args:
    - new-session
    - -A
    - -s
    - main

key_bindings:
  - { key: V, mods: Control|Shift, action: Paste }
  - { key: C, mods: Control|Shift, action: Copy }
```

```bash
# ~/.tmux.conf pour Alacritty
set -g default-terminal "xterm-256color"
set -ga terminal-overrides ",xterm-256color:Tc"
```

### Kitty

```conf
# ~/.config/kitty/kitty.conf

# Shell tmux
shell tmux new-session -A -s main

# True color
term xterm-kitty

# Clipboard
map ctrl+shift+c copy_to_clipboard
map ctrl+shift+v paste_from_clipboard
```

```bash
# ~/.tmux.conf pour Kitty
set -g default-terminal "xterm-kitty"
set -ga terminal-overrides ",xterm-kitty:Tc"
```

## Zellij comparison

### Zellij vs Tmux

```bash
# Différences principales:

# Tmux:
# - Plus mature et stable
# - Écosystème plugins riche
# - Configuration via .tmux.conf
# - Nécessite apprentissage keybindings

# Zellij:
# - Plus moderne
# - UI intégré (hints, tabs)
# - Configuration YAML
# - Keybindings visibles

# Choisir tmux si:
# - Besoin stabilité
# - Beaucoup de scripts existants
# - Besoin compatibilité maximale

# Choisir zellij si:
# - Débutant
# - Préférence UI moderne
# - Moins besoin customisation
```

## Best practices intégration

### Terminal setup complet

```bash
# ~/.bashrc ou ~/.zshrc

# Détection terminal
if [ -n "$TMUX" ]; then
    export TERM=screen-256color
else
    export TERM=xterm-256color
fi

# Auto-start tmux
if command -v tmux &> /dev/null && [ -z "$TMUX" ] && [ -z "$INSIDE_EMACS" ]; then
    # Attacher ou créer session
    tmux attach || tmux new-session
fi

# SSH agent
if [ ! -z "$SSH_AUTH_SOCK" ]; then
    ln -sf $SSH_AUTH_SOCK ~/.ssh/ssh_auth_sock
    export SSH_AUTH_SOCK=~/.ssh/ssh_auth_sock
fi

# Aliases
alias ta='tmux attach -t'
alias ts='tmux new-session -s'
alias tl='tmux list-sessions'
```

### Environnement développement

```bash
# ~/.tmux.conf

# True color
set -ga terminal-overrides ",xterm-256color:Tc"

# Clipboard
set -g @plugin 'tmux-plugins/tmux-yank'

# Vim integration
set -g @plugin 'christoomey/vim-tmux-navigator'

# Sessions
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'

# Focus events (vim)
set -g focus-events on

# Escape time (vim)
set -s escape-time 0

# Status bar avec git
set -g status-right "#(cd #{pane_current_path}; git branch 2>/dev/null | grep '*' | cut -d' ' -f2) | %H:%M"
```

### Multi-machine config

```bash
# ~/.tmux.conf

# Config de base
source-file ~/.tmux/tmux-base.conf

# Config spécifique par machine
if-shell "test -f ~/.tmux-local.conf" "source-file ~/.tmux-local.conf"

# Config par OS
if-shell "uname | grep -q Darwin" "source-file ~/.tmux/tmux-macos.conf"
if-shell "uname | grep -q Linux" "source-file ~/.tmux/tmux-linux.conf"

# Config par hostname
if-shell "test $(hostname) = laptop" "source-file ~/.tmux/tmux-laptop.conf"
if-shell "test $(hostname) = server" "source-file ~/.tmux/tmux-server.conf"
```

[← Scripts et automatisation](./infos-tmux-08-scripts-automatisation.md) | [Index](./infos-tmux-00-index.md) | [Cas pratiques →](./infos-tmux-10-cas-pratiques.md)

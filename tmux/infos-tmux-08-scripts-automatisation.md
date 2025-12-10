# 📜 Scripts et automatisation

[← Plugins et TPM](./infos-tmux-07-plugins-tpm.md) | [Index](./infos-tmux-00-index.md) | [Intégration →](./infos-tmux-09-integration.md)

## Scripts shell basiques

### Créer session avec layout

```bash
#!/bin/bash
# dev-session.sh

SESSION="dev"

# Créer session si n'existe pas
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
    # Créer session
    tmux new-session -d -s $SESSION -n editor

    # Window 1: Editor
    tmux send-keys -t $SESSION:editor "cd ~/project && vim" C-m

    # Split vertical
    tmux split-window -h -t $SESSION:editor
    tmux send-keys -t $SESSION:editor.2 "cd ~/project" C-m

    # Window 2: Server
    tmux new-window -t $SESSION:2 -n server
    tmux send-keys -t $SESSION:server "cd ~/project && npm run dev" C-m

    # Window 3: Logs
    tmux new-window -t $SESSION:3 -n logs
    tmux send-keys -t $SESSION:logs "cd ~/project && tail -f logs/app.log" C-m

    # Sélectionner première window
    tmux select-window -t $SESSION:editor
fi

# Attacher session
tmux attach -t $SESSION
```

### Script avec paramètres

```bash
#!/bin/bash
# create-project-session.sh

PROJECT_NAME=$1
PROJECT_PATH=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$PROJECT_PATH" ]; then
    echo "Usage: $0 <session-name> <project-path>"
    exit 1
fi

# Vérifier que le path existe
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Directory $PROJECT_PATH does not exist"
    exit 1
fi

# Créer session
tmux new-session -d -s $PROJECT_NAME -c $PROJECT_PATH

# Setup windows
tmux rename-window -t $PROJECT_NAME:1 "editor"
tmux send-keys -t $PROJECT_NAME:editor "vim ." C-m

tmux new-window -t $PROJECT_NAME:2 -n "terminal" -c $PROJECT_PATH

tmux new-window -t $PROJECT_NAME:3 -n "server" -c $PROJECT_PATH

# Attacher
tmux attach -t $PROJECT_NAME
```

### Script multi-panes

```bash
#!/bin/bash
# monitor-session.sh

SESSION="monitor"

tmux new-session -d -s $SESSION -n system

# Pane 1: htop
tmux send-keys -t $SESSION:system "htop" C-m

# Split horizontal
tmux split-window -h -t $SESSION:system
tmux send-keys -t $SESSION:system.2 "watch -n 1 df -h" C-m

# Split vertical (pane 1)
tmux split-window -v -t $SESSION:system.1
tmux send-keys -t $SESSION:system.3 "tail -f /var/log/syslog" C-m

# Split vertical (pane 2)
tmux select-pane -t $SESSION:system.2
tmux split-window -v -t $SESSION:system.2
tmux send-keys -t $SESSION:system.4 "watch -n 1 'ss -tulpn'" C-m

# Layout
tmux select-layout -t $SESSION:system tiled

# Attacher
tmux attach -t $SESSION
```

## Tmuxinator

### Installation

```bash
# Avec gem (Ruby)
gem install tmuxinator

# Ubuntu/Debian
sudo apt install tmuxinator

# macOS
brew install tmuxinator

# Vérifier
tmuxinator version
```

### Configuration

```bash
# Créer nouveau projet
tmuxinator new project-name

# Éditer projet existant
tmuxinator edit project-name

# Lister projets
tmuxinator list

# Supprimer projet
tmuxinator delete project-name
```

### Fichier tmuxinator basique

```yaml
# ~/.tmuxinator/dev.yml

name: dev
root: ~/projects/myapp

windows:
  - editor:
      layout: main-vertical
      panes:
        - vim
        - git status
  - server: npm run dev
  - logs: tail -f logs/app.log
```

### Exemple complet

```yaml
# ~/.tmuxinator/webapp.yml

name: webapp
root: ~/projects/webapp

# Commandes avant démarrage
pre_window: source ~/.nvm/nvm.sh

# Startup window
startup_window: editor

windows:
  - editor:
      layout: main-horizontal
      panes:
        - editor:
          - vim
        - terminal:
          - git status
        - tests:
          - npm run test:watch

  - server:
      layout: even-horizontal
      panes:
        - backend:
          - cd backend
          - npm run dev
        - frontend:
          - cd frontend
          - npm start

  - database:
      - psql mydb

  - logs:
      layout: even-horizontal
      panes:
        - backend: tail -f backend/logs/app.log
        - frontend: tail -f frontend/logs/app.log
        - nginx: sudo tail -f /var/log/nginx/access.log

  - monitoring:
      layout: tiled
      panes:
        - htop
        - watch -n 1 df -h
        - watch -n 1 free -h
        - docker stats
```

### Layouts tmuxinator

```yaml
# Layouts disponibles:
# - even-horizontal
# - even-vertical
# - main-horizontal
# - main-vertical
# - tiled

# Exemple avec layout custom
windows:
  - name: code
    layout: main-vertical
    panes:
      - vim
      - bundle exec guard
      - git log

  - name: server
    layout: tiled
    panes:
      - rails s
      - redis-server
      - sidekiq
      - mailcatcher
```

### Commandes pré/post

```yaml
# ~/.tmuxinator/project.yml

name: project
root: ~/project

# Avant tout
pre: docker-compose up -d

# Avant chaque window
pre_window: source .env

# Après arrêt
on_project_stop: docker-compose down

windows:
  - editor: vim
  - server: npm start
```

### Variables tmuxinator

```yaml
# Variables disponibles:

# <%= @settings["name"] %>
# <%= @settings["root"] %>

name: myproject
root: ~/projects/<%= @settings["name"] %>

windows:
  - editor:
    root: <%= @settings["root"] %>/src
    panes:
      - vim
```

### Utilisation tmuxinator

```bash
# Démarrer projet
tmuxinator start project-name
tmuxinator project-name
mux project-name

# Avec options
tmuxinator start project-name -n session-name
tmuxinator start project-name -p other-project.yml

# Debug
tmuxinator debug project-name

# Copy projet
tmuxinator copy source destination

# Doctor (vérifier config)
tmuxinator doctor
```

## Tmuxp

Alternative à tmuxinator en Python

### Installation

```bash
# Avec pip
pip install tmuxp

# Ou pipx
pipx install tmuxp

# Vérifier
tmuxp --version
```

### Configuration tmuxp

```yaml
# ~/.tmuxp/dev.yaml

session_name: dev
start_directory: ~/projects/myapp
windows:
  - window_name: editor
    layout: main-horizontal
    panes:
      - vim
      - git status

  - window_name: server
    panes:
      - npm run dev

  - window_name: logs
    panes:
      - tail -f logs/app.log
```

### Exemple complet tmuxp

```yaml
# ~/.tmuxp/webapp.yaml

session_name: webapp
start_directory: ~/projects/webapp

# Commandes avant
before_script: ./setup.sh

# Environnement
environment:
  NODE_ENV: development
  DATABASE_URL: postgresql://localhost/mydb

windows:
  - window_name: editor
    layout: main-vertical
    shell_command_before:
      - cd ~/projects/webapp
    panes:
      - shell_command:
        - vim
      - shell_command:
        - git status
        - git fetch

  - window_name: servers
    layout: tiled
    panes:
      - shell_command:
        - cd backend
        - npm run dev
      - shell_command:
        - cd frontend
        - npm start
      - shell_command:
        - redis-server
      - shell_command:
        - docker-compose up

  - window_name: logs
    panes:
      - tail -f logs/*.log
```

### Utilisation tmuxp

```bash
# Load config
tmuxp load project

# Load avec path
tmuxp load ~/.tmuxp/dev.yaml

# Convert tmuxinator -> tmuxp
tmuxp convert ~/.tmuxinator/project.yml

# Shell completion
tmuxp load <TAB>

# Freeze (capturer session courante)
tmuxp freeze session-name
```

## Scripts avancés

### Sauvegarder/restaurer sessions

```bash
#!/bin/bash
# save-session.sh

SESSION=$1

if [ -z "$SESSION" ]; then
    echo "Usage: $0 <session-name>"
    exit 1
fi

OUTPUT_FILE="$HOME/.tmux-sessions/${SESSION}.txt"
mkdir -p $(dirname $OUTPUT_FILE)

# Sauvegarder layout
tmux list-windows -t $SESSION -F "#{window_index}:#{window_name}:#{window_layout}" > $OUTPUT_FILE

# Sauvegarder panes
tmux list-panes -s -t $SESSION -F "#{session_name}:#{window_index}.#{pane_index} #{pane_current_path} #{pane_current_command}" >> $OUTPUT_FILE

echo "Session saved to $OUTPUT_FILE"
```

### Script de monitoring

```bash
#!/bin/bash
# tmux-status.sh

# Affiche status de toutes les sessions

echo "=== Tmux Sessions ==="
echo

tmux list-sessions -F "Session: #{session_name} | Windows: #{session_windows} | Created: #{session_created_string}" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "No tmux server running"
    exit 0
fi

echo
echo "=== Active Sessions ==="
echo

for session in $(tmux list-sessions -F "#{session_name}"); do
    echo "Session: $session"
    tmux list-windows -t $session -F "  Window #{window_index}: #{window_name} (#{window_panes} panes)"
done
```

### Auto-attach ou créer

```bash
#!/bin/bash
# tmux-attach-or-create.sh

SESSION=$1

if [ -z "$SESSION" ]; then
    SESSION="default"
fi

# Si session existe, attacher
tmux has-session -t $SESSION 2>/dev/null

if [ $? == 0 ]; then
    echo "Attaching to existing session: $SESSION"
    tmux attach -t $SESSION
else
    echo "Creating new session: $SESSION"
    tmux new-session -s $SESSION
fi
```

### Backup automatique

```bash
#!/bin/bash
# backup-tmux-sessions.sh

BACKUP_DIR="$HOME/.tmux-backups"
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/tmux-$DATE.txt"

mkdir -p $BACKUP_DIR

# Sauvegarder toutes les sessions
tmux list-sessions -F "#{session_name}" | while read session; do
    echo "=== Session: $session ===" >> $BACKUP_FILE
    tmux list-windows -t $session -F "#{window_index}:#{window_name}:#{window_layout}" >> $BACKUP_FILE
    echo "" >> $BACKUP_FILE
done

echo "Backup saved to $BACKUP_FILE"

# Garder seulement 10 derniers backups
ls -t $BACKUP_DIR/tmux-*.txt | tail -n +11 | xargs -r rm
```

## Intégration shell

### Bashrc

```bash
# ~/.bashrc

# Auto-start tmux
if command -v tmux &> /dev/null && [ -z "$TMUX" ]; then
    # Attacher à session existante ou créer nouvelle
    tmux attach -t default || tmux new -s default
fi

# Ou seulement en SSH
if [ -n "$SSH_CONNECTION" ] && command -v tmux &> /dev/null && [ -z "$TMUX" ]; then
    tmux attach -t ssh || tmux new -s ssh
fi

# Alias tmux
alias ta='tmux attach -t'
alias tad='tmux attach -d -t'
alias ts='tmux new-session -s'
alias tl='tmux list-sessions'
alias tksv='tmux kill-server'
alias tkss='tmux kill-session -t'

# Fonction smart attach
tm() {
    if [ -z "$1" ]; then
        tmux attach || tmux new-session
    else
        tmux attach -t "$1" || tmux new-session -s "$1"
    fi
}

# Auto-completion tmux sessions
_tmux_complete_session() {
    local sessions
    sessions=$(tmux list-sessions -F "#{session_name}" 2>/dev/null)
    COMPREPLY=($(compgen -W "$sessions" -- "${COMP_WORDS[COMP_CWORD]}"))
}
complete -F _tmux_complete_session ta tad tkss
```

### Zshrc

```bash
# ~/.zshrc

# Auto-start tmux
if command -v tmux &> /dev/null && [ -z "$TMUX" ]; then
    tmux attach || tmux new
fi

# Alias
alias ta='tmux attach -t'
alias tad='tmux attach -d -t'
alias ts='tmux new-session -s'
alias tl='tmux list-sessions'
alias tksv='tmux kill-server'
alias tkss='tmux kill-session -t'

# Fonction
tm() {
    [[ -n "$1" ]] && tmux attach -t "$1" || tmux new -s "$1" || tmux
}

# Completion zsh
_tmux_sessions() {
    local sessions
    sessions=(${(f)"$(tmux list-sessions -F "#{session_name}" 2>/dev/null)"})
    _describe 'session' sessions
}
compdef _tmux_sessions ta tad tkss
```

## Systemd integration

### Service tmux

```ini
# ~/.config/systemd/user/tmux.service

[Unit]
Description=Tmux server
After=network.target

[Service]
Type=forking
ExecStart=/usr/bin/tmux new-session -d -s default
ExecStop=/usr/bin/tmux kill-server
Restart=on-failure

[Install]
WantedBy=default.target
```

### Utilisation service

```bash
# Activer service
systemctl --user enable tmux.service

# Démarrer service
systemctl --user start tmux.service

# Status
systemctl --user status tmux.service

# Logs
journalctl --user -u tmux.service
```

## Workflows automatisés

### Git workflow

```yaml
# ~/.tmuxinator/git.yml

name: git
root: ~/projects/<%= @args[0] %>

windows:
  - main:
      layout: main-horizontal
      panes:
        - editor: vim
        - git:
          - git status
          - git log --oneline -10

  - review:
      panes:
        - git diff
        - git log --graph --all

  - branches:
      panes:
        - git branch -a
```

```bash
# Usage
tmuxinator git myproject
```

### Docker workflow

```yaml
# ~/.tmuxinator/docker.yml

name: docker
root: ~/projects/docker-project

pre: docker-compose up -d

windows:
  - logs:
      layout: tiled
      panes:
        - docker-compose logs -f web
        - docker-compose logs -f db
        - docker-compose logs -f redis
        - docker-compose logs -f worker

  - exec:
      panes:
        - docker-compose exec web bash
        - docker-compose exec db psql

  - monitor:
      panes:
        - docker stats
        - watch -n 1 docker-compose ps

on_project_stop: docker-compose down
```

### Admin SSH workflow

```bash
#!/bin/bash
# ssh-multi.sh

SESSION="ssh-multi"
SERVERS=("server1" "server2" "server3" "server4")

tmux new-session -d -s $SESSION

# Premier server
tmux send-keys -t $SESSION "ssh ${SERVERS[0]}" C-m

# Autres servers
for server in "${SERVERS[@]:1}"; do
    tmux split-window -t $SESSION
    tmux send-keys -t $SESSION "ssh $server" C-m
    tmux select-layout -t $SESSION tiled
done

# Synchronize panes
tmux set-window-option -t $SESSION synchronize-panes on

# Attacher
tmux attach -t $SESSION
```

## Scripts utilitaires

### Tmux session picker

```bash
#!/bin/bash
# tmux-picker.sh

# Nécessite fzf

SESSION=$(tmux list-sessions -F "#{session_name}" 2>/dev/null | fzf)

if [ -n "$SESSION" ]; then
    if [ -z "$TMUX" ]; then
        tmux attach -t "$SESSION"
    else
        tmux switch-client -t "$SESSION"
    fi
fi
```

### Window picker

```bash
#!/bin/bash
# tmux-window-picker.sh

# Liste toutes les windows de toutes les sessions

WINDOW=$(tmux list-windows -a -F "#{session_name}:#{window_index} - #{window_name}" | fzf)

if [ -n "$WINDOW" ]; then
    TARGET=$(echo $WINDOW | awk '{print $1}')
    tmux switch-client -t "$TARGET"
fi
```

### Kill zombies

```bash
#!/bin/bash
# kill-tmux-zombies.sh

# Tuer sessions détachées depuis plus de X jours

DAYS=7

tmux list-sessions -F "#{session_name} #{session_attached}" | while read session attached; do
    if [ "$attached" -eq 0 ]; then
        # Vérifier age session
        created=$(tmux display-message -t $session -p "#{session_created}")
        now=$(date +%s)
        age=$(( ($now - $created) / 86400 ))

        if [ $age -gt $DAYS ]; then
            echo "Killing old session: $session (${age} days old)"
            tmux kill-session -t $session
        fi
    fi
done
```

[← Plugins et TPM](./infos-tmux-07-plugins-tpm.md) | [Index](./infos-tmux-00-index.md) | [Intégration →](./infos-tmux-09-integration.md)

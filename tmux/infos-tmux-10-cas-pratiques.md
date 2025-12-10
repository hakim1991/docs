# 💡 Cas pratiques

[← Intégration](./infos-tmux-09-integration.md) | [Index](./infos-tmux-00-index.md) | [Troubleshooting →](./infos-tmux-11-troubleshooting.md)

## Développement web

### Setup frontend/backend

```yaml
# ~/.tmuxinator/webapp.yml

name: webapp
root: ~/projects/webapp

windows:
  - editor:
      layout: main-horizontal
      panes:
        - vim
        - git status

  - frontend:
      root: ~/projects/webapp/frontend
      layout: even-horizontal
      panes:
        - npm run dev
        - npm run test:watch

  - backend:
      root: ~/projects/webapp/backend
      layout: even-horizontal
      panes:
        - npm start
        - npm run test

  - database:
      panes:
        - psql mydb

  - logs:
      layout: tiled
      panes:
        - tail -f frontend/logs/app.log
        - tail -f backend/logs/app.log
        - tail -f /var/log/nginx/access.log
```

### React + Node.js

```bash
#!/bin/bash
# dev-react-node.sh

SESSION="react-node"
PROJECT_DIR="$HOME/projects/myapp"

cd $PROJECT_DIR

# Créer session
tmux new-session -d -s $SESSION -n editor

# Window 1: Editor
tmux send-keys -t $SESSION:editor "vim" C-m
tmux split-window -h -t $SESSION:editor -c $PROJECT_DIR
tmux send-keys -t $SESSION:editor.2 "git status" C-m

# Window 2: React
tmux new-window -t $SESSION:2 -n react -c $PROJECT_DIR/frontend
tmux send-keys -t $SESSION:react "npm start" C-m
tmux split-window -h -t $SESSION:react -c $PROJECT_DIR/frontend
tmux send-keys -t $SESSION:react.2 "npm run test:watch" C-m

# Window 3: Node.js
tmux new-window -t $SESSION:3 -n node -c $PROJECT_DIR/backend
tmux send-keys -t $SESSION:node "npm run dev" C-m
tmux split-window -h -t $SESSION:node -c $PROJECT_DIR/backend
tmux send-keys -t $SESSION:node.2 "npm run test" C-m

# Window 4: Database
tmux new-window -t $SESSION:4 -n db
tmux send-keys -t $SESSION:db "psql myapp" C-m

# Window 5: Logs
tmux new-window -t $SESSION:5 -n logs
tmux send-keys -t $SESSION:logs "tail -f backend/logs/app.log" C-m
tmux split-window -h -t $SESSION:logs
tmux send-keys -t $SESSION:logs.2 "tail -f frontend/logs/app.log" C-m

# Sélectionner première window
tmux select-window -t $SESSION:editor

# Attacher
tmux attach -t $SESSION
```

### Django development

```yaml
# ~/.tmuxinator/django.yml

name: django
root: ~/projects/django-app

pre_window: source venv/bin/activate

windows:
  - editor:
      layout: main-horizontal
      panes:
        - vim
        - git status

  - server:
      panes:
        - python manage.py runserver
        - python manage.py shell

  - celery:
      layout: even-horizontal
      panes:
        - celery -A myapp worker -l info
        - celery -A myapp beat -l info

  - database:
      panes:
        - python manage.py dbshell

  - tests:
      panes:
        - pytest --watch

  - logs:
      layout: tiled
      panes:
        - tail -f logs/django.log
        - tail -f logs/celery.log
        - tail -f /var/log/postgresql/postgresql.log
```

## DevOps / SRE

### Monitoring système

```bash
#!/bin/bash
# monitoring.sh

SESSION="monitor"

tmux new-session -d -s $SESSION -n system

# Layout 4 panes
tmux send-keys -t $SESSION:system "htop" C-m

tmux split-window -h -t $SESSION:system
tmux send-keys -t $SESSION:system.2 "watch -n 1 'df -h | head -10'" C-m

tmux split-window -v -t $SESSION:system.1
tmux send-keys -t $SESSION:system.3 "watch -n 1 'free -h'" C-m

tmux split-window -v -t $SESSION:system.2
tmux send-keys -t $SESSION:system.4 "watch -n 1 'ss -tulpn | head -20'" C-m

# Window 2: Logs
tmux new-window -t $SESSION:2 -n logs

tmux send-keys -t $SESSION:logs "tail -f /var/log/syslog" C-m

tmux split-window -h -t $SESSION:logs
tmux send-keys -t $SESSION:logs.2 "journalctl -f" C-m

# Window 3: Docker
tmux new-window -t $SESSION:3 -n docker

tmux send-keys -t $SESSION:docker "docker stats" C-m

tmux split-window -h -t $SESSION:docker
tmux send-keys -t $SESSION:docker.2 "watch -n 1 docker ps" C-m

# Attacher
tmux attach -t $SESSION
```

### Kubernetes monitoring

```yaml
# ~/.tmuxinator/k8s-monitor.yml

name: k8s
root: ~/

windows:
  - pods:
      layout: even-horizontal
      panes:
        - watch -n 2 kubectl get pods
        - watch -n 2 kubectl get services
        - watch -n 2 kubectl get deployments

  - logs:
      layout: tiled
      panes:
        - kubectl logs -f deployment/frontend
        - kubectl logs -f deployment/backend
        - kubectl logs -f deployment/worker
        - kubectl logs -f deployment/redis

  - nodes:
      panes:
        - watch -n 2 kubectl top nodes
        - watch -n 2 kubectl top pods

  - exec:
      panes:
        - kubectl exec -it deployment/backend -- bash
```

### Multi-server admin

```bash
#!/bin/bash
# admin-multi-servers.sh

SESSION="admin"
SERVERS=("web1.example.com" "web2.example.com" "db1.example.com" "db2.example.com")

tmux new-session -d -s $SESSION

# Premier serveur
tmux send-keys -t $SESSION "ssh ${SERVERS[0]}" C-m

# Autres serveurs
for server in "${SERVERS[@]:1}"; do
    tmux split-window -t $SESSION
    tmux send-keys -t $SESSION "ssh $server" C-m
    tmux select-layout -t $SESSION tiled
done

# Window pour commandes individuelles
tmux new-window -t $SESSION:2 -n individual

for server in "${SERVERS[@]}"; do
    if [ "$server" = "${SERVERS[0]}" ]; then
        tmux send-keys -t $SESSION:individual "ssh $server" C-m
    else
        tmux split-window -t $SESSION:individual
        tmux send-keys -t $SESSION:individual "ssh $server" C-m
        tmux select-layout -t $SESSION:individual tiled
    fi
done

# Sélectionner première window et synchroniser
tmux select-window -t $SESSION:1
tmux set-window-option -t $SESSION:1 synchronize-panes on

# Attacher
tmux attach -t $SESSION
```

### Deployment workflow

```yaml
# ~/.tmuxinator/deploy.yml

name: deploy
root: ~/projects/myapp

windows:
  - preparation:
      panes:
        - git status
        - git log --oneline -10

  - build:
      layout: even-horizontal
      panes:
        - npm run build
        - docker build -t myapp:latest .

  - test:
      layout: tiled
      panes:
        - npm run test
        - npm run lint
        - npm run audit
        - docker-compose up -d && npm run test:e2e

  - deploy:
      panes:
        - echo "Ready to deploy"

  - monitoring:
      layout: even-horizontal
      panes:
        - watch -n 2 kubectl get pods
        - kubectl logs -f deployment/myapp
```

## Data Science

### Jupyter + Python

```yaml
# ~/.tmuxinator/datascience.yml

name: datascience
root: ~/projects/ml-project

pre_window: source venv/bin/activate

windows:
  - jupyter:
      panes:
        - jupyter lab

  - notebook:
      panes:
        - ipython

  - editor:
      layout: main-horizontal
      panes:
        - vim
        - python

  - training:
      layout: even-horizontal
      panes:
        - python train.py
        - watch -n 1 'nvidia-smi'

  - tensorboard:
      panes:
        - tensorboard --logdir=./logs

  - monitoring:
      layout: tiled
      panes:
        - htop
        - watch -n 1 'df -h'
        - watch -n 1 'free -h'
        - watch -n 1 'nvidia-smi'
```

### ML Training

```bash
#!/bin/bash
# ml-training.sh

SESSION="ml-training"
PROJECT_DIR="$HOME/ml/project"

cd $PROJECT_DIR
source venv/bin/activate

tmux new-session -d -s $SESSION -n training

# Training script
tmux send-keys -t $SESSION:training "python train.py --config config.yaml" C-m

# Split pour monitoring
tmux split-window -h -t $SESSION:training
tmux send-keys -t $SESSION:training.2 "watch -n 1 nvidia-smi" C-m

tmux split-window -v -t $SESSION:training.2
tmux send-keys -t $SESSION:training.3 "tail -f logs/training.log" C-m

# Window 2: Tensorboard
tmux new-window -t $SESSION:2 -n tensorboard
tmux send-keys -t $SESSION:tensorboard "tensorboard --logdir=./runs" C-m

# Window 3: Jupyter
tmux new-window -t $SESSION:3 -n jupyter
tmux send-keys -t $SESSION:jupyter "jupyter lab" C-m

# Attacher
tmux attach -t $SESSION
```

## Administration système

### Log monitoring

```bash
#!/bin/bash
# log-monitor.sh

SESSION="logs"

tmux new-session -d -s $SESSION -n system

# System logs
tmux send-keys -t $SESSION:system "tail -f /var/log/syslog" C-m

tmux split-window -h -t $SESSION:system
tmux send-keys -t $SESSION:system.2 "tail -f /var/log/auth.log" C-m

tmux split-window -v -t $SESSION:system.1
tmux send-keys -t $SESSION:system.3 "journalctl -f" C-m

tmux split-window -v -t $SESSION:system.2
tmux send-keys -t $SESSION:system.4 "dmesg -w" C-m

# Window 2: Application logs
tmux new-window -t $SESSION:2 -n app

tmux send-keys -t $SESSION:app "tail -f /var/log/nginx/access.log" C-m

tmux split-window -h -t $SESSION:app
tmux send-keys -t $SESSION:app.2 "tail -f /var/log/nginx/error.log" C-m

# Window 3: Databases
tmux new-window -t $SESSION:3 -n db

tmux send-keys -t $SESSION:db "tail -f /var/log/postgresql/postgresql.log" C-m

tmux split-window -h -t $SESSION:db
tmux send-keys -t $SESSION:db.2 "tail -f /var/log/mysql/error.log" C-m

# Attacher
tmux attach -t $SESSION
```

### Backup management

```yaml
# ~/.tmuxinator/backup.yml

name: backup
root: ~/

windows:
  - status:
      panes:
        - watch -n 5 'df -h'
        - watch -n 5 'du -sh /backups/*'

  - databases:
      layout: even-horizontal
      panes:
        - echo "PostgreSQL backup" && pg_dumpall > /backups/postgres-$(date +%Y%m%d).sql
        - echo "MySQL backup" && mysqldump --all-databases > /backups/mysql-$(date +%Y%m%d).sql

  - files:
      panes:
        - rsync -avz --progress /data/ /backups/data/

  - monitoring:
      layout: tiled
      panes:
        - tail -f /var/log/backup.log
        - watch -n 1 'ls -lh /backups/ | tail -20'
        - htop
```

## Pair programming

### Setup collaboration

```bash
#!/bin/bash
# pair-session.sh

SESSION="pair"
USER2="colleague"

# Créer session
tmux new-session -d -s $SESSION -n code

# Permissions pour partage
chmod 777 /tmp/tmux-$(id -u)

# Window 1: Code
tmux send-keys -t $SESSION:code "vim" C-m
tmux split-window -h -t $SESSION:code
tmux send-keys -t $SESSION:code.2 "git status" C-m

# Window 2: Terminal
tmux new-window -t $SESSION:2 -n term

# Window 3: Tests
tmux new-window -t $SESSION:3 -n tests
tmux send-keys -t $SESSION:tests "npm run test:watch" C-m

# Partager session
echo "Session créée. Pour rejoindre:"
echo "tmux attach -t $SESSION"
echo ""
echo "Ou depuis SSH:"
echo "ssh -t $USER2@localhost tmux attach -t $SESSION"

# Attacher
tmux attach -t $SESSION
```

### Screen sharing tips

```bash
# ~/.tmux.conf - Configuration pair programming

# Taille minimale (éviter resize fights)
setw -g aggressive-resize on

# Afficher qui contrôle
set -g status-right "#{session_attached} users | %H:%M"

# Notification activité
setw -g monitor-activity on
set -g visual-activity on

# Bell pour alertes
set -g visual-bell on
set -g bell-action any
```

## Testing / QA

### Test suite monitoring

```yaml
# ~/.tmuxinator/testing.yml

name: testing
root: ~/projects/myapp

windows:
  - unit:
      layout: even-horizontal
      panes:
        - npm run test:unit:watch
        - npm run test:unit:coverage

  - integration:
      panes:
        - npm run test:integration:watch

  - e2e:
      layout: main-horizontal
      panes:
        - npm run test:e2e
        - npm run test:e2e:headed

  - linting:
      layout: tiled
      panes:
        - npm run lint:watch
        - npm run stylelint:watch
        - npm run tsc:watch
        - npm run audit

  - ci:
      panes:
        - act -l  # GitHub Actions local
```

### Load testing

```bash
#!/bin/bash
# load-testing.sh

SESSION="loadtest"
TARGET="https://api.example.com"

tmux new-session -d -s $SESSION -n artillery

# Artillery load test
tmux send-keys -t $SESSION:artillery "artillery quick --count 100 --num 10 $TARGET" C-m

# Split pour monitoring
tmux split-window -h -t $SESSION:artillery
tmux send-keys -t $SESSION:artillery.2 "watch -n 1 'curl -s $TARGET/health | jq .'" C-m

# Window 2: Server monitoring
tmux new-window -t $SESSION:2 -n monitor

tmux send-keys -t $SESSION:monitor "ssh server htop" C-m

tmux split-window -h -t $SESSION:monitor
tmux send-keys -t $SESSION:monitor.2 "ssh server 'tail -f /var/log/app.log'" C-m

# Window 3: Metrics
tmux new-window -t $SESSION:3 -n metrics

tmux send-keys -t $SESSION:metrics "watch -n 1 'curl -s http://localhost:9090/metrics | grep http_requests'" C-m

# Attacher
tmux attach -t $SESSION
```

## Remote work

### VPN + Work session

```bash
#!/bin/bash
# work-session.sh

SESSION="work"

tmux new-session -d -s $SESSION -n vpn

# Window 1: VPN
tmux send-keys -t $SESSION:vpn "sudo openvpn --config ~/vpn/work.ovpn" C-m

# Attendre VPN (5 secondes)
sleep 5

# Window 2: SSH servers
tmux new-window -t $SESSION:2 -n servers

tmux send-keys -t $SESSION:servers "ssh work-server-1" C-m

tmux split-window -h -t $SESSION:servers
tmux send-keys -t $SESSION:servers.2 "ssh work-server-2" C-m

# Window 3: Local dev
tmux new-window -t $SESSION:3 -n dev

tmux send-keys -t $SESSION:dev "cd ~/work/project && vim" C-m

tmux split-window -h -t $SESSION:dev
tmux send-keys -t $SESSION:dev.2 "cd ~/work/project && npm start" C-m

# Window 4: Communication
tmux new-window -t $SESSION:4 -n comm

tmux send-keys -t $SESSION:comm "weechat" C-m

# Attacher
tmux attach -t $SESSION
```

### Multi-project workspace

```yaml
# ~/.tmuxinator/workspace.yml

name: workspace
root: ~/projects

windows:
  - project1:
      root: ~/projects/project1
      layout: main-horizontal
      panes:
        - vim
        - git status

  - project2:
      root: ~/projects/project2
      layout: main-horizontal
      panes:
        - vim
        - git status

  - project3:
      root: ~/projects/project3
      layout: main-horizontal
      panes:
        - vim
        - git status

  - terminals:
      layout: tiled
      panes:
        - cd ~/projects/project1
        - cd ~/projects/project2
        - cd ~/projects/project3
        - htop

  - communication:
      panes:
        - weechat
```

## Scripts personnalisés

### Quick project launcher

```bash
#!/bin/bash
# quickstart.sh

# Lancer projet basé sur le répertoire

PROJECT_DIR="$1"
PROJECT_NAME=$(basename "$PROJECT_DIR")

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: $PROJECT_DIR does not exist"
    exit 1
fi

SESSION="${PROJECT_NAME}"

# Vérifier si session existe
tmux has-session -t $SESSION 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Session $SESSION already exists, attaching..."
    tmux attach -t $SESSION
    exit 0
fi

# Créer session
cd "$PROJECT_DIR"
tmux new-session -d -s $SESSION -n editor

# Détecter type de projet
if [ -f "package.json" ]; then
    # Node.js project
    tmux send-keys -t $SESSION:editor "vim" C-m
    tmux split-window -h -t $SESSION:editor

    tmux new-window -t $SESSION:2 -n server
    tmux send-keys -t $SESSION:server "npm start" C-m

elif [ -f "manage.py" ]; then
    # Django project
    tmux send-keys -t $SESSION:editor "vim" C-m
    tmux split-window -h -t $SESSION:editor

    tmux new-window -t $SESSION:2 -n server
    tmux send-keys -t $SESSION:server "source venv/bin/activate && python manage.py runserver" C-m

elif [ -f "docker-compose.yml" ]; then
    # Docker project
    tmux send-keys -t $SESSION:editor "vim" C-m
    tmux split-window -h -t $SESSION:editor

    tmux new-window -t $SESSION:2 -n docker
    tmux send-keys -t $SESSION:docker "docker-compose up" C-m
else
    # Generic project
    tmux send-keys -t $SESSION:editor "vim" C-m
    tmux split-window -h -t $SESSION:editor
fi

# Window git
tmux new-window -t $SESSION:3 -n git
tmux send-keys -t $SESSION:git "git status" C-m

# Sélectionner editor
tmux select-window -t $SESSION:editor

# Attacher
tmux attach -t $SESSION
```

[← Intégration](./infos-tmux-09-integration.md) | [Index](./infos-tmux-00-index.md) | [Troubleshooting →](./infos-tmux-11-troubleshooting.md)

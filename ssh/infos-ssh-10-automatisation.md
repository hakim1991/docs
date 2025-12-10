# 🤖 Automatisation SSH

[← Avancé](./infos-ssh-09-avance.md) | [Index](./infos-ssh-00-index.md) | [Troubleshooting →](./infos-ssh-11-troubleshooting.md)

## Scripts SSH basiques

```bash
#!/bin/bash
# Exécuter une commande sur plusieurs serveurs

SERVERS="server1 server2 server3"
COMMAND="uptime"

for server in $SERVERS; do
    echo "=== $server ==="
    ssh $server "$COMMAND"
    echo ""
done
```

```bash
#!/bin/bash
# Backup automatique via SSH

SOURCE="/var/www"
DEST="backup@backup-server:/backups"
DATE=$(date +%Y%m%d)

rsync -avz --delete $SOURCE/ $DEST/www-$DATE/

if [ $? -eq 0 ]; then
    echo "✅ Backup réussi"
else
    echo "❌ Échec backup"
    exit 1
fi
```

## Ansible pour SSH

```yaml
# playbook.yml
---
- name: Configuration serveurs
  hosts: all
  become: yes

  tasks:
    - name: Mettre à jour les paquets
      apt:
        update_cache: yes
        upgrade: dist

    - name: Installer packages
      apt:
        name:
          - nginx
          - postgresql
          - redis
        state: present

    - name: Copier fichiers
      copy:
        src: ./config/nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: Redémarrer nginx

    - name: Déployer application
      git:
        repo: https://github.com/user/app.git
        dest: /var/www/app
        version: main

  handlers:
    - name: Redémarrer nginx
      service:
        name: nginx
        state: restarted
```

```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
db2.example.com

[all:vars]
ansible_user=admin
ansible_ssh_private_key_file=~/.ssh/id_ed25519
ansible_become=yes
ansible_become_method=sudo
```

```bash
# Exécuter
ansible-playbook -i inventory.ini playbook.yml

# Commande ad-hoc
ansible all -i inventory.ini -m ping
ansible webservers -i inventory.ini -m command -a "uptime"
ansible databases -i inventory.ini -m apt -a "name=postgresql state=present"

# Avec jump host
ansible all -i inventory.ini \
    --ssh-extra-args="-J bastion.example.com" \
    -m ping
```

## Fabric pour déploiement

```python
# fabfile.py
from fabric import task, Connection

@task
def deploy(c):
    """Déployer l'application"""
    with Connection('server.example.com', user='deploy') as conn:
        # Git pull
        conn.run('cd /var/www/app && git pull origin main')

        # Install dependencies
        conn.run('cd /var/www/app && npm install')

        # Build
        conn.run('cd /var/www/app && npm run build')

        # Restart
        conn.sudo('systemctl restart app')

        print("✅ Déploiement réussi")

@task
def backup(c):
    """Backup de la base de données"""
    with Connection('db.example.com', user='admin') as conn:
        # Dump database
        conn.run('pg_dump mydb > /tmp/backup.sql')

        # Download
        conn.get('/tmp/backup.sql', './backup-{}.sql'.format(
            datetime.now().strftime('%Y%m%d')
        ))

        # Cleanup
        conn.run('rm /tmp/backup.sql')

        print("✅ Backup téléchargé")

@task
def check_status(c):
    """Vérifier le statut des services"""
    servers = ['web1', 'web2', 'db1']

    for server in servers:
        with Connection(f'{server}.example.com') as conn:
            print(f"\n=== {server} ===")
            conn.run('uptime')
            conn.run('free -h')
            conn.sudo('systemctl status nginx')
```

```bash
# Utilisation
pip install fabric

fab deploy
fab backup
fab check-status
```

## Parallel SSH (pssh)

```bash
# Installer
sudo apt install pssh

# Exécuter sur plusieurs serveurs
parallel-ssh -h servers.txt -l user "uptime"

# servers.txt:
web1.example.com
web2.example.com
db1.example.com

# Avec options
parallel-ssh -h servers.txt -l admin \
    -o output/ \
    -e errors/ \
    -t 30 \
    "systemctl status nginx"

# Copier des fichiers
parallel-scp -h servers.txt -l user \
    config.txt /etc/app/config.txt

# Récupérer des fichiers
parallel-slurp -h servers.txt -l user \
    -L logs/ \
    /var/log/app/error.log \
    error.log
```

## expect pour automatisation interactive

```bash
#!/usr/bin/expect -f
# ssh-auto-password.exp

set timeout 20
set host [lindex $argv 0]
set user [lindex $argv 1]
set password [lindex $argv 2]

spawn ssh $user@$host

expect {
    "Are you sure you want to continue connecting" {
        send "yes\r"
        expect "*assword:"
        send "$password\r"
    }
    "*assword:" {
        send "$password\r"
    }
}

interact
```

```bash
# Utilisation
./ssh-auto-password.exp server.com admin mypassword
```

```bash
#!/usr/bin/expect -f
# ssh-keygen-auto.exp

set timeout 20

spawn ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "auto-generated"

expect {
    "Enter file in which to save the key" {
        send "\r"
    }
}

expect {
    "Enter passphrase" {
        send "my-secure-passphrase\r"
    }
}

expect {
    "Enter same passphrase again" {
        send "my-secure-passphrase\r"
    }
}

expect eof
```

## Terraform provisioning

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  key_name      = "my-ssh-key"

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_ed25519")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y nginx",
      "sudo systemctl start nginx"
    ]
  }

  provisioner "file" {
    source      = "nginx.conf"
    destination = "/tmp/nginx.conf"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo mv /tmp/nginx.conf /etc/nginx/nginx.conf",
      "sudo systemctl restart nginx"
    ]
  }
}

output "server_ip" {
  value = aws_instance.web.public_ip
}
```

## Scripts de maintenance

```bash
#!/bin/bash
# update-all-servers.sh

SERVERS="web1 web2 db1 cache1"
LOG="/var/log/server-updates.log"

echo "=== Update $(date) ===" >> $LOG

for server in $SERVERS; do
    echo "Updating $server..." | tee -a $LOG

    ssh $server << 'EOF' 2>&1 | tee -a $LOG
        sudo apt update
        sudo apt upgrade -y
        sudo apt autoremove -y
        echo "✅ $(hostname) updated"
EOF

    if [ $? -eq 0 ]; then
        echo "✅ $server OK" | tee -a $LOG
    else
        echo "❌ $server FAILED" | tee -a $LOG
    fi
done

echo "" >> $LOG
```

```bash
#!/bin/bash
# collect-logs.sh

SERVERS="web1 web2 db1"
OUTPUT_DIR="./collected-logs-$(date +%Y%m%d)"

mkdir -p $OUTPUT_DIR

for server in $SERVERS; do
    echo "Collecting logs from $server..."

    mkdir -p $OUTPUT_DIR/$server

    # Rsync logs
    rsync -avz \
        --include='*.log' \
        --include='*/' \
        --exclude='*' \
        $server:/var/log/ \
        $OUTPUT_DIR/$server/

    # System info
    ssh $server "uname -a" > $OUTPUT_DIR/$server/system.txt
    ssh $server "df -h" > $OUTPUT_DIR/$server/disk.txt
    ssh $server "free -h" > $OUTPUT_DIR/$server/memory.txt
done

# Compress
tar czf collected-logs-$(date +%Y%m%d).tar.gz $OUTPUT_DIR

echo "✅ Logs collected: collected-logs-$(date +%Y%m%d).tar.gz"
```

## CI/CD avec SSH

```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  before_script:
    - 'which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )'
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
    - ssh-keyscan $DEPLOY_SERVER >> ~/.ssh/known_hosts
    - chmod 644 ~/.ssh/known_hosts
  script:
    - rsync -avz --delete dist/ $DEPLOY_USER@$DEPLOY_SERVER:/var/www/app/
    - ssh $DEPLOY_USER@$DEPLOY_SERVER "cd /var/www/app && pm2 restart app"
  only:
    - main
```

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'

    - name: Install dependencies
      run: npm ci

    - name: Build
      run: npm run build

    - name: Deploy via SSH
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        port: ${{ secrets.PORT }}
        script: |
          cd /var/www/app
          git pull origin main
          npm install
          npm run build
          pm2 restart app
```

## Monitoring automatisé

```bash
#!/bin/bash
# health-check.sh

SERVERS="web1 web2 db1"
ALERT_EMAIL="admin@example.com"

for server in $SERVERS; do
    echo "Checking $server..."

    # SSH health
    if ! ssh -o ConnectTimeout=5 $server "exit" 2>/dev/null; then
        echo "❌ $server: SSH down" | mail -s "Alert: $server SSH down" $ALERT_EMAIL
        continue
    fi

    # CPU load
    LOAD=$(ssh $server "uptime | awk -F'load average:' '{print \$2}' | awk '{print \$1}'")
    if (( $(echo "$LOAD > 10" | bc -l) )); then
        echo "⚠️  $server: High load $LOAD" | mail -s "Alert: $server high load" $ALERT_EMAIL
    fi

    # Disk space
    DISK=$(ssh $server "df -h / | tail -1 | awk '{print \$5}' | sed 's/%//'")
    if [ $DISK -gt 90 ]; then
        echo "⚠️  $server: Disk $DISK%" | mail -s "Alert: $server disk space" $ALERT_EMAIL
    fi

    # Memory
    MEM=$(ssh $server "free | grep Mem | awk '{print (\$3/\$2) * 100}'")
    if (( $(echo "$MEM > 90" | bc -l) )); then
        echo "⚠️  $server: Memory $MEM%" | mail -s "Alert: $server memory" $ALERT_EMAIL
    fi

    echo "✅ $server OK"
done
```

## Synchronisation bidirectionnelle

```bash
#!/bin/bash
# bidirectional-sync.sh

SERVER="backup-server"
LOCAL_DIR="/data"
REMOTE_DIR="/backups/data"

# Sync to server
echo "Syncing to server..."
rsync -avzu --delete $LOCAL_DIR/ $SERVER:$REMOTE_DIR/

# Sync from server
echo "Syncing from server..."
rsync -avzu $SERVER:$REMOTE_DIR/ $LOCAL_DIR/

# Utiliser Unison pour vrai bidirectionnel
# sudo apt install unison
# unison $LOCAL_DIR ssh://$SERVER/$REMOTE_DIR -batch -auto
```

## SSH dans Docker

```dockerfile
# Dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd

# Configuration SSH
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Ajouter clé publique
RUN mkdir -p /root/.ssh
COPY authorized_keys /root/.ssh/authorized_keys
RUN chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  ssh-server:
    build: .
    ports:
      - "2222:22"
    volumes:
      - ./data:/data
```

```bash
# Se connecter
ssh -p 2222 root@localhost
```

## Gestion de configuration

```bash
#!/bin/bash
# deploy-config.sh

CONFIG_REPO="git@github.com:company/configs.git"
TEMP_DIR="/tmp/configs"

# Clone config repo
git clone $CONFIG_REPO $TEMP_DIR

# Deploy to servers
SERVERS=$(cat $TEMP_DIR/servers.txt)

for server in $SERVERS; do
    echo "Deploying to $server..."

    # Copy configs
    rsync -avz $TEMP_DIR/nginx/ $server:/etc/nginx/
    rsync -avz $TEMP_DIR/systemd/ $server:/etc/systemd/system/

    # Reload services
    ssh $server << 'EOF'
        sudo nginx -t && sudo systemctl reload nginx
        sudo systemctl daemon-reload
        sudo systemctl restart app
EOF

    echo "✅ $server updated"
done

# Cleanup
rm -rf $TEMP_DIR
```

[← Avancé](./infos-ssh-09-avance.md) | [Index](./infos-ssh-00-index.md) | [Troubleshooting →](./infos-ssh-11-troubleshooting.md)

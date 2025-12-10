# 🌐 Tunneling et Port Forwarding

[← Authentification avancée](./infos-ssh-04-authentification-avancee.md) | [Index](./infos-ssh-00-index.md) | [Transfert de fichiers →](./infos-ssh-06-transfert-fichiers.md)

## Local Port Forwarding

```bash
# Syntaxe de base
ssh -L [local_port]:destination_host:destination_port user@ssh_server

# Accéder à un serveur distant via SSH
ssh -L 8080:localhost:80 user@server
# Puis accéder à http://localhost:8080

# Accéder à une base de données distante
ssh -L 3306:localhost:3306 user@server
# Puis se connecter à MySQL sur localhost:3306

# Accéder à un service sur un autre serveur via SSH
ssh -L 5432:database.internal:5432 user@bastion
# PostgreSQL sur database.internal accessible via localhost:5432

# Plusieurs tunnels en une commande
ssh -L 3000:localhost:3000 -L 5432:localhost:5432 user@server

# En arrière-plan
ssh -f -N -L 8080:localhost:80 user@server
# -f : background
# -N : pas de commande à distance

# Avec interface spécifique
ssh -L 127.0.0.1:8080:localhost:80 user@server
# Écoute uniquement sur localhost

ssh -L 0.0.0.0:8080:localhost:80 user@server
# Écoute sur toutes les interfaces (attention sécurité!)
```

## Remote Port Forwarding

```bash
# Syntaxe de base
ssh -R [remote_port]:destination_host:destination_port user@ssh_server

# Exposer un service local sur le serveur distant
ssh -R 8080:localhost:80 user@server
# Le port 8080 du serveur pointe vers localhost:80

# Exposer un service local au monde via un serveur public
ssh -R 8080:localhost:3000 user@public-server
# Autres peuvent accéder via public-server:8080

# Reverse SSH (accéder à la machine locale depuis le serveur)
ssh -R 2222:localhost:22 user@server
# Depuis le serveur: ssh -p 2222 localhost

# Avec interface spécifique sur le serveur
ssh -R 192.168.1.100:8080:localhost:80 user@server

# En arrière-plan
ssh -f -N -R 8080:localhost:3000 user@server

# Configuration serveur nécessaire pour remote forwarding public
# /etc/ssh/sshd_config
GatewayPorts yes
# ou
GatewayPorts clientspecified
```

## Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Créer un proxy SOCKS
ssh -D 8080 user@server

# Avec options
ssh -f -N -D 8080 user@server

# Sur toutes les interfaces (attention!)
ssh -D 0.0.0.0:8080 user@server

# Utiliser le proxy SOCKS

# Avec curl
curl --socks5 localhost:8080 https://api.example.com

# Avec wget
wget -e use_proxy=yes -e https_proxy=socks5://localhost:8080 https://example.com

# Configuration Firefox:
# Préférences → Réseau → Paramètres
# SOCKS Host: localhost
# Port: 8080
# SOCKS v5

# Configuration Chrome/Chromium
google-chrome --proxy-server="socks5://localhost:8080"

# Configuration système (Linux)
export http_proxy="socks5://localhost:8080"
export https_proxy="socks5://localhost:8080"
export no_proxy="localhost,127.0.0.1"
```

## Tunneling avancé

```bash
# Tunnel persistant avec autossh
sudo apt install autossh

# Tunnel local persistant
autossh -M 0 -f -N -L 8080:localhost:80 user@server

# Tunnel remote persistant
autossh -M 0 -f -N -R 8080:localhost:3000 user@server

# Options utiles:
# -M 0 : désactive le monitoring port (utilise ServerAliveInterval)
# -f : background
# -N : pas de commande

# Avec retry et monitoring
autossh -M 20000 -f -N \
    -o "ServerAliveInterval 30" \
    -o "ServerAliveCountMax 3" \
    -L 8080:localhost:80 \
    user@server

# Service systemd pour tunnel persistant
sudo nano /etc/systemd/system/ssh-tunnel.service
```

```ini
[Unit]
Description=SSH Tunnel to Server
After=network.target

[Service]
User=myuser
ExecStart=/usr/bin/autossh -M 0 -N \
    -o "ServerAliveInterval=30" \
    -o "ServerAliveCountMax=3" \
    -o "ExitOnForwardFailure=yes" \
    -L 8080:localhost:80 \
    user@server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start ssh-tunnel
sudo systemctl enable ssh-tunnel
```

## VPN sur SSH (tun/tap)

```bash
# Configuration serveur
# /etc/ssh/sshd_config
PermitTunnel yes
PermitRootLogin yes  # Ou créer un user avec permissions

# Créer tunnel TUN
ssh -w 0:0 root@server

# Configurer l'interface côté client
sudo ip addr add 10.0.0.1/24 dev tun0
sudo ip link set tun0 up

# Configurer l'interface côté serveur
sudo ip addr add 10.0.0.2/24 dev tun0
sudo ip link set tun0 up

# Routing côté client
sudo ip route add 192.168.1.0/24 via 10.0.0.2

# Script automatisé
#!/bin/bash
# ssh-vpn.sh
ssh -w 0:0 root@server "
    ip addr add 10.0.0.2/24 dev tun0;
    ip link set tun0 up;
    echo 1 > /proc/sys/net/ipv4/ip_forward;
" &

sleep 2
sudo ip addr add 10.0.0.1/24 dev tun0
sudo ip link set tun0 up
sudo ip route add 192.168.1.0/24 via 10.0.0.2
```

## ProxyJump (Bastion/Jump Host)

```bash
# Méthode moderne (OpenSSH 7.3+)
ssh -J bastion user@internal-server

# Plusieurs jump hosts
ssh -J bastion1,bastion2,bastion3 user@final-server

# Avec port personnalisé
ssh -J user@bastion:2222 user@internal-server

# Dans ~/.ssh/config
Host internal-server
    HostName 10.0.0.100
    User admin
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User jumpuser
    Port 2222

# Utilisation simplifiée
ssh internal-server

# Ancienne méthode (ProxyCommand)
Host internal-server
    HostName 10.0.0.100
    User admin
    ProxyCommand ssh -W %h:%p bastion

# Avec netcat
Host internal-server
    ProxyCommand ssh bastion nc %h %p
```

## Port Forwarding dans config

```bash
# ~/.ssh/config

# Local forwarding
Host dev
    HostName dev.example.com
    User developer
    LocalForward 3000 localhost:3000
    LocalForward 5432 localhost:5432
    LocalForward 6379 localhost:6379

# Remote forwarding
Host public
    HostName public-server.com
    User admin
    RemoteForward 8080 localhost:3000

# Dynamic forwarding (SOCKS)
Host proxy
    HostName proxy.example.com
    User proxyuser
    DynamicForward 8080

# Combinaison
Host complete
    HostName server.example.com
    User admin
    LocalForward 3000 localhost:3000
    RemoteForward 8080 localhost:8080
    DynamicForward 9090
    ExitOnForwardFailure yes
```

## Cas pratiques

### Accéder à une base de données

```bash
# PostgreSQL via tunnel
ssh -L 5432:localhost:5432 user@db-server

# Dans une autre console
psql -h localhost -p 5432 -U postgres mydb

# MySQL via tunnel
ssh -L 3306:localhost:3306 user@db-server

# Dans une autre console
mysql -h 127.0.0.1 -P 3306 -u root -p

# MongoDB via tunnel
ssh -L 27017:localhost:27017 user@mongo-server

# Dans une autre console
mongo localhost:27017
```

### Accéder à un service web interne

```bash
# Application web sur port 3000
ssh -L 8080:localhost:3000 user@app-server

# Ouvrir dans le navigateur
firefox http://localhost:8080

# Plusieurs applications
ssh -L 8001:app1.internal:80 \
    -L 8002:app2.internal:80 \
    -L 8003:app3.internal:80 \
    user@bastion

# Accéder via:
# http://localhost:8001
# http://localhost:8002
# http://localhost:8003
```

### Exposer un service local

```bash
# Développer localement, tester depuis serveur distant
ssh -R 3000:localhost:3000 user@test-server

# Sur le serveur, tester:
curl http://localhost:3000

# Webhook development
ssh -R 8080:localhost:3000 user@public-server
# Webhook URL: http://public-server:8080/webhook
```

### Bypass de firewall

```bash
# Accéder à un site bloqué via proxy SOCKS
ssh -D 8080 user@external-server

# Configurer le navigateur pour utiliser SOCKS localhost:8080
# Tous les sites sont maintenant accessibles via external-server

# CLI avec proxy
curl --socks5 localhost:8080 https://blocked-site.com
```

### Reverse SSH pour support technique

```bash
# Sur la machine du client (derrière NAT/firewall)
ssh -R 2222:localhost:22 user@support-server

# Sur le serveur de support
ssh -p 2222 client-user@localhost

# Maintenant vous avez accès à la machine du client
```

### Tunnel SSH persistant au démarrage

```bash
# ~/.ssh/config
Host tunnel
    HostName server.example.com
    User tunneluser
    IdentityFile ~/.ssh/tunnel_key
    LocalForward 5432 db.internal:5432
    LocalForward 6379 redis.internal:6379
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ExitOnForwardFailure yes

# Script de démarrage
#!/bin/bash
# start-tunnels.sh
ssh -f -N tunnel

# Service systemd
[Unit]
Description=SSH Tunnels
After=network.target

[Service]
Type=forking
User=myuser
ExecStart=/usr/bin/ssh -f -N tunnel
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Multiplexing

```bash
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m

# Créer le répertoire
mkdir -p ~/.ssh/sockets

# Première connexion crée le master
ssh user@server

# Connexions suivantes réutilisent le master (plus rapides)
ssh user@server
scp file.txt user@server:/tmp/

# Voir les connexions actives
ssh -O check user@server

# Fermer le master
ssh -O exit user@server

# Avantages:
# - Connexions plus rapides
# - Pas de ré-authentification
# - Partage de tunnel
```

## Troubleshooting

```bash
# Tunnel ne fonctionne pas
# Vérifier que le forwarding est autorisé
# /etc/ssh/sshd_config
AllowTcpForwarding yes
# Pour remote:
GatewayPorts yes

# Port déjà utilisé
lsof -i :8080
# Choisir un autre port ou tuer le processus

# Connection dropped
# Utiliser ServerAliveInterval
ssh -o "ServerAliveInterval=30" -L 8080:localhost:80 user@server

# Ou dans config:
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Test de tunnel local
ssh -v -L 8080:localhost:80 user@server
# Vérifier la sortie verbose

# Tunnel remote ne fonctionne pas
# Vérifier GatewayPorts côté serveur
sudo sshd -T | grep gatewayports

# Voir les forwards actifs
netstat -tlnp | grep ssh
ss -tlnp | grep ssh
```

## Sécurité

```bash
# ⚠️ Risques du tunneling:

# 1. Bypass de firewall/proxy d'entreprise
# Peut violer les politiques de sécurité

# 2. GatewayPorts yes expose les services
# Limiter avec:
GatewayPorts clientspecified

# 3. Dynamic forwarding = proxy ouvert
# Utiliser authentification et limitation

# 4. Tunnels persistants oubliés
# Auditer régulièrement:
ps aux | grep ssh | grep '\-[LRD]'

# ✅ Bonnes pratiques:
# - Utiliser des clés SSH différentes pour tunnels
# - Limiter le forwarding par utilisateur (Match)
# - Logger les tunnels
# - Utiliser autossh pour stability
# - Fermer les tunnels quand inutilisés
# - Ne pas utiliser GatewayPorts yes en production
```

[← Authentification avancée](./infos-ssh-04-authentification-avancee.md) | [Index](./infos-ssh-00-index.md) | [Transfert de fichiers →](./infos-ssh-06-transfert-fichiers.md)

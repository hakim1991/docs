# 🚀 Introduction et Installation Nginx

[Index](./infos-nginx-00-index.md) | [Configuration de base →](./infos-nginx-02-configuration-base.md)

---

## Qu'est-ce que Nginx ?

**Nginx** (prononcé "engine-x") est un serveur web haute performance, reverse proxy, load balancer et cache HTTP.

### Caractéristiques principales

```
✅ Performance exceptionnelle
✅ Faible consommation de ressources
✅ Architecture asynchrone event-driven
✅ Gestion de milliers de connexions simultanées
✅ Reverse proxy et load balancing
✅ Cache HTTP
✅ Support HTTP/2 et HTTP/3 (QUIC)
✅ SSL/TLS termination
```

### Cas d'usage

```
🌐 Serveur web statique
🔄 Reverse proxy (Node.js, Python, PHP-FPM)
⚖️  Load balancer
💾 Cache HTTP
🔒 SSL/TLS termination
📱 API Gateway
```

---

## Installation sur Linux

### Ubuntu / Debian

```bash
# Mettre à jour les paquets
sudo apt update

# Installer Nginx
sudo apt install -y nginx

# Vérifier l'installation
nginx -v
# nginx version: nginx/1.18.0 (Ubuntu)

# Démarrer Nginx
sudo systemctl start nginx

# Activer au démarrage
sudo systemctl enable nginx

# Vérifier le statut
sudo systemctl status nginx
```

### Installation depuis le dépôt officiel Nginx

```bash
# Ajouter la clé GPG
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg

# Ajouter le dépôt
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list

# Installer
sudo apt update
sudo apt install -y nginx

# Version plus récente disponible
nginx -v
```

### CentOS / RHEL / Fedora

```bash
# CentOS/RHEL
sudo yum install -y epel-release
sudo yum install -y nginx

# Ou depuis le dépôt officiel
sudo yum install -y yum-utils
sudo tee /etc/yum.repos.d/nginx.repo <<EOF
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/\$releasever/\$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
EOF

sudo yum install -y nginx

# Démarrer et activer
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Installation sur Windows

### Téléchargement

```powershell
# Télécharger depuis nginx.org
# http://nginx.org/en/download.html

# Ou avec curl (PowerShell)
curl -O http://nginx.org/download/nginx-1.24.0.zip

# Extraire
Expand-Archive nginx-1.24.0.zip -DestinationPath C:\nginx

# Aller dans le dossier
cd C:\nginx\nginx-1.24.0
```

### Démarrage sur Windows

```cmd
REM Démarrer Nginx
start nginx

REM Arrêter Nginx
nginx -s stop

REM Reload gracieux
nginx -s reload

REM Quit gracieux
nginx -s quit

REM Tester la configuration
nginx -t
```

### Service Windows

```powershell
# Avec NSSM (Non-Sucking Service Manager)
# Télécharger depuis https://nssm.cc/download

# Installer le service
nssm install nginx "C:\nginx\nginx.exe"

# Démarrer le service
nssm start nginx

# Arrêter
nssm stop nginx

# Gérer avec services.msc
services.msc
```

---

## Compilation depuis les sources

### Prérequis

```bash
# Ubuntu/Debian
sudo apt install -y build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev

# CentOS/RHEL
sudo yum install -y gcc gcc-c++ make pcre-devel zlib-devel openssl-devel gd-devel
```

### Compilation

```bash
# Télécharger Nginx
cd /tmp
wget http://nginx.org/download/nginx-1.24.0.tar.gz
tar -xzf nginx-1.24.0.tar.gz
cd nginx-1.24.0

# Configuration
./configure \
  --prefix=/etc/nginx \
  --sbin-path=/usr/sbin/nginx \
  --conf-path=/etc/nginx/nginx.conf \
  --error-log-path=/var/log/nginx/error.log \
  --http-log-path=/var/log/nginx/access.log \
  --pid-path=/var/run/nginx.pid \
  --lock-path=/var/run/nginx.lock \
  --http-client-body-temp-path=/var/cache/nginx/client_temp \
  --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
  --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
  --user=nginx \
  --group=nginx \
  --with-http_ssl_module \
  --with-http_v2_module \
  --with-http_realip_module \
  --with-http_addition_module \
  --with-http_sub_module \
  --with-http_dav_module \
  --with-http_flv_module \
  --with-http_mp4_module \
  --with-http_gunzip_module \
  --with-http_gzip_static_module \
  --with-http_random_index_module \
  --with-http_secure_link_module \
  --with-http_stub_status_module \
  --with-http_auth_request_module \
  --with-threads \
  --with-stream \
  --with-stream_ssl_module \
  --with-http_slice_module \
  --with-file-aio

# Compilation
make

# Installation
sudo make install

# Créer l'utilisateur nginx
sudo useradd -r -M -s /sbin/nologin nginx

# Créer les dossiers
sudo mkdir -p /var/cache/nginx/client_temp
sudo mkdir -p /var/cache/nginx/proxy_temp
sudo mkdir -p /var/cache/nginx/fastcgi_temp

# Permissions
sudo chown -R nginx:nginx /var/cache/nginx/
```

### Service systemd

```bash
# Créer le fichier de service
sudo tee /lib/systemd/system/nginx.service <<EOF
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/var/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s QUIT \$MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Recharger systemd
sudo systemctl daemon-reload

# Activer et démarrer
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## Première configuration

### Structure des fichiers

```
/etc/nginx/
├── nginx.conf                 # Configuration principale
├── conf.d/                    # Configurations incluses
│   └── default.conf
├── sites-available/           # Sites disponibles (Ubuntu/Debian)
│   └── default
├── sites-enabled/             # Sites activés (symlinks)
│   └── default -> ../sites-available/default
├── snippets/                  # Fragments réutilisables
├── mime.types                 # Types MIME
└── modules-enabled/           # Modules activés
```

### Configuration minimale

```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    tcp_nopush     on;
    keepalive_timeout  65;
    gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

### Premier site web

```nginx
# /etc/nginx/conf.d/default.conf (ou sites-available/default)
server {
    listen 80;
    listen [::]:80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;

    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### Page HTML de test

```bash
# Créer une page d'accueil
sudo tee /usr/share/nginx/html/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Nginx fonctionne !</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 100px;
        }
        h1 { color: #009639; }
    </style>
</head>
<body>
    <h1>✅ Nginx fonctionne correctement !</h1>
    <p>Si vous voyez cette page, Nginx est installé et fonctionne.</p>
</body>
</html>
EOF
```

---

## Commandes de base

### Gestion du service

```bash
# Démarrer Nginx
sudo systemctl start nginx

# Arrêter Nginx
sudo systemctl stop nginx

# Redémarrer Nginx
sudo systemctl restart nginx

# Recharger la configuration (sans interruption)
sudo systemctl reload nginx
# ou
sudo nginx -s reload

# Statut
sudo systemctl status nginx

# Activer au démarrage
sudo systemctl enable nginx

# Désactiver au démarrage
sudo systemctl disable nginx
```

### Test de configuration

```bash
# Tester la syntaxe
sudo nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Afficher la configuration complète
sudo nginx -T

# Afficher la version
nginx -v
# nginx version: nginx/1.24.0

# Afficher version + modules compilés
nginx -V
```

### Signaux Nginx

```bash
# Reload gracieux
sudo nginx -s reload

# Arrêt rapide
sudo nginx -s stop

# Arrêt gracieux (attend la fin des requêtes)
sudo nginx -s quit

# Réouverture des logs
sudo nginx -s reopen
```

### Logs

```bash
# Logs en temps réel
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Dernières lignes
sudo tail -n 100 /var/log/nginx/access.log

# Recherche dans les logs
sudo grep "404" /var/log/nginx/access.log
sudo grep "error" /var/log/nginx/error.log
```

---

## Vérification de l'installation

### Test depuis le serveur

```bash
# Avec curl
curl http://localhost

# Avec wget
wget -O- http://localhost

# Vérifier le port
sudo netstat -tulpn | grep nginx
# ou
sudo ss -tulpn | grep nginx

# Résultat attendu:
# tcp   0   0 0.0.0.0:80   0.0.0.0:*   LISTEN   1234/nginx: master
```

### Test depuis un navigateur

```
http://localhost
http://<IP_du_serveur>

# Si tout fonctionne:
# Vous devriez voir la page Nginx par défaut
# ou votre page personnalisée
```

### Firewall

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw allow 'Nginx Full'  # HTTP + HTTPS

# Ou par port
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Ou par port
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
```

---

## Troubleshooting installation

### Nginx ne démarre pas

```bash
# Vérifier les erreurs
sudo systemctl status nginx -l
sudo journalctl -u nginx -n 50

# Vérifier la configuration
sudo nginx -t

# Vérifier les permissions
ls -la /var/log/nginx/
ls -la /var/run/nginx.pid

# Vérifier si le port 80 est libre
sudo netstat -tulpn | grep :80
# ou
sudo ss -tulpn | grep :80

# Tuer les processus sur le port 80 si nécessaire
sudo fuser -k 80/tcp
```

### Permission denied

```bash
# Vérifier l'utilisateur Nginx
ps aux | grep nginx

# Vérifier les permissions du dossier web
ls -la /usr/share/nginx/html/

# Corriger si nécessaire
sudo chown -R nginx:nginx /usr/share/nginx/html/
sudo chmod -R 755 /usr/share/nginx/html/
```

### Erreur 13: Permission denied (logs)

```bash
# Créer les dossiers de logs
sudo mkdir -p /var/log/nginx

# Permissions
sudo chown -R nginx:nginx /var/log/nginx/
sudo chmod -R 755 /var/log/nginx/

# SELinux (CentOS/RHEL)
sudo setsebool -P httpd_can_network_connect 1
sudo chcon -R -t httpd_log_t /var/log/nginx/
```

---

## Best practices installation

```bash
# ✅ Toujours tester la configuration avant reload
sudo nginx -t && sudo systemctl reload nginx

# ✅ Utiliser systemctl reload plutôt que restart
# (reload ne coupe pas les connexions)
sudo systemctl reload nginx

# ✅ Vérifier les logs après changements
sudo tail -f /var/log/nginx/error.log

# ✅ Activer au démarrage
sudo systemctl enable nginx

# ✅ Sauvegarder la config avant modifications
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# ✅ Utiliser la version du dépôt officiel pour
# les dernières features et correctifs de sécurité
```

---

## Commandes de référence rapide

```bash
# Installation
sudo apt install nginx              # Ubuntu/Debian
sudo yum install nginx              # CentOS/RHEL

# Service
sudo systemctl start nginx          # Démarrer
sudo systemctl stop nginx           # Arrêter
sudo systemctl reload nginx         # Recharger
sudo systemctl status nginx         # Statut

# Configuration
sudo nginx -t                       # Tester
sudo nginx -T                       # Afficher config complète
nginx -v                            # Version
nginx -V                            # Version + modules

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

[Index](./infos-nginx-00-index.md) | [Configuration de base →](./infos-nginx-02-configuration-base.md)

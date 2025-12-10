# ⚙️ Configuration de Base Nginx

[← Introduction](./infos-nginx-01-introduction-installation.md) | [Index](./infos-nginx-00-index.md) | [Fichiers statiques →](./infos-nginx-03-fichiers-statiques.md)

## Structure de configuration

```nginx
# /etc/nginx/nginx.conf - Configuration principale

# Contexte MAIN - Configuration globale
user nginx;
worker_processes auto;  # auto = nombre de CPU
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

# Contexte EVENTS - Gestion des connexions
events {
    worker_connections 1024;    # Max connexions par worker
    use epoll;                  # Méthode efficace sur Linux
    multi_accept on;            # Accepter plusieurs connexions à la fois
}

# Contexte HTTP - Configuration HTTP
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logs
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent"';
    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    # Contexte SERVER - Configuration d'un serveur virtuel
    server {
        listen 80;
        server_name example.com;
        root /var/www/html;
        index index.html;

        # Contexte LOCATION - Configuration d'une route
        location / {
            try_files $uri $uri/ =404;
        }
    }

    # Inclure les configurations additionnelles
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

## Directives essentielles

```nginx
# worker_processes: nombre de processus workers
worker_processes auto;              # auto = CPU cores
worker_processes 4;                 # Fixe à 4

# worker_connections: connexions max par worker
worker_connections 1024;            # Total = workers × connections

# server_name: nom(s) du serveur
server_name example.com;                        # Un domaine
server_name example.com www.example.com;        # Plusieurs domaines
server_name *.example.com;                      # Wildcard
server_name ~^www\d+\.example\.com$;           # Regex

# listen: port d'écoute
listen 80;                          # IPv4 port 80
listen [::]:80;                     # IPv6 port 80
listen 443 ssl http2;               # HTTPS avec HTTP/2
listen 8080 default_server;         # Port custom + serveur par défaut

# root: racine des fichiers
root /var/www/html;
root /usr/share/nginx/html;

# index: fichiers index par défaut
index index.html index.htm;
index index.php index.html;

# try_files: essayer plusieurs fichiers
try_files $uri $uri/ =404;
try_files $uri $uri/ /index.html;
try_files $uri $uri/ /index.php?$query_string;
```

## Variables Nginx

```nginx
# Variables courantes
$uri                # URI de la requête (/path/to/page)
$request_uri        # URI complète avec query string
$args               # Query string (?param=value)
$query_string       # Alias de $args
$request_method     # GET, POST, etc.
$host               # Nom d'hôte de la requête
$remote_addr        # IP du client
$remote_port        # Port du client
$server_name        # Nom du serveur
$server_port        # Port du serveur
$scheme             # http ou https
$request_time       # Temps de traitement en secondes
$status             # Code de statut HTTP
$body_bytes_sent    # Bytes envoyés (body)

# Utilisation des variables
location /api {
    add_header X-Request-URI $request_uri;
    add_header X-Real-IP $remote_addr;
    proxy_pass http://backend$request_uri;
}
```

## Includes et modularité

```nginx
# nginx.conf
http {
    # Inclure types MIME
    include /etc/nginx/mime.types;

    # Inclure toutes les configs du dossier conf.d
    include /etc/nginx/conf.d/*.conf;

    # Inclure sites activés
    include /etc/nginx/sites-enabled/*;
}

# Créer des snippets réutilisables
# /etc/nginx/snippets/ssl-params.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;

# Utilisation
server {
    listen 443 ssl;
    include snippets/ssl-params.conf;
}
```

## Commandes de référence

```bash
# Tester la configuration
sudo nginx -t

# Recharger après modification
sudo nginx -s reload
# ou
sudo systemctl reload nginx

# Voir la configuration complète
sudo nginx -T

# Trouver le fichier de configuration
nginx -V 2>&1 | grep -o '\-\-conf-path=\S*'
```

[← Introduction](./infos-nginx-01-introduction-installation.md) | [Index](./infos-nginx-00-index.md) | [Fichiers statiques →](./infos-nginx-03-fichiers-statiques.md)

# 🌐 Virtual Hosts (Server Blocks)

[← Fichiers statiques](./infos-nginx-03-fichiers-statiques.md) | [Index](./infos-nginx-00-index.md) | [Reverse Proxy →](./infos-nginx-05-reverse-proxy.md)

## Concept de Virtual Hosts

Les Virtual Hosts (appelés **Server Blocks** dans Nginx) permettent d'héberger plusieurs sites sur un seul serveur.

## Virtual Host simple

```nginx
# /etc/nginx/sites-available/site1.com

server {
    listen 80;
    listen [::]:80;

    server_name site1.com www.site1.com;

    root /var/www/site1;
    index index.html;

    access_log /var/log/nginx/site1.access.log;
    error_log /var/log/nginx/site1.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/site1.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Plusieurs sites sur le même serveur

```nginx
# /etc/nginx/sites-available/site1.com
server {
    listen 80;
    server_name site1.com www.site1.com;
    root /var/www/site1;
    index index.html;
}

# /etc/nginx/sites-available/site2.com
server {
    listen 80;
    server_name site2.com www.site2.com;
    root /var/www/site2;
    index index.html;
}

# /etc/nginx/sites-available/site3.com
server {
    listen 80;
    server_name site3.com www.site3.com;
    root /var/www/site3;
    index index.html;
}
```

## Server name matching

```nginx
# Correspondance exacte
server {
    server_name example.com;
}

# Plusieurs noms
server {
    server_name example.com www.example.com;
}

# Wildcard au début
server {
    server_name *.example.com;
    # Match: sub.example.com, api.example.com
}

# Wildcard à la fin
server {
    server_name example.*;
    # Match: example.com, example.net, example.org
}

# Regex (commence par ~)
server {
    server_name ~^www\d+\.example\.com$;
    # Match: www1.example.com, www2.example.com
}

# Ordre de priorité:
# 1. Nom exact
# 2. Wildcard au début (*.example.com)
# 3. Wildcard à la fin (example.*)
# 4. Regex (dans l'ordre de déclaration)
# 5. default_server
```

## Serveur par défaut

```nginx
# Serveur par défaut (catch-all)
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    # Retourner 444 (fermer connexion)
    return 444;

    # Ou rediriger
    # return 301 https://www.example.com$request_uri;

    # Ou servir une page par défaut
    # root /var/www/default;
}
```

## Sous-domaines

```nginx
# Sous-domaine principal
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
}

# Blog
server {
    listen 80;
    server_name blog.example.com;
    root /var/www/blog.example.com;
}

# API
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:3000;
    }
}

# Admin
server {
    listen 80;
    server_name admin.example.com;

    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;

    root /var/www/admin.example.com;
}

# Wildcard pour tous les sous-domaines
server {
    listen 80;
    server_name *.example.com;

    root /var/www/subdomains/$host;
    # $host = nom du sous-domaine
}
```

## Multi-tenant avec wildcard

```nginx
# Héberger plusieurs clients avec sous-domaines
server {
    listen 80;
    server_name ~^(?<subdomain>.+)\.example\.com$;

    root /var/www/clients/$subdomain;
    index index.html;

    # Log par client
    access_log /var/log/nginx/$subdomain.access.log;
    error_log /var/log/nginx/$subdomain.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Configuration avec includes

```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/example.com;
    index index.php index.html;

    # Include configurations communes
    include /etc/nginx/snippets/common-locations.conf;
    include /etc/nginx/snippets/php-fpm.conf;
}

# /etc/nginx/snippets/common-locations.conf
location = /favicon.ico {
    log_not_found off;
    access_log off;
}

location = /robots.txt {
    log_not_found off;
    access_log off;
}

location ~ /\. {
    deny all;
}

# /etc/nginx/snippets/php-fpm.conf
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_index index.php;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

## Redirection www

```nginx
# Rediriger www vers non-www
server {
    listen 80;
    server_name www.example.com;
    return 301 http://example.com$request_uri;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/example.com;
}

# Ou l'inverse (non-www vers www)
server {
    listen 80;
    server_name example.com;
    return 301 http://www.example.com$request_uri;
}

server {
    listen 80;
    server_name www.example.com;
    root /var/www/example.com;
}
```

## HTTP vers HTTPS

```nginx
# Rediriger tout le HTTP vers HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name example.com www.example.com;

    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;

    root /var/www/example.com;
}
```

## Plusieurs ports

```nginx
# Site sur plusieurs ports
server {
    listen 80;
    listen 8080;
    listen 8888;

    server_name example.com;
    root /var/www/example.com;
}

# Comportement différent par port
server {
    listen 80;
    server_name example.com;

    location / {
        root /var/www/public;
    }
}

server {
    listen 8080;
    server_name example.com;

    auth_basic "Admin";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        root /var/www/admin;
    }
}
```

## IP-based Virtual Hosts

```nginx
# Site 1 sur IP 192.168.1.10
server {
    listen 192.168.1.10:80;
    server_name _;

    root /var/www/site1;
}

# Site 2 sur IP 192.168.1.11
server {
    listen 192.168.1.11:80;
    server_name _;

    root /var/www/site2;
}

# Combination IP + nom
server {
    listen 192.168.1.10:80;
    server_name example.com;

    root /var/www/example.com;
}
```

## Configuration par environnement

```nginx
# Développement
server {
    listen 80;
    server_name dev.example.com localhost;

    root /var/www/dev;

    # Afficher les erreurs PHP
    fastcgi_param PHP_VALUE "display_errors=On";

    # Pas de cache
    expires -1;
    add_header Cache-Control "no-store, no-cache";
}

# Staging
server {
    listen 80;
    server_name staging.example.com;

    root /var/www/staging;

    # Authentification basique
    auth_basic "Staging";
    auth_basic_user_file /etc/nginx/.htpasswd;
}

# Production
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    root /var/www/prod;

    # Cache activé
    location ~* \.(jpg|jpeg|png|gif|css|js)$ {
        expires 30d;
    }

    # HTTPS strict
    add_header Strict-Transport-Security "max-age=31536000" always;
}
```

## Sites avec chemins personnalisés

```nginx
# Structure de projet
# /var/www/
# ├── site1/
# │   ├── public/
# │   ├── storage/
# │   └── logs/
# └── site2/
#     ├── public/
#     ├── storage/
#     └── logs/

server {
    listen 80;
    server_name site1.com;

    root /var/www/site1/public;

    access_log /var/www/site1/logs/access.log;
    error_log /var/www/site1/logs/error.log;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }
}
```

## Template de Virtual Host

```nginx
# /etc/nginx/templates/vhost.template

server {
    listen 80;
    listen [::]:80;

    server_name DOMAIN www.DOMAIN;

    root /var/www/DOMAIN;
    index index.html index.htm index.php;

    access_log /var/log/nginx/DOMAIN.access.log;
    error_log /var/log/nginx/DOMAIN.error.log;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

```bash
# Script pour créer un nouveau vhost
#!/bin/bash
# create-vhost.sh

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 domain.com"
    exit 1
fi

# Créer répertoire
sudo mkdir -p /var/www/$DOMAIN

# Créer config depuis template
sudo sed "s/DOMAIN/$DOMAIN/g" /etc/nginx/templates/vhost.template \
    > /etc/nginx/sites-available/$DOMAIN

# Activer
sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/

# Tester et recharger
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Vhost créé: $DOMAIN"
```

## Gestion des Virtual Hosts

```bash
# Lister les sites disponibles
ls -la /etc/nginx/sites-available/

# Lister les sites actifs
ls -la /etc/nginx/sites-enabled/

# Activer un site
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/

# Désactiver un site
sudo rm /etc/nginx/sites-enabled/example.com

# Tester la config
sudo nginx -t

# Recharger Nginx
sudo systemctl reload nginx

# Voir la config d'un site
sudo nginx -T | grep -A 50 "server_name example.com"
```

## Troubleshooting

```bash
# Vérifier quel serveur gère une requête
curl -H "Host: example.com" http://localhost/

# Voir les server names actifs
sudo nginx -T | grep "server_name"

# Tester avec verbose
curl -v http://example.com/

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Voir quelle config est chargée
sudo nginx -T | grep "include"
```

[← Fichiers statiques](./infos-nginx-03-fichiers-statiques.md) | [Index](./infos-nginx-00-index.md) | [Reverse Proxy →](./infos-nginx-05-reverse-proxy.md)

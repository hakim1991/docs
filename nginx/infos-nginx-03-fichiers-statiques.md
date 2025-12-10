# 📁 Servir des fichiers statiques

[← Configuration base](./infos-nginx-02-configuration-base.md) | [Index](./infos-nginx-00-index.md) | [Virtual Hosts →](./infos-nginx-04-virtual-hosts.md)

## Serveur de fichiers statiques simple

```nginx
server {
    listen 80;
    server_name static.example.com;

    root /var/www/static;
    index index.html;

    # Servir les fichiers directement
    location / {
        try_files $uri $uri/ =404;
    }

    # Logs
    access_log /var/log/nginx/static.access.log;
    error_log /var/log/nginx/static.error.log;
}
```

## Types de fichiers

```nginx
server {
    listen 80;
    server_name files.example.com;
    root /var/www/files;

    # HTML et texte
    location ~* \.(html|htm|txt)$ {
        add_header Content-Type text/html;
    }

    # Images
    location ~* \.(jpg|jpeg|png|gif|ico|svg|webp)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # CSS et JavaScript
    location ~* \.(css|js)$ {
        expires 7d;
        add_header Cache-Control "public";
    }

    # Fonts
    location ~* \.(woff|woff2|ttf|otf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Access-Control-Allow-Origin *;
    }

    # Documents
    location ~* \.(pdf|doc|docx|xls|xlsx|ppt|pptx)$ {
        add_header Content-Disposition "attachment";
    }

    # Vidéos
    location ~* \.(mp4|webm|ogg|mp3)$ {
        expires 30d;
        mp4;  # Enable streaming
    }
}
```

## Cache des fichiers statiques

```nginx
server {
    listen 80;
    server_name cdn.example.com;
    root /var/www/cdn;

    # Pas de cache pour HTML
    location ~* \.html$ {
        expires -1;
        add_header Cache-Control "no-store, no-cache, must-revalidate";
    }

    # Cache court pour CSS/JS (versionnés)
    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Cache long pour images
    location ~* \.(jpg|jpeg|png|gif|webp|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Ajouter ETag
    etag on;
}
```

## Compression Gzip

```nginx
http {
    # Activer gzip
    gzip on;

    # Compression minimum
    gzip_min_length 1000;

    # Niveau de compression (1-9)
    gzip_comp_level 6;

    # Types à compresser
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/xml
        image/svg+xml;

    # Vary header
    gzip_vary on;

    # Proxy settings
    gzip_proxied any;

    # Désactiver pour IE6
    gzip_disable "msie6";

    server {
        listen 80;
        root /var/www/html;

        # Désactiver gzip pour certains fichiers
        location ~* \.(jpg|jpeg|png|gif|ico)$ {
            gzip off;
        }
    }
}
```

## Brotli (compression moderne)

```nginx
# Installer module
# sudo apt install nginx-module-brotli

load_module modules/ngx_http_brotli_filter_module.so;
load_module modules/ngx_http_brotli_static_module.so;

http {
    # Activer Brotli
    brotli on;
    brotli_comp_level 6;
    brotli_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/xml
        image/svg+xml;

    # Brotli statique (fichiers .br pré-compressés)
    brotli_static on;
}
```

## Autoindex (liste de fichiers)

```nginx
server {
    listen 80;
    server_name files.example.com;
    root /var/www/downloads;

    location / {
        # Activer l'autoindex
        autoindex on;

        # Format HTML (par défaut)
        autoindex_format html;

        # Afficher tailles exactes (off) ou humaines (on)
        autoindex_exact_size off;

        # Heure locale au lieu de UTC
        autoindex_localtime on;
    }

    # Autoindex JSON
    location /api/ {
        autoindex on;
        autoindex_format json;
    }

    # Désactiver pour certains dossiers
    location /private/ {
        autoindex off;
        deny all;
    }
}
```

## Téléchargements

```nginx
server {
    listen 80;
    server_name download.example.com;
    root /var/www/downloads;

    # Force le téléchargement
    location /files/ {
        add_header Content-Disposition "attachment";
    }

    # Téléchargement avec nom personnalisé
    location ~ ^/download/(.+)$ {
        alias /var/www/files/$1;
        add_header Content-Disposition "attachment; filename=\"$1\"";
    }

    # Limite de vitesse de téléchargement
    location /slow/ {
        limit_rate 100k;  # 100 KB/s
        limit_rate_after 5m;  # Après 5 MB
    }

    # X-Accel-Redirect (téléchargement via backend)
    location /secure/ {
        internal;
        alias /var/www/secure/;
    }
}
```

## Range requests (streaming)

```nginx
server {
    listen 80;
    server_name video.example.com;
    root /var/www/videos;

    # Support des range requests
    location / {
        # Activer par défaut
        # Nginx supporte automatiquement
    }

    # Pour MP4
    location ~ \.mp4$ {
        mp4;
        mp4_buffer_size 1m;
        mp4_max_buffer_size 5m;
    }

    # Pour FLV
    location ~ \.flv$ {
        flv;
    }
}
```

## CORS pour fichiers statiques

```nginx
server {
    listen 80;
    server_name cdn.example.com;
    root /var/www/cdn;

    # CORS pour tous
    location / {
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Origin, Content-Type";

        # Preflight
        if ($request_method = OPTIONS) {
            return 204;
        }
    }

    # CORS restreint
    location /restricted/ {
        if ($http_origin ~* (https://example\.com|https://app\.example\.com)) {
            add_header Access-Control-Allow-Origin $http_origin;
        }
    }

    # CORS pour fonts
    location ~* \.(woff|woff2|ttf|otf)$ {
        add_header Access-Control-Allow-Origin *;
    }
}
```

## Sécurité des fichiers statiques

```nginx
server {
    listen 80;
    server_name secure-files.example.com;
    root /var/www/secure;

    # Interdire fichiers cachés
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Interdire fichiers sensibles
    location ~* (\.git|\.svn|\.env|\.htaccess|\.htpasswd)$ {
        deny all;
    }

    # Interdire exécution PHP dans uploads
    location /uploads/ {
        location ~ \.php$ {
            deny all;
        }
    }

    # Headers de sécurité
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

## Fallback images

```nginx
server {
    listen 80;
    server_name img.example.com;
    root /var/www/images;

    # Image par défaut si introuvable
    location / {
        try_files $uri $uri/ /default.jpg;
    }

    # Ou avec error_page
    location / {
        error_page 404 /404.jpg;
    }

    # Named location
    location / {
        try_files $uri @fallback;
    }

    location @fallback {
        rewrite .* /placeholder.png break;
    }
}
```

## CDN statique avec sous-domaines

```nginx
# cdn1.example.com
server {
    listen 80;
    server_name cdn1.example.com;
    root /var/www/cdn;

    location / {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# cdn2.example.com
server {
    listen 80;
    server_name cdn2.example.com;
    root /var/www/cdn;

    location / {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# cdn3.example.com
server {
    listen 80;
    server_name cdn3.example.com;
    root /var/www/cdn;

    location / {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## SPA (Single Page Application)

```nginx
server {
    listen 80;
    server_name app.example.com;
    root /var/www/spa/dist;
    index index.html;

    # Toutes les routes vers index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Fichiers statiques avec cache
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:3000;
    }
}
```

## WebP avec fallback

```nginx
server {
    listen 80;
    server_name images.example.com;
    root /var/www/images;

    # WebP si supporté
    location ~ \.(png|jpg|jpeg)$ {
        add_header Vary Accept;

        # Si le client supporte WebP
        if ($http_accept ~* "webp") {
            rewrite ^(.*)\.(?:png|jpg|jpeg)$ $1.webp break;
        }

        try_files $uri $uri.webp $uri =404;
    }
}
```

## Optimisation performance

```nginx
server {
    listen 80;
    server_name fast.example.com;
    root /var/www/fast;

    # Sendfile
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;

    # Open file cache
    open_file_cache max=10000 inactive=30s;
    open_file_cache_valid 60s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    # Disable access log for static files
    location ~* \.(jpg|jpeg|png|gif|css|js|ico|svg)$ {
        access_log off;
        expires 30d;
    }
}
```

## Structure recommandée

```bash
/var/www/
├── monsite/
│   ├── public/           # Fichiers publics
│   │   ├── index.html
│   │   ├── assets/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   └── uploads/
│   └── private/          # Fichiers privés (hors root)
│       ├── config/
│       └── logs/
```

```nginx
server {
    listen 80;
    server_name example.com;

    # Root sur public uniquement
    root /var/www/monsite/public;

    # Servir depuis root
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Les fichiers private ne sont pas accessibles
    # Car ils sont hors du root
}
```

[← Configuration base](./infos-nginx-02-configuration-base.md) | [Index](./infos-nginx-00-index.md) | [Virtual Hosts →](./infos-nginx-04-virtual-hosts.md)

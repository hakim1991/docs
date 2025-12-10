# 🔄 Reverse Proxy

[← Virtual Hosts](./infos-nginx-04-virtual-hosts.md) | [Index](./infos-nginx-00-index.md) | [Load Balancing →](./infos-nginx-06-load-balancing.md)

## Concept de Reverse Proxy

Un reverse proxy reçoit les requêtes des clients et les transmet à des serveurs backend, puis renvoie la réponse au client.

```
Client → Nginx (Reverse Proxy) → Backend Server
       ← Nginx                  ← Backend Server
```

## Configuration basique

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        # Proxy vers backend
        proxy_pass http://localhost:3000;
    }
}
```

## Proxy headers

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;

        # Headers importants
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
    }
}
```

## Snippet de configuration proxy

```nginx
# /etc/nginx/snippets/proxy-params.conf
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;

# Utilisation
server {
    listen 80;
    server_name example.com;

    location / {
        include snippets/proxy-params.conf;
        proxy_pass http://localhost:3000;
    }
}
```

## Proxy vers différents backends

```nginx
server {
    listen 80;
    server_name example.com;

    # Frontend (React, Vue, etc.)
    location / {
        proxy_pass http://localhost:3000;
        include snippets/proxy-params.conf;
    }

    # API backend
    location /api/ {
        proxy_pass http://localhost:8080;
        include snippets/proxy-params.conf;
    }

    # Admin backend
    location /admin/ {
        proxy_pass http://localhost:8081;
        include snippets/proxy-params.conf;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Proxy avec chemin modifié

```nginx
# Supprimer le préfixe
location /api/ {
    # /api/users → http://backend/users
    proxy_pass http://localhost:8080/;
}

# Garder le préfixe
location /api/ {
    # /api/users → http://backend/api/users
    proxy_pass http://localhost:8080;
}

# Remplacer le chemin
location /old-api/ {
    # /old-api/users → http://backend/v2/users
    rewrite ^/old-api/(.*)$ /v2/$1 break;
    proxy_pass http://localhost:8080;
}
```

## Timeouts et buffers

```nginx
location / {
    proxy_pass http://backend;

    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    # Buffers
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;

    # Taille max du corps de requête
    client_max_body_size 10m;
}
```

## Proxy cache

```nginx
http {
    # Définir zone de cache
    proxy_cache_path /var/cache/nginx/proxy
                     levels=1:2
                     keys_zone=my_cache:10m
                     max_size=1g
                     inactive=60m;

    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://backend;

            # Activer le cache
            proxy_cache my_cache;
            proxy_cache_valid 200 302 10m;
            proxy_cache_valid 404 1m;

            # Ajouter header pour voir si cached
            add_header X-Cache-Status $upstream_cache_status;

            # Bypass cache avec paramètre
            proxy_cache_bypass $cookie_nocache $arg_nocache;
        }
    }
}
```

## WebSocket support

```nginx
# Configuration pour WebSocket
location /ws/ {
    proxy_pass http://localhost:3000;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # Timeouts longs pour WebSocket
    proxy_read_timeout 86400;
    proxy_send_timeout 86400;
}

# Map pour Connection header
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }
}
```

## Server-Sent Events (SSE)

```nginx
location /events {
    proxy_pass http://localhost:3000;

    proxy_http_version 1.1;
    proxy_set_header Connection '';

    # Désactiver buffering
    proxy_buffering off;

    # Garder la connexion ouverte
    proxy_read_timeout 24h;

    # Headers nécessaires
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## gRPC proxy

```nginx
server {
    listen 80 http2;
    server_name grpc.example.com;

    location / {
        grpc_pass grpc://localhost:50051;
    }
}

# Avec SSL
server {
    listen 443 ssl http2;
    server_name grpc.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        grpc_pass grpcs://backend:50051;
    }
}
```

## Upstream (groupe de backends)

```nginx
upstream backend {
    server localhost:3000;
    server localhost:3001;
    server localhost:3002;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

## Health checks

```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;

    # Check toutes les 5 secondes
    # 2 échecs = down, 3 succès = up
    check interval=5000 rise=3 fall=2 timeout=1000;
}

# Ou avec module commercial nginx-plus
upstream backend {
    zone backend 64k;
    server backend1:8080;
    server backend2:8080;

    # Health check
    health_check interval=10 fails=3 passes=2;
}
```

## Proxy avec authentification

```nginx
# Authentification côté Nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        # Basic auth
        auth_basic "API Access";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}

# Passer l'auth au backend
server {
    listen 80;
    server_name api.example.com;

    location / {
        # Passer Authorization header
        proxy_set_header Authorization $http_authorization;
        proxy_pass_header Authorization;

        proxy_pass http://backend;
    }
}
```

## Gérer les erreurs backend

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;

        # Intercepter les erreurs
        proxy_intercept_errors on;

        # Pages d'erreur personnalisées
        error_page 502 503 504 /50x.html;
    }

    location = /50x.html {
        root /usr/share/nginx/html;
    }
}

# Failover sur erreur
upstream backend {
    server backend1:8080 max_fails=3 fail_timeout=30s;
    server backup2:8080 backup;
}
```

## Proxy avec SSL vers backend

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        # HTTPS vers backend
        proxy_pass https://backend;

        # Vérifier certificat backend
        proxy_ssl_verify on;
        proxy_ssl_trusted_certificate /path/to/ca.pem;
        proxy_ssl_verify_depth 2;

        # Ou ignorer (pas recommandé en prod)
        # proxy_ssl_verify off;

        include snippets/proxy-params.conf;
    }
}
```

## Rate limiting sur proxy

```nginx
http {
    # Zone de limite
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name api.example.com;

        location /api/ {
            # Appliquer limite
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://backend;
            include snippets/proxy-params.conf;
        }
    }
}
```

## IP whitelisting sur proxy

```nginx
server {
    listen 80;
    server_name admin.example.com;

    location / {
        # Autoriser certaines IPs
        allow 192.168.1.0/24;
        allow 10.0.0.0/8;
        deny all;

        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}

# Ou avec geo
http {
    geo $allowed_ip {
        default 0;
        192.168.1.0/24 1;
        10.0.0.0/8 1;
    }

    server {
        location / {
            if ($allowed_ip = 0) {
                return 403;
            }

            proxy_pass http://backend;
        }
    }
}
```

## Streaming de fichiers volumineux

```nginx
location /downloads/ {
    proxy_pass http://file-server;

    # Désactiver buffering pour streaming
    proxy_buffering off;

    # Pas de limite de taille
    client_max_body_size 0;

    # Timeouts longs
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
}
```

## Proxy avec sticky sessions

```nginx
upstream backend {
    # IP hash pour session persistante
    ip_hash;

    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}

# Ou avec cookie (nginx-plus)
upstream backend {
    server backend1:8080;
    server backend2:8080;

    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

## Logs spécifiques pour proxy

```nginx
# Format de log avec infos proxy
log_format proxy '$remote_addr - $remote_user [$time_local] '
                 '"$request" $status $body_bytes_sent '
                 '"$http_referer" "$http_user_agent" '
                 'upstream: $upstream_addr '
                 'upstream_status: $upstream_status '
                 'request_time: $request_time '
                 'upstream_response_time: $upstream_response_time';

server {
    listen 80;
    server_name example.com;

    access_log /var/log/nginx/proxy.access.log proxy;

    location / {
        proxy_pass http://backend;
    }
}
```

## Cas pratiques

### Application Node.js

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### API Python (FastAPI/Django)

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout pour requêtes longues
        proxy_read_timeout 300;
    }
}
```

### Application Docker

```nginx
server {
    listen 80;
    server_name docker-app.example.com;

    location / {
        # Proxy vers container Docker
        proxy_pass http://172.17.0.2:8080;
        include snippets/proxy-params.conf;
    }
}

# Ou avec docker-compose et réseau
upstream docker_app {
    server app:8080;
}

server {
    location / {
        proxy_pass http://docker_app;
    }
}
```

[← Virtual Hosts](./infos-nginx-04-virtual-hosts.md) | [Index](./infos-nginx-00-index.md) | [Load Balancing →](./infos-nginx-06-load-balancing.md)

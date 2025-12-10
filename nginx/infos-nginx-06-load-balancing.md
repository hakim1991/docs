# ⚖️ Load Balancing

[← Reverse Proxy](./infos-nginx-05-reverse-proxy.md) | [Index](./infos-nginx-00-index.md) | [SSL/HTTPS →](./infos-nginx-07-ssl-https.md)

## Concept de Load Balancing

Le load balancing distribue les requêtes entrantes entre plusieurs serveurs backend pour améliorer la performance et la disponibilité.

## Configuration basique

```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Méthodes de load balancing

### Round Robin (défaut)

```nginx
# Distribution cyclique (par défaut)
upstream backend {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}
# Requête 1 → backend1
# Requête 2 → backend2
# Requête 3 → backend3
# Requête 4 → backend1 (recommence)
```

### Least Connections

```nginx
# Envoie au serveur avec le moins de connexions actives
upstream backend {
    least_conn;

    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}
```

### IP Hash (sticky sessions)

```nginx
# Même client → même serveur (basé sur IP)
upstream backend {
    ip_hash;

    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}
```

### Hash (custom key)

```nginx
# Hash basé sur une clé personnalisée
upstream backend {
    hash $request_uri consistent;

    server backend1:8080;
    server backend2:8080;
}

# Autres exemples de hash
upstream backend {
    hash $cookie_userid;  # Par cookie
}

upstream backend {
    hash $arg_session_id;  # Par paramètre URL
}
```

### Least Time (Nginx Plus)

```nginx
# Envoie au serveur le plus rapide
upstream backend {
    least_time header;  # Basé sur temps de réponse

    server backend1:8080;
    server backend2:8080;
}
```

### Random

```nginx
# Distribution aléatoire
upstream backend {
    random;

    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}

# Random avec 2 choix (plus équilibré)
upstream backend {
    random two least_conn;

    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}
```

## Poids des serveurs

```nginx
upstream backend {
    # backend1 reçoit 3x plus de requêtes
    server backend1:8080 weight=3;
    server backend2:8080 weight=1;
    server backend3:8080 weight=1;
}
```

## Serveurs de backup

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;

    # Utilisé seulement si les autres sont down
    server backup1:8080 backup;
}
```

## Max fails et fail timeout

```nginx
upstream backend {
    # Marquer down après 3 échecs
    # Réessayer après 30 secondes
    server backend1:8080 max_fails=3 fail_timeout=30s;
    server backend2:8080 max_fails=3 fail_timeout=30s;

    # Serveur de backup
    server backup1:8080 backup;
}
```

## Serveurs down

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;

    # Marquer temporairement down (maintenance)
    server backend3:8080 down;
}
```

## Connexions max par serveur

```nginx
upstream backend {
    # Max 100 connexions simultanées par serveur
    server backend1:8080 max_conns=100;
    server backend2:8080 max_conns=100;
}
```

## Slow start (Nginx Plus)

```nginx
upstream backend {
    server backend1:8080;

    # Montée en charge progressive sur 30s
    server backend2:8080 slow_start=30s;
}
```

## Health checks

### Passive health checks

```nginx
# Health checks passifs (par défaut)
upstream backend {
    server backend1:8080 max_fails=3 fail_timeout=30s;
    server backend2:8080 max_fails=3 fail_timeout=30s;
}
# Nginx marque down après échecs réels
```

### Active health checks (Nginx Plus)

```nginx
upstream backend {
    zone backend 64k;

    server backend1:8080;
    server backend2:8080;

    # Health check actif
    health_check interval=10 fails=3 passes=2 uri=/health;
}

server {
    location / {
        proxy_pass http://backend;

        # Retourner 503 si tous les backends sont down
        proxy_next_upstream error timeout invalid_header http_503;
    }
}
```

## Keepalive connections

```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;

    # Garder 32 connexions keepalive
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    location / {
        proxy_pass http://backend;

        # Nécessaire pour keepalive upstream
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Zone partagée

```nginx
# Zone partagée entre workers
upstream backend {
    zone backend 64k;

    server backend1:8080;
    server backend2:8080;
}
```

## Configuration avancée complète

```nginx
upstream backend {
    # Méthode
    least_conn;

    # Zone partagée
    zone backend 64k;

    # Serveurs
    server backend1:8080 weight=3 max_fails=3 fail_timeout=30s max_conns=100;
    server backend2:8080 weight=2 max_fails=3 fail_timeout=30s max_conns=100;
    server backend3:8080 weight=1 max_fails=2 fail_timeout=20s;
    server backup1:8080 backup;

    # Keepalive
    keepalive 32;
    keepalive_timeout 60s;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend;

        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Retry next server on error
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 2;
        proxy_next_upstream_timeout 5s;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

## Load balancing par type de requête

```nginx
# API
upstream api_backend {
    least_conn;
    server api1:8080;
    server api2:8080;
}

# Images
upstream images_backend {
    server img1:8080;
    server img2:8080;
}

# Websocket
upstream ws_backend {
    ip_hash;  # Pour sticky sessions
    server ws1:8080;
    server ws2:8080;
}

server {
    listen 80;
    server_name example.com;

    # Routes API
    location /api/ {
        proxy_pass http://api_backend;
    }

    # Images
    location /images/ {
        proxy_pass http://images_backend;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://ws_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Load balancing avec Docker

```nginx
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app1
      - app2
      - app3

  app1:
    image: myapp:latest
    expose:
      - "3000"

  app2:
    image: myapp:latest
    expose:
      - "3000"

  app3:
    image: myapp:latest
    expose:
      - "3000"
```

```nginx
# nginx.conf
upstream backend {
    server app1:3000;
    server app2:3000;
    server app3:3000;
}

server {
    listen 80;

    location / {
        proxy_pass http://backend;
    }
}
```

## Session persistence (sticky)

```nginx
# Avec IP hash
upstream backend {
    ip_hash;
    server backend1:8080;
    server backend2:8080;
}

# Avec hash sur cookie
upstream backend {
    hash $cookie_jsessionid;
    server backend1:8080;
    server backend2:8080;
}

# Nginx Plus: sticky cookie
upstream backend {
    server backend1:8080;
    server backend2:8080;

    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

## Logs et monitoring

```nginx
# Log format avec info upstream
log_format upstreamlog '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'upstream: $upstream_addr '
                       'upstream_status: $upstream_status '
                       'upstream_response_time: $upstream_response_time '
                       'request_time: $request_time';

server {
    access_log /var/log/nginx/upstream.log upstreamlog;

    location / {
        proxy_pass http://backend;

        # Ajouter headers pour debug
        add_header X-Upstream-Addr $upstream_addr always;
        add_header X-Upstream-Status $upstream_status always;
        add_header X-Upstream-Response-Time $upstream_response_time always;
    }
}
```

## API de stats (Nginx Plus)

```nginx
server {
    listen 8080;

    location /api {
        api write=on;
    }

    location /dashboard.html {
        root /usr/share/nginx/html;
    }
}
```

## Split testing (A/B testing)

```nginx
# 80% vers version A, 20% vers version B
split_clients $remote_addr $backend_variant {
    80%     versionA;
    20%     versionB;
    *       versionA;  # Fallback
}

upstream versionA {
    server app-v1-1:8080;
    server app-v1-2:8080;
}

upstream versionB {
    server app-v2-1:8080;
    server app-v2-2:8080;
}

server {
    location / {
        proxy_pass http://$backend_variant;
    }
}
```

## Canary deployment

```nginx
# 95% production, 5% canary
split_clients $remote_addr $deployment {
    5%      canary;
    *       production;
}

upstream production {
    server prod1:8080;
    server prod2:8080;
    server prod3:8080;
}

upstream canary {
    server canary1:8080;
}

server {
    location / {
        proxy_pass http://$deployment;
    }
}
```

## Geo load balancing

```nginx
# Diriger selon localisation
geo $closest_region {
    default         us;
    1.0.0.0/8       asia;
    2.0.0.0/8       eu;
    192.168.0.0/16  us;
}

upstream us_servers {
    server us1.example.com:8080;
    server us2.example.com:8080;
}

upstream eu_servers {
    server eu1.example.com:8080;
    server eu2.example.com:8080;
}

upstream asia_servers {
    server asia1.example.com:8080;
    server asia2.example.com:8080;
}

server {
    location / {
        proxy_pass http://${closest_region}_servers;
    }
}
```

## Troubleshooting

```bash
# Voir les upstreams actifs
sudo nginx -T | grep -A 10 "upstream"

# Tester manuellement un backend
curl -v http://backend1:8080/

# Voir quel backend répond
curl -v http://example.com/ -H "Host: example.com"

# Logs upstream
sudo tail -f /var/log/nginx/access.log | grep upstream_addr

# Stats en temps réel (si stub_status activé)
curl http://localhost/nginx_status
```

```nginx
# Activer stub_status
server {
    listen 8080;
    location /nginx_status {
        stub_status;
        allow 127.0.0.1;
        deny all;
    }
}
```

[← Reverse Proxy](./infos-nginx-05-reverse-proxy.md) | [Index](./infos-nginx-00-index.md) | [SSL/HTTPS →](./infos-nginx-07-ssl-https.md)

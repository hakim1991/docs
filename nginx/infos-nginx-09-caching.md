# 💾 Caching avec Nginx

[← Sécurité](./infos-nginx-08-securite.md) | [Index](./infos-nginx-00-index.md) | [Optimisation →](./infos-nginx-10-optimisation-performance.md)

## Cache proxy

```nginx
# Configuration du cache
proxy_cache_path /var/cache/nginx/proxy
    levels=1:2
    keys_zone=my_cache:10m
    max_size=1g
    inactive=60m
    use_temp_path=off;

server {
    location / {
        proxy_pass http://backend;

        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        proxy_cache_lock on;

        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

## Cache FastCGI (PHP)

```nginx
fastcgi_cache_path /var/cache/nginx/fastcgi
    levels=1:2
    keys_zone=php_cache:10m
    max_size=1g
    inactive=60m;

server {
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;

        fastcgi_cache php_cache;
        fastcgi_cache_valid 200 60m;
        fastcgi_cache_bypass $skip_cache;
        fastcgi_no_cache $skip_cache;

        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

## Cache statique (Browser cache)

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

location ~* \.(pdf|docx|xlsx)$ {
    expires 7d;
    add_header Cache-Control "public";
}
```

## Purge du cache

```nginx
# Avec ngx_cache_purge module
location ~ /purge(/.*) {
    allow 127.0.0.1;
    deny all;
    proxy_cache_purge my_cache "$scheme$request_method$host$1";
}
```

```bash
# Purger une URL
curl -X PURGE http://localhost/purge/api/users

# Ou purger manuellement
sudo rm -rf /var/cache/nginx/proxy/*
sudo systemctl reload nginx
```

## Cache conditionnel

```nginx
# Ne pas cacher certaines pages
map $request_uri $skip_cache {
    default 0;
    ~*/admin 1;
    ~*/login 1;
    ~*/api/private 1;
}

server {
    location / {
        proxy_cache_bypass $skip_cache;
        proxy_no_cache $skip_cache;
    }
}
```

[← Sécurité](./infos-nginx-08-securite.md) | [Index](./infos-nginx-00-index.md) | [Optimisation →](./infos-nginx-10-optimisation-performance.md)

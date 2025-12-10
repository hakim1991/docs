# ⚡ Optimisation des Performances

[← Caching](./infos-nginx-09-caching.md) | [Index](./infos-nginx-00-index.md) | [Logs →](./infos-nginx-11-logs-monitoring.md)

## Worker processes et connections

```nginx
# Nombre de workers = nombre de CPU cores
worker_processes auto;

# Connexions simultanées par worker
events {
    worker_connections 1024;
    use epoll;  # Linux
    multi_accept on;
}
```

## Buffers et timeouts

```nginx
http {
    # Buffers clients
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;

    # Buffers proxy
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;

    # Timeouts
    client_body_timeout 12;
    client_header_timeout 12;
    keepalive_timeout 65;
    send_timeout 10;

    # Proxy timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

## Keepalive connections

```nginx
upstream backend {
    server backend1.example.com;
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Compression gzip

```nginx
http {
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 1024;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    gzip_disable "msie6";
}
```

## Open file cache

```nginx
http {
    open_file_cache max=10000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;
}
```

## Optimisation TCP

```nginx
http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
}
```

## HTTP/2

```nginx
server {
    listen 443 ssl http2;

    # HTTP/2 settings
    http2_max_field_size 16k;
    http2_max_header_size 32k;
}
```

## Configuration optimale complète

```nginx
user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logs
    access_log /var/log/nginx/access.log;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # Buffers
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;

    # Timeouts
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript;

    # File cache
    open_file_cache max=10000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;

    include /etc/nginx/conf.d/*.conf;
}
```

[← Caching](./infos-nginx-09-caching.md) | [Index](./infos-nginx-00-index.md) | [Logs →](./infos-nginx-11-logs-monitoring.md)

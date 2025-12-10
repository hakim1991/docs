# 📊 Logs et Monitoring

[← Optimisation](./infos-nginx-10-optimisation-performance.md) | [Index](./infos-nginx-00-index.md) | [Troubleshooting →](./infos-nginx-12-troubleshooting.md)

## Configuration des logs

```nginx
http {
    # Format de log personnalisé
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    log_format detailed '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time uct="$upstream_connect_time" '
                       'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;
}

server {
    access_log /var/log/nginx/site-access.log detailed;
    error_log /var/log/nginx/site-error.log;
}
```

## Log rotation

```bash
# /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 nginx adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

## Analyse des logs

```bash
# Voir les logs en temps réel
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Top 10 des IPs
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10

# Top 10 des URLs
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10

# Codes de statut
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# Erreurs 404
grep " 404 " /var/log/nginx/access.log

# Erreurs 5xx
grep " 50[0-9] " /var/log/nginx/access.log
```

## Monitoring avec stub_status

```nginx
server {
    listen 8080;
    location /nginx_status {
        stub_status;
        allow 127.0.0.1;
        deny all;
    }
}
```

```bash
# Consulter les stats
curl http://localhost:8080/nginx_status

# Résultat:
# Active connections: 291
# server accepts handled requests
#  16630948 16630948 31070465
# Reading: 6 Writing: 179 Waiting: 106
```

## Prometheus metrics

```nginx
# Avec nginx-prometheus-exporter
server {
    listen 9113;
    location /metrics {
        stub_status on;
        allow 127.0.0.1;
        deny all;
    }
}
```

```bash
# Installer l'exporter
docker run -d \
    --name nginx-exporter \
    -p 9113:9113 \
    nginx/nginx-prometheus-exporter:latest \
    -nginx.scrape-uri=http://nginx:8080/nginx_status
```

[← Optimisation](./infos-nginx-10-optimisation-performance.md) | [Index](./infos-nginx-00-index.md) | [Troubleshooting →](./infos-nginx-12-troubleshooting.md)

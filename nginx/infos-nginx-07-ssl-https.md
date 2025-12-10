# 🔒 SSL/TLS et HTTPS

[← Load Balancing](./infos-nginx-06-load-balancing.md) | [Index](./infos-nginx-00-index.md) | [Sécurité →](./infos-nginx-08-securite.md)

## Configuration HTTPS de base

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    root /var/www/html;
    index index.html;
}
```

## Let's Encrypt avec Certbot

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir et installer le certificat
sudo certbot --nginx -d example.com -d www.example.com

# Renouvellement automatique (cron déjà configuré)
sudo certbot renew --dry-run

# Tester le renouvellement
sudo certbot renew --dry-run
```

## Redirection HTTP → HTTPS

```nginx
# Rediriger tout le trafic HTTP vers HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # Configuration SSL optimale
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

## Configuration SSL optimale

```nginx
# Protocoles et ciphers modernes
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;

# Session cache
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# Security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

## Certificats auto-signés (développement)

```bash
# Générer un certificat auto-signé
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt \
    -subj "/C=FR/ST=Paris/L=Paris/O=Dev/OU=IT/CN=localhost"

# Générer un Diffie-Hellman group
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```

```nginx
server {
    listen 443 ssl http2;
    server_name localhost;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;
}
```

## HTTP/2

```nginx
server {
    listen 443 ssl http2;  # Activer HTTP/2

    # HTTP/2 push (optionnel)
    location = /index.html {
        http2_push /style.css;
        http2_push /script.js;
    }
}
```

[← Load Balancing](./infos-nginx-06-load-balancing.md) | [Index](./infos-nginx-00-index.md) | [Sécurité →](./infos-nginx-08-securite.md)

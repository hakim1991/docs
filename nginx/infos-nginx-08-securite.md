# 🛡️ Sécurité Nginx

[← SSL/HTTPS](./infos-nginx-07-ssl-https.md) | [Index](./infos-nginx-00-index.md) | [Caching →](./infos-nginx-09-caching.md)

## Headers de sécurité

```nginx
# Headers de sécurité essentiels
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

# HSTS (si HTTPS)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

## Limitation de débit (Rate Limiting)

```nginx
# Définir la zone de limitation
limit_req_zone $binary_remote_addr zone=limitbyaddr:10m rate=10r/s;
limit_req_status 429;

server {
    location /api/ {
        limit_req zone=limitbyaddr burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

## Limitation des connexions

```nginx
# Limiter le nombre de connexions simultanées
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    location /downloads/ {
        limit_conn addr 2;  # Max 2 connexions par IP
        limit_rate 500k;    # Limite à 500 KB/s
    }
}
```

## Authentification basique

```nginx
server {
    location /admin/ {
        auth_basic "Zone restreinte";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}
```

```bash
# Créer le fichier de mots de passe
sudo apt install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Ajouter un autre utilisateur
sudo htpasswd /etc/nginx/.htpasswd user2
```

## Bloquer les IPs

```nginx
# Bloquer une IP spécifique
deny 192.168.1.100;

# Autoriser un réseau et bloquer le reste
allow 10.0.0.0/8;
deny all;

# Géolocalisation (nécessite le module GeoIP)
geo $allowed_country {
    default no;
    FR yes;
    BE yes;
    CH yes;
}

server {
    if ($allowed_country = no) {
        return 403;
    }
}
```

## Protection contre les attaques

```nginx
# Bloquer les User-Agents suspects
if ($http_user_agent ~* (bot|crawler|spider|scraper)) {
    return 403;
}

# Limiter la taille des requêtes
client_max_body_size 10M;
client_body_buffer_size 128k;

# Timeout appropriés
client_body_timeout 12;
client_header_timeout 12;
send_timeout 10;

# Masquer la version Nginx
server_tokens off;
```

## Fail2ban pour Nginx

```bash
# Installer Fail2ban
sudo apt install fail2ban

# Configuration Fail2ban pour Nginx
sudo tee /etc/fail2ban/jail.d/nginx.conf <<EOF
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log

[nginx-badbots]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log

[nginx-noproxy]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
EOF

# Redémarrer Fail2ban
sudo systemctl restart fail2ban
```

## Protection DDoS

```nginx
# Limiter les requêtes
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
    limit_req zone=one burst=5;
    limit_conn addr 10;

    # Timeouts courts
    client_body_timeout 5s;
    client_header_timeout 5s;
}
```

## ModSecurity (WAF)

```bash
# Installer ModSecurity
sudo apt install libmodsecurity3 nginx-module-modsecurity

# Charger le module
echo 'load_module modules/ngx_http_modsecurity_module.so;' | \
    sudo tee /etc/nginx/modules-enabled/50-mod-modsecurity.conf
```

```nginx
server {
    modsecurity on;
    modsecurity_rules_file /etc/nginx/modsec/main.conf;
}
```

[← SSL/HTTPS](./infos-nginx-07-ssl-https.md) | [Index](./infos-nginx-00-index.md) | [Caching →](./infos-nginx-09-caching.md)

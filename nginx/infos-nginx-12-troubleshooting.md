# 🔧 Troubleshooting Nginx

[← Logs](./infos-nginx-11-logs-monitoring.md) | [Index](./infos-nginx-00-index.md)

## Problèmes courants

### Nginx ne démarre pas

```bash
# Vérifier la configuration
sudo nginx -t

# Voir les logs d'erreur
sudo journalctl -u nginx -n 50
sudo tail -50 /var/log/nginx/error.log

# Vérifier si le port 80 est déjà utilisé
sudo netstat -tulpn | grep :80
sudo ss -tulpn | grep :80

# Tuer le processus sur le port 80
sudo fuser -k 80/tcp
```

### Erreur 502 Bad Gateway

```nginx
# Causes possibles:
# 1. Backend down
# 2. Timeout trop court
# 3. Socket fermé

# Solutions:
location / {
    proxy_pass http://backend;

    # Augmenter les timeouts
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
    proxy_read_timeout 300;

    # Retry sur d'autres backends
    proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
}
```

### Erreur 503 Service Unavailable

```bash
# Vérifier que les backends sont up
curl http://backend:3000

# Vérifier la configuration upstream
sudo nginx -T | grep upstream

# Tester la connexion
telnet backend 3000
```

### Erreur 504 Gateway Timeout

```nginx
# Augmenter les timeouts
proxy_connect_timeout 600;
proxy_send_timeout 600;
proxy_read_timeout 600;
send_timeout 600;
```

### Permission denied

```bash
# Vérifier les permissions
ls -la /var/www/html

# Corriger les permissions
sudo chown -R nginx:nginx /var/www/html
sudo chmod -R 755 /var/www/html

# SELinux (CentOS/RHEL)
sudo setsebool -P httpd_can_network_connect 1
sudo chcon -R -t httpd_sys_content_t /var/www/html
```

## Debug

```nginx
# Activer le debug
error_log /var/log/nginx/error.log debug;

# Debug pour une IP spécifique
events {
    debug_connection 192.168.1.100;
}
```

```bash
# Tester la configuration
sudo nginx -t

# Voir la configuration complète
sudo nginx -T

# Version et modules
nginx -V

# Recharger sans couper les connexions
sudo nginx -s reload
```

## Commandes de diagnostic

```bash
# Processus Nginx
ps aux | grep nginx

# Connexions actives
sudo netstat -anp | grep nginx
sudo ss -anp | grep nginx

# Fichiers ouverts
sudo lsof -i :80
sudo lsof -i :443

# Mémoire utilisée
sudo pmap $(pgrep nginx) | tail -1

# Tester depuis l'extérieur
curl -I http://example.com
curl -v https://example.com
```

## Best practices troubleshooting

```bash
# ✅ Toujours tester avant reload
sudo nginx -t && sudo systemctl reload nginx

# ✅ Sauvegarder avant modifications
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# ✅ Vérifier les logs après changements
sudo tail -f /var/log/nginx/error.log

# ✅ Utiliser le mode debug temporairement
error_log /var/log/nginx/error.log debug;

# ✅ Monitorer les performances
sudo nginx -V 2>&1 | grep --with-http_stub_status_module
```

[← Logs](./infos-nginx-11-logs-monitoring.md) | [Index](./infos-nginx-00-index.md)

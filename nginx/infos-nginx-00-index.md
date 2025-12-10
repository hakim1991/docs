# 📚 Nginx - Documentation Complète

## Table des matières

### 🚀 Bases
1. [Introduction et Installation](./infos-nginx-01-introduction-installation.md)
   - Qu'est-ce que Nginx ?
   - Installation Linux / Windows
   - Première configuration
   - Commandes de base

2. [Configuration de base](./infos-nginx-02-configuration-base.md)
   - Structure des fichiers de configuration
   - Contextes et directives
   - Variables
   - Syntaxe

### 🌐 Serveur Web
3. [Servir des fichiers statiques](./infos-nginx-03-fichiers-statiques.md)
   - Configuration de base
   - Index et autoindex
   - Types MIME
   - Compression gzip

4. [Virtual Hosts (Server Blocks)](./infos-nginx-04-virtual-hosts.md)
   - Configuration multi-sites
   - Server names
   - Domaines et sous-domaines
   - Ports personnalisés

### 🔄 Reverse Proxy
5. [Reverse Proxy](./infos-nginx-05-reverse-proxy.md)
   - Principes du reverse proxy
   - Configuration proxy_pass
   - Headers HTTP
   - WebSocket proxy

6. [Load Balancing](./infos-nginx-06-load-balancing.md)
   - Méthodes de load balancing
   - Upstream servers
   - Health checks
   - Session persistence

### 🔒 Sécurité et HTTPS
7. [SSL/TLS et HTTPS](./infos-nginx-07-ssl-https.md)
   - Certificats SSL
   - Let's Encrypt
   - Configuration HTTPS
   - Redirection HTTP → HTTPS
   - HSTS et sécurité

8. [Sécurité](./infos-nginx-08-securite.md)
   - Authentification basique
   - Limitation de débit
   - Protection DDoS
   - ModSecurity
   - Best practices sécurité

### ⚡ Performance
9. [Caching](./infos-nginx-09-caching.md)
   - Cache proxy
   - Cache FastCGI
   - Cache statique
   - Configuration cache
   - Purge et invalidation

10. [Optimisation des performances](./infos-nginx-10-optimisation-performance.md)
    - Tuning des workers
    - Buffers et timeouts
    - Keepalive connections
    - Compression
    - HTTP/2 et HTTP/3

### 🔧 Avancé
11. [Logs et monitoring](./infos-nginx-11-logs-monitoring.md)
    - Configuration des logs
    - Log rotation
    - Formats personnalisés
    - Monitoring avec Prometheus
    - Outils d'analyse

12. [Troubleshooting](./infos-nginx-12-troubleshooting.md)
    - Problèmes courants
    - Debug
    - Erreurs 502, 503, 504
    - Outils de diagnostic

---

## 🎯 Commandes rapides

```bash
# Gestion du service
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx
sudo systemctl status nginx

# Tests de configuration
sudo nginx -t
sudo nginx -T

# Version et modules
nginx -v
nginx -V

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 📖 Structure de la documentation

Chaque chapitre contient:
- ✅ Explications détaillées
- ✅ Exemples de configuration
- ✅ Cas d'usage pratiques
- ✅ Best practices
- ✅ Troubleshooting

---

## 🔗 Ressources

- [Documentation officielle](https://nginx.org/en/docs/)
- [Nginx GitHub](https://github.com/nginx/nginx)
- [Community](https://forum.nginx.org/)

---

**Prêt à commencer ?** → [Introduction et Installation](./infos-nginx-01-introduction-installation.md)

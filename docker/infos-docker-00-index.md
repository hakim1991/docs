# Guide Complet Docker - Index

## 📚 Table des Matières

### Bases Docker
1. [📥 Introduction et Installation](./infos-docker-01-introduction-installation.md)
   - Qu'est-ce que Docker ?
   - Installation sur Linux (Ubuntu, Debian, CentOS, RHEL)
   - Installation sur Windows (WSL2, Docker Desktop)
   - Vérification de l'installation
   - Différences Windows vs Linux

2. [🖼️ Images Docker](./infos-docker-02-images.md)
   - Concept des images
   - Gestion des images (pull, build, tag, push)
   - Sauvegarder et charger des images
   - Optimisation des images
   - Multi-stage builds

3. [📦 Conteneurs Docker](./infos-docker-03-conteneurs.md)
   - Concept des conteneurs
   - Créer et gérer des conteneurs
   - Cycle de vie (run, start, stop, rm)
   - Logs et monitoring
   - Exécuter des commandes
   - Copier des fichiers
   - Inspection

4. [💾 Volumes et Persistance](./infos-docker-04-volumes.md)
   - Pourquoi les volumes ?
   - Volumes Docker vs Bind mounts vs tmpfs
   - Créer et gérer des volumes
   - Partager des volumes entre conteneurs
   - Sauvegarder et restaurer
   - Bonnes pratiques

5. [🌐 Réseaux Docker](./infos-docker-05-reseaux.md)
   - Concepts des réseaux
   - Types de réseaux (bridge, host, overlay, none)
   - Créer et gérer des réseaux
   - Communication entre conteneurs
   - DNS et résolution de noms
   - Exposition de ports
   - Isolation et sécurité

### Outils et Orchestration
6. [🎼 Docker Compose](./infos-docker-06-compose.md)
   - Qu'est-ce que Docker Compose ?
   - Structure d'un docker-compose.yml
   - Commandes principales
   - Variables d'environnement
   - Profils et environnements multiples
   - Override files
   - Stack multi-services complète

7. [🏗️ Dockerfile](./infos-docker-07-dockerfile.md)
   - Qu'est-ce qu'un Dockerfile ?
   - Instructions de base (FROM, RUN, COPY, WORKDIR, etc.)
   - CMD vs ENTRYPOINT
   - Multi-stage builds
   - Exemples complets (Node.js, Python, Next.js)
   - .dockerignore
   - Optimisations avancées

### Production et CI/CD
8. [🔐 Registres et CI/CD](./infos-docker-08-registres-cicd.md)
   - Docker Hub
   - GitLab Container Registry
   - GitHub Container Registry
   - Azure Container Registry
   - Registre privé auto-hébergé
   - Intégration CI/CD (GitLab CI, GitHub Actions)

9. [🧹 Maintenance et Nettoyage](./infos-docker-09-maintenance.md)
   - Voir l'utilisation disque
   - Nettoyer les images, conteneurs, volumes
   - Scripts de maintenance automatique
   - Cron jobs
   - Monitoring de l'espace disque

10. [🔍 Debug et Monitoring](./infos-docker-10-debug-monitoring.md)
    - Logs avancés
    - Stats et monitoring en temps réel
    - Inspection et debug
    - Healthchecks
    - Troubleshooting commun
    - Outils (cAdvisor, Portainer)

### Sauvegarde et Migration
11. [💾 Backup et Restauration](./infos-docker-11-backup.md)
    - Sauvegarder des volumes
    - Backup de bases de données (PostgreSQL, MySQL, MongoDB)
    - Sauvegarder des images
    - Stratégie de backup complète
    - Scripts automatiques
    - Backup vers le cloud (AWS S3)

### Spécificités Plateforme
12. [🪟 Différences Linux vs Windows](./infos-docker-12-differences-linux-windows.md)
    - Chemins de fichiers
    - Line endings (CRLF vs LF)
    - Performance (WSL2)
    - Réseau
    - Docker Desktop vs Docker Engine
    - Scripts cross-platform

### Applications Pratiques
13. [🚀 Cas Pratiques](./infos-docker-13-cas-pratiques.md)
    - Stack Odoo + PostgreSQL
    - Stack Next.js + FastAPI + PostgreSQL + Redis + MinIO
    - Configuration Nginx reverse proxy
    - Commandes de gestion quotidienne
    - Exemples complets prêts à l'emploi

---

## 🎯 Guide d'utilisation

### Pour les débutants
Commencez par lire dans l'ordre :
1. **Introduction et Installation** - Installer Docker
2. **Conteneurs** - Comprendre les bases
3. **Volumes** - Persister les données
4. **Docker Compose** - Gérer plusieurs conteneurs

### Pour les développeurs
Focus sur :
- **Dockerfile** - Créer vos propres images
- **Docker Compose** - Environnements de développement
- **Cas Pratiques** - Exemples adaptés à vos projets

### Pour la production
Lire :
- **Registres et CI/CD** - Déploiement automatisé
- **Backup et Restauration** - Stratégies de sauvegarde
- **Debug et Monitoring** - Surveillance et dépannage
- **Maintenance** - Nettoyage et optimisation

### Pour les ops/DevOps
Tous les chapitres, avec emphasis sur :
- **Réseaux** - Architecture multi-tiers
- **Maintenance** - Scripts automatiques
- **Backup** - Stratégies de récupération
- **Debug** - Outils de monitoring

---

## 📝 Commandes de référence rapide

```bash
# Images
docker images                          # Lister les images
docker pull IMAGE                      # Télécharger une image
docker build -t NAME .                 # Construire une image
docker rmi IMAGE                       # Supprimer une image

# Conteneurs
docker ps                              # Lister (actifs)
docker ps -a                           # Lister (tous)
docker run IMAGE                       # Créer et lancer
docker exec -it CONTAINER bash         # Shell interactif
docker logs -f CONTAINER               # Voir les logs
docker stop CONTAINER                  # Arrêter
docker rm CONTAINER                    # Supprimer

# Volumes
docker volume ls                       # Lister
docker volume create NAME              # Créer
docker volume rm NAME                  # Supprimer
docker volume prune                    # Nettoyer

# Réseaux
docker network ls                      # Lister
docker network create NAME             # Créer
docker network inspect NAME            # Inspecter

# Docker Compose
docker compose up -d                   # Démarrer
docker compose down                    # Arrêter
docker compose logs -f                 # Logs
docker compose exec SERVICE bash       # Shell
docker compose ps                      # Statut

# Maintenance
docker system prune -a                 # Nettoyer tout
docker system df                       # Espace disque
docker stats                           # Stats en temps réel

# Debug
docker inspect CONTAINER               # Détails complets
docker top CONTAINER                   # Processus
docker port CONTAINER                  # Ports mappés
```

---

## 🔗 Ressources additionnelles

- **Documentation officielle**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Best practices**: https://docs.docker.com/develop/dev-best-practices/

---

**Version**: 1.0
**Dernière mise à jour**: Décembre 2025
**Auteur**: Documentation pour gestion de projets Docker

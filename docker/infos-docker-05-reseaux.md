# 🌐 Réseaux Docker

[← Volumes](./infos-docker-04-volumes.md) | [Index](./infos-docker-00-index.md) | [Docker Compose →](./infos-docker-06-compose.md)

---

## Table des matières
- [Qu'est-ce qu'un réseau Docker ?](#quest-ce-quun-reseau-docker)
- [Types de réseaux](#types-de-reseaux)
- [Réseau bridge](#reseau-bridge)
- [Réseau host](#reseau-host)
- [Réseau none](#reseau-none)
- [Réseaux personnalisés](#reseaux-personnalises)
- [Communication entre conteneurs](#communication-entre-conteneurs)
- [DNS et discovery](#dns-et-discovery)
- [Exposer des ports](#exposer-des-ports)

---

## Qu'est-ce qu'un réseau Docker ?

### Concepts de base

Les **réseaux Docker** permettent aux conteneurs de communiquer entre eux et avec l'extérieur.

```
Internet
   ↕
Host (Docker Engine)
   ↕
Docker Networks
   ├── bridge (défaut)
   │   ├── conteneur1 (172.17.0.2)
   │   └── conteneur2 (172.17.0.3)
   ├── custom-network
   │   ├── web (172.18.0.2)
   │   └── db (172.18.0.3)
   └── host (partage IP host)
```

### Pourquoi des réseaux ?

```bash
# Isolation
# Conteneurs sur des réseaux différents ne peuvent pas communiquer

# Découverte de services (DNS automatique)
# Les conteneurs peuvent se joindre par leur nom

# Sécurité
# Contrôle fin de qui peut communiquer avec qui

# Flexibilité
# Connecter/déconnecter à chaud
```

---

## Types de réseaux

Docker propose plusieurs **drivers de réseau**:

### Vue d'ensemble

| Driver | Usage | Isolation | DNS | Performance |
|--------|-------|-----------|-----|-------------|
| **bridge** | Défaut, un seul host | ✅ | ✅ (custom) | ⚡ Bonne |
| **host** | Partage réseau host | ❌ | ❌ | ⚡⚡ Excellente |
| **none** | Pas de réseau | ✅✅ | ❌ | N/A |
| **overlay** | Multi-host (Swarm) | ✅ | ✅ | ⚡ Bonne |
| **macvlan** | IP physique | ✅ | ⚠️ | ⚡⚡ Excellente |

### Lister les réseaux

```bash
# Lister tous les réseaux
docker network ls

# Résultat:
NETWORK ID     NAME      DRIVER    SCOPE
abc123         bridge    bridge    local
def456         host      host      local
ghi789         none      null      local

# Inspecter un réseau
docker network inspect bridge

# Format personnalisé
docker network ls --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}"
```

---

## Réseau bridge

### Bridge par défaut

Le réseau **bridge** est utilisé par défaut pour tous les conteneurs.

```
┌─────────────────────────────────┐
│        Host (192.168.1.10)       │
│                                  │
│  ┌────────────────────────────┐ │
│  │    Docker Bridge           │ │
│  │    docker0 (172.17.0.1)    │ │
│  │                            │ │
│  │  ┌──────────┐  ┌─────────┐│ │
│  │  │Container1│  │Container2││ │
│  │  │172.17.0.2│  │172.17.0.3││ │
│  │  └──────────┘  └─────────┘│ │
│  └────────────────────────────┘ │
└─────────────────────────────────┘
         ↕
      Internet
```

```bash
# Utiliser le bridge par défaut (implicite)
docker run -d --name web nginx

# Vérifier le réseau
docker inspect web | grep NetworkMode
# "NetworkMode": "bridge"

# IP du conteneur
docker inspect web | grep IPAddress
# "IPAddress": "172.17.0.2"
```

### Limites du bridge par défaut

```bash
# ❌ Pas de résolution DNS automatique
docker run -d --name db postgres
docker run -d --name web nginx

# Depuis web, impossible de ping db par son nom:
docker exec web ping db
# ping: unknown host

# ✅ Solution: Utiliser un réseau personnalisé
```

---

## Réseau host

### Mode host

Le conteneur **partage le réseau du host** directement.

```
┌─────────────────────────────────┐
│        Host (192.168.1.10)       │
│                                  │
│        Port 80, 443, etc.        │
│               ↕                  │
│        ┌──────────────┐          │
│        │  Container   │          │
│        │  (mode host) │          │
│        └──────────────┘          │
│                                  │
│  Même réseau que le host !       │
└─────────────────────────────────┘
```

```bash
# Utiliser le mode host
docker run -d --network host nginx

# Le conteneur utilise directement le port 80 du host
# Pas besoin de -p 80:80

# Avantages:
# ✅ Performance maximale (pas de NAT)
# ✅ Accès direct aux interfaces réseau du host

# Inconvénients:
# ❌ Pas d'isolation réseau
# ❌ Conflits de ports possibles
# ❌ Moins portable
```

### Cas d'usage host

```bash
# Monitoring (Prometheus, Grafana)
docker run -d \
  --network host \
  --name prometheus \
  prom/prometheus

# Performance critique
docker run -d \
  --network host \
  high-performance-app

# Accès aux interfaces réseau du host
docker run -d \
  --network host \
  network-tool
```

---

## Réseau none

### Mode none

**Aucun réseau** configuré (isolation complète).

```bash
# Créer un conteneur sans réseau
docker run -d --network none --name isolated alpine sleep 3600

# Vérifier
docker exec isolated ip addr
# Seulement l'interface loopback (lo)

# Pas d'accès réseau
docker exec isolated ping 8.8.8.8
# Network unreachable
```

### Cas d'usage none

```bash
# Traitement de données sensibles
docker run --network none \
  -v /data:/data \
  data-processor

# Builds isolés
docker run --network none \
  -v $(pwd):/build \
  build-tool

# Tests de sécurité
docker run --network none security-scanner
```

---

## Réseaux personnalisés

### Créer un réseau bridge personnalisé

```bash
# Créer un réseau
docker network create mon-reseau

# Créer avec options
docker network create \
  --driver bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  mon-reseau

# Créer avec nom de domaine
docker network create \
  --driver bridge \
  --subnet 172.21.0.0/16 \
  --ip-range 172.21.5.0/24 \
  --gateway 172.21.0.1 \
  --opt com.docker.network.bridge.name=custom-bridge \
  custom-network

# Avec labels
docker network create \
  --label project=myapp \
  --label env=production \
  prod-network
```

### Utiliser un réseau personnalisé

```bash
# Connecter un conteneur au réseau à la création
docker run -d \
  --name web \
  --network mon-reseau \
  nginx

# Connecter un conteneur existant
docker network connect mon-reseau existing-container

# Déconnecter
docker network disconnect mon-reseau existing-container

# Avec IP fixe
docker run -d \
  --name web \
  --network mon-reseau \
  --ip 172.20.0.10 \
  nginx
```

### Avantages des réseaux personnalisés

```bash
# ✅ Résolution DNS automatique
docker network create app-network
docker run -d --name db --network app-network postgres
docker run -d --name web --network app-network nginx

# Depuis web:
docker exec web ping db
# ✅ Fonctionne ! Résolution DNS automatique

# ✅ Isolation
# Seuls les conteneurs sur app-network peuvent communiquer

# ✅ Contrôle fin
# Subnet, gateway, IP ranges personnalisés

# ✅ Hot-swap
# Connecter/déconnecter sans redémarrer
```

---

## Communication entre conteneurs

### Pattern: Application multi-tiers

```bash
# Créer un réseau
docker network create app-net

# 1. Base de données
docker run -d \
  --name postgres \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# 2. Backend API
docker run -d \
  --name api \
  --network app-net \
  -e DATABASE_URL=postgresql://postgres:secret@postgres:5432/mydb \
  backend-api

# 3. Frontend
docker run -d \
  --name web \
  --network app-net \
  -p 80:80 \
  frontend-app

# Communication:
# web → api (par nom "api")
# api → postgres (par nom "postgres")
```

### Plusieurs réseaux

```bash
# Créer deux réseaux
docker network create frontend-net
docker network create backend-net

# Base de données (seulement backend)
docker run -d \
  --name db \
  --network backend-net \
  postgres

# API (frontend + backend)
docker run -d \
  --name api \
  --network backend-net \
  backend-api

docker network connect frontend-net api

# Web (seulement frontend)
docker run -d \
  --name web \
  --network frontend-net \
  -p 80:80 \
  frontend-app

# Résultat:
# web → api ✅ (via frontend-net)
# web → db ❌ (pas sur le même réseau)
# api → db ✅ (via backend-net)
```

### Alias réseau

```bash
# Créer avec alias
docker run -d \
  --name postgres-primary \
  --network app-net \
  --network-alias database \
  --network-alias db \
  postgres

# Autres conteneurs peuvent utiliser les alias
docker run --rm \
  --network app-net \
  alpine \
  ping database
# ✅ Fonctionne !

docker run --rm \
  --network app-net \
  alpine \
  ping db
# ✅ Fonctionne aussi !
```

---

## DNS et discovery

### Résolution DNS automatique

```bash
# Sur un réseau personnalisé
docker network create mynet

docker run -d --name service1 --network mynet alpine sleep 3600
docker run -d --name service2 --network mynet alpine sleep 3600

# service1 peut joindre service2 par son nom
docker exec service1 ping service2
# ✅ Fonctionne

# Résolution DNS interne
docker exec service1 nslookup service2
# Server:    127.0.0.11
# Address:   127.0.0.11:53
# Name:      service2
# Address:   172.20.0.3
```

### DNS personnalisé

```bash
# Utiliser un serveur DNS spécifique
docker run -d \
  --dns 8.8.8.8 \
  --dns 8.8.4.4 \
  --name web \
  nginx

# DNS search domain
docker run -d \
  --dns-search example.com \
  --name web \
  nginx

# Options DNS
docker run -d \
  --dns-opt ndots:1 \
  --name web \
  nginx

# Fichier hosts personnalisé
docker run -d \
  --add-host myhost:192.168.1.100 \
  --add-host otherhost:192.168.1.101 \
  --name web \
  nginx
```

---

## Exposer des ports

### Port mapping

```bash
# Syntaxe: -p HOST_PORT:CONTAINER_PORT

# Port spécifique
docker run -d -p 8080:80 nginx
# localhost:8080 → container:80

# Port aléatoire
docker run -d -p 80 nginx
# Docker choisit un port libre sur le host

# Trouver le port
docker port <container> 80
# 0.0.0.0:32768

# Plusieurs ports
docker run -d \
  -p 8080:80 \
  -p 8443:443 \
  nginx

# Interface spécifique
docker run -d -p 127.0.0.1:8080:80 nginx
# Seulement accessible depuis localhost

# Protocole UDP
docker run -d -p 53:53/udp dns-server

# TCP + UDP
docker run -d \
  -p 53:53/tcp \
  -p 53:53/udp \
  dns-server
```

### Exposer vs publier

```bash
# EXPOSE (dans Dockerfile)
# Documentation uniquement, ne publie PAS le port
EXPOSE 80

# -p / --publish
# Publie réellement le port sur le host
docker run -d -p 8080:80 nginx

# -P / --publish-all
# Publie tous les ports EXPOSEd
docker run -d -P nginx
# Tous les ports EXPOSE sont mappés sur des ports aléatoires
```

### Exemples pratiques

```bash
# 1. Application web standard
docker run -d \
  --name web \
  -p 80:80 \
  -p 443:443 \
  nginx

# 2. API avec plusieurs instances (load balancing manuel)
docker run -d --name api1 -p 8081:8080 api-image
docker run -d --name api2 -p 8082:8080 api-image
docker run -d --name api3 -p 8083:8080 api-image

# 3. Base de données (localhost uniquement)
docker run -d \
  --name postgres \
  -p 127.0.0.1:5432:5432 \
  postgres

# 4. Application complète
docker network create app-net

# Database (pas de port publié)
docker run -d \
  --name db \
  --network app-net \
  postgres

# Backend (port interne uniquement)
docker run -d \
  --name api \
  --network app-net \
  -e DATABASE_URL=postgresql://db:5432/mydb \
  backend-api

# Frontend (port public)
docker run -d \
  --name web \
  --network app-net \
  -p 80:80 \
  frontend-app
```

---

## Inspection et debugging

### Inspecter le réseau

```bash
# Informations détaillées
docker network inspect mon-reseau

# Voir les conteneurs connectés
docker network inspect mon-reseau \
  --format '{{range .Containers}}{{.Name}} {{end}}'

# Configuration IP
docker network inspect mon-reseau \
  --format '{{.IPAM.Config}}'

# Subnet
docker network inspect mon-reseau \
  --format '{{(index .IPAM.Config 0).Subnet}}'
```

### Debugging réseau

```bash
# Tester la connectivité
docker run --rm \
  --network mon-reseau \
  alpine \
  ping -c 3 autre-conteneur

# DNS lookup
docker run --rm \
  --network mon-reseau \
  alpine \
  nslookup autre-conteneur

# Scan de ports
docker run --rm \
  --network mon-reseau \
  alpine \
  nc -zv autre-conteneur 80

# Curl depuis un conteneur
docker run --rm \
  --network mon-reseau \
  curlimages/curl \
  curl http://web-server

# Utiliser un conteneur de debug
docker run -it --rm \
  --network container:web-server \
  nicolaka/netshoot

# Outils disponibles: tcpdump, nmap, curl, dig, etc.
```

### Voir les connexions

```bash
# Ports d'un conteneur
docker port <container>

# Tous les mappings
docker ps --format "table {{.Names}}\t{{.Ports}}"

# IP d'un conteneur
docker inspect <container> \
  --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# Réseau d'un conteneur
docker inspect <container> \
  --format '{{range $net, $conf := .NetworkSettings.Networks}}{{$net}}{{end}}'
```

---

## Gestion des réseaux

### Supprimer des réseaux

```bash
# Supprimer un réseau
docker network rm mon-reseau

# Supprimer plusieurs réseaux
docker network rm reseau1 reseau2 reseau3

# Supprimer les réseaux non utilisés
docker network prune

# Avec force
docker network prune -f

# Filtrer par label
docker network prune --filter "label=temporary=true"
```

### Réseaux overlay (Swarm)

```bash
# Initialiser Swarm
docker swarm init

# Créer un réseau overlay
docker network create \
  --driver overlay \
  --attachable \
  overlay-net

# Utilisable sur plusieurs hosts
docker service create \
  --name web \
  --network overlay-net \
  --replicas 3 \
  nginx
```

---

## Patterns et best practices

### Pattern: Stack applicative

```bash
# Architecture type:
# Frontend → Backend → Database → Cache

docker network create frontend-net
docker network create backend-net

# Cache (Redis)
docker run -d \
  --name redis \
  --network backend-net \
  redis:7

# Database (PostgreSQL)
docker run -d \
  --name postgres \
  --network backend-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Backend API
docker run -d \
  --name api \
  --network backend-net \
  -e DATABASE_URL=postgresql://postgres:5432/db \
  -e REDIS_URL=redis://redis:6379 \
  backend-api

# Connecter aussi au frontend-net
docker network connect frontend-net api

# Frontend
docker run -d \
  --name web \
  --network frontend-net \
  -p 80:80 \
  -p 443:443 \
  frontend-app

# Sécurité:
# ✅ Frontend ne peut pas accéder directement à la DB
# ✅ DB/Redis isolés sur backend-net
# ✅ Seule l'API fait le pont
```

### Best practices

```bash
# ✅ Utiliser des réseaux personnalisés (pas le bridge par défaut)
docker network create app-net
docker run -d --network app-net nginx

# ✅ Nommer les réseaux de manière descriptive
docker network create frontend-net
docker network create backend-net
docker network create database-net

# ✅ Ne pas exposer de ports inutiles
# Si un conteneur est seulement utilisé en interne:
docker run -d --network app-net postgres
# Pas de -p, seulement accessible via le réseau Docker

# ✅ Utiliser plusieurs réseaux pour isolation
docker network create public-net
docker network create private-net

# ✅ Limiter l'exposition au localhost si nécessaire
docker run -d -p 127.0.0.1:5432:5432 postgres

# ❌ Ne pas utiliser --network host en production
# Sauf cas très spécifiques (monitoring, performance critique)

# ✅ Utiliser des alias pour la flexibilité
docker run -d \
  --network app-net \
  --network-alias db \
  --network-alias database \
  postgres

# ✅ Labels pour organisation
docker network create \
  --label env=production \
  --label project=myapp \
  prod-network
```

---

## Commandes de référence rapide

```bash
# Gestion des réseaux
docker network create nom                # Créer
docker network ls                        # Lister
docker network inspect nom               # Inspecter
docker network rm nom                    # Supprimer
docker network prune                     # Nettoyer

# Connecter/Déconnecter
docker network connect net container     # Connecter
docker network disconnect net container  # Déconnecter

# Utilisation
docker run --network nom image           # Utiliser un réseau
docker run --network host image          # Mode host
docker run --network none image          # Pas de réseau

# Ports
docker run -p 8080:80 image             # Mapper un port
docker run -P image                      # Tous les ports EXPOSE
docker port container                    # Voir les mappings

# DNS
docker run --dns 8.8.8.8 image          # DNS personnalisé
docker run --add-host host:ip image      # Entrée hosts
docker run --network-alias alias image   # Alias réseau

# Debugging
docker exec container ping host          # Test connectivité
docker network inspect net               # Voir conteneurs connectés
```

---

[← Volumes](./infos-docker-04-volumes.md) | [Index](./infos-docker-00-index.md) | [Docker Compose →](./infos-docker-06-compose.md)

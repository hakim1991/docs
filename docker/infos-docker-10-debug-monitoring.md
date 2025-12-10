# 🐛 Debug et Monitoring

[← Maintenance](./infos-docker-09-maintenance.md) | [Index](./infos-docker-00-index.md) | [Backup →](./infos-docker-11-backup.md)

---

## Table des matières
- [Debugging des conteneurs](#debugging-des-conteneurs)
- [Logs et traces](#logs-et-traces)
- [Inspection et diagnostic](#inspection-et-diagnostic)
- [Monitoring](#monitoring)
- [Outils de monitoring](#outils-de-monitoring)
- [Troubleshooting commun](#troubleshooting-commun)

---

## Debugging des conteneurs

### Accéder à un conteneur

```bash
# Shell interactif
docker exec -it mon-conteneur bash
docker exec -it mon-conteneur sh      # Pour Alpine

# En tant qu'utilisateur spécifique
docker exec -it -u root mon-conteneur bash

# Avec working directory
docker exec -it -w /app mon-conteneur bash

# Exécuter une commande ponctuelle
docker exec mon-conteneur ls -la /app
docker exec mon-conteneur cat /etc/hosts
docker exec mon-conteneur ps aux
```

### Démarrer un conteneur en mode debug

```bash
# Override de la commande par défaut
docker run -it --rm nginx bash
# Lance bash au lieu de nginx

# Avec volumes pour debug
docker run -it --rm \
  -v $(pwd):/debug \
  -w /debug \
  python:3.11 bash

# Mode privilégié (pour outils système)
docker run -it --rm --privileged nginx bash

# Partager les namespaces d'un conteneur
docker run -it --rm \
  --network container:mon-conteneur \
  --pid container:mon-conteneur \
  alpine sh
```

### Attacher à un conteneur running

```bash
# Attacher au processus principal
docker attach mon-conteneur

# Détacher sans arrêter: Ctrl+P puis Ctrl+Q

# Voir les processus
docker top mon-conteneur

# Avec format personnalisé
docker top mon-conteneur aux
```

### Copier des fichiers pour debug

```bash
# Depuis conteneur vers host
docker cp mon-conteneur:/app/logs/error.log ./debug/
docker cp mon-conteneur:/etc/nginx/nginx.conf ./debug/

# Depuis host vers conteneur
docker cp debug-script.sh mon-conteneur:/tmp/
docker cp fixed-config.json mon-conteneur:/app/config/

# Copier un dossier entier
docker cp mon-conteneur:/var/log ./logs-backup/
```

---

## Logs et traces

### Voir les logs

```bash
# Logs d'un conteneur
docker logs mon-conteneur

# Suivre en temps réel (tail -f)
docker logs -f mon-conteneur

# Dernières N lignes
docker logs --tail 100 mon-conteneur
docker logs --tail 50 -f mon-conteneur

# Logs depuis un timestamp
docker logs --since 2024-01-01 mon-conteneur
docker logs --since 1h mon-conteneur
docker logs --since 30m mon-conteneur

# Logs jusqu'à un timestamp
docker logs --until 2024-01-02 mon-conteneur

# Avec timestamps
docker logs -t mon-conteneur

# Combine plusieurs options
docker logs -f --tail 50 --since 10m mon-conteneur
```

### Logs avec Docker Compose

```bash
# Logs de tous les services
docker compose logs

# Suivre en temps réel
docker compose logs -f

# Un service spécifique
docker compose logs -f web

# Plusieurs services
docker compose logs -f web api

# Avec timestamps et tail
docker compose logs -f --tail=100 -t
```

### Configuration des logs

```dockerfile
# Dans le Dockerfile
# Envoyer les logs vers stdout/stderr
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log
```

```yaml
# docker-compose.yml
services:
  web:
    image: nginx
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "production"
```

```bash
# Au démarrage du conteneur
docker run -d \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=5 \
  nginx
```

### Drivers de logs

```bash
# JSON file (défaut)
docker run -d --log-driver json-file nginx

# Syslog
docker run -d --log-driver syslog \
  --log-opt syslog-address=udp://192.168.1.100:514 \
  nginx

# Journald
docker run -d --log-driver journald nginx

# Fluentd
docker run -d --log-driver fluentd \
  --log-opt fluentd-address=localhost:24224 \
  nginx

# Graylog (GELF)
docker run -d --log-driver gelf \
  --log-opt gelf-address=udp://192.168.1.100:12201 \
  nginx

# Splunk
docker run -d --log-driver splunk \
  --log-opt splunk-token=<token> \
  --log-opt splunk-url=https://splunk.example.com:8088 \
  nginx

# Désactiver les logs (⚠️)
docker run -d --log-driver none nginx
```

---

## Inspection et diagnostic

### Inspecter un conteneur

```bash
# Informations complètes (JSON)
docker inspect mon-conteneur

# Format spécifique
docker inspect --format='{{.State.Status}}' mon-conteneur
docker inspect --format='{{.NetworkSettings.IPAddress}}' mon-conteneur
docker inspect --format='{{.Config.Image}}' mon-conteneur

# Plusieurs valeurs
docker inspect --format='{{.State.Status}} {{.State.Health.Status}}' mon-conteneur

# État et santé
docker inspect --format='{{json .State}}' mon-conteneur | jq

# Variables d'environnement
docker inspect --format='{{.Config.Env}}' mon-conteneur

# Volumes montés
docker inspect --format='{{json .Mounts}}' mon-conteneur | jq

# Ports
docker inspect --format='{{json .NetworkSettings.Ports}}' mon-conteneur | jq
```

### Diagnostiquer les problèmes réseau

```bash
# Voir l'IP du conteneur
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mon-conteneur

# Tester la connectivité depuis le host
ping $(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mon-conteneur)

# Tester depuis un autre conteneur
docker run --rm --network mon-reseau alpine ping conteneur-cible

# DNS lookup
docker run --rm --network mon-reseau alpine nslookup conteneur-cible

# Port scan
docker run --rm --network mon-reseau alpine nc -zv conteneur-cible 80

# Curl test
docker run --rm --network mon-reseau curlimages/curl curl http://conteneur-cible

# Utiliser netshoot (toolbox complète)
docker run -it --rm --network mon-reseau nicolaka/netshoot
# Contient: tcpdump, nmap, curl, dig, iperf3, etc.
```

### Diagnostiquer les problèmes de performance

```bash
# Stats en temps réel
docker stats mon-conteneur

# Snapshot
docker stats --no-stream mon-conteneur

# Processus dans le conteneur
docker top mon-conteneur
docker top mon-conteneur aux

# Événements Docker
docker events

# Filtrer les événements
docker events --filter container=mon-conteneur
docker events --filter event=start
docker events --filter event=die

# Historique des changements dans un conteneur
docker diff mon-conteneur
```

### Healthchecks

```dockerfile
# Dans le Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

```yaml
# docker-compose.yml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

```bash
# Voir le statut de santé
docker inspect --format='{{.State.Health.Status}}' mon-conteneur

# Historique des checks
docker inspect --format='{{json .State.Health}}' mon-conteneur | jq

# Voir seulement les conteneurs unhealthy
docker ps --filter health=unhealthy
```

---

## Monitoring

### Métriques de base

```bash
# CPU et mémoire
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Réseau
docker stats --format "table {{.Container}}\t{{.NetIO}}"

# I/O disque
docker stats --format "table {{.Container}}\t{{.BlockIO}}"

# Tout
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

# JSON pour parsing
docker stats --no-stream --format '{{json .}}'
```

### Monitoring des ressources

```bash
# Script de monitoring simple
#!/bin/bash
# docker-monitor.sh

while true; do
    clear
    echo "=== Docker Monitoring ==="
    echo ""
    echo "📊 Conteneurs:"
    docker ps --format "table {{.Names}}\t{{.Status}}"
    echo ""
    echo "💻 Ressources:"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    echo ""
    echo "💾 Espace disque:"
    docker system df
    sleep 5
done
```

### Exporter les métriques

```bash
# Exporter vers un fichier
docker stats --no-stream --format '{{.Container}},{{.CPUPerc}},{{.MemUsage}}' > metrics.csv

# Loop pour monitoring continu
while true; do
    date=$(date +%Y-%m-%d\ %H:%M:%S)
    docker stats --no-stream --format "$date,{{.Container}},{{.CPUPerc}},{{.MemUsage}}" >> metrics.csv
    sleep 60
done
```

---

## Outils de monitoring

### cAdvisor (Container Advisor)

```bash
# Démarrer cAdvisor
docker run -d \
  --name=cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  gcr.io/cadvisor/cadvisor:latest

# Interface web: http://localhost:8080
```

### Prometheus + Grafana

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  # Node Exporter
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    restart: unless-stopped

  # cAdvisor
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    restart: unless-stopped

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

### Portainer

```bash
# Démarrer Portainer
docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer-data:/data \
  portainer/portainer-ce:latest

# Interface web: https://localhost:9443
```

### Elasticsearch + Kibana + Filebeat (ELK Stack)

```yaml
# docker-compose.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    user: root
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - elasticsearch

volumes:
  elasticsearch-data:
```

### Datadog

```bash
# Agent Datadog
docker run -d \
  --name dd-agent \
  -e DD_API_KEY=<YOUR_API_KEY> \
  -e DD_SITE="datadoghq.com" \
  -e DD_LOGS_ENABLED=true \
  -e DD_PROCESS_AGENT_ENABLED=true \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  gcr.io/datadoghq/agent:latest
```

---

## Troubleshooting commun

### Conteneur qui crashe

```bash
# Voir les logs avant le crash
docker logs mon-conteneur

# Dernières lignes avant l'arrêt
docker logs --tail 100 mon-conteneur

# Raison de l'arrêt
docker inspect --format='{{.State.Status}} {{.State.ExitCode}}' mon-conteneur

# Historique des redémarrages
docker inspect --format='{{.RestartCount}}' mon-conteneur

# Démarrer en mode interactif pour debug
docker run -it --rm mon-image bash

# Override de l'entrypoint
docker run -it --rm --entrypoint bash mon-image
```

### Problèmes de réseau

```bash
# Vérifier les réseaux
docker network ls
docker network inspect mon-reseau

# Voir les conteneurs connectés
docker network inspect mon-reseau --format='{{range .Containers}}{{.Name}} {{end}}'

# Tester la résolution DNS
docker exec mon-conteneur nslookup autre-conteneur
docker exec mon-conteneur ping autre-conteneur

# Vérifier les ports
docker port mon-conteneur

# Écoute sur les ports
docker exec mon-conteneur netstat -tuln
```

### Problèmes de volumes

```bash
# Vérifier les volumes
docker volume ls
docker volume inspect mon-volume

# Voir où est monté un volume
docker inspect --format='{{json .Mounts}}' mon-conteneur | jq

# Vérifier les permissions
docker exec mon-conteneur ls -la /path/to/volume

# Changer les permissions
docker exec -u root mon-conteneur chown -R user:group /path/to/volume
```

### Problèmes de mémoire

```bash
# Vérifier l'utilisation
docker stats --no-stream mon-conteneur

# Voir les limites
docker inspect --format='{{.HostConfig.Memory}}' mon-conteneur

# Augmenter la limite
docker update --memory="2g" mon-conteneur

# OOM killed?
docker inspect --format='{{.State.OOMKilled}}' mon-conteneur

# Logs kernel (Linux)
dmesg | grep -i oom
journalctl -k | grep -i oom
```

### Problèmes de build

```bash
# Build avec progression détaillée
docker build --progress=plain -t mon-image .

# Sans cache
docker build --no-cache -t mon-image .

# Voir l'historique des layers
docker history mon-image

# Debug un stage spécifique (multi-stage)
docker build --target builder -t debug-image .
docker run -it --rm debug-image bash

# Avec build args pour debug
docker build --build-arg DEBUG=true -t mon-image .
```

### Problèmes de permissions

```bash
# Fichiers créés par root dans un bind mount
# Voir le propriétaire
docker exec mon-conteneur ls -la /path

# Solution 1: Utiliser l'UID/GID du host
docker run -u $(id -u):$(id -g) ...

# Solution 2: Changer dans le conteneur
docker exec -u root mon-conteneur chown -R user:group /path

# Solution 3: Dans le Dockerfile
USER node
# ou
RUN chown -R node:node /app
USER node
```

---

## Scripts utiles

### Script de diagnostic complet

```bash
#!/bin/bash
# docker-diagnostic.sh

echo "🔍 Diagnostic Docker"
echo "===================="
echo ""

echo "📦 Version Docker:"
docker version --format 'Client: {{.Client.Version}} | Server: {{.Server.Version}}'
echo ""

echo "🏃 Conteneurs actifs:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
echo ""

echo "⚠️  Conteneurs problématiques:"
docker ps -a --filter status=exited --format "table {{.Names}}\t{{.Status}}"
docker ps --filter health=unhealthy --format "table {{.Names}}\t{{.Status}}"
echo ""

echo "💾 Utilisation disque:"
docker system df
echo ""

echo "📊 Utilisation ressources:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
echo ""

echo "🌐 Réseaux:"
docker network ls
echo ""

echo "💿 Volumes:"
docker volume ls
echo ""

echo "🖼️  Images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## Commandes de référence rapide

```bash
# Debugging
docker exec -it container bash              # Shell interactif
docker logs -f container                    # Logs en temps réel
docker inspect container                    # Informations détaillées
docker stats                                # Ressources en temps réel

# Réseau
docker network inspect network              # Détails réseau
docker exec container ping target           # Test connectivité

# Healthcheck
docker inspect --format='{{.State.Health.Status}}' container

# Copie pour debug
docker cp container:/path local-path        # Exporter fichiers
docker cp local-file container:/path        # Importer fichiers

# Monitoring
docker stats --no-stream                    # Snapshot ressources
docker events                               # Événements temps réel
```

---

[← Maintenance](./infos-docker-09-maintenance.md) | [Index](./infos-docker-00-index.md) | [Backup →](./infos-docker-11-backup.md)

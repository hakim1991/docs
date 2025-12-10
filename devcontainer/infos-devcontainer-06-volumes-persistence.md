# 💾 Volumes et Persistence

[← Ports](./infos-devcontainer-05-ports-networking.md) | [Index](./infos-devcontainer-00-index.md) | [Docker Compose →](./infos-devcontainer-07-docker-compose.md)

## Workspace Mount (par défaut)

Par défaut, le workspace est monté automatiquement :

```
Machine hôte                Container
/Users/me/project    →     /workspace
```

## Mounts personnalisés

### Syntaxe

```json
{
  "mounts": [
    "source=/path/on/host,target=/path/in/container,type=bind"
  ]
}
```

### Types de mounts

- `bind` : mount un dossier/fichier de l'hôte
- `volume` : utilise un volume Docker
- `tmpfs` : mount en mémoire (temporaire)

## Exemples de mounts

### SSH Keys

Partager les clés SSH avec le container.

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,readonly,type=bind"
  ]
}
```

```json
{
  "mounts": [
    "source=${localEnv:HOME}${localEnv:USERPROFILE}/.ssh,target=/home/node/.ssh,readonly,type=bind,consistency=cached"
  ]
}
```

### Git config

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.gitconfig,target=/home/vscode/.gitconfig,readonly,type=bind"
  ]
}
```

### Fichiers de configuration

```json
{
  "mounts": [
    "source=${localWorkspaceFolder}/.env,target=/workspace/.env,type=bind"
  ]
}
```

### Cache npm/yarn

Persister le cache npm entre rebuilds.

```json
{
  "mounts": [
    "source=my-project-node-modules,target=/workspace/node_modules,type=volume"
  ]
}
```

### Multiple mounts

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,readonly,type=bind",
    "source=${localEnv:HOME}/.gitconfig,target=/home/vscode/.gitconfig,readonly,type=bind",
    "source=node-modules-cache,target=/workspace/node_modules,type=volume"
  ]
}
```

## workspaceMount

Personnaliser le mount du workspace.

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached",
  "workspaceFolder": "/workspace"
}
```

### Consistency modes

- `consistent` : synchronisation complète (par défaut)
- `cached` : plus rapide, OK pour la plupart des cas
- `delegated` : encore plus rapide, pour les opérations intensives

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
}
```

## Variables d'environnement

### localEnv

Accéder aux variables d'environnement de l'hôte.

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/root/.ssh,readonly,type=bind"
  ]
}
```

### localWorkspaceFolder

Chemin du workspace sur l'hôte.

```json
{
  "mounts": [
    "source=${localWorkspaceFolder}/.devcontainer/scripts,target=/scripts,type=bind"
  ]
}
```

### containerWorkspaceFolder

Chemin du workspace dans le container.

```json
{
  "containerEnv": {
    "WORKSPACE": "${containerWorkspaceFolder}"
  }
}
```

## Docker Volumes

### Named volumes

```json
{
  "mounts": [
    "source=my-data,target=/data,type=volume"
  ]
}
```

Créer le volume :

```bash
docker volume create my-data
```

### Volumes avec Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - ..:/workspace:cached
      - node-modules:/workspace/node_modules

  db:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  node-modules:
  postgres-data:
```

## Persistance de données

### Base de données

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb

volumes:
  postgres-data:
```

Les données persistent entre rebuilds du container.

### node_modules

Éviter de copier node_modules entre hôte et container (performances).

```yaml
services:
  app:
    volumes:
      - ..:/workspace:cached
      - node-modules:/workspace/node_modules

volumes:
  node-modules:
```

Ou avec Dockerfile :

```dockerfile
FROM node:18

WORKDIR /workspace

# Volume anonyme pour node_modules
VOLUME ["/workspace/node_modules"]
```

## Exemple complet

```json
// .devcontainer/devcontainer.json
{
  "name": "Full Stack App",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "mounts": [
    // SSH keys
    "source=${localEnv:HOME}/.ssh,target=/home/node/.ssh,readonly,type=bind",

    // Git config
    "source=${localEnv:HOME}/.gitconfig,target=/home/node/.gitconfig,readonly,type=bind",

    // AWS credentials
    "source=${localEnv:HOME}/.aws,target=/home/node/.aws,readonly,type=bind"
  ],

  "remoteUser": "node"
}
```

```yaml
# .devcontainer/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      # Workspace
      - ..:/workspace:cached

      # node_modules persistant
      - node-modules:/workspace/node_modules

      # Cache npm
      - npm-cache:/home/node/.npm

    command: sleep infinity
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/mydb

  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb

volumes:
  node-modules:
  npm-cache:
  postgres-data:
```

## Permissions

### Problèmes courants

Le container crée des fichiers en tant que root.

### Solution 1 : remoteUser

```json
{
  "remoteUser": "node"
}
```

Les fichiers créés appartiendront à l'utilisateur `node`.

### Solution 2 : USER dans Dockerfile

```dockerfile
FROM node:18

USER node
```

### Solution 3 : chown au démarrage

```json
{
  "postCreateCommand": "sudo chown -R node:node /workspace"
}
```

## Performance

### Cached mode

Améliore les performances sur Mac.

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
}
```

### Exclure node_modules

```yaml
volumes:
  - ..:/workspace:cached
  - /workspace/node_modules
```

Le second volume "masque" node_modules du host.

### tmpfs pour fichiers temporaires

```json
{
  "mounts": [
    "type=tmpfs,target=/tmp"
  ]
}
```

## Backup et restore

### Backup volume

```bash
# Créer backup
docker run --rm \
  -v my-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data

# Restore
docker run --rm \
  -v my-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /
```

### Copier depuis container

```bash
docker cp <container-id>:/workspace/data ./data
```

## Nettoyage

### Lister volumes

```bash
docker volume ls
```

### Supprimer volume

```bash
docker volume rm my-volume
```

### Supprimer volumes non utilisés

```bash
docker volume prune
```

## Sécurité

### Readonly mounts

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,readonly,type=bind"
  ]
}
```

### Ne pas monter tout le HOME

❌ Mauvais :
```json
{
  "mounts": [
    "source=${localEnv:HOME},target=/home/vscode,type=bind"
  ]
}
```

✅ Bon :
```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/vscode/.ssh,readonly,type=bind",
    "source=${localEnv:HOME}/.gitconfig,target=/home/vscode/.gitconfig,readonly,type=bind"
  ]
}
```

## Troubleshooting

### Permissions denied

```bash
# Vérifier les permissions
ls -la /workspace

# Changer les permissions
sudo chown -R $USER:$USER /workspace
```

### Volume ne persiste pas

Vérifier que c'est un named volume :

```yaml
volumes:
  - my-data:/data  # Named volume

volumes:
  my-data:  # Définition du volume
```

### Fichiers non synchronisés

Vérifier le consistency mode :

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
}
```

## Commandes utiles

```bash
# Lister volumes
docker volume ls

# Inspecter volume
docker volume inspect my-volume

# Voir les mounts d'un container
docker inspect <container-id> | grep Mounts -A 20

# Taille d'un volume
docker system df -v
```

## Bonnes pratiques

1. **Utiliser cached pour workspace** : meilleure performance
2. **Volume séparé pour node_modules** : évite sync inutile
3. **Readonly pour credentials** : sécurité
4. **Named volumes pour data persistante** : bases de données
5. **Documenter les volumes** : dans README.md
6. **Backup régulièrement** : données critiques

[← Ports](./infos-devcontainer-05-ports-networking.md) | [Index](./infos-devcontainer-00-index.md) | [Docker Compose →](./infos-devcontainer-07-docker-compose.md)

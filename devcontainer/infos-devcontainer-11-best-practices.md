# ✅ Best Practices

[← Avancé](./infos-devcontainer-10-sujets-avances.md) | [Index](./infos-devcontainer-00-index.md)

## Structure du projet

### Organisation recommandée

```
projet/
├── .devcontainer/
│   ├── devcontainer.json        # Config principale
│   ├── Dockerfile               # Image personnalisée (optionnel)
│   ├── docker-compose.yml       # Multi-containers (optionnel)
│   └── scripts/
│       ├── setup.sh             # Scripts d'initialisation
│       └── post-create.sh
├── .vscode/
│   ├── settings.json            # Settings locaux (optionnel)
│   ├── extensions.json          # Extensions recommandées
│   └── launch.json              # Config debug
├── src/
├── tests/
├── .gitignore
├── README.md
└── package.json
```

### .gitignore

```gitignore
# Ne pas commiter
.env
.env.local

# Optionnel : garder .vscode/settings.json local
.vscode/settings.json
```

## Configuration

### Versions explicites

✅ Bon :
```json
{
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18-bullseye"
}
```

❌ Éviter :
```json
{
  "image": "node:latest"
}
```

### Features avec versions

✅ Bon :
```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "18.17.0"
    }
  }
}
```

❌ Éviter :
```json
{
  "features": {
    "ghcr.io/devcontainers/features/node:1": "latest"
  }
}
```

### Commentaires

```json
{
  // Configuration pour Node.js 18
  "name": "Mon Projet",

  // Image de base avec Node 18
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",

  // Extensions essentielles
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",  // Linting
        "esbenp.prettier-vscode"    // Formatting
      ]
    }
  }
}
```

## Sécurité

### Ne pas inclure de secrets

❌ Mauvais :
```json
{
  "containerEnv": {
    "DATABASE_PASSWORD": "secret123"
  }
}
```

✅ Bon :
```json
{
  "containerEnv": {
    "DATABASE_URL": "${localEnv:DATABASE_URL}"
  }
}
```

### Utiliser remoteUser

✅ Bon :
```json
{
  "remoteUser": "node"
}
```

❌ Éviter :
```json
{
  "remoteUser": "root"
}
```

### Readonly mounts

```json
{
  "mounts": [
    "source=${localEnv:HOME}/.ssh,target=/home/node/.ssh,readonly,type=bind"
  ]
}
```

### Ne pas exposer ports sensibles

```json
{
  "forwardPorts": [3000],
  // Ne pas forwarder 5432, 6379, etc.
}
```

## Performance

### Cached volumes

```json
{
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
}
```

### Named volumes pour node_modules

```yaml
services:
  app:
    volumes:
      - .:/workspace:cached
      - node-modules:/workspace/node_modules

volumes:
  node-modules:
```

### Multi-stage builds

```dockerfile
# Builder
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
```

### Layer caching

```dockerfile
# ✅ Bon : cache les layers
FROM node:18
WORKDIR /app

# Copier package.json en premier
COPY package*.json ./
RUN npm ci

# Copier le code ensuite
COPY . .

# ❌ Mauvais : invalide le cache à chaque changement
FROM node:18
WORKDIR /app
COPY . .
RUN npm ci
```

## Documentation

### README.md complet

```markdown
# Mon Projet

## Développement avec Dev Containers

### Prérequis

- Docker Desktop
- VS Code avec extension Dev Containers

### Démarrage rapide

1. Clone le repo
2. Ouvrir dans VS Code
3. `F1` → "Dev Containers: Reopen in Container"
4. Attendre l'installation (première fois : ~5 min)
5. `npm run dev`

### Services

- Frontend : http://localhost:3000
- Backend API : http://localhost:5000
- PostgreSQL : localhost:5432
- pgAdmin : http://localhost:5050

### Commandes utiles

```bash
npm run dev      # Démarrer en mode dev
npm test         # Lancer les tests
npm run build    # Build production
```

### Troubleshooting

#### Le container ne démarre pas
```bash
docker-compose down
docker-compose build --no-cache
```

#### Permissions denied
```bash
sudo chown -R $USER:$USER .
```
```

### CONTRIBUTING.md

```markdown
# Contribution

## Setup

Suivre les instructions dans README.md pour démarrer le Dev Container.

## Workflow

1. Créer une branche : `git checkout -b feature/ma-feature`
2. Développer et tester
3. Commit : `git commit -m "feat: ma feature"`
4. Push : `git push origin feature/ma-feature`
5. Créer une Pull Request

## Standards

- ESLint : code doit passer `npm run lint`
- Tests : `npm test` doit réussir
- Formatting : Prettier (automatique on save)

## Dev Container

Si vous modifiez `.devcontainer/` :
1. Tester localement
2. Documenter les changements
3. Notifier l'équipe
```

## Maintenance

### Mise à jour régulière

```bash
# Mettre à jour les images
docker pull mcr.microsoft.com/devcontainers/javascript-node:18

# Rebuild le container
F1 → "Dev Containers: Rebuild Container"
```

### Nettoyage

```bash
# Supprimer containers arrêtés
docker container prune

# Supprimer volumes non utilisés
docker volume prune

# Supprimer images non utilisées
docker image prune -a

# Tout nettoyer
docker system prune -a --volumes
```

## Tests

### Tester la config

```bash
# Build sans cache
devcontainer build --no-cache --workspace-folder .

# Exec commande
devcontainer exec --workspace-folder . npm test

# CI
devcontainer up --workspace-folder .
```

### CI/CD

```yaml
# .github/workflows/test.yml
name: Test Dev Container

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Dev Container
        uses: devcontainers/ci@v0.3
        with:
          runCmd: |
            npm install
            npm test
            npm run build
```

## Équipe

### Onboarding

1. **Documentation claire** : README.md détaillé
2. **Pas de config manuelle** : tout dans devcontainer.json
3. **Scripts automatiques** : postCreateCommand
4. **Support** : canal dédié (Slack, Discord)

### Communication

Quand modifier `.devcontainer/` :
1. Discuter avec l'équipe
2. Tester localement
3. PR avec description détaillée
4. Notifier via message/email
5. Documenter dans CHANGELOG.md

### Migration

Pour migrer un projet existant :

```bash
# 1. Créer .devcontainer/
mkdir .devcontainer

# 2. Utiliser template
F1 → "Dev Containers: Add Dev Container Configuration Files..."

# 3. Personnaliser
# Éditer devcontainer.json

# 4. Tester
F1 → "Dev Containers: Reopen in Container"

# 5. Documenter
# Mettre à jour README.md

# 6. Commiter
git add .devcontainer
git commit -m "feat: add dev container config"
```

## Multi-projets

### Workspace VS Code

```json
// workspace.code-workspace
{
  "folders": [
    { "path": "frontend" },
    { "path": "backend" },
    { "path": "shared" }
  ],
  "settings": {
    "editor.formatOnSave": true
  }
}
```

### Devcontainer par projet

```
monorepo/
├── frontend/
│   └── .devcontainer/
├── backend/
│   └── .devcontainer/
└── shared/
```

Ouvrir individuellement chaque projet.

### Devcontainer partagé

```
monorepo/
├── .devcontainer/
│   ├── devcontainer.json
│   └── docker-compose.yml
├── frontend/
├── backend/
└── shared/
```

Un seul container pour tout le monorepo.

## Patterns anti-patterns

### ❌ Anti-patterns

```json
// ❌ Latest sans version
{
  "image": "node:latest"
}

// ❌ Secrets hardcodés
{
  "containerEnv": {
    "API_KEY": "abc123"
  }
}

// ❌ Root user
{
  "remoteUser": "root"
}

// ❌ Trop d'extensions
{
  "customizations": {
    "vscode": {
      "extensions": [
        // 50 extensions...
      ]
    }
  }
}

// ❌ Pas de documentation
// README.md vide

// ❌ .env commité
// .env dans le repo
```

### ✅ Bonnes pratiques

```json
// ✅ Version spécifique
{
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18-bullseye"
}

// ✅ Variables d'environnement depuis l'hôte
{
  "containerEnv": {
    "API_KEY": "${localEnv:API_KEY}"
  }
}

// ✅ User non-root
{
  "remoteUser": "node"
}

// ✅ Extensions essentielles uniquement
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  }
}

// ✅ README.md complet
// Instructions claires

// ✅ .env.example
// Template pour .env
```

## Checklist déploiement

- [ ] README.md à jour
- [ ] .env.example fourni
- [ ] Versions explicites (image, features)
- [ ] Extensions nécessaires uniquement
- [ ] Ports documentés
- [ ] Scripts testés (postCreateCommand, etc.)
- [ ] Pas de secrets hardcodés
- [ ] remoteUser configuré (non-root)
- [ ] .gitignore complet
- [ ] Tests passent dans le container
- [ ] Documentation troubleshooting
- [ ] Équipe notifiée

## Ressources

### Documentation officielle

- https://containers.dev/
- https://code.visualstudio.com/docs/devcontainers/containers

### Templates

- https://containers.dev/templates

### Features

- https://containers.dev/features

### Community

- GitHub Discussions
- Stack Overflow (tag: dev-containers)
- Discord VS Code

## Conclusion

Les Dev Containers améliorent drastiquement l'expérience de développement quand bien configurés :

✅ **Onboarding rapide** : nouveaux devs opérationnels en minutes
✅ **Reproductibilité** : même environnement pour tous
✅ **Isolation** : pas de pollution de la machine
✅ **Documentation as code** : configuration versionnée

Investir du temps dans la configuration initiale paie sur le long terme !

[← Avancé](./infos-devcontainer-10-sujets-avances.md) | [Index](./infos-devcontainer-00-index.md)

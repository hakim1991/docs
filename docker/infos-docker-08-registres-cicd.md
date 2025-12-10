# 📦 Registres et CI/CD

[← Dockerfile](./infos-docker-07-dockerfile.md) | [Index](./infos-docker-00-index.md) | [Maintenance →](./infos-docker-09-maintenance.md)

---

## Table des matières
- [Container Registries](#container-registries)
- [Docker Hub](#docker-hub)
- [GitHub Container Registry](#github-container-registry)
- [GitLab Container Registry](#gitlab-container-registry)
- [Azure Container Registry](#azure-container-registry)
- [Registry privé](#registry-prive)
- [CI/CD avec Docker](#cicd-avec-docker)

---

## Container Registries

### Qu'est-ce qu'un registry ?

Un **Container Registry** est un service de stockage et distribution d'images Docker.

```
Développeur → Build → Push → Registry → Pull → Production

Local Image → docker push → Registry (Docker Hub, GitHub, etc.)
                                  ↓
                            docker pull → Server
```

### Registries populaires

| Registry | Public | Privé | Gratuit | CI/CD Intégré |
|----------|--------|-------|---------|---------------|
| **Docker Hub** | ✅ | ✅ (limité) | ✅ | ⚠️ |
| **GitHub (GHCR)** | ✅ | ✅ | ✅ | ✅ |
| **GitLab** | ✅ | ✅ | ✅ | ✅ |
| **Azure (ACR)** | ❌ | ✅ | ⚠️ | ✅ |
| **AWS (ECR)** | ❌ | ✅ | ⚠️ | ✅ |
| **Google (GCR)** | ❌ | ✅ | ⚠️ | ✅ |

---

## Docker Hub

### Connexion

```bash
# Se connecter à Docker Hub
docker login

# Avec identifiants
docker login -u username -p password

# Avec access token (recommandé)
docker login -u username --password-stdin
# Puis coller le token

# Se déconnecter
docker logout
```

### Push vers Docker Hub

```bash
# Format: username/repository:tag
docker tag mon-image:latest username/mon-image:latest

# Push
docker push username/mon-image:latest

# Push avec plusieurs tags
docker tag mon-image:latest username/mon-image:1.0.0
docker push username/mon-image:1.0.0
docker push username/mon-image:latest
```

### Pull depuis Docker Hub

```bash
# Pull une image publique
docker pull nginx:alpine
docker pull username/mon-image:latest

# Pull avec digest spécifique
docker pull nginx@sha256:abc123...

# Pull toutes les tags d'un repository
docker pull --all-tags username/mon-image
```

### Repository public vs privé

```bash
# Repository public
# Visible par tous
# Pull gratuit illimité

# Repository privé (Docker Hub)
# Gratuit: 1 repo privé
# Pro: Illimité

# Créer un repo privé sur hub.docker.com
# Repositories → Create Repository → Private
```

---

## GitHub Container Registry

### Configuration

```bash
# Créer un Personal Access Token (PAT)
# GitHub → Settings → Developer settings → Personal access tokens
# Permissions: write:packages, read:packages, delete:packages

# Login avec le token
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Push vers GHCR

```bash
# Format: ghcr.io/username/repository:tag
docker tag mon-image:latest ghcr.io/username/mon-image:latest

# Push
docker push ghcr.io/username/mon-image:latest

# Exemple complet
docker build -t ghcr.io/mycompany/myapp:1.0.0 .
docker push ghcr.io/mycompany/myapp:1.0.0
```

### Pull depuis GHCR

```bash
# Image publique
docker pull ghcr.io/username/image:latest

# Image privée (nécessite login)
docker login ghcr.io
docker pull ghcr.io/username/private-image:latest
```

### GitHub Actions avec GHCR

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## GitLab Container Registry

### Configuration

```bash
# Login avec GitLab token
# GitLab → Settings → Access Tokens
docker login registry.gitlab.com -u USERNAME -p ACCESS_TOKEN

# Ou avec deploy token
docker login registry.gitlab.com -u DEPLOY_TOKEN_NAME -p DEPLOY_TOKEN
```

### Push vers GitLab Registry

```bash
# Format: registry.gitlab.com/group/project:tag
docker tag mon-image:latest registry.gitlab.com/mygroup/myproject:latest

# Push
docker push registry.gitlab.com/mygroup/myproject:latest
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG

before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

build:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - tags

build-tagged:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - tags

deploy:
  stage: deploy
  image: docker:24
  script:
    - docker pull $IMAGE_TAG
    - docker stop myapp || true
    - docker rm myapp || true
    - docker run -d --name myapp -p 80:80 $IMAGE_TAG
  only:
    - main
  environment:
    name: production
    url: https://myapp.example.com
```

---

## Azure Container Registry

### Configuration

```bash
# Login avec Azure CLI
az login
az acr login --name myregistry

# Ou avec service principal
docker login myregistry.azurecr.io -u SERVICE_PRINCIPAL_ID -p SERVICE_PRINCIPAL_PASSWORD
```

### Push vers ACR

```bash
# Format: myregistry.azurecr.io/repository:tag
docker tag mon-image:latest myregistry.azurecr.io/mon-image:latest

# Push
docker push myregistry.azurecr.io/mon-image:latest
```

### Azure DevOps Pipeline

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
  tags:
    include:
      - v*

pool:
  vmImage: 'ubuntu-latest'

variables:
  dockerRegistryServiceConnection: 'MyACRConnection'
  imageRepository: 'myapp'
  containerRegistry: 'myregistry.azurecr.io'
  dockerfilePath: '$(Build.SourcesDirectory)/Dockerfile'
  tag: '$(Build.BuildId)'

stages:
- stage: Build
  displayName: Build and push Docker image
  jobs:
  - job: Build
    displayName: Build
    steps:
    - task: Docker@2
      displayName: Build and push image
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          latest

- stage: Deploy
  displayName: Deploy to production
  dependsOn: Build
  jobs:
  - deployment: Deploy
    displayName: Deploy
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebAppContainer@1
            displayName: Deploy to Azure Web App
            inputs:
              azureSubscription: 'MyAzureSubscription'
              appName: 'myapp'
              containers: '$(containerRegistry)/$(imageRepository):$(tag)'
```

---

## Registry privé

### Déployer un registry local

```bash
# Démarrer un registry local
docker run -d \
  -p 5000:5000 \
  --name registry \
  --restart=always \
  -v registry-data:/var/lib/registry \
  registry:2

# Push vers le registry local
docker tag mon-image:latest localhost:5000/mon-image:latest
docker push localhost:5000/mon-image:latest

# Pull depuis le registry local
docker pull localhost:5000/mon-image:latest
```

### Registry avec authentification

```bash
# Créer un fichier de mots de passe
mkdir auth
docker run --rm \
  --entrypoint htpasswd \
  httpd:2 -Bbn admin password > auth/htpasswd

# Démarrer le registry avec auth
docker run -d \
  -p 5000:5000 \
  --name registry \
  --restart=always \
  -v registry-data:/var/lib/registry \
  -v $(pwd)/auth:/auth \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_REALM="Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  registry:2

# Login
docker login localhost:5000
# Username: admin
# Password: password
```

### Registry avec HTTPS

```bash
# Générer certificats SSL
mkdir certs
openssl req -newkey rsa:4096 -nodes -sha256 \
  -keyout certs/domain.key -x509 -days 365 \
  -out certs/domain.crt

# Démarrer avec HTTPS
docker run -d \
  -p 5000:5000 \
  --name registry \
  --restart=always \
  -v registry-data:/var/lib/registry \
  -v $(pwd)/certs:/certs \
  -v $(pwd)/auth:/auth \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  registry:2
```

### Docker Compose Registry

```yaml
# docker-compose.yml
version: '3.8'

services:
  registry:
    image: registry:2
    container_name: docker-registry
    restart: always
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
      REGISTRY_HTTP_TLS_KEY: /certs/domain.key
      REGISTRY_STORAGE_DELETE_ENABLED: "true"
    volumes:
      - ./data:/var/lib/registry
      - ./auth:/auth
      - ./certs:/certs

  # UI pour le registry
  registry-ui:
    image: joxit/docker-registry-ui:latest
    container_name: registry-ui
    restart: always
    ports:
      - "8080:80"
    environment:
      REGISTRY_TITLE: My Docker Registry
      REGISTRY_URL: https://registry:5000
      DELETE_IMAGES: "true"
      SINGLE_REGISTRY: "true"
    depends_on:
      - registry

volumes:
  data:
```

---

## CI/CD avec Docker

### GitHub Actions - Exemple complet

```yaml
# .github/workflows/docker-cicd.yml
name: Docker CI/CD

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Job 1: Tests
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build test image
        uses: docker/build-push-action@v5
        with:
          context: .
          target: test
          load: true
          tags: ${{ env.IMAGE_NAME }}:test

      - name: Run tests
        run: docker run --rm ${{ env.IMAGE_NAME }}:test npm test

  # Job 2: Build et Push
  build-and-push:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name != 'pull_request'
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # Job 3: Deploy
  deploy:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            docker login ghcr.io -u ${{ github.actor }} -p ${{ secrets.GITHUB_TOKEN }}
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main
            docker stop myapp || true
            docker rm myapp || true
            docker run -d --name myapp -p 80:80 ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main
```

### GitLab CI/CD - Pipeline complète

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE: $CI_REGISTRY_IMAGE
  TAG: $CI_COMMIT_REF_SLUG

# Template pour DinD
.docker:
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

# Tests
test:unit:
  stage: test
  extends: .docker
  script:
    - docker build --target test -t $IMAGE:test .
    - docker run --rm $IMAGE:test npm test
  only:
    - merge_requests
    - main

test:lint:
  stage: test
  extends: .docker
  script:
    - docker build --target test -t $IMAGE:test .
    - docker run --rm $IMAGE:test npm run lint
  only:
    - merge_requests
    - main

# Build
build:main:
  stage: build
  extends: .docker
  script:
    - docker build -t $IMAGE:$TAG .
    - docker push $IMAGE:$TAG
  only:
    - main

build:tag:
  stage: build
  extends: .docker
  script:
    - docker build -t $IMAGE:$CI_COMMIT_TAG -t $IMAGE:latest .
    - docker push $IMAGE:$CI_COMMIT_TAG
    - docker push $IMAGE:latest
  only:
    - tags

# Deploy
deploy:staging:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
  script:
    - ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$STAGING_HOST "
        docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY &&
        docker pull $IMAGE:$TAG &&
        docker stop myapp || true &&
        docker rm myapp || true &&
        docker run -d --name myapp -p 80:80 --restart unless-stopped $IMAGE:$TAG
      "
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main

deploy:production:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
  script:
    - ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$PROD_HOST "
        docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY &&
        docker pull $IMAGE:latest &&
        docker stop myapp || true &&
        docker rm myapp || true &&
        docker run -d --name myapp -p 80:80 --restart unless-stopped $IMAGE:latest
      "
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - tags
```

---

## Best practices

### Sécurité

```bash
# ✅ Utiliser des access tokens (pas de mots de passe)
docker login -u username --password-stdin < token.txt

# ✅ Ne jamais commiter de credentials
# Utiliser des secrets (GitHub Secrets, GitLab CI/CD Variables)

# ✅ Scanner les images pour vulnérabilités
docker scan myimage:latest

# ✅ Signer les images
docker trust sign myimage:latest

# ✅ Utiliser des images officielles
FROM node:18-alpine  # Image officielle vérifiée
```

### Tags et versioning

```bash
# ✅ BON: Tags sémantiques
docker tag myapp:latest myregistry/myapp:1.2.3
docker tag myapp:latest myregistry/myapp:1.2
docker tag myapp:latest myregistry/myapp:1
docker tag myapp:latest myregistry/myapp:latest

# ✅ Tag avec commit SHA
docker tag myapp:latest myregistry/myapp:${CI_COMMIT_SHORT_SHA}

# ❌ Éviter de se fier uniquement au tag 'latest'
# Toujours utiliser des tags versionnés en production
```

### Optimisation CI/CD

```yaml
# Utiliser le cache Docker layers
- name: Build with cache
  uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Build multi-plateforme
- name: Build multi-arch
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64

# Matrix builds
strategy:
  matrix:
    node-version: [16, 18, 20]
```

---

## Commandes de référence rapide

```bash
# Login/Logout
docker login                             # Docker Hub
docker login ghcr.io                     # GitHub
docker login registry.gitlab.com         # GitLab
docker logout

# Push/Pull
docker push user/image:tag               # Push
docker pull user/image:tag               # Pull

# Tags
docker tag source:tag target:tag         # Créer tag

# Registry local
docker run -d -p 5000:5000 registry:2    # Démarrer registry

# Inspection
docker search nginx                      # Rechercher images
docker manifest inspect image:tag        # Voir manifest
```

---

[← Dockerfile](./infos-docker-07-dockerfile.md) | [Index](./infos-docker-00-index.md) | [Maintenance →](./infos-docker-09-maintenance.md)

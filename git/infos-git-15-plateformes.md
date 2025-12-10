# 🐙 GitHub / GitLab / Bitbucket

[← Hooks](./infos-git-14-hooks-automatisation.md) | [Index](./infos-git-00-index.md) | [Bonnes pratiques →](./infos-git-16-bonnes-pratiques.md)

---

## Table des matières
- [GitHub](#github)
- [GitLab](#gitlab)
- [Bitbucket](#bitbucket)
- [Comparaison des plateformes](#comparaison-des-plateformes)
- [CLI Tools](#cli-tools)

---

## GitHub

### Pull Requests

```bash
# 1. Créer une branche
git checkout -b feature/new-feature

# 2. Développer et pousser
git commit -am "feat: add feature"
git push -u origin feature/new-feature

# 3. Sur GitHub: Create Pull Request
# - Base: main
# - Compare: feature/new-feature
# - Titre et description
# - Reviewers, labels, assignees

# 4. Code Review
# - Commentaires sur les lignes
# - Suggestions de code
# - Approve / Request changes

# 5. Merge (options):
# - Merge commit
# - Squash and merge (recommandé)
# - Rebase and merge
```

### Draft Pull Requests

```bash
# PR en cours de développement
# Sur GitHub: Create draft pull request

# Permet:
# - CI/CD sur la branche
# - Feedback précoce
# - Pas prêt pour merge

# Quand prêt:
# Ready for review
```

### GitHub CLI (gh)

```bash
# Installation
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: apt install gh

# Login
gh auth login

# Créer une PR
gh pr create --title "Add feature" --body "Description"
gh pr create --fill  # Depuis commit messages

# Lister les PRs
gh pr list
gh pr list --state open
gh pr list --author @me

# Voir une PR
gh pr view 123
gh pr view --web  # Ouvrir dans le navigateur

# Checkout une PR
gh pr checkout 123

# Review
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Comments"
gh pr review 123 --comment --body "Looks good"

# Merger
gh pr merge 123
gh pr merge 123 --squash
gh pr merge 123 --rebase

# Issues
gh issue create --title "Bug" --body "Description"
gh issue list
gh issue close 456
```

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm test

    - name: Build
      run: npm run build

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### GitHub Pages

```bash
# Déployer un site statique

# Option 1: gh-pages branch
npm install -g gh-pages
gh-pages -d build

# Option 2: GitHub Actions
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: npm ci && npm run build
    - uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./build
```

---

## GitLab

### Merge Requests

```bash
# 1. Créer une branche
git checkout -b feature/new-feature

# 2. Pousser
git push -u origin feature/new-feature

# 3. Sur GitLab: Create merge request
# - Source: feature/new-feature
# - Target: main
# - Titre, description
# - Assignee, labels, milestone

# 4. Pipeline CI/CD automatique

# 5. Review et merge
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"

# Template pour Node.js
.node_template: &node
  image: node:${NODE_VERSION}
  before_script:
    - npm ci

# Tests
test:
  <<: *node
  stage: test
  script:
    - npm run lint
    - npm test
  coverage: '/Statements\s+:\s+(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

# Build
build:
  <<: *node
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
  only:
    - main

# Deploy
deploy:production:
  stage: deploy
  script:
    - npm run deploy
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

### GitLab CLI (glab)

```bash
# Installation
# Windows: scoop install glab
# Mac: brew install glab
# Linux: apt install glab

# Login
glab auth login

# MR
glab mr create --title "Add feature"
glab mr list
glab mr view 123
glab mr checkout 123
glab mr merge 123

# Issues
glab issue create --title "Bug"
glab issue list
glab issue close 456

# Pipelines
glab ci view
glab ci trace
glab ci lint
```

---

## Bitbucket

### Pull Requests

```bash
# Similaire à GitHub/GitLab

# Créer une branche
git checkout -b feature/new-feature
git push -u origin feature/new-feature

# Sur Bitbucket: Create pull request
# - Source: feature/new-feature
# - Destination: main

# Review et merge
```

### Bitbucket Pipelines

```yaml
# bitbucket-pipelines.yml
image: node:18

pipelines:
  default:
    - step:
        name: Test and Build
        caches:
          - node
        script:
          - npm ci
          - npm run lint
          - npm test
          - npm run build
        artifacts:
          - dist/**

  branches:
    main:
      - step:
          name: Deploy to Production
          deployment: production
          script:
            - npm run deploy
```

---

## Comparaison des plateformes

### Tableau comparatif

| Fonctionnalité | GitHub | GitLab | Bitbucket |
|----------------|--------|--------|-----------|
| **Gratuit** | ✅ Public illimité | ✅ Public + Privé | ✅ Petit équipe |
| **CI/CD intégré** | ✅ Actions | ✅ Très complet | ✅ Pipelines |
| **Self-hosted** | ❌ Payant | ✅ Gratuit | ✅ Payant |
| **Issues** | ✅ Basique | ✅ Avancé | ✅ Jira intégré |
| **Wiki** | ✅ | ✅ | ✅ |
| **Pages** | ✅ | ✅ | ❌ |
| **CLI** | ✅ gh | ✅ glab | ⚠️ Limité |
| **API** | ✅ Excellente | ✅ Excellente | ✅ Bonne |
| **Popularité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

### Recommandations

**GitHub** ✅
- Open source
- Communauté
- Popularité
- GitHub Actions

**GitLab** ✅
- CI/CD complet
- Self-hosted gratuit
- DevOps complet
- Enterprise

**Bitbucket** ✅
- Intégration Atlassian
- Jira
- Confluence
- Petites équipes

---

## CLI Tools

### gh (GitHub CLI)

```bash
# Repository
gh repo create mon-projet --public
gh repo clone user/repo
gh repo view
gh repo fork

# Pull Requests
gh pr create
gh pr list
gh pr view 123
gh pr checkout 123
gh pr merge 123 --squash
gh pr review 123 --approve

# Issues
gh issue create
gh issue list
gh issue close 456

# Releases
gh release create v1.0.0
gh release list
gh release download v1.0.0

# Workflows
gh workflow list
gh workflow run ci.yml
gh run list
gh run view
```

### glab (GitLab CLI)

```bash
# Repository
glab repo clone group/project
glab repo view

# Merge Requests
glab mr create
glab mr list
glab mr view 123
glab mr checkout 123
glab mr merge 123

# Issues
glab issue create
glab issue list
glab issue close 456

# Pipelines
glab ci view
glab ci trace
glab ci lint
glab ci run

# Variables
glab variable list
glab variable set KEY value
```

### Configuration des CLI

```bash
# GitHub CLI
gh auth login
gh config set editor vim
gh config set git_protocol ssh

# GitLab CLI
glab auth login
glab config set editor vim
glab config set gitlab_uri https://gitlab.com
```

---

## Workflows avancés

### Automatisation PR/MR

```bash
# Script: create-pr.sh
#!/bin/bash

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# GitHub
gh pr create \
  --title "$(git log -1 --pretty=%s)" \
  --body "$(git log -1 --pretty=%b)" \
  --base main \
  --head $BRANCH

# GitLab
glab mr create \
  --title "$(git log -1 --pretty=%s)" \
  --description "$(git log -1 --pretty=%b)" \
  --target-branch main \
  --source-branch $BRANCH
```

### Protection de branches

**GitHub:**
```
Settings → Branches → Add rule
- Require pull request reviews
- Require status checks
- Require signed commits
- Include administrators
```

**GitLab:**
```
Settings → Repository → Protected branches
- Allowed to merge: Maintainers
- Allowed to push: No one
- Allowed to force push: No
```

### Templates

**GitHub Pull Request Template:**
```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## Description
Brief description of changes

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change

## Checklist
- [ ] Tests added
- [ ] Documentation updated
- [ ] Code reviewed
```

**GitLab Merge Request Template:**
```markdown
<!-- .gitlab/merge_request_templates/default.md -->
## What does this MR do?
Description

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Changelog updated
```

---

## Commandes de référence rapide

```bash
# GitHub CLI (gh)
gh pr create                    # Créer PR
gh pr list                      # Lister PRs
gh pr merge 123 --squash        # Merger PR
gh issue create                 # Créer issue
gh release create v1.0.0        # Release

# GitLab CLI (glab)
glab mr create                  # Créer MR
glab mr list                    # Lister MRs
glab mr merge 123               # Merger MR
glab ci view                    # Voir pipeline
glab issue create               # Créer issue
```

---

[← Hooks](./infos-git-14-hooks-automatisation.md) | [Index](./infos-git-00-index.md) | [Bonnes pratiques →](./infos-git-16-bonnes-pratiques.md)

# ✅ Bonnes Pratiques Git

[← Plateformes](./infos-git-15-plateformes.md) | [Index](./infos-git-00-index.md) | [Troubleshooting →](./infos-git-17-troubleshooting.md)

---

## Table des matières
- [Messages de commit](#messages-de-commit)
- [Commits](#commits)
- [Branches](#branches)
- [Collaboration](#collaboration)
- [Sécurité](#securite)
- [Performance](#performance)

---

## Messages de commit

### Format recommandé

```bash
# Format Conventional Commits
<type>(<scope>): <subject>

<body>

<footer>
```

### Types de commits

```bash
feat:     Nouvelle fonctionnalité
fix:      Correction de bug
docs:     Documentation uniquement
style:    Formatage (pas de changement de logique)
refactor: Refactoring (ni fix ni feat)
perf:     Amélioration de performance
test:     Ajout ou modification de tests
build:    Build system (webpack, npm, etc.)
ci:       CI/CD (GitHub Actions, etc.)
chore:    Maintenance (dépendances, etc.)
revert:   Annulation d'un commit précédent
```

### Exemples de bons messages

```bash
# ✅ BON: Clair et descriptif
git commit -m "feat(auth): add JWT token validation

Implement token validation middleware to secure API endpoints.
Tokens are validated using jsonwebtoken library.

Closes #123"

# ✅ BON: Bug fix détaillé
git commit -m "fix(api): resolve memory leak in cache service

The cache was not clearing expired entries, causing memory
to grow indefinitely. Added automatic cleanup every 5 minutes.

Fixes #456"

# ✅ BON: Breaking change
git commit -m "feat!: change API response format

BREAKING CHANGE: API responses now wrapped in { data, meta }
instead of returning data directly.

Migration guide in docs/migration-v2.md

Closes #789"

# ❌ MAUVAIS: Vague
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
git commit -m "WIP"

# ❌ MAUVAIS: Trop long dans le sujet
git commit -m "feat: add user authentication with JWT tokens and refresh tokens and password reset functionality"

# ✅ BON: Sujet court, détails dans le body
git commit -m "feat(auth): add complete authentication system

Features:
- JWT access and refresh tokens
- Password reset via email
- Account verification
- Session management

Closes #100, #101, #102"
```

### Règles d'or

```bash
# 1. Sujet: 50 caractères max
# 2. Body: 72 caractères par ligne
# 3. Impératif: "add" pas "added" ou "adds"
# 4. Première lettre minuscule après le type
# 5. Pas de point à la fin du sujet
# 6. Ligne vide entre sujet et body
# 7. Expliquer le "pourquoi", pas le "quoi"

# ✅ BON
git commit -m "fix: resolve null pointer exception

User.email was null when fetched from cache because
the cache serialization was stripping null values."

# ❌ MAUVAIS
git commit -m "Fixed a bug where User.email was null."
```

---

## Commits

### Commits atomiques

**Un commit = une chose**

```bash
# ❌ MAUVAIS: Tout mélangé
git add .
git commit -m "Add login and fix bugs and update docs"

# ✅ BON: Commits séparés
git add src/auth/login.js
git commit -m "feat(auth): add login endpoint"

git add src/auth/validate.js
git commit -m "fix(auth): resolve token validation bug"

git add README.md
git commit -m "docs: update authentication guide"
```

### Quand commiter ?

```bash
# ✅ Commiter quand:
- Une fonctionnalité est complète
- Un bug est fixé
- Un refactoring logique est terminé
- Avant de changer de tâche
- Fin de journée (au moins une fois)

# ❌ Ne pas commiter:
- Code qui ne compile pas
- Tests qui échouent (sauf WIP marqué)
- Code non testé
- Fichiers temporaires
- Secrets / credentials
```

### Commits fréquents

```bash
# ✅ BON: Commits réguliers (plusieurs par jour)
10h00: git commit -m "feat: add user model"
11h30: git commit -m "feat: add user API endpoints"
14h00: git commit -m "test: add user API tests"
16h00: git commit -m "docs: add API documentation"

# ❌ MAUVAIS: Un seul commit en fin de semaine
vendredi 17h: git commit -m "Add entire user management system"
```

### Amend vs nouveau commit

```bash
# ✅ Amend: Correction immédiate
git commit -m "feat: add login"
# Oups, oublié un fichier
git add forgotten-file.js
git commit --amend --no-edit

# ✅ Nouveau commit: Correction après review
git commit -m "feat: add login"
git push
# Review: "Please add validation"
git commit -m "feat: add login validation"
git push

# ❌ Ne pas amend après push (réécrit l'historique)
```

---

## Branches

### Nommage des branches

```bash
# Convention: type/description

# ✅ BON
feature/user-authentication
feature/dashboard-redesign
bugfix/login-timeout
bugfix/memory-leak-in-cache
hotfix/critical-security-patch
release/v1.2.0
chore/update-dependencies

# ❌ MAUVAIS
my-branch
test
fix
new-stuff
branch-2024-01-15
```

### Durée de vie des branches

```bash
# ✅ BON: Branches courtes (1-3 jours)
lundi: créer feature/login
mardi: développer
mercredi: merge

# ❌ MAUVAIS: Branches longues (plusieurs semaines)
# Problèmes:
# - Merge conflicts
# - Code qui diverge
# - Review difficile

# Solution pour grandes features:
# Diviser en petites branches
feature/login-ui
feature/login-api
feature/login-validation
```

### Nettoyage des branches

```bash
# Après merge, supprimer la branche
git branch -d feature/login
git push origin --delete feature/login

# Nettoyer les branches remote supprimées
git fetch --prune

# Supprimer les branches mergées localement
git branch --merged | grep -v "\*\|main\|develop" | xargs git branch -d
```

---

## Collaboration

### Pull Requests / Merge Requests

```bash
# ✅ BON: PR description complète
Title: feat(auth): Add JWT authentication

Description:
## What
Implement JWT authentication with access and refresh tokens.

## Why
Current session-based auth doesn't work for mobile apps.

## How
- JWT tokens with 15min expiry
- Refresh tokens with 7 days expiry
- Stored in HTTP-only cookies

## Testing
- Unit tests for token generation/validation
- Integration tests for auth endpoints
- Manual testing with Postman

## Screenshots
[Screenshots of login flow]

## Checklist
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
- [x] Code reviewed

# ❌ MAUVAIS: PR vague
Title: Update auth
Description: Made some changes
```

### Code Review

```bash
# ✅ Pour le reviewer:
# - Review dans les 24h
# - Commentaires constructifs
# - Tester localement si possible
# - Approuver ou demander des changements clairement

# ✅ Pour l'auteur:
# - PR de taille raisonnable (< 400 lignes)
# - Tests inclus
# - Documentation à jour
# - Répondre aux commentaires rapidement
# - Ne pas prendre personnellement
```

### Résolution de conflits

```bash
# ✅ BON: Résoudre dès qu'ils apparaissent
git fetch origin
git merge origin/main
# Résoudre les conflits
git commit

# ❌ MAUVAIS: Ignorer les conflits
# Accumulation de conflits = cauchemar

# Prévention:
git pull --rebase origin main  # Régulièrement
```

---

## Sécurité

### Ne jamais commiter de secrets

```bash
# ❌ JAMAIS commiter:
# - Mots de passe
# - API keys
# - Tokens
# - Certificats privés
# - .env files avec secrets

# ✅ Utiliser:
# - Variables d'environnement
# - .env.example (sans valeurs)
# - Secrets managers (AWS Secrets, etc.)
# - .gitignore

# .gitignore
.env
.env.local
*.key
*.pem
secrets/
config/local.js
```

### Si secrets commitées

```bash
# 1. Supprimer immédiatement de l'historique
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret" \
  --prune-empty --tag-name-filter cat -- --all

# Ou avec git-filter-repo (plus rapide)
git filter-repo --path path/to/secret --invert-paths

# 2. Force push (⚠️ Coordonner avec l'équipe)
git push origin --force --all

# 3. Révoquer/changer les secrets exposés

# 4. Notifier l'équipe
```

### Signer les commits (GPG)

```bash
# Configurer GPG
gpg --full-generate-key
gpg --list-secret-keys --keyid-format LONG

# Configurer Git
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Commits signés automatiquement
git commit -m "feat: add feature"
# ✅ Verified commit

# Vérifier les signatures
git log --show-signature
```

---

## Performance

### .gitignore optimal

```bash
# Toujours ignorer:

# Dependencies
node_modules/
vendor/
*.egg-info/

# Build artifacts
dist/
build/
*.o
*.so
*.exe

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporaire
tmp/
temp/
*.tmp

# Tests
coverage/
.nyc_output/

# Environment
.env
.env.local
```

### Fichiers volumineux

```bash
# ❌ Ne pas commiter:
# - Fichiers binaires larges
# - Vidéos
# - Images haute résolution
# - Datasets
# - Builds compilés

# ✅ Utiliser Git LFS
git lfs install
git lfs track "*.psd"
git lfs track "*.mp4"
git add .gitattributes
```

### Shallow clone

```bash
# Pour gros repositories
git clone --depth 1 https://github.com/user/repo.git

# CI/CD: toujours shallow
# .github/workflows/ci.yml
- uses: actions/checkout@v3
  with:
    fetch-depth: 1  # Shallow clone
```

---

## Documentation

### README.md

```markdown
# Project Name

Brief description

## Features
- Feature 1
- Feature 2

## Installation
\`\`\`bash
npm install
\`\`\`

## Usage
\`\`\`bash
npm start
\`\`\`

## Development
\`\`\`bash
npm run dev
\`\`\`

## Testing
\`\`\`bash
npm test
\`\`\`

## Contributing
See CONTRIBUTING.md

## License
MIT
```

### CONTRIBUTING.md

```markdown
# Contributing Guide

## Getting Started
1. Fork the repository
2. Clone your fork
3. Create a branch
4. Make changes
5. Push and create PR

## Code Style
- Follow ESLint rules
- Run `npm run lint` before commit

## Commit Messages
Use Conventional Commits format

## Pull Requests
- Small, focused PRs
- Include tests
- Update documentation
```

### CHANGELOG.md

```markdown
# Changelog

## [1.1.0] - 2024-01-15

### Added
- User authentication
- Profile management

### Fixed
- Login timeout issue
- Memory leak in cache

### Changed
- API response format

## [1.0.0] - 2024-01-01

Initial release
```

---

## Checklist du développeur

### Avant chaque commit

```bash
✅ Code compile
✅ Tests passent
✅ Linter OK
✅ Pas de secrets
✅ Message descriptif
✅ Fichiers pertinents uniquement
```

### Avant chaque push

```bash
✅ Branche à jour avec main
✅ Conflits résolus
✅ Tests complets passent
✅ Documentation à jour
✅ Changelog mis à jour (si release)
```

### Avant chaque PR

```bash
✅ Description complète
✅ Screenshots/vidéos si UI
✅ Tests inclus
✅ Pas de breaking changes (ou documentés)
✅ PR de taille raisonnable
✅ Reviewers assignés
```

---

## Commandes de référence rapide

```bash
# Commits de qualité
git commit -m "type(scope): subject"  # Conventional Commits
git commit --amend --no-edit          # Corriger dernier commit

# Branches propres
git branch -d feature                 # Supprimer branche
git branch --merged | grep -v main | xargs git branch -d  # Nettoyer

# Sécurité
git config commit.gpgsign true        # Signer commits
echo ".env" >> .gitignore             # Ignorer secrets

# Performance
git clone --depth 1 URL               # Shallow clone
git lfs install                       # Git LFS
```

---

[← Plateformes](./infos-git-15-plateformes.md) | [Index](./infos-git-00-index.md) | [Troubleshooting →](./infos-git-17-troubleshooting.md)

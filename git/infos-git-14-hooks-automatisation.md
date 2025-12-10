# 🪝 Hooks et Automatisation

[← Outils avancés](./infos-git-13-outils-avances.md) | [Index](./infos-git-00-index.md) | [Plateformes →](./infos-git-15-plateformes.md)

---

## Table des matières
- [Qu'est-ce qu'un hook ?](#quest-ce-quun-hook)
- [Hooks côté client](#hooks-cote-client)
- [Hooks côté serveur](#hooks-cote-serveur)
- [Créer des hooks](#creer-des-hooks)
- [Husky (Node.js)](#husky-nodejs)
- [Automatisation avancée](#automatisation-avancee)

---

## Qu'est-ce qu'un hook ?

### Définition

Les **hooks** sont des **scripts automatiques** exécutés à certains moments du workflow Git.

```
Événement Git → Hook script → Action
```

### Emplacement

```bash
# Hooks dans .git/hooks/
.git/hooks/
├── pre-commit.sample
├── pre-push.sample
├── commit-msg.sample
└── ...

# Pour activer un hook:
mv .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Hooks côté client

### pre-commit

Exécuté **avant** la création du commit.

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running pre-commit hook..."

# Linter
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ Linting failed"
    exit 1
fi

# Tests
npm test
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi

echo "✅ Pre-commit checks passed"
exit 0
```

**Cas d'usage:**
- Linter (ESLint, Prettier)
- Tests unitaires
- Vérification de formatage
- Détection de secrets

### prepare-commit-msg

Prépare le message de commit avant l'éditeur.

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

# Ajouter le numéro de ticket depuis le nom de branche
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TICKET=$(echo $BRANCH | grep -oP 'JIRA-\d+')

if [ -n "$TICKET" ]; then
    echo "$TICKET: $(cat $COMMIT_MSG_FILE)" > $COMMIT_MSG_FILE
fi
```

### commit-msg

Valide le message de commit.

```bash
# .git/hooks/commit-msg
#!/bin/bash

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat $COMMIT_MSG_FILE)

# Vérifier le format Conventional Commits
PATTERN="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"

if ! echo "$COMMIT_MSG" | grep -qE "$PATTERN"; then
    echo "❌ Invalid commit message format"
    echo "Format: <type>(<scope>): <subject>"
    echo "Example: feat(auth): add login"
    exit 1
fi

echo "✅ Commit message valid"
exit 0
```

### post-commit

Exécuté après la création du commit.

```bash
# .git/hooks/post-commit
#!/bin/bash

# Notification
notify-send "Git Commit" "Commit created successfully"

# Log
echo "$(date): Commit $(git rev-parse HEAD)" >> .git/commit.log
```

### pre-push

Exécuté avant le push.

```bash
# .git/hooks/pre-push
#!/bin/bash

echo "Running pre-push hook..."

# Tests complets
npm run test:full
if [ $? -ne 0 ]; then
    echo "❌ Tests failed, push cancelled"
    exit 1
fi

# Build
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Build failed, push cancelled"
    exit 1
fi

echo "✅ Pre-push checks passed"
exit 0
```

**Cas d'usage:**
- Tests d'intégration
- Build
- Vérification de la branche
- Empêcher push sur main

---

## Hooks côté serveur

### pre-receive

Exécuté sur le serveur avant d'accepter le push.

```bash
# Empêcher push force sur main
#!/bin/bash

while read oldrev newrev refname; do
    if [ "$refname" = "refs/heads/main" ]; then
        if [ "$oldrev" != "0000000000000000000000000000000000000000" ]; then
            # Vérifier si c'est un force push
            if ! git merge-base --is-ancestor $oldrev $newrev; then
                echo "❌ Force push to main is not allowed"
                exit 1
            fi
        fi
    fi
done
```

### update

Exécuté sur le serveur pour chaque branche pushée.

```bash
#!/bin/bash

refname="$1"
oldrev="$2"
newrev="$3"

# Empêcher suppression de branches protégées
if [ "$refname" = "refs/heads/main" ] && [ "$newrev" = "0000000000000000000000000000000000000000" ]; then
    echo "❌ Cannot delete main branch"
    exit 1
fi

exit 0
```

### post-receive

Exécuté après que le push soit accepté.

```bash
#!/bin/bash

# Déploiement automatique
while read oldrev newrev refname; do
    if [ "$refname" = "refs/heads/main" ]; then
        echo "Deploying to production..."
        cd /var/www/app
        git pull origin main
        npm install
        npm run build
        pm2 restart app
        echo "✅ Deployed successfully"
    fi
done
```

---

## Créer des hooks

### Exemple complet: Pre-commit

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running pre-commit checks..."

# 1. Vérifier les fichiers staged
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.js$')

if [ -z "$FILES" ]; then
    echo "No JS files to check"
    exit 0
fi

# 2. ESLint
echo "📝 Running ESLint..."
npx eslint $FILES
if [ $? -ne 0 ]; then
    echo "❌ ESLint failed. Fix errors and try again."
    exit 1
fi

# 3. Prettier
echo "💅 Running Prettier..."
npx prettier --check $FILES
if [ $? -ne 0 ]; then
    echo "❌ Prettier check failed. Run 'npm run format'"
    exit 1
fi

# 4. Tests affectés
echo "🧪 Running tests..."
npm test -- --findRelatedTests $FILES
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi

# 5. Vérifier les secrets
echo "🔒 Checking for secrets..."
if grep -rE '(password|secret|api[_-]?key|token).{0,5}[=:].{0,5}["\x27][a-zA-Z0-9]{10,}["\x27]' $FILES; then
    echo "❌ Possible secret detected!"
    exit 1
fi

echo "✅ All checks passed!"
exit 0
```

### Partager les hooks

Les hooks dans `.git/hooks/` ne sont PAS versionnés.

**Solution:** Dossier de hooks partagé

```bash
# Créer un dossier de hooks
mkdir .githooks

# Script pre-commit
cat > .githooks/pre-commit << 'EOF'
#!/bin/bash
npm run lint && npm test
EOF

chmod +x .githooks/pre-commit

# Configurer Git pour utiliser ce dossier
git config core.hooksPath .githooks

# Dans le README
echo "Run: git config core.hooksPath .githooks" >> README.md
```

---

## Husky (Node.js)

### Installation

```bash
# Installer Husky
npm install --save-dev husky

# Initialiser
npx husky install

# Ajouter au package.json
npm pkg set scripts.prepare="husky install"
```

### Créer des hooks avec Husky

```bash
# Créer pre-commit hook
npx husky add .husky/pre-commit "npm run lint"
npx husky add .husky/pre-commit "npm test"

# Créer commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'

# Créer pre-push hook
npx husky add .husky/pre-push "npm run build"
```

### Configuration complète

```json
// package.json
{
  "scripts": {
    "prepare": "husky install",
    "lint": "eslint .",
    "format": "prettier --write .",
    "test": "jest",
    "build": "webpack"
  },
  "devDependencies": {
    "husky": "^8.0.0",
    "lint-staged": "^13.0.0",
    "@commitlint/cli": "^17.0.0",
    "@commitlint/config-conventional": "^17.0.0"
  },
  "lint-staged": {
    "*.js": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

```bash
# .husky/commit-msg
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx --no -- commitlint --edit $1
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']
    ],
    'subject-max-length': [2, 'always', 72]
  }
};
```

### lint-staged

Exécuter des commandes seulement sur les fichiers staged.

```bash
# Installer
npm install --save-dev lint-staged

# Configurer dans package.json
```

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --findRelatedTests"
    ],
    "*.{css,scss}": [
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

---

## Automatisation avancée

### Workflow complet avec hooks

```bash
# Installation du projet
npm install

# Configuration automatique
# package.json
{
  "scripts": {
    "prepare": "husky install && npm run setup-git",
    "setup-git": "git config core.hooksPath .husky"
  }
}

# Hooks configurés:
# - pre-commit: lint + format + tests
# - commit-msg: validate message
# - pre-push: build + full tests

# Workflow développeur:
# 1. git add .
# 2. git commit -m "feat: add feature"
#    → lint-staged s'exécute
#    → commitlint valide le message
# 3. git push
#    → build + tests complets
#    → push si tout OK
```

### Protection des branches

```bash
# .git/hooks/pre-push
#!/bin/bash

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Empêcher push direct sur main
if [ "$BRANCH" = "main" ]; then
    echo "❌ Direct push to main is not allowed"
    echo "Please create a Pull Request"
    exit 1
fi

# Vérifier que la branche est à jour
git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "⚠️  Your branch is behind origin"
    echo "Run: git pull --rebase"
    exit 1
fi

exit 0
```

### Génération automatique de changelog

```bash
# .git/hooks/post-commit
#!/bin/bash

# Générer changelog après chaque commit
npx conventional-changelog -p angular -i CHANGELOG.md -s

# Add si changé
if ! git diff --quiet CHANGELOG.md; then
    git add CHANGELOG.md
    git commit --amend --no-edit
fi
```

### Notification

```bash
# .git/hooks/post-commit
#!/bin/bash

# Notification desktop
notify-send "Git Commit" "Commit $(git rev-parse --short HEAD) created"

# Notification Slack
COMMIT_MSG=$(git log -1 --pretty=%B)
AUTHOR=$(git config user.name)
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"$AUTHOR committed: $COMMIT_MSG\"}"
```

---

## Bypass des hooks

```bash
# Skip pre-commit hook
git commit --no-verify -m "message"
git commit -n -m "message"

# Skip tous les hooks
git push --no-verify

# ⚠️ À utiliser avec précaution !
```

---

## Commandes de référence rapide

```bash
# Hooks manuels
chmod +x .git/hooks/pre-commit  # Activer
git commit --no-verify           # Skip hooks

# Husky
npx husky install                # Initialiser
npx husky add .husky/pre-commit "npm test"  # Ajouter hook

# lint-staged
npx lint-staged                  # Exécuter

# Configuration
git config core.hooksPath .githooks  # Dossier custom
```

---

[← Outils avancés](./infos-git-13-outils-avances.md) | [Index](./infos-git-00-index.md) | [Plateformes →](./infos-git-15-plateformes.md)

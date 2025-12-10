# 📦 NPM et Packages

[← Bases de Node.js](./infos-nodejs-02-bases-nodejs.md) | [Index](./infos-nodejs-00-index.md) | [Modules →](./infos-nodejs-04-modules-commonjs-esm.md)

## Initialiser un projet

### npm init

```bash
# Init interactif
npm init

# Init avec valeurs par défaut
npm init -y
npm init --yes

# Avec scope
npm init --scope=@username

# Résultat: package.json créé
```

### package.json

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "Mon projet Node.js",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": ["nodejs", "example"],
  "author": "John Doe",
  "license": "MIT"
}
```

### Champs importants

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "Description du projet",
  "main": "index.js",
  "type": "module",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack"
  },
  "keywords": ["keyword1", "keyword2"],
  "author": "Name <email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "bugs": {
    "url": "https://github.com/user/repo/issues"
  },
  "homepage": "https://github.com/user/repo#readme",
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=8.0.0"
  }
}
```

## Installer des packages

### Installation basique

```bash
# Installer package
npm install express
npm i express

# Installer plusieurs packages
npm install express cors dotenv

# Installer version spécifique
npm install express@4.18.0

# Installer dernière version
npm install express@latest

# Installer version avec range
npm install express@^4.0.0
npm install express@~4.18.0
```

### Types d'installation

```bash
# Dependencies (production)
npm install express
npm install --save express          # Par défaut
npm i -S express

# DevDependencies (développement uniquement)
npm install --save-dev jest
npm i -D jest
npm i --save-dev nodemon eslint

# Global
npm install -g nodemon
npm i -g typescript

# Pas de save (test temporaire)
npm install --no-save express

# Optional dependencies
npm install --save-optional package-name
```

### package.json après installation

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.0.3"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.5.0",
    "eslint": "^8.45.0"
  }
}
```

## Versions et Semver

### Semantic Versioning

```
Version: MAJOR.MINOR.PATCH

MAJOR: Breaking changes (incompatible API)
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)

Exemple: 4.18.2
- 4: Major version
- 18: Minor version
- 2: Patch version
```

### Ranges de versions

```json
{
  "dependencies": {
    "express": "4.18.2",      // Version exacte
    "cors": "^2.8.5",         // ^2.8.5 <= version < 3.0.0
    "dotenv": "~16.0.3",      // ~16.0.3 <= version < 16.1.0
    "lodash": "*",            // Dernière version
    "axios": ">=1.0.0",       // >= 1.0.0
    "moment": "<3.0.0",       // < 3.0.0
    "chalk": ">=4.0.0 <5.0.0" // Range
  }
}
```

### Symboles de version

```
^4.18.2    Caret: Updates compatible (MINOR et PATCH)
~4.18.2    Tilde: Updates PATCH uniquement
*          Dernière version
latest     Dernière version
4.x        Dernière version 4.x.x
4.18.x     Dernière version 4.18.x
```

## package-lock.json

### Utilité

```json
// package-lock.json
// Verrouille les versions exactes de toutes les dépendances
// (y compris dépendances transitives)

{
  "name": "my-project",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "my-project",
      "version": "1.0.0",
      "dependencies": {
        "express": "^4.18.2"
      }
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-...",
      "dependencies": {
        "body-parser": "1.20.1"
      }
    }
  }
}
```

### Commandes lock

```bash
# Générer/updater lock file
npm install

# Installer depuis lock file exact
npm ci

# Ignorer lock file
npm install --no-package-lock

# Update lock file uniquement
npm install --package-lock-only
```

## Gérer les dépendances

### Lister packages

```bash
# Lister dépendances installées
npm list
npm ls

# Lister avec profondeur
npm ls --depth=0          # Niveau racine uniquement
npm ls --depth=1

# Lister global
npm ls -g --depth=0

# Lister specific package
npm ls express

# Lister outdated
npm outdated

# Format JSON
npm ls --json
```

### Mettre à jour packages

```bash
# Update tous les packages (respect semver)
npm update
npm up

# Update package spécifique
npm update express

# Update à latest (ignore semver)
npm install express@latest

# Update global
npm update -g

# Check outdated
npm outdated
```

### Supprimer packages

```bash
# Uninstall package
npm uninstall express
npm remove express
npm rm express
npm un express

# Uninstall devDependency
npm uninstall -D jest

# Uninstall global
npm uninstall -g nodemon

# Prune (supprimer unused packages)
npm prune

# Prune devDependencies
npm prune --production
```

## Scripts NPM

### Scripts basiques

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "build": "webpack",
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

```bash
# Exécuter scripts
npm start              # Raccourci pour npm run start
npm test               # Raccourci pour npm run test

npm run dev
npm run build
npm run lint
npm run format
```

### Scripts avancés

```json
{
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest --coverage",
    "test:watch": "jest --watch",
    "build": "webpack --mode production",
    "build:dev": "webpack --mode development",
    "clean": "rm -rf dist",
    "prebuild": "npm run clean",
    "postbuild": "echo 'Build complete'",
    "lint": "eslint src/**/*.js",
    "lint:fix": "eslint src/**/*.js --fix",
    "format": "prettier --write src/**/*.js",
    "prepare": "husky install"
  }
}
```

### Hooks scripts

```json
{
  "scripts": {
    "prebuild": "echo 'Before build'",
    "build": "webpack",
    "postbuild": "echo 'After build'",

    "pretest": "echo 'Before test'",
    "test": "jest",
    "posttest": "echo 'After test'"
  }
}
```

```bash
npm run build
# Exécute: prebuild -> build -> postbuild
```

### Scripts avec arguments

```json
{
  "scripts": {
    "start": "node index.js",
    "start:prod": "NODE_ENV=production node index.js",
    "start:port": "node index.js --port"
  }
}
```

```bash
# Passer arguments
npm run start:port -- 8080

# Variables d'environnement
npm run start:prod
```

### Scripts cross-platform

```bash
# Installer cross-env pour compatibilité Windows/Unix
npm install --save-dev cross-env
```

```json
{
  "scripts": {
    "start": "cross-env NODE_ENV=production node index.js",
    "dev": "cross-env NODE_ENV=development nodemon index.js"
  }
}
```

## Configuration NPM

### .npmrc

```bash
# Créer .npmrc
touch .npmrc
```

```ini
# .npmrc

# Registry
registry=https://registry.npmjs.org/

# Scope registry
@mycompany:registry=https://npm.mycompany.com/

# Auth token
//registry.npmjs.org/:_authToken=${NPM_TOKEN}

# Save exact versions
save-exact=true

# Save prefix
save-prefix=~

# Engine strict
engine-strict=true

# Init defaults
init-author-name=John Doe
init-author-email=john@example.com
init-license=MIT
init-version=1.0.0
```

### Config via CLI

```bash
# Voir config
npm config list
npm config ls

# Get value
npm config get registry
npm config get init-author-name

# Set value
npm config set init-author-name "John Doe"
npm config set save-exact true

# Delete value
npm config delete key

# Edit config file
npm config edit
```

## Packages utiles

### Packages de développement

```bash
# Hot reload
npm install --save-dev nodemon

# Linting
npm install --save-dev eslint

# Formatting
npm install --save-dev prettier

# Testing
npm install --save-dev jest

# TypeScript
npm install --save-dev typescript @types/node

# Build tools
npm install --save-dev webpack webpack-cli
```

### Packages production

```bash
# Web framework
npm install express

# Environment variables
npm install dotenv

# CORS
npm install cors

# Body parser (intégré dans Express 4.16+)
npm install body-parser

# Validation
npm install joi
npm install validator

# Database
npm install mongoose        # MongoDB
npm install pg             # PostgreSQL
npm install mysql2         # MySQL

# Authentication
npm install jsonwebtoken
npm install bcrypt

# HTTP client
npm install axios

# Utilities
npm install lodash
npm install moment
npm install uuid
```

## npx

### Utiliser npx

```bash
# Exécuter package sans installer
npx create-react-app my-app
npx cowsay "Hello"

# Exécuter version spécifique
npx node@18 --version

# Exécuter local package
npx jest

# Force remote package
npx --yes create-react-app@latest my-app
```

## Publier un package

### Préparer publication

```json
{
  "name": "my-awesome-package",
  "version": "1.0.0",
  "description": "Description du package",
  "main": "index.js",
  "keywords": ["awesome", "package"],
  "author": "John Doe",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "files": [
    "index.js",
    "lib/",
    "README.md"
  ]
}
```

### .npmignore

```
# .npmignore
node_modules/
test/
*.test.js
.env
.git
.DS_Store
coverage/
```

### Publier

```bash
# Login
npm login

# Test avant publication
npm pack

# Publish
npm publish

# Publish avec tag
npm publish --tag beta

# Publish scoped package
npm publish --access public

# Unpublish (dans 72h)
npm unpublish my-package@1.0.0
```

## Alternatives à NPM

### Yarn

```bash
# Installer Yarn
npm install -g yarn

# Commandes équivalentes
npm install          -> yarn install / yarn
npm install express  -> yarn add express
npm uninstall        -> yarn remove
npm update           -> yarn upgrade
npm run script       -> yarn script
```

### PNPM

```bash
# Installer pnpm
npm install -g pnpm

# Commandes équivalentes
npm install          -> pnpm install / pnpm i
npm install express  -> pnpm add express
npm uninstall        -> pnpm remove
npm update           -> pnpm update
npm run script       -> pnpm script
```

## Troubleshooting

### Problèmes courants

```bash
# Erreur permissions (éviter sudo)
# Solution: utiliser nvm ou corriger permissions
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH

# Clear cache
npm cache clean --force

# Rebuild
npm rebuild

# Supprimer node_modules et reinstaller
rm -rf node_modules package-lock.json
npm install

# Vérifier intégrité
npm audit
npm audit fix

# Update npm
npm install -g npm@latest
```

### npm audit

```bash
# Vérifier vulnérabilités
npm audit

# Fix automatique
npm audit fix

# Fix force
npm audit fix --force

# Voir détails
npm audit --json
```

[← Bases de Node.js](./infos-nodejs-02-bases-nodejs.md) | [Index](./infos-nodejs-00-index.md) | [Modules →](./infos-nodejs-04-modules-commonjs-esm.md)

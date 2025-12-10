# 🚀 Introduction et Installation

[Index](./infos-nodejs-00-index.md) | [Bases de Node.js →](./infos-nodejs-02-bases-nodejs.md)

## Qu'est-ce que Node.js ?

Node.js est un runtime JavaScript construit sur le moteur V8 de Chrome qui permet d'exécuter du JavaScript côté serveur.

### Caractéristiques principales

```
✅ JavaScript côté serveur
✅ Asynchrone et non-bloquant (Event-driven)
✅ Single-threaded avec Event Loop
✅ NPM (Node Package Manager)
✅ Performance élevée
✅ Large écosystème de packages
✅ Cross-platform (Windows, macOS, Linux)
```

### Cas d'usage

```
📌 API REST / GraphQL
📌 Applications temps réel (WebSocket)
📌 Microservices
📌 Outils CLI
📌 Server-Side Rendering (SSR)
📌 Automatisation et scripts
📌 IoT
```

### Architecture

```
┌─────────────────────────────────┐
│     Application JavaScript      │
├─────────────────────────────────┤
│          Node.js APIs           │
├─────────────────────────────────┤
│     V8 JavaScript Engine        │
├─────────────────────────────────┤
│         libuv (Event Loop)      │
├─────────────────────────────────┤
│     Operating System (OS)       │
└─────────────────────────────────┘
```

## Installation

### Windows

#### Avec installeur officiel

```bash
# Télécharger depuis nodejs.org
# https://nodejs.org/

# Choisir version:
# - LTS (Long Term Support) - Recommandé pour production
# - Current - Dernières features

# Installer le fichier .msi téléchargé

# Vérifier installation
node --version
npm --version
```

#### Avec Chocolatey

```powershell
# Installer Chocolatey d'abord
# https://chocolatey.org/install

# Installer Node.js
choco install nodejs-lts

# Ou version courante
choco install nodejs

# Vérifier
node --version
```

#### Avec Scoop

```powershell
# Installer Scoop d'abord
# https://scoop.sh/

# Installer Node.js
scoop install nodejs-lts

# Vérifier
node --version
```

### macOS

#### Avec Homebrew

```bash
# Installer Homebrew d'abord
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Node.js
brew install node

# Version spécifique
brew install node@18

# Vérifier
node --version
npm --version
```

#### Avec installeur officiel

```bash
# Télécharger depuis nodejs.org
# https://nodejs.org/

# Installer le fichier .pkg téléchargé

# Vérifier
node --version
```

### Linux

#### Ubuntu / Debian

```bash
# Méthode 1: Repository officiel
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Ou version spécifique (18.x)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Vérifier
node --version
npm --version

# Méthode 2: Avec apt (version ancienne)
sudo apt update
sudo apt install nodejs npm
```

#### CentOS / RHEL / Fedora

```bash
# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs

# Fedora
sudo dnf install nodejs npm

# Vérifier
node --version
npm --version
```

#### Arch Linux

```bash
# Installer Node.js
sudo pacman -S nodejs npm

# Vérifier
node --version
```

## NVM (Node Version Manager)

NVM permet de gérer plusieurs versions de Node.js sur la même machine.

### Installation NVM

#### Unix / macOS

```bash
# Installer NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Ou avec wget
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Ajouter à .bashrc / .zshrc (si pas automatique)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Recharger shell
source ~/.bashrc
# ou
source ~/.zshrc

# Vérifier
nvm --version
```

#### Windows

```powershell
# Utiliser nvm-windows
# https://github.com/coreybutler/nvm-windows/releases

# Télécharger nvm-setup.exe
# Installer

# Vérifier
nvm version
```

### Utilisation NVM

```bash
# Lister versions disponibles
nvm ls-remote
nvm ls-remote --lts

# Installer version
nvm install 18
nvm install 20
nvm install node          # Dernière version
nvm install --lts         # Dernière LTS

# Lister versions installées
nvm ls

# Utiliser une version
nvm use 18
nvm use 20
nvm use --lts

# Version par défaut
nvm alias default 18
nvm alias default node

# Version courante
nvm current

# Désinstaller version
nvm uninstall 16

# Exécuter avec version spécifique
nvm exec 18 node app.js
nvm run 18 app.js
```

### Fichier .nvmrc

```bash
# Créer .nvmrc à la racine du projet
echo "18.17.0" > .nvmrc

# Ou
echo "lts/*" > .nvmrc

# Utiliser la version du .nvmrc
nvm use

# Installer la version du .nvmrc
nvm install
```

## Première utilisation

### Version Node.js

```bash
# Version
node --version
node -v

# Informations
node -p process.versions

# Aide
node --help
```

### Premier script

```javascript
// hello.js
console.log('Hello, Node.js!');
console.log('Version:', process.version);
console.log('Platform:', process.platform);
```

```bash
# Exécuter
node hello.js
```

### REPL (Read-Eval-Print Loop)

```bash
# Lancer REPL
node

# Dans REPL:
> console.log('Hello')
Hello
> 1 + 1
2
> const x = 10
undefined
> x * 2
20
> .help          # Aide
> .exit          # Quitter (ou Ctrl+D)
```

### Script avec arguments

```javascript
// args.js
console.log('Arguments:', process.argv);

// process.argv[0] = chemin node
// process.argv[1] = chemin script
// process.argv[2+] = arguments

const args = process.argv.slice(2);
console.log('User args:', args);
```

```bash
# Exécuter
node args.js hello world
# Output:
# Arguments: [ '/usr/bin/node', '/path/to/args.js', 'hello', 'world' ]
# User args: [ 'hello', 'world' ]
```

## NPM (Node Package Manager)

NPM est installé automatiquement avec Node.js.

### Vérifier NPM

```bash
# Version
npm --version
npm -v

# Mettre à jour NPM
npm install -g npm@latest

# Aide
npm help
npm help install
```

### Alternatives à NPM

#### Yarn

```bash
# Installer Yarn
npm install -g yarn

# Vérifier
yarn --version

# Utilisation
yarn add package-name
yarn install
yarn remove package-name
```

#### PNPM

```bash
# Installer pnpm
npm install -g pnpm

# Vérifier
pnpm --version

# Utilisation
pnpm add package-name
pnpm install
pnpm remove package-name
```

## Configuration Node.js

### Variables d'environnement

```bash
# NODE_ENV
export NODE_ENV=production
export NODE_ENV=development

# PORT
export PORT=3000

# Dans script
NODE_ENV=production node app.js
```

### Fichier .env

```bash
# Installer dotenv
npm install dotenv

# Créer .env
PORT=3000
DATABASE_URL=mongodb://localhost:27017/mydb
SECRET_KEY=mysecretkey
```

```javascript
// app.js
require('dotenv').config();

console.log('Port:', process.env.PORT);
console.log('Database:', process.env.DATABASE_URL);
```

## Outils de développement

### Nodemon

Redémarre automatiquement l'application lors de changements.

```bash
# Installer globalement
npm install -g nodemon

# Ou localement
npm install --save-dev nodemon

# Utilisation
nodemon app.js

# Avec options
nodemon --watch src app.js
nodemon --ext js,json app.js
```

### Configuration nodemon.json

```json
{
  "watch": ["src"],
  "ext": "js,json",
  "ignore": ["src/**/*.test.js"],
  "exec": "node src/index.js",
  "env": {
    "NODE_ENV": "development"
  }
}
```

### Package.json scripts

```json
{
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "prod": "NODE_ENV=production node src/index.js"
  }
}
```

```bash
# Exécuter
npm start
npm run dev
npm run prod
```

## Vérifier installation

### Script de vérification

```javascript
// check.js
console.log('✅ Node.js:', process.version);
console.log('✅ NPM:', process.env.npm_config_user_agent?.split(' ')[0]);
console.log('✅ Platform:', process.platform);
console.log('✅ Architecture:', process.arch);
console.log('✅ Directory:', process.cwd());
console.log('✅ Memory:', Math.round(process.memoryUsage().heapUsed / 1024 / 1024), 'MB');

// Test module
try {
  const fs = require('fs');
  console.log('✅ File System module OK');
} catch (e) {
  console.log('❌ Error:', e.message);
}
```

```bash
# Exécuter
node check.js
```

## Versions Node.js

### Historique

```
Node.js 18 (LTS) - Octobre 2022 - Avril 2025
Node.js 20 (LTS) - Avril 2023 - Avril 2026
Node.js 21 (Current) - Octobre 2023
Node.js 22 (Current) - Avril 2024

Recommandation: Utiliser la dernière version LTS
```

### Choisir une version

```bash
# Pour production
- Utiliser LTS (Long Term Support)
- Stable et maintenue
- Support de sécurité garanti

# Pour développement
- Utiliser Current
- Dernières features
- Tester les nouveautés

# Vérifier schedule
https://nodejs.org/en/about/releases/
```

## Ressources

```
Documentation officielle:
- https://nodejs.org/docs/
- https://nodejs.org/api/

Tutoriels:
- https://nodejs.dev/learn
- https://www.freecodecamp.org/news/tag/nodejs/

Communauté:
- https://github.com/nodejs/node
- r/node
- Node.js Discord

Package registry:
- https://www.npmjs.com/
```

## Prochaines étapes

```
1. Apprendre les bases Node.js (REPL, modules)
2. Créer un projet NPM
3. Installer des packages
4. Créer un serveur HTTP simple
5. Explorer les APIs natives
6. Apprendre Express.js
```

[Index](./infos-nodejs-00-index.md) | [Bases de Node.js →](./infos-nodejs-02-bases-nodejs.md)

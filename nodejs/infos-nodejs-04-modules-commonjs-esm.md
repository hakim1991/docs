# 🔧 Modules (CommonJS et ESM)

[← NPM et Packages](./infos-nodejs-03-npm-packages.md) | [Index](./infos-nodejs-00-index.md) | [APIs Natives →](./infos-nodejs-05-apis-natives.md)

## CommonJS (CJS)

### Exporter avec module.exports

```javascript
// math.js

// Export simple
module.exports = function add(a, b) {
  return a + b;
};
```

```javascript
// utils.js

// Export objet
module.exports = {
  add: function(a, b) {
    return a + b;
  },
  subtract: function(a, b) {
    return a - b;
  },
  multiply: (a, b) => a * b
};
```

```javascript
// user.js

// Export classe
class User {
  constructor(name) {
    this.name = name;
  }

  sayHello() {
    return `Hello, ${this.name}`;
  }
}

module.exports = User;
```

### Exporter avec exports

```javascript
// helpers.js

// Ajouter des exports
exports.formatDate = function(date) {
  return date.toISOString();
};

exports.capitalize = function(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

// ⚠️ Ne pas réassigner exports
// exports = { ... } // Ne fonctionne pas
// Utiliser module.exports = { ... } à la place
```

### Importer avec require

```javascript
// app.js

// Import simple
const add = require('./math');
console.log(add(2, 3)); // 5

// Import objet
const utils = require('./utils');
console.log(utils.add(2, 3)); // 5
console.log(utils.multiply(2, 3)); // 6

// Destructuring
const { add, subtract } = require('./utils');
console.log(add(5, 3)); // 8

// Import classe
const User = require('./user');
const user = new User('Alice');
console.log(user.sayHello()); // Hello, Alice
```

### Modules built-in

```javascript
// Modules natifs Node.js
const fs = require('fs');
const path = require('path');
const http = require('http');
const os = require('os');

// Utilisation
console.log('Platform:', os.platform());
console.log('Home:', os.homedir());
```

### Cache des modules

```javascript
// counter.js
let count = 0;

module.exports = {
  increment() {
    count++;
  },
  getCount() {
    return count;
  }
};
```

```javascript
// app.js
const counter1 = require('./counter');
const counter2 = require('./counter');

counter1.increment();
console.log(counter1.getCount()); // 1
console.log(counter2.getCount()); // 1 (même instance)

// Même référence
console.log(counter1 === counter2); // true

// Clear cache
delete require.cache[require.resolve('./counter')];
```

## ES Modules (ESM)

### Configuration ESM

```json
// package.json
{
  "type": "module"
}
```

Ou utiliser extension `.mjs`:

```javascript
// math.mjs
export function add(a, b) {
  return a + b;
}
```

### Export named

```javascript
// math.js

// Export inline
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export const PI = 3.14159;

// Export à la fin
function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  return a / b;
}

export { multiply, divide };

// Rename export
function square(x) {
  return x * x;
}

export { square as sqr };
```

### Export default

```javascript
// user.js

// Export default classe
export default class User {
  constructor(name) {
    this.name = name;
  }

  sayHello() {
    return `Hello, ${this.name}`;
  }
}

// Ou
class User {
  // ...
}

export default User;

// Export default fonction
export default function greet(name) {
  return `Hello, ${name}`;
}

// Export default objet
export default {
  name: 'App',
  version: '1.0.0'
};
```

### Import named

```javascript
// app.js

// Import named
import { add, subtract } from './math.js';
console.log(add(2, 3)); // 5

// Import avec rename
import { add as sum } from './math.js';
console.log(sum(2, 3)); // 5

// Import all
import * as math from './math.js';
console.log(math.add(2, 3)); // 5
console.log(math.PI); // 3.14159

// Import multiple
import { add, subtract, multiply, divide } from './math.js';
```

### Import default

```javascript
// app.js

// Import default (nom libre)
import User from './user.js';
const user = new User('Alice');

import greet from './utils.js';
console.log(greet('Bob'));

import config from './config.js';
console.log(config.name);
```

### Import mixte

```javascript
// utils.js
export function helper() {
  return 'helper';
}

export default class Main {
  // ...
}
```

```javascript
// app.js
import Main, { helper } from './utils.js';

const main = new Main();
console.log(helper());
```

### Dynamic import

```javascript
// app.js

// Import dynamique (async)
async function loadModule() {
  const { add } = await import('./math.js');
  console.log(add(2, 3));
}

loadModule();

// Avec then
import('./math.js')
  .then(({ add }) => {
    console.log(add(2, 3));
  })
  .catch(err => {
    console.error('Error loading module:', err);
  });

// Conditionnel
if (condition) {
  const module = await import('./feature.js');
  module.init();
}
```

### Import modules built-in

```javascript
// ESM
import fs from 'fs';
import path from 'path';
import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// __dirname en ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('Directory:', __dirname);
```

## CommonJS vs ESM

### Différences principales

```javascript
// CommonJS
const module = require('./module');
module.exports = { ... };

// ESM
import module from './module.js';
export default { ... };
```

### Comparaison

```
┌────────────────────────────────────────────────────┐
│ Feature        │ CommonJS       │ ES Modules       │
├────────────────────────────────────────────────────┤
│ Syntaxe        │ require()      │ import/export    │
│ Extension      │ .js            │ .js / .mjs       │
│ Chargement     │ Synchrone      │ Asynchrone       │
│ Top-level      │ Non            │ Oui (await)      │
│ this           │ module.exports │ undefined        │
│ __dirname      │ Oui            │ Non (emulation)  │
│ __filename     │ Oui            │ Non (emulation)  │
│ Dynamic import │ require()      │ import()         │
│ Condition      │ Oui            │ import()         │
│ Tree shaking   │ Non            │ Oui              │
│ Browser        │ Non (bundler)  │ Oui (natif)      │
└────────────────────────────────────────────────────┘
```

### Interopérabilité

```javascript
// Utiliser CommonJS dans ESM
import cjsModule from './commonjs-module.cjs';

// Utiliser ESM dans CommonJS (dynamic import)
async function loadESM() {
  const { namedExport } = await import('./esm-module.js');
  return namedExport;
}
```

## Créer ses modules

### Structure basique

```
my-module/
├── package.json
├── index.js
├── lib/
│   ├── utils.js
│   └── helpers.js
└── README.md
```

### Module simple (CommonJS)

```javascript
// lib/utils.js
function formatName(name) {
  return name.trim().toLowerCase();
}

function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

module.exports = {
  formatName,
  validateEmail
};
```

```javascript
// index.js
const utils = require('./lib/utils');

module.exports = {
  ...utils,
  version: '1.0.0'
};
```

### Module simple (ESM)

```javascript
// lib/utils.js
export function formatName(name) {
  return name.trim().toLowerCase();
}

export function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}
```

```javascript
// index.js
export * from './lib/utils.js';
export const version = '1.0.0';
```

### Module avec classe

```javascript
// logger.js
class Logger {
  constructor(prefix = '') {
    this.prefix = prefix;
  }

  log(message) {
    console.log(`${this.prefix}${message}`);
  }

  error(message) {
    console.error(`${this.prefix}ERROR: ${message}`);
  }

  warn(message) {
    console.warn(`${this.prefix}WARN: ${message}`);
  }
}

module.exports = Logger;

// Utilisation
// const Logger = require('./logger');
// const logger = new Logger('[APP] ');
// logger.log('Hello');
```

### Module avec config

```javascript
// database.js
class Database {
  constructor(config) {
    this.config = {
      host: 'localhost',
      port: 5432,
      ...config
    };
  }

  connect() {
    console.log(`Connecting to ${this.config.host}:${this.config.port}`);
  }
}

module.exports = Database;

// Utilisation
// const Database = require('./database');
// const db = new Database({ host: 'prod.example.com' });
// db.connect();
```

## Patterns de modules

### Singleton

```javascript
// config.js (CommonJS)
class Config {
  constructor() {
    if (Config.instance) {
      return Config.instance;
    }

    this.data = {};
    Config.instance = this;
  }

  set(key, value) {
    this.data[key] = value;
  }

  get(key) {
    return this.data[key];
  }
}

module.exports = new Config();

// Utilisation
// const config = require('./config');
// config.set('apiKey', '12345');
```

### Factory

```javascript
// user-factory.js
class User {
  constructor(name, role) {
    this.name = name;
    this.role = role;
  }
}

function createUser(type, name) {
  switch (type) {
    case 'admin':
      return new User(name, 'admin');
    case 'user':
      return new User(name, 'user');
    default:
      throw new Error('Invalid user type');
  }
}

module.exports = { createUser };
```

### Module revealing pattern

```javascript
// calculator.js
const Calculator = (function() {
  // Private
  let result = 0;

  function log(operation) {
    console.log(`${operation}: ${result}`);
  }

  // Public
  return {
    add(n) {
      result += n;
      log('add');
      return this;
    },
    subtract(n) {
      result -= n;
      log('subtract');
      return this;
    },
    getResult() {
      return result;
    },
    reset() {
      result = 0;
      return this;
    }
  };
})();

module.exports = Calculator;

// Utilisation
// const calc = require('./calculator');
// calc.add(5).subtract(2).getResult(); // 3
```

## Package.json exports

### Exports field

```json
{
  "name": "my-package",
  "type": "module",
  "exports": {
    ".": "./index.js",
    "./utils": "./lib/utils.js",
    "./helpers": "./lib/helpers.js"
  }
}
```

```javascript
// Utilisation
import pkg from 'my-package';
import { utils } from 'my-package/utils';
import { helpers } from 'my-package/helpers';
```

### Conditional exports

```json
{
  "exports": {
    ".": {
      "import": "./index.mjs",
      "require": "./index.cjs",
      "default": "./index.js"
    },
    "./utils": {
      "node": "./lib/utils-node.js",
      "browser": "./lib/utils-browser.js",
      "default": "./lib/utils.js"
    }
  }
}
```

### Dual package (CJS + ESM)

```json
{
  "name": "my-package",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

## Top-level await (ESM)

```javascript
// config.js (ESM)
const response = await fetch('https://api.example.com/config');
const config = await response.json();

export default config;
```

```javascript
// app.js
import config from './config.js';
console.log('Config loaded:', config);

// Ou dans fonction async
async function main() {
  const data = await loadData();
  console.log(data);
}

// Top-level await
await main();
```

## Import maps (ESM)

```html
<!-- index.html -->
<script type="importmap">
{
  "imports": {
    "lodash": "https://cdn.jsdelivr.net/npm/lodash@4.17.21/+esm",
    "react": "https://esm.sh/react@18"
  }
}
</script>

<script type="module">
import _ from 'lodash';
import React from 'react';
</script>
```

## Best practices

### Choisir entre CJS et ESM

```
Utiliser CommonJS si:
- Legacy code / compatibilité
- Node.js < 12
- Synchronous loading requis

Utiliser ES Modules si:
- Nouveau projet
- Node.js >= 14
- Partage avec frontend
- Tree shaking important
- Top-level await nécessaire
```

### Organisation

```
src/
├── index.js          # Point d'entrée
├── config/
│   └── database.js
├── models/
│   ├── user.js
│   └── product.js
├── controllers/
│   ├── userController.js
│   └── productController.js
├── services/
│   └── emailService.js
└── utils/
    ├── logger.js
    └── validator.js
```

### Conventions

```javascript
// 1 module = 1 fichier
// Nom de fichier = nom de classe/fonction

// ✅ Bon
// user.js
export default class User { }

// ❌ Éviter
// utils.js
export class User { }
export class Product { }

// Exports clairs
// ✅ Bon
export { User, Product };

// ❌ Éviter
export default { User, Product };
```

[← NPM et Packages](./infos-nodejs-03-npm-packages.md) | [Index](./infos-nodejs-00-index.md) | [APIs Natives →](./infos-nodejs-05-apis-natives.md)

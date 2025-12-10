# 📘 Bases de Node.js

[← Introduction et Installation](./infos-nodejs-01-introduction-installation.md) | [Index](./infos-nodejs-00-index.md) | [NPM et Packages →](./infos-nodejs-03-npm-packages.md)

## Premier script Node.js

### Hello World

```javascript
// hello.js
console.log('Hello, World!');
```

```bash
node hello.js
```

### Console

```javascript
// console.js

// Log basique
console.log('Information');

// Avec variables
const name = 'Node.js';
const version = process.version;
console.log('Running', name, version);

// Template literals
console.log(`Running ${name} ${version}`);

// Error
console.error('Une erreur est survenue');

// Warning
console.warn('Attention!');

// Info
console.info('Information importante');

// Table
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' }
];
console.table(users);

// Time
console.time('opération');
// ... code ...
console.timeEnd('opération');

// Trace
console.trace('Debug trace');

// Clear
console.clear();
```

## Process

### Informations système

```javascript
// process-info.js

// Version Node.js
console.log('Node version:', process.version);
console.log('Versions:', process.versions);

// Platform
console.log('Platform:', process.platform);
console.log('Architecture:', process.arch);

// Mémoire
console.log('Memory usage:', process.memoryUsage());

// Uptime
console.log('Uptime:', process.uptime(), 'seconds');

// PID
console.log('Process ID:', process.pid);

// Directory
console.log('Current directory:', process.cwd());

// Arguments
console.log('Arguments:', process.argv);

// Environment variables
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('PATH:', process.env.PATH);
```

### Arguments ligne de commande

```javascript
// args.js

// Tous les arguments
console.log('All args:', process.argv);

// Arguments utilisateur (sans node et script)
const args = process.argv.slice(2);
console.log('User args:', args);

// Parser arguments
const name = args[0] || 'World';
const greeting = args[1] || 'Hello';
console.log(`${greeting}, ${name}!`);
```

```bash
node args.js Alice Bonjour
# Output: Bonjour, Alice!
```

### Variables d'environnement

```javascript
// env.js

// Lire variable
const port = process.env.PORT || 3000;
const env = process.env.NODE_ENV || 'development';

console.log('Port:', port);
console.log('Environment:', env);

// Toutes les variables
console.log('All env vars:', process.env);
```

```bash
# Définir variables
PORT=8080 NODE_ENV=production node env.js

# Ou
export PORT=8080
export NODE_ENV=production
node env.js
```

### Exit codes

```javascript
// exit.js

// Exit avec succès
process.exit(0);

// Exit avec erreur
process.exit(1);

// Exit handler
process.on('exit', (code) => {
  console.log(`Exiting with code: ${code}`);
});

// Avant exit
process.on('beforeExit', (code) => {
  console.log('Before exit:', code);
});

// SIGINT (Ctrl+C)
process.on('SIGINT', () => {
  console.log('Received SIGINT');
  process.exit(0);
});

// SIGTERM
process.on('SIGTERM', () => {
  console.log('Received SIGTERM');
  process.exit(0);
});
```

## Global objects

### Globals disponibles

```javascript
// globals.js

// Console
console.log('Console is global');

// setTimeout / setInterval
setTimeout(() => {
  console.log('After 1 second');
}, 1000);

const interval = setInterval(() => {
  console.log('Every 2 seconds');
}, 2000);

// Clear
setTimeout(() => {
  clearInterval(interval);
}, 10000);

// __dirname (CommonJS uniquement)
console.log('Directory:', __dirname);

// __filename (CommonJS uniquement)
console.log('Filename:', __filename);

// Buffer
const buf = Buffer.from('Hello');
console.log('Buffer:', buf);

// global (équivalent de window dans browser)
global.myVar = 'test';
console.log(global.myVar);
```

### Timers

```javascript
// timers.js

// setTimeout
const timeout = setTimeout(() => {
  console.log('Executed after delay');
}, 2000);

// Annuler timeout
clearTimeout(timeout);

// setInterval
let count = 0;
const interval = setInterval(() => {
  count++;
  console.log('Count:', count);

  if (count >= 5) {
    clearInterval(interval);
  }
}, 1000);

// setImmediate
setImmediate(() => {
  console.log('Immediate callback');
});

// process.nextTick
process.nextTick(() => {
  console.log('Next tick callback');
});

console.log('End of script');

// Ordre d'exécution:
// 1. End of script
// 2. Next tick callback
// 3. Immediate callback
// 4. Count: 1, 2, 3, 4, 5
```

## Event Loop

### Comprendre l'Event Loop

```javascript
// event-loop.js

console.log('1. Synchronous');

setTimeout(() => {
  console.log('2. setTimeout 0ms');
}, 0);

setImmediate(() => {
  console.log('3. setImmediate');
});

process.nextTick(() => {
  console.log('4. nextTick');
});

Promise.resolve().then(() => {
  console.log('5. Promise');
});

console.log('6. Synchronous');

// Ordre d'exécution:
// 1. Synchronous
// 6. Synchronous
// 4. nextTick
// 5. Promise
// 2. setTimeout 0ms
// 3. setImmediate
```

### Phases de l'Event Loop

```javascript
// event-loop-phases.js

/*
Event Loop phases:
1. Timers (setTimeout, setInterval)
2. Pending callbacks (I/O callbacks)
3. Idle, prepare (internal)
4. Poll (retrieve I/O events)
5. Check (setImmediate)
6. Close callbacks (socket close, etc.)

Entre chaque phase: process.nextTick et microtasks (Promises)
*/

// Exemple
const fs = require('fs');

console.log('Start');

// Microtask (Promise)
Promise.resolve().then(() => console.log('Promise 1'));

// nextTick
process.nextTick(() => console.log('nextTick 1'));

// Timer
setTimeout(() => console.log('setTimeout'), 0);

// Immediate
setImmediate(() => console.log('setImmediate'));

// I/O
fs.readFile(__filename, () => {
  console.log('I/O callback');

  setTimeout(() => console.log('setTimeout in I/O'), 0);
  setImmediate(() => console.log('setImmediate in I/O'));

  process.nextTick(() => console.log('nextTick in I/O'));
});

console.log('End');
```

## Asynchrone

### Callbacks

```javascript
// callbacks.js

// Callback pattern
function fetchData(callback) {
  setTimeout(() => {
    const data = { name: 'Alice', age: 30 };
    callback(null, data);
  }, 1000);
}

fetchData((error, data) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Data:', data);
});

// Callback Hell (à éviter)
fetchData((err, data1) => {
  if (err) return console.error(err);

  fetchData((err, data2) => {
    if (err) return console.error(err);

    fetchData((err, data3) => {
      if (err) return console.error(err);
      console.log('All data:', data1, data2, data3);
    });
  });
});
```

### Promises

```javascript
// promises.js

// Créer une Promise
function fetchData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const data = { name: 'Alice', age: 30 };
      resolve(data);
      // ou reject(new Error('Failed'));
    }, 1000);
  });
}

// Utiliser Promise
fetchData()
  .then(data => {
    console.log('Data:', data);
    return data.age;
  })
  .then(age => {
    console.log('Age:', age);
  })
  .catch(error => {
    console.error('Error:', error);
  })
  .finally(() => {
    console.log('Done');
  });

// Promise.all
const promise1 = Promise.resolve(1);
const promise2 = Promise.resolve(2);
const promise3 = Promise.resolve(3);

Promise.all([promise1, promise2, promise3])
  .then(results => {
    console.log('All results:', results); // [1, 2, 3]
  });

// Promise.race
Promise.race([promise1, promise2, promise3])
  .then(result => {
    console.log('First result:', result); // 1
  });

// Promise.allSettled
Promise.allSettled([
  Promise.resolve(1),
  Promise.reject('error'),
  Promise.resolve(3)
])
  .then(results => {
    console.log('All settled:', results);
  });
```

### Async/Await

```javascript
// async-await.js

// Fonction async
async function fetchData() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ name: 'Alice', age: 30 });
    }, 1000);
  });
}

// Utiliser async/await
async function main() {
  try {
    console.log('Fetching data...');
    const data = await fetchData();
    console.log('Data:', data);

    const age = data.age;
    console.log('Age:', age);
  } catch (error) {
    console.error('Error:', error);
  }
}

main();

// Async/await multiple
async function fetchMultiple() {
  try {
    // Séquentiel
    const data1 = await fetchData();
    const data2 = await fetchData();
    console.log('Sequential:', data1, data2);

    // Parallèle
    const [data3, data4] = await Promise.all([
      fetchData(),
      fetchData()
    ]);
    console.log('Parallel:', data3, data4);
  } catch (error) {
    console.error('Error:', error);
  }
}

fetchMultiple();
```

## Erreurs

### Try/Catch

```javascript
// errors.js

// Try/catch synchrone
try {
  const result = riskyOperation();
  console.log('Result:', result);
} catch (error) {
  console.error('Error:', error.message);
} finally {
  console.log('Cleanup');
}

// Try/catch async
async function asyncOperation() {
  try {
    const data = await fetchData();
    console.log('Data:', data);
  } catch (error) {
    console.error('Async error:', error.message);
  }
}

// Créer erreurs custom
class CustomError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'CustomError';
    this.code = code;
  }
}

function validateAge(age) {
  if (age < 0) {
    throw new CustomError('Age cannot be negative', 'INVALID_AGE');
  }
  return true;
}

try {
  validateAge(-5);
} catch (error) {
  console.error('Error:', error.message);
  console.error('Code:', error.code);
}
```

### Error handling global

```javascript
// error-handling.js

// Uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Log error
  // Cleanup
  process.exit(1);
});

// Unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  console.error('Promise:', promise);
  // Log error
  // Cleanup
  process.exit(1);
});

// Warning
process.on('warning', (warning) => {
  console.warn('Warning:', warning.name);
  console.warn('Message:', warning.message);
  console.warn('Stack:', warning.stack);
});

// Exemple erreur
throw new Error('Test uncaught exception');
```

## Debugging

### Console debugging

```javascript
// debug.js

const user = {
  name: 'Alice',
  age: 30,
  address: {
    city: 'Paris',
    country: 'France'
  }
};

// Inspect objet
console.log('User:', user);

// Dir (plus détaillé)
console.dir(user, { depth: null, colors: true });

// Assert
console.assert(user.age > 18, 'User must be adult');

// Trace
console.trace('Debug trace');

// Count
for (let i = 0; i < 5; i++) {
  console.count('loop');
}
console.countReset('loop');

// Group
console.group('User info');
console.log('Name:', user.name);
console.log('Age:', user.age);
console.groupEnd();
```

### Node.js debugger

```javascript
// app.js

function calculate(a, b) {
  debugger; // Point d'arrêt
  const result = a + b;
  return result;
}

const sum = calculate(5, 3);
console.log('Sum:', sum);
```

```bash
# Lancer avec debugger
node inspect app.js

# Chrome DevTools
node --inspect app.js
# Puis ouvrir chrome://inspect

# VS Code
# Ajouter breakpoint dans l'éditeur
# F5 pour debug
```

## REPL avancé

```bash
# Lancer REPL
node

# Commandes spéciales
.help           # Aide
.break          # Sortir du mode multi-ligne
.clear          # Reset context
.editor         # Mode éditeur
.exit           # Quitter
.load file.js   # Charger fichier
.save file.js   # Sauvegarder session

# Variables spéciales
_               # Dernière valeur
```

```javascript
// Dans REPL
> 1 + 1
2
> _
2
> const double = x => x * 2
undefined
> double(5)
10
> _
10
```

## Performance

### Mesurer performance

```javascript
// performance.js

// console.time
console.time('operation');
for (let i = 0; i < 1000000; i++) {
  // operation
}
console.timeEnd('operation');

// performance hooks
const { performance } = require('perf_hooks');

const start = performance.now();
// operation
const end = performance.now();
console.log(`Duration: ${end - start}ms`);

// Memory usage
const used = process.memoryUsage();
console.log('Memory:', {
  rss: Math.round(used.rss / 1024 / 1024) + 'MB',
  heapTotal: Math.round(used.heapTotal / 1024 / 1024) + 'MB',
  heapUsed: Math.round(used.heapUsed / 1024 / 1024) + 'MB',
  external: Math.round(used.external / 1024 / 1024) + 'MB'
});
```

[← Introduction et Installation](./infos-nodejs-01-introduction-installation.md) | [Index](./infos-nodejs-00-index.md) | [NPM et Packages →](./infos-nodejs-03-npm-packages.md)

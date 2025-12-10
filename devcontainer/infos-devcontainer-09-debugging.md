# 🐛 Debugging

[← Templates](./infos-devcontainer-08-templates-exemples.md) | [Index](./infos-devcontainer-00-index.md) | [Avancé →](./infos-devcontainer-10-sujets-avances.md)

## Configuration VS Code Debugger

### Node.js

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/src/index.js",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"]
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229,
      "restart": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

### TypeScript

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug TypeScript",
      "preLaunchTask": "npm: build",
      "program": "${workspaceFolder}/src/index.ts",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "sourceMaps": true,
      "smartStep": true,
      "internalConsoleOptions": "openOnSessionStart"
    }
  ]
}
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "sourceMap": true,
    "outDir": "./dist"
  }
}
```

### Python

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "Python: Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_DEBUG": "1"
      },
      "args": ["run", "--no-debugger", "--no-reload"],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Python: Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver"],
      "django": true,
      "justMyCode": false
    }
  ]
}
```

### Go

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Go",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}/main.go"
    }
  ]
}
```

### Rust

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug Rust",
      "cargo": {
        "args": ["build", "--bin=myapp", "--package=myapp"]
      },
      "args": [],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

## Debugging Node.js avec nodemon

### package.json

```json
{
  "scripts": {
    "dev": "nodemon --inspect=0.0.0.0:9229 src/index.js"
  }
}
```

### launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Nodemon",
      "processId": "${command:PickProcess}",
      "restart": true,
      "protocol": "inspector"
    }
  ]
}
```

## Debugging dans Docker Compose

### Node.js

```yaml
# docker-compose.yml
services:
  app:
    build: .
    command: npm run dev
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    environment:
      NODE_OPTIONS: "--inspect=0.0.0.0:9229"
```

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Docker",
      "address": "localhost",
      "port": 9229,
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/workspace",
      "restart": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

### Python

```yaml
# docker-compose.yml
services:
  app:
    build: .
    command: python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py
    ports:
      - "8000:8000"
      - "5678:5678"  # Debug port
```

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Remote Attach",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "/workspace"
        }
      ],
      "justMyCode": false
    }
  ]
}
```

## Breakpoints

### Breakpoints classiques

Cliquer dans la marge gauche de l'éditeur.

### Conditional breakpoints

Clic droit sur le breakpoint → "Edit Breakpoint" → Condition

```javascript
// S'arrêter si count > 10
count > 10

// S'arrêter si user.name contient "Alice"
user.name.includes('Alice')
```

### Logpoints

Clic droit sur le breakpoint → "Edit Breakpoint" → Log Message

```javascript
// Logger sans s'arrêter
User {user.name} logged in at {new Date()}
```

## Debug Console

### Node.js

```javascript
// Dans Debug Console
> user.name
'Alice'

> user.email
'alice@example.com'

> JSON.stringify(user, null, 2)
```

### Python

```python
# Dans Debug Console
>>> user.name
'Alice'

>>> dir(user)
['__class__', '__delattr__', ...]

>>> vars(user)
{'name': 'Alice', 'email': 'alice@example.com'}
```

## Watch expressions

Ajouter dans "Watch" :
```
user.name
user.email
users.length
process.env.NODE_ENV
```

## Call Stack

Voir la pile d'appels dans le panneau "Call Stack".

## Variables

Voir toutes les variables dans le scope actuel dans "Variables".

## Logs

### Container logs

```bash
# Voir les logs
F1 → "Dev Containers: Show Container Log"
```

```bash
# Via CLI
docker logs <container-id>
docker logs -f <container-id>  # Follow
docker-compose logs -f
```

### Application logs

```javascript
// Node.js
console.log('Debug:', data);
console.error('Error:', error);

// Utiliser un logger
const winston = require('winston');
const logger = winston.createLogger({
  transports: [new winston.transports.Console()],
});

logger.info('User logged in', { userId: user.id });
logger.error('Error occurred', { error: error.message });
```

```python
# Python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.error('Error message', exc_info=True)
```

## Troubleshooting

### Debugger ne se connecte pas

1. Vérifier que le port est forwardé

```json
{
  "forwardPorts": [9229]
}
```

2. Vérifier que l'application écoute sur 0.0.0.0

```bash
node --inspect=0.0.0.0:9229 app.js
```

3. Vérifier les path mappings

```json
{
  "localRoot": "${workspaceFolder}",
  "remoteRoot": "/workspace"
}
```

### Breakpoints ne s'arrêtent pas

1. Vérifier que les source maps sont activés

```json
// tsconfig.json
{
  "compilerOptions": {
    "sourceMap": true
  }
}
```

2. Vérifier `justMyCode`

```json
{
  "justMyCode": false
}
```

3. Rebuild le container

```bash
F1 → "Dev Containers: Rebuild Container"
```

### Performance

Désactiver `smartStep` si lent :

```json
{
  "smartStep": false
}
```

## Debugging tests

### Jest

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Jest All Tests",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Jest Current File",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["${fileBasenameNoExtension}", "--runInBand"],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    }
  ]
}
```

### pytest

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

## Remote debugging

### SSH Tunnel

```bash
# Sur la machine distante
node --inspect=0.0.0.0:9229 app.js

# En local, créer tunnel SSH
ssh -L 9229:localhost:9229 user@remote-host

# Attacher debugger à localhost:9229
```

### Kubernetes

```bash
# Port forward
kubectl port-forward pod/my-pod 9229:9229

# Attacher debugger à localhost:9229
```

## Profiling

### Node.js

```bash
# CPU profiling
node --prof app.js

# Analyser
node --prof-process isolate-0xnnnnnnnnnnnn-v8.log > processed.txt

# Memory profiling
node --inspect --expose-gc app.js
```

### Python

```python
# cProfile
python -m cProfile -o output.prof app.py

# Visualiser avec snakeviz
pip install snakeviz
snakeviz output.prof

# memory_profiler
pip install memory_profiler
python -m memory_profiler app.py
```

## VS Code Tasks

Automatiser build et debug.

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "npm: build",
      "type": "npm",
      "script": "build",
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "docker: build",
      "type": "shell",
      "command": "docker-compose build"
    }
  ]
}
```

```json
// .vscode/launch.json
{
  "configurations": [
    {
      "preLaunchTask": "npm: build",
      "name": "Debug after build"
    }
  ]
}
```

## Extensions utiles

- **Error Lens** : affiche les erreurs inline
- **Console Ninja** : meilleur console.log
- **Debug Visualizer** : visualise les structures de données
- **Turbo Console Log** : génère des console.log

## Bonnes pratiques

1. **Utiliser des breakpoints conditionnels** : éviter les arrêts inutiles
2. **Utiliser des logpoints** : logger sans arrêter
3. **Path mappings corrects** : crucial pour containers
4. **Source maps activés** : pour TypeScript/transpiled code
5. **Documenter la config de debug** : dans README.md

[← Templates](./infos-devcontainer-08-templates-exemples.md) | [Index](./infos-devcontainer-00-index.md) | [Avancé →](./infos-devcontainer-10-sujets-avances.md)

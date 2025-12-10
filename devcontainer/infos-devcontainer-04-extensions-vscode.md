# 🔌 Extensions VS Code

[← Features](./infos-devcontainer-03-features.md) | [Index](./infos-devcontainer-00-index.md) | [Ports →](./infos-devcontainer-05-ports-networking.md)

## Configuration des extensions

Les extensions sont définies dans `customizations.vscode.extensions`.

```json
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
```

## Extensions vs Local

- **Extensions dans devcontainer.json** : installées dans le container
- **Extensions locales** : restent sur la machine hôte

Certaines extensions fonctionnent uniquement localement (thèmes, keymaps).

## Extensions recommandées par langage

### JavaScript / TypeScript / Node.js

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "christian-kohler.npm-intellisense",
        "eg2.vscode-npm-script",
        "ms-vscode.vscode-typescript-next"
      ]
    }
  }
}
```

### React / Next.js

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss",
        "dsznajder.es7-react-js-snippets",
        "formulahendry.auto-rename-tag",
        "christiankohler.path-intellisense"
      ]
    }
  }
}
```

### Python

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "ms-toolsai.jupyter"
      ]
    }
  }
}
```

### Go

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "golang.go",
        "golang.go-nightly"
      ]
    }
  }
}
```

### Rust

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "rust-lang.rust-analyzer",
        "vadimcn.vscode-lldb",
        "serayuzgur.crates"
      ]
    }
  }
}
```

### Java

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "vscjava.vscode-java-pack",
        "vscjava.vscode-java-debug",
        "vscjava.vscode-maven",
        "vscjava.vscode-spring-initializr"
      ]
    }
  }
}
```

### PHP

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "bmewburn.vscode-intelephense-client",
        "xdebug.php-debug",
        "wongjn.php-sniffer"
      ]
    }
  }
}
```

### C# / .NET

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-dotnettools.csharp",
        "ms-dotnettools.csdevkit"
      ]
    }
  }
}
```

## Extensions générales

### Git

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "eamodio.gitlens",
        "mhutchie.git-graph",
        "donjayamanne.githistory"
      ]
    }
  }
}
```

### Docker

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker",
        "ms-vscode-remote.remote-containers"
      ]
    }
  }
}
```

### Base de données

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "cweijan.vscode-postgresql-client2",
        "mongodb.mongodb-vscode",
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg"
      ]
    }
  }
}
```

### Markdown

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "yzhang.markdown-all-in-one",
        "davidanson.vscode-markdownlint"
      ]
    }
  }
}
```

### YAML / JSON

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "redhat.vscode-yaml",
        "tamasfe.even-better-toml"
      ]
    }
  }
}
```

### Testing

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "orta.vscode-jest",
        "hbenl.vscode-test-explorer",
        "kavod-io.vscode-pytest-test-adapter"
      ]
    }
  }
}
```

## Settings VS Code

Configurer VS Code dans le container.

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2,
        "editor.insertSpaces": true,
        "files.autoSave": "onFocusChange",
        "files.trimTrailingWhitespace": true,
        "terminal.integrated.defaultProfile.linux": "zsh"
      }
    }
  }
}
```

### ESLint

```json
{
  "customizations": {
    "vscode": {
      "extensions": ["dbaeumer.vscode-eslint"],
      "settings": {
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": true
        },
        "eslint.validate": [
          "javascript",
          "javascriptreact",
          "typescript",
          "typescriptreact"
        ]
      }
    }
  }
}
```

### Prettier

```json
{
  "customizations": {
    "vscode": {
      "extensions": ["esbenp.prettier-vscode"],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "prettier.singleQuote": true,
        "prettier.trailingComma": "es5"
      }
    }
  }
}
```

### Python

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": false,
        "python.linting.ruffEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.codeActionsOnSave": {
            "source.organizeImports": true
          }
        }
      }
    }
  }
}
```

## Configuration complète

### Full Stack (Node + React + PostgreSQL)

```json
{
  "name": "Full Stack App",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",

  "customizations": {
    "vscode": {
      "extensions": [
        // JavaScript/TypeScript
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "christian-kohler.npm-intellisense",

        // React
        "dsznajder.es7-react-js-snippets",
        "bradlc.vscode-tailwindcss",

        // Git
        "eamodio.gitlens",
        "mhutchie.git-graph",

        // Docker
        "ms-azuretools.vscode-docker",

        // Database
        "cweijan.vscode-postgresql-client2",

        // Testing
        "orta.vscode-jest",

        // Utils
        "formulahendry.auto-rename-tag",
        "christian-kohler.path-intellisense",
        "wayou.vscode-todo-highlight"
      ],

      "settings": {
        // Editor
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2,
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": true
        },

        // Files
        "files.autoSave": "onFocusChange",
        "files.trimTrailingWhitespace": true,
        "files.exclude": {
          "**/.git": true,
          "**/node_modules": true,
          "**/.next": true,
          "**/dist": true
        },

        // Terminal
        "terminal.integrated.defaultProfile.linux": "bash",

        // ESLint
        "eslint.validate": [
          "javascript",
          "javascriptreact",
          "typescript",
          "typescriptreact"
        ],

        // Prettier
        "prettier.singleQuote": true,
        "prettier.trailingComma": "es5"
      }
    }
  }
}
```

### Python Data Science

```json
{
  "name": "Python Data Science",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "customizations": {
    "vscode": {
      "extensions": [
        // Python
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.debugpy",
        "charliermarsh.ruff",
        "ms-python.black-formatter",

        // Jupyter
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-keymap",
        "ms-toolsai.jupyter-renderers",

        // Git
        "eamodio.gitlens",

        // Utils
        "visualstudioexptteam.vscodeintellicode"
      ],

      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.ruffEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.codeActionsOnSave": {
            "source.organizeImports": true
          }
        },
        "jupyter.askForKernelRestart": false
      }
    }
  }
}
```

## Extensions UI vs Backend

Certaines extensions s'exécutent côté UI (local), d'autres côté backend (container).

### Extensions UI (Local)

- Thèmes
- Keybindings
- Icons
- UI tweaks

### Extensions Backend (Container)

- Linters
- Formatters
- Debuggers
- Language servers

VS Code gère automatiquement où exécuter chaque extension.

## Vérifier les extensions installées

Dans le container :

```bash
# Lister les extensions
code --list-extensions

# Avec versions
code --list-extensions --show-versions
```

## Extensions recommandées

Suggérer des extensions aux utilisateurs (`.vscode/extensions.json`) :

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "eamodio.gitlens"
  ]
}
```

Différence :
- **devcontainer.json** : installées automatiquement dans le container
- **extensions.json** : suggérées à l'utilisateur

## Désactiver des extensions

```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint"
      ],
      "settings": {
        "remote.extensionKind": {
          "ms-vsliveshare.vsliveshare": ["ui"]
        }
      }
    }
  }
}
```

## Extensions populaires

### Top 10

1. **ESLint** - `dbaeumer.vscode-eslint`
2. **Prettier** - `esbenp.prettier-vscode`
3. **GitLens** - `eamodio.gitlens`
4. **Docker** - `ms-azuretools.vscode-docker`
5. **Python** - `ms-python.python`
6. **Pylance** - `ms-python.vscode-pylance`
7. **Go** - `golang.go`
8. **Tailwind CSS** - `bradlc.vscode-tailwindcss`
9. **Auto Rename Tag** - `formulahendry.auto-rename-tag`
10. **Path Intellisense** - `christian-kohler.path-intellisense`

## Bonnes pratiques

1. **Installer uniquement les extensions nécessaires** : plus rapide
2. **Utiliser des versions spécifiques si critique** : stabilité
3. **Documenter les extensions** : dans README.md
4. **Tester avant de commiter** : vérifier compatibilité
5. **Séparer extensions UI et backend** : clarté

[← Features](./infos-devcontainer-03-features.md) | [Index](./infos-devcontainer-00-index.md) | [Ports →](./infos-devcontainer-05-ports-networking.md)

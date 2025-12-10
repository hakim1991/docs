# 🚀 Introduction et Installation

[Index](./infos-reactjs-00-index.md) | [JSX et Components →](./infos-reactjs-02-jsx-components.md)

## Qu'est-ce que React ?

React est une bibliothèque JavaScript pour construire des interfaces utilisateur, développée et maintenue par Meta (Facebook).

### Caractéristiques

```
✅ Component-based (composants réutilisables)
✅ Virtual DOM (performance optimale)
✅ JSX (syntaxe JavaScript + HTML)
✅ Unidirectional data flow
✅ Hooks (gestion d'état moderne)
✅ Large écosystème
✅ React Native (apps mobiles)
```

### Virtual DOM

```
Real DOM Update:
- Lent et coûteux
- Re-render complet

Virtual DOM:
1. Changement d'état
2. Update Virtual DOM
3. Diff avec ancien Virtual DOM
4. Update uniquement les changements dans Real DOM
```

## Create React App

### Installation

```bash
# Créer nouvelle app
npx create-react-app my-app

# Avec TypeScript
npx create-react-app my-app --template typescript

# Entrer dans le dossier
cd my-app

# Démarrer
npm start
```

### Structure projet

```
my-app/
├── node_modules/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── App.js
│   ├── App.css
│   ├── App.test.js
│   ├── index.js
│   ├── index.css
│   └── logo.svg
├── package.json
└── README.md
```

### Scripts disponibles

```bash
# Development
npm start          # Port 3000

# Production build
npm run build

# Tests
npm test

# Eject (⚠️ irréversible)
npm run eject
```

## Vite (Recommandé)

### Pourquoi Vite ?

```
✅ Build ultra-rapide
✅ Hot Module Replacement (HMR) instantané
✅ Configuration simple
✅ Moderne et léger
✅ Support TypeScript natif
```

### Installation

```bash
# Créer app avec Vite
npm create vite@latest my-app -- --template react

# Ou avec TypeScript
npm create vite@latest my-app -- --template react-ts

# Installer dépendances
cd my-app
npm install

# Démarrer
npm run dev
```

### Structure Vite

```
my-app/
├── node_modules/
├── public/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
└── vite.config.js
```

### Scripts Vite

```bash
npm run dev        # Development (port 5173)
npm run build      # Production build
npm run preview    # Preview build localement
```

## Premier composant

### App.jsx

```jsx
// src/App.jsx
function App() {
  return (
    <div className="App">
      <h1>Hello React!</h1>
      <p>Bienvenue dans votre première app React</p>
    </div>
  );
}

export default App;
```

### main.jsx (Vite)

```jsx
// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### index.js (CRA)

```jsx
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## React DevTools

### Installation

```
Chrome:
https://chrome.google.com/webstore/detail/react-developer-tools

Firefox:
https://addons.mozilla.org/en-US/firefox/addon/react-devtools/
```

### Utilisation

```
1. Ouvrir DevTools (F12)
2. Onglets "Components" et "Profiler" ajoutés
3. Inspecter components, props, state
4. Profiler les performances
```

## Configuration VS Code

### Extensions recommandées

```
1. ES7+ React/Redux/React-Native snippets
2. Prettier - Code formatter
3. ESLint
4. Auto Rename Tag
5. Path Intellisense
```

### Snippets utiles

```javascript
// rfc - React Functional Component
function ComponentName() {
  return <div></div>;
}
export default ComponentName;

// rafce - React Arrow Function Component Export
const ComponentName = () => {
  return <div></div>;
};
export default ComponentName;

// useState
const [state, setState] = useState(initialState);

// useEffect
useEffect(() => {
  // effect
  return () => {
    // cleanup
  };
}, [dependencies]);
```

### settings.json

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  }
}
```

## Configuration ESLint

```bash
# Installer ESLint
npm install --save-dev eslint eslint-plugin-react
```

```json
// .eslintrc.json
{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime"
  ],
  "parserOptions": {
    "ecmaVersion": 12,
    "sourceType": "module"
  },
  "rules": {
    "react/prop-types": "off",
    "no-unused-vars": "warn"
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

## Configuration Prettier

```bash
npm install --save-dev prettier
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80,
  "arrowParens": "avoid"
}
```

## Package.json basique

```json
{
  "name": "my-react-app",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.3.9"
  }
}
```

## vite.config.js

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: 'build'
  }
});
```

## Dépendances utiles

### Installation

```bash
# Router
npm install react-router-dom

# State management
npm install zustand
# ou
npm install @reduxjs/toolkit react-redux

# Forms
npm install react-hook-form

# HTTP client
npm install axios

# UI libraries
npm install @mui/material @emotion/react @emotion/styled
# ou
npm install antd

# Icons
npm install react-icons

# Styling
npm install styled-components
# ou
npm install -D tailwindcss postcss autoprefixer
```

## Structure projet recommandée

```
src/
├── components/
│   ├── common/
│   │   ├── Button.jsx
│   │   └── Input.jsx
│   ├── layout/
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   └── features/
│       └── users/
│           ├── UserList.jsx
│           └── UserCard.jsx
├── pages/
│   ├── Home.jsx
│   ├── About.jsx
│   └── NotFound.jsx
├── hooks/
│   └── useAuth.js
├── services/
│   └── api.js
├── utils/
│   └── helpers.js
├── styles/
│   └── global.css
├── App.jsx
└── main.jsx
```

## Exemple complet minimal

```jsx
// src/App.jsx
import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <h1>React Counter</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(count - 1)}>Decrement</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}

export default App;
```

```css
/* src/App.css */
.App {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

button {
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}
```

## Troubleshooting

### Problèmes courants

```bash
# Port déjà utilisé
# Changer port dans vite.config.js ou package.json

# Cache issues
rm -rf node_modules package-lock.json
npm install

# Build errors
npm run build -- --verbose

# Clear cache (CRA)
rm -rf node_modules/.cache
```

[Index](./infos-reactjs-00-index.md) | [JSX et Components →](./infos-reactjs-02-jsx-components.md)

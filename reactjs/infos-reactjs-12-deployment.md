# 🚀 Déploiement

[← Testing](./infos-reactjs-11-testing.md) | [Index](./infos-reactjs-00-index.md)

## Build production

```bash
# Vite
npm run build

# Create React App
npm run build

# Fichiers dans dist/ ou build/
```

## Variables d'environnement

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

# Usage
const apiUrl = import.meta.env.VITE_API_URL;

# CRA (sans VITE_)
REACT_APP_API_URL=https://api.example.com
const apiUrl = process.env.REACT_APP_API_URL;
```

## Vercel

```bash
npm install -g vercel
vercel login
vercel        # Deploy
vercel --prod # Production
```

## Netlify

```bash
npm install -g netlify-cli
netlify login
netlify deploy
netlify deploy --prod
```

## GitHub Pages

```bash
npm install --save-dev gh-pages
```

```json
// package.json
{
  "homepage": "https://username.github.io/repo-name",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

```bash
npm run deploy
```

## Nginx

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/app/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## Optimisations

```javascript
// vite.config.js
export default {
  build: {
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom']
        }
      }
    }
  }
};
```

[← Testing](./infos-reactjs-11-testing.md) | [Index](./infos-reactjs-00-index.md)

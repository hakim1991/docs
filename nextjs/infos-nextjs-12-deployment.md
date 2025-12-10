# 🚀 Déploiement

[← Testing](./infos-nextjs-11-testing.md) | [Index](./infos-nextjs-00-index.md)

## Vercel (Recommandé)

### CLI

```bash
npm install -g vercel
vercel login
vercel        # Preview deployment
vercel --prod # Production deployment
```

### Git Integration

1. Push sur GitHub/GitLab/Bitbucket
2. Connecter le repo sur vercel.com
3. Déploiements automatiques à chaque push

### Variables d'environnement

```bash
# Via CLI
vercel env add DATABASE_URL production
vercel env add API_KEY production

# Ou via dashboard Vercel
```

### Configuration

```javascript
// vercel.json (optionnel)
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["cdg1"],
  "env": {
    "CUSTOM_VAR": "value"
  }
}
```

## Netlify

### Installation

```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy
netlify deploy --prod
```

### Configuration

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = ".next"

[[plugins]]
  package = "@netlify/plugin-nextjs"

[build.environment]
  NODE_VERSION = "18"
```

### Next on Netlify

```bash
npm install -D @netlify/plugin-nextjs
```

## Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM node:18-alpine AS base

# Dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

```javascript
// next.config.js
module.exports = {
  output: 'standalone',
};
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - '3000:3000'
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - NODE_ENV=production
```

```bash
# Build et run
docker build -t my-next-app .
docker run -p 3000:3000 my-next-app

# Avec docker-compose
docker-compose up -d
```

## AWS (EC2, ECS, Amplify)

### AWS Amplify

```bash
npm install -g @aws-amplify/cli
amplify init
amplify add hosting
amplify publish
```

### EC2

```bash
# Sur EC2
sudo apt update
sudo apt install nodejs npm

# Clone et install
git clone https://github.com/user/repo.git
cd repo
npm install
npm run build

# PM2
npm install -g pm2
pm2 start npm --name "next-app" -- start
pm2 save
pm2 startup
```

## Static Export

### Configuration

```javascript
// next.config.js
module.exports = {
  output: 'export',
  images: {
    unoptimized: true, // Requis pour export statique
  },
};
```

```bash
npm run build
# Fichiers dans out/
```

### GitHub Pages

```json
// package.json
{
  "scripts": {
    "deploy": "next build && touch out/.nojekyll && gh-pages -d out -t true"
  }
}
```

```bash
npm install -D gh-pages
npm run deploy
```

## Self-hosting (Node.js)

### Build

```bash
npm run build
npm start
```

### PM2

```bash
npm install -g pm2

# Start
pm2 start npm --name "next-app" -- start

# Logs
pm2 logs next-app

# Restart
pm2 restart next-app

# Stop
pm2 stop next-app

# Status
pm2 status

# Auto-start on reboot
pm2 startup
pm2 save
```

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'next-app',
      script: 'npm',
      args: 'start',
      env: {
        NODE_ENV: 'production',
        PORT: 3000,
      },
    },
  ],
};
```

```bash
pm2 start ecosystem.config.js
```

## Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/next-app
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/next-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
```

## Environment Variables

### Build time

```bash
# .env.production
DATABASE_URL="postgresql://..."
API_SECRET="secret"
NEXT_PUBLIC_API_URL="https://api.example.com"
```

### Runtime

```javascript
// next.config.js
module.exports = {
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
};
```

## CI/CD avec GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

## Railway

```bash
# Install CLI
npm install -g @railway/cli

# Login et deploy
railway login
railway init
railway up
```

## Render

1. Connecter le repo sur render.com
2. Sélectionner "Web Service"
3. Build Command: `npm install && npm run build`
4. Start Command: `npm start`

## Fly.io

```bash
# Install CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch
fly deploy
```

```toml
# fly.toml
app = "my-next-app"

[build]
  [build.args]
    NODE_VERSION = "18"

[env]
  PORT = "3000"

[[services]]
  http_checks = []
  internal_port = 3000
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

## Checklist déploiement

- [ ] Build sans erreurs
- [ ] Tests passent
- [ ] Variables d'environnement configurées
- [ ] Base de données accessible
- [ ] Sécurité : HTTPS, CORS, rate limiting
- [ ] Monitoring : logs, erreurs, performance
- [ ] Backup base de données
- [ ] CDN pour assets statiques
- [ ] Compression activée
- [ ] Caching configuré

## Performance

```javascript
// next.config.js
module.exports = {
  compress: true,
  poweredByHeader: false,
  generateEtags: true,

  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ];
  },
};
```

## Monitoring

### Sentry

```bash
npm install @sentry/nextjs
```

```javascript
// sentry.client.config.js
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

### Vercel Analytics

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

[← Testing](./infos-nextjs-11-testing.md) | [Index](./infos-nextjs-00-index.md)

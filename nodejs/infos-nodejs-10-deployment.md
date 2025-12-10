# 🚀 Déploiement

[← Tests](./infos-nodejs-09-tests.md) | [Index](./infos-nodejs-00-index.md) | [Best Practices →](./infos-nodejs-11-best-practices.md)

## PM2

### Installation

```bash
npm install -g pm2
```

### Commandes basiques

```bash
# Démarrer app
pm2 start app.js
pm2 start app.js --name my-app

# Lister apps
pm2 list
pm2 ls

# Logs
pm2 logs
pm2 logs my-app

# Restart
pm2 restart my-app
pm2 restart all

# Stop
pm2 stop my-app
pm2 stop all

# Delete
pm2 delete my-app
pm2 delete all

# Info
pm2 info my-app

# Monitoring
pm2 monit
```

### Configuration ecosystem

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'my-app',
    script: './app.js',
    instances: 'max',  // ou nombre
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development',
      PORT: 3000
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 8080
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
    watch: false,
    ignore_watch: ['node_modules', 'logs'],
    max_memory_restart: '1G',
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s'
  }]
};
```

```bash
# Utiliser ecosystem
pm2 start ecosystem.config.js
pm2 start ecosystem.config.js --env production

# Reload sans downtime
pm2 reload my-app

# Graceful reload
pm2 reload my-app --update-env
```

### Auto-start au démarrage

```bash
# Générer script startup
pm2 startup

# Sauvegarder liste apps
pm2 save

# Désactiver startup
pm2 unstartup
```

## Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM node:18-alpine

# Working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy app files
COPY . .

# Expose port
EXPOSE 3000

# User non-root
USER node

# Start app
CMD ["node", "app.js"]
```

### .dockerignore

```
node_modules
npm-debug.log
.git
.env
.DS_Store
coverage
*.md
```

### Commandes Docker

```bash
# Build image
docker build -t my-app .

# Run container
docker run -p 3000:3000 my-app

# Run avec env variables
docker run -p 3000:3000 -e NODE_ENV=production my-app

# Run en background
docker run -d -p 3000:3000 --name my-app-container my-app

# Logs
docker logs my-app-container
docker logs -f my-app-container

# Stop/Start
docker stop my-app-container
docker start my-app-container

# Remove
docker rm my-app-container
docker rmi my-app
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password

volumes:
  mongo-data:
```

```bash
# Démarrer services
docker-compose up

# En background
docker-compose up -d

# Rebuild
docker-compose up --build

# Stop
docker-compose down

# Logs
docker-compose logs -f app
```

## Heroku

### Installation

```bash
# Installer Heroku CLI
npm install -g heroku

# Login
heroku login
```

### Déploiement

```bash
# Créer app
heroku create my-app-name

# Deploy
git push heroku main

# Logs
heroku logs --tail

# Ouvrir app
heroku open

# Info
heroku info
```

### Configuration

```bash
# Variables d'environnement
heroku config:set NODE_ENV=production
heroku config:set DATABASE_URL=mongodb://...

# Voir config
heroku config

# Procfile
echo "web: node app.js" > Procfile

# Scale
heroku ps:scale web=2
```

### package.json pour Heroku

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "engines": {
    "node": "18.x",
    "npm": "9.x"
  },
  "scripts": {
    "start": "node app.js"
  }
}
```

## Vercel

### Installation

```bash
npm install -g vercel
```

### Déploiement

```bash
# Login
vercel login

# Deploy
vercel

# Production
vercel --prod
```

### Configuration

```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "app.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/app.js"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

## AWS EC2

### Setup serveur

```bash
# Connecter SSH
ssh -i key.pem ubuntu@ec2-ip-address

# Update system
sudo apt update && sudo apt upgrade -y

# Installer Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Installer PM2
sudo npm install -g pm2

# Clone repo
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install --production

# Start avec PM2
pm2 start app.js --name my-app

# Setup auto-start
pm2 startup
pm2 save
```

### Nginx reverse proxy

```bash
# Installer Nginx
sudo apt install -y nginx

# Configuration
sudo nano /etc/nginx/sites-available/my-app
```

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Activer site
sudo ln -s /etc/nginx/sites-available/my-app /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir certificat
sudo certbot --nginx -d example.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Digital Ocean

### App Platform

```bash
# Installer doctl
snap install doctl

# Auth
doctl auth init

# Deploy depuis Git
# Via interface web ou doctl
doctl apps create --spec app.yaml
```

```yaml
# app.yaml
name: my-app
services:
- name: api
  github:
    repo: user/repo
    branch: main
  run_command: npm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: NODE_ENV
    value: production
```

## Netlify Functions

### Configuration

```bash
npm install -g netlify-cli
```

```javascript
// netlify/functions/api.js
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello from Netlify Functions' })
  };
};
```

```toml
# netlify.toml
[build]
  functions = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

## Railway

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Login
railway login

# Init projet
railway init

# Deploy
railway up
```

## CI/CD GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy to production
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          HOST: ${{ secrets.HOST }}
        run: |
          echo "$SSH_PRIVATE_KEY" > key.pem
          chmod 600 key.pem
          scp -i key.pem -r dist/* user@$HOST:/var/www/app/
```

## Variables d'environnement

```bash
# Development (.env)
NODE_ENV=development
PORT=3000
DB_HOST=localhost

# Production
# Configurer via plateforme (Heroku, Vercel, etc.)
heroku config:set NODE_ENV=production
vercel env add NODE_ENV production
```

## Health checks

```javascript
// app.js
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: Date.now()
  });
});

app.get('/ready', async (req, res) => {
  try {
    // Check database
    await db.ping();

    res.json({ status: 'ready' });
  } catch (err) {
    res.status(503).json({ status: 'not ready' });
  }
});
```

## Monitoring

### Logging

```bash
npm install winston
```

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

module.exports = logger;
```

### Error tracking

```bash
npm install @sentry/node
```

```javascript
const Sentry = require('@sentry/node');

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});

// Error handler
app.use(Sentry.Handlers.errorHandler());
```

[← Tests](./infos-nodejs-09-tests.md) | [Index](./infos-nodejs-00-index.md) | [Best Practices →](./infos-nodejs-11-best-practices.md)

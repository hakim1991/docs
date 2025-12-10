# ✨ Best Practices

[← Déploiement](./infos-nodejs-10-deployment.md) | [Index](./infos-nodejs-00-index.md)

## Structure de projet

### Structure recommandée

```
project/
├── src/
│   ├── controllers/
│   │   ├── authController.js
│   │   └── userController.js
│   ├── models/
│   │   └── User.js
│   ├── routes/
│   │   ├── auth.js
│   │   └── users.js
│   ├── middleware/
│   │   ├── auth.js
│   │   ├── errorHandler.js
│   │   └── validate.js
│   ├── services/
│   │   ├── authService.js
│   │   └── emailService.js
│   ├── utils/
│   │   ├── logger.js
│   │   └── helpers.js
│   ├── config/
│   │   ├── database.js
│   │   └── redis.js
│   ├── app.js
│   └── server.js
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

### Séparation des concerns

```javascript
// ❌ Mauvais (tout dans une fonction)
app.get('/users', async (req, res) => {
  try {
    const users = await User.find();
    const filtered = users.filter(u => u.active);
    await sendEmail(users);
    res.json(filtered);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ✅ Bon (séparé en couches)
// Controller
const getUsers = async (req, res) => {
  try {
    const users = await userService.getActiveUsers();
    res.json(users);
  } catch (err) {
    next(err);
  }
};

// Service
const getActiveUsers = async () => {
  const users = await User.find({ active: true });
  await emailService.notifyAdmins(users);
  return users;
};
```

## Configuration

### Centralisée

```javascript
// config/index.js
require('dotenv').config();

module.exports = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT) || 3000,
  database: {
    url: process.env.DATABASE_URL,
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true
    }
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: '24h'
  },
  email: {
    host: process.env.EMAIL_HOST,
    port: process.env.EMAIL_PORT,
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
};
```

### Par environnement

```javascript
// config/index.js
const dev = {
  port: 3000,
  database: 'mongodb://localhost:27017/dev'
};

const prod = {
  port: process.env.PORT,
  database: process.env.DATABASE_URL
};

const config = process.env.NODE_ENV === 'production' ? prod : dev;

module.exports = config;
```

## Error handling

### Error middleware centralisé

```javascript
// middleware/errorHandler.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

const errorHandler = (err, req, res, next) => {
  let { statusCode, message } = err;

  if (!err.isOperational) {
    statusCode = 500;
    message = 'Internal server error';
  }

  if (process.env.NODE_ENV === 'development') {
    console.error('ERROR:', err);
  }

  res.status(statusCode).json({
    status: 'error',
    statusCode,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = { AppError, errorHandler };
```

### Async error wrapper

```javascript
// utils/asyncHandler.js
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

module.exports = asyncHandler;

// Utilisation
const getUsers = asyncHandler(async (req, res) => {
  const users = await User.find();
  res.json(users);
});
```

## Validation

### Avec Joi

```javascript
// validators/userValidator.js
const Joi = require('joi');

const createUserSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  name: Joi.string().min(2).max(50).required()
});

const updateUserSchema = Joi.object({
  email: Joi.string().email(),
  name: Joi.string().min(2).max(50)
}).min(1);

module.exports = { createUserSchema, updateUserSchema };

// middleware/validate.js
const validate = (schema) => (req, res, next) => {
  const { error, value } = schema.validate(req.body, { abortEarly: false });

  if (error) {
    const errors = error.details.map(detail => ({
      field: detail.path.join('.'),
      message: detail.message
    }));

    return res.status(400).json({ errors });
  }

  req.validatedBody = value;
  next();
};

module.exports = validate;
```

## Logging

### Winston

```javascript
// utils/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'my-app' },
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }));
}

module.exports = logger;

// Utilisation
logger.info('Server started', { port: 3000 });
logger.error('Database error', { error: err.message });
logger.warn('Deprecated API used');
```

## Sécurité

### Headers sécurité

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

### Rate limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests',
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/api/', limiter);
```

### Input sanitization

```javascript
const { body, validationResult } = require('express-validator');

app.post('/users',
  body('email').isEmail().normalizeEmail(),
  body('name').trim().escape(),
  body('password').isLength({ min: 8 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process request
  }
);
```

## Performance

### Compression

```javascript
const compression = require('compression');

app.use(compression({
  level: 6,
  threshold: 10 * 1024,
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  }
}));
```

### Caching

```javascript
// Redis cache
const redis = require('redis');
const client = redis.createClient();

const cacheMiddleware = (duration) => async (req, res, next) => {
  const key = `cache:${req.originalUrl}`;

  try {
    const cached = await client.get(key);

    if (cached) {
      return res.json(JSON.parse(cached));
    }

    // Override res.json
    const originalJson = res.json.bind(res);
    res.json = (body) => {
      client.setEx(key, duration, JSON.stringify(body));
      return originalJson(body);
    };

    next();
  } catch (err) {
    next();
  }
};

// Utilisation
app.get('/api/users', cacheMiddleware(300), getUsers);
```

### Pagination

```javascript
const paginate = async (model, query = {}, options = {}) => {
  const page = parseInt(options.page) || 1;
  const limit = parseInt(options.limit) || 10;
  const skip = (page - 1) * limit;

  const [data, total] = await Promise.all([
    model.find(query).limit(limit).skip(skip),
    model.countDocuments(query)
  ]);

  return {
    data,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  };
};

// Utilisation
app.get('/api/users', async (req, res) => {
  const result = await paginate(User, {}, req.query);
  res.json(result);
});
```

## Tests

### Testabilité

```javascript
// ❌ Mauvais (dépendances hardcodées)
function processPayment(amount) {
  const stripe = require('stripe')('secret_key');
  return stripe.charges.create({ amount });
}

// ✅ Bon (injection de dépendances)
function processPayment(amount, paymentService) {
  return paymentService.charge(amount);
}

// Test
test('processPayment should charge correct amount', () => {
  const mockService = { charge: jest.fn().mockResolvedValue({}) };
  await processPayment(100, mockService);
  expect(mockService.charge).toHaveBeenCalledWith(100);
});
```

## Documentation

### JSDoc

```javascript
/**
 * Crée un nouvel utilisateur
 * @param {Object} userData - Données de l'utilisateur
 * @param {string} userData.email - Email de l'utilisateur
 * @param {string} userData.password - Mot de passe
 * @param {string} userData.name - Nom
 * @returns {Promise<Object>} Utilisateur créé
 * @throws {AppError} Si email déjà utilisé
 */
async function createUser(userData) {
  // Implementation
}
```

### Swagger/OpenAPI

```javascript
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'My API',
      version: '1.0.0'
    }
  },
  apis: ['./routes/*.js']
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: Récupère tous les utilisateurs
 *     responses:
 *       200:
 *         description: Liste des utilisateurs
 */
app.get('/api/users', getUsers);
```

## Code quality

### ESLint

```json
// .eslintrc.json
{
  "env": {
    "node": true,
    "es2021": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": 12
  },
  "rules": {
    "indent": ["error", 2],
    "linebreak-style": ["error", "unix"],
    "quotes": ["error", "single"],
    "semi": ["error", "always"],
    "no-console": "warn",
    "no-unused-vars": "error"
  }
}
```

### Prettier

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80
}
```

### Husky (pre-commit)

```bash
npm install --save-dev husky lint-staged

npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

```json
// package.json
{
  "lint-staged": {
    "*.js": [
      "eslint --fix",
      "prettier --write",
      "git add"
    ]
  }
}
```

## Monitoring

### Health checks

```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: Date.now(),
    memory: process.memoryUsage()
  });
});

app.get('/ready', async (req, res) => {
  try {
    await db.ping();
    await redis.ping();

    res.json({ status: 'ready' });
  } catch (err) {
    res.status(503).json({ status: 'not ready', error: err.message });
  }
});
```

### Metrics

```javascript
const promClient = require('prom-client');

const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

// Middleware
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on('finish', () => {
    end({ method: req.method, route: req.route?.path, status_code: res.statusCode });
  });
  next();
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

## Checklist production

```
✅ Variables d'environnement sécurisées
✅ Secrets pas dans le code
✅ Logs configurés (Winston)
✅ Error tracking (Sentry)
✅ Rate limiting activé
✅ Helmet configuré
✅ CORS configuré
✅ HTTPS activé
✅ Compression activée
✅ PM2 ou Docker configuré
✅ Health checks implémentés
✅ Database indexes créés
✅ Tests écrits et passent
✅ Documentation à jour
✅ Monitoring configuré
✅ Backups automatiques
```

[← Déploiement](./infos-nodejs-10-deployment.md) | [Index](./infos-nodejs-00-index.md)

# 🔒 Sécurité

[← Base de données](./infos-nodejs-07-base-de-donnees.md) | [Index](./infos-nodejs-00-index.md) | [Tests →](./infos-nodejs-09-tests.md)

## Helmet

```bash
npm install helmet
```

```javascript
const helmet = require('helmet');
const express = require('express');
const app = express();

// Utiliser tous les middlewares Helmet
app.use(helmet());

// Ou configuration personnalisée
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
```

## JWT Authentication

```bash
npm install jsonwebtoken bcrypt
```

### Créer et vérifier tokens

```javascript
const jwt = require('jsonwebtoken');
const SECRET = process.env.JWT_SECRET || 'your-secret-key';

// Créer token
function generateToken(payload) {
  return jwt.sign(payload, SECRET, { expiresIn: '24h' });
}

// Vérifier token
function verifyToken(token) {
  try {
    return jwt.verify(token, SECRET);
  } catch (err) {
    return null;
  }
}

// Middleware auth
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const decoded = verifyToken(token);
  if (!decoded) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  req.user = decoded;
  next();
};

// Routes
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  // Verify user credentials
  const user = await User.findOne({ email });

  if (!user || !await bcrypt.compare(password, user.password)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken({ id: user.id, email: user.email });
  res.json({ token });
});

app.get('/protected', authMiddleware, (req, res) => {
  res.json({ user: req.user });
});
```

## Hashing passwords

```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;

// Hash password
async function hashPassword(password) {
  return await bcrypt.hash(password, SALT_ROUNDS);
}

// Compare password
async function comparePassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// Exemple utilisation
app.post('/register', async (req, res) => {
  const { email, password } = req.body;

  // Hash password
  const hashedPassword = await hashPassword(password);

  // Create user
  const user = await User.create({
    email,
    password: hashedPassword
  });

  res.status(201).json({ id: user.id, email: user.email });
});

app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Compare passwords
  const isValid = await comparePassword(password, user.password);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken({ id: user.id, email: user.email });
  res.json({ token });
});
```

## CORS

```bash
npm install cors
```

```javascript
const cors = require('cors');

// Autoriser toutes les origines
app.use(cors());

// Configuration personnalisée
app.use(cors({
  origin: 'https://example.com',
  methods: ['GET', 'POST'],
  credentials: true
}));

// Origines multiples
app.use(cors({
  origin: ['https://example.com', 'https://app.example.com'],
  credentials: true
}));

// Fonction origin
app.use(cors({
  origin: function(origin, callback) {
    const allowedOrigins = ['https://example.com'];
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
}));
```

## Rate limiting

```bash
npm install express-rate-limit
```

```javascript
const rateLimit = require('express-rate-limit');

// Rate limiter global
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requêtes par IP
  message: 'Too many requests, please try again later'
});

app.use(limiter);

// Rate limiter pour login
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts'
});

app.post('/login', loginLimiter, (req, res) => {
  // Login logic
});
```

## Validation avec Joi

```bash
npm install joi
```

```javascript
const Joi = require('joi');

// Schéma validation
const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  name: Joi.string().min(2).max(50),
  age: Joi.number().integer().min(0).max(120)
});

// Middleware validation
const validate = (schema) => (req, res, next) => {
  const { error, value } = schema.validate(req.body);

  if (error) {
    return res.status(400).json({
      error: error.details[0].message
    });
  }

  req.validatedBody = value;
  next();
};

// Utilisation
app.post('/users', validate(userSchema), (req, res) => {
  // req.validatedBody contient les données validées
  res.json(req.validatedBody);
});

// Validation personnalisée
const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required()
});

app.post('/login', validate(loginSchema), async (req, res) => {
  // Login logic
});
```

## Sanitization

```bash
npm install express-validator
```

```javascript
const { body, validationResult } = require('express-validator');

app.post('/users',
  // Validation
  body('email').isEmail().normalizeEmail(),
  body('name').trim().escape().isLength({ min: 2, max: 50 }),
  body('password').isLength({ min: 8 }),

  // Handler
  (req, res) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    // Create user
    res.json({ message: 'User created' });
  }
);
```

## SQL Injection prevention

```javascript
// ❌ Mauvais (vulnérable)
const userId = req.params.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// ✅ Bon (paramétrisé)
const userId = req.params.id;
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);

// Avec ORM (Prisma, TypeORM, Mongoose)
// Automatiquement sécurisé
const user = await User.findById(userId);
```

## XSS Prevention

```bash
npm install xss
```

```javascript
const xss = require('xss');

// Sanitize input
app.post('/comment', (req, res) => {
  const cleanComment = xss(req.body.comment);

  // Save cleanComment
  res.json({ comment: cleanComment });
});

// Avec express-validator
body('comment').trim().escape();
```

## CSRF Protection

```bash
npm install csurf cookie-parser
```

```javascript
const csrf = require('csurf');
const cookieParser = require('cookie-parser');

app.use(cookieParser());
app.use(csrf({ cookie: true }));

app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/submit', (req, res) => {
  res.send('Form submitted');
});
```

## Environment variables

```bash
npm install dotenv
```

```
# .env
NODE_ENV=production
PORT=3000
DATABASE_URL=mongodb://localhost:27017/mydb
JWT_SECRET=your-secret-key
API_KEY=your-api-key
```

```javascript
require('dotenv').config();

const config = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 3000,
  database: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  apiKey: process.env.API_KEY
};

// ⚠️ Ne jamais commit .env
// Ajouter dans .gitignore
```

## HTTPS

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};

https.createServer(options, app).listen(443, () => {
  console.log('HTTPS server running on port 443');
});
```

## Security headers

```javascript
// Security headers manuels
app.use((req, res, next) => {
  // Strict Transport Security
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');

  // X-Frame-Options
  res.setHeader('X-Frame-Options', 'DENY');

  // X-Content-Type-Options
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // X-XSS-Protection
  res.setHeader('X-XSS-Protection', '1; mode=block');

  // Content Security Policy
  res.setHeader('Content-Security-Policy', "default-src 'self'");

  next();
});
```

## Exemple complet sécurisé

```javascript
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const Joi = require('joi');
require('dotenv').config();

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true
}));

app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
app.use(limiter);

// Validation middleware
const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body);
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }
  next();
};

// Auth middleware
const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Schemas
const registerSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  name: Joi.string().min(2).max(50).required()
});

const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required()
});

// Routes
app.post('/register', validate(registerSchema), async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create user (avec votre DB)
    // const user = await User.create({ email, password: hashedPassword, name });

    res.status(201).json({ message: 'User created' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5
});

app.post('/login', loginLimiter, validate(loginSchema), async (req, res) => {
  try {
    const { email, password } = req.body;

    // Get user (avec votre DB)
    // const user = await User.findOne({ email });

    // Verify password
    // const isValid = await bcrypt.compare(password, user.password);

    // Generate token
    const token = jwt.sign(
      { id: 'user-id', email },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/protected', auth, (req, res) => {
  res.json({ user: req.user });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

[← Base de données](./infos-nodejs-07-base-de-donnees.md) | [Index](./infos-nodejs-00-index.md) | [Tests →](./infos-nodejs-09-tests.md)

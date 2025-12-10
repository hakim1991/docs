# 🌐 Express et Serveur Web

[← APIs Natives](./infos-nodejs-05-apis-natives.md) | [Index](./infos-nodejs-00-index.md) | [Base de données →](./infos-nodejs-07-base-de-donnees.md)

## Installation Express

```bash
# Installer Express
npm install express

# Avec TypeScript
npm install express
npm install --save-dev @types/express
```

## Serveur basique

```javascript
// app.js
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

## Routing

### Routes basiques

```javascript
const express = require('express');
const app = express();

// GET
app.get('/', (req, res) => {
  res.send('GET request');
});

// POST
app.post('/users', (req, res) => {
  res.send('POST request');
});

// PUT
app.put('/users/:id', (req, res) => {
  res.send('PUT request');
});

// DELETE
app.delete('/users/:id', (req, res) => {
  res.send('DELETE request');
});

// ALL methods
app.all('/test', (req, res) => {
  res.send('Any HTTP method');
});
```

### Paramètres de route

```javascript
// URL params
app.get('/users/:id', (req, res) => {
  const userId = req.params.id;
  res.send(`User ID: ${userId}`);
});

// Multiple params
app.get('/users/:userId/posts/:postId', (req, res) => {
  const { userId, postId } = req.params;
  res.json({ userId, postId });
});

// Query params
app.get('/search', (req, res) => {
  const { q, page } = req.query;
  res.json({ query: q, page });
});
// GET /search?q=nodejs&page=1
```

### Router

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.json({ users: [] });
});

router.get('/:id', (req, res) => {
  res.json({ id: req.params.id });
});

router.post('/', (req, res) => {
  res.status(201).json({ message: 'User created' });
});

module.exports = router;

// app.js
const usersRouter = require('./routes/users');
app.use('/api/users', usersRouter);
```

## Middleware

### Middleware basique

```javascript
// Logger middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

// Authentication middleware
const auth = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  // Verify token
  next();
};

app.get('/protected', auth, (req, res) => {
  res.json({ message: 'Protected route' });
});
```

### Built-in middleware

```javascript
// Body parser (JSON)
app.use(express.json());

// Body parser (URL-encoded)
app.use(express.urlencoded({ extended: true }));

// Static files
app.use(express.static('public'));
app.use('/static', express.static('public'));
```

### Third-party middleware

```javascript
// CORS
const cors = require('cors');
app.use(cors());

// Morgan (logging)
const morgan = require('morgan');
app.use(morgan('dev'));

// Helmet (security)
const helmet = require('helmet');
app.use(helmet());

// Compression
const compression = require('compression');
app.use(compression());

// Cookie parser
const cookieParser = require('cookie-parser');
app.use(cookieParser());
```

## Request

```javascript
app.get('/request-demo', (req, res) => {
  // URL params
  console.log('Params:', req.params);

  // Query params
  console.log('Query:', req.query);

  // Body
  console.log('Body:', req.body);

  // Headers
  console.log('Headers:', req.headers);
  console.log('User-Agent:', req.get('User-Agent'));

  // Cookies
  console.log('Cookies:', req.cookies);

  // Method & URL
  console.log('Method:', req.method);
  console.log('URL:', req.url);
  console.log('Path:', req.path);
  console.log('Protocol:', req.protocol);
  console.log('Hostname:', req.hostname);

  // IP
  console.log('IP:', req.ip);

  res.send('Check console');
});
```

## Response

```javascript
app.get('/response-demo', (req, res) => {
  // Send text
  res.send('Hello');

  // Send JSON
  res.json({ message: 'Hello' });

  // Status code
  res.status(404).send('Not Found');
  res.status(201).json({ created: true });

  // Redirect
  res.redirect('/other-route');
  res.redirect(301, '/permanent');

  // Download file
  res.download('/path/to/file.pdf');

  // Send file
  res.sendFile(__dirname + '/public/index.html');

  // Set headers
  res.set('Content-Type', 'text/html');
  res.header('X-Custom-Header', 'value');

  // Cookies
  res.cookie('name', 'value', { maxAge: 900000 });
  res.clearCookie('name');

  // End
  res.end();
});
```

## REST API complet

```javascript
// app.js
const express = require('express');
const app = express();

app.use(express.json());

// In-memory database
let users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
];

// GET all users
app.get('/api/users', (req, res) => {
  res.json(users);
});

// GET user by ID
app.get('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

// POST create user
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required' });
  }

  const newUser = {
    id: users.length + 1,
    name,
    email
  };

  users.push(newUser);
  res.status(201).json(newUser);
});

// PUT update user
app.put('/api/users/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  const { name, email } = req.body;
  if (name) user.name = name;
  if (email) user.email = email;

  res.json(user);
});

// DELETE user
app.delete('/api/users/:id', (req, res) => {
  const index = users.findIndex(u => u.id === parseInt(req.params.id));

  if (index === -1) {
    return res.status(404).json({ error: 'User not found' });
  }

  users.splice(index, 1);
  res.status(204).send();
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## Error handling

```javascript
// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// Custom error
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
  }
}

app.get('/error-demo', (req, res, next) => {
  try {
    throw new AppError('Custom error', 400);
  } catch (err) {
    next(err);
  }
});

// Async error handler
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get('/async-route', asyncHandler(async (req, res) => {
  const data = await someAsyncFunction();
  res.json(data);
}));
```

## Validation

```javascript
// Avec Joi
const Joi = require('joi');

const userSchema = Joi.object({
  name: Joi.string().min(3).max(30).required(),
  email: Joi.string().email().required(),
  age: Joi.number().integer().min(0).max(120)
});

app.post('/api/users', (req, res) => {
  const { error, value } = userSchema.validate(req.body);

  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }

  // Create user avec value
  res.json(value);
});

// Middleware validation
const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body);
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }
  next();
};

app.post('/api/users', validate(userSchema), (req, res) => {
  res.json(req.body);
});
```

## Configuration

```javascript
// config.js
module.exports = {
  port: process.env.PORT || 3000,
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    name: process.env.DB_NAME || 'mydb'
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'secret',
    expiresIn: '24h'
  }
};

// app.js
const config = require('./config');

app.listen(config.port, () => {
  console.log(`Server running on port ${config.port}`);
});
```

## Structure projet

```
project/
├── src/
│   ├── controllers/
│   │   ├── userController.js
│   │   └── authController.js
│   ├── routes/
│   │   ├── users.js
│   │   └── auth.js
│   ├── middleware/
│   │   ├── auth.js
│   │   ├── validate.js
│   │   └── errorHandler.js
│   ├── models/
│   │   └── User.js
│   ├── services/
│   │   └── emailService.js
│   ├── utils/
│   │   └── logger.js
│   ├── config/
│   │   └── database.js
│   └── app.js
├── tests/
├── package.json
└── .env
```

## Template engines

### EJS

```bash
npm install ejs
```

```javascript
app.set('view engine', 'ejs');
app.set('views', './views');

app.get('/', (req, res) => {
  res.render('index', { title: 'Home', user: 'Alice' });
});
```

```html
<!-- views/index.ejs -->
<!DOCTYPE html>
<html>
<head>
  <title><%= title %></title>
</head>
<body>
  <h1>Welcome <%= user %></h1>
</body>
</html>
```

### Pug

```bash
npm install pug
```

```javascript
app.set('view engine', 'pug');

app.get('/', (req, res) => {
  res.render('index', { title: 'Home' });
});
```

```pug
// views/index.pug
html
  head
    title= title
  body
    h1 Welcome
```

## File upload

```bash
npm install multer
```

```javascript
const multer = require('multer');

// Storage config
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage });

// Single file
app.post('/upload', upload.single('file'), (req, res) => {
  res.json({ file: req.file });
});

// Multiple files
app.post('/uploads', upload.array('files', 10), (req, res) => {
  res.json({ files: req.files });
});

// Multiple fields
app.post('/form', upload.fields([
  { name: 'avatar', maxCount: 1 },
  { name: 'gallery', maxCount: 8 }
]), (req, res) => {
  res.json({
    avatar: req.files.avatar,
    gallery: req.files.gallery
  });
});
```

## Sessions

```bash
npm install express-session
```

```javascript
const session = require('express-session');

app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 3600000 } // 1 hour
}));

app.get('/login', (req, res) => {
  req.session.userId = 123;
  res.send('Logged in');
});

app.get('/profile', (req, res) => {
  if (!req.session.userId) {
    return res.status(401).send('Not authenticated');
  }
  res.send(`User ID: ${req.session.userId}`);
});

app.get('/logout', (req, res) => {
  req.session.destroy();
  res.send('Logged out');
});
```

## WebSockets

```bash
npm install socket.io
```

```javascript
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

io.on('connection', (socket) => {
  console.log('Client connected');

  socket.on('message', (data) => {
    console.log('Received:', data);
    socket.emit('response', { received: true });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(3000);
```

[← APIs Natives](./infos-nodejs-05-apis-natives.md) | [Index](./infos-nodejs-00-index.md) | [Base de données →](./infos-nodejs-07-base-de-donnees.md)

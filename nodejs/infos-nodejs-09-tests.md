# 🧪 Tests

[← Sécurité](./infos-nodejs-08-securite.md) | [Index](./infos-nodejs-00-index.md) | [Déploiement →](./infos-nodejs-10-deployment.md)

## Jest

### Installation

```bash
npm install --save-dev jest
```

### Configuration

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "jest": {
    "testEnvironment": "node",
    "coveragePathIgnorePatterns": ["/node_modules/"]
  }
}
```

### Tests unitaires

```javascript
// math.js
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

module.exports = { add, subtract };
```

```javascript
// math.test.js
const { add, subtract } = require('./math');

describe('Math functions', () => {
  test('add 2 + 3 should equal 5', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('subtract 5 - 3 should equal 2', () => {
    expect(subtract(5, 3)).toBe(2);
  });

  test('add should return number', () => {
    expect(typeof add(1, 2)).toBe('number');
  });
});
```

### Matchers

```javascript
// Equality
expect(value).toBe(4);
expect(value).toEqual({ name: 'Alice' });

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3.5);
expect(value).toBeLessThan(5);
expect(value).toBeCloseTo(0.3);

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');

// Arrays
expect(array).toContain('item');
expect(array).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toMatchObject({ name: 'Alice' });

// Exceptions
expect(() => {
  throw new Error('error');
}).toThrow();
```

### Async tests

```javascript
// Async/await
test('async test', async () => {
  const data = await fetchData();
  expect(data).toBe('value');
});

// Promises
test('promise test', () => {
  return fetchData().then(data => {
    expect(data).toBe('value');
  });
});

// Resolve/Reject
test('resolves to value', async () => {
  await expect(fetchData()).resolves.toBe('value');
});

test('rejects with error', async () => {
  await expect(fetchError()).rejects.toThrow('error');
});
```

### Setup et Teardown

```javascript
// Avant/Après chaque test
beforeEach(() => {
  // Setup
  initializeDatabase();
});

afterEach(() => {
  // Cleanup
  clearDatabase();
});

// Avant/Après tous les tests
beforeAll(() => {
  // Setup global
  connectDatabase();
});

afterAll(() => {
  // Cleanup global
  disconnectDatabase();
});
```

### Mocks

```javascript
// Mock function
const mockFn = jest.fn();
mockFn('arg');
expect(mockFn).toHaveBeenCalledWith('arg');

// Mock return value
const mockFn = jest.fn().mockReturnValue('value');
expect(mockFn()).toBe('value');

// Mock module
jest.mock('./api');
const api = require('./api');
api.fetchData.mockResolvedValue({ data: 'test' });

// Spy
const spy = jest.spyOn(object, 'method');
object.method();
expect(spy).toHaveBeenCalled();
spy.mockRestore();
```

## Supertest (Tests API)

### Installation

```bash
npm install --save-dev supertest
```

### Tests routes Express

```javascript
// app.js
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/users', (req, res) => {
  res.json([{ id: 1, name: 'Alice' }]);
});

app.post('/api/users', (req, res) => {
  res.status(201).json(req.body);
});

module.exports = app;
```

```javascript
// app.test.js
const request = require('supertest');
const app = require('./app');

describe('API Tests', () => {
  test('GET /api/users should return users', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect(200)
      .expect('Content-Type', /json/);

    expect(response.body).toBeInstanceOf(Array);
    expect(response.body[0]).toHaveProperty('name', 'Alice');
  });

  test('POST /api/users should create user', async () => {
    const newUser = { name: 'Bob', email: 'bob@example.com' };

    const response = await request(app)
      .post('/api/users')
      .send(newUser)
      .expect(201)
      .expect('Content-Type', /json/);

    expect(response.body).toMatchObject(newUser);
  });

  test('GET /api/invalid should return 404', async () => {
    await request(app)
      .get('/api/invalid')
      .expect(404);
  });
});
```

### Tests avec authentification

```javascript
test('Protected route without token', async () => {
  await request(app)
    .get('/api/protected')
    .expect(401);
});

test('Protected route with token', async () => {
  const token = 'valid-jwt-token';

  await request(app)
    .get('/api/protected')
    .set('Authorization', `Bearer ${token}`)
    .expect(200);
});
```

## Tests de base de données

### MongoDB Memory Server

```bash
npm install --save-dev mongodb-memory-server
```

```javascript
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const User = require('./models/User');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const mongoUri = mongoServer.getUri();
  await mongoose.connect(mongoUri);
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

afterEach(async () => {
  await User.deleteMany({});
});

describe('User Model', () => {
  test('Create user', async () => {
    const user = await User.create({
      name: 'Alice',
      email: 'alice@example.com'
    });

    expect(user).toHaveProperty('_id');
    expect(user.name).toBe('Alice');
  });

  test('Find user', async () => {
    await User.create({ name: 'Alice', email: 'alice@example.com' });

    const user = await User.findOne({ name: 'Alice' });
    expect(user).toBeTruthy();
    expect(user.email).toBe('alice@example.com');
  });
});
```

## Coverage

```bash
# Générer coverage
npm run test:coverage

# Fichiers générés dans coverage/
```

```json
// package.json
{
  "jest": {
    "collectCoverageFrom": [
      "src/**/*.js",
      "!src/index.js",
      "!src/**/*.test.js"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Exemple complet

```javascript
// userService.js
const User = require('./models/User');

class UserService {
  async createUser(userData) {
    if (!userData.email) {
      throw new Error('Email is required');
    }

    const existingUser = await User.findOne({ email: userData.email });
    if (existingUser) {
      throw new Error('User already exists');
    }

    return await User.create(userData);
  }

  async getUserById(id) {
    const user = await User.findById(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async getAllUsers() {
    return await User.find();
  }
}

module.exports = new UserService();
```

```javascript
// userService.test.js
const userService = require('./userService');
const User = require('./models/User');

jest.mock('./models/User');

describe('UserService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    test('should create user successfully', async () => {
      const userData = { name: 'Alice', email: 'alice@example.com' };

      User.findOne.mockResolvedValue(null);
      User.create.mockResolvedValue({ id: 1, ...userData });

      const user = await userService.createUser(userData);

      expect(User.findOne).toHaveBeenCalledWith({ email: userData.email });
      expect(User.create).toHaveBeenCalledWith(userData);
      expect(user).toMatchObject(userData);
    });

    test('should throw error if email missing', async () => {
      await expect(userService.createUser({ name: 'Alice' }))
        .rejects.toThrow('Email is required');
    });

    test('should throw error if user exists', async () => {
      User.findOne.mockResolvedValue({ id: 1 });

      await expect(userService.createUser({ email: 'alice@example.com' }))
        .rejects.toThrow('User already exists');
    });
  });

  describe('getUserById', () => {
    test('should return user', async () => {
      const user = { id: 1, name: 'Alice' };
      User.findById.mockResolvedValue(user);

      const result = await userService.getUserById(1);

      expect(User.findById).toHaveBeenCalledWith(1);
      expect(result).toEqual(user);
    });

    test('should throw error if user not found', async () => {
      User.findById.mockResolvedValue(null);

      await expect(userService.getUserById(999))
        .rejects.toThrow('User not found');
    });
  });
});
```

```javascript
// userController.test.js
const request = require('supertest');
const app = require('./app');
const userService = require('./userService');

jest.mock('./userService');

describe('User Controller', () => {
  describe('POST /api/users', () => {
    test('should create user', async () => {
      const userData = { name: 'Alice', email: 'alice@example.com' };
      userService.createUser.mockResolvedValue({ id: 1, ...userData });

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject(userData);
    });

    test('should return 400 on validation error', async () => {
      userService.createUser.mockRejectedValue(new Error('Email is required'));

      await request(app)
        .post('/api/users')
        .send({ name: 'Alice' })
        .expect(400);
    });
  });

  describe('GET /api/users/:id', () => {
    test('should return user', async () => {
      const user = { id: 1, name: 'Alice' };
      userService.getUserById.mockResolvedValue(user);

      const response = await request(app)
        .get('/api/users/1')
        .expect(200);

      expect(response.body).toEqual(user);
    });

    test('should return 404 if not found', async () => {
      userService.getUserById.mockRejectedValue(new Error('User not found'));

      await request(app)
        .get('/api/users/999')
        .expect(404);
    });
  });
});
```

[← Sécurité](./infos-nodejs-08-securite.md) | [Index](./infos-nodejs-00-index.md) | [Déploiement →](./infos-nodejs-10-deployment.md)

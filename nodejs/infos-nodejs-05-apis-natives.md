# ⚙️ APIs Natives

[← Modules](./infos-nodejs-04-modules-commonjs-esm.md) | [Index](./infos-nodejs-00-index.md) | [Express →](./infos-nodejs-06-express-serveur-web.md)

## File System (fs)

### Lire fichiers

```javascript
const fs = require('fs');

// Synchrone
try {
  const data = fs.readFileSync('file.txt', 'utf8');
  console.log(data);
} catch (err) {
  console.error('Error:', err);
}

// Asynchrone (callback)
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log(data);
});

// Asynchrone (promises)
const fs = require('fs/promises');

async function readFile() {
  try {
    const data = await fs.readFile('file.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error('Error:', err);
  }
}

readFile();
```

### Écrire fichiers

```javascript
const fs = require('fs');

// Synchrone
fs.writeFileSync('output.txt', 'Hello World');

// Asynchrone
fs.writeFile('output.txt', 'Hello World', (err) => {
  if (err) console.error(err);
  console.log('File written');
});

// Promises
const fs = require('fs/promises');

await fs.writeFile('output.txt', 'Hello World');

// Append
await fs.appendFile('log.txt', 'New log entry\n');
```

### Opérations fichiers

```javascript
const fs = require('fs/promises');

// Copier
await fs.copyFile('source.txt', 'dest.txt');

// Renommer / déplacer
await fs.rename('old.txt', 'new.txt');

// Supprimer
await fs.unlink('file.txt');

// Stats
const stats = await fs.stat('file.txt');
console.log('Size:', stats.size);
console.log('Is file:', stats.isFile());
console.log('Is directory:', stats.isDirectory());
console.log('Modified:', stats.mtime);

// Vérifier existence
try {
  await fs.access('file.txt');
  console.log('File exists');
} catch {
  console.log('File does not exist');
}
```

### Répertoires

```javascript
const fs = require('fs/promises');

// Créer répertoire
await fs.mkdir('mydir');
await fs.mkdir('nested/dir', { recursive: true });

// Lire répertoire
const files = await fs.readdir('mydir');
console.log('Files:', files);

// Avec détails
const entries = await fs.readdir('mydir', { withFileTypes: true });
for (const entry of entries) {
  console.log(entry.name, entry.isDirectory() ? '(dir)' : '(file)');
}

// Supprimer répertoire
await fs.rmdir('mydir');
await fs.rm('mydir', { recursive: true, force: true });
```

### Streams

```javascript
const fs = require('fs');

// Read stream
const readStream = fs.createReadStream('large-file.txt', 'utf8');

readStream.on('data', (chunk) => {
  console.log('Chunk:', chunk);
});

readStream.on('end', () => {
  console.log('Finished reading');
});

readStream.on('error', (err) => {
  console.error('Error:', err);
});

// Write stream
const writeStream = fs.createWriteStream('output.txt');
writeStream.write('Line 1\n');
writeStream.write('Line 2\n');
writeStream.end();

// Pipe
const readStream = fs.createReadStream('input.txt');
const writeStream = fs.createWriteStream('output.txt');
readStream.pipe(writeStream);
```

## Path

```javascript
const path = require('path');

// Join paths
const filePath = path.join('/users', 'john', 'documents', 'file.txt');
console.log(filePath); // /users/john/documents/file.txt

// Resolve (absolu)
const absolute = path.resolve('docs', 'file.txt');
console.log(absolute); // /current/working/dir/docs/file.txt

// Basename
console.log(path.basename('/users/john/file.txt')); // file.txt
console.log(path.basename('/users/john/file.txt', '.txt')); // file

// Dirname
console.log(path.dirname('/users/john/file.txt')); // /users/john

// Extension
console.log(path.extname('file.txt')); // .txt
console.log(path.extname('file.tar.gz')); // .gz

// Parse
const parsed = path.parse('/users/john/file.txt');
console.log(parsed);
// {
//   root: '/',
//   dir: '/users/john',
//   base: 'file.txt',
//   ext: '.txt',
//   name: 'file'
// }

// Format
const formatted = path.format({
  dir: '/users/john',
  base: 'file.txt'
});
console.log(formatted); // /users/john/file.txt

// Normalize
console.log(path.normalize('/users//john/../file.txt')); // /users/file.txt

// Relatif
console.log(path.relative('/users/john', '/users/jane/file.txt')); // ../jane/file.txt

// Separator
console.log(path.sep); // / (Unix) ou \ (Windows)
console.log(path.delimiter); // : (Unix) ou ; (Windows)
```

## OS

```javascript
const os = require('os');

// Platform
console.log('Platform:', os.platform()); // linux, darwin, win32
console.log('Architecture:', os.arch()); // x64, arm, etc.
console.log('Release:', os.release());
console.log('Type:', os.type());

// CPU
console.log('CPUs:', os.cpus().length);
console.log('CPU Info:', os.cpus()[0]);

// Memory
console.log('Total memory:', os.totalmem() / 1024 / 1024 / 1024, 'GB');
console.log('Free memory:', os.freemem() / 1024 / 1024 / 1024, 'GB');

// User
console.log('Hostname:', os.hostname());
console.log('User info:', os.userInfo());
console.log('Home directory:', os.homedir());
console.log('Temp directory:', os.tmpdir());

// Network
console.log('Network interfaces:', os.networkInterfaces());

// Uptime
console.log('Uptime:', os.uptime(), 'seconds');

// EOL
console.log('End of line:', os.EOL); // \n (Unix) ou \r\n (Windows)
```

## HTTP

### Serveur HTTP basique

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  console.log('Request:', req.method, req.url);

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Routes basiques

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/' && req.method === 'GET') {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>Home Page</h1>');
  }
  else if (req.url === '/api/users' && req.method === 'GET') {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ users: ['Alice', 'Bob'] }));
  }
  else {
    res.statusCode = 404;
    res.end('Not Found');
  }
});

server.listen(3000);
```

### HTTP Client

```javascript
const http = require('http');

// GET request
http.get('http://api.example.com/data', (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('Response:', data);
  });
}).on('error', (err) => {
  console.error('Error:', err);
});

// POST request
const postData = JSON.stringify({ name: 'Alice' });

const options = {
  hostname: 'api.example.com',
  port: 80,
  path: '/users',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = http.request(options, (res) => {
  console.log('Status:', res.statusCode);

  res.on('data', (chunk) => {
    console.log('Body:', chunk.toString());
  });
});

req.on('error', (err) => {
  console.error('Error:', err);
});

req.write(postData);
req.end();
```

## Events

```javascript
const EventEmitter = require('events');

// Créer emitter
class MyEmitter extends EventEmitter {}
const myEmitter = new MyEmitter();

// On (écouter événement)
myEmitter.on('event', (data) => {
  console.log('Event occurred:', data);
});

// Once (une seule fois)
myEmitter.once('event', () => {
  console.log('This will run only once');
});

// Emit (déclencher événement)
myEmitter.emit('event', { message: 'Hello' });

// Remove listener
const listener = () => console.log('Listener');
myEmitter.on('event', listener);
myEmitter.removeListener('event', listener);

// Remove all listeners
myEmitter.removeAllListeners('event');

// Exemple pratique
class Logger extends EventEmitter {
  log(message) {
    console.log(message);
    this.emit('logged', { message, timestamp: Date.now() });
  }
}

const logger = new Logger();
logger.on('logged', (data) => {
  console.log('Log event:', data);
});

logger.log('Test message');
```

## Streams

```javascript
const { Readable, Writable, Transform, pipeline } = require('stream');

// Readable stream
class MyReadable extends Readable {
  constructor(options) {
    super(options);
    this.counter = 0;
  }

  _read() {
    if (this.counter < 10) {
      this.push(`Data ${this.counter}\n`);
      this.counter++;
    } else {
      this.push(null); // Fin
    }
  }
}

const readable = new MyReadable();
readable.pipe(process.stdout);

// Writable stream
class MyWritable extends Writable {
  _write(chunk, encoding, callback) {
    console.log('Writing:', chunk.toString());
    callback();
  }
}

const writable = new MyWritable();
readable.pipe(writable);

// Transform stream
class MyTransform extends Transform {
  _transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
}

const transform = new MyTransform();
readable.pipe(transform).pipe(process.stdout);

// Pipeline
const fs = require('fs');
const { createGzip } = require('zlib');

pipeline(
  fs.createReadStream('input.txt'),
  createGzip(),
  fs.createWriteStream('input.txt.gz'),
  (err) => {
    if (err) {
      console.error('Pipeline failed:', err);
    } else {
      console.log('Pipeline succeeded');
    }
  }
);
```

## Buffer

```javascript
// Créer buffer
const buf1 = Buffer.from('Hello');
const buf2 = Buffer.from([72, 101, 108, 108, 111]);
const buf3 = Buffer.alloc(10); // Buffer vide de 10 bytes
const buf4 = Buffer.allocUnsafe(10); // Plus rapide mais non initialisé

// Lire
console.log(buf1.toString()); // Hello
console.log(buf1.toString('hex')); // 48656c6c6f
console.log(buf1.toString('base64')); // SGVsbG8=

// Écrire
buf3.write('Hello');
console.log(buf3.toString());

// Comparer
console.log(buf1.equals(buf2)); // true
console.log(Buffer.compare(buf1, buf2)); // 0

// Concat
const buf5 = Buffer.concat([buf1, buf2]);
console.log(buf5.toString()); // HelloHello

// Slice
const buf6 = buf1.slice(0, 2);
console.log(buf6.toString()); // He

// JSON
console.log(buf1.toJSON()); // { type: 'Buffer', data: [72, 101, 108, 108, 111] }
```

## URL

```javascript
const url = require('url');

// Parse URL
const myURL = new URL('https://user:pass@example.com:8080/path?query=value#hash');

console.log('Protocol:', myURL.protocol); // https:
console.log('Username:', myURL.username); // user
console.log('Password:', myURL.password); // pass
console.log('Host:', myURL.host); // example.com:8080
console.log('Hostname:', myURL.hostname); // example.com
console.log('Port:', myURL.port); // 8080
console.log('Pathname:', myURL.pathname); // /path
console.log('Search:', myURL.search); // ?query=value
console.log('Hash:', myURL.hash); // #hash

// Query params
const params = myURL.searchParams;
console.log('Query:', params.get('query')); // value
params.append('new', 'param');
params.set('query', 'newvalue');
console.log(myURL.href);

// Format URL
const formatted = url.format({
  protocol: 'https',
  hostname: 'example.com',
  pathname: '/path',
  search: '?query=value'
});
console.log(formatted); // https://example.com/path?query=value
```

## Crypto

```javascript
const crypto = require('crypto');

// Hash
const hash = crypto.createHash('sha256');
hash.update('Hello World');
console.log('Hash:', hash.digest('hex'));

// HMAC
const hmac = crypto.createHmac('sha256', 'secret-key');
hmac.update('Hello World');
console.log('HMAC:', hmac.digest('hex'));

// Random
const randomBytes = crypto.randomBytes(16);
console.log('Random:', randomBytes.toString('hex'));

const randomUUID = crypto.randomUUID();
console.log('UUID:', randomUUID);

// Encrypt / Decrypt
const algorithm = 'aes-256-cbc';
const key = crypto.randomBytes(32);
const iv = crypto.randomBytes(16);

function encrypt(text) {
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
}

function decrypt(encrypted) {
  const decipher = crypto.createDecipheriv(algorithm, key, iv);
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

const encrypted = encrypt('Secret message');
console.log('Encrypted:', encrypted);
console.log('Decrypted:', decrypt(encrypted));
```

## Child Process

```javascript
const { exec, spawn, execFile, fork } = require('child_process');

// exec (commande shell)
exec('ls -la', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Output:', stdout);
});

// spawn (processus)
const ls = spawn('ls', ['-la']);

ls.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

ls.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

ls.on('close', (code) => {
  console.log(`Exit code: ${code}`);
});

// execFile
execFile('node', ['--version'], (error, stdout, stderr) => {
  console.log('Node version:', stdout);
});

// fork (Node.js process)
const child = fork('child.js');
child.send({ hello: 'world' });
child.on('message', (msg) => {
  console.log('Message from child:', msg);
});
```

## Timers

```javascript
// setTimeout
const timeout = setTimeout(() => {
  console.log('Executed after 2 seconds');
}, 2000);

clearTimeout(timeout);

// setInterval
let count = 0;
const interval = setInterval(() => {
  count++;
  console.log('Count:', count);
  if (count >= 5) {
    clearInterval(interval);
  }
}, 1000);

// setImmediate
setImmediate(() => {
  console.log('Immediate');
});

// Promises
const { setTimeout: setTimeoutPromise } = require('timers/promises');

async function delay() {
  await setTimeoutPromise(2000);
  console.log('After 2 seconds');
}

delay();
```

[← Modules](./infos-nodejs-04-modules-commonjs-esm.md) | [Index](./infos-nodejs-00-index.md) | [Express →](./infos-nodejs-06-express-serveur-web.md)

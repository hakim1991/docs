# 🗄️ Base de données

[← Authentification](./infos-nextjs-08-authentication.md) | [Index](./infos-nextjs-00-index.md) | [Optimisation →](./infos-nextjs-10-optimization.md)

## Prisma (Recommandé)

### Installation

```bash
npm install prisma @prisma/client
npx prisma init
```

### Configuration

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

### Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
}
```

### Migrations

```bash
# Créer migration
npx prisma migrate dev --name init

# Appliquer migrations en production
npx prisma migrate deploy

# Générer client
npx prisma generate

# Prisma Studio (GUI)
npx prisma studio
```

### Client Prisma

```tsx
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

### CRUD Operations

```tsx
// app/users/page.tsx
import { prisma } from '@/lib/prisma';

export default async function UsersPage() {
  // READ - Lire tous les users
  const users = await prisma.user.findMany({
    include: {
      posts: true,
    },
    orderBy: {
      createdAt: 'desc',
    },
  });

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.name} - {user.posts.length} posts
          </li>
        ))}
      </ul>
    </div>
  );
}
```

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// CREATE - Créer user
export async function POST(request: NextRequest) {
  const { email, name } = await request.json();

  const user = await prisma.user.create({
    data: {
      email,
      name,
    },
  });

  return NextResponse.json(user, { status: 201 });
}
```

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// UPDATE - Modifier user
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { name, email } = await request.json();

  const user = await prisma.user.update({
    where: { id: params.id },
    data: { name, email },
  });

  return NextResponse.json(user);
}

// DELETE - Supprimer user
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await prisma.user.delete({
    where: { id: params.id },
  });

  return NextResponse.json({ message: 'User deleted' });
}
```

### Relations et Queries avancées

```tsx
// Créer user avec posts
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    posts: {
      create: [
        { title: 'Post 1', content: 'Content 1' },
        { title: 'Post 2', content: 'Content 2' },
      ],
    },
  },
  include: {
    posts: true,
  },
});

// Trouver un user avec conditions
const user = await prisma.user.findFirst({
  where: {
    email: 'alice@example.com',
    posts: {
      some: {
        published: true,
      },
    },
  },
  include: {
    posts: {
      where: {
        published: true,
      },
    },
  },
});

// Compter
const userCount = await prisma.user.count({
  where: {
    posts: {
      some: {
        published: true,
      },
    },
  },
});

// Agréger
const result = await prisma.post.aggregate({
  _count: true,
  _avg: {
    views: true,
  },
});
```

### Transactions

```tsx
// Transaction avec Prisma
const result = await prisma.$transaction([
  prisma.user.create({ data: { email: 'user@example.com', name: 'User' } }),
  prisma.post.create({ data: { title: 'Post', authorId: 'user-id' } }),
]);

// Transaction interactive
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'user@example.com', name: 'User' },
  });

  await tx.post.create({
    data: { title: 'Post', authorId: user.id },
  });
});
```

## MongoDB avec Mongoose

### Installation

```bash
npm install mongoose
```

### Configuration

```bash
# .env
MONGODB_URI="mongodb://localhost:27017/mydb"
```

### Connexion

```tsx
// lib/mongodb.ts
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI!;

if (!MONGODB_URI) {
  throw new Error('Please define MONGODB_URI in .env');
}

let cached = (global as any).mongoose;

if (!cached) {
  cached = (global as any).mongoose = { conn: null, promise: null };
}

export async function connectDB() {
  if (cached.conn) {
    return cached.conn;
  }

  if (!cached.promise) {
    cached.promise = mongoose.connect(MONGODB_URI).then((mongoose) => {
      return mongoose;
    });
  }

  cached.conn = await cached.promise;
  return cached.conn;
}
```

### Modèles

```tsx
// models/User.ts
import mongoose from 'mongoose';

const UserSchema = new mongoose.Schema(
  {
    email: { type: String, required: true, unique: true },
    name: { type: String },
    password: { type: String },
  },
  { timestamps: true }
);

export default mongoose.models.User || mongoose.model('User', UserSchema);
```

### Usage

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { connectDB } from '@/lib/mongodb';
import User from '@/models/User';

export async function GET() {
  await connectDB();

  const users = await User.find({}).sort({ createdAt: -1 });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  await connectDB();

  const { email, name } = await request.json();

  const user = await User.create({ email, name });

  return NextResponse.json(user, { status: 201 });
}
```

## Drizzle ORM

### Installation

```bash
npm install drizzle-orm postgres
npm install -D drizzle-kit
```

### Configuration

```tsx
// drizzle.config.ts
import type { Config } from 'drizzle-kit';

export default {
  schema: './lib/schema.ts',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

### Schema

```tsx
// lib/schema.ts
import { pgTable, serial, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: serial('author_id').references(() => users.id),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### Client

```tsx
// lib/db.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client, { schema });
```

### Usage

```tsx
// app/users/page.tsx
import { db } from '@/lib/db';
import { users } from '@/lib/schema';

export default async function UsersPage() {
  const allUsers = await db.select().from(users);

  return (
    <ul>
      {allUsers.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Supabase

### Installation

```bash
npm install @supabase/supabase-js
```

### Configuration

```bash
# .env
NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your-anon-key"
```

### Client

```tsx
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseKey);
```

### Usage

```tsx
// app/users/page.tsx
import { supabase } from '@/lib/supabase';

export default async function UsersPage() {
  const { data: users } = await supabase
    .from('users')
    .select('*')
    .order('created_at', { ascending: false });

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Server Actions avec DB

```tsx
// app/actions/posts.ts
'use server';

import { prisma } from '@/lib/prisma';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await prisma.post.create({
    data: {
      title,
      content,
      authorId: 'user-id', // Get from session
    },
  });

  revalidatePath('/posts');
}

export async function deletePost(id: string) {
  await prisma.post.delete({
    where: { id },
  });

  revalidatePath('/posts');
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '@/app/actions/posts';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input type="text" name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" />
      <button type="submit">Créer</button>
    </form>
  );
}
```

[← Authentification](./infos-nextjs-08-authentication.md) | [Index](./infos-nextjs-00-index.md) | [Optimisation →](./infos-nextjs-10-optimization.md)

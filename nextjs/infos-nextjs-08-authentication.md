# 🔐 Authentification

[← Styling](./infos-nextjs-07-styling.md) | [Index](./infos-nextjs-00-index.md) | [Base de données →](./infos-nextjs-09-database.md)

## NextAuth.js (Auth.js v5)

### Installation

```bash
npm install next-auth@beta
npm install @auth/prisma-adapter
```

### Configuration

```bash
# .env.local
AUTH_SECRET="votre-secret-genere"
AUTH_URL="http://localhost:3000"

# OAuth
GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."
GITHUB_ID="..."
GITHUB_SECRET="..."
```

```bash
# Générer un secret
openssl rand -base64 32
```

### Setup NextAuth

```tsx
// auth.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: {
    strategy: 'jwt',
  },
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });

        if (!user || !user.password) {
          return null;
        }

        const isValid = await bcrypt.compare(
          credentials.password as string,
          user.password
        );

        if (!isValid) {
          return null;
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
        };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
      }
      return session;
    },
  },
  pages: {
    signIn: '/login',
    error: '/error',
  },
});
```

### Route Handler

```tsx
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';

export const { GET, POST } = handlers;
```

### Middleware (Protection routes)

```tsx
// middleware.ts
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isAuthenticated = !!req.auth;
  const isAuthPage = req.nextUrl.pathname.startsWith('/login');

  if (isAuthPage) {
    if (isAuthenticated) {
      return NextResponse.redirect(new URL('/dashboard', req.url));
    }
    return NextResponse.next();
  }

  if (!isAuthenticated && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Page de connexion

```tsx
// app/login/page.tsx
'use client';

import { signIn } from 'next-auth/react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const result = await signIn('credentials', {
      email,
      password,
      redirect: false,
    });

    if (result?.ok) {
      router.push('/dashboard');
    } else {
      alert('Invalid credentials');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8">
        <h1 className="text-2xl font-bold">Connexion</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded border p-2"
          />
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded border p-2"
          />
          <button
            type="submit"
            className="w-full rounded bg-blue-500 p-2 text-white"
          >
            Se connecter
          </button>
        </form>

        <div className="space-y-2">
          <button
            onClick={() => signIn('github', { callbackUrl: '/dashboard' })}
            className="w-full rounded bg-gray-800 p-2 text-white"
          >
            Connexion avec GitHub
          </button>

          <button
            onClick={() => signIn('google', { callbackUrl: '/dashboard' })}
            className="w-full rounded bg-red-500 p-2 text-white"
          >
            Connexion avec Google
          </button>
        </div>
      </div>
    </div>
  );
}
```

### Utiliser la session

```tsx
// app/dashboard/page.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function Dashboard() {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Bienvenue {session.user?.name}</p>
      <p>Email: {session.user?.email}</p>
    </div>
  );
}
```

### Client Component

```tsx
// components/UserProfile.tsx
'use client';

import { useSession, signOut } from 'next-auth/react';

export default function UserProfile() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div>Chargement...</div>;
  }

  if (!session) {
    return <div>Non connecté</div>;
  }

  return (
    <div>
      <p>Connecté en tant que {session.user?.name}</p>
      <button onClick={() => signOut()}>Déconnexion</button>
    </div>
  );
}
```

### Session Provider

```tsx
// app/providers.tsx
'use client';

import { SessionProvider } from 'next-auth/react';

export default function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

```tsx
// app/layout.tsx
import Providers from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## JWT Custom

### Générer token

```tsx
// lib/jwt.ts
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET!;

export function generateToken(payload: any) {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: '7d' });
}

export function verifyToken(token: string) {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
}
```

### API Login

```tsx
// app/api/auth/login/route.ts
import { NextRequest, NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';
import { generateToken } from '@/lib/jwt';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();

    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user || !user.password) {
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      );
    }

    const isValid = await bcrypt.compare(password, user.password);

    if (!isValid) {
      return NextResponse.json(
        { error: 'Invalid credentials' },
        { status: 401 }
      );
    }

    const token = generateToken({ id: user.id, email: user.email });

    const response = NextResponse.json({
      user: { id: user.id, name: user.name, email: user.email },
    });

    response.cookies.set('token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 60 * 60 * 24 * 7, // 7 jours
      path: '/',
    });

    return response;
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

### API Register

```tsx
// app/api/auth/register/route.ts
import { NextRequest, NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
  try {
    const { name, email, password } = await request.json();

    // Validation
    if (!name || !email || !password) {
      return NextResponse.json(
        { error: 'All fields are required' },
        { status: 400 }
      );
    }

    // Vérifier si user existe
    const existingUser = await prisma.user.findUnique({
      where: { email },
    });

    if (existingUser) {
      return NextResponse.json(
        { error: 'User already exists' },
        { status: 400 }
      );
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Créer user
    const user = await prisma.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
      },
    });

    return NextResponse.json(
      { user: { id: user.id, name: user.name, email: user.email } },
      { status: 201 }
    );
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

### Middleware JWT

```tsx
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyToken } from '@/lib/jwt';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  // Pages publiques
  if (request.nextUrl.pathname.startsWith('/login')) {
    if (token && verifyToken(token)) {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
    return NextResponse.next();
  }

  // Pages protégées
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token || !verifyToken(token)) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## Server Actions

```tsx
// app/actions/auth.ts
'use server';

import { signIn, signOut } from '@/auth';
import { AuthError } from 'next-auth';

export async function authenticate(formData: FormData) {
  try {
    await signIn('credentials', {
      email: formData.get('email'),
      password: formData.get('password'),
      redirect: false,
    });
  } catch (error) {
    if (error instanceof AuthError) {
      return { error: 'Invalid credentials' };
    }
    throw error;
  }
}

export async function logout() {
  await signOut({ redirect: false });
}
```

```tsx
// app/login/page.tsx
import { authenticate } from '@/app/actions/auth';
import { redirect } from 'next/navigation';

export default function LoginPage() {
  async function handleLogin(formData: FormData) {
    'use server';

    const result = await authenticate(formData);

    if (!result?.error) {
      redirect('/dashboard');
    }
  }

  return (
    <form action={handleLogin}>
      <input type="email" name="email" required />
      <input type="password" name="password" required />
      <button type="submit">Se connecter</button>
    </form>
  );
}
```

[← Styling](./infos-nextjs-07-styling.md) | [Index](./infos-nextjs-00-index.md) | [Base de données →](./infos-nextjs-09-database.md)

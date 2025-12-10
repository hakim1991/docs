# 🌐 API Routes et Route Handlers

[← Data Fetching](./infos-nextjs-04-data-fetching.md) | [Index](./infos-nextjs-00-index.md) | [Metadata →](./infos-nextjs-06-metadata-seo.md)

## Route Handlers (App Router)

Les Route Handlers remplacent les API Routes dans l'App Router.

### GET Request

```tsx
// app/api/posts/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const posts = [
    { id: 1, title: 'Article 1' },
    { id: 2, title: 'Article 2' },
  ];

  return NextResponse.json(posts);
}
```

### POST Request

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validation
  if (!body.title) {
    return NextResponse.json(
      { error: 'Title is required' },
      { status: 400 }
    );
  }

  // Créer post
  const newPost = {
    id: Date.now(),
    title: body.title,
    content: body.content,
  };

  return NextResponse.json(newPost, { status: 201 });
}
```

### Toutes les méthodes HTTP

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';

// GET /api/posts
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q');

  return NextResponse.json({ query });
}

// POST /api/posts
export async function POST(request: NextRequest) {
  const body = await request.json();
  return NextResponse.json(body, { status: 201 });
}

// PUT /api/posts
export async function PUT(request: NextRequest) {
  const body = await request.json();
  return NextResponse.json(body);
}

// DELETE /api/posts
export async function DELETE(request: NextRequest) {
  return NextResponse.json({ message: 'Deleted' });
}

// PATCH /api/posts
export async function PATCH(request: NextRequest) {
  const body = await request.json();
  return NextResponse.json(body);
}
```

### Routes dynamiques

```tsx
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const post = await getPost(params.id);

  if (!post) {
    return NextResponse.json(
      { error: 'Post not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(post);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await deletePost(params.id);
  return NextResponse.json({ message: 'Post deleted' });
}
```

### Headers et Cookies

```tsx
// app/api/user/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { cookies, headers } from 'next/headers';

export async function GET(request: NextRequest) {
  // Lire headers
  const headersList = headers();
  const authorization = headersList.get('authorization');

  // Lire cookies
  const cookieStore = cookies();
  const token = cookieStore.get('token');

  // Set cookies
  const response = NextResponse.json({ user: 'John' });
  response.cookies.set('session', 'abc123', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    maxAge: 60 * 60 * 24 * 7, // 1 semaine
    path: '/',
  });

  // Set headers
  response.headers.set('X-Custom-Header', 'value');

  return response;
}
```

### CORS

```tsx
// app/api/public/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json(
    { message: 'Public API' },
    {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    }
  );
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
```

## REST API complet

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// GET /api/users
export async function GET(request: NextRequest) {
  try {
    const users = await prisma.user.findMany({
      select: {
        id: true,
        name: true,
        email: true,
      },
    });

    return NextResponse.json(users);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}

// POST /api/users
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validation
    if (!body.email || !body.name) {
      return NextResponse.json(
        { error: 'Email and name are required' },
        { status: 400 }
      );
    }

    const user = await prisma.user.create({
      data: {
        email: body.email,
        name: body.name,
      },
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

```tsx
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// GET /api/users/:id
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const user = await prisma.user.findUnique({
      where: { id: params.id },
    });

    if (!user) {
      return NextResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(user);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}

// PATCH /api/users/:id
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();

    const user = await prisma.user.update({
      where: { id: params.id },
      data: body,
    });

    return NextResponse.json(user);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}

// DELETE /api/users/:id
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    await prisma.user.delete({
      where: { id: params.id },
    });

    return NextResponse.json({ message: 'User deleted' });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

## Middleware d'authentification

```tsx
// lib/auth.ts
import { NextRequest } from 'next/server';
import jwt from 'jsonwebtoken';

export function verifyAuth(request: NextRequest) {
  const token = request.headers.get('authorization')?.split(' ')[1];

  if (!token) {
    return { authenticated: false };
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    return { authenticated: true, user: decoded };
  } catch (error) {
    return { authenticated: false };
  }
}
```

```tsx
// app/api/protected/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';

export async function GET(request: NextRequest) {
  const auth = verifyAuth(request);

  if (!auth.authenticated) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  return NextResponse.json({ message: 'Protected data', user: auth.user });
}
```

## Upload de fichiers

```tsx
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { writeFile } from 'fs/promises';
import { join } from 'path';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      );
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);

    // Sauvegarder le fichier
    const path = join(process.cwd(), 'public', 'uploads', file.name);
    await writeFile(path, buffer);

    return NextResponse.json({
      message: 'File uploaded successfully',
      filename: file.name,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Upload failed' },
      { status: 500 }
    );
  }
}
```

## Webhooks

```tsx
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature')!;

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    // Traiter l'événement
    switch (event.type) {
      case 'payment_intent.succeeded':
        const paymentIntent = event.data.object;
        console.log('PaymentIntent succeeded:', paymentIntent.id);
        break;

      case 'customer.subscription.created':
        const subscription = event.data.object;
        console.log('Subscription created:', subscription.id);
        break;

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Webhook signature verification failed' },
      { status: 400 }
    );
  }
}
```

## Streaming Response

```tsx
// app/api/stream/route.ts
import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        const message = `Data chunk ${i}\n`;
        controller.enqueue(encoder.encode(message));
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  });
}
```

## Route Segment Config

```tsx
// app/api/data/route.ts

// Force dynamic
export const dynamic = 'force-dynamic';

// Runtime Edge
export const runtime = 'edge';

// Max duration (Vercel)
export const maxDuration = 5;

export async function GET() {
  return NextResponse.json({ data: 'value' });
}
```

[← Data Fetching](./infos-nextjs-04-data-fetching.md) | [Index](./infos-nextjs-00-index.md) | [Metadata →](./infos-nextjs-06-metadata-seo.md)

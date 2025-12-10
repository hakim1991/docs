# 🔄 Data Fetching (SSR, SSG, ISR)

[← Server Components](./infos-nextjs-03-server-client-components.md) | [Index](./infos-nextjs-00-index.md) | [API Routes →](./infos-nextjs-05-api-routes.md)

## Server Components (async/await)

Dans Next.js 13+, fetch directement dans les Server Components.

```tsx
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');

  if (!res.ok) {
    throw new Error('Failed to fetch posts');
  }

  return res.json();
}

export default async function Posts() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Articles</h1>
      <ul>
        {posts.map((post: any) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## SSR (Server-Side Rendering)

Par défaut, `fetch` utilise SSR (données fraîches à chaque requête).

```tsx
// app/dashboard/page.tsx
async function getStats() {
  // Force SSR (no cache)
  const res = await fetch('https://api.example.com/stats', {
    cache: 'no-store',
  });

  return res.json();
}

export default async function Dashboard() {
  const stats = await getStats();

  return (
    <div>
      <h1>Statistiques</h1>
      <p>Visiteurs: {stats.visitors}</p>
    </div>
  );
}
```

## SSG (Static Site Generation)

Générer la page au build time.

```tsx
// app/blog/[slug]/page.tsx
async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    cache: 'force-cache', // SSG (défaut)
  });

  return res.json();
}

export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// Générer les routes statiques au build
export async function generateStaticParams() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();

  return posts.map((post: any) => ({
    slug: post.slug,
  }));
}
```

## ISR (Incremental Static Regeneration)

Régénérer la page après un certain temps.

```tsx
// app/products/page.tsx
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 }, // Revalider toutes les 60 secondes
  });

  return res.json();
}

export default async function Products() {
  const products = await getProducts();

  return (
    <div>
      <h1>Produits</h1>
      <ul>
        {products.map((product: any) => (
          <li key={product.id}>{product.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Revalidation on-demand

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

export async function revalidateProducts() {
  // Revalider un path
  revalidatePath('/products');

  // Revalider un tag
  revalidateTag('products');
}
```

```tsx
// Utiliser un tag
async function getProducts() {
  const res = await fetch('https://api.example.com/products', {
    next: { tags: ['products'] },
  });

  return res.json();
}
```

## Streaming avec Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function Analytics() {
  const data = await fetch('https://api.example.com/analytics');
  const analytics = await data.json();

  return <div>Analytics: {analytics.views}</div>;
}

async function Stats() {
  const data = await fetch('https://api.example.com/stats');
  const stats = await data.json();

  return <div>Stats: {stats.users}</div>;
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Les composants se chargent indépendamment */}
      <Suspense fallback={<div>Loading analytics...</div>}>
        <Analytics />
      </Suspense>

      <Suspense fallback={<div>Loading stats...</div>}>
        <Stats />
      </Suspense>
    </div>
  );
}
```

## Parallel Data Fetching

```tsx
// app/user/[id]/page.tsx
async function getUser(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}`);
  return res.json();
}

async function getUserPosts(id: string) {
  const res = await fetch(`https://api.example.com/users/${id}/posts`);
  return res.json();
}

export default async function UserProfile({ params }: { params: { id: string } }) {
  // Fetch en parallèle
  const [user, posts] = await Promise.all([
    getUser(params.id),
    getUserPosts(params.id),
  ]);

  return (
    <div>
      <h1>{user.name}</h1>
      <h2>Posts</h2>
      <ul>
        {posts.map((post: any) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Sequential Data Fetching

```tsx
// app/artist/[id]/page.tsx
async function getArtist(id: string) {
  const res = await fetch(`https://api.example.com/artists/${id}`);
  return res.json();
}

async function getAlbums(artistId: string) {
  const res = await fetch(`https://api.example.com/albums?artist=${artistId}`);
  return res.json();
}

export default async function ArtistPage({ params }: { params: { id: string } }) {
  // Fetch séquentiel (albums dépend de artist)
  const artist = await getArtist(params.id);
  const albums = await getAlbums(artist.id);

  return (
    <div>
      <h1>{artist.name}</h1>
      <ul>
        {albums.map((album: any) => (
          <li key={album.id}>{album.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Accès direct à la DB

```tsx
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

```tsx
// app/users/page.tsx
import { prisma } from '@/lib/prisma';

export default async function Users() {
  const users = await prisma.user.findMany({
    include: {
      posts: true,
    },
  });

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          {user.name} - {user.posts.length} posts
        </li>
      ))}
    </ul>
  );
}
```

## Error Handling

```tsx
// app/posts/page.tsx
async function getPosts() {
  try {
    const res = await fetch('https://api.example.com/posts');

    if (!res.ok) {
      throw new Error('Failed to fetch posts');
    }

    return res.json();
  } catch (error) {
    console.error('Error fetching posts:', error);
    throw error; // Propagé à error.tsx
  }
}

export default async function Posts() {
  const posts = await getPosts();

  return (
    <ul>
      {posts.map((post: any) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

```tsx
// app/posts/error.tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Erreur lors du chargement des articles</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Réessayer</button>
    </div>
  );
}
```

## Loading States

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="spinner">Chargement des articles...</div>
    </div>
  );
}
```

## Cache Configuration

```tsx
// Différentes stratégies de cache

// 1. Force cache (SSG)
fetch(url, { cache: 'force-cache' });

// 2. No store (SSR)
fetch(url, { cache: 'no-store' });

// 3. Revalidate (ISR)
fetch(url, { next: { revalidate: 60 } });

// 4. Tags (on-demand revalidation)
fetch(url, { next: { tags: ['posts'] } });
```

## Route Segment Config

```tsx
// app/dashboard/page.tsx

// Force dynamic rendering
export const dynamic = 'force-dynamic';

// Revalidate toutes les 60 secondes
export const revalidate = 60;

// Force static rendering
export const dynamic = 'force-static';

// Runtime Edge
export const runtime = 'edge';

export default function Dashboard() {
  return <div>Dashboard</div>;
}
```

## Bonnes pratiques

1. **SSG par défaut** : utiliser pour les pages statiques
2. **ISR pour contenu semi-dynamique** : blog, produits
3. **SSR pour données temps réel** : dashboard, profil
4. **Streaming avec Suspense** : améliorer UX
5. **Parallel fetching** : quand les données sont indépendantes
6. **Tags pour revalidation** : revalider plusieurs routes

[← Server Components](./infos-nextjs-03-server-client-components.md) | [Index](./infos-nextjs-00-index.md) | [API Routes →](./infos-nextjs-05-api-routes.md)

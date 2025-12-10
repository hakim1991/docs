# 🛣️ Routing et Navigation

[← Introduction](./infos-nextjs-01-introduction-installation.md) | [Index](./infos-nextjs-00-index.md) | [Server Components →](./infos-nextjs-03-server-client-components.md)

## File-based Routing

### Routes statiques

```
app/
├── page.tsx              # /
├── about/
│   └── page.tsx          # /about
└── blog/
    └── page.tsx          # /blog
```

```tsx
// app/about/page.tsx
export default function About() {
  return <h1>À propos</h1>;
}
```

### Routes dynamiques

```
app/
└── blog/
    └── [slug]/
        └── page.tsx      # /blog/:slug
```

```tsx
// app/blog/[slug]/page.tsx
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <h1>Article: {params.slug}</h1>;
}

// Générer les routes statiques
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(res => res.json());

  return posts.map((post: any) => ({
    slug: post.slug,
  }));
}
```

### Routes imbriquées

```
app/
└── dashboard/
    ├── layout.tsx        # Layout pour /dashboard/*
    ├── page.tsx          # /dashboard
    ├── settings/
    │   └── page.tsx      # /dashboard/settings
    └── profile/
        └── page.tsx      # /dashboard/profile
```

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex">
      <aside className="w-64 bg-gray-100">
        <nav>
          <a href="/dashboard">Dashboard</a>
          <a href="/dashboard/settings">Settings</a>
          <a href="/dashboard/profile">Profile</a>
        </nav>
      </aside>
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
```

### Catch-all routes

```
app/
└── shop/
    └── [...slug]/
        └── page.tsx      # /shop/*, /shop/a/b/c
```

```tsx
// app/shop/[...slug]/page.tsx
export default function Shop({ params }: { params: { slug: string[] } }) {
  return (
    <div>
      <h1>Boutique</h1>
      <p>Segments: {params.slug.join(' / ')}</p>
    </div>
  );
}
```

### Optional catch-all

```
app/
└── docs/
    └── [[...slug]]/
        └── page.tsx      # /docs ET /docs/a/b/c
```

## Navigation

### Link Component

```tsx
import Link from 'next/link';

export default function Nav() {
  return (
    <nav>
      <Link href="/">Accueil</Link>
      <Link href="/about">À propos</Link>
      <Link href="/blog">Blog</Link>

      {/* Avec paramètres */}
      <Link href="/blog/mon-article">Article</Link>

      {/* Avec query string */}
      <Link href="/search?q=nextjs">Recherche</Link>

      {/* Avec objet */}
      <Link
        href={{
          pathname: '/blog/[slug]',
          query: { slug: 'mon-article' },
        }}
      >
        Article
      </Link>

      {/* Scroll vers ancre */}
      <Link href="/docs#installation">Installation</Link>

      {/* Replace (ne pas ajouter à l'historique) */}
      <Link href="/login" replace>
        Login
      </Link>

      {/* Prefetch disabled */}
      <Link href="/slow-page" prefetch={false}>
        Page lente
      </Link>
    </nav>
  );
}
```

### useRouter (Client Component)

```tsx
'use client';

import { useRouter, usePathname, useSearchParams } from 'next/navigation';

export default function Navigation() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const handleClick = () => {
    // Naviguer
    router.push('/about');

    // Avec query
    router.push('/search?q=nextjs');

    // Remplacer (sans historique)
    router.replace('/login');

    // Retour
    router.back();

    // Avancer
    router.forward();

    // Rafraîchir
    router.refresh();
  };

  // Lire pathname
  console.log('Current path:', pathname); // /blog/mon-article

  // Lire query params
  const query = searchParams.get('q'); // nextjs

  return <button onClick={handleClick}>Navigate</button>;
}
```

### Redirect

```tsx
// Server Component
import { redirect } from 'next/navigation';

export default function Profile() {
  const session = await getSession();

  if (!session) {
    redirect('/login');
  }

  return <div>Profile</div>;
}
```

### Route Groups

```
app/
├── (marketing)/
│   ├── about/
│   │   └── page.tsx      # /about (pas /(marketing)/about)
│   └── blog/
│       └── page.tsx      # /blog
└── (shop)/
    ├── products/
    │   └── page.tsx      # /products
    └── cart/
        └── page.tsx      # /cart
```

Les parenthèses `()` créent un groupe sans affecter l'URL.

### Parallel Routes

```
app/
└── dashboard/
    ├── @analytics/
    │   └── page.tsx
    ├── @team/
    │   └── page.tsx
    └── layout.tsx
```

```tsx
// app/dashboard/layout.tsx
export default function Layout({
  children,
  analytics,
  team,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div>
      {children}
      <div className="grid grid-cols-2 gap-4">
        {analytics}
        {team}
      </div>
    </div>
  );
}
```

### Intercepting Routes

```
app/
├── photos/
│   ├── page.tsx          # /photos
│   └── [id]/
│       └── page.tsx      # /photos/123
└── @modal/
    └── (..)photos/
        └── [id]/
            └── page.tsx  # Intercepte /photos/123
```

## Loading UI

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="spinner">Chargement...</div>
    </div>
  );
}
```

## Error Handling

```tsx
// app/dashboard/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Erreur : {error.message}</h2>
      <button onClick={() => reset()}>Réessayer</button>
    </div>
  );
}
```

## Not Found

```tsx
// app/dashboard/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>404 - Page non trouvée</h2>
      <a href="/dashboard">Retour au dashboard</a>
    </div>
  );
}
```

[← Introduction](./infos-nextjs-01-introduction-installation.md) | [Index](./infos-nextjs-00-index.md) | [Server Components →](./infos-nextjs-03-server-client-components.md)

# ⚡ Optimisation

[← Base de données](./infos-nextjs-09-database.md) | [Index](./infos-nextjs-00-index.md) | [Testing →](./infos-nextjs-11-testing.md)

## Images (next/image)

### Usage basique

```tsx
import Image from 'next/image';

export default function Page() {
  return (
    <Image
      src="/photo.jpg"
      alt="Description"
      width={800}
      height={600}
      priority // Pour images above-the-fold
    />
  );
}
```

### Images externes

```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['example.com', 'cdn.example.com'],
    // Ou avec remotePatterns (recommandé)
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },
};
```

```tsx
<Image
  src="https://example.com/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
/>
```

### Responsive

```tsx
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

### Fill container

```tsx
<div className="relative h-64 w-full">
  <Image
    src="/photo.jpg"
    alt="Photo"
    fill
    style={{ objectFit: 'cover' }}
  />
</div>
```

### Placeholder

```tsx
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..." // Généré avec plaiceholder
/>
```

## Fonts (next/font)

### Google Fonts

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-roboto-mono',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

### Local Fonts

```tsx
import localFont from 'next/font/local';

const myFont = localFont({
  src: [
    {
      path: '../public/fonts/font-regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/font-bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-my-font',
});
```

## Script Optimization

```tsx
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        {children}

        {/* Charger après interactivité (défaut) */}
        <Script src="https://example.com/script.js" />

        {/* Charger avant interactivité */}
        <Script
          src="https://example.com/script.js"
          strategy="beforeInteractive"
        />

        {/* Charger après chargement de la page */}
        <Script
          src="https://example.com/script.js"
          strategy="afterInteractive"
        />

        {/* Lazy load */}
        <Script
          src="https://example.com/script.js"
          strategy="lazyOnload"
        />

        {/* Inline script */}
        <Script id="analytics">
          {`
            window.analytics = window.analytics || [];
          `}
        </Script>
      </body>
    </html>
  );
}
```

## Code Splitting

### Dynamic Import

```tsx
// app/page.tsx
import dynamic from 'next/dynamic';

// Sans SSR
const HeavyComponent = dynamic(() => import('@/components/HeavyComponent'), {
  ssr: false,
  loading: () => <p>Loading...</p>,
});

export default function Home() {
  return (
    <div>
      <h1>Page</h1>
      <HeavyComponent />
    </div>
  );
}
```

### Lazy Loading avec Suspense

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('@/components/HeavyComponent'));

export default function Home() {
  return (
    <div>
      <h1>Page</h1>
      <Suspense fallback={<p>Loading...</p>}>
        <HeavyComponent />
      </Suspense>
    </div>
  );
}
```

## Bundle Analysis

```bash
npm install @next/bundle-analyzer
```

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // votre config
});
```

```json
// package.json
{
  "scripts": {
    "analyze": "ANALYZE=true npm run build"
  }
}
```

## Caching

### fetch() caching

```tsx
// Force cache (SSG)
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache',
});

// No cache (SSR)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});

// Revalidate (ISR)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }, // 60 secondes
});

// Tags
const data = await fetch('https://api.example.com/data', {
  next: { tags: ['products'] },
});
```

### Revalidation

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

export async function revalidateProducts() {
  revalidatePath('/products');
  revalidateTag('products');
}
```

### Route Segment Config

```tsx
// app/page.tsx

// Force dynamic
export const dynamic = 'force-dynamic';

// Force static
export const dynamic = 'force-static';

// Revalidate
export const revalidate = 60;

// Runtime
export const runtime = 'edge'; // ou 'nodejs'

export default function Page() {
  return <div>Page</div>;
}
```

## React Optimization

### memo

```tsx
import { memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  // Ne re-render que si data change
  return <div>{data}</div>;
});
```

### useMemo

```tsx
'use client';

import { useMemo } from 'react';

export default function Component({ items }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);

  return <ul>{sortedItems.map((item) => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

### useCallback

```tsx
'use client';

import { useCallback } from 'react';

export default function Parent() {
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);

  return <Child onClick={handleClick} />;
}
```

## Loading States

### Streaming avec Suspense

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';

async function Analytics() {
  const data = await fetch('https://api.example.com/analytics');
  return <div>Analytics</div>;
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading analytics...</div>}>
        <Analytics />
      </Suspense>
    </div>
  );
}
```

### Loading.tsx

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="flex h-screen items-center justify-center">
      <div className="spinner">Loading...</div>
    </div>
  );
}
```

## Prefetching

```tsx
// Prefetch automatique avec Link
import Link from 'next/link';

<Link href="/about" prefetch={true}>
  About
</Link>

// Désactiver prefetch
<Link href="/about" prefetch={false}>
  About
</Link>
```

## Edge Runtime

```tsx
// app/api/hello/route.ts
export const runtime = 'edge';

export async function GET() {
  return new Response('Hello from Edge!');
}
```

## Compression

```javascript
// next.config.js
module.exports = {
  compress: true, // Activé par défaut
};
```

## Build Output

```javascript
// next.config.js
module.exports = {
  output: 'standalone', // Pour Docker
  // output: 'export', // Pour static export
};
```

## Environment Variables

```bash
# .env.local (development)
DATABASE_URL="..."
NEXT_PUBLIC_API_URL="..."

# .env.production (production)
DATABASE_URL="..."
NEXT_PUBLIC_API_URL="..."
```

## Performance Monitoring

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights /> {/* Vercel */}
      </body>
    </html>
  );
}
```

## Webpack Config

```javascript
// next.config.js
module.exports = {
  webpack: (config, { dev, isServer }) => {
    // Custom webpack config
    return config;
  },
};
```

## Turbopack (Beta)

```json
// package.json
{
  "scripts": {
    "dev": "next dev --turbo"
  }
}
```

## Bonnes pratiques

1. **Utiliser next/image** : optimisation automatique
2. **Code splitting** : lazy load composants lourds
3. **Server Components par défaut** : moins de JavaScript client
4. **ISR pour contenu semi-statique** : meilleure performance
5. **Edge Runtime** : latence minimale
6. **Streaming avec Suspense** : meilleure UX
7. **Bundle analysis régulière** : identifier le bloat
8. **Prefetch intelligent** : routes importantes uniquement

[← Base de données](./infos-nextjs-09-database.md) | [Index](./infos-nextjs-00-index.md) | [Testing →](./infos-nextjs-11-testing.md)

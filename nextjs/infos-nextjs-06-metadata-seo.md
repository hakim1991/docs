# 🔍 Metadata et SEO

[← API Routes](./infos-nextjs-05-api-routes.md) | [Index](./infos-nextjs-00-index.md) | [Styling →](./infos-nextjs-07-styling.md)

## Metadata statique

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Mon Application',
  description: 'Description de mon application',
  keywords: ['Next.js', 'React', 'TypeScript'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
```

## Metadata dynamique

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

type Props = {
  params: { slug: string };
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  // Fetch post data
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(res =>
    res.json()
  );

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  };
}

export default function BlogPost({ params }: Props) {
  return <article>...</article>;
}
```

## Template de titre

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    template: '%s | Mon Site',
    default: 'Mon Site',
  },
};
```

```tsx
// app/blog/page.tsx
export const metadata: Metadata = {
  title: 'Blog', // Devient "Blog | Mon Site"
};
```

## Open Graph

```tsx
// app/products/[id]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.id);

  return {
    title: product.name,
    description: product.description,
    openGraph: {
      title: product.name,
      description: product.description,
      url: `https://example.com/products/${params.id}`,
      siteName: 'Mon E-commerce',
      images: [
        {
          url: product.image,
          width: 1200,
          height: 630,
          alt: product.name,
        },
      ],
      locale: 'fr_FR',
      type: 'website',
    },
  };
}
```

## Twitter Cards

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      creator: '@username',
      images: [post.image],
    },
  };
}
```

## Robots

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};
```

## Verification

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  verification: {
    google: 'google-site-verification-code',
    yandex: 'yandex-verification-code',
  },
};
```

## Canonical URL

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  return {
    alternates: {
      canonical: `https://example.com/blog/${params.slug}`,
    },
  };
}
```

## Langues alternatives

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  alternates: {
    languages: {
      'en-US': 'https://example.com/en',
      'fr-FR': 'https://example.com/fr',
      'es-ES': 'https://example.com/es',
    },
  },
};
```

## Manifest PWA

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  manifest: '/manifest.json',
};
```

```json
// public/manifest.json
{
  "name": "Mon Application",
  "short_name": "App",
  "description": "Description de mon application",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## Favicon

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-icon.png',
    shortcut: '/shortcut-icon.png',
  },
};
```

Ou utiliser les conventions de fichiers :
- `app/favicon.ico`
- `app/icon.png`
- `app/apple-icon.png`

## Sitemap

```tsx
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetch('https://api.example.com/posts').then(res => res.json());

  const postEntries: MetadataRoute.Sitemap = posts.map((post: any) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'weekly',
    priority: 0.8,
  }));

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    ...postEntries,
  ];
}
```

## Robots.txt

```tsx
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: '/private/',
    },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

## JSON-LD Structured Data

```tsx
// app/products/[id]/page.tsx
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'EUR',
      availability: 'https://schema.org/InStock',
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
        <p>{product.price} €</p>
      </div>
    </>
  );
}
```

## Article Schema

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.image,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>
        <h1>{post.title}</h1>
        <div dangerouslySetInnerHTML={{ __html: post.content }} />
      </article>
    </>
  );
}
```

## Viewport

```tsx
// app/layout.tsx
import type { Viewport } from 'next';

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  themeColor: '#000000',
};
```

## Metadata complet

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | Mon Site',
    default: 'Mon Site - Bienvenue',
  },
  description: 'Description complète de mon site',
  keywords: ['Next.js', 'React', 'TypeScript', 'SEO'],
  authors: [{ name: 'John Doe', url: 'https://johndoe.com' }],
  creator: 'John Doe',
  publisher: 'Mon Entreprise',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-icon.png',
  },
  metadataBase: new URL('https://example.com'),
  alternates: {
    canonical: '/',
    languages: {
      'en-US': '/en',
      'fr-FR': '/fr',
    },
  },
  openGraph: {
    title: 'Mon Site',
    description: 'Description pour les réseaux sociaux',
    url: 'https://example.com',
    siteName: 'Mon Site',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Mon Site',
      },
    ],
    locale: 'fr_FR',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Mon Site',
    description: 'Description pour Twitter',
    creator: '@username',
    images: ['/twitter-image.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
  verification: {
    google: 'google-verification-code',
  },
};
```

[← API Routes](./infos-nextjs-05-api-routes.md) | [Index](./infos-nextjs-00-index.md) | [Styling →](./infos-nextjs-07-styling.md)

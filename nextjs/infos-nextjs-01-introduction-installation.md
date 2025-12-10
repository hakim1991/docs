# 🚀 Introduction et Installation

[Index](./infos-nextjs-00-index.md) | [Routing →](./infos-nextjs-02-routing-navigation.md)

## Qu'est-ce que Next.js ?

Next.js est un framework React qui permet :
- **SSR** (Server-Side Rendering) : génération côté serveur
- **SSG** (Static Site Generation) : génération statique
- **ISR** (Incremental Static Regeneration) : régénération incrémentale
- **Routing basé sur les fichiers** : structure simple
- **API Routes** : backend intégré
- **Optimisation automatique** : images, fonts, scripts

## Installation

### Créer un nouveau projet

```bash
# Avec npm
npx create-next-app@latest my-app

# Avec pnpm
pnpm create next-app my-app

# Avec yarn
yarn create next-app my-app
```

### Options d'installation

```bash
npx create-next-app@latest my-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
```

### Démarrer le projet

```bash
cd my-app
npm run dev

# Ouvre http://localhost:3000
```

## Structure du projet (App Router)

```
my-app/
├── app/                    # Routes de l'application
│   ├── layout.tsx         # Layout racine
│   ├── page.tsx           # Page d'accueil
│   ├── globals.css        # CSS global
│   └── api/               # API Routes
├── public/                # Fichiers statiques
├── components/            # Composants réutilisables
├── lib/                   # Utilitaires
├── next.config.js         # Config Next.js
├── package.json
└── tsconfig.json
```

## App Router vs Pages Router

### App Router (Recommandé - Next.js 13+)

```
app/
├── layout.tsx            # Layout partagé
├── page.tsx              # Route: /
├── about/
│   └── page.tsx          # Route: /about
└── blog/
    ├── page.tsx          # Route: /blog
    └── [slug]/
        └── page.tsx      # Route: /blog/:slug
```

### Pages Router (Legacy)

```
pages/
├── _app.tsx              # App wrapper
├── index.tsx             # Route: /
├── about.tsx             # Route: /about
└── blog/
    ├── index.tsx         # Route: /blog
    └── [slug].tsx        # Route: /blog/:slug
```

## Premier composant

```tsx
// app/page.tsx
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">Bienvenue sur Next.js</h1>
      <p className="mt-4 text-lg">Framework React pour la production</p>
    </main>
  );
}
```

## Layout racine

```tsx
// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Mon Application Next.js',
  description: 'Créée avec Next.js 14',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

## Configuration Next.js

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['example.com'],
  },
  env: {
    CUSTOM_KEY: 'value',
  },
};

module.exports = nextConfig;
```

## Scripts package.json

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

## Variables d'environnement

```bash
# .env.local (ne pas commit)
DATABASE_URL="postgresql://..."
NEXT_PUBLIC_API_URL="https://api.example.com"
SECRET_KEY="secret"
```

```tsx
// Côté serveur uniquement
const dbUrl = process.env.DATABASE_URL;

// Accessible client ET serveur (préfixe NEXT_PUBLIC_)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

[Index](./infos-nextjs-00-index.md) | [Routing →](./infos-nextjs-02-routing-navigation.md)

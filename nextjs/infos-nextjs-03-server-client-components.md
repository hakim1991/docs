# ⚙️ Server Components et Client Components

[← Routing](./infos-nextjs-02-routing-navigation.md) | [Index](./infos-nextjs-00-index.md) | [Data Fetching →](./infos-nextjs-04-data-fetching.md)

## Server Components (par défaut)

Par défaut, tous les composants dans `app/` sont des **Server Components**.

### Avantages

- ✅ Accès direct aux ressources backend (DB, API)
- ✅ Bundle JavaScript plus petit (pas envoyé au client)
- ✅ Meilleure sécurité (secrets côté serveur)
- ✅ Meilleur SEO (HTML généré)
- ✅ Streaming et Suspense

### Exemple

```tsx
// app/posts/page.tsx (Server Component par défaut)
async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
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

### Ce qu'on peut faire

```tsx
// ✅ Async/await
async function ServerComponent() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// ✅ Accès direct à la DB
import { prisma } from '@/lib/prisma';

async function Users() {
  const users = await prisma.user.findMany();
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// ✅ Utiliser des secrets
async function getData() {
  const data = await fetch('https://api.example.com', {
    headers: {
      Authorization: `Bearer ${process.env.API_SECRET}`, // Safe côté serveur
    },
  });
  return data.json();
}
```

### Ce qu'on ne peut PAS faire

```tsx
// ❌ Hooks React (useState, useEffect, etc.)
function ServerComponent() {
  const [count, setCount] = useState(0); // ❌ Erreur
  return <div>{count}</div>;
}

// ❌ Event handlers
function ServerComponent() {
  const handleClick = () => console.log('click'); // ❌ Erreur
  return <button onClick={handleClick}>Click</button>;
}

// ❌ Browser APIs
function ServerComponent() {
  const width = window.innerWidth; // ❌ Erreur (window n'existe pas)
  return <div>{width}</div>;
}
```

## Client Components

Pour utiliser interactivité, hooks, ou browser APIs, ajouter `'use client'`.

### Déclaration

```tsx
// components/Counter.tsx
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

### Quand utiliser 'use client'

- ✅ useState, useEffect, useContext, etc.
- ✅ Event handlers (onClick, onChange, etc.)
- ✅ Browser APIs (window, localStorage, etc.)
- ✅ Bibliothèques qui utilisent des hooks
- ✅ Interactivité utilisateur

### Exemple complet

```tsx
'use client';

import { useState, useEffect } from 'react';

export default function Theme() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Accès à localStorage (browser API)
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  };

  return (
    <button onClick={toggleTheme}>
      Theme: {theme}
    </button>
  );
}
```

## Composition Server + Client

### Pattern recommandé

```tsx
// app/page.tsx (Server Component)
import Counter from '@/components/Counter'; // Client Component

async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  return res.json();
}

export default async function Home() {
  const posts = await getPosts();

  return (
    <div>
      {/* Données chargées côté serveur */}
      <h1>Articles ({posts.length})</h1>

      {/* Interactivité côté client */}
      <Counter />

      <ul>
        {posts.map((post: any) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Passer des données Server → Client

```tsx
// app/page.tsx (Server Component)
import PostList from '@/components/PostList';

async function getPosts() {
  const res = await fetch('https://api.example.com/posts');
  return res.json();
}

export default async function Home() {
  const posts = await getPosts();

  // Passer les données au Client Component via props
  return <PostList posts={posts} />;
}
```

```tsx
// components/PostList.tsx (Client Component)
'use client';

import { useState } from 'react';

export default function PostList({ posts }: { posts: any[] }) {
  const [filter, setFilter] = useState('');

  const filteredPosts = posts.filter(post =>
    post.title.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filtrer..."
      />

      <ul>
        {filteredPosts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Children pattern

```tsx
// app/layout.tsx (Server Component)
import Sidebar from '@/components/Sidebar'; // Client Component

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex">
      {/* Client Component avec Server Component children */}
      <Sidebar>
        {children} {/* children est un Server Component */}
      </Sidebar>
    </div>
  );
}
```

```tsx
// components/Sidebar.tsx (Client Component)
'use client';

import { useState } from 'react';

export default function Sidebar({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(true);

  return (
    <div className="flex">
      <aside className={open ? 'w-64' : 'w-0'}>
        <button onClick={() => setOpen(!open)}>Toggle</button>
        <nav>...</nav>
      </aside>

      <main className="flex-1">
        {children} {/* Server Component rendu ici */}
      </main>
    </div>
  );
}
```

## Context Providers

Les Context Providers doivent être des Client Components.

```tsx
// app/providers.tsx
'use client';

import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext<any>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

```tsx
// app/layout.tsx (Server Component)
import { ThemeProvider } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

## Third-party libraries

Si une bibliothèque utilise des hooks, créer un wrapper Client Component.

```tsx
// components/ChartWrapper.tsx
'use client';

import { Chart } from 'third-party-chart-library';

export default function ChartWrapper({ data }: { data: any }) {
  return <Chart data={data} />;
}
```

```tsx
// app/dashboard/page.tsx (Server Component)
import ChartWrapper from '@/components/ChartWrapper';

async function getChartData() {
  const res = await fetch('https://api.example.com/stats');
  return res.json();
}

export default async function Dashboard() {
  const data = await getChartData();

  return (
    <div>
      <h1>Dashboard</h1>
      <ChartWrapper data={data} />
    </div>
  );
}
```

## Bonnes pratiques

1. **Par défaut, utiliser Server Components** : meilleure performance
2. **'use client' au plus bas niveau possible** : minimiser le JavaScript client
3. **Passer les données via props** : Server → Client
4. **Children pattern pour composition** : Client Component avec Server children
5. **Wrapper pour bibliothèques tierces** : isoler 'use client'

[← Routing](./infos-nextjs-02-routing-navigation.md) | [Index](./infos-nextjs-00-index.md) | [Data Fetching →](./infos-nextjs-04-data-fetching.md)

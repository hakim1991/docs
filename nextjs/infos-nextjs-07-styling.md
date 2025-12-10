# 🎨 Styling

[← Metadata](./infos-nextjs-06-metadata-seo.md) | [Index](./infos-nextjs-00-index.md) | [Authentification →](./infos-nextjs-08-authentication.md)

## Tailwind CSS (Recommandé)

### Installation

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Configuration

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#10b981',
      },
    },
  },
  plugins: [],
};
```

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
  }
}
```

### Usage

```tsx
// app/page.tsx
export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold text-blue-600">Next.js + Tailwind</h1>
      <button className="btn-primary mt-4">Click me</button>
    </div>
  );
}
```

### Dark Mode

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // ou 'media'
  // ...
};
```

```tsx
// app/page.tsx
export default function Home() {
  return (
    <div className="bg-white dark:bg-gray-900">
      <h1 className="text-gray-900 dark:text-white">Hello</h1>
    </div>
  );
}
```

```tsx
// components/ThemeToggle.tsx
'use client';

import { useEffect, useState } from 'react';

export default function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const theme = localStorage.getItem('theme');
    setIsDark(theme === 'dark');
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, []);

  const toggleTheme = () => {
    const newTheme = isDark ? 'light' : 'dark';
    setIsDark(!isDark);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', !isDark);
  };

  return (
    <button onClick={toggleTheme}>
      {isDark ? '🌞' : '🌙'}
    </button>
  );
}
```

## CSS Modules

```css
/* app/components/Button.module.css */
.button {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

.primary {
  background-color: #3b82f6;
  color: white;
}

.primary:hover {
  background-color: #2563eb;
}

.secondary {
  background-color: #10b981;
  color: white;
}
```

```tsx
// components/Button.tsx
import styles from './Button.module.css';

export default function Button({
  children,
  variant = 'primary',
}: {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

## Styled Components

### Installation

```bash
npm install styled-components
npm install -D @types/styled-components
```

### Configuration

```tsx
// lib/registry.tsx
'use client';

import React, { useState } from 'react';
import { useServerInsertedHTML } from 'next/navigation';
import { ServerStyleSheet, StyleSheetManager } from 'styled-components';

export default function StyledComponentsRegistry({
  children,
}: {
  children: React.ReactNode;
}) {
  const [styledComponentsStyleSheet] = useState(() => new ServerStyleSheet());

  useServerInsertedHTML(() => {
    const styles = styledComponentsStyleSheet.getStyleElement();
    styledComponentsStyleSheet.instance.clearTag();
    return <>{styles}</>;
  });

  if (typeof window !== 'undefined') return <>{children}</>;

  return (
    <StyleSheetManager sheet={styledComponentsStyleSheet.instance}>
      {children}
    </StyleSheetManager>
  );
}
```

```tsx
// app/layout.tsx
import StyledComponentsRegistry from '@/lib/registry';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <StyledComponentsRegistry>{children}</StyledComponentsRegistry>
      </body>
    </html>
  );
}
```

### Usage

```tsx
// components/Button.tsx
'use client';

import styled from 'styled-components';

const StyledButton = styled.button<{ $variant?: 'primary' | 'secondary' }>`
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  border: none;

  background-color: ${(props) =>
    props.$variant === 'secondary' ? '#10b981' : '#3b82f6'};
  color: white;

  &:hover {
    background-color: ${(props) =>
      props.$variant === 'secondary' ? '#059669' : '#2563eb'};
  }
`;

export default function Button({
  children,
  variant,
}: {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}) {
  return <StyledButton $variant={variant}>{children}</StyledButton>;
}
```

## CSS-in-JS (Emotion)

### Installation

```bash
npm install @emotion/react @emotion/styled
```

### Usage

```tsx
// components/Button.tsx
'use client';

import styled from '@emotion/styled';

const Button = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  border: none;
  background-color: ${(props) =>
    props.variant === 'secondary' ? '#10b981' : '#3b82f6'};
  color: white;

  &:hover {
    background-color: ${(props) =>
      props.variant === 'secondary' ? '#059669' : '#2563eb'};
  }
`;

export default Button;
```

## Sass/SCSS

### Installation

```bash
npm install -D sass
```

### Usage

```scss
// app/components/Button.module.scss
$primary-color: #3b82f6;
$secondary-color: #10b981;

.button {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;

  &.primary {
    background-color: $primary-color;
    color: white;

    &:hover {
      background-color: darken($primary-color, 10%);
    }
  }

  &.secondary {
    background-color: $secondary-color;
    color: white;

    &:hover {
      background-color: darken($secondary-color, 10%);
    }
  }
}
```

```tsx
// components/Button.tsx
import styles from './Button.module.scss';

export default function Button({ children, variant = 'primary' }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

## Global CSS

```css
/* app/globals.css */
:root {
  --primary-color: #3b82f6;
  --secondary-color: #10b981;
  --text-color: #1f2937;
  --bg-color: #ffffff;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',
    Arial, sans-serif;
  color: var(--text-color);
  background-color: var(--bg-color);
}

a {
  color: inherit;
  text-decoration: none;
}
```

```tsx
// app/layout.tsx
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

## shadcn/ui (Composants)

### Installation

```bash
npx shadcn-ui@latest init
```

### Ajouter des composants

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
```

### Usage

```tsx
// app/page.tsx
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

export default function Home() {
  return (
    <div className="p-8">
      <Card>
        <CardHeader>
          <CardTitle>Mon Composant</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Contenu de la carte</p>
          <Button variant="default" className="mt-4">
            Click me
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Fonts (next/font)

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
  display: 'swap',
  variable: '--font-roboto-mono',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --font-inter: 'Inter', sans-serif;
    --font-roboto-mono: 'Roboto Mono', monospace;
  }
}
```

## Local Fonts

```tsx
// app/layout.tsx
import localFont from 'next/font/local';

const myFont = localFont({
  src: '../public/fonts/my-font.woff2',
  display: 'swap',
  variable: '--font-my-font',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={myFont.variable}>
      <body>{children}</body>
    </html>
  );
}
```

[← Metadata](./infos-nextjs-06-metadata-seo.md) | [Index](./infos-nextjs-00-index.md) | [Authentification →](./infos-nextjs-08-authentication.md)

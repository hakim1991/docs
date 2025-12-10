# 🧪 Testing

[← Optimisation](./infos-nextjs-10-optimization.md) | [Index](./infos-nextjs-00-index.md) | [Déploiement →](./infos-nextjs-12-deployment.md)

## Jest et React Testing Library

### Installation

```bash
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### Configuration

```javascript
// jest.config.js
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  // Chemin vers Next.js app
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
};

module.exports = createJestConfig(customJestConfig);
```

```javascript
// jest.setup.js
import '@testing-library/jest-dom';
```

```json
// package.json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

### Test composant simple

```tsx
// components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);

    const button = screen.getByRole('button', { name: 'Click me' });
    expect(button).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Button</Button>);

    const button = screen.getByRole('button');
    expect(button).toHaveClass('custom-class');
  });
});
```

### Test avec state

```tsx
// components/Counter.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

describe('Counter', () => {
  it('starts at 0', () => {
    render(<Counter />);
    expect(screen.getByText(/count: 0/i)).toBeInTheDocument();
  });

  it('increments counter', () => {
    render(<Counter />);

    const incrementButton = screen.getByRole('button', { name: '+' });
    fireEvent.click(incrementButton);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });

  it('decrements counter', () => {
    render(<Counter />);

    const incrementButton = screen.getByRole('button', { name: '+' });
    const decrementButton = screen.getByRole('button', { name: '-' });

    fireEvent.click(incrementButton);
    fireEvent.click(incrementButton);
    fireEvent.click(decrementButton);

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
  });
});
```

### Test async

```tsx
// components/UserList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import UserList from './UserList';

// Mock fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' },
    ]),
  })
) as jest.Mock;

describe('UserList', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('displays loading state', () => {
    render(<UserList />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays users after loading', async () => {
    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText('Alice')).toBeInTheDocument();
      expect(screen.getByText('Bob')).toBeInTheDocument();
    });
  });

  it('calls fetch with correct URL', async () => {
    render(<UserList />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('https://api.example.com/users');
    });
  });
});
```

### Test avec user-event

```tsx
// components/Form.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Form from './Form';

describe('Form', () => {
  it('submits form with user input', async () => {
    const user = userEvent.setup();
    const handleSubmit = jest.fn();

    render(<Form onSubmit={handleSubmit} />);

    // Taper dans l'input
    const input = screen.getByRole('textbox');
    await user.type(input, 'Hello');

    // Cliquer sur le bouton
    const submitButton = screen.getByRole('button', { name: /submit/i });
    await user.click(submitButton);

    expect(handleSubmit).toHaveBeenCalledWith({ text: 'Hello' });
  });
});
```

## Test API Routes

```tsx
// app/api/users/route.test.ts
import { GET, POST } from './route';
import { prisma } from '@/lib/prisma';

// Mock Prisma
jest.mock('@/lib/prisma', () => ({
  prisma: {
    user: {
      findMany: jest.fn(),
      create: jest.fn(),
    },
  },
}));

describe('/api/users', () => {
  describe('GET', () => {
    it('returns users', async () => {
      const mockUsers = [
        { id: '1', name: 'Alice', email: 'alice@example.com' },
      ];

      (prisma.user.findMany as jest.Mock).mockResolvedValue(mockUsers);

      const response = await GET();
      const data = await response.json();

      expect(data).toEqual(mockUsers);
      expect(prisma.user.findMany).toHaveBeenCalled();
    });
  });

  describe('POST', () => {
    it('creates user', async () => {
      const newUser = { id: '1', name: 'Alice', email: 'alice@example.com' };

      (prisma.user.create as jest.Mock).mockResolvedValue(newUser);

      const request = new Request('http://localhost:3000/api/users', {
        method: 'POST',
        body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' }),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(data).toEqual(newUser);
      expect(response.status).toBe(201);
    });
  });
});
```

## Playwright (E2E Testing)

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Test E2E

```typescript
// e2e/home.spec.ts
import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/Next.js/);
});

test('navigation works', async ({ page }) => {
  await page.goto('/');

  // Click on about link
  await page.click('text=About');

  // Check URL
  await expect(page).toHaveURL('/about');

  // Check content
  await expect(page.locator('h1')).toContainText('About');
});

test('form submission', async ({ page }) => {
  await page.goto('/contact');

  // Fill form
  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Hello');

  // Submit
  await page.click('button[type="submit"]');

  // Check success message
  await expect(page.locator('text=Success')).toBeVisible();
});
```

### Test avec authentication

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can login', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password');

    await page.click('button[type="submit"]');

    // Check redirect to dashboard
    await expect(page).toHaveURL('/dashboard');

    // Check user name is displayed
    await expect(page.locator('text=Welcome')).toBeVisible();
  });

  test('protected route redirects to login', async ({ page }) => {
    await page.goto('/dashboard');

    // Should redirect to login
    await expect(page).toHaveURL('/login');
  });
});
```

### Scripts

```json
// package.json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed"
  }
}
```

## Cypress

### Installation

```bash
npm install -D cypress
npx cypress open
```

### Configuration

```javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    setupNodeEvents(on, config) {},
  },
});
```

### Test

```javascript
// cypress/e2e/home.cy.js
describe('Homepage', () => {
  it('should display title', () => {
    cy.visit('/');
    cy.contains('h1', 'Welcome');
  });

  it('should navigate to about page', () => {
    cy.visit('/');
    cy.contains('About').click();
    cy.url().should('include', '/about');
  });

  it('should submit form', () => {
    cy.visit('/contact');

    cy.get('input[name="name"]').type('John Doe');
    cy.get('input[name="email"]').type('john@example.com');
    cy.get('textarea[name="message"]').type('Hello');

    cy.get('button[type="submit"]').click();

    cy.contains('Success').should('be.visible');
  });
});
```

## Vitest (Alternative à Jest)

### Installation

```bash
npm install -D vitest @vitejs/plugin-react jsdom
```

### Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './vitest.setup.ts',
  },
});
```

```typescript
// vitest.setup.ts
import '@testing-library/jest-dom';
```

### Usage (similaire à Jest)

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders button', () => {
    render(<Button>Click</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });
});
```

## Coverage

```json
// package.json
{
  "scripts": {
    "test:coverage": "jest --coverage"
  }
}
```

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'app/**/*.{js,jsx,ts,tsx}',
    'components/**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

[← Optimisation](./infos-nextjs-10-optimization.md) | [Index](./infos-nextjs-00-index.md) | [Déploiement →](./infos-nextjs-12-deployment.md)

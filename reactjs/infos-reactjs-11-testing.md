# 🧪 Testing

[← Optimisation](./infos-reactjs-10-optimization.md) | [Index](./infos-reactjs-00-index.md) | [Déploiement →](./infos-reactjs-12-deployment.md)

## React Testing Library

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

```jsx
// Button.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('renders button with text', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});

test('calls onClick when clicked', () => {
  const handleClick = jest.fn();
  render(<Button onClick={handleClick}>Click</Button>);

  fireEvent.click(screen.getByText('Click'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

// Counter.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

test('increments counter', () => {
  render(<Counter />);

  const button = screen.getByRole('button', { name: '+' });
  fireEvent.click(button);

  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});

// Async test
test('loads and displays data', async () => {
  render(<UserList />);

  expect(screen.getByText('Loading...')).toBeInTheDocument();

  const user = await screen.findByText('Alice');
  expect(user).toBeInTheDocument();
});
```

[← Optimisation](./infos-reactjs-10-optimization.md) | [Index](./infos-reactjs-00-index.md) | [Déploiement →](./infos-reactjs-12-deployment.md)

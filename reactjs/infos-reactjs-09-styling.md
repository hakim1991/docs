# 🎨 Styling

[← API](./infos-reactjs-08-api-data-fetching.md) | [Index](./infos-reactjs-00-index.md) | [Optimisation →](./infos-reactjs-10-optimization.md)

## Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```js
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: { extend: {} },
  plugins: []
};
```

```css
/* index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

```jsx
function Button() {
  return (
    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
      Click me
    </button>
  );
}
```

## Styled Components

```bash
npm install styled-components
```

```jsx
import styled from 'styled-components';

const Button = styled.button`
  background: ${props => props.primary ? 'blue' : 'white'};
  color: ${props => props.primary ? 'white' : 'blue'};
  padding: 10px 20px;
  border: 2px solid blue;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background: darkblue;
    color: white;
  }
`;

function App() {
  return (
    <>
      <Button primary>Primary</Button>
      <Button>Secondary</Button>
    </>
  );
}
```

## CSS Modules

```css
/* Button.module.css */
.button {
  padding: 10px 20px;
  border-radius: 4px;
}

.primary {
  background: blue;
  color: white;
}
```

```jsx
import styles from './Button.module.css';

function Button({ primary }) {
  return (
    <button className={`${styles.button} ${primary ? styles.primary : ''}`}>
      Click me
    </button>
  );
}
```

[← API](./infos-reactjs-08-api-data-fetching.md) | [Index](./infos-reactjs-00-index.md) | [Optimisation →](./infos-reactjs-10-optimization.md)

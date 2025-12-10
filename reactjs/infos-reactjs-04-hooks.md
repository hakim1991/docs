# 🪝 Hooks

[← State et Props](./infos-reactjs-03-state-props.md) | [Index](./infos-reactjs-00-index.md) | [Routing →](./infos-reactjs-05-routing.md)

## useState

```jsx
const [state, setState] = useState(initialValue);

// Avec fonction
const [count, setCount] = useState(() => {
  const saved = localStorage.getItem('count');
  return saved ? JSON.parse(saved) : 0;
});
```

## useEffect

```jsx
import { useEffect } from 'react';

// Run après chaque render
useEffect(() => {
  console.log('Component rendered');
});

// Run une fois (mount)
useEffect(() => {
  console.log('Component mounted');
}, []);

// Run quand dépendances changent
useEffect(() => {
  console.log('Count changed:', count);
}, [count]);

// Cleanup
useEffect(() => {
  const timer = setInterval(() => {}, 1000);

  return () => {
    clearInterval(timer);
  };
}, []);
```

### Exemples useEffect

```jsx
// Fetch data
function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://api.example.com/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Document title
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}

// Event listener
function WindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return <p>Width: {size.width}, Height: {size.height}</p>;
}
```

## useContext

```jsx
import { createContext, useContext } from 'react';

// Créer context
const ThemeContext = createContext('light');

// Provider
function App() {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Toolbar />
    </ThemeContext.Provider>
  );
}

// Consumer
function ThemedButton() {
  const { theme, setTheme } = useContext(ThemeContext);

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Current theme: {theme}
    </button>
  );
}
```

## useReducer

```jsx
import { useReducer } from 'react';

// Reducer
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'reset':
      return { count: 0 };
    default:
      throw new Error('Unknown action');
  }
}

// Component
function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

## useRef

```jsx
import { useRef } from 'react';

// DOM reference
function Input() {
  const inputRef = useRef(null);

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus</button>
    </>
  );
}

// Valeur mutable (persiste entre renders)
function Timer() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    return () => clearInterval(intervalRef.current);
  }, []);

  return <p>Count: {count}</p>;
}
```

## useMemo

```jsx
import { useMemo } from 'react';

function ExpensiveComponent({ items }) {
  // Calcul coûteux mémorisé
  const sortedItems = useMemo(() => {
    console.log('Sorting items...');
    return items.sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);

  return (
    <ul>
      {sortedItems.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
}
```

## useCallback

```jsx
import { useCallback } from 'react';

function Parent() {
  const [count, setCount] = useState(0);

  // Fonction mémorisée
  const increment = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return <Child onIncrement={increment} />;
}
```

## Custom Hooks

```jsx
// useLocalStorage
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}

// Usage
function App() {
  const [name, setName] = useLocalStorage('name', '');

  return (
    <input value={name} onChange={e => setName(e.target.value)} />
  );
}

// useFetch
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [url]);

  return { data, loading, error };
}

// useToggle
function useToggle(initialValue = false) {
  const [value, setValue] = useState(initialValue);

  const toggle = useCallback(() => {
    setValue(v => !v);
  }, []);

  return [value, toggle];
}

// usePrevious
function usePrevious(value) {
  const ref = useRef();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// useDebounce
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// useWindowSize
function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return size;
}
```

## Rules of Hooks

```
✅ Appeler hooks au top level
✅ Appeler hooks dans React functions
❌ Pas dans loops
❌ Pas dans conditions
❌ Pas dans nested functions
```

```jsx
// ❌ Mauvais
function Bad({ condition }) {
  if (condition) {
    const [state, setState] = useState(0); // ❌
  }
}

// ✅ Bon
function Good({ condition }) {
  const [state, setState] = useState(0);

  if (condition) {
    // Use state here
  }
}
```

[← State et Props](./infos-reactjs-03-state-props.md) | [Index](./infos-reactjs-00-index.md) | [Routing →](./infos-reactjs-05-routing.md)

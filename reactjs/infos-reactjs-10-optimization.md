# ⚡ Optimisation

[← Styling](./infos-reactjs-09-styling.md) | [Index](./infos-reactjs-00-index.md) | [Testing →](./infos-reactjs-11-testing.md)

## React.memo

```jsx
// Évite re-renders inutiles
const ChildComponent = React.memo(function Child({ name }) {
  console.log('Child rendered');
  return <p>{name}</p>;
});

function Parent() {
  const [count, setCount] = useState(0);
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <ChildComponent name="Alice" /> {/* Ne re-render pas */}
    </>
  );
}
```

## useMemo / useCallback

```jsx
// useMemo - mémorise valeur
function ExpensiveList({ items }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => a.name.localeCompare(b.name));
  }, [items]);

  return sortedItems.map(item => <div key={item.id}>{item.name}</div>);
}

// useCallback - mémorise fonction
function Parent() {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);

  return <Child onClick={handleClick} />;
}
```

## Code Splitting

```jsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## React DevTools Profiler

```jsx
import { Profiler } from 'react';

function onRenderCallback(id, phase, actualDuration) {
  console.log(`${id} took ${actualDuration}ms`);
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

[← Styling](./infos-reactjs-09-styling.md) | [Index](./infos-reactjs-00-index.md) | [Testing →](./infos-reactjs-11-testing.md)

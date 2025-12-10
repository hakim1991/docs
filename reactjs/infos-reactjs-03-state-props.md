# 🔄 State et Props

[← JSX et Components](./infos-reactjs-02-jsx-components.md) | [Index](./infos-reactjs-00-index.md) | [Hooks →](./infos-reactjs-04-hooks.md)

## useState Hook

### Basique

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
      <button onClick={() => setCount(count - 1)}>-</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

### Types de state

```jsx
// String
const [name, setName] = useState('');

// Number
const [age, setAge] = useState(0);

// Boolean
const [isOpen, setIsOpen] = useState(false);

// Array
const [items, setItems] = useState([]);

// Object
const [user, setUser] = useState({ name: '', email: '' });

// Null
const [data, setData] = useState(null);
```

### Update state

```jsx
function Examples() {
  // Number
  const [count, setCount] = useState(0);
  setCount(count + 1);                    // Direct
  setCount(prev => prev + 1);             // Fonction (recommandé)

  // String
  const [name, setName] = useState('');
  setName('Alice');

  // Boolean toggle
  const [isOpen, setIsOpen] = useState(false);
  setIsOpen(!isOpen);
  setIsOpen(prev => !prev);               // Fonction

  // Array
  const [items, setItems] = useState([]);
  setItems([...items, newItem]);          // Add
  setItems(items.filter(i => i.id !== id)); // Remove
  setItems(items.map(i => i.id === id ? updated : i)); // Update

  // Object
  const [user, setUser] = useState({ name: '', age: 0 });
  setUser({ ...user, name: 'Alice' });    // Update property
  setUser(prev => ({ ...prev, age: 30 }));
}
```

### Exemples pratiques

```jsx
// Toggle
function Toggle() {
  const [isOn, setIsOn] = useState(false);

  return (
    <button onClick={() => setIsOn(!isOn)}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  );
}

// Input controlled
function Input() {
  const [value, setValue] = useState('');

  return (
    <div>
      <input
        value={value}
        onChange={e => setValue(e.target.value)}
      />
      <p>You typed: {value}</p>
    </div>
  );
}

// Todo list
function TodoList() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    setTodos([...todos, { id: Date.now(), text: input }]);
    setInput('');
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={addTodo}>Add</button>

      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            {todo.text}
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Props détaillés

### Props vs State

```
Props:
- Passés du parent
- Immutables (read-only)
- Contrôlés par parent

State:
- Gérés dans composant
- Mutables avec setState
- Privés au composant
```

### Passer callbacks en props

```jsx
// Parent
function Parent() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(count + 1);

  return <Child count={count} onIncrement={increment} />;
}

// Child
function Child({ count, onIncrement }) {
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={onIncrement}>Increment</button>
    </div>
  );
}
```

### Props drilling

```jsx
// Problème: passer props à travers plusieurs niveaux

// App
function App() {
  const [user, setUser] = useState({ name: 'Alice' });
  return <Parent user={user} />;
}

// Parent
function Parent({ user }) {
  return <Child user={user} />;
}

// Child
function Child({ user }) {
  return <GrandChild user={user} />;
}

// GrandChild
function GrandChild({ user }) {
  return <p>{user.name}</p>;
}

// Solution: Context API (voir chapitre State Management)
```

### PropTypes validation

```bash
npm install prop-types
```

```jsx
import PropTypes from 'prop-types';

function User({ name, age, isAdmin }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>Age: {age}</p>
      {isAdmin && <span>Admin</span>}
    </div>
  );
}

User.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number.isRequired,
  isAdmin: PropTypes.bool
};

User.defaultProps = {
  isAdmin: false
};
```

## Lifting State Up

```jsx
// Partager state entre siblings: lifter dans parent commun

function App() {
  const [temperature, setTemperature] = useState(0);

  return (
    <div>
      <TemperatureInput
        temperature={temperature}
        onTemperatureChange={setTemperature}
      />
      <BoilingVerdict temperature={temperature} />
    </div>
  );
}

function TemperatureInput({ temperature, onTemperatureChange }) {
  return (
    <input
      type="number"
      value={temperature}
      onChange={e => onTemperatureChange(Number(e.target.value))}
    />
  );
}

function BoilingVerdict({ temperature }) {
  return (
    <p>
      {temperature >= 100 ? 'Water would boil' : 'Water would not boil'}
    </p>
  );
}
```

## Conditional Rendering avancé

```jsx
// Multiple conditions
function Status({ status }) {
  if (status === 'loading') return <Spinner />;
  if (status === 'error') return <Error />;
  if (status === 'empty') return <Empty />;
  return <Data />;
}

// Switch case pattern
function Status({ status }) {
  switch (status) {
    case 'loading':
      return <Spinner />;
    case 'error':
      return <Error />;
    case 'success':
      return <Success />;
    default:
      return null;
  }
}

// Object mapping
const STATUS_COMPONENTS = {
  loading: Spinner,
  error: Error,
  success: Success
};

function Status({ status }) {
  const Component = STATUS_COMPONENTS[status];
  return Component ? <Component /> : null;
}
```

## Formulaires

### Controlled components

```jsx
function Form() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    age: '',
    gender: '',
    agree: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form data:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="Name"
      />

      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        placeholder="Email"
      />

      <input
        name="age"
        type="number"
        value={formData.age}
        onChange={handleChange}
        placeholder="Age"
      />

      <select name="gender" value={formData.gender} onChange={handleChange}>
        <option value="">Select...</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>

      <label>
        <input
          name="agree"
          type="checkbox"
          checked={formData.agree}
          onChange={handleChange}
        />
        I agree
      </label>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Validation simple

```jsx
function Form() {
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};

    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Email is invalid';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      console.log('Form is valid');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
      />
      {errors.email && <span className="error">{errors.email}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Exemples complets

### Counter avec historique

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]);

  const increment = () => {
    setCount(prev => prev + 1);
    setHistory(prev => [...prev, count + 1]);
  };

  const decrement = () => {
    setCount(prev => prev - 1);
    setHistory(prev => [...prev, count - 1]);
  };

  return (
    <div>
      <h2>Count: {count}</h2>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>

      <h3>History:</h3>
      <ul>
        {history.map((value, index) => (
          <li key={index}>{value}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Todo avec filter

```jsx
function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');
  const [filter, setFilter] = useState('all');

  const addTodo = () => {
    if (input.trim()) {
      setTodos([...todos, { id: Date.now(), text: input, completed: false }]);
      setInput('');
    }
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.completed;
    if (filter === 'completed') return todo.completed;
    return true;
  });

  return (
    <div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && addTodo()}
      />
      <button onClick={addTodo}>Add</button>

      <div>
        <button onClick={() => setFilter('all')}>All</button>
        <button onClick={() => setFilter('active')}>Active</button>
        <button onClick={() => setFilter('completed')}>Completed</button>
      </div>

      <ul>
        {filteredTodos.map(todo => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
            />
            <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
              {todo.text}
            </span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

[← JSX et Components](./infos-reactjs-02-jsx-components.md) | [Index](./infos-reactjs-00-index.md) | [Hooks →](./infos-reactjs-04-hooks.md)

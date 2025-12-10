# 📘 JSX et Components

[← Introduction](./infos-reactjs-01-introduction-installation.md) | [Index](./infos-reactjs-00-index.md) | [State et Props →](./infos-reactjs-03-state-props.md)

## JSX

### Qu'est-ce que JSX ?

JSX (JavaScript XML) est une extension syntaxique de JavaScript qui ressemble à HTML.

```jsx
// JSX
const element = <h1>Hello, World!</h1>;

// Transpilé en JavaScript
const element = React.createElement('h1', null, 'Hello, World!');
```

### Syntaxe JSX

```jsx
// Élément simple
const element = <h1>Hello</h1>;

// Avec attributs
const element = <img src="image.jpg" alt="Description" />;

// Auto-fermant
const element = <input type="text" />;

// Nested
const element = (
  <div>
    <h1>Title</h1>
    <p>Paragraph</p>
  </div>
);

// JavaScript expressions dans JSX
const name = 'Alice';
const element = <h1>Hello, {name}!</h1>;

// Expressions complexes
const element = <h1>{user.name.toUpperCase()}</h1>;
const element = <p>{2 + 2}</p>;
const element = <p>{isLoggedIn ? 'Welcome' : 'Please login'}</p>;
```

### Différences JSX vs HTML

```jsx
// className au lieu de class
<div className="container">Content</div>

// htmlFor au lieu de for
<label htmlFor="input-id">Label</label>

// onClick au lieu de onclick
<button onClick={handleClick}>Click</button>

// Style en objet
<div style={{ color: 'red', fontSize: '16px' }}>Text</div>

// Tous les attributs en camelCase
<input onChange={handleChange} maxLength={10} />

// Self-closing obligatoire
<img src="image.jpg" />
<input type="text" />
```

### Commentaires en JSX

```jsx
function App() {
  return (
    <div>
      {/* Commentaire JSX */}
      <h1>Title</h1>

      {/*
        Commentaire
        multi-lignes
      */}
    </div>
  );
}
```

### Fragments

```jsx
// Avec Fragment
import { Fragment } from 'react';

function App() {
  return (
    <Fragment>
      <h1>Title</h1>
      <p>Paragraph</p>
    </Fragment>
  );
}

// Syntaxe courte
function App() {
  return (
    <>
      <h1>Title</h1>
      <p>Paragraph</p>
    </>
  );
}

// Avec key (dans map)
function List() {
  return items.map(item => (
    <Fragment key={item.id}>
      <h3>{item.title}</h3>
      <p>{item.description}</p>
    </Fragment>
  ));
}
```

## Functional Components

### Composant basique

```jsx
// src/components/Hello.jsx
function Hello() {
  return <h1>Hello, World!</h1>;
}

export default Hello;

// Utilisation
import Hello from './components/Hello';

function App() {
  return (
    <div>
      <Hello />
    </div>
  );
}
```

### Arrow function component

```jsx
const Hello = () => {
  return <h1>Hello, World!</h1>;
};

export default Hello;

// Avec return implicite
const Hello = () => <h1>Hello, World!</h1>;

// Multi-lignes
const Hello = () => (
  <div>
    <h1>Hello</h1>
    <p>World</p>
  </div>
);
```

### Composant avec logique

```jsx
function Greeting() {
  const name = 'Alice';
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : 'Good afternoon';

  return (
    <div>
      <h1>{greeting}, {name}!</h1>
      <p>Current hour: {hour}</p>
    </div>
  );
}
```

## Props

### Passer props

```jsx
// Définir composant
function Welcome(props) {
  return <h1>Hello, {props.name}!</h1>;
}

// Utiliser composant
<Welcome name="Alice" />
<Welcome name="Bob" />
```

### Destructuring props

```jsx
// Avec destructuring
function Welcome({ name, age }) {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>Age: {age}</p>
    </div>
  );
}

// Utilisation
<Welcome name="Alice" age={30} />

// Props par défaut
function Welcome({ name = 'Guest', age = 0 }) {
  return <h1>Hello, {name}! Age: {age}</h1>;
}
```

### Types de props

```jsx
function User({ name, age, isAdmin, hobbies, address }) {
  return (
    <div>
      {/* String */}
      <h2>{name}</h2>

      {/* Number */}
      <p>Age: {age}</p>

      {/* Boolean */}
      <p>Admin: {isAdmin ? 'Yes' : 'No'}</p>

      {/* Array */}
      <ul>
        {hobbies.map((hobby, index) => (
          <li key={index}>{hobby}</li>
        ))}
      </ul>

      {/* Object */}
      <p>City: {address.city}</p>
    </div>
  );
}

// Utilisation
<User
  name="Alice"
  age={30}
  isAdmin={true}
  hobbies={['Reading', 'Gaming']}
  address={{ city: 'Paris', country: 'France' }}
/>
```

### Children prop

```jsx
// Composant avec children
function Card({ title, children }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-body">{children}</div>
    </div>
  );
}

// Utilisation
<Card title="My Card">
  <p>This is the content</p>
  <button>Click me</button>
</Card>
```

### Spread props

```jsx
const userProps = {
  name: 'Alice',
  age: 30,
  email: 'alice@example.com'
};

<User {...userProps} />

// Équivalent à:
<User name="Alice" age={30} email="alice@example.com" />

// Override props
<User {...userProps} name="Bob" />
```

## Render conditionnel

### If/Else avec variable

```jsx
function Greeting({ isLoggedIn }) {
  let message;

  if (isLoggedIn) {
    message = <h1>Welcome back!</h1>;
  } else {
    message = <h1>Please log in</h1>;
  }

  return <div>{message}</div>;
}
```

### Ternaire

```jsx
function Greeting({ isLoggedIn }) {
  return (
    <div>
      {isLoggedIn ? <h1>Welcome back!</h1> : <h1>Please log in</h1>}
    </div>
  );
}

// Inline complexe
function User({ user }) {
  return (
    <div>
      {user ? (
        <div>
          <h2>{user.name}</h2>
          <p>{user.email}</p>
        </div>
      ) : (
        <p>No user found</p>
      )}
    </div>
  );
}
```

### Logical AND (&&)

```jsx
function Notification({ hasNotifications, count }) {
  return (
    <div>
      {hasNotifications && <span>You have {count} notifications</span>}
    </div>
  );
}

// Avec plusieurs conditions
function Profile({ user, isAdmin }) {
  return (
    <div>
      <h1>{user.name}</h1>
      {isAdmin && <span className="badge">Admin</span>}
      {user.email && <p>Email: {user.email}</p>}
    </div>
  );
}
```

### Early return

```jsx
function UserProfile({ user }) {
  if (!user) {
    return <p>Loading...</p>;
  }

  if (user.error) {
    return <p>Error: {user.error}</p>;
  }

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

## Listes et Keys

### Render liste

```jsx
function UserList() {
  const users = [
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' },
    { id: 3, name: 'Charlie' }
  ];

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Keys importance

```jsx
// ❌ Mauvais (index comme key)
{items.map((item, index) => (
  <li key={index}>{item}</li>
))}

// ✅ Bon (ID unique)
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}

// ✅ Bon (génération ID unique)
import { nanoid } from 'nanoid';

{items.map(item => (
  <li key={nanoid()}>{item}</li>
))}
```

### Composant liste réutilisable

```jsx
function UserCard({ user }) {
  return (
    <div className="card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}

function UserList({ users }) {
  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

// Utilisation
const users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
];

<UserList users={users} />
```

## Events

### Gérer événements

```jsx
function Button() {
  const handleClick = () => {
    console.log('Button clicked!');
  };

  return <button onClick={handleClick}>Click me</button>;
}

// Inline
<button onClick={() => console.log('Clicked')}>Click</button>

// Avec paramètres
function Button() {
  const handleClick = (message) => {
    console.log(message);
  };

  return (
    <button onClick={() => handleClick('Hello!')}>Click</button>
  );
}
```

### Événements courants

```jsx
function EventsDemo() {
  return (
    <div>
      {/* Click */}
      <button onClick={() => console.log('Clicked')}>Click</button>

      {/* Double click */}
      <button onDoubleClick={() => console.log('Double clicked')}>
        Double Click
      </button>

      {/* Mouse events */}
      <div
        onMouseEnter={() => console.log('Mouse enter')}
        onMouseLeave={() => console.log('Mouse leave')}
      >
        Hover me
      </div>

      {/* Input */}
      <input
        onChange={(e) => console.log(e.target.value)}
        placeholder="Type something"
      />

      {/* Form */}
      <form onSubmit={(e) => {
        e.preventDefault();
        console.log('Form submitted');
      }}>
        <button type="submit">Submit</button>
      </form>

      {/* Keyboard */}
      <input
        onKeyDown={(e) => console.log('Key down:', e.key)}
        onKeyUp={(e) => console.log('Key up:', e.key)}
      />
    </div>
  );
}
```

### Event object

```jsx
function Input() {
  const handleChange = (event) => {
    console.log('Value:', event.target.value);
    console.log('Name:', event.target.name);
    console.log('Type:', event.type);
  };

  return (
    <input
      name="username"
      onChange={handleChange}
      placeholder="Username"
    />
  );
}

// Prevent default
function Form() {
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Form submitted without page reload');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Style

### Inline styles

```jsx
function StyledComponent() {
  const style = {
    color: 'red',
    fontSize: '24px',
    fontWeight: 'bold',
    backgroundColor: '#f0f0f0'
  };

  return (
    <div style={style}>
      Styled Text
    </div>
  );
}

// Inline direct
<div style={{ color: 'blue', padding: '20px' }}>
  Blue text
</div>
```

### CSS Classes

```jsx
// Component
function Card({ isActive }) {
  const className = isActive ? 'card active' : 'card';

  return <div className={className}>Content</div>;
}

// Template literals
const className = `card ${isActive ? 'active' : ''} ${large ? 'large' : ''}`;

// Classnames library
import classNames from 'classnames';

const className = classNames('card', {
  active: isActive,
  large: isLarge
});
```

### CSS Modules

```css
/* Card.module.css */
.card {
  padding: 20px;
  border: 1px solid #ddd;
}

.active {
  border-color: blue;
}
```

```jsx
// Card.jsx
import styles from './Card.module.css';

function Card({ isActive }) {
  return (
    <div className={`${styles.card} ${isActive ? styles.active : ''}`}>
      Content
    </div>
  );
}
```

[← Introduction](./infos-reactjs-01-introduction-installation.md) | [Index](./infos-reactjs-00-index.md) | [State et Props →](./infos-reactjs-03-state-props.md)

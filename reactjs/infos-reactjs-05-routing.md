# 🗺️ Routing

[← Hooks](./infos-reactjs-04-hooks.md) | [Index](./infos-reactjs-00-index.md) | [State Management →](./infos-reactjs-06-state-management.md)

## React Router

```bash
npm install react-router-dom
```

## Setup basique

```jsx
// main.jsx
import { BrowserRouter } from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

// App.jsx
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
    </Routes>
  );
}
```

## Navigation

```jsx
import { Link, NavLink } from 'react-router-dom';

function Navigation() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>

      {/* NavLink avec style actif */}
      <NavLink
        to="/about"
        className={({ isActive }) => isActive ? 'active' : ''}
      >
        About
      </NavLink>
    </nav>
  );
}

// Navigation programmatique
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  const handleSubmit = () => {
    // Login logic
    navigate('/dashboard');
  };
}
```

## Paramètres URL

```jsx
// Routes avec params
<Route path="/users/:id" element={<UserProfile />} />

// Accéder params
import { useParams } from 'react-router-dom';

function UserProfile() {
  const { id } = useParams();

  return <h1>User ID: {id}</h1>;
}

// Query params
import { useSearchParams } from 'react-router-dom';

function Products() {
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get('category');

  return <p>Category: {category}</p>;
}
// URL: /products?category=electronics
```

## Nested Routes

```jsx
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="products" element={<Products />}>
          <Route index element={<ProductList />} />
          <Route path=":id" element={<ProductDetail />} />
        </Route>
      </Route>
    </Routes>
  );
}

// Layout avec Outlet
import { Outlet } from 'react-router-dom';

function Layout() {
  return (
    <div>
      <Header />
      <main>
        <Outlet /> {/* Nested routes render here */}
      </main>
      <Footer />
    </div>
  );
}
```

## Protected Routes

```jsx
function ProtectedRoute({ children }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// Usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

## 404 Page

```jsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="*" element={<NotFound />} />
</Routes>

function NotFound() {
  return (
    <div>
      <h1>404 - Page Not Found</h1>
      <Link to="/">Go Home</Link>
    </div>
  );
}
```

[← Hooks](./infos-reactjs-04-hooks.md) | [Index](./infos-reactjs-00-index.md) | [State Management →](./infos-reactjs-06-state-management.md)

# 🌐 API et Data Fetching

[← Forms](./infos-reactjs-07-forms-validation.md) | [Index](./infos-reactjs-00-index.md) | [Styling →](./infos-reactjs-09-styling.md)

## Fetch API

```jsx
function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('https://api.example.com/users')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

## Axios

```bash
npm install axios
```

```jsx
import axios from 'axios';

// api.js
export const api = axios.create({
  baseURL: 'https://api.example.com',
  headers: { 'Content-Type': 'application/json' }
});

// Component
function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get('/users')
      .then(res => setUsers(res.data))
      .catch(err => console.error(err));
  }, []);

  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

## React Query

```bash
npm install @tanstack/react-query
```

```jsx
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';

const queryClient = new QueryClient();

// main.jsx
<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>

// Component
function Users() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('https://api.example.com/users').then(res => res.json())
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// Mutation
import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreateUser() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newUser) => api.post('/users', newUser),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });

  const handleSubmit = (data) => {
    mutation.mutate(data);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

[← Forms](./infos-reactjs-07-forms-validation.md) | [Index](./infos-reactjs-00-index.md) | [Styling →](./infos-reactjs-09-styling.md)

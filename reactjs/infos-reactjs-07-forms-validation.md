# 📝 Forms et Validation

[← State Management](./infos-reactjs-06-state-management.md) | [Index](./infos-reactjs-00-index.md) | [API et Data Fetching →](./infos-reactjs-08-api-data-fetching.md)

## React Hook Form

```bash
npm install react-hook-form
```

```jsx
import { useForm } from 'react-hook-form';

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name', { required: 'Name is required' })} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('email', {
        required: 'Email is required',
        pattern: {
          value: /\S+@\S+\.\S+/,
          message: 'Email is invalid'
        }
      })} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('age', {
        min: { value: 18, message: 'Must be 18+' },
        max: { value: 99, message: 'Must be under 100' }
      })} type="number" />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Validation avec Yup/Zod

```bash
npm install @hookform/resolvers yup
```

```jsx
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

const schema = yup.object({
  name: yup.string().required('Name is required'),
  email: yup.string().email('Invalid email').required('Email is required'),
  age: yup.number().min(18, 'Must be 18+').required()
});

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema)
  });

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}

      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('age')} type="number" />
      {errors.age && <span>{errors.age.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

[← State Management](./infos-reactjs-06-state-management.md) | [Index](./infos-reactjs-00-index.md) | [API et Data Fetching →](./infos-reactjs-08-api-data-fetching.md)

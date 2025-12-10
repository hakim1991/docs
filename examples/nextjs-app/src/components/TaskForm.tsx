import { useState } from 'react';
import { TaskCreate } from '@/services/api';

interface TaskFormProps {
  onSubmit: (task: TaskCreate) => void;
}

export function TaskForm({ onSubmit }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
    priority: 'medium',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title.trim()) {
      alert('Le titre est obligatoire');
      return;
    }
    onSubmit(formData);
    // Réinitialiser le formulaire
    setFormData({
      title: '',
      description: '',
      priority: 'medium',
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700"
        >
          Titre <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={formData.title}
          onChange={(e) =>
            setFormData({ ...formData, title: e.target.value })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Ex: Terminer le rapport mensuel"
          required
        />
      </div>

      <div>
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700"
        >
          Description
        </label>
        <textarea
          id="description"
          value={formData.description}
          onChange={(e) =>
            setFormData({ ...formData, description: e.target.value })
          }
          rows={4}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Décrivez la tâche en détail..."
        />
      </div>

      <div>
        <label
          htmlFor="priority"
          className="block text-sm font-medium text-gray-700"
        >
          Priorité
        </label>
        <select
          id="priority"
          value={formData.priority}
          onChange={(e) =>
            setFormData({
              ...formData,
              priority: e.target.value as TaskCreate['priority'],
            })
          }
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        >
          <option value="low">🔵 Basse</option>
          <option value="medium">🟡 Moyenne</option>
          <option value="high">🔴 Haute</option>
        </select>
      </div>

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={() =>
            setFormData({ title: '', description: '', priority: 'medium' })
          }
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Réinitialiser
        </button>
        <button
          type="submit"
          className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          ✅ Créer la tâche
        </button>
      </div>
    </form>
  );
}

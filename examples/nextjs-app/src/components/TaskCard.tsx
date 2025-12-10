import { Task } from '@/services/api';

interface TaskCardProps {
  task: Task;
  onUpdate: (id: number, updates: Partial<Task>) => void;
  onDelete: (id: number) => void;
}

const statusColors = {
  todo: 'bg-orange-100 text-orange-800',
  in_progress: 'bg-blue-100 text-blue-800',
  done: 'bg-green-100 text-green-800',
};

const statusLabels = {
  todo: '📝 À faire',
  in_progress: '⏳ En cours',
  done: '✅ Terminé',
};

const priorityColors = {
  low: 'bg-gray-100 text-gray-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-red-100 text-red-800',
};

const priorityLabels = {
  low: '🔵 Basse',
  medium: '🟡 Moyenne',
  high: '🔴 Haute',
};

export function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onUpdate(task.id, { status: e.target.value as Task['status'] });
  };

  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onUpdate(task.id, { priority: e.target.value as Task['priority'] });
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">{task.title}</h3>
          {task.description && (
            <p className="mt-1 text-sm text-gray-600">{task.description}</p>
          )}

          <div className="mt-3 flex flex-wrap gap-2">
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                statusColors[task.status]
              }`}
            >
              {statusLabels[task.status]}
            </span>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                priorityColors[task.priority]
              }`}
            >
              {priorityLabels[task.priority]}
            </span>
          </div>

          <div className="mt-2 text-xs text-gray-500">
            Créée le {new Date(task.created_at).toLocaleDateString('fr-FR')}
          </div>
        </div>

        <div className="ml-4 flex-shrink-0 flex items-center space-x-2">
          <button
            onClick={() => onDelete(task.id)}
            className="text-red-600 hover:text-red-800"
            title="Supprimer"
          >
            <svg
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">
            Statut
          </label>
          <select
            value={task.status}
            onChange={handleStatusChange}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
          >
            <option value="todo">À faire</option>
            <option value="in_progress">En cours</option>
            <option value="done">Terminé</option>
          </select>
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">
            Priorité
          </label>
          <select
            value={task.priority}
            onChange={handlePriorityChange}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
          >
            <option value="low">Basse</option>
            <option value="medium">Moyenne</option>
            <option value="high">Haute</option>
          </select>
        </div>
      </div>
    </div>
  );
}

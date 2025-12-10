// Configuration de l'URL de l'API
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types pour les tâches
export type TaskStatus = 'todo' | 'in_progress' | 'done';
export type TaskPriority = 'low' | 'medium' | 'high';

export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  created_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority: TaskPriority;
}

export interface Statistics {
  total: number;
  by_status: {
    todo: number;
    in_progress: number;
    done: number;
  };
  by_priority: {
    low: number;
    medium: number;
    high: number;
  };
  completion_rate: number;
}

// Gestion des erreurs
class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Fonction utilitaire pour les requêtes
async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        response.status,
        errorData
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      'Erreur de connexion à l\'API. Vérifiez que le backend est démarré.',
      0,
      error
    );
  }
}

// API pour les tâches
export const tasksApi = {
  /**
   * Récupérer toutes les tâches avec filtres optionnels
   */
  getTasks: async (params?: {
    status?: string;
    priority?: string;
  }): Promise<Task[]> => {
    const queryParams = new URLSearchParams();
    if (params?.status && params.status !== 'all') {
      queryParams.append('status', params.status);
    }
    if (params?.priority && params.priority !== 'all') {
      queryParams.append('priority', params.priority);
    }

    const query = queryParams.toString();
    const endpoint = `/tasks${query ? `?${query}` : ''}`;

    return fetchApi<Task[]>(endpoint);
  },

  /**
   * Récupérer une tâche par son ID
   */
  getTask: async (id: number): Promise<Task> => {
    return fetchApi<Task>(`/tasks/${id}`);
  },

  /**
   * Créer une nouvelle tâche
   */
  createTask: async (task: TaskCreate): Promise<Task> => {
    return fetchApi<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  },

  /**
   * Mettre à jour une tâche
   */
  updateTask: async (
    id: number,
    updates: Partial<Omit<Task, 'id' | 'created_at'>>
  ): Promise<Task> => {
    return fetchApi<Task>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  /**
   * Supprimer une tâche
   */
  deleteTask: async (id: number): Promise<{ message: string }> => {
    return fetchApi<{ message: string }>(`/tasks/${id}`, {
      method: 'DELETE',
    });
  },

  /**
   * Récupérer les statistiques
   */
  getStatistics: async (): Promise<Statistics> => {
    return fetchApi<Statistics>('/stats');
  },
};

// Export de l'URL de l'API pour référence
export { API_URL };

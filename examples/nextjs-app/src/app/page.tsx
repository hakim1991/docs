'use client';

import { useState, useEffect } from 'react';
import { TaskList } from '@/components/TaskList';
import { TaskForm } from '@/components/TaskForm';
import { Statistics } from '@/components/Statistics';
import { tasksApi, type Task, type TaskCreate, type Statistics as StatsType } from '@/services/api';

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [statistics, setStatistics] = useState<StatsType | null>(null);
  const [activeTab, setActiveTab] = useState<'tasks' | 'add' | 'stats'>('tasks');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Charger les tâches au démarrage
  useEffect(() => {
    loadTasks();
    loadStatistics();
  }, [filterStatus, filterPriority]);

  // Fonction pour charger les tâches
  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const params: any = {};
      if (filterStatus !== 'all') params.status = filterStatus;
      if (filterPriority !== 'all') params.priority = filterPriority;

      const data = await tasksApi.getTasks(params);
      setTasks(data);
    } catch (err) {
      setError('Erreur lors du chargement des tâches');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Fonction pour charger les statistiques
  const loadStatistics = async () => {
    try {
      const data = await tasksApi.getStatistics();
      setStatistics(data);
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques', err);
    }
  };

  // Fonction pour créer une tâche
  const handleCreateTask = async (taskData: TaskCreate) => {
    try {
      await tasksApi.createTask(taskData);
      await loadTasks();
      await loadStatistics();
      setActiveTab('tasks');
    } catch (err) {
      setError('Erreur lors de la création de la tâche');
      console.error(err);
    }
  };

  // Fonction pour mettre à jour une tâche
  const handleUpdateTask = async (id: number, updates: Partial<Task>) => {
    try {
      await tasksApi.updateTask(id, updates);
      await loadTasks();
      await loadStatistics();
    } catch (err) {
      setError('Erreur lors de la mise à jour de la tâche');
      console.error(err);
    }
  };

  // Fonction pour supprimer une tâche
  const handleDeleteTask = async (id: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) return;

    try {
      await tasksApi.deleteTask(id);
      await loadTasks();
      await loadStatistics();
    } catch (err) {
      setError('Erreur lors de la suppression de la tâche');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* En-tête */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            📋 Gestionnaire de Tâches
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Application Next.js + React + FastAPI
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistiques dans la sidebar */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          {statistics && (
            <>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-sm font-medium text-gray-500">Total</div>
                <div className="mt-2 text-3xl font-bold text-gray-900">
                  {statistics.total}
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-sm font-medium text-gray-500">À faire</div>
                <div className="mt-2 text-3xl font-bold text-orange-600">
                  {statistics.by_status.todo}
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-sm font-medium text-gray-500">En cours</div>
                <div className="mt-2 text-3xl font-bold text-blue-600">
                  {statistics.by_status.in_progress}
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-sm font-medium text-gray-500">Terminé</div>
                <div className="mt-2 text-3xl font-bold text-green-600">
                  {statistics.by_status.done}
                </div>
              </div>
            </>
          )}
        </div>

        {/* Messages d'erreur */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <div className="text-sm text-red-800">{error}</div>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-800 hover:text-red-900"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {/* Navigation par onglets */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('tasks')}
                className={`${
                  activeTab === 'tasks'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                📋 Tâches
              </button>
              <button
                onClick={() => setActiveTab('add')}
                className={`${
                  activeTab === 'add'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                ➕ Ajouter
              </button>
              <button
                onClick={() => setActiveTab('stats')}
                className={`${
                  activeTab === 'stats'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                📈 Statistiques
              </button>
            </nav>
          </div>
        </div>

        {/* Contenu des onglets */}
        <div className="bg-white rounded-lg shadow">
          {activeTab === 'tasks' && (
            <div className="p-6">
              {/* Filtres */}
              <div className="mb-6 flex flex-wrap gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Statut
                  </label>
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  >
                    <option value="all">Tous</option>
                    <option value="todo">À faire</option>
                    <option value="in_progress">En cours</option>
                    <option value="done">Terminé</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Priorité
                  </label>
                  <select
                    value={filterPriority}
                    onChange={(e) => setFilterPriority(e.target.value)}
                    className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  >
                    <option value="all">Toutes</option>
                    <option value="low">Basse</option>
                    <option value="medium">Moyenne</option>
                    <option value="high">Haute</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <button
                    onClick={loadTasks}
                    disabled={loading}
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                  >
                    🔄 Actualiser
                  </button>
                </div>
              </div>

              {/* Liste des tâches */}
              <TaskList
                tasks={tasks}
                loading={loading}
                onUpdate={handleUpdateTask}
                onDelete={handleDeleteTask}
              />
            </div>
          )}

          {activeTab === 'add' && (
            <div className="p-6">
              <TaskForm onSubmit={handleCreateTask} />
            </div>
          )}

          {activeTab === 'stats' && (
            <div className="p-6">
              {statistics && <Statistics statistics={statistics} />}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

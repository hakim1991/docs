import { Statistics as StatsType } from '@/services/api';

interface StatisticsProps {
  statistics: StatsType;
}

export function Statistics({ statistics }: StatisticsProps) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          📊 Statistiques Globales
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6">
            <div className="text-sm font-medium text-blue-600">Total</div>
            <div className="mt-2 text-4xl font-bold text-blue-900">
              {statistics.total}
            </div>
            <div className="mt-2 text-xs text-blue-600">tâches au total</div>
          </div>

          <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-6">
            <div className="text-sm font-medium text-orange-600">À faire</div>
            <div className="mt-2 text-4xl font-bold text-orange-900">
              {statistics.by_status.todo}
            </div>
            <div className="mt-2 text-xs text-orange-600">
              {((statistics.by_status.todo / statistics.total) * 100).toFixed(1)}% du total
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6">
            <div className="text-sm font-medium text-blue-600">En cours</div>
            <div className="mt-2 text-4xl font-bold text-blue-900">
              {statistics.by_status.in_progress}
            </div>
            <div className="mt-2 text-xs text-blue-600">
              {((statistics.by_status.in_progress / statistics.total) * 100).toFixed(1)}% du total
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6">
            <div className="text-sm font-medium text-green-600">Terminé</div>
            <div className="mt-2 text-4xl font-bold text-green-900">
              {statistics.by_status.done}
            </div>
            <div className="mt-2 text-xs text-green-600">
              {((statistics.by_status.done / statistics.total) * 100).toFixed(1)}% du total
            </div>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          📈 Taux de complétion
        </h3>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Progression</span>
            <span className="text-2xl font-bold text-indigo-600">
              {statistics.completion_rate.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-gradient-to-r from-indigo-500 to-indigo-600 h-4 rounded-full transition-all duration-500"
              style={{ width: `${statistics.completion_rate}%` }}
            ></div>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {statistics.by_status.done} tâche(s) terminée(s) sur {statistics.total}
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          🎯 Répartition par priorité
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-gray-700">🔴 Haute</div>
                <div className="mt-2 text-3xl font-bold text-red-600">
                  {statistics.by_priority.high}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-500">
                  {((statistics.by_priority.high / statistics.total) * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-gray-700">🟡 Moyenne</div>
                <div className="mt-2 text-3xl font-bold text-yellow-600">
                  {statistics.by_priority.medium}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-500">
                  {((statistics.by_priority.medium / statistics.total) * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-gray-700">🔵 Basse</div>
                <div className="mt-2 text-3xl font-bold text-gray-600">
                  {statistics.by_priority.low}
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-gray-500">
                  {((statistics.by_priority.low / statistics.total) * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 border border-purple-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          💡 Recommandations
        </h3>
        <ul className="space-y-2 text-sm text-gray-700">
          {statistics.by_priority.high > 0 && (
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>
                Vous avez <strong>{statistics.by_priority.high}</strong> tâche(s) de haute priorité.
                Concentrez-vous dessus en premier !
              </span>
            </li>
          )}
          {statistics.by_status.todo > statistics.by_status.in_progress * 2 && (
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>
                Beaucoup de tâches en attente. Commencez-en quelques-unes pour progresser.
              </span>
            </li>
          )}
          {statistics.completion_rate >= 70 && (
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>
                Excellent travail ! Vous avez terminé plus de 70% de vos tâches. 🎉
              </span>
            </li>
          )}
          {statistics.completion_rate < 30 && statistics.total > 5 && (
            <li className="flex items-start">
              <span className="mr-2">•</span>
              <span>
                Restez concentré ! Terminez les tâches en cours avant d'en ajouter de nouvelles.
              </span>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}

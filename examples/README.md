# 📚 Exemples FastAPI, Streamlit et Next.js

Ce dossier contient des exemples complets d'applications web modernes utilisant différentes technologies.

## 📁 Structure

```
examples/
├── fastapi-example/          # Exemple FastAPI pur
│   ├── main.py              # API REST complète
│   └── requirements.txt
├── streamlit-example/        # Exemple Streamlit pur
│   ├── app.py               # Dashboard interactif
│   └── requirements.txt
├── fastapi-streamlit-app/   # Application complète (Python)
│   ├── backend/
│   │   ├── api.py           # API FastAPI
│   │   └── requirements.txt
│   └── frontend/
│       ├── app.py           # Interface Streamlit
│       └── requirements.txt
└── nextjs-app/              # Application Next.js + React (JavaScript)
    ├── src/
    │   ├── app/             # Pages Next.js (App Router)
    │   ├── components/      # Composants React
    │   └── services/        # Services API
    └── package.json
```

## 🚀 Démarrage Rapide

### 1. FastAPI seul

API REST complète avec CRUD, validation, documentation automatique.

```bash
cd fastapi-example
pip install -r requirements.txt
python main.py
```

Accéder à:
- API: http://localhost:8000
- Documentation Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Fonctionnalités:**
- ✅ CRUD complet utilisateurs
- ✅ Validation avec Pydantic
- ✅ Recherche et filtres
- ✅ Statistiques
- ✅ Upload de fichiers
- ✅ CORS configuré
- ✅ Documentation interactive

### 2. Streamlit seul

Dashboard interactif avec graphiques et analyses.

```bash
cd streamlit-example
pip install -r requirements.txt
streamlit run app.py
```

Accéder à: http://localhost:8501

**Fonctionnalités:**
- ✅ Dashboard de ventes
- ✅ Filtres dynamiques
- ✅ Graphiques Plotly interactifs
- ✅ Métriques KPI
- ✅ Tableaux de données
- ✅ Export CSV
- ✅ Formulaires
- ✅ Session state

### 3. Application complète (FastAPI + Streamlit)

Gestionnaire de tâches TODO avec backend API et frontend interactif.

**Démarrer le backend:**
```bash
cd fastapi-streamlit-app/backend
pip install -r requirements.txt
python api.py
```

API accessible sur http://localhost:8000

**Démarrer le frontend:**
```bash
cd fastapi-streamlit-app/frontend
pip install -r requirements.txt
streamlit run app.py
```

Interface accessible sur http://localhost:8501

**Fonctionnalités:**
- ✅ CRUD complet des tâches
- ✅ Statuts (À faire, En cours, Terminé)
- ✅ Priorités (Basse, Moyenne, Haute)
- ✅ Filtres en temps réel
- ✅ Statistiques et graphiques
- ✅ Communication REST API
- ✅ Interface responsive

### 4. Application Next.js + React + TypeScript

Gestionnaire de tâches moderne avec Next.js 14, React 18 et TypeScript.

**Prérequis:** Backend FastAPI démarré (voir ci-dessus)

**Installer et démarrer:**
```bash
cd nextjs-app
npm install
npm run dev
```

Interface accessible sur http://localhost:3000

**Fonctionnalités:**
- ✅ Interface moderne avec Tailwind CSS
- ✅ TypeScript pour typage fort
- ✅ Composants React modulaires
- ✅ Navigation par onglets
- ✅ Filtres et recherche en temps réel
- ✅ Statistiques avec KPI et graphiques
- ✅ Design responsive (mobile, tablette, desktop)
- ✅ Gestion des erreurs
- ✅ App Router de Next.js 14

**Avantages vs Streamlit:**
- Plus rapide et scalable
- SEO optimisé
- Meilleure expérience utilisateur
- Plus personnalisable
- Production-ready

## 📋 Détails des exemples

### FastAPI Example (main.py)

**Endpoints disponibles:**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Page d'accueil |
| GET | `/health` | Health check |
| GET | `/users` | Liste utilisateurs |
| GET | `/users/{id}` | Un utilisateur |
| POST | `/users` | Créer utilisateur |
| PUT | `/users/{id}` | Modifier utilisateur |
| DELETE | `/users/{id}` | Supprimer utilisateur |
| GET | `/users/search/by-name?q=` | Recherche par nom |
| GET | `/stats/users` | Statistiques |

**Exemple de requête:**
```bash
# Créer un utilisateur
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "password": "secret123"
  }'

# Obtenir tous les utilisateurs
curl http://localhost:8000/users

# Rechercher
curl http://localhost:8000/users/search/by-name?q=john
```

### Streamlit Example (app.py)

**Composants:**
- 📊 Métriques KPI (ventes, quantité, prix moyen)
- 📈 Graphiques Plotly (lignes, barres, pie, histogramme, heatmap)
- 🎛️ Filtres interactifs (date, produits, régions)
- 📋 Tableau de données avec tri et sélection
- 💾 Export CSV
- ➕ Formulaire d'ajout

**Technologies:**
- Streamlit pour l'interface
- Plotly pour les graphiques
- Pandas pour les données
- NumPy pour les calculs

### Application Complète (FastAPI + Streamlit)

**Architecture:**
```
Frontend (Streamlit)
    ↓ HTTP REST
Backend (FastAPI)
    ↓
Base de données (simulée)
```

**Backend (api.py):**
- API REST complète
- Modèles Pydantic
- Validation automatique
- CORS activé
- Documentation Swagger

**Frontend (app.py):**
- Interface utilisateur intuitive
- Communication avec l'API
- Statistiques en temps réel
- Graphiques interactifs
- Formulaires de création/modification

### Application Next.js

**Architecture:**
```
Frontend (Next.js/React)
    ↓ HTTP REST
Backend (FastAPI)
    ↓
Base de données (simulée)
```

**Frontend (Next.js):**
- Next.js 14 avec App Router
- React 18 avec hooks modernes
- TypeScript pour typage statique
- Tailwind CSS pour styling
- Composants modulaires et réutilisables
- Service API centralisé

**Composants React:**
- `TaskList`: Affichage de la liste avec loader
- `TaskCard`: Carte individuelle de tâche
- `TaskForm`: Formulaire de création
- `Statistics`: Tableau de bord statistiques

**Services:**
- API centralisée avec gestion d'erreurs
- Types TypeScript pour sécurité
- Fetch API avec async/await

## 🛠️ Technologies utilisées

### FastAPI
- Framework web moderne et rapide
- Validation automatique avec Pydantic
- Documentation interactive automatique (Swagger/ReDoc)
- Support async/await
- Type hints Python

### Streamlit
- Framework pour dashboards et data apps
- Composants interactifs
- Support Plotly, Matplotlib, etc.
- Session state pour persistance
- Cache pour performance

### Next.js + React
- Framework React pour production
- Routing basé sur fichiers
- Rendu côté serveur (SSR)
- Optimisations automatiques
- TypeScript intégré

### Autres
- **Uvicorn**: Serveur ASGI pour FastAPI
- **Plotly**: Graphiques interactifs
- **Pandas**: Manipulation de données
- **Requests**: Client HTTP pour Streamlit → FastAPI
- **Tailwind CSS**: Framework CSS utilitaire

## 📚 Apprendre plus

### FastAPI
- Documentation: https://fastapi.tiangolo.com
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- GitHub: https://github.com/tiangolo/fastapi

### Streamlit
- Documentation: https://docs.streamlit.io
- Gallery: https://streamlit.io/gallery
- GitHub: https://github.com/streamlit/streamlit

### Next.js
- Documentation: https://nextjs.org/docs
- Learn: https://nextjs.org/learn
- GitHub: https://github.com/vercel/next.js

### React
- Documentation: https://react.dev
- Tutorial: https://react.dev/learn
- Hooks: https://react.dev/reference/react

### TypeScript
- Documentation: https://www.typescriptlang.org/docs
- Handbook: https://www.typescriptlang.org/docs/handbook/intro.html

### Tailwind CSS
- Documentation: https://tailwindcss.com/docs
- Components: https://tailwindui.com

## 💡 Conseils

### Développement
1. Utiliser `--reload` avec FastAPI pour auto-reload
2. Streamlit se recharge automatiquement
3. Next.js avec `npm run dev` pour hot-reload
4. Tester l'API avec Swagger UI `/docs`
5. Utiliser `st.cache_data` pour performances Streamlit
6. TypeScript pour catch des erreurs à la compilation

### Production
1. Désactiver `reload=True` en FastAPI
2. Configurer CORS correctement (pas `allow_origins=["*"]`)
3. Utiliser une vraie base de données (PostgreSQL, etc.)
4. Ajouter authentification JWT
5. Utiliser HTTPS
6. Containeriser avec Docker

## 🐳 Docker (bonus)

```dockerfile
# Dockerfile FastAPI
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile Streamlit
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

## ❓ Questions fréquentes

**Q: Pourquoi FastAPI + Streamlit?**
A: FastAPI pour une API robuste et performante, Streamlit pour une interface rapide sans JavaScript.

**Q: Peut-on utiliser une vraie base de données?**
A: Oui! Remplacer `tasks_db` par SQLAlchemy + PostgreSQL/MySQL.

**Q: Comment déployer en production?**
A: Docker + Kubernetes, ou services cloud (Heroku, AWS, GCP, Azure).

**Q: Streamlit peut-il gérer beaucoup d'utilisateurs?**
A: Pour beaucoup d'utilisateurs, préférer un frontend React/Vue/Next.js + FastAPI backend.

**Q: Quelle technologie frontend choisir?**
A:
- **Streamlit**: Prototypage rapide, data science, usage interne
- **Next.js/React**: Applications production, SEO important, grande échelle
- Les deux peuvent utiliser la même API FastAPI!

**Q: Next.js vs Streamlit, lequel utiliser?**
A:
- **Streamlit si**: Prototype rapide, dashboard interne, pas de design complexe
- **Next.js si**: Application production, SEO nécessaire, UI personnalisée, scaling

## 🎯 Exercices

1. **Facile**: Ajouter un champ "date d'échéance" aux tâches
2. **Moyen**: Implémenter la recherche de tâches par titre
3. **Difficile**: Ajouter authentification JWT
4. **Expert**: Migrer vers PostgreSQL avec SQLAlchemy

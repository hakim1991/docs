# 🚀 Guide de Démarrage Rapide

## 📦 Installation

### Prérequis
- Python 3.8+ installé
- pip installé

### Option 1: FastAPI seul (API REST)

```bash
# Se placer dans le dossier
cd fastapi-example

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'API
python main.py
```

✅ **API disponible sur:** http://localhost:8000
📚 **Documentation:** http://localhost:8000/docs

### Option 2: Streamlit seul (Dashboard)

```bash
# Se placer dans le dossier
cd streamlit-example

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'application
streamlit run app.py
```

✅ **Dashboard disponible sur:** http://localhost:8501

### Option 3: Application complète (FastAPI + Streamlit)

**Terminal 1 - Backend:**
```bash
cd fastapi-streamlit-app/backend
pip install -r requirements.txt
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd fastapi-streamlit-app/frontend
pip install -r requirements.txt
streamlit run app.py
```

✅ **API:** http://localhost:8000
✅ **Interface:** http://localhost:8501

### Option 4: Application Next.js + React + TypeScript

**Terminal 1 - Backend:**
```bash
cd fastapi-streamlit-app/backend
pip install -r requirements.txt
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd nextjs-app
npm install
npm run dev
```

✅ **API:** http://localhost:8000
✅ **Interface:** http://localhost:3000

## 🎯 Tester les exemples

### FastAPI Example

**1. Ouvrir la documentation interactive:**
http://localhost:8000/docs

**2. Tester les endpoints:**

```bash
# Obtenir tous les utilisateurs
curl http://localhost:8000/users

# Créer un utilisateur
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "age": 25,
    "password": "test123"
  }'

# Obtenir un utilisateur
curl http://localhost:8000/users/1

# Rechercher
curl "http://localhost:8000/users/search/by-name?q=alice"

# Statistiques
curl http://localhost:8000/stats/users
```

**3. Utiliser Swagger UI:**
- Aller sur http://localhost:8000/docs
- Cliquer sur "Try it out" pour tester chaque endpoint
- Voir les réponses en temps réel

### Streamlit Example

**1. Charger les données:**
- Cliquer sur "🔄 Charger/Recharger les données" dans la sidebar

**2. Explorer le dashboard:**
- Visualiser les métriques KPI en haut
- Observer les graphiques de ventes par mois
- Analyser la répartition par produit et région
- Filtrer les données par date, produit et région

**3. Interagir:**
- Modifier les filtres dans la sidebar
- Trier le tableau de données
- Télécharger les données en CSV
- Remplir le formulaire d'ajout (simulation)

### Application Complète (Streamlit)

**1. Vérifier la connexion:**
- L'interface Streamlit doit afficher les statistiques
- Si erreur: vérifier que le backend est démarré

**2. Créer une tâche:**
- Aller dans l'onglet "➕ Ajouter"
- Remplir le formulaire
- Cliquer sur "✅ Créer la tâche"

**3. Gérer les tâches:**
- Onglet "📋 Tâches": voir toutes les tâches
- Changer le statut (À faire → En cours → Terminé)
- Modifier la priorité
- Supprimer des tâches

**4. Analyser:**
- Onglet "📈 Analyse": voir les statistiques et graphiques
- Observer le taux de complétion
- Analyser la répartition par statut et priorité

### Application Next.js

**1. Vérifier la connexion:**
- L'interface Next.js doit afficher les statistiques en haut
- Si erreur: vérifier que le backend est démarré sur http://localhost:8000

**2. Navigation:**
- Onglet **📋 Tâches**: voir et gérer toutes les tâches
- Onglet **➕ Ajouter**: créer de nouvelles tâches
- Onglet **📈 Statistiques**: voir les analyses détaillées

**3. Créer une tâche:**
- Cliquer sur l'onglet "➕ Ajouter"
- Remplir le titre (obligatoire)
- Ajouter une description (optionnelle)
- Choisir la priorité
- Cliquer sur "✅ Créer la tâche"

**4. Gérer les tâches:**
- Utiliser les filtres pour trier par statut et priorité
- Cliquer sur "🔄 Actualiser" pour recharger
- Modifier le statut et la priorité directement dans chaque carte
- Cliquer sur l'icône 🗑️ pour supprimer (avec confirmation)

**5. Voir les statistiques:**
- 4 KPI en haut de la page (Total, À faire, En cours, Terminé)
- Onglet "📈 Statistiques" pour analyses détaillées
- Taux de complétion avec barre de progression
- Répartition par priorité
- Recommandations personnalisées

## 🛠️ Résolution de problèmes

### FastAPI ne démarre pas

**Problème:** Port 8000 déjà utilisé
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Problème:** Module introuvable
```bash
pip install -r requirements.txt --force-reinstall
```

### Streamlit ne démarre pas

**Problème:** Port 8501 déjà utilisé
```bash
streamlit run app.py --server.port 8502
```

**Problème:** Erreur d'import
```bash
pip install --upgrade streamlit pandas plotly
```

### Application complète: Frontend ne se connecte pas au Backend

**Pour Streamlit:**

**1. Vérifier que le backend est démarré:**
```bash
curl http://localhost:8000
```

**2. Vérifier l'URL dans le code:**
```python
# Dans frontend/app.py, ligne 16
API_URL = "http://localhost:8000"
```

**3. Vérifier CORS:**
Le backend doit avoir CORS activé (déjà configuré dans les exemples)

**Pour Next.js:**

**1. Vérifier que le backend est démarré:**
```bash
curl http://localhost:8000/tasks
```

**2. Vérifier le fichier .env.local:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**3. Redémarrer le serveur Next.js après modification de .env.local:**
```bash
npm run dev
```

**4. Vérifier CORS dans le backend:**
Le backend doit accepter les requêtes de localhost:3000 (déjà configuré)

## 📖 Prochaines étapes

### Niveau Débutant
1. Modifier les textes et labels
2. Ajouter de nouveaux champs aux modèles
3. Changer les couleurs des graphiques
4. Personnaliser les couleurs Tailwind dans Next.js

### Niveau Intermédiaire
1. Ajouter de nouveaux endpoints à l'API
2. Créer de nouveaux graphiques dans Streamlit
3. Ajouter validation personnalisée
4. Créer de nouveaux composants React dans Next.js
5. Ajouter animations avec Framer Motion

### Niveau Avancé
1. Intégrer une vraie base de données (PostgreSQL)
2. Ajouter authentification JWT
3. Déployer sur un serveur
4. Ajouter tests unitaires et E2E (Jest, Cypress)
5. Implémenter React Query pour caching côté client
6. Ajouter SEO optimization avec Next.js metadata

## 🎓 Ressources

### Documentation
- **FastAPI:** https://fastapi.tiangolo.com
- **Streamlit:** https://docs.streamlit.io
- **Next.js:** https://nextjs.org/docs
- **React:** https://react.dev
- **TypeScript:** https://www.typescriptlang.org/docs
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Pydantic:** https://docs.pydantic.dev
- **Plotly:** https://plotly.com/python/

### Tutoriels
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- Streamlit Tutorials: https://docs.streamlit.io/library/get-started
- Next.js Learn: https://nextjs.org/learn
- React Tutorial: https://react.dev/learn
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- REST API Best Practices: https://restfulapi.net/

### Communautés
- FastAPI Discord: https://discord.gg/fastapi
- Streamlit Forum: https://discuss.streamlit.io/
- Next.js Discussions: https://github.com/vercel/next.js/discussions
- React Community: https://react.dev/community
- Stack Overflow: Tags `fastapi`, `streamlit`, `next.js`, `reactjs`, `typescript`

## ❓ Questions fréquentes

**Q: Puis-je utiliser ces exemples en production?**
R: Ces exemples sont pour l'apprentissage. Pour la production, ajouter:
- Base de données réelle
- Authentification
- Tests
- Logging
- Monitoring
- HTTPS

**Q: Comment connecter à une vraie base de données?**
R: Utiliser SQLAlchemy avec FastAPI:
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")
```

**Q: Streamlit peut-il gérer plusieurs utilisateurs?**
R: Oui, mais chaque session utilisateur est isolée. Pour une vraie app multi-utilisateurs à grande échelle, considérer React + FastAPI.

**Q: Comment déployer?**
R: Options:
- **Streamlit:** Streamlit Cloud (gratuit)
- **FastAPI:** Heroku, Railway, AWS, GCP, Azure
- **Next.js:** Vercel (recommandé), Netlify, AWS Amplify
- **Les deux:** Docker + Kubernetes

**Q: Next.js ou Streamlit pour mon projet?**
R:
- **Streamlit si:** Prototype rapide, data science, dashboard interne, pas besoin SEO
- **Next.js si:** Application production, SEO important, UI complexe, performance critique
- Les deux utilisent la même API FastAPI!

## 🎉 Amusez-vous bien!

Ces exemples sont conçus pour apprendre. N'hésitez pas à:
- Modifier le code
- Expérimenter
- Casser des choses (et les réparer!)
- Créer vos propres applications

**Bon coding! 💻🚀**

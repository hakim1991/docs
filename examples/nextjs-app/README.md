# 📋 Gestionnaire de Tâches - Next.js + React + FastAPI

Application moderne de gestion de tâches construite avec **Next.js 14**, **React 18**, **TypeScript**, et **Tailwind CSS**, communiquant avec une API backend **FastAPI**.

## ✨ Fonctionnalités

### 📋 Gestion des Tâches
- ✅ Créer, lire, mettre à jour et supprimer des tâches (CRUD complet)
- 🔄 Changer le statut des tâches (À faire → En cours → Terminé)
- 🎯 Définir la priorité (Basse, Moyenne, Haute)
- 🔍 Filtrer par statut et priorité
- 🗑️ Supprimer des tâches avec confirmation

### 📊 Statistiques et Analyse
- 📈 Tableau de bord avec KPI en temps réel
- 📊 Taux de complétion avec barre de progression
- 🎯 Répartition par statut et priorité
- 💡 Recommandations intelligentes basées sur les données

### 🎨 Interface Utilisateur
- 🎨 Design moderne avec Tailwind CSS
- 📱 Interface responsive (mobile, tablette, desktop)
- ⚡ Navigation par onglets intuitive
- 🔄 Actualisation en temps réel
- ⚠️ Gestion des erreurs avec messages clairs

## 🛠️ Technologies Utilisées

### Frontend
- **Next.js 14** - Framework React avec App Router
- **React 18** - Bibliothèque UI avec hooks modernes
- **TypeScript** - Typage statique pour plus de sécurité
- **Tailwind CSS** - Framework CSS utilitaire
- **@tailwindcss/forms** - Styles pour les formulaires

### Backend
- **FastAPI** - API REST moderne et rapide
- **Pydantic** - Validation des données
- **Uvicorn** - Serveur ASGI

## 📦 Installation

### Prérequis

- **Node.js** 18+ et npm/yarn installés
- **Python** 3.8+ installé
- **Backend FastAPI** démarré (voir ci-dessous)

### 1. Démarrer le Backend FastAPI

```bash
# Se placer dans le dossier backend
cd ../fastapi-streamlit-app/backend

# Installer les dépendances Python
pip install -r requirements.txt

# Démarrer l'API
python api.py
```

✅ **Backend disponible sur:** http://localhost:8000
📚 **Documentation API:** http://localhost:8000/docs

### 2. Installer et Démarrer le Frontend Next.js

```bash
# Se placer dans le dossier Next.js
cd nextjs-app

# Installer les dépendances
npm install
# ou avec yarn
yarn install

# Copier le fichier d'environnement
copy .env.local.example .env.local

# Démarrer en mode développement
npm run dev
# ou avec yarn
yarn dev
```

✅ **Application disponible sur:** http://localhost:3000

## 🚀 Utilisation

### 1. Voir les Tâches

- Ouvrir http://localhost:3000
- L'onglet **📋 Tâches** affiche toutes les tâches
- Utiliser les filtres pour trier par statut ou priorité
- Cliquer sur **🔄 Actualiser** pour recharger les données

### 2. Créer une Tâche

1. Cliquer sur l'onglet **➕ Ajouter**
2. Remplir le formulaire :
   - **Titre** (obligatoire)
   - **Description** (optionnelle)
   - **Priorité** (Basse, Moyenne, Haute)
3. Cliquer sur **✅ Créer la tâche**
4. La tâche apparaît instantanément dans la liste

### 3. Modifier une Tâche

- Dans la liste des tâches, utiliser les menus déroulants :
  - **Statut** : Changer entre À faire / En cours / Terminé
  - **Priorité** : Changer entre Basse / Moyenne / Haute
- Les modifications sont instantanées

### 4. Supprimer une Tâche

- Cliquer sur l'icône 🗑️ (poubelle)
- Confirmer la suppression
- La tâche est immédiatement retirée

### 5. Voir les Statistiques

- Onglet **📈 Statistiques** affiche :
  - Total des tâches et répartition par statut
  - Taux de complétion avec barre de progression
  - Répartition par priorité
  - Recommandations personnalisées

## 📁 Structure du Projet

```
nextjs-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Layout principal de l'application
│   │   ├── page.tsx              # Page d'accueil (composant principal)
│   │   └── globals.css           # Styles globaux avec Tailwind
│   ├── components/
│   │   ├── TaskList.tsx          # Liste des tâches avec loader
│   │   ├── TaskCard.tsx          # Carte individuelle d'une tâche
│   │   ├── TaskForm.tsx          # Formulaire de création
│   │   └── Statistics.tsx        # Composant statistiques
│   └── services/
│       └── api.ts                # Service API (fetch, types, erreurs)
├── public/                       # Fichiers statiques
├── package.json                  # Dépendances et scripts
├── tsconfig.json                 # Configuration TypeScript
├── next.config.js                # Configuration Next.js
├── tailwind.config.js            # Configuration Tailwind CSS
├── postcss.config.js             # Configuration PostCSS
├── .env.local.example            # Variables d'environnement (exemple)
└── README.md                     # Ce fichier
```

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env.local` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Changer le Port du Frontend

```bash
# Démarrer sur un port différent
npm run dev -- -p 3001
```

### Changer l'URL de l'API

Modifier `.env.local` :

```env
NEXT_PUBLIC_API_URL=http://votre-api.com
```

## 🎨 Personnalisation

### Modifier les Couleurs

Éditer `tailwind.config.js` :

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#your-color',
      },
    },
  },
};
```

### Ajouter de Nouveaux Champs

1. Mettre à jour les types dans `src/services/api.ts`
2. Modifier le formulaire dans `src/components/TaskForm.tsx`
3. Mettre à jour l'affichage dans `src/components/TaskCard.tsx`

## 📝 Scripts Disponibles

```bash
# Démarrer en mode développement
npm run dev

# Créer un build de production
npm run build

# Démarrer le serveur de production
npm run start

# Lancer le linter
npm run lint
```

## 🐛 Résolution de Problèmes

### Erreur de connexion à l'API

**Problème :** "Erreur de connexion à l'API"

**Solutions :**
1. Vérifier que le backend est démarré sur http://localhost:8000
2. Tester l'API directement : `curl http://localhost:8000/tasks`
3. Vérifier CORS dans le backend (déjà configuré dans les exemples)
4. Vérifier `.env.local` avec la bonne URL

### Port déjà utilisé

**Problème :** Port 3000 occupé

**Solution :**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Ou utiliser un autre port
npm run dev -- -p 3001
```

### Erreurs TypeScript

**Problème :** Erreurs de types

**Solutions :**
```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules
npm install

# Réinitialiser le cache Next.js
rm -rf .next
npm run dev
```

### Styles Tailwind ne s'appliquent pas

**Solutions :**
1. Vérifier que `globals.css` importe Tailwind :
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```
2. Redémarrer le serveur de développement
3. Vérifier `tailwind.config.js` pour les chemins des fichiers

## 🚀 Déploiement

### Vercel (Recommandé)

```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
vercel

# Ou déployer directement depuis GitHub
# 1. Push sur GitHub
# 2. Connecter le repo sur vercel.com
# 3. Ajouter NEXT_PUBLIC_API_URL dans les variables d'environnement
```

### Build Local

```bash
# Créer un build de production
npm run build

# Démarrer le serveur
npm run start
```

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
```

```bash
# Build et run
docker build -t nextjs-todo .
docker run -p 3000:3000 nextjs-todo
```

## 📚 Concepts Clés Utilisés

### Next.js App Router
- Routing basé sur les fichiers dans `src/app/`
- Server Components et Client Components
- Metadata API pour SEO

### React Hooks
- `useState` - Gestion de l'état local
- `useEffect` - Effets de bord et chargement de données
- Custom hooks possibles pour réutilisation

### TypeScript
- Typage fort pour éviter les erreurs
- Interfaces pour les données API
- Types génériques dans les fonctions

### Tailwind CSS
- Classes utilitaires pour styling rapide
- Responsive design avec préfixes (sm:, md:, lg:)
- Dark mode prêt (si activé dans config)

## 🔗 Ressources

### Documentation
- **Next.js** : https://nextjs.org/docs
- **React** : https://react.dev
- **TypeScript** : https://www.typescriptlang.org/docs
- **Tailwind CSS** : https://tailwindcss.com/docs

### Tutoriels
- Next.js Tutorial : https://nextjs.org/learn
- React Hooks : https://react.dev/reference/react
- TypeScript Handbook : https://www.typescriptlang.org/docs/handbook/intro.html

## 🤝 Intégration avec d'Autres Frameworks

Cette application peut être facilement adaptée pour utiliser :

- **Redux** ou **Zustand** pour la gestion d'état globale
- **React Query** ou **SWR** pour le data fetching
- **NextAuth.js** pour l'authentification
- **Prisma** pour accéder à une base de données
- **Framer Motion** pour les animations

## 📄 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 🎉 Bon Coding !

N'hésitez pas à :
- Modifier le code pour l'adapter à vos besoins
- Ajouter de nouvelles fonctionnalités
- Expérimenter avec différents styles
- Intégrer d'autres bibliothèques

**Créé avec ❤️ en utilisant Next.js, React et FastAPI**

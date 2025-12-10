# 🔄 Workflows Git

[← Tags](./infos-git-11-tags-releases.md) | [Index](./infos-git-00-index.md) | [Outils avancés →](./infos-git-13-outils-avances.md)

---

## Table des matières
- [Git Flow](#git-flow)
- [GitHub Flow](#github-flow)
- [GitLab Flow](#gitlab-flow)
- [Trunk-Based Development](#trunk-based-development)
- [Choisir un workflow](#choisir-un-workflow)
- [Conventions de commits](#conventions-de-commits)

---

## Git Flow

### Description

**Git Flow** est un workflow structuré avec plusieurs types de branches pour différentes phases du développement.

```
main (production)
  ├── develop (intégration)
  │     ├── feature/* (nouvelles fonctionnalités)
  │     ├── release/* (préparation release)
  │     └── hotfix/* (corrections urgentes)
  └── hotfix/* (directement depuis main)
```

### Branches principales

```
main
  │  Production, toujours stable
  │  Tagué avec versions (v1.0.0, v1.1.0...)
  │
develop
  │  Intégration, prochaine release
  │  Features mergées ici
```

### Branches de support

**Feature branches**
```bash
# Créer depuis develop
git checkout develop
git checkout -b feature/user-authentication

# Développer
git commit -am "feat: add JWT authentication"
git commit -am "feat: add login endpoint"

# Merger dans develop
git checkout develop
git merge --no-ff feature/user-authentication
git branch -d feature/user-authentication
git push origin develop
```

**Release branches**
```bash
# Créer depuis develop quand prêt pour release
git checkout develop
git checkout -b release/v1.1.0

# Corrections de bugs, pas de nouvelles features
git commit -am "fix: resolve minor issues"
git commit -am "chore: bump version to 1.1.0"

# Merger dans main ET develop
git checkout main
git merge --no-ff release/v1.1.0
git tag -a v1.1.0 -m "Version 1.1.0"

git checkout develop
git merge --no-ff release/v1.1.0

git branch -d release/v1.1.0
git push origin main develop --tags
```

**Hotfix branches**
```bash
# Bug critique en production
git checkout main
git checkout -b hotfix/critical-security-fix

# Fixer
git commit -am "fix: patch security vulnerability"

# Merger dans main ET develop
git checkout main
git merge --no-ff hotfix/critical-security-fix
git tag -a v1.1.1 -m "Hotfix 1.1.1"

git checkout develop
git merge --no-ff hotfix/critical-security-fix

git branch -d hotfix/critical-security-fix
git push origin main develop --tags
```

### Avantages et inconvénients

✅ **Avantages:**
- Structure claire
- Isolation des features
- Releases planifiées
- Hotfixes faciles

❌ **Inconvénients:**
- Complexe
- Beaucoup de branches
- Overhead pour petites équipes
- Pas adapté au déploiement continu

### Quand utiliser Git Flow

✅ **Bon pour:**
- Releases planifiées (ex: tous les 3 mois)
- Plusieurs versions en production
- Grosses équipes
- Produits avec versions (desktop, mobile)

❌ **Pas adapté pour:**
- Déploiement continu (plusieurs fois par jour)
- Petites équipes
- SaaS web (une seule version en prod)

---

## GitHub Flow

### Description

**GitHub Flow** est un workflow **simple et linéaire** orienté déploiement continu.

```
main (toujours déployable)
  ├── feature/A
  ├── feature/B
  └── bugfix/C
```

### Workflow

```bash
# 1. Tout part de main
git checkout main
git pull origin main

# 2. Créer une branche descriptive
git checkout -b feature/add-user-profile

# 3. Développer et commiter régulièrement
git commit -am "feat: add profile model"
git commit -am "feat: add profile API endpoints"
git commit -am "feat: add profile UI"

# 4. Pousser et ouvrir une Pull Request
git push -u origin feature/add-user-profile
# Ouvrir PR sur GitHub

# 5. Discussion, review, tests CI
# Faire des modifications si besoin
git commit -am "fix: address review comments"
git push

# 6. Merger via GitHub (squash optionnel)
# Le merge déclenche le déploiement automatique

# 7. Supprimer la branche
git checkout main
git pull
git branch -d feature/add-user-profile
```

### Principes clés

```
1. main est TOUJOURS déployable
2. Branches descriptives depuis main
3. Push régulièrement
4. Pull Requests pour review
5. Merge = déploiement
6. Déploiement continu
```

### Avantages et inconvénients

✅ **Avantages:**
- Simple et rapide
- Déploiement continu
- Adapté aux équipes de toutes tailles
- Feedback rapide

❌ **Inconvénients:**
- Pas de releases planifiées
- Difficile avec plusieurs versions
- Nécessite bons tests automatisés
- Pas de branche develop

### Quand utiliser GitHub Flow

✅ **Bon pour:**
- SaaS web (une version en prod)
- Déploiement continu
- Petites et moyennes équipes
- Projets avec bons tests CI/CD

---

## GitLab Flow

### Description

**GitLab Flow** combine Git Flow et GitHub Flow avec des **environnements**.

```
main (source de vérité)
  ├── feature/* (développement)
  ├── pre-production (staging)
  └── production (prod)
```

### Avec branches d'environnement

```bash
# 1. Développer sur feature
git checkout main
git checkout -b feature/new-feature
git commit -am "feat: add feature"

# 2. Merger dans main (via MR)
# Tests automatiques sur main

# 3. Promouvoir vers pre-production
git checkout pre-production
git merge main
git push origin pre-production
# Déploiement auto vers staging

# 4. Tests sur staging
# Si OK, promouvoir vers production

git checkout production
git merge pre-production
git push origin production
# Déploiement auto vers prod
```

### Avec releases

```bash
# Pour produits avec versions
main → v1.x → v2.x → v3.x

# Hotfix sur ancienne version
git checkout v1.x
git checkout -b hotfix/security
git commit -am "fix: security patch"

# Merger dans v1.x ET main
git checkout v1.x
git merge hotfix/security
git tag v1.12.5

git checkout main
git cherry-pick <commit>
```

### Avantages et inconvénients

✅ **Avantages:**
- Flexible
- Environnements clairs
- Adapté CI/CD
- Simple

❌ **Inconvénients:**
- Peut devenir complexe
- Merge conflicts possibles
- Nécessite discipline

---

## Trunk-Based Development

### Description

**Trunk-Based Development** : Tout le monde commit sur **main** (trunk) directement ou via branches de très courte durée.

```
main (trunk)
  │
  ├─ commit 1 (direct)
  ├─ commit 2 (direct)
  ├─ [short-lived branch] → commit 3
  ├─ commit 4 (direct)
  └─ ...
```

### Workflow

```bash
# Option 1: Commit direct sur main (petits changements)
git checkout main
git pull --rebase
# Modifier
git commit -am "fix: typo in README"
git push

# Option 2: Branche de courte durée (< 1 jour)
git checkout -b quick-fix
# Développer rapidement (quelques heures max)
git commit -am "feat: add button"
git push -u origin quick-fix

# Merger rapidement (même jour)
git checkout main
git merge quick-fix
git branch -d quick-fix
git push
```

### Feature Flags

Pour grandes features, utiliser des **feature flags**:

```javascript
// Code avec feature flag
if (featureFlags.newDashboard) {
  // Nouveau dashboard (en développement)
  return <NewDashboard />;
} else {
  // Ancien dashboard (stable)
  return <OldDashboard />;
}

// Commit sur main même si pas fini
// La feature est cachée derrière le flag
```

### Avantages et inconvénients

✅ **Avantages:**
- Très simple
- Pas de long-lived branches
- Intégration continue réelle
- Moins de merge conflicts

❌ **Inconvénients:**
- Nécessite feature flags
- Excellents tests requis
- Discipline de l'équipe
- Pas pour tout le monde

---

## Choisir un workflow

### Tableau comparatif

| Critère | Git Flow | GitHub Flow | GitLab Flow | Trunk-Based |
|---------|----------|-------------|-------------|-------------|
| **Complexité** | ⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ |
| **Déploiement continu** | ❌ | ✅ | ✅ | ✅ |
| **Releases planifiées** | ✅ | ❌ | ✅ | ❌ |
| **Taille équipe** | Grande | Tous | Tous | Petite/Moyenne |
| **Courbe apprentissage** | Élevée | Faible | Moyenne | Faible |

### Recommandations

**Startup / SaaS web**
```
→ GitHub Flow ou Trunk-Based
Déploiement continu, simplicité
```

**Produit desktop/mobile**
```
→ Git Flow
Versions multiples, releases planifiées
```

**Entreprise moyenne**
```
→ GitLab Flow
Flexibilité, environnements multiples
```

**Équipe expérimentée**
```
→ Trunk-Based + Feature Flags
Intégration continue maximale
```

---

## Conventions de commits

### Conventional Commits

Format standardisé des messages de commit.

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

```bash
feat:     Nouvelle fonctionnalité
fix:      Correction de bug
docs:     Documentation
style:    Formatage (pas de changement de code)
refactor: Refactoring
perf:     Amélioration performance
test:     Ajout/modification tests
build:    Build system (npm, webpack...)
ci:       CI/CD (GitHub Actions, GitLab CI...)
chore:    Maintenance, dépendances
revert:   Revert d'un commit
```

### Exemples

```bash
# Feature simple
git commit -m "feat: add user login"

# Avec scope
git commit -m "feat(auth): add JWT token validation"

# Avec body
git commit -m "fix: resolve memory leak in cache

The cache was not clearing expired entries,
causing memory to grow over time.

Fixes #123"

# Breaking change
git commit -m "feat!: change API response format

BREAKING CHANGE: API now returns data in { data } wrapper"

# Plusieurs types
git commit -m "feat: add dashboard
fix: resolve navigation bug
docs: update README"
```

### Outils de validation

```bash
# commitlint (valide les messages)
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# commitizen (assistant interactif)
npm install --save-dev commitizen
npx cz  # Au lieu de git commit

# husky (git hooks)
npm install --save-dev husky
# Configure pre-commit hooks
```

---

## Workflow recommandé (complet)

### Pour équipe de 5-10 personnes

```bash
# Structure de branches
main (production)
develop (intégration)
feature/* (nouvelles fonctionnalités)

# Convention de nommage
feature/user-authentication
feature/dashboard-redesign
bugfix/login-error
hotfix/critical-security

# Process
1. Feature depuis develop
   git checkout develop
   git checkout -b feature/my-feature

2. Commits conventionnels
   git commit -m "feat: add feature"

3. Pull Request vers develop
   git push -u origin feature/my-feature
   # Créer PR sur GitHub/GitLab

4. Review + CI
   - 2 approbations minimum
   - Tests passent
   - Pas de conflits

5. Squash merge dans develop
   - 1 commit propre
   - Message de merge descriptif

6. Release depuis develop
   - Créer release branch
   - Tests finaux
   - Merger dans main
   - Tagger (v1.2.0)

7. Déploiement
   - CI/CD automatique depuis main
   - Monitoring

8. Hotfix si nécessaire
   - Depuis main
   - Merger dans main ET develop
```

---

## Commandes de référence rapide

```bash
# Git Flow
git flow init                   # Initialiser
git flow feature start NAME     # Nouvelle feature
git flow feature finish NAME    # Terminer feature
git flow release start VERSION  # Release
git flow hotfix start VERSION   # Hotfix

# GitHub Flow
git checkout main
git pull
git checkout -b feature/name
git push -u origin feature/name
# Pull Request → Merge

# Conventional Commits
git commit -m "feat: add feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update README"
```

---

[← Tags](./infos-git-11-tags-releases.md) | [Index](./infos-git-00-index.md) | [Outils avancés →](./infos-git-13-outils-avances.md)

# 🌐 Remotes et Collaboration

[← Branches](./infos-git-05-branches-merge.md) | [Index](./infos-git-00-index.md) | [Conflits →](./infos-git-07-conflits.md)

---

## Table des matières
- [Concept de remote](#concept-de-remote)
- [Gérer les remotes](#gerer-les-remotes)
- [git push - Envoyer des commits](#git-push---envoyer-des-commits)
- [git pull - Récupérer et merger](#git-pull---recuperer-et-merger)
- [git fetch - Récupérer sans merger](#git-fetch---recuperer-sans-merger)
- [Tracking branches](#tracking-branches)
- [Fork et Pull Requests](#fork-et-pull-requests)

---

## Concept de remote

### Qu'est-ce qu'un remote ?

Un **remote** est un repository Git hébergé sur un serveur (GitHub, GitLab, Bitbucket, serveur perso).

```
┌──────────────────────────────┐
│   VOTRE ORDINATEUR           │
│                              │
│   Repository Local           │
│   main → E                   │
│   A ← B ← C ← D ← E         │
│                              │
└──────────┬───────────────────┘
           │
           │ git push
           │ git pull
           │ git fetch
           ▼
┌──────────────────────────────┐
│   SERVEUR (GitHub)           │
│                              │
│   Repository Remote (origin) │
│   main → E                   │
│   A ← B ← C ← D ← E         │
│                              │
└──────────────────────────────┘
```

### Nomenclature

**origin** : Nom par défaut du remote principal (celui d'où vous avez cloné)

```bash
# Après un clone
git clone https://github.com/user/repo.git

# Le remote "origin" est automatiquement créé
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)
```

---

## Gérer les remotes

### Lister les remotes

```bash
# Lister les remotes
git remote
# origin

# Lister avec les URLs
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)

# Voir les détails d'un remote
git remote show origin
# * remote origin
#   Fetch URL: https://github.com/user/repo.git
#   Push  URL: https://github.com/user/repo.git
#   HEAD branch: main
#   Remote branches:
#     main tracked
#     develop tracked
#   Local branch configured for 'git pull':
#     main merges with remote main
#   Local ref configured for 'git push':
#     main pushes to main (up to date)
```

### Ajouter un remote

```bash
# Ajouter un remote
git remote add origin https://github.com/user/repo.git

# Ajouter un remote avec SSH
git remote add origin git@github.com:user/repo.git

# Ajouter plusieurs remotes
git remote add upstream https://github.com/original/repo.git
git remote add backup https://gitlab.com/user/repo.git

# Vérifier
git remote -v
# origin    https://github.com/user/repo.git (fetch)
# origin    https://github.com/user/repo.git (push)
# upstream  https://github.com/original/repo.git (fetch)
# upstream  https://github.com/original/repo.git (push)
```

### Modifier un remote

```bash
# Changer l'URL d'un remote
git remote set-url origin https://github.com/newuser/repo.git

# Passer de HTTPS à SSH
git remote set-url origin git@github.com:user/repo.git

# Changer seulement l'URL de push
git remote set-url --push origin git@github.com:user/repo.git

# Voir les URLs
git remote get-url origin
# https://github.com/user/repo.git
```

### Renommer et supprimer

```bash
# Renommer un remote
git remote rename origin upstream
git remote rename old-name new-name

# Supprimer un remote
git remote remove origin
git remote rm origin

# Vérifier
git remote -v
```

---

## git push - Envoyer des commits

### Push basique

```bash
# Push vers le remote par défaut
git push

# Push explicite (remote + branche)
git push origin main

# Push et créer l'upstream (tracking)
git push -u origin main
git push --set-upstream origin main

# Après avoir créé l'upstream, juste:
git push
```

### Push d'une nouvelle branche

```bash
# Créer une branche locale
git switch -c feature/new-login

# Faire des commits
git commit -m "feat: add login"

# Pousser vers le remote (crée la branche distante)
git push -u origin feature/new-login

# Maintenant la branche track origin/feature/new-login
git push  # Suffit pour les prochains push
```

### Push avancé

```bash
# Pousser toutes les branches
git push --all

# Pousser les tags
git push --tags

# Pousser tout (branches + tags)
git push --all --tags

# Force push (⚠️ DANGEREUX)
git push --force
git push -f
# Écrase l'historique distant !
# À utiliser seulement sur vos branches personnelles

# Force push avec sécurité (Git 2.30+)
git push --force-with-lease
# Échoue si quelqu'un d'autre a pushé entre temps

# Push vers un remote différent
git push backup main
git push upstream main

# Push une branche locale vers une branche distante différente
git push origin local-branch:remote-branch
git push origin feature:main  # Push feature vers main (dangereux)
```

### Supprimer une branche distante

```bash
# Supprimer une branche sur le remote
git push origin --delete feature/old-branch
git push origin :feature/old-branch  # Ancienne syntaxe
```

### Gérer les rejets

```bash
# Push rejeté (quelqu'un a pushé avant vous)
git push
# To https://github.com/user/repo.git
#  ! [rejected]        main -> main (fetch first)
# error: failed to push some refs

# Solution 1: Pull puis push
git pull
git push

# Solution 2: Pull avec rebase (historique plus propre)
git pull --rebase
git push

# Solution 3: Fetch, review, puis merge
git fetch
git log origin/main..main  # Voir vos commits
git log main..origin/main  # Voir leurs commits
git merge origin/main
git push
```

---

## git pull - Récupérer et merger

### Pull basique

```bash
# Pull = fetch + merge
git pull

# Équivalent à:
git fetch origin
git merge origin/main

# Pull depuis un remote/branche spécifique
git pull origin main
git pull upstream develop
```

### Pull avec rebase

```bash
# Pull avec rebase au lieu de merge (historique plus propre)
git pull --rebase

# Équivalent à:
git fetch origin
git rebase origin/main

# Configurer rebase par défaut
git config --global pull.rebase true

# Maintenant git pull fera automatiquement un rebase
```

### Pull avec options

```bash
# Pull en fast-forward uniquement (échoue si impossible)
git pull --ff-only

# Pull sans fast-forward (force un commit de merge)
git pull --no-ff

# Pull et nettoyer les branches remote supprimées
git pull --prune
git pull -p

# Pull d'une branche spécifique dans la branche courante
git pull origin feature/remote-branch
```

### Différence pull vs fetch

```bash
# git pull = fetch + merge automatique
git pull
# 1. Récupère les changements
# 2. Les merge immédiatement dans votre branche

# git fetch = récupère sans merger (plus sûr)
git fetch
# 1. Récupère les changements
# 2. Les stocke dans origin/main
# 3. Ne touche pas à votre branche locale

# Workflow recommandé:
git fetch
git log ..origin/main  # Voir ce qui a changé
git diff main origin/main  # Voir les différences
git merge origin/main  # Merger quand prêt
```

---

## git fetch - Récupérer sans merger

### Fetch basique

```bash
# Fetcher depuis origin
git fetch

# Fetcher depuis un remote spécifique
git fetch origin
git fetch upstream

# Fetcher une branche spécifique
git fetch origin main
git fetch origin feature/login

# Fetcher toutes les branches de tous les remotes
git fetch --all
```

### Après fetch

```bash
# 1. Fetcher
git fetch origin

# 2. Voir les branches remote
git branch -r
# origin/main
# origin/develop
# origin/feature/login

# 3. Voir ce qui a changé
git log main..origin/main
git log --oneline main..origin/main

# 4. Voir les différences
git diff main origin/main

# 5. Merger quand prêt
git merge origin/main
# Ou
git rebase origin/main
```

### Fetch avancé

```bash
# Fetcher et nettoyer les références obsolètes
git fetch --prune
git fetch -p

# Exemple:
# La branche origin/feature/old a été supprimée sur GitHub
git fetch -p
# [deleted]  (none)     -> origin/feature/old

# Fetcher les tags aussi
git fetch --tags

# Fetch superficiel (shallow)
git fetch --depth=1

# Défaire un fetch (utiliser reflog)
git reflog
git reset --hard HEAD@{before-fetch}
```

---

## Tracking branches

### Qu'est-ce qu'une tracking branch ?

Une **tracking branch** est une branche locale qui "suit" une branche distante.

```
main (local) ←→ tracks ←→ origin/main (remote)
```

### Créer une tracking branch

```bash
# Méthode 1: Lors du premier push
git push -u origin feature
git push --set-upstream origin feature

# Méthode 2: Lors de la création de la branche
git switch -c feature origin/feature
git checkout -b feature origin/feature

# Méthode 3: Pour une branche existante
git branch --set-upstream-to=origin/feature feature
git branch -u origin/feature feature
```

### Voir les tracking branches

```bash
# Voir les branches avec leur upstream
git branch -vv
# * main    a3f7b2c [origin/main] Commit message
#   feature b8e3c1d [origin/feature: ahead 2] WIP
#   local   c9d4e2f No upstream configured

# Légende:
# [origin/main] : track origin/main, à jour
# [origin/feature: ahead 2] : 2 commits en avance sur origin
# [origin/main: behind 3] : 3 commits en retard
# [origin/main: ahead 1, behind 2] : 1 en avance, 2 en retard
# No upstream : pas de tracking configuré
```

### Pourquoi utiliser tracking branches ?

✅ `git push` et `git pull` fonctionnent sans arguments
✅ Git vous informe de l'état (ahead/behind)
✅ Facilite la collaboration

```bash
# Sans tracking:
git push origin feature  # Doit spécifier remote et branche
git pull origin feature

# Avec tracking:
git push  # Suffit !
git pull
```

---

## Fork et Pull Requests

### Workflow Fork + Pull Request

```
┌────────────────────────────────────┐
│  REPOSITORY ORIGINAL (upstream)    │
│  github.com/original-owner/repo    │
└──────────────┬─────────────────────┘
               │ Fork
               ▼
┌────────────────────────────────────┐
│  VOTRE FORK (origin)               │
│  github.com/your-username/repo     │
└──────────────┬─────────────────────┘
               │ Clone
               ▼
┌────────────────────────────────────┐
│  VOTRE ORDINATEUR (local)          │
│  Repository local                  │
└────────────────────────────────────┘
```

### Étapes complètes

#### 1. Forker sur GitHub

1. Aller sur le repository original
2. Cliquer sur "Fork"
3. Le repository est copié sur votre compte

#### 2. Cloner votre fork

```bash
# Cloner votre fork
git clone git@github.com:your-username/repo.git
cd repo

# Vérifier les remotes
git remote -v
# origin  git@github.com:your-username/repo.git (fetch)
# origin  git@github.com:your-username/repo.git (push)
```

#### 3. Ajouter l'upstream

```bash
# Ajouter le repository original comme upstream
git remote add upstream git@github.com:original-owner/repo.git

# Vérifier
git remote -v
# origin    git@github.com:your-username/repo.git (fetch)
# origin    git@github.com:your-username/repo.git (push)
# upstream  git@github.com:original-owner/repo.git (fetch)
# upstream  git@github.com:original-owner/repo.git (push)
```

#### 4. Créer une branche pour votre feature

```bash
# S'assurer d'être à jour avec upstream
git fetch upstream
git checkout main
git merge upstream/main

# Créer une branche
git switch -c feature/new-feature

# Développer
git add .
git commit -m "feat: add new feature"
```

#### 5. Pousser vers votre fork

```bash
# Pousser vers origin (votre fork)
git push -u origin feature/new-feature
```

#### 6. Créer une Pull Request

1. Aller sur GitHub sur votre fork
2. Cliquer sur "Compare & pull request"
3. Vérifier les changements
4. Écrire une description claire
5. Créer la Pull Request

#### 7. Mettre à jour avec upstream

```bash
# Pendant que la PR est en review, upstream peut avoir changé
git fetch upstream
git switch feature/new-feature
git rebase upstream/main

# Si conflits, résoudre puis:
git rebase --continue
git push --force-with-lease
```

#### 8. Après merge de la PR

```bash
# Nettoyer
git switch main
git pull upstream main
git push origin main
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### Maintenir un fork à jour

```bash
# Régulièrement:

# 1. Fetcher upstream
git fetch upstream

# 2. Merger dans main
git switch main
git merge upstream/main

# 3. Pousser vers votre fork
git push origin main

# Script de mise à jour
git fetch upstream && \
git switch main && \
git merge upstream/main && \
git push origin main
```

---

## Workflow de collaboration

### Workflow classique (équipe)

```bash
# 1. Cloner le repository
git clone git@github.com:team/project.git
cd project

# 2. Créer une branche
git switch -c feature/user-auth

# 3. Développer
git commit -am "feat: add JWT authentication"

# 4. Pousser
git push -u origin feature/user-auth

# 5. Créer une Pull Request sur GitHub

# 6. Après review et merge
git switch main
git pull
git branch -d feature/user-auth
```

### Workflow avec rebase (historique propre)

```bash
# Configuration
git config pull.rebase true

# Workflow
git switch -c feature/clean-history

# Commits locaux
git commit -am "feat: part 1"
git commit -am "feat: part 2"

# Avant de pousser, rebaser sur main à jour
git fetch
git rebase origin/main

# Résoudre conflits si nécessaire
git rebase --continue

# Pousser
git push -u origin feature/clean-history
```

---

## Commandes de référence rapide

```bash
# Remotes
git remote -v                   # Lister les remotes
git remote add origin URL       # Ajouter un remote
git remote remove origin        # Supprimer un remote
git remote set-url origin URL   # Changer l'URL

# Push
git push                        # Push vers upstream
git push -u origin main         # Push et set upstream
git push --force-with-lease     # Force push sécurisé
git push origin --delete branch # Supprimer branche remote

# Pull
git pull                        # Fetch + merge
git pull --rebase               # Fetch + rebase
git pull --ff-only              # Fast-forward seulement

# Fetch
git fetch                       # Fetcher depuis origin
git fetch --all                 # Fetcher tous les remotes
git fetch --prune               # Nettoyer les refs

# Tracking
git push -u origin branch       # Set upstream
git branch -vv                  # Voir les upstreams
```

---

## Prochaines étapes

Maintenant que vous savez collaborer, apprenez à gérer les conflits :

- [**Résolution de Conflits**](./infos-git-07-conflits.md) - Gérer les conflits de merge
- [**Stash**](./infos-git-08-stash.md) - Sauvegarder le travail temporairement

---

[← Branches](./infos-git-05-branches-merge.md) | [Index](./infos-git-00-index.md) | [Conflits →](./infos-git-07-conflits.md)

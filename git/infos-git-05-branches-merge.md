# 🌳 Branches et Merge

[← Commandes de base](./infos-git-04-commandes-base.md) | [Index](./infos-git-00-index.md) | [Remotes →](./infos-git-06-remotes-collaboration.md)

---

## Table des matières
- [Qu'est-ce qu'une branche ?](#quest-ce-quune-branche)
- [Créer des branches](#creer-des-branches)
- [Naviguer entre branches](#naviguer-entre-branches)
- [Merger des branches](#merger-des-branches)
- [Supprimer des branches](#supprimer-des-branches)
- [Stratégies de merge](#strategies-de-merge)
- [Visualiser les branches](#visualiser-les-branches)

---

## Qu'est-ce qu'une branche ?

### Concept

Une **branche** est un **pointeur léger** vers un commit. Elle permet de développer des fonctionnalités isolément.

```
main
  ↓
A ← B ← C ← D ← E
```

Créer une branche créé simplement un nouveau pointeur :

```
      main
        ↓
A ← B ← C ← D ← E
              ↑
           feature
```

### Pourquoi utiliser des branches ?

✅ **Isoler le travail** : Développer sans affecter main
✅ **Expérimenter** : Tester des idées sans risque
✅ **Collaborer** : Chacun sa branche
✅ **Organiser** : Une branche par fonctionnalité
✅ **Faciliter la review** : Pull Requests par branche

---

## Créer des branches

### Lister les branches

```bash
# Lister les branches locales
git branch
# * main
#   feature
#   bugfix

# L'étoile (*) indique la branche courante

# Lister avec plus d'infos
git branch -v
# * main    a3f7b2c Add authentication
#   feature b8e3c1d Work in progress
#   bugfix  c9d4e2f Fix login bug

# Lister toutes les branches (locales + remote)
git branch -a
git branch --all

# Lister seulement les branches remote
git branch -r
git branch --remote
```

### Créer une nouvelle branche

```bash
# Créer une branche (mais reste sur la branche courante)
git branch feature/login

# Créer et switcher immédiatement (ancienne méthode)
git checkout -b feature/login

# Créer et switcher (nouvelle méthode, Git 2.23+)
git switch -c feature/login
git switch --create feature/login

# Créer depuis un commit spécifique
git branch feature/login abc123

# Créer depuis une branche distante
git branch feature/login origin/feature/login
```

### Exemple pratique

```bash
# État actuel
git branch
# * main

# Créer une branche pour nouvelle fonctionnalité
git switch -c feature/user-profile
# Switched to a new branch 'feature/user-profile'

# Vérifier
git branch
#   main
# * feature/user-profile

# Faire des modifications
echo "profile code" > profile.js
git add profile.js
git commit -m "feat: add user profile"

# Historique
git log --oneline --graph
# * d1f2e3a (HEAD -> feature/user-profile) feat: add user profile
# * a3f7b2c (main) Initial commit
```

---

## Naviguer entre branches

### Changer de branche

```bash
# Ancienne méthode (checkout)
git checkout main
git checkout feature/login

# Nouvelle méthode (switch, Git 2.23+)
git switch main
git switch feature/login

# Créer et switcher si la branche n'existe pas
git switch -c feature/new-feature

# Revenir à la branche précédente
git switch -
# Comme cd - en bash
```

### Différence checkout vs switch

```bash
# checkout fait plusieurs choses:
git checkout main           # Changer de branche
git checkout abc123         # Se déplacer sur un commit (detached HEAD)
git checkout -- file.txt    # Restaurer un fichier

# switch est spécialisé pour les branches (plus clair)
git switch main             # Changer de branche uniquement

# restore est pour restaurer des fichiers
git restore file.txt        # Restaurer un fichier
```

### Précautions avant de changer de branche

```bash
# ⚠️ Vous devez avoir un working directory propre

# Si modifications non commitées:
git status
# Changes not staged for commit:
#   modified: file.txt

git switch main
# error: Your local changes to the following files would be overwritten by checkout

# Solutions:

# 1. Commiter les changements
git add file.txt
git commit -m "WIP"
git switch main

# 2. Stasher (sauvegarder temporairement)
git stash
git switch main
# Plus tard:
git switch feature
git stash pop

# 3. Forcer (⚠️ perd les modifications)
git switch -f main
git switch --force main
```

---

## Merger des branches

### Merge basique

```bash
# Vous êtes sur main et voulez merger feature
git switch main
git merge feature/login

# Résultat:
# Updating a3f7b2c..d1f2e3a
# Fast-forward
#  login.js | 20 ++++++++++++++++++++
#  1 file changed, 20 insertions(+)
```

### Types de merge

#### 1. Fast-Forward Merge

Quand la branche courante n'a pas divergé.

```
Avant:
      main
        ↓
A ← B ← C
        ↑
      feature

Après (fast-forward):
            main
              ↓
A ← B ← C ← D ← E
```

```bash
git switch main
git merge feature
# Fast-forward

# Désactiver fast-forward (créer un commit de merge)
git merge --no-ff feature
```

#### 2. Three-Way Merge (Merge Commit)

Quand les deux branches ont divergé.

```
Avant:
        main
          ↓
A ← B ← C ← D
      ↖
        E ← F
          ↑
       feature

Après (merge commit):
            main
              ↓
A ← B ← C ← D ← G (merge commit)
      ↖       ↗
        E ← F
       feature
```

```bash
git switch main
git merge feature
# Merge made by the 'recursive' strategy

# Message de merge automatique:
# "Merge branch 'feature' into main"

# Personnaliser le message
git merge feature -m "Merge feature: add login system"
```

#### 3. Squash Merge

Combine tous les commits en un seul.

```bash
# Tous les commits de feature deviennent un seul commit sur main
git switch main
git merge --squash feature
git commit -m "feat: add complete login system"

# Avant:
# feature: A ← B ← C ← D (4 commits)

# Après sur main:
# main: E (1 commit contenant tous les changements)
```

### Merge avec options

```bash
# Merge sans commit automatique (pour review)
git merge --no-commit feature

# Abort d'un merge en cours
git merge --abort

# Continuer après résolution de conflits
git merge --continue

# Stratégie de merge
git merge -s recursive feature
git merge -s ours feature      # Prend notre version
git merge -s theirs feature    # Prend leur version

# Options de stratégie
git merge -X ours feature      # En cas de conflit, prendre notre version
git merge -X theirs feature    # En cas de conflit, prendre leur version
```

---

## Supprimer des branches

### Supprimer une branche locale

```bash
# Supprimer une branche mergée
git branch -d feature/login
# Deleted branch feature/login (was abc123)

# Forcer la suppression (même non mergée)
git branch -D feature/abandoned
git branch --delete --force feature/abandoned
# ⚠️ Attention: perte potentielle de travail !

# Supprimer plusieurs branches
git branch -d feature1 feature2 feature3
```

### Supprimer une branche remote

```bash
# Supprimer une branche sur le remote
git push origin --delete feature/login
git push origin :feature/login  # Ancienne syntaxe

# Nettoyer les références de branches remote supprimées
git fetch --prune
git fetch -p
```

### Nettoyer les branches

```bash
# Lister les branches déjà mergées
git branch --merged
#   feature/done
#   bugfix/resolved
# * main

# Supprimer toutes les branches mergées (sauf main/develop)
git branch --merged | grep -v "\*\|main\|develop" | xargs git branch -d

# Lister les branches non mergées
git branch --no-merged
#   feature/wip
#   experimental

# Script de nettoyage
git branch --merged main | grep -v "^\*\|main\|develop" | xargs -n 1 git branch -d
```

---

## Stratégies de merge

### Git Flow

```
main (production)
  ├── develop (intégration)
  │     ├── feature/A
  │     ├── feature/B
  │     └── feature/C
  ├── release/v1.0
  └── hotfix/critical-bug
```

```bash
# Créer une feature
git switch develop
git switch -c feature/new-login
# Développement...
git commit -am "feat: implement login"

# Merger dans develop
git switch develop
git merge --no-ff feature/new-login
git branch -d feature/new-login

# Créer une release
git switch -c release/v1.0 develop
# Tests, corrections...
git commit -am "chore: bump version"

# Merger dans main et develop
git switch main
git merge --no-ff release/v1.0
git tag v1.0
git switch develop
git merge --no-ff release/v1.0
git branch -d release/v1.0
```

### GitHub Flow (simplifié)

```
main (toujours déployable)
  ├── feature/A
  ├── feature/B
  └── bugfix/C
```

```bash
# 1. Créer une branche depuis main
git switch main
git pull
git switch -c feature/user-auth

# 2. Développer et commiter
git commit -am "feat: add JWT auth"
git commit -am "feat: add login endpoint"

# 3. Pousser et créer une Pull Request
git push -u origin feature/user-auth

# 4. Review, tests, puis merge via GitHub

# 5. Supprimer la branche
git switch main
git pull
git branch -d feature/user-auth
```

### Trunk-Based Development

```
main (trunk)
  ├── short-lived feature branches (< 1 jour)
  └── direct commits
```

```bash
# Branches de très courte durée
git switch -c quick-fix
# Développement rapide (quelques heures max)
git commit -am "fix: resolve issue"
git switch main
git merge quick-fix
git branch -d quick-fix
git push
```

---

## Visualiser les branches

### Graphes en CLI

```bash
# Graphe simple
git log --oneline --graph

# Graphe de toutes les branches
git log --oneline --graph --all

# Graphe détaillé et coloré
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --all

# Résultat:
# * d1f2e3a - (HEAD -> feature) feat: add profile (2 hours ago) <John>
# * c9d4e2f - feat: add avatar (3 hours ago) <John>
# | * b8e3c1d - (main) fix: resolve bug (1 day ago) <Jane>
# |/
# * a3f7b2c - Initial commit (2 days ago) <John>

# Alias recommandé
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --all"

# Utilisation:
git lg
```

### Voir les différences entre branches

```bash
# Commits dans feature mais pas dans main
git log main..feature

# Commits dans main mais pas dans feature
git log feature..main

# Tous les commits différents
git log main...feature

# Fichiers différents
git diff main feature
git diff --name-only main feature
git diff --stat main feature
```

### Outils graphiques

```bash
# Gitk (inclus avec Git)
gitk --all

# Git GUI
git gui
```

---

## Cas pratiques

### Workflow complet

```bash
# 1. Partir de main à jour
git switch main
git pull

# 2. Créer une branche pour nouvelle feature
git switch -c feature/shopping-cart

# 3. Développer
echo "cart code" > cart.js
git add cart.js
git commit -m "feat: add shopping cart"

echo "checkout code" > checkout.js
git add checkout.js
git commit -m "feat: add checkout process"

# 4. Voir l'historique
git log --oneline --graph --all
# * b8e3c1d (HEAD -> feature/shopping-cart) feat: add checkout
# * a3f7b2c feat: add shopping cart
# * d1f2e3a (main) Initial commit

# 5. Merger dans main
git switch main
git merge feature/shopping-cart
# Fast-forward ou merge commit

# 6. Pousser
git push

# 7. Nettoyer
git branch -d feature/shopping-cart
```

### Travailler sur plusieurs features

```bash
# Feature 1
git switch -c feature/user-auth
# Développement...
git commit -m "feat: add auth"

# Besoin de travailler sur autre chose
git switch main
git switch -c feature/dashboard
# Développement...
git commit -m "feat: add dashboard"

# Revenir à feature 1
git switch feature/user-auth
# Continuer le développement...

# Voir toutes les branches
git branch
#   main
# * feature/user-auth
#   feature/dashboard
```

### Merger plusieurs branches

```bash
# Sur develop, merger plusieurs features
git switch develop

git merge feature/login
git merge feature/profile
git merge feature/settings

# Ou avec octopus merge (toutes en une fois)
git merge feature/login feature/profile feature/settings
```

---

## Commandes de référence rapide

```bash
# Lister
git branch                      # Branches locales
git branch -a                   # Toutes les branches
git branch -v                   # Avec détails

# Créer
git branch nom                  # Créer (sans switcher)
git switch -c nom               # Créer et switcher
git checkout -b nom             # Créer et switcher (ancien)

# Naviguer
git switch nom                  # Changer de branche
git switch -                    # Branche précédente
git checkout nom                # Changer (ancien)

# Merger
git merge feature               # Merge basique
git merge --no-ff feature       # Force merge commit
git merge --squash feature      # Squash tous les commits
git merge --abort               # Annuler merge en cours

# Supprimer
git branch -d nom               # Supprimer (si mergée)
git branch -D nom               # Forcer suppression
git push origin --delete nom    # Supprimer remote

# Visualiser
git log --oneline --graph --all # Graphe
git diff main feature           # Différences
```

---

## Prochaines étapes

Maintenant que vous maîtrisez les branches, apprenez à collaborer avec des remotes :

- [**Remotes et Collaboration**](./infos-git-06-remotes-collaboration.md) - Travailler avec GitHub/GitLab
- [**Résolution de Conflits**](./infos-git-07-conflits.md) - Gérer les conflits de merge

---

[← Commandes de base](./infos-git-04-commandes-base.md) | [Index](./infos-git-00-index.md) | [Remotes →](./infos-git-06-remotes-collaboration.md)

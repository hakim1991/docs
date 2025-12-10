# 🎯 Commandes de Base Git

[← Concepts](./infos-git-03-concepts-fondamentaux.md) | [Index](./infos-git-00-index.md) | [Branches →](./infos-git-05-branches-merge.md)

---

## Table des matières
- [git init - Créer un repository](#git-init---creer-un-repository)
- [git clone - Cloner un repository](#git-clone---cloner-un-repository)
- [git status - Voir l'état](#git-status---voir-letat)
- [git add - Ajouter au staging](#git-add---ajouter-au-staging)
- [git commit - Créer un commit](#git-commit---creer-un-commit)
- [git log - Voir l'historique](#git-log---voir-lhistorique)
- [git diff - Voir les différences](#git-diff---voir-les-differences)
- [.gitignore - Ignorer des fichiers](#gitignore---ignorer-des-fichiers)

---

## git init - Créer un repository

### Créer un nouveau repository

```bash
# Créer un dossier et initialiser Git
mkdir mon-projet
cd mon-projet
git init

# Résultat:
# Initialized empty Git repository in /path/to/mon-projet/.git/

# Ou tout en une commande
git init mon-projet
cd mon-projet
```

### Ce qui se passe

```
mon-projet/
└── .git/           ← Repository Git créé
    ├── HEAD
    ├── config
    ├── description
    ├── hooks/
    ├── info/
    ├── objects/
    └── refs/
```

### Options avancées

```bash
# Créer avec une branche initiale spécifique
git init -b main
git init --initial-branch=main

# Créer un repository bare (pour serveur)
git init --bare projet.git
# Pas de working directory, juste la base Git

# Template directory
git init --template=/path/to/template
```

### Réinitialiser un repository existant

```bash
# ⚠️ Supprime tout l'historique Git !
rm -rf .git
git init

# Ou pour garder les fichiers mais recommencer l'historique
# Sauvegarder d'abord !
```

---

## git clone - Cloner un repository

### Cloner depuis un remote

```bash
# Cloner depuis GitHub
git clone https://github.com/user/repo.git

# Cloner avec HTTPS (demande mot de passe)
git clone https://github.com/user/repo.git

# Cloner avec SSH (recommandé)
git clone git@github.com:user/repo.git

# Cloner depuis GitLab
git clone https://gitlab.com/user/repo.git
git clone git@gitlab.com:user/repo.git

# Cloner depuis Bitbucket
git clone https://bitbucket.org/user/repo.git
```

### Options de clonage

```bash
# Cloner dans un dossier spécifique
git clone https://github.com/user/repo.git mon-dossier

# Cloner une branche spécifique
git clone -b develop https://github.com/user/repo.git
git clone --branch feature/login https://github.com/user/repo.git

# Clone superficiel (sans historique complet) - plus rapide
git clone --depth 1 https://github.com/user/repo.git
# Utile pour gros repos, CI/CD

# Clone avec sous-modules
git clone --recurse-submodules https://github.com/user/repo.git

# Clone avec un seul commit (très rapide)
git clone --depth 1 --single-branch https://github.com/user/repo.git
```

### Ce qui se passe lors du clone

```bash
git clone https://github.com/user/repo.git

# 1. Crée le dossier "repo"
# 2. Initialise un repository Git (.git/)
# 3. Ajoute le remote "origin"
# 4. Télécharge tous les commits
# 5. Checkout la branche par défaut (main/master)

# Vérifier le remote configuré
cd repo
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)
```

---

## git status - Voir l'état

### Usage de base

```bash
# Voir l'état du repository
git status

# Résultat typique:
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   file1.txt

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes)
        modified:   file2.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        file3.txt
```

### Format court

```bash
# Status court et concis
git status -s
git status --short

# Résultat:
# M  file1.txt    ← Modifié et staged
#  M file2.txt    ← Modifié mais pas staged
# ?? file3.txt    ← Untracked
# A  file4.txt    ← Ajouté (nouveau)
# D  file5.txt    ← Supprimé
# R  old → new    ← Renommé

# Légende:
# ?? = Untracked
# A  = Added (staged)
# M  = Modified
# D  = Deleted
# R  = Renamed
# C  = Copied
# U  = Updated but unmerged
```

### Options avancées

```bash
# Ignorer les fichiers non trackés
git status --untracked-files=no
git status -uno

# Voir les sous-modules aussi
git status --recurse-submodules

# Format machine (pour scripts)
git status --porcelain
```

---

## git add - Ajouter au staging

### Ajouter des fichiers

```bash
# Ajouter un fichier spécifique
git add file.txt

# Ajouter plusieurs fichiers
git add file1.txt file2.txt file3.txt

# Ajouter tous les fichiers modifiés et nouveaux
git add .

# Ajouter tous les fichiers du repository
git add -A
git add --all

# Ajouter seulement les fichiers modifiés (pas les nouveaux)
git add -u
git add --update

# Ajouter par extension
git add *.js
git add src/*.py

# Ajouter un dossier entier
git add src/
```

### Add interactif

```bash
# Mode interactif
git add -i
git add --interactive

# Menu:
# 1: status       - Voir les fichiers
# 2: update       - Ajouter des fichiers
# 3: revert       - Unstage des fichiers
# 4: add untracked - Ajouter des fichiers non trackés
# 5: patch        - Staging partiel
# 6: diff         - Voir les différences
# 7: quit         - Quitter
```

### Add par patch (staging partiel)

```bash
# Ajouter des morceaux de fichiers (hunks)
git add -p file.txt
git add --patch file.txt

# Pour chaque morceau, choisir:
# y - yes, stage this hunk
# n - no, don't stage
# q - quit
# a - stage this and all remaining hunks
# d - don't stage this and all remaining
# s - split into smaller hunks
# e - manually edit the hunk

# Exemple: vous avez modifié 3 fonctions dans un fichier
# mais ne voulez commiter que 2 d'entre elles
```

### Cas pratiques

```bash
# 1. Premier commit (tout ajouter)
git add .
git commit -m "Initial commit"

# 2. Ajouter seulement les fichiers .js modifiés
git add -u '*.js'

# 3. Ajouter tout sauf un fichier
git add .
git reset HEAD unwanted.txt

# 4. Ajouter avec vérification
git add -n file.txt  # Dry-run (simulation)
git add file.txt     # Si OK
```

---

## git commit - Créer un commit

### Commit basique

```bash
# Commit avec message court
git commit -m "Add user authentication"

# Commit avec message multi-lignes
git commit -m "Add user authentication" -m "- Implement JWT tokens" -m "- Add login endpoint"

# Ouvrir l'éditeur pour un message long
git commit
# Écrivez le message, sauvegardez et fermez

# Commit avec add automatique (fichiers trackés seulement)
git commit -am "Fix bug in login"
git commit -a -m "Fix bug in login"
```

### Format de message recommandé

```
Type: Sujet court (50 caractères max)

Description plus détaillée si nécessaire (72 caractères par ligne).
Expliquez le "pourquoi" plus que le "quoi".

- Point 1
- Point 2
- Point 3

Fixes #123
```

**Types de commits :**
```bash
feat:     Nouvelle fonctionnalité
fix:      Correction de bug
docs:     Documentation
style:    Formatage, point-virgules, etc.
refactor: Refactoring du code
test:     Ajout de tests
chore:    Maintenance, outils

# Exemples:
git commit -m "feat: add user profile page"
git commit -m "fix: resolve null pointer exception in auth"
git commit -m "docs: update README with installation steps"
```

### Commit avancé

```bash
# Amender le dernier commit (ajouter des fichiers oubliés)
git add forgotten-file.txt
git commit --amend --no-edit
# Garde le même message

# Amender et changer le message
git commit --amend -m "Nouveau message"

# Commit vide (utile pour CI/CD)
git commit --allow-empty -m "Trigger CI"

# Commit avec date spécifique
git commit --date="2024-01-01 10:00:00" -m "Backdated commit"

# Commit au nom de quelqu'un d'autre
git commit --author="John Doe <john@example.com>" -m "Commit by John"
```

### Bonnes pratiques de commit

```bash
# ❌ MAUVAIS
git commit -m "fix"
git commit -m "changes"
git commit -m "WIP"
git commit -m "update file"

# ✅ BON
git commit -m "fix: resolve login button alignment on mobile"
git commit -m "feat: add password reset functionality"
git commit -m "refactor: extract auth logic into separate service"
git commit -m "docs: add API documentation for user endpoints"

# Commits atomiques (une chose à la fois)
# ✅ BON
git add auth.js
git commit -m "feat: add JWT token validation"

git add login.html
git commit -m "feat: create login form UI"

# ❌ MAUVAIS (tout mélangé)
git add auth.js login.html dashboard.js
git commit -m "Add authentication and dashboard"
```

---

## git log - Voir l'historique

### Log basique

```bash
# Voir tous les commits
git log

# Résultat:
commit a3f7b2c891e4567f890123456789abcdef012345
Author: John Doe <john@example.com>
Date:   Mon Jan 15 14:30:00 2024 +0100

    feat: add user authentication

commit b8e3c1d902f5678a901234567890bcdef0123456
Author: Jane Smith <jane@example.com>
Date:   Sun Jan 14 10:15:00 2024 +0100

    fix: resolve database connection issue
```

### Log formaté

```bash
# Une ligne par commit
git log --oneline
# a3f7b2c feat: add user authentication
# b8e3c1d fix: resolve database connection issue

# Avec graphe
git log --oneline --graph
git log --oneline --graph --all

# Résultat:
* a3f7b2c (HEAD -> main) feat: add user authentication
* b8e3c1d (origin/main) fix: resolve database issue
*   c9d4e2f Merge branch 'feature'
|\
| * d0e5f3a feat: add new component
|/
* e1f6g4b Initial commit

# Avec décoration (branches, tags)
git log --oneline --graph --decorate --all

# Format personnalisé
git log --pretty=format:"%h - %an, %ar : %s"
# a3f7b2c - John Doe, 2 hours ago : feat: add user authentication

# Format complet personnalisé
git log --pretty=format:"%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)%d%Creset %C(bold blue)<%an>%Creset" --date=short
```

### Filtrer les logs

```bash
# Derniers N commits
git log -5          # 5 derniers commits
git log -n 5        # Même chose

# Depuis une date
git log --since="2024-01-01"
git log --after="2024-01-01"
git log --since="2 weeks ago"
git log --since="3 days ago"

# Jusqu'à une date
git log --until="2024-01-31"
git log --before="yesterday"

# Par auteur
git log --author="John"
git log --author="john@example.com"

# Par message de commit
git log --grep="auth"
git log --grep="fix"

# Par fichier
git log -- file.txt
git log --follow -- file.txt  # Suit les renommages

# Par contenu (recherche dans les diffs)
git log -S "function login"
git log -G "regex pattern"

# Commits qui ont modifié un fichier
git log --all -- path/to/file.txt
```

### Log avancé

```bash
# Voir les statistiques
git log --stat
# Affiche les fichiers modifiés et nombre de lignes

# Voir les différences complètes
git log -p
git log --patch

# Combiner filtres
git log --oneline --author="John" --since="1 week ago" --grep="fix"

# Commits entre deux points
git log main..feature
# Commits dans feature mais pas dans main

git log feature..main
# Commits dans main mais pas dans feature

# Commits sur toutes les branches
git log --all

# Format graph détaillé (très utile)
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
```

---

## git diff - Voir les différences

### Diff basique

```bash
# Différences entre working directory et staging
git diff
# Montre les modifications non stagées

# Différences entre staging et dernier commit
git diff --staged
git diff --cached

# Différences entre working directory et dernier commit
git diff HEAD
```

### Diff entre commits/branches

```bash
# Entre deux commits
git diff abc123 def456
git diff abc123..def456

# Entre branches
git diff main feature
git diff main..feature

# Entre branche locale et remote
git diff main origin/main

# Depuis un commit jusqu'à maintenant
git diff abc123 HEAD
```

### Diff sur des fichiers spécifiques

```bash
# Un fichier spécifique
git diff file.txt
git diff --staged file.txt

# Plusieurs fichiers
git diff file1.txt file2.txt

# Un dossier
git diff src/

# Statistiques uniquement
git diff --stat
git diff --stat main feature

# Noms de fichiers uniquement
git diff --name-only
git diff --name-status
```

### Diff avancé

```bash
# Diff par mot (au lieu de par ligne)
git diff --word-diff
git diff --color-words

# Ignorer les espaces
git diff -w
git diff --ignore-all-space

# Ignorer les changements d'espaces en fin de ligne
git diff --ignore-space-at-eol

# Afficher le contexte (lignes avant/après)
git diff -U10  # 10 lignes de contexte
git diff --unified=10

# Diff avec outil externe (vimdiff, meld, etc.)
git difftool
git difftool --tool=vimdiff
```

### Exemples pratiques

```bash
# Voir ce qui sera commité
git diff --staged

# Voir toutes les modifications depuis le dernier commit
git diff HEAD

# Voir ce qui a changé dans une branche depuis main
git diff main..feature

# Comparer deux fichiers
git diff main:file.txt feature:file.txt

# Voir les conflits
git diff --name-only --diff-filter=U
```

---

## .gitignore - Ignorer des fichiers

### Créer un .gitignore

```bash
# Créer le fichier
touch .gitignore

# Ou avec contenu initial
cat > .gitignore << 'EOF'
# Node
node_modules/
npm-debug.log

# Python
__pycache__/
*.pyc

# IDE
.vscode/
.idea/
EOF
```

### Patterns courants

```gitignore
# Fichiers et dossiers spécifiques
secret.txt
/config.local.js

# Extensions
*.log
*.tmp
*.bak

# Dossiers
node_modules/
dist/
build/
.cache/

# Patterns
**/temp/        # temp dans n'importe quel sous-dossier
*.swp           # Fichiers vim
.DS_Store       # macOS
Thumbs.db       # Windows

# Exceptions (ne pas ignorer)
!important.log
!/config/production.js

# Commenter
# Ceci est un commentaire
```

### .gitignore par langage/framework

**Node.js / JavaScript:**
```gitignore
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build
dist/
build/
.next/
out/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test
coverage/
.nyc_output/
```

**Python:**
```gitignore
# Byte-compiled / optimized
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
ENV/
.venv/

# Distribution / packaging
dist/
build/
*.egg-info/

# Pytest
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/

# Environment
.env
```

**Java:**
```gitignore
# Compiled
*.class
*.jar
*.war

# Build
target/
build/
out/

# IDE
.idea/
*.iml
.classpath
.project
.settings/

# Logs
*.log
```

### .gitignore global

```bash
# Créer un .gitignore global (pour tous vos projets)
cat > ~/.gitignore_global << 'EOF'
# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
Desktop.ini

# Logs
*.log
EOF

# Configurer Git pour l'utiliser
git config --global core.excludesfile ~/.gitignore_global
```

### Gérer les fichiers déjà trackés

```bash
# Si vous ajoutez un fichier à .gitignore mais qu'il est déjà tracké

# Supprimer du staging (mais garder le fichier)
git rm --cached file.txt

# Supprimer un dossier
git rm -r --cached node_modules/

# Puis commit
git commit -m "chore: update .gitignore"

# Le fichier reste local mais ne sera plus tracké
```

### Vérifier ce qui est ignoré

```bash
# Voir quels fichiers sont ignorés
git status --ignored

# Vérifier si un fichier est ignoré
git check-ignore file.txt

# Voir quelle règle ignore un fichier
git check-ignore -v file.txt
# .gitignore:3:*.txt	file.txt
```

---

## Workflow complet

### Première utilisation

```bash
# 1. Créer un nouveau projet
mkdir mon-projet
cd mon-projet
git init

# 2. Créer des fichiers
echo "# Mon Projet" > README.md
echo "console.log('Hello');" > app.js

# 3. Voir l'état
git status
# Untracked files: README.md, app.js

# 4. Ajouter au staging
git add .

# 5. Voir l'état
git status
# Changes to be committed: README.md, app.js

# 6. Commit
git commit -m "Initial commit"

# 7. Voir l'historique
git log --oneline
# a3f7b2c (HEAD -> main) Initial commit
```

### Workflow quotidien

```bash
# 1. Vérifier l'état
git status

# 2. Modifier des fichiers
# (éditer app.js dans votre éditeur)

# 3. Voir les modifications
git diff

# 4. Ajouter au staging
git add app.js

# 5. Voir ce qui sera commité
git diff --staged

# 6. Commit
git commit -m "feat: add login function"

# 7. Voir l'historique
git log --oneline --graph
```

---

## Commandes de référence rapide

```bash
# Repository
git init                        # Créer un repo
git clone URL                   # Cloner un repo

# État
git status                      # Voir l'état
git status -s                   # État court

# Staging
git add file.txt                # Ajouter un fichier
git add .                       # Ajouter tout
git add -p                      # Staging partiel

# Commit
git commit -m "message"         # Commit simple
git commit -am "message"        # Add + commit
git commit --amend              # Modifier le dernier commit

# Historique
git log                         # Historique complet
git log --oneline               # Une ligne par commit
git log --graph --all           # Graphe des branches

# Différences
git diff                        # Modifs non stagées
git diff --staged               # Modifs stagées
git diff main feature           # Entre branches
```

---

## Prochaines étapes

Maintenant que vous maîtrisez les commandes de base, apprenez à travailler avec des branches :

- [**Branches et Merge**](./infos-git-05-branches-merge.md) - Travailler avec des branches
- [**Remotes et Collaboration**](./infos-git-06-remotes-collaboration.md) - Collaborer avec Git

---

[← Concepts](./infos-git-03-concepts-fondamentaux.md) | [Index](./infos-git-00-index.md) | [Branches →](./infos-git-05-branches-merge.md)

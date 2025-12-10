# 🧠 Concepts Fondamentaux de Git

[← Configuration](./infos-git-02-configuration.md) | [Index](./infos-git-00-index.md) | [Commandes de base →](./infos-git-04-commandes-base.md)

---

## Table des matières
- [Repository (Dépôt)](#repository-depot)
- [Les trois états de Git](#les-trois-etats-de-git)
- [Working Directory, Staging Area, Repository](#working-directory-staging-area-repository)
- [Commits et SHA](#commits-et-sha)
- [Branches](#branches)
- [HEAD et pointeurs](#head-et-pointeurs)
- [Remote repositories](#remote-repositories)
- [Cycle de vie des fichiers](#cycle-de-vie-des-fichiers)

---

## Repository (Dépôt)

### Qu'est-ce qu'un repository Git ?

Un **repository** (ou dépôt) est un espace de stockage pour votre projet qui contient :
- Tous les fichiers du projet
- L'historique complet des modifications
- Les branches
- Les métadonnées Git (dans le dossier `.git/`)

```
mon-projet/
├── .git/              ← Repository Git (base de données)
│   ├── objects/       ← Tous les commits, fichiers
│   ├── refs/          ← Références (branches, tags)
│   ├── HEAD           ← Pointeur vers la branche courante
│   └── config         ← Configuration locale
├── src/               ← Vos fichiers de travail
├── README.md
└── .gitignore
```

### Types de repositories

**Repository local** : Sur votre machine
```bash
# Créer un nouveau repository local
git init mon-projet
cd mon-projet
```

**Repository distant (remote)** : Sur un serveur (GitHub, GitLab, etc.)
```bash
# Cloner un repository distant
git clone https://github.com/user/projet.git
```

**Repository bare** : Sans working directory (pour serveurs)
```bash
# Créer un repository bare (serveur)
git init --bare projet.git
```

---

## Les trois états de Git

Git a **trois états principaux** pour vos fichiers :

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Working Directory  →  Staging Area  →  Repository         │
│  (Modified)            (Staged)         (Committed)         │
│                                                             │
│  Fichiers modifiés    Fichiers prêts   Fichiers            │
│  mais non ajoutés     à être commités  sauvegardés         │
│                                                             │
│     git add →           git commit →                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1. Modified (Modifié)
Vous avez changé le fichier mais pas encore ajouté à Git.

### 2. Staged (Indexé)
Vous avez marqué le fichier pour être inclus dans le prochain commit.

### 3. Committed (Validé)
Le fichier est sauvegardé de façon permanente dans la base Git.

---

## Working Directory, Staging Area, Repository

### Schéma détaillé

```
┌──────────────────────────────────────────────────────────────┐
│                    WORKING DIRECTORY                         │
│  (Répertoire de travail - ce que vous voyez)                │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ file1.js│  │ file2.js│  │ file3.js│  │ file4.js│      │
│  │ modifié │  │ modifié │  │ inchangé│  │ nouveau │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
│       │            │                           │            │
│       │ git add    │ git add                   │ git add    │
│       ▼            ▼                           ▼            │
└──────────────────────────────────────────────────────────────┘
                     │
                     │
┌──────────────────────────────────────────────────────────────┐
│                    STAGING AREA (Index)                      │
│  (Zone de transit - fichiers prêts à être commités)         │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
│  │ file1.js│  │ file2.js│  │ file4.js│                    │
│  │  staged │  │  staged │  │  staged │                    │
│  └─────────┘  └─────────┘  └─────────┘                    │
│       │            │            │                            │
│       └────────────┴────────────┘                           │
│                    │ git commit -m "message"                │
│                    ▼                                         │
└──────────────────────────────────────────────────────────────┘
                     │
                     │
┌──────────────────────────────────────────────────────────────┐
│                    REPOSITORY (.git)                         │
│  (Base de données - historique permanent)                   │
│                                                              │
│  Commit 3: abc123 "Add file4"                               │
│  Commit 2: def456 "Update file2"                            │
│  Commit 1: ghi789 "Initial commit"                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Exemple pratique

```bash
# État initial
git status
# On branch main
# nothing to commit, working tree clean

# Modifier un fichier
echo "nouveau contenu" >> file1.txt

# État: Modified (Working Directory)
git status
# Changes not staged for commit:
#   modified:   file1.txt

# Ajouter au staging
git add file1.txt

# État: Staged (Staging Area)
git status
# Changes to be committed:
#   modified:   file1.txt

# Créer un commit
git commit -m "Mise à jour file1"

# État: Committed (Repository)
git status
# nothing to commit, working tree clean
```

---

## Commits et SHA

### Qu'est-ce qu'un commit ?

Un **commit** est un instantané (snapshot) de votre projet à un moment donné.

```
Commit
├── SHA (identifiant unique): a3f7b2c...
├── Auteur: John Doe <john@example.com>
├── Date: 2024-01-15 14:30:00
├── Message: "Add user authentication"
├── Pointeur vers commit parent
└── Snapshot des fichiers (tree)
```

### SHA-1 (Secure Hash Algorithm)

Chaque commit a un **identifiant unique** de 40 caractères hexadécimaux.

```bash
# SHA complet (40 caractères)
commit a3f7b2c891e4567f890123456789abcdef012345

# SHA court (7 premiers caractères, généralement suffisant)
commit a3f7b2c

# Les 7 premiers caractères sont généralement uniques dans un projet
```

### Anatomie d'un commit

```bash
# Voir un commit en détail
git show a3f7b2c

# Résultat:
commit a3f7b2c891e4567f890123456789abcdef012345
Author: John Doe <john@example.com>
Date:   Mon Jan 15 14:30:00 2024 +0100

    Add user authentication

    - Implement JWT tokens
    - Add login/logout endpoints
    - Create user model

diff --git a/src/auth.js b/src/auth.js
new file mode 100644
index 0000000..abcdef0
--- /dev/null
+++ b/src/auth.js
@@ -0,0 +1,20 @@
+function login(user, password) {
+    // Implementation...
+}
```

### Graphe de commits

Les commits forment un **graphe dirigé acyclique** (DAG).

```
                main
                  ↓
    A ← B ← C ← D ← E
         ↖
          F ← G
            ↑
         feature
```

Chaque commit pointe vers son **parent**.

```bash
# Voir le graphe
git log --oneline --graph --all

# Résultat:
* e2a7b9c (HEAD -> main) E: Add feature X
* d1c8f3e D: Fix bug in auth
*   c3b5a2d C: Merge feature branch
|\
| * g9f4e1a (feature) G: Update UI
| * f8d2c0b F: Add new component
|/
* b7a1d4c B: Initial setup
* a0c9e6f A: First commit
```

---

## Branches

### Qu'est-ce qu'une branche ?

Une **branche** est simplement un **pointeur mobile** vers un commit.

```
                main (pointeur)
                  ↓
    A ← B ← C ← D ← E
```

Quand vous créez un nouveau commit, la branche avance :

```bash
# Avant commit
main → E

# Après commit F
main → F (nouveau commit)
       ↑
       E
```

### Branches multiples

```
                main
                  ↓
    A ← B ← C ← D ← E
         ↖
          F ← G ← H
                ↑
             feature
```

**Points clés:**
- Les branches sont légères (juste un pointeur)
- Créer/supprimer une branche est quasi-instantané
- Vous pouvez avoir des centaines de branches sans impact

### Pourquoi utiliser des branches ?

```
main (production)
  ↓
  A ← B ← C ← D ← E
       ↖
        F ← G        ← feature/login
         ↖
          H ← I      ← feature/dashboard
```

**Avantages:**
- Travailler sur plusieurs fonctionnalités en parallèle
- Isoler les changements
- Tester sans affecter la production
- Collaborer sans conflits

---

## HEAD et pointeurs

### HEAD : Où suis-je ?

**HEAD** est un pointeur spécial qui indique **où vous êtes** dans votre repository.

```
HEAD → main → E
               ↑
           A ← B ← C ← D ← E
```

HEAD pointe généralement vers une **branche** (qui pointe vers un commit).

### Détached HEAD

Quand HEAD pointe directement vers un commit (pas de branche) :

```
       main
         ↓
    A ← B ← C ← D ← E
              ↑
             HEAD (detached)
```

```bash
# Créer un detached HEAD
git checkout abc123

# Message:
# You are in 'detached HEAD' state...

# Revenir à une branche
git checkout main
```

### Références relatives

```bash
# Références par rapport à HEAD

HEAD       # Commit courant
HEAD~1     # Parent de HEAD (1 commit avant)
HEAD~2     # Grand-parent (2 commits avant)
HEAD~3     # 3 commits avant

# Équivalent avec ^
HEAD^      # Parent de HEAD
HEAD^^     # Grand-parent
HEAD^^^    # 3 commits avant

# Différence avec plusieurs parents (après merge)
HEAD^1     # Premier parent
HEAD^2     # Deuxième parent (branche mergée)
```

```
        main
          ↓
    A ← B ← C ← D ← E
             ↑   ↑   ↑
          HEAD~2 HEAD~1 HEAD
```

### Pointeurs de branches

```bash
# main pointe vers le dernier commit de main
main

# origin/main pointe vers le dernier commit de origin
origin/main

# feature pointe vers le dernier commit de feature
feature

# Références complètes
refs/heads/main        # Branche locale
refs/remotes/origin/main  # Branche remote
refs/tags/v1.0         # Tag
```

---

## Remote repositories

### Qu'est-ce qu'un remote ?

Un **remote** est un repository hébergé sur un serveur (GitHub, GitLab, etc.).

```
┌─────────────────────────────────┐
│   REPOSITORY LOCAL              │
│                                 │
│   main → E                      │
│   A ← B ← C ← D ← E            │
│                                 │
└────────────┬────────────────────┘
             │ git push
             │ git pull
             ▼
┌─────────────────────────────────┐
│   REPOSITORY DISTANT (origin)   │
│                                 │
│   main → E                      │
│   A ← B ← C ← D ← E            │
│                                 │
└─────────────────────────────────┘
```

### Branches locales vs remote

```bash
# Branches locales
main          # Votre branche locale
feature       # Votre branche de développement

# Branches remote (lecture seule localement)
origin/main      # État de main sur origin
origin/feature   # État de feature sur origin

# Tracking branches
# Votre branche locale "main" track "origin/main"
main → tracks → origin/main
```

### Workflow avec remote

```
1. Développement local
   main → E (local)

2. Quelqu'un d'autre push sur origin
   origin/main → F

3. Fetch (récupérer l'info)
   main → E (local)
   origin/main → F (remote)

4. Pull (merge)
   main → G (merge de E et F)
   origin/main → F

5. Push
   main → G
   origin/main → G
```

---

## Cycle de vie des fichiers

### États des fichiers

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  Untracked  →  Unmodified  →  Modified  →  Staged  │
│  (nouveau)     (suivi)        (modifié)    (indexé)  │
│                                                      │
└──────────────────────────────────────────────────────┘

     │              │             │            │
     │              │             │            │
git add            edit         git add    git commit
     │              │             │            │
     ▼              ▼             ▼            ▼
```

### Diagramme détaillé

```
┌─────────────┐
│  UNTRACKED  │ ← Nouveau fichier, Git ne le connaît pas
│  (nouveau)  │
└──────┬──────┘
       │ git add
       ▼
┌─────────────┐
│   STAGED    │ ← Ajouté au staging (sera commité)
│  (indexé)   │
└──────┬──────┘
       │ git commit
       ▼
┌─────────────┐
│ UNMODIFIED  │ ← Commit, fichier non modifié
│   (suivi)   │
└──────┬──────┘
       │ edit file
       ▼
┌─────────────┐
│  MODIFIED   │ ← Fichier modifié, pas encore staged
│  (modifié)  │
└──────┬──────┘
       │ git add
       ▼
┌─────────────┐
│   STAGED    │ ← Prêt à être commité
│  (indexé)   │
└──────┬──────┘
       │ git commit
       ▼
┌─────────────┐
│ UNMODIFIED  │ ← Cycle recommence
└─────────────┘
```

### Exemple pratique

```bash
# 1. Créer un nouveau fichier (UNTRACKED)
echo "hello" > new.txt
git status
# Untracked files:
#   new.txt

# 2. Ajouter au staging (STAGED)
git add new.txt
git status
# Changes to be committed:
#   new file:   new.txt

# 3. Commit (UNMODIFIED)
git commit -m "Add new.txt"
git status
# nothing to commit, working tree clean

# 4. Modifier le fichier (MODIFIED)
echo "world" >> new.txt
git status
# Changes not staged for commit:
#   modified:   new.txt

# 5. Ajouter au staging (STAGED)
git add new.txt

# 6. Commit (UNMODIFIED)
git commit -m "Update new.txt"
```

---

## Concepts visuels résumés

### Vue d'ensemble complète

```
┌────────────────────────────────────────────────────────────┐
│                    DÉVELOPPEUR                             │
│                                                            │
│  Working Directory                                         │
│  ┌──────────────┐                                         │
│  │ file1.js     │  Modified                               │
│  │ file2.js     │  Modified                               │
│  └──────────────┘                                         │
│         │                                                  │
│         │ git add                                          │
│         ▼                                                  │
│  Staging Area                                             │
│  ┌──────────────┐                                         │
│  │ file1.js     │  Staged                                 │
│  │ file2.js     │  Staged                                 │
│  └──────────────┘                                         │
│         │                                                  │
│         │ git commit                                       │
│         ▼                                                  │
│  Local Repository                                         │
│  ┌──────────────────────────────┐                        │
│  │ main → E                      │                        │
│  │ A ← B ← C ← D ← E            │                        │
│  └──────────────────────────────┘                        │
│         │                                                  │
│         │ git push                                         │
│         ▼                                                  │
└────────────────────────────────────────────────────────────┘
         │
         │
┌────────────────────────────────────────────────────────────┐
│              REMOTE REPOSITORY (GitHub)                    │
│                                                            │
│  ┌──────────────────────────────┐                        │
│  │ main → E                      │                        │
│  │ A ← B ← C ← D ← E            │                        │
│  └──────────────────────────────┘                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Points clés à retenir

✅ **Repository** : Base de données contenant tout l'historique

✅ **Trois états** : Modified → Staged → Committed

✅ **Commit** : Snapshot immuable avec SHA unique

✅ **Branche** : Pointeur léger vers un commit

✅ **HEAD** : Indique où vous êtes actuellement

✅ **Remote** : Repository distant (GitHub, GitLab, etc.)

✅ **Cycle de vie** : Untracked → Staged → Committed → Modified

---

## Prochaines étapes

Maintenant que vous comprenez les concepts, passez à la pratique :

- [**Commandes de Base**](./infos-git-04-commandes-base.md) - Créer vos premiers commits
- [**Branches et Merge**](./infos-git-05-branches-merge.md) - Travailler avec des branches

---

[← Configuration](./infos-git-02-configuration.md) | [Index](./infos-git-00-index.md) | [Commandes de base →](./infos-git-04-commandes-base.md)

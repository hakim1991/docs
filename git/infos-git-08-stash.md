# 💼 Stash - Travail Temporaire

[← Conflits](./infos-git-07-conflits.md) | [Index](./infos-git-00-index.md) | [Historique →](./infos-git-09-historique-navigation.md)

---

## Table des matières
- [Qu'est-ce que le stash ?](#quest-ce-que-le-stash)
- [Sauvegarder le travail](#sauvegarder-le-travail)
- [Voir les stash](#voir-les-stash)
- [Appliquer un stash](#appliquer-un-stash)
- [Supprimer des stash](#supprimer-des-stash)
- [Cas d'usage pratiques](#cas-dusage-pratiques)

---

## Qu'est-ce que le stash ?

### Définition

Le **stash** permet de **sauvegarder temporairement** vos modifications en cours sans créer de commit.

```
Working Directory (modifié)
         ↓
    git stash
         ↓
Working Directory (propre) + Stash (modifications sauvegardées)
```

### Quand utiliser le stash ?

✅ Changer de branche rapidement
✅ Pull sans conflits
✅ Expérimenter sans commit
✅ Sauvegarder le travail en cours
✅ Nettoyer le working directory

---

## Sauvegarder le travail

### Stash basique

```bash
# Stasher les modifications (tracked files)
git stash
# Saved working directory and index state WIP on main: abc123 Last commit message

# Ou avec un message descriptif
git stash save "Work in progress on login feature"
# Mieux pour s'y retrouver

# Nouvelle syntaxe (Git 2.16+)
git stash push -m "WIP: login feature"
```

### Stash avec options

```bash
# Stasher les fichiers tracked + untracked
git stash -u
git stash --include-untracked

# Stasher TOUT (tracked + untracked + ignored)
git stash -a
git stash --all

# Stasher seulement les fichiers stagés
git stash --staged

# Stasher seulement les fichiers non stagés
git stash --keep-index

# Stash interactif (choisir quoi stasher)
git stash -p
git stash --patch
# Pour chaque modification, choisir:
# y - yes, stash this hunk
# n - no, don't stash
# q - quit
```

### Exemple pratique

```bash
# Situation: Vous travaillez sur une feature
echo "new code" >> feature.js
git add feature.js

# Urgence: besoin de fixer un bug sur main
git status
# Changes to be committed:
#   modified: feature.js

# Impossible de changer de branche:
git switch main
# error: Your local changes would be overwritten

# Solution: Stash
git stash save "WIP: feature work"
# Working directory propre

# Maintenant possible:
git switch main
# Fix le bug
git commit -am "fix: urgent bug"

# Retour à la feature
git switch feature
git stash pop
# Récupère le travail en cours
```

---

## Voir les stash

### Lister les stash

```bash
# Lister tous les stash
git stash list
# stash@{0}: WIP on feature: abc123 Add login
# stash@{1}: On main: def456 Fix bug
# stash@{2}: WIP on develop: ghi789 Update deps

# Format:
# stash@{N}: message
# N = index (0 = plus récent)
```

### Voir le contenu d'un stash

```bash
# Voir les fichiers dans le dernier stash
git stash show
#  file1.js | 10 ++++++++++
#  file2.js |  5 -----
#  2 files changed, 10 insertions(+), 5 deletions(-)

# Voir les modifications complètes
git stash show -p
git stash show --patch

# Voir un stash spécifique
git stash show stash@{1}
git stash show -p stash@{2}

# Statistiques détaillées
git stash show --stat
```

---

## Appliquer un stash

### Apply vs Pop

```bash
# POP: Applique ET supprime le stash
git stash pop
# Applique stash@{0} et le supprime

# APPLY: Applique SANS supprimer
git stash apply
# Applique stash@{0} mais le garde

# Différence:
# pop  = apply + drop
# apply = juste appliquer, garde le stash
```

### Appliquer un stash spécifique

```bash
# Appliquer un stash par son index
git stash pop stash@{1}
git stash apply stash@{2}

# Exemples:
git stash list
# stash@{0}: WIP on feature
# stash@{1}: WIP on bugfix
# stash@{2}: WIP on main

# Appliquer le 2ème stash
git stash apply stash@{1}
```

### Appliquer sur une autre branche

```bash
# Créer une branche depuis un stash
git stash branch nouvelle-branche
# 1. Créé une nouvelle branche
# 2. Checkout la branche
# 3. Applique le stash
# 4. Supprime le stash si succès

# Avec un stash spécifique
git stash branch nouvelle-branche stash@{2}

# Cas d'usage:
# Vous stashez sur main par erreur
# Créer une branche feature et y appliquer le stash
```

### Gérer les conflits

```bash
# Si appliquer un stash cause des conflits:
git stash pop
# CONFLICT (content): Merge conflict in file.js

# Résoudre comme un conflit normal:
# 1. Éditer le fichier
code file.js

# 2. Marquer comme résolu
git add file.js

# 3. Le stash est toujours là (en cas de pop)
# Le supprimer manuellement:
git stash drop

# Avec apply, pas de problème (stash conservé)
```

---

## Supprimer des stash

### Drop (supprimer)

```bash
# Supprimer le dernier stash
git stash drop
# Dropped stash@{0} (abc123...)

# Supprimer un stash spécifique
git stash drop stash@{1}

# Supprimer tous les stash
git stash clear
# ⚠️ ATTENTION: Irréversible !

# Vérifier avant de clear
git stash list
# Si liste vide: rien à perdre
```

---

## Cas d'usage pratiques

### Cas 1: Changer de branche rapidement

```bash
# Sur feature, travail en cours
git status
# Modified: file.js

# Besoin urgent de changer de branche
git stash -u "WIP: feature work"
git switch main

# Plus tard, retour
git switch feature
git stash pop
```

### Cas 2: Pull propre

```bash
# Avant un pull, stasher pour éviter conflits
git stash
git pull --rebase
git stash pop
```

### Cas 3: Tester rapidement

```bash
# Expérimenter sans commit
# Faire des modifications

# Tester
npm test

# Si ça marche pas, annuler facilement
git stash

# Si ça marche, récupérer et commiter
git stash pop
git commit -am "feat: new feature"
```

### Cas 4: Nettoyer le working directory

```bash
# Voir l'état propre du repository
git stash -u
git status
# nothing to commit, working tree clean

# Récupérer plus tard
git stash pop
```

### Cas 5: Travailler sur plusieurs tâches

```bash
# Tâche 1 en cours
echo "task 1" >> task1.js
git stash save "Task 1: login"

# Tâche 2
echo "task 2" >> task2.js
git stash save "Task 2: profile"

# Tâche 3
echo "task 3" >> task3.js
git stash save "Task 3: settings"

# Liste
git stash list
# stash@{0}: Task 3: settings
# stash@{1}: Task 2: profile
# stash@{2}: Task 1: login

# Appliquer une tâche spécifique
git stash apply stash@{2}  # Task 1
```

### Cas 6: Partager un stash

```bash
# Créer un patch depuis un stash
git stash show -p > my-changes.patch

# Envoyer my-changes.patch à quelqu'un

# Appliquer le patch
git apply my-changes.patch
```

---

## Stash avancé

### Stash partiel

```bash
# Stasher des morceaux spécifiques
git stash -p

# Pour chaque modification:
# y - yes, stash
# n - no, don't stash
# q - quit
# a - stash this and all remaining
# d - don't stash this and all remaining
# s - split into smaller hunks
# e - manually edit
```

### Créer un stash depuis l'index

```bash
# Situation: fichiers stagés + fichiers modifiés
git add file1.js
# Modifié: file2.js (non stagé)

# Stasher seulement file1.js (stagé)
git stash --staged

# Résultat:
# - file1.js: stashé
# - file2.js: toujours modifié (non stagé)
```

### Stash avec untracked

```bash
# Sans -u, les fichiers non trackés sont ignorés
echo "new file" > new.js
git stash
git status
# Untracked: new.js (toujours là)

# Avec -u, tout est stashé
git stash -u
git status
# nothing to commit
```

### Récupérer un stash supprimé

```bash
# Oups, supprimé un stash par erreur
git stash drop stash@{0}

# Récupérer avec reflog
git fsck --unreachable | grep commit
# unreachable commit abc123...

# Voir le commit
git show abc123

# Si c'est le bon stash, l'appliquer
git stash apply abc123

# Ou recréer le stash
git update-ref refs/stash abc123 -m "Recovered stash"
```

---

## Workflow recommandé

### Bon workflow

```bash
# 1. Vérifier l'état
git status

# 2. Stasher avec message clair
git stash save "WIP: add user authentication - login form"

# 3. Faire autre chose
git switch main
# ...

# 4. Revenir
git switch feature

# 5. Vérifier les stash
git stash list

# 6. Appliquer le bon stash
git stash pop stash@{0}

# 7. Si conflits, résoudre
# ...

# 8. Continuer le travail
```

### Mauvaises pratiques

```bash
# ❌ Accumuler trop de stash sans messages
git stash
git stash
git stash
git stash list
# stash@{0}: WIP on main
# stash@{1}: WIP on main
# stash@{2}: WIP on main
# stash@{3}: WIP on main
# Impossible de savoir ce que contient chaque stash !

# ❌ Garder des stash pendant des mois
# Les stash sont temporaires, pas un système de backup

# ❌ Utiliser stash au lieu de commits
# Si c'est du vrai travail, commitez !
```

---

## Alias utiles

```bash
# Alias pour stash
git config --global alias.st stash
git config --global alias.stl "stash list"
git config --global alias.stp "stash pop"
git config --global alias.sta "stash apply"
git config --global alias.std "stash drop"

# Stash avec message automatique
git config --global alias.save "stash save"

# Voir le dernier stash
git config --global alias.stshow "stash show -p"

# Utilisation:
git st              # stash
git stl             # stash list
git stp             # stash pop
```

---

## Commandes de référence rapide

```bash
# Sauvegarder
git stash                       # Stash modifications
git stash save "message"        # Stash avec message
git stash -u                    # Stash + untracked
git stash -p                    # Stash interactif

# Voir
git stash list                  # Lister stash
git stash show                  # Voir dernier stash
git stash show -p stash@{1}     # Voir stash spécifique

# Appliquer
git stash pop                   # Appliquer + supprimer
git stash apply                 # Appliquer sans supprimer
git stash apply stash@{2}       # Appliquer stash spécifique
git stash branch nom            # Créer branche + appliquer

# Supprimer
git stash drop                  # Supprimer dernier
git stash drop stash@{1}        # Supprimer spécifique
git stash clear                 # Tout supprimer
```

---

## Prochaines étapes

Maintenant que vous savez gérer le travail temporaire, explorez l'historique :

- [**Historique et Navigation**](./infos-git-09-historique-navigation.md) - Explorer l'historique
- [**Annuler des Changements**](./infos-git-10-annuler-changements.md) - Défaire des erreurs

---

[← Conflits](./infos-git-07-conflits.md) | [Index](./infos-git-00-index.md) | [Historique →](./infos-git-09-historique-navigation.md)

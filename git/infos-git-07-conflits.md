# ⚔️ Résolution de Conflits

[← Remotes](./infos-git-06-remotes-collaboration.md) | [Index](./infos-git-00-index.md) | [Stash →](./infos-git-08-stash.md)

---

## Table des matières
- [Comprendre les conflits](#comprendre-les-conflits)
- [Anatomie d'un conflit](#anatomie-dun-conflit)
- [Résoudre manuellement](#resoudre-manuellement)
- [Outils de merge](#outils-de-merge)
- [Prévenir les conflits](#prevenir-les-conflits)
- [Stratégies de résolution](#strategies-de-resolution)

---

## Comprendre les conflits

### Qu'est-ce qu'un conflit ?

Un **conflit** survient quand Git ne peut pas merger automatiquement deux versions d'un même fichier.

```
Vous:                    Collègue:
main → C                 main → C
       ↓                        ↓
     modif file.txt          modif file.txt
       ↓                        ↓
       D                        E

Tentative de merge:
       D (vos modifs)
       ↓
       ? ← CONFLIT !
       ↑
       E (ses modifs)
```

### Quand surviennent les conflits ?

```bash
# 1. Lors d'un merge
git merge feature
# CONFLICT (content): Merge conflict in file.txt

# 2. Lors d'un pull
git pull origin main
# CONFLICT (content): Merge conflict in file.txt

# 3. Lors d'un rebase
git rebase main
# CONFLICT (content): Merge conflict in file.txt

# 4. Lors d'un cherry-pick
git cherry-pick abc123
# CONFLICT (content): Merge conflict in file.txt
```

---

## Anatomie d'un conflit

### Structure d'un conflit

Quand un conflit survient, Git marque le fichier ainsi:

```javascript
// Avant le conflit (version originale)
function greet() {
    console.log("Hello");
}

// Après conflit dans file.txt
<<<<<<< HEAD (Current Change)
function greet() {
    console.log("Bonjour");
    console.log("Comment allez-vous?");
}
=======
function greet() {
    console.log("Hi there!");
}
>>>>>>> feature (Incoming Change)
```

**Explication:**
- `<<<<<<< HEAD` : Début de votre version (branche courante)
- `=======` : Séparateur
- `>>>>>>> feature` : Fin de la version à merger (branche entrante)

### Identifier les fichiers en conflit

```bash
# Voir les fichiers en conflit
git status
# You have unmerged paths.
# Unmerged paths:
#   (use "git add <file>..." to mark resolution)
#         both modified:   file.txt

# Lister seulement les fichiers en conflit
git diff --name-only --diff-filter=U

# Voir les détails des conflits
git diff
```

---

## Résoudre manuellement

### Méthode 1: Éditer le fichier

```bash
# 1. Ouvrir le fichier en conflit
nano file.txt
# ou
code file.txt

# 2. Choisir la version à garder
# Option A: Garder votre version (HEAD)
function greet() {
    console.log("Bonjour");
    console.log("Comment allez-vous?");
}

# Option B: Garder leur version (incoming)
function greet() {
    console.log("Hi there!");
}

# Option C: Combiner les deux (souvent la meilleure solution)
function greet() {
    console.log("Bonjour");
    console.log("Hi there!");
    console.log("Comment allez-vous?");
}

# 3. Supprimer les marqueurs de conflit
# Supprimer: <<<<<<< HEAD
# Supprimer: =======
# Supprimer: >>>>>>> feature

# 4. Sauvegarder le fichier

# 5. Marquer comme résolu (staging)
git add file.txt

# 6. Finaliser le merge
git commit
# Un message par défaut sera proposé: "Merge branch 'feature'"
```

### Méthode 2: Accepter une version complètement

```bash
# Accepter votre version (checkout --ours)
git checkout --ours file.txt
git add file.txt

# Accepter leur version (checkout --theirs)
git checkout --theirs file.txt
git add file.txt

# Continuer le merge
git commit
```

### Méthode 3: Utiliser VS Code

VS Code détecte automatiquement les conflits et offre des boutons:

```
<<<<<<< HEAD (Current Change)
function greet() {
    console.log("Bonjour");
}

[Accept Current Change] [Accept Incoming Change] [Accept Both Changes] [Compare Changes]

=======
function greet() {
    console.log("Hi there!");
}
>>>>>>> feature (Incoming Change)
```

---

## Outils de merge

### Configurer un mergetool

```bash
# VS Code
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Vim (vimdiff)
git config --global merge.tool vimdiff

# Meld (GUI)
git config --global merge.tool meld

# KDiff3
git config --global merge.tool kdiff3

# P4Merge
git config --global merge.tool p4merge

# Ne pas créer de fichiers .orig
git config --global mergetool.keepBackup false
```

### Utiliser le mergetool

```bash
# Lancer le mergetool sur un conflit
git mergetool

# Le tool s'ouvre et affiche:
# - LOCAL: votre version (HEAD)
# - BASE: ancêtre commun
# - REMOTE: leur version (incoming)
# - MERGED: résultat final (à éditer)

# Résoudre le conflit dans l'outil
# Sauvegarder et fermer

# Git ajoute automatiquement le fichier résolu
# Finaliser
git commit
```

### Mergetool avec VS Code

```bash
# Après configuration
git mergetool

# VS Code s'ouvre en mode comparaison 3-way:
# - Gauche: Current (HEAD)
# - Centre: Result (résultat)
# - Droite: Incoming (feature)

# Utiliser les boutons pour accepter les changements
# Sauvegarder et fermer
# Git add automatique

git commit
```

---

## Prévenir les conflits

### Bonnes pratiques

```bash
# 1. Pull régulièrement
git pull origin main
# Ou mieux avec rebase
git pull --rebase origin main

# 2. Commits fréquents et petits
# ✅ BON
git commit -m "feat: add login button"
git commit -m "feat: add login logic"

# ❌ MAUVAIS (gros commit après 3 jours)
git commit -m "Add entire authentication system"

# 3. Branches de courte durée
# ✅ BON: feature branches de 1-3 jours
# ❌ MAUVAIS: feature branches de plusieurs semaines

# 4. Communiquer avec l'équipe
# Qui travaille sur quels fichiers?

# 5. Diviser les fichiers
# Au lieu d'un gros fichier de 1000 lignes
# Créer plusieurs petits fichiers modulaires
```

### Voir ce qui va conflictuer avant le merge

```bash
# Voir les différences avant de merger
git diff main..feature

# Voir les fichiers modifiés des deux côtés
git diff --name-only main...feature

# Simuler le merge
git merge --no-commit --no-ff feature
# Regarde ce qui se passe
git merge --abort  # Annuler

# Ou utiliser git-merge-tree (Git 2.38+)
git merge-tree $(git merge-base main feature) main feature
```

---

## Stratégies de résolution

### Stratégie 1: Merge avec "ours" ou "theirs"

```bash
# Stratégie "ours" : En cas de conflit, prendre notre version
git merge -X ours feature

# Stratégie "theirs" : En cas de conflit, prendre leur version
git merge -X theirs feature

# Attention: Cela ne résout que les CONFLITS
# Les changements non-conflictuels sont toujours mergés

# Pour tout prendre de l'autre branche (pas recommandé):
git merge -s ours feature  # Ignore complètement feature
```

### Stratégie 2: Rebase au lieu de merge

Le rebase peut réduire les conflits en rejouant vos commits un par un.

```bash
# Au lieu de merger
git merge feature

# Faire un rebase
git rebase feature
# Si conflit à un commit:
# 1. Résoudre le conflit
git add file.txt
git rebase --continue

# 2. Ou sauter ce commit
git rebase --skip

# 3. Ou abandonner
git rebase --abort
```

### Stratégie 3: Squash avant merge

Combiner tous les commits en un seul pour simplifier.

```bash
# Squash interactif de vos 5 derniers commits
git rebase -i HEAD~5

# Changer "pick" en "squash" (ou "s")
pick abc123 commit 1
squash def456 commit 2
squash ghi789 commit 3
squash jkl012 commit 4
squash mno345 commit 5

# Maintenant vous avez 1 seul commit
# Merger dans main
git switch main
git merge feature  # Plus simple !
```

---

## Workflow complet de résolution

### Scénario: Merge avec conflits

```bash
# 1. Tenter le merge
git switch main
git merge feature
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt
# Automatic merge failed; fix conflicts and then commit the result.

# 2. Voir l'état
git status
# On branch main
# You have unmerged paths.
# Unmerged paths:
#   both modified:   file.txt

# 3. Voir les fichiers en conflit
git diff --name-only --diff-filter=U
# file.txt

# 4. Option A: Résoudre manuellement
code file.txt
# Éditer, résoudre, sauvegarder

# 5. Option B: Utiliser mergetool
git mergetool

# 6. Marquer comme résolu
git add file.txt

# 7. Vérifier que tous les conflits sont résolus
git status
# All conflicts fixed but you are still merging.

# 8. Finaliser le merge
git commit
# Message par défaut: "Merge branch 'feature'"
# Ou personnaliser:
git commit -m "Merge feature: resolve conflicts in file.txt"

# 9. Vérifier
git log --oneline --graph
```

### Scénario: Pull avec conflits

```bash
# 1. Pull
git pull origin main
# CONFLICT (content): Merge conflict in app.js

# 2. Résoudre (même process)
git mergetool
git add app.js
git commit

# 3. Pousser
git push origin main
```

### Scénario: Rebase avec conflits

```bash
# 1. Rebase
git rebase main
# CONFLICT (content): Merge conflict in app.js
# error: could not apply abc123... feat: add feature

# 2. Résoudre le conflit
code app.js
# Éditer, sauvegarder

# 3. Ajouter
git add app.js

# 4. Continuer le rebase
git rebase --continue
# Applique le commit suivant
# Peut y avoir d'autres conflits, répéter

# 5. Si trop de conflits, abandonner
git rebase --abort

# 6. Une fois terminé
git log --oneline --graph
```

---

## Cas particuliers

### Conflits dans les fichiers binaires

```bash
# Git ne peut pas merger les fichiers binaires (images, etc.)

# Conflit dans image.png
git status
# both modified: image.png

# Choisir une version
git checkout --ours image.png    # Garder notre image
# ou
git checkout --theirs image.png  # Garder leur image

git add image.png
git commit
```

### Conflits de suppressions

```bash
# Vous: supprimez file.txt
# Eux: modifient file.txt

# Conflit: deleted by us
git status
# deleted by us: file.txt

# Garder la suppression
git rm file.txt

# Ou garder le fichier modifié
git add file.txt

git commit
```

### Conflits de renommage

```bash
# Vous: renommez old.txt → new.txt
# Eux: modifient old.txt

# Git essaie de merger, peut causer des conflits

# Résoudre dans le fichier renommé
code new.txt
git add new.txt
git commit
```

---

## Annuler un merge conflictuel

```bash
# Si vous êtes perdu dans les conflits

# Avant le commit de merge:
git merge --abort
# Retour à l'état avant le merge

# Après le commit de merge:
git reset --hard HEAD~1
# ⚠️ Perd le commit de merge

# Ou créer un commit inverse
git revert HEAD
```

---

## Outils et astuces

### Voir le conflit en contexte

```bash
# Voir le conflit avec 3 versions (base, ours, theirs)
git config --global merge.conflictstyle diff3

# Maintenant les conflits montrent:
<<<<<<< HEAD
Votre version
||||||| base
Version d'origine
=======
Leur version
>>>>>>> feature
```

### Rerere (Reuse Recorded Resolution)

Git peut se souvenir de vos résolutions de conflits.

```bash
# Activer rerere
git config --global rerere.enabled true

# Maintenant:
# 1. Vous résolvez un conflit une fois
# 2. Si le même conflit survient plus tard (rebase, etc.)
# 3. Git applique automatiquement la même résolution !
```

### Diff avancé

```bash
# Voir les différences pendant un conflit
git diff --ours file.txt      # Diff avec notre version
git diff --theirs file.txt    # Diff avec leur version
git diff --base file.txt      # Diff avec la base commune
```

---

## Commandes de référence rapide

```bash
# Identifier conflits
git status                      # Voir fichiers en conflit
git diff --name-only --diff-filter=U  # Lister conflits

# Résoudre
git mergetool                   # Ouvrir outil de merge
git checkout --ours file        # Garder notre version
git checkout --theirs file      # Garder leur version

# Marquer résolu
git add file                    # Marquer comme résolu
git commit                      # Finaliser merge

# Annuler
git merge --abort               # Annuler merge en cours
git rebase --abort              # Annuler rebase en cours

# Configuration
git config merge.tool vscode    # Configurer mergetool
git config merge.conflictstyle diff3  # Style 3-way
git config rerere.enabled true  # Mémoriser résolutions
```

---

## Prochaines étapes

Maintenant que vous savez gérer les conflits, apprenez à sauvegarder temporairement votre travail :

- [**Stash**](./infos-git-08-stash.md) - Travail temporaire
- [**Annuler des Changements**](./infos-git-10-annuler-changements.md) - Défaire des erreurs

---

[← Remotes](./infos-git-06-remotes-collaboration.md) | [Index](./infos-git-00-index.md) | [Stash →](./infos-git-08-stash.md)

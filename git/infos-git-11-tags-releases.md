# 🏷️ Tags et Releases

[← Annuler](./infos-git-10-annuler-changements.md) | [Index](./infos-git-00-index.md) | [Workflows →](./infos-git-12-workflows.md)

---

## Table des matières
- [Qu'est-ce qu'un tag ?](#quest-ce-quun-tag)
- [Tags légers vs annotés](#tags-legers-vs-annotes)
- [Créer des tags](#creer-des-tags)
- [Gérer les tags](#gerer-les-tags)
- [Releases GitHub/GitLab](#releases-githubgitlab)
- [Versioning sémantique](#versioning-semantique)

---

## Qu'est-ce qu'un tag ?

### Définition

Un **tag** est un **marqueur permanent** pointant vers un commit spécifique. Utilisé pour marquer des **versions** (releases).

```
main
  ↓
A ← B ← C ← D ← E
    ↑       ↑   ↑
  v1.0    v1.1 v2.0
```

**Différence avec les branches :**
- Branche : pointeur **mobile** (avance avec les commits)
- Tag : pointeur **fixe** (ne bouge jamais)

---

## Tags légers vs annotés

### Tag léger (lightweight)

Simple pointeur vers un commit.

```bash
# Créer un tag léger
git tag v1.0.0

# C'est juste un nom pour un commit
# Pas de métadonnées
```

### Tag annoté (annotated)

Objet Git complet avec métadonnées.

```bash
# Créer un tag annoté
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"

# Contient:
# - Nom du tagger
# - Email
# - Date
# - Message
# - Peut être signé (GPG)
```

**✅ Recommandation : Toujours utiliser des tags annotés pour les releases**

---

## Créer des tags

### Tag basique

```bash
# Tag annoté sur HEAD
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag sur un commit spécifique
git tag -a v1.0.0 abc123 -m "Release 1.0.0"

# Tag léger
git tag v1.0.0-beta

# Tag avec message multi-lignes
git tag -a v2.0.0 -m "Version 2.0.0

New features:
- User authentication
- Profile management
- Dark mode

Bug fixes:
- Fix login timeout
- Resolve memory leak"
```

### Tag avec éditeur

```bash
# Ouvrir l'éditeur pour le message
git tag -a v1.0.0

# Écrire le message dans l'éditeur:
Version 1.0.0 - Major Release

## What's New
- Feature A
- Feature B

## Breaking Changes
- Changed API endpoint

## Bug Fixes
- Fixed issue #123
```

### Lister les tags

```bash
# Lister tous les tags
git tag
# v1.0.0
# v1.1.0
# v2.0.0

# Lister avec pattern
git tag -l "v1.*"
# v1.0.0
# v1.1.0

# Lister avec messages
git tag -n
# v1.0.0     Release version 1.0.0
# v2.0.0     Major update

# Lister avec plus de lignes du message
git tag -n5
```

### Voir un tag

```bash
# Voir les détails d'un tag annoté
git show v1.0.0

# Résultat:
# tag v1.0.0
# Tagger: John Doe <john@example.com>
# Date:   Mon Jan 15 14:30:00 2024 +0100
#
# Release version 1.0.0
#
# commit abc123...
# Author: John Doe <john@example.com>
# ...

# Voir juste le commit
git show v1.0.0^{commit}
```

---

## Gérer les tags

### Pousser des tags

```bash
# Les tags ne sont PAS poussés automatiquement !

# Pousser un tag spécifique
git push origin v1.0.0

# Pousser tous les tags
git push origin --tags
git push --tags

# Pousser tags annotés seulement (Git 2.4+)
git push --follow-tags
```

### Configuration pour push automatique

```bash
# Pousser automatiquement les tags annotés
git config --global push.followTags true

# Maintenant:
git push
# Pousse aussi les tags annotés !
```

### Checkout un tag

```bash
# Se déplacer sur un tag (detached HEAD)
git checkout v1.0.0
# You are in 'detached HEAD' state...

# Créer une branche depuis un tag
git checkout -b hotfix/v1.0.1 v1.0.0
# Utile pour faire des hotfixes sur une ancienne version
```

### Supprimer des tags

```bash
# Supprimer un tag local
git tag -d v1.0.0
git tag --delete v1.0.0

# Supprimer un tag remote
git push origin --delete v1.0.0
git push origin :refs/tags/v1.0.0  # Ancienne syntaxe

# Supprimer plusieurs tags
git tag -d v1.0.0 v1.1.0 v1.2.0
```

### Renommer un tag

```bash
# Git ne permet pas de renommer directement
# Il faut supprimer et recréer

# 1. Créer nouveau tag au même endroit
git tag -a v1.0.1 v1.0.0^{} -m "Renamed from v1.0.0"

# 2. Supprimer l'ancien tag local
git tag -d v1.0.0

# 3. Supprimer l'ancien tag remote
git push origin :refs/tags/v1.0.0

# 4. Pousser le nouveau tag
git push origin v1.0.1
```

---

## Releases GitHub/GitLab

### GitHub Releases

```bash
# 1. Créer et pousser un tag
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0

# 2. Sur GitHub:
# - Aller dans "Releases"
# - Cliquer "Create a new release"
# - Sélectionner le tag v1.0.0
# - Écrire les release notes
# - Ajouter des fichiers binaires si besoin
# - Publier

# Ou avec GitHub CLI (gh)
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes here"

# Avec fichiers
gh release create v1.0.0 --title "v1.0.0" --notes "Release" ./dist/*.zip
```

### GitLab Releases

```bash
# 1. Créer et pousser un tag
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0

# 2. Sur GitLab:
# - Aller dans "Repository" → "Tags"
# - Cliquer sur le tag
# - "Edit release notes"
# - Ajouter description et assets
# - Sauvegarder

# Ou avec GitLab CLI
glab release create v1.0.0 --name "Version 1.0.0" --notes "Release notes"
```

### Générer release notes automatiquement

```bash
# Générer changelog depuis les commits
git log v0.9.0..v1.0.0 --oneline --pretty=format:"- %s (%h)"

# Avec groupement par type (si vous utilisez conventional commits)
git log v0.9.0..v1.0.0 --oneline | \
  awk '/^[a-f0-9]+ feat:/ {print "### Features\n" $0; next} \
       /^[a-f0-9]+ fix:/ {print "### Bug Fixes\n" $0; next} \
       {print "### Other\n" $0}'

# Outils automatiques:
# - conventional-changelog (npm)
# - standard-version (npm)
# - semantic-release (npm)
```

---

## Versioning sémantique

### Format: MAJOR.MINOR.PATCH

```
v2.3.1
│ │ │
│ │ └─ PATCH: Bug fixes (backward compatible)
│ └─── MINOR: New features (backward compatible)
└───── MAJOR: Breaking changes (not backward compatible)
```

### Exemples

```bash
# Version initiale
v1.0.0

# Ajout de features (backward compatible)
v1.1.0
v1.2.0

# Bug fixes
v1.2.1
v1.2.2

# Breaking change
v2.0.0

# Pre-releases
v2.0.0-alpha.1
v2.0.0-beta.1
v2.0.0-rc.1  (release candidate)

# Metadata
v1.0.0+build.123
v1.0.0+20240115
```

### Workflow de versioning

```bash
# Feature branch
git checkout -b feature/new-feature
# Développement...
git commit -m "feat: add new feature"

# Merge dans main
git checkout main
git merge feature/new-feature

# Déterminer le numéro de version:
# - Breaking change? → MAJOR
# - New feature? → MINOR
# - Bug fix? → PATCH

# Créer le tag
git tag -a v1.1.0 -m "Version 1.1.0

New features:
- Add new feature

Changes:
- feat: add new feature (abc123)"

# Pousser
git push origin main
git push origin v1.1.0

# Créer la release sur GitHub
gh release create v1.1.0 --generate-notes
```

### Outils de versioning automatique

```bash
# npm version (pour projets Node.js)
npm version patch  # 1.0.0 → 1.0.1
npm version minor  # 1.0.1 → 1.1.0
npm version major  # 1.1.0 → 2.0.0
# Crée automatiquement le tag et met à jour package.json

# standard-version
npm install -g standard-version
standard-version
# Analyse les commits et crée le tag approprié

# semantic-release
npm install -g semantic-release
semantic-release
# Entièrement automatique basé sur les commits
```

---

## Cas pratiques

### Workflow release complet

```bash
# 1. S'assurer que main est à jour
git checkout main
git pull origin main

# 2. Vérifier les changements depuis la dernière release
git log v1.0.0..HEAD --oneline

# 3. Décider de la version
# Breaking changes? → v2.0.0
# New features? → v1.1.0
# Bug fixes only? → v1.0.1

# 4. Mettre à jour la version dans les fichiers
# - package.json
# - VERSION file
# - etc.

# 5. Commit de version
git commit -am "chore: bump version to 1.1.0"

# 6. Créer le tag
git tag -a v1.1.0 -m "Version 1.1.0

## New Features
- Feature A
- Feature B

## Bug Fixes
- Fix issue #123

## Breaking Changes
None"

# 7. Pousser
git push origin main
git push origin v1.1.0

# 8. Créer la release sur GitHub
gh release create v1.1.0 \
  --title "Version 1.1.0" \
  --notes-file CHANGELOG.md \
  --latest

# 9. Notifier l'équipe
```

### Hotfix sur une ancienne version

```bash
# Problème critique sur v1.0.0
# Mais main est déjà à v1.1.0

# 1. Créer branche depuis le tag v1.0.0
git checkout -b hotfix/v1.0.1 v1.0.0

# 2. Fixer le bug
git commit -am "fix: critical security issue"

# 3. Tagger la nouvelle version
git tag -a v1.0.1 -m "Version 1.0.1 - Security hotfix"

# 4. Pousser
git push origin hotfix/v1.0.1
git push origin v1.0.1

# 5. Merger le fix dans main aussi
git checkout main
git cherry-pick <commit-hash>
git push origin main
```

---

## Bonnes pratiques

### ✅ À faire

```bash
# Toujours des tags annotés pour releases
git tag -a v1.0.0 -m "Release 1.0.0"

# Messages descriptifs
git tag -a v1.0.0 -m "Version 1.0.0

## What's New
- Feature list
- Bug fixes
- Breaking changes"

# Suivre semver
v1.0.0 → v1.1.0 → v1.1.1 → v2.0.0

# Tagger depuis main/master
git checkout main
git tag -a v1.0.0 -m "Release"

# Pousser les tags
git push origin --tags
```

### ❌ À éviter

```bash
# Tags légers pour releases
git tag v1.0.0  # Pas de métadonnées

# Messages vagues
git tag -a v1.0.0 -m "release"
git tag -a v1.0.0 -m "version bump"

# Versions incohérentes
v1.0 → v1.1.5 → v2 → v2.0.3.1

# Tagger n'importe où
git tag v1.0.0  # Sur une feature branch?

# Oublier de pousser
git tag v1.0.0  # Reste local!
```

---

## Commandes de référence rapide

```bash
# Créer
git tag v1.0.0                  # Tag léger
git tag -a v1.0.0 -m "msg"      # Tag annoté
git tag -a v1.0.0 abc123 -m ""  # Tag sur commit

# Lister
git tag                         # Tous les tags
git tag -l "v1.*"               # Avec pattern
git tag -n                      # Avec messages

# Voir
git show v1.0.0                 # Détails du tag
git log v1.0.0                  # Historique jusqu'au tag

# Pousser
git push origin v1.0.0          # Un tag
git push origin --tags          # Tous les tags
git push --follow-tags          # Tags annotés

# Supprimer
git tag -d v1.0.0               # Local
git push origin --delete v1.0.0 # Remote

# Checkout
git checkout v1.0.0             # Detached HEAD
git checkout -b branch v1.0.0   # Branche depuis tag
```

---

[← Annuler](./infos-git-10-annuler-changements.md) | [Index](./infos-git-00-index.md) | [Workflows →](./infos-git-12-workflows.md)

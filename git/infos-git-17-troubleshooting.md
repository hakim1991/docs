# 🔧 Troubleshooting Git

[← Bonnes pratiques](./infos-git-16-bonnes-pratiques.md) | [Index](./infos-git-00-index.md)

---

## Table des matières
- [Problèmes courants](#problemes-courants)
- [Erreurs de commit](#erreurs-de-commit)
- [Problèmes de branches](#problemes-de-branches)
- [Problèmes de remote](#problemes-de-remote)
- [Récupération de données](#recuperation-de-donnees)
- [Performance et maintenance](#performance-et-maintenance)

---

## Problèmes courants

### "Permission denied (publickey)"

```bash
# Problème: SSH key non configurée

# Solution 1: Générer une clé SSH
ssh-keygen -t ed25519 -C "your.email@example.com"
# Ajouter à l'agent
ssh-add ~/.ssh/id_ed25519
# Copier la clé publique
cat ~/.ssh/id_ed25519.pub
# Ajouter à GitHub/GitLab: Settings → SSH Keys

# Solution 2: Vérifier la connexion
ssh -T git@github.com
# "Hi username! You've successfully authenticated..."

# Solution 3: Utiliser HTTPS au lieu de SSH
git remote set-url origin https://github.com/user/repo.git
```

### "fatal: not a git repository"

```bash
# Problème: Pas dans un repository Git

# Solution: Vérifier où vous êtes
pwd
ls -la  # Chercher .git/

# Initialiser si nécessaire
git init

# Ou se déplacer dans le bon dossier
cd /path/to/repo
```

### "Your branch is ahead of 'origin/main' by N commits"

```bash
# Problème: Commits locaux non pushés

# Solution: Push les commits
git push origin main

# Si rejected (quelqu'un a pushé avant vous):
git pull --rebase origin main
git push origin main
```

### "Your branch is behind 'origin/main' by N commits"

```bash
# Problème: Le remote a avancé

# Solution: Pull les changements
git pull origin main

# Ou avec rebase (historique plus propre)
git pull --rebase origin main
```

### "divergent branches"

```bash
# Problème: Branches ont divergé

# Solution 1: Merge
git pull origin main
# Résoudre les conflits
git push origin main

# Solution 2: Rebase (historique linéaire)
git pull --rebase origin main
# Résoudre les conflits
git rebase --continue
git push origin main

# Solution 3: Force push (⚠️ DANGEREUX si branche partagée)
git push --force-with-lease origin main
```

---

## Erreurs de commit

### "Commit sur la mauvaise branche"

```bash
# Problème: Commité sur main au lieu de feature

# Solution 1: Déplacer le commit vers une nouvelle branche
git branch feature-branch  # Créé branche au commit actuel
git reset --hard HEAD~1    # Reculer main
git checkout feature-branch

# Solution 2: Cherry-pick vers la bonne branche
git checkout feature-branch
git cherry-pick abc123  # SHA du commit à déplacer
git checkout main
git reset --hard HEAD~1
```

### "Mauvais message de commit"

```bash
# Problème: Message de commit à corriger

# Solution: Si pas encore pushé
git commit --amend -m "Nouveau message"

# Si déjà pushé et branche personnelle
git commit --amend -m "Nouveau message"
git push --force-with-lease

# Si déjà pushé et branche partagée
# Ne pas modifier ! Faire un nouveau commit explicatif
```

### "Commit avec des fichiers en trop"

```bash
# Problème: Commité des fichiers par erreur

# Solution: Si pas encore pushé
# Retirer les fichiers
git reset HEAD~1  # Annuler le commit
git add fichier-correct.js  # Ajouter seulement les bons fichiers
git commit -m "message"

# Ou amend
git reset HEAD fichier-erreur.js
git commit --amend --no-edit
```

### "Secret commitée par erreur"

```bash
# ⚠️ URGENT: Secret exposée

# Solution 1: Si pas pushé
git reset --hard HEAD~1
# Changer le secret !

# Solution 2: Si pushé récemment
git revert HEAD
git push
# Changer le secret immédiatement !

# Solution 3: Nettoyer l'historique (complexe)
# Utiliser git-filter-repo
pip install git-filter-repo
git filter-repo --path secret.txt --invert-paths
git push --force --all
# Changer le secret !

# ⚠️ Toujours révoquer/changer le secret exposé
```

---

## Problèmes de branches

### "Cannot delete branch (not fully merged)"

```bash
# Problème: Branche non mergée

# Solution 1: Merger d'abord
git checkout main
git merge feature-branch
git branch -d feature-branch

# Solution 2: Force delete (⚠️ perte de travail)
git branch -D feature-branch

# Solution 3: Vérifier si vraiment non mergée
git branch --no-merged
git log main..feature-branch  # Voir les commits non mergés
```

### "Branche supprimée par erreur"

```bash
# Problème: Branche supprimée, besoin de la récupérer

# Solution: Utiliser reflog
git reflog
# Trouver le SHA du dernier commit de la branche

# Recréer la branche
git branch feature-branch abc123
# ou
git checkout -b feature-branch abc123

# Si elle était pushée
git checkout -b feature-branch origin/feature-branch
```

### "Detached HEAD state"

```bash
# Problème: HEAD détaché (pas sur une branche)

# Solution 1: Retourner à une branche
git checkout main

# Solution 2: Créer une branche depuis cette position
git checkout -b nouvelle-branche

# Solution 3: Si vous avez fait des commits en detached HEAD
git checkout -b sauver-mon-travail
git checkout main
git merge sauver-mon-travail
```

---

## Problèmes de remote

### "failed to push some refs"

```bash
# Problème: Push rejeté

# Cause 1: Quelqu'un a pushé avant vous
git pull --rebase origin main
git push origin main

# Cause 2: Historique divergent
git pull origin main
# Résoudre les conflits
git push origin main

# Cause 3: Branch protected
# Créer une Pull Request au lieu de push direct
```

### "fatal: refusing to merge unrelated histories"

```bash
# Problème: Deux historiques différents

# Solution: Permettre le merge
git pull origin main --allow-unrelated-histories

# Cas d'usage:
# - Nouveau repo local + repo remote existant
# - Import d'un ancien repo
```

### "Repository not found"

```bash
# Problème: Mauvaise URL ou pas d'accès

# Solution 1: Vérifier l'URL
git remote -v
git remote set-url origin git@github.com:user/correct-repo.git

# Solution 2: Vérifier les permissions
# Sur GitHub/GitLab: Settings → Collaborators

# Solution 3: Vérifier l'authentification
git config credential.helper
# Peut nécessiter de se reconnecter
```

### "fatal: could not read from remote repository"

```bash
# Problème: Problème d'authentification

# Solution SSH:
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com

# Solution HTTPS:
# Vérifier les credentials
git config credential.helper

# Windows: Credential Manager
# Mac: Keychain
# Linux: cache ou store
```

---

## Récupération de données

### "Récupérer un commit supprimé"

```bash
# Utiliser reflog
git reflog
# abc123 HEAD@{0}: reset: moving to HEAD~1
# def456 HEAD@{1}: commit: Lost commit

# Récupérer
git checkout def456
git checkout -b recovered-branch
# ou
git cherry-pick def456
```

### "Récupérer un fichier supprimé"

```bash
# Fichier supprimé dans un commit récent

# Trouver quand il existait encore
git log --all --full-history -- path/to/file

# Récupérer depuis un commit spécifique
git checkout abc123 -- path/to/file

# Ou depuis le dernier commit où il existait
git checkout $(git rev-list -n 1 HEAD -- path/to/file)^ -- path/to/file
```

### "Annuler un reset --hard"

```bash
# Utiliser reflog
git reflog
# abc123 HEAD@{0}: reset: moving to HEAD~5
# def456 HEAD@{1}: commit: Last good commit

# Retourner avant le reset
git reset --hard def456
# ou
git reset --hard HEAD@{1}
```

### "Récupérer du travail non commité"

```bash
# Si vous avez fait git reset --hard par erreur
# et perdu des modifs non commitées

# Malheureusement, c'est généralement impossible
# Sauf si:

# 1. Vous aviez stashé
git stash list
git stash pop

# 2. Votre IDE a un historique local
# VSCode: Local History
# IntelliJ: Local History

# 3. Backup automatique du système
```

---

## Conflits récurrents

### "Même conflit à chaque rebase"

```bash
# Problème: Conflits répétitifs

# Solution: Activer rerere (Reuse Recorded Resolution)
git config --global rerere.enabled true

# Git se souviendra de vos résolutions
# et les appliquera automatiquement
```

### "Conflit dans un fichier binaire"

```bash
# Problème: Image, PDF, etc. en conflit

# Solution: Choisir une version
git checkout --ours image.png    # Garder la nôtre
git checkout --theirs image.png  # Garder la leur

git add image.png
git commit
```

### "Trop de conflits"

```bash
# Problème: Conflits massifs difficiles à résoudre

# Solution 1: Abort et demander de l'aide
git merge --abort
# ou
git rebase --abort

# Solution 2: Utiliser un outil graphique
git mergetool

# Solution 3: Stratégie de merge
git merge -X ours branch    # Favoriser notre version
git merge -X theirs branch  # Favoriser leur version
```

---

## Performance et maintenance

### "Git est lent"

```bash
# Problème: Opérations Git lentes

# Solution 1: Garbage collection
git gc --aggressive --prune=now

# Solution 2: Repack
git repack -a -d --depth=250 --window=250

# Solution 3: Vérifier la taille du repo
git count-objects -vH
# Si trop gros, chercher les gros fichiers
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort --numeric-sort --key=2 | \
  tail -20

# Solution 4: Nettoyer l'historique avec git-filter-repo
```

### "Repository trop gros"

```bash
# Problème: .git/ prend trop de place

# Solution 1: Vérifier l'espace
git count-objects -vH

# Solution 2: Supprimer les gros fichiers de l'historique
# Installer git-filter-repo
pip install git-filter-repo

# Trouver les gros fichiers
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort -k2 -nr | head -10

# Supprimer de l'historique
git filter-repo --path-glob '*.zip' --invert-paths

# Solution 3: Utiliser Git LFS pour les gros fichiers
git lfs install
git lfs track "*.psd"
git lfs track "*.mp4"
```

### ".git/index.lock existe"

```bash
# Problème: Fichier lock bloque les opérations

# Solution: Supprimer le fichier lock
rm -f .git/index.lock

# Cause: Git process interrompu
# Safe de supprimer si aucun git process ne tourne
```

### "Corrupted repository"

```bash
# Problème: Repository corrompu

# Solution 1: Vérifier l'intégrité
git fsck --full

# Solution 2: Récupération
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Solution 3: Si vraiment corrompu
# Cloner depuis le remote
cd ..
git clone git@github.com:user/repo.git repo-new
# Copier les modifications locales non pushées
```

---

## Workflows cassés

### "Merge au lieu de rebase"

```bash
# Problème: Historique plein de merges

# Solution: Trop tard pour changer l'historique
# Adopter un workflow pour l'avenir:
git config pull.rebase true

# Ou utiliser squash merge sur GitHub/GitLab
```

### "Force push sur main"

```bash
# Problème: Quelqu'un a force pushé sur main

# Solution 1: Si vous étiez à jour avant
git reflog
git reset --hard HEAD@{before-force-push}
git push --force-with-lease

# Solution 2: Récupérer depuis un autre dev
git fetch other-dev
git reset --hard other-dev/main
git push --force-with-lease

# Prévention: Protéger la branche main
# GitHub: Settings → Branches → Add rule
# - Require pull request reviews
# - Include administrators
```

---

## Commandes de diagnostic

```bash
# État général
git status
git log --oneline --graph --all

# Reflog (historique des actions)
git reflog
git reflog show --all

# Vérifier l'intégrité
git fsck --full

# Voir la config
git config --list
git config --list --show-origin

# Debug
GIT_TRACE=1 git command
GIT_CURL_VERBOSE=1 git command
```

---

## Checklist de dépannage

### Avant de paniquer

```bash
✅ git status          # Comprendre l'état actuel
✅ git log --oneline   # Voir l'historique récent
✅ git reflog          # Voir toutes les actions
✅ git stash list      # Vérifier les stash
✅ git remote -v       # Vérifier les remotes
✅ git branch -a       # Voir toutes les branches
```

### En cas de problème grave

```bash
1. Ne pas paniquer
2. Ne pas faire git reset --hard sans reflog
3. Sauvegarder l'état actuel:
   cp -r .git .git-backup
4. Chercher la solution
5. Tester dans un clone si possible
```

---

## Ressources d'aide

```bash
# Documentation
git help command
git command --help
man git-command

# Sites web
https://git-scm.com/docs
https://stackoverflow.com/questions/tagged/git
https://github.com/k88hudson/git-flight-rules

# Oh Shit Git!
https://ohshitgit.com/

# Visualiser
https://git-school.github.io/visualizing-git/
```

---

## Commandes de secours

```bash
# Annuler presque tout
git reflog                          # Voir l'historique
git reset --hard HEAD@{1}           # Revenir en arrière

# Récupérer un commit
git reflog | grep "commit message"
git cherry-pick SHA

# Nettoyer complètement
git clean -fdx                      # ⚠️ Supprime TOUT

# Recommencer from scratch
git reset --hard origin/main        # ⚠️ Perd les modifs locales

# Dernière option (⚠️ NUCLÉAIRE)
rm -rf .git
git clone URL .
# Copier manuellement vos modifs non pushées
```

---

[← Bonnes pratiques](./infos-git-16-bonnes-pratiques.md) | [Index](./infos-git-00-index.md)

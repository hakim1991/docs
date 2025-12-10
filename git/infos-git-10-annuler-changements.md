# ↩️ Annuler des Changements

[← Historique](./infos-git-09-historique-navigation.md) | [Index](./infos-git-00-index.md) | [Tags →](./infos-git-11-tags-releases.md)

---

## Table des matières
- [git restore - Restaurer des fichiers](#git-restore---restaurer-des-fichiers)
- [git reset - Réinitialiser](#git-reset---reinitialiser)
- [git revert - Annuler un commit](#git-revert---annuler-un-commit)
- [git clean - Nettoyer](#git-clean---nettoyer)
- [Différences entre les commandes](#differences-entre-les-commandes)
- [Récupérer des commits perdus](#recuperer-des-commits-perdus)

---

## git restore - Restaurer des fichiers

### Restaurer le working directory

```bash
# Annuler les modifications d'un fichier (revenir à HEAD)
git restore file.txt

# Annuler plusieurs fichiers
git restore file1.txt file2.txt

# Annuler tous les fichiers modifiés
git restore .

# Restaurer depuis un commit spécifique
git restore --source=abc123 file.txt
git restore --source=HEAD~3 file.txt

# Restaurer depuis une autre branche
git restore --source=main file.txt
```

### Unstage (retirer du staging)

```bash
# Retirer un fichier du staging (garde les modifications)
git restore --staged file.txt

# Retirer tous les fichiers du staging
git restore --staged .

# Équivalent ancien (avant Git 2.23)
git reset HEAD file.txt
```

### Combiner les deux

```bash
# Unstage ET annuler les modifications
git restore --staged --worktree file.txt
# Ou en deux étapes:
git restore --staged file.txt
git restore file.txt
```

---

## git reset - Réinitialiser

### Les trois modes de reset

```
        --soft          --mixed         --hard
Repository  ✓ reset      ✓ reset        ✓ reset
Staging     ✗ intact     ✓ reset        ✓ reset
Working     ✗ intact     ✗ intact       ✓ reset
```

### reset --soft

**Annule le commit mais garde tout staged**

```bash
# Annuler le dernier commit (garde les modifications staged)
git reset --soft HEAD~1

# Avant:
# main → C (HEAD)
# Staging: vide
# Working: vide

# Après git reset --soft HEAD~1:
# main → B (HEAD)
# Staging: modifications de C
# Working: vide

# Cas d'usage: Refaire le commit avec un meilleur message
git reset --soft HEAD~1
git commit -m "Meilleur message"
```

### reset --mixed (défaut)

**Annule le commit ET le staging, garde le working directory**

```bash
# Annuler le dernier commit (garde les modifications non staged)
git reset HEAD~1
git reset --mixed HEAD~1  # Même chose

# Avant:
# main → C (HEAD)
# Staging: vide
# Working: vide

# Après git reset HEAD~1:
# main → B (HEAD)
# Staging: vide
# Working: modifications de C (non staged)

# Cas d'usage: Refaire les commits différemment
git reset HEAD~3
# Maintenant vous avez les modifs de 3 commits
# Vous pouvez les recommiter comme vous voulez
git add file1.txt
git commit -m "Part 1"
git add file2.txt
git commit -m "Part 2"
```

### reset --hard

**⚠️ DESTRUCTIF: Annule tout (commit + staging + working)**

```bash
# ATTENTION: Perd toutes les modifications !
git reset --hard HEAD~1

# Avant:
# main → C (HEAD)

# Après:
# main → B (HEAD)
# Tout est perdu (C est supprimé)

# Cas d'usage: Vraiment annuler du travail
git reset --hard HEAD~1

# Revenir au dernier commit propre
git reset --hard HEAD

# Revenir à l'état d'origin
git reset --hard origin/main
```

### Reset vers un commit spécifique

```bash
# Reset vers un commit par son SHA
git reset --hard abc123

# Reset vers un tag
git reset --hard v1.0.0

# Reset vers une branche
git reset --hard origin/main
```

---

## git revert - Annuler un commit

### Revert basique

**Crée un NOUVEAU commit qui annule les changements**

```bash
# Annuler le dernier commit
git revert HEAD

# Avant:
# A ← B ← C (HEAD)

# Après git revert HEAD:
# A ← B ← C ← C' (HEAD)
# C' annule les changements de C

# Avantage: Garde l'historique (important pour branches publiques)
```

### Revert d'un commit spécifique

```bash
# Annuler un commit ancien
git revert abc123

# Annuler plusieurs commits
git revert abc123 def456 ghi789

# Annuler une plage de commits
git revert HEAD~5..HEAD
git revert abc123..def456
```

### Revert avec options

```bash
# Revert sans commit automatique (pour review)
git revert --no-commit HEAD
git revert -n HEAD
# Faire des modifications supplémentaires si besoin
git commit -m "Revert avec corrections"

# Revert d'un merge commit
git revert -m 1 abc123
# -m 1: garde les changements du premier parent (main)
# -m 2: garde les changements du second parent (branche mergée)

# Revert sans éditer le message
git revert --no-edit HEAD

# Continuer un revert en cours (après résolution de conflits)
git revert --continue

# Abandonner un revert
git revert --abort
```

---

## git clean - Nettoyer

### Nettoyer les fichiers untracked

```bash
# ⚠️ ATTENTION: Supprime définitivement les fichiers !

# Dry-run (voir ce qui sera supprimé)
git clean -n
git clean --dry-run

# Supprimer les fichiers untracked
git clean -f
git clean --force

# Supprimer les fichiers ET dossiers untracked
git clean -fd

# Supprimer aussi les fichiers ignored (.gitignore)
git clean -fx

# Supprimer TOUT (untracked + ignored)
git clean -fdx

# Mode interactif
git clean -i
# Vous demande pour chaque fichier
```

### Clean avec options

```bash
# Limiter à un dossier
git clean -f src/

# Exclure certains fichiers
git clean -f -e "*.log"

# Voir ce qui sera nettoyé (détaillé)
git clean -fdxn
```

---

## Différences entre les commandes

### Comparaison visuelle

```
┌─────────────────────────────────────────────────────┐
│              ANNULER DES CHANGEMENTS                │
└─────────────────────────────────────────────────────┘

Working Directory (modifié)
         │
         │ git restore file.txt
         ▼
Working Directory (restauré depuis HEAD)

────────────────────────────────────────────────────

Staging Area
         │
         │ git restore --staged file.txt
         ▼
Working Directory (unstaged)

────────────────────────────────────────────────────

Repository: A ← B ← C (HEAD)
         │
         │ git reset --soft HEAD~1
         ▼
Repository: A ← B (HEAD)
Staging: changements de C

────────────────────────────────────────────────────

Repository: A ← B ← C (HEAD)
         │
         │ git reset HEAD~1
         ▼
Repository: A ← B (HEAD)
Working: changements de C (unstaged)

────────────────────────────────────────────────────

Repository: A ← B ← C (HEAD)
         │
         │ git reset --hard HEAD~1
         ▼
Repository: A ← B (HEAD)
TOUT PERDU ⚠️

────────────────────────────────────────────────────

Repository: A ← B ← C (HEAD)
         │
         │ git revert HEAD
         ▼
Repository: A ← B ← C ← C' (HEAD)
C' annule C
```

### Tableau comparatif

| Commande | Scope | Destructif | Historique | Usage |
|----------|-------|------------|------------|-------|
| `restore` | Working/Staging | ❌ Non | ✅ Garde | Annuler modifs locales |
| `reset --soft` | Repository | ❌ Non | ⚠️ Modifie | Refaire commits |
| `reset --mixed` | Repo + Staging | ⚠️ Staging | ⚠️ Modifie | Unstage et recommit |
| `reset --hard` | Tout | ✅ OUI | ⚠️ Modifie | ⚠️ Tout supprimer |
| `revert` | Repository | ❌ Non | ✅ Ajoute | Annuler commit public |
| `clean` | Working | ✅ OUI | N/A | Supprimer untracked |

### Quand utiliser quoi ?

```bash
# ❓ Annuler des modifications locales non commitées
git restore file.txt

# ❓ Retirer du staging
git restore --staged file.txt

# ❓ Refaire le dernier commit avec un meilleur message
git reset --soft HEAD~1
git commit -m "Meilleur message"

# ❓ Annuler les 3 derniers commits mais garder les modifs
git reset HEAD~3
# Puis recommiter

# ❓ Tout supprimer et revenir au dernier commit
git reset --hard HEAD

# ❓ Annuler un commit déjà pushé (branche publique)
git revert abc123
git push

# ❓ Supprimer les fichiers untracked
git clean -fd
```

---

## Récupérer des commits perdus

### git reflog - Journal des actions

Le **reflog** enregistre TOUS les mouvements de HEAD (commits, reset, checkout, etc.).

```bash
# Voir le reflog
git reflog
# abc123 HEAD@{0}: commit: Add feature
# def456 HEAD@{1}: reset: moving to HEAD~1
# ghi789 HEAD@{2}: commit: WIP
# jkl012 HEAD@{3}: commit: Fix bug

# Format détaillé
git reflog show --all
```

### Récupérer un commit "perdu"

```bash
# Scénario: Vous avez fait un reset --hard par erreur
git reset --hard HEAD~3
# Oh non ! Vous avez perdu 3 commits !

# Solution: Utiliser reflog
git reflog
# abc123 HEAD@{0}: reset: moving to HEAD~3
# def456 HEAD@{1}: commit: Lost commit 3
# ghi789 HEAD@{2}: commit: Lost commit 2
# jkl012 HEAD@{3}: commit: Lost commit 1

# Récupérer le commit perdu
git reset --hard def456
# Ou
git reset --hard HEAD@{1}

# Tout est revenu ! 🎉
```

### Récupérer une branche supprimée

```bash
# Scénario: Branche supprimée par erreur
git branch -D feature
# Deleted branch feature (was abc123)

# Récupérer avec reflog
git reflog
# Trouver le dernier commit de la branche

# Recréer la branche
git branch feature abc123
# Ou
git checkout -b feature abc123
```

### Récupérer des commits d'une branche mergée et supprimée

```bash
# La branche a été mergée puis supprimée
# Mais vous voulez voir ses commits individuels

git reflog show feature
# Voir l'historique de la branche supprimée

# Ou chercher dans le reflog complet
git reflog | grep "feature"
```

---

## Cas pratiques

### Cas 1: Mauvais message de commit

```bash
# Vient de commiter avec un mauvais message
git commit -m "fix bug"  # Trop vague !

# Solution 1: Amend (si pas encore pushé)
git commit --amend -m "fix: resolve login timeout issue (fixes #123)"

# Solution 2: Reset et recommit
git reset --soft HEAD~1
git commit -m "fix: resolve login timeout issue (fixes #123)"
```

### Cas 2: Commité dans la mauvaise branche

```bash
# Vous êtes sur main et commitez par erreur
git switch main
git commit -m "feat: new feature"  # Oups !

# Solution: Déplacer le commit vers une nouvelle branche
git branch feature-branch  # Créé une branche pointant vers le commit
git reset --hard HEAD~1    # Revenir en arrière sur main
git switch feature-branch  # Switcher vers la nouvelle branche
```

### Cas 3: Supprimer plusieurs commits

```bash
# Supprimer les 5 derniers commits mais garder les modifs
git reset HEAD~5

# Supprimer les 5 derniers commits ET les modifs
git reset --hard HEAD~5

# Après un reset --hard par erreur, récupérer:
git reflog
git reset --hard HEAD@{1}
```

### Cas 4: Annuler un merge

```bash
# Viens de merger mais c'était une erreur
git merge feature
# Auto-merging...
# Merge made...

# Solution 1: Avant de push
git reset --hard HEAD~1

# Solution 2: Après push (branche publique)
git revert -m 1 HEAD
git push
```

### Cas 5: Fichier supprimé par erreur

```bash
# Supprimé un fichier
rm important.txt
git add important.txt
git commit -m "Remove file"

# Récupérer le fichier
git checkout HEAD~1 -- important.txt
# Ou
git show HEAD~1:important.txt > important.txt
```

---

## Commandes de référence rapide

```bash
# Restaurer
git restore file.txt             # Annuler modifs
git restore --staged file.txt    # Unstage
git restore --source=abc123 file # Restaurer depuis commit

# Reset
git reset --soft HEAD~1          # Annuler commit, garde staging
git reset HEAD~1                 # Annuler commit et staging
git reset --hard HEAD~1          # ⚠️ Tout supprimer

# Revert
git revert HEAD                  # Annuler commit (nouveau commit)
git revert abc123                # Annuler commit spécifique
git revert -m 1 abc123           # Annuler merge

# Clean
git clean -n                     # Dry-run
git clean -fd                    # Supprimer untracked
git clean -fdx                   # Tout supprimer

# Récupération
git reflog                       # Voir l'historique
git reset --hard HEAD@{1}        # Revenir en arrière
```

---

## ⚠️ Règles de sécurité

### Ne jamais utiliser sur branches publiques

```bash
# ❌ JAMAIS faire sur une branche publique (main, develop, etc.):
git reset --hard HEAD~1
git push --force

# Pourquoi? Cela réécrit l'historique et cause des problèmes pour les autres

# ✅ À la place, utiliser:
git revert HEAD
git push
```

### Toujours vérifier avant --hard

```bash
# ❌ MAUVAIS
git reset --hard HEAD~5  # Perte de données !

# ✅ BON
git log --oneline -5     # Vérifier ce qui sera perdu
git reset --hard HEAD~5  # Si vraiment sûr
```

---

## Prochaines étapes

Maintenant que vous savez annuler des changements, apprenez à marquer des versions :

- [**Tags et Releases**](./infos-git-11-tags-releases.md) - Versioning
- [**Workflows**](./infos-git-12-workflows.md) - Workflows Git professionnels

---

[← Historique](./infos-git-09-historique-navigation.md) | [Index](./infos-git-00-index.md) | [Tags →](./infos-git-11-tags-releases.md)

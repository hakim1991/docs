# 🚀 Outils Avancés Git

[← Workflows](./infos-git-12-workflows.md) | [Index](./infos-git-00-index.md) | [Hooks →](./infos-git-14-hooks-automatisation.md)

---

## Table des matières
- [git rebase](#git-rebase)
- [git cherry-pick](#git-cherry-pick)
- [git bisect](#git-bisect)
- [git reflog](#git-reflog)
- [git submodules](#git-submodules)
- [git worktree](#git-worktree)

---

## git rebase

### Qu'est-ce que le rebase ?

**Rebase** réécrit l'historique en déplaçant des commits sur une nouvelle base.

```
Avant rebase:
      main
        ↓
A ← B ← C ← D
      ↖
        E ← F
          ↑
       feature

Après git rebase main (sur feature):
            main
              ↓
A ← B ← C ← D ← E' ← F'
                  ↑
               feature

E et F sont "rejoués" sur D
```

### Rebase basique

```bash
# Sur votre branche feature
git checkout feature
git rebase main

# Résout les conflits si nécessaire
git rebase --continue

# Ou abandonner
git rebase --abort

# Équivalent:
git checkout feature
git rebase main
# = Rejoue les commits de feature sur main
```

### Rebase vs Merge

```bash
# MERGE: Crée un commit de merge
git checkout main
git merge feature
# Historique: A ← B ← C ← D ← M (merge commit)
#                   ↖     ↗
#                     E ← F

# REBASE: Linéarise l'historique
git checkout feature
git rebase main
git checkout main
git merge feature  # Fast-forward
# Historique: A ← B ← C ← D ← E' ← F'
```

### Rebase interactif

**Modifier, réorganiser, squash des commits**

```bash
# Rebase interactif des 5 derniers commits
git rebase -i HEAD~5

# L'éditeur s'ouvre:
pick abc123 feat: add login
pick def456 fix: typo
pick ghi789 feat: add logout
pick jkl012 fix: another typo
pick mno345 feat: add profile

# Options:
# pick   = utiliser le commit
# reword = utiliser mais changer le message
# edit   = utiliser mais s'arrêter pour amend
# squash = fusionner avec le commit précédent
# fixup  = comme squash mais ignorer le message
# drop   = supprimer le commit

# Exemple: Squash les fixes
pick abc123 feat: add login
fixup def456 fix: typo
pick ghi789 feat: add logout
fixup jkl012 fix: another typo
pick mno345 feat: add profile

# Résultat: 3 commits au lieu de 5
```

### Cas pratiques du rebase

```bash
# 1. Nettoyer l'historique avant merge
git checkout feature
git rebase -i main
# Squash les "WIP" commits
git checkout main
git merge feature

# 2. Mettre à jour la feature branch
git checkout feature
git rebase main
# feature est maintenant à jour avec main

# 3. Réorganiser les commits
git rebase -i HEAD~10
# Réorganiser dans l'ordre logique
```

### ⚠️ Règle d'or du rebase

**NE JAMAIS rebaser des commits déjà pushés/publics !**

```bash
# ❌ MAUVAIS
git checkout main
git rebase feature
git push --force
# Casse l'historique pour tout le monde !

# ✅ BON
git checkout main
git merge feature
git push
```

---

## git cherry-pick

### Qu'est-ce que cherry-pick ?

**Cherry-pick** applique un commit spécifique sur la branche courante.

```
main
  ↓
A ← B ← C
      ↖
        D ← E ← F
            ↑
         feature

git cherry-pick E
# Applique E sur main

main
  ↓
A ← B ← C ← E'
```

### Cherry-pick basique

```bash
# Appliquer un commit
git checkout main
git cherry-pick abc123

# Appliquer plusieurs commits
git cherry-pick abc123 def456 ghi789

# Appliquer une plage
git cherry-pick abc123..def456
```

### Cherry-pick avec options

```bash
# Cherry-pick sans commit auto (pour review)
git cherry-pick --no-commit abc123
git cherry-pick -n abc123

# Cherry-pick et changer l'auteur
git cherry-pick --edit abc123

# Cherry-pick et signer
git cherry-pick -S abc123

# Continuer après résolution de conflit
git cherry-pick --continue

# Abandonner
git cherry-pick --abort
```

### Cas pratiques

```bash
# 1. Hotfix depuis develop vers main
git checkout main
git cherry-pick abc123  # Commit du fix sur develop

# 2. Backport un fix vers une ancienne version
git checkout v1.x
git cherry-pick def456  # Fix de main

# 3. Récupérer un commit d'une feature branch
git checkout main
git cherry-pick ghi789  # Un commit de feature
```

---

## git bisect

### Qu'est-ce que bisect ?

**Bisect** trouve le commit qui a introduit un bug par **recherche binaire**.

```
Historique:
A ← B ← C ← D ← E ← F ← G ← H
✅  ✅  ✅  ❌  ❌  ❌  ❌  ❌

Bisect teste automatiquement:
1. Teste E (milieu) → ❌
2. Teste C (milieu de A-E) → ✅
3. Teste D (milieu de C-E) → ❌

D est le commit fautif!
```

### Bisect manuel

```bash
# 1. Démarrer bisect
git bisect start

# 2. Marquer le commit actuel comme mauvais
git bisect bad
# Ou un commit spécifique
git bisect bad HEAD

# 3. Marquer un commit ancien comme bon
git bisect good abc123

# Git checkout automatiquement le commit du milieu
# Testing: 5 revisions left to test after this

# 4. Tester manuellement
npm test
# Si ça passe:
git bisect good
# Si ça échoue:
git bisect bad

# 5. Répéter jusqu'à trouver le commit fautif
# Git affiche:
# abc123 is the first bad commit

# 6. Terminer
git bisect reset
```

### Bisect automatique

```bash
# Avec un script de test automatique
git bisect start HEAD abc123
git bisect run npm test

# Git teste automatiquement chaque commit
# et trouve le coupable !

# Avec script personnalisé
git bisect run ./test-script.sh

# Le script doit retourner:
# 0 = bon
# 1-127 (sauf 125) = mauvais
# 125 = skip (ne peut pas tester)
```

### Exemple complet

```bash
# Bug: Le login ne fonctionne plus

# 1. Démarrer
git bisect start

# 2. HEAD est mauvais (bug présent)
git bisect bad

# 3. Il y a 2 semaines c'était bon
git bisect good HEAD~50

# 4. Git checkout le commit du milieu
# Tester manuellement
npm test
git bisect bad

# 5. Continuer...
npm test
git bisect good

# ...

# 6. Git trouve le commit
# abc123 is the first bad commit
# commit abc123
# Author: John Doe
# Date: ...
# feat: refactor authentication

# 7. Examiner le commit
git show abc123

# 8. Terminer
git bisect reset

# 9. Fixer le bug
git revert abc123
# ou créer un fix
```

---

## git reflog

### Qu'est-ce que reflog ?

**Reflog** (reference log) enregistre TOUS les mouvements de HEAD.

```bash
# Voir le reflog
git reflog

# Résultat:
abc123 HEAD@{0}: commit: Add feature
def456 HEAD@{1}: reset: moving to HEAD~1
ghi789 HEAD@{2}: commit: WIP
jkl012 HEAD@{3}: checkout: moving from main to feature

# Chaque action est enregistrée !
```

### Utiliser reflog

```bash
# Voir le reflog complet
git reflog show

# Reflog d'une branche spécifique
git reflog show main
git reflog show feature

# Reflog avec dates
git reflog show --date=iso

# Reflog formaté
git reflog --pretty=oneline
```

### Récupérer avec reflog

```bash
# Scénario: Reset --hard par erreur
git reset --hard HEAD~5
# Oh non ! 5 commits perdus

# Trouver dans reflog
git reflog
# abc123 HEAD@{0}: reset: moving to HEAD~5
# def456 HEAD@{1}: commit: Lost commit

# Récupérer
git reset --hard def456
# ou
git reset --hard HEAD@{1}

# Tout est revenu ! 🎉
```

---

## git submodules

### Qu'est-ce qu'un submodule ?

**Submodule** inclut un repository Git dans un autre repository.

```
mon-projet/
├── .git/
├── src/
└── lib/
    └── external-lib/  ← Submodule (autre repository)
        ├── .git/
        └── ...
```

### Ajouter un submodule

```bash
# Ajouter un submodule
git submodule add https://github.com/user/lib.git lib/external-lib

# Commit
git commit -m "Add external-lib submodule"

# Résultat: .gitmodules créé
[submodule "lib/external-lib"]
    path = lib/external-lib
    url = https://github.com/user/lib.git
```

### Cloner avec submodules

```bash
# Cloner et initialiser les submodules
git clone --recurse-submodules https://github.com/user/projet.git

# Ou après clone
git clone https://github.com/user/projet.git
cd projet
git submodule init
git submodule update

# Ou en une commande
git submodule update --init --recursive
```

### Mettre à jour les submodules

```bash
# Update tous les submodules
git submodule update --remote

# Update un submodule spécifique
git submodule update --remote lib/external-lib

# Commit les changements
git add lib/external-lib
git commit -m "Update external-lib submodule"
```

### Supprimer un submodule

```bash
# 1. Désinscrire
git submodule deinit lib/external-lib

# 2. Supprimer du .git
git rm lib/external-lib

# 3. Commit
git commit -m "Remove external-lib submodule"

# 4. Nettoyer
rm -rf .git/modules/lib/external-lib
```

---

## git worktree

### Qu'est-ce qu'un worktree ?

**Worktree** permet d'avoir plusieurs **working directories** pour le même repository.

```
projet/
├── main/          ← Worktree principal
│   ├── .git/
│   └── src/
├── feature/       ← Worktree supplémentaire
│   └── src/
└── hotfix/        ← Autre worktree
    └── src/
```

### Créer un worktree

```bash
# Dans le repository principal
cd projet

# Créer un worktree pour une branche
git worktree add ../projet-feature feature/login
# Créé ../projet-feature avec la branche feature/login

# Créer et créer une nouvelle branche
git worktree add -b hotfix/critical ../projet-hotfix

# Lister les worktrees
git worktree list
# /home/user/projet              abc123 [main]
# /home/user/projet-feature      def456 [feature/login]
# /home/user/projet-hotfix       ghi789 [hotfix/critical]
```

### Utiliser les worktrees

```bash
# Travailler dans différents worktrees simultanément

# Terminal 1: Main
cd projet
# Continuer le développement sur main

# Terminal 2: Feature
cd projet-feature
# Travailler sur la feature

# Terminal 3: Hotfix
cd projet-hotfix
# Fixer le bug urgent

# Tous partagent le même repository Git !
# Les commits sont visibles partout
```

### Supprimer un worktree

```bash
# Supprimer le worktree
git worktree remove ../projet-feature

# Ou manuellement
rm -rf ../projet-feature
git worktree prune

# Lister les worktrees
git worktree list
```

### Cas pratiques

```bash
# 1. Review de PR sans perdre son travail
git worktree add ../review-pr123 feature/pr123
cd ../review-pr123
# Tester la PR
cd ../projet
# Reprendre son travail

# 2. Hotfix urgent sans stash
git worktree add ../hotfix hotfix/critical
cd ../hotfix
# Fixer le bug
git commit -am "fix: critical bug"
git push
cd ../projet
# Reprendre le travail en cours

# 3. Compiler deux versions simultanément
git worktree add ../build-v1 v1.0
git worktree add ../build-v2 v2.0
# Compiler les deux versions en parallèle
```

---

## Commandes de référence rapide

```bash
# Rebase
git rebase main                 # Rebaser sur main
git rebase -i HEAD~5            # Rebase interactif
git rebase --continue           # Continuer
git rebase --abort              # Abandonner

# Cherry-pick
git cherry-pick abc123          # Appliquer un commit
git cherry-pick abc..def        # Plage de commits
git cherry-pick --continue      # Continuer

# Bisect
git bisect start                # Démarrer
git bisect bad                  # Marquer mauvais
git bisect good abc123          # Marquer bon
git bisect reset                # Terminer
git bisect run npm test         # Automatique

# Reflog
git reflog                      # Voir le reflog
git reflog show main            # Reflog d'une branche
git reset --hard HEAD@{1}       # Récupérer

# Submodules
git submodule add URL path      # Ajouter
git submodule update --init     # Initialiser
git submodule update --remote   # Update

# Worktree
git worktree add path branch    # Créer
git worktree list               # Lister
git worktree remove path        # Supprimer
```

---

[← Workflows](./infos-git-12-workflows.md) | [Index](./infos-git-00-index.md) | [Hooks →](./infos-git-14-hooks-automatisation.md)

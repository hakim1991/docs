# Guide Complet Git - Index

## 📚 Table des Matières

### Fondamentaux Git
1. [📥 Introduction et Installation](./infos-git-01-introduction-installation.md)
   - Qu'est-ce que Git ?
   - Installation sur Linux (Ubuntu, Debian, CentOS, RHEL)
   - Installation sur Windows (Git Bash, Git for Windows)
   - Installation sur macOS
   - Vérification de l'installation
   - Interfaces graphiques (GitKraken, SourceTree, GitHub Desktop)

2. [⚙️ Configuration Git](./infos-git-02-configuration.md)
   - Configuration de base (user.name, user.email)
   - Niveaux de configuration (system, global, local)
   - Éditeur par défaut
   - Alias Git
   - Configuration SSH et GPG
   - Configuration avancée

3. [🧠 Concepts Fondamentaux](./infos-git-03-concepts-fondamentaux.md)
   - Repository (dépôt)
   - Working Directory, Staging Area, Repository
   - Commits et SHA
   - Branches
   - HEAD et pointeurs
   - Remote repositories
   - Les trois états de Git

4. [🎯 Commandes de Base](./infos-git-04-commandes-base.md)
   - git init - Créer un repository
   - git clone - Cloner un repository
   - git status - Voir l'état
   - git add - Ajouter au staging
   - git commit - Créer un commit
   - git log - Voir l'historique
   - git diff - Voir les différences
   - .gitignore - Ignorer des fichiers

### Branches et Collaboration
5. [🌳 Branches et Merge](./infos-git-05-branches-merge.md)
   - Créer des branches (git branch, git checkout, git switch)
   - Naviguer entre branches
   - Merger des branches (merge, fast-forward, 3-way merge)
   - Supprimer des branches
   - Stratégies de merge
   - Visualiser les branches

6. [🌐 Remotes et Collaboration](./infos-git-06-remotes-collaboration.md)
   - Concept de remote
   - git remote - Gérer les remotes
   - git push - Envoyer des commits
   - git pull - Récupérer et merger
   - git fetch - Récupérer sans merger
   - Upstream et tracking branches
   - Fork et Pull Requests

7. [⚔️ Résolution de Conflits](./infos-git-07-conflits.md)
   - Comprendre les conflits
   - Anatomie d'un conflit
   - Résoudre manuellement
   - Outils de merge (mergetool)
   - Prévenir les conflits
   - Stratégies de résolution
   - Conflits lors de rebase

### Gestion du Code
8. [💼 Stash - Travail Temporaire](./infos-git-08-stash.md)
   - Sauvegarder le travail en cours
   - Liste des stash
   - Appliquer un stash
   - Supprimer des stash
   - Stash avec branches
   - Cas d'usage pratiques

9. [📜 Historique et Navigation](./infos-git-09-historique-navigation.md)
   - git log avancé (formats, filtres)
   - git show - Voir un commit
   - git diff avancé
   - git blame - Qui a écrit quoi
   - git grep - Rechercher dans l'historique
   - Navigation dans l'historique
   - Références relatives (HEAD~, HEAD^)

10. [↩️ Annuler des Changements](./infos-git-10-annuler-changements.md)
    - git restore - Restaurer des fichiers
    - git reset (soft, mixed, hard)
    - git revert - Annuler un commit
    - git clean - Nettoyer les fichiers non trackés
    - Différences entre reset, revert, restore
    - Récupérer des commits perdus (reflog)

### Outils Avancés
11. [🏷️ Tags et Releases](./infos-git-11-tags-releases.md)
    - Tags légers vs annotés
    - Créer des tags
    - Lister et filtrer les tags
    - Pousser des tags
    - Supprimer des tags
    - Créer des releases (GitHub/GitLab)
    - Versioning sémantique

12. [🔄 Workflows Git](./infos-git-12-workflows.md)
    - Git Flow (feature, develop, release, hotfix)
    - GitHub Flow (simple et efficace)
    - GitLab Flow
    - Trunk-Based Development
    - Choisir un workflow
    - Conventions de commits

13. [🚀 Outils Avancés](./infos-git-13-outils-avances.md)
    - git rebase (interactive, onto)
    - git cherry-pick
    - git bisect - Trouver un bug
    - git reflog - Journal des actions
    - git submodules
    - git worktree
    - git archive

14. [🪝 Hooks et Automatisation](./infos-git-14-hooks-automatisation.md)
    - Types de hooks
    - pre-commit, post-commit
    - pre-push, post-merge
    - Créer des hooks
    - Hooks avec scripts
    - Husky (Node.js)
    - Linters et formatters automatiques

### Plateformes et Production
15. [🐙 GitHub / GitLab / Bitbucket](./infos-git-15-plateformes.md)
    - Pull Requests / Merge Requests
    - Code Review
    - Issues et Project Management
    - Actions / CI-CD
    - GitHub Pages
    - Webhooks
    - API et automatisation

16. [✅ Bonnes Pratiques](./infos-git-16-bonnes-pratiques.md)
    - Messages de commit clairs
    - Commits atomiques
    - Branches de courte durée
    - Ne jamais rebase sur public
    - Protection des branches
    - Code review
    - Documentation
    - Sécurité (secrets, tokens)

17. [🔧 Troubleshooting et Cas Pratiques](./infos-git-17-troubleshooting.md)
    - Problèmes courants et solutions
    - Récupérer un commit supprimé
    - Corriger le dernier commit
    - Changer l'historique
    - Nettoyer un repository
    - Migrer vers un nouveau remote
    - Gros fichiers (Git LFS)

---

## 🎯 Guide d'utilisation

### Pour les débutants
Commencez par lire dans l'ordre :
1. **Introduction et Installation** - Installer Git
2. **Configuration** - Configurer votre identité
3. **Concepts Fondamentaux** - Comprendre Git
4. **Commandes de Base** - Vos premiers commits
5. **Branches** - Travailler avec des branches

### Pour les développeurs
Focus sur :
- **Branches et Merge** - Workflow quotidien
- **Remotes** - Collaboration avec l'équipe
- **Résolution de Conflits** - Gérer les conflits
- **Workflows** - Adopter un workflow d'équipe
- **GitHub/GitLab** - Utiliser les plateformes

### Pour les leads et architectes
Lire :
- **Workflows** - Choisir un workflow adapté
- **Bonnes Pratiques** - Standards de l'équipe
- **Hooks** - Automatisation et qualité
- **GitHub/GitLab** - CI/CD et automatisation

### Pour les experts
- **Outils Avancés** - rebase, cherry-pick, bisect
- **Annuler des Changements** - reset, revert, reflog
- **Hooks** - Automatisation avancée
- **Troubleshooting** - Résoudre les problèmes complexes

---

## 📝 Commandes de référence rapide

### Configuration initiale
```bash
git config --global user.name "Votre Nom"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main
```

### Commandes de base
```bash
git init                           # Créer un repo
git clone URL                      # Cloner un repo
git status                         # Voir l'état
git add .                          # Ajouter tous les fichiers
git commit -m "message"            # Créer un commit
git log                            # Voir l'historique
git diff                           # Voir les changements
```

### Branches
```bash
git branch                         # Lister les branches
git branch nom                     # Créer une branche
git checkout nom                   # Changer de branche
git switch nom                     # Changer de branche (nouveau)
git merge nom                      # Merger une branche
git branch -d nom                  # Supprimer une branche
```

### Remote
```bash
git remote add origin URL          # Ajouter un remote
git push origin main               # Pousser vers remote
git pull origin main               # Récupérer et merger
git fetch origin                   # Récupérer sans merger
git push -u origin branch          # Pousser et tracker
```

### Annulation
```bash
git restore fichier                # Annuler modifications
git restore --staged fichier       # Unstage
git reset HEAD~1                   # Annuler dernier commit
git revert SHA                     # Créer commit inverse
git reflog                         # Voir l'historique des actions
```

### Stash
```bash
git stash                          # Sauvegarder le travail
git stash list                     # Lister les stash
git stash pop                      # Appliquer et supprimer
git stash apply                    # Appliquer sans supprimer
```

### Information
```bash
git log --oneline --graph --all    # Graphe des commits
git show SHA                       # Voir un commit
git blame fichier                  # Qui a écrit quoi
git diff branch1..branch2          # Comparer branches
```

### Avancé
```bash
git rebase main                    # Rebaser sur main
git rebase -i HEAD~3               # Rebase interactif
git cherry-pick SHA                # Appliquer un commit
git bisect start                   # Chercher un bug
```

---

## 🔗 Ressources additionnelles

### Documentation officielle
- **Git Documentation**: https://git-scm.com/doc
- **Pro Git Book** (gratuit): https://git-scm.com/book/fr/v2
- **Git Reference**: https://git-scm.com/docs

### Plateformes
- **GitHub**: https://github.com
- **GitLab**: https://gitlab.com
- **Bitbucket**: https://bitbucket.org

### Apprendre Git
- **Learn Git Branching**: https://learngitbranching.js.org/?locale=fr_FR
- **GitHub Learning Lab**: https://lab.github.com/
- **Atlassian Git Tutorials**: https://www.atlassian.com/git/tutorials

### Outils
- **GitKraken**: https://www.gitkraken.com/
- **SourceTree**: https://www.sourcetreeapp.com/
- **GitHub Desktop**: https://desktop.github.com/

---

## 🎨 Conventions

### Messages de commit

```bash
# Format recommandé
<type>(<scope>): <subject>

<body>

<footer>

# Types courants:
feat:     nouvelle fonctionnalité
fix:      correction de bug
docs:     documentation
style:    formatage, virgules manquantes, etc.
refactor: refactoring du code
test:     ajout de tests
chore:    maintenance

# Exemples:
feat(auth): add JWT authentication
fix(api): resolve CORS issue on production
docs(readme): update installation instructions
```

### Stratégie de branches

```bash
main/master     # Production
develop         # Développement
feature/*       # Nouvelles fonctionnalités
bugfix/*        # Corrections de bugs
hotfix/*        # Corrections urgentes production
release/*       # Préparation de release
```

---

## ⚡ Aide-mémoire visuel

### Les trois états de Git
```
Working Directory  →  Staging Area  →  Repository
(fichiers modifiés)   (git add)        (git commit)
```

### Workflow de base
```
1. Modifier des fichiers
2. git add fichier
3. git commit -m "message"
4. git push origin main
```

### Workflow avec branches
```
1. git checkout -b feature/nouvelle-fonction
2. Faire des modifications
3. git add .
4. git commit -m "feat: nouvelle fonction"
5. git push origin feature/nouvelle-fonction
6. Créer une Pull Request
7. Après review: git checkout main
8. git merge feature/nouvelle-fonction
```

---

**Version**: 1.0
**Dernière mise à jour**: Décembre 2025
**Auteur**: Documentation complète pour la gestion de projets avec Git

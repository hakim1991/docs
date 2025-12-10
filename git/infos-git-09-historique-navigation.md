# 📜 Historique et Navigation

[← Stash](./infos-git-08-stash.md) | [Index](./infos-git-00-index.md) | [Annuler →](./infos-git-10-annuler-changements.md)

---

## Table des matières
- [git log avancé](#git-log-avance)
- [git show - Voir un commit](#git-show---voir-un-commit)
- [git diff avancé](#git-diff-avance)
- [git blame - Qui a écrit quoi](#git-blame---qui-a-ecrit-quoi)
- [git grep - Rechercher](#git-grep---rechercher)
- [Références relatives](#references-relatives)

---

## git log avancé

### Formats personnalisés

```bash
# Format oneline custom
git log --pretty=format:"%h %an %ar - %s"
# abc123 John Doe 2 hours ago - feat: add login

# Format avec couleurs
git log --pretty=format:"%C(yellow)%h%Creset %C(blue)%an%Creset %C(green)%ar%Creset - %s"

# Placeholders disponibles:
# %H  - SHA complet
# %h  - SHA court
# %an - Nom auteur
# %ae - Email auteur
# %ad - Date auteur
# %ar - Date relative (2 days ago)
# %cn - Nom committer
# %s  - Sujet (première ligne du message)
# %b  - Corps du message
# %d  - Refs (branches, tags)

# Format complexe
git log --pretty=format:"%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)"
```

### Filtres temporels

```bash
# Depuis une date
git log --since="2024-01-01"
git log --after="2024-01-01"

# Jusqu'à une date
git log --until="2024-12-31"
git log --before="2024-12-31"

# Période
git log --since="2024-01-01" --until="2024-12-31"

# Dates relatives
git log --since="2 weeks ago"
git log --since="3 days ago"
git log --since="yesterday"
git log --since="1 month ago"
git log --since="2024-01-01" --until="yesterday"

# Dernières N heures
git log --since="5 hours ago"
```

### Filtres par auteur

```bash
# Par nom
git log --author="John"
git log --author="John Doe"

# Par email
git log --author="john@example.com"

# Plusieurs auteurs (regex)
git log --author="John\|Jane"

# Exclure un auteur
git log --author="^(?!John).*$"

# Par committer (différent de l'auteur)
git log --committer="John"
```

### Filtres par message

```bash
# Recherche dans les messages de commit
git log --grep="fix"
git log --grep="feature"
git log --grep="bug"

# Case insensitive
git log --grep="FIX" -i

# Regex
git log --grep="feat|fix"

# Messages contenant plusieurs mots (ET)
git log --grep="login" --grep="auth" --all-match

# Messages contenant plusieurs mots (OU)
git log --grep="login\|auth"

# Exclure des commits
git log --grep="WIP" --invert-grep
```

### Filtres par fichiers

```bash
# Commits qui ont modifié un fichier
git log -- path/to/file.txt
git log --follow -- file.txt  # Suit les renommages

# Plusieurs fichiers
git log -- file1.txt file2.txt

# Tous les fichiers .js
git log -- "*.js"

# Fichiers dans un dossier
git log -- src/

# Commits qui ont ajouté/supprimé du code contenant "function"
git log -S "function"
git log -S "console.log"

# Commits qui ont ajouté/supprimé du code matchant une regex
git log -G "function.*login"

# Voir les modifications du fichier
git log -p -- file.txt
```

### Limiter les résultats

```bash
# Derniers N commits
git log -5
git log -n 5
git log --max-count=5

# Skip N commits
git log --skip=10

# Combiner
git log --skip=10 -n 5  # Commits 11-15

# Jusqu'à un certain commit
git log abc123..HEAD
git log abc123..

# Entre deux commits
git log abc123..def456

# Pas dans une branche
git log main..feature      # Commits dans feature pas dans main
git log feature..main      # Commits dans main pas dans feature
git log main...feature     # Commits différents entre les deux
```

### Options d'affichage

```bash
# Avec graphe
git log --graph --oneline --all

# Avec stats
git log --stat
# Montre les fichiers modifiés et nombre de lignes

# Avec patch (diff complet)
git log -p
git log --patch

# Format court
git log --oneline

# Décoration (branches, tags)
git log --decorate
git log --oneline --decorate

# Tout combiner (alias recommandé)
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative --all
```

---

## git show - Voir un commit

### Show basique

```bash
# Voir le dernier commit
git show
git show HEAD

# Voir un commit spécifique
git show abc123
git show HEAD~3

# Avec un format spécifique
git show --pretty=fuller abc123
```

### Show avancé

```bash
# Voir seulement les stats
git show --stat abc123

# Voir seulement les noms de fichiers
git show --name-only abc123
git show --name-status abc123

# Voir un fichier spécifique d'un commit
git show abc123:path/to/file.txt

# Voir un fichier d'une autre branche
git show main:file.txt
git show feature:src/app.js

# Voir les métadonnées seulement (pas de diff)
git show --no-patch abc123
git show -s abc123

# Comparer un fichier entre commits
git show abc123:file.txt > /tmp/old.txt
git show def456:file.txt > /tmp/new.txt
diff /tmp/old.txt /tmp/new.txt
```

---

## git diff avancé

### Diff entre commits

```bash
# Entre deux commits
git diff abc123 def456

# Entre commit et HEAD
git diff abc123
git diff abc123 HEAD

# Depuis N commits
git diff HEAD~5
git diff HEAD~5 HEAD
```

### Diff entre branches

```bash
# Entre deux branches
git diff main feature
git diff main..feature  # Même chose

# Triple-dot (depuis leur ancêtre commun)
git diff main...feature
# Montre seulement ce qui a changé dans feature

# Fichiers différents
git diff --name-only main feature
git diff --name-status main feature
```

### Options de diff

```bash
# Par mot au lieu de par ligne
git diff --word-diff
git diff --color-words

# Ignorer les espaces
git diff -w
git diff --ignore-all-space

# Ignorer les changements d'espaces en fin de ligne
git diff --ignore-space-at-eol

# Contexte (lignes avant/après)
git diff -U10
git diff --unified=10

# Stats seulement
git diff --stat
git diff --shortstat
git diff --numstat

# Noms de fichiers et stats
git diff --name-status
```

### Diff fonctions

```bash
# Montrer dans quelle fonction le changement a eu lieu
git diff -p
git diff --show-function

# Exemple de sortie:
# diff --git a/app.js b/app.js
# @@ -15,7 +15,9 @@ function login(user, password) {
#    if (password.length < 8) {
# +    console.log("Password too short");
#      return false;
#    }
```

---

## git blame - Qui a écrit quoi

### Blame basique

```bash
# Voir qui a écrit chaque ligne
git blame file.txt

# Résultat:
# abc123 (John Doe 2024-01-15 14:30:00 1) function login() {
# def456 (Jane Smith 2024-01-20 10:15:00 2)   console.log("Login");
# abc123 (John Doe 2024-01-15 14:30:00 3) }
```

### Blame avancé

```bash
# Lignes spécifiques
git blame -L 10,20 file.txt
git blame -L 10,+10 file.txt  # 10 lignes à partir de la ligne 10

# Ignorer les espaces
git blame -w file.txt

# Montrer l'email
git blame -e file.txt

# Format court
git blame -s file.txt

# Voir les commits de merge aussi
git blame -M file.txt

# Détecter les lignes copiées
git blame -C file.txt

# Voir le contenu du commit qui a modifié
git blame -c file.txt
```

### Blame interactif

```bash
# Dans VS Code avec GitLens
# Hover sur une ligne → voir qui l'a écrite

# En ligne de commande avec less
git blame file.txt | less

# Combiner avec show
git blame file.txt | grep "abc123"
git show abc123
```

---

## git grep - Rechercher

### Grep basique

```bash
# Rechercher dans le working directory
git grep "function"

# Case insensitive
git grep -i "function"

# Ligne entière
git grep -w "function"  # Mot entier seulement

# Avec numéros de ligne
git grep -n "function"

# Compter les occurrences
git grep -c "function"
```

### Grep avancé

```bash
# Rechercher dans un commit spécifique
git grep "function" abc123

# Rechercher dans toutes les branches
git grep "function" $(git rev-list --all)

# Rechercher avec regex
git grep -E "function.*(login|auth)"

# Rechercher plusieurs patterns (AND)
git grep -e "function" --and -e "login"

# Rechercher plusieurs patterns (OR)
git grep -e "function" -e "class"

# Rechercher dans certains fichiers
git grep "function" -- "*.js"

# Exclure certains fichiers
git grep "function" -- ":!*.test.js"

# Contexte (lignes avant/après)
git grep -A 3 "function"  # 3 lignes après
git grep -B 3 "function"  # 3 lignes avant
git grep -C 3 "function"  # 3 lignes avant et après
```

---

## Références relatives

### HEAD~N et HEAD^N

```bash
# HEAD~N : N commits en arrière (en suivant les premiers parents)
HEAD~1    # Parent de HEAD (1 commit avant)
HEAD~2    # Grand-parent (2 commits avant)
HEAD~3    # 3 commits avant

# HEAD^N : Nème parent (pour les merges)
HEAD^1    # Premier parent
HEAD^2    # Deuxième parent (branche mergée)

# Exemples:
git show HEAD~1        # Voir le commit parent
git show HEAD~3        # Voir 3 commits avant
git diff HEAD~5 HEAD   # Diff des 5 derniers commits

# Combiner
HEAD~2^2   # Deuxième parent du grand-parent
HEAD^^^    # Même que HEAD~3
```

### Références symboliques

```bash
# Branches
main           # Dernier commit de main
origin/main    # Dernier commit de origin/main
feature        # Dernier commit de feature

# Tags
v1.0.0         # Tag v1.0.0

# HEAD
HEAD           # Commit courant
HEAD@{1}       # Position précédente de HEAD
HEAD@{5}       # HEAD il y a 5 mouvements

# Branches avec reflog
main@{yesterday}         # main hier
main@{2.days.ago}       # main il y a 2 jours
main@{2024-01-01}       # main au 1er janvier 2024
```

### Plages de commits

```bash
# Depuis un commit jusqu'à HEAD
abc123..HEAD
abc123..

# Entre deux commits
abc123..def456

# Exclusion
^abc123 def456   # Tous les commits jusqu'à def456 sauf abc123

# Triple-dot (différence symétrique)
main...feature
# Commits dans main OU feature mais pas dans les deux
```

---

## Commandes combinées utiles

### Alias recommandés

```bash
# Log graphique complet
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# Utilisation:
git lg
git lg --all
git lg -20  # 20 derniers commits

# Log avec stats
git config --global alias.ls "log --stat --oneline"

# Voir l'historique d'un fichier
git config --global alias.filelog "log --follow -p --"

# Utilisation:
git filelog path/to/file.txt
```

### Workflows pratiques

```bash
# Voir ce qui a changé cette semaine
git log --since="1 week ago" --oneline --author="$(git config user.name)"

# Voir les commits non pushés
git log origin/main..HEAD

# Voir les commits à pull
git log HEAD..origin/main

# Chercher qui a introduit un bug
git log -S "buggy code" -p

# Statistiques des contributeurs
git shortlog -sn
git shortlog -sn --since="1 month ago"

# Voir les fichiers les plus modifiés
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10
```

---

## Commandes de référence rapide

```bash
# Log
git log --oneline --graph --all  # Graphe complet
git log --author="John"          # Par auteur
git log --since="1 week ago"     # Depuis date
git log --grep="fix"             # Par message
git log -- file.txt              # Par fichier
git log -S "code"                # Par contenu

# Show
git show HEAD                    # Voir commit
git show abc123:file.txt         # Voir fichier d'un commit

# Diff
git diff abc123 def456           # Entre commits
git diff main feature            # Entre branches
git diff --stat                  # Stats seulement

# Blame
git blame file.txt               # Qui a écrit
git blame -L 10,20 file.txt      # Lignes spécifiques

# Grep
git grep "pattern"               # Rechercher
git grep -n "pattern"            # Avec numéros ligne
```

---

## Prochaines étapes

Maintenant que vous savez naviguer dans l'historique, apprenez à annuler des changements :

- [**Annuler des Changements**](./infos-git-10-annuler-changements.md) - Défaire des erreurs
- [**Tags et Releases**](./infos-git-11-tags-releases.md) - Marquer des versions

---

[← Stash](./infos-git-08-stash.md) | [Index](./infos-git-00-index.md) | [Annuler →](./infos-git-10-annuler-changements.md)

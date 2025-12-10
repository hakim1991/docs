# ⚙️ Configuration Git

[← Introduction](./infos-git-01-introduction-installation.md) | [Index](./infos-git-00-index.md) | [Concepts →](./infos-git-03-concepts-fondamentaux.md)

---

## Table des matières
- [Configuration de base](#configuration-de-base)
- [Niveaux de configuration](#niveaux-de-configuration)
- [Configuration de l'identité](#configuration-de-lidentite)
- [Configuration de l'éditeur](#configuration-de-lediteur)
- [Alias Git](#alias-git)
- [Configuration SSH](#configuration-ssh)
- [Configuration GPG](#configuration-gpg)
- [Configurations avancées](#configurations-avancees)

---

## Configuration de base

### Première configuration obligatoire

Avant d'utiliser Git, vous **devez** configurer votre identité. Ces informations seront associées à chaque commit.

```bash
# Configurer votre nom (obligatoire)
git config --global user.name "Votre Nom"

# Configurer votre email (obligatoire)
git config --global user.email "votre.email@example.com"

# Vérifier la configuration
git config --list

# Ou vérifier une valeur spécifique
git config user.name
git config user.email
```

**⚠️ Important :** Utilisez l'email associé à votre compte GitHub/GitLab pour que vos commits soient correctement attribués.

### Configuration de la branche par défaut

```bash
# Définir "main" comme nom de branche par défaut (recommandé)
git config --global init.defaultBranch main

# Au lieu de "master" (ancien standard)
# Note: GitHub, GitLab utilisent "main" par défaut maintenant
```

---

## Niveaux de configuration

Git a **trois niveaux** de configuration qui s'appliquent dans cet ordre de priorité :

```
Local (repository)  >  Global (utilisateur)  >  System (machine)
   .git/config      >    ~/.gitconfig       >  /etc/gitconfig
```

### 1. Configuration System (--system)

S'applique à **tous les utilisateurs** de la machine.

```bash
# Voir la configuration system
git config --system --list

# Modifier (nécessite sudo/admin)
sudo git config --system core.editor vim

# Fichier de configuration:
# Linux: /etc/gitconfig
# Windows: C:\Program Files\Git\etc\gitconfig
```

### 2. Configuration Global (--global)

S'applique à **l'utilisateur courant** sur tous ses repositories.

```bash
# Voir la configuration global
git config --global --list

# Modifier
git config --global user.name "Votre Nom"

# Fichier de configuration:
# Linux/Mac: ~/.gitconfig ou ~/.config/git/config
# Windows: C:\Users\USERNAME\.gitconfig
```

### 3. Configuration Local (--local)

S'applique **uniquement au repository courant**. C'est le niveau par défaut.

```bash
# Voir la configuration local (dans un repo)
git config --local --list

# Modifier
git config --local user.email "autre.email@example.com"

# Fichier de configuration:
# .git/config (dans le repository)
```

### Ordre de priorité

```bash
# Exemple: Différentes identités pour différents repos

# Global (pour tous vos projets perso)
git config --global user.name "John Doe"
git config --global user.email "john@personal.com"

# Local (pour un projet professionnel spécifique)
cd ~/work/company-project
git config --local user.email "john.doe@company.com"
# Le nom reste "John Doe", mais l'email change pour ce repo
```

---

## Configuration de l'identité

### Nom et email

```bash
# Configuration globale (recommandé pour débuter)
git config --global user.name "Prénom Nom"
git config --global user.email "email@example.com"

# Vérifier
git config user.name
git config user.email

# Voir d'où vient la configuration
git config --show-origin user.name
# Affiche: file:/home/user/.gitconfig	Prénom Nom
```

### Identités multiples (travail vs personnel)

```bash
# Méthode 1: Configuration conditionnelle (Git 2.13+)

# Dans ~/.gitconfig
[user]
    name = Prénom Nom
    email = perso@email.com

# Utiliser un email différent pour les repos de travail
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work

# Créer ~/.gitconfig-work
[user]
    email = prenom.nom@company.com

# Maintenant:
# - Repos dans ~/work/ utilisent prenom.nom@company.com
# - Autres repos utilisent perso@email.com
```

```bash
# Méthode 2: Configuration locale par projet

# Pour un projet spécifique
cd ~/work/company-project
git config --local user.email "prenom.nom@company.com"

# Vérifier quelle identité sera utilisée
git config user.email
```

### Masquer votre email (GitHub)

GitHub fournit un email "no-reply" pour masquer votre vrai email :

```bash
# Format: USERNAME@users.noreply.github.com
git config --global user.email "username@users.noreply.github.com"

# Ou avec votre ID GitHub:
# ID@username.users.noreply.github.com
git config --global user.email "12345678+username@users.noreply.github.com"

# Trouver votre email no-reply:
# GitHub → Settings → Emails → "Keep my email addresses private"
```

---

## Configuration de l'éditeur

### Choisir l'éditeur par défaut

Git utilise un éditeur pour les messages de commit, rebase interactif, etc.

```bash
# Visual Studio Code (recommandé)
git config --global core.editor "code --wait"

# Vim (par défaut sur Linux)
git config --global core.editor vim

# Nano (simple)
git config --global core.editor nano

# Sublime Text
git config --global core.editor "subl -n -w"

# Atom
git config --global core.editor "atom --wait"

# Notepad++ (Windows)
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"

# Notepad (Windows, simple)
git config --global core.editor notepad

# Emacs
git config --global core.editor emacs

# Vérifier
git config core.editor
```

### Test de l'éditeur

```bash
# Ouvrir l'éditeur configuré
git config --global --edit

# Cela ouvre ~/.gitconfig dans votre éditeur
```

---

## Alias Git

Les **alias** permettent de créer des raccourcis pour les commandes Git.

### Alias simples

```bash
# Créer des alias
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'

# Utilisation
git st          # au lieu de git status
git co main     # au lieu de git checkout main
git br          # au lieu de git branch
git ci -m "msg" # au lieu de git commit -m "msg"
git unstage file.txt  # au lieu de git reset HEAD -- file.txt
git last        # voir le dernier commit
```

### Alias avancés

```bash
# Log graphique coloré
git config --global alias.lg "log --oneline --graph --decorate --all"

# Log avec statistiques
git config --global alias.ll "log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)%d%Creset %C(bold blue)<%an>%Creset' --date=short"

# Voir les branches avec leur dernier commit
git config --global alias.b "branch -vv"

# Diff avec couleurs
git config --global alias.d "diff --color-words"

# Voir les fichiers modifiés
git config --global alias.changed "diff --name-only"

# Annuler le dernier commit (garde les changements)
git config --global alias.undo "reset HEAD~1 --mixed"

# Amend rapide
git config --global alias.amend "commit --amend --no-edit"

# Lister les alias
git config --global alias.aliases "config --get-regexp ^alias\."
```

### Alias avec paramètres (fonctions shell)

```bash
# Créer une branche et switcher dessus
git config --global alias.cb '!git checkout -b'

# Utilisation:
git cb feature/nouvelle-fonction
# Équivaut à: git checkout -b feature/nouvelle-fonction

# Pousser et créer l'upstream automatiquement
git config --global alias.publish '!git push -u origin $(git branch --show-current)'

# Supprimer les branches mergées
git config --global alias.cleanup '!git branch --merged | grep -v "\*" | xargs -n 1 git branch -d'
```

### Alias recommandés (copier-coller)

Ajoutez ceci à votre `~/.gitconfig` :

```ini
[alias]
    # Raccourcis de base
    st = status
    co = checkout
    sw = switch
    br = branch
    ci = commit
    cp = cherry-pick

    # Log amélioré
    lg = log --oneline --graph --decorate --all
    ll = log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)%d%Creset %C(bold blue)<%an>%Creset' --date=short
    last = log -1 HEAD

    # Diff
    d = diff
    ds = diff --staged
    dw = diff --color-words

    # Status
    s = status -sb

    # Branches
    b = branch -vv
    ba = branch -a -vv

    # Commit
    c = commit
    ca = commit -a
    cm = commit -m
    cam = commit -am
    amend = commit --amend --no-edit

    # Reset
    unstage = reset HEAD --
    undo = reset HEAD~1 --mixed

    # Remote
    publish = !git push -u origin $(git branch --show-current)

    # Utilitaires
    aliases = config --get-regexp ^alias\.
    cleanup = !git branch --merged | grep -v "\\*" | xargs -n 1 git branch -d
```

---

## Configuration SSH

SSH permet de se connecter à GitHub/GitLab sans mot de passe.

### Générer une clé SSH

```bash
# Générer une nouvelle clé SSH
ssh-keygen -t ed25519 -C "votre.email@example.com"

# Si ed25519 n'est pas supporté, utiliser RSA
ssh-keygen -t rsa -b 4096 -C "votre.email@example.com"

# Suivre les instructions:
# 1. Chemin: Appuyer sur Entrée (utilise ~/.ssh/id_ed25519)
# 2. Passphrase: Optionnel (recommandé pour la sécurité)

# Démarrer l'agent SSH
eval "$(ssh-agent -s)"

# Ajouter la clé à l'agent
ssh-add ~/.ssh/id_ed25519

# Afficher la clé publique (à copier)
cat ~/.ssh/id_ed25519.pub
```

### Windows (Git Bash)

```bash
# Même commandes que Linux/Mac
ssh-keygen -t ed25519 -C "votre.email@example.com"

# Ou utiliser l'agent SSH de Windows
# Services → OpenSSH Authentication Agent → Démarrer
```

### Ajouter la clé à GitHub

1. Copier la clé publique:
```bash
# Linux/Mac
cat ~/.ssh/id_ed25519.pub | pbcopy    # Mac
cat ~/.ssh/id_ed25519.pub | xclip     # Linux

# Windows (Git Bash)
cat ~/.ssh/id_ed25519.pub | clip
```

2. GitHub → Settings → SSH and GPG keys → New SSH key
3. Coller la clé et donner un nom

### Tester la connexion

```bash
# Tester la connexion à GitHub
ssh -T git@github.com
# Résultat: Hi username! You've successfully authenticated...

# GitLab
ssh -T git@gitlab.com

# Bitbucket
ssh -T git@bitbucket.org
```

### Configuration SSH avancée

```bash
# Fichier ~/.ssh/config

# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# GitLab
Host gitlab.com
    HostName gitlab.com
    User git
    IdentityFile ~/.ssh/id_ed25519_gitlab
    IdentitiesOnly yes

# Serveur perso
Host git.mycompany.com
    HostName git.mycompany.com
    User git
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_work
```

---

## Configuration GPG

GPG permet de **signer** vos commits pour prouver leur authenticité.

### Générer une clé GPG

```bash
# Installer GPG si nécessaire
# Ubuntu/Debian
sudo apt install gnupg

# macOS
brew install gnupg

# Générer une clé
gpg --full-generate-key

# Choisir:
# 1. Type: RSA and RSA (default)
# 2. Taille: 4096 bits
# 3. Validité: 0 (n'expire pas) ou 1y (1 an)
# 4. Nom et email (même que Git)
# 5. Passphrase

# Lister les clés
gpg --list-secret-keys --keyid-format LONG

# Résultat:
# sec   rsa4096/ABCD1234EFGH5678 2024-01-01 [SC]
#       ABC...DEF
# uid                 [ultimate] Votre Nom <email@example.com>

# L'ID de la clé est: ABCD1234EFGH5678
```

### Configurer Git pour utiliser GPG

```bash
# Configurer la clé GPG dans Git
git config --global user.signingkey ABCD1234EFGH5678

# Signer les commits automatiquement
git config --global commit.gpgsign true

# Signer les tags automatiquement
git config --global tag.gpgsign true

# Windows: Indiquer où est gpg.exe
git config --global gpg.program "C:/Program Files/Git/usr/bin/gpg.exe"
```

### Ajouter la clé à GitHub

```bash
# Exporter la clé publique
gpg --armor --export ABCD1234EFGH5678

# Copier le résultat (commence par -----BEGIN PGP PUBLIC KEY BLOCK-----)

# GitHub → Settings → SSH and GPG keys → New GPG key
# Coller la clé
```

### Signer un commit

```bash
# Signer un commit spécifique
git commit -S -m "Commit signé"

# Si commit.gpgsign = true, automatique
git commit -m "Commit signé automatiquement"

# Vérifier les signatures
git log --show-signature
```

---

## Configurations avancées

### Line endings (CRLF vs LF)

```bash
# Windows (convertit LF → CRLF au checkout)
git config --global core.autocrlf true

# Linux/Mac (convertit CRLF → LF au commit)
git config --global core.autocrlf input

# Désactiver (pas recommandé)
git config --global core.autocrlf false
```

### Couleurs

```bash
# Activer les couleurs (généralement déjà actif)
git config --global color.ui auto

# Personnaliser les couleurs
git config --global color.status.changed "yellow bold"
git config --global color.status.untracked "red bold"
git config --global color.diff.meta "blue bold"
```

### Comportement de push

```bash
# Push uniquement la branche courante (recommandé)
git config --global push.default simple

# Push toutes les branches
git config --global push.default matching

# Push et créer upstream automatiquement (Git 2.37+)
git config --global push.autoSetupRemote true
```

### Comportement de pull

```bash
# Pull avec rebase (recommandé pour un historique propre)
git config --global pull.rebase true

# Pull avec merge (comportement par défaut)
git config --global pull.rebase false

# Fast-forward uniquement
git config --global pull.ff only
```

### Merge et diff

```bash
# Outil de merge
git config --global merge.tool vimdiff

# Outil de diff
git config --global diff.tool vimdiff

# Ne pas créer de fichiers .orig après résolution de conflits
git config --global mergetool.keepBackup false

# Afficher les conflits avec 3 colonnes
git config --global merge.conflictstyle diff3
```

### Performance

```bash
# Activer le cache de credentials
# Linux/Mac (cache pendant 1h)
git config --global credential.helper cache

# Linux/Mac (cache pendant 24h)
git config --global credential.helper 'cache --timeout=86400'

# Windows (stocke de façon permanente)
git config --global credential.helper wincred

# macOS (utilise Keychain)
git config --global credential.helper osxkeychain
```

### Ignorer les permissions

```bash
# Utile sur Windows où les permissions sont différentes
git config --global core.fileMode false
```

### Configuration du proxy

```bash
# Si vous êtes derrière un proxy d'entreprise

# HTTP/HTTPS
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy http://proxy.company.com:8080

# Avec authentification
git config --global http.proxy http://user:password@proxy.company.com:8080

# Désactiver la vérification SSL (pas recommandé)
git config --global http.sslVerify false

# Proxy pour un site spécifique
git config --global http.https://github.com.proxy http://proxy:8080

# Supprimer le proxy
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## Voir et éditer la configuration

### Lister la configuration

```bash
# Voir toute la configuration
git config --list

# Voir avec l'origine (fichier)
git config --list --show-origin

# Voir un niveau spécifique
git config --global --list
git config --local --list
git config --system --list

# Voir une valeur spécifique
git config user.name
git config user.email
```

### Éditer la configuration

```bash
# Éditer avec l'éditeur configuré
git config --global --edit

# Éditer directement le fichier
# Linux/Mac
nano ~/.gitconfig
vim ~/.gitconfig

# Windows
notepad C:\Users\USERNAME\.gitconfig

# Ou dans VS Code
code ~/.gitconfig
```

### Supprimer une configuration

```bash
# Supprimer une clé
git config --global --unset user.name

# Supprimer une section entière
git config --global --remove-section alias
```

---

## Configuration complète recommandée

Voici un fichier `~/.gitconfig` complet et optimisé :

```ini
[user]
    name = Votre Nom
    email = votre.email@example.com
    signingkey = VOTRE_CLE_GPG

[init]
    defaultBranch = main

[core]
    editor = code --wait
    autocrlf = input    # Linux/Mac: input, Windows: true
    fileMode = false    # Ignorer les changements de permissions

[commit]
    gpgsign = true      # Signer les commits (si GPG configuré)

[pull]
    rebase = true       # Rebase au lieu de merge lors du pull

[push]
    default = simple
    autoSetupRemote = true  # Git 2.37+

[merge]
    conflictstyle = diff3
    tool = vscode

[mergetool "vscode"]
    cmd = code --wait $MERGED

[diff]
    tool = vscode

[difftool "vscode"]
    cmd = code --wait --diff $LOCAL $REMOTE

[color]
    ui = auto

[alias]
    # Raccourcis
    st = status
    co = checkout
    sw = switch
    br = branch
    ci = commit

    # Log
    lg = log --oneline --graph --decorate --all
    ll = log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)%d%Creset %C(bold blue)<%an>%Creset' --date=short

    # Utilitaires
    unstage = reset HEAD --
    amend = commit --amend --no-edit
    publish = !git push -u origin $(git branch --show-current)
    aliases = config --get-regexp ^alias\.

[credential]
    helper = cache --timeout=86400  # Linux/Mac
    # helper = wincred              # Windows
    # helper = osxkeychain          # macOS
```

---

## Commandes de référence rapide

```bash
# Configuration de base
git config --global user.name "Nom"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main

# Voir la configuration
git config --list
git config --list --show-origin
git config user.name

# Éditer
git config --global --edit

# Supprimer
git config --global --unset key
git config --global --remove-section section

# Alias
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"

# SSH
ssh-keygen -t ed25519 -C "email@example.com"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
```

---

## Prochaines étapes

Maintenant que Git est configuré, apprenez les concepts fondamentaux :

- [**Concepts Fondamentaux**](./infos-git-03-concepts-fondamentaux.md) - Comprendre comment Git fonctionne
- [**Commandes de Base**](./infos-git-04-commandes-base.md) - Vos premiers commits

---

[← Introduction](./infos-git-01-introduction-installation.md) | [Index](./infos-git-00-index.md) | [Concepts →](./infos-git-03-concepts-fondamentaux.md)

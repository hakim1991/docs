# 💻 Bash Aliases - Guide Complet

## Qu'est-ce qu'un alias bash ?

Un alias est un raccourci pour une commande ou une série de commandes. Il permet de créer des commandes personnalisées plus courtes et plus faciles à retenir.

```bash
# Exemple simple
alias ll='ls -lah'

# Maintenant 'll' exécute 'ls -lah'
ll
```

## Fichiers de configuration

### ~/.bashrc

Fichier principal de configuration bash pour les sessions interactives.

```bash
# Éditer .bashrc
nano ~/.bashrc
# ou
vim ~/.bashrc
```

### ~/.bash_aliases

Fichier dédié aux alias (plus propre et organisé).

```bash
# Créer ou éditer .bash_aliases
nano ~/.bash_aliases

# Dans ~/.bashrc, ajouter si pas déjà présent :
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
```

### Recharger la configuration

```bash
# Recharger .bashrc
source ~/.bashrc

# Ou
. ~/.bashrc

# Recharger .bash_aliases
source ~/.bash_aliases
```

## Créer des alias

### Syntaxe de base

```bash
# Syntaxe
alias nom='commande'

# Exemples
alias l='ls'
alias la='ls -a'
alias ll='ls -lah'
```

### Alias temporaire (session actuelle uniquement)

```bash
# Créer un alias temporaire
alias temp='echo "Alias temporaire"'

# Il disparaîtra à la fermeture du terminal
```

### Alias permanent

```bash
# Ajouter dans ~/.bash_aliases
echo "alias ll='ls -lah'" >> ~/.bash_aliases

# Recharger
source ~/.bash_aliases
```

## Alias courants et utiles

### Navigation

```bash
# Navigation rapide
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

# Retour au répertoire précédent
alias back='cd -'

# Aller au home
alias home='cd ~'

# Répertoires fréquents
alias proj='cd ~/projets'
alias docs='cd ~/Documents'
alias down='cd ~/Downloads'
alias desk='cd ~/Desktop'
```

### Listing de fichiers (ls)

```bash
# Listing détaillé
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'

# Tri par date (plus récent en premier)
alias lt='ls -lath'

# Tri par taille
alias lsize='ls -laSh'

# Afficher uniquement les dossiers
alias ldir='ls -d */'

# Avec couleurs
alias ls='ls --color=auto'
```

### Grep avec couleurs

```bash
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
```

### Confirmation avant actions dangereuses

```bash
# Demander confirmation avant suppression
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Ou version plus agressive
alias rmi='rm -i'
alias rmf='rm -rf'  # Attention !
```

### Git

```bash
# Status
alias gs='git status'
alias gst='git status -sb'

# Add
alias ga='git add'
alias gaa='git add .'

# Commit
alias gc='git commit'
alias gcm='git commit -m'
alias gcam='git commit -am'

# Push/Pull
alias gp='git push'
alias gpl='git pull'
alias gpom='git push origin main'
alias gplom='git pull origin main'

# Branch
alias gb='git branch'
alias gba='git branch -a'
alias gbd='git branch -d'

# Checkout
alias gco='git checkout'
alias gcob='git checkout -b'

# Log
alias gl='git log'
alias glo='git log --oneline'
alias glog='git log --oneline --graph --decorate'

# Diff
alias gd='git diff'
alias gds='git diff --staged'

# Stash
alias gst='git stash'
alias gsta='git stash apply'
alias gstp='git stash pop'

# Clone
alias gcl='git clone'

# Fetch
alias gf='git fetch'
alias gfa='git fetch --all'

# Merge
alias gm='git merge'

# Reset
alias grh='git reset HEAD'
alias grhh='git reset --hard HEAD'

# Aliases composés
alias gcpom='git commit -am "update" && git push origin main'
alias gsync='git pull && git push'
```

### Docker

```bash
# Docker
alias d='docker'
alias dc='docker-compose'
alias dcu='docker-compose up'
alias dcd='docker-compose down'
alias dcb='docker-compose build'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias dex='docker exec -it'
alias drm='docker rm'
alias drmi='docker rmi'
alias dstop='docker stop $(docker ps -aq)'
alias dprune='docker system prune -af'

# Docker logs
alias dlogs='docker logs -f'
```

### Système et processus

```bash
# Informations système
alias df='df -h'
alias du='du -h'
alias free='free -h'

# Top amélioré
alias top='htop'

# Processus
alias ps='ps aux'
alias psg='ps aux | grep'

# Ports
alias ports='netstat -tulanp'
alias listening='lsof -i -P | grep LISTEN'

# Redémarrage rapide
alias reboot='sudo reboot'
alias shutdown='sudo shutdown -h now'
```

### Réseau

```bash
# Ping
alias ping='ping -c 5'

# IP publique
alias myip='curl ifconfig.me'
alias localip='hostname -I'

# Connexions réseau
alias netstat='netstat -tulanp'

# Speed test
alias speedtest='curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -'

# Wget avec reprise
alias wget='wget -c'
```

### Apt (Debian/Ubuntu)

```bash
alias update='sudo apt update'
alias upgrade='sudo apt upgrade'
alias install='sudo apt install'
alias remove='sudo apt remove'
alias autoremove='sudo apt autoremove'
alias search='apt search'
alias full-upgrade='sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y'
```

### Python

```bash
# Python
alias py='python3'
alias python='python3'
alias pip='pip3'

# Venv
alias venv='python3 -m venv venv'
alias activate='source venv/bin/activate'

# Server
alias serve='python3 -m http.server'
alias serve8080='python3 -m http.server 8080'
```

### Node.js

```bash
# NPM
alias ni='npm install'
alias nid='npm install --save-dev'
alias nig='npm install -g'
alias nr='npm run'
alias ns='npm start'
alias nt='npm test'
alias nb='npm run build'
alias nrd='npm run dev'

# Yarn
alias yi='yarn install'
alias ya='yarn add'
alias yad='yarn add --dev'
alias yr='yarn run'
alias ys='yarn start'
alias yb='yarn build'
```

### Édition rapide

```bash
# Éditer fichiers de config
alias bashrc='nano ~/.bashrc'
alias aliases='nano ~/.bash_aliases'
alias vimrc='nano ~/.vimrc'
alias hosts='sudo nano /etc/hosts'

# Recharger config
alias reload='source ~/.bashrc'
alias refresh='source ~/.bash_aliases'
```

### Utilitaires

```bash
# Historique
alias h='history'
alias hg='history | grep'

# Effacer écran
alias c='clear'
alias cls='clear'

# Date et heure
alias now='date +"%T"'
alias nowdate='date +"%Y-%m-%d"'
alias timestamp='date +"%Y%m%d_%H%M%S"'

# Calculatrice
alias calc='bc -l'

# Afficher PATH
alias path='echo -e ${PATH//:/\\n}'

# Créer répertoire et y entrer
alias mkcd='function _mkcd(){ mkdir -p "$1" && cd "$1"; }; _mkcd'
```

## Fonctions bash (alias avec paramètres)

Les alias ne peuvent pas prendre de paramètres. Pour cela, utilisez des fonctions.

### Syntaxe de fonction

```bash
# Dans ~/.bash_aliases

# Fonction simple
function mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Ou syntaxe alternative
mkcd() {
    mkdir -p "$1" && cd "$1"
}
```

### Exemples de fonctions utiles

```bash
# Créer et entrer dans un dossier
mkcd() {
    mkdir -p "$1" && cd "$1"
}
# Usage: mkcd nouveau-dossier

# Extraire n'importe quelle archive
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"     ;;
            *.tar.gz)    tar xzf "$1"     ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.rar)       unrar x "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.tar)       tar xf "$1"      ;;
            *.tbz2)      tar xjf "$1"     ;;
            *.tgz)       tar xzf "$1"     ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *.7z)        7z x "$1"        ;;
            *)           echo "'$1' cannot be extracted" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}
# Usage: extract archive.tar.gz

# Créer backup d'un fichier
backup() {
    cp "$1" "$1.backup-$(date +%Y%m%d-%H%M%S)"
}
# Usage: backup fichier.txt

# Rechercher un fichier
ff() {
    find . -type f -name "*$1*"
}
# Usage: ff "nom_fichier"

# Rechercher dans les fichiers
ftext() {
    grep -rnw . -e "$1"
}
# Usage: ftext "texte à chercher"

# Créer un fichier et ses dossiers parents
touchp() {
    mkdir -p "$(dirname "$1")" && touch "$1"
}
# Usage: touchp path/to/file.txt

# Git commit et push rapide
gcap() {
    git add . && git commit -m "$1" && git push
}
# Usage: gcap "mon message de commit"

# Créer un nouveau projet Python
newpy() {
    mkdir -p "$1" && cd "$1"
    python3 -m venv venv
    source venv/bin/activate
    touch main.py requirements.txt README.md .gitignore
    echo "venv/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo "__pycache__/" >> .gitignore
}
# Usage: newpy mon-projet

# Créer un serveur HTTP avec un port spécifique
serve() {
    local port="${1:-8000}"
    python3 -m http.server "$port"
}
# Usage: serve 3000

# Info rapide sur un fichier
info() {
    if [ -f "$1" ]; then
        echo "Fichier: $1"
        echo "Taille: $(du -h "$1" | cut -f1)"
        echo "Type: $(file -b "$1")"
        echo "Modifié: $(date -r "$1")"
    elif [ -d "$1" ]; then
        echo "Dossier: $1"
        echo "Contenu: $(ls -A "$1" | wc -l) éléments"
        echo "Taille: $(du -sh "$1" | cut -f1)"
    else
        echo "'$1' n'existe pas"
    fi
}
# Usage: info fichier.txt

# Changer extension de fichiers
change-ext() {
    for file in *."$1"; do
        mv "$file" "${file%.$1}.$2"
    done
}
# Usage: change-ext txt md

# Note rapide
note() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $*" >> ~/notes.txt
}
# Usage: note "Ma note importante"

# Todo list simple
todo() {
    if [ $# -eq 0 ]; then
        cat ~/todo.txt 2>/dev/null || echo "Aucune tâche"
    else
        echo "- $*" >> ~/todo.txt
    fi
}
# Usage: todo "Faire quelque chose"

# Convertir video en gif
vid2gif() {
    ffmpeg -i "$1" -vf "fps=10,scale=720:-1:flags=lanczos" -c:v gif "$2"
}
# Usage: vid2gif input.mp4 output.gif
```

## Alias par environnement

### Développement Web

```bash
# Serveurs de développement
alias serve='python3 -m http.server'
alias phps='php -S localhost:8000'
alias nodemon='npx nodemon'

# Build
alias build='npm run build'
alias dev='npm run dev'
alias prod='npm run prod'

# Tests
alias test='npm test'
alias testw='npm test -- --watch'
```

### DevOps

```bash
# Kubernetes
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kl='kubectl logs'
alias kex='kubectl exec -it'
alias kdel='kubectl delete'

# Terraform
alias tf='terraform'
alias tfi='terraform init'
alias tfp='terraform plan'
alias tfa='terraform apply'
alias tfd='terraform destroy'

# Ansible
alias ap='ansible-playbook'
alias ai='ansible-inventory'
```

## Fichier ~/.bash_aliases complet exemple

```bash
# ~/.bash_aliases

# ============================================
# NAVIGATION
# ============================================
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias ~='cd ~'
alias back='cd -'

# ============================================
# LISTING
# ============================================
alias ls='ls --color=auto'
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias lt='ls -lath'
alias lsize='ls -laSh'

# ============================================
# GREP
# ============================================
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

# ============================================
# SÉCURITÉ
# ============================================
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias ln='ln -i'

# ============================================
# GIT
# ============================================
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gcm='git commit -m'
alias gp='git push'
alias gpl='git pull'
alias gco='git checkout'
alias gb='git branch'
alias glog='git log --oneline --graph --decorate'

# ============================================
# DOCKER
# ============================================
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'

# ============================================
# SYSTÈME
# ============================================
alias update='sudo apt update'
alias upgrade='sudo apt upgrade'
alias install='sudo apt install'
alias df='df -h'
alias du='du -h'
alias free='free -h'

# ============================================
# PYTHON
# ============================================
alias py='python3'
alias pip='pip3'
alias venv='python3 -m venv venv'
alias activate='source venv/bin/activate'

# ============================================
# ÉDITION
# ============================================
alias bashrc='nano ~/.bashrc'
alias aliases='nano ~/.bash_aliases'
alias reload='source ~/.bashrc'

# ============================================
# UTILITAIRES
# ============================================
alias c='clear'
alias h='history'
alias now='date +"%T"'
alias path='echo -e ${PATH//:/\\n}'

# ============================================
# FONCTIONS
# ============================================

# Créer et entrer dans un dossier
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extraire archives
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"     ;;
            *.tar.gz)    tar xzf "$1"     ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.rar)       unrar x "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.tar)       tar xf "$1"      ;;
            *.tbz2)      tar xjf "$1"     ;;
            *.tgz)       tar xzf "$1"     ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *.7z)        7z x "$1"        ;;
            *)           echo "'$1' cannot be extracted" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Backup rapide
backup() {
    cp "$1" "$1.backup-$(date +%Y%m%d-%H%M%S)"
}

# Rechercher fichiers
ff() {
    find . -type f -name "*$1*"
}

# Git commit et push
gcap() {
    git add . && git commit -m "$1" && git push
}
```

## Lister et gérer les alias

```bash
# Afficher tous les alias
alias

# Afficher un alias spécifique
alias ll

# Supprimer un alias (temporaire)
unalias ll

# Supprimer tous les alias (temporaire)
unalias -a

# Vérifier si une commande est un alias
type ll

# Exécuter commande originale (ignorer alias)
\ls    # au lieu de ls
/bin/ls  # chemin complet
```

## Bonnes pratiques

```bash
# ✅ Noms courts et mémorables
alias gp='git push'

# ✅ Utiliser des préfixes cohérents
alias g='git'
alias gs='git status'
alias gc='git commit'

# ✅ Commenter vos alias
# Git shortcuts
alias gp='git push'  # Push to remote

# ✅ Grouper par catégorie
# === NAVIGATION ===
alias ..='cd ..'

# === GIT ===
alias gs='git status'

# ✅ Sauvegarder avant modification
cp ~/.bash_aliases ~/.bash_aliases.backup

# ❌ Éviter de remplacer des commandes système critiques
# alias cd='echo "CD is disabled"'  # Mauvaise idée !

# ❌ Alias trop longs (utilisez des fonctions)
# alias longalias='command1 && command2 && command3 && ...'  # Trop long

# ✅ Utilisez des fonctions pour des commandes complexes
myfunction() {
    command1
    command2
    command3
}
```

## Déboguer les alias

```bash
# Voir tous les alias chargés
alias | grep git

# Tracer l'exécution
bash -x -c 'll'

# Vérifier le fichier source
grep -n "alias ll" ~/.bash_aliases

# Tester sans recharger
source <(echo "alias test='echo test'")
test
```

## Exemples avancés

### Alias conditionnels

```bash
# Utiliser différents alias selon l'OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    alias open='xdg-open'
elif [[ "$OSTYPE" == "darwin"* ]]; then
    alias ls='ls -G'
fi
```

### Alias avec couleurs

```bash
# Définir couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Alias avec couleur
alias error='echo -e "${RED}Erreur!${NC}"'
alias success='echo -e "${GREEN}Succès!${NC}"'
```

### Alias avec completion

```bash
# Activer completion pour alias
complete -F _git g
complete -F _git gs
complete -F _git gc
```

## Ressources

- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Awesome Bash](https://github.com/awesome-lists/awesome-bash)
- [Oh My Bash](https://ohmybash.nntoan.com/)
- [Bash-it](https://github.com/Bash-it/bash-it)

## Template ~/.bash_aliases

```bash
#!/bin/bash
# ~/.bash_aliases
#
# Fichier d'alias personnalisés
# Rechargé automatiquement par ~/.bashrc

# ============================================
# NAVIGATION
# ============================================
alias ..='cd ..'
alias ...='cd ../..'

# ============================================
# LISTING
# ============================================
alias ll='ls -lah'
alias la='ls -A'

# ============================================
# GIT
# ============================================
alias gs='git status'
alias gp='git push'

# ============================================
# DOCKER
# ============================================
alias d='docker'
alias dc='docker-compose'

# ============================================
# SYSTÈME
# ============================================
alias update='sudo apt update && sudo apt upgrade -y'

# ============================================
# DÉVELOPPEMENT
# ============================================
alias py='python3'
alias pip='pip3'

# ============================================
# UTILITAIRES
# ============================================
alias c='clear'
alias reload='source ~/.bashrc'

# ============================================
# FONCTIONS PERSONNALISÉES
# ============================================

# Ajouter vos fonctions ici
```

# ⚙️ Gestion des Processus Linux

[← Réseau](./infos-terminal-04-linux-reseau.md) | [Index](./infos-terminal-00-index.md) | [Windows CMD →](./infos-terminal-06-windows-cmd.md)

## Voir les processus

### ps - Process Status

```bash
# Processus utilisateur
ps

# Tous les processus (format BSD)
ps aux

# Tous les processus (format System V)
ps -ef

# Format personnalisé
ps -eo pid,user,cmd,%mem,%cpu

# Processus en arbre
ps auxf
ps -ejH

# Processus spécifique
ps aux | grep nginx
pgrep nginx

# Par utilisateur
ps -u username
```

### top

Moniteur interactif.

```bash
# Lancer top
top

# Raccourcis dans top:
# h ou ? : aide
# q : quitter
# k : tuer processus (demande PID)
# r : renice (changer priorité)
# M : trier par mémoire
# P : trier par CPU
# T : trier par temps
# c : commande complète
# 1 : afficher tous les CPUs
# u : filtrer par utilisateur
# f : sélectionner champs
# W : sauvegarder configuration

# Options au lancement
top -u username  # Filtrer utilisateur
top -d 2        # Délai 2 secondes
top -n 10       # 10 itérations puis quitter
top -b          # Mode batch (pour logs)
```

### htop

Top amélioré.

```bash
# Installer
sudo apt install htop

# Lancer
htop

# Avantages:
# - Interface couleurs
# - Navigation souris
# - F keys pour actions
# - Arbre des processus
# - Recherche intégrée

# Raccourcis:
# F3 : rechercher
# F4 : filtrer
# F5 : arbre
# F6 : trier
# F9 : tuer
# F10 : quitter
```

### pstree

Arbre des processus.

```bash
# Arbre complet
pstree

# Avec PIDs
pstree -p

# Avec utilisateurs
pstree -u

# Processus spécifique
pstree -p PID

# Compact
pstree -c
```

### pgrep

Trouver PID par nom.

```bash
# Trouver processus
pgrep nginx

# Avec nom complet
pgrep -f "python script.py"

# Par utilisateur
pgrep -u username

# Afficher commande
pgrep -a nginx

# Dernier processus correspondant
pgrep -n nginx

# Premier processus
pgrep -o nginx
```

## Gérer les processus

### kill

Envoyer signal à processus.

```bash
# SIGTERM (15) - Terminaison propre
kill PID
kill 1234

# SIGKILL (9) - Force kill
kill -9 PID
kill -KILL PID

# SIGHUP (1) - Reload config
kill -HUP PID
kill -1 PID

# SIGINT (2) - Interrupt
kill -INT PID

# Liste des signaux
kill -l

# Signaux courants:
# 1  HUP    : Hang up, reload config
# 2  INT    : Interrupt (Ctrl+C)
# 3  QUIT   : Quit
# 9  KILL   : Force kill (non attrapable)
# 15 TERM   : Terminaison propre (défaut)
# 18 CONT   : Continuer
# 19 STOP   : Arrêter (non attrapable)
# 20 TSTP   : Arrêter (Ctrl+Z)

# Tuer par nom
kill $(pgrep nginx)
```

### killall

Tuer par nom.

```bash
# Tuer tous les processus nginx
killall nginx

# Force kill
killall -9 nginx

# Par utilisateur
killall -u username

# Interactif (confirmation)
killall -i nginx

# Verbose
killall -v nginx

# Attendre que processus se termine
killall -w nginx
```

### pkill

kill + pgrep.

```bash
# Tuer par nom
pkill nginx

# Force kill
pkill -9 nginx

# Par utilisateur
pkill -u username

# Pattern complet
pkill -f "python script.py"

# Signal spécifique
pkill -HUP nginx

# Exclude pattern
pkill -x "nginx: worker"
```

## Priorité des processus

### nice

Lancer avec priorité.

```bash
# Priorité par défaut (10)
nice command

# Priorité basse (19)
nice -n 19 command

# Priorité haute (-20, root uniquement)
sudo nice -n -20 command

# Vérifier priorité
ps -eo pid,ni,cmd | grep command

# Échelle: -20 (haute priorité) à 19 (basse priorité)
# Défaut: 0
```

### renice

Changer priorité processus existant.

```bash
# Changer priorité par PID
renice -n 10 -p 1234

# Par utilisateur
renice -n 5 -u username

# Par groupe
renice -n 5 -g groupname

# Exemple: baisser priorité processus gourmand
renice -n 19 -p $(pgrep chrome)
```

## Jobs (contrôle de processus)

### Gestion jobs

```bash
# Lancer en arrière-plan
command &

# Lister jobs
jobs

# Job en avant-plan
fg
fg %1

# Job en arrière-plan
bg
bg %1

# Suspendre job (Ctrl+Z)
# En avant-plan, appuyer Ctrl+Z

# Détacher job du terminal
disown
disown %1

# Exemple workflow:
./long_script.sh
# Ctrl+Z pour suspendre
bg           # Continue en arrière-plan
disown       # Détache du terminal

# Tuer job
kill %1
```

### nohup

Lancer commande immune à hangup.

```bash
# Basique (sortie dans nohup.out)
nohup command &

# Avec redirection
nohup command > output.log 2>&1 &

# Sans sortie
nohup command > /dev/null 2>&1 &

# Vérifier processus
ps aux | grep command
```

### screen

Terminal virtuel persistant.

```bash
# Installer
sudo apt install screen

# Créer session
screen

# Nommer session
screen -S mysession

# Détacher session (Ctrl+A, D)

# Lister sessions
screen -ls

# Réattacher
screen -r
screen -r mysession

# Tuer session
screen -X -S mysession quit

# Commandes dans screen:
# Ctrl+A, D : détacher
# Ctrl+A, C : nouvelle fenêtre
# Ctrl+A, N : fenêtre suivante
# Ctrl+A, P : fenêtre précédente
# Ctrl+A, " : lister fenêtres
# Ctrl+A, K : tuer fenêtre
```

### tmux

Alternative à screen.

```bash
# Installer
sudo apt install tmux

# Créer session
tmux

# Nommer session
tmux new -s mysession

# Détacher (Ctrl+B, D)

# Lister sessions
tmux ls

# Réattacher
tmux attach
tmux attach -t mysession

# Tuer session
tmux kill-session -t mysession

# Commandes dans tmux:
# Ctrl+B, D : détacher
# Ctrl+B, C : nouvelle fenêtre
# Ctrl+B, N : fenêtre suivante
# Ctrl+B, P : fenêtre précédente
# Ctrl+B, W : lister fenêtres
# Ctrl+B, & : tuer fenêtre
# Ctrl+B, % : split vertical
# Ctrl+B, " : split horizontal
# Ctrl+B, flèches : naviguer splits
```

## Informations processus

### /proc/PID

Informations détaillées.

```bash
# Info processus
ls -l /proc/PID/

# Commande lancée
cat /proc/PID/cmdline

# Variables environnement
cat /proc/PID/environ

# Répertoire courant
ls -l /proc/PID/cwd

# Binaire exécuté
ls -l /proc/PID/exe

# Fichiers ouverts
ls -l /proc/PID/fd/

# Statut
cat /proc/PID/status

# Limites
cat /proc/PID/limits

# Utilisation mémoire
cat /proc/PID/smaps
cat /proc/PID/statm
```

### lsof

Fichiers ouverts par processus.

```bash
# Fichiers ouverts par PID
lsof -p PID

# Processus utilisant fichier
lsof /path/to/file

# Processus utilisant dossier
lsof +D /path/to/dir

# Par utilisateur
lsof -u username

# Par commande
lsof -c nginx

# Ports réseau
sudo lsof -i
sudo lsof -i :80
sudo lsof -i TCP:22

# Tout sauf utilisateur
lsof -u ^username
```

### strace

Tracer appels système.

```bash
# Tracer processus
strace command

# Tracer PID existant
strace -p PID

# Sauvegarder trace
strace -o trace.log command

# Statistiques
strace -c command

# Filtrer appels
strace -e open command
strace -e network command

# Suivre forks
strace -f command

# Timestamp
strace -t command
strace -tt command  # microsecondes
```

### ltrace

Tracer appels bibliothèque.

```bash
# Tracer appels
ltrace command

# Tracer PID
ltrace -p PID

# Sauvegarder
ltrace -o trace.log command

# Compteur
ltrace -c command

# Avec timestamp
ltrace -t command
```

## Monitoring avancé

### vmstat

Statistiques mémoire virtuelle.

```bash
# Une fois
vmstat

# Rafraîchir toutes les 2 secondes
vmstat 2

# 10 fois toutes les 2 secondes
vmstat 2 10

# Mémoire en MB
vmstat -S M 2

# Colonnes:
# r  : processus en attente CPU
# b  : processus bloqués
# swpd : swap utilisée
# free : mémoire libre
# buff : buffers
# cache: cache
# si : swap in
# so : swap out
# bi : blocks in (disque)
# bo : blocks out
# in : interrupts
# cs : context switches
# us : user CPU
# sy : system CPU
# id : idle CPU
# wa : wait IO
```

### iostat

Statistiques I/O.

```bash
# Installer
sudo apt install sysstat

# Basique
iostat

# Détaillé
iostat -x

# Rafraîchir
iostat 2

# Device spécifique
iostat -x sda 2

# En MB
iostat -m 2
```

### iotop

Top pour I/O.

```bash
# Installer
sudo apt install iotop

# Lancer
sudo iotop

# Processus actifs uniquement
sudo iotop -o

# Mode batch
sudo iotop -b

# Raccourcis:
# o : actifs seulement
# p : processus vs threads
# a : I/O accumulé
# q : quitter
```

### dstat

Statistiques système combinées.

```bash
# Installer
sudo apt install dstat

# Basique
dstat

# Tout
dstat -a

# CPU et disque
dstat -cd

# Réseau
dstat -n

# Top processus CPU
dstat --top-cpu

# Top processus mémoire
dstat --top-mem

# Top I/O
dstat --top-io
```

### pidstat

Statistiques par processus.

```bash
# CPU par processus
pidstat

# Rafraîchir toutes les 2 secondes
pidstat 2

# I/O
pidstat -d

# Mémoire
pidstat -r

# Threads
pidstat -t

# Processus spécifique
pidstat -p PID
```

## Limites processus

### ulimit

Limites utilisateur.

```bash
# Afficher toutes les limites
ulimit -a

# Fichiers ouverts
ulimit -n

# Augmenter limite fichiers (temporaire)
ulimit -n 4096

# Taille core dumps
ulimit -c
ulimit -c unlimited  # illimité

# Nombre processus
ulimit -u

# Taille mémoire virtuelle
ulimit -v

# Stack size
ulimit -s

# Permanent dans /etc/security/limits.conf
sudo nano /etc/security/limits.conf
# username soft nofile 4096
# username hard nofile 8192
# * soft nproc 1024
```

### cgroups

Control groups (limitation ressources).

```bash
# Lister cgroups
ls /sys/fs/cgroup/

# Créer cgroup (systemd)
sudo systemd-run --unit=myapp --scope -p MemoryMax=512M -p CPUQuota=50% command

# Voir statistiques
systemd-cgtop

# Limites processus
cat /sys/fs/cgroup/system.slice/UNIT/memory.max
cat /sys/fs/cgroup/system.slice/UNIT/cpu.max
```

## Débogage

### core dumps

Crash dumps.

```bash
# Activer core dumps
ulimit -c unlimited

# Emplacement
cat /proc/sys/kernel/core_pattern

# Configurer emplacement
echo "core.%e.%p" | sudo tee /proc/sys/kernel/core_pattern

# Analyser avec gdb
gdb program core.file
```

### gdb

Débogueur.

```bash
# Installer
sudo apt install gdb

# Déboguer programme
gdb ./program

# Attacher à processus
gdb -p PID

# Commandes gdb:
# run : lancer
# break : breakpoint
# continue : continuer
# step : step into
# next : step over
# print var : afficher variable
# backtrace : stack trace
# quit : quitter
```

## Bonnes pratiques

```bash
# ✅ Surveiller processus gourmands
top -o %CPU
top -o %MEM

# ✅ Tuer processus proprement
kill PID      # SIGTERM d'abord
sleep 5
kill -9 PID   # SIGKILL si nécessaire

# ✅ Utiliser nice pour tâches longues
nice -n 19 ./long_task.sh

# ✅ Utiliser nohup/screen/tmux pour jobs longs
nohup ./script.sh > output.log 2>&1 &

# ✅ Monitorer ressources régulièrement
htop
vmstat 2
iostat -x 2

# ❌ Ne jamais kill -9 systemd (PID 1)
# ❌ Attention avec killall
# ❌ Vérifier avant kill que c'est le bon processus
```

[← Réseau](./infos-terminal-04-linux-reseau.md) | [Index](./infos-terminal-00-index.md) | [Windows CMD →](./infos-terminal-06-windows-cmd.md)

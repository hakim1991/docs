# 📁 Système de Fichiers Linux

[← Linux Avancées](./infos-terminal-02-linux-avancees.md) | [Index](./infos-terminal-00-index.md) | [Réseau →](./infos-terminal-04-linux-reseau.md)

## Structure des répertoires

### Arborescence FHS (Filesystem Hierarchy Standard)

```
/                    # Racine
├── bin/            # Binaires essentiels (ls, cat, etc.)
├── boot/           # Fichiers de démarrage (kernel, grub)
├── dev/            # Fichiers devices (disques, périphériques)
├── etc/            # Fichiers de configuration
├── home/           # Répertoires utilisateurs
├── lib/            # Bibliothèques partagées
├── media/          # Points de montage amovibles (USB, CD)
├── mnt/            # Points de montage temporaires
├── opt/            # Applications optionnelles
├── proc/           # Informations processus (virtuel)
├── root/           # Home du root
├── run/            # Données runtime
├── sbin/           # Binaires système (root)
├── srv/            # Données services (web, ftp)
├── sys/            # Informations système (virtuel)
├── tmp/            # Fichiers temporaires
├── usr/            # Applications utilisateur
│   ├── bin/       # Binaires utilisateur
│   ├── lib/       # Bibliothèques
│   ├── local/     # Applications locales
│   └── share/     # Données partagées
└── var/            # Données variables
    ├── log/       # Logs système
    ├── www/       # Sites web
    └── tmp/       # Temporaire persistant
```

### Répertoires importants

```bash
# Configuration système
/etc/

# Logs
/var/log/

# Home utilisateurs
/home/username/

# Programmes installés
/usr/local/bin/
/opt/

# Devices
/dev/
```

## Fichiers de configuration système

### /etc/passwd

Informations utilisateurs.

```bash
# Format:
# username:password:UID:GID:comment:home:shell

cat /etc/passwd
# root:x:0:0:root:/root:/bin/bash
# user:x:1000:1000:User Name:/home/user:/bin/bash

# Afficher utilisateurs avec UID > 1000
awk -F: '$3 >= 1000 {print $1}' /etc/passwd
```

### /etc/group

Groupes système.

```bash
# Format:
# groupname:password:GID:users

cat /etc/group
# sudo:x:27:user1,user2
# docker:x:999:user1

# Afficher groupes d'un utilisateur
groups username
```

### /etc/shadow

Mots de passe chiffrés (root only).

```bash
sudo cat /etc/shadow
# username:$6$encrypted$hash:18000:0:99999:7:::
```

### /etc/hosts

Résolution DNS locale.

```bash
cat /etc/hosts
# 127.0.0.1       localhost
# 192.168.1.100   server.local

# Éditer
sudo nano /etc/hosts
```

### /etc/fstab

Points de montage automatiques.

```bash
cat /etc/fstab
# UUID=xxx  /  ext4  defaults  0  1

# Format:
# device  mountpoint  type  options  dump  pass
```

### /etc/crontab

Cron système.

```bash
cat /etc/crontab

# Crons utilisateur vs système:
crontab -e           # Utilisateur
sudo nano /etc/crontab  # Système
```

### /etc/resolv.conf

Configuration DNS.

```bash
cat /etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 1.1.1.1
```

### /etc/environment

Variables d'environnement globales.

```bash
cat /etc/environment
# PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Éditer
sudo nano /etc/environment
```

### /etc/profile

Configuration shell globale.

```bash
# Fichiers de configuration shell:
/etc/profile         # Global, tous les users
~/.bashrc           # User, shells interactifs
~/.bash_profile     # User, shells de login
~/.profile          # User, shells de login
```

## Fichiers de logs

### /var/log/

```bash
# Logs système
/var/log/syslog      # Logs système généraux (Debian/Ubuntu)
/var/log/messages    # Logs système (RedHat/CentOS)

# Logs d'authentification
/var/log/auth.log    # Debian/Ubuntu
/var/log/secure      # RedHat/CentOS

# Logs kernel
/var/log/kern.log
/var/log/dmesg

# Logs boot
/var/log/boot.log

# Logs applications
/var/log/apache2/    # Apache
/var/log/nginx/      # Nginx
/var/log/mysql/      # MySQL
```

### Consulter logs

```bash
# Dernières lignes
tail -f /var/log/syslog

# Rechercher erreurs
grep -i error /var/log/syslog

# Logs avec journalctl (systemd)
journalctl
journalctl -u nginx.service
journalctl -f

# Logs boot
journalctl -b

# Logs depuis date
journalctl --since "2025-01-01"
journalctl --since "1 hour ago"

# Logs avec priorité
journalctl -p err
```

## Permissions et ownership

### Comprendre les permissions

```bash
ls -l
# -rw-r--r-- 1 user group 1234 Jan 10 10:00 file.txt
# │││││││││
# │││││││└┴─ autres (r--)
# ││││││└─┴── groupe (r--)
# │││└─┴───── propriétaire (rw-)
# ││└──────── liens
# │└───────── type (- = fichier, d = dossier, l = lien)

# Types:
# - : fichier
# d : directory
# l : symbolic link
# b : block device
# c : character device
# p : pipe
# s : socket

# Permissions:
# r (4) : read
# w (2) : write
# x (1) : execute
```

### Bits spéciaux

```bash
# SUID (Set User ID)
chmod u+s fichier
chmod 4755 fichier
# Exécute avec permissions du propriétaire

# SGID (Set Group ID)
chmod g+s dossier
chmod 2755 dossier
# Nouveaux fichiers héritent du groupe

# Sticky bit
chmod +t dossier
chmod 1777 dossier
# Seul propriétaire peut supprimer ses fichiers
# Utilisé sur /tmp

# Exemples
ls -l /usr/bin/passwd
# -rwsr-xr-x (SUID)

ls -ld /tmp
# drwxrwxrwt (Sticky bit)
```

### umask

Masque de permissions par défaut.

```bash
# Afficher umask
umask
# 0022

# Définir umask
umask 022

# Calcul permissions:
# Fichiers: 666 - umask
# Dossiers: 777 - umask

# umask 022:
# Fichiers: 644 (rw-r--r--)
# Dossiers: 755 (rwxr-xr-x)

# Permanent dans ~/.bashrc
echo "umask 022" >> ~/.bashrc
```

### ACL (Access Control Lists)

Permissions étendues.

```bash
# Afficher ACL
getfacl fichier.txt

# Définir ACL
setfacl -m u:username:rwx fichier.txt

# Définir ACL groupe
setfacl -m g:groupname:rx fichier.txt

# Supprimer ACL
setfacl -x u:username fichier.txt

# Supprimer toutes les ACL
setfacl -b fichier.txt

# ACL récursive
setfacl -R -m u:username:rx dossier/

# ACL par défaut (nouveaux fichiers)
setfacl -d -m u:username:rwx dossier/
```

## Attributs de fichiers

### chattr / lsattr

Attributs étendus.

```bash
# Afficher attributs
lsattr fichier.txt

# Rendre immuable (non modifiable, même par root)
sudo chattr +i fichier.txt

# Retirer immuable
sudo chattr -i fichier.txt

# Append only
sudo chattr +a fichier.log

# Attributs courants:
# i : immutable
# a : append only
# d : no dump
# A : no atime update
```

### Extended Attributes

```bash
# Définir attribut
setfattr -n user.description -v "My file" file.txt

# Lire attribut
getfattr -d file.txt

# Supprimer attribut
setfattr -x user.description file.txt
```

## Liens symboliques et hard links

### Liens symboliques (symlinks)

```bash
# Créer symlink
ln -s /path/to/original symlink_name

# Symlink vers dossier
ln -s /var/www/html/ ~/web

# Force créer (écraser existant)
ln -sf /path/to/original symlink_name

# Lister symlinks
ls -l | grep "^l"

# Trouver destination
readlink symlink_name
realpath symlink_name

# Supprimer symlink
rm symlink_name
unlink symlink_name

# Symlink cassé (broken)
find . -type l ! -exec test -e {} \; -print
```

### Hard links

```bash
# Créer hard link
ln /path/to/original hardlink_name

# Même inode
ls -li original hardlink
# 123456 original
# 123456 hardlink

# Nombre de hard links
ls -l fichier.txt
# -rw-r--r-- 2 user group ...
#            ^ nombre de liens

# Trouver tous les hard links
find . -samefile original

# Différences symlink vs hard link:
# Symlink: peut pointer vers autre partition, peut être cassé
# Hard link: même partition, toujours valide si fichier existe
```

## Quotas disque

### Configuration quotas

```bash
# Installer
sudo apt install quota

# Activer dans /etc/fstab
/dev/sda1  /home  ext4  defaults,usrquota,grpquota  0  2

# Créer fichiers quota
sudo quotacheck -cum /home

# Activer quotas
sudo quotaon -v /home

# Éditer quota utilisateur
sudo edquota -u username

# Éditer quota groupe
sudo edquota -g groupname

# Afficher quotas
quota -u username
repquota -a

# Grace period
sudo edquota -t
```

## Inodes

### Comprendre les inodes

```bash
# Afficher inodes
ls -i
# 123456 fichier.txt

# Info inode
stat fichier.txt

# Nombre d'inodes disponibles
df -i

# Trouver fichiers avec inode
find . -inum 123456

# Problème: inodes pleins mais espace disponible
# Solution: supprimer petits fichiers nombreux
```

## /proc et /sys

### /proc - Informations processus

```bash
# Info CPU
cat /proc/cpuinfo

# Info mémoire
cat /proc/meminfo

# Uptime
cat /proc/uptime

# Version kernel
cat /proc/version

# Montages
cat /proc/mounts

# Info processus
cat /proc/PID/cmdline
cat /proc/PID/environ
cat /proc/PID/status

# Limites système
cat /proc/sys/fs/file-max
cat /proc/sys/kernel/pid_max
```

### /sys - Informations matériel

```bash
# Info système
ls /sys/class/
ls /sys/devices/

# Info réseau
cat /sys/class/net/eth0/address

# Info disques
ls /sys/block/

# Info puissance
cat /sys/class/power_supply/BAT0/capacity
```

## Devices (/dev)

```bash
# Devices blocs (disques)
ls -l /dev/sd*
/dev/sda   # Premier disque
/dev/sda1  # Première partition
/dev/sdb   # Deuxième disque

# Null device
/dev/null    # Supprime sortie
/dev/zero    # Source de zéros

# Random
/dev/random   # Nombres aléatoires
/dev/urandom  # Nombres pseudo-aléatoires

# Terminaux
/dev/tty     # Terminal actuel
/dev/pts/0   # Pseudo-terminal

# Exemples
# Rediriger vers null
command > /dev/null 2>&1

# Créer fichier vide de 1GB
dd if=/dev/zero of=file.img bs=1M count=1024
```

## Swap

```bash
# Afficher swap
swapon --show
free -h

# Créer fichier swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Permanent dans /etc/fstab
/swapfile none swap sw 0 0

# Désactiver swap
sudo swapoff /swapfile

# Swappiness (0-100)
cat /proc/sys/vm/swappiness
sudo sysctl vm.swappiness=10

# Permanent
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
```

## Bonnes pratiques

```bash
# ✅ Vérifier espace disque régulièrement
df -h

# ✅ Nettoyer logs anciens
sudo journalctl --vacuum-time=7d

# ✅ Nettoyer cache apt
sudo apt clean
sudo apt autoclean

# ✅ Trouver gros fichiers
du -ah /home | sort -rh | head -20
find / -type f -size +100M

# ✅ Permissions sécurisées
chmod 600 ~/.ssh/id_rsa
chmod 700 ~/.ssh

# ✅ Backup avant modification
cp /etc/important.conf /etc/important.conf.bak

# ❌ Ne jamais rm -rf /
# ❌ Attention avec sudo
# ❌ Vérifier permissions avant chmod -R
```

[← Linux Avancées](./infos-terminal-02-linux-avancees.md) | [Index](./infos-terminal-00-index.md) | [Réseau →](./infos-terminal-04-linux-reseau.md)

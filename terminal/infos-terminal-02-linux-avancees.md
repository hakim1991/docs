# 🚀 Commandes Linux Avancées

[← Linux Base](./infos-terminal-01-linux-base.md) | [Index](./infos-terminal-00-index.md) | [Filesystem →](./infos-terminal-03-linux-filesystem.md)

## Archives et compression

### tar

Créer et extraire archives.

```bash
# Créer archive .tar
tar -cvf archive.tar dossier/
# c = create, v = verbose, f = file

# Créer archive .tar.gz (compressée)
tar -czvf archive.tar.gz dossier/
# z = gzip

# Créer archive .tar.bz2 (meilleure compression)
tar -cjvf archive.tar.bz2 dossier/
# j = bzip2

# Extraire .tar
tar -xvf archive.tar
# x = extract

# Extraire .tar.gz
tar -xzvf archive.tar.gz

# Extraire .tar.bz2
tar -xjvf archive.tar.bz2

# Lister contenu
tar -tvf archive.tar

# Extraire dans dossier spécifique
tar -xzvf archive.tar.gz -C /destination/

# Extraire fichier spécifique
tar -xzvf archive.tar.gz fichier.txt

# Exclure fichiers
tar -czvf archive.tar.gz --exclude="*.log" dossier/
```

### gzip / gunzip

Compression/décompression.

```bash
# Compresser
gzip fichier.txt
# Crée fichier.txt.gz et supprime original

# Garder original
gzip -k fichier.txt

# Décompresser
gunzip fichier.txt.gz
# ou
gzip -d fichier.txt.gz

# Compresser multiple
gzip *.txt

# Force compression
gzip -f fichier.txt
```

### zip / unzip

Archives ZIP.

```bash
# Créer archive ZIP
zip archive.zip fichier1.txt fichier2.txt

# Zipper dossier récursivement
zip -r archive.zip dossier/

# Extraire
unzip archive.zip

# Lister contenu
unzip -l archive.zip

# Extraire dans dossier
unzip archive.zip -d /destination/

# Extraire fichier spécifique
unzip archive.zip fichier.txt
```

## Téléchargement

### wget

Télécharger fichiers.

```bash
# Télécharger fichier
wget https://example.com/file.zip

# Avec nom personnalisé
wget -O fichier.zip https://example.com/file.zip

# Continuer téléchargement interrompu
wget -c https://example.com/file.zip

# Télécharger en arrière-plan
wget -b https://example.com/file.zip

# Limiter bande passante (Ko/s)
wget --limit-rate=200k https://example.com/file.zip

# Télécharger récursivement (site web)
wget -r https://example.com

# Avec authentification
wget --user=username --password=pass https://example.com/file.zip
```

### curl

Transférer données avec URLs.

```bash
# Télécharger fichier
curl -O https://example.com/file.zip

# Avec nom personnalisé
curl -o fichier.zip https://example.com/file.zip

# Suivre redirections
curl -L https://example.com

# Afficher headers
curl -I https://example.com

# POST request
curl -X POST -d "data=value" https://api.example.com

# JSON POST
curl -X POST -H "Content-Type: application/json" \
  -d '{"key":"value"}' https://api.example.com

# Avec authentification
curl -u username:password https://example.com

# Télécharger avec progression
curl -# -O https://example.com/file.zip

# Sauvegarder cookies
curl -c cookies.txt https://example.com

# Utiliser cookies
curl -b cookies.txt https://example.com
```

## Traitement de texte

### sed - Stream Editor

Éditer texte en stream.

```bash
# Remplacer première occurrence
sed 's/old/new/' fichier.txt

# Remplacer toutes les occurrences
sed 's/old/new/g' fichier.txt

# Éditer fichier en place
sed -i 's/old/new/g' fichier.txt

# Avec backup
sed -i.bak 's/old/new/g' fichier.txt

# Supprimer lignes vides
sed '/^$/d' fichier.txt

# Supprimer ligne spécifique
sed '5d' fichier.txt

# Supprimer lignes 5 à 10
sed '5,10d' fichier.txt

# Afficher lignes 5 à 10
sed -n '5,10p' fichier.txt

# Remplacer sur lignes contenant pattern
sed '/pattern/s/old/new/g' fichier.txt
```

### awk

Traitement et analyse de texte.

```bash
# Afficher colonne spécifique
awk '{print $1}' fichier.txt

# Afficher colonnes 1 et 3
awk '{print $1, $3}' fichier.txt

# Avec séparateur personnalisé
awk -F: '{print $1}' /etc/passwd

# Condition
awk '$3 > 100 {print $1}' fichier.txt

# Somme d'une colonne
awk '{sum += $1} END {print sum}' fichier.txt

# Nombre de lignes
awk 'END {print NR}' fichier.txt

# Afficher avec format
awk '{printf "%-10s %s\n", $1, $2}' fichier.txt
```

### cut

Couper colonnes.

```bash
# Colonne 1 (séparateur espace)
cut -d' ' -f1 fichier.txt

# Colonnes 1 et 3
cut -d' ' -f1,3 fichier.txt

# Colonnes 1 à 3
cut -d' ' -f1-3 fichier.txt

# Caractères 1 à 10
cut -c1-10 fichier.txt

# Avec séparateur :
cut -d: -f1 /etc/passwd
```

### sort

Trier lignes.

```bash
# Tri alphabétique
sort fichier.txt

# Tri inverse
sort -r fichier.txt

# Tri numérique
sort -n fichier.txt

# Tri par colonne spécifique
sort -k2 fichier.txt

# Supprimer doublons
sort -u fichier.txt

# Tri sur fichier volumineux
sort -T /tmp fichier.txt
```

### uniq

Filtrer lignes dupliquées.

```bash
# Supprimer doublons consécutifs
uniq fichier.txt

# Compter occurrences
uniq -c fichier.txt

# Afficher uniquement doublons
uniq -d fichier.txt

# Afficher uniquement lignes uniques
uniq -u fichier.txt

# Ignorer N premiers caractères
uniq -s 5 fichier.txt
```

### wc - Word Count

Compter lignes/mots/caractères.

```bash
# Compter lignes
wc -l fichier.txt

# Compter mots
wc -w fichier.txt

# Compter caractères
wc -c fichier.txt

# Tout en un
wc fichier.txt
# lignes mots caractères
```

### tr - Translate

Remplacer ou supprimer caractères.

```bash
# Minuscules vers majuscules
tr 'a-z' 'A-Z' < fichier.txt

# Supprimer caractère
tr -d ',' < fichier.txt

# Remplacer espaces par underscores
tr ' ' '_' < fichier.txt

# Supprimer répétitions
tr -s ' ' < fichier.txt

# Supprimer tout sauf
tr -cd '[:alnum:]' < fichier.txt
```

## Monitoring et performance

### top

Moniteur de processus interactif.

```bash
# Lancer top
top

# Raccourcis dans top:
# h : aide
# q : quitter
# k : tuer processus
# r : renice
# M : trier par mémoire
# P : trier par CPU
# 1 : afficher tous les CPUs
# c : commande complète
```

### htop

Top amélioré (à installer).

```bash
# Installer
sudo apt install htop

# Lancer
htop

# Plus visuel et interactif que top
```

### ps - Process Status

Lister processus.

```bash
# Tous les processus
ps aux

# Processus utilisateur
ps -u username

# Processus en arbre
ps auxf
pstree

# Processus spécifique
ps aux | grep firefox

# Format personnalisé
ps -eo pid,user,cmd,%mem,%cpu

# Trier par mémoire
ps aux --sort=-%mem | head

# Trier par CPU
ps aux --sort=-%cpu | head
```

### kill

Terminer processus.

```bash
# Tuer par PID
kill 1234

# Force kill
kill -9 1234
kill -KILL 1234

# Tuer par nom
killall firefox

# Tuer processus utilisateur
killall -u username

# Liste des signaux
kill -l

# Signaux courants:
# SIGTERM (15) : Terminaison propre (défaut)
# SIGKILL (9)  : Force kill
# SIGHUP (1)   : Hang up
# SIGINT (2)   : Interrupt (Ctrl+C)
```

### nice / renice

Priorité des processus.

```bash
# Lancer avec priorité basse
nice -n 19 command

# Lancer avec priorité haute (root)
sudo nice -n -20 command

# Changer priorité processus existant
renice -n 10 -p 1234

# Priorité: -20 (haute) à 19 (basse)
```

### time

Mesurer temps d'exécution.

```bash
# Temps d'exécution
time command

# Temps détaillé
time -v command

# Format personnalisé
/usr/bin/time -f "Temps: %E Mémoire: %M KB" command
```

## Liens

### ln - Link

Créer liens (shortcuts).

```bash
# Lien symbolique (symlink)
ln -s /path/to/source link_name

# Lien dur (hard link)
ln /path/to/source link_name

# Lien vers dossier
ln -s /path/to/directory/ link_name

# Force création
ln -sf /path/to/source link_name

# Différence:
# Symlink : pointeur vers chemin (peut pointer vers autre partition)
# Hard link : même inode (même partition uniquement)
```

## Utilisateurs et groupes

### useradd / adduser

Créer utilisateur.

```bash
# Créer utilisateur (basique)
sudo useradd username

# Créer avec home directory
sudo useradd -m username

# Avec shell spécifique
sudo useradd -m -s /bin/bash username

# Créer utilisateur (interactif)
sudo adduser username
```

### usermod

Modifier utilisateur.

```bash
# Ajouter à groupe
sudo usermod -aG groupname username

# Changer shell
sudo usermod -s /bin/zsh username

# Changer home
sudo usermod -d /new/home username

# Désactiver compte
sudo usermod -L username

# Réactiver compte
sudo usermod -U username
```

### passwd

Changer mot de passe.

```bash
# Changer son mot de passe
passwd

# Changer mot de passe utilisateur
sudo passwd username

# Forcer changement au prochain login
sudo passwd -e username

# Désactiver mot de passe
sudo passwd -d username
```

### su - Switch User

Changer d'utilisateur.

```bash
# Devenir root
su

# Devenir utilisateur
su username

# Avec environnement utilisateur
su - username
```

### sudo

Exécuter comme super-utilisateur.

```bash
# Exécuter commande en root
sudo command

# Devenir root
sudo -i
sudo su

# Exécuter comme autre utilisateur
sudo -u username command

# Éditer fichier système
sudo nano /etc/file

# Lister permissions sudo
sudo -l
```

### groups

Afficher groupes.

```bash
# Groupes de l'utilisateur actuel
groups

# Groupes d'un utilisateur
groups username

# Créer groupe
sudo groupadd groupname

# Supprimer groupe
sudo groupdel groupname
```

## Disques et partitions

### mount / umount

Monter/démonter systèmes de fichiers.

```bash
# Lister montages
mount

# Monter partition
sudo mount /dev/sdb1 /mnt

# Monter avec type
sudo mount -t ext4 /dev/sdb1 /mnt

# Démonter
sudo umount /mnt

# Force démontage
sudo umount -f /mnt

# Montage lecture seule
sudo mount -o ro /dev/sdb1 /mnt
```

### fdisk

Gérer partitions.

```bash
# Lister disques
sudo fdisk -l

# Éditer partitions
sudo fdisk /dev/sdb

# Dans fdisk:
# m : aide
# p : afficher partitions
# n : nouvelle partition
# d : supprimer partition
# w : écrire et quitter
# q : quitter sans sauver
```

### mkfs

Formater partition.

```bash
# Formater en ext4
sudo mkfs.ext4 /dev/sdb1

# Formater en FAT32
sudo mkfs.vfat /dev/sdb1

# Formater en NTFS
sudo mkfs.ntfs /dev/sdb1
```

## Système

### systemctl

Gérer services (systemd).

```bash
# Démarrer service
sudo systemctl start nginx

# Arrêter service
sudo systemctl stop nginx

# Redémarrer service
sudo systemctl restart nginx

# Recharger configuration
sudo systemctl reload nginx

# Statut service
systemctl status nginx

# Activer au démarrage
sudo systemctl enable nginx

# Désactiver au démarrage
sudo systemctl disable nginx

# Lister services
systemctl list-units --type=service

# Lister services actifs
systemctl list-units --type=service --state=running
```

### journalctl

Consulter logs systemd.

```bash
# Tous les logs
journalctl

# Logs d'un service
journalctl -u nginx

# Suivre logs en temps réel
journalctl -f

# Logs depuis démarrage
journalctl -b

# Logs dernière heure
journalctl --since "1 hour ago"

# Logs aujourd'hui
journalctl --since today

# Logs avec priorité erreur
journalctl -p err

# Vider logs
sudo journalctl --vacuum-time=3d
```

### cron

Tâches planifiées.

```bash
# Éditer crontab
crontab -e

# Lister crontab
crontab -l

# Supprimer crontab
crontab -r

# Format:
# * * * * * commande
# │ │ │ │ │
# │ │ │ │ └─ jour de la semaine (0-7)
# │ │ │ └─── mois (1-12)
# │ │ └───── jour du mois (1-31)
# │ └─────── heure (0-23)
# └───────── minute (0-59)

# Exemples:
# Toutes les heures
0 * * * * command

# Tous les jours à 3h
0 3 * * * command

# Tous les lundis à 8h
0 8 * * 1 command

# Toutes les 5 minutes
*/5 * * * * command
```

### at

Exécuter commande à heure donnée.

```bash
# Exécuter dans 5 minutes
echo "command" | at now + 5 minutes

# Exécuter à 15h30
echo "command" | at 15:30

# Exécuter demain
echo "command" | at tomorrow

# Lister jobs
atq

# Supprimer job
atrm job_number
```

## Réseau de base

### ping

Test de connectivité.

```bash
# Ping
ping google.com

# Limite à 5 paquets
ping -c 5 google.com

# Intervalle personnalisé
ping -i 2 google.com

# Taille paquet
ping -s 100 google.com
```

### ifconfig / ip

Configuration réseau.

```bash
# Afficher interfaces (ancien)
ifconfig

# Afficher interfaces (nouveau)
ip addr
ip a

# Interface spécifique
ip addr show eth0

# Configurer IP
sudo ip addr add 192.168.1.100/24 dev eth0

# Activer interface
sudo ip link set eth0 up

# Désactiver interface
sudo ip link set eth0 down
```

### netstat / ss

Statistiques réseau.

```bash
# Connexions actives (ancien)
netstat -tuln

# Connexions actives (nouveau)
ss -tuln

# Ports en écoute
ss -tuln | grep LISTEN

# Processus utilisant port
sudo ss -tulnp

# Toutes les connexions
ss -a
```

[← Linux Base](./infos-terminal-01-linux-base.md) | [Index](./infos-terminal-00-index.md) | [Filesystem →](./infos-terminal-03-linux-filesystem.md)

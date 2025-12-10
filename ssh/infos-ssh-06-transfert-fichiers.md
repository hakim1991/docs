# 📁 Transfert de fichiers

[← Tunneling](./infos-ssh-05-tunneling.md) | [Index](./infos-ssh-00-index.md) | [Sécurisation →](./infos-ssh-07-securisation.md)

## SCP (Secure Copy)

```bash
# Copier un fichier vers un serveur
scp file.txt user@server:/path/to/destination/

# Copier depuis un serveur
scp user@server:/path/to/file.txt .

# Copier un répertoire
scp -r folder/ user@server:/path/to/destination/

# Avec port personnalisé
scp -P 2222 file.txt user@server:/path/

# Préserver les métadonnées (timestamps, permissions)
scp -p file.txt user@server:/path/

# Mode verbeux
scp -v file.txt user@server:/path/

# Copier plusieurs fichiers
scp file1.txt file2.txt user@server:/path/

# Avec wildcard
scp *.txt user@server:/path/

# Copier entre deux serveurs distants
scp user1@server1:/path/file.txt user2@server2:/path/

# Avec compression
scp -C large-file.txt user@server:/path/

# Limiter la bande passante (en Kbit/s)
scp -l 1000 file.txt user@server:/path/
# 1000 Kbit/s = 125 KB/s

# Copier avec clé spécifique
scp -i ~/.ssh/mykey file.txt user@server:/path/
```

## SFTP (SSH File Transfer Protocol)

```bash
# Se connecter à un serveur SFTP
sftp user@server

# Avec port personnalisé
sftp -P 2222 user@server

# Commandes SFTP:

# Navigation
pwd                 # Répertoire distant actuel
lpwd                # Répertoire local actuel
ls                  # Lister répertoire distant
lls                 # Lister répertoire local
cd /path            # Changer répertoire distant
lcd /path           # Changer répertoire local

# Upload
put file.txt                    # Upload un fichier
put file.txt remote-name.txt    # Upload avec nouveau nom
put -r folder/                  # Upload un répertoire
mput *.txt                      # Upload multiple

# Download
get file.txt                    # Download un fichier
get file.txt local-name.txt     # Download avec nouveau nom
get -r folder/                  # Download un répertoire
mget *.txt                      # Download multiple

# Gestion fichiers
mkdir newdir                    # Créer répertoire distant
lmkdir newdir                   # Créer répertoire local
rm file.txt                     # Supprimer fichier distant
rmdir folder/                   # Supprimer répertoire distant
rename old.txt new.txt          # Renommer distant

# Permissions
chmod 644 file.txt              # Changer permissions distant
chown user file.txt             # Changer propriétaire distant
chgrp group file.txt            # Changer groupe distant

# Infos
df -h                           # Espace disque distant
!df -h                          # Espace disque local
version                         # Version SFTP

# Quitter
exit
quit
bye

# Mode batch (non-interactif)
sftp -b commands.txt user@server

# commands.txt:
cd /var/www
put index.html
chmod 644 index.html
bye

# Avec commande directe
sftp user@server <<EOF
cd /uploads
put file.txt
bye
EOF
```

## Rsync via SSH

```bash
# Synchroniser vers un serveur
rsync -avz file.txt user@server:/path/

# Synchroniser depuis un serveur
rsync -avz user@server:/path/file.txt .

# Options importantes:
# -a : archive (préserve tout)
# -v : verbose
# -z : compression
# -h : human-readable
# -P : progress + partial (reprendre si interrompu)
# --delete : supprimer fichiers absents de la source

# Synchroniser un répertoire
rsync -avz folder/ user@server:/path/destination/
# Note: "/" après folder/ inclut le contenu, sans "/" inclut le dossier

# Avec progress
rsync -avzP folder/ user@server:/path/

# Dry-run (tester sans exécuter)
rsync -avzn folder/ user@server:/path/

# Exclure des fichiers
rsync -avz --exclude='*.log' --exclude='node_modules/' folder/ user@server:/path/

# Inclure seulement certains fichiers
rsync -avz --include='*.txt' --exclude='*' folder/ user@server:/path/

# Supprimer les fichiers sur destination absents de source
rsync -avz --delete folder/ user@server:/path/

# Avec bande passante limitée (Ko/s)
rsync -avz --bwlimit=1000 folder/ user@server:/path/

# Avec port SSH personnalisé
rsync -avz -e "ssh -p 2222" folder/ user@server:/path/

# Avec clé SSH spécifique
rsync -avz -e "ssh -i ~/.ssh/mykey" folder/ user@server:/path/

# Backup incrémentiel
rsync -avz --backup --backup-dir=../backup-$(date +%Y%m%d) folder/ user@server:/path/

# Voir les différences avant sync
rsync -avzn --itemize-changes folder/ user@server:/path/
```

## Tar + SSH (pipe)

```bash
# Compresser et transférer
tar czf - folder/ | ssh user@server 'cat > backup.tar.gz'

# Transférer et décompresser
tar czf - folder/ | ssh user@server 'tar xzf - -C /destination/'

# Depuis serveur vers local
ssh user@server 'tar czf - /path/folder/' | tar xzf - -C /local/dest/

# Avec progress (pv)
tar czf - folder/ | pv | ssh user@server 'cat > backup.tar.gz'

# Backup complet d'un serveur
ssh user@server 'tar czf - /var/www /etc/nginx' | cat > server-backup.tar.gz

# Exclure des fichiers
tar czf - --exclude='*.log' --exclude='node_modules' folder/ | ssh user@server 'tar xzf - -C /dest/'
```

## DD via SSH (clone disk/partition)

```bash
# Cloner une partition vers un fichier
ssh user@server 'dd if=/dev/sda1 bs=1M' | dd of=partition-backup.img

# Restaurer une partition
dd if=partition-backup.img bs=1M | ssh user@server 'dd of=/dev/sda1'

# Avec compression
ssh user@server 'dd if=/dev/sda1 bs=1M | gzip' | cat > partition-backup.img.gz

# Avec progress (pv)
ssh user@server 'dd if=/dev/sda1 bs=1M' | pv | dd of=partition-backup.img

# Cloner un disque complet
ssh user@server 'dd if=/dev/sda bs=1M status=progress' | dd of=disk-backup.img
```

## Scripts de transfert automatisés

```bash
#!/bin/bash
# backup_to_server.sh

SOURCE="/var/www"
DEST="user@server:/backups"
DATE=$(date +%Y%m%d_%H%M%S)
LOG="/var/log/backup.log"

echo "=== Backup $(date) ===" >> $LOG

# Rsync avec options
rsync -avz \
    --delete \
    --backup \
    --backup-dir=../old-$DATE \
    --exclude='*.log' \
    --exclude='cache/' \
    $SOURCE/ $DEST/ >> $LOG 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Backup réussi" >> $LOG
else
    echo "❌ Échec du backup" >> $LOG
    # Envoyer alerte
    mail -s "Backup failed" admin@example.com < $LOG
fi

echo "" >> $LOG
```

```bash
#!/bin/bash
# sync_website.sh - Déploiement

LOCAL="./dist"
REMOTE="user@server:/var/www/html"

echo "🚀 Déploiement en cours..."

# Dry-run d'abord
echo "Test (dry-run):"
rsync -avzn --delete $LOCAL/ $REMOTE/

read -p "Continuer? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rsync -avz --delete $LOCAL/ $REMOTE/
    echo "✅ Déploiement terminé"
else
    echo "❌ Déploiement annulé"
fi
```

## SSHFS (monter un répertoire distant)

```bash
# Installer
sudo apt install sshfs

# Monter un répertoire distant
mkdir ~/remote
sshfs user@server:/path/to/remote ~/remote

# Avec options
sshfs user@server:/path ~/remote \
    -o reconnect \
    -o ServerAliveInterval=15 \
    -o ServerAliveCountMax=3

# Port personnalisé
sshfs -p 2222 user@server:/path ~/remote

# Démonter
fusermount -u ~/remote

# Auto-mount au boot (/etc/fstab)
user@server:/path /home/user/remote fuse.sshfs defaults,_netdev,user,idmap=user,allow_other 0 0

# Avec clé SSH
sshfs -o IdentityFile=~/.ssh/mykey user@server:/path ~/remote
```

## FTP via SSH (ProFTPD/vsftpd avec SFTP)

```bash
# ProFTPD avec SFTP
sudo apt install proftpd-basic

# Configuration /etc/proftpd/proftpd.conf
SFTPEngine on
Port 2222
SFTPHostKey /etc/ssh/ssh_host_rsa_key
SFTPHostKey /etc/ssh/ssh_host_ecdsa_key

# vsftpd avec SSL (FTPS)
sudo apt install vsftpd
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/vsftpd.key \
    -out /etc/ssl/certs/vsftpd.crt

# /etc/vsftpd.conf
rsa_cert_file=/etc/ssl/certs/vsftpd.crt
rsa_private_key_file=/etc/ssl/private/vsftpd.key
ssl_enable=YES
```

## Clients graphiques

```bash
# FileZilla (GUI)
sudo apt install filezilla

# Configuration:
# Host: sftp://server.example.com
# Port: 22
# Protocol: SFTP
# Login: user
# Password: ou utiliser clé SSH

# WinSCP (Windows)
# - Support SFTP, SCP, FTP
# - Interface graphique
# - Synchronisation
# - Scripting

# Cyberduck (Mac/Windows)
# - Support SFTP
# - Interface drag & drop
# - Bookmark servers
```

## Performance et optimisation

```bash
# Compression pour connexions lentes
scp -C file.txt user@server:/path/
rsync -avz file.txt user@server:/path/

# Désactiver compression pour connexions rapides
scp -o "Compression=no" file.txt user@server:/path/
rsync -av file.txt user@server:/path/

# Augmenter le buffer SSH
ssh -o "SendEnv BUFSIZE=262144" user@server

# Paralléliser avec GNU parallel
find . -type f | parallel -j4 scp {} user@server:/dest/

# Rsync avec plusieurs threads (--fuzzy)
rsync -avz --fuzzy folder/ user@server:/path/

# Checksum au lieu de timestamp (plus lent mais précis)
rsync -avzc folder/ user@server:/path/
```

## Cas pratiques

```bash
# Backup automatique quotidien
# /etc/cron.d/backup
0 2 * * * user /usr/local/bin/backup.sh

# backup.sh:
#!/bin/bash
rsync -avz --delete /var/www/ user@backup-server:/backups/www/
rsync -avz --delete /var/lib/mysql/ user@backup-server:/backups/mysql/

# Déploiement git + rsync
#!/bin/bash
cd /path/to/repo
git pull origin main
npm run build
rsync -avz --delete dist/ user@server:/var/www/html/

# Synchronisation bidirectionnelle (attention!)
# Serveur → Local
rsync -avz user@server:/data/ /local/data/
# Local → Serveur
rsync -avz /local/data/ user@server:/data/

# Mirror complet d'un site web
rsync -avz --delete \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='*.log' \
    /var/www/ user@mirror-server:/var/www/
```

## Troubleshooting

```bash
# Permission denied
# Vérifier les permissions destination
ssh user@server 'ls -la /destination/path/'

# Slow transfer
# Activer compression
scp -C file.txt user@server:/path/

# Tester la vitesse
dd if=/dev/zero bs=1M count=100 | ssh user@server 'cat > /dev/null'

# Connection lost pendant transfert
# Utiliser rsync avec -P (partial + progress)
rsync -avzP file.txt user@server:/path/

# SFTP chroot issues
# Vérifier /etc/ssh/sshd_config:
Match Group sftponly
    ChrootDirectory /home/%u
    ForceCommand internal-sftp

# Le répertoire chroot doit appartenir à root
sudo chown root:root /home/sftpuser
sudo chmod 755 /home/sftpuser

# Rsync errors
# Vérifier les permissions et l'espace disque
rsync -avzn --dry-run folder/ user@server:/path/
```

[← Tunneling](./infos-ssh-05-tunneling.md) | [Index](./infos-ssh-00-index.md) | [Sécurisation →](./infos-ssh-07-securisation.md)

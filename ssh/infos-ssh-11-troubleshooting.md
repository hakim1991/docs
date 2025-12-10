# 🔧 Troubleshooting SSH

[← Automatisation](./infos-ssh-10-automatisation.md) | [Index](./infos-ssh-00-index.md)

## Erreurs courantes de connexion

### Connection refused

```bash
# Erreur: "Connection refused"

# 1. Vérifier que SSH est démarré
sudo systemctl status ssh
sudo systemctl status sshd

# Si arrêté, démarrer
sudo systemctl start ssh

# 2. Vérifier le port
sudo netstat -tulpn | grep :22
sudo ss -tulpn | grep :22

# 3. Vérifier le firewall
sudo ufw status
sudo ufw allow 22/tcp

# CentOS/RHEL
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload

# 4. Vérifier la configuration
sudo sshd -t

# 5. Logs
sudo tail -f /var/log/auth.log
sudo journalctl -u ssh -f
```

### Connection timeout

```bash
# Erreur: "Connection timed out"

# 1. Ping le serveur
ping server.example.com

# 2. Vérifier la route
traceroute server.example.com

# 3. Tester le port
telnet server.example.com 22
nc -zv server.example.com 22

# 4. Vérifier le firewall distant
# Sur le serveur:
sudo iptables -L -n | grep 22

# 5. Augmenter le timeout
ssh -o ConnectTimeout=60 user@server
```

### Permission denied (publickey)

```bash
# Erreur: "Permission denied (publickey)"

# 1. Vérifier les permissions locales
ls -la ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# 2. Vérifier que la clé est sur le serveur
ssh user@server "cat ~/.ssh/authorized_keys" | grep -f ~/.ssh/id_ed25519.pub

# 3. Permissions sur le serveur
ssh user@server "ls -la ~/.ssh"
# Doit être:
# drwx------ .ssh
# -rw------- authorized_keys

# Corriger:
ssh user@server "chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"

# 4. Vérifier la configuration serveur
sudo grep "PubkeyAuthentication" /etc/ssh/sshd_config
# Doit être: PubkeyAuthentication yes

# 5. Test verbose
ssh -vvv user@server

# 6. Vérifier SELinux (si activé)
ssh user@server "restorecon -Rv ~/.ssh"

# 7. Essayer avec password temporairement
ssh -o PreferredAuthentications=password user@server
```

### Host key verification failed

```bash
# Erreur: "Host key verification failed" ou "REMOTE HOST IDENTIFICATION HAS CHANGED"

# ⚠️ ATTENTION: Vérifier pourquoi la clé a changé avant de continuer!
# Peut indiquer une attaque man-in-the-middle

# Si changement légitime (réinstallation serveur):

# 1. Supprimer l'ancienne clé
ssh-keygen -R server.example.com

# 2. Ou éditer ~/.ssh/known_hosts
nano ~/.ssh/known_hosts
# Supprimer la ligne correspondante

# 3. Reconnecter
ssh user@server
# Taper "yes" pour accepter la nouvelle clé

# Pour éviter la vérification (DEV UNIQUEMENT)
ssh -o StrictHostKeyChecking=no user@server
```

### Too many authentication failures

```bash
# Erreur: "Too many authentication failures"

# Cause: Trop de clés SSH essayées

# Solution 1: Utiliser une clé spécifique
ssh -o IdentitiesOnly=yes -i ~/.ssh/specific_key user@server

# Solution 2: Dans ~/.ssh/config
Host server
    IdentityFile ~/.ssh/specific_key
    IdentitiesOnly yes

# Solution 3: Limiter les clés dans ssh-agent
ssh-add -D              # Supprimer toutes
ssh-add ~/.ssh/key1     # Ajouter uniquement nécessaires
ssh-add ~/.ssh/key2
```

## Problèmes d'authentification

### Password authentication disabled

```bash
# Erreur: "Password authentication is disabled"

# Temporairement activer (si vous avez accès physique/console):
# /etc/ssh/sshd_config
PasswordAuthentication yes

sudo systemctl restart ssh

# Se connecter et copier la clé SSH
ssh-copy-id user@server

# Désactiver à nouveau
PasswordAuthentication no
sudo systemctl restart ssh
```

### Agent forwarding not working

```bash
# Agent forwarding ne fonctionne pas

# 1. Vérifier que l'agent est actif
ssh-add -l

# Si erreur, démarrer l'agent
eval $(ssh-agent)
ssh-add

# 2. Configuration client
# ~/.ssh/config
Host server
    ForwardAgent yes

# 3. Vérifier serveur
# /etc/ssh/sshd_config
AllowAgentForwarding yes

# 4. Test
ssh -A user@server
# Sur le serveur:
ssh-add -l
# Doit afficher les clés
```

### 2FA not prompting

```bash
# 2FA ne demande pas le code

# 1. Vérifier PAM
# /etc/pam.d/sshd
# Doit contenir:
auth required pam_google_authenticator.so

# 2. Vérifier sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# 3. Logs
sudo tail -f /var/log/auth.log

# 4. Test
ssh -v user@server
```

## Problèmes de performance

### Connexion lente

```bash
# Connexion prend du temps à s'établir

# 1. Désactiver DNS lookup
# /etc/ssh/sshd_config
UseDNS no

sudo systemctl restart ssh

# 2. Désactiver GSSAPI
# ~/.ssh/config
Host *
    GSSAPIAuthentication no

# 3. Vérifier la latence
ping server.example.com

# 4. Test avec verbosité
ssh -vvv user@server 2>&1 | grep "time"

# 5. Multiplexing
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%C
    ControlPersist 10m
```

### Transfert lent

```bash
# Transferts SCP/SFTP lents

# 1. Activer compression
scp -C file.txt user@server:/path/

# 2. Utiliser un cipher plus rapide
scp -c aes128-gcm@openssh.com file.txt user@server:/path/

# 3. Augmenter le buffer
# ~/.ssh/config
Host *
    SendEnv BUFSIZE=262144

# 4. Utiliser rsync
rsync -avz --progress file.txt user@server:/path/

# 5. Test de vitesse
dd if=/dev/zero bs=1M count=100 | ssh user@server 'cat > /dev/null'
# Compare avec:
dd if=/dev/zero bs=1M count=100 | pv | ssh user@server 'cat > /dev/null'
```

### Disconnections fréquentes

```bash
# Déconnexions aléatoires

# 1. KeepAlive client
# ~/.ssh/config
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes

# 2. KeepAlive serveur
# /etc/ssh/sshd_config
ClientAliveInterval 60
ClientAliveCountMax 3

# 3. Vérifier MTU
ip link show | grep mtu

# 4. Test de stabilité
while true; do
    ssh user@server "date"
    sleep 60
done
```

## Problèmes de tunneling

### Port forwarding not working

```bash
# Port forwarding ne fonctionne pas

# 1. Vérifier la configuration serveur
# /etc/ssh/sshd_config
AllowTcpForwarding yes

# Pour remote forwarding:
GatewayPorts yes

sudo systemctl restart ssh

# 2. Test local forwarding
ssh -v -L 8080:localhost:80 user@server

# Vérifier que le port écoute
netstat -tlnp | grep 8080
ss -tlnp | grep 8080

# 3. Test remote forwarding
ssh -v -R 8080:localhost:3000 user@server

# Sur le serveur:
netstat -tlnp | grep 8080

# 4. Port déjà utilisé
lsof -i :8080
# Choisir un autre port

# 5. Firewall
sudo ufw allow 8080/tcp
```

### SOCKS proxy issues

```bash
# Proxy SOCKS ne fonctionne pas

# 1. Créer le proxy
ssh -v -D 8080 user@server

# 2. Tester
curl --socks5 localhost:8080 https://ifconfig.me

# 3. Vérifier que le port écoute
netstat -tlnp | grep 8080

# 4. Test avec browser
# Firefox: Préférences → Réseau → SOCKS v5: localhost:8080

# 5. Logs
ssh -vvv -D 8080 user@server
```

## Problèmes de clés SSH

### Can't load private key

```bash
# Erreur: "Load key: invalid format"

# 1. Vérifier le format
head -1 ~/.ssh/id_rsa
# Doit commencer par: -----BEGIN OPENSSH PRIVATE KEY-----

# 2. Si format ancien
ssh-keygen -p -m PEM -f ~/.ssh/id_rsa

# 3. Permissions
chmod 600 ~/.ssh/id_rsa

# 4. Vérifier l'intégrité
ssh-keygen -y -f ~/.ssh/id_rsa
```

### Passphrase issues

```bash
# Passphrase demandée à chaque fois

# 1. Utiliser ssh-agent
eval $(ssh-agent)
ssh-add ~/.ssh/id_ed25519

# 2. Vérifier
ssh-add -l

# 3. Permanent (ajouter dans ~/.bashrc)
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval $(ssh-agent)
    ssh-add ~/.ssh/id_ed25519
fi

# 4. Avec timeout
ssh-add -t 3600 ~/.ssh/id_ed25519

# 5. Keychain (Ubuntu/Debian)
sudo apt install keychain
eval $(keychain --eval id_ed25519)
```

### Key not accepted

```bash
# Clé non acceptée

# 1. Vérifier que la clé est sur le serveur
ssh user@server "cat ~/.ssh/authorized_keys"

# 2. Format de la clé
# Doit être une ligne, format:
# ssh-ed25519 AAAAC3... comment

# 3. Vérifier que clé publique correspond à privée
ssh-keygen -y -f ~/.ssh/id_ed25519 | diff - ~/.ssh/id_ed25519.pub

# 4. Algorithme non supporté
ssh -Q key

# 5. Logs serveur
sudo tail -f /var/log/auth.log | grep sshd
```

## Problèmes serveur

### sshd won't start

```bash
# SSH ne démarre pas

# 1. Vérifier la syntaxe
sudo sshd -t

# 2. Logs
sudo journalctl -u ssh -n 50
sudo tail -50 /var/log/auth.log

# 3. Port déjà utilisé
sudo lsof -i :22
sudo ss -tlnp | grep :22

# 4. Permissions
ls -la /etc/ssh/sshd_config
# Doit être: -rw-------

sudo chmod 600 /etc/ssh/sshd_config

# 5. Clés host manquantes
ls -la /etc/ssh/ssh_host_*
# Régénérer si nécessaire
sudo ssh-keygen -A

# 6. Forcer le démarrage
sudo /usr/sbin/sshd -d
```

### Too many connections

```bash
# "Too many open files" ou "Resource temporarily unavailable"

# 1. Voir les limites
ulimit -n

# 2. Augmenter temporairement
ulimit -n 4096

# 3. Permanent
# /etc/security/limits.conf
*  soft  nofile  4096
*  hard  nofile  8192

# 4. Pour SSH spécifiquement
# /etc/systemd/system/ssh.service.d/override.conf
[Service]
LimitNOFILE=8192

# 5. Recharger
sudo systemctl daemon-reload
sudo systemctl restart ssh

# 6. Vérifier les connexions actives
who
w
ss -tn | grep :22 | wc -l
```

### Logs flooding

```bash
# Logs SSH qui remplissent le disque

# 1. Vérifier la taille
du -sh /var/log/auth.log

# 2. fail2ban pour bloquer attaques
sudo apt install fail2ban

# 3. Rotation des logs
# /etc/logrotate.d/ssh
/var/log/auth.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
}

# 4. Changer le port SSH
# /etc/ssh/sshd_config
Port 2222

# 5. Limiter les tentatives
# /etc/ssh/sshd_config
MaxAuthTries 3
MaxStartups 3:50:10
```

## Debug avancé

### Mode debug complet

```bash
# Serveur en mode debug
sudo /usr/sbin/sshd -d -p 2222

# Client en mode debug
ssh -vvv user@server

# Capturer tout
ssh -vvv user@server 2>&1 | tee ssh-debug.log

# Analyser
grep -i "error\|fail\|denied" ssh-debug.log
```

### Packet capture

```bash
# Capturer les paquets SSH
sudo tcpdump -i eth0 -w ssh.pcap 'port 22'

# Analyser avec Wireshark
wireshark ssh.pcap

# Ou avec tcpdump
tcpdump -r ssh.pcap -A
```

### strace

```bash
# Tracer les appels système
strace ssh user@server 2>&1 | tee ssh-strace.log

# Côté serveur
sudo strace -p $(pgrep -f "sshd.*user")
```

## Checklist diagnostic

```
📋 Checklist troubleshooting SSH:

☐ 1. SSH est-il démarré?
     systemctl status ssh

☐ 2. Port ouvert?
     ss -tlnp | grep :22

☐ 3. Firewall autorise?
     ufw status | grep 22

☐ 4. Configuration valide?
     sshd -t

☐ 5. Connexion réseau?
     ping server && nc -zv server 22

☐ 6. Permissions correctes?
     ls -la ~/.ssh && ls -la ~/.ssh/authorized_keys

☐ 7. Clé SSH sur le serveur?
     ssh user@server "cat ~/.ssh/authorized_keys"

☐ 8. Logs d'erreur?
     tail -f /var/log/auth.log

☐ 9. Test verbeux?
     ssh -vvv user@server

☐ 10. fail2ban actif?
      fail2ban-client status sshd
```

## Commandes utiles

```bash
# Informations système
ssh user@server "uname -a"
ssh user@server "cat /etc/os-release"

# Vérifier l'uptime
ssh user@server "uptime"

# Espace disque
ssh user@server "df -h"

# Mémoire
ssh user@server "free -h"

# Processus SSH
ssh user@server "ps aux | grep ssh"

# Connexions actives
ssh user@server "who"
ssh user@server "w"
ssh user@server "last | head"

# Logs en temps réel
ssh user@server "sudo tail -f /var/log/auth.log"

# Tester une config sans appliquer
sudo sshd -t -f /etc/ssh/sshd_config.new
```

## Ressources

```
📚 Ressources utiles:

Documentation:
- man ssh
- man sshd
- man ssh_config
- man sshd_config

Sites web:
- https://www.openssh.com/
- https://wiki.archlinux.org/title/OpenSSH
- https://linux.die.net/man/1/ssh

Forums:
- Stack Overflow: [ssh]
- Server Fault
- Unix & Linux Stack Exchange

Outils:
- ssh -vvv : Debug verbose
- sshd -t : Test config
- ssh-keygen : Gestion clés
- ssh-copy-id : Copier clés
- fail2ban : Protection
- ssh-audit : Audit sécurité
```

[← Automatisation](./infos-ssh-10-automatisation.md) | [Index](./infos-ssh-00-index.md)

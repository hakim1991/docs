# 🔒 Sécurisation SSH

[← Transfert de fichiers](./infos-ssh-06-transfert-fichiers.md) | [Index](./infos-ssh-00-index.md) | [Hardening →](./infos-ssh-08-hardening.md)

## Configuration sécurisée de base

```bash
# /etc/ssh/sshd_config

# Désactiver root login
PermitRootLogin no

# Désactiver authentification par mot de passe
PasswordAuthentication no
ChallengeResponseAuthentication no

# Utiliser uniquement clés publiques
PubkeyAuthentication yes

# Désactiver mots de passe vides
PermitEmptyPasswords no

# Désactiver X11 forwarding si inutile
X11Forwarding no

# Désactiver rhosts
IgnoreRhosts yes
HostbasedAuthentication no

# Logs détaillés
LogLevel VERBOSE

# Limiter les utilisateurs
AllowUsers admin developer
# Ou par groupe
AllowGroups sshusers

# Timeout
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Limiter les tentatives
MaxAuthTries 3
MaxSessions 5
MaxStartups 5:50:10

# Redémarrer
sudo systemctl restart ssh
```

## Changer le port SSH

```bash
# /etc/ssh/sshd_config
Port 2222

# Firewall
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp

# SELinux (si activé)
sudo semanage port -a -t ssh_port_t -p tcp 2222

# Redémarrer
sudo systemctl restart ssh

# Connexion
ssh -p 2222 user@server
```

## fail2ban

```bash
# Installer
sudo apt install fail2ban

# Configuration
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
# Ban pour 1 heure après 3 échecs en 10 minutes
bantime = 3600
findtime = 600
maxretry = 3
destemail = admin@example.com
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

# Pour port personnalisé
port = 2222

# Ban plus long pour récidivistes
[sshd-aggressive]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 2
bantime = 86400
findtime = 3600
```

```bash
# Démarrer
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Statut
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Voir les IPs bannies
sudo fail2ban-client get sshd banned

# Débannir une IP
sudo fail2ban-client set sshd unbanip 192.168.1.100

# Logs
sudo tail -f /var/log/fail2ban.log
```

## Algorithmes cryptographiques sécurisés

```bash
# /etc/ssh/sshd_config

# Supprimer les algorithmes faibles
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256

Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr

MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256

# Clés host modernes uniquement
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Supprimer les anciennes clés host
sudo rm /etc/ssh/ssh_host_dsa_key*
sudo rm /etc/ssh/ssh_host_ecdsa_key*

# Régénérer les clés RSA 4096 bits
sudo rm /etc/ssh/ssh_host_rsa_key*
sudo ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""
```

## Authentification par clé uniquement

```bash
# /etc/ssh/sshd_config
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM no

# Générer une clé forte côté client
ssh-keygen -t ed25519 -C "user@email.com"

# Copier sur le serveur
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Tester AVANT de désactiver les passwords
ssh -i ~/.ssh/id_ed25519 user@server

# Une fois validé, désactiver les passwords
sudo systemctl restart ssh
```

## IP Whitelisting

```bash
# /etc/ssh/sshd_config

# Autoriser seulement certaines IPs
Match Address 192.168.1.0/24,10.0.0.0/8
    PasswordAuthentication yes

Match Address *,!192.168.1.0/24,!10.0.0.0/8
    PasswordAuthentication no
    MaxAuthTries 1

# Par utilisateur
Match User admin Address 192.168.1.0/24
    PermitRootLogin no
    AllowTcpForwarding yes

Match User admin Address !192.168.1.0/24
    DenyUsers admin

# Avec iptables
# Autoriser SSH uniquement depuis certaines IPs
sudo iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j DROP

# Sauvegarder
sudo iptables-save > /etc/iptables/rules.v4

# Avec ufw
sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw deny 22
```

## Port Knocking

```bash
# Installer
sudo apt install knockd

# /etc/knockd.conf
[options]
    UseSyslog
    LogFile = /var/log/knockd.log

[openSSH]
    sequence    = 7000,8000,9000
    seq_timeout = 15
    command     = /sbin/iptables -A INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn

[closeSSH]
    sequence    = 9000,8000,7000
    seq_timeout = 15
    command     = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn

# /etc/default/knockd
START_KNOCKD=1
KNOCKD_OPTS="-i eth0"

# Démarrer
sudo systemctl start knockd
sudo systemctl enable knockd

# Côté client
knock server.example.com 7000 8000 9000
ssh user@server.example.com
# Après utilisation
knock server.example.com 9000 8000 7000
```

## SSH Honeypot (détection d'attaques)

```bash
# Installer cowrie (honeypot SSH)
sudo apt install python3-pip python3-venv
git clone https://github.com/cowrie/cowrie.git
cd cowrie
python3 -m venv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt

# Configuration
cp etc/cowrie.cfg.dist etc/cowrie.cfg
nano etc/cowrie.cfg

# Démarrer sur port 2222
bin/cowrie start

# Rediriger port 22 vers 2222
sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 2222

# SSH réel sur port 2223
# /etc/ssh/sshd_config
Port 2223
```

## Monitoring et alertes

```bash
# Script de monitoring
#!/bin/bash
# monitor_ssh.sh

LOG="/var/log/auth.log"
EMAIL="admin@example.com"

# Échecs d'authentification
FAILURES=$(grep "Failed password" $LOG | grep $(date +%b\ %d) | wc -l)

if [ $FAILURES -gt 10 ]; then
    echo "⚠️  $FAILURES tentatives d'authentification échouées aujourd'hui" | \
        mail -s "SSH Alert" $EMAIL
fi

# Nouvelles connexions réussies
grep "Accepted publickey" $LOG | grep $(date +%b\ %d) | \
    mail -s "SSH Successful Logins" $EMAIL

# IPs suspectes (multiples échecs)
grep "Failed password" $LOG | \
    awk '{print $(NF-3)}' | \
    sort | uniq -c | sort -nr | head -5 | \
    mail -s "SSH Failed IPs" $EMAIL
```

```bash
# Cron quotidien
# /etc/cron.daily/ssh-monitor
0 8 * * * /usr/local/bin/monitor_ssh.sh
```

## Logging et audit

```bash
# /etc/ssh/sshd_config
SyslogFacility AUTH
LogLevel VERBOSE

# Logs détaillés
sudo tail -f /var/log/auth.log

# Analyser les logs
# Connexions réussies
sudo grep "Accepted" /var/log/auth.log

# Échecs
sudo grep "Failed" /var/log/auth.log

# Par utilisateur
sudo grep "user admin" /var/log/auth.log

# Top 10 IPs avec échecs
sudo grep "Failed password" /var/log/auth.log | \
    awk '{print $(NF-3)}' | \
    sort | uniq -c | sort -nr | head -10

# Connexions actives
who
w
last

# Historique complet
last -a
lastlog

# Script d'analyse quotidien
#!/bin/bash
# ssh-report.sh
echo "=== Rapport SSH $(date) ==="
echo ""
echo "Connexions réussies:"
grep "Accepted" /var/log/auth.log | grep $(date +%b\ %d) | wc -l
echo ""
echo "Tentatives échouées:"
grep "Failed" /var/log/auth.log | grep $(date +%b\ %d) | wc -l
echo ""
echo "Top 5 IPs:"
grep "Failed password" /var/log/auth.log | \
    grep $(date +%b\ %d) | \
    awk '{print $(NF-3)}' | \
    sort | uniq -c | sort -nr | head -5
```

## SSH Bastion/Jump Server

```bash
# Configuration bastion
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
AllowTcpForwarding yes
X11Forwarding no
PermitTunnel no
AllowAgentForwarding yes

# Logs tout
LogLevel VERBOSE

# Utilisateurs limités
Match Group bastion-users
    AllowTcpForwarding yes
    ForceCommand /usr/local/bin/bastion-shell

# Script bastion-shell
#!/bin/bash
echo "=== Bastion Server ==="
echo "Connexion de $(whoami) depuis $SSH_CLIENT"
logger "Bastion: $(whoami) from $SSH_CLIENT"

# Menu des serveurs
echo "Serveurs disponibles:"
echo "1) prod-web"
echo "2) prod-db"
echo "3) dev-server"
read -p "Choix: " choice

case $choice in
    1) ssh prod-web ;;
    2) ssh prod-db ;;
    3) ssh dev-server ;;
    *) echo "Choix invalide" ;;
esac
```

## Certificats SSL/TLS pour SFTP

```bash
# Générer certificat
sudo openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout /etc/ssh/sftp-server.key \
    -out /etc/ssh/sftp-server.crt

# /etc/ssh/sshd_config
Subsystem sftp /usr/lib/openssh/sftp-server

Match Group sftpusers
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    X11Forwarding no
    AllowTcpForwarding no
    PubkeyAuthentication yes
    PasswordAuthentication no
```

## Audit avec auditd

```bash
# Installer
sudo apt install auditd

# Auditer SSH
sudo auditctl -w /etc/ssh/sshd_config -p wa -k sshd_config
sudo auditctl -w /home -p wa -k home_changes

# Voir les audits
sudo ausearch -k sshd_config
sudo ausearch -k home_changes

# Rapport
sudo aureport -au
```

## Détection d'intrusion avec OSSEC

```bash
# Installer OSSEC
wget https://github.com/ossec/ossec-hids/archive/3.7.0.tar.gz
tar -zxf 3.7.0.tar.gz
cd ossec-hids-*/
sudo sh install.sh

# Configuration
sudo nano /var/ossec/etc/ossec.conf

# Surveiller SSH
<localfile>
    <log_format>syslog</log_format>
    <location>/var/log/auth.log</location>
</localfile>

# Démarrer
sudo /var/ossec/bin/ossec-control start
```

## Checklist sécurité

```
✅ Configuration sécurisée:
  ☐ Port SSH changé
  ☐ Root login désactivé
  ☐ Authentification par clé uniquement
  ☐ fail2ban installé et configuré
  ☐ Algorithmes faibles désactivés
  ☐ Timeouts configurés
  ☐ Utilisateurs limités (AllowUsers/AllowGroups)
  ☐ Logs en mode VERBOSE

✅ Monitoring:
  ☐ Logs surveillés quotidiennement
  ☐ Alertes configurées
  ☐ fail2ban actif
  ☐ Connexions auditées

✅ Clés SSH:
  ☐ Clés Ed25519 ou RSA 4096 bits
  ☐ Passphrases sur toutes les clés
  ☐ Clés différentes par serveur
  ☐ ssh-agent utilisé
  ☐ Permissions correctes (600/700)

✅ Firewall:
  ☐ SSH limité aux IPs nécessaires
  ☐ Rate limiting actif
  ☐ Port knocking (optionnel)

✅ Audits:
  ☐ Audit mensuel des clés autorisées
  ☐ Révision des utilisateurs SSH
  ☐ Analyse des logs
  ☐ Test de pénétration
```

[← Transfert de fichiers](./infos-ssh-06-transfert-fichiers.md) | [Index](./infos-ssh-00-index.md) | [Hardening →](./infos-ssh-08-hardening.md)

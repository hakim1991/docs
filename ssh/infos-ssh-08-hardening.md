# 🛡️ Hardening SSH

[← Sécurisation](./infos-ssh-07-securisation.md) | [Index](./infos-ssh-00-index.md) | [Avancé →](./infos-ssh-09-avance.md)

## Configuration ultra-sécurisée

```bash
# /etc/ssh/sshd_config - Configuration maximale sécurité

# Protocol et port
Protocol 2
Port 2222                           # Port non-standard
#AddressFamily inet                 # IPv4 uniquement
ListenAddress 192.168.1.100        # Interface spécifique

# Authentification
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
PermitEmptyPasswords no
HostbasedAuthentication no
IgnoreRhosts yes
UsePAM no

# Méthodes d'authentification
AuthenticationMethods publickey
PubkeyAcceptedKeyTypes ssh-ed25519,rsa-sha2-512,rsa-sha2-256

# Clés autorisées
AuthorizedKeysFile .ssh/authorized_keys
StrictModes yes

# Forwarding (tout désactiver)
AllowTcpForwarding no
AllowStreamLocalForwarding no
GatewayPorts no
X11Forwarding no
PermitTunnel no
PermitUserEnvironment no
AllowAgentForwarding no

# Timeouts et limites
LoginGraceTime 20
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 2
MaxSessions 2
MaxStartups 2:50:5

# Utilisateurs
AllowUsers admin@192.168.1.* deploy@10.0.0.*
DenyUsers root guest

# Cryptographie moderne uniquement
Protocol 2
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key

# Algorithmes d'échange de clés
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256

# Chiffrements
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com

# MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Logs
SyslogFacility AUTH
LogLevel VERBOSE

# Autres
Compression no                      # Désactiver compression
TCPKeepAlive no
UseDNS no
PrintMotd no
PrintLastLog yes
Banner /etc/ssh/banner.txt

# Chrono
PermitUserRC no
```

```bash
# Vérifier et redémarrer
sudo sshd -t
sudo systemctl restart ssh
```

## Régénérer toutes les clés host

```bash
# Sauvegarder les anciennes clés
sudo mkdir /root/ssh_backup
sudo cp /etc/ssh/ssh_host_* /root/ssh_backup/

# Supprimer toutes les anciennes clés
sudo rm /etc/ssh/ssh_host_*

# Générer nouvelles clés Ed25519 (recommandé)
sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" < /dev/null

# Générer nouvelles clés RSA 4096 bits
sudo ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N "" < /dev/null

# Permissions
sudo chmod 600 /etc/ssh/ssh_host_*
sudo chmod 644 /etc/ssh/ssh_host_*.pub

# Redémarrer
sudo systemctl restart ssh

# Côté client, supprimer l'ancienne empreinte
ssh-keygen -R server.example.com
# Ou éditer ~/.ssh/known_hosts
```

## Audit de sécurité SSH

```bash
# Installer ssh-audit
sudo apt install python3-pip
pip3 install ssh-audit

# Auditer un serveur
ssh-audit server.example.com

# Auditer localhost
ssh-audit localhost

# Sortie JSON
ssh-audit -j server.example.com > audit.json

# Vérifier les algorithmes faibles
ssh-audit localhost | grep "fail"

# Rapport complet
ssh-audit -v localhost > ssh-audit-report.txt
```

## Durcissement système

```bash
# Limiter les ressources SSH
# /etc/security/limits.conf
@sshusers hard nproc 50
@sshusers hard nofile 100
@sshusers hard cpu 10

# Limiter la mémoire
# /etc/systemd/system/ssh.service.d/override.conf
[Service]
MemoryLimit=512M
CPUQuota=25%

# Recharger
sudo systemctl daemon-reload
sudo systemctl restart ssh

# Protection kernel
# /etc/sysctl.conf
# Protéger contre SYN flood
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2

# Désactiver IP forwarding (si pas de routeur)
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Protéger contre IP spoofing
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignorer ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Désactiver source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Appliquer
sudo sysctl -p
```

## SELinux pour SSH

```bash
# Vérifier SELinux
getenforce

# Activer SELinux pour SSH
sudo semanage boolean -m --on ssh_sysadm_login

# Port SSH personnalisé avec SELinux
sudo semanage port -a -t ssh_port_t -p tcp 2222

# Contexte SSH
sudo ls -Z /etc/ssh/
sudo restorecon -Rv /etc/ssh/

# Logs SELinux
sudo ausearch -m avc -ts recent | grep ssh
```

## AppArmor pour SSH

```bash
# Installer AppArmor
sudo apt install apparmor apparmor-utils

# Profil SSH
sudo nano /etc/apparmor.d/usr.sbin.sshd
```

```
#include <tunables/global>

/usr/sbin/sshd {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  capability sys_chroot,
  capability setuid,
  capability setgid,
  capability sys_resource,
  capability audit_write,

  /etc/ssh/** r,
  /etc/motd r,
  /usr/sbin/sshd mr,
  /var/log/auth.log w,

  /home/*/.ssh/authorized_keys r,
  /root/.ssh/authorized_keys r,
}
```

```bash
# Charger le profil
sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.sshd

# Vérifier
sudo aa-status | grep ssh
```

## Chroot SFTP

```bash
# Configuration SFTP avec chroot
# /etc/ssh/sshd_config
Match Group sftponly
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no
    AllowAgentForwarding no

# Créer groupe et utilisateur
sudo groupadd sftponly
sudo useradd -m -G sftponly -s /bin/false sftpuser
sudo passwd sftpuser

# Configurer le chroot
# Le répertoire chroot DOIT appartenir à root
sudo chown root:root /home/sftpuser
sudo chmod 755 /home/sftpuser

# Créer répertoire accessible
sudo mkdir /home/sftpuser/uploads
sudo chown sftpuser:sftponly /home/sftpuser/uploads
sudo chmod 755 /home/sftpuser/uploads

# Redémarrer
sudo systemctl restart ssh

# Test
sftp sftpuser@localhost
```

## Authentification multi-facteurs renforcée

```bash
# 2FA avec Google Authenticator + YubiKey

# Installer
sudo apt install libpam-google-authenticator libpam-yubico

# Configuration utilisateur
google-authenticator

# /etc/pam.d/sshd
# 2FA: Google Authenticator OU YubiKey
auth [success=done default=ignore] pam_google_authenticator.so
auth [success=done default=die] pam_yubico.so id=YUBICO_ID key=SECRET_KEY

# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive:pam
```

## Isolation réseau

```bash
# Créer un namespace réseau pour SSH
sudo ip netns add ssh-isolation

# Interface virtuelle
sudo ip link add veth0 type veth peer name veth1
sudo ip link set veth1 netns ssh-isolation

# Configurer
sudo ip addr add 10.0.0.1/24 dev veth0
sudo ip link set veth0 up

sudo ip netns exec ssh-isolation ip addr add 10.0.0.2/24 dev veth1
sudo ip netns exec ssh-isolation ip link set veth1 up

# Démarrer SSH dans le namespace
sudo ip netns exec ssh-isolation /usr/sbin/sshd -D

# iptables strict pour SSH
sudo iptables -N SSH_RULES
sudo iptables -A SSH_RULES -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A SSH_RULES -p tcp --dport 2222 -m recent --set --name SSH
sudo iptables -A SSH_RULES -p tcp --dport 2222 -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
sudo iptables -A SSH_RULES -p tcp --dport 2222 -j ACCEPT
sudo iptables -A INPUT -j SSH_RULES
```

## Monitoring avancé

```bash
# Script de monitoring sécurité
#!/bin/bash
# ssh-security-check.sh

echo "=== SSH Security Check $(date) ==="

# Vérifier config
echo "Vérification configuration..."
sudo sshd -t && echo "✅ Config OK" || echo "❌ Config invalide"

# Vérifier fail2ban
systemctl is-active fail2ban && echo "✅ fail2ban actif" || echo "❌ fail2ban inactif"

# Tentatives échouées récentes
FAILED=$(grep "Failed password" /var/log/auth.log | grep $(date +%b\ %d) | wc -l)
echo "Tentatives échouées aujourd'hui: $FAILED"
[ $FAILED -gt 20 ] && echo "⚠️  ALERTE: Trop de tentatives"

# Connexions root
ROOT_ATTEMPTS=$(grep "root" /var/log/auth.log | grep "Failed\|Accepted" | grep $(date +%b\ %d) | wc -l)
[ $ROOT_ATTEMPTS -gt 0 ] && echo "⚠️  ALERTE: Tentatives root: $ROOT_ATTEMPTS"

# Vérifier permissions
WRONG_PERMS=$(find /home -name "authorized_keys" ! -perm 600 2>/dev/null)
[ -n "$WRONG_PERMS" ] && echo "⚠️  Permissions incorrectes: $WRONG_PERMS"

# Algorithmes faibles
WEAK=$(sudo sshd -T | grep -E "cbc|md5|sha1" | grep -v sha2)
[ -n "$WEAK" ] && echo "⚠️  Algorithmes faibles détectés"

# Port par défaut
PORT=$(sudo sshd -T | grep "^port" | awk '{print $2}')
[ $PORT -eq 22 ] && echo "⚠️  Port par défaut utilisé"

echo ""
```

## Certificate Authority (CA) complète

```bash
# Créer infrastructure CA
mkdir -p ~/ssh-ca/{ca,users,hosts}
cd ~/ssh-ca/ca

# Clé CA (à protéger!)
ssh-keygen -t ed25519 -f ca_user_key -C "User CA"
ssh-keygen -t ed25519 -f ca_host_key -C "Host CA"

# Signer une clé utilisateur
ssh-keygen -s ca_user_key \
    -I "john_doe" \
    -n john,admin \
    -V +52w \
    -z 1 \
    -O source-address="192.168.1.0/24" \
    ~/ssh-ca/users/john_id_ed25519.pub

# Signer une clé host
ssh-keygen -s ca_host_key \
    -I "server.example.com" \
    -h \
    -n server.example.com,192.168.1.100 \
    -V +520w \
    -z 1 \
    /etc/ssh/ssh_host_ed25519_key.pub

# Configuration serveur
# /etc/ssh/sshd_config
TrustedUserCAKeys /etc/ssh/ca_user_key.pub
HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub

# Configuration client
# ~/.ssh/known_hosts
@cert-authority *.example.com ssh-ed25519 AAAAC3... (ca_host_key.pub)

# Révocation
# /etc/ssh/revoked_keys
ssh-keygen -kf /etc/ssh/revoked_keys /path/to/revoked-cert.pub

# /etc/ssh/sshd_config
RevokedKeys /etc/ssh/revoked_keys
```

## Conformité et standards

```bash
# CIS Benchmark pour OpenSSH
# https://www.cisecurity.org/

# Vérifications clés:
echo "=== CIS Benchmark Check ==="

# Protocol 2 uniquement
sudo sshd -T | grep "^protocol 2"

# Pas de rhosts
sudo sshd -T | grep "ignorerhosts yes"

# Logs
sudo sshd -T | grep "loglevel VERBOSE"

# Root login
sudo sshd -T | grep "permitrootlogin no"

# Permissions
ls -la /etc/ssh/sshd_config | grep "^-rw-------"

# Ownership
ls -la /etc/ssh/sshd_config | grep "root root"

# FIPS 140-2 (si requis)
# Activer FIPS
sudo fips-mode-setup --enable
sudo reboot

# Vérifier
fips-mode-setup --check
```

## Tests de pénétration

```bash
# Nmap scan
nmap -sV -p 22 server.example.com
nmap --script ssh-auth-methods server.example.com
nmap --script ssh2-enum-algos server.example.com

# Hydra (test force brute)
hydra -l user -P passwords.txt ssh://server.example.com

# Medusa
medusa -h server.example.com -u user -P passwords.txt -M ssh

# ⚠️ À faire uniquement sur vos propres serveurs!
```

[← Sécurisation](./infos-ssh-07-securisation.md) | [Index](./infos-ssh-00-index.md) | [Avancé →](./infos-ssh-09-avance.md)

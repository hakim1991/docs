# ⚙️ Configuration SSH

[← Introduction](./infos-ssh-01-introduction-installation.md) | [Index](./infos-ssh-00-index.md) | [Clés SSH →](./infos-ssh-03-cles-ssh.md)

## Configuration client (~/.ssh/config)

```bash
# ~/.ssh/config - Configuration utilisateur

# Serveur de production
Host prod production
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/prod_key
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Serveur de développement
Host dev development
    HostName dev.example.com
    User developer
    IdentityFile ~/.ssh/dev_key
    LocalForward 3000 localhost:3000
    LocalForward 5432 localhost:5432

# Bastion/Jump server
Host bastion
    HostName bastion.example.com
    User jumpuser
    IdentityFile ~/.ssh/bastion_key

# Serveurs derrière le bastion
Host internal-*
    ProxyJump bastion
    User admin

# Wildcard pour tous les serveurs de l'entreprise
Host *.company.com
    User admin
    IdentityFile ~/.ssh/company_key
    Port 22
    Compression yes

# GitHub
Host github.com
    User git
    IdentityFile ~/.ssh/github_key
    PreferredAuthentications publickey

# GitLab
Host gitlab.com
    User git
    IdentityFile ~/.ssh/gitlab_key

# Configuration par défaut
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    TCPKeepAlive yes
    Compression yes
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m
```

```bash
# Créer le répertoire pour les sockets
mkdir -p ~/.ssh/sockets
chmod 700 ~/.ssh/sockets

# Utilisation
ssh prod                    # Se connecte à production
ssh dev                     # Se connecte à développement
ssh internal-db             # Via bastion
```

## Configuration serveur (/etc/ssh/sshd_config)

```bash
# /etc/ssh/sshd_config - Configuration serveur

# Port et adresses
Port 22                             # Changer en production (ex: 2222)
#ListenAddress 0.0.0.0              # Toutes les interfaces
#ListenAddress ::                   # IPv6
ListenAddress 192.168.1.100        # Interface spécifique

# Authentification
PermitRootLogin no                  # Interdire root (recommandé)
#PermitRootLogin prohibit-password  # Root avec clé uniquement
PasswordAuthentication no           # Désactiver mots de passe
PubkeyAuthentication yes            # Authentification par clé
AuthorizedKeysFile .ssh/authorized_keys

# Sécurité
PermitEmptyPasswords no             # Pas de mot de passe vide
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no                    # Désactiver X11 si inutile
PrintMotd no                        # Message du jour
PrintLastLog yes
TCPKeepAlive yes

# Timeouts et limites
LoginGraceTime 60                   # Timeout connexion (secondes)
ClientAliveInterval 300             # Ping toutes les 5 min
ClientAliveCountMax 2               # Déconnexion après 2 pings ratés
MaxAuthTries 3                      # Tentatives d'auth max
MaxSessions 10                      # Sessions max par connexion
MaxStartups 10:30:60                # Connexions simultanées

# Restrictions utilisateurs
AllowUsers admin developer          # Utilisateurs autorisés
#DenyUsers baduser                  # Utilisateurs interdits
#AllowGroups sshusers               # Groupes autorisés
#DenyGroups noremote                # Groupes interdits

# Algorithmes cryptographiques
# Supprimer les algorithmes faibles
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256

# Logs
SyslogFacility AUTH
LogLevel VERBOSE                    # INFO ou VERBOSE

# Subsystèmes
Subsystem sftp /usr/lib/openssh/sftp-server

# Banner
#Banner /etc/ssh/banner.txt

# Match pour configurations spécifiques
Match User developer
    AllowTcpForwarding yes
    PermitTunnel yes

Match User limited
    AllowTcpForwarding no
    PermitTunnel no
    ForceCommand /usr/bin/restricted-shell
```

```bash
# Appliquer la configuration
# Vérifier la syntaxe
sudo sshd -t

# Recharger sans couper les connexions
sudo systemctl reload ssh

# Redémarrer (coupe les connexions)
sudo systemctl restart ssh
```

## Configuration sécurisée

```bash
# /etc/ssh/sshd_config - Configuration haute sécurité

# Ports et interfaces
Port 2222                           # Port non-standard
ListenAddress 192.168.1.100

# Authentification stricte
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
PermitEmptyPasswords no
ChallengeResponseAuthentication no

# Désactiver fonctionnalités inutiles
X11Forwarding no
AllowTcpForwarding no
AllowStreamLocalForwarding no
GatewayPorts no
PermitTunnel no
PermitUserEnvironment no

# Timeouts stricts
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 2
MaxSessions 5
MaxStartups 5:50:10

# Utilisateurs restreints
AllowUsers admin@192.168.1.* deploy@10.0.0.*
DenyUsers root

# Algorithmes modernes uniquement
Protocol 2
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Logs verbeux
LogLevel VERBOSE

# Banner d'avertissement
Banner /etc/ssh/banner.txt
```

```bash
# /etc/ssh/banner.txt
cat << 'EOF' | sudo tee /etc/ssh/banner.txt
**********************************************************************
*                        UNAUTHORIZED ACCESS                         *
*                                                                    *
* This system is for authorized users only. All activities are      *
* monitored and logged. Unauthorized access will be prosecuted.     *
*                                                                    *
**********************************************************************
EOF
```

## Configurations par utilisateur (Match)

```bash
# Configuration différente par utilisateur/groupe

# Développeurs: accès complet
Match Group developers
    AllowTcpForwarding yes
    X11Forwarding yes
    PermitTunnel yes

# Utilisateurs normaux: accès restreint
Match Group users
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no

# SFTP seulement
Match Group sftponly
    ForceCommand internal-sftp
    ChrootDirectory /home/%u
    AllowTcpForwarding no
    X11Forwarding no

# Admin depuis certaines IPs uniquement
Match User admin Address 192.168.1.0/24,10.0.0.0/8
    PermitRootLogin no
    AllowTcpForwarding yes

# Restriction par horaire (nécessite un script)
Match User backup
    ForceCommand /usr/local/bin/time-restricted-shell
```

## Configuration SFTP chroot

```bash
# /etc/ssh/sshd_config

# SFTP avec chroot
Match Group sftpusers
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no

# Créer un utilisateur SFTP
sudo groupadd sftpusers
sudo useradd -m -G sftpusers -s /bin/false sftpuser
sudo passwd sftpuser

# Configurer le chroot
sudo chown root:root /home/sftpuser
sudo chmod 755 /home/sftpuser
sudo mkdir /home/sftpuser/uploads
sudo chown sftpuser:sftpusers /home/sftpuser/uploads

# Tester
sftp sftpuser@localhost
```

## Configuration 2FA (Two-Factor Authentication)

```bash
# Installer Google Authenticator
sudo apt install libpam-google-authenticator

# Configurer pour un utilisateur
google-authenticator
# Répondre: y, y, y, n, y

# Configurer PAM
sudo nano /etc/pam.d/sshd
# Ajouter:
auth required pam_google_authenticator.so

# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# Redémarrer
sudo systemctl restart ssh

# Test
ssh user@server
# Demande: clé SSH + code 2FA
```

## Configuration client avancée

```bash
# ~/.ssh/config

# Connexion persistante (réutiliser la connexion)
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    ControlPersist 10m

# Compression
Host slow-connection
    Compression yes
    CompressionLevel 9

# Proxy SOCKS
Host proxy
    DynamicForward 8080
    ExitOnForwardFailure yes

# Jump hosts
Host final-server
    ProxyJump bastion1,bastion2

# Multiplexing
Host production
    ControlMaster auto
    ControlPath ~/.ssh/control-%r@%h:%p
    ControlPersist yes

# Forward X11
Host gui-server
    ForwardX11 yes
    ForwardX11Trusted yes

# Agent forwarding (attention sécurité)
Host trusted
    ForwardAgent yes

# Sans strict host key checking (dev uniquement)
Host *.dev.local
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
```

## Variables d'environnement SSH

```bash
# Variables côté client
export SSH_AUTH_SOCK=/tmp/ssh-agent.sock
export SSH_AGENT_PID=12345

# Configurer dans le serveur
# /etc/ssh/sshd_config
AcceptEnv LANG LC_*
AcceptEnv MY_CUSTOM_VAR

# Envoyer une variable
ssh -o "SetEnv MY_VAR=value" user@server

# Ou dans ~/.ssh/config
Host server
    SetEnv MY_VAR=value
```

## Logs et monitoring

```bash
# Configuration logs serveur
# /etc/ssh/sshd_config
SyslogFacility AUTH
LogLevel VERBOSE

# Logs système
tail -f /var/log/auth.log              # Debian/Ubuntu
tail -f /var/log/secure                # CentOS/RHEL
journalctl -u ssh -f                   # systemd

# Analyser les logs
# Échecs d'authentification
sudo grep "Failed password" /var/log/auth.log

# Connexions réussies
sudo grep "Accepted" /var/log/auth.log

# Déconnexions
sudo grep "session closed" /var/log/auth.log

# Par utilisateur
sudo grep "user admin" /var/log/auth.log
```

## Tester la configuration

```bash
# Tester la syntaxe serveur
sudo sshd -t

# Afficher la config effective
sudo sshd -T

# Afficher la config pour un utilisateur
sudo sshd -T -C user=admin,host=192.168.1.100,addr=192.168.1.100

# Test de connexion verbeux
ssh -vvv user@server

# Tester les algorithmes
ssh -Q cipher
ssh -Q mac
ssh -Q kex
ssh -Q key
```

## Reload vs Restart

```bash
# Reload: recharge config sans couper connexions
sudo systemctl reload ssh

# Restart: redémarre (coupe connexions)
sudo systemctl restart ssh

# Graceful restart: attend que les connexions se terminent
sudo systemctl reload-or-restart ssh
```

## Backup de la configuration

```bash
#!/bin/bash
# backup_ssh_config.sh

BACKUP_DIR="/backup/ssh"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Sauvegarder configs
sudo cp /etc/ssh/sshd_config $BACKUP_DIR/sshd_config_$DATE
sudo cp -r /etc/ssh/ssh_host_* $BACKUP_DIR/

# Sauvegarder clés utilisateur
cp -r ~/.ssh $BACKUP_DIR/user_ssh_$DATE

echo "✅ Backup SSH effectué: $BACKUP_DIR"
```

[← Introduction](./infos-ssh-01-introduction-installation.md) | [Index](./infos-ssh-00-index.md) | [Clés SSH →](./infos-ssh-03-cles-ssh.md)

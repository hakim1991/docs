# 🚀 SSH Avancé

[← Hardening](./infos-ssh-08-hardening.md) | [Index](./infos-ssh-00-index.md) | [Automatisation →](./infos-ssh-10-automatisation.md)

## Multiplexing avancé

```bash
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%C
    ControlPersist 10m

# %C = hash de %l%h%p%r (unique par connexion)
# Avantages:
# - Connexions instantanées
# - Partage de tunnels
# - Pas de ré-authentification

# Créer le répertoire
mkdir -p ~/.ssh/sockets

# Vérifier les masters actifs
ls -la ~/.ssh/sockets/

# Commandes de contrôle
ssh -O check user@server       # Vérifier si master actif
ssh -O exit user@server         # Fermer le master
ssh -O stop user@server         # Stopper forwarding
ssh -O forward user@server      # Activer forwarding

# Master en background
ssh -fNM user@server

# Connexion via master existant
ssh -S ~/.ssh/sockets/* user@server
```

## ProxyCommand avancé

```bash
# ~/.ssh/config

# Via HTTP proxy (corkscrew)
Host external
    ProxyCommand corkscrew proxy.company.com 8080 %h %p

# Via SOCKS proxy (netcat)
Host via-socks
    ProxyCommand nc -X 5 -x localhost:8080 %h %p

# Via bastion avec port forwarding
Host internal
    ProxyCommand ssh -W %h:%p bastion.example.com

# Chain de bastions
Host final
    ProxyCommand ssh bastion1 -W $(ssh bastion2 -W %h:%p)

# Avec timeout
Host slow-server
    ProxyCommand timeout 30 ssh -W %h:%p bastion

# Via VPN
Host vpn-internal
    ProxyCommand openvpn --config vpn.conf --daemon && ssh -W %h:%p vpn-gateway

# Avec authentification proxy
Host auth-proxy
    ProxyCommand socat - PROXY:proxy.com:%h:%p,proxyport=8080,proxyauth=user:pass
```

## Escape sequences

```bash
# Pendant une session SSH, taper ~? pour voir les commandes

~.      # Déconnecter
~^Z     # Mettre en background
~#      # Lister les forwards
~~      # Envoyer ~
~?      # Aide

# Ajouter un forward dynamiquement
~C      # Ouvrir la ligne de commande SSH
-L 8080:localhost:80    # Ajouter un forward local
-R 9090:localhost:3000  # Ajouter un forward remote
-D 1080                 # Ajouter un SOCKS proxy

# Exemple d'utilisation
# 1. Se connecter: ssh user@server
# 2. Taper: ~C
# 3. Taper: -L 8080:localhost:80
# 4. Taper: Enter

# Background/Foreground
~^Z     # Mettre SSH en background
fg      # Revenir au premier plan
```

## SSH over HTTP/HTTPS

```bash
# Installer corkscrew
sudo apt install corkscrew

# Via proxy HTTP
ssh -o "ProxyCommand corkscrew proxy.example.com 8080 %h %p" user@server

# Via proxy HTTPS avec auth
ssh -o "ProxyCommand corkscrew proxy.example.com 443 %h %p ~/.ssh/proxy-auth" user@server

# ~/.ssh/proxy-auth
username:password

# Permissions
chmod 600 ~/.ssh/proxy-auth

# Dans config
Host via-http-proxy
    ProxyCommand corkscrew proxy.example.com 8080 %h %p ~/.ssh/proxy-auth
```

## SSH over WebSocket

```bash
# Serveur WebSocket SSH (websockify)
sudo apt install websockify

# Démarrer websockify
websockify 8080 localhost:22

# Configuration nginx
location /ssh {
    proxy_pass http://localhost:8080/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}

# Client (avec wssh)
pip install webssh

# Connexion
wssh --host=localhost --port=8080
```

## SSH basé sur FIDO2/U2F

```bash
# Générer une clé FIDO2 (YubiKey, etc.)
ssh-keygen -t ed25519-sk
# Toucher la clé physique quand demandé

# Ou avec résidence (clé stockée dans le token)
ssh-keygen -t ed25519-sk -O resident

# Copier sur le serveur
ssh-copy-id -i ~/.ssh/id_ed25519_sk.pub user@server

# Se connecter (nécessite toucher la clé)
ssh user@server

# Lister les clés résidentes
ssh-keygen -K

# Options avancées
# Nécessiter PIN + touch
ssh-keygen -t ed25519-sk -O verify-required

# Voir les options
ssh-keygen -t ed25519-sk -O help
```

## Connection Multiplexing avec tmux

```bash
# ~/.ssh/config
Host *
    RequestTTY yes
    RemoteCommand tmux new-session -A -s main

# Se connecter
ssh user@server
# Automatiquement dans une session tmux

# Ou avec script
#!/bin/bash
# ssh-tmux.sh
ssh -t user@server "tmux attach-session -t main || tmux new-session -s main"
```

## SSH Agent Forwarding sécurisé

```bash
# ~/.ssh/config
# Agent forwarding sélectif
Host trusted-server
    ForwardAgent yes

Host *
    ForwardAgent no

# Avec confirmation
ssh-add -c ~/.ssh/id_ed25519
# Demande confirmation à chaque utilisation

# Avec timeout
ssh-add -t 3600 ~/.ssh/id_ed25519
# Expire après 1 heure

# Alternative: ProxyJump (plus sécurisé)
Host final-server
    ProxyJump bastion
# Pas besoin de ForwardAgent
```

## SSH avec Kerberos/GSSAPI

```bash
# Configuration Kerberos
# /etc/krb5.conf
[libdefaults]
    default_realm = EXAMPLE.COM
    dns_lookup_realm = false
    dns_lookup_kdc = true

[realms]
    EXAMPLE.COM = {
        kdc = kerberos.example.com
        admin_server = kerberos.example.com
    }

[domain_realm]
    .example.com = EXAMPLE.COM
    example.com = EXAMPLE.COM

# /etc/ssh/sshd_config
GSSAPIAuthentication yes
GSSAPICleanupCredentials yes
GSSAPIStrictAcceptorCheck yes

# Obtenir un ticket
kinit user@EXAMPLE.COM

# Vérifier
klist

# Se connecter
ssh -K user@server.example.com
# -K forward Kerberos credentials

# Renouvellement automatique
# ~/.ssh/config
Host *.example.com
    GSSAPIAuthentication yes
    GSSAPIDelegateCredentials yes
```

## SSH Jump Host avancé

```bash
# ~/.ssh/config

# Chaîne de jumps
Host final
    HostName 10.0.0.100
    ProxyJump jump1,jump2,jump3

# Jump conditionnel
Host internal-*
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User jumpuser
    IdentityFile ~/.ssh/bastion_key

# Jump avec forward
Host app-server
    ProxyJump bastion
    LocalForward 3000 localhost:3000
    LocalForward 5432 localhost:5432

# Jump avec options différentes
Host production
    ProxyJump bastion -p 2222 -i ~/.ssh/bastion_key
```

## Custom AuthorizedKeysCommand

```bash
# Script pour récupérer les clés d'une API
# /usr/local/bin/ssh-keys-from-api
#!/bin/bash
USER=$1
curl -s https://api.example.com/users/$USER/ssh-keys

# Permissions
sudo chmod 755 /usr/local/bin/ssh-keys-from-api

# /etc/ssh/sshd_config
AuthorizedKeysCommand /usr/local/bin/ssh-keys-from-api
AuthorizedKeysCommandUser nobody

# Depuis LDAP
#!/bin/bash
USER=$1
ldapsearch -x -LLL -h ldap.example.com \
    -b "dc=example,dc=com" \
    "(&(uid=$USER)(objectClass=posixAccount))" \
    sshPublicKey | grep "^sshPublicKey:" | sed 's/^sshPublicKey: //'

# Depuis GitHub
#!/bin/bash
USER=$1
curl -s https://github.com/$USER.keys

# Test
/usr/local/bin/ssh-keys-from-api username
```

## Match conditionnelle avancée

```bash
# /etc/ssh/sshd_config

# Par heure
Match User backup LocalPort 22 Address 192.168.1.0/24
    ForceCommand /usr/local/bin/backup.sh

# Par groupe et IP
Match Group developers Address 192.168.1.0/24,10.0.0.0/8
    AllowTcpForwarding yes
    X11Forwarding yes

Match Group developers Address *,!192.168.1.0/24,!10.0.0.0/8
    AllowTcpForwarding no
    X11Forwarding no
    ForceCommand /usr/local/bin/restricted-shell

# Par utilisateur et hôte
Match User admin Host server1.example.com,server2.example.com
    PermitRootLogin no
    AllowTcpForwarding yes

# SFTP pour certains, SSH pour d'autres
Match Group sftponly
    ForceCommand internal-sftp
    ChrootDirectory /home/%u

Match Group developers
    AllowTcpForwarding yes

# Par LocalPort (utile pour multi-instance)
Match LocalPort 2222
    Banner /etc/ssh/banner-alt.txt
    AllowUsers admin
```

## SSH Certificates avancés

```bash
# CA avec options étendues
ssh-keygen -s ca_key \
    -I "john_doe_2024" \
    -n john,admin,root \
    -V +52w \
    -z $(date +%s) \
    -O clear \
    -O source-address="192.168.1.0/24,10.0.0.0/8" \
    -O force-command="/usr/local/bin/restricted-shell" \
    -O no-port-forwarding \
    -O no-agent-forwarding \
    -O no-x11-forwarding \
    -O permit-pty \
    ~/.ssh/john_id_ed25519.pub

# Vérifier le certificat
ssh-keygen -Lf ~/.ssh/john_id_ed25519-cert.pub

# Certificat serveur avec SAN
ssh-keygen -s ca_host_key \
    -I "server.example.com" \
    -h \
    -n server.example.com,*.example.com,192.168.1.100 \
    -V +520w \
    /etc/ssh/ssh_host_ed25519_key.pub

# KRL (Key Revocation List)
# Révoquer par serial
ssh-keygen -k -f revoked_keys -s ca_key -z 12345

# Révoquer par clé publique
ssh-keygen -k -f revoked_keys -u revoked_cert.pub

# Révoquer par hash
ssh-keygen -k -f revoked_keys sha256:HASH

# Utiliser KRL
# /etc/ssh/sshd_config
RevokedKeys /etc/ssh/revoked_keys

# Mettre à jour KRL
ssh-keygen -k -f revoked_keys -u new_revoked_cert.pub
sudo systemctl reload ssh
```

## Audit et forensics

```bash
# Tracer toutes les commandes SSH
# /etc/ssh/sshd_config
ForceCommand /usr/local/bin/ssh-wrapper.sh

# /usr/local/bin/ssh-wrapper.sh
#!/bin/bash
LOG="/var/log/ssh-commands.log"
echo "$(date) - $USER - $SSH_CLIENT - $SSH_ORIGINAL_COMMAND" >> $LOG
logger "SSH: $USER from $SSH_CLIENT executed: $SSH_ORIGINAL_COMMAND"

if [ -z "$SSH_ORIGINAL_COMMAND" ]; then
    # Session interactive
    script -q -c "$SHELL" /var/log/ssh-sessions/$USER-$(date +%Y%m%d-%H%M%S).log
else
    # Commande non-interactive
    eval "$SSH_ORIGINAL_COMMAND"
fi

# Permissions
sudo chmod 755 /usr/local/bin/ssh-wrapper.sh
sudo mkdir -p /var/log/ssh-sessions
sudo chmod 700 /var/log/ssh-sessions

# Audit avec auditd
sudo auditctl -a always,exit -F arch=b64 -S connect -k ssh-connections
sudo auditctl -w /usr/sbin/sshd -p x -k sshd-exec

# Analyser
sudo ausearch -k ssh-connections
sudo ausearch -k sshd-exec
```

## Performance tuning

```bash
# ~/.ssh/config ou /etc/ssh/ssh_config

# Compression
Host slow-connection
    Compression yes
    CompressionLevel 6

# Cipher rapide
Host fast-connection
    Ciphers aes128-gcm@openssh.com
    MACs hmac-sha2-256-etm@openssh.com

# TCP optimizations
Host *
    TCPKeepAlive yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    IPQoS throughput

# Multiplexing
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%C
    ControlPersist 10m

# /etc/ssh/sshd_config côté serveur
# Buffer sizes
# Augmenter pour haute latence
# UseDNS no pour éviter reverse DNS lookup
UseDNS no

# Sysctl optimizations
# /etc/sysctl.conf
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_window_scaling = 1
```

## SSH pour IoT/Embedded

```bash
# Dropbear (SSH léger pour embedded)
sudo apt install dropbear

# Configuration
sudo nano /etc/default/dropbear
DROPBEAR_PORT=22
DROPBEAR_EXTRA_ARGS="-w -s"  # Désactiver root et password

# Démarrer
sudo systemctl start dropbear
sudo systemctl enable dropbear

# Client dropbear
dbclient user@server

# TinySSH (encore plus léger)
git clone https://github.com/janmojzis/tinyssh.git
cd tinyssh
make
sudo make install
```

[← Hardening](./infos-ssh-08-hardening.md) | [Index](./infos-ssh-00-index.md) | [Automatisation →](./infos-ssh-10-automatisation.md)

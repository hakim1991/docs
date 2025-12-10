# 🔐 Authentification avancée

[← Clés SSH](./infos-ssh-03-cles-ssh.md) | [Index](./infos-ssh-00-index.md) | [Tunneling →](./infos-ssh-05-tunneling.md)

## Authentification multi-facteurs (2FA)

### Google Authenticator

```bash
# Installer
sudo apt install libpam-google-authenticator

# Configurer pour l'utilisateur actuel
google-authenticator

# Réponses recommandées:
# Do you want authentication tokens to be time-based? y
# Update .google_authenticator file? y
# Disallow multiple uses? y
# Increase time window? n
# Enable rate-limiting? y

# Scanner le QR code avec l'app mobile

# Configurer PAM
sudo nano /etc/pam.d/sshd
# Commenter cette ligne:
# @include common-auth
# Ajouter:
auth required pam_google_authenticator.so

# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# Optionnel: 2FA ou clé SSH (pas les deux)
# AuthenticationMethods publickey keyboard-interactive

# Redémarrer SSH
sudo systemctl restart ssh

# Test de connexion
ssh user@server
# 1. Clé SSH validée
# 2. Demande du code 2FA
```

### 2FA avec Duo Security

```bash
# Installer
wget https://dl.duosecurity.com/duo_unix-latest.tar.gz
tar xzf duo_unix-latest.tar.gz
cd duo_unix-*
./configure --prefix=/usr
make
sudo make install

# Configuration
sudo nano /etc/duo/pam_duo.conf
```

```ini
[duo]
ikey = YOUR_INTEGRATION_KEY
skey = YOUR_SECRET_KEY
host = api-XXXXXXXX.duosecurity.com
failmode = safe
autopush = yes
```

```bash
# PAM configuration
sudo nano /etc/pam.d/sshd
# Ajouter:
auth required pam_duo.so

# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

sudo systemctl restart ssh
```

## Certificats SSH

### Créer une CA (Certificate Authority)

```bash
# Générer la clé de la CA
ssh-keygen -t ed25519 -f ssh_ca -C "SSH CA"

# Sécuriser la clé CA (très important!)
chmod 600 ssh_ca
chmod 644 ssh_ca.pub

# Sauvegarder la clé CA dans un endroit sûr
# Ne jamais la mettre sur un serveur accessible par SSH
```

### Signer des clés utilisateurs

```bash
# Signer une clé utilisateur
ssh-keygen \
    -s ssh_ca \
    -I "user_john" \
    -n john,admin \
    -V +52w \
    ~/.ssh/id_ed25519.pub

# Options:
# -s ssh_ca          : Clé de la CA
# -I "user_john"     : Identity (unique)
# -n john,admin      : Principals (noms d'utilisateur autorisés)
# -V +52w            : Validité (52 semaines)
# -z 001             : Serial number (optionnel)

# Crée le certificat: ~/.ssh/id_ed25519-cert.pub

# Signer avec des options de sécurité
ssh-keygen \
    -s ssh_ca \
    -I "backup_user" \
    -n backup \
    -V +1d \
    -O source-address=192.168.1.0/24 \
    -O force-command="/usr/local/bin/backup.sh" \
    ~/.ssh/id_ed25519.pub

# Vérifier le certificat
ssh-keygen -Lf ~/.ssh/id_ed25519-cert.pub
```

### Configurer le serveur pour les certificats

```bash
# /etc/ssh/sshd_config
TrustedUserCAKeys /etc/ssh/trusted_user_ca.pub

# Copier la clé publique de la CA sur le serveur
sudo cp ssh_ca.pub /etc/ssh/trusted_user_ca.pub
sudo chmod 644 /etc/ssh/trusted_user_ca.pub

# Redémarrer
sudo systemctl restart ssh

# Test
ssh -i ~/.ssh/id_ed25519 john@server
# Le certificat est automatiquement utilisé
```

### Certificats pour serveurs

```bash
# Sur le serveur, générer une clé host
sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""

# Signer la clé host avec la CA
ssh-keygen \
    -s ssh_ca \
    -I "server.example.com" \
    -h \
    -n server.example.com,192.168.1.100 \
    -V +52w \
    /etc/ssh/ssh_host_ed25519_key.pub

# Crée: /etc/ssh/ssh_host_ed25519_key-cert.pub

# /etc/ssh/sshd_config
HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub

# Côté client, faire confiance à la CA
# ~/.ssh/known_hosts
@cert-authority *.example.com ssh-ed25519 AAAAC3NzaC... (contenu de ssh_ca.pub)

# Test
ssh server.example.com
# Plus d'avertissement "unknown host"
```

## Authentification par hardware (YubiKey)

```bash
# Installer support YubiKey
sudo apt install libpam-yubico yubikey-manager

# Générer une clé sur la YubiKey
ykman piv keys generate -a RSA2048 9a /tmp/public-key.pem

# Créer un certificat auto-signé
ykman piv certificates generate -s "SSH Key" 9a /tmp/public-key.pem

# Extraire la clé publique SSH
ssh-keygen -D /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so -e

# Copier sur le serveur
ssh-copy-id -i <(ssh-keygen -D /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so -e) user@server

# Se connecter avec la YubiKey
ssh -I /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so user@server
```

## LDAP/Active Directory

```bash
# Installer
sudo apt install sssd-ldap ldap-utils

# Configuration SSSD
sudo nano /etc/sssd/sssd.conf
```

```ini
[sssd]
services = nss, pam, ssh
domains = example.com

[domain/example.com]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://ldap.example.com
ldap_search_base = dc=example,dc=com
ldap_default_bind_dn = cn=admin,dc=example,dc=com
ldap_default_authtok = password
```

```bash
# Permissions
sudo chmod 600 /etc/sssd/sssd.conf

# Démarrer
sudo systemctl start sssd
sudo systemctl enable sssd

# Tester
getent passwd
id ldapuser

# /etc/ssh/sshd_config
AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys
AuthorizedKeysCommandUser nobody
PubkeyAuthentication yes

sudo systemctl restart ssh
```

## Kerberos

```bash
# Installer
sudo apt install krb5-user krb5-config

# Configuration
sudo nano /etc/krb5.conf
```

```ini
[libdefaults]
    default_realm = EXAMPLE.COM
    dns_lookup_realm = false
    dns_lookup_kdc = true
    ticket_lifetime = 24h
    renew_lifetime = 7d
    forwardable = true

[realms]
    EXAMPLE.COM = {
        kdc = kerberos.example.com
        admin_server = kerberos.example.com
    }

[domain_realm]
    .example.com = EXAMPLE.COM
    example.com = EXAMPLE.COM
```

```bash
# Obtenir un ticket
kinit user@EXAMPLE.COM

# Vérifier le ticket
klist

# /etc/ssh/sshd_config
GSSAPIAuthentication yes
GSSAPICleanupCredentials yes

sudo systemctl restart ssh

# Se connecter
ssh -K user@server.example.com
# -K forward Kerberos credentials
```

## PAM (Pluggable Authentication Modules)

```bash
# Configuration PAM pour SSH
sudo nano /etc/pam.d/sshd
```

```conf
# Standard Unix authentication
@include common-auth
@include common-account
@include common-session
@include common-password

# Google Authenticator (2FA)
auth required pam_google_authenticator.so

# Fail2ban
auth required pam_abl.so config=/etc/security/pam_abl.conf

# Time restrictions
account required pam_time.so

# Environment variables
session required pam_env.so

# Limits
session required pam_limits.so
```

### Restrictions horaires

```bash
# /etc/security/time.conf
# Format: services;ttys;users;times
# times: Wk0800-1800 (weekdays 8-18h)

# SSH seulement pendant les heures de bureau
sshd;*;*;Wk0800-1800

# Admin seulement la nuit
sshd;*;admin;!Wk0800-1800

# User limité au weekend
sshd;*;backup;Sa-Su
```

## Authentification basée sur l'IP

```bash
# /etc/ssh/sshd_config

# Autoriser depuis certaines IPs seulement
Match User admin Address 192.168.1.0/24,10.0.0.0/8
    PasswordAuthentication yes
    PubkeyAuthentication yes

Match User admin Address !192.168.1.0/24,!10.0.0.0/8
    DenyUsers admin

# Par utilisateur et IP
Match User deploy Address 192.168.1.100
    PubkeyAuthentication yes
    ForceCommand /usr/local/bin/deploy.sh

# Bastion host requis pour autres
Match Address *,!192.168.1.0/24
    ProxyJump bastion.example.com
```

## Port Knocking

```bash
# Installer knockd
sudo apt install knockd

# Configuration
sudo nano /etc/knockd.conf
```

```ini
[options]
    UseSyslog

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
```

```bash
# Démarrer knockd
sudo systemctl start knockd
sudo systemctl enable knockd

# Côté client, frapper aux ports
knock server.example.com 7000 8000 9000
ssh user@server.example.com

# Fermer après
knock server.example.com 9000 8000 7000
```

## Single Sign-On (SSO) avec OAuth

```bash
# Utiliser pam-oauth2
git clone https://github.com/CyberDem0n/pam-oauth2-device.git
cd pam-oauth2-device
make
sudo make install

# Configuration
sudo nano /etc/pam.d/sshd
auth sufficient pam_oauth2_device.so client_id=xxx token_endpoint=https://oauth.example.com/token
```

## Authentification avec JWT

```bash
# Script custom d'authentification
# /usr/local/bin/ssh-jwt-auth
```

```python
#!/usr/bin/env python3
import jwt
import sys

def verify_jwt(token):
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return payload.get('username')
    except:
        return None

if __name__ == '__main__':
    token = sys.argv[1]
    username = verify_jwt(token)
    if username:
        print(f"Authorized: {username}")
        sys.exit(0)
    else:
        sys.exit(1)
```

```bash
# /etc/ssh/sshd_config
AuthorizedKeysCommand /usr/local/bin/ssh-jwt-auth %u
AuthorizedKeysCommandUser nobody
```

## Rate Limiting

```bash
# fail2ban
sudo apt install fail2ban

# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600

sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Vérifier les bans
sudo fail2ban-client status sshd

# Débanner une IP
sudo fail2ban-client set sshd unbanip 192.168.1.100
```

## Logs et audit

```bash
# Activer logs détaillés
# /etc/ssh/sshd_config
LogLevel VERBOSE
SyslogFacility AUTH

# Analyser les tentatives de connexion
sudo grep "Failed password" /var/log/auth.log
sudo grep "Accepted publickey" /var/log/auth.log

# IPs avec échecs multiples
sudo grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr

# Connexions réussies
sudo last | grep still
sudo w
```

[← Clés SSH](./infos-ssh-03-cles-ssh.md) | [Index](./infos-ssh-00-index.md) | [Tunneling →](./infos-ssh-05-tunneling.md)

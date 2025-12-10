# 🔑 Clés SSH

[← Configuration](./infos-ssh-02-configuration.md) | [Index](./infos-ssh-00-index.md) | [Authentification avancée →](./infos-ssh-04-authentification-avancee.md)

## Types de clés SSH

```bash
# RSA (classique, bien supporté)
ssh-keygen -t rsa -b 4096
# Taille recommandée: 4096 bits minimum

# Ed25519 (recommandé, moderne, rapide, sécurisé)
ssh-keygen -t ed25519
# Toujours 256 bits, très sécurisé

# ECDSA (courbes elliptiques)
ssh-keygen -t ecdsa -b 521
# Tailles: 256, 384, 521 bits

# DSA (obsolète, ne pas utiliser)
# Déprécié depuis OpenSSH 7.0
```

## Générer des clés

```bash
# Clé Ed25519 (recommandé)
ssh-keygen -t ed25519 -C "user@email.com"

# Clé RSA 4096 bits
ssh-keygen -t rsa -b 4096 -C "user@email.com"

# Avec nom de fichier personnalisé
ssh-keygen -t ed25519 -f ~/.ssh/myproject_key -C "project key"

# Sans passphrase (déconseillé en prod)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519

# Avec passphrase spécifique
ssh-keygen -t ed25519 -N "my-passphrase" -f ~/.ssh/id_ed25519

# Générer plusieurs clés
ssh-keygen -t ed25519 -f ~/.ssh/github_key -C "github"
ssh-keygen -t ed25519 -f ~/.ssh/gitlab_key -C "gitlab"
ssh-keygen -t ed25519 -f ~/.ssh/prod_key -C "production"
```

## Structure des fichiers de clés

```bash
# Clé privée (garder secrète!)
~/.ssh/id_ed25519
~/.ssh/id_rsa

# Clé publique (partager librement)
~/.ssh/id_ed25519.pub
~/.ssh/id_rsa.pub

# Format clé publique
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbcdef123... user@email.com

# Format clé privée (ne jamais partager)
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
...
-----END OPENSSH PRIVATE KEY-----
```

## Permissions des clés

```bash
# Permissions correctes (très important!)
chmod 700 ~/.ssh                    # Répertoire
chmod 600 ~/.ssh/id_ed25519        # Clé privée
chmod 644 ~/.ssh/id_ed25519.pub    # Clé publique
chmod 600 ~/.ssh/authorized_keys   # Clés autorisées
chmod 600 ~/.ssh/config            # Configuration

# Vérifier les permissions
ls -la ~/.ssh

# Corriger automatiquement
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
chmod 644 ~/.ssh/*.pub
```

## Copier la clé publique vers un serveur

```bash
# Méthode 1: ssh-copy-id (recommandé)
ssh-copy-id user@server

# Avec clé spécifique
ssh-copy-id -i ~/.ssh/mykey.pub user@server

# Avec port personnalisé
ssh-copy-id -p 2222 user@server

# Méthode 2: Manuelle
cat ~/.ssh/id_ed25519.pub | ssh user@server 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'

# Méthode 3: Via SCP
scp ~/.ssh/id_ed25519.pub user@server:/tmp/
ssh user@server
mkdir -p ~/.ssh
cat /tmp/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
rm /tmp/id_ed25519.pub

# Méthode 4: Copy-paste manuel
cat ~/.ssh/id_ed25519.pub
# Copier le contenu
ssh user@server
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
# Coller la clé publique
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

## authorized_keys

```bash
# ~/.ssh/authorized_keys - Clés autorisées sur le serveur

# Clé simple
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbcdef123... user@laptop

# Clé avec options
command="/usr/bin/backup" ssh-ed25519 AAAAC3Nz... backup@server

# Restreindre par IP
from="192.168.1.0/24" ssh-ed25519 AAAAC3Nz... admin@office

# Plusieurs restrictions
command="/usr/bin/backup",no-port-forwarding,no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3Nz... backup

# Options disponibles:
# command="cmd"                 Force l'exécution de cette commande
# from="pattern"                Restreint par IP/hostname
# no-port-forwarding            Désactive port forwarding
# no-X11-forwarding             Désactive X11 forwarding
# no-agent-forwarding           Désactive agent forwarding
# no-pty                        Désactive allocation de terminal
# no-user-rc                    Désactive ~/.ssh/rc
# environment="NAME=value"      Définit une variable d'environnement
```

```bash
# Exemples pratiques

# Utilisateur backup (script seulement)
command="/usr/local/bin/backup.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-ed25519 AAAAC3... backup@server

# Admin depuis le bureau seulement
from="192.168.1.100" ssh-ed25519 AAAAC3... admin@office

# Deploy avec forwarding
no-X11-forwarding,no-agent-forwarding ssh-ed25519 AAAAC3... deploy@ci

# Read-only SFTP
command="internal-sftp -R" ssh-ed25519 AAAAC3... readonly@client
```

## Gérer les clés avec ssh-agent

```bash
# Démarrer ssh-agent
eval $(ssh-agent)

# Ajouter une clé
ssh-add ~/.ssh/id_ed25519
# Entre la passphrase

# Ajouter toutes les clés par défaut
ssh-add

# Ajouter avec timeout (1 heure)
ssh-add -t 3600 ~/.ssh/id_ed25519

# Lister les clés chargées
ssh-add -l

# Afficher les clés publiques chargées
ssh-add -L

# Supprimer une clé
ssh-add -d ~/.ssh/id_ed25519

# Supprimer toutes les clés
ssh-add -D

# Tuer l'agent
ssh-agent -k

# Agent au démarrage (ajouter dans ~/.bashrc ou ~/.zshrc)
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval $(ssh-agent)
    ssh-add ~/.ssh/id_ed25519
fi
```

## ssh-agent avec systemd

```bash
# ~/.config/systemd/user/ssh-agent.service
[Unit]
Description=SSH key agent

[Service]
Type=simple
Environment=SSH_AUTH_SOCK=%t/ssh-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a $SSH_AUTH_SOCK

[Install]
WantedBy=default.target

# Activer
systemctl --user enable ssh-agent
systemctl --user start ssh-agent

# Ajouter dans ~/.bashrc
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"
```

## Gérer plusieurs clés

```bash
# ~/.ssh/config

# GitHub
Host github.com
    User git
    IdentityFile ~/.ssh/github_key

# GitLab
Host gitlab.com
    User git
    IdentityFile ~/.ssh/gitlab_key

# Production
Host prod*.example.com
    User admin
    IdentityFile ~/.ssh/prod_key

# Development
Host dev*.example.com
    User developer
    IdentityFile ~/.ssh/dev_key

# Work
Host *.work.com
    User employee
    IdentityFile ~/.ssh/work_key

# Personal projects
Host personal
    HostName 192.168.1.100
    User me
    IdentityFile ~/.ssh/personal_key
```

## Convertir des clés

```bash
# PuTTY (Windows) vers OpenSSH
puttygen privatekey.ppk -O private-openssh -o id_rsa

# OpenSSH vers PuTTY
puttygen id_rsa -o privatekey.ppk

# Extraire la clé publique d'une clé privée
ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub

# Changer le format de la clé (OpenSSH vers RFC4716)
ssh-keygen -e -f ~/.ssh/id_rsa.pub > id_rsa_rfc4716.pub

# Convertir de RFC4716 vers OpenSSH
ssh-keygen -i -f id_rsa_rfc4716.pub > id_rsa_openssh.pub
```

## Afficher les informations d'une clé

```bash
# Empreinte (fingerprint)
ssh-keygen -lf ~/.ssh/id_ed25519
ssh-keygen -lf ~/.ssh/id_ed25519.pub

# Avec hash MD5
ssh-keygen -l -E md5 -f ~/.ssh/id_ed25519

# Avec hash SHA256 (par défaut)
ssh-keygen -l -E sha256 -f ~/.ssh/id_ed25519

# Visual fingerprint (ASCII art)
ssh-keygen -lvf ~/.ssh/id_ed25519

# Type de clé et bits
ssh-keygen -lf ~/.ssh/id_ed25519
# Output: 256 SHA256:abcdef... user@email.com (ED25519)

# Vérifier qu'une clé publique correspond à une clé privée
ssh-keygen -y -f ~/.ssh/id_ed25519 | diff - ~/.ssh/id_ed25519.pub
# Pas de sortie = elles correspondent
```

## Changer la passphrase

```bash
# Changer la passphrase d'une clé
ssh-keygen -p -f ~/.ssh/id_ed25519

# Ajouter une passphrase (si la clé n'en a pas)
ssh-keygen -p -f ~/.ssh/id_ed25519

# Supprimer la passphrase (déconseillé)
ssh-keygen -p -N "" -f ~/.ssh/id_ed25519

# Changer avec nouvelle passphrase directement
ssh-keygen -p -P "old-passphrase" -N "new-passphrase" -f ~/.ssh/id_ed25519
```

## Certificats SSH

```bash
# Créer une CA (Certificate Authority)
ssh-keygen -t ed25519 -f ssh_ca -C "SSH CA"

# Signer une clé utilisateur (créer un certificat)
ssh-keygen -s ssh_ca -I user_id -n username -V +52w ~/.ssh/id_ed25519.pub
# Crée: ~/.ssh/id_ed25519-cert.pub

# Options du certificat:
# -I : Identity (nom unique)
# -n : Principals (utilisateurs autorisés)
# -V : Validity (+52w = 52 semaines)
# -z : Serial number
# -O : Options (source-address, force-command, etc.)

# Configurer le serveur pour accepter la CA
# /etc/ssh/sshd_config
TrustedUserCAKeys /etc/ssh/ssh_ca.pub

# Copier la CA publique sur le serveur
sudo cp ssh_ca.pub /etc/ssh/ssh_ca.pub

# Vérifier un certificat
ssh-keygen -Lf ~/.ssh/id_ed25519-cert.pub

# Se connecter avec le certificat
ssh user@server
# Le certificat est automatiquement utilisé
```

## Sécurité des clés

```bash
# ✅ Bonnes pratiques:
# 1. Toujours utiliser une passphrase forte
# 2. Permissions 600 sur les clés privées
# 3. Ne jamais partager la clé privée
# 4. Utiliser ssh-agent pour ne pas retaper la passphrase
# 5. Utiliser des clés différentes par projet/serveur
# 6. Rotation régulière des clés
# 7. Révoquer les anciennes clés

# ❌ À éviter:
# - Clés sans passphrase (sauf scripts automatisés sécurisés)
# - Réutiliser la même clé partout
# - Stocker les clés dans le cloud non chiffré
# - Permissions trop ouvertes (644, 777, etc.)
```

## Révocation de clés

```bash
# Sur le serveur, supprimer la clé du authorized_keys
ssh user@server
nano ~/.ssh/authorized_keys
# Supprimer la ligne correspondante

# Ou automatiquement
ssh user@server "sed -i '/specific-key-content/d' ~/.ssh/authorized_keys"

# Si la clé est compromise:
# 1. La supprimer immédiatement de tous les serveurs
# 2. Générer une nouvelle clé
# 3. Distribuer la nouvelle clé
# 4. Vérifier les logs pour toute activité suspecte
```

## Backup des clés

```bash
#!/bin/bash
# backup_ssh_keys.sh

BACKUP_DIR="$HOME/backup/ssh_keys"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup des clés privées (ATTENTION: sécuriser ce backup!)
tar czf "$BACKUP_DIR/ssh_keys_$DATE.tar.gz" \
    --exclude="*.pub" \
    --exclude="known_hosts*" \
    --exclude="authorized_keys*" \
    ~/.ssh/

# Chiffrer le backup (recommandé)
gpg --symmetric --cipher-algo AES256 "$BACKUP_DIR/ssh_keys_$DATE.tar.gz"
rm "$BACKUP_DIR/ssh_keys_$DATE.tar.gz"

# Ou avec age (moderne)
age -p -o "$BACKUP_DIR/ssh_keys_$DATE.tar.gz.age" "$BACKUP_DIR/ssh_keys_$DATE.tar.gz"

echo "✅ Backup chiffré: $BACKUP_DIR/ssh_keys_$DATE.tar.gz.gpg"
```

## Troubleshooting

```bash
# Permission denied (publickey)
# Vérifier les permissions
ls -la ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

# Côté serveur
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Vérifier que la clé est dans authorized_keys
ssh user@server 'cat ~/.ssh/authorized_keys' | grep -f ~/.ssh/id_ed25519.pub

# Test verbeux
ssh -vvv user@server

# La clé n'est pas acceptée
# Vérifier les algorithmes autorisés côté serveur
# /etc/ssh/sshd_config
PubkeyAcceptedKeyTypes +ssh-rsa

# Agent doesn't have the key
ssh-add -l
ssh-add ~/.ssh/id_ed25519

# Too many authentication failures
# Limiter les clés essayées
ssh -o IdentitiesOnly=yes -i ~/.ssh/specific_key user@server

# Ou dans ~/.ssh/config
Host server
    IdentitiesOnly yes
    IdentityFile ~/.ssh/specific_key
```

[← Configuration](./infos-ssh-02-configuration.md) | [Index](./infos-ssh-00-index.md) | [Authentification avancée →](./infos-ssh-04-authentification-avancee.md)

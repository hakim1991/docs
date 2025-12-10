# 🚀 Introduction et Installation SSH

[Index](./infos-ssh-00-index.md) | [Configuration →](./infos-ssh-02-configuration.md)

## Qu'est-ce que SSH ?

**SSH (Secure Shell)** est un protocole réseau cryptographique permettant de se connecter à distance de manière sécurisée à un serveur.

### Caractéristiques principales

```
✅ Connexion sécurisée et chiffrée
✅ Authentification par mot de passe ou clé
✅ Transfert de fichiers (SCP, SFTP)
✅ Tunneling et port forwarding
✅ Proxy SOCKS
✅ Exécution de commandes à distance
✅ Standard de l'industrie
```

## Installation sur Linux

### Ubuntu / Debian

```bash
# Installer le client SSH (souvent déjà installé)
sudo apt update
sudo apt install openssh-client

# Installer le serveur SSH
sudo apt install openssh-server

# Vérifier l'installation
ssh -V

# Démarrer le service
sudo systemctl start ssh
sudo systemctl enable ssh

# Vérifier le statut
sudo systemctl status ssh
```

### CentOS / RHEL / Fedora

```bash
# Installer client et serveur
sudo yum install openssh-clients openssh-server

# Ou avec dnf
sudo dnf install openssh-clients openssh-server

# Démarrer et activer
sudo systemctl start sshd
sudo systemctl enable sshd

# Statut
sudo systemctl status sshd
```

### Arch Linux

```bash
# Installer
sudo pacman -S openssh

# Démarrer
sudo systemctl start sshd
sudo systemctl enable sshd
```

## Installation sur Windows

### Windows 10/11 (OpenSSH intégré)

```powershell
# Vérifier si déjà installé
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'

# Installer le client
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Installer le serveur
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Démarrer le service
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Vérifier
ssh -V
```

### PuTTY (alternative Windows)

```powershell
# Avec Chocolatey
choco install putty

# Ou télécharger depuis
# https://www.putty.org/
```

## Installation sur macOS

```bash
# Client SSH (déjà installé)
ssh -V

# Activer le serveur SSH (Remote Login)
sudo systemsetup -setremotelogin on

# Vérifier
sudo systemsetup -getremotelogin

# Désactiver
sudo systemsetup -setremotelogin off
```

## Configuration firewall

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow ssh
sudo ufw allow 22/tcp
sudo ufw enable
sudo ufw status

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-all

# iptables (méthode manuelle)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables-save > /etc/iptables/rules.v4
```

## Première connexion

```bash
# Connexion simple
ssh user@hostname

# Avec adresse IP
ssh user@192.168.1.100

# Spécifier le port
ssh -p 2222 user@hostname

# Avec clé spécifique
ssh -i ~/.ssh/mykey user@hostname

# Mode verbose (debug)
ssh -v user@hostname
ssh -vv user@hostname    # Plus de détails
ssh -vvv user@hostname   # Maximum de détails

# Connexion et exécuter une commande
ssh user@hostname 'ls -la'
ssh user@hostname 'uptime && df -h'
```

## Variables d'environnement

```bash
# Variables SSH utiles
export SSH_AUTH_SOCK=$SSH_AUTH_SOCK    # Socket ssh-agent
export SSH_AGENT_PID=$SSH_AGENT_PID    # PID ssh-agent

# Voir les variables SSH actives
env | grep SSH
```

## Commandes de base

```bash
# Se connecter
ssh user@server

# Copier un fichier (SCP)
scp file.txt user@server:/path/to/destination
scp user@server:/path/to/file.txt .

# Copier un répertoire
scp -r folder/ user@server:/path/

# SFTP (transfert interactif)
sftp user@server
# Commandes SFTP: get, put, ls, cd, lcd, pwd, lpwd, exit

# Rsync via SSH
rsync -avz -e ssh folder/ user@server:/backup/

# Exécuter une commande
ssh user@server 'command'

# Session avec pseudo-terminal
ssh -t user@server 'sudo command'
```

## Fichiers de configuration

```bash
# Fichiers client
~/.ssh/config              # Configuration utilisateur
~/.ssh/known_hosts         # Empreintes des serveurs
~/.ssh/id_rsa             # Clé privée par défaut
~/.ssh/id_rsa.pub         # Clé publique
~/.ssh/authorized_keys     # Clés autorisées (serveur)

# Fichiers serveur
/etc/ssh/sshd_config      # Configuration serveur
/etc/ssh/ssh_config       # Configuration client globale
/etc/ssh/ssh_host_*       # Clés du serveur
```

## Vérifier le service SSH

```bash
# Statut du service
sudo systemctl status ssh
sudo systemctl status sshd

# Redémarrer
sudo systemctl restart ssh

# Recharger la config sans interrompre les connexions
sudo systemctl reload ssh

# Logs
sudo tail -f /var/log/auth.log          # Ubuntu/Debian
sudo tail -f /var/log/secure            # CentOS/RHEL
sudo journalctl -u ssh -f               # systemd

# Port d'écoute
sudo netstat -tulpn | grep :22
sudo ss -tulpn | grep :22
sudo lsof -i :22

# Connexions actives
who
w
last

# Dernières connexions
lastlog
last -a
```

## Générer des clés SSH

```bash
# Générer une clé RSA (par défaut)
ssh-keygen

# Clé RSA avec taille spécifique
ssh-keygen -t rsa -b 4096

# Clé Ed25519 (recommandé, plus sécurisé)
ssh-keygen -t ed25519

# Avec commentaire
ssh-keygen -t ed25519 -C "user@email.com"

# Spécifier le fichier
ssh-keygen -t ed25519 -f ~/.ssh/mykey

# Sans passphrase (pas recommandé en prod)
ssh-keygen -t ed25519 -N ""

# Afficher l'empreinte d'une clé
ssh-keygen -lf ~/.ssh/id_rsa.pub

# Changer la passphrase
ssh-keygen -p -f ~/.ssh/id_rsa
```

## Copier la clé publique vers un serveur

```bash
# Méthode automatique (recommandé)
ssh-copy-id user@server

# Avec clé spécifique
ssh-copy-id -i ~/.ssh/mykey.pub user@server

# Avec port personnalisé
ssh-copy-id -p 2222 user@server

# Méthode manuelle
cat ~/.ssh/id_rsa.pub | ssh user@server 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'

# Ou avec scp
scp ~/.ssh/id_rsa.pub user@server:/tmp/
ssh user@server 'mkdir -p ~/.ssh && cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys && rm /tmp/id_rsa.pub'

# Vérifier les permissions
ssh user@server 'chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'
```

## Tester la connexion

```bash
# Test basique
ssh -T user@server

# Test avec verbosité
ssh -vT user@server

# Test de connexion sans exécuter de commande
ssh -q user@server exit
echo $?  # 0 si succès

# Vérifier l'authentification par clé
ssh -o PreferredAuthentications=publickey user@server
```

## SSH Agent

```bash
# Démarrer ssh-agent
eval $(ssh-agent)

# Ajouter une clé
ssh-add ~/.ssh/id_rsa

# Ajouter toutes les clés par défaut
ssh-add

# Lister les clés chargées
ssh-add -l

# Supprimer toutes les clés
ssh-add -D

# Supprimer une clé spécifique
ssh-add -d ~/.ssh/id_rsa

# Tuer l'agent
ssh-agent -k
```

## Configuration ~/.ssh/config

```bash
# ~/.ssh/config

# Serveur de production
Host prod
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/prod_key

# Serveur de développement
Host dev
    HostName dev.example.com
    User developer
    IdentityFile ~/.ssh/dev_key
    ForwardAgent yes

# Tous les serveurs *.example.com
Host *.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/company_key

# Utilisation
# Connexion simplifiée
ssh prod
ssh dev
```

## Troubleshooting installation

```bash
# SSH ne démarre pas
sudo systemctl status ssh
sudo journalctl -u ssh -n 50

# Vérifier la configuration
sudo sshd -t
sudo sshd -T  # Afficher la config complète

# Permission denied (publickey)
# Vérifier les permissions
ls -la ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys

# Connexion refuse
# Vérifier le firewall
sudo ufw status
sudo iptables -L -n | grep 22

# Port déjà utilisé
sudo lsof -i :22
sudo netstat -tulpn | grep :22

# Logs d'erreur
sudo tail -f /var/log/auth.log | grep ssh
```

## Sécurité de base

```bash
# Désactiver l'authentification par mot de passe
# Dans /etc/ssh/sshd_config:
PasswordAuthentication no

# Désactiver root login
PermitRootLogin no

# Changer le port par défaut
Port 2222

# Redémarrer après modifications
sudo systemctl restart ssh
```

## Vérification post-installation

```bash
# Checklist installation
echo "✅ Vérification SSH"

# 1. Service actif
systemctl is-active ssh && echo "✅ Service démarré" || echo "❌ Service arrêté"

# 2. Port ouvert
sudo ss -tulpn | grep -q :22 && echo "✅ Port 22 ouvert" || echo "❌ Port 22 fermé"

# 3. Clés générées
[ -f ~/.ssh/id_rsa ] && echo "✅ Clé RSA existe" || echo "⚠️  Pas de clé RSA"
[ -f ~/.ssh/id_ed25519 ] && echo "✅ Clé Ed25519 existe" || echo "⚠️  Pas de clé Ed25519"

# 4. Config accessible
[ -f ~/.ssh/config ] && echo "✅ Config existe" || echo "ℹ️  Pas de config"

# 5. Agent actif
pgrep ssh-agent > /dev/null && echo "✅ Agent actif" || echo "ℹ️  Agent non actif"
```

## Commandes utiles

```bash
# Version OpenSSH
ssh -V

# Configuration serveur
sudo sshd -T

# Tester la config serveur
sudo sshd -t

# Voir les algorithmes supportés
ssh -Q cipher
ssh -Q mac
ssh -Q kex
ssh -Q key

# Benchmark
ssh -o Compression=yes user@server 'dd if=/dev/zero bs=1M count=100' | dd of=/dev/null
```

[Index](./infos-ssh-00-index.md) | [Configuration →](./infos-ssh-02-configuration.md)

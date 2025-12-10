# 📚 SSH - Documentation Complète

## Table des matières

### 🚀 Bases
1. [Introduction et Installation](./infos-ssh-01-introduction-installation.md)
   - Qu'est-ce que SSH ?
   - Installation Linux / Windows
   - Première connexion
   - Commandes de base

2. [Configuration](./infos-ssh-02-configuration.md)
   - Fichiers de configuration
   - ssh_config (client)
   - sshd_config (serveur)
   - Options importantes

### 🔑 Authentification
3. [Clés SSH](./infos-ssh-03-cles-ssh.md)
   - Génération de clés
   - Types de clés (RSA, Ed25519)
   - Clés publiques/privées
   - ssh-agent
   - Passphrases

4. [Authentification avancée](./infos-ssh-04-authentification-avancee.md)
   - Authentification par clés
   - Authentification multi-facteur
   - Certificats SSH
   - LDAP/Active Directory

### 🔄 Tunneling et Port Forwarding
5. [Tunneling SSH](./infos-ssh-05-tunneling.md)
   - Port forwarding local
   - Port forwarding distant
   - Port forwarding dynamique (SOCKS)
   - Tunneling inversé

6. [Transfert de fichiers](./infos-ssh-06-transfert-fichiers.md)
   - scp
   - sftp
   - rsync over SSH
   - Best practices

### 🔒 Sécurité
7. [Sécurisation SSH](./infos-ssh-07-securisation.md)
   - Désactiver root login
   - Changer le port
   - Fail2ban
   - Authentification par clés uniquement
   - Best practices sécurité

8. [Hardening SSH](./infos-ssh-08-hardening.md)
   - Algorithmes de chiffrement
   - Configuration avancée
   - Auditing
   - Compliance

### 🔧 Avancé
9. [SSH Avancé](./infos-ssh-09-avance.md)
   - Multiplexing
   - ProxyJump et ProxyCommand
   - SSH over HTTPS
   - Bastions et jump hosts

10. [Automatisation](./infos-ssh-10-automatisation.md)
    - Scripts SSH
    - Ansible
    - SSH dans CI/CD
    - Configuration Management

11. [Troubleshooting](./infos-ssh-11-troubleshooting.md)
    - Problèmes courants
    - Debug SSH
    - Connection refused
    - Permission denied
    - Timeout issues

---

## 🎯 Commandes rapides

```bash
# Connexion
ssh user@host
ssh -i key.pem user@host
ssh -p 2222 user@host

# Génération de clés
ssh-keygen -t ed25519 -C "email@example.com"
ssh-keygen -t rsa -b 4096

# Copie de clé publique
ssh-copy-id user@host
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host

# Port forwarding
ssh -L 8080:localhost:80 user@host     # Local
ssh -R 8080:localhost:80 user@host     # Remote
ssh -D 1080 user@host                  # Dynamic (SOCKS)

# Transfert de fichiers
scp file.txt user@host:/path/
scp -r folder/ user@host:/path/
rsync -avz folder/ user@host:/path/

# Agent SSH
eval $(ssh-agent)
ssh-add ~/.ssh/id_ed25519

# Tests
ssh -v user@host         # Verbose
ssh -vv user@host        # More verbose
ssh -vvv user@host       # Most verbose
```

## 📖 Structure de la documentation

Chaque chapitre contient:
- ✅ Explications détaillées
- ✅ Exemples de configuration
- ✅ Cas d'usage pratiques
- ✅ Best practices sécurité
- ✅ Troubleshooting

---

## 🔗 Ressources

- [OpenSSH Documentation](https://www.openssh.com/manual.html)
- [SSH.com](https://www.ssh.com/)
- [GitHub SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**Prêt à commencer ?** → [Introduction et Installation](./infos-ssh-01-introduction-installation.md)

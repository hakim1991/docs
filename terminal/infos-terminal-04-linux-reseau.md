# 🌐 Réseau et Sécurité Linux

[← Filesystem](./infos-terminal-03-linux-filesystem.md) | [Index](./infos-terminal-00-index.md) | [Processus →](./infos-terminal-05-linux-processus.md)

## Configuration réseau

### ip (iproute2)

Gestion réseau moderne.

```bash
# Afficher toutes les interfaces
ip addr
ip a

# Interface spécifique
ip addr show eth0

# Ajouter IP
sudo ip addr add 192.168.1.100/24 dev eth0

# Supprimer IP
sudo ip addr del 192.168.1.100/24 dev eth0

# Activer interface
sudo ip link set eth0 up

# Désactiver interface
sudo ip link set eth0 down

# Afficher routes
ip route
ip r

# Ajouter route
sudo ip route add 192.168.2.0/24 via 192.168.1.1

# Route par défaut
sudo ip route add default via 192.168.1.1

# Supprimer route
sudo ip route del 192.168.2.0/24

# Statistiques
ip -s link
```

### ifconfig (obsolète mais encore utilisé)

```bash
# Afficher interfaces
ifconfig

# Interface spécifique
ifconfig eth0

# Configurer IP
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# Activer/désactiver
sudo ifconfig eth0 up
sudo ifconfig eth0 down
```

### nmcli (NetworkManager)

Gestion réseau simplifié.

```bash
# Statut général
nmcli general status

# Lister connexions
nmcli connection show

# Lister devices
nmcli device status

# Connecter WiFi
nmcli device wifi list
nmcli device wifi connect SSID password PASSWORD

# Créer connexion
nmcli connection add type ethernet con-name my-eth ifname eth0

# Modifier connexion
nmcli connection modify my-eth ipv4.addresses 192.168.1.100/24
nmcli connection modify my-eth ipv4.gateway 192.168.1.1
nmcli connection modify my-eth ipv4.dns "8.8.8.8 8.8.4.4"
nmcli connection modify my-eth ipv4.method manual

# Activer connexion
nmcli connection up my-eth

# Désactiver connexion
nmcli connection down my-eth
```

### Configuration fichiers

```bash
# Netplan (Ubuntu 18.04+)
sudo nano /etc/netplan/01-netcfg.yaml

# network:
#   version: 2
#   ethernets:
#     eth0:
#       dhcp4: false
#       addresses: [192.168.1.100/24]
#       gateway4: 192.168.1.1
#       nameservers:
#         addresses: [8.8.8.8, 8.8.4.4]

# Appliquer
sudo netplan apply

# interfaces (Debian/Ubuntu ancien)
sudo nano /etc/network/interfaces

# auto eth0
# iface eth0 inet static
#   address 192.168.1.100
#   netmask 255.255.255.0
#   gateway 192.168.1.1

# Redémarrer réseau
sudo systemctl restart networking
```

## DNS

### Configuration DNS

```bash
# Fichier resolv.conf
cat /etc/resolv.conf
# nameserver 8.8.8.8
# nameserver 1.1.1.1

# Éditer (temporaire)
sudo nano /etc/resolv.conf

# Permanent avec systemd-resolved
sudo nano /etc/systemd/resolved.conf
```

### nslookup

Requête DNS.

```bash
# Lookup simple
nslookup google.com

# Serveur DNS spécifique
nslookup google.com 8.8.8.8

# Record MX
nslookup -type=MX google.com

# Record NS
nslookup -type=NS google.com
```

### dig

DNS lookup détaillé.

```bash
# Lookup
dig google.com

# Short
dig google.com +short

# Serveur DNS spécifique
dig @8.8.8.8 google.com

# Record type
dig google.com MX
dig google.com NS
dig google.com AAAA

# Reverse lookup
dig -x 8.8.8.8

# Trace DNS
dig google.com +trace
```

### host

Simple DNS lookup.

```bash
# Lookup
host google.com

# Reverse
host 8.8.8.8

# Type record
host -t MX google.com
```

## Diagnostics réseau

### ping

Test connectivité.

```bash
# Ping
ping google.com

# Nombre de paquets
ping -c 5 google.com

# Intervalle
ping -i 0.5 google.com

# Taille paquet
ping -s 1000 google.com

# IPv4/IPv6
ping -4 google.com
ping -6 google.com

# Flood ping (root)
sudo ping -f google.com
```

### traceroute / tracepath

Tracer route.

```bash
# Traceroute (à installer)
traceroute google.com

# Tracepath (intégré)
tracepath google.com

# Avec numéros de port
traceroute -p 80 google.com

# IPv6
traceroute6 google.com
```

### mtr

Traceroute + ping combiné.

```bash
# Installer
sudo apt install mtr

# Lancer
mtr google.com

# Mode rapport
mtr --report google.com

# Nombre de cycles
mtr --report-cycles 10 google.com
```

### netstat

Statistiques réseau (obsolète).

```bash
# Connexions actives
netstat -tuln

# Avec processus
sudo netstat -tulnp

# Ports en écoute
netstat -tuln | grep LISTEN

# Routes
netstat -r

# Interfaces
netstat -i

# Statistiques
netstat -s

# Options:
# t = TCP
# u = UDP
# l = listening
# n = numérique (pas de résolution DNS)
# p = processus
```

### ss

Socket statistics (remplace netstat).

```bash
# Toutes les connexions
ss -tuln

# Avec processus
sudo ss -tulnp

# Ports en écoute
ss -tuln | grep LISTEN

# Connexions établies
ss -o state established

# Connexions TCP
ss -t

# Connexions UDP
ss -u

# Statistiques
ss -s

# Filtrer par port
ss -tuln sport = :80
ss -tuln dport = :443
```

### lsof

List open files (inclut sockets).

```bash
# Installer
sudo apt install lsof

# Processus utilisant port
sudo lsof -i :80
sudo lsof -i :443

# Tous les ports en écoute
sudo lsof -i -P | grep LISTEN

# Par utilisateur
lsof -u username

# Par processus
lsof -c nginx

# Fichiers ouverts
lsof /path/to/file
```

### tcpdump

Capture de paquets.

```bash
# Installer
sudo apt install tcpdump

# Capturer interface
sudo tcpdump -i eth0

# Capturer et sauvegarder
sudo tcpdump -i eth0 -w capture.pcap

# Lire capture
tcpdump -r capture.pcap

# Filtrer par port
sudo tcpdump -i eth0 port 80

# Filtrer par host
sudo tcpdump -i eth0 host 192.168.1.100

# HTTP traffic
sudo tcpdump -i eth0 'tcp port 80'

# DNS traffic
sudo tcpdump -i eth0 'udp port 53'

# Verbose
sudo tcpdump -i eth0 -v
sudo tcpdump -i eth0 -vv
```

### wireshark / tshark

Analyseur de paquets GUI/CLI.

```bash
# Installer
sudo apt install wireshark tshark

# Capture avec tshark
sudo tshark -i eth0

# Sauvegarder
sudo tshark -i eth0 -w capture.pcap

# Lire
tshark -r capture.pcap

# Filtres
tshark -i eth0 -f "port 80"
tshark -r capture.pcap -Y "http"
```

## Firewall

### iptables

Firewall Linux.

```bash
# Lister règles
sudo iptables -L
sudo iptables -L -v -n

# Accepter tout (ATTENTION!)
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT

# Bloquer tout (par défaut)
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Autoriser SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Autoriser HTTP/HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Autoriser loopback
sudo iptables -A INPUT -i lo -j ACCEPT

# Autoriser connexions établies
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Supprimer règle
sudo iptables -D INPUT 3

# Vider toutes les règles
sudo iptables -F

# Sauvegarder
sudo iptables-save > /etc/iptables/rules.v4

# Restaurer
sudo iptables-restore < /etc/iptables/rules.v4
```

### ufw (Uncomplicated Firewall)

Firewall simplifié.

```bash
# Installer
sudo apt install ufw

# Activer
sudo ufw enable

# Désactiver
sudo ufw disable

# Statut
sudo ufw status
sudo ufw status verbose

# Autoriser port
sudo ufw allow 22
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Autoriser service
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# Autoriser depuis IP
sudo ufw allow from 192.168.1.100

# Autoriser subnet vers port
sudo ufw allow from 192.168.1.0/24 to any port 22

# Refuser
sudo ufw deny 23

# Supprimer règle
sudo ufw delete allow 80

# Réinitialiser
sudo ufw reset

# Règles par défaut
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### firewalld

Firewall dynamique (RedHat/CentOS).

```bash
# Statut
sudo firewall-cmd --state

# Zones
sudo firewall-cmd --get-zones
sudo firewall-cmd --get-active-zones

# Services
sudo firewall-cmd --list-services

# Autoriser service
sudo firewall-cmd --add-service=http
sudo firewall-cmd --add-service=https

# Permanent
sudo firewall-cmd --permanent --add-service=http

# Port
sudo firewall-cmd --add-port=8080/tcp

# Recharger
sudo firewall-cmd --reload
```

## SSH

### Connexion SSH

```bash
# Connexion basique
ssh user@hostname

# Port spécifique
ssh -p 2222 user@hostname

# Avec clé
ssh -i ~/.ssh/id_rsa user@hostname

# Verbose
ssh -v user@hostname

# X11 Forwarding
ssh -X user@hostname

# Port forwarding local
ssh -L 8080:localhost:80 user@hostname

# Port forwarding remote
ssh -R 8080:localhost:80 user@hostname

# Proxy SOCKS
ssh -D 8080 user@hostname

# Exécuter commande
ssh user@hostname 'ls -la'

# Keep alive
ssh -o ServerAliveInterval=60 user@hostname
```

### Configuration SSH (~/.ssh/config)

```bash
# Créer config
nano ~/.ssh/config

# Host alias
# Host myserver
#     HostName 192.168.1.100
#     User admin
#     Port 22
#     IdentityFile ~/.ssh/id_rsa

# Utiliser
ssh myserver

# Wildcard
# Host *.example.com
#     User admin
#     IdentityFile ~/.ssh/company_key

# Options communes:
# ServerAliveInterval 60
# ServerAliveCountMax 3
# Compression yes
# ForwardAgent yes
```

### Génération clés SSH

```bash
# Générer clé RSA
ssh-keygen -t rsa -b 4096 -C "email@example.com"

# Générer clé ED25519 (recommandé)
ssh-keygen -t ed25519 -C "email@example.com"

# Avec mot de passe
ssh-keygen -t ed25519 -C "email@example.com" -f ~/.ssh/id_custom

# Copier clé sur serveur
ssh-copy-id user@hostname

# Manuel
cat ~/.ssh/id_rsa.pub | ssh user@hostname "cat >> ~/.ssh/authorized_keys"

# Permissions correctes
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys
```

### Configuration serveur SSH

```bash
# Fichier config
sudo nano /etc/ssh/sshd_config

# Désactiver root login
PermitRootLogin no

# Authentification par clé uniquement
PasswordAuthentication no
PubkeyAuthentication yes

# Changer port
Port 2222

# Limiter utilisateurs
AllowUsers user1 user2

# Redémarrer SSH
sudo systemctl restart sshd
```

### scp - Secure Copy

```bash
# Copier vers serveur
scp file.txt user@hostname:/path/to/destination/

# Copier depuis serveur
scp user@hostname:/path/to/file.txt ./

# Copier dossier
scp -r dossier/ user@hostname:/path/

# Port spécifique
scp -P 2222 file.txt user@hostname:/path/

# Avec compression
scp -C file.txt user@hostname:/path/

# Limiter bande passante (Ko/s)
scp -l 1000 file.txt user@hostname:/path/
```

### rsync over SSH

```bash
# Synchroniser dossiers
rsync -avz source/ user@hostname:/destination/

# Avec suppression
rsync -avz --delete source/ user@hostname:/destination/

# Dry run
rsync -avz --dry-run source/ user@hostname:/destination/

# Exclure fichiers
rsync -avz --exclude='*.log' source/ user@hostname:/destination/

# Avec progression
rsync -avz --progress source/ user@hostname:/destination/

# Options:
# a = archive (preserve permissions, times, etc.)
# v = verbose
# z = compression
```

## VPN

### OpenVPN

```bash
# Installer
sudo apt install openvpn

# Connecter
sudo openvpn --config client.ovpn

# En service
sudo cp client.ovpn /etc/openvpn/client.conf
sudo systemctl start openvpn@client
sudo systemctl enable openvpn@client
```

### WireGuard

```bash
# Installer
sudo apt install wireguard

# Générer clés
wg genkey | tee privatekey | wg pubkey > publickey

# Configuration
sudo nano /etc/wireguard/wg0.conf

# [Interface]
# PrivateKey = PRIVATE_KEY
# Address = 10.0.0.2/24
#
# [Peer]
# PublicKey = PEER_PUBLIC_KEY
# Endpoint = server.com:51820
# AllowedIPs = 0.0.0.0/0

# Démarrer
sudo wg-quick up wg0

# Arrêter
sudo wg-quick down wg0

# Statut
sudo wg show
```

## Sécurité

### fail2ban

Protection contre brute force.

```bash
# Installer
sudo apt install fail2ban

# Configuration
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# [sshd]
# enabled = true
# port = 22
# maxretry = 3
# bantime = 3600

# Démarrer
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Statut
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Débannir IP
sudo fail2ban-client set sshd unbanip 192.168.1.100
```

### Ports scan (nmap)

```bash
# Installer
sudo apt install nmap

# Scan ports
nmap hostname

# Scan rapide
nmap -F hostname

# Scan tous les ports
nmap -p- hostname

# Scan ports spécifiques
nmap -p 22,80,443 hostname

# Détection OS
sudo nmap -O hostname

# Détection services
nmap -sV hostname

# Scan agressif
sudo nmap -A hostname

# Scan réseau
nmap 192.168.1.0/24
```

[← Filesystem](./infos-terminal-03-linux-filesystem.md) | [Index](./infos-terminal-00-index.md) | [Processus →](./infos-terminal-05-linux-processus.md)

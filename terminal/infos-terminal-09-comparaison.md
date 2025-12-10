# ⚖️ Linux vs Windows - Comparaison

[← Windows Système](./infos-terminal-08-windows-systeme.md) | [Index](./infos-terminal-00-index.md)

## Commandes équivalentes

### Navigation et fichiers

| Tâche | Linux | Windows CMD | PowerShell |
|-------|-------|-------------|------------|
| Répertoire courant | `pwd` | `cd` | `Get-Location`, `pwd` |
| Changer répertoire | `cd /path` | `cd C:\path` | `Set-Location C:\path`, `cd` |
| Lister fichiers | `ls`, `ls -la` | `dir` | `Get-ChildItem`, `ls`, `dir` |
| Créer fichier | `touch file` | `type nul > file` | `New-Item file`, `ni` |
| Créer dossier | `mkdir dir` | `mkdir dir`, `md dir` | `New-Item -ItemType Directory`, `mkdir` |
| Copier | `cp src dest` | `copy src dest` | `Copy-Item src dest`, `cp` |
| Déplacer | `mv src dest` | `move src dest` | `Move-Item src dest`, `mv` |
| Supprimer fichier | `rm file` | `del file`, `erase` | `Remove-Item file`, `rm`, `del` |
| Supprimer dossier | `rm -rf dir` | `rmdir /s /q dir` | `Remove-Item dir -Recurse -Force` |
| Afficher fichier | `cat file` | `type file` | `Get-Content file`, `cat`, `type` |
| Rechercher fichiers | `find . -name "*.txt"` | `dir /s *.txt` | `Get-ChildItem -Recurse -Filter "*.txt"` |
| Rechercher dans fichiers | `grep "text" file` | `findstr "text" file` | `Select-String "text" file` |

### Système

| Tâche | Linux | Windows CMD | PowerShell |
|-------|-------|-------------|------------|
| Nom machine | `hostname` | `hostname` | `hostname`, `$env:COMPUTERNAME` |
| Utilisateur actuel | `whoami` | `whoami` | `whoami`, `$env:USERNAME` |
| Info système | `uname -a` | `systeminfo` | `Get-ComputerInfo` |
| Processus | `ps aux` | `tasklist` | `Get-Process` |
| Tuer processus | `kill PID` | `taskkill /pid PID` | `Stop-Process -Id PID` |
| Services | `systemctl list-units` | `sc query` | `Get-Service` |
| Variables env | `env`, `echo $VAR` | `set`, `echo %VAR%` | `Get-ChildItem Env:`, `$env:VAR` |
| Arrêter système | `shutdown -h now` | `shutdown /s /t 0` | `Stop-Computer` |
| Redémarrer | `reboot` | `shutdown /r /t 0` | `Restart-Computer` |

### Réseau

| Tâche | Linux | Windows CMD | PowerShell |
|-------|-------|-------------|------------|
| IP configuration | `ip addr`, `ifconfig` | `ipconfig` | `Get-NetIPAddress` |
| Ping | `ping -c 5 host` | `ping -n 5 host` | `Test-Connection host -Count 5` |
| Traceroute | `traceroute host` | `tracert host` | `Test-NetConnection host -TraceRoute` |
| DNS lookup | `dig`, `nslookup` | `nslookup` | `Resolve-DnsName` |
| Connexions réseau | `netstat -tuln` | `netstat -ano` | `Get-NetTCPConnection` |
| Flush DNS | `sudo systemd-resolve --flush-caches` | `ipconfig /flushdns` | `Clear-DnsClientCache` |
| Ports ouverts | `ss -tuln` | `netstat -ano` | `Get-NetTCPConnection -State Listen` |

### Disques et partitions

| Tâche | Linux | Windows CMD | PowerShell |
|-------|-------|-------------|------------|
| Espace disque | `df -h` | `dir` (basic) | `Get-PSDrive` |
| Utilisation dossier | `du -sh dir` | `dir /s` | `Get-ChildItem -Recurse | Measure-Object` |
| Monter disque | `mount /dev/sdb1 /mnt` | (auto) | `N/A` (auto) |
| Lister disques | `lsblk`, `fdisk -l` | `wmic diskdrive list` | `Get-Disk` |

### Permissions

| Tâche | Linux | Windows CMD | PowerShell |
|-------|-------|-------------|------------|
| Permissions fichier | `ls -l` | `icacls file` | `Get-Acl file` |
| Changer permissions | `chmod 755 file` | `icacls file /grant user:F` | `Set-Acl` |
| Changer propriétaire | `chown user:group file` | `icacls file /setowner user` | `Set-Acl` |
| Attributs | `chattr +i file` | `attrib +r file` | `Set-ItemProperty -Name IsReadOnly` |

## Philosophie et différences

### Système de fichiers

**Linux:**
```bash
# Arborescence unique
/
├── /home/user/
├── /etc/
├── /var/
└── /usr/

# Sensible à la casse
file.txt ≠ File.txt ≠ FILE.TXT

# Permissions: rwx (read, write, execute)
chmod 755 file

# Pas d'extensions obligatoires
myprogram  # Peut être exécutable
```

**Windows:**
```cmd
REM Lecteurs séparés
C:\
D:\
E:\

REM Insensible à la casse
file.txt = File.txt = FILE.TXT

REM Permissions: ACL (Access Control Lists)
icacls file /grant user:F

REM Extensions importantes
myprogram.exe  # Doit avoir .exe
```

### Ligne de commande

**Linux (Bash):**
```bash
# Philosophie Unix: faire une chose bien
ls | grep ".txt" | wc -l

# Pipes puissants
cat file.txt | grep "error" | sort | uniq -c

# Variables
$VAR
${VAR}

# Scripts: .sh
#!/bin/bash
```

**Windows CMD:**
```cmd
REM Commandes intégrées limitées
dir | find ".txt"

REM Pipes moins puissants
type file.txt | findstr "error"

REM Variables
%VAR%
%VARIABLE%

REM Scripts: .bat, .cmd
@echo off
```

**PowerShell:**
```powershell
# Orienté objet
Get-Process | Where-Object CPU -gt 100

# Cmdlets (Verb-Noun)
Get-Service | Stop-Service

# Variables
$var
${var}

# Scripts: .ps1
# PowerShell syntax
```

### Gestion de packages

**Linux:**
```bash
# Debian/Ubuntu (apt)
sudo apt update
sudo apt install package
sudo apt remove package

# RedHat/CentOS (yum/dnf)
sudo yum install package
sudo dnf install package

# Arch (pacman)
sudo pacman -S package

# Universal
snap install package
flatpak install package
```

**Windows:**
```powershell
# Windows Package Manager (winget)
winget search app
winget install app
winget uninstall app

# Chocolatey
choco install package
choco uninstall package

# Scoop
scoop install package
scoop uninstall package
```

### Services

**Linux (systemd):**
```bash
# Gérer services
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl status nginx
sudo systemctl enable nginx  # Auto-start
sudo systemctl disable nginx

# Logs
journalctl -u nginx
```

**Windows:**
```cmd
REM CMD
sc start service
sc stop service
sc query service
sc config service start= auto

REM PowerShell
Start-Service servicename
Stop-Service servicename
Get-Service servicename
Set-Service -Name servicename -StartupType Automatic
```

### Utilisateurs et permissions

**Linux:**
```bash
# Root (superuser)
sudo command

# Utilisateurs
useradd username
usermod -aG group username
passwd username

# Permissions
chmod 755 file        # rwxr-xr-x
chown user:group file

# Sudo
sudo visudo  # Éditer /etc/sudoers
```

**Windows:**
```cmd
REM Administrator
runas /user:Administrator command

REM Utilisateurs
net user username password /add
net localgroup Administrators username /add

REM Permissions (ACL)
icacls file /grant user:F

REM UAC (User Account Control)
REM Élévation de privilèges
```

## Environnement de développement

### Shells disponibles

**Linux:**
- Bash (défaut sur la plupart)
- Zsh (avec Oh My Zsh)
- Fish
- Dash
- Ksh

**Windows:**
- CMD (legacy)
- PowerShell 5.1 (intégré)
- PowerShell 7+ (cross-platform)
- Windows Terminal (émulateur moderne)
- WSL (Windows Subsystem for Linux)

### Scripts

**Linux (Bash script):**
```bash
#!/bin/bash

# Variables
name="Alice"

# Conditions
if [ "$name" = "Alice" ]; then
    echo "Hello Alice"
fi

# Boucles
for i in {1..5}; do
    echo $i
done

# Fonctions
function greet() {
    echo "Hello $1"
}
```

**Windows (Batch):**
```cmd
@echo off

REM Variables
set name=Alice

REM Conditions
if "%name%"=="Alice" (
    echo Hello Alice
)

REM Boucles
for %%i in (1 2 3 4 5) do (
    echo %%i
)
```

**PowerShell:**
```powershell
# Variables
$name = "Alice"

# Conditions
if ($name -eq "Alice") {
    Write-Host "Hello Alice"
}

# Boucles
for ($i = 1; $i -le 5; $i++) {
    Write-Host $i
}

# Fonctions
function Greet {
    param($name)
    Write-Host "Hello $name"
}
```

## Outils de développement

### Compilation

**Linux:**
```bash
# GCC/G++
gcc program.c -o program
g++ program.cpp -o program

# Make
make
make install
make clean

# CMake
cmake .
make
```

**Windows:**
```cmd
REM Visual Studio (cl.exe)
cl /EHsc program.cpp

REM MinGW (GCC pour Windows)
gcc program.c -o program.exe

REM MSBuild
msbuild project.sln
```

### Conteneurs

**Linux:**
```bash
# Docker natif
docker run -it ubuntu bash
docker-compose up

# Podman
podman run -it ubuntu bash
```

**Windows:**
```powershell
# Docker Desktop (avec WSL2)
docker run -it mcr.microsoft.com/windows/servercore cmd

# Windows Containers
docker run -it mcr.microsoft.com/windows/nanoserver
```

## Avantages et inconvénients

### Linux

**✅ Avantages:**
- Open source et gratuit
- Très stable et sécurisé
- Performances excellentes
- Personnalisable à l'extrême
- Idéal pour serveurs et développement
- Communauté active
- Gestion de packages centralisée

**❌ Inconvénients:**
- Courbe d'apprentissage plus raide
- Support matériel parfois limité
- Moins de logiciels commerciaux
- Fragmentation (nombreuses distributions)

### Windows

**✅ Avantages:**
- Interface graphique intuitive
- Large compatibilité logiciels
- Excellent support matériel
- Gaming (DirectX)
- Support commercial (Microsoft)
- Active Directory pour entreprises
- PowerShell moderne et puissant

**❌ Inconvénients:**
- Coût (licences)
- Moins stable que Linux
- Cible fréquente malwares
- Mises à jour forcées
- Bloatware pré-installé
- Télémétrie

## Cas d'usage

### Quand utiliser Linux?

- Serveurs web/applications
- Développement software
- DevOps/Infrastructure
- Conteneurs et orchestration
- Data science/Machine learning
- Systèmes embarqués
- Recherche scientifique

### Quand utiliser Windows?

- Bureautique (Office)
- Gaming
- Applications Adobe/Autodesk
- Développement .NET
- Active Directory
- Applications métier spécifiques
- Utilisateur desktop grand public

## Interopérabilité

### WSL (Windows Subsystem for Linux)

```powershell
# Installer WSL
wsl --install

# Lister distributions disponibles
wsl --list --online

# Installer distribution
wsl --install -d Ubuntu

# Lancer WSL
wsl

# Depuis Windows, accéder fichiers Linux
explorer.exe \\wsl$\Ubuntu\home\user

# Depuis Linux, accéder fichiers Windows
cd /mnt/c/Users/username
```

### Partage de fichiers

**Linux vers Windows:**
- Samba (SMB/CIFS)
- NFS
- SSH/SFTP

**Windows vers Linux:**
- SMB natif
- SSH/SFTP
- FTP

## Commandes universelles (cross-platform)

Certains outils fonctionnent partout:

```bash
# Git
git clone repo
git commit -m "message"
git push

# Node.js / npm
npm install
npm start

# Python
python script.py
pip install package

# Docker
docker build -t image .
docker run image

# VS Code
code .
```

[← Windows Système](./infos-terminal-08-windows-systeme.md) | [Index](./infos-terminal-00-index.md)

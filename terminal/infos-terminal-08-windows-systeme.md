# 🔧 Gestion Système Windows

[← PowerShell](./infos-terminal-07-windows-powershell.md) | [Index](./infos-terminal-00-index.md) | [Comparaison →](./infos-terminal-09-comparaison.md)

## Windows Management Instrumentation (WMI)

### WMIC (Legacy)

```cmd
REM Info système
wmic computersystem get model,name,manufacturer,systemtype

REM BIOS
wmic bios get serialnumber,manufacturer,version

REM CPU
wmic cpu get name,numberofcores,maxclockspeed,loadpercentage

REM Mémoire
wmic memorychip get capacity,speed,manufacturer

REM Carte mère
wmic baseboard get product,manufacturer,version,serialnumber

REM Disques
wmic diskdrive get model,size,interfacetype

REM Partitions
wmic partition get name,size,type

REM Logiciel installé
wmic product get name,version,vendor

REM Désinstaller logiciel
wmic product where name="AppName" call uninstall

REM Processus
wmic process list brief
wmic process where name="chrome.exe" get processid,executablepath

REM Tuer processus
wmic process where name="notepad.exe" delete

REM Services
wmic service list brief
wmic service where name="wuauserv" get name,state,startmode

REM Démarrer service
wmic service where name="wuauserv" call startservice

REM Utilisateurs
wmic useraccount list brief
wmic useraccount where name="username" get name,sid,accounttype

REM Groupes
wmic group list brief

REM Startup programs
wmic startup list full

REM Température (si disponible)
wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature
```

### PowerShell CIM/WMI

```powershell
# Get-CimInstance (recommandé)
Get-CimInstance -ClassName Win32_ComputerSystem
Get-CimInstance -ClassName Win32_OperatingSystem
Get-CimInstance -ClassName Win32_Processor
Get-CimInstance -ClassName Win32_PhysicalMemory
Get-CimInstance -ClassName Win32_DiskDrive

# Get-WmiObject (legacy)
Get-WmiObject -Class Win32_ComputerSystem

# Classes WMI courantes:
# Win32_ComputerSystem : Info système
# Win32_OperatingSystem : OS
# Win32_Processor : CPU
# Win32_PhysicalMemory : RAM
# Win32_DiskDrive : Disques
# Win32_LogicalDisk : Partitions
# Win32_NetworkAdapter : Réseau
# Win32_BIOS : BIOS
# Win32_Product : Logiciels installés
# Win32_Service : Services
# Win32_Process : Processus
```

## Gestion des mises à jour

### Windows Update (CMD)

```cmd
REM Vérifier mises à jour
UsoClient StartScan

REM Télécharger mises à jour
UsoClient StartDownload

REM Installer mises à jour
UsoClient StartInstall

REM Historique mises à jour
systeminfo | findstr /B /C:"Hotfix"
```

### PowerShell

```powershell
# Module PSWindowsUpdate (à installer)
Install-Module PSWindowsUpdate -Force

# Lister mises à jour disponibles
Get-WindowsUpdate

# Installer toutes les mises à jour
Install-WindowsUpdate -AcceptAll -AutoReboot

# Historique
Get-HotFix

# Dernière mise à jour
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 1
```

## Gestion des drivers

```powershell
# Lister drivers
Get-WindowsDriver -Online -All

# Export drivers
Export-WindowsDriver -Online -Destination C:\Drivers\

# Info driver
pnputil /enum-drivers

# Installer driver
pnputil /add-driver C:\path\to\driver.inf /install

# Supprimer driver
pnputil /delete-driver oem1.inf
```

## Gestion des fonctionnalités Windows

### DISM (Deployment Image Servicing and Management)

```cmd
REM Vérifier intégrité image
dism /online /cleanup-image /checkhealth

REM Scanner image
dism /online /cleanup-image /scanhealth

REM Réparer image
dism /online /cleanup-image /restorehealth

REM Lister fonctionnalités
dism /online /get-features

REM Activer fonctionnalité
dism /online /enable-feature /featurename:Microsoft-Hyper-V-All

REM Désactiver fonctionnalité
dism /online /disable-feature /featurename:WindowsMediaPlayer

REM Nettoyer composants
dism /online /cleanup-image /startcomponentcleanup
```

### PowerShell

```powershell
# Lister fonctionnalités
Get-WindowsOptionalFeature -Online

# Activer fonctionnalité
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All

# Désactiver fonctionnalité
Disable-WindowsOptionalFeature -Online -FeatureName WindowsMediaPlayer

# Fonctionnalités installées
Get-WindowsOptionalFeature -Online | Where-Object State -eq "Enabled"
```

## Système de fichiers

### Vérification disque

```cmd
REM CHKDSK
chkdsk C: /f /r

REM SFC (System File Checker)
sfc /scannow

REM Scanner fichier spécifique
sfc /scanfile=C:\windows\system32\kernel32.dll

REM Vérifier uniquement
sfc /verifyonly
```

### Quotas disque

```powershell
# Lister quotas
Get-FSRMQuota

# Créer quota
New-FSRMQuota -Path "C:\Users\username" -Size 10GB
```

### Compression

```powershell
# Compresser fichier
Compress-Archive -Path C:\files\* -DestinationPath C:\archive.zip

# Ajouter à archive
Compress-Archive -Path C:\newfile.txt -Update -DestinationPath C:\archive.zip

# Extraire
Expand-Archive -Path C:\archive.zip -DestinationPath C:\extracted\

# Compression NTFS
compact /c /s:C:\folder
compact /u /s:C:\folder  # Décompresser
```

## Journaux d'événements (Event Logs)

### Event Viewer (CMD)

```cmd
REM Afficher événements
eventvwr.msc

REM Exporter log
wevtutil epl System C:\system.evtx

REM Effacer log
wevtutil cl System
```

### PowerShell

```powershell
# Lister logs
Get-EventLog -List

# Derniers événements système
Get-EventLog -LogName System -Newest 100

# Événements applicatifs
Get-EventLog -LogName Application -Newest 50

# Filtrer par type
Get-EventLog -LogName System -EntryType Error -Newest 50

# Filtrer par source
Get-EventLog -LogName System -Source "Service Control Manager"

# Événements après date
Get-EventLog -LogName System -After (Get-Date).AddDays(-1)

# Event Viewer moderne
Get-WinEvent -LogName System -MaxEvents 100

# Filtrer erreurs
Get-WinEvent -FilterHashtable @{LogName='System'; Level=2}

# Avec FilterXPath
Get-WinEvent -LogName System -FilterXPath "*[System[EventID=1074]]"
```

## Performances

### Performance Monitor

```cmd
REM Lancer perfmon
perfmon

REM Compteurs de performances
typeperf "\Processor(_Total)\% Processor Time"

REM Multiple compteurs
typeperf "\Processor(_Total)\% Processor Time" "\Memory\Available MBytes"

REM Avec intervalle
typeperf "\Processor(_Total)\% Processor Time" -si 1 -sc 60

REM Export CSV
typeperf -cf counters.txt -o output.csv -si 1 -sc 3600
```

### PowerShell

```powershell
# Compteurs disponibles
Get-Counter -ListSet *

# CPU
Get-Counter '\Processor(_Total)\% Processor Time'

# Mémoire
Get-Counter '\Memory\Available MBytes'

# Disque
Get-Counter '\PhysicalDisk(_Total)\% Disk Time'

# Continu
Get-Counter '\Processor(_Total)\% Processor Time' -Continuous

# Multiple compteurs
Get-Counter @(
    '\Processor(_Total)\% Processor Time',
    '\Memory\Available MBytes'
)
```

## Tâches système

### Task Scheduler

```cmd
REM GUI
taskschd.msc

REM CLI
schtasks /query

REM Créer tâche quotidienne
schtasks /create /tn "Backup" /tr "C:\backup.bat" /sc daily /st 02:00

REM Hebdomadaire
schtasks /create /tn "Maintenance" /tr "C:\maint.exe" /sc weekly /d SUN /st 03:00

REM Au démarrage
schtasks /create /tn "Startup" /tr "C:\startup.bat" /sc onstart

REM À la connexion
schtasks /create /tn "Login" /tr "C:\login.bat" /sc onlogon

REM Exécuter tâche
schtasks /run /tn "Backup"

REM Supprimer tâche
schtasks /delete /tn "Backup" /f
```

### PowerShell (voir fichier PowerShell)

## Pare-feu Windows

### netsh

```cmd
REM Statut pare-feu
netsh advfirewall show allprofiles

REM Activer pare-feu
netsh advfirewall set allprofiles state on

REM Désactiver (non recommandé)
netsh advfirewall set allprofiles state off

REM Autoriser programme
netsh advfirewall firewall add rule name="My App" dir=in action=allow program="C:\app.exe"

REM Autoriser port
netsh advfirewall firewall add rule name="Port 8080" dir=in action=allow protocol=TCP localport=8080

REM Bloquer port
netsh advfirewall firewall add rule name="Block 23" dir=in action=block protocol=TCP localport=23

REM Supprimer règle
netsh advfirewall firewall delete rule name="My App"

REM Lister règles
netsh advfirewall firewall show rule name=all

REM Réinitialiser
netsh advfirewall reset
```

### PowerShell

```powershell
# Lister règles
Get-NetFirewallRule

# Règles actives
Get-NetFirewallRule | Where-Object Enabled -eq True

# Autoriser programme
New-NetFirewallRule -DisplayName "My App" -Direction Inbound -Program "C:\app.exe" -Action Allow

# Autoriser port
New-NetFirewallRule -DisplayName "Port 8080" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

# Supprimer règle
Remove-NetFirewallRule -DisplayName "My App"

# Profils
Get-NetFirewallProfile
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

## Utilisateurs et sécurité

### Comptes locaux

```cmd
REM Lister utilisateurs
net user

REM Info utilisateur
net user username

REM Créer utilisateur
net user username password /add

REM Modifier mot de passe
net user username newpassword

REM Supprimer utilisateur
net user username /delete

REM Désactiver compte
net user username /active:no

REM Activer compte
net user username /active:yes

REM Ajouter à groupe
net localgroup Administrators username /add

REM Retirer de groupe
net localgroup Administrators username /delete

REM Lister groupes
net localgroup

REM Membres groupe
net localgroup Administrators
```

### Permissions fichiers (icacls)

```cmd
REM Afficher permissions
icacls file.txt

REM Donner accès complet
icacls file.txt /grant username:F

REM Permissions:
REM F : Full access
REM M : Modify
REM RX : Read & Execute
REM R : Read
REM W : Write

REM Lecture seule
icacls file.txt /grant username:R

REM Supprimer permissions
icacls file.txt /remove username

REM Héritage
icacls folder /inheritance:r

REM Récursif
icacls folder /grant username:F /t

REM Réinitialiser
icacls file.txt /reset
```

## Optimisation système

### Nettoyage disque

```cmd
REM Cleanmgr
cleanmgr /d C:

REM Automatique
cleanmgr /sagerun:1
```

### Defragmentation

```cmd
REM Analyser
defrag C: /A

REM Défragmenter
defrag C: /O

REM Tous les lecteurs
defrag /C /O

REM SSD (TRIM)
defrag C: /L
```

### PowerShell

```powershell
# Analyser fragmentation
Get-Volume C | Optimize-Volume -Analyze

# Défragmenter
Optimize-Volume -DriveLetter C

# Tous les volumes
Get-Volume | Optimize-Volume
```

## Registre (avancé)

```cmd
REM Exporter clé
reg export "HKLM\Software\MyApp" backup.reg

REM Importer
reg import backup.reg

REM Backup complet
reg save HKLM\Software\MyApp backup.hiv

REM Restaurer
reg restore HKLM\Software\MyApp backup.hiv

REM Comparer
reg compare "HKLM\Software\MyApp" "HKLM\Software\MyApp2"
```

## Sauvegarde et restauration

### System Restore

```cmd
REM Créer point de restauration
wmic.exe /Namespace:\\root\default Path SystemRestore Call CreateRestorePoint "My Restore Point", 100, 7

REM Lister points
vssadmin list shadows

REM Restaurer (GUI)
rstrui.exe
```

### Backup (PowerShell)

```powershell
# Windows Server Backup (si installé)
Get-WBBackupSet

# Créer backup
$policy = New-WBPolicy
$volume = Get-WBVolume -VolumePath C:
Add-WBVolume -Policy $policy -Volume $volume
$target = New-WBBackupTarget -VolumePath D:
Add-WBBackupTarget -Policy $policy -Target $target
Start-WBBackup -Policy $policy
```

## Bonnes pratiques

```powershell
# ✅ Toujours créer point de restauration avant modifications
Checkpoint-Computer -Description "Before changes"

# ✅ Sauvegarder registre avant modifications
reg export "HKLM\Software\MyKey" backup.reg

# ✅ Vérifier intégrité système régulièrement
sfc /scannow
dism /online /cleanup-image /restorehealth

# ✅ Tenir système à jour
Install-WindowsUpdate -AcceptAll

# ✅ Nettoyer disque régulièrement
cleanmgr /d C:

# ✅ Surveiller logs d'événements
Get-EventLog -LogName System -EntryType Error -Newest 50

# ❌ Ne jamais désactiver pare-feu sans raison
# ❌ Éviter modifications registre sans backup
# ❌ Ne pas exécuter scripts non vérifiés en admin
```

[← PowerShell](./infos-terminal-07-windows-powershell.md) | [Index](./infos-terminal-00-index.md) | [Comparaison →](./infos-terminal-09-comparaison.md)

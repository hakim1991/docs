# ⚡ PowerShell Windows

[← Windows CMD](./infos-terminal-06-windows-cmd.md) | [Index](./infos-terminal-00-index.md) | [Windows Système →](./infos-terminal-08-windows-systeme.md)

## Introduction

PowerShell est un shell moderne orienté objet et un langage de script.

```powershell
# Version PowerShell
$PSVersionTable

# Aide
Get-Help
Get-Help Get-Process
Get-Help Get-Process -Examples
Get-Help Get-Process -Full
Update-Help  # Mettre à jour aide
```

## Commandes de base (Cmdlets)

### Navigation

```powershell
# Répertoire courant
Get-Location
pwd  # Alias

# Changer répertoire
Set-Location C:\Users
cd C:\Users  # Alias

# Lister fichiers
Get-ChildItem
ls  # Alias
dir  # Alias

# Récursif
Get-ChildItem -Recurse

# Fichiers uniquement
Get-ChildItem -File

# Dossiers uniquement
Get-ChildItem -Directory

# Fichiers cachés
Get-ChildItem -Force

# Avec filtre
Get-ChildItem *.txt
Get-ChildItem -Filter *.log

# Par propriété
Get-ChildItem | Where-Object Length -gt 1MB
```

### Fichiers

```powershell
# Créer fichier
New-Item file.txt -ItemType File
ni file.txt  # Alias

# Créer dossier
New-Item folder -ItemType Directory
mkdir folder  # Alias

# Copier
Copy-Item source.txt destination.txt
cp source.txt dest.txt  # Alias

# Copier dossier
Copy-Item folder newfolder -Recurse

# Déplacer
Move-Item file.txt newfolder/
mv file.txt newfolder/  # Alias

# Renommer
Rename-Item oldname.txt newname.txt
ren oldname.txt newname.txt  # Alias

# Supprimer
Remove-Item file.txt
rm file.txt  # Alias
del file.txt  # Alias

# Supprimer dossier
Remove-Item folder -Recurse -Force

# Lire fichier
Get-Content file.txt
cat file.txt  # Alias
type file.txt  # Alias

# Premières lignes
Get-Content file.txt -Head 10

# Dernières lignes
Get-Content file.txt -Tail 10

# Suivre fichier (logs)
Get-Content file.log -Wait

# Écrire fichier (écrase)
Set-Content file.txt "Hello World"

# Ajouter
Add-Content file.txt "New line"
```

### Recherche

```powershell
# Rechercher fichiers
Get-ChildItem -Recurse -Filter "*.txt"

# Rechercher dans contenu
Select-String "pattern" file.txt
Select-String "error" *.log

# Insensible à la casse
Select-String "pattern" file.txt -CaseSensitive:$false

# Avec regex
Select-String -Pattern "\d{3}-\d{3}-\d{4}" file.txt
```

## Variables

```powershell
# Définir variable
$name = "Alice"
$age = 25
$items = @("item1", "item2", "item3")

# Afficher
$name
Write-Host $name

# Types
$number = 42
$text = "Hello"
$bool = $true
$array = @(1, 2, 3)
$hash = @{Name="Alice"; Age=25}

# Variables automatiques
$PWD          # Répertoire courant
$HOME         # Home
$PSVersionTable  # Version PS
$_            # Objet actuel dans pipeline

# Variables d'environnement
$env:PATH
$env:USERNAME
$env:COMPUTERNAME
```

## Objets et Pipeline

```powershell
# PowerShell travaille avec des objets
Get-Process | Get-Member

# Sélectionner propriétés
Get-Process | Select-Object Name, CPU, Memory

# Trier
Get-Process | Sort-Object CPU -Descending

# Filtrer
Get-Process | Where-Object CPU -gt 100
Get-Process | Where-Object {$_.CPU -gt 100}

# Premier/Dernier
Get-Process | Select-Object -First 5
Get-Process | Select-Object -Last 5

# Format tableau
Get-Process | Format-Table Name, CPU, Memory

# Format liste
Get-Process | Format-List *

# Export
Get-Process | Export-Csv processes.csv
Get-Process | ConvertTo-Json > processes.json
Get-Process | Out-File processes.txt
```

## Processus

```powershell
# Lister processus
Get-Process

# Processus spécifique
Get-Process chrome
Get-Process -Name chrome

# Par ID
Get-Process -Id 1234

# Avec filtres
Get-Process | Where-Object CPU -gt 100

# Trier par CPU
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Trier par mémoire
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# Démarrer processus
Start-Process notepad.exe
Start-Process chrome.exe "https://google.com"

# Avec élévation
Start-Process powershell -Verb RunAs

# Tuer processus
Stop-Process -Name notepad
Stop-Process -Id 1234
Stop-Process -Name chrome -Force

# Attendre processus
Wait-Process -Name notepad
```

## Services

```powershell
# Lister services
Get-Service

# Service spécifique
Get-Service -Name wuauserv

# Services en cours
Get-Service | Where-Object Status -eq "Running"

# Démarrer service
Start-Service -Name wuauserv

# Arrêter service
Stop-Service -Name wuauserv

# Redémarrer service
Restart-Service -Name wuauserv

# Statut service
Get-Service -Name wuauserv | Select-Object Name, Status, StartType

# Changer startup type
Set-Service -Name wuauserv -StartupType Automatic
```

## Réseau

```powershell
# Configuration IP
Get-NetIPAddress
Get-NetIPConfiguration

# Adaptateurs
Get-NetAdapter

# Activer/désactiver
Enable-NetAdapter -Name "Ethernet"
Disable-NetAdapter -Name "Ethernet"

# Route
Get-NetRoute

# Connexions
Get-NetTCPConnection
Get-NetTCPConnection -State Listen

# Processus utilisant port
Get-NetTCPConnection -LocalPort 80 | Select-Object OwningProcess

# DNS
Resolve-DnsName google.com
Clear-DnsClientCache  # Flush DNS

# Ping
Test-Connection google.com
Test-Connection -ComputerName google.com -Count 4

# Port ouvert
Test-NetConnection -ComputerName google.com -Port 443

# Traceroute
Test-NetConnection -ComputerName google.com -TraceRoute

# Download
Invoke-WebRequest -Uri "https://example.com/file.zip" -OutFile "file.zip"
```

## Système

```powershell
# Info système
Get-ComputerInfo

# Nom ordinateur
$env:COMPUTERNAME
hostname

# Uptime
(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime

# Disques
Get-PSDrive

# Espace disque
Get-PSDrive C | Select-Object Used,Free

# Informations disque
Get-Disk
Get-Volume

# Processeur
Get-WmiObject Win32_Processor | Select-Object Name, MaxClockSpeed, NumberOfCores

# Mémoire
Get-WmiObject Win32_PhysicalMemory | Select-Object Capacity
Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity

# Date/Heure
Get-Date
Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Redémarrer/Arrêter
Restart-Computer
Stop-Computer

# Avec délai
Restart-Computer -Delay 60
```

## Utilisateurs et groupes

```powershell
# Utilisateur actuel
$env:USERNAME
whoami

# Lister utilisateurs locaux
Get-LocalUser

# Créer utilisateur
New-LocalUser -Name "newuser" -Password (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force)

# Modifier utilisateur
Set-LocalUser -Name "username" -Description "Description"

# Supprimer utilisateur
Remove-LocalUser -Name "username"

# Groupes
Get-LocalGroup

# Membres groupe
Get-LocalGroupMember -Group "Administrators"

# Ajouter à groupe
Add-LocalGroupMember -Group "Administrators" -Member "username"

# Retirer de groupe
Remove-LocalGroupMember -Group "Administrators" -Member "username"
```

## Registre

```powershell
# Naviguer registre
cd HKLM:\Software

# Lire valeur
Get-ItemProperty -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion"

# Valeur spécifique
Get-ItemPropertyValue -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion" -Name "ProgramFilesDir"

# Créer clé
New-Item -Path "HKCU:\Software\MyApp"

# Créer valeur
New-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting" -Value "Value" -PropertyType String

# Modifier valeur
Set-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting" -Value "NewValue"

# Supprimer valeur
Remove-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting"

# Supprimer clé
Remove-Item -Path "HKCU:\Software\MyApp" -Recurse
```

## Tâches planifiées

```powershell
# Lister tâches
Get-ScheduledTask

# Tâche spécifique
Get-ScheduledTask -TaskName "MyTask"

# Info détaillée
Get-ScheduledTask -TaskName "MyTask" | Get-ScheduledTaskInfo

# Créer action
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\script.ps1"

# Créer trigger
$trigger = New-ScheduledTaskTrigger -Daily -At 9am

# Créer tâche
Register-ScheduledTask -TaskName "MyTask" -Action $action -Trigger $trigger

# Démarrer tâche
Start-ScheduledTask -TaskName "MyTask"

# Arrêter tâche
Stop-ScheduledTask -TaskName "MyTask"

# Supprimer tâche
Unregister-ScheduledTask -TaskName "MyTask" -Confirm:$false
```

## Scripting

### Conditions

```powershell
# If-Else
$age = 25
if ($age -ge 18) {
    Write-Host "Adult"
} elseif ($age -ge 13) {
    Write-Host "Teenager"
} else {
    Write-Host "Child"
}

# Opérateurs de comparaison
# -eq  : égal
# -ne  : différent
# -gt  : supérieur
# -ge  : supérieur ou égal
# -lt  : inférieur
# -le  : inférieur ou égal
# -like : pattern matching
# -match : regex

# Switch
$day = "Monday"
switch ($day) {
    "Monday"    { Write-Host "Start of week" }
    "Friday"    { Write-Host "End of week" }
    "Saturday"  { Write-Host "Weekend" }
    default     { Write-Host "Midweek" }
}
```

### Boucles

```powershell
# For
for ($i = 0; $i -lt 10; $i++) {
    Write-Host $i
}

# ForEach
$items = @("item1", "item2", "item3")
foreach ($item in $items) {
    Write-Host $item
}

# ForEach-Object (dans pipeline)
Get-Process | ForEach-Object {
    Write-Host $_.Name
}

# While
$i = 0
while ($i -lt 10) {
    Write-Host $i
    $i++
}

# Do-While
$i = 0
do {
    Write-Host $i
    $i++
} while ($i -lt 10)
```

### Fonctions

```powershell
# Fonction simple
function Say-Hello {
    Write-Host "Hello!"
}

# Avec paramètres
function Say-Hello {
    param(
        [string]$Name
    )
    Write-Host "Hello, $Name!"
}

# Appel
Say-Hello -Name "Alice"

# Avec valeur de retour
function Add-Numbers {
    param(
        [int]$a,
        [int]$b
    )
    return $a + $b
}

$result = Add-Numbers -a 5 -b 3

# Paramètres avancés
function Get-Info {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,

        [Parameter(Mandatory=$false)]
        [int]$Age = 0,

        [switch]$Verbose
    )

    if ($Verbose) {
        Write-Host "Name: $Name, Age: $Age"
    }
}
```

### Gestion erreurs

```powershell
# Try-Catch
try {
    Get-Content "nonexistent.txt" -ErrorAction Stop
}
catch {
    Write-Host "Error: $_"
}
finally {
    Write-Host "Cleanup"
}

# Erreurs non-terminantes
Get-ChildItem -Path "C:\NonExistent" -ErrorAction SilentlyContinue

# ErrorAction:
# - Stop : Lance exception
# - Continue : Affiche erreur et continue (défaut)
# - SilentlyContinue : Ignore erreur
# - Inquire : Demande confirmation
```

## Modules

```powershell
# Lister modules disponibles
Get-Module -ListAvailable

# Modules chargés
Get-Module

# Importer module
Import-Module ModuleName

# Commandes d'un module
Get-Command -Module ModuleName

# Installer module (PSGallery)
Install-Module -Name ModuleName

# Mettre à jour module
Update-Module -Name ModuleName

# Supprimer module
Uninstall-Module -Name ModuleName
```

## Remoting

```powershell
# Activer remoting
Enable-PSRemoting -Force

# Session interactive
Enter-PSSession -ComputerName Server01

# Quitter session
Exit-PSSession

# Exécuter commande distante
Invoke-Command -ComputerName Server01 -ScriptBlock {
    Get-Process
}

# Avec credentials
$cred = Get-Credential
Invoke-Command -ComputerName Server01 -Credential $cred -ScriptBlock {
    Get-Service
}

# Session persistante
$session = New-PSSession -ComputerName Server01
Invoke-Command -Session $session -ScriptBlock { Get-Process }
Remove-PSSession $session
```

## Utilitaires

```powershell
# Mesurer temps d'exécution
Measure-Command { Get-Process }

# Comparer objets
Compare-Object (Get-Content file1.txt) (Get-Content file2.txt)

# Grouper
Get-Process | Group-Object ProcessName

# Compter
Get-Process | Measure-Object

# Statistiques
Get-Process | Measure-Object WorkingSet -Sum -Average -Maximum -Minimum

# Sélectionner propriétés uniques
Get-Process | Select-Object -ExpandProperty ProcessName -Unique

# Hash fichier
Get-FileHash file.txt
Get-FileHash file.txt -Algorithm SHA256
```

## Alias

```powershell
# Lister alias
Get-Alias

# Alias d'une commande
Get-Alias ls

# Créer alias
New-Alias -Name ll -Value Get-ChildItem

# Supprimer alias
Remove-Alias -Name ll

# Alias permanents dans profile
# $PROFILE
notepad $PROFILE
```

## Profile PowerShell

```powershell
# Emplacement profile
$PROFILE

# Tester si existe
Test-Path $PROFILE

# Créer si n'existe pas
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -ItemType File -Force
}

# Éditer
notepad $PROFILE

# Exemple profile:
# Set-Location C:\Projects
# New-Alias -Name ll -Value Get-ChildItem
# function prompt { "PS $(Get-Location)> " }
```

## Execution Policy

```powershell
# Voir policy
Get-ExecutionPolicy

# Modifier (admin requis)
Set-ExecutionPolicy RemoteSigned
Set-ExecutionPolicy Unrestricted

# Policies:
# - Restricted : Aucun script (défaut)
# - AllSigned : Scripts signés uniquement
# - RemoteSigned : Scripts locaux OK, distants signés
# - Unrestricted : Tous scripts (attention!)

# Bypass pour un script
powershell -ExecutionPolicy Bypass -File script.ps1
```

## Bonnes pratiques

```powershell
# ✅ Utiliser cmdlets au lieu d'alias dans scripts
Get-ChildItem  # au lieu de ls

# ✅ Paramètres explicites
Get-Process -Name chrome

# ✅ Gestion erreurs
try {
    Get-Content $file -ErrorAction Stop
} catch {
    Write-Error "Cannot read file"
}

# ✅ Commentaires
# Single line comment
<#
Multi-line
comment
#>

# ✅ Approved verbs pour fonctions
Get-Verb

# ❌ Éviter Write-Host (utiliser Write-Output)
# ❌ Ne pas ignorer erreurs systématiquement
# ❌ Vérifier ExecutionPolicy en production
```

## Raccourcis clavier

```
Tab : Auto-complétion
Ctrl + Space : IntelliSense
Ctrl + C : Interrompre
Ctrl + L : Effacer écran (clear)
F7 : Historique commandes
↑ / ↓ : Naviguer historique
Ctrl + R : Recherche historique
```

[← Windows CMD](./infos-terminal-06-windows-cmd.md) | [Index](./infos-terminal-00-index.md) | [Windows Système →](./infos-terminal-08-windows-systeme.md)

# 🪟 Commandes Windows CMD

[← Linux Processus](./infos-terminal-05-linux-processus.md) | [Index](./infos-terminal-00-index.md) | [PowerShell →](./infos-terminal-07-windows-powershell.md)

## Navigation

### cd - Change Directory

```cmd
REM Changer de dossier
cd C:\Users\username\Documents

REM Dossier parent
cd..

REM Racine du lecteur
cd \

REM Changer de lecteur
D:

REM Afficher dossier courant
cd

REM Changer lecteur et dossier
cd /d D:\Projects
```

### dir - List Directory

```cmd
REM Liste simple
dir

REM Détails
dir /a

REM Fichiers uniquement
dir /a-d

REM Dossiers uniquement
dir /ad

REM Fichiers cachés
dir /ah

REM Récursif
dir /s

REM Tri par date
dir /od

REM Tri par taille
dir /os

REM Format compact
dir /b

REM Avec pause
dir /p

REM Avec pattern
dir *.txt
dir file?.txt
```

### tree

Arborescence.

```cmd
REM Arbre complet
tree

REM Avec fichiers
tree /f

REM Dossier spécifique
tree C:\Users\username
```

## Gestion fichiers

### copy

Copier fichiers.

```cmd
REM Copier fichier
copy source.txt destination.txt

REM Copier vers dossier
copy file.txt C:\Backup\

REM Copier multiple
copy *.txt C:\Backup\

REM Avec confirmation
copy /y source.txt dest.txt

REM Verbose
copy /v source.txt dest.txt

REM Binaire
copy /b file1.exe file2.exe
```

### xcopy

Copie avancée.

```cmd
REM Copier dossier
xcopy source destination /e /i

REM Avec sous-dossiers
xcopy source destination /s

REM Y compris vides
xcopy source destination /e

REM Avec attributs
xcopy source destination /k

REM Mise à jour uniquement
xcopy source destination /d /u

REM Exclure fichiers
xcopy source destination /exclude:exclude.txt
```

### robocopy

Copie robuste.

```cmd
REM Copier dossier
robocopy source destination /e

REM Avec retry
robocopy source destination /e /r:3 /w:5

REM Miroir (attention: supprime destination)
robocopy source destination /mir

REM Exclure fichiers
robocopy source destination /e /xf *.log

REM Exclure dossiers
robocopy source destination /e /xd temp logs

REM Limite bande passante (Ko/s)
robocopy source destination /e /ipm:1000

REM Avec log
robocopy source destination /e /log:copy.log
```

### move

Déplacer/renommer.

```cmd
REM Déplacer fichier
move file.txt C:\Destination\

REM Renommer
move oldname.txt newname.txt

REM Déplacer multiple
move *.txt C:\Destination\

REM Avec confirmation
move /y file.txt destination\
```

### del / erase

Supprimer fichiers.

```cmd
REM Supprimer fichier
del file.txt

REM Supprimer multiple
del *.txt

REM Force suppression
del /f file.txt

REM Avec confirmation
del /p file.txt

REM Récursif
del /s *.tmp

REM Tout le dossier
del /q /s folder\*
```

### rd / rmdir

Supprimer dossiers.

```cmd
REM Supprimer dossier vide
rmdir folder

REM Supprimer avec contenu
rmdir /s folder

REM Sans confirmation
rmdir /s /q folder
```

### md / mkdir

Créer dossiers.

```cmd
REM Créer dossier
mkdir newfolder

REM Créer avec sous-dossiers
mkdir parent\child\grandchild

REM Multiple
mkdir folder1 folder2 folder3
```

### ren / rename

Renommer.

```cmd
REM Renommer fichier
ren oldname.txt newname.txt

REM Renommer extension
ren *.txt *.bak

REM Renommer dossier
ren oldfolder newfolder
```

### type

Afficher contenu fichier.

```cmd
REM Afficher fichier
type file.txt

REM Multiple
type file1.txt file2.txt

REM Avec pagination
type file.txt | more
```

### more

Pagination.

```cmd
REM Afficher avec pagination
more file.txt

REM Avec commande
dir /s | more
```

### find

Rechercher texte dans fichiers.

```cmd
REM Rechercher dans fichier
find "texte" file.txt

REM Insensible à la casse
find /i "texte" file.txt

REM Compter occurrences
find /c "texte" file.txt

REM Numéros de ligne
find /n "texte" file.txt

REM Inverser (ne contenant PAS)
find /v "texte" file.txt

REM Multiple fichiers
find "error" *.log
```

### findstr

Recherche avec regex.

```cmd
REM Recherche simple
findstr "pattern" file.txt

REM Insensible à la casse
findstr /i "pattern" file.txt

REM Regex
findstr /r "^Start.*End$" file.txt

REM Récursif
findstr /s "error" *.log

REM Multiple patterns
findstr /c:"error" /c:"warning" file.txt

REM Numéros de ligne
findstr /n "pattern" file.txt
```

### fc

Comparer fichiers.

```cmd
REM Comparer texte
fc file1.txt file2.txt

REM Comparer binaire
fc /b file1.exe file2.exe

REM Ignorer casse
fc /c file1.txt file2.txt

REM Ignorer blancs
fc /w file1.txt file2.txt
```

## Système

### systeminfo

Informations système.

```cmd
REM Info complètes
systeminfo

REM Format CSV
systeminfo /fo csv

REM Machine distante
systeminfo /s computername /u username /p password
```

### hostname

Nom de l'ordinateur.

```cmd
hostname
```

### ver

Version Windows.

```cmd
ver
```

### date / time

Date et heure.

```cmd
REM Afficher date
date /t

REM Afficher heure
time /t

REM Modifier date
date

REM Modifier heure
time
```

### shutdown

Arrêter/redémarrer.

```cmd
REM Arrêt immédiat
shutdown /s /t 0

REM Redémarrage
shutdown /r /t 0

REM Avec délai (secondes)
shutdown /s /t 60

REM Annuler
shutdown /a

REM Arrêt forcé
shutdown /s /f /t 0

REM Avec message
shutdown /s /t 60 /c "Maintenance système"

REM Déconnexion
shutdown /l

REM Hibernation
shutdown /h
```

## Réseau

### ipconfig

Configuration IP.

```cmd
REM Configuration réseau
ipconfig

REM Détaillé
ipconfig /all

REM Renouveler DHCP
ipconfig /renew

REM Libérer DHCP
ipconfig /release

REM Vider cache DNS
ipconfig /flushdns

REM Afficher cache DNS
ipconfig /displaydns
```

### ping

Test connectivité.

```cmd
REM Ping
ping google.com

REM Nombre de paquets
ping -n 5 google.com

REM Continu
ping -t google.com

REM Taille paquet
ping -l 1000 google.com
```

### tracert

Tracer route.

```cmd
REM Traceroute
tracert google.com

REM Avec timeout
tracert -w 1000 google.com
```

### netstat

Statistiques réseau.

```cmd
REM Connexions actives
netstat

REM Toutes les connexions
netstat -a

REM Avec processus
netstat -ano

REM Ports en écoute
netstat -an | find "LISTENING"

REM Statistiques
netstat -s

REM Routes
netstat -r

REM Rafraîchir toutes les 5 secondes
netstat -ano 5
```

### nslookup

Requêtes DNS.

```cmd
REM Lookup
nslookup google.com

REM Serveur DNS spécifique
nslookup google.com 8.8.8.8

REM Record MX
nslookup -type=MX google.com
```

### net

Commandes réseau.

```cmd
REM Partages réseau
net share

REM Utilisateurs connectés
net session

REM Mapper lecteur
net use Z: \\server\share

REM Démapper
net use Z: /delete

REM Avec credentials
net use Z: \\server\share /user:username password

REM Services
net start
net stop servicename
net start servicename

REM Utilisateurs
net user
net user username
net user username password /add
net user username /delete
```

## Processus et tâches

### tasklist

Liste processus.

```cmd
REM Tous les processus
tasklist

REM Avec services
tasklist /svc

REM Format CSV
tasklist /fo csv

REM Filtrer
tasklist /fi "imagename eq chrome.exe"
tasklist /fi "memusage gt 100000"
```

### taskkill

Tuer processus.

```cmd
REM Par nom
taskkill /im notepad.exe

REM Par PID
taskkill /pid 1234

REM Force
taskkill /f /im chrome.exe

REM Tous les processus d'un nom
taskkill /f /im "chrome.exe" /t
```

### start

Lancer programme.

```cmd
REM Lancer application
start notepad.exe

REM Avec priorité
start /low command
start /high command

REM Attendre fin
start /wait command

REM Nouvelle fenêtre
start cmd

REM Minimisé
start /min command
```

### schtasks

Tâches planifiées.

```cmd
REM Lister tâches
schtasks /query

REM Créer tâche
schtasks /create /tn "MyTask" /tr "C:\script.bat" /sc daily /st 09:00

REM Supprimer tâche
schtasks /delete /tn "MyTask" /f

REM Lancer tâche
schtasks /run /tn "MyTask"

REM Arrêter tâche
schtasks /end /tn "MyTask"
```

## Gestion disques

### diskpart

Gestion disques (interactif).

```cmd
REM Lancer diskpart
diskpart

REM Commandes diskpart:
list disk
select disk 0
list partition
select partition 1
detail disk
clean
create partition primary
format fs=ntfs quick
assign letter=D
```

### chkdsk

Vérifier disque.

```cmd
REM Vérifier
chkdsk C:

REM Réparer
chkdsk C: /f

REM Réparer secteurs
chkdsk C: /r

REM Scan seulement
chkdsk C: /scan
```

### format

Formater disque.

```cmd
REM Formater
format D:

REM Quick format
format D: /q

REM Système de fichiers
format D: /fs:ntfs

REM Label
format D: /v:MyDrive
```

## Permissions et sécurité

### attrib

Attributs fichiers.

```cmd
REM Afficher attributs
attrib file.txt

REM Lecture seule
attrib +r file.txt
attrib -r file.txt

REM Caché
attrib +h file.txt
attrib -h file.txt

REM Système
attrib +s file.txt

REM Archive
attrib +a file.txt

REM Récursif
attrib +r /s /d *.*
```

### icacls

Permissions NTFS.

```cmd
REM Afficher permissions
icacls file.txt

REM Donner accès complet
icacls file.txt /grant username:F

REM Lecture seule
icacls file.txt /grant username:R

REM Supprimer permissions
icacls file.txt /remove username

REM Héritage
icacls folder /inheritance:r
```

### cipher

Chiffrement.

```cmd
REM Chiffrer
cipher /e folder

REM Déchiffrer
cipher /d folder

REM Effacer espace libre
cipher /w:C:\
```

## Variables et environnement

### set

Variables d'environnement.

```cmd
REM Afficher toutes
set

REM Afficher variable
echo %PATH%
echo %USERNAME%

REM Définir variable
set MY_VAR=value

REM Afficher avec set
set MY_VAR

REM Supprimer
set MY_VAR=

REM Variables système courantes:
REM %PATH% : Chemins exécutables
REM %USERNAME% : Utilisateur
REM %COMPUTERNAME% : Nom PC
REM %USERPROFILE% : C:\Users\username
REM %TEMP% : Dossier temp
REM %CD% : Dossier courant
```

### setx

Variables permanentes.

```cmd
REM Variable utilisateur (permanent)
setx MY_VAR "value"

REM Variable système (admin)
setx MY_VAR "value" /m

REM Ajouter au PATH
setx PATH "%PATH%;C:\newpath"
```

## Redirection et pipes

```cmd
REM Redirection sortie (écrase)
command > output.txt

REM Ajouter
command >> output.txt

REM Redirection erreur
command 2> errors.txt

REM Tout rediriger
command > output.txt 2>&1

REM Supprimer sortie
command > nul

REM Redirection entrée
command < input.txt

REM Pipe
command1 | command2

REM Exemples
dir > list.txt
dir >> list.txt
dir | find ".txt"
type file.txt | findstr "error"
```

## Batch scripting

### Basique

```cmd
@echo off
REM Commentaire

REM Variables
set NAME=Alice
echo Hello %NAME%

REM Input utilisateur
set /p ANSWER=Question:
echo Vous avez dit: %ANSWER%

REM If
if "%NAME%"=="Alice" (
    echo Hello Alice
) else (
    echo Who are you?
)

REM If exist
if exist file.txt (
    echo File exists
)

REM For loop
for %%i in (1 2 3 4 5) do (
    echo %%i
)

REM For files
for %%f in (*.txt) do (
    echo %%f
)

REM Goto
:start
echo Loop
goto start
```

### Arguments

```cmd
@echo off
REM %1, %2, etc. = arguments
echo First arg: %1
echo Second arg: %2
echo All args: %*

REM Shift arguments
shift
echo New first: %1
```

## Outils système

### reg

Registre Windows.

```cmd
REM Lire clé
reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion"

REM Ajouter valeur
reg add "HKEY_CURRENT_USER\Software\MyApp" /v Setting /t REG_SZ /d "value"

REM Supprimer
reg delete "HKEY_CURRENT_USER\Software\MyApp" /v Setting /f

REM Exporter
reg export "HKEY_CURRENT_USER\Software\MyApp" backup.reg

REM Importer
reg import backup.reg
```

### sc

Services.

```cmd
REM Liste services
sc query

REM Info service
sc query servicename

REM Démarrer
sc start servicename

REM Arrêter
sc stop servicename

REM Configurer
sc config servicename start= auto

REM Créer service
sc create servicename binpath= "C:\path\to\service.exe"

REM Supprimer
sc delete servicename
```

### wmic

WMI Command.

```cmd
REM Info système
wmic computersystem get model,name,manufacturer

REM Info CPU
wmic cpu get name,maxclockspeed

REM Info RAM
wmic memorychip get capacity,speed

REM Info disque
wmic diskdrive get model,size

REM Processus
wmic process list brief
wmic process where name="chrome.exe" list full

REM Services
wmic service list brief
```

## Raccourcis clavier

```
Ctrl + C : Interrompre commande
Ctrl + Break : Pause
Tab : Auto-complétion
↑ / ↓ : Historique
F7 : Liste historique
F8 : Recherche historique
F9 : Numéro historique
Ctrl + V : Coller (récent)
```

## Bonnes pratiques

```cmd
REM ✅ Désactiver echo dans scripts
@echo off

REM ✅ Vérifier erreurs
if errorlevel 1 (
    echo Error occurred
    exit /b 1
)

REM ✅ Commenter code
REM This is a comment

REM ✅ Utiliser quotes pour paths avec espaces
cd "C:\Program Files"

REM ✅ Pause à la fin des scripts (debug)
pause

REM ❌ Ne pas utiliser del /s /q C:\
REM ❌ Vérifier paths avant suppression
REM ❌ Attention avec /f (force)
```

[← Linux Processus](./infos-terminal-05-linux-processus.md) | [Index](./infos-terminal-00-index.md) | [PowerShell →](./infos-terminal-07-windows-powershell.md)

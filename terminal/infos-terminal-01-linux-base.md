# 🐧 Commandes Linux de Base

[Index](./infos-terminal-00-index.md) | [Linux Avancées →](./infos-terminal-02-linux-avancees.md)

## Navigation

### pwd - Print Working Directory

Affiche le répertoire courant.

```bash
pwd
# /home/user/documents
```

### cd - Change Directory

Changer de répertoire.

```bash
# Aller dans un dossier
cd /home/user/documents

# Revenir au répertoire parent
cd ..

# Remonter de 2 niveaux
cd ../..

# Aller au répertoire home
cd ~
cd

# Revenir au répertoire précédent
cd -

# Aller au répertoire racine
cd /
```

### ls - List

Lister les fichiers et dossiers.

```bash
# Liste simple
ls

# Liste détaillée
ls -l

# Afficher fichiers cachés
ls -a

# Liste détaillée avec fichiers cachés
ls -la
ls -lah  # h = human readable (tailles lisibles)

# Trier par date (plus récent en premier)
ls -lt

# Trier par taille
ls -lS

# Liste récursive
ls -R

# Avec couleurs
ls --color=auto
```

## Gestion des fichiers

### touch

Créer un fichier vide ou modifier la date.

```bash
# Créer un fichier
touch fichier.txt

# Créer plusieurs fichiers
touch file1.txt file2.txt file3.txt

# Créer fichiers avec pattern
touch file{1..10}.txt
```

### cat - Concatenate

Afficher le contenu d'un fichier.

```bash
# Afficher un fichier
cat fichier.txt

# Afficher plusieurs fichiers
cat file1.txt file2.txt

# Afficher avec numéros de ligne
cat -n fichier.txt

# Créer un fichier avec contenu
cat > fichier.txt
Hello World
Ctrl+D (pour sauvegarder)

# Ajouter à un fichier
cat >> fichier.txt
Nouvelle ligne
Ctrl+D
```

### less / more

Afficher fichier page par page.

```bash
# Afficher avec less (recommandé)
less fichier.txt
# q pour quitter
# / pour rechercher
# n pour occurence suivante

# Afficher avec more
more fichier.txt
# Espace pour page suivante
```

### head / tail

Afficher début ou fin de fichier.

```bash
# 10 premières lignes (défaut)
head fichier.txt

# 20 premières lignes
head -n 20 fichier.txt
head -20 fichier.txt

# 10 dernières lignes
tail fichier.txt

# 20 dernières lignes
tail -n 20 fichier.txt

# Suivre fichier en temps réel (logs)
tail -f fichier.log

# Suivre avec retry si fichier supprimé
tail -F fichier.log
```

### cp - Copy

Copier fichiers/dossiers.

```bash
# Copier fichier
cp source.txt destination.txt

# Copier vers un dossier
cp fichier.txt /home/user/backup/

# Copier plusieurs fichiers
cp file1.txt file2.txt /destination/

# Copier dossier (récursif)
cp -r dossier/ /destination/

# Copier avec confirmation
cp -i source.txt dest.txt

# Copier en préservant attributs
cp -p source.txt dest.txt

# Copier verbose
cp -v source.txt dest.txt
```

### mv - Move

Déplacer ou renommer fichiers/dossiers.

```bash
# Renommer fichier
mv ancien.txt nouveau.txt

# Déplacer fichier
mv fichier.txt /destination/

# Déplacer plusieurs fichiers
mv file1.txt file2.txt /destination/

# Déplacer dossier
mv dossier/ /destination/

# Avec confirmation
mv -i source.txt dest.txt

# Verbose
mv -v source.txt dest.txt
```

### rm - Remove

Supprimer fichiers/dossiers.

```bash
# Supprimer fichier
rm fichier.txt

# Supprimer plusieurs fichiers
rm file1.txt file2.txt

# Supprimer avec confirmation
rm -i fichier.txt

# Supprimer dossier vide
rmdir dossier/

# Supprimer dossier et contenu (récursif)
rm -r dossier/

# Force suppression (attention !)
rm -rf dossier/

# Supprimer verbose
rm -v fichier.txt

# Supprimer tous les fichiers .txt
rm *.txt

# Supprimer en interactive
rm -ri dossier/
```

### mkdir - Make Directory

Créer des dossiers.

```bash
# Créer un dossier
mkdir nouveau_dossier

# Créer plusieurs dossiers
mkdir dossier1 dossier2 dossier3

# Créer avec sous-dossiers
mkdir -p parent/enfant/petit-enfant

# Créer avec permissions spécifiques
mkdir -m 755 dossier

# Verbose
mkdir -v dossier
```

## Recherche

### find

Rechercher fichiers et dossiers.

```bash
# Rechercher par nom
find . -name "fichier.txt"

# Rechercher insensible à la casse
find . -iname "fichier.txt"

# Rechercher tous les .txt
find . -name "*.txt"

# Rechercher dossiers uniquement
find . -type d -name "dossier"

# Rechercher fichiers uniquement
find . -type f -name "*.txt"

# Rechercher fichiers modifiés il y a moins de 7 jours
find . -type f -mtime -7

# Rechercher fichiers plus grands que 100MB
find . -type f -size +100M

# Rechercher et supprimer
find . -name "*.tmp" -delete

# Rechercher et exécuter commande
find . -name "*.txt" -exec cat {} \;
```

### grep

Rechercher dans le contenu des fichiers.

```bash
# Rechercher dans un fichier
grep "texte" fichier.txt

# Insensible à la casse
grep -i "texte" fichier.txt

# Rechercher récursivement
grep -r "texte" .

# Afficher numéros de ligne
grep -n "texte" fichier.txt

# Afficher nombre d'occurrences
grep -c "texte" fichier.txt

# Inverser recherche (lignes ne contenant PAS)
grep -v "texte" fichier.txt

# Rechercher mot entier
grep -w "mot" fichier.txt

# Multiple patterns
grep -e "pattern1" -e "pattern2" fichier.txt

# Avec contexte (3 lignes avant et après)
grep -C 3 "texte" fichier.txt
grep -B 3 "texte" fichier.txt  # Avant
grep -A 3 "texte" fichier.txt  # Après

# Regex
grep "^Start" fichier.txt  # Ligne commence par
grep "End$" fichier.txt    # Ligne finit par
```

### locate

Recherche rapide dans base de données.

```bash
# Rechercher fichier
locate fichier.txt

# Insensible à la casse
locate -i fichier.txt

# Mettre à jour base de données
sudo updatedb

# Limiter résultats
locate -n 10 fichier.txt
```

### which

Trouver emplacement d'une commande.

```bash
# Trouver commande
which python
# /usr/bin/python

which python3
# /usr/bin/python3

# Toutes les localisations
which -a python
```

### whereis

Trouver binaire, source et manuel.

```bash
whereis python
# python: /usr/bin/python /usr/lib/python /usr/share/man/man1/python.1.gz
```

## Affichage et édition

### echo

Afficher du texte.

```bash
# Afficher texte
echo "Hello World"

# Sans retour à la ligne
echo -n "Hello"

# Avec variables
NAME="Alice"
echo "Hello $NAME"

# Redirection vers fichier
echo "Hello" > fichier.txt

# Ajouter à fichier
echo "World" >> fichier.txt
```

### nano

Éditeur de texte simple.

```bash
# Ouvrir fichier
nano fichier.txt

# Raccourcis:
# Ctrl+O : Sauvegarder
# Ctrl+X : Quitter
# Ctrl+K : Couper ligne
# Ctrl+U : Coller
# Ctrl+W : Rechercher
# Ctrl+\ : Remplacer
```

### vim

Éditeur de texte avancé.

```bash
# Ouvrir fichier
vim fichier.txt

# Modes:
# i : Mode insertion
# Esc : Mode commande
# :w : Sauvegarder
# :q : Quitter
# :wq : Sauvegarder et quitter
# :q! : Quitter sans sauvegarder

# Commandes utiles:
# dd : Supprimer ligne
# yy : Copier ligne
# p : Coller
# /texte : Rechercher
# n : Occurence suivante
```

## Permissions

### chmod - Change Mode

Modifier permissions.

```bash
# Format numérique (rwx = 421)
chmod 755 fichier.sh  # rwxr-xr-x
chmod 644 fichier.txt # rw-r--r--
chmod 600 fichier.txt # rw-------

# Format symbolique
chmod u+x fichier.sh    # Ajouter exécution pour user
chmod g+w fichier.txt   # Ajouter écriture pour groupe
chmod o-r fichier.txt   # Retirer lecture pour autres
chmod a+x fichier.sh    # Ajouter exécution pour tous

# Récursif
chmod -R 755 dossier/

# Référence
# u = user, g = group, o = others, a = all
# + = ajouter, - = retirer, = = définir
# r = read (4), w = write (2), x = execute (1)
```

### chown - Change Owner

Changer propriétaire.

```bash
# Changer propriétaire
sudo chown user fichier.txt

# Changer propriétaire et groupe
sudo chown user:group fichier.txt

# Récursif
sudo chown -R user:group dossier/

# Changer uniquement le groupe
sudo chgrp group fichier.txt
```

## Information système

### whoami

Afficher nom utilisateur actuel.

```bash
whoami
# user
```

### hostname

Afficher nom de la machine.

```bash
hostname
# my-computer

# Afficher nom complet
hostname -f
```

### uname

Informations système.

```bash
# Nom système
uname
# Linux

# Toutes les infos
uname -a

# Nom kernel
uname -s

# Version kernel
uname -r

# Architecture
uname -m
# x86_64
```

### date

Afficher/modifier date et heure.

```bash
# Date actuelle
date
# Fri Jan 10 14:30:00 UTC 2025

# Format personnalisé
date +"%Y-%m-%d"
# 2025-01-10

date +"%Y-%m-%d %H:%M:%S"
# 2025-01-10 14:30:00

date +"%d/%m/%Y"
# 10/01/2025

# Timestamp
date +%s
# 1704896400
```

### cal - Calendar

Afficher calendrier.

```bash
# Mois actuel
cal

# Année complète
cal 2025

# Mois spécifique
cal 12 2025

# 3 mois
cal -3
```

### df - Disk Free

Espace disque.

```bash
# Espace disque
df

# Format lisible
df -h

# Système de fichiers spécifique
df -h /

# Type filesystem
df -T
```

### du - Disk Usage

Utilisation disque.

```bash
# Taille dossier
du -sh dossier/

# Détails sous-dossiers
du -h dossier/

# Top 10 plus gros dossiers
du -h | sort -rh | head -10
```

### free

Mémoire disponible.

```bash
# Mémoire
free

# Format lisible
free -h

# En MB
free -m

# En GB
free -g
```

## Aide

### man - Manual

Afficher manuel d'une commande.

```bash
# Manuel d'une commande
man ls
man grep

# Rechercher dans les manuels
man -k keyword

# Sections
man 1 printf  # Commande
man 3 printf  # Fonction C
```

### help

Aide intégrée bash.

```bash
# Aide commande bash
help cd
help echo

# Aide commande externe
ls --help
grep --help
```

### info

Documentation détaillée.

```bash
# Info d'une commande
info ls
info grep
```

## Redirection et pipes

### Redirection de sortie

```bash
# Rediriger stdout vers fichier (écrase)
ls > fichiers.txt

# Ajouter à fichier
ls >> fichiers.txt

# Rediriger stderr
command 2> errors.txt

# Rediriger stdout et stderr
command > output.txt 2>&1
command &> output.txt  # Raccourci

# Supprimer sortie
command > /dev/null
command &> /dev/null
```

### Redirection d'entrée

```bash
# Lire depuis fichier
command < input.txt

# Here document
cat << EOF
Ligne 1
Ligne 2
EOF

# Here string
grep "text" <<< "some text here"
```

### Pipes (|)

```bash
# Enchaîner commandes
ls | grep ".txt"

# Multiple pipes
cat fichier.txt | grep "error" | wc -l

# Avec tee (affiche ET sauvegarde)
ls | tee fichiers.txt

# Append avec tee
ls | tee -a fichiers.txt
```

## Chaînage de commandes

```bash
# ET logique (exécute si précédente réussit)
mkdir dossier && cd dossier

# OU logique (exécute si précédente échoue)
cd /tmp || cd ~

# Séquentiel (toujours exécute suivante)
command1 ; command2 ; command3

# En arrière-plan
command &

# Pipeline
command1 | command2 | command3
```

## Wildcards (caractères joker)

```bash
# * = n'importe quels caractères
ls *.txt        # Tous les .txt
rm file*        # Tous les fichiers commençant par "file"

# ? = un caractère
ls file?.txt    # file1.txt, fileA.txt, etc.

# [] = ensemble de caractères
ls file[123].txt    # file1.txt, file2.txt, file3.txt
ls file[a-z].txt    # filea.txt, fileb.txt, etc.

# {} = alternatives
cp file.{txt,bak}   # Copie file.txt et file.bak
mv file{,.bak}      # Renomme file en file.bak
```

## Historique

```bash
# Afficher historique
history

# Afficher 20 dernières commandes
history 20

# Exécuter commande du historique
!100    # Commande numéro 100
!!      # Dernière commande
!-2     # Avant-dernière commande

# Rechercher dans historique
Ctrl+R
# Taper début de commande

# Effacer historique
history -c
```

## Variables d'environnement

```bash
# Afficher toutes les variables
env
printenv

# Afficher variable spécifique
echo $HOME
echo $PATH
echo $USER

# Définir variable (session actuelle)
MY_VAR="valeur"
echo $MY_VAR

# Export (disponible pour sous-processus)
export MY_VAR="valeur"

# Variables communes:
# $HOME : Répertoire home
# $USER : Nom utilisateur
# $PATH : Chemins pour commandes
# $PWD  : Répertoire courant
# $SHELL : Shell par défaut
```

[Index](./infos-terminal-00-index.md) | [Linux Avancées →](./infos-terminal-02-linux-avancees.md)

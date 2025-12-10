# 🚀 Introduction et Installation

[Index](./infos-python-00-index.md) | [Bases →](./infos-python-02-bases-python.md)

## Qu'est-ce que Python ?

Python est un langage de programmation :
- 🐍 **Interprété** : pas de compilation nécessaire
- 📝 **Syntaxe claire** : facile à lire et écrire
- 🔧 **Polyvalent** : web, data science, IA, automation, etc.
- 📦 **Riche écosystème** : des milliers de bibliothèques
- 🌍 **Multi-plateforme** : Windows, macOS, Linux

## Installation

### Windows

```powershell
# Télécharger depuis python.org
# https://www.python.org/downloads/

# Ou avec winget
winget install Python.Python.3.11

# Ou avec Chocolatey
choco install python

# Vérifier
python --version
pip --version
```

### macOS

```bash
# Avec Homebrew
brew install python@3.11

# Vérifier
python3 --version
pip3 --version
```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip

# Vérifier
python3 --version
pip3 --version
```

## Environnements virtuels

### Pourquoi ?

- ✅ Isoler les dépendances par projet
- ✅ Éviter les conflits de versions
- ✅ Faciliter le déploiement

### venv (intégré)

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Installer des packages
pip install requests

# Désactiver
deactivate
```

### virtualenv

```bash
# Installer
pip install virtualenv

# Créer
virtualenv venv

# Activer (même commandes que venv)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### pyenv (gestion de versions Python)

```bash
# macOS/Linux
curl https://pyenv.run | bash

# Installer une version
pyenv install 3.11.0

# Utiliser globalement
pyenv global 3.11.0

# Utiliser localement (projet)
pyenv local 3.11.0

# Lister versions
pyenv versions
```

## pip (gestionnaire de packages)

### Commandes de base

```bash
# Installer un package
pip install requests

# Version spécifique
pip install requests==2.28.0

# Mise à jour
pip install --upgrade requests

# Désinstaller
pip uninstall requests

# Lister les packages installés
pip list

# Packages obsolètes
pip list --outdated

# Infos sur un package
pip show requests
```

### requirements.txt

```bash
# Générer
pip freeze > requirements.txt

# Installer depuis requirements.txt
pip install -r requirements.txt
```

```txt
# requirements.txt
requests==2.28.0
flask==2.3.0
django==4.2.0
streamlit==1.25.0
```

## Premier programme

### Hello World

```python
# hello.py
print("Hello, World!")
```

```bash
python hello.py
```

### Variables et types

```python
# Variables
name = "Alice"
age = 25
height = 1.75
is_student = True

print(f"{name} a {age} ans")
```

### Input utilisateur

```python
# input.py
name = input("Comment t'appelles-tu ? ")
age = input("Quel âge as-tu ? ")

print(f"Bonjour {name}, tu as {age} ans !")
```

## IDE et éditeurs

### VS Code (recommandé)

```bash
# Installer VS Code
# https://code.visualstudio.com/

# Extensions recommandées
# Python (Microsoft)
# Pylance
# Python Indent
# autoDocstring
```

### PyCharm

```bash
# Version Community gratuite
# https://www.jetbrains.com/pycharm/
```

### Jupyter Notebook

```bash
# Installer
pip install jupyter

# Lancer
jupyter notebook

# Ou JupyterLab
pip install jupyterlab
jupyter lab
```

## Configuration Python

### .python-version

```bash
# pyenv
echo "3.11.0" > .python-version
```

### pyproject.toml

```toml
[project]
name = "mon-projet"
version = "1.0.0"
description = "Mon projet Python"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28.0",
    "flask>=2.3.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

### setup.py (legacy)

```python
from setuptools import setup, find_packages

setup(
    name="mon-projet",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "flask>=2.3.0",
    ],
)
```

## Outils de développement

### Black (formatage)

```bash
# Installer
pip install black

# Formater
black .

# Vérifier sans modifier
black --check .
```

### flake8 (linting)

```bash
# Installer
pip install flake8

# Linter
flake8 .

# Configuration : .flake8
[flake8]
max-line-length = 88
exclude = venv,__pycache__
```

### pylint

```bash
# Installer
pip install pylint

# Linter
pylint mon_module.py
```

### mypy (type checking)

```bash
# Installer
pip install mypy

# Vérifier
mypy .

# Configuration : mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
```

### isort (tri des imports)

```bash
# Installer
pip install isort

# Trier
isort .

# Configuration : .isort.cfg
[settings]
profile = black
```

## Poetry (gestionnaire moderne)

### Installation

```bash
# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Windows
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Utilisation

```bash
# Créer un projet
poetry new mon-projet

# Initialiser dans projet existant
poetry init

# Ajouter une dépendance
poetry add requests

# Installer
poetry install

# Activer l'environnement
poetry shell

# Exécuter une commande
poetry run python script.py
```

### pyproject.toml (Poetry)

```toml
[tool.poetry]
name = "mon-projet"
version = "0.1.0"
description = "Mon projet Python"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.28.0"
flask = "^2.3.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
flake8 = "^6.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Structure de projet

### Projet simple

```
mon-projet/
├── venv/
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── requirements.txt
└── README.md
```

### Projet package

```
mon-projet/
├── venv/
├── mon_package/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   ├── __init__.py
│   └── test_module1.py
├── setup.py
├── requirements.txt
└── README.md
```

### Projet complet

```
mon-projet/
├── venv/
├── src/
│   └── mon_package/
│       ├── __init__.py
│       └── core/
├── tests/
├── docs/
├── scripts/
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
└── LICENSE
```

## .gitignore Python

```gitignore
# Environnements virtuels
venv/
env/
ENV/
.venv

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Distribution
build/
dist/
*.egg-info/
.eggs/

# Tests
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp

# Env
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

## Commandes utiles

```bash
# Version Python
python --version

# REPL interactif
python

# Exécuter un script
python script.py

# Exécuter un module
python -m module_name

# Installer package en mode dev
pip install -e .

# Créer un package
python -m build

# Upload sur PyPI
python -m twine upload dist/*
```

## Premiers pas

### Variables et types

```python
# Types de base
x = 5           # int
y = 3.14        # float
name = "Alice"  # str
is_valid = True # bool

# Listes
numbers = [1, 2, 3, 4, 5]
fruits = ["pomme", "banane", "orange"]

# Dictionnaires
person = {
    "name": "Alice",
    "age": 25,
    "city": "Paris"
}

# Tuples (immuables)
coordinates = (10, 20)
```

### Fonctions

```python
def greet(name):
    return f"Bonjour, {name} !"

result = greet("Alice")
print(result)  # Bonjour, Alice !
```

### Conditions

```python
age = 18

if age >= 18:
    print("Majeur")
else:
    print("Mineur")
```

### Boucles

```python
# For
for i in range(5):
    print(i)

# While
count = 0
while count < 5:
    print(count)
    count += 1

# Itérer sur liste
fruits = ["pomme", "banane", "orange"]
for fruit in fruits:
    print(fruit)
```

[Index](./infos-python-00-index.md) | [Bases →](./infos-python-02-bases-python.md)

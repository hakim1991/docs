# 📦 Modules et Packages

[← Bases](./infos-python-02-bases-python.md) | [Index](./infos-python-00-index.md) | [POO →](./infos-python-04-poo.md)

## Modules

Un module est un fichier Python `.py`.

### Créer un module

```python
# math_utils.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

PI = 3.14159
```

### Importer un module

```python
# main.py
import math_utils

result = math_utils.add(5, 3)
print(math_utils.PI)
```

### Import spécifique

```python
from math_utils import add, PI

result = add(5, 3)
print(PI)
```

### Import avec alias

```python
import math_utils as mu

result = mu.add(5, 3)
```

```python
from math_utils import add as addition

result = addition(5, 3)
```

### Import tout (déconseillé)

```python
from math_utils import *

result = add(5, 3)
```

## Packages

Un package est un dossier contenant un fichier `__init__.py`.

### Structure

```
mon_package/
├── __init__.py
├── module1.py
├── module2.py
└── sub_package/
    ├── __init__.py
    └── module3.py
```

### __init__.py

```python
# mon_package/__init__.py
from .module1 import function1
from .module2 import function2

__version__ = "1.0.0"
```

### Importer depuis un package

```python
# Import package
import mon_package

# Import module
from mon_package import module1

# Import fonction
from mon_package.module1 import function1

# Import sous-package
from mon_package.sub_package import module3
```

## Imports relatifs

```python
# Dans mon_package/module1.py

# Import depuis même niveau
from .module2 import function2

# Import depuis parent
from ..autre_package import something

# Import depuis sous-package
from .sub_package.module3 import function3
```

## Modules built-in

### math

```python
import math

math.pi           # 3.141592653589793
math.e            # 2.718281828459045
math.sqrt(16)     # 4.0
math.pow(2, 3)    # 8.0
math.ceil(3.2)    # 4
math.floor(3.8)   # 3
math.sin(math.pi/2)  # 1.0
math.cos(0)       # 1.0
```

### random

```python
import random

random.random()              # Float entre 0 et 1
random.randint(1, 10)        # Int entre 1 et 10
random.choice([1, 2, 3])     # Choisir dans liste
random.shuffle(liste)        # Mélanger liste
random.sample([1,2,3,4], 2)  # 2 éléments aléatoires
```

### datetime

```python
from datetime import datetime, date, time, timedelta

# Date actuelle
now = datetime.now()
today = date.today()

# Créer date
birthday = date(1990, 5, 15)
meeting = datetime(2024, 1, 15, 14, 30)

# Formater
now.strftime("%Y-%m-%d %H:%M:%S")
now.strftime("%d/%m/%Y")

# Parser
date_str = "2024-01-15"
parsed = datetime.strptime(date_str, "%Y-%m-%d")

# Opérations
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)
two_hours_later = now + timedelta(hours=2)
```

### json

```python
import json

# Dict → JSON string
data = {"name": "Alice", "age": 25}
json_str = json.dumps(data)
json_str = json.dumps(data, indent=2)  # Formaté

# JSON string → Dict
data = json.loads(json_str)

# Fichier → Dict
with open("data.json") as f:
    data = json.load(f)

# Dict → Fichier
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
```

### os

```python
import os

# Répertoire courant
os.getcwd()

# Changer répertoire
os.chdir("/path/to/dir")

# Lister fichiers
os.listdir(".")

# Créer dossier
os.mkdir("new_dir")
os.makedirs("path/to/dir", exist_ok=True)

# Supprimer
os.remove("file.txt")
os.rmdir("dir")

# Path operations
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("dir")
os.path.join("path", "to", "file.txt")
os.path.basename("/path/to/file.txt")  # file.txt
os.path.dirname("/path/to/file.txt")   # /path/to
```

### sys

```python
import sys

# Arguments ligne de commande
print(sys.argv)  # ['script.py', 'arg1', 'arg2']

# Version Python
print(sys.version)

# Chemin des modules
print(sys.path)

# Sortie du programme
sys.exit(0)
```

### pathlib (moderne)

```python
from pathlib import Path

# Créer Path
path = Path("data/file.txt")
path = Path.home() / "Documents" / "file.txt"

# Propriétés
path.exists()
path.is_file()
path.is_dir()
path.name        # file.txt
path.stem        # file
path.suffix      # .txt
path.parent      # data/

# Opérations
path.mkdir(parents=True, exist_ok=True)
path.unlink()    # Supprimer fichier
path.rmdir()     # Supprimer dossier

# Lister
for item in path.iterdir():
    print(item)

# Glob
for txt_file in path.glob("*.txt"):
    print(txt_file)
```

### collections

```python
from collections import Counter, defaultdict, namedtuple

# Counter
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
counter = Counter(words)
# Counter({'apple': 3, 'banana': 2, 'orange': 1})
counter.most_common(2)  # [('apple', 3), ('banana', 2)]

# defaultdict
d = defaultdict(list)
d["fruits"].append("apple")  # Pas d'erreur si clé absente

d = defaultdict(int)
for word in words:
    d[word] += 1

# namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x, p.y)
```

### itertools

```python
from itertools import count, cycle, repeat, chain, combinations, permutations

# Générateurs infinis
count(10)        # 10, 11, 12, 13, ...
cycle([1, 2, 3]) # 1, 2, 3, 1, 2, 3, ...
repeat(10, 3)    # 10, 10, 10

# Combinaisons
list(combinations([1, 2, 3], 2))    # [(1, 2), (1, 3), (2, 3)]
list(permutations([1, 2, 3], 2))    # [(1, 2), (1, 3), (2, 1), ...]

# Chain
list(chain([1, 2], [3, 4], [5, 6])) # [1, 2, 3, 4, 5, 6]
```

### re (regex)

```python
import re

# Recherche
match = re.search(r'\d+', 'User123')
if match:
    print(match.group())  # '123'

# Findall
numbers = re.findall(r'\d+', 'abc123def456')  # ['123', '456']

# Replace
text = re.sub(r'\d+', 'X', 'abc123def456')    # 'abcXdefX'

# Split
parts = re.split(r'\s+', 'hello   world')     # ['hello', 'world']

# Match
if re.match(r'^\d+$', '123'):
    print("Que des chiffres")

# Compile (pour réutiliser)
pattern = re.compile(r'\d+')
pattern.findall('abc123def456')
```

## Packages tiers populaires

### requests (HTTP)

```bash
pip install requests
```

```python
import requests

# GET
response = requests.get('https://api.example.com/users')
data = response.json()
print(response.status_code)

# POST
data = {"name": "Alice", "age": 25}
response = requests.post('https://api.example.com/users', json=data)

# Headers
headers = {"Authorization": "Bearer token"}
response = requests.get(url, headers=headers)
```

### pandas (data)

```bash
pip install pandas
```

```python
import pandas as pd

# Créer DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["Paris", "Lyon", "Marseille"]
})

# Lire CSV
df = pd.read_csv("data.csv")

# Manipulations
df.head()
df.info()
df.describe()
df["age"].mean()
df[df["age"] > 25]
df.sort_values("age")
```

### numpy (calcul numérique)

```bash
pip install numpy
```

```python
import numpy as np

# Arrays
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4]])

# Opérations
arr + 10
arr * 2
arr ** 2
np.mean(arr)
np.std(arr)
```

## __name__ == "__main__"

```python
# module.py
def main():
    print("Programme principal")

def helper():
    print("Fonction auxiliaire")

if __name__ == "__main__":
    main()
```

Quand exécuté directement : `python module.py`
- `__name__` = `"__main__"` → main() est exécuté

Quand importé : `import module`
- `__name__` = `"module"` → main() n'est pas exécuté

## Créer un package installable

### Structure

```
mon_package/
├── mon_package/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   └── test_module1.py
├── setup.py
├── README.md
└── LICENSE
```

### setup.py

```python
from setuptools import setup, find_packages

setup(
    name="mon_package",
    version="1.0.0",
    author="Your Name",
    author_email="you@example.com",
    description="Description courte",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/mon_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "pandas>=1.5.0",
    ],
)
```

### Installation

```bash
# Mode développement
pip install -e .

# Build
python -m build

# Upload PyPI
python -m twine upload dist/*
```

## Bonnes pratiques

1. **Un fichier = un module** : gardez les fichiers courts
2. **Imports en haut** : toujours au début du fichier
3. **Imports absolus** : préférer aux imports relatifs
4. **__all__** : contrôler ce qui est exporté
5. **Documentation** : docstrings pour modules et fonctions

```python
# module.py
"""
Module pour les opérations mathématiques.

Ce module fournit des fonctions de base pour
les calculs mathématiques.
"""

__all__ = ["add", "subtract"]  # Exporter uniquement ces fonctions

def add(a, b):
    """Additionne deux nombres."""
    return a + b
```

[← Bases](./infos-python-02-bases-python.md) | [Index](./infos-python-00-index.md) | [POO →](./infos-python-04-poo.md)

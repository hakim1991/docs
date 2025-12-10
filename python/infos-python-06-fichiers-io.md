# 📁 Fichiers et I/O

[← Erreurs](./infos-python-05-gestion-erreurs.md) | [Index](./infos-python-00-index.md) | [Streamlit →](./infos-python-07-streamlit.md)

## Lire des fichiers

### Mode texte

```python
# Lire tout
with open("file.txt", "r") as f:
    content = f.read()

# Lire ligne par ligne
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())

# Lire dans une liste
with open("file.txt", "r") as f:
    lines = f.readlines()

# Lire N caractères
with open("file.txt", "r") as f:
    chunk = f.read(100)
```

### Encodage

```python
# UTF-8 (défaut)
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Latin-1
with open("file.txt", "r", encoding="latin-1") as f:
    content = f.read()
```

## Écrire des fichiers

```python
# Écraser (mode 'w')
with open("output.txt", "w") as f:
    f.write("Hello\n")
    f.write("World\n")

# Ajouter (mode 'a')
with open("output.txt", "a") as f:
    f.write("New line\n")

# Écrire liste
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)
```

## Modes d'ouverture

```python
"r"   # Lecture (défaut)
"w"   # Écriture (écrase)
"a"   # Ajout
"x"   # Création (erreur si existe)
"r+"  # Lecture/Écriture
"w+"  # Lecture/Écriture (écrase)
"a+"  # Lecture/Ajout

# Binaire
"rb"  # Lecture binaire
"wb"  # Écriture binaire
```

## Fichiers binaires

```python
# Lire
with open("image.jpg", "rb") as f:
    data = f.read()

# Écrire
with open("copy.jpg", "wb") as f:
    f.write(data)
```

## JSON

```python
import json

# Écrire JSON
data = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "JavaScript"]
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Lire JSON
with open("data.json", "r") as f:
    data = json.load(f)

# String → Dict
json_str = '{"name": "Alice", "age": 25}'
data = json.loads(json_str)

# Dict → String
data = {"name": "Alice"}
json_str = json.dumps(data, indent=2)
```

## CSV

```python
import csv

# Lire CSV
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# Lire avec DictReader
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])

# Écrire CSV
data = [
    ["name", "age", "city"],
    ["Alice", 25, "Paris"],
    ["Bob", 30, "Lyon"]
]

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Écrire avec DictWriter
data = [
    {"name": "Alice", "age": 25, "city": "Paris"},
    {"name": "Bob", "age": 30, "city": "Lyon"}
]

with open("output.csv", "w", newline="") as f:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

## Fichiers YAML

```bash
pip install pyyaml
```

```python
import yaml

# Lire YAML
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Écrire YAML
data = {
    "database": {
        "host": "localhost",
        "port": 5432
    },
    "debug": True
}

with open("config.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False)
```

## Pickle (sérialisation Python)

```python
import pickle

# Sauvegarder
data = {"name": "Alice", "scores": [95, 87, 92]}
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Charger
with open("data.pkl", "rb") as f:
    data = pickle.load(f)
```

## pathlib

```python
from pathlib import Path

# Créer Path
path = Path("data/file.txt")
path = Path.home() / "Documents" / "file.txt"

# Propriétés
path.name        # file.txt
path.stem        # file
path.suffix      # .txt
path.parent      # data/
path.exists()
path.is_file()
path.is_dir()

# Lire/Écrire
text = path.read_text()
path.write_text("Hello World")
data = path.read_bytes()
path.write_bytes(b"\x00\x01")

# Créer dossier
path = Path("data")
path.mkdir(parents=True, exist_ok=True)

# Lister
for item in path.iterdir():
    print(item)

# Glob
for txt_file in path.glob("*.txt"):
    print(txt_file)

for py_file in path.rglob("**/*.py"):  # Récursif
    print(py_file)
```

## os et shutil

```python
import os
import shutil

# Créer dossier
os.mkdir("data")
os.makedirs("path/to/dir", exist_ok=True)

# Supprimer
os.remove("file.txt")
os.rmdir("dir")
shutil.rmtree("dir")  # Récursif

# Copier
shutil.copy("src.txt", "dst.txt")
shutil.copytree("src_dir", "dst_dir")

# Déplacer
shutil.move("src.txt", "dst.txt")

# Renommer
os.rename("old.txt", "new.txt")

# Lister
files = os.listdir(".")
for file in files:
    print(file)

# Walk (récursif)
for root, dirs, files in os.walk("path"):
    for file in files:
        filepath = os.path.join(root, file)
        print(filepath)
```

## Fichiers temporaires

```python
import tempfile

# Fichier temporaire
with tempfile.TemporaryFile(mode="w+") as f:
    f.write("Temporary data")
    f.seek(0)
    print(f.read())
# Supprimé automatiquement

# Fichier nommé
with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
    f.write("Data")
    temp_path = f.name
print(f"Fichier: {temp_path}")

# Dossier temporaire
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Dossier temp: {tmpdir}")
    # Utiliser tmpdir
# Supprimé automatiquement
```

## Compression

### ZIP

```python
import zipfile

# Créer ZIP
with zipfile.ZipFile("archive.zip", "w") as zipf:
    zipf.write("file1.txt")
    zipf.write("file2.txt")

# Lire ZIP
with zipfile.ZipFile("archive.zip", "r") as zipf:
    # Lister
    print(zipf.namelist())

    # Extraire tout
    zipf.extractall("extracted/")

    # Extraire un fichier
    zipf.extract("file1.txt", "extracted/")

    # Lire sans extraire
    with zipf.open("file1.txt") as f:
        content = f.read()
```

### TAR

```python
import tarfile

# Créer TAR.GZ
with tarfile.open("archive.tar.gz", "w:gz") as tar:
    tar.add("file1.txt")
    tar.add("file2.txt")

# Lire TAR.GZ
with tarfile.open("archive.tar.gz", "r:gz") as tar:
    # Lister
    print(tar.getnames())

    # Extraire tout
    tar.extractall("extracted/")

    # Extraire un fichier
    tar.extract("file1.txt", "extracted/")
```

## URLs et HTTP

```bash
pip install requests
```

```python
import requests

# GET
response = requests.get("https://api.example.com/data")
data = response.json()
print(response.status_code)
print(response.text)

# Télécharger fichier
response = requests.get("https://example.com/image.jpg")
with open("image.jpg", "wb") as f:
    f.write(response.content)

# Télécharger gros fichier (streaming)
response = requests.get(url, stream=True)
with open("large_file.zip", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

## Stdin/Stdout

```python
import sys

# Lire depuis stdin
for line in sys.stdin:
    print(line.strip().upper())

# Écrire vers stdout
sys.stdout.write("Message\n")

# Stderr
sys.stderr.write("Erreur\n")

# Arguments ligne de commande
import sys
print(sys.argv)  # ['script.py', 'arg1', 'arg2']

# argparse
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", default="output.txt")
args = parser.parse_args()
print(args.input)
```

## Bonnes pratiques

```python
# ✅ Utiliser with
with open("file.txt") as f:
    content = f.read()

# ❌ Sans with
f = open("file.txt")
content = f.read()
f.close()  # Peut être oublié

# ✅ pathlib (moderne)
from pathlib import Path
path = Path("data/file.txt")
content = path.read_text()

# ✅ Vérifier existence
if path.exists():
    content = path.read_text()

# ✅ Gérer erreurs
try:
    with open("file.txt") as f:
        content = f.read()
except FileNotFoundError:
    print("Fichier introuvable")
```

[← Erreurs](./infos-python-05-gestion-erreurs.md) | [Index](./infos-python-00-index.md) | [Streamlit →](./infos-python-07-streamlit.md)

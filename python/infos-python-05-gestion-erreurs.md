# 🛡️ Gestion des erreurs

[← POO](./infos-python-04-poo.md) | [Index](./infos-python-00-index.md) | [Fichiers →](./infos-python-06-fichiers-io.md)

## Exceptions

### try/except

```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("Division par zéro !")
```

### Plusieurs exceptions

```python
try:
    value = int(input("Entrez un nombre: "))
    result = 10 / value
except ValueError:
    print("Pas un nombre valide")
except ZeroDivisionError:
    print("Division par zéro")
```

### Capturer dans une variable

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Erreur: {e}")
```

### Exception générique

```python
try:
    # Code risqué
    risky_operation()
except Exception as e:
    print(f"Erreur: {e}")
```

### else et finally

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("Fichier introuvable")
else:
    print("Fichier lu avec succès")  # Si pas d'erreur
finally:
    file.close()  # Toujours exécuté
```

## Lever des exceptions

### raise

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Le diviseur ne peut pas être zéro")
    return a / b

try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Erreur: {e}")
```

### Re-lever une exception

```python
try:
    risky_operation()
except ValueError as e:
    print(f"Erreur capturée: {e}")
    raise  # Re-lever l'exception
```

## Exceptions personnalisées

```python
class InvalidAgeError(Exception):
    """Exception levée quand l'âge est invalide."""
    pass

class UserNotFoundError(Exception):
    """Exception levée quand l'utilisateur n'existe pas."""
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"Utilisateur {user_id} introuvable")

def set_age(age):
    if age < 0 or age > 150:
        raise InvalidAgeError(f"Âge invalide: {age}")
    return age

try:
    set_age(-5)
except InvalidAgeError as e:
    print(f"Erreur: {e}")
```

## Exceptions courantes

```python
# ValueError : valeur incorrecte
int("abc")  # ValueError

# TypeError : type incorrect
"2" + 2  # TypeError

# KeyError : clé inexistante
d = {"a": 1}
d["b"]  # KeyError

# IndexError : index hors limites
liste = [1, 2, 3]
liste[10]  # IndexError

# AttributeError : attribut inexistant
obj.nonexistent_attr  # AttributeError

# FileNotFoundError : fichier introuvable
open("inexistant.txt")  # FileNotFoundError

# ZeroDivisionError : division par zéro
10 / 0  # ZeroDivisionError

# ImportError : module introuvable
import nonexistent_module  # ImportError

# RuntimeError : erreur d'exécution générique
```

## Context managers (with)

```python
# Sans with
file = open("data.txt", "r")
try:
    content = file.read()
finally:
    file.close()

# Avec with (recommandé)
with open("data.txt", "r") as file:
    content = file.read()
# Fichier fermé automatiquement
```

## Assertions

```python
def divide(a, b):
    assert b != 0, "Le diviseur ne peut pas être zéro"
    return a / b

# En développement
assert len(users) > 0, "Liste d'utilisateurs vide"

# Désactiver en production
python -O script.py  # Désactive les assertions
```

## Logging

```python
import logging

# Configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

# Niveaux
logging.debug("Message de debug")
logging.info("Information")
logging.warning("Avertissement")
logging.error("Erreur")
logging.critical("Erreur critique")

# Avec exception
try:
    risky_operation()
except Exception as e:
    logging.error("Erreur dans risky_operation", exc_info=True)
```

### Logger personnalisé

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Handler fichier
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Utilisation
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

## Traceback

```python
import traceback

try:
    risky_operation()
except Exception as e:
    # Afficher traceback complet
    traceback.print_exc()

    # Obtenir traceback en string
    tb_str = traceback.format_exc()
    print(tb_str)
```

## Bonnes pratiques

```python
# ✅ Spécifique
try:
    value = int(input())
except ValueError:
    print("Pas un nombre")

# ❌ Trop générique
try:
    value = int(input())
except:
    print("Erreur")

# ✅ Gérer erreurs attendues
try:
    file = open("config.json")
    data = json.load(file)
except FileNotFoundError:
    # Utiliser config par défaut
    data = default_config()
except json.JSONDecodeError:
    print("Fichier JSON invalide")

# ✅ Utiliser with
with open("file.txt") as f:
    content = f.read()

# ✅ Logger plutôt que print
logging.error("Erreur: %s", e)

# ❌ Silencer les erreurs
try:
    risky()
except:
    pass  # Mauvais !

# ✅ Au moins logger
try:
    risky()
except Exception as e:
    logging.error("Erreur dans risky(): %s", e)
```

[← POO](./infos-python-04-poo.md) | [Index](./infos-python-00-index.md) | [Fichiers →](./infos-python-06-fichiers-io.md)

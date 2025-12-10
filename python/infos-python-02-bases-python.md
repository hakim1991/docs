# 📚 Bases de Python

[← Introduction](./infos-python-01-introduction-installation.md) | [Index](./infos-python-00-index.md) | [Modules →](./infos-python-03-modules-packages.md)

## Types de données

### Types numériques

```python
# Entiers
x = 10
y = -5
big_number = 1_000_000  # Lisibilité

# Flottants
pi = 3.14159
price = 19.99

# Complexes
z = 2 + 3j

# Opérations
a = 10 + 5   # Addition
b = 10 - 5   # Soustraction
c = 10 * 5   # Multiplication
d = 10 / 3   # Division (float)
e = 10 // 3  # Division entière
f = 10 % 3   # Modulo
g = 10 ** 2  # Puissance
```

### Chaînes de caractères

```python
# Déclaration
name = "Alice"
message = 'Hello'
multi = """Texte
sur plusieurs
lignes"""

# Concaténation
full_name = "Alice" + " " + "Smith"

# f-strings (recommandé)
age = 25
text = f"J'ai {age} ans"
text = f"2 + 2 = {2 + 2}"

# Méthodes utiles
text = "Hello World"
text.upper()        # HELLO WORLD
text.lower()        # hello world
text.capitalize()   # Hello world
text.replace("o", "0")  # Hell0 W0rld
text.split()        # ['Hello', 'World']
text.strip()        # Enlève espaces

# Slicing
text = "Python"
text[0]      # 'P'
text[-1]     # 'n'
text[0:3]    # 'Pyt'
text[2:]     # 'thon'
text[:4]     # 'Pyth'
text[::2]    # 'Pto' (1 sur 2)
text[::-1]   # 'nohtyP' (inverse)
```

### Booléens

```python
is_valid = True
is_empty = False

# Opérateurs logiques
a = True and False  # False
b = True or False   # True
c = not True        # False

# Comparaisons
x = 10
x == 10   # True
x != 5    # True
x > 5     # True
x < 20    # True
x >= 10   # True
x <= 10   # True
```

## Structures de données

### Listes

```python
# Création
fruits = ["pomme", "banane", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Accès
fruits[0]      # 'pomme'
fruits[-1]     # 'orange'
fruits[1:3]    # ['banane', 'orange']

# Modification
fruits[0] = "poire"
fruits.append("kiwi")         # Ajouter à la fin
fruits.insert(1, "fraise")    # Insérer à l'index 1
fruits.remove("banane")       # Supprimer par valeur
fruits.pop()                  # Supprimer dernier
fruits.pop(0)                 # Supprimer par index
del fruits[0]                 # Supprimer par index

# Méthodes utiles
len(fruits)                   # Longueur
fruits.count("pomme")         # Compter occurrences
fruits.index("orange")        # Trouver index
fruits.sort()                 # Trier
fruits.reverse()              # Inverser
fruits.clear()                # Vider

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

### Tuples (immuables)

```python
# Création
point = (10, 20)
person = ("Alice", 25, "Paris")

# Accès
point[0]   # 10
x, y = point  # Unpacking

# Ne peut pas être modifié
# point[0] = 5  # Erreur !
```

### Dictionnaires

```python
# Création
person = {
    "name": "Alice",
    "age": 25,
    "city": "Paris"
}

# Accès
person["name"]           # 'Alice'
person.get("age")        # 25
person.get("country", "FR")  # Valeur par défaut

# Modification
person["age"] = 26
person["email"] = "alice@example.com"
del person["city"]

# Méthodes utiles
person.keys()            # Clés
person.values()          # Valeurs
person.items()           # Paires (clé, valeur)
person.pop("age")        # Supprimer et retourner
person.update({"age": 27})  # Mettre à jour

# Dict comprehension
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### Sets (ensembles)

```python
# Création
numbers = {1, 2, 3, 4, 5}
fruits = set(["pomme", "banane", "orange"])

# Pas de doublons
numbers = {1, 2, 2, 3, 3, 3}  # {1, 2, 3}

# Opérations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b   # Union: {1, 2, 3, 4, 5, 6}
a & b   # Intersection: {3, 4}
a - b   # Différence: {1, 2}
a ^ b   # Différence symétrique: {1, 2, 5, 6}

# Méthodes
numbers.add(6)
numbers.remove(3)
numbers.discard(10)  # Pas d'erreur si absent
```

## Conditions

### if/elif/else

```python
age = 18

if age < 18:
    print("Mineur")
elif age == 18:
    print("Tout juste majeur")
else:
    print("Majeur")

# Opérateur ternaire
status = "Majeur" if age >= 18 else "Mineur"

# Conditions multiples
x = 10
if 5 < x < 15:
    print("x est entre 5 et 15")

# in / not in
fruits = ["pomme", "banane"]
if "pomme" in fruits:
    print("Pomme disponible")
```

## Boucles

### for

```python
# Itérer sur liste
fruits = ["pomme", "banane", "orange"]
for fruit in fruits:
    print(fruit)

# Range
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10):    # 2 à 9
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8
    print(i)

# Enumerate (avec index)
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Itérer sur dictionnaire
person = {"name": "Alice", "age": 25}
for key, value in person.items():
    print(f"{key}: {value}")

# Break et continue
for i in range(10):
    if i == 5:
        break  # Sortir de la boucle
    if i % 2 == 0:
        continue  # Passer à l'itération suivante
    print(i)
```

### while

```python
count = 0
while count < 5:
    print(count)
    count += 1

# Boucle infinie (avec break)
while True:
    response = input("Continuer ? (o/n) ")
    if response == "n":
        break
```

## Fonctions

### Déclaration

```python
# Fonction simple
def greet(name):
    return f"Bonjour, {name} !"

result = greet("Alice")

# Plusieurs paramètres
def add(a, b):
    return a + b

# Valeurs par défaut
def greet(name, greeting="Bonjour"):
    return f"{greeting}, {name} !"

greet("Alice")              # Bonjour, Alice !
greet("Alice", "Salut")     # Salut, Alice !

# Arguments nommés
def create_user(name, age, city="Paris"):
    return {"name": name, "age": age, "city": city}

user = create_user(name="Alice", age=25)
user = create_user(age=25, name="Alice", city="Lyon")

# Plusieurs valeurs de retour
def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([1, 5, 3, 9, 2])
```

### *args et **kwargs

```python
# *args : nombre variable d'arguments
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3)           # 6
sum_all(1, 2, 3, 4, 5)     # 15

# **kwargs : arguments nommés variables
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Paris")

# Combinaison
def full_function(a, b, *args, **kwargs):
    print(f"a: {a}, b: {b}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

full_function(1, 2, 3, 4, name="Alice", age=25)
```

### Lambda (fonctions anonymes)

```python
# Fonction lambda
square = lambda x: x ** 2
square(5)  # 25

add = lambda x, y: x + y
add(3, 4)  # 7

# Utile avec map, filter, sorted
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Tri avec key
people = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 20}
]
sorted_people = sorted(people, key=lambda p: p["age"])
```

## Fonctions built-in utiles

```python
# Conversion de types
int("10")          # 10
float("3.14")      # 3.14
str(42)            # "42"
list("hello")      # ['h', 'e', 'l', 'l', 'o']

# Math
abs(-5)            # 5
round(3.7)         # 4
pow(2, 3)          # 8
min(1, 2, 3)       # 1
max(1, 2, 3)       # 3
sum([1, 2, 3])     # 6

# Itérables
len([1, 2, 3])     # 3
sorted([3, 1, 2])  # [1, 2, 3]
reversed([1, 2, 3])  # [3, 2, 1]
all([True, True])  # True
any([False, True]) # True

# Autres
type(5)            # <class 'int'>
isinstance(5, int) # True
dir(obj)           # Liste attributs/méthodes
help(print)        # Documentation
```

## Compréhensions

### List comprehension

```python
# Carres de 0 à 9
squares = [x**2 for x in range(10)]

# Nombres pairs
evens = [x for x in range(20) if x % 2 == 0]

# Avec condition
positive = [x for x in [-2, -1, 0, 1, 2] if x > 0]

# Nested
matrix = [[i*j for j in range(3)] for i in range(3)]
```

### Dict comprehension

```python
# Carrés
squares = {x: x**2 for x in range(6)}

# Inverser dict
original = {"a": 1, "b": 2}
inverted = {v: k for k, v in original.items()}
```

### Set comprehension

```python
squares = {x**2 for x in range(10)}
```

## Unpacking

```python
# Listes/tuples
a, b, c = [1, 2, 3]
x, y = (10, 20)

# Swap
a, b = b, a

# Rest operator
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5

# Dictionnaires
person = {"name": "Alice", "age": 25}
combined = {**person, "city": "Paris"}
```

## Opérateurs

```python
# Arithmétiques
+, -, *, /, //, %, **

# Comparaison
==, !=, <, >, <=, >=

# Logiques
and, or, not

# Identité
is, is not

# Appartenance
in, not in

# Bitwise
&, |, ^, ~, <<, >>

# Assignment
=, +=, -=, *=, /=, //=, %=, **=
```

[← Introduction](./infos-python-01-introduction-installation.md) | [Index](./infos-python-00-index.md) | [Modules →](./infos-python-03-modules-packages.md)

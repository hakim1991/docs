# 🎯 POO (Programmation Orientée Objet)

[← Modules](./infos-python-03-modules-packages.md) | [Index](./infos-python-00-index.md) | [Erreurs →](./infos-python-05-gestion-erreurs.md)

## Classes et objets

### Créer une classe

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Bonjour, je suis {self.name}"

    def is_adult(self):
        return self.age >= 18

# Créer instance
person = Person("Alice", 25)
print(person.name)      # Alice
print(person.greet())   # Bonjour, je suis Alice
print(person.is_adult())  # True
```

### __init__ (constructeur)

```python
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0  # Valeur par défaut

    def drive(self, km):
        self.mileage += km
        return f"Conduit {km} km. Total: {self.mileage} km"

car = Car("Toyota", "Corolla", 2020)
car.drive(100)
```

## Attributs

### Attributs d'instance

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name      # Attribut d'instance
        self.breed = breed    # Attribut d'instance
```

### Attributs de classe

```python
class Dog:
    species = "Canis familiaris"  # Attribut de classe (partagé)

    def __init__(self, name):
        self.name = name

dog1 = Dog("Rex")
dog2 = Dog("Max")
print(dog1.species)  # Canis familiaris
print(dog2.species)  # Canis familiaris
```

### Attributs privés

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # Privé (convention)

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

account = BankAccount(1000)
# account.__balance  # Erreur
print(account.get_balance())  # 1000
```

## Méthodes

### Méthodes d'instance

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):  # Méthode d'instance
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)
```

### Méthodes de classe

```python
class Person:
    count = 0

    def __init__(self, name):
        self.name = name
        Person.count += 1

    @classmethod
    def get_count(cls):  # cls = classe
        return cls.count

    @classmethod
    def from_birth_year(cls, name, birth_year):
        age = 2024 - birth_year
        return cls(name, age)

person = Person.from_birth_year("Alice", 1995)
print(Person.get_count())
```

### Méthodes statiques

```python
class MathUtils:
    @staticmethod
    def add(a, b):  # Pas besoin de self ou cls
        return a + b

    @staticmethod
    def is_even(n):
        return n % 2 == 0

result = MathUtils.add(5, 3)
print(MathUtils.is_even(4))  # True
```

## Propriétés

### @property

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.radius)  # 5
circle.radius = 10    # Utilise le setter
print(circle.area)    # Calculé automatiquement
```

## Héritage

### Héritage simple

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass  # À implémenter dans sous-classes

class Dog(Animal):
    def speak(self):
        return f"{self.name} dit: Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} dit: Meow!"

dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.speak())  # Rex dit: Woof!
print(cat.speak())  # Whiskers dit: Meow!
```

### super()

```python
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def info(self):
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)  # Appel constructeur parent
        self.doors = doors

    def info(self):
        base_info = super().info()  # Appel méthode parent
        return f"{base_info} - {self.doors} portes"

car = Car("Toyota", "Corolla", 4)
print(car.info())  # Toyota Corolla - 4 portes
```

### Héritage multiple

```python
class Flyable:
    def fly(self):
        return "Je peux voler"

class Swimmable:
    def swim(self):
        return "Je peux nager"

class Duck(Flyable, Swimmable):
    def quack(self):
        return "Coin coin"

duck = Duck()
print(duck.fly())    # Je peux voler
print(duck.swim())   # Je peux nager
print(duck.quack())  # Coin coin
```

## Méthodes spéciales (dunder methods)

### __str__ et __repr__

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):  # Pour print()
        return f"Person: {self.name}, {self.age} ans"

    def __repr__(self):  # Pour développeurs
        return f"Person('{self.name}', {self.age})"

person = Person("Alice", 25)
print(person)       # Person: Alice, 25 ans
print(repr(person)) # Person('Alice', 25)
```

### Opérateurs

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):  # +
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):  # -
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):  # *
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):  # ==
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2  # Utilise __add__
print(v3)     # Vector(4, 6)
```

### Collections

```python
class MyList:
    def __init__(self):
        self.items = []

    def __len__(self):  # len()
        return len(self.items)

    def __getitem__(self, index):  # []
        return self.items[index]

    def __setitem__(self, index, value):  # [] =
        self.items[index] = value

    def __iter__(self):  # for ... in
        return iter(self.items)

    def __contains__(self, item):  # in
        return item in self.items

my_list = MyList()
my_list.items = [1, 2, 3]
print(len(my_list))  # 3
print(my_list[0])    # 1
print(2 in my_list)  # True
```

### Context manager

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

# Utilisation
with FileManager("data.txt", "r") as f:
    content = f.read()
```

## Encapsulation

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.__owner = owner     # Privé
        self.__balance = balance # Privé

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.balance)  # 1500
```

## Polymorphisme

```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

# Polymorphisme
shapes = [Rectangle(10, 5), Circle(7)]
for shape in shapes:
    print(f"Area: {shape.area()}")
```

## Classes abstraites

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

    @abstractmethod
    def move(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

    def move(self):
        return "Running"

# animal = Animal()  # Erreur : ne peut pas instancier
dog = Dog()  # OK
```

## Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    city: str = "Paris"  # Valeur par défaut

    def is_adult(self):
        return self.age >= 18

person = Person("Alice", 25)
print(person)  # Person(name='Alice', age=25, city='Paris')
print(person.name)  # Alice
```

### Avec options

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)  # Immuable
class Point:
    x: int
    y: int

@dataclass
class Inventory:
    items: list = field(default_factory=list)
    count: int = field(init=False)

    def __post_init__(self):
        self.count = len(self.items)
```

## Composition vs Héritage

### Composition (préféré)

```python
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()  # Composition

    def start(self):
        return self.engine.start()

car = Car()
print(car.start())  # Engine started
```

## Bonnes pratiques

1. **Une classe = une responsabilité** : principe SOLID
2. **Noms explicites** : PascalCase pour classes
3. **Docstrings** : documenter classes et méthodes
4. **Properties** : pour getters/setters
5. **Composition > Héritage** : préférer composition
6. **ABC pour interfaces** : clarifier contrats

```python
class User:
    """
    Représente un utilisateur de l'application.

    Attributes:
        username: Nom d'utilisateur unique
        email: Adresse email
    """

    def __init__(self, username, email):
        """
        Initialise un nouvel utilisateur.

        Args:
            username: Nom d'utilisateur
            email: Adresse email
        """
        self.username = username
        self.email = email
```

[← Modules](./infos-python-03-modules-packages.md) | [Index](./infos-python-00-index.md) | [Erreurs →](./infos-python-05-gestion-erreurs.md)

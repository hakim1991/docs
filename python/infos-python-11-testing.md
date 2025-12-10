# 🧪 Testing

[← Bases de données](./infos-python-10-bases-donnees.md) | [Index](./infos-python-00-index.md) | [Deployment →](./infos-python-12-deployment.md)

## unittest (intégré)

### Test basique

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_add_strings(self):
        self.assertEqual(add("Hello", " World"), "Hello World")

if __name__ == "__main__":
    unittest.main()
```

### Assertions

```python
import unittest

class TestAssertions(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1, 2)

    def test_boolean(self):
        self.assertTrue(True)
        self.assertFalse(False)

    def test_none(self):
        self.assertIsNone(None)
        self.assertIsNotNone("value")

    def test_in(self):
        self.assertIn(1, [1, 2, 3])
        self.assertNotIn(4, [1, 2, 3])

    def test_instance(self):
        self.assertIsInstance("hello", str)
        self.assertIsInstance(123, int)

    def test_raises(self):
        with self.assertRaises(ValueError):
            int("abc")

        with self.assertRaises(ZeroDivisionError):
            1 / 0

    def test_almost_equal(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3)

    def test_greater_less(self):
        self.assertGreater(5, 3)
        self.assertLess(3, 5)
        self.assertGreaterEqual(5, 5)
        self.assertLessEqual(3, 5)
```

### setUp et tearDown

```python
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Appelé avant chaque test"""
        self.db = DatabaseConnection()
        self.db.connect()

    def tearDown(self):
        """Appelé après chaque test"""
        self.db.disconnect()

    @classmethod
    def setUpClass(cls):
        """Appelé une fois au début"""
        cls.config = load_config()

    @classmethod
    def tearDownClass(cls):
        """Appelé une fois à la fin"""
        cleanup_resources()

    def test_insert(self):
        self.db.insert("test")
        self.assertTrue(self.db.exists("test"))

    def test_delete(self):
        self.db.insert("test")
        self.db.delete("test")
        self.assertFalse(self.db.exists("test"))
```

### Skip tests

```python
import unittest
import sys

class TestSkip(unittest.TestCase):
    @unittest.skip("En cours de développement")
    def test_future_feature(self):
        pass

    @unittest.skipIf(sys.platform == "win32", "Ne fonctionne pas sur Windows")
    def test_unix_only(self):
        pass

    @unittest.skipUnless(sys.platform == "linux", "Linux uniquement")
    def test_linux_only(self):
        pass

    @unittest.expectedFailure
    def test_known_bug(self):
        self.assertEqual(1, 2)  # Bug connu
```

### Subtests

```python
import unittest

class TestSubtests(unittest.TestCase):
    def test_numbers(self):
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)  # Affiche tous les échecs
```

## pytest

### Installation

```bash
pip install pytest
```

### Test basique

```python
# test_math.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_add_strings():
    assert add("Hello", " World") == "Hello World"
```

```bash
# Lancer tests
pytest

# Verbose
pytest -v

# Test spécifique
pytest test_math.py::test_add

# Pattern
pytest -k "add"

# Dernier échec
pytest --lf

# Stop au premier échec
pytest -x
```

### Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Fixture simple"""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_length(sample_data):
    assert len(sample_data) == 5

# Fixture avec setup/teardown
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db  # Fournit la fixture
    db.disconnect()  # Cleanup

def test_query(database):
    result = database.query("SELECT * FROM users")
    assert len(result) > 0
```

### Fixtures avec scope

```python
import pytest

@pytest.fixture(scope="function")  # Défaut, avant chaque test
def func_fixture():
    return "function"

@pytest.fixture(scope="class")  # Une fois par classe
def class_fixture():
    return "class"

@pytest.fixture(scope="module")  # Une fois par module
def module_fixture():
    return "module"

@pytest.fixture(scope="session")  # Une fois par session
def session_fixture():
    return "session"

# Fixture autouse (automatique)
@pytest.fixture(autouse=True)
def setup_teardown():
    print("Setup")
    yield
    print("Teardown")
```

### Parametrize

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input, expected):
    assert input ** 2 == expected

# Plusieurs paramètres
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (2, 3, 5),
    (10, 20, 30),
])
def test_add(a, b, expected):
    assert a + b == expected

# Produit cartésien
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    assert x < y
```

### Marks

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    # Test lent
    pass

@pytest.mark.skip(reason="En développement")
def test_skip():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix uniquement")
def test_unix():
    pass

@pytest.mark.xfail
def test_known_bug():
    assert 1 == 2  # Bug connu

# Lancer uniquement certains marks
# pytest -m slow
# pytest -m "not slow"
```

### Exceptions

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Division par zéro")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)

    assert "Division par zéro" in str(exc_info.value)

def test_divide_type_error():
    with pytest.raises(TypeError):
        divide("10", 2)
```

### conftest.py

```python
# conftest.py (fixtures partagées)
import pytest

@pytest.fixture
def database():
    """Disponible pour tous les tests"""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def api_client():
    return APIClient(base_url="http://localhost:5000")

# Hooks
def pytest_configure(config):
    print("Configuration pytest")

def pytest_collection_modifyitems(items):
    """Modifier les tests collectés"""
    pass
```

## Testing Flask

```bash
pip install pytest flask
```

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Flask"

@app.route("/api/users/<int:id>")
def get_user(id):
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    user = users.get(id)
    if user:
        return jsonify(user)
    return jsonify({"error": "Not found"}), 404

# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello Flask" in response.data

def test_get_user(client):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json == {"name": "Alice"}

def test_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert "error" in response.json

def test_post_user(client):
    response = client.post("/api/users", json={"name": "Charlie"})
    assert response.status_code == 201
```

### Flask avec base de données

```python
import pytest
from app import app, db
from app.models import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def sample_user():
    user = User(username="alice", email="alice@example.com")
    db.session.add(user)
    db.session.commit()
    return user

def test_create_user(client):
    response = client.post("/api/users", json={
        "username": "bob",
        "email": "bob@example.com"
    })
    assert response.status_code == 201
    assert response.json["username"] == "bob"

def test_get_users(client, sample_user):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["username"] == "alice"
```

## Testing Django

```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            password="password123"
        )

    def test_create_post(self):
        post = Post.objects.create(
            title="Test Post",
            content="Content",
            author=self.user
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.author.username, "alice")

    def test_post_str(self):
        post = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        self.assertEqual(str(post), "Test")

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="alice",
            password="password123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Content",
            author=self.user
        )

    def test_post_list_view(self):
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_post_detail_view(self):
        response = self.client.get(f"/posts/{self.post.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")

    def test_post_create_requires_auth(self):
        response = self.client.get("/posts/create/")
        self.assertEqual(response.status_code, 302)  # Redirect to login

        self.client.login(username="alice", password="password123")
        response = self.client.get("/posts/create/")
        self.assertEqual(response.status_code, 200)
```

### Django API tests

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Post

class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            password="password123"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="Content",
            author=self.user
        )

    def test_get_posts(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "New Post", "content": "Content"}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_unauthenticated(self):
        data = {"title": "New Post", "content": "Content"}
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

## Mocking

### unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

# Mock simple
def test_mock_basic():
    mock = Mock()
    mock.method.return_value = 42

    result = mock.method()
    assert result == 42
    mock.method.assert_called_once()

# Patch
def get_data_from_api():
    import requests
    response = requests.get("https://api.example.com/data")
    return response.json()

@patch("requests.get")
def test_api_call(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response

    result = get_data_from_api()
    assert result == {"data": "test"}
    mock_get.assert_called_once_with("https://api.example.com/data")

# Patch comme context manager
def test_api_with_context():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = get_data_from_api()
        assert result == {"data": "test"}

# Side effects
def test_side_effect():
    mock = Mock()
    mock.method.side_effect = [1, 2, 3]

    assert mock.method() == 1
    assert mock.method() == 2
    assert mock.method() == 3

# Patch objet
class APIClient:
    def get_user(self, id):
        # Appel API réel
        pass

def test_patch_object():
    client = APIClient()
    with patch.object(client, "get_user", return_value={"name": "Alice"}):
        result = client.get_user(1)
        assert result == {"name": "Alice"}
```

### pytest-mock

```bash
pip install pytest-mock
```

```python
import pytest

def get_data():
    import requests
    response = requests.get("https://api.example.com")
    return response.json()

def test_api_call(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"data": "test"}

    mocker.patch("requests.get", return_value=mock_response)

    result = get_data()
    assert result == {"data": "test"}

# Spy
def test_spy(mocker):
    spy = mocker.spy(math, "sqrt")
    result = math.sqrt(16)
    assert result == 4
    spy.assert_called_once_with(16)
```

## Coverage

```bash
pip install coverage pytest-cov
```

### Avec coverage

```bash
# Lancer tests avec coverage
coverage run -m pytest

# Rapport
coverage report

# Rapport détaillé
coverage report -m

# HTML
coverage html
# Ouvre htmlcov/index.html
```

### Avec pytest-cov

```bash
# Coverage avec pytest
pytest --cov=myapp

# Rapport détaillé
pytest --cov=myapp --cov-report=term-missing

# HTML
pytest --cov=myapp --cov-report=html

# Minimum coverage (échec si < 80%)
pytest --cov=myapp --cov-fail-under=80
```

### .coveragerc

```ini
# .coveragerc
[run]
source = myapp
omit =
    */tests/*
    */migrations/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

## Bonnes pratiques

```python
# ✅ Tests isolés
def test_add():
    assert add(2, 3) == 5  # Ne dépend pas d'autres tests

# ✅ Un concept par test
def test_user_creation():
    user = User("Alice")
    assert user.name == "Alice"

def test_user_email():
    user = User("Alice", "alice@example.com")
    assert user.email == "alice@example.com"

# ✅ Noms descriptifs
def test_user_cannot_be_created_with_invalid_email():
    with pytest.raises(ValueError):
        User("Alice", "invalid-email")

# ✅ Arrange-Act-Assert
def test_add_item_to_cart():
    # Arrange
    cart = ShoppingCart()
    item = Item("Book", 10)

    # Act
    cart.add(item)

    # Assert
    assert len(cart.items) == 1
    assert cart.total == 10

# ✅ Fixtures pour réutilisation
@pytest.fixture
def cart():
    return ShoppingCart()

@pytest.fixture
def book():
    return Item("Book", 10)

def test_add_item(cart, book):
    cart.add(book)
    assert len(cart.items) == 1

# ✅ Mock dépendances externes
@patch("requests.get")
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    result = fetch_data()
    assert result["data"] == "test"

# ✅ Tests parametrés
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

# ❌ Tests interdépendants
class TestBad:
    def test_1(self):
        self.value = 10

    def test_2(self):
        assert self.value == 10  # Dépend de test_1

# ❌ Tests trop longs
def test_everything():  # Test trop de choses
    user = create_user()
    post = create_post()
    comment = create_comment()
    # ...

# ❌ Hardcoded values
def test_time():
    assert get_time() == "2024-01-01"  # Fragile
```

## Structure de projet

```
myapp/
├── myapp/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_utils.py
├── pytest.ini
├── .coveragerc
└── requirements.txt
```

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --cov=myapp
    --cov-report=term-missing
    --cov-report=html
markers =
    slow: marks tests as slow
    integration: integration tests
    unit: unit tests
```

[← Bases de données](./infos-python-10-bases-donnees.md) | [Index](./infos-python-00-index.md) | [Deployment →](./infos-python-12-deployment.md)

# 🌶️ Flask

[← Streamlit](./infos-python-07-streamlit.md) | [Index](./infos-python-00-index.md) | [Django →](./infos-python-09-django.md)

## Installation

```bash
pip install flask
```

## Application simple

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Flask!"

@app.route("/about")
def about():
    return "À propos"

if __name__ == "__main__":
    app.run(debug=True)
```

```bash
python app.py
# ou
flask run
```

Ouvre `http://localhost:5000`

## Routes

### Routes de base

```python
@app.route("/")
def index():
    return "Accueil"

@app.route("/users")
def users():
    return "Liste des utilisateurs"

# Paramètres d'URL
@app.route("/users/<int:user_id>")
def user_detail(user_id):
    return f"Utilisateur #{user_id}"

@app.route("/posts/<string:slug>")
def post_detail(slug):
    return f"Post: {slug}"

# Plusieurs méthodes HTTP
@app.route("/api/data", methods=["GET", "POST"])
def data():
    return {"message": "Data endpoint"}
```

### Variables d'URL

```python
@app.route("/users/<int:id>")
def user(id):
    return f"User {id}"

# Types disponibles: string, int, float, path, uuid
@app.route("/files/<path:filepath>")
def files(filepath):
    return f"File: {filepath}"
```

## Request et Response

```python
from flask import request, jsonify, make_response

@app.route("/api/users", methods=["POST"])
def create_user():
    # JSON body
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    # Query params
    page = request.args.get("page", 1, type=int)

    # Form data
    username = request.form.get("username")

    # Headers
    auth = request.headers.get("Authorization")

    # Cookies
    session_id = request.cookies.get("session_id")

    # JSON response
    return jsonify({"id": 1, "name": name, "email": email})

    # Custom status code
    return jsonify({"error": "Not found"}), 404

    # Custom headers
    response = make_response(jsonify({"data": "value"}))
    response.headers["X-Custom"] = "Header"
    return response
```

## Templates (Jinja2)

### Structure

```
app/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── user.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

### Render template

```python
from flask import render_template

@app.route("/")
def index():
    users = ["Alice", "Bob", "Charlie"]
    return render_template("index.html", users=users, title="Accueil")
```

### base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Mon Site{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">Accueil</a>
        <a href="{{ url_for('about') }}">À propos</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

### index.html

```html
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>

    {% if users %}
        <ul>
        {% for user in users %}
            <li>{{ user }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Aucun utilisateur</p>
    {% endif %}
{% endblock %}
```

## Forms

```bash
pip install flask-wtf
```

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app.config["SECRET_KEY"] = "your-secret-key"

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Connexion")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Traiter connexion
        return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)
```

```html
<!-- login.html -->
<form method="POST">
    {{ form.hidden_tag() }}

    {{ form.email.label }}
    {{ form.email(class="form-control") }}
    {% if form.email.errors %}
        {% for error in form.email.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    {% endif %}

    {{ form.password.label }}
    {{ form.password(class="form-control") }}

    {{ form.submit(class="btn btn-primary") }}
</form>
```

## Base de données (SQLAlchemy)

```bash
pip install flask-sqlalchemy
```

```python
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modèles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Créer tables
with app.app_context():
    db.create_all()

# CRUD
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id}), 201

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"id": user.id, "username": user.username})

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get("username", user.username)
    db.session.commit()
    return jsonify({"id": user.id})

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
```

## Authentification

```bash
pip install flask-login
```

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        login_user(user)
        return jsonify({"message": "Logged in"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hello {current_user.username}"
```

## Blueprints (modularité)

```python
# users/routes.py
from flask import Blueprint

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/")
def list_users():
    return "Liste utilisateurs"

@users_bp.route("/<int:id>")
def user_detail(id):
    return f"User {id}"

# app.py
from users.routes import users_bp
app.register_blueprint(users_bp)
```

## REST API

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/api/users/<int:id>", methods=["GET"])
def get_user(id):
    user = next((u for u in users if u["id"] == id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = next((u for u in users if u["id"] == id), None)
    if user:
        data = request.get_json()
        user.update(data)
        return jsonify(user)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    global users
    users = [u for u in users if u["id"] != id]
    return "", 204
```

## CORS

```bash
pip install flask-cors
```

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Activer CORS pour toutes les routes

# Ou pour routes spécifiques
@app.route("/api/data")
@cross_origin()
def data():
    return jsonify({"data": "value"})
```

## Error handling

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500
```

## Configuration

```python
# config.py
class Config:
    SECRET_KEY = "your-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# app.py
from config import DevelopmentConfig

app.config.from_object(DevelopmentConfig)
```

## CLI commands

```python
import click

@app.cli.command()
def init_db():
    """Initialiser la base de données."""
    db.create_all()
    click.echo("Database initialized")

@app.cli.command()
@click.argument("username")
def create_user(username):
    """Créer un utilisateur."""
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User {username} created")
```

```bash
flask init-db
flask create-user alice
```

## Structure complète

```
myapp/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── api.py
│   ├── templates/
│   │   └── base.html
│   └── static/
│       ├── css/
│       └── js/
├── tests/
├── config.py
├── requirements.txt
└── run.py
```

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app

# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

[← Streamlit](./infos-python-07-streamlit.md) | [Index](./infos-python-00-index.md) | [Django →](./infos-python-09-django.md)

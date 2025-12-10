# 🎸 Django

[← Flask](./infos-python-08-flask.md) | [Index](./infos-python-00-index.md) | [Database →](./infos-python-10-bases-donnees.md)

## Installation

```bash
pip install django
```

## Créer un projet

```bash
# Créer projet
django-admin startproject myproject
cd myproject

# Structure
myproject/
├── manage.py
└── myproject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py

# Démarrer serveur
python manage.py runserver

# Ouvre http://127.0.0.1:8000
```

## Créer une app

```bash
python manage.py startapp blog

# Structure
blog/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
└── migrations/
```

### Enregistrer l'app

```python
# myproject/settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",  # Ajouter ici
]
```

## Modèles

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
```

### Migrations

```bash
# Créer migrations
python manage.py makemigrations

# Appliquer migrations
python manage.py migrate

# Voir SQL
python manage.py sqlmigrate blog 0001
```

## Admin

```python
# blog/admin.py
from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "created_at"]
    list_filter = ["status", "created_at", "category"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "created_at"
```

### Créer superuser

```bash
python manage.py createsuperuser
# Username, email, password

# Accéder à http://127.0.0.1:8000/admin
```

## Views

### Function-based views

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.filter(status="published")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    return render(request, "blog/post_detail.html", {"post": post})
```

### Class-based views

```python
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status="published")

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
```

## URLs

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
]

# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
]
```

## Templates

### Structure

```
blog/
└── templates/
    └── blog/
        ├── base.html
        ├── post_list.html
        └── post_detail.html
```

### base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Mon Blog{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav>
        <a href="{% url 'blog:post_list' %}">Accueil</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

### post_list.html

```html
{% extends "blog/base.html" %}

{% block title %}Blog{% endblock %}

{% block content %}
    <h1>Articles</h1>

    {% for post in posts %}
        <article>
            <h2>
                <a href="{% url 'blog:post_detail' post.slug %}">
                    {{ post.title }}
                </a>
            </h2>
            <p>Par {{ post.author.username }} le {{ post.created_at|date:"d F Y" }}</p>
            <p>{{ post.content|truncatewords:30 }}</p>
        </article>
    {% empty %}
        <p>Aucun article</p>
    {% endfor %}

    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">Première</a>
                <a href="?page={{ page_obj.previous_page_number }}">Précédente</a>
            {% endif %}

            Page {{ page_obj.number }} sur {{ page_obj.paginator.num_pages }}

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">Suivante</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">Dernière</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

## Forms

```python
# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "status"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
        }

# blog/views.py
from django.shortcuts import render, redirect
from .forms import PostForm

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})
```

```html
<!-- post_form.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enregistrer</button>
</form>
```

## Authentification

```python
# blog/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def dashboard(request):
    return render(request, "blog/dashboard.html")

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    login_url = "/login/"

# blog/urls.py
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
```

## REST API (Django REST Framework)

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
]

# blog/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "content", "author", "created_at"]
        read_only_fields = ["slug"]

# blog/views.py
from rest_framework import generics
from .serializers import PostSerializer

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status="published")
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

# blog/urls.py
urlpatterns = [
    path("api/posts/", PostListAPIView.as_view(), name="api_post_list"),
    path("api/posts/<slug:slug>/", PostDetailAPIView.as_view(), name="api_post_detail"),
]
```

## Queries ORM

```python
# Tous les objets
posts = Post.objects.all()

# Filtrer
posts = Post.objects.filter(status="published")
posts = Post.objects.filter(status="published", author__username="alice")

# Exclude
posts = Post.objects.exclude(status="draft")

# Get (un seul objet)
post = Post.objects.get(id=1)
post = Post.objects.get(slug="mon-article")

# Get or 404
from django.shortcuts.get_object_or_404
post = get_object_or_404(Post, slug="mon-article")

# Comparaisons
posts = Post.objects.filter(created_at__year=2024)
posts = Post.objects.filter(created_at__gte="2024-01-01")
posts = Post.objects.filter(title__icontains="python")
posts = Post.objects.filter(title__startswith="Django")

# Ordering
posts = Post.objects.order_by("-created_at")
posts = Post.objects.order_by("author__username", "-created_at")

# Limit
posts = Post.objects.all()[:10]

# Count
count = Post.objects.filter(status="published").count()

# Exists
exists = Post.objects.filter(slug="test").exists()

# Relations
post = Post.objects.select_related("author", "category").get(id=1)
posts = Post.objects.prefetch_related("comments").all()

# Créer
post = Post.objects.create(
    title="Titre",
    content="Contenu",
    author=user
)

# Update
Post.objects.filter(id=1).update(status="published")

# Delete
Post.objects.filter(id=1).delete()

# Aggregation
from django.db.models import Count, Avg
Post.objects.aggregate(Count("id"))
Category.objects.annotate(num_posts=Count("post"))
```

## Static et Media

```python
# settings.py
import os

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# urls.py (développement)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Collecter static
python manage.py collectstatic
```

## Signals

```python
# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def post_saved(sender, instance, created, **kwargs):
    if created:
        print(f"Nouveau post créé: {instance.title}")

# blog/apps.py
class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        import blog.signals
```

## Management commands

```python
# blog/management/commands/populate_posts.py
from django.core.management.base import BaseCommand
from blog.models import Post

class Command(BaseCommand):
    help = "Populate database with sample posts"

    def handle(self, *args, **kwargs):
        Post.objects.create(title="Test", content="Content")
        self.stdout.write(self.style.SUCCESS("Posts created"))
```

```bash
python manage.py populate_posts
```

## Tests

```python
# blog/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")

    def test_post_creation(self):
        post = Post.objects.create(
            title="Test",
            content="Content",
            author=self.user
        )
        self.assertEqual(post.title, "Test")
        self.assertEqual(post.author.username, "test")

# Lancer tests
python manage.py test
python manage.py test blog
```

[← Flask](./infos-python-08-flask.md) | [Index](./infos-python-00-index.md) | [Database →](./infos-python-10-bases-donnees.md)

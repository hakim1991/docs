# FastAPI - Exemple complet d'API REST
# Installation: pip install fastapi uvicorn sqlalchemy pydantic python-multipart

from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
import uvicorn

# ============================================
# Configuration de l'application
# ============================================

app = FastAPI(
    title="API de Gestion des Utilisateurs",
    description="API REST complète avec FastAPI",
    version="1.0.0"
)

# CORS (pour permettre les appels depuis Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Modèles Pydantic
# ============================================

class UserBase(BaseModel):
    """Modèle de base utilisateur"""
    name: str = Field(..., min_length=2, max_length=50, description="Nom de l'utilisateur")
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    age: Optional[int] = Field(None, ge=0, le=150, description="Âge de l'utilisateur")

    class Config:
        schema_extra = {
            "example": {
                "name": "Alice Dupont",
                "email": "alice@example.com",
                "age": 25
            }
        }

class UserCreate(UserBase):
    """Modèle pour créer un utilisateur"""
    password: str = Field(..., min_length=6, description="Mot de passe")

class UserResponse(UserBase):
    """Modèle de réponse utilisateur"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    """Modèle pour mettre à jour un utilisateur"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)

class MessageResponse(BaseModel):
    """Modèle de réponse générique"""
    message: str
    success: bool

# ============================================
# Base de données simulée
# ============================================

users_db = [
    {
        "id": 1,
        "name": "Alice Dupont",
        "email": "alice@example.com",
        "age": 25,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "name": "Bob Martin",
        "email": "bob@example.com",
        "age": 30,
        "created_at": datetime.now()
    },
    {
        "id": 3,
        "name": "Charlie Bernard",
        "email": "charlie@example.com",
        "age": 35,
        "created_at": datetime.now()
    }
]

# Compteur pour les IDs
next_user_id = 4

# ============================================
# Routes de base
# ============================================

@app.get("/", tags=["Root"])
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API de gestion des utilisateurs",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de santé pour monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }

# ============================================
# Routes CRUD Utilisateurs
# ============================================

@app.get(
    "/users",
    response_model=List[UserResponse],
    tags=["Users"],
    summary="Récupérer tous les utilisateurs",
    description="Retourne la liste complète des utilisateurs"
)
def get_users(
    skip: int = 0,
    limit: int = 10,
    min_age: Optional[int] = None
):
    """
    Récupérer la liste des utilisateurs avec pagination et filtres

    - **skip**: Nombre d'utilisateurs à ignorer
    - **limit**: Nombre maximum d'utilisateurs à retourner
    - **min_age**: Filtrer par âge minimum
    """
    filtered_users = users_db

    # Filtrer par âge si spécifié
    if min_age is not None:
        filtered_users = [u for u in filtered_users if u.get("age", 0) >= min_age]

    # Pagination
    return filtered_users[skip:skip + limit]

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Récupérer un utilisateur par ID"
)
def get_user(user_id: int):
    """Récupérer un utilisateur spécifique par son ID"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'ID {user_id} non trouvé"
        )
    return user

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Créer un nouvel utilisateur"
)
def create_user(user: UserCreate):
    """Créer un nouvel utilisateur"""
    global next_user_id

    # Vérifier si l'email existe déjà
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà"
        )

    # Créer l'utilisateur
    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.now()
    }

    users_db.append(new_user)
    next_user_id += 1

    return new_user

@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Mettre à jour un utilisateur"
)
def update_user(user_id: int, user_update: UserUpdate):
    """Mettre à jour les informations d'un utilisateur"""
    user = next((u for u in users_db if u["id"] == user_id), None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'ID {user_id} non trouvé"
        )

    # Mettre à jour uniquement les champs fournis
    update_data = user_update.dict(exclude_unset=True)

    # Vérifier unicité email si modifié
    if "email" in update_data:
        if any(u["email"] == update_data["email"] and u["id"] != user_id for u in users_db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà"
            )

    user.update(update_data)
    return user

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
    summary="Supprimer un utilisateur"
)
def delete_user(user_id: int):
    """Supprimer un utilisateur"""
    global users_db

    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)

    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'ID {user_id} non trouvé"
        )

    users_db.pop(user_index)
    return None

# ============================================
# Routes de recherche
# ============================================

@app.get(
    "/users/search/by-name",
    response_model=List[UserResponse],
    tags=["Search"],
    summary="Rechercher des utilisateurs par nom"
)
def search_users_by_name(q: str):
    """Rechercher des utilisateurs par nom (insensible à la casse)"""
    results = [u for u in users_db if q.lower() in u["name"].lower()]
    return results

@app.get(
    "/users/search/by-email",
    response_model=UserResponse,
    tags=["Search"],
    summary="Rechercher un utilisateur par email"
)
def search_user_by_email(email: EmailStr):
    """Rechercher un utilisateur par email"""
    user = next((u for u in users_db if u["email"] == email), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun utilisateur trouvé avec l'email {email}"
        )
    return user

# ============================================
# Routes de statistiques
# ============================================

@app.get(
    "/stats/users",
    tags=["Statistics"],
    summary="Statistiques des utilisateurs"
)
def get_user_stats():
    """Obtenir des statistiques sur les utilisateurs"""
    total_users = len(users_db)
    ages = [u.get("age", 0) for u in users_db if u.get("age")]

    return {
        "total_users": total_users,
        "average_age": sum(ages) / len(ages) if ages else 0,
        "min_age": min(ages) if ages else 0,
        "max_age": max(ages) if ages else 0
    }

# ============================================
# Upload de fichiers
# ============================================

@app.post(
    "/upload",
    response_model=MessageResponse,
    tags=["Files"],
    summary="Upload d'un fichier"
)
async def upload_file(file: UploadFile = File(...)):
    """Upload un fichier"""
    contents = await file.read()

    return {
        "message": f"Fichier '{file.filename}' uploadé avec succès",
        "success": True,
        "size": len(contents),
        "content_type": file.content_type
    }

# ============================================
# Gestion des erreurs personnalisée
# ============================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return {
        "error": "Erreur de validation",
        "detail": str(exc)
    }

# ============================================
# Point d'entrée principal
# ============================================

if __name__ == "__main__":
    # Lancer le serveur
    # uvicorn main:app --reload --host 0.0.0.0 --port 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en développement
        log_level="info"
    )

# ============================================
# Documentation
# ============================================

"""
Pour démarrer l'application:
    python main.py

Ou avec uvicorn directement:
    uvicorn main:app --reload

Documentation interactive:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)

Exemples de requêtes:

1. Obtenir tous les utilisateurs:
   GET http://localhost:8000/users

2. Créer un utilisateur:
   POST http://localhost:8000/users
   Body: {"name": "John Doe", "email": "john@example.com", "age": 28, "password": "secret123"}

3. Obtenir un utilisateur:
   GET http://localhost:8000/users/1

4. Mettre à jour un utilisateur:
   PUT http://localhost:8000/users/1
   Body: {"name": "John Smith", "age": 29}

5. Supprimer un utilisateur:
   DELETE http://localhost:8000/users/1

6. Rechercher par nom:
   GET http://localhost:8000/users/search/by-name?q=alice

7. Statistiques:
   GET http://localhost:8000/stats/users
"""

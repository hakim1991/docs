# Backend FastAPI - API de gestion de tâches (TODO)
# Installation: pip install fastapi uvicorn sqlalchemy

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# ============================================
# Configuration FastAPI
# ============================================

app = FastAPI(
    title="API TODO",
    description="API de gestion de tâches pour Streamlit",
    version="1.0.0"
)

# CORS pour Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Modèles
# ============================================

class TaskStatus(str, Enum):
    """Statuts possibles d'une tâche"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Priority(str, Enum):
    """Niveaux de priorité"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(BaseModel):
    """Modèle de base d'une tâche"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    status: TaskStatus = Field(default=TaskStatus.TODO)

class TaskCreate(TaskBase):
    """Modèle pour créer une tâche"""
    pass

class TaskUpdate(BaseModel):
    """Modèle pour mettre à jour une tâche"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    """Modèle complet d'une tâche"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ============================================
# Base de données simulée
# ============================================

tasks_db = [
    {
        "id": 1,
        "title": "Apprendre FastAPI",
        "description": "Étudier la documentation et créer une API",
        "priority": Priority.HIGH,
        "status": TaskStatus.IN_PROGRESS,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "title": "Créer interface Streamlit",
        "description": "Développer le frontend avec Streamlit",
        "priority": Priority.HIGH,
        "status": TaskStatus.TODO,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 3,
        "title": "Déployer l'application",
        "description": "Déployer sur un serveur de production",
        "priority": Priority.MEDIUM,
        "status": TaskStatus.TODO,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

next_task_id = 4

# ============================================
# Routes
# ============================================

@app.get("/", tags=["Root"])
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "API TODO",
        "version": "1.0.0",
        "endpoints": {
            "tasks": "/tasks",
            "docs": "/docs"
        }
    }

@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[Priority] = None
):
    """
    Récupérer toutes les tâches avec filtres optionnels

    - **status**: Filtrer par statut (todo, in_progress, done)
    - **priority**: Filtrer par priorité (low, medium, high)
    """
    filtered_tasks = tasks_db

    if status:
        filtered_tasks = [t for t in filtered_tasks if t["status"] == status]

    if priority:
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority]

    return filtered_tasks

@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: int):
    """Récupérer une tâche par son ID"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée"
        )

    return task

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate):
    """Créer une nouvelle tâche"""
    global next_task_id

    new_task = {
        "id": next_task_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "status": task.status,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    tasks_db.append(new_task)
    next_task_id += 1

    return new_task

@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate):
    """Mettre à jour une tâche"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée"
        )

    update_data = task_update.dict(exclude_unset=True)
    task.update(update_data)
    task["updated_at"] = datetime.now()

    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int):
    """Supprimer une tâche"""
    global tasks_db

    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)

    if task_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tâche avec l'ID {task_id} non trouvée"
        )

    tasks_db.pop(task_index)
    return None

@app.get("/stats", tags=["Statistics"])
def get_statistics():
    """Obtenir des statistiques sur les tâches"""
    total = len(tasks_db)
    todo = len([t for t in tasks_db if t["status"] == TaskStatus.TODO])
    in_progress = len([t for t in tasks_db if t["status"] == TaskStatus.IN_PROGRESS])
    done = len([t for t in tasks_db if t["status"] == TaskStatus.DONE])

    by_priority = {
        "high": len([t for t in tasks_db if t["priority"] == Priority.HIGH]),
        "medium": len([t for t in tasks_db if t["priority"] == Priority.MEDIUM]),
        "low": len([t for t in tasks_db if t["priority"] == Priority.LOW])
    }

    return {
        "total": total,
        "by_status": {
            "todo": todo,
            "in_progress": in_progress,
            "done": done
        },
        "by_priority": by_priority,
        "completion_rate": (done / total * 100) if total > 0 else 0
    }

# ============================================
# Point d'entrée
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

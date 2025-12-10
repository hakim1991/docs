# ⚡ FastAPI

[← Deployment](./infos-python-12-deployment.md) | [Index](./infos-python-00-index.md)

## Installation

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

## Application simple

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

```bash
# Lancer serveur
uvicorn main:app --reload

# Ouvre http://localhost:8000
# Docs: http://localhost:8000/docs (Swagger)
# ReDoc: http://localhost:8000/redoc
```

## Routes et méthodes HTTP

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items")
def get_items():
    return {"items": []}

@app.post("/items")
def create_item(item: dict):
    return {"item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted": item_id}

@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, item: dict):
    return {"item_id": item_id, "item": item}
```

## Path Parameters

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}

# Avec validation
@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="Item ID", ge=1, le=1000)
):
    return {"item_id": item_id}

# Enum pour paths
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model": "AlexNet", "message": "Deep Learning"}
    return {"model": model_name.value}
```

## Query Parameters

```python
from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

# Paramètres optionnels
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Avec Optional
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Avec validation
@app.get("/items")
def read_items(
    q: str = Query(None, min_length=3, max_length=50, regex="^[a-zA-Z]+$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return {"q": q, "skip": skip, "limit": limit}

# Liste de paramètres
@app.get("/items")
def read_items(q: list[str] = Query([])):
    return {"q": q}
# /items?q=foo&q=bar
```

## Pydantic Models

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    tax: Optional[float] = None
    tags: list[str] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "Gaming laptop",
                "price": 1299.99,
                "tax": 10.5,
                "tags": ["electronics", "gaming"]
            }
        }

@app.post("/items")
def create_item(item: Item):
    return {"item": item}

# Modèles imbriqués
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class Post(BaseModel):
    title: str
    content: str
    author: User
    published_at: datetime = Field(default_factory=datetime.now)

@app.post("/posts")
def create_post(post: Post):
    return {"post": post}
```

## Response Models

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    # Password n'est pas dans la réponse
    return user

# Multiple response models
from fastapi import status

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item

# Liste
@app.get("/items", response_model=list[Item])
def get_items():
    return [
        {"name": "Item 1", "price": 10.0},
        {"name": "Item 2", "price": 20.0}
    ]

# Response model avec exclusion
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
def get_item(item_id: int):
    return {"name": "Item", "price": 10.0}
```

## Status Codes

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None

# Custom status
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id == 0:
        return {"error": "Not found"}, 404
    return {"item_id": item_id}
```

## Gestion des erreurs

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return {"item_id": item_id}

# Custom exception
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong"}
    )

@app.get("/test/{name}")
def test(name: str):
    if name == "error":
        raise CustomException(name=name)
    return {"name": name}
```

## Dépendances

```python
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional

app = FastAPI()

# Dépendance simple
def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items")
def read_items(commons: dict = Depends(common_parameters)):
    return commons

# Dépendance de classe
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/users")
def read_users(commons: CommonQueryParams = Depends()):
    return commons

# Dépendances imbriquées
def verify_token(token: str):
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

def get_current_user(token: str = Depends(verify_token)):
    return {"username": "john", "token": token}

@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user
```

## Authentification

### JWT Token

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Fake DB
fake_users_db = {
    "john": {
        "username": "john",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False
    }
}

# Fonctions utilitaires
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Base de données (SQLAlchemy)

```bash
pip install sqlalchemy databases asyncpg
```

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    email: str

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI
app = FastAPI()

@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"deleted": True}
```

## Upload de fichiers

```python
from fastapi import FastAPI, File, UploadFile
from typing import List

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

# Multiple files
@app.post("/uploadfiles")
async def upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

# Sauvegarder fichier
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        contents = await file.read()
        buffer.write(contents)
    return {"filename": file.filename}
```

## Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def write_log(message: str):
    time.sleep(5)
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent in background"}
```

## WebSockets

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left")
```

## CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou liste de domaines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello"}
```

## Middleware

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Testing

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI"}

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert "item_id" in response.json()

def test_auth():
    response = client.post(
        "/token",
        data={"username": "john", "password": "secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## Déploiement

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Heroku

```
# Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Production avec Gunicorn + Uvicorn

```bash
pip install gunicorn
```

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Bonnes pratiques

```python
# ✅ Structure du projet
myapp/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── items.py
├── tests/
├── requirements.txt
└── Dockerfile

# ✅ APIRouter pour modularité
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return {"users": []}

# main.py
from fastapi import FastAPI
from routers import users

app = FastAPI()
app.include_router(users.router)

# ✅ Validation avec Pydantic
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)

# ✅ Documentation enrichie
@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
    description="Create a new item with name and price",
    response_description="The created item"
)
def create_item(item: Item):
    return item

# ✅ Configuration avec pydantic
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()

# ✅ Gestion asynchrone
@app.get("/items")
async def get_items():
    items = await fetch_items_from_db()
    return items

# ✅ Logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/items")
async def get_items():
    logger.info("Fetching items")
    return {"items": []}
```

## Ressources

- Documentation officielle : https://fastapi.tiangolo.com
- GitHub : https://github.com/tiangolo/fastapi
- Tutorial : https://fastapi.tiangolo.com/tutorial/
- Awesome FastAPI : https://github.com/mjhea0/awesome-fastapi

[← Deployment](./infos-python-12-deployment.md) | [Index](./infos-python-00-index.md)

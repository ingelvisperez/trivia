
# TalaTrivia API

## Descripción del Proyecto

**TalaTrivia** es una API REST desarrollada con **FastAPI**, PostgreSQL y SQLAlchemy, diseñada para administrar trivias de conocimiento, permitiendo:

- Registro de usuarios  
- Gestión de preguntas  
- Creación de trivias  
- Jugar trivias  
- Registrar participaciones  
- Generar ranking  

---

# 🏗️ Diagrama de Arquitectura
```mermaid
graph TD
    C[Cliente Frontend] --> A[FastAPI API]
    A --> B[PostgreSQL DB]

```
---

# 🎬 Diagrama de Secuencia – Flujo “Jugar Trivia”

```mermaid
sequenceDiagram
    participant U as Usuario
    participant API as FastAPI - TalaTrivia API
    participant DB as PostgreSQL

    U->>API: GET /trivias/{id}/play?user_id=X
    API->>DB: Validar trivia y asignación de usuario
    DB-->>API: OK
    API->>DB: Obtener preguntas
    DB-->>API: Preguntas
    API-->>U: Preguntas (sin respuestas correctas)

    U->>API: POST /trivias/{id}/answer
    API->>DB: Obtener preguntas
    DB-->>API: Preguntas completas
    API->>API: Calcular puntaje
    API->>DB: Guardar participación
    DB-->>API: Participación guardada
    API-->>U: Score final
```

---

# 🗂️ Diagrama ER (Entidad–Relación)

```mermaid
erDiagram
    USER {
        int id PK
        string name
        string email
    }

    QUESTION {
        int id PK
        string text
        string difficulty
        json options
        string correct_option
    }

    TRIVIA {
        int id PK
        string name
        string description
    }

    TRIVIA_QUESTION {
        int id PK
        int trivia_id FK
        int question_id FK
        int order
    }

    TRIVIA_ASSIGNMENT {
        int id PK
        int trivia_id FK
        int user_id FK
    }

    PARTICIPATION {
        int id PK
        int trivia_id FK
        int user_id FK
        json answers
        int score
        datetime created_at
    }

    USER ||--o{ TRIVIA_ASSIGNMENT : asignado
    TRIVIA ||--o{ TRIVIA_ASSIGNMENT : tiene
    TRIVIA ||--o{ TRIVIA_QUESTION : contiene
    QUESTION ||--o{ TRIVIA_QUESTION : pertenece
    USER ||--o{ PARTICIPATION : realiza
    TRIVIA ||--o{ PARTICIPATION : registra
```

---

# 🧩 Diagrama de Componentes

```mermaid
graph LR
    subgraph API["FastAPI Application"]
        A["main.py"]
        R1["Router: Users"]
        R2["Router: Questions"]
        R3["Router: Trivias"]
        R4["Router: Ranking"]
        S1["Schemas"]
        M1["Models"]
        SC["Scoring Service"]
    end

    subgraph DB["PostgreSQL"]
        DBInst["Database"]
    end

    A --> R1
    A --> R2
    A --> R3
    A --> R4

    R1 --> M1
    R2 --> M1
    R3 --> M1
    R4 --> M1

    M1 --> DBInst
    SC --> R3
```

---

# ⚙️ Tecnologías Utilizadas

- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy ORM
- PostgreSQL 14
- Docker & Docker Compose
- Pydantic v2
- JSONB

---

# 📂 Estructura del Proyecto

```text
app/
├── main.py
├── database.py
├── models/
│   ├── user.py
│   ├── question.py
│   ├── trivia.py
│   ├── trivia_question.py
│   ├── trivia_assignment.py
│   ├── participation.py
│   └── __init__.py
├── schemas/
│   ├── user.py
│   ├── question.py
│   ├── trivia.py
│   ├── ranking.py
│   └── __init__.py
├── routers/
│   ├── users.py
│   ├── questions.py
│   ├── trivias.py
│   ├── ranking.py
│   └── __init__.py
└── services/
    └── scoring_service.py
```

---

# 🐳 Cómo levantar PostgreSQL con Docker

```bash
docker-compose up -d
```

---

# ▶️ Ejecutar API en Local

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger 👉 http://127.0.0.1:8000/docs

---

# 📌 Endpoints

- `/users`
- `/questions`
- `/trivias`
- `/ranking`

---

# 🧠 Autor

**Elvis Pérez**  
Backend Developer  

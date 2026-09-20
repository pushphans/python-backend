# Python Backend - FastAPI Learning Project

Ye mera FastAPI/Python backend seekhne ka project hai. Jaise jaise cheezein seekhta jaunga, yahan update hota rahega.

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy 2.0** - ORM (async)
- **Alembic** - Database migrations
- **PostgreSQL** - Database (asyncpg driver)
- **Pydantic** - Data validation & schemas
- **Pydantic Settings** - Environment variable management
- **uvicorn** - ASGI server

## Project Structure

```
src/fastapi_practice/
├── main.py              # FastAPI app entry point
├── core/
│   └── config.py        # Settings (.env management via pydantic-settings)
├── db/
│   └── database.py      # Async SQLAlchemy engine, session factory, Base
├── models/
│   └── todo.py          # SQLAlchemy ORM models
├── schema/
│   └── todo.py          # Pydantic schemas (request/response validation)
└── api/
    └── todo_router.py   # Route handlers (endpoints)
```

## Learnings So Far

### 1. Project Setup

- Python 3.12+ use ho raha hai
- Dependencies `pyproject.toml` mein manage hoti hain
- `.env` file se environment variables load hote hain (DATABASE_URL, PROJECT_NAME)

### 2. Async SQLAlchemy Setup (`db/database.py`)

- `create_async_engine` se async connection banta hai PostgreSQL se
- `async_sessionmaker` se request ke liye session banta hai
- `expire_on_commit=False` rakha taaki commit ke baad object access ho sake
- `get_db()` generator function hai jo har request ke liye naya session deta hai aur `Depends()` ke saath use hota hai
- `Base` class jo models inherit karte hain

### 3. SQLAlchemy Models (`models/todo.py`)

```python
class Todo(Base):
    __tablename__ = "todo"
    id          : Mapped[int]       = mapped_column(primary_key=True, autoincrement=True)
    title       : Mapped[str]       = mapped_column(String(150))
    description : Mapped[str | None] = mapped_column(Text)
    is_completed: Mapped[bool]      = mapped_column(default=False)
    created_at  : Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at  : Mapped[datetime]  = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

Seekha:
- `Mapped[]` type annotation se SQLAlchemy samajhta hai column type
- `String(150)` vs `Text` - length limited vs unlimited text
- `server_default=func.now()` - database level default timestamp
- `onupdate=func.now()` - update hone pe automatically timestamp change
- `mapped_column(default=False)` - Python level default value

### 4. Pydantic Schemas (`schema/todo.py`)

Teen schemas banaye:

| Schema | Purpose |
|--------|---------|
| `CreateTodoSchema` | POST request body validation |
| `UpdateTodoSchema` | PUT request body validation |
| `TodoResponseSchema` | Response format define karta hai |

Seekha:
- `Field(...)` - `...` ka matlab field required hai
- `Field(default=None)` - optional field
- `Field(min_length=1, max_length=150)` - validation constraints
- `ConfigDict(from_attributes=True)` - ORM objects se directly Pydantic model bana sake (response mein `return todo` kar sakte hain directly)
- `bool | None = None` se field optional ho jaati hai

### 5. API Endpoints (`api/todo_router.py`)

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `POST` | `/todo/create-todo` | Naya todo create karo | 201 Created |
| `GET` | `/todo/get-todo/{todo_id}` | Single todo lao by ID | 200 OK |
| `GET` | `/todo/get-todo` | Saare todos lao (paginated + search + filter) | 200 OK |
| `PUT` | `/todo/update-todo/{todo_id}` | Todo update karo | 200 OK |
| `DELETE` | `/todo/delete-todo/{todo_id}` | Todo delete karo | 204 No Content |

### 6. Key Concepts Seekhe

**Dependency Injection:**
- `Depends(get_db)` se har endpoint mein DB session milta hai automatically
- Function call hota hai internally, aur session yield hota hai

**Status Codes:**
- `201 Created` - resource create hua
- `200 OK` - successful operation
- `204 No Content` - delete successful, kuch return nahi
- `404 Not Found` - resource nahi mila

**HTTPException:**
- `raise HTTPException(status_code=404, detail="Todo not found")` se error response bhejte hain
- FastAPI automatically JSON response banata hai

**Pagination:**
- `Query(default=1, ge=1)` - minimum value constraint
- `offset = (page - 1) * limit` formula
- `limit` pe `le=100` lagaya taaki koi 100000 records na maange

**Search & Filter:**
- `ilike` se case-insensitive search hota hai
- Query params optional rakhe `str | None = None` se
- Conditional query building - `if search:` toh where clause add hota hai

**Async/Await:**
- Saare DB operations `await` ke saath hain
- `await db.execute(query)` - query run hoti hai
- `await db.commit()` - changes save hote hain
- `await db.refresh(todo)` - object mein fresh data aata hai DB se

### 7. Alembic Migrations

- `alembic init` se setup hota hai
- `alembic revision --autogenerate -m "message"` se migration file banti hai
- `alembic upgrade head` se migration apply hota hai
- Migration file mein `upgrade()` aur `downgrade()` functions hote hain
- Database schema changes version controlled hote hain

### 8. Router Setup (`main.py`)

```python
app = FastAPI()
app.include_router(router=todo_router)
```

- `APIRouter(prefix="/todo")` se saare endpoints `/todo/...` ke under aate hain
- `include_router` se main app mein mount hota hai
- Alag alag files mein routers rakhne se code organized rehta hai

## Running the Project

```bash
# Install dependencies
uv sync

# Run server
uvicorn fastapi_practice.main:app --reload

# Apply migrations
alembic upgrade head
```

## Future Topics (To Learn)

- [ ] Authentication & Authorization (JWT)
- [ ] Rate Limiting
- [ ] Background Tasks
- [ ] File Uploads
- [ ] WebSockets
- [ ] Testing (pytest)
- [ ] Docker setup
- [ ] CI/CD pipeline

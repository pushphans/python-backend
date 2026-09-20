from fastapi import status
from fastapi_practice.schema.todo import TodoResponseSchema
from fastapi_practice.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_practice.schema.todo import CreateTodoSchema
from fastapi import APIRouter, Depends
from fastapi_practice.models.todo import Todo




todo_router = APIRouter(
    prefix="/todo"
)


@todo_router.post("/create-todo", response_model=TodoResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_todo(data : CreateTodoSchema, db : AsyncSession = Depends(get_db)):
    todo : Todo = Todo(
        title = data.title,
        description = data.description
    )
    
    db.add(todo)
    await db.commit()
    await db.refresh(todo)


    return todo
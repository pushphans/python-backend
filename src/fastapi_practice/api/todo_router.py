from fastapi_practice.schema.todo import UpdateTodoSchema
from sqlalchemy.orm import query
from fastapi import status
from fastapi_practice.schema.todo import TodoResponseSchema
from fastapi_practice.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_practice.schema.todo import CreateTodoSchema
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_practice.models.todo import Todo
from sqlalchemy import select




todo_router = APIRouter(
    prefix="/todo",
    tags=["Todo"]
)



# CREATING TODO IN DB
@todo_router.post("/create-todo", response_model=TodoResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_todo(data : CreateTodoSchema, db : AsyncSession = Depends(get_db)):
    todo : Todo = Todo(
        title = data.title,
        description = data.description,
        is_completed  = data.is_completed
    )
    
    db.add(todo)
    await db.commit()
    await db.refresh(todo)


    return todo



# GETTING A SINGLE TODO FROM DB
@todo_router.get("/get-todo/{todo_id}", response_model=TodoResponseSchema, status_code=status.HTTP_200_OK)
async def get_todo(todo_id : int, db : AsyncSession = Depends(get_db)) -> TodoResponseSchema:
    query = select(Todo).where(Todo.id == todo_id)
    result = await db.execute(query)

    todo = result.scalar_one_or_none()

    if todo is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return todo
    


# # GETTING ALL TODOS
# @todo_router.get("/get-todo", response_model=list[TodoResponseSchema])
# async def get_todos(db : AsyncSession = Depends(get_db)):
#     query = select(Todo)

#     result = await db.execute(query)
#     todos = result.scalars().all()

#     return todos



# # GETTING TODOS WITH PAGINATED DATA
# @todo_router.get("/get-todo", response_model=list[TodoResponseSchema], status_code=status.HTTP_200_OK)
# async def get_todo(
#     db : AsyncSession = Depends(get_db), 
#     page : int = Query(default=1, ge = 1), 
#     limit : int = Query(default=10, ge=1, le=100),
#     ):

#     offset = (page - 1) * limit


#     query = select(Todo)

#     query = (
#         query
#         .offset(offset)
#         .limit(limit)
#     )


#     result = await db.execute(query)

#     todos = result.scalars().all()

#     return todos




# # GETTING TODOS WITH PAGINATED DATA and SEARCH
# @todo_router.get("/get-todo", response_model=list[TodoResponseSchema], status_code=status.HTTP_200_OK)
# async def get_todo(
#     db : AsyncSession = Depends(get_db), 
#     page : int = Query(default=1, ge = 1), 
#     limit : int = Query(default=10, ge=1, le=100),
#     search : str | None = None
#     ):

#     offset = (page - 1) * limit


#     query = select(Todo)


#     if search:
#         query = (
#             query
#             .where(Todo.title.ilike(f"%{search}%"))
#         )


#     query = (
#         query
#         .offset(offset)
#         .limit(limit)
#     )


#     result = await db.execute(query)

#     todos = result.scalars().all()

#     return todos





# GETTING TODOS WITH PAGINATED DATA, SEARCH and FILTER
@todo_router.get("/get-todo", response_model=list[TodoResponseSchema], status_code=status.HTTP_200_OK)
async def get_todo(
    db : AsyncSession = Depends(get_db), 
    page : int = Query(default=1, ge = 1), 
    limit : int = Query(default=10, ge=1, le=100),
    search : str | None = None,
    is_completed : bool | None = None
    ):

    offset = (page - 1) * limit


    query = select(Todo)


    if search:
        query = (
            query
            .where(Todo.title.ilike(f"%{search}%"))
        )

    if is_completed is not None:
        query = (
            query
            .where(Todo.is_completed == is_completed)
        )


    query = (
        query
        .offset(offset)
        .limit(limit)
    )


    result = await db.execute(query)

    todos = result.scalars().all()

    return todos




# UPDATING THE TODO
@todo_router.put("/update-todo/{todo_id}", response_model=TodoResponseSchema, status_code=status.HTTP_200_OK)
async def update_todo(
    todo_id : int,
    data : UpdateTodoSchema,
    db : AsyncSession = Depends(get_db)
    ):

    select_query = (
        select(Todo)
        .where(Todo.id == todo_id)
        )
    
    result = await db.execute(select_query)

    todo = result.scalar_one_or_none()

    if todo is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )

    todo.title = data.title
    todo.description = data.description
    todo.is_completed = data.is_completed

    await db.commit()
    await db.refresh(todo)

    return todo



#DELETING TODO
@todo_router.delete("/delete-todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id : int,
    db : AsyncSession = Depends(get_db)
    ):
    select_query = (
        select(Todo)
        .where(Todo.id == todo_id)
    ) 

    result = await db.execute(select_query)

    todo = result.scalar_one_or_none()

    if todo is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )

    await db.delete(todo)
    await db.commit()

    



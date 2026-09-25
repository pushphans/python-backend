from fastapi_practice.api.auth_router import auth_router
from fastapi_practice.api.file_router import file_router
from fastapi_practice.api.todo_router import todo_router
from fastapi import FastAPI, status


app = FastAPI()


app.include_router(router=todo_router)
app.include_router(router=file_router)
app.include_router(router=auth_router)


@app.get("/", status_code= status.HTTP_200_OK)
async def root():
    return {"status" : "ok"}



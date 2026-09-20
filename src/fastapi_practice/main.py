from fastapi_practice.api.todo_router import todo_router
from fastapi import FastAPI, status


app = FastAPI()


app.include_router(router=todo_router)


@app.get("/", status_code= status.HTTP_200_OK)
async def root():
    return {"status" : "ok"}



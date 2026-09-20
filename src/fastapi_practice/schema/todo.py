from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CreateTodoSchema(BaseModel):
    title : str = Field(..., min_length=1, max_length=150)
    description : str | None = Field(default=None, max_length=2000)
    is_completed : bool = Field(default=False)


class UpdateTodoSchema(BaseModel):
    title : str = Field(min_length=1, max_length=150)
    description : str | None = Field(default=None, max_length=2000)
    is_completed : bool = Field(default=False)



class TodoResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id : int 
    title : str
    description : str | None
    is_completed : bool
    created_at : datetime
    updated_at : datetime



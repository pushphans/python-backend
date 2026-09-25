from fastapi_practice.models import refresh_token
from datetime import datetime
from pydantic import EmailStr
from pydantic import Field
from pydantic import BaseModel, ConfigDict

class RegisterRequestSchema(BaseModel):
    email : EmailStr
    password : str = Field(..., min_length=6, max_length=100)


class RegisterResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


    id : int
    email : EmailStr
    created_at : datetime




class LoginRequestSchema(BaseModel):
    email : EmailStr
    password : str = Field(..., min_length=6, max_length=100)



class LoginResponseSchema(BaseModel):
    id : int
    email : str
    access_token : str
    token_type : str
    refresh_token : str
    expires_in : int 




class RefreshTokenRequestSchema(BaseModel):
    refresh_token : str


class RefreshTokenResponseSchema(BaseModel):
    access_token : str
    expires_in : int
    token_type : str

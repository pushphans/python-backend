from fastapi_practice.schema.user_schemas import RefreshTokenRequestSchema
from fastapi_practice.schema.user_schemas import RefreshTokenResponseSchema
from fastapi_practice.models.refresh_token import RefreshToken
from datetime import timedelta, datetime, timezone
from fastapi_practice.core.security import create_refresh_token
from fastapi_practice.core.config import settings
from fastapi_practice.core.security import create_access_token
from fastapi_practice.core.security import verify_password
from fastapi_practice.schema.user_schemas import LoginResponseSchema
from fastapi_practice.schema.user_schemas import LoginRequestSchema
from fastapi import HTTPException, status
from sqlalchemy import select
from fastapi_practice.schema.user_schemas import RegisterResponseSchema
from fastapi_practice.models.user_model import UserModel
from fastapi_practice.core.security import hash_password
from fastapi_practice.db.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_practice.schema.user_schemas import RegisterRequestSchema
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Auth"])



# REGISTER
@auth_router.post("/register", response_model=RegisterResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(
    data : RegisterRequestSchema,
    db : AsyncSession = Depends(get_db)
    ):
    email = data.email
    password = data.password

    query = (
        select(UserModel)
        .where(UserModel.email == email)
        )

    result = await db.execute(query)

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with same email already exists"
        )

    hashed_password = hash_password(password = password)

    user = UserModel(
        email = email,
        password_hash = hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user





# LOGIN
@auth_router.post("/login", response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
async def login(
    data : LoginRequestSchema,
    db : AsyncSession = Depends(get_db)
    ):
    email = data.email
    password = data.password

    query = (
        select(UserModel)
        .where(UserModel.email == email)
    )

    result = await db.execute(query)

    user_exists = result.scalar_one_or_none()

    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )
    
    hashed_password =  user_exists.password_hash

    password_verified : bool = verify_password(password=password, hashed_password=hashed_password)

    if password_verified == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(user_id=user_exists.id)
    refresh_token = create_refresh_token()

    refresh_token_expires_at = (datetime.now(timezone.utc) + timedelta(days = settings.REFRESH_TOKEN_EXPIRY))

    refresh_token_table_content = RefreshToken(
        user_id = user_exists.id,
        token = refresh_token,
        expires_at = refresh_token_expires_at
    )

    db.add(refresh_token_table_content)
    await db.commit()
    await db.refresh(refresh_token_table_content)

    return LoginResponseSchema(
        id=user_exists.id,
        email=user_exists.email,
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRY * 60,
        token_type="bearer",
        refresh_token=refresh_token
    )






# Refresh Access Token
@auth_router.post("/refresh-token", response_model=RefreshTokenResponseSchema, status_code=status.HTTP_200_OK)
async def refresh_access_token(
    data : RefreshTokenRequestSchema,
    db : AsyncSession = Depends(get_db)
    ):
    query = (
        select(RefreshToken)
        .where(RefreshToken.token == data.refresh_token)
    )

    result = await db.execute(query)

    refresh_token = result.scalar_one_or_none()

    # DB mein refresh token exist nai karta
    if refresh_token is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh token"
        )


    # db mein refresh token hai but expired hai
    if refresh_token.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Refresh token expired"
        )

    new_access_token = create_access_token(
        user_id=refresh_token.user_id
    )


    return RefreshTokenResponseSchema(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRY * 60
    )

    




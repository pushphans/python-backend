from datetime import timezone
from datetime import timedelta
from datetime import datetime
from pwdlib import PasswordHash
from fastapi_practice.core.config import settings
import jwt
import secrets


password_hasher = PasswordHash.recommended()


ALGORITHM = "HS256"




def hash_password(password : str) -> str: 
    return password_hasher.hash(password)


def verify_password(
    password,
    hashed_password
    ) -> bool:
    return password_hasher.verify(
        hash=hashed_password,
        password=password
    )
    


def create_access_token(user_id : int) -> str:
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
    }


    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


def decode_jwt(token : str):
    return  jwt.decode(
        token, 
        settings.JWT_SECRET_KEY,
        algorithms=[ALGORITHM]
    )





def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)
    


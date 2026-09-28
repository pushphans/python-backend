from fastapi_practice.core.security import decode_jwt
from fastapi import status
from fastapi import Request
from fastapi.responses import JSONResponse


PUBLIC_PATHS = {
    "/auth/register",
    "/auth/login"
}



async def auth_middleware(request : Request, call_next):
    if request.url.path in PUBLIC_PATHS:
        return call_next(request)

    authorization = request.headers.get("Authorization")
    
    if not authorization:
        return JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED,
            content = {"detail" : "Authentication required"}
        )


    if not authorization.startswith("Bearer"):
        return JSONResponse(
            status_code=401,
            content={"detail" : "Bearer token required"}
        )

    
    token = authorization.removeprefix("Bearer ")

    try:
        payload = decode_jwt(token=token)
    except:
        return JSONResponse(
            status_code=401,
            content={"detail" : "Invalid or expired token"}
        )

    user_id = payload.get("sub")

    if user_id is None:
        return JSONResponse(
            status_code=401,
            content={"detail" : "Invalid token"}
        )

    request.state.user_id = int(user_id)

    return call_next(request)

    

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


# this will come from env
API_KEY = "abcd"

EXCLUDED_PATHS = {"/docs", "/openapi.json", "/redoc"}


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if request.headers.get("X-API-Key") != API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Not authencated"})

        return await call_next(request)

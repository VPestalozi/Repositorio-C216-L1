from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.db.connection import db

class DBMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            # Obtém a conexão com o banco e a injeta no state
            async with await db.get_connection() as connection:
                request.state.db = connection
                response = await call_next(request)
                return response
        except Exception as e:
            # Pode-se tratar de outra forma se a conexão falhar
            raise e

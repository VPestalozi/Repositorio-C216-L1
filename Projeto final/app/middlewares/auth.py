from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth import decode_access_token

# Esquema OAuth2 — extrai o token do header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Middleware de autenticação.
    Extrai o token JWT do header Authorization, decodifica e retorna o usuário.
    Lança HTTPException 401 se o token for inválido ou o usuário não existir.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decodificar o token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Extrair o username do payload
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Buscar o usuário no banco
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user

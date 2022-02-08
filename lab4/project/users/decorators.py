from fastapi import Depends, HTTPException, status,WebSocket
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from project.database import get_db
from . import models
from .auth import get_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def login_required(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    current_user = get_user_from_token(db, token)
    if not current_user or not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return current_user

def superuser_required(current_user: models.User = Depends(login_required)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return current_user


# async def ws_login_required(websocket: WebSocket, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     try:
#         user = get_user_from_token(db, token)
#         if not user:
#             await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#             return None
#         return user
#     except HTTPException as e:
#         await websocket.close(code=e.status_code)
#         return None

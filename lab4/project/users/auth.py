import jwt
from jwt import PyJWTError
from passlib.context import CryptContext


from . import schemas,crud
from datetime import datetime, timedelta
from project.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SHA_ALGORITHM)
    return encoded_jwt

def get_user_from_token(db,token):
    username:str = None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SHA_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            # raise credentials_exception
            return None
    except PyJWTError:
        # raise credentials_exception
        return None
    user = crud.get_user_by_username(db, username)


    return user


from sqlalchemy.orm import Session
from . import models
from . import schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    print(f"finding user {email}")
    return db.query(models.User).filter(models.User.email == email).first()
def get_user_by_username(db: Session, username: str):
    print(f"finding user {username}")
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate,hashed_password: str):
    db_user = models.User(username=user.username, email=user.email,hashed_password=hashed_password,is_superuser=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, update_data: dict):
    db_user = get_user(db, user_id)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user
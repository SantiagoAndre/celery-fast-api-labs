from sqlalchemy.orm import Session
from . import models, schemas
from project.users.models import User,chatroom_member
from .models import Chatroom

def get_chatroom(db: Session, user: User, chatroom_id: int=None,name:str=None):
    if chatroom_id is not None:
        chatroom = db.query(models.Chatroom).filter(models.Chatroom.id == chatroom_id).first()
    else:
        chatroom = db.query(models.Chatroom).filter(models.Chatroom.name == name).first()

    print(chatroom)
    if chatroom and any(user.id == user.id for user in chatroom.users):
        return chatroom
    print("hola")

    return None
def get_chatrooms(db: Session, user: User, skip: int = 0, limit: int = 10):
    if user:
        print(user.username)
        return (
            db.query(models.Chatroom)
            .join(chatroom_member)  # Assuming you have an association table for many-to-many
            # .filter(chatroom_member.user_id == user.id)
            .filter(chatroom_member.c.user_id == user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return []

def create_chatroom(db: Session, chatroom: schemas.ChatRoomCreate, owner:User):
    db_chatroom = models.Chatroom(**chatroom.dict(), owner_id=owner.id)
    db_chatroom.users.append(owner)
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    return db_chatroom


def add_user_to_chatroom(db: Session, user: User, chatroom: Chatroom):
    # chatroom = db.query(models.Chatroom).filter(models.Chatroom.id == chatroom_id).first()
    if user and chatroom:
        chatroom.users.append(user)
        db.commit()
def remove_user_from_chatroom(db: Session, user: User, chatroom: Chatroom):
    # chatroom = db.query(models.Chatroom).filter(models.Chatroom.id == Chatroom.id).first()
    if user and chatroom:
        chatroom.users.remove(user)
        db.commit()
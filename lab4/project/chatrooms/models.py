from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from project.database import Base
from project.users.models import chatroom_member

class Chatroom(Base):
    __tablename__ = "chatrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    users = relationship('User', secondary=chatroom_member, back_populates='chatrooms')
    # messages = relationship("Message", back_populates="chatroom")
    users = relationship('User', secondary=chatroom_member, back_populates='chatrooms')

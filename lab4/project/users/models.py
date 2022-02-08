from sqlalchemy import Column, Integer, String, Sequence
from project.database import Base
from sqlalchemy import Table, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


chatroom_member = Table(
    'chatroom_member',  # Name of the table in the database
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),     # Foreign key column pointing to the users table
    Column('chatroom_id', Integer, ForeignKey('chatrooms.id'))  # Foreign key column pointing to the chatrooms table
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    chatrooms = relationship('Chatroom', secondary=chatroom_member, back_populates='users')
    is_active  = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)


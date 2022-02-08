from pydantic import BaseModel
from typing import List

class ChatRoomBase(BaseModel):
    name: str

class ChatRoomCreate(ChatRoomBase):
    pass

class ChatRoom(ChatRoomBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

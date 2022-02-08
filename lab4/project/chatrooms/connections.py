import json
from typing import List, Dict
from fastapi import WebSocket
from sqlalchemy.orm import Session
from collections import defaultdict
from project.users.models import User
from . import crud
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, user:User):
        await websocket.accept()
        self.active_connections[user.id].append(websocket)

    def disconnect(self, websocket: WebSocket, user: User):
        self.active_connections[user.id].remove(websocket)



    async def broadcast_to_room(self, db: Session,room: str, message: str, sender: User):
        chatroom  =crud.get_chatroom(db,sender,name = room)
        if  chatroom:
            sender_dict =  {"username": sender.username, "full_name": sender.full_name}
            for user in chatroom.users:
                if user.id != sender.id and user.id in  self.active_connections:
                    for connection in self.active_connections[user.id]:
                        await connection.send_text(json.dumps( {
                            "room": room,
                            "message": message,
                            "sender": sender_dict
                        }))

manager = ConnectionManager()

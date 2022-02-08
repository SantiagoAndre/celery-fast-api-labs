


import json
from fastapi import APIRouter, Depends, HTTPException, status,WebSocket,WebSocketDisconnect

from typing import List,Optional
from sqlalchemy.orm import Session
from . import crud, schemas
from project.database import get_db
from project.users.decorators import login_required
from project.users.auth import get_user_from_token
from project.users.models import User
from project.users.crud import get_user_by_username

router = APIRouter()

@router.post("/create/", response_model=schemas.ChatRoom)
def create_chatroom(chatroom: schemas.ChatRoomCreate, db: Session = Depends(get_db), current_user: User = Depends(login_required)):
    return crud.create_chatroom(db=db, chatroom=chatroom, owner=current_user)

@router.get("/", response_model=List[schemas.ChatRoom])
def read_chatrooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(login_required)):
    chatrooms = crud.get_chatrooms(db, current_user,skip=skip, limit=limit)
    return chatrooms



@router.post("/chatrooms/{chatroom_id}/add_user")
def add_user_to_chatroom_endpoint(
    chatroom_name: str, 
    username: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(login_required)
):
    # Perform some validation if necessary, e.g. checking if the current_user is allowed to add users
    # For example, you might check if current_user is the owner of the chatroom
    chatroom = crud.get_chatroom(db,current_user, name=chatroom_name)

    if chatroom is None or  chatroom.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to add users to this chatroom."
        )
    user_to_add = get_user_by_username(db, username)  # You need to implement this function
    if not user_to_add:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )
    crud.add_user_to_chatroom(db, user_to_add, chatroom)
    return {"msg": "User added to chatroom successfully"}

@router.post("/chatrooms/{chatroom_name}/remove_user")
def remove_user_from_chatroom_endpoint(
    chatroom_name: int, 
    username: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(login_required)
):
    # Perform similar validation as above
    chatroom = crud.get_chatroom(db,current_user,name=chatroom_name)
    if chatroom.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to remove users from this chatroom."
        )
    user_to_remove = get_user_by_username(db,username)  # You need to implement this function
    if not user_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )
    crud.remove_user_from_chatroom(db, user_to_remove, chatroom)
    return {"msg": "User removed from chatroom successfully"}


from fastapi import  WebSocket
from fastapi.responses import HTMLResponse


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MDExMjQwNDh9.qyJFqiwV3JoQEV78RpNASMlGHlh09v9OBPDr7WsLxqM'

            var ws = new WebSocket(`ws://localhost:8010/chatrooms/ws?token=${token}`);

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/wsclient")
async def get():
    return HTMLResponse(html)
from .connections import ConnectionManager
manager  = ConnectionManager()
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    # await websocket.accept()
    token = websocket.query_params.get('token')
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    user = get_user_from_token(db,token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(websocket, user)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            room = data_json['room']
            message = data_json['message']
            await manager.broadcast_to_room(db,room, message, user)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.username)
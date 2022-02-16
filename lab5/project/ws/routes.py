import json

# import socketio
from fastapi import APIRouter,Request
from fastapi import FastAPI, WebSocket
# from socketio import AsyncNamespace
from fastapi.templating import Jinja2Templates

from project import broadcast
from project.celery_utils import get_task_info
from project.config import settings

templates = Jinja2Templates(directory="project/ws/templates")

ws_router = APIRouter()

@ws_router.get("/form_ws/")
def form_ws_example(request: Request):
    return templates.TemplateResponse("ws_form.html", {"request": request})



@ws_router.websocket("/ws/task_status/{task_id}")
async def ws_task_status(websocket: WebSocket):
    await websocket.accept()
    task_id = websocket.scope["path_params"]["task_id"]
    await broadcast.connect()
    async with broadcast.subscribe(channel=task_id) as subscriber:
        # just in case the task already finish
        data = get_task_info(task_id)
        print(data)
        await websocket.send_json(data)

        async for event in subscriber:
            await websocket.send_json(json.loads(event.message))


async def update_celery_task_status(task_id: str):
    """
    This function is called by Celery worker in task_postrun signal handler
    """
    await broadcast.connect()
    await broadcast.publish(
        channel=task_id,
        message=json.dumps(get_task_info(task_id))  # RedisProtocol.publish expect str
    )
    await broadcast.disconnect()


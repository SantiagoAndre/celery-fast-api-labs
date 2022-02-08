from fastapi import FastAPI
from .celery_utils import create_celery  # new

def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()  # new

    from .users import router as users_router
    from .chatrooms.routers import router as chatroom_router

    # from fastapi import  WebSocket
    app.include_router(users_router, prefix="/users")
    app.include_router(chatroom_router, prefix="/chatrooms")
    # @app.websocket("/ws")
    # async def websocket_endpoint(websocket: WebSocket):
    #     await websocket.accept()
    #     while True:
    #         data = await websocket.receive_text()
    #         await websocket.send_text(f"Message text was: {data}")



    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app


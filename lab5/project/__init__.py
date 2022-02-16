from fastapi import FastAPI
from broadcaster import Broadcast
from project.config import settings
from .celery_utils import create_celery  # new


broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)

def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()  # new

    from .users import router as users_router
    app.include_router(users_router, prefix="/users")
    from project.ws import ws_router
    app.include_router(ws_router)
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app


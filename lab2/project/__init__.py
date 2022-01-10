from fastapi import FastAPI
from .celery_utils import create_celery  # new

def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()  # new

    from .users import router as users_router
    app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app


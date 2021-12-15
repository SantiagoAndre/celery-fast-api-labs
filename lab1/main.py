from celery import Celery
from celery.result import AsyncResult

from fastapi import FastAPI
import os
app = FastAPI()


celery = Celery(
    __name__,
    broker= os.environ['CELERY_BROKER_URL'],
    backend=os.environ['CELERY_RESULT_BACKEND'] 
)



@celery.task
def divide(x, y):
    import time
    time.sleep(2
    )
    return x / y


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/divide-celery")
async def divide_route(a: float, b: float):
    task = divide.delay(a,b)
    # print(dir(answer))
    return {"task_id": task.task_id}


@app.get("/query-task-status")
async def query_celery_task(task_id: str):
    # Create an AsyncResult object based on the task_id
    task_result = AsyncResult(task_id, app=celery)
    
    # Check the status of the task
    status = task_result.status
    
    # If the task is successful, you can also get the result
    result = task_result.result if task_result.successful() else None

    return {
        "task_id": task_id,
        "status": status,
        "result": result
    }
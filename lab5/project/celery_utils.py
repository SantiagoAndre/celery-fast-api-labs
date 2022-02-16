from celery import Celery
from celery.result import AsyncResult

def create_celery():
    celery_app = Celery(__name__)
    celery_app.config_from_object("project.config.settings", namespace="CELERY")
    return celery_app

def get_task_info(task_id):
    """
    return task info according to the task_id
    """
    task = AsyncResult(task_id)
    state = task.state

    if state == "FAILURE":
        error = str(task.result)
        response = {
            "state": task.state,
            "error": error,
        }
    else:
        response = {
            "state": task.state,
            "task_id": task_id,
        # "status": status,
            "result": task.result
        }
    return response
from celery import Celery

def create_celery():
    celery_app = Celery(__name__)
    celery_app.config_from_object("project.config.settings", namespace="CELERY")
    return celery_app

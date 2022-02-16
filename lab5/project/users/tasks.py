from celery import shared_task
import time

@shared_task
def divide(x, y):
    time.sleep(10)
    return x / y


import smtplib
from email.message import EmailMessage
from project.config import settings

# @shared_task
# def send_email(subject, to_email, body):
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg['Subject'] = subject
#     msg['From'] = settings.EMAIL_FROM # Your email
#     msg['To'] = to_email
    
#     # Connect to your email server. You might want to use a library like yagmail for ease.
#     with smtplib.SMTP('smtp.example.com', 587) as server:
#         server.login(settings.EMAIL_FROM, settings.EMAIL_APP_PASSWORD) 
#         server.send_message(msg)
    
#     return 'Email sent successfully!'


@shared_task
def send_email(subject, to_email, body):
    time.sleep(15)
    return "success"


from asgiref.sync import async_to_sync
from celery.signals import task_postrun

@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.ws.routes import update_celery_task_status
    async_to_sync(update_celery_task_status)(task_id)

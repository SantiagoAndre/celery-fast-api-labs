from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, schemas
from project.database import get_db
from .tasks import send_email
from .auth import get_password_hash, verify_password,create_access_token
from .models import User
from .decorators import superuser_required
# from . import models, tasks  # noqa

router = APIRouter()

@router.post("/", response_model=schemas.UserOut)
def create_user_route(new_user: schemas.UserCreate, db: Session = Depends(get_db),_:User = Depends(superuser_required)):

    db_user = crud.get_user_by_email(db, email=new_user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(new_user.password)
   
    response =  crud.create_user(db=db, user=new_user,hashed_password=hashed_password)
    if response.id:
        celery_task = send_email.delay("Success registration os SANTOSDEV platform",new_user.email,"")
        print("Celery task created: " ,celery_task.task_id)

    return response

@router.post("/token/", response_model=schemas.TokenResponse)
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    print(access_token)
    return {"access_token": str(access_token)}




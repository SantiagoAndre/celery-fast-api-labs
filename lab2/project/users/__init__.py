from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, models, schemas
from project.database import SessionLocal
from .tasks import send_email
# from . import models, tasks  # noqa

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserOut)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(db)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    response =  crud.create_user(db=db, user=user)
    if response.id:
        celery_task = send_email.delay("Success registration os SANTOSDEV platform",user.email,"")
        print("Celery task created: " ,celery_task.task_id)

    return response


@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[schemas.UserOut])
def read_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.patch("/{user_id}", response_model=schemas.UserOut)
def update_user_route(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user.dict())

@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"detail": "User deleted"}

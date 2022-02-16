from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    task_id:str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str
    grant_type:str


class TokenResponse(BaseModel):
    access_token: str

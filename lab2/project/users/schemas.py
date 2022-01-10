from pydantic import BaseModel

# Schema for user creation
class UserCreate(BaseModel):
    username: str
    email: str

# Schema for user response
class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

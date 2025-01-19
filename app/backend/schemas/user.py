from pydantic import BaseModel
from typing import Optional, List


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class UserInDB(BaseModel):
    username: str
    firstname: str
    age: int
    slug: str
    lastname: str
    id: int

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: Optional[List[UserInDB]] = None

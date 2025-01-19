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


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool = False


class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool


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


class TaskInDB(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool
    id: int
    user_id: int

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: Optional[List[TaskInDB]] = None

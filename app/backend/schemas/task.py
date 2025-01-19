from pydantic import BaseModel
from typing import Optional, List


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


class TaskInDB(BaseModel):
    id: int
    priority: int
    user_id: int
    content: str
    title: str
    completed: bool
    slug: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, task):
        return cls(
            id=task.id,
            priority=task.priority,
            user_id=task.user_id,
            content=task.content,
            title=task.title,
            completed=task.completed,
            slug=task.title.lower(),
        )


class TaskList(BaseModel):
    tasks: Optional[List[TaskInDB]] = None

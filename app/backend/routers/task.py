import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.backend.models.task import Task
from app.backend.schemas.schemas import (
    TaskList,
    TaskInDB,
    CreateTask,
    UpdateTask,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

task_router = APIRouter(prefix='/task', tags=['task'])


@task_router.get('/', response_model=TaskList)
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    result = db.scalars(select(Task)).all()
    if not result:
        return TaskList(tasks=[])
    tasks = [TaskInDB.model_validate(task) for task in result]
    return TaskList(tasks=tasks)


@task_router.get('/{task_id}', response_model=TaskInDB)
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.scalar(select(Task).where(Task.id == task_id))
    if result:
        return TaskInDB.model_validate(result)
    else:
        raise HTTPException(status_code=404, detail='Task was not found')


@task_router.post('/create_task')
async def create_task(
    task: CreateTask, db: Annotated[Session, Depends(get_db)]
):
    try:
        logger.info(f'Creating task with data: {task.model_dump()}')
        new_task = Task(**task.model_dump())
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful',
        }
    except Exception as e:
        logger.error(f'Error creating task: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')


@task_router.put('/update/{task_id}')
async def update_task(
    task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]
):
    result = db.scalar(select(Task).where(Task.id == task_id))
    if result:
        db.execute(
            update(Task).where(Task.id == task_id).values(**task.model_dump())
        )
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!',
        }
    else:
        raise HTTPException(status_code=404, detail='Task was not found')


@task_router.delete('/delete/{task_id}')
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.scalar(select(Task).where(Task.id == task_id))
    if result:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task deletion is successful!',
        }
    else:
        raise HTTPException(status_code=404, detail='Task was not found')

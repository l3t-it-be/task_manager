import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from starlette import status

from app.backend.db_depends import get_db
from app.backend.models.user import User
from app.backend.models.task import Task
from app.backend.schemas.user import (
    UserList,
    UserInDB,
    CreateUser,
    UpdateUser,
)
from app.backend.schemas.task import TaskList, TaskInDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_router = APIRouter(prefix='/user', tags=['user'])


@user_router.get('/', response_model=UserList)
async def all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.scalars(select(User)).all()
    if not result:
        return UserList(users=[])
    users = [UserInDB.model_validate(user) for user in result if user.slug]
    return UserList(users=users)


@user_router.get('/{user_id}', response_model=UserInDB)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.scalar(select(User).where(User.id == user_id))
    if result and result.slug:
        return UserInDB.model_validate(result)
    else:
        raise HTTPException(status_code=404, detail='User was not found')


@user_router.post('/create_user')
async def create_user(
    user: CreateUser, db: Annotated[Session, Depends(get_db)]
):
    try:
        logger.info(f'Creating user with data: {user.model_dump()}')
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful',
        }
    except Exception as e:
        logger.error(f'Error creating user: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')


@user_router.put('/update/{user_id}')
async def update_user(
    user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]
):
    result = db.scalar(select(User).where(User.id == user_id))
    if result:
        db.execute(
            update(User).where(User.id == user_id).values(**user.model_dump())
        )
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful!',
        }
    else:
        raise HTTPException(status_code=404, detail='User was not found')


@user_router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.scalar(select(User).where(User.id == user_id))
    if result:
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User deletion is successful!',
        }
    else:
        raise HTTPException(status_code=404, detail='User was not found')


@user_router.get('/{user_id}/tasks', response_model=TaskList)
async def tasks_by_user_id(
    user_id: int, db: Annotated[Session, Depends(get_db)]
):
    result = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if not result:
        return TaskList(tasks=[])
    tasks = [TaskInDB.from_orm(task) for task in result]
    return TaskList(tasks=tasks)

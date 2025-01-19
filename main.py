import uvicorn
from fastapi import FastAPI

from app.backend.db import Base, engine
from app.backend.routers import user_router, task_router

app = FastAPI()


@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}


routers = (user_router, task_router)
[app.include_router(router) for router in routers]

# Ensure the database tables are created
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost')

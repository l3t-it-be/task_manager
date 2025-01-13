import uvicorn
from fastapi import FastAPI

from app.routers.task import task_router
from app.routers.user import user_router

app = FastAPI()

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}

routers = (user_router, task_router)
[app.include_router(router) for router in routers]

if __name__ == '__main__':
    uvicorn.run(app, host='localhost')

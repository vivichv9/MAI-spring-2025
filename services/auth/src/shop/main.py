import uvicorn
from fastapi import FastAPI

from apps import apps_router

app = FastAPI()

app.include_router(router=apps_router)
def start():
    uvicorn.run(app="shop.main:app", reload=True, port=14882)

import uvicorn
from fastapi import FastAPI
from core.logger import setup_logging

from apps import apps_router
setup_logging(log_file_path="/tmp/logs/logs.txt", service_name="shop-app")

app = FastAPI()

app.include_router(router=apps_router)
def start():
    uvicorn.run(app="shop.main:app", reload=True, port=14882)

from fastapi import APIRouter

from apps.auth.routes import auth_router

apps_router = APIRouter()

# Подключаем маршруты приложения auth
apps_router.include_router(router=auth_router)
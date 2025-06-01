from typing import Annotated

import logging

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from apps.auth.depends import get_current_user
from apps.auth.schemas import AuthUser, UserReturnData, UserVerifySchema, UserInDB, LoginUser
from apps.auth.services import UserService

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get(path="/get-user", status_code=status.HTTP_200_OK, response_model=UserVerifySchema)
async def get_auth_user(user: Annotated[UserVerifySchema, Depends(get_current_user)]) -> UserVerifySchema:
    return user

@auth_router.post(
    "/register",
    response_model=UserReturnData,
    status_code=status.HTTP_201_CREATED
)
async def registration(
    user: AuthUser,
    service: UserService = Depends(UserService)
) -> UserReturnData:
    logger.info(
        "Попытка регистрации нового пользователя",
        extra={"custom_field": f"register:{user.email}"}
    )
    return await service.register_user(user=user)

@auth_router.get(path="/logout", status_code=status.HTTP_200_OK)
async def logout(
    user: Annotated[UserVerifySchema, Depends(get_current_user)],
    service: UserService = Depends(UserService),
) -> JSONResponse:
    logger.info(
        "Пользователь вышел из системы",
        extra={"custom_field": f"logout:{user.user_id}"}
    )
    return await service.logout_user(user=user)

@auth_router.get(path="/register_confirm", status_code=status.HTTP_200_OK)
async def confirm_registration(token: str, service: UserService = Depends(UserService)) -> dict[str, str]:
    await service.confirm_user(token=token)
    return {"message": "Электронная почта подтверждена"}

@auth_router.post(path="/login", status_code=status.HTTP_200_OK)
async def login(user: LoginUser, service: UserService = Depends(UserService)) -> JSONResponse:
    return await service.login_user(user=user)

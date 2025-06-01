import uuid
import datetime

from pydantic import BaseModel, EmailStr, Field, conint


class GetUserByID(BaseModel):
    user_id: uuid.UUID | str


class GetUserByEmail(BaseModel):
    email: EmailStr


class AuthUser(GetUserByEmail):
    password: str
    first_name: str
    last_name: str
    age: int

class LoginUser(GetUserByEmail):
    password: str

class UserInDB(GetUserByEmail):
    password_hash: str

class CreateUser(GetUserByEmail):
    password_hash: str
    first_name: str
    last_name: str
    age: int


class UserReturnData(GetUserByID, GetUserByEmail):
    first_name: str
    last_name: str
    age: int

    is_active: bool
    is_verified: bool
    is_superuser: bool
    registration_dttm: datetime.datetime
    updated_at: datetime.datetime

class GetUserWithIDAndEmail(GetUserByID, UserInDB):
    pass

class UserVerifySchema(GetUserByID, GetUserByEmail):
    session_id: uuid.UUID | str | None = None
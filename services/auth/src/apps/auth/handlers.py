import datetime
import uuid

import jwt
from fastapi import HTTPException
from starlette import status
from passlib.context import CryptContext

from apps.auth.named_tuples import CreateTokenTuple
from core.settings import settings

class AuthHandler:
    secret = settings.secret_key.get_secret_value()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(raw_password, hashed_password)

    async def create_access_token(self, user_id: uuid.UUID) -> CreateTokenTuple:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=settings.access_token_expire)
        session_id = str(uuid.uuid4())

        data = {
            "exp": expire,
            "session_id": session_id,
            "user_id": str(user_id)
        }

        encoded_jwt = jwt.encode(payload=data, key=self.secret, algorithm="HS256")

        return CreateTokenTuple(encoded_jwt=encoded_jwt, session_id=session_id)

    async def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(jwt=token, key=self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
import fastapi
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import json

from starlette.responses import JSONResponse

from db import Database
import httpx
import jwt
import uvicorn
import os
from typing import List
from dotenv import load_dotenv
from log import *
from datetime import datetime, timezone
from fastapi import Body
from pydantic import BaseModel
from dotenv import load_dotenv
class BalanceItem(BaseModel):
    user_id: str
    amount: float



load_dotenv()
PRODUCTS_SERVICE_URL = "http://127.0.0.1:8001"
app = FastAPI()

db_params = {
"host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT")),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}


db = Database(db_params)
SECRET_KEY = os.getenv("SECRET_KEY")
auth_scheme = HTTPBearer()
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    # try:
    #     payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    #     return payload
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/pay")
async def pay(user_data: dict = Depends(verify_token),body:BalanceItem = Body(...)):
    user_balance = float(db.get_user_balance(body.user_id))
    if (user_balance < body.amount):
        return JSONResponse({"result": "not enough balance"}, status_code=500)
    else:
        res = db.set_balance(body.user_id,user_balance-body.amount)
        db.add_payment(body.user_id,user_balance-body.amount,datetime.now(timezone.utc))
        if res:
            save_log("changing data", "development", f"user: {body.user_id} balance changed", "INFO",
                     "finance_service")
            return JSONResponse({"result": "OK"}, status_code=200)
        else:
            return JSONResponse({"result": "error"}, status_code=500)
@app.post("/refill_user_balance")
async def refill_user_balance(user_data: dict = Depends(verify_token),body:BalanceItem = Body(...)):
    user_balance = db.get_user_balance(body.user_id)
    new_balance = float(user_balance) + body.amount
    res = db.set_balance(body.user_id, new_balance)
    if res:
        save_log("changing data", "development", f"user: {body.user_id} balance changed", "INFO",
                 "finance_service")
        return JSONResponse({"result": "OK"}, status_code=200)
    else:
        return JSONResponse({"result": "error"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)

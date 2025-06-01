import fastapi
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import json

from starlette.responses import JSONResponse

from db import Database
import httpx
import jwt
import uvicorn
import os, requests
from log import *
from typing import List
from dotenv import load_dotenv
from dotenv import load_dotenv
from datetime import datetime, timezone
from fastapi import Body
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
class GetUserOrdersItem(BaseModel):
    user_id: str
class CreateOrderItem(BaseModel):
    user_id: str
    product_ids: List[int]
    product_costs: List[float]
    pick_up_id: int
    order_type: str
class CancelOrderItem(BaseModel):
    user_id: str
    order_id: int

load_dotenv()
FINANCE_SERVICE_URL = os.getenv("FINANCE_SERVICE_URL")
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
    return credentials
@app.post("/create_order")
def create_order(user_data: dict = Depends(verify_token),body:CreateOrderItem = Body(...)):
    order_id = db.create_order(body.user_id,body.product_ids,body.product_costs,datetime.now(timezone.utc),body.pick_up_id, body.order_type)
    body_ = {
        "user_id": body.user_id,
        "amount": sum(body.product_costs)
    }
    header = {
        "Authorization": f"Bearer {user_data.credentials}"  # если verify_token возвращает credentials
    }

    response = requests.post(f"{FINANCE_SERVICE_URL}/pay",json=body_,headers=header)

    if order_id and response.status_code == 200:
        save_log("adding data", "development", f"order created: user_id:{body.user_id} order_id {order_id}", "INFO",
                 "orders_service")

        return JSONResponse({"order_id":order_id},status_code=200)
    else:
        if response.status_code == 500:
            # return JSONResponse(response,status_code=response.status_code)
            return response.json()
        else:
            return JSONResponse({"order_id":None},status_code=500)




@app.post("/get_user_orders")
async def get_user_orders(user_data: dict = Depends(verify_token),body:GetUserOrdersItem = Body(...)):
    orders = db.get_user_orders(body.user_id)
    result = [
        [*row[:4], row[4].isoformat(), *row[5:]] for row in orders
    ]
    if not orders:
        return JSONResponse({"orders": []},status_code=200)
    else:
        return JSONResponse({"orders":result},status_code=200)
@app.post("/cancel_order")
async def cancel_order(user_data: dict = Depends(verify_token),body:CancelOrderItem = Body(...)):
    order = db.get_order(body.order_id)
    amount = sum(order[3])
    body_ = {
        "user_id": body.user_id,
        "amount": amount
    }
    header = {
        "Authorization": f"Bearer {user_data.credentials}"  # если verify_token возвращает credentials
    }

    response = requests.post(f"{FINANCE_SERVICE_URL}/refill_user_balance", json=body_, headers=header)
    is_canceled = db.cancel_order(body.order_id)

    if is_canceled:
        save_log("adding data", "development", f"order canceled: user_id:{body.user_id} order_id {body.order_id}", "INFO",
                 "orders_service")
        return JSONResponse({"status": "canceled"},status_code=200)
    else:
        return JSONResponse({"status": "not found"},status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
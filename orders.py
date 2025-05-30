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
from dotenv import load_dotenv
from datetime import datetime, timezone



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
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/create_order")
async def create_order(req_data = Depends(verify_token)):
    user_id = req_data["user_id"]

    order_id = db.create_order(user_id,req_data["product_ids"],req_data["product_costs"],datetime.now(timezone.utc),req_data["pickup_id"],req_data["order_type"])
    if order_id:
        return JSONResponse({"order_id":order_id})
    else:
        return JSONResponse({"order_id":None},status_code=500)



@app.get("/purchases")
async def get_purchases(user_data = Depends(verify_token)):
    user_id = user_data["user_id"]
    product_ids = db.get_purchases(user_id)

    if not product_ids:
        return {"products": []}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PRODUCTS_SERVICE_URL, json={"product_ids": product_ids})
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Ошибка при обращении к сервису продуктов: {e}")

    products_info = response.json()
    return {"products": products_info}
@app.post("/cancel_order")
async def cancel_order(req_data = Depends(verify_token)):
    user_id = req_data["user_id"]

    is_canceled = db.cancel_order(req_data["order_id"])
    if is_canceled:
        return JSONResponse({"status: canceled"},status_code=200)
    else:
        return JSONResponse({"status:not found"},status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
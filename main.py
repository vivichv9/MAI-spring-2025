import fastapi
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import json
from db import Database
import httpx
import jwt
import uvicorn
from dotenv import load_dotenv
from crypt import *
import os
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
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/cart")
async def get_cart(user_data = Depends(verify_token)):
    user_id = user_data["user_id"]
    product_ids = db.get_cart(user_id)

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


@app.get("/change_password")
async def change_password(user_data = Depends(verify_token)):
    user_id = user_data["user_id"]
    new_pass = user_data["new_password"]
    res =  db.change_password(user_id,hash_password(new_pass))
    if res:
        return JSONResponse("",status_code=200)
    else:
        return JSONResponse("",status_code=401)

@app.get("/get_orders")
async def get_orders(req_data = Depends(verify_token)):
    user_id = req_data["user_id"]
    product_ids = db.get_orders(user_id)

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
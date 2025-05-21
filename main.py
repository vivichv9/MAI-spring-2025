import fastapi
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import json
from db import Database
import httpx
import jwt
import uvicorn



PRODUCTS_SERVICE_URL = "http://127.0.0.1:8001"
app = FastAPI()

with open("./params.json", "r") as file:
    db_params = json.load(file)
db = Database(db_params)

SECRET_KEY = "my_secret"
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

@app.get("/cart/{user_id}")
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


@app.get("/purchases/{user_id}")
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
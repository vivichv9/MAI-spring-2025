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
from log import *
from pydantic import BaseModel
load_dotenv()

from fastapi import Body
from pydantic import BaseModel

class ChangePasswordItem(BaseModel):
    user_id: str
    new_password: str
class GetOrdersItem(BaseModel):
    user_id: str
class ChangeNameItem(BaseModel):
    user_id: str
    new_name: str
class ChangeSurnameItem(BaseModel):
    user_id: str
    new_surname: str
class ChangeEmailItem(BaseModel):
    user_id: str
    new_email: str
class ChangeAgeItem(BaseModel):
    user_id: str
    new_age: int
class GetCartItem(BaseModel):
    user_id: str
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


@app.post("/cart")
async def get_cart(user_data: dict = Depends(verify_token),body:GetCartItem = Body(...)):
    user_id = body.user_id
    product_ids = db.get_cart(user_id)
    if not product_ids:
        return JSONResponse({"products": []},status_code=200)
    return JSONResponse({"products": product_ids}, status_code=200)


@app.post("/change_password")
async def change_password(user_data: dict = Depends(verify_token),body:ChangePasswordItem = Body(...)):
    new_pass = body.new_password
    user_id  = body.user_id
    res =  db.change_password(user_id,hash_password(new_pass))
    if res:
        save_log("changing data","development",f"user: {user_id} changed password","INFO","personal_account_service")
        return JSONResponse(content= {"result": "OK"},status_code=200)
    else:
        return JSONResponse("",status_code=401)




@app.post("/change_name")
async def change_name(user_data: dict = Depends(verify_token),body:ChangeNameItem = Body(...)):
    user_id = body.user_id
    new_name = body.new_name
    is_name_changed = db.change_user_name(user_id,new_name)
    if is_name_changed:
        save_log("changing data","development",f"user: {user_id} changed name to {new_name}","INFO","personal_account_service")
        return JSONResponse({"result":"changed"},status_code=200)
    else:
        return JSONResponse({"status":"not changed"},status_code=500)

@app.post("/change_surname")
async def change_surname(user_data: dict = Depends(verify_token),body:ChangeSurnameItem = Body(...)):
    user_id = body.user_id
    new_surname = body.new_surname
    is_surname_changed = db.change_user_surname(user_id,new_surname)
    if is_surname_changed:
        save_log("changing data", "development", f"user: {user_id} changed name to {new_surname}", "INFO","personal_account_service")
        return JSONResponse({"result":"changed"},status_code=200)
    else:
        return JSONResponse({"status":"not changed"},status_code=500)
@app.post("/change_email")
async def change_email(user_data: dict = Depends(verify_token),body:ChangeEmailItem = Body(...)):
    user_id = body.user_id
    new_email = body.new_email
    is_email_changed = db.change_user_email(user_id,new_email)
    if is_email_changed:
        save_log("changing data", "development", f"user: {user_id} changed email to {new_email}", "INFO","personal_account_service")
        return JSONResponse({"result":"changed"},status_code=200)
    else:
        return JSONResponse({"status":"not changed"},status_code=500)
@app.post("/change_age")
async def change_age(user_data: dict = Depends(verify_token),body:ChangeAgeItem = Body(...)):
    user_id = body.user_id
    new_age = body.new_age
    is_age_changed = db.change_user_age(user_id,new_age)
    if is_age_changed:
        save_log("changing data", "development", f"user: {user_id} changed age to {new_age}", "INFO","personal_account_service")
        return JSONResponse({"result":"changed"},status_code=200)
    else:
        return JSONResponse({"status":"not changed"},status_code=500)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
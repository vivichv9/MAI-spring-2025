from typing import List
import logging
from fastapi import FastAPI, Depends, HTTPException, Query

import app.logger

from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine
from app.dependencies import get_db


logger = logging.getLogger(__name__)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Products Microservice")


@app.get(
    "/products/random",
    response_model=List[schemas.ProductResponse],
)
def get_random_products(
    n: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    products = crud.get_random_products(db=db, n=n)
    return products


@app.get(
    "/products/search",
    response_model=List[schemas.ProductResponse],
)
def search_products(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    products = crud.search_products_by_name(db=db, name_substr=name)
    return products


@app.post(
    "/products/bulk",
    response_model=List[schemas.ProductResponse],
)
def get_products_by_ids(
    payload: schemas.ProductIDsRequest,
    db: Session = Depends(get_db)
):
    products = crud.get_products_by_ids(db=db, ids=payload.ids)
    return products

@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=201,
)
def add_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(get_db),
):
    logger.info(
        "Попытка добавить новый продукт",
        extra={"custom_field": f"adding_product_{product_in.product_id}"}
    )
    existing = crud.get_product_by_id(db=db, product_id=product_in.product_id)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Продукт с product_id={product_in.product_id} уже существует.",
        )

    new_product = crud.create_product(db=db, product_in=product_in)
    logger.info(
        "Продукт создан успешно",
        extra={"custom_field": f"created_{new_product.product_id}"}
    )
    return new_product



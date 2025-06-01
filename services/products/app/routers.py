from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Product
from app.schemas import ProductResponse, ProductCreate

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.get(
    "/products/random",
    response_model=List[ProductResponse],
)
def get_random_products(
    n: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    products = (
        db.query(Product)
        .order_by(func.random())
        .limit(n)
        .all()
    )
    if not products:
        return []
    return products


@products_router.get(
    "/products/search",
    response_model=List[ProductResponse],
)
def search_products(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    pattern = f"%{name}%"
    products = (
        db.query(Product)
        .filter(Product.name.ilike(pattern))
        .all()
    )
    return products


@products_router.post(
    "/products",
    response_model=ProductResponse,
    status_code=201,
)
def add_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Product).filter(Product.product_id == product_in.product_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Продукт с product_id={product_in.product_id} уже существует.",
        )

    new_product = Product(
        product_id=product_in.product_id,
        price=product_in.price,
        weight=product_in.weight,
        description=product_in.description,
        name=product_in.name,
        discount=product_in.discount,
        amount=product_in.amount,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

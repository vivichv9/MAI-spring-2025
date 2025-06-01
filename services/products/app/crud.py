# app/crud.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas


def get_random_products(db: Session, n: int) -> List[models.Product]:
    return (
        db.query(models.Product)
        .order_by(func.random())
        .limit(n)
        .all()
    )


def search_products_by_name(db: Session, name_substr: str) -> List[models.Product]:
    pattern = f"%{name_substr}%"
    return (
        db.query(models.Product)
        .filter(models.Product.name.ilike(pattern))
        .all()
    )


def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()


def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    new_product = models.Product(
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

def get_products_by_ids(db: Session, ids: List[int]) -> List[models.Product]:
    if not ids:
        return []
    return (
        db.query(models.Product)
        .filter(models.Product.product_id.in_(ids))
        .all()
    )
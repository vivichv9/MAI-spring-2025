# app/schemas.py
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    price: Decimal = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    description: Optional[str] = Field(None)
    name: str = Field(..., min_length=1)
    discount: Optional[float] = Field(0.0, ge=0.0, le=1.0)
    amount: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    product_id: int = Field(...)


class ProductResponse(ProductBase):
    product_id: int

    class Config:
        orm_mode = True



class ProductIDsRequest(BaseModel):
    ids: List[int] = Field(
        ...,
    )
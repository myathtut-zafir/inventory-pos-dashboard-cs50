from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    sku: str = Field(max_length=50)
    name: str = Field(max_length=255)
    price: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    stock_quantity: int = Field(ge=0, default=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = Field(default=None, max_length=50)
    name: str | None = Field(default=None, max_length=255)
    price: Decimal | None = Field(default=None, max_digits=10, decimal_places=2, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

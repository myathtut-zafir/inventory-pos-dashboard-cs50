import re
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

SKU_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9\-]*$")


class ProductBase(BaseModel):
    sku: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(ge=0, le=1_000_000, default=0)

    @field_validator("sku", mode="before")
    @classmethod
    def _normalize_sku(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("SKU must be a string")
        v = v.strip().upper()
        if not SKU_PATTERN.match(v):
            raise ValueError(
                "SKU must contain only uppercase letters, digits, and hyphens, "
                "and must start with a letter or digit"
            )
        return v

    @field_validator("name", mode="before")
    @classmethod
    def _strip_name(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Name must be a string")
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty")
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = Field(default=None, min_length=3, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int | None = Field(default=None, ge=0, le=1_000_000)


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

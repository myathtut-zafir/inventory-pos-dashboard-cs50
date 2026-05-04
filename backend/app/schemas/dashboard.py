from decimal import Decimal

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_sale_amount: Decimal
    total_sale_quantity: int
    total_products: int


class MonthlyOrderCount(BaseModel):
    month: str
    count: int


class RoleCount(BaseModel):
    role: str
    count: int

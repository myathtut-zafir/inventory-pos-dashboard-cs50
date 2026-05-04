from decimal import Decimal

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_sale_amount: Decimal
    total_sale_quantity: int
    total_products: int

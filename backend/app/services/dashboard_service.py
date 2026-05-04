from decimal import Decimal
from typing import cast

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.schemas.dashboard import DashboardSummary


def get_summary(db: Session) -> DashboardSummary:
    total_sale_amount: Decimal = cast(
        Decimal,
        db.scalar(
            select(func.coalesce(func.sum(Sale.total_amount), Decimal("0")))
        ),
    )
    total_sale_quantity: int = cast(
        int,
        db.scalar(select(func.coalesce(func.sum(SaleItem.quantity), 0))),
    )
    total_products: int = cast(
        int,
        db.scalar(select(func.count(Product.id))),
    )

    return DashboardSummary(
        total_sale_amount=total_sale_amount,
        total_sale_quantity=total_sale_quantity,
        total_products=total_products,
    )

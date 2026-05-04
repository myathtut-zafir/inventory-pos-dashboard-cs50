from decimal import Decimal
from typing import cast

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.user import User
from app.schemas.dashboard import DashboardSummary, MonthlyOrderCount, RoleCount

KNOWN_ROLES: tuple[str, ...] = ("admin", "staff")


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


def get_sales_count_by_month(db: Session) -> list[MonthlyOrderCount]:
    month_col = func.to_char(Sale.created_at, "YYYY-MM").label("month")
    rows = db.execute(
        select(month_col, func.count(Sale.id).label("count"))
        .group_by(month_col)
        .order_by(month_col)
    ).all()

    return [
        MonthlyOrderCount(month=cast(str, row.month), count=cast(int, row.count))
        for row in rows
    ]


def get_users_by_role(db: Session) -> list[RoleCount]:
    rows = db.execute(
        select(User.role, func.count(User.id).label("count")).group_by(User.role)
    ).all()
    counts: dict[str, int] = {cast(str, row.role): cast(int, row.count) for row in rows}

    return [RoleCount(role=role, count=counts.get(role, 0)) for role in KNOWN_ROLES]

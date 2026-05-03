from collections import defaultdict
from collections.abc import Sequence
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.schemas.sale import SaleCreate


def _sale_with_relations_query():
    return select(Sale).options(
        joinedload(Sale.user),
        selectinload(Sale.items).joinedload(SaleItem.product),
    )


def list_sales(db: Session) -> Sequence[Sale]:
    return db.scalars(
        _sale_with_relations_query().order_by(Sale.id.desc())
    ).unique().all()


def get_sale_with_relations(db: Session, sale_id: int) -> Sale | None:
    return db.scalars(
        _sale_with_relations_query().where(Sale.id == sale_id)
    ).unique().one_or_none()


def create_sale(db: Session, data: SaleCreate, user_id: int) -> Sale:
    requested_ids = {item.product_id for item in data.items}
    requested_qty: dict[int, int] = defaultdict(int)
    for item in data.items:
        requested_qty[item.product_id] += item.quantity

    products = db.scalars(
        select(Product)
        .where(Product.id.in_(requested_ids))
        .with_for_update()
    ).all()
    products_by_id = {p.id: p for p in products}

    missing = requested_ids - products_by_id.keys()
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product(s) not found: {sorted(missing)}",
        )

    insufficient = [
        f"product {pid} (need {qty}, have {products_by_id[pid].stock_quantity})"
        for pid, qty in requested_qty.items()
        if products_by_id[pid].stock_quantity < qty
    ]
    if insufficient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Insufficient stock for: {', '.join(insufficient)}",
        )

    total_amount = Decimal("0")
    sale = Sale(user_id=user_id, total_amount=Decimal("0"))

    for item in data.items:
        product = products_by_id[item.product_id]
        unit_price = product.price
        subtotal = unit_price * item.quantity
        total_amount += subtotal

        sale.items.append(
            SaleItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )
        )

    sale.total_amount = total_amount

    for product_id, qty in requested_qty.items():
        products_by_id[product_id].stock_quantity -= qty

    db.add(sale)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return get_sale_with_relations(db, sale.id)

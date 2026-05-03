from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


def list_products(db: Session) -> Sequence[Product]:
    return db.scalars(select(Product).order_by(Product.id)).all()

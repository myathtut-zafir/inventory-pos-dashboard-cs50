from fastapi import APIRouter

from app.schemas.product import ProductRead

router = APIRouter(prefix="/products", tags=["products"])


_STATIC_PRODUCTS: list[ProductRead] = [
    ProductRead(id=1, name="Coca-Cola 330ml", sku="BEV-COKE-330", quantity=120, price=0.99),
    ProductRead(id=2, name="Lay's Classic 50g", sku="SNK-LAYS-050", quantity=45, price=1.50),
    ProductRead(id=3, name="Colgate Toothpaste 100g", sku="HYG-COLG-100", quantity=30, price=2.75),
]


@router.get("", response_model=list[ProductRead])
def list_products() -> list[ProductRead]:
    return _STATIC_PRODUCTS

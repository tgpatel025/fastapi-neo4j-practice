from app.routers.categories import router as categories_router
from app.routers.customers import router as customers_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router
from app.routers.suppliers import router as suppliers_router

__all__ = [
    "categories_router",
    "customers_router",
    "orders_router",
    "products_router",
    "suppliers_router",
]

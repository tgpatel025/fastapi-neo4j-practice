from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import (
    close_database,
    configure_database,
    connect_database,
    read_transaction,
)
from app.routers import (
    categories_router,
    customers_router,
    orders_router,
    products_router,
    suppliers_router,
)
from app.services.exceptions import ServiceError

configure_database()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    connect_database()
    yield
    close_database()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(ServiceError)
async def handle_service_error(_: Request, exc: ServiceError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/", include_in_schema=False)
def health_check() -> bool:
    with read_transaction():
        return True


app.include_router(products_router)
app.include_router(categories_router)
app.include_router(suppliers_router)
app.include_router(customers_router)
app.include_router(orders_router)

from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.models import Category, Product, Supplier
from app.schemas import (
    CategoryResponse,
    ProductCreate,
    ProductOrderLineResponse,
    ProductResponse,
    ProductUpdate,
    SupplierResponse,
)
from app.services import CrudService, RelationshipService

router = APIRouter(prefix="/products", tags=["products"])
service = CrudService(Product, "productID", "Product")
relationship_service = RelationshipService()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate) -> Product:
    return service.create(payload)


@router.get("", response_model=list[ProductResponse])
def list_products(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Product]:
    return service.list(skip, limit)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str) -> Product:
    return service.get(product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, payload: ProductUpdate) -> Product:
    return service.update(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str) -> Response:
    service.delete(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{product_id}/category", response_model=CategoryResponse)
def get_product_category(product_id: str) -> Category:
    return relationship_service.product_category(product_id)


@router.put("/{product_id}/category/{category_id}", response_model=CategoryResponse)
def assign_product_category(product_id: str, category_id: str) -> Category:
    return relationship_service.assign_product_category(product_id, category_id)


@router.delete("/{product_id}/category", status_code=status.HTTP_204_NO_CONTENT)
def remove_product_category(product_id: str) -> Response:
    relationship_service.remove_product_category(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{product_id}/suppliers", response_model=list[SupplierResponse])
def list_product_suppliers(
    product_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Supplier]:
    return relationship_service.product_suppliers(product_id, skip, limit)


@router.get("/{product_id}/orders", response_model=list[ProductOrderLineResponse])
def list_product_orders(
    product_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[dict]:
    return relationship_service.product_orders(product_id, skip, limit)

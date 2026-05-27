from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.models import Product, Supplier
from app.schemas import ProductResponse, SupplierCreate, SupplierResponse, SupplierUpdate
from app.services import CrudService, RelationshipService

router = APIRouter(prefix="/suppliers", tags=["suppliers"])
service = CrudService(Supplier, "supplierID", "Supplier")
relationship_service = RelationshipService()


@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(payload: SupplierCreate) -> Supplier:
    return service.create(payload)


@router.get("", response_model=list[SupplierResponse])
def list_suppliers(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Supplier]:
    return service.list(skip, limit)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: str) -> Supplier:
    return service.get(supplier_id)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: str, payload: SupplierUpdate) -> Supplier:
    return service.update(supplier_id, payload)


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: str) -> Response:
    service.delete(supplier_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{supplier_id}/products", response_model=list[ProductResponse])
def list_supplier_products(
    supplier_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Product]:
    return relationship_service.supplier_products(supplier_id, skip, limit)


@router.put("/{supplier_id}/products/{product_id}", response_model=ProductResponse)
def link_supplier_product(supplier_id: str, product_id: str) -> Product:
    return relationship_service.link_supplier_product(supplier_id, product_id)


@router.delete(
    "/{supplier_id}/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT
)
def unlink_supplier_product(supplier_id: str, product_id: str) -> Response:
    relationship_service.unlink_supplier_product(supplier_id, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

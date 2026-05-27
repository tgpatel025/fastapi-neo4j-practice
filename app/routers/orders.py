from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.models import Customer, Order
from app.schemas import (
    CustomerResponse,
    OrderCreate,
    OrderLinePut,
    OrderProductLineResponse,
    OrderResponse,
    OrderUpdate,
)
from app.services import CrudService, RelationshipService

router = APIRouter(prefix="/orders", tags=["orders"])
service = CrudService(Order, "orderID", "Order")
relationship_service = RelationshipService()


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate) -> Order:
    return service.create(payload)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Order]:
    return service.list(skip, limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str) -> Order:
    return service.get(order_id)


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(order_id: str, payload: OrderUpdate) -> Order:
    return service.update(order_id, payload)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: str) -> Response:
    service.delete(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{order_id}/customer", response_model=CustomerResponse)
def get_order_customer(order_id: str) -> Customer:
    return relationship_service.order_customer(order_id)


@router.put("/{order_id}/customer/{customer_id}", response_model=CustomerResponse)
def assign_order_customer(order_id: str, customer_id: str) -> Customer:
    return relationship_service.assign_order_customer(order_id, customer_id)


@router.delete("/{order_id}/customer", status_code=status.HTTP_204_NO_CONTENT)
def remove_order_customer(order_id: str) -> Response:
    relationship_service.remove_order_customer(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{order_id}/products", response_model=list[OrderProductLineResponse])
def list_order_products(
    order_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[dict]:
    return relationship_service.order_products(order_id, skip, limit)


@router.put("/{order_id}/products/{product_id}", response_model=OrderProductLineResponse)
def put_order_product(
    order_id: str, product_id: str, payload: OrderLinePut
) -> dict:
    return relationship_service.put_order_product(order_id, product_id, payload)


@router.delete(
    "/{order_id}/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT
)
def unlink_order_product(order_id: str, product_id: str) -> Response:
    relationship_service.unlink_order_product(order_id, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

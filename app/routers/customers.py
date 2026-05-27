from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.models import Customer, Order
from app.schemas import CustomerCreate, CustomerResponse, CustomerUpdate, OrderResponse
from app.services import CrudService, RelationshipService

router = APIRouter(prefix="/customers", tags=["customers"])
service = CrudService(Customer, "customerID", "Customer")
relationship_service = RelationshipService()


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate) -> Customer:
    return service.create(payload)


@router.get("", response_model=list[CustomerResponse])
def list_customers(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Customer]:
    return service.list(skip, limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str) -> Customer:
    return service.get(customer_id)


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, payload: CustomerUpdate) -> Customer:
    return service.update(customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: str) -> Response:
    service.delete(customer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{customer_id}/orders", response_model=list[OrderResponse])
def list_customer_orders(
    customer_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Order]:
    return relationship_service.customer_orders(customer_id, skip, limit)

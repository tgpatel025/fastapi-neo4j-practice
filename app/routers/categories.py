from typing import Annotated

from fastapi import APIRouter, Query, Response, status

from app.models import Category, Product
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate, ProductResponse
from app.services import CrudService, RelationshipService

router = APIRouter(prefix="/categories", tags=["categories"])
service = CrudService(Category, "categoryID", "Category")
relationship_service = RelationshipService()


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate) -> Category:
    return service.create(payload)


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Category]:
    return service.list(skip, limit)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str) -> Category:
    return service.get(category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, payload: CategoryUpdate) -> Category:
    return service.update(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str) -> Response:
    service.delete(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{category_id}/products", response_model=list[ProductResponse])
def list_category_products(
    category_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[Product]:
    return relationship_service.category_products(category_id, skip, limit)

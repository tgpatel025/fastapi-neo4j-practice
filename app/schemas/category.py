from app.schemas.base import RequestSchema, ResponseSchema


class CategoryFields:
    description: str | None = None
    categoryName: str | None = None
    picture: str | None = None


class CategoryCreate(RequestSchema, CategoryFields):
    categoryID: str


class CategoryUpdate(RequestSchema, CategoryFields):
    pass


class CategoryResponse(ResponseSchema, CategoryFields):
    categoryID: str

from app.schemas.base import RequestSchema, ResponseSchema


class ProductFields:
    unitPrice: float | None = None
    unitsInStock: int | None = None
    reorderLevel: int | None = None
    supplierID: str | None = None
    discontinued: bool | None = None
    quantityPerUnit: str | None = None
    productName: str | None = None
    categoryID: str | None = None
    unitsOnOrder: int | None = None


class ProductCreate(RequestSchema, ProductFields):
    productID: str


class ProductUpdate(RequestSchema, ProductFields):
    pass


class ProductResponse(ResponseSchema, ProductFields):
    productID: str

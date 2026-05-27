from app.schemas.base import RequestSchema, ResponseSchema


class OrderFields:
    shipCity: str | None = None
    freight: str | None = None
    requiredDate: str | None = None
    employeeID: str | None = None
    shipName: str | None = None
    shipPostalCode: str | None = None
    shipCountry: str | None = None
    shipAddress: str | None = None
    shipVia: str | None = None
    customerID: str | None = None
    shipRegion: str | None = None
    orderDate: str | None = None
    shippedDate: str | None = None


class OrderCreate(RequestSchema, OrderFields):
    orderID: str


class OrderUpdate(RequestSchema, OrderFields):
    pass


class OrderResponse(ResponseSchema, OrderFields):
    orderID: str

from app.schemas.base import RequestSchema, ResponseSchema
from app.schemas.order import OrderResponse
from app.schemas.product import ProductResponse


class OrderLinePut(RequestSchema):
    unitPrice: str
    quantity: int
    discount: str


class OrderLineProperties(ResponseSchema):
    unitPrice: str
    quantity: int
    discount: str
    orderID: str
    productID: str


class OrderProductLineResponse(ResponseSchema):
    product: ProductResponse
    relationship: OrderLineProperties


class ProductOrderLineResponse(ResponseSchema):
    order: OrderResponse
    relationship: OrderLineProperties

from neomodel import (
    IntegerProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    ZeroOrMore,
    ZeroOrOne,
)


class OrdersRel(StructuredRel):
    unitPrice = StringProperty()
    discount = StringProperty()
    quantity = IntegerProperty()
    productID = StringProperty()
    orderID = StringProperty()


class Order(StructuredNode):
    shipCity = StringProperty()
    orderID = StringProperty(required=True, unique_index=True)
    freight = StringProperty()
    requiredDate = StringProperty()
    employeeID = StringProperty()
    shipName = StringProperty()
    shipPostalCode = StringProperty()
    shipCountry = StringProperty()
    shipAddress = StringProperty()
    shipVia = StringProperty()
    customerID = StringProperty()
    shipRegion = StringProperty()
    orderDate = StringProperty()
    shippedDate = StringProperty()
    customer = RelationshipFrom(
        "app.models.customer.Customer", "PURCHASED", cardinality=ZeroOrOne
    )
    orders = RelationshipTo(
        "app.models.product.Product",
        "ORDERS",
        cardinality=ZeroOrMore,
        model=OrdersRel,
    )

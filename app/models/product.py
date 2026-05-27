from neomodel import (
    BooleanProperty,
    FloatProperty,
    IntegerProperty,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    ZeroOrMore,
    ZeroOrOne,
)


class Product(StructuredNode):
    unitPrice = FloatProperty()
    unitsInStock = IntegerProperty()
    reorderLevel = IntegerProperty()
    supplierID = StringProperty()
    productID = StringProperty(required=True, unique_index=True)
    discontinued = BooleanProperty()
    quantityPerUnit = StringProperty()
    productName = StringProperty()
    categoryID = StringProperty()
    unitsOnOrder = IntegerProperty()
    part_of = RelationshipTo(
        "app.models.category.Category", "PART_OF", cardinality=ZeroOrOne
    )
    suppliers = RelationshipFrom(
        "app.models.supplier.Supplier", "SUPPLIES", cardinality=ZeroOrMore
    )
    orders = RelationshipFrom(
        "app.models.order.Order", "ORDERS", cardinality=ZeroOrMore
    )

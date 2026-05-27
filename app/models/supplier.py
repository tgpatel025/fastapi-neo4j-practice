from neomodel import RelationshipTo, StringProperty, StructuredNode, ZeroOrMore


class Supplier(StructuredNode):
    country = StringProperty()
    contactTitle = StringProperty()
    address = StringProperty()
    supplierID = StringProperty(required=True, unique_index=True)
    city = StringProperty()
    phone = StringProperty()
    contactName = StringProperty()
    companyName = StringProperty()
    postalCode = StringProperty()
    region = StringProperty()
    fax = StringProperty()
    homePage = StringProperty()
    supplies = RelationshipTo(
        "app.models.product.Product", "SUPPLIES", cardinality=ZeroOrMore
    )

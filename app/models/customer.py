from neomodel import RelationshipTo, StringProperty, StructuredNode, ZeroOrMore


class Customer(StructuredNode):
    country = StringProperty()
    contactTitle = StringProperty()
    address = StringProperty()
    city = StringProperty()
    phone = StringProperty()
    contactName = StringProperty()
    companyName = StringProperty()
    postalCode = StringProperty()
    customerID = StringProperty(required=True, unique_index=True)
    fax = StringProperty()
    region = StringProperty()
    purchased = RelationshipTo(
        "app.models.order.Order", "PURCHASED", cardinality=ZeroOrMore
    )

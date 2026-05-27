from neomodel import RelationshipFrom, StringProperty, StructuredNode, ZeroOrMore


class Category(StructuredNode):
    description = StringProperty()
    categoryName = StringProperty()
    categoryID = StringProperty(required=True, unique_index=True)
    picture = StringProperty()
    products = RelationshipFrom(
        "app.models.product.Product", "PART_OF", cardinality=ZeroOrMore
    )

from typing import Any

from neomodel import StructuredNode
from neomodel.exceptions import AttemptedCardinalityViolation, CardinalityViolation

from app.database import read_transaction, write_transaction
from app.models import Category, Customer, Order, Product, Supplier
from app.schemas import OrderLinePut
from app.services.exceptions import RelationshipConflict, ResourceNotFound


class RelationshipService:
    def product_category(self, product_id: str) -> Category:
        with read_transaction():
            product = self._get(Product, "productID", product_id, "Product")
            return self._related_or_404(product.part_of.single(), "Product category")

    def assign_product_category(
        self, product_id: str, category_id: str
    ) -> Category:
        try:
            with write_transaction():
                product = self._get(Product, "productID", product_id, "Product")
                category = self._get(Category, "categoryID", category_id, "Category")
                existing = product.part_of.single()
                if existing is None:
                    product.part_of.connect(category)
                elif existing != category:
                    product.part_of.replace(category)
                product.categoryID = category_id
                product.save()
                return category
        except (AttemptedCardinalityViolation, CardinalityViolation) as exc:
            raise RelationshipConflict("Unable to assign product category") from exc

    def remove_product_category(self, product_id: str) -> None:
        with write_transaction():
            product = self._get(Product, "productID", product_id, "Product")
            category = product.part_of.single()
            self._related_or_404(category, "Product category")
            product.part_of.disconnect(category)
            product.categoryID = None
            product.save()

    def category_products(
        self, category_id: str, skip: int, limit: int
    ) -> list[Product]:
        with read_transaction():
            category = self._get(Category, "categoryID", category_id, "Category")
            return self._page(category.products, skip, limit)

    def order_customer(self, order_id: str) -> Customer:
        with read_transaction():
            order = self._get(Order, "orderID", order_id, "Order")
            return self._related_or_404(order.customer.single(), "Order customer")

    def assign_order_customer(self, order_id: str, customer_id: str) -> Customer:
        try:
            with write_transaction():
                order = self._get(Order, "orderID", order_id, "Order")
                customer = self._get(
                    Customer, "customerID", customer_id, "Customer"
                )
                existing = order.customer.single()
                if existing is None:
                    customer.purchased.connect(order)
                elif existing != customer:
                    order.customer.replace(customer)
                order.customerID = customer_id
                order.save()
                return customer
        except (AttemptedCardinalityViolation, CardinalityViolation) as exc:
            raise RelationshipConflict("Unable to assign order customer") from exc

    def remove_order_customer(self, order_id: str) -> None:
        with write_transaction():
            order = self._get(Order, "orderID", order_id, "Order")
            customer = order.customer.single()
            self._related_or_404(customer, "Order customer")
            order.customer.disconnect(customer)
            order.customerID = None
            order.save()

    def customer_orders(self, customer_id: str, skip: int, limit: int) -> list[Order]:
        with read_transaction():
            customer = self._get(Customer, "customerID", customer_id, "Customer")
            return self._page(customer.purchased, skip, limit)

    def supplier_products(
        self, supplier_id: str, skip: int, limit: int
    ) -> list[Product]:
        with read_transaction():
            supplier = self._get(Supplier, "supplierID", supplier_id, "Supplier")
            return self._page(supplier.supplies, skip, limit)

    def product_suppliers(
        self, product_id: str, skip: int, limit: int
    ) -> list[Supplier]:
        with read_transaction():
            product = self._get(Product, "productID", product_id, "Product")
            return self._page(product.suppliers, skip, limit)

    def link_supplier_product(self, supplier_id: str, product_id: str) -> Product:
        with write_transaction():
            supplier = self._get(Supplier, "supplierID", supplier_id, "Supplier")
            product = self._get(Product, "productID", product_id, "Product")
            supplier.supplies.connect(product)
            return product

    def unlink_supplier_product(self, supplier_id: str, product_id: str) -> None:
        with write_transaction():
            supplier = self._get(Supplier, "supplierID", supplier_id, "Supplier")
            product = self._get(Product, "productID", product_id, "Product")
            if not supplier.supplies.is_connected(product):
                raise ResourceNotFound("Supplier product relationship was not found")
            supplier.supplies.disconnect(product)

    def order_products(
        self, order_id: str, skip: int, limit: int
    ) -> list[dict[str, Any]]:
        with read_transaction():
            order = self._get(Order, "orderID", order_id, "Order")
            products = self._page(order.orders, skip, limit)
            return [self._order_product_line(order, product) for product in products]

    def product_orders(
        self, product_id: str, skip: int, limit: int
    ) -> list[dict[str, Any]]:
        with read_transaction():
            product = self._get(Product, "productID", product_id, "Product")
            orders = self._page(product.orders, skip, limit)
            return [self._product_order_line(order, product) for order in orders]

    def put_order_product(
        self, order_id: str, product_id: str, payload: OrderLinePut
    ) -> dict[str, Any]:
        with write_transaction():
            order = self._get(Order, "orderID", order_id, "Order")
            product = self._get(Product, "productID", product_id, "Product")
            properties = payload.model_dump() | {
                "orderID": order_id,
                "productID": product_id,
            }
            relationship = order.orders.relationship(product)
            if relationship is None:
                order.orders.connect(product, properties)
            else:
                for field, value in properties.items():
                    setattr(relationship, field, value)
                relationship.save()
            return self._order_product_line(order, product)

    def unlink_order_product(self, order_id: str, product_id: str) -> None:
        with write_transaction():
            order = self._get(Order, "orderID", order_id, "Order")
            product = self._get(Product, "productID", product_id, "Product")
            if order.orders.relationship(product) is None:
                raise ResourceNotFound("Order product relationship was not found")
            order.orders.disconnect(product)

    def _order_product_line(
        self, order: Order, product: Product
    ) -> dict[str, Any]:
        relationship = order.orders.relationship(product)
        return {"product": product, "relationship": relationship}

    def _product_order_line(
        self, order: Order, product: Product
    ) -> dict[str, Any]:
        relationship = order.orders.relationship(product)
        return {"order": order, "relationship": relationship}

    @staticmethod
    def _page(manager: Any, skip: int, limit: int) -> list[Any]:
        return list(manager[skip : skip + limit])

    @staticmethod
    def _related_or_404(node: Any, name: str) -> Any:
        if node is None:
            raise ResourceNotFound(f"{name} relationship was not found")
        return node

    @staticmethod
    def _get(
        model: type[StructuredNode], id_field: str, resource_id: str, name: str
    ) -> StructuredNode:
        node = model.nodes.get_or_none(**{id_field: resource_id})
        if node is None:
            raise ResourceNotFound(
                f"{name} with {id_field} '{resource_id}' was not found"
            )
        return node

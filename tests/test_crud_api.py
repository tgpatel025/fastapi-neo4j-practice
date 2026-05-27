import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.database import write_transaction
from app.main import app
from app.models import Category, Customer, Order, Product, Supplier


class CrudApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client_context.__exit__(None, None, None)

    def temporary_id(self, resource: str) -> str:
        return f"TEST_{resource.upper()}_{uuid4().hex}"

    def delete_if_present(self, resource: str, resource_id: str) -> None:
        response = self.client.delete(f"/{resource}/{resource_id}")
        self.assertIn(response.status_code, (204, 404))

    def detach_delete(self, *nodes: tuple[type, str, str]) -> None:
        with write_transaction():
            for model, id_field, resource_id in nodes:
                node = model.nodes.get_or_none(**{id_field: resource_id})
                if node is not None:
                    node.delete()

    def test_crud_contract_for_each_resource(self) -> None:
        resources = {
            "products": ("productID", "productName"),
            "categories": ("categoryID", "categoryName"),
            "suppliers": ("supplierID", "companyName"),
            "customers": ("customerID", "companyName"),
            "orders": ("orderID", "shipName"),
        }

        for resource, (id_field, editable_field) in resources.items():
            with self.subTest(resource=resource):
                resource_id = self.temporary_id(resource)
                payload = {id_field: resource_id, editable_field: "Created"}
                self.addCleanup(self.delete_if_present, resource, resource_id)

                created = self.client.post(f"/{resource}", json=payload)
                self.assertEqual(created.status_code, 201, created.text)

                fetched = self.client.get(f"/{resource}/{resource_id}")
                self.assertEqual(fetched.status_code, 200, fetched.text)

                patched = self.client.patch(
                    f"/{resource}/{resource_id}", json={editable_field: "Updated"}
                )
                self.assertEqual(patched.status_code, 200, patched.text)
                self.assertEqual(patched.json()[editable_field], "Updated")

                immutable_id = self.client.patch(
                    f"/{resource}/{resource_id}", json={id_field: "changed"}
                )
                self.assertEqual(immutable_id.status_code, 422, immutable_id.text)

                duplicate = self.client.post(f"/{resource}", json=payload)
                self.assertEqual(duplicate.status_code, 409, duplicate.text)

                removed = self.client.delete(f"/{resource}/{resource_id}")
                self.assertEqual(removed.status_code, 204, removed.text)

                missing = self.client.get(f"/{resource}/{resource_id}")
                self.assertEqual(missing.status_code, 404, missing.text)

    def test_list_pagination_validation(self) -> None:
        product_id = self.temporary_id("products")
        self.addCleanup(self.delete_if_present, "products", product_id)
        created = self.client.post(
            "/products", json={"productID": product_id, "productName": "Page Item"}
        )
        self.assertEqual(created.status_code, 201, created.text)

        response = self.client.get("/products", params={"skip": 0, "limit": 1})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(
            self.client.get("/products", params={"limit": 101}).status_code, 422
        )

    def test_linked_nodes_cannot_be_deleted(self) -> None:
        product_id = self.temporary_id("products")
        category_id = self.temporary_id("categories")
        self.client.post("/products", json={"productID": product_id})
        self.client.post("/categories", json={"categoryID": category_id})

        try:
            with write_transaction():
                product = Product.nodes.get(productID=product_id)
                category = Category.nodes.get(categoryID=category_id)
                product.part_of.connect(category)

            self.assertEqual(self.client.delete(f"/products/{product_id}").status_code, 409)
            self.assertEqual(
                self.client.delete(f"/categories/{category_id}").status_code, 409
            )
        finally:
            with write_transaction():
                product = Product.nodes.get_or_none(productID=product_id)
                category = Category.nodes.get_or_none(categoryID=category_id)
                if product is not None:
                    product.delete()
                if category is not None:
                    category.delete()

    def test_relationship_routes_are_documented(self) -> None:
        paths = self.client.get("/openapi.json").json()["paths"]
        expected = {
            "/products/{product_id}/category",
            "/products/{product_id}/category/{category_id}",
            "/categories/{category_id}/products",
            "/orders/{order_id}/customer",
            "/orders/{order_id}/customer/{customer_id}",
            "/customers/{customer_id}/orders",
            "/suppliers/{supplier_id}/products",
            "/suppliers/{supplier_id}/products/{product_id}",
            "/products/{product_id}/suppliers",
            "/orders/{order_id}/products",
            "/orders/{order_id}/products/{product_id}",
            "/products/{product_id}/orders",
        }
        self.assertTrue(expected.issubset(paths.keys()))

    def test_product_category_assignment_replacement_and_traversal(self) -> None:
        product_id = self.temporary_id("products")
        category_one = self.temporary_id("categories")
        category_two = self.temporary_id("categories")
        self.client.post("/products", json={"productID": product_id})
        self.client.post("/categories", json={"categoryID": category_one})
        self.client.post("/categories", json={"categoryID": category_two})

        try:
            assigned = self.client.put(f"/products/{product_id}/category/{category_one}")
            self.assertEqual(assigned.status_code, 200, assigned.text)
            self.assertEqual(assigned.json()["categoryID"], category_one)
            self.assertEqual(
                self.client.get(f"/products/{product_id}/category").json()["categoryID"],
                category_one,
            )
            reverse = self.client.get(f"/categories/{category_one}/products")
            self.assertEqual(reverse.status_code, 200, reverse.text)
            self.assertEqual(reverse.json()[0]["productID"], product_id)

            replaced = self.client.put(f"/products/{product_id}/category/{category_two}")
            self.assertEqual(replaced.status_code, 200, replaced.text)
            self.assertEqual(
                self.client.get(f"/products/{product_id}").json()["categoryID"],
                category_two,
            )
            self.assertEqual(
                self.client.get(f"/categories/{category_one}/products").json(), []
            )

            self.assertEqual(
                self.client.delete(f"/products/{product_id}/category").status_code, 204
            )
            self.assertEqual(
                self.client.get(f"/products/{product_id}/category").status_code, 404
            )
            self.assertIsNone(
                self.client.get(f"/products/{product_id}").json()["categoryID"]
            )
        finally:
            self.detach_delete(
                (Product, "productID", product_id),
                (Category, "categoryID", category_one),
                (Category, "categoryID", category_two),
            )

    def test_order_customer_assignment_replacement_and_traversal(self) -> None:
        order_id = self.temporary_id("orders")
        customer_one = self.temporary_id("customers")
        customer_two = self.temporary_id("customers")
        self.client.post("/orders", json={"orderID": order_id})
        self.client.post("/customers", json={"customerID": customer_one})
        self.client.post("/customers", json={"customerID": customer_two})

        try:
            assigned = self.client.put(f"/orders/{order_id}/customer/{customer_one}")
            self.assertEqual(assigned.status_code, 200, assigned.text)
            self.assertEqual(
                self.client.get(f"/orders/{order_id}/customer").json()["customerID"],
                customer_one,
            )
            self.assertEqual(
                self.client.get(f"/customers/{customer_one}/orders").json()[0]["orderID"],
                order_id,
            )

            replaced = self.client.put(f"/orders/{order_id}/customer/{customer_two}")
            self.assertEqual(replaced.status_code, 200, replaced.text)
            self.assertEqual(
                self.client.get(f"/orders/{order_id}").json()["customerID"],
                customer_two,
            )
            self.assertEqual(
                self.client.get(f"/customers/{customer_one}/orders").json(), []
            )

            self.assertEqual(
                self.client.delete(f"/orders/{order_id}/customer").status_code, 204
            )
            self.assertIsNone(
                self.client.get(f"/orders/{order_id}").json()["customerID"]
            )
        finally:
            self.detach_delete(
                (Order, "orderID", order_id),
                (Customer, "customerID", customer_one),
                (Customer, "customerID", customer_two),
            )

    def test_supplier_product_link_crud_and_reverse_traversal(self) -> None:
        supplier_id = self.temporary_id("suppliers")
        product_id = self.temporary_id("products")
        self.client.post("/suppliers", json={"supplierID": supplier_id})
        self.client.post(
            "/products", json={"productID": product_id, "supplierID": "imported-value"}
        )

        try:
            path = f"/suppliers/{supplier_id}/products/{product_id}"
            self.assertEqual(self.client.put(path).status_code, 200)
            self.assertEqual(self.client.put(path).status_code, 200)
            self.assertEqual(
                self.client.get(f"/suppliers/{supplier_id}/products").json()[0][
                    "productID"
                ],
                product_id,
            )
            self.assertEqual(
                self.client.get(f"/products/{product_id}/suppliers").json()[0][
                    "supplierID"
                ],
                supplier_id,
            )
            self.assertEqual(
                self.client.get(f"/products/{product_id}").json()["supplierID"],
                "imported-value",
            )
            self.assertEqual(self.client.delete(path).status_code, 204)
            self.assertEqual(self.client.delete(path).status_code, 404)
        finally:
            self.detach_delete(
                (Supplier, "supplierID", supplier_id),
                (Product, "productID", product_id),
            )

    def test_order_line_upsert_reverse_traversal_and_delete_protection(self) -> None:
        order_id = self.temporary_id("orders")
        product_id = self.temporary_id("products")
        self.client.post("/orders", json={"orderID": order_id})
        self.client.post("/products", json={"productID": product_id})
        path = f"/orders/{order_id}/products/{product_id}"

        try:
            created = self.client.put(
                path, json={"unitPrice": "10.00", "quantity": 2, "discount": "0.00"}
            )
            self.assertEqual(created.status_code, 200, created.text)
            self.assertEqual(created.json()["relationship"]["orderID"], order_id)
            self.assertEqual(created.json()["relationship"]["productID"], product_id)
            self.assertEqual(self.client.delete(f"/orders/{order_id}").status_code, 409)

            updated = self.client.put(
                path, json={"unitPrice": "12.50", "quantity": 3, "discount": "0.10"}
            )
            self.assertEqual(updated.status_code, 200, updated.text)
            self.assertEqual(updated.json()["relationship"]["quantity"], 3)
            order_lines = self.client.get(f"/orders/{order_id}/products", params={"limit": 1})
            product_lines = self.client.get(
                f"/products/{product_id}/orders", params={"limit": 1}
            )
            self.assertEqual(order_lines.json()[0]["product"]["productID"], product_id)
            self.assertEqual(product_lines.json()[0]["order"]["orderID"], order_id)
            self.assertEqual(
                self.client.get(f"/orders/{order_id}/products", params={"limit": 101}).status_code,
                422,
            )

            self.assertEqual(self.client.delete(path).status_code, 204)
            self.assertEqual(self.client.delete(path).status_code, 404)
            self.assertEqual(self.client.delete(f"/orders/{order_id}").status_code, 204)
            self.assertEqual(self.client.delete(f"/products/{product_id}").status_code, 204)
        finally:
            self.detach_delete(
                (Order, "orderID", order_id), (Product, "productID", product_id)
            )

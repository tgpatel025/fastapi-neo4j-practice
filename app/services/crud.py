from typing import Any

from neomodel import StructuredNode, db
from neomodel.exceptions import UniqueProperty
from pydantic import BaseModel

from app.database import read_transaction, write_transaction
from app.services.exceptions import (
    ResourceAlreadyExists,
    ResourceLinked,
    ResourceNotFound,
)


class CrudService:
    def __init__(
        self, model: type[StructuredNode], id_field: str, resource_name: str
    ) -> None:
        self.model = model
        self.id_field = id_field
        self.resource_name = resource_name

    def list(self, skip: int, limit: int) -> list[StructuredNode]:
        with read_transaction():
            return list(self.model.nodes[skip : skip + limit])

    def get(self, resource_id: str) -> StructuredNode:
        with read_transaction():
            return self._get(resource_id)

    def create(self, payload: BaseModel) -> StructuredNode:
        try:
            with write_transaction():
                return self.model(**payload.model_dump()).save()
        except UniqueProperty as exc:
            raise ResourceAlreadyExists(
                f"{self.resource_name} with {self.id_field} '{getattr(payload, self.id_field)}' already exists"
            ) from exc

    def update(self, resource_id: str, payload: BaseModel) -> StructuredNode:
        with write_transaction():
            node = self._get(resource_id)
            for field, value in payload.model_dump(exclude_unset=True).items():
                setattr(node, field, value)
            return node.save()

    def delete(self, resource_id: str) -> None:
        with write_transaction():
            node = self._get(resource_id)
            result, _ = node.cypher(
                f"MATCH (self) WHERE {db.get_id_method()}(self)=$self "
                "OPTIONAL MATCH (self)-[r]-() RETURN count(r)"
            )
            if result and result[0][0]:
                raise ResourceLinked(
                    f"{self.resource_name} '{resource_id}' cannot be deleted while it has relationships"
                )
            node.delete()

    def _get(self, resource_id: str) -> StructuredNode:
        filters: dict[str, Any] = {self.id_field: resource_id}
        node = self.model.nodes.get_or_none(**filters)
        if node is None:
            raise ResourceNotFound(
                f"{self.resource_name} with {self.id_field} '{resource_id}' was not found"
            )
        return node

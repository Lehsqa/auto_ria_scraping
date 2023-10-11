from typing import Any, Generic, Type

from infrastructure.database.table import ConcreteTable
from infrastructure.database.session import Session
from infrastructure.errors import UnprocessableError


class BaseRepository(Session, Generic[ConcreteTable]):

    schema_class: Type[ConcreteTable]

    def __init__(self) -> None:
        super().__init__()

        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Can not initiate the class without schema_class attribute"
                )
            )

    async def _save(self, payload: dict[str, Any]) -> ConcreteTable:
        schema = self.schema_class(**payload)
        await self.save(schema)
        return schema

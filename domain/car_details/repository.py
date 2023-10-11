from typing import Any

from infrastructure.database import BaseRepository, CarDetailsTable

from .models import CarDetailsUncommited, CarDetails


class CarDetailsRepository(BaseRepository[CarDetailsTable]):
    schema_class = CarDetailsTable

    async def create(self, schema: CarDetailsUncommited):
        instance: CarDetailsTable = await self._save(schema.model_dump())
        print(f'{schema.title} was saved')
        return CarDetails.model_validate(instance)

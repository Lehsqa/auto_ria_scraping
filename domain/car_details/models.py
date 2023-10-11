from datetime import datetime

from infrastructure.models import InternalModel, PublicModel


# Public models
# ------------------------------------------------------
class _CarDetailsPublic(PublicModel):
    url: str
    title: str
    price_usd: str
    odometer: int
    username: str
    phone_number: str
    image_url: str
    images_count: int
    car_number: str
    car_vin: str
    datetime_found: datetime


class CarDetailsPublic(_CarDetailsPublic):
    id: int


# Internal models
# ------------------------------------------------------
class CarDetailsUncommited(InternalModel):
    url: str
    title: str
    price_usd: str
    odometer: int
    username: str
    phone_number: str
    image_url: str
    images_count: int
    car_number: str
    car_vin: str
    datetime_found: datetime


class CarDetails(CarDetailsUncommited):
    id: int

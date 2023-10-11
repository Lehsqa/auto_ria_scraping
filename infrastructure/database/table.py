from typing import TypeVar

from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import declarative_base, relationship

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class CarDetailsTable(Base):
    __tablename__ = "car_details"

    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price_usd = Column(String, nullable=False)
    odometer = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    images_count = Column(Integer, nullable=False)
    car_number = Column(String)
    car_vin = Column(String)
    datetime_found = Column(DateTime, nullable=False)

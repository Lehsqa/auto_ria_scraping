import json
from typing import TypeVar

from pydantic import BaseModel


def to_camelcase(string: str) -> str:
    resp = "".join(
        word.capitalize() if index else word
        for index, word in enumerate(string.split("_"))
    )
    return resp


_json_encoders = {
    # np.float32: lambda v: float(v) if v else None,
}


class FrozenModel(BaseModel):
    class Config:
        json_encoders = _json_encoders
        from_attributes = True
        use_enum_values = True
        populate_by_name = True
        arbitrary_types_allowed = True


class InternalModel(BaseModel):
    class Config:
        json_encoders = _json_encoders
        extra = 'forbid'
        from_attributes = True
        use_enum_values = True
        populate_by_name = True
        validate_assignment = True
        arbitrary_types_allowed = True


_InternalModel = TypeVar("_InternalModel", bound=InternalModel)


class PublicModel(BaseModel):
    class Config:
        json_encoders = _json_encoders
        extra = 'ignore'
        from_attributes = True
        use_enum_values = True
        validate_assignment = True
        alias_generator = to_camelcase
        populate_by_name = True
        arbitrary_types_allowed = True

    def encoded_dict(self, by_alias=True):
        return json.loads(self.model_dump_json(by_alias=by_alias))


_PublicModel = TypeVar("_PublicModel", bound=PublicModel)

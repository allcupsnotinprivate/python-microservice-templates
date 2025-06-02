from typing import TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class BaseAPISchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

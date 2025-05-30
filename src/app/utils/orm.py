import re
from typing import Literal

from sqlalchemy import VARCHAR, Dialect, TypeDecorator

from app.utils.regex import ip_v4_pattern, ip_v6_pattern

IPType = Literal["v4", "v6"]


class IPAddress(TypeDecorator[str | None]):
    impl = VARCHAR(39)

    def __init__(self, type_: Literal["v4", "v6"]):
        if type_ == "v4":
            pattern = ip_v4_pattern
        elif type_ == "v6":
            pattern = ip_v6_pattern
        else:
            raise TypeError(
                f"Invalid IP type '{type_}' passed to {self.__class__.__name__}. Expected one of: 'v4' or 'v6'."
            )

        self.ip_type = type_
        self.ip_pattern = re.compile(pattern)
        super().__init__()

    def process_bind_param(self, value: str | None, dialect: Dialect) -> str | None:
        if value is None:
            return value

        if not isinstance(value, str):
            raise TypeError(f"Expected a string for {self.ip_type} address, got {type(value).__name__}.")

        if not self.ip_pattern.fullmatch(value):
            raise ValueError(
                f"Invalid {self.ip_type} address: '{value}'. "
                f"Expected format matching pattern: {self.ip_pattern.pattern}"
            )

        return value

    def process_result_value(self, value: str | None, dialect: Dialect) -> str | None:
        return value

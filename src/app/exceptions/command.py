from typing import Any, Mapping, Optional


class ErrorCommand:
    def __init__(self, name: str, data: Optional[Mapping[str, Any]] = None):
        self.name = name  # ex. "retry", "alert", "ignore"
        self.data = data or {}

    def __repr__(self) -> str:
        return f"ErrorCommand(name={self.name!r}, data={self.data!r})"

    def __str__(self) -> str:
        if self.data:
            return f"{self.name}({self.data})"
        return self.name

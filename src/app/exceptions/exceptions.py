from .command import ErrorCommand


class ServiceError(RuntimeError):
    """Basic error for the application service layer."""

    def __init__(self, message: str = "", code: int | str | None = None, command: ErrorCommand | None = None):
        super().__init__(message)
        self.code = code
        self.command = command

    def __str__(self) -> str:
        base = super().__str__()
        details = []
        if self.code is not None:
            details.append(f"code={self.code}")
        if self.command is not None:
            details.append(f"command={self.command}")
        if details:
            return f"{base} ({', '.join(details)})"
        return base


class DataError(ServiceError):
    """Error related to data access or integrity."""

    ...


class NotFoundError(DataError):
    """Error when the entity is not found."""

    ...


class DuplicateError(DataError):
    """Error when the entity already exists and cannot be added again."""

    ...


class ValidationError(DataError):
    """Data validation error."""

    ...


class BusinessLogicError(ServiceError):
    """Business logic error."""

    ...


class PermissionDeniedError(BusinessLogicError):
    """Insufficient access rights error."""

    ...


class OperationNotAllowedError(BusinessLogicError):
    """Error when operation is not allowed in current state."""

    ...


class ExternalServiceError(ServiceError):
    """Error interacting with external service."""

    ...


class DatabaseError(ExternalServiceError):
    """Error interacting with database."""

    ...


class APIServiceError(ExternalServiceError):
    """Error calling external API."""

    ...


class TimeoutServiceError(ExternalServiceError):
    """Timeout error accessing external resource."""

    ...


class InfrastructureError(ServiceError):
    """Error related to infrastructure problems."""

    ...


class ConfigurationError(InfrastructureError):
    """Application configuration error."""

    ...


class DependencyUnavailableError(InfrastructureError):
    """Error when external dependency is unavailable."""

    ...

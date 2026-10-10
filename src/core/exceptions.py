class DomainError(Exception):
    """Базовый тип ошибки."""

class InvalidCredentialsError(DomainError):
    """Неверный email или пароль."""

class InvalidTokenError(DomainError):
    """Токен отсутствует, невалиден или истёк."""

class EmailAlreadyExistsError(DomainError):
    """Email уже занят."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} already exists")

class UsernameAlreadyExistsError(DomainError):
    """Username уже занят."""
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username {username} already exists")

class UserAlreadyDeletedError(DomainError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} already deleted")

class NotFoundError(DomainError):
    model_name: str | None = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "model_name" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must define class attribute 'model_name'"
            )

    def __init__(self, model_object_id: int):
        self.model_object_id = model_object_id
        super().__init__(f"{self.model_name} with id={model_object_id} not found")

class PermissionDeniedError(DomainError):
    """Нет прав на объект. HTTP 403."""

    def __init__(self, message: str = "Permission denied"):
        self.message = message
        super().__init__(message)

class DuplicateError(DomainError):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

class DateValidationError(DomainError):
    def __init__(self, detail: str):
        self.detail = detail


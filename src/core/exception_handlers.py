from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from core.exceptions import InvalidCredentialsError, InvalidTokenError, EmailAlreadyExistsError, NotFoundError, DuplicateError, DateValidationError
from core import exceptions

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(exceptions.InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: exceptions.InvalidCredentialsError):
        return JSONResponse(
            status_code=401,
            content={'detail': 'Неверный email или пароль'},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(exceptions.InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: exceptions.InvalidTokenError):
        return JSONResponse(
            status_code=401,
            content={'detail': 'Токен невалиден или истёк'},
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    @app.exception_handler(exceptions.EmailAlreadyExistsError)
    async def email_exists_handler(request: Request, exc: exceptions.EmailAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Email уже занят"},
        )
    
    @app.exception_handler(exceptions.UsernameAlreadyExistsError)
    async def email_exists_handler(request: Request, exc: exceptions.UsernameAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Username уже занят"},
        )

    @app.exception_handler(exceptions.NotFoundError)
    async def not_found_handler(request: Request, exc: exceptions.NotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "error": "not_found",
                "detail": f"{exc.model_name} with id={exc.model_object_id} not found",
            },
        )

    # Обработчик ошибки: Дублирование уникальных данных
    @app.exception_handler(exceptions.DuplicateError)
    async def duplicate_handler(request: Request, exc: exceptions.DuplicateError):
        return JSONResponse(
            status_code=409,
            content={
                "error": "duplicate",
                "detail": f"Значение '{exc.value}' для поля '{exc.field}' уже существует",
            },
        )

    # Обработчик ошибки: Некорректные даты
    @app.exception_handler(exceptions.DateValidationError)
    async def date_validation_handler(request: Request, exc: exceptions.DateValidationError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "date_validation",
                "detail": exc.detail,
            },
        )

    # Переопределение дефолтной ошибки валидации Pydantic (Убираем loc и делаем понятный JSON)
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            locs = [str(loc) for loc in error["loc"] if loc != "body"]
            field = " -> ".join(locs) if locs else "body"
            errors.append({"field": field, "message": error["msg"]})
            
        return JSONResponse(
            status_code=422,
            content={"error": "validation_error", "detail": errors},
        )
    
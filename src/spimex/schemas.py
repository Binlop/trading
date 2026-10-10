from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SpimexResRead(BaseModel):
    id: int
    exchange_product_id: str = Field(..., description="Код биржевого товара")
    exchange_product_name: str = Field(..., description="Наименование биржевого товара")
    delivery_basis_name: str = Field(..., description="Наименование базиса поставки")
    volume: int = Field(..., description="Объём")
    total: int = Field(..., description="Общая стоимость")
    count: int = Field(..., description="Количество сделок")
    oil_id: str = Field(..., max_length=4, description="Идентификатор нефтепродукта")
    delivery_basis_id: str = Field(..., max_length=3, description="Код базиса поставки")
    delivery_type_id: str = Field(..., max_length=1, description="Код типа поставки")
    date: datetime = Field(..., description="Дата торгов")

    model_config = ConfigDict(from_attributes=True)

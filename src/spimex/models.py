from datetime import datetime
from sqlalchemy import Integer, String, CheckConstraint, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from db.session import Base

class PetroleumProducts(Base):
    __tablename__ = "petroleum_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exchange_product_id: Mapped[str] = mapped_column(String(255), nullable=False)
    exchange_product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    delivery_basis_name: Mapped[str] = mapped_column(String(255), nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger)
    total: Mapped[int] = mapped_column(BigInteger)
    count: Mapped[int] = mapped_column(BigInteger, nullable=False)
    oil_id: Mapped[str] = mapped_column(String(4), nullable=False)
    delivery_basis_id: Mapped[str] = mapped_column(String(3), nullable=False)
    delivery_type_id: Mapped[str] = mapped_column(String(1), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime)

    __table_args__ = (
        CheckConstraint("count > 0", name="check_count_positive"),
    )
from datetime import date, datetime, time, timedelta
from sqlalchemy import select
from db.uow import UnitOfWork
from spimex.models import PetroleumProducts

class SpimexRepository:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_last_trading_dates(self, last_days: int):
        cutoff = datetime.combine(
            date.today() - timedelta(days=last_days),
            time.min,
        )
        stmt = (select(PetroleumProducts)
                .where(PetroleumProducts.date >= cutoff)
                .order_by(PetroleumProducts.date.desc())
                )
        res = await self.uow.db.scalars(stmt)
        return list(res.all())

    async def get_dynamics(
        self, 
        start_date: date, 
        end_date: date, 
        oil_id: str | None = None, 
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None
    ):
        stmt = (
            select(PetroleumProducts)
            .where(
                PetroleumProducts.date >= start_date,
                PetroleumProducts.date <= end_date + timedelta(days=1),
            )
            .order_by(PetroleumProducts.date.desc())
        )
        if oil_id:
            stmt = stmt.where(PetroleumProducts.oil_id == oil_id)
        if delivery_type_id:
            stmt = stmt.where(PetroleumProducts.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            stmt = stmt.where(PetroleumProducts.delivery_basis_id == delivery_basis_id)
        res = await self.uow.db.scalars(stmt)
        return list(res.all())

    async def get_trading_results(
        self,
        limit: int,
        oil_id: str | None = None, 
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
    ):
        stmt = (
            select(PetroleumProducts)
            .limit(limit).order_by(PetroleumProducts.date.desc())
        )
        if oil_id:
            stmt = stmt.where(PetroleumProducts.oil_id == oil_id)
        if delivery_type_id:
            stmt = stmt.where(PetroleumProducts.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            stmt = stmt.where(PetroleumProducts.delivery_basis_id == delivery_basis_id)
        res = await self.uow.db.scalars(stmt)
        return list(res.all())
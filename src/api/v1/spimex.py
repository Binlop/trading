import structlog
import json
from fastapi import APIRouter, Query
from datetime import datetime, time, timedelta, date
from redis_fastapi import CacheBackendDep
from spimex.schemas import SpimexResRead
from api.deps import SpimexRepo

router = APIRouter(prefix='/spimex', tags=['Spimex'])
log = structlog.get_logger(__name__)

def ttl_until_1411() -> int:
    now = datetime.now()
    target = datetime.combine(now.date(), time(14, 11))
    if now >= target:
        target += timedelta(days=1)
    return max(1, int((target - now).total_seconds()))

class SpimexView:

    @router.get("/dates", response_model=list[SpimexResRead])
    async def get_last_trading_dates(
        repo: SpimexRepo, 
        cashe: CacheBackendDep,
        last_days: int = Query(30, ge=1, le=366, description="Последние N торговых дней (default: 30)")
    ):
        key = f"spimex:dates:last_days:{last_days}"
        cashed = await cashe.get(key)
        if cashed:
            return cashed
        res = await repo.get_last_trading_dates(last_days=last_days)
        serialized = [SpimexResRead.model_validate(item).model_dump(mode="json") for item in res]
        await cashe.set(key, serialized, ttl=ttl_until_1411())
        return serialized

    @router.get("/dynamics", response_model=list[SpimexResRead])
    async def get_dynamics(
        start_date: date,
        end_date: date,
        repo: SpimexRepo,
        cashe: CacheBackendDep,
        oil_id: str | None = Query(None),
        delivery_type_id: str | None = Query(None),
        delivery_basis_id: str | None = Query(None),
    ):
        data = json.dumps(
            {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'oil_id': oil_id,
                'delivery_type_id': delivery_type_id,
                'delivery_basis_id': delivery_basis_id,
            },
            sort_keys=True,
        )
        key = f"spimex:dynamics:{hash(data)}"
        cashed = await cashe.get(key)
        if cashed:
            return cashed
        res = await repo.get_dynamics(start_date, end_date, oil_id, delivery_type_id, delivery_basis_id)
        serialized = [SpimexResRead.model_validate(item).model_dump(mode="json") for item in res]
        await cashe.set(key, serialized, ttl=ttl_until_1411())
        return serialized

    @router.get("/results", response_model=list[SpimexResRead])
    async def get_trading_results(
        repo: SpimexRepo,
        cashe: CacheBackendDep,
        oil_id: str | None = Query(None),
        delivery_type_id: str | None = Query(None),
        delivery_basis_id: str | None = Query(None),
        limit: int = Query(100, ge=1, le=1000, description="Сколько записей вернуть"),
    ):
        data = json.dumps(
            {
                'oil_id': oil_id,
                'delivery_type_id': delivery_type_id,
                'delivery_basis_id': delivery_basis_id,
                'limit': limit,
            },
            sort_keys=True,
        )
        key = f"spimex:dynamics:{hash(data)}"
        cashed = await cashe.get(key)
        if cashed:
            return cashed
        res = await repo.get_trading_results(limit, oil_id, delivery_type_id, delivery_basis_id)
        serialized = [SpimexResRead.model_validate(item).model_dump(mode="json") for item in res]
        await cashe.set(key, serialized, ttl=ttl_until_1411())
        return serialized
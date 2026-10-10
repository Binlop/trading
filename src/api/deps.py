from typing import Annotated
from fastapi import Depends
from db.uow import UnitOfWork, get_uow
from spimex.repository import SpimexRepository

def get_spimex_repository(uow: UnitOfWork = Depends(get_uow)):
    return SpimexRepo(uow)

SpimexRepo = Annotated[SpimexRepository, Depends(get_spimex_repository)]


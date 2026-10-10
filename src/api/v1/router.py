from fastapi import APIRouter
from api.v1.spimex import router as spimex_router

router = APIRouter(prefix="/api/v1")
router.include_router(spimex_router)
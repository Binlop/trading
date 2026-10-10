import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis_fastapi import redis_lifespan

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with redis_lifespan(app):
        logger.info("Trading API запущен.")
        yield
        logger.info("Trading API останавливается.")
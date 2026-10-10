from fastapi import FastAPI, WebSocket
from redis_fastapi import FastAPIRedis
from api.v1.router import router as v1_router
# from ws.routes import router as web_socket_router
# from middlewares.custom_header import CustomHeaderMiddleware
from middleware import ProcessTimeMiddleware, AccessLogMiddleware
# from middlewares.process_time import ProcessTimeMiddleware
from core.exception_handlers import register_exception_handlers
from core.config import settings
from core.logging import configure_logging
from core.lifespan import lifespan
from fastapi.staticfiles import StaticFiles

configure_logging()

app = FastAPI(
    title=settings.PROJECT_NAME, 
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)
FastAPIRedis(app).caching()

register_exception_handlers(app)
app.include_router(v1_router)
# app.include_router(web_socket_router)
app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(AccessLogMiddleware)
# app.add_middleware(CustomHeaderMiddleware, header_value='Production-Mode')
# app.mount("/static", StaticFiles(directory="static"), name="static")

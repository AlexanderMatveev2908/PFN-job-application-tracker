from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.middleware.json_logger import LoggerJSON
from src.routes.index import api
from .lib.logger import __cg


@asynccontextmanager
async def lifespan(app: FastAPI):
    __cg("🚀 server running on 3000...")
    yield
    __cg("💣 server shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggerJSON)

app.include_router(router=api)

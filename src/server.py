from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.routes.index import api
from .lib.logger import __cg


@asynccontextmanager
async def lifespan(app: FastAPI):
    __cg("🚀 server running on 3000...")
    yield
    __cg("💣 server shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(router=api)

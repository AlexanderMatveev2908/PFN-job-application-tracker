from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.lib.logger import log
from src.middleware.json_logger import LoggerJSON
from src.routes.index import api
from .middleware.query_parser import ParserQuery


@asynccontextmanager
async def lifespan(app: FastAPI):
    log(ttl="🚀 server running on 3000...")
    yield
    log(ttl="💣 server shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggerJSON)
app.add_middleware(ParserQuery)

app.include_router(router=api)

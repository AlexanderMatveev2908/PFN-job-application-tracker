import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.lib.logger import clg
from src.middleware.form_data_parser import FormDataParser
from src.middleware.json_logger import LoggerJSON
from src.middleware.wrap_api import WrapAPI
from src.routes.index import api
from .middleware.query_parser import ParserQuery
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    clg(ttl=f"🚀 server running on {os.getenv('PORT')}...")
    yield
    clg(ttl="💣 server shutting down")


app = FastAPI(lifespan=lifespan)


app.add_middleware(LoggerJSON)
app.add_middleware(ParserQuery)
app.add_middleware(FormDataParser)
app.add_middleware(WrapAPI)

app.include_router(router=api)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.conf.db import test_connect
from src.decorators.err import ErrAPI
from src.lib.logger import clg
from src.middleware.cors import CorsMDW
from src.middleware.form_data_parser import FormDataParser
from src.middleware.json_logger import LoggerJSON
from src.middleware.wrap_api import WrapAPI
from src.routes.index import api
from .middleware.query_parser import ParserQuery
from .conf.env import env_var
from fastapi.middleware.cors import CORSMiddleware
from .constants.api import whitelist

if env_var.secret != "👻":
    raise ErrAPI(msg="Missing .env var", status=500)


@asynccontextmanager
async def lifespan(app: FastAPI):
    clg(ttl=f"🚀 server running on {env_var.port}...")

    await test_connect()

    clg(ttl="🗃️ DB connection passed")

    yield
    clg(ttl="💣 server shutting down")


app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggerJSON)
app.add_middleware(ParserQuery)
app.add_middleware(FormDataParser)
app.add_middleware(WrapAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelist,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorsMDW, whitelist=whitelist)

app.include_router(router=api)

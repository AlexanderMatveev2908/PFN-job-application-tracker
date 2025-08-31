from typing import AsyncIterator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.decorators.err import ErrAPI
from src.lib.logger import cent
from src.middleware.security.cors import CorsMDW
from src.middleware.parsers.form_data_parser import FormDataParser
from src.middleware.dev_only.json_logger import LoggerJSON
from src.middleware.wrap_api import WrapAPI
from src.routes.idx import api
from .middleware.parsers.query_parser import ParserQuery
from src.conf.env import get_env
from fastapi.middleware.cors import CORSMiddleware
from .constants.api import EXPOSE_HEADERS, whitelist
from src.lib.ce import get_cost  # noqa: F401
from src.lib.db.idx import get_all  # noqa: F401
from src.lib.etc import wrap_loop  # noqa: F401
from src.lib.resdis.idx import get_all_redis  # noqa: F401
from src.lib.s3.get import gen_list_assets  # noqa: F401
from src.__dev_only.delete import clean_DBs  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    cent(f"🚀 server running on {get_env().port}...")

    # await get_all()
    # await get_all_redis()
    # await gen_list_assets()
    # await get_cost()

    # await clean_DBs(True)

    cent("⬜ whitelist ⬜", False)
    print(whitelist)

    if not whitelist:
        raise ErrAPI(msg="missing whitelist var ☢️", status=500)

    yield

    cent("💣 server shutting down")


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
    expose_headers=EXPOSE_HEADERS,
)
app.add_middleware(CorsMDW, whitelist=whitelist)

app.include_router(router=api)

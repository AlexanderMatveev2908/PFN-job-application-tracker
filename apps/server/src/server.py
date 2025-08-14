from typing import AsyncIterator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.conf.redis import get_all_redis
from src.decorators.err import ErrAPI
from src.__dev_only.db.delete import clean_tables  # noqa: F401
from src.lib.emails.aiosmtp.idx import send_email  # noqa: F401
from src.lib.etc import wrap_loop  # noqa: F401
from src.lib.logger import cent
from src.middleware.cors import CorsMDW
from src.middleware.form_data_parser import FormDataParser
from src.middleware.json_logger import LoggerJSON
from src.middleware.wrap_api import WrapAPI
from src.routes.idx import api
from .middleware.query_parser import ParserQuery
from src.conf.env import get_env
from fastapi.middleware.cors import CORSMiddleware
from .constants.api import whitelist


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    cent(f"🚀 server running on {get_env().port}...")

    # await get_all()
    # await gen_list_assets()
    # await get_cost()
    await get_all_redis()

    cent("⬜ whitelist ⬜", False)
    print(whitelist)

    if not whitelist:
        raise ErrAPI(msg="☢️ missing whitelist var", status=500)

    yield

    cent("💣 server shutting down")


# wrap_loop(send_email)
# wrap_loop(clean_tables)

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

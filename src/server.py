from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.lib.logger import log
from src.middleware.json_logger import LoggerJSON
from src.middleware.wrap_api import WrapAPI
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
app.add_middleware(WrapAPI)

app.include_router(router=api)


# @app.middleware("http")
# async def err_catcher(req: Request, next: Callable) -> Response | ResAPI:
#     try:
#         return await next(req)
#     except Exception as err:
#         log(
#             err,
#             ttl="last wall",
#         )
#         return ResAPI.err_500()

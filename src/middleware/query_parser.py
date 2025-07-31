import attr
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


@attr.s(auto_attribs=True)
class QueryParser(BaseHTTPMiddleware):
    app: ASGIApp

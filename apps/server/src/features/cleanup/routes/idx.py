from fastapi import APIRouter

from src.features.cleanup.controllers.delete import clean_cbc_hmac_ctrl


cleanup_router = APIRouter(prefix="/cleanup")

cleanup_router.add_api_route(
    "/cbc-hmac", clean_cbc_hmac_ctrl, methods=["DELETE"]
)

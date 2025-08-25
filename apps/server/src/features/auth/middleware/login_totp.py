from pydantic import BaseModel, Field

from src.constants.reg import REG_TOTP_CODE


class TotpFormT(BaseModel):
    totp_code: str = Field(min_length=1, pattern=REG_TOTP_CODE)

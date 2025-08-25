from pydantic import BaseModel, Field

from src.constants.reg import REG_BACKUP_CODE


class BackupCodeFormT(BaseModel):
    backup_code: str = Field(min_length=1, pattern=REG_BACKUP_CODE)

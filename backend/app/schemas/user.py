import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

USERNAME_PATTERN = re.compile(r"^[a-z0-9_]+$")


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username", mode="before")
    @classmethod
    def _normalize_username(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Username must be a string")
        v = v.strip().lower()
        if not USERNAME_PATTERN.match(v):
            raise ValueError(
                "Username must contain only lowercase letters, digits, and underscores"
            )
        return v

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str
    created_at: datetime

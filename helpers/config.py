from __future__ import annotations

from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

load_dotenv()

__all__ = ("Config",)

@dataclass
class Config:
    database_url: str
    bot_token: str
    owner_id: int

    @classmethod
    def from_env(cls):
        return cls(
            database_url=getenv("DATABASE_URL"),
            bot_token=getenv("BOT_TOKEN"),
            owner_id=int(getenv("OWNER_ID")),
        )
from os.path import join, dirname
from typing import AsyncGenerator

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram import Bot, Dispatcher
from fastapi import FastAPI


class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    
    WEBAPP_URL: str = ""
    
    WEBHOOK_URL: str = ""
    WEBHOOK_PATH: str = "/webhook"
    
    APP_HOST: str = "localhost"
    APP_PORT: int = 7700
    
    
    model_config = SettingsConfigDict(
        env_file=join(dirname(__file__), ".env"),
        env_file_encoding="utf-8"
    )


async def lifespan(app: FastAPI) -> AsyncGenerator:
    await bot.set_webhook(
        url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types()
    )
    
    yield
    await bot.session.close()


config = Config()

bot = Bot(config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
app = FastAPI(lifespan=lifespan)

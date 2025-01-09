from fastapi import Request
from fastapi.exceptions import HTTPException

from aiogram.utils.web_app import WebAppInitData, safe_parse_webapp_init_data

from config_reader import config


def auth(request: Request) -> WebAppInitData:
    try:
        auth_string = request.headers.get("authorization", None)
        if auth_string:
            data = safe_parse_webapp_init_data(
                config.BOT_TOKEN.get_secret_value(), auth_string
            )
            return data
        else:
            raise HTTPException(401, {"error": "Unauthorized"})
    except Exception:
        raise HTTPException(401, {"error": "Unauthorized"})
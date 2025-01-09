from aiogram import Router, F
from aiogram.types import Message, WebAppInfo, PreCheckoutQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config

router = Router()
markup = (
    InlineKeyboardBuilder()
    .button(text="Open Me", web_app=WebAppInfo(url=config.WEBAPP_URL))
).as_markup()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Hello!", reply_markup=markup)


@router.pre_checkout_query()
async def precheck(event: PreCheckoutQuery) -> None:
    await event.answer(True)
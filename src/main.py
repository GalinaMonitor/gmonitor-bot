import asyncio
from logging import getLogger

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from gmonitor_lib.schemas import TopicsEnum, GptRequest

from broker import broker
from settings import settings

logger = getLogger(__name__)

dp = Dispatcher()


@dp.message(CommandStart())  # type: ignore
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n"
        f"Попробуй задать мне вопрос."
    )


@dp.message()  # type: ignore
async def echo_handler(message: Message) -> None:
    try:
        await message.answer("Ваш запрос обрабатывается...")
        await broker.connect()
        await broker.publish(
            GptRequest(chat_id=message.chat.id, text=message.text),
            TopicsEnum.GPT_BOT_REQUEST,
        )
    except TypeError:
        await message.answer(
            "Твой запрос поломал бота)\nПопробуй переформулировать запрос."
        )


async def main() -> None:
    bot = Bot(
        token=settings.api_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

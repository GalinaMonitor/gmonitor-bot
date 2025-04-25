import asyncio
from logging import getLogger

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from pydantic import BaseModel

from broker import broker, TopicsEnum
from settings import settings

logger = getLogger(__name__)

dp = Dispatcher()


class GptRequest(BaseModel):
    chat_id: int
    text: str


@dp.message(CommandStart())  # type: ignore
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()  # type: ignore
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        await broker.connect()
        await broker.publish(
            GptRequest(chat_id=message.chat.id, text=message.text),
            TopicsEnum.GPT_BOT_REQUEST,
        )
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(
        token=settings.api_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

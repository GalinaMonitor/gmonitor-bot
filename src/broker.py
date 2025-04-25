from enum import StrEnum

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from faststream import FastStream
from faststream.kafka import KafkaBroker
from pydantic import BaseModel

from settings import settings


class TopicsEnum(StrEnum):
    GPT_BOT_RESULT = "gpt_bot_result"
    GPT_BOT_REQUEST = "gpt_bot_request"


class GptResponse(BaseModel):
    chat_id: int
    text: str


broker = KafkaBroker(f"{settings.kafka_host}:{settings.kafka_port}")
bot = Bot(
    token=settings.api_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
app = FastStream(broker)


@broker.subscriber(TopicsEnum.GPT_BOT_RESULT)  # type: ignore
async def wait_gpt_response(gpt_response: GptResponse) -> None:
    await bot.send_message(gpt_response.chat_id, gpt_response.text)

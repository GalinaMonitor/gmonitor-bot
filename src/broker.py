from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from faststream import FastStream
from faststream.kafka import KafkaBroker
from gmonitor_lib.schemas import GptResponse, TopicsEnum

from settings import settings

broker = KafkaBroker(f"{settings.kafka_host}:{settings.kafka_port}")
bot = Bot(
    token=settings.api_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)
app = FastStream(broker)


@broker.subscriber(TopicsEnum.GPT_BOT_RESULT)  # type: ignore
async def wait_gpt_response(response: GptResponse) -> None:
    from src.services import MessageService

    try:
        await MessageService().process_message(response)
    except TelegramBadRequest:
        await bot.send_message(
            response.chat_id,
            "Нейронка вернула какой-то странный формат ответа.\n"
            "Попробуй переформулировать запрос.",
        )
    except Exception:
        await bot.send_message(response.chat_id, "Что-то поломалось.")

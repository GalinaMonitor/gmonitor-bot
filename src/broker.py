import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from faststream import FastStream
from faststream.kafka import KafkaBroker
from gmonitor_lib.schemas import GptDto, TopicsEnum

from settings import settings

logger = logging.getLogger(__name__)

broker = KafkaBroker(f"{settings.kafka_host}:{settings.kafka_port}")
bot = Bot(
    token=settings.api_token,
    default=DefaultBotProperties(),
)
app = FastStream(broker)


@broker.subscriber(TopicsEnum.GPT_BOT_RESULT)  # type: ignore
async def wait_gpt_response(response: GptDto) -> None:
    from services import MessageService

    try:
        await MessageService().process_reply_message(response)
    except TelegramBadRequest as e:
        logger.error(f"Нейронка вернула ответ, который не смог обработать тг: {e.message}")
        await bot.send_message(
            response.chat_id,
            "Нейронка вернула какой-то странный формат ответа.\n"
            "Попробуй переформулировать запрос.",
        )
    except Exception:
        await bot.send_message(response.chat_id, "Что-то поломалось.")

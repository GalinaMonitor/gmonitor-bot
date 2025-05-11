import logging

from aiogram.enums import ContentType
from aiogram.types import Message
from gmonitor_lib.schemas import GptDtoType, GptDto, TopicsEnum

from broker import bot, broker
from parsers import TextParser, AudioParser

logger = logging.getLogger(__name__)


class MessageService:
    async def process_reply_message(self, response: GptDto) -> None:
        """Обработка ответа от нейросети"""
        if response.type == GptDtoType.IMAGE:
            await bot.send_photo(response.chat_id, photo=response.content)
        else:
            await bot.send_message(response.chat_id, response.content)

    async def process_income_message(self, message: Message) -> None:
        """Обработка сообщения из тг"""
        if message.content_type == ContentType.TEXT:
            dto = await TextParser().process_request(message)
        elif message.content_type == ContentType.VOICE:
            dto = await AudioParser().process_request(message)
        else:
            raise Exception
        await broker.connect()
        await broker.publish(
            dto,
            TopicsEnum.GPT_BOT_REQUEST,
        )

from abc import ABC, abstractmethod

from aiogram.types import Message
from gmonitor_lib.clients import AWSClient
from gmonitor_lib.schemas import GptDto, GptDtoType

from broker import bot


class BaseParser(ABC):
    @abstractmethod
    async def process_request(self, message: Message) -> GptDto: ...


class AudioParser(BaseParser):
    async def process_request(self, message: Message) -> GptDto:
        voice_filename = f"{message.voice.file_id}.mp3"
        file_path = (await bot.get_file(message.voice.file_id)).file_path
        file = await bot.download_file(file_path)
        s3_link = AWSClient().upload_file(file, voice_filename)
        return GptDto(chat_id=message.chat.id, content=s3_link, type=GptDtoType.AUDIO)


class TextParser(BaseParser):
    async def process_request(self, message: Message) -> GptDto:
        return GptDto(chat_id=message.chat.id, content=message.text)

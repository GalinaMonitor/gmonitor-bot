from gmonitor_lib.schemas import GptResponse, GptResponseType

from src.broker import bot


class MessageService:
    async def process_message(self, response: GptResponse) -> None:
        if response.type == GptResponseType.IMAGE:
            await bot.send_photo(response.chat_id, photo=response.text)
        else:
            await bot.send_message(response.chat_id, response.text)

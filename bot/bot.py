from typing import Optional
from aiogram import Bot, Dispatcher

from bot.data_types import ReplyMarkupType


# Dominoes Poker
class DPBot(Bot):
    def __init__(self, token: str) -> None:
        super().__init__(token)
        self._dispatcher: Dispatcher = None

    @property
    def dispatcher(self) -> Dispatcher:
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, dispatcher: Dispatcher) -> None:
        self._dispatcher = dispatcher

    async def send(self,
                   chat_id: int,
                   text: str,
                   reply_markup: Optional[ReplyMarkupType] = None):
        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown',
        )

    async def start_polling(self):
        if not self.dispatcher:
            raise RuntimeError('Dispatcher was not added to the bot')
        return await self.dispatcher.start_polling(self)

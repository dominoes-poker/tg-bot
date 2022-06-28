from typing import Optional
from aiogram import Bot as bot, Dispatcher

from bot.types import ReplyMarkupType, ReplyKeyboardRemove

# Dominoes Poker
class DPBot(bot):
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
                   reply_markup: Optional[ReplyMarkupType] = ReplyKeyboardRemove):
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

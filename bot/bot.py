from typing import Optional, Union
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

REPLY_MARKUP_TYPE = Union[ReplyKeyboardMarkup, ReplyKeyboardRemove]

class TGBot(Bot):
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
                   reply_markup: Optional[REPLY_MARKUP_TYPE] = ReplyKeyboardRemove,):
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


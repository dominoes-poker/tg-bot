from aiogram import Router
from aiogram.types import TelegramObject, Message
from aiogram.dispatcher.fsm.context import FSMContext

from bot.types import EventCallbackType, IncommingMessage, IncommingMessageWrapper


class TGRouter(Router):

    @staticmethod
    def create_message(tg_object: TelegramObject) -> IncommingMessage:
        if isinstance(tg_object, Message):
            return IncommingMessageWrapper(tg_object=tg_object)
        raise TypeError

    def handler(self, event_callback: EventCallbackType):
        async def callback(tg_object: TelegramObject, state: FSMContext):
            message = self.create_message(tg_object)
            return await event_callback(message, state)
        return callback

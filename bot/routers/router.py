from typing import Callable
from aiogram import Router
from aiogram.types import TelegramObject, Message
from aiogram.dispatcher.fsm.context import FSMContext

from bot.services.context_service.factory import create_context_service
from bot.types import IncommingMessage, IncommingMessageWrapper


class TGRouter(Router):

    @staticmethod
    def create_message(tg_object: TelegramObject) -> IncommingMessage:
        if isinstance(tg_object, Message):
            return IncommingMessageWrapper(tg_object=tg_object)
        raise TypeError

    def handler(self, event_callback: Callable[[Message, FSMContext], None]):
        async def callback(tg_object: TelegramObject, state: FSMContext):
            message = self.create_message(tg_object)
            context_service = create_context_service(state)
            return await event_callback(message, context_service)
        return callback

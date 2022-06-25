from enum import Enum
from typing import Any, Callable, Dict, Optional

from aiogram import Router
from aiogram.dispatcher.event.telegram import FilterType, TelegramEventObserver
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State
from aiogram.types import Message, TelegramObject
from bot.services.context_service.factory import create_context_service
from bot.types import IncommingMessage, IncommingMessageWrapper


class EventType(Enum):
    MESSAGE = 'message'

class TGRouter(Router):

    @staticmethod
    def create_message(tg_object: TelegramObject) -> IncommingMessage:
        if isinstance(tg_object, Message):
            return IncommingMessageWrapper(tg_object=tg_object)
        raise TypeError

    def _get_observer_by_event_type(self, event_type: EventType) -> TelegramEventObserver:
        if event_type == EventType.MESSAGE:
            return self.message
        raise ValueError(f'Event type {event_type} is not supported')

    def setup_handler(self, event_callback: Callable[[Message, FSMContext], State],
                      *filters: FilterType,
                      event_type: EventType = EventType.MESSAGE,
                      flags: Optional[Dict[str, Any]] = None,
                      **bound_filters: Any,
                      ):

        async def callback(tg_object: TelegramObject, state: FSMContext):
            message = self.create_message(tg_object)
            context_service = create_context_service(state)

            state = await event_callback(message, context_service)

            if isinstance(state, State):
                await context_service.set_state(state)

        observer = self._get_observer_by_event_type(event_type)
        observer.register(callback, *filters, flags=flags, **bound_filters)

        return callback

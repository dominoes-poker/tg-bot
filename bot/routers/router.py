from enum import Enum
from typing import Any, Callable, Dict, Optional

from aiogram import Router
from aiogram.dispatcher.event.telegram import FilterType, TelegramEventObserver
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State
from aiogram.types import Message, TelegramObject
from bot.services.context_service.factory import create_context_service
from bot.data_types import IncomingMessage, IncomingMessageWrapper


class EventType(Enum):
    MESSAGE = 'message'


CallbackType = Callable[[Message, FSMContext], State]


class DPRouter(Router):

    @staticmethod
    def create_message(tg_object: TelegramObject) -> IncomingMessage:
        if isinstance(tg_object, Message):
            return IncomingMessageWrapper(tg_object=tg_object)
        raise TypeError

    def _get_observer_by_event_type(self, event_type: EventType) -> TelegramEventObserver:
        if event_type == EventType.MESSAGE:
            return self.message
        raise ValueError(f'Event type {event_type} is not supported')

    def setup_handler(self, event_callback: CallbackType,
                      *filters: FilterType,
                      event_type: EventType = EventType.MESSAGE,
                      flags: Optional[Dict[str, Any]] = None,
                      **bound_filters: Any,
                      ) -> CallbackType:

        async def callback(tg_object: TelegramObject, state: FSMContext):
            message = self.create_message(tg_object)
            context_service = create_context_service(state)

            state = await event_callback(message, context_service)

            if state and isinstance(state, State):
                await context_service.set_state(state)

        observer = self._get_observer_by_event_type(event_type)
        observer.register(callback, *filters, flags=flags, **bound_filters)

        return callback

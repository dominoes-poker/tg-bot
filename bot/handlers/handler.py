from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

class Handler:
    
    async def handle(self, message: Message, state: FSMContext) -> None:
        raise NotImplementedError

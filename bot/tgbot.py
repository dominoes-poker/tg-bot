from aiogram import Bot, Dispatcher


class TGBot:
    def __init__(self, token, dispatcher: Dispatcher) -> None:
        self._bot = Bot(token=token)
        self._dispatcher = dispatcher

    async def polling(self) -> None:
        return await self._dispatcher.start_polling(self._bot)

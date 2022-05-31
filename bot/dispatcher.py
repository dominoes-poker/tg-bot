from aiogram import Dispatcher

from bot.bot import TGBot

class TGDispatcher(Dispatcher):
    def __init__(self, bot: TGBot) -> None:
        super().__init__()
        self._bot = bot

    @property
    def bot(self) -> TGBot:
        return self._bot

    async def polling(self) -> None:
        return await self.start_polling(self._bot)

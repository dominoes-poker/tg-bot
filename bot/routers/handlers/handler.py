
from bot.bot import TGBot
from bot.dispatcher import TGDispatcher


class Handler:
    def __init__(self, dispatcher: TGDispatcher) -> None:
        self._dispatcher = dispatcher

    @property
    def bot(self) -> TGBot:
        return self._dispatcher.bot
from bot.bot import TGBot


class Handler:
    def __init__(self, bot: TGBot) -> None:
        self._bot = bot

    @property
    def bot(self) -> TGBot:
        return self._bot
from bot.bot import DPBot


class Handler:
    def __init__(self, bot: DPBot) -> None:
        self._bot = bot

    @property
    def bot(self) -> DPBot:
        return self._bot

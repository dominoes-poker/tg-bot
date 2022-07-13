from bot.bot import DPBot
from bot.messages.service import MessageService


class Handler:
    def __init__(self, bot: DPBot, message_service: MessageService = None) -> None:
        self._bot = bot
        self._message_service = message_service

    @property
    def bot(self) -> DPBot:
        return self._bot

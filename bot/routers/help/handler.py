
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.types import IncommingMessage


class HelpHandler(Handler):

    async def help_handler(self, message: IncommingMessage, _: ContextService) -> None:
        return await self.root_help(message.user_id)

    async def root_help(self, chat_id: int) -> None:
        message = 'The bot helps you manage Dominoes Poker game.'
        return await self.bot.send(
            chat_id=chat_id,
            text=message
        )

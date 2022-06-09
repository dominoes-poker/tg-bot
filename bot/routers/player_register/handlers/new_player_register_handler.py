from bot.routers.player_register.handlers.player_register_handler import PlayerRegisterHandler
from bot.services.context_service import ContextService
from bot.states import NewPlayerRegisterState
from bot.types import IncommingMessage


class NewPlayerRegisterHandler(PlayerRegisterHandler):
    async def ask_username(self, message: IncommingMessage, context_service: ContextService) -> None:
        await super().ask_username(message, context_service)
        return await context_service.set_state(NewPlayerRegisterState.WAIT_USERNAME)

    async def handle_username(self, message: IncommingMessage, context_service: ContextService) -> None:
        username = message.text
        if not self._allow_username_pattern.match(username):
            return await self._bad_username_response(message.user_id)
        
        await self._register_player(message.user_id, None, username, context_service)

    @staticmethod
    def _get_final_message(username: str) -> str:
        return f'Congratulations! We have registrated a new player - `{username}`! What do you want next?'
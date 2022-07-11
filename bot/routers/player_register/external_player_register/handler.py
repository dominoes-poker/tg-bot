from bot.routers.player_register.handler import \
    PlayerRegisterHandler
from bot.services.context_service import ContextService
from bot.states import ExternalPlayerRegisterState
from bot.data_types import IncomingMessage


class ExternalPlayerRegisterHandler(PlayerRegisterHandler):
    async def ask_username(self, message: IncomingMessage,
                           context_service: ContextService) -> None:
        await super().ask_username(message, context_service)
        return ExternalPlayerRegisterState.WAIT_USERNAME

    async def handle_username(self, message: IncomingMessage,
                              _: ContextService) -> None:
        username = message.text
        if not self._allow_username_pattern.match(username):
            return await self._bad_username_response(message.user_id)

        return await self._register_player(message.user_id, None, username)

    @staticmethod
    def _get_final_message(username: str) -> str:
        return f'Congratulations! We have registrated a new player - `{username}`! ' \
                'What do you want next?'

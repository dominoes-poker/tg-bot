from bot.bot import DPBot
from bot.routers.common.keyboards import KEYBOARD_ON_HOLD
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.states import GameState
from bot.types import IncommingMessage


class FinishGameHandler(Handler):
    def __init__(self, bot: DPBot, game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def finish(self, message: IncommingMessage, context_service: ContextService) -> None:

        game_id = await context_service.get_current_game_id()
        await self._game_data_service.finish(game_id)

        await self.bot.send(
            chat_id=message.user_id,
            text='Hope, it was wonderful for you as for me!',
            reply_markup=KEYBOARD_ON_HOLD
        )
        return GameState.WAIT_PLAYER_USERNAMES

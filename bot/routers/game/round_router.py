from aiogram import F
from bot.bot import TGBot
from bot.routers.game.handlers import CreateGameHandler
from bot.routers.game.handlers.round_handler import RoundHandler
from bot.routers.handlers.common.keyboards import BUTTON_NEW_GAME

from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import GameState, RootState


class RoundRouter(TGRouter):
    def __init__(self, handler: RoundHandler) -> None:
        super().__init__(use_builtin_filters=True, name='RoundRouter')
        self.setup(handler=handler)

    def setup(self, handler: RoundHandler) -> None:
        self.message.register(self.handler(handler.start_round), GameState.START_ROUND, F.text.regexp(r'Start the \w+ round'))


def create_rpund_router(bot: TGBot,
                        player_data_service: PlayerDataService,
                        game_data_service: GameDataService) -> RoundRouter:
    handler = RoundHandler(bot, player_data_service, game_data_service)
    return RoundRouter(handler)

from aiogram import F
from bot.bot import TGBot
from bot.routers.game.handlers import CreateGameHandler
from bot.routers.handlers.common.keyboards import BUTTON_NEW_GAME

from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import GameState, RootState


class CreateGameRouter(TGRouter):
    def __init__(self, handler: CreateGameHandler) -> None:
        super().__init__(use_builtin_filters=True, name='RootGameRouter')
        self.setup(handler=handler)

    def setup(self, handler: CreateGameHandler) -> None:
        self.setup_handler(handler.ask_player_usernames, RootState.ON_HOLD, F.text == BUTTON_NEW_GAME.text)
        self.setup_handler(handler.handle_player_usernames, GameState.WAIT_PLAYER_USERNAMES)


def create_game_maker_router(bot: TGBot,
                            player_data_service: PlayerDataService,
                            game_data_service: GameDataService) -> CreateGameRouter:
    handler = CreateGameHandler(bot, player_data_service, game_data_service)
    return CreateGameRouter(handler)

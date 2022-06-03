from aiogram import F
from bot.bot import TGBot
from bot.routers.handlers.game_handler import CreateGameHandler

from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.gamer_service import GamerDataService
from bot.states import GameState, RootState


class CreateGameRouter(TGRouter):
    def __init__(self, handler: CreateGameHandler) -> None:
        super().__init__(use_builtin_filters=True, name='RootGameRouter')
        self.setup(handler=handler)

    def setup(self, handler: CreateGameHandler) -> None:
        self.message.register(self.handler(handler.ask_gamer_usernames), 
                              RootState.ON_HOLD, F.text.casefold() == 'start a new game')
        self.message.register(self.handler(handler.handle_gamer_names), 
                              GameState.ADD_GAMERS)        
        self.message.register(self.handler(handler.handle_accept), 
                              GameState.WAIT_ANSWER,  F.text.casefold() == 'yes')


def create_game_maker_router(bot: TGBot,
                            gamer_data_service: GamerDataService,
                            game_data_service: GameDataService) -> CreateGameRouter:
    handler = CreateGameHandler(bot, gamer_data_service, game_data_service)
    return CreateGameRouter(handler)
